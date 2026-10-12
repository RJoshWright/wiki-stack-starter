# Design Before You Build: the method

The default method for the `designing-builds` skill. A wiki can replace it with its own playbook page; the skill then follows that page instead.

**Where it comes from.** The core comes from Profound University's *Marketing Engineering Concepts* course (https://university.tryprofound.com/courses/marketing-engineering-concepts). The rest was added after checking it against other published guidance: Anthropic's "Building effective agents" and its posts on evals and context engineering, OpenAI's practical guide to building agents, Hamel Husain and Shreya Shankar's evals FAQ, GitHub Spec Kit and Kiro specs, SIPOC, Jobs to Be Done, the n8n, Make and Zapier error-handling docs, and interactive-calculator guides. Steps marked *(Profound)* come from the course and steps marked *(added)* from that research. Rules of thumb are labelled as such. This is outside reading, not tested in every business: adjust it after your first builds.

## Contents
- Build mode steps
- Improve mode steps
- Build-type checks
- Building blocks, prompts and alerts
- Spec template sections

## Build mode (something new)
1. **Discovery** *(Profound)*. Anchor on the last time the task really happened ("What did you open first?"). Break every verb into steps, labelling each **lights-on** (anyone with instructions could do it) or **judgment**. Probe before, after and when it went wrong. If you are your own user, a short self-interview works the same way.
2. **Should we build it?**
   - Two gates first *(added)*: could an existing tool, template or skill do most of it? Does any step need judgment, or would plain rules do?
   - Score **Frequency × Effort × Impact** *(Profound)* × **Confidence** (100%, 80% or 50%) *(added, from RICE)*. Sort into Build first, Build later or Wrong target.
   - Cap the build hours *(added, from xkcd 1205)*: saving 5 minutes on a daily task is worth about 6 days of building over five years, on a weekly task about 21 hours. Use a 2–3 year horizon and subtract upkeep.
   - Lead-generation tools save no time, so they go in their own queue, scored on pipeline.
3. **Write the spec** using the template. Start from the output and work backwards *(Profound)*. Sections 10–14 get deeper when the build writes, sends or touches customer data; for a read-only build, "none, read-only" is a valid answer *(added)*. Pin down outputs and tests firmly; keep prompts loose until real outputs show what's needed *(added)*.
4. **Approve the spec.** No building until the owner approves it.
5. **Build a thin slice first:** the smallest version that produces the real output end to end.
6. **Check it against the provisional tests** (section 12). Expect the tests to change once you've read real outputs *(added)*.
7. **Go live** with an owner, a failure alert and a review date set (sections 11 and 14).

## Improve mode (something already built)
Read real runs before changing anything *(added)*: what "good" means only becomes clear once you've read real outputs.
1. **Triage:** improve, rebuild or retire? If nobody uses it or it costs more upkeep than it saves, consider retiring it (rule of thumb; weakly sourced).
2. **Collect** 20–50 recent real runs, plus every known complaint.
3. **Note each failure and group them** into 3–8 failure types, then count each type.
4. **Revise "good":** turn the top failure types into pass/fail checks and update the spec.
5. **Freeze a test set** from those inputs.
6. **Find the first step that fails** and diagnose it (rule of thumb):
   - **prompt** problem: misreads data that is present *(Profound)*.
   - **data** problem: the data was stripped or mis-mapped earlier *(Profound)*.
   - **structure** problem: weak despite a good prompt and data, so split the step or add a check *(Profound)*.
   - **plumbing** problem: logins, rate limits, timeouts, duplicates *(added)*.
7. **Change one thing** (prompt wording, model or input format) *(Profound)*. Switch models only when the failures point at the model.
8. **Run every test input 2–3 times** and record pass/fail *(added)*. Keep the change only if the target failure improves and nothing else gets worse.
9. **Add fixed failures to a regression set** that should stay near 100% *(added)*.
10. **Monitor:** reread a sample of runs after any significant change.

## Build-type checks *(added)*
- **Scheduled automation or routine** (n8n, Zapier, Make, Claude Code routines): these fail silently. A green run only means nothing crashed.
  - Give it only the connections it needs, and write a prompt that stands on its own and says what success looks like.
  - Send an error alert to a person, separate from the result alerts.
  - Give every write step a duplicate check *before* retries or replays are switched on. Have a kill switch, and reread the run logs.
- **Claude skill:** these fail by not triggering, or by drifting.
  - The description says what it does, when to use it and what it's not for.
  - Set how much freedom each step gets.
  - Keep `SKILL.md` under 500 lines, with detail in reference files.
  - Write at least 3 test scenarios, plus about 20 trigger phrases, half of which should *not* trigger it.
- **Public web tool** (calculator, quiz, grader): these fail on completion and trust.
  - Ask 3–6 questions people can answer from memory.
  - Show one main number, with its assumptions and a "how we calculated this".
  - Show the result before asking for contact details: guides report far more opt-ins after the result than before it. Then offer optional follow-up, and follow any gating rule in your House Rules.
  - Make the call to action refer to the specific result, and track completion and opt-in rates.
  - Keep the calculation fixed and transparent (no AI-written results on public pages). Check consent rules for your jurisdiction before collecting details.

## Building blocks, prompts and alerts *(Profound)*
- **Five blocks:**
  - **Retrieval:** fetch data you already own.
  - **Research:** find new outside information.
  - **Reasoning:** an AI model summarizes, drafts, scores or classifies.
  - **Logic:** branch on what the reasoning found.
  - **Delivery:** send the result out.
- **Getting the data:** through an API, a web scrape or a stored file. To detect change, read the last run's stored copy, compare it with today's, then overwrite it.
- **Prompts:** each one gives context, an instruction and an output format.
  - Split a prompt that does several jobs.
  - Say exactly what to output when nothing is found, and allow an "Ambiguous" answer.
  - Never let the model supply facts from its own knowledge.
  - Apply the "3 AM test": would you trust it running unwatched?
- **Structured outputs:** shape each answer for the next step: a yes/no for go/no-go, a number for maths, a short label for routing, a list for looping. Name variables `source_thing`.
- **Code or model:** use code for exact work (maths, filtering, sorting, formatting, de-duplication) and the model for judgment.
- **Alert tiers:**
  1. Silence when nothing is unusual.
  2. A digest for things that are real but not urgent.
  3. A channel summary for things that are notable.
  4. A direct alert for things that need attention now.

  Noisy alerts make people stop trusting the build.

## Spec template sections
Mirrors `assets/design-spec-template.md`:

| # | Section | What it answers |
|---|---|---|
| 1 | Job and outcome | Who receives this, and what progress are they trying to make? |
| 2 | Output definition | The exact deliverable, its format and one example *(Profound)* |
| 3 | Scope | Sources → inputs → 4–7 steps → outputs → recipients (SIPOC); what's out of scope |
| 4 | Trigger and state | Event or schedule; what "since last run" means *(Profound)* |
| 5 | Pattern and autonomy | Single call, chain, routing, review loop or agent; why anything more than a fixed workflow |
| 6 | Step map | Each step as a building block; code or model; what it passes on *(Profound)* |
| 7 | Data and tools | Each source and tool; read or write |
| 8 | Prompt contract | Context, instruction, output shape, null case, "Ambiguous" label *(Profound)* |
| 9 | Delivery rules | Silence, digest, channel or alert; the 3 AM test *(Profound)* |
| 10 | Guardrails and approvals | Approval before sends and writes; failure limits; max runs or spend |
| 11 | Failure handling | Retries, error alert, duplicate checks, replay |
| 12 | Acceptance tests | 5–20 real cases with expected results, including null and ambiguous cases; pass mark |
| 13 | Cost and budget | Per-run cost, model, build-hour cap, expected upkeep |
| 14 | Owner and review | Owner, version log, review date, when to retire it, manual fallback |
