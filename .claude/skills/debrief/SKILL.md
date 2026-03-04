---
name: debrief
description: Debrief a voice simulation — analyze transcript against coached answers, track anti-patterns, log session
argument-hint: <path-to-cv>
user-invocable: true
allowed-tools: Read(*), Glob(*), Grep(*), Write(coaching/**), Edit(coaching/**)
---

# Debrief — Voice Simulation Post-Session Analysis

Analyze a recruiter screening transcript from a Claude App voice simulation. Compare the candidate's answers against coached answers, identify anti-patterns, rate performance, and log the session to the progress tracker.

## Prerequisites

The user has:
1. Completed a voice simulation in the Claude App (generated via `/voice-export`)
2. Pasted or provided the conversation transcript in this Claude Code conversation
3. Invoked this skill with the CV path to identify the role

## Arguments

- `$ARGUMENTS` (required): Path to the CV file used for the simulation (e.g. `output/20260210-target-role-slug.md`)

The transcript is expected to be in the conversation context — the user pastes it before or after invoking the skill.

## Instructions

### Step 1: Load Context

Load these files in parallel using the CV path to derive filenames:

1. **Cheat sheet** — `*-cheatsheet.md` matching CV filename (full file — this IS the coaching side, coached answers are needed here)
2. **Coached answers** — `coaching/coached-answers.md` (general coached phrasings)
3. **Deep review** — `*-DEEP-REVIEW.md` matching CV filename (to know what tough questions were expected)
4. **Anti-pattern scorecard** — `coaching/progress-recruiter/_summary.md`
5. **Anti-pattern tracker** — `coaching/anti-pattern-tracker.md` (global pattern status — which are resolved, which to watch for)
6. **Voice profile** — `data/voice.md` (candidate's communication style and avoidances)
7. **Session template** — `framework/templates/recruiter-session.md`

If the transcript is not yet in the conversation, ask the user to paste it.

### Step 2: Parse Transcript

Break the transcript into Q&A pairs:
- **Recruiter question** — what was asked
- **Candidate answer** — what the candidate said
- **Topic** — categorize (pitch, technical, compensation, availability, experience, team fit, logistics, closing)

Note which deep review probing questions were actually asked by the recruiter, and which were skipped.

### Step 3: Analyze Each Answer

For each Q&A pair, assess:

#### A. Answer Quality (1-5)
- **5** — Strong, close to or better than coached version. Concise, direct, memorable.
- **4** — Good, minor improvements possible. Got the point across.
- **3** — Adequate but missed opportunities. Could have been stronger.
- **2** — Weak. Rambling, defensive, or missed the point.
- **1** — Harmful. Volunteered a negative, contradicted self, or failed to answer.

#### B. Trust/Credibility Impact
**Key insight:** Real recruiters don't understand technical details, but they DO notice evasiveness, dodging, and red flags that signal "this person might embarrass me in the client interview."

For each answer, assess trust impact:
- ✅ **Builds trust:** Direct answer, confident, no hedging
- ⚠️ **Neutral:** Adequate answer, no red flags
- ❌ **Damages trust:** Dodged question, vague when pressed for specifics, inconsistent, defensive

**Special attention to:**
- "Didn't answer the actual question" — even non-technical recruiters notice this
- Being asked the same question twice because the first answer was too vague
- Any moment where the recruiter might think "is this person hiding something?"

#### C. Comparison to Coached Answer
- If a coached answer exists (in cheat sheet or coached-answers.md) for this topic, compare:
  - What was the coached phrasing?
  - How close did the candidate get?
  - What was different — better or worse?

#### D. Anti-Pattern Check
Scan each answer for known anti-patterns. Load the full pattern list from `coaching/anti-pattern-tracker.md` § "Known Anti-Patterns Reference" — that file is the single source of truth for which patterns exist and their numbering. If the tracker has no patterns yet (new user), use these universal seed patterns:
- Volunteered a negative unprompted
- Over-explained technical details
- Hesitated or waffled on compensation/availability
- Didn't answer the actual question
- Essay structure (verdict last)

Also watch for any NEW anti-patterns not yet tracked — add them to the tracker after the debrief.

#### E. Voice Profile Cross-Reference

After identifying triggered anti-patterns, scan `data/voice.md` "Things to Avoid":
- If a triggered anti-pattern also appears in voice.md, flag it as a deep-rooted
  pattern (shows up in both writing and delivery) — note this in the debrief report.
- If a newly discovered anti-pattern reflects a fundamental communication style
  (not a one-off performance mistake), add it to voice.md "Things to Avoid"
  with a note that it was first observed in a debrief session.

Patterns that cross both systems (e.g. essay structure, passive-voice self-description,
leading with context before the point): label these **deep-rooted** in the Anti-Patterns
Triggered section of the report so the candidate knows the issue spans writing and speech.

### Step 4: Generate Debrief Report

Present the analysis to the user in this structure:

```markdown
## Debrief — [Role Title] (Voice Simulation)

**Date:** [today]
**Questions asked:** [count]
**Overall confidence rating:** [1-5, based on answer quality average]

### Takeaway

[3-4 sentence executive summary: what happened in the simulation, what the dominant patterns were, what went well, and the single most important thing to fix next.]

### Recruiter Assessment Framework

Real recruiter screening has two dimensions:

| Dimension | Rating | What It Measures |
|-----------|--------|------------------|
| **Checkbox Match** | [1-5] | Did you hit the technical keywords from the job ad? |
| **Trust/Credibility** | [1-5] | "Will this candidate embarrass me if I send them to the client?" |

**Checkbox match:** [X/5] — [brief summary: e.g., "Hit all primary keywords, minor gap on [specific requirement]"]
**Trust/credibility:** [X/5] — [brief summary: e.g., "Strong except for dodging a concrete example on [topic]"]

**Likelihood of being forwarded:** [X/5] — Checkbox × Trust = overall outcome
**Likelihood of strong advocacy:** [X/5] — Would the recruiter champion you or just pass you along?

### Answer-by-Answer Analysis

| # | Topic | Question (summary) | Rating | Trust Impact | Anti-Patterns | Notes |
|---|-------|-------------------|--------|--------------|---------------|-------|
| 1 | Pitch | Self-introduction | 4/5 | ✅ | — | Strong opening, close to coached version |
| 2 | Technical | [Technical requirement] | 2/5 | ❌ | Didn't answer yes/no | Recruiter asked twice, creates doubt |
| ... | | | | | | |

### Anti-Patterns Triggered

- [x] Pattern name — specific example from transcript
- [ ] Pattern name — NOT triggered

### What Went Well
- [bullet points of strongest moments]

### What Needs Work
- [bullet points of weakest moments with coached alternatives]

### Strong Phrasings to Keep
- [any new strong phrasings worth saving to coached-answers.md]

### Deep Review Questions Coverage
- [which tough questions were asked, which weren't, how they were handled]

### Focus for Next Session
- [2-3 specific priorities based on this session's patterns]
```

### Step 5: Discuss with User

Present the debrief report and discuss:
- Ask if the confidence rating feels right
- Ask if any answers felt better/worse than the analysis suggests
- Ask if any strong phrasings should be saved to coached-answers.md
- Confirm the anti-pattern assessment

### Step 6: Log Session

After the user confirms the assessment:

1. **Create session file** — copy `framework/templates/recruiter-session.md` to `coaching/progress-recruiter/YYYY-MM-DD-HHMM-[role-slug].md`. Include:
   - Takeaway (copy from the debrief report)
   - Mode: **Voice simulation**
   - All anti-patterns with checkboxes (checked = triggered)
   - What went well / what needs work
   - Coach's key feedback
   - Strong phrasings to keep
   - Focus for next session

2. **Update summary** at `coaching/progress-recruiter/_summary.md` (if it doesn't exist yet, copy `framework/templates/recruiter-summary.md` first):
   - Increment session count
   - Update last session date
   - Recalculate average confidence rating
   - Update anti-pattern scorecard (increment counts, update "Last Seen", update trends)
   - Add session to the Session Index table

3. **Update coached-answers.md** if the user approved any new strong phrasings.

4. **Update anti-pattern tracker** at `coaching/anti-pattern-tracker.md`:
   - Update status, last-seen, and trend for any pattern triggered or notably absent
   - Move patterns between status categories if warranted (e.g., persistent → resolved after multiple clean sessions)
   - Add new patterns if discovered during the simulation
   - Add a line to the Update Log

5. **Data enrichment** — check if the simulation surfaced new information (project details, achievements, technologies, skills) that should be captured in the data files. Follow the procedure in `framework/data-enrichment.md`.

### Session File Naming

If a session file for this date and role already exists (from a text-based coaching session), append a suffix:
- First session: `2026-02-10-target-role-slug.md`
- Second session same day: `2026-02-10-target-role-slug-v2.md`
- Voice simulation: `2026-02-11-target-role-slug-voice.md` (prefer `-voice` suffix to distinguish from text sessions)
