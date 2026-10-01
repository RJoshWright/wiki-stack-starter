---
name: session-start
description: On-request session planning for this wiki. Reads CLAUDE.md, hot.md and the log, checks git for uncommitted work and raw/ for files not yet ingested, then suggests what to do next. Use only when the user asks "what should I work on", "what's my context", "start session", "plan my session" or "where did we leave off". For wrapping up, see session-end.
---

# Session Start

CLAUDE.md already sets what happens at the start of every session: re-read CLAUDE.md, read `wiki/hot.md` silently, then check recent log entries and `#failure` dead ends. That silent read happens anyway. **This skill runs only when the user asks for their context or a plan.** CLAUDE.md says not to summarise hot.md unprompted.

If CLAUDE.md still contains `{{` placeholders, stop and suggest the `setup-wiki` skill instead.

## 1. Read the wiki's state
- `CLAUDE.md`, `wiki/hot.md` (Current Focus, Open Questions, Recent Decisions).
- `grep "^## \[" wiki/log.md | tail -5` (recent activity) and `grep "^## \[.*#failure" wiki/log.md` (dead ends).
- If hot.md is more than a few days old or contradicts the log, say so and trust the log.

## 2. Check for pending work
- `git status --short`. Uncommitted work goes on the list.
- **Sources not yet ingested:** files in `raw/` (not `.gitkeep`) whose path appears in no `source_file:` line in `wiki/sources/`. Check with `grep -rh "^source_file:" wiki/sources/`.
- **Last lint:** the date of the last `lint` entry in the log, and how many pages were added since.

Only read at this stage. Don't commit or ingest until the user chooses.

## 3. Sort and suggest
Put what you found into three lists:
- **Waiting on you:** unanswered questions from hot.md's Open Questions and confirmations the user owes.
- **Ready for Claude:** ingests due, uncommitted work, a lint if the last one is old or many pages were added since, `#failure` gaps that a known source could fill.
- **Suggested top 3:** in order, each with a one-line reason. Rank first what unblocks other work (an ingest due, an answer that settles several pages), then what's time-sensitive, then quick wins.

## 4. Reply
Keep it short, and don't restate hot.md in full:

```
**Where we left off:** one or two lines.

**Waiting on you:**
- ...

**Ready for me:**
- ...

**Suggested next:**
1. ... (why)
2. ... (why)
3. ... (why)

What would you like to start with?
```

## Memory
Don't scan every memory file at the start. If something from memory conflicts with what the files or git show, flag that one conflict and trust the files. Memory is reviewed at wrap-up (session-end).

## Don't
- Summarise hot.md when the user hasn't asked.
- Commit, ingest or edit pages before the user picks what to do.
