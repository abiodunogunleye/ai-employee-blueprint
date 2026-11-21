# AI Employee for a Client's Business: Build Book v1

## What this project is about
A hands-on build of the six-piece blueprint for making AI run the routine work of a client's business: Context, Skills, Memory, Tools, Schedules, Board. The owner stays the owner; the AI drafts, the owner decides. Anything involving money, contracts or an angry customer always waits for the owner.

Build order: context, then one skill, then one job, then put that one job on a schedule. Run it for 2 weeks, fix what breaks, then add the next job.

Principle throughout: UK GDPR by default (no personal data in the business brain, no pre-ticked consent boxes, least access for every tool).

## Checklist
- [ ] Ch 1: Context (business-brain folder, 5 files)
  - [x] 01-business.md
  - [x] 02-customers.md
  - [x] 03-voice.md (drafted; commit pending)
  - [x] 04-approvals.md
  - [x] 05-faq.md (commit pending)
  - [ ] Test the brain: give the five files and sample customer emails to Claude and check the drafts follow the voice and the tiers
- [ ] Ch 2: Skills (one job written step by step)
- [ ] Ch 3: Memory (running record the AI reads and updates)
- [ ] Ch 4: Tools (inbox: read and draft only)
- [ ] Ch 5: Schedules (that one job on a daily schedule)
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
- **Takeaway:** context is the AI's job description plus house style. Write the facts down once, show the voice with real examples, and keep examples consistent with the rules.
- **Academy:** do the lesson on writing effective prompts and instructions after you have used this.

## Chapter 1: Context
**Goal:** write down the business so every AI job reads it first and sounds like the owner, not a stranger.

**Steps**
1. Create a folder called `business-brain/`.
2. Write five plain files: business, customers, voice, approvals, FAQ.
3. Describe types of customer, never named individuals.

**Key prompt (interview method):** ask Claude to interview you one file at a time, then shape your real answers into a clean file. You supply the facts; Claude supplies the structure.

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
- Next: commit 05-faq.md; test the brain with sample emails; then Piece 2 (Skills)
