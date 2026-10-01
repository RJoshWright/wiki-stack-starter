---
type: meta
title: "Dashboard"
created: {{SETUP_DATE}}
updated: {{SETUP_DATE}}
---

# Dashboard

> [!info] Live views of the wiki
> Needs the Dataview plugin enabled in Obsidian. These tables render only in Obsidian; lint still works from the files. See [[index|Wiki Index]] for the catalog and [[overview|Overview]] for navigation.

## Needs review
Low- and medium-confidence pages, low first.

```dataview
TABLE confidence, length(sources) AS "Sources", cluster, updated
FROM "wiki/concepts" OR "wiki/entities" OR "wiki/sources"
WHERE confidence = "low" OR confidence = "medium"
SORT confidence ASC, updated ASC
```

## Source depth
Concepts and entities by number of sources. Pages with one source are the thinnest.

```dataview
TABLE length(sources) AS "Sources", confidence, cluster, updated
FROM "wiki/concepts" OR "wiki/entities"
SORT length(sources) DESC, file.name ASC
```

## Pages by cluster

```dataview
TABLE rows.file.link AS "Pages"
FROM "wiki/concepts" OR "wiki/entities"
GROUP BY cluster
SORT cluster ASC
```

## Recently updated (last 7 days)

```dataview
TABLE type, updated
FROM "wiki"
WHERE updated >= date(today) - dur(7 days)
SORT updated DESC
```

## Comparisons and syntheses

```dataview
TABLE date, length(sources) AS "Sources"
FROM "wiki/comparisons" OR "wiki/syntheses"
SORT date DESC
```

## Lint helpers

**Orphans** (no inbound links other than the navigation pages):

```dataview
LIST
FROM "wiki/concepts" OR "wiki/entities" OR "wiki/sources" OR "wiki/comparisons" OR "wiki/syntheses"
WHERE length(filter(file.inlinks, (l) => !contains(list("wiki/index.md", "wiki/overview.md", "wiki/hot.md", "wiki/log.md", "wiki/dashboard.md"), meta(l).path))) = 0
```

**Missing `cluster`:**

```dataview
LIST
FROM "wiki/concepts" OR "wiki/entities"
WHERE !cluster
```

**Missing `confidence`:**

```dataview
LIST
FROM "wiki/concepts" OR "wiki/entities" OR "wiki/sources"
WHERE !confidence
```

**Hubs not linked from the index:**

```dataview
LIST
FROM "wiki/concepts"
WHERE cluster_role = "hub" AND !contains(map(file.inlinks, (l) => meta(l).path), "wiki/index.md")
```

**Near-orphan syntheses** (1 or fewer inbound links):

```dataview
TABLE length(file.inlinks) AS "Inbound links"
FROM "wiki/syntheses"
WHERE length(file.inlinks) <= 1
```
