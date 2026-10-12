---
type: spec
title: "Spec: {Build Name}"
build_type: automation | skill | web-tool | other
mode: build | improve
status: draft   # draft | parked | approved | live | retired
decision: build-first | build-later | wrong-target
owner: "{owner}"
created: YYYY-MM-DD
updated: YYYY-MM-DD
review_date: YYYY-MM-DD
related: []
---

# Spec: {Build Name}

**Decision:** {Build first / Build later / Wrong target}. Score: Frequency {…} × Effort {…} × Impact {…} × Confidence {…}. Build-hour cap: {…}.

## 1. Job and outcome
Who receives this, and what progress are they trying to make?

## 2. Output definition
The exact deliverable, its format and one example of a good output.

## 3. Scope
Sources → inputs → steps (10–15, each lights-on or judgment) → outputs → recipients. Out of scope: …

## 4. Trigger and state
Event or schedule; what "since last run" means and where the last run is stored.

## 5. Pattern and autonomy
Single call, chain, routing, review loop or agent; why, if it's more than a fixed workflow.

## 6. Step map
| # | Step | Block (Retrieval, Research, Reasoning, Logic, Delivery) | Code or model | Passes on |
|---|---|---|---|---|

## 7. Data and tools
| Source or tool | What it provides | Access (API, scrape, file) | Read or write |
|---|---|---|---|

## 8. Prompt contract
Context, instruction, output shape, what to do when nothing is found, when to say "Ambiguous". Keep it loose until real outputs have been read.

## 9. Delivery rules
Silence / digest / channel / direct alert, and the 3 AM test.

## 10. Guardrails and approvals
Approval before sends and writes; failure limits; max runs or spend. Read-only: "none, read-only".

## 11. Failure handling
Retries, error alert (to whom), duplicate checks on writes, replay.

## 12. Acceptance tests (provisional)
| # | Input (real case) | Expected result | Regression? | Run 1 | Run 2 | Run 3 |
|---|---|---|---|---|---|---|

Pass mark: …

## 13. Cost and budget
Per-run cost, model, build-hour cap, expected upkeep.

## 14. Owner and review
Owner, review date, when to retire it, manual fallback.

## Version log
- YYYY-MM-DD: created ({mode} mode).
