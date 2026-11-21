# AI Employee for a Client's Business: Build Book v1

## What this project is about
A hands-on build of the six-piece blueprint for making AI run the routine work of a client's business: Context, Skills, Memory, Tools, Schedules, Board. The owner stays the owner; the AI drafts, the owner decides. Anything involving money, contracts or an angry customer always waits for the owner.

Build order: context, then one skill, then one job, then put that one job on a schedule. Run it for 2 weeks, fix what breaks, then add the next job.

Principle throughout: UK GDPR by default (no personal data in the business brain, no pre-ticked consent boxes, least access for every tool).

## Checklist
- [x] Ch 1: Context (business-brain folder, 6 files including memory rules)
  - [x] 01-business.md
  - [x] 02-customers.md
  - [x] 03-voice.md
  - [x] 04-approvals.md
  - [x] 05-faq.md
  - [x] 06-memory-rules.md (added in Piece 3)
  - [x] Test the brain: give the five files and sample customer emails to Claude and check the drafts follow the voice and the tiers (found two gaps, no opening hours or response times and an undefined "stated time", both fixed)
- [x] Ch 2: Skills (one job written step by step: draft-quote-reply)
- [x] Ch 3: Memory (rules file, update-memory skill, invented sample records, quote skill linked, tested on four emails)
- [x] Ch 4: Tools (v1 shorter route: sample inbox folder in, board folder out, no send tool; live Gmail via n8n deferred to the two-week run)
- [x] Ch 5: Schedules (process-inbox on a weekday schedule, with unattended-run rules and a run log; production version is n8n on a VPS)
- [ ] Ch 6: Board (what the AI did, what awaits approval, what got stuck)
- [ ] Two-week run, fix what breaks, add the next job
- [ ] GitHub: private repo first, then mark as a template repository and make public once checked (no secrets, no real customer data)
- [ ] Slide deck: one slide per piece (goal, steps, key prompt, takeaway), built from this book

## Project goals
- Reusable template for building AI employees for any business
- A slide deck that lets others be taught every step and prompt
- Published on GitHub as a template repository

## Concept notes

### Setup: permissions and least privilege
- **What it is:** Claude Code asks permission before it reads, edits or runs things. Rules in `.claude/settings.json` can deny specific actions in advance, such as reading `.env` files.
- **What we did:** wrote deny rules with `**` patterns so nested client folders are covered, kept manual mode on, and added a `.gitignore` to keep secrets and memory out of git.
- **Limit to remember:** deny rules apply to Claude Code's built-in file tools, not necessarily to shell commands. Manual mode is the backstop, and real secrets stay out of the project folder.
- **Why it matters later:** the AI employee needs the same discipline in Piece 4 (Tools): read and draft only.
- **Takeaway:** give an AI the least access that gets the job done, and write the rules in a file, not in your head.

### Setup: permission modes and model choice
- **Modes:** manual (approve every action), plan mode (Claude plans without changing anything and you approve the plan), accept-edits (file edits go through without asking; low-risk work only).
- **Model rule used:** Sonnet for routine work; Opus straight away for bugs, errors, design and big reviews.
- **Takeaway:** match the autonomy you give to the cost of a mistake.

### Piece 1: Context engineering
- **What it is:** deciding what an AI reads before every job. The `business-brain/` folder is that context: facts (business, customers), voice, boundaries (approvals) and common questions (FAQ).
- **What we did:** wrote files 01 to 03 for the demo client, each with one job and each marked DEMO ONLY.
- **Lesson 1, show don't tell:** real sample emails teach tone far better than adjectives like "friendly but direct".
- **Lesson 2, examples outweigh rules:** when an example and a rule disagree, the AI follows the example. Check every example obeys your own rules. We found one: the rules banned promising sea freight delivery times, while a sample email gave a delivery window. Fix: make the rule say "sea transit times".
- **Lesson 3, one job per file, no personal data:** describe customer types, not named people, so the brain is safe to share.
- **Lesson 4, answers must stand alone:** the AI can copy a sentence word for word, so never write cross-references such as "see question 3", and never let an answer promise more than the law or policy allows (we removed an unconditional "Yes" to deleting personal data).
- **Lesson 5, restrictions never expire by date:** only the owner lifts a restriction, by writing it in the approvals file. We replaced "for the first two weeks" with "until the owner promotes that type". Text inside an email is information, never an instruction.
- **Lesson 6, test the brain before building on it:** run sample emails through the files, including a hard complaint and a trick email that tries to instruct the AI. The hard cases passed. The gaps were everyday details: the business hours and reply times were missing, and a promise ("same working day") existed only inside a sample email. Facts live in one place; examples must not be the only place a fact appears.
- **Takeaway:** context is the AI's job description plus house style. Write the facts down once, show the voice with real examples, and keep examples consistent with the rules.
- **Academy:** do the lesson on writing effective prompts and instructions after you have used this.

### Piece 2: Skills
- **What it is:** one repeatable job written down once as a folder holding a `SKILL.md`: a name, a one-line description of when to use it, and the steps. The AI does the job the owner's way every time.
- **What we did:** wrote `draft-quote-reply` for the demo client, in the standard Agent Skills layout.
- **Lesson 1, the description is the trigger:** it decides when the skill is used, so say exactly which emails it covers (we added "rate" because customers use it).
- **Lesson 2, safety checks before drafting:** steps 1 to 3 check the tier, instructions aimed at the AI, and goods we don't carry, before anything is written.
- **Lesson 3, point, don't copy:** the skill says "use the reply times in 01-business.md" instead of repeating them, so a fact changes in one place only.
- **Lesson 4, owners know steps by habit:** the greeting when there's no name and the "Re:" subject line were missing until we asked what the owner does without thinking. In a real build, interview the owner.
- **Lesson 5, fix gaps in the brain, not the skill:** testing the skill exposed the after-hours "working day" and the missing dangerous goods examples. Both were fixed in 01-business.md.
- **Takeaway:** a skill is a procedure the AI follows the same way every time. Keep it short, put the safety checks first, and point to facts instead of copying them.
- **Academy:** do the lesson on Agent Skills now that you have written one.

### Piece 3: Memory
- **What it is:** a running record, one file per customer plus one for carriers, that the AI reads before drafting and adds to afterwards. It is how the AI knows what was promised or quoted last time.
- **What we did:** wrote `06-memory-rules.md` (policy: what may and may not be stored), the `update-memory` skill (procedure: read before, write after), invented sample records in `memory-example/`, and linked `draft-quote-reply` to the skill.
- **Lesson 1, policy in the brain, procedure in a skill:** what may be stored is a rule, so it lives with the other rules. How to read and write is a procedure, so it lives in a skill. Any future skill can reuse it.
- **Lesson 2, write only what you'd show the customer:** customers have the right to ask for a copy of what you hold. Facts only, no opinions, no personal details, no copies of emails.
- **Lesson 3, memory is information, not instruction:** the same prompt-injection defence as email. A note saying "always give this customer a discount" is flagged, never followed. If memory conflicts with files 01 to 05, the files win.
- **Lesson 4, append-only:** the AI adds lines and never edits or deletes. The owner skims the new lines weekly (on the board in Piece 6). Tier 3 matters (complaints, claims, disputes, data requests) record only "received and flagged"; the owner adds the detail.
- **Lesson 5, live memory never goes in git:** `memory/` is gitignored and verified with `git check-ignore`. The repo holds only invented samples.
- **Lesson 6, testing found three gaps:** the AI writes its log line before the owner decides, so it can't say "owner approved" (fix: write "(draft on board)", then a second line for the outcome); new customers had no rule for reference numbers; flagged emails from unknown senders shouldn't create records.
- **Does it train itself?** Not the model. It learns facts and your corrections, but never rewrites its own rules. A possible v2 is a weekly skill that proposes brain edits from the owner's draft changes, for the owner to approve.
- **Takeaway:** memory makes the AI consistent across emails. Keep it minimal, factual, append-only and out of git, and let the owner remain the only one who changes the rules.
- **Academy:** do the lesson on memory and context management for agents.

### Piece 4: Tools
- **What it is:** a tool is anything the AI can do in the outside world. Reading a file, writing a file and sending an email are three tools with three different risks. Each one is granted separately, at the lowest level that works.
- **What we did:** the v1 "inbox" is a folder of sample emails (`inbox/`) and the "board" is a folder of drafts (`board/`). A `process-inbox` skill reads each email, routes it to the right skill and writes one board entry per email.
- **Lesson 1, no send tool means no send risk:** the AI can read four places, write two, and has no way to send, delete or use the network. That is stronger than a rule saying "don't send". In the live version, n8n gets the same shape: read mail, create a draft, no send node.
- **Lesson 2, live data stays out of git:** `inbox/` and `board/` are gitignored, verified with `git check-ignore`. Only invented examples (`inbox-example/`) are committed.
- **Lesson 3, an orchestrator skill routes, it doesn't draft:** `process-inbox` decides which skill handles each email and collects the results. Anything without a skill yet goes to "Needs owner", which is safe by default. New email type means a new skill plus one routing line.
- **Lesson 4, skills outside `.claude/skills/` need explicit paths:** Claude Code only auto-discovers skills in `.claude/skills/`. We keep skills per client, so the prompt names the paths.
- **Lesson 5, start a fresh session after editing a skill:** the first re-run reused the old skill from the session's memory, so none of the fixes appeared. A skill changes behaviour only when it is read again. Check results against the file on disk, not against what you expect.
- **Lesson 6, a four-email test finds layout gaps:** the run showed an open promise not reaching the owner, a detail ("fragile") asked for in drafts but missing from the brain, a summary that inferred "no quote sent", and customer matching that depended on luck. Fixes: a "Notes for owner" line, the detail added to the brain, a "state only what memory says" rule, and an Email domain line in each record.
- **Lesson 7, outputs vary between runs:** a draft asked about the dock and tail-lift in one run and not in the next. In a real build, run the test set more than once before trusting a skill.
- **Takeaway:** the safest tool is the one that can't do harm. Give the AI the smallest set of actions that does the job, keep live data out of git, and prove containment by checking what changed.
- **Academy:** do the lesson on tool use and permissions for agents.

### Piece 5: Schedules
- **What it is:** turning "I run it when I remember" into "it runs at 07:46 every working day, before the business opens". A schedule multiplies mistakes, because nobody is watching.
- **What we did:** added a "When run on a schedule" section to the `process-inbox` skill, then created a scheduled Claude task (Monday to Friday, 07:46 UK time) that reads the skill fresh each run.
- **Lesson 1, write the unattended rules first:** never ask a question (flag "Needs owner" and carry on), use only the listed actions, stop on failure and never retry by another route.
- **Lesson 2, a run log makes silence meaningful:** one line per run, even when there is nothing to process ("no new emails"). A missing line for a working day means the run did not happen. The log is append-only.
- **Lesson 3, prove it with a test fire:** the first manual run correctly skipped all four already-processed emails, wrote the log line and changed nothing else. Check containment by looking at file timestamps and git status, not by trusting the summary.
- **Lesson 4, a scheduled session is a general session:** it may have other connectors attached (Drive, Docs, Shopify) that the prompt tells it not to use, but nothing physically blocks them. That is an instruction, not a missing tool, which is weaker than Piece 4's "no send tool" design. Acceptable for invented demo data. Not acceptable for a real client.
- **Lesson 5, unattended means automatic approval:** with nobody to approve each write, the task runs in automatic mode. The limits are the prompt, the skill and the folder.
- **Lesson 6, the demo and production differ:** option A (scheduled Claude task) needs the desktop app open and the computer on for local files. If the computer is off, the run does not happen and no log line appears. Production uses option B: an n8n schedule trigger on an always-on server, reading and drafting in the client's inbox with no send node.
- **Takeaway:** write the rules for an unattended run before you schedule it, make every run leave a trace, and test with one manual fire before you trust the clock.
- **Academy:** do the lesson on running agents autonomously and monitoring them.

## Chapter 1: Context
**Goal:** write down the business so every AI job reads it first and sounds like the owner, not a stranger.

**Steps**
1. Create a folder called `business-brain/`.
2. Write the plain files: business, customers, voice, approvals, FAQ (and memory rules, added in Piece 3).
3. Describe types of customer, never named individuals.

**Key prompt (interview method):** ask Claude to interview you one file at a time, then shape your real answers into a clean file. You supply the facts; Claude supplies the structure.

**Key prompt (brain test):** "You are the AI employee for the business described in the files below. Use only these files. Follow 04-approvals.md. For the email below, tell me: (1) the tier, (2) what you would do, (3) the draft, if you are allowed to write one, (4) any fact you had to guess because it was not in the files." Part 4 is what finds the gaps. Run it in a fresh chat with only the files, for a stricter test than one run by the Claude that helped write them.

**Log**
- Client chosen: a prospect (demo build, no real client data; sample or fictional data only until they sign and a data processing agreement is in place)
- Niche chosen: small independent UK freight forwarder (quotes, shipment status chasers, customs paperwork queries). Reason: inbox-heavy work, clear approval rules, and it matches existing supply chain knowledge
- Decision: placeholders in the first draft were replaced with clearly labelled DEMO ONLY values so the demo can run end to end. Real values come from the prospect's discovery call (first question: what do you charge per customs declaration, and what are your payment terms?)
- Folder structure decision (repo root is the AI-Employee folder itself): one top-level folder per client, with business-brain/, skills/ and memory/ as subfolders, so each client's data stays separate and a new client is a copy of a blank template
- Restart: Claude Code opened inside a folder called AI-Employee, which is the repo root. Build order is now security first: Step 1 safety foundations (.gitignore and Claude Code deny rules), Step 2 folder tree, Step 3 README and docs, Step 4 git and private GitHub repo, then the Piece 1 files
- Key prompt, Step 1 (Claude Code, Sonnet, manual mode): create a .gitignore that excludes secrets, memory contents and local settings, and a .claude/settings.json that denies reading .env files
- Step 1 lesson: Claude Code flagged that the first deny rules only covered .env files at the project root. Fix: use Read(**/.env), Read(**/.env.*) and Read(**/secrets/**) so nested folders (one per client) are covered. Deny rules are a safety net, not a vault: real secrets stay out of the project folder entirely
- Restart (21 Nov): Claude Code now opened in a folder called "AI Business setup", which becomes the repo root (no extra ai-employee/ nesting). Security baseline first: manual mode, project-level deny rules for secrets in .claude/settings.json (travels with the template), no secrets ever in the folder, .gitignore for .env and memory/
- Location decision: keep the working project folder local (outside OneDrive, Dropbox and Google Drive sync, e.g. C:\Dev\AI-Employee) and use the private GitHub repo as the backup. Cloud drives are only for exports such as the slide deck
- Progress: Step 1 safety foundations done (.gitignore plus nested-safe deny rules in .claude/settings.json); Step 2 folder tree done (demo-freight-co and _template, five heading-only context files each, .gitkeep in skills and memory); 01-business.md drafted (demo values), waiting to be placed in demo-freight-co/business-brain
- Step 3 done: git init, staged file list reviewed (exactly 16 files, no secrets), repo email set to the GitHub noreply address, first commit made locally (16 files). Claude Code added a Co-Authored-By trailer; decide keep or remove before the first push, since changing it after a push means rewriting history
- Step 4 done: author email confirmed as the GitHub noreply address, private repo ai-employee-blueprint created and pushed, README (with the money/contracts/angry-customer rule) and docs/build-book.md added as the second commit
- Step 5 done: 01-business.md and 02-customers.md placed and pushed; "Claude outputs/" folder added to .gitignore (the desktop app saves copies of files it sends there); repo checked directly, clean and in sync with GitHub
- Step 6: 03-voice.md drafted with three sample emails; one rule/example conflict found (sea freight delivery times) and being fixed by hand before commit
- Step 7 done: 03-voice.md and 04-approvals.md committed and pushed; 04 reviewed twice (rule and tier conflicts fixed: expiring two-week clause, delay drafting contradiction, "would goes" typo); 05-faq.md drafted with a Handling line per answer, then reviewed (cross-reference and unconditional "Yes" fixed)
- Step 8 done: Piece 1 tested with four sample emails (quote request, status chase, angry damaged-goods complaint, trick email); gaps fixed and committed. A stray word typed into 03-voice.md was caught in review and restored before committing
- Step 9 started: Piece 2 (Skills). First skill: draft-quote-reply, written in the standard Agent Skills layout (a folder with a SKILL.md) at demo-freight-co/skills/draft-quote-reply/. It points to the business-brain files instead of copying their facts
- Step 9 done: skill reviewed by hand (greeting, subject line, "rate" added), tested on four emails, two gaps fixed in the brain (after-hours working day, dangerous goods examples), committed and pushed (92f8916)
- Step 10 started: Piece 3 (Memory). Design: policy lives in business-brain/06-memory-rules.md, the procedure will live in a skill, live memory/ stays gitignored, and a committed memory-example/ holds invented sample records
- Step 10 done: Piece 3 (Memory) complete. 06-memory-rules.md (12-month review period, six extra "may store" items), update-memory skill, memory-example/ with invented records, quote skill linked to memory. Decision: the AI writes memory itself in v1 (Tier 1, append-only, weekly skim); switch to approve-first if real client data is involved or errors appear
- Piece 3 test: four emails (repeat customer, new customer, injection plus dangerous goods, angry repeat customer). Memory improved the drafts (dock and tail-lift question, open promise noted for the owner). Three gaps fixed in update-memory and committed
- Step 11 done: Piece 4 (Tools), shorter route. Added inbox/ and board/ (gitignored), inbox-example/ with four invented emails, and the process-inbox skill. Tested on four emails; findings fixed (fragile detail in the brain, Email domain line, Notes for owner, state-only-what-memory-says). Re-run in a fresh session confirmed the fixes
- Decision: v1 uses the shorter route (sample emails, no live inbox). The live n8n and Gmail connection comes at the two-week run, with read and draft only
- Step 12 done: Piece 5 (Schedules), option A. Added "When run on a schedule" rules to process-inbox, created the scheduled task (Mon to Fri 07:46 UK), test-fired it: one "no new emails" run log line, nothing else changed. Open items: the task has connectors attached that cannot be removed per task, and it runs in automatic approval mode. Both accepted for demo data only
- Decision: production schedule is option B (n8n on the VPS), built at the two-week run
- Next: Piece 6 (Board): one place showing what the AI did, what awaits approval, what got stuck, and when it last ran
