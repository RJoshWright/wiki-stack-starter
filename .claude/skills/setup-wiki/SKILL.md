---
name: setup-wiki
description: One-time setup for a new LLM wiki. Interviews the owner about their business, fills the {{PLACEHOLDERS}} in CLAUDE.md and the wiki/ navigation files, creates the starting cluster hub pages, and makes the first git commit. Use when the user says "set up my wiki", "setup", "get started", or when CLAUDE.md still contains {{PLACEHOLDERS}}.
---

# Setup Wiki

Turns this starter kit into a working wiki for one business. Run it once. If CLAUDE.md has no `{{` left, setup is done: say so and stop.

## 1. Interview
Ask these in one message, numbered, and say that short answers are fine and anything can be changed later:

1. **Business name**, with its exact capitalization.
2. **What the wiki is for**, in one line (e.g. "marketing intelligence and enablement", "sales enablement", "product and competitor research").
3. **Your name and role**, and **who reads what the wiki finds** (just you, your team, leadership, clients).
4. **Brands, divisions, products or markets** the business has. A rough list is fine.
5. **Main competitors**, if you know them.
6. **Starting topics**: 3–5 big areas you want to understand. These become clusters. If unsure, say "suggest some".
7. **Any other kinds of thing you'll track** that need their own folder (e.g. locations, clients, suppliers, campaigns).
8. **Names that are easy to get wrong** (odd capitalization, all-caps units, abbreviations).

Wait for the answers. If the user asks you to suggest clusters, propose 3–5 from answers 1–4 (always include a Competitive Landscape cluster if they have competitors) and confirm them before writing.

## 2. Fill CLAUDE.md
Replace every placeholder:
- `{{BUSINESS_NAME}}`, `{{WIKI_PURPOSE}}` (e.g. "marketing intelligence and enablement system"), `{{OWNER_NAME}}`, `{{OWNER_ROLE}}`, `{{AUDIENCE}}`.
- `{{NAME_EXAMPLES}}`: 2–4 of their real names with correct capitalization, from answers 1, 4 and 8.
- `{{EXTRA_ENTITY_FOLDERS}}`: one bullet per extra folder from answer 7, same style as the bullets above it (`wiki/entities/{folder}/` — what goes there). Create each folder with a `.gitkeep`. If none, delete the line.
- `{{CLUSTER_LIST}}`: one bullet per cluster: `` - `slug` — Display Name: one-line scope. Hub: [[hub-slug|Hub Title]] ``.
- `{{HOUSE_RULES}}`: rules from answer 8 as bullets, or `- (none yet)`.
- Delete the "Not set up yet" warning block at the top.

Then `grep -n "{{" CLAUDE.md` must return nothing.

## 3. Fill the navigation files
In `wiki/index.md`, `wiki/overview.md`, `wiki/hot.md`, `wiki/log.md` and `wiki/dashboard.md`: replace every `{{...}}` placeholder. `{{BUSINESS_NAME}}` is the business name and `{{SETUP_DATE}}` is today (YYYY-MM-DD); the rest are below.
- **index.md** `{{CLUSTER_BLOCKS}}`: one `## Cluster:` block per cluster (format in CLAUDE.md), with its hub on the `**Hub:**` line. Add the organization entity page under the right cluster's `**Entities:**`, and the setup source page under Source Summaries.
- **overview.md:** `{{WHAT_THIS_WIKI_IS}}` (purpose, owner, 1 source, page count, cluster count), `{{CLUSTER_MAP}}` (one line), `{{CLUSTER_SECTIONS}}` (one `## Cluster:` section per cluster: Enter at the hub, "No sources yet." as its findings, 1–2 Key entry points) and `{{BIGGEST_GAPS}}` ("Everything: only the setup interview so far.").
- **hot.md:** `{{CURRENT_FOCUS}}` = setup done, next step is the first ingest. `{{OPEN_QUESTIONS}}` = the sources the user should drop into raw/ first (suggest 3–5 from the interview).

Search each file for `{{` afterwards; none should be left.

## 4. Create starter pages
Only from what the user told you. No invented facts.
- One **hub concept page** per cluster in `wiki/concepts/` (`cluster_role: hub`, `confidence: low`, `sources: []`), with a one-paragraph scope, an empty `## In this cluster` table (header row only), and links to the other hubs.
- One **entity page** for the business in `wiki/entities/organization/`, listing the brands, divisions or products from answer 4 as facts "from the owner, in chat".
- One **source page** `wiki/sources/summary-setup-interview.md` with `source_file: "user-provided in chat, YYYY-MM-DD (not stored in raw/)"`, recording the interview answers. Every starter page cites it in `sources:`.
- Don't create competitor pages yet unless the user named competitors: if they did, one page each in `wiki/entities/competitors/` with only the name and the note "named by the owner at setup; nothing else known yet", `confidence: low`.

## 5. Log, commit, report
- Append to `wiki/log.md`: `## [YYYY-MM-DD] ingest | Setup interview (user-provided)` with Pages created and Pages updated.
- If the folder is not a git repo, run `git init`, then `git add -A` and commit "Set up wiki for {Business Name}". If git isn't installed, skip and say so.
- Tell the user: what was created, how to open the folder as an Obsidian vault and trust the Dataview plugin, and what to do next: drop a document into `raw/` and say `ingest raw/<folder>/<file>`.

## Don't
- Write to raw/.
- Invent facts about the business, its competitors or its market. Pages start thin; ingests fill them.
- Leave any `{{` placeholder behind.
