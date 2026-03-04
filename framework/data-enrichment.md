# Data Enrichment — Session Wrap-Up

After every coaching session, simulation, or debrief, check whether the candidate revealed information that should be captured in the data files. This is the last step before the session is fully closed.

## Why This Matters

During coaching, candidates talk freely about their work. They mention achievements they forgot to write down, technologies they used but didn't list, project details that are missing from their files. This information is valuable and easy to lose. Capturing it immediately, while the context is fresh, keeps the data files accurate and makes future CVs and coaching sessions stronger.

## What to Look For

Scan the session transcript (or conversation) for information the candidate mentioned that falls into these categories:

1. **Project details** — responsibilities, scope, team size, architecture decisions, business context not already in the project file
2. **Achievements** — measurable outcomes, problems solved, impact delivered (the hardest category to get from candidates, and the most valuable for CVs)
3. **Technologies** — tools, frameworks, platforms, cloud services mentioned in context that aren't in the project's technology list or in `data/skills.md`
4. **Skills** — new skills or higher proficiency evidence (e.g., candidate demonstrated deep knowledge of something listed at a lower level)
5. **Certifications or education** — anything mentioned but not tracked
6. **TODO resolution** — information that fills gaps marked with `<!-- TODO: ... -->` in existing data files

## How to Do It

### 1. Cross-Reference Against Data Files

For each piece of new information identified:

- **Projects:** Read the relevant project file(s) from `data/projects/`. Compare what the candidate said against what's written. Look for gaps in Description, Responsibilities, Key Achievements, and Technologies.
- **Skills:** Check `data/skills.md`. Is the technology listed? Is the experience level still accurate?
- **TODOs:** Scan project files discussed during the session for `<!-- TODO` markers. Check if the session provided the missing information.

### 2. Present Findings Naturally

Don't dump a checklist. Present findings conversationally, grouped by project or topic. Reference what the candidate actually said:

**Good:**
> During this session you described building a payment reconciliation system that reduced manual processing by 80%. Your NordPay project file doesn't mention that in key achievements. You also talked about using Kafka for event streaming there, which isn't in the technology list. Want me to add both?

**Bad:**
> I found 3 data gaps. Gap 1: Missing achievement in project file. Gap 2: Missing technology. Gap 3: TODO marker unresolved. Should I update?

### 3. Update Only With Approval

Wait for the candidate to confirm before writing anything. They may want to adjust the phrasing, skip certain updates, or correct what they said. Present all proposed changes first, then update.

### 4. What to Update

When approved:

- **Project files** (`data/projects/*.md`) — add achievements, responsibilities, technologies, description details
- **Skills** (`data/skills.md`) — add new skills or adjust experience levels
- **Certifications** (`data/certifications.md`) — add newly mentioned certifications
- **Project index** (`data/project-index.md`) — update if project descriptions changed significantly
- **TODO markers** — replace `<!-- TODO: ... -->` with the actual information, removing the TODO comment entirely

### 5. Keep It Brief

This step should take 1-2 minutes, not become a second session. If the enrichment is substantial (5+ updates across multiple files), offer to do it and summarize what changed. Don't re-coach or re-discuss the content.

## Voice Capture Update

If voice capture was enabled at the start of this session, update `data/voice.md`
as the **final step** — after all data file updates are complete.

Follow the full procedure in `framework/voice-capture.md`: review the session for
observations, append new entries to the relevant sections, update the **Last
updated** date, and add the session to the **Observed Over** list.

If voice capture was not enabled, skip this step entirely.

---

## What NOT to Do

- **Don't invent details.** Only capture what the candidate actually said. Don't infer achievements or embellish.
- **Don't update coached-answers.md here.** Strong phrasings are already handled in the progress tracking step. This step is for raw data, not coached delivery.
- **Don't update coaching files** (anti-pattern tracker, pressure points, etc.). Those are handled in earlier progress tracking steps.
- **Don't force it.** If the session didn't surface any new data file information, say so and move on. Not every session produces enrichment.
