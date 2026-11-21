"""Build the owner's board: one read-only HTML page from files.

Reads  board/*.md, board/run-log.md, memory/customers/*.md, memory/carriers.md
Writes board/dashboard.html  (inside board/, which Git ignores)

Standard library only. No network. Run from anywhere:
    python demo-freight-co/dashboard/build_dashboard.py
"""
import html
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # the client folder
BOARD = ROOT / "board"
MEMORY = ROOT / "memory"
OUT = BOARD / "dashboard.html"
RUN_TIME = (7, 46)  # scheduled run, UK time
GRACE = timedelta(minutes=60)
MEMORY_DAYS = 7
CLIENT = "Demo Freight Co"


def esc(value):
    """Every value from a file is untrusted text. Always escape."""
    return html.escape(str(value), quote=True)


def read(path):
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def parse_entry(path):
    head, _, rest = read(path).partition("\n## Draft")
    fields = {}
    for line in head.splitlines()[1:]:
        m = re.match(r"^([A-Za-z ]+): (.*)$", line)
        if m:
            fields[m.group(1).strip()] = m.group(2).strip()
    draft, _, memory = rest.partition("\n## Memory")
    fields["_draft"] = draft.strip()
    fields["_memory"] = memory.strip()
    fields["_file"] = path.name
    return fields


def load_entries():
    entries = []
    for p in sorted(BOARD.glob("*.md")):
        if p.name == "run-log.md":
            continue
        entries.append(parse_entry(p))
    return entries


def load_run_log():
    runs = []
    path = BOARD / "run-log.md"
    if not path.exists():
        return runs
    for line in read(path).splitlines():
        m = re.match(r"^- (\d{1,2} \w{3} \d{4}) (\d{2}:\d{2}): (.*)$", line)
        if m:
            when = datetime.strptime(f"{m.group(1)} {m.group(2)}", "%d %b %Y %H:%M")
            runs.append((when, m.group(3)))
    return runs


def run_has_problem(text):
    m = re.search(r"(\d+) errors?", text)
    if m and int(m.group(1)) > 0:
        return True
    return bool(re.search(r"\b(stopped|failed|problem)\b", text, re.I))


def expected_last_run(now):
    """The most recent weekday run time that should already have happened."""
    day = now.replace(hour=RUN_TIME[0], minute=RUN_TIME[1], second=0, microsecond=0)
    if day + GRACE > now:
        day -= timedelta(days=1)
    while day.weekday() >= 5:
        day -= timedelta(days=1)
    return day


def load_memory_lines(now):
    cutoff = now - timedelta(days=MEMORY_DAYS)
    found = []
    files = sorted((MEMORY / "customers").glob("*.md")) + [MEMORY / "carriers.md"]
    for p in files:
        if not p.exists():
            continue
        text = read(p)
        title = re.search(r"^# (.+)$", text, re.M)
        name = title.group(1).strip() if title else p.stem
        in_log = False
        for line in text.splitlines():
            if line.startswith("## "):
                in_log = line.strip() == "## Log"
                continue
            m = re.match(r"^- (\d{1,2} \w{3} \d{4}): (.*)$", line)
            if in_log and m:
                when = datetime.strptime(m.group(1), "%d %b %Y")
                if when >= cutoff.replace(hour=0, minute=0, second=0, microsecond=0):
                    found.append((when, name, m.group(2)))
    return sorted(found, key=lambda x: x[0], reverse=True)


def card(entry, kind):
    f = entry
    label = {"urgent": "Urgent: needs owner", "owner": "Needs owner", "draft": "Draft: awaiting approval"}[kind]
    notes = f.get("Notes for owner", "none")
    parts = [
        f'<article class="card {kind}">',
        f'<div class="badge {kind}">{esc(label)}</div>',
        f'<h3>{esc(f.get("Summary", f["_file"]))}</h3>',
        f'<p class="meta">{esc(f.get("Customer", "unknown"))} &middot; {esc(f.get("Type", ""))} &middot; Tier {esc(f.get("Tier", "?"))} &middot; {esc(f["_file"])}</p>',
    ]
    if kind != "draft":
        parts.append(f'<p><strong>Why:</strong> {esc(f.get("Needs owner", ""))}</p>')
    if notes and notes.lower() != "none":
        parts.append(f'<p><strong>Notes for owner:</strong> {esc(notes)}</p>')
    missing = f.get("Missing details", "")
    if kind == "draft" and missing and missing.lower() != "none":
        parts.append(f'<p><strong>Missing details we ask for:</strong> {esc(missing)}</p>')
    if kind == "draft":
        parts.append(f'<details><summary>Show draft (not sent)</summary><pre>{esc(f["_draft"])}</pre></details>')
    parts.append("</article>")
    return "\n".join(parts)


def build():
    now = datetime.now()
    entries = load_entries()
    runs = load_run_log()
    mem = load_memory_lines(now)

    urgent = [e for e in entries if e.get("Needs owner", "").lower().startswith("yes") and "urgent" in e.get("Needs owner", "").lower()]
    owner = [e for e in entries if e.get("Needs owner", "").lower().startswith("yes") and e not in urgent]
    drafts = [e for e in entries if e not in urgent and e not in owner and not e["_draft"].lower().startswith("no draft")]

    expected = expected_last_run(now)
    last = runs[-1][0] if runs else None
    if last is None:
        run_state, run_text = "bad", "No runs logged yet"
    elif last < expected:
        run_state = "bad"
        run_text = f"Last run {last:%a %d %b %H:%M}. A run was due {expected:%a %d %b %H:%M}. Check the schedule."
    else:
        run_state = "ok"
        run_text = f"Last run {last:%a %d %b %H:%M}"
    problems = [r for r in runs if run_has_problem(r[1])]

    def section(title, items, empty):
        body = "\n".join(items) if items else f'<p class="empty">{esc(empty)}</p>'
        return f"<section><h2>{esc(title)}</h2>\n{body}\n</section>"

    cards = [card(e, "urgent") for e in urgent] + [card(e, "owner") for e in owner]
    draft_cards = [card(e, "draft") for e in drafts]
    mem_rows = "\n".join(
        f'<li><span class="when">{w:%d %b}</span> <strong>{esc(n)}</strong>: {esc(t)}</li>' for w, n, t in mem
    )
    run_rows = "\n".join(
        f'<li class="{"bad" if run_has_problem(t) else ""}"><span class="when">{w:%d %b %H:%M}</span> {esc(t)}</li>'
        for w, t in reversed(runs[-10:])
    )

    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'">
<title>AI Employee Board</title>
<style>
:root {{
  --bg:#f6f5f1; --panel:#ffffff; --ink:#1f2328; --muted:#5b6470; --line:#dcd9d0;
  --urgent:#b3261e; --urgent-bg:#fdecea; --owner:#8a5a00; --owner-bg:#fff4dc;
  --draft:#1a5fb4; --draft-bg:#e8f0fb; --ok:#1e7a3c; --ok-bg:#e6f4ea;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --bg:#15171a; --panel:#1e2125; --ink:#e8e6e1; --muted:#a3a8b0; --line:#34383e;
    --urgent:#ff8a80; --urgent-bg:#3a1f1d; --owner:#f2c46d; --owner-bg:#3a2f16;
    --draft:#8ab4f8; --draft-bg:#1d2a3d; --ok:#7ddc9b; --ok-bg:#1c3326;
  }}
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink); font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; }}
main {{ max-width:980px; margin:0 auto; padding:24px 16px 48px; }}
header h1 {{ margin:0 0 4px; font-size:1.6rem; }}
header p {{ margin:0; color:var(--muted); }}
.demo {{ display:inline-block; margin-top:8px; padding:2px 10px; border:1px solid var(--line); border-radius:999px; font-size:.8rem; color:var(--muted); }}
.strip {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:12px; margin:20px 0 8px; }}
.tile {{ background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:12px 14px; }}
.tile .n {{ font-size:1.8rem; font-weight:650; line-height:1.1; }}
.tile .l {{ color:var(--muted); font-size:.85rem; }}
.tile.ok {{ background:var(--ok-bg); }} .tile.bad {{ background:var(--urgent-bg); }}
.tile .t {{ font-weight:600; }}
section {{ margin-top:28px; }}
h2 {{ font-size:1.1rem; margin:0 0 10px; }}
.card {{ background:var(--panel); border:1px solid var(--line); border-left-width:5px; border-radius:10px; padding:12px 16px; margin-bottom:12px; }}
.card.urgent {{ border-left-color:var(--urgent); }} .card.owner {{ border-left-color:var(--owner); }} .card.draft {{ border-left-color:var(--draft); }}
.card h3 {{ margin:6px 0 2px; font-size:1.02rem; }}
.card p {{ margin:6px 0; }}
.meta {{ color:var(--muted); font-size:.85rem; }}
.badge {{ display:inline-block; font-size:.75rem; font-weight:650; padding:2px 8px; border-radius:6px; }}
.badge.urgent {{ color:var(--urgent); background:var(--urgent-bg); }}
.badge.owner {{ color:var(--owner); background:var(--owner-bg); }}
.badge.draft {{ color:var(--draft); background:var(--draft-bg); }}
details {{ margin-top:8px; }} summary {{ cursor:pointer; color:var(--draft); font-weight:550; }}
pre {{ white-space:pre-wrap; background:var(--bg); border:1px solid var(--line); border-radius:8px; padding:12px; font:inherit; font-size:.92rem; }}
ul {{ list-style:none; margin:0; padding:0; }}
li {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:8px 12px; margin-bottom:6px; }}
li.bad {{ border-color:var(--urgent); }}
.when {{ color:var(--muted); font-variant-numeric:tabular-nums; margin-right:6px; }}
.empty {{ color:var(--muted); background:var(--panel); border:1px dashed var(--line); border-radius:8px; padding:10px 12px; }}
footer {{ margin-top:32px; color:var(--muted); font-size:.85rem; }}
</style>
</head>
<body>
<main>
<header>
  <h1>{esc(CLIENT)}: AI employee board</h1>
  <p>Built {now:%a %d %b %Y, %H:%M}. Read-only. Nothing here can send or approve anything.</p>
  <span class="demo">Demo data only</span>
</header>

<div class="strip">
  <div class="tile {'bad' if urgent else ''}"><div class="n">{len(urgent)}</div><div class="l">Urgent, needs you</div></div>
  <div class="tile"><div class="n">{len(owner)}</div><div class="l">Other items needing you</div></div>
  <div class="tile"><div class="n">{len(drafts)}</div><div class="l">Drafts awaiting approval</div></div>
  <div class="tile {run_state}"><div class="t">{'Schedule OK' if run_state == 'ok' else 'Schedule warning'}</div><div class="l">{esc(run_text)}</div></div>
  <div class="tile {'bad' if problems else ''}"><div class="n">{len(problems)}</div><div class="l">Runs with problems</div></div>
</div>

{section("Needs you (urgent first)", cards, "Nothing needs you right now.")}
{section("Drafts awaiting your approval", draft_cards, "No drafts waiting.")}
{section(f"New memory lines, last {MEMORY_DAYS} days (your weekly skim)", [f"<ul>{mem_rows}</ul>"] if mem else [], "No new memory lines.")}
{section("Recent runs", [f"<ul>{run_rows}</ul>"] if runs else [], "No runs logged yet.")}

<footer>Generated from board/ and memory/ by build_dashboard.py. Never commit or share this file: it holds customer information.</footer>
</main>
</body>
</html>
"""


if __name__ == "__main__":
    if not BOARD.exists():
        sys.exit(f"No board folder at {BOARD}")
    OUT.write_text(build(), encoding="utf-8")
    print(f"Wrote {OUT}")
