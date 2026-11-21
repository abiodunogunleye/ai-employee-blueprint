# AI Employee Blueprint

## What this is

A reusable template for building an AI employee for any business. It is built from six pieces:

- **Context**: what the AI employee knows about the business, its customers and its voice.
- **Skills**: the specific tasks it has been taught to carry out.
- **Memory**: what it remembers between sessions.
- **Tools**: the systems it can connect to and act through.
- **Schedules**: the work it does automatically, at set times.
- **Approval board**: where a human reviews and signs off its work before anything goes out.

## How to start a new client

1. Copy `_template/` to a new folder named after the client.
2. Fill in the six files in `business-brain/`.
3. Add skills to the `skills/` folder.
4. Never put real customer data or secrets in the repo.

## Security rules

- Secrets never go in files.
- Use demo data only until a client signs and a data processing agreement is in place.
- Tools get least-privilege access: read and draft only.
- The contents of `memory/` are never committed.
- Built for UK GDPR by default.
- This repo stays private until it has been reviewed.
- Anything involving money, contracts or an angry customer always waits for the owner. The AI drafts; a human decides.

## Status

Work in progress. `demo-freight-co` is a worked example using invented demo data.
