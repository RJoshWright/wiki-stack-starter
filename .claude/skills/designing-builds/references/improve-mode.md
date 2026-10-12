# Improve mode: stages

Follow "Improve mode" in `method.md` (or the wiki's own playbook, if it has one). Improve mode is not Build mode run again: it is a loop that gathers evidence first and then rewrites the spec. One stage per turn. Don't propose a fix before Stage 3.

## Stage 1: Triage → spec header and section 14
1. What is it, and where does it live (tool, file path, workflow name)?
2. What's wrong with it, in your words? Give the last real example.
3. How often is it used, and by whom?
4. Is there a spec for it already? (Check `wiki/specs/` first.)

Propose improve, rebuild (go to Build mode) or retire. Retiring is a rule-of-thumb call: suggest it only if it's barely used or costs more upkeep than it saves, and let the user decide.

## Stage 2: Collect runs
Ask the user for 20–50 recent real runs (inputs and outputs, run logs, transcripts, or the files it produced) plus any complaints. If fewer exist, use what there is and say the evidence is thin. Where you can read them yourself (local files, logs), do so instead of asking.

## Stage 3: Find the failures → sections 2, 12
Read every run. Write a short note on each failure, group the notes into 3–8 failure types, and count each type. Show the table to the user. Then:
1. Do these failure types match your experience? Any missing?
2. Which matter most?

Turn the top types into pass/fail checks, update "good" in section 2, and freeze the test set in section 12, marking which cases are regression tests.

## Stage 4: Locate and diagnose → section 6
For the top failure type, trace back to the first step that goes wrong. Classify it with the method's rule of thumb: prompt, data, structure or plumbing. Explain the evidence, and propose **one** change.

## Stage 5: Test the change
After the user approves the spec update and the change:
- Run every test input 2–3 times (or ask the user to) and record pass/fail in a new column.
- Keep the change only if the target failure improves and no regression test gets worse; otherwise revert it.
- Add the fixed cases to the regression set and add a dated line to the spec's version log.
- Repeat Stages 4–5 for the next failure type, or stop when the user is satisfied.

Then run the completeness check in `SKILL.md` and set a new review date.
