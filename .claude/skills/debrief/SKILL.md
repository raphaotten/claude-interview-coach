---
name: debrief
description: Debrief a real interview or drill — Nick-first cold scoring against the v0.9+ rubric, then Claude annotates, then ≥1pt disagreements trigger reconciliation. Updates progress/_summary.md, hypotheses.md, anti-pattern-tracker.md.
argument-hint: <path-to-cv-or-call-context>
user-invocable: true
allowed-tools: Read(*), Glob(*), Grep(*), Write(coaching/**), Edit(coaching/**), Write(data/company-notes/**)
---

# /debrief — Cross-call interview debrief

> **MANDATORY READ before writing any output:** `framework/two-tier-capture.md` and `coaching/debrief-rubric.md`. This skill is a synthesis-producing skill operating on voice-corpus material AND a scoring skill bound to a versioned rubric. The principle: raw transcript preserved verbatim with wiki-links + synthesized debrief written separately. Both exist. Never collapse.

## Purpose

Score a single interview call against the 5-dimension rubric, surface
anti-patterns and hypothesis evidence, and propagate updates to the
canonical cross-call view (`coaching/progress/_summary.md`).

## Inputs

- A Granola transcript (live or pasted) OR a session note Nick wrote
- The call's date, target, and (best guess) format tag
- The rubric: `coaching/debrief-rubric.md` (read on every invocation — reference for scoring)
- Active hypotheses: `coaching/hypotheses.md`
- Cross-call view: `coaching/progress/_summary.md`
- Anti-pattern catalog: `coaching/anti-pattern-tracker.md`

## Workflow (mandatory order)

### Step 1: Pull and stage

Pull the transcript via `/granola-pull` if not already provided. Confirm
date, target, and format tag with Nick. Create the per-call file at
`coaching/progress/<YYYY-MM-DD>-<HHMM>-<slug>.md` with metadata block:

```markdown
<!-- session-metadata
format: <compound-tag>
time-pressure: <1|2|3>
structure: <1|2|3>
asymmetry: <1|2|3>
stage: <stage-tag>
holistic-rating: TBD
v0.9-tagged-by: claude-pending-confirm
-->
```

Compound formats: `unstructured-chat | structured-behavioral | founder-vibe-check | peer-screen | technical-deep-dive | drill`.
Stages: `networking | recruiter-screen | hiring-manager | founder-meet | peer-meet | onsite-loop | drill`.
Drill format leaves orthogonal axes blank.

### Step 2: NICK-FIRST SCORING (mandatory gate)

Before producing ANY analysis output, ask Nick to score the call cold:

> "Score 1–5 (half-points OK) on each dimension, with one-line evidence
> in your own words. I'll annotate after you submit."
>
> 1. Format Resilience:
> 2. Delivery Crispness:
> 3. STAR Quality:
> 4. Applied Listening:
> 5. Authenticity:
> Overall (your gut):
> Interviewer signal (low/med/high):

**Do not produce dimension scoring or evidence aggregation before Nick
submits.** This is the polish-anchoring defense (per `feedback_llm_verification_system` memory).

Save Nick's scores to the per-call file under `## Nick's Cold Score`.

### Step 3: Claude annotates

Now read the transcript and rubric. For each dimension:
- Independently score (Claude's read).
- Surface specific evidence Nick may have missed (quoted lines, counts).
- Cross-reference against prior calls (e.g. "filler density of X is up
  Y% vs your last 3 calls").

Save under `## Claude's Annotation`.

### Step 4: Disagreement trigger

For any dimension where Claude's score ≠ Nick's by ≥1 point:
- Generate a `## Reconciliation: Dim N` section
- Show both scores side by side, evidence for each
- Ask Nick to adjudicate: "Keep your score, take mine, or split?"
- Nick's adjudicated score is final.

For dimensions within 0.5 of each other: take Nick's score, no reconciliation needed.

### Step 5: Final scores + interviewer signal

Record final scores under `## Final Scores`:
- Per-dimension (1–5 with half-points)
- Overall (combined; Nick's call)
- Interviewer signal (low/med/high) + one-line evidence

### Step 6: Anti-pattern check

Scan transcript and Nick's evidence for any patterns from
`coaching/anti-pattern-tracker.md`. For each detected:
- Increment count in `_summary.md` Anti-Pattern Scorecard
- Append occurrence to the per-pattern History section in
  `anti-pattern-tracker.md`

For new patterns Nick names: add as `NEW (candidate)` row in `_summary.md`
Anti-Pattern Scorecard, and a new section in `anti-pattern-tracker.md`.

### Step 7: Hypothesis test log

For each Active or Tested hypothesis in `coaching/hypotheses.md`:
- Compute prediction for this call (from claim + format tag)
- Compare to observed scores
- Append a row to that hypothesis's test log:
  `| <date> | <call> | <format> | <pred> | <obs> | Support|Refute|Inconclusive | <note> |`

After appending: check promotion criteria. If met, flag for Nick:
"H<N> meets promotion criteria — review and promote?"

### Step 8: Cross-call correlation surface (judgment-as-wedge)

Compute and surface (NOT propose) any notable cross-call patterns:
- Dimension correlations with format/orthogonal axes (n permitting)
- Recent vs baseline deltas (filler density, anti-pattern counts)
- Predictions from last debrief's "focus for next session" — did they
  hold up?

Present to Nick:
> "Surfaced patterns (suggestive, not statistical at n=<n>): …
> Anything worth registering as a hypothesis?"

If Nick names one: add to `coaching/hypotheses.md` Hypothesis Backlog
section as a Hunch (Ladder: Hunch → Active when Nick promotes).

### Step 9: Propagate updates

Update files in this order (each as a separate atomic write):
1. `coaching/progress/<call-file>.md` — full debrief
2. `coaching/hypotheses.md` — append test log rows, append new hunches
3. `coaching/anti-pattern-tracker.md` — append history entries
4. `coaching/progress/_summary.md` — recompute computed sections, append Session Index row, append Update Log entry

### Step 10: Predictions for next call

Ask Nick: "Based on this debrief, what's the focus for your next
session?" Record under `## Predictions for Next Session` in the per-call
file. `/prep-interview` reads this back at the start of the next call.

## Anti-patterns this skill is designed against

- **Polish anchoring:** Step 2 is mandatory before any Claude output.
- **Status retconning:** Hypothesis test log is append-only; never
  edit a row, even if verdict turns out wrong (add a corrective row).
- **Action-loop drift:** Step 10 is required; `/prep-interview` reads it back.
- **Two-ledger drift:** Anti-pattern counts are canonical in `_summary.md`,
  per-pattern detail lives in `anti-pattern-tracker.md`. Don't maintain
  duplicate counts.

## Memory rules honored

- `feedback_judgment_as_wedge` — Step 2 enforces Nick-first scoring; Step 8 surfaces correlations without proposing hypotheses.
- `feedback_qualitative_vs_binary_verification` — pre-committed rubric (v0.9 → v1) provides scoring scaffold; multi-pass via Step 4 disagreement trigger.
- `feedback_multipass_independent_review` — divergence is signal, not noise.
- `feedback_llm_verification_system` — append-only test log; Nick-first gate; no polish before Nick scores.
- `feedback_two_tier_capture` — raw transcript and synthesized debrief both preserved.
