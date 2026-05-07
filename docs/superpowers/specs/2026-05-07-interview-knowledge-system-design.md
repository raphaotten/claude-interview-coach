# Interview Knowledge System — Design Spec

**Date:** 2026-05-07
**Status:** Draft for Nick review
**Scope:** M layer (~5 hr) — cross-call interview-debrief system with pre-committed rubric, hypothesis registry, and pre-call read-forward
**Origin:** Inbox handoff 2026-05-07; trigger "I don't really think that my debrief skill is working properly"; framing "judgment as part of the system"
**Seed evidence:** `coaching/progress-recruiter/2026-05-07-govra-arc-retrospective.md` (format-fragility hypothesis, drawn from 4 of 5 transcripts)

---

## 1. Problem and Optimization Target

### 1.1 Diagnosed gaps in current `/debrief`

1. No cross-call view — each debrief is self-contained.
2. Fresh-Claude judgment every call — no pre-committed rubric, polish-as-yellow-flag drift risk.
3. Nick's judgment buried under Claude's polish (e.g. Josh debrief has Nick's reflections at the bottom, not structured).
4. No action-loop closure — "focus for next session" prescriptions don't get checked.
5. Format-blind prep — `/prep-interview` and `/debrief` don't talk to each other.

### 1.2 Optimization target (Q1 resolved)

The system optimizes for **C as spine + D as engine + hypothesis loop**:

- **C — Rubric + pattern memory replaces Claude's per-call judgment.** Nick authors a stable rubric. Claude executes against it instead of generating fresh judgment each call. Implements judgment-as-wedge.
- **D — Claude automates cross-call bookkeeping.** Claude does the mechanical aggregation (correlations, frequencies, deltas); Nick does the interpretation.
- **Hypothesis loop.** Patterns surface candidate hypotheses → registered in a registry → tested against the rubric in subsequent calls → promoted to behavior changes when confirmed. Format-fragility is hypothesis #1, not the destination.

### 1.3 Primary design constraint

**Rubric stability over time.** Once dimensions are committed, they must stay stable enough to compare call 3 to call 12. Claude-influence at the rubric-authoring level is acceptable; structural drift in dimensions is not.

---

## 2. Rubric Design

### 2.1 Authorship rule (Q2 resolved)

**Hybrid C: Nick authors dimensions; Claude proposes criteria within them.** Dimensions encode what interview performance *is*. Criteria describe what scores look like at each level. Splitting authorship at this seam preserves judgment-as-wedge while not requiring Nick to author the entire rubric cold.

### 2.2 Five dimensions (Q3 resolved)

| # | Dimension | What it measures |
|---|---|---|
| 1 | **Format resilience** | Adapting when format compresses or asymmetricizes. The Govra hypothesis lives here. |
| 2 | **Delivery crispness** | Filler words, hedging, sentence economy. (Filler counts roll up here, not into format resilience.) |
| 3 | **STAR quality** | Story specificity, quantitative grounding, structural integrity. |
| 4 | **Applied listening** | Picking the *right* story for what they just said; bridging the answer back to the question. Distinct from STAR — "good story" ≠ "right story for this moment." |
| 5 | **Authenticity / un-rehearsed feel** | Actual-Nick voice, not polished-Nick voice. |

### 2.3 Scoring (Q4 resolved)

- **Per-dimension score:** 1–5 scale, half-points permitted, to match existing holistic ratings (e.g. 3.5/5).
- **Self-score:** Nick scores all 5 dimensions cold.
- **Overall score:** Combo of self-score average + interviewer-signal qualifier. Recorded separately. (Holistic ratings of past calls map here.)
- **Interviewer signal (NOT a self-rated dimension):** rapport-energy match, drill-deeper behavior, follow-up questions, lean-in cues. Tracked as `low | med | high` with one-line evidence per call.

### 2.4 Criteria authoring sequence

1. Nick commits to the 5 dimension names (this spec).
2. Claude reads all 5 transcripts + 9 existing session files and proposes scoring criteria within each dimension (what 1, 3, 5 looks like).
3. Nick edits the criteria until they're his.
4. Rubric is locked. Future criteria changes require explicit version bump (see §6).

### 2.5 Rubric file

`coaching/debrief-rubric.md` — single source of truth. Format:

```markdown
# Debrief Rubric (v1, locked 2026-05-XX)

## Dimension 1: Format Resilience
What it measures: …
Scoring:
  5 — …
  3 — …
  1 — …
Common evidence cues: …
```

---

## 3. Workflow

### 3.1 Debrief workflow (Q5 resolved): B-with-disagreement-trigger

1. **Pull transcript.** `/granola-pull` or paste, as today.
2. **Format tagging.** Nick tags the call: format (compound) + orthogonal scores + stage. See §5.
3. **Nick scores cold.** All 5 dimensions, brief evidence in his own words. No Claude output yet. Saved into the per-call file before Claude runs.
4. **Claude annotates.** Reads transcript + Nick's scores. For each dimension: agree/disagree, surfaced evidence Nick missed, pattern matches against prior calls (e.g. "this 'kind of' count is up 40% vs your last 3 calls").
5. **Disagreement trigger.** If Claude's score diverges from Nick's by ≥1 point on any dimension, generate a reconciliation note: side-by-side evidence, which Nick adjudicates. Final score is whichever Nick keeps after reading.
6. **Overall score + interviewer signal recorded** in the per-call file (`coaching/progress/<date>-<call>.md`) under structured headers.
7. **Update propagation:** anti-pattern frequencies → `_summary.md` Anti-Pattern Scorecard (recomputed); hypothesis test log rows → `hypotheses.md` (appended); session entry → `_summary.md` Session Index (appended); per-call file → `coaching/progress/<date>-<call>.md` (created/updated).

This is the **Nick-first scoring gate**. Solves Gap #3 (Nick's judgment buried under Claude's polish).

### 3.2 Pre-call read-forward (Q7 resolved): extend `/prep-interview`

`/prep-interview` already covers cheat sheet, drilling, and company/role/interviewer research. M extends it with three new sections sourced from the system:

1. **Active anti-patterns to watch for** — top 3 by frequency from `_summary.md` Anti-Pattern Scorecard, with most recent occurrence and defense (one line each).
2. **Promoted hypotheses for this format** — pull from `hypotheses.md` where status = Promoted and format-tag matches anticipated call format. Inject behavior-change rule directly.
3. **Last debrief's "focus for next session"** — predicted commitments. Surfaces predictions-vs-outcomes loop closure (Gap #4).

Solves Gap #5 (format-blind prep).

### 3.3 Cross-call view (Q8 resolved): upgrade `_summary.md`, no new files

The cross-call view *already exists* as `coaching/progress-recruiter/_summary.md`. M upgrades it in place:

- **Session Index** gains 5 dimension columns (one per rubric dimension) plus format tag and interviewer-signal column.
- **New section: Format-Stratified View** — dimension averages grouped by compound format tag.
- **Anti-Pattern Scorecard** — declared canonical cross-call rollup. `coaching/anti-pattern-tracker.md` becomes the per-pattern detail view (one row per pattern with mechanism, defense, history); counts and trends come from `_summary.md`.
- **Hypothesis Status Board** — new section pulling from `hypotheses.md`. Promoted hypotheses bolded.

**Auto-refresh semantics:** After each debrief, computed sections (Anti-Pattern Scorecard, Format-Stratified View, Hypothesis Status Board, Overall Status metrics) are recomputed and overwritten. Append-only sections (Session Index, Update Log) gain a new entry but never lose old ones. Append-only history already exists in dated per-call files (`coaching/progress/<date>-<call>.md`) and the Update Log in `_summary.md`. No new history file needed.

**On-demand:** `/cross-call-view` (or invocation from `/standup`, `/weekly-review`) reads `_summary.md` as currently rendered. No regeneration required for read access.

---

## 4. Hypothesis Registry

### 4.1 Generation rule (Q6a resolved): C — Claude surfaces correlations, Nick interprets

Claude does not propose hypotheses as such. After each debrief, Claude surfaces *notable cross-call patterns numerically* (e.g. "dimension 4 correlates -0.7 with `asymmetry` score across n=9 — flagging for interpretation"). Nick reads the patterns and decides whether to register a hypothesis.

This handles small-N honestly: with 5–15 calls, "correlations" are suggestive, not statistical. Surfacing them without naming them as hypotheses keeps the rigor honest.

### 4.2 Schema (Q6b resolved): claim + mechanism + boundary, append-only test log, promotion ladder

Each hypothesis combines three rigor patterns:

- **Decomposed (claim + mechanism + boundary)** — forces a theory, not just a pattern.
- **Append-only test log** — kills retcon risk; current state computed from log, not stated.
- **Promotion ladder with explicit behavior change** — closes the action loop.

Schema:

```markdown
## H1: Format-fragility

Registered: 2026-05-07
Origin: 2026-05-07-govra-arc-retrospective.md

Claim:     Scores on dims 1, 2, 4 degrade in time-compressed
           asymmetric formats vs unstructured.
Mechanism: Compression denies time to think → falls back to
           rehearsed STAR → applied listening collapses.
Boundary:  Should hold for recruiter screens <30 min and
           founder vibe-checks. Should NOT hold for technical
           deep-dives or peer-style intros even when short.

Ladder state: Active   (Hunch → [Active] → Tested → Confirmed → Promoted)

Promotion criteria:
  - n ≥ 5 tested calls
  - ≥ 4 support
  - ≥ 0 strong refute

Behavior change on Promote:
  - Pre-call read-forward flags format type and injects
    "compression drill" if compressed format expected.
  - Update rubric criteria for dim 1 to weight format-shift
    moments more heavily.

Test log (append-only):
| Date       | Call           | Format               | Pred  | Obs   | Verdict   | Note |
|------------|----------------|----------------------|-------|-------|-----------|------|
| 2026-05-05 | Govra/Sam      | unstructured-chat    | high  | 4.5/5 | Support   | …    |
| 2026-05-06 | Govra/Josh     | founder-vibe-check   | low   | 2.5/5 | Support   | …    |
| 2026-05-05 | Formic/Theresa | structured-behavioral| low   | 2.5/5 | Support   | …    |
| 2026-04-20 | Feltsense/Matt | peer-screen          | mid   | 3.0/5 | Inconcl.  | …    |
| 2026-04-28 | TBV/Steven     | unstructured-chat    | high  | 2.5/5 | Refute    | …    |
```

Note the Steven Lurie row: it's a **refute on the seed hypothesis** (unstructured but scored low). That row is preserved exactly because it's the kind of evidence the append-only design is meant to protect.

### 4.3 Skipped patterns and why

- **Pre-registered scientific (option 2):** sample sizes too small for real decision rules. Revisit at n=15.
- **Tetlock-style probabilistic forecasts (option 5):** heaviest cognitive load; not enough calls for Brier scores to mean anything. Revisit at n=30.

### 4.4 Hypothesis file

`coaching/hypotheses.md` — registry. Seeded with H1 (format-fragility) at v1 build, pre-loaded with 5 existing calls as test log entries.

---

## 5. Format Tagging

### 5.1 Approach (Q9 resolved): compound primary, orthogonal secondary

Each call is tagged with both a compound name (legible) and three orthogonal scores (analyzable when n grows).

### 5.2 Compound formats (5)

| Tag | Definition | Existing examples |
|---|---|---|
| `unstructured-chat` | Generous time, free-flowing, peer/advisor framing, Nick can lead | Sam Lazarus (4.5), Tessa Lau (3.5), Steven Lurie (2.5) |
| `structured-behavioral` | Checklist of behavioral questions, recruiter or HM running the clock | Theresa Dobson (2.5) |
| `founder-vibe-check` | Short, chemistry-driven, founder-led, fast pattern-match judgment | Josh Sandler (2.5) |
| `peer-screen` | Recruiter screen conducted by a peer/operator who's also evaluating | Matt Wood (3) |
| `technical-deep-dive` | Domain probing, ops/data/strategy depth, slower pace | (anticipated) |

### 5.3 Orthogonal axes (3, scored 1–3 each)

- **Time pressure** — 1 = spacious, 2 = mid, 3 = compressed
- **Structure** — 1 = free-flowing, 2 = mid, 3 = scripted/checklist
- **Asymmetry** — 1 = collaborative, 2 = mid, 3 = evaluative

Scores live in per-call file metadata. Surfaced in `_summary.md` Session Index. Become the dataset for correlation analysis once n ≥ 20.

### 5.4 Stage (orthogonal metadata, NOT format)

Tracked separately for pipeline cross-reference, not used in fragility scoring:
`networking | recruiter-screen | hiring-manager | founder-meet | peer-meet | onsite-loop | drill`

### 5.5 Drills

Drills are scored on the rubric (filler counts and crispness still measure something) but **excluded from format-fragility hypothesis test logs.** Drill sessions get `format: drill, stage: drill`.

### 5.6 Retroactive tagging

All 9 existing sessions get format-tagged during v1 build. Prospective tagging applies from first new debrief forward.

---

## 6. File Structure and Migration

### 6.1 Folder collapse (Q10 resolved)

`coaching/progress-recruiter/` and `coaching/progress-interview/` → single `coaching/progress/`. The recruiter/interview distinction has no teeth in practice (`progress-recruiter/` already contains a CEO first round and a VC intro), and the rubric is format-agnostic.

### 6.2 Final state

```
coaching/
├── debrief-rubric.md            NEW — 5 dimensions, criteria, locked v1
├── hypotheses.md                NEW — registry, seeded with H1
├── anti-pattern-tracker.md      KEPT, repositioned — per-pattern detail view
├── coached-answers.md           UNCHANGED
├── pressure-points.md           UNCHANGED
├── ai-fluency-interview-spine.md UNCHANGED
└── progress/                    REPLACES progress-recruiter + progress-interview
    ├── _summary.md              UPGRADED — dimension columns, format-stratified view, hypothesis status board
    └── <date>-<call>.md         per-call files (migrated + new)
```

### 6.3 Anti-pattern ledger reconciliation

Two ledgers exist today (`anti-pattern-tracker.md` Occurrences column shows 7 for filler; `_summary.md` Anti-Pattern Scorecard shows 11). M makes `_summary.md` Anti-Pattern Scorecard canonical for counts and trends. `anti-pattern-tracker.md` becomes per-pattern detail (one row per pattern with mechanism, defense, history) but no longer maintains its own Occurrences count. The current Update Log in tracker.md migrates to `_summary.md` Update Log (already partially duplicated there).

### 6.4 Migration steps (covered in implementation plan, not here)

1. Create `coaching/progress/`.
2. Move 9 session files from `progress-recruiter/` to `progress/`. Delete empty `progress-interview/`.
3. Add format tags + orthogonal scores to each migrated session (Nick-driven, Claude-assisted; the Govra retrospective already informs most of these).
4. Upgrade `_summary.md` schema. Backfill dimension columns for sessions where transcripts exist (5 calls); leave older sessions with holistic rating only and a one-line note.
5. Author `debrief-rubric.md` (Nick dimensions, Claude criteria draft, Nick edits, lock).
6. Seed `hypotheses.md` with H1.
7. Reposition `anti-pattern-tracker.md` (drop Occurrences column, expand mechanism/defense, link to `_summary.md` for counts).
8. Rewrite `/debrief` skill to enforce Nick-first gate + disagreement trigger.
9. Extend `/prep-interview` skill with three new sections (active anti-patterns, promoted hypotheses, last-session focus).

---

## 7. Versioning and Stability

The rubric is the load-bearing artifact. Stability rules:

- **Locked version:** Each `debrief-rubric.md` carries a version (`v1`) and lock date. All scores reference the version they were scored under.
- **Adding a dimension** is a major version bump (v1 → v2). Old scores stay locked at v1; new calls scored under v2; cross-version comparisons flagged in views.
- **Changing criteria within a dimension** is a minor version bump (v1.0 → v1.1). Old scores stay; nothing else changes; minor versions are fine to churn.
- **Removing a dimension** is also major. Old scores preserved; that column drops from the active Session Index.

Hypotheses do not version — they live, get tested, get promoted or refuted. The append-only log preserves their history.

---

## 8. What's Out of Scope (Deferred to L)

- Pre-call format predictor (auto-classify the format from job ad / interviewer / company)
- Drill recommender (suggest which drill to run based on format + active anti-patterns)
- Multi-pass independent review (full option C from Q5 — second-Claude or human reviewer)
- Tetlock-style probabilistic hypothesis forecasting
- Pre-registered decision rules with sample sizes
- Cross-folder integration (interview-stage gets the same treatment when first real interview-stage call arrives — same files, no rebuild)

---

## 9. Resolved Decisions Reference

| Q | Decision |
|---|---|
| Q1 — what M optimizes for | C + D + hypothesis loop; format-fragility is H1 |
| Q2 — rubric authorship | Hybrid C: Nick dimensions, Claude criteria, Nick edits |
| Q3 — dimensions | Format resilience, Delivery crispness, STAR quality, Applied listening, Authenticity |
| Q4 — applied listening + signal | Applied listening = own dimension; rapport-energy = interviewer signal, not self-axis |
| Q5 — workflow | B-with-disagreement-trigger (Nick scores cold → Claude annotates → ≥1pt diverge = reconciliation) |
| Q6 — hypothesis schema | Claim+Mechanism+Boundary + append-only log + promotion ladder |
| Q6a — hypothesis generation | C: Claude surfaces correlations, Nick interprets |
| Q7 — pre-call integration | Extend `/prep-interview` (option A) |
| Q8 — cross-call view | Upgrade `_summary.md` in place; auto-refresh + on-demand; no new files |
| Q9 — format tagging | Compound primary (5 tags) + orthogonal secondary (3 axes, 1–3) |
| Q10 — folder structure | Collapse `progress-recruiter/` + `progress-interview/` → `progress/` |
| Q11 — scoring scale | 1–5, half-points, matches existing holistic ratings |

---

## 10. Memory Rules Honored

- `feedback_judgment_as_wedge` — Nick authors dimensions; Nick-first scoring gate; Nick interprets correlations into hypotheses; promotion changes behavior
- `feedback_qualitative_vs_binary_verification` — pre-committed rubric + measurement-over-time + multi-pass review (B-with-stub-of-C)
- `feedback_multipass_independent_review` — disagreement trigger surfaces divergence as signal
- `feedback_llm_verification_system` — append-only logs prevent retcon; Nick-first prevents polish from anchoring
- `feedback_demand_signal_vs_dopamine_signal` — demand signal real (named annoyance + 5-call manual friction)
- `feedback_infrastructure_during_search` — hot ROI loop, gates met
