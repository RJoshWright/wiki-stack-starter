---
name: designing-builds
description: Plans and improves AI agents, automations, Claude skills and small web tools (calculators, quizzes, graders) before any building starts, by running the Design Before You Build method and writing a one-page design spec. Build mode is for something new; Improve mode is for something already built that isn't working well. Use when the user says "design before you build", "I want to build/automate X", "should we automate this", "let's make a tool/skill/agent for...", "where do I start with this workflow", or "this workflow/skill isn't working, help me rethink it". Not for writing copy, fixing a single known bug, or building from a spec that's already approved.
---

# Designing Builds

Runs the Design Before You Build method with the user, one stage at a time, and produces a design spec saved in the wiki.

## Standing rules (apply for the whole task)
1. **Read the method first.** If the wiki has its own playbook for this (search `wiki/concepts/` for "Design Before You Build"), read it and follow it. Otherwise read [references/method.md](references/method.md). If this skill and the wiki's playbook disagree, follow the playbook and tell the user.
2. **No building before the spec is approved.** Don't write code, prompts, workflows or skill files for the build itself until the user says the spec is approved. Then set `status: approved`.
3. **One stage at a time.** Ask one batch of numbered questions per stage (at most 5), wait for the answers, then fill that part of the spec.
4. **Write as you go.** Create the spec file at the start and update it after every stage, so progress survives a long session.
5. **Offer defaults, not menus.** Suggest a likely answer the user can accept or change.
6. **Scale the depth.** For read-only builds, sections 10–14 can be one line each. Anything that writes, sends or touches customer data gets full answers there.
7. **Only record what the user says.** Mark your own suggestions "proposed" until the user confirms them.
8. **House rules apply.** Follow CLAUDE.md, including its House Rules (for example, any rules on gating content, brand names or voice).

## Choose the mode
- Something new → **Build mode**: read [references/build-mode.md](references/build-mode.md).
- Something already built → **Improve mode**: read [references/improve-mode.md](references/improve-mode.md).
- Unclear → ask: "Is this new, or something we already have?"

Say which mode you're in, list its stages, and say the user can stop or skip a stage at any time.

## The spec file
- Path: `wiki/specs/{build-slug}.md` (lowercase kebab-case).
- Start from [assets/design-spec-template.md](assets/design-spec-template.md). Set `owner:` from the Owner line in CLAUDE.md. In Improve mode, if a spec already exists, update it and add a dated entry to its version log; don't start a new one.
- If the wiki has a playbook page for this method, link the spec from its "Specs" list.

## Progress checklist
Copy into the conversation and tick off as you go:
```
- [ ] Method read; mode chosen; spec file created
- [ ] Stage questions answered and spec sections filled
- [ ] Completeness check passed
- [ ] User approved the spec (status: approved)
- [ ] Wiki bookkeeping done (index, log)
```

## Completeness check (before asking for approval)
- Every section in the template has an answer, or "n/a" with a reason.
- Section 12 has at least 5 real test cases, including a "nothing found" case.
- If the build writes or sends: section 10 names an approval step and section 11 names an error alert and a duplicate check.
- Section 14 names an owner and a review date.
- Every "proposed" item is confirmed or removed.
Then show a short summary of the spec and ask: "Approve this spec?"

## After approval
- Set `status: approved` and update the date.
- Add a line for the spec to `wiki/index.md` (under a "Specs" heading after Syntheses; create the heading if it's missing) and append a log entry to `wiki/log.md` (`## [YYYY-MM-DD] query | Design spec: {title}`).
- Ask whether to start building now.

## Gotchas
- Don't skip discovery because the user already has a solution in mind. Ask about the last real time the task happened.
- People describe a workflow in 3–4x fewer steps than it really has. Keep asking until there are 10–15 steps.
- In Improve mode, don't propose a fix before reading real runs.
- A green run in an automation tool only means nothing crashed, not that the output was right.
