# Build mode: stages

Follow "Build mode" in `method.md` (or the wiki's own playbook, if it has one). This file gives the questions for each stage and which spec sections each stage fills. One stage per turn.

## Stage 1: Discovery → spec sections 1, 3
1. Who will use or receive this, and what are they trying to get done?
2. Walk me through the last time this task actually happened. What did you open first?
3. What happens before it starts, and after the result is sent?
4. When has it gone wrong, and what did that cost?
5. Which steps need judgment, and which could anyone do with written instructions?

Then draft the step list (10–15 steps, each labelled lights-on or judgment) and the scope line (sources → inputs → steps → outputs → recipients). Ask the user to correct it.

## Stage 2: Should we build it? → decision line at the top of the spec
1. Could an existing tool, template or skill do most of this?
2. How often does this actually happen today? (daily, weekly, monthly, one-off)
3. Roughly how long does it take each time, and how long would the build take?
4. Who benefits, and how close is it to revenue (leads, pipeline, customers)?
5. How sure are we of these numbers? (100%, 80% or 50%)

Score Frequency × Effort × Impact × Confidence, give the build-hour cap from the method, and propose Build first, Build later or Wrong target. Lead-generation tools are scored on pipeline instead. If the answer is "Wrong target" or "Build later", record it in the spec, set `status: parked`, and stop unless the user wants to continue.

## Stage 3: Output and trigger → sections 2, 4, 5
1. What exactly does the finished output look like? Can you show or describe one good example?
2. Where does it go, and who sees it?
3. What starts it: a schedule, an event, or a person asking?
4. Does it need to know what changed since the last run?

Then propose the simplest pattern that works (single call, chain, routing, review loop, agent), with a reason for anything beyond a fixed workflow.

## Stage 4: Step map and data → sections 6, 7, 8, 9
Draft the step map yourself from Stages 1 and 3: each step as Retrieval, Research, Reasoning, Logic or Delivery (see "Building blocks, prompts and alerts" in `method.md`), whether it's code or model, and the structured output it passes on. Then ask:
1. Where does each piece of data live, and how do we get it (API, scrape, stored file)?
2. Which steps read, and which write or send?
3. When there's nothing to report, what should happen?
4. Which results deserve silence, a digest, a channel post or a direct alert?

## Stage 5: Safety and upkeep → sections 10, 11, 13, 14
Add the build-type checks from the method (automation, skill or web tool) here.
1. What could this send, write or change? Which of those need approval first?
2. If a step fails, who hears about it, and how?
3. What would it cost per run, and how much upkeep do you expect?
4. Who owns it, when should it be reviewed, and what would make us retire it?

For read-only builds, keep this to one line per section.

## Stage 6: Tests → section 12
Ask for 5–20 real past cases with the result that would have been right. Include at least one "nothing found" case and one ambiguous case, then agree a pass mark. Tell the user these tests are provisional and will change once real outputs have been read.

Then run the completeness check in `SKILL.md`.
