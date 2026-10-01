# LLM Wiki — Master Schema

> [!warning] Not set up yet
> This file still has `{{PLACEHOLDERS}}`. If you are Claude and you see this block, run the `setup-wiki` skill before doing anything else, then delete this block.

## Domain
{{BUSINESS_NAME}} {{WIKI_PURPOSE}}

Owner: {{OWNER_NAME}} ({{OWNER_ROLE}}). Findings are read by: {{AUDIENCE}}.

## Project Structure
- `raw/` — immutable source documents. NEVER modify any file in raw/.
  - `raw/articles/` web articles and clippings · `raw/papers/` reports and PDFs · `raw/transcripts/` meeting and call transcripts · `raw/data/` CSVs and exports · `raw/assets/` internal documents and images · `raw/repos/` code or config snapshots.
- `wiki/` — LLM-generated wiki. Claude owns this layer entirely.
- `wiki/index.md` — master catalog. Update on EVERY ingest. Organized cluster-first: one `## Cluster: Display Name (`slug`)` block per cluster with a one-line `>` description, a `**Hub:**` line, member concepts as bullets, then `**Entities:**` bullets. After the clusters: Comparisons, Syntheses (with dates), Source Summaries (with dates), Navigation Files. Entries use `- [[slug|Proper Name]] — one-line summary`. No source counts (lint checks depth instead).
- `wiki/log.md` — append-only activity log, oldest first. Never delete or reorder entries. At session start, after reading hot.md, run `grep "^## \[" wiki/log.md | tail -5` (recent activity) and `grep "^## \[.*#failure" wiki/log.md` (known dead ends).
- `wiki/overview.md` — cluster navigation hub and high-level synthesis. Revise after major ingests. Sections: What This Wiki Is (with source, page and cluster counts), Cluster Map (one line until clusters need a diagram), one `## Cluster: Display Name` section per cluster (`**Enter at:**` hub, 2–3 sentences with the cluster's main findings, `**Key entry points:**` as "Question?" → page, `**Synthesis:**` lines only once syntheses exist), Biggest Gaps, Graph Health (one line, refreshed by lint). Describes clusters; does not list every page (that is index.md's job).
- `wiki/dashboard.md` — Dataview dashboard (review queue, source depth, clusters, lint helpers). Renders only in Obsidian; Claude lints from the files, not from it.
- `CLAUDE.md` — this file. Re-read at the start of every session.
- `wiki/hot.md` — session hot cache (~500 words). Read silently at session start BEFORE responding. Rewrite per the Hot Cache rules below.

## Page Conventions
Every wiki page MUST have YAML frontmatter. Use these schemas:

**Links in frontmatter:** quote each wiki-link individually inside a YAML list, e.g. `related: ["[[concept1]]", "[[concept2]]"]`. Unquoted `[[x]]` is parsed as a nested list (or invalid YAML), so Obsidian, Dataview and backlinks won't see it. Never quote the whole list as one string. Links in the page body need no quotes.

**Names and link text:** always write brand, company and product names with their correct capitalization ({{NAME_EXAMPLES}}). File names stay lowercase kebab-case slugs, so every wiki-link must show the page's proper name: `[[acme-widgets|Acme Widgets]]`, in frontmatter and body alike. Inside a Markdown table, escape the pipe: `[[acme-widgets\|Acme Widgets]]`. Cluster values stay lowercase in frontmatter; where a cluster is shown as a heading or label, use its display name.

### Source Summary Pages (wiki/sources/)
Facts given in chat are recorded as a source page with `source_file: "user-provided in chat, YYYY-MM-DD (not stored in raw/)"`, since raw/ is read-only. If dictated notes have unclear names, ask or wait for a clean list before writing pages.

---
type: source
title: "Article/Paper Title"
slug: summary-{slug}
source_file: raw/articles/{filename}.md
author: "Author Name"
date_published: YYYY-MM-DD
date_ingested: YYYY-MM-DD
key_claims: [claim1, claim2, claim3]
related: ["[[concept1]]", "[[concept2]]"]
confidence: high | medium | low
---

### Concept Pages (wiki/concepts/)
---
type: concept
title: "Concept Name"
aliases: [alt-name, abbreviation]
sources: ["[[source1]]", "[[source2]]"]
related: ["[[concept2]]", "[[entity1]]"]
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: high | medium | low
cluster: {cluster-name}
cluster_role: hub | member   # hub pages must have an "In this cluster" body section
---

### Entity Pages (wiki/entities/)
Entity pages go in a subfolder:
- `wiki/entities/organization/` — {{BUSINESS_NAME}} itself, its brands, divisions, products and teams.
- `wiki/entities/competitors/` — competing companies.
- `wiki/entities/people/` — named people who matter to the domain (only when a source names them in a work role).
{{EXTRA_ENTITY_FOLDERS}}

Wiki-links use the file name only (`[[acme-widgets|Acme Widgets]]`), so file names must stay unique across all subfolders. When two companies share a name, add a qualifier to the slug (`summit-group-denver`, `summit-group-texas`).

Every competitor named in an ingested source gets an entity page in `wiki/entities/competitors/`, listed on the Competitive Landscape hub. A sub-brand or regional name goes on its parent's page as an alias, once checked to be the same company.

---
type: entity
entity_type: person | company | product | org | place
title: "Entity Name"
sources: ["[[source1]]", "[[source2]]"]
related: ["[[concept1]]", "[[entity2]]"]
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: high | medium | low
cluster: {cluster-name}
contradictions: []
open_questions: []
---

### Comparison Pages (wiki/comparisons/)
---
type: comparison
title: "Comparing X vs Y"
sources: ["[[source1]]", "[[source2]]"]
related: ["[[concept1]]"]  # Back-link upward to member pages
filed_from_query: true
date: YYYY-MM-DD
---

### Synthesis Pages (wiki/syntheses/)
---
type: synthesis
title: "Synthesis Title"
sources: ["[[source1]]", "[[source2]]"]
related: ["[[concept1]]"]  # REQUIRED: Back-link upward to member pages
filed_from_query: true
date: YYYY-MM-DD
---

## Clusters
Clusters are the top-level topics of the wiki. Each has one hub concept page (`cluster_role: hub`). Starting clusters, set at setup:
{{CLUSTER_LIST}}

New clusters are added when a source doesn't fit an existing one: add them here, to wiki/index.md and to wiki/overview.md.

## Ingest Workflow
When I say "ingest [filename]" or "ingest raw/[path]":
1. Read the source file from raw/.
2. Discuss key takeaways with me (3–5 bullet points).
3. Create wiki/sources/summary-{slug}.md with full summary.
4. Update wiki/index.md — add new page under its cluster section.
5. Update ALL relevant concept and entity pages with new info.
6. If new info contradicts an existing page, flag it explicitly using a > [!contradiction] callout block.
7. Create new concept/entity pages if the source introduces them.
   - Assign each new page a `cluster:` field.
   - If the page is a hub (`cluster_role: hub`), add an `## In this cluster` body section listing members.
   - If the page is a member, link it from its cluster hub's `## In this cluster` table.
   - If a new cluster is needed, add it to wiki/index.md and wiki/overview.md.
8. Append a structured entry to wiki/log.md (see Log Format below).
9. Rewrite wiki/hot.md (see Hot Cache below).
10. A single ingest should touch 5–15 wiki pages.

## Query Workflow
When I ask a question:
1. Check `grep "^## \[.*#failure" wiki/log.md` for earlier dead ends on the same topic. If one matches, follow its `Lesson:` line instead of repeating the search, and say so.
2. Read wiki/index.md to identify relevant pages.
3. Read those pages directly.
4. Synthesize an answer with [[wiki-link]] citations.
5. If the answer is a valuable analysis, offer to file it as a new page in wiki/comparisons/ or wiki/syntheses/.
   - If a synthesis is filed, add a `See also: [[synthesis-slug]]` line in the body of each concept page it drew from (body, not frontmatter).
6. Update wiki/log.md with a query entry. If the wiki had no relevant information, tag it `#failure` (see Log Format).
7. If a page was filed in step 5, or the query was a `#failure`, rewrite wiki/hot.md (see Hot Cache below).

## Lint Workflow
When I say "lint" or "health check":
1. Scan for contradictions between pages. List them.
2. Find orphan pages (0 inbound links). List them.
3. List concepts mentioned 3+ times but lacking their own page.
4. Check for stale claims that newer sources may have superseded.
   - For any confirmed hallucination (a claim no source supports), fix the page (add a `> [!contradiction]` callout or lower its confidence) and log it as a `#failure` entry.
5. **Cluster health check:**
   - Every concept/entity page has a `cluster:` field. List any missing.
   - Every `cluster_role: hub` page has an `## In this cluster` section. List any missing.
   - Every cluster hub is listed in wiki/index.md under its cluster section. List gaps.
6. **Synthesis back-link check:**
   - Every synthesis page is back-linked from the concept pages it drew on. List near-orphan syntheses (≤1 inbound link).
7. Suggest 3–5 new questions or sources to investigate.
8. Refresh the Graph Health line in wiki/overview.md (date, content page count, orphan count, known structural debt) and the counts in What This Wiki Is.
9. Append a lint entry to wiki/log.md, with the one-line count summary (see Log Format).
10. Rewrite wiki/hot.md (see Hot Cache below).

## Hot Cache
wiki/hot.md is a short snapshot so the next session can pick up where this one left off.
- **Read:** silently at the start of every session, before responding. Don't summarize it to me; use it to restore context.
- **When to rewrite:** at the end of every ingest and lint, after any query that files a new page or is a `#failure`, and when I say "wrap up" or "close".
- **How:** rewrite the whole page; never append. Keep it under ~500 words. Update the `updated:` date.
- **Sections:**
  - Current Focus — 1–2 sentences on what we're actively investigating.
  - Open Questions — unresolved questions and next sources to ingest.
  - Recent Decisions — decisions from the last 1–2 sessions only. Permanent rules go in CLAUDE.md; facts go on wiki pages.
  - Last Operations — the last 3 log entries, one line each.
  - Active Pages — wiki pages being developed or recently updated.
- List recent `#failure` dead ends under Open Questions, with what would resolve them, until a source fills the gap.
- Drop items that are resolved or stale. Full history belongs in wiki/log.md, not here.

## Log Format
Each log entry MUST start with this prefix for parsability:
## [YYYY-MM-DD] {ingest|query|lint} | {title/description}

Example:
## [2026-04-12] ingest | Market Sizing Report 2026
Source: raw/papers/2026-04-market-sizing.pdf
Pages created: wiki/sources/summary-market-sizing-2026.md
Pages updated: wiki/concepts/target-markets.md,
               wiki/entities/competitors/summit-group.md
Contradictions flagged: wiki/concepts/pricing-strategy.md (see note)

Query entries list `Question:`, `Pages read:`, `Result:` and `Pages filed:`. Lint entries start with a one-line count summary:
Contradictions: N | Orphans: N | Missing pages suggested: N | Hallucinations: N

**Failure log.** Add `#failure` to the end of the heading line (an Obsidian tag, and greppable) for:
- queries where the wiki had no relevant information;
- ingest errors (source too noisy, broken formatting, unreadable);
- hallucinations confirmed during lint.
Every failure entry ends with a `Lesson:` line saying what not to retry and what would resolve it. Old entries are not retro-tagged.

Example:
## [2026-09-23] query | How is each product line positioned? #failure
Question: Which customer segment does each product line target?
Pages read: wiki/concepts/product-portfolio.md
Result: No source covers positioning or target segments.
Pages filed: none
Lesson: Don't re-search the wiki; needs a brand strategy or positioning document.

## Safety Rules
- NEVER write to raw/. This is a hard constraint with no exceptions.
- NEVER delete wiki pages. Mark as deprecated in frontmatter instead.
- Always update wiki/index.md and wiki/log.md on every operation.
- When uncertain about a claim's accuracy, set confidence: low.
- Cross-reference all new pages to at least 2 existing pages.

## Working Principles
- **Surface assumptions.** If a source is unclear or could be read more than one way, ask before filing it. Don't guess silently. Mark inferred claims `confidence: low`.
- **AI-generated research is medium confidence.** Sources produced by ChatGPT or similar tools get `confidence: medium` at most, and so do claims that rest only on them.
- **Only claim what the source says.** Don't add filler analysis or guessed facts. Summaries state what the source says.
- **Small, targeted edits.** When updating an existing page, change only the sections the new source affects. Don't rewrite or reformat other content. If you spot unrelated problems, mention them and leave them for a lint.
- **Check before finishing.** At the end of every ingest, confirm and report: the frontmatter is valid YAML with quoted wiki-links, index.md is updated, a log.md entry is added, hot.md is rewritten, each new page has 2+ cross-links, and names are capitalized correctly.

## House Rules
Rules specific to this wiki, added over time (the session-end skill offers to add them here).
{{HOUSE_RULES}}
