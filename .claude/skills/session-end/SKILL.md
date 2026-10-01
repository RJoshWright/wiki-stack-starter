---
name: session-end
description: End-of-session wrap-up for this wiki. Checks the vault is committed, rewrites wiki/hot.md per CLAUDE.md, captures decisions and open loops, reviews memory, and offers to promote lasting rules to CLAUDE.md. Use when the user says "end session", "wrap up", "close", "lets end session" or "save progress".
---

# Session End

What "wrap up" means in CLAUDE.md, as a checklist. The session's record already lives in `wiki/log.md` (one entry per ingest, query or lint) and `wiki/hot.md` (the snapshot for the next session). This skill doesn't add another record. It makes sure those two, git and memory are current.

## 1. Check the vault is committed
Run `git status --short`. Commit leftovers locally with a message that says what they are. New files in `raw/` are added to git as they are; never edit anything in raw/. Push only if the repo has a remote and the user has asked for pushing before; otherwise don't suggest it.

## 2. Rewrite wiki/hot.md
Follow the Hot Cache rules in CLAUDE.md: rewrite the whole page, never append.
- Sections: Current Focus, Open Questions, Recent Decisions, Last Operations (the last 3 log entries, one line each), Active Pages.
- Under ~500 words. Count them and trim if over.
- Update `updated:` to today.
- Drop items that are resolved or stale. Keep recent `#failure` dead ends under Open Questions with what would resolve them.
- **Recount, don't copy.** Any number carried over (page counts, sources) is checked against the files before it's kept.

## 3. Capture the session briefly
Pick out, from this session only:
- **Key decisions** (1–3) → Recent Decisions in hot.md.
- **Open loops:** questions put to the user and still unanswered, and things waiting on them → Open Questions.
- **Next focus** → the end of Current Focus.

Don't retell the session. Don't add a log.md entry for the wrap-up itself: log.md takes only ingest, query and lint entries.

## 4. Review memory
If this Claude setup has a memory folder for this project, review it:
- Look for corrections the user gave, approaches they confirmed, and project facts that git and the wiki don't already record.
- Check for an existing memory first and update it rather than adding a duplicate.
- When the user stated a rule in their own words, quote them exactly rather than paraphrasing.
- Fix or delete memories this session proved wrong.

## 5. Offer CLAUDE.md promotion
If a learning should apply to every future session (a new rule for pages, links or workflows), ask: "Should this go into CLAUDE.md?" If yes, add it under House Rules. Edit CLAUDE.md only after the user says yes.

## 6. Report
Keep it short:
- **Committed:** commit hash (or "nothing to commit").
- **hot.md:** rewritten, word count.
- **Memory:** changes, or "no memory changes".
- **Open loops:** what's waiting on the user.
- **Next focus:** one line.

## Don't
- Write to raw/.
- Create daily, session or mirror pages in the wiki. They'd have no cluster, and lint would flag them.
- Retell the whole session.
- Edit CLAUDE.md without asking.
