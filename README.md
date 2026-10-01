# Wiki Stack Starter

A starter kit for building your own business knowledge wiki with **Claude Code** and **Obsidian**.

You drop source documents (reports, articles, transcripts, CSVs, internal docs) into `raw/`. Claude reads them and writes a linked wiki in `wiki/`: one summary page per source, plus concept, company and competitor pages that get richer with every source. You browse it in Obsidian and ask Claude questions against it.

## What you need
- **Claude Code**: the Claude desktop app (Code tab) or the `claude` CLI. <https://claude.com/claude-code>
- **Obsidian** (free) for reading the wiki. <https://obsidian.md>
- **Git** (optional, recommended) so every change is saved as a version. <https://git-scm.com>

## Setup (about 10 minutes)
1. **Unzip** this folder somewhere backed up (OneDrive, Dropbox, Google Drive, or a git remote). Rename it if you like, e.g. `acme-wiki`.
2. **Open it in Claude Code:** in the desktop app, start a new Code session and pick this folder. In a terminal: `cd` into the folder and run `claude`.
3. **Say: `set up my wiki`.** Claude asks you 8 short questions about your business (name, what the wiki is for, brands or products, competitors, starting topics). It then fills in the placeholders, creates starter pages and makes the first commit.
4. **Open it in Obsidian:** *Open folder as vault* → pick this folder. When asked, click **Trust author and enable plugins**. That turns on Dataview, which powers `wiki/dashboard.md`.
5. **Add your first source:** copy a document into the right `raw/` folder, then tell Claude `ingest raw/papers/your-file.pdf`.

## Everyday commands
Say these to Claude in the session:

| Say | What happens |
|---|---|
| `ingest raw/<folder>/<file>` | Reads the source, discusses 3–5 takeaways with you, then writes and updates 5–15 wiki pages |
| Any question, e.g. `who are our biggest competitors?` | Answers from the wiki with links; offers to file good answers as a page |
| `lint` | Health check: contradictions, orphan pages, missing pages, stale claims |
| `where did we leave off?` | Plans the session: what's waiting, what's ready, top 3 next steps |
| `wrap up` | Commits, updates the hot cache, notes open questions for next time |

You can also give facts in chat ("our Denver office opened in 2019") and ask Claude to record them. They're saved as a source page, since `raw/` is read-only.

## Folder map
```
CLAUDE.md            The rulebook Claude follows: page formats, workflows, safety rules
.claude/skills/      setup-wiki, session-start, session-end, plus Obsidian syntax helpers
.obsidian/           Obsidian settings, with the Dataview plugin bundled
raw/                 YOUR sources. Claude reads these but never edits them
  articles/  papers/  transcripts/  data/  assets/  repos/
wiki/                Claude's wiki. Claude writes here
  index.md           Catalog of every page, by cluster
  overview.md        Where to start: one section per topic cluster
  hot.md             Short "where we left off" note for the next session
  log.md             Append-only history of every ingest, question and lint
  dashboard.md       Live review tables (Obsidian only)
  sources/           One summary page per source
  concepts/          Topics and ideas; each cluster has one hub page
  entities/          organization/, competitors/, people/ (setup may add more)
  comparisons/  syntheses/   Answers worth keeping, filed from questions
```

## Tips
- **Keep `raw/` untouched.** Add files; don't edit or delete them. Claude cites them by path.
- **Name files clearly** before adding them, e.g. `2026-03-competitor-pricing-report.pdf`.
- **Start with your best internal document** (a company overview, strategy deck or brand guide). It gives every later source something to link to.
- **Answer Claude's questions.** When a source is unclear, Claude asks rather than guessing, and marks uncertain claims `confidence: low`.
- **Change the rules** by editing `CLAUDE.md`, or ask Claude to add a House Rule when you correct it.
- **Lint every 5–10 ingests** to keep links and clusters healthy.
