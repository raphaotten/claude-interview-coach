# Interview Knowledge System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (recommended for this plan — markdown-file authorship, no test framework). Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stand up a cross-call interview-debrief system with a pre-committed rubric, hypothesis registry, format tagging, and pre-call read-forward — implementing the M layer per spec.

**Architecture:** Markdown-only. Two new canonical files (`coaching/debrief-rubric.md`, `coaching/hypotheses.md`), one folder collapse (`progress-recruiter/` + `progress-interview/` → `progress/`), one schema upgrade (`_summary.md` gains dimension columns + format-stratified view + hypothesis board), two skill rewrites (`/debrief`, `/prep-interview`).

**Tech Stack:** Markdown, shell (`mv`, `find`, `grep`), git. No build, no tests, no Python. Verification = file-existence + section-presence + grep-pattern checks.

**Spec:** `docs/superpowers/specs/2026-05-07-interview-knowledge-system-design.md`

**Two interactive points** (cannot be fully autonomized):
1. Rubric criteria — Claude drafts (v0.9), Nick edits and locks (v1).
2. Retroactive format tagging — Claude proposes from session notes; Nick confirms on return.

Both are landed in committed v0.9 state so the system is usable; Nick finalizes interactively.

---

## Task 1: Folder collapse and session migration

**Files:**
- Create: `coaching/progress/`
- Move: `coaching/progress-recruiter/*.md` → `coaching/progress/`
- Delete: `coaching/progress-interview/` (empty after `_summary.md` is gone, see Task 5)
- Delete: `coaching/progress-recruiter/` (empty after move)

The `progress-interview/_summary.md` is a 0-session scaffold — its content is fully superseded by `progress/_summary.md` (Task 5), so this file is deleted, not migrated.

- [ ] **Step 1.1: Verify current state**

Run:
```bash
ls coaching/progress-recruiter/ | wc -l
ls coaching/progress-interview/
```
Expected: 13 files in `progress-recruiter/` (11 session files + `_summary.md` + the 2026-05-07 retrospective), 1 file in `progress-interview/` (`_summary.md` only).

- [ ] **Step 1.2: Create new folder**

Run:
```bash
mkdir -p coaching/progress
```

- [ ] **Step 1.3: Move session files**

Run:
```bash
git mv coaching/progress-recruiter/*.md coaching/progress/
```

This includes `_summary.md` from `progress-recruiter/`. The retrospective file (`2026-05-07-govra-arc-retrospective.md`) moves with the rest.

- [ ] **Step 1.4: Delete the empty progress-interview scaffold**

Run:
```bash
git rm coaching/progress-interview/_summary.md
rmdir coaching/progress-interview
```

- [ ] **Step 1.5: Remove the now-empty progress-recruiter directory**

Run:
```bash
rmdir coaching/progress-recruiter
```

- [ ] **Step 1.6: Verify migration**

Run:
```bash
ls coaching/progress/ | wc -l
test ! -d coaching/progress-recruiter && test ! -d coaching/progress-interview && echo "OK"
```
Expected: 13 files in `coaching/progress/`. "OK" printed.

- [ ] **Step 1.7: Commit**

```bash
git add -A coaching/
git commit -m "$(cat <<'EOF'
refactor(coaching): collapse progress-recruiter + progress-interview into progress/

Per interview-knowledge-system spec: stage distinction has no teeth in
practice (progress-recruiter already mixes recruiter screens, founder
calls, and VC intros). Format tagging carries the meaningful axis.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: Author `coaching/debrief-rubric.md` (v0.9 draft)

**Files:**
- Create: `coaching/debrief-rubric.md`
- Read for context: `data/voice-corpus/granola/` (5 transcript pairs), `coaching/progress/_summary.md`, `coaching/anti-pattern-tracker.md`

**Approach:** Write 5 dimensions with 1/3/5 anchor descriptions per dimension. Ground criteria in observed evidence from the 5 transcripts (e.g. dim 2 "filler crispness" anchors come from actual filler-count data). Mark file `v0.9 — awaiting Nick lock`.

- [ ] **Step 2.1: Read seed material**

Read these files to ground the criteria in real evidence:
- `coaching/progress/2026-05-05-1215-govra-sam-screen.md` (4.5/5 — top of range)
- `coaching/progress/2026-05-06-1500-govra-josh-founder.md` (2.5/5 — bottom)
- `coaching/progress/2026-05-05-1315-formic-theresa-screen.md` (2.5/5)
- `coaching/progress/2026-05-07-govra-arc-retrospective.md` (cross-call synthesis)
- `coaching/anti-pattern-tracker.md` (anti-pattern catalog)

- [ ] **Step 2.2: Write the rubric file**

Create `coaching/debrief-rubric.md`:

```markdown
# Debrief Rubric

**Status:** v0.9 — draft, awaiting Nick lock
**Locked version:** (pending)
**Origin spec:** docs/superpowers/specs/2026-05-07-interview-knowledge-system-design.md

> Five dimensions, each scored 1–5 with half-points permitted. Nick scores
> cold (no Claude output yet). Claude annotates after. Disagreements ≥1pt
> trigger reconciliation. See `/debrief` skill for workflow.

---

## Dimension 1: Format Resilience

**What it measures:** How well Nick adapts his delivery when the format
compresses, switches, or gets asymmetric mid-call. The Govra-Sam-vs-Josh
gap lives here. NOT about delivery mechanics (those are dim 2).

**Scoring anchors:**
- **5 — Resilient.** Format shift detected and absorbed; pace adjusted; no
  visible degradation. Holds operator framing under push.
- **3 — Adequate.** Notices format pressure; partially adapts; one visible
  break (chronological reversion, caved when steered) but recovers.
- **1 — Brittle.** Format pressure not detected or not absorbed; reverts
  to chronological walkthrough or rehearsed STAR; absorbs reframes
  without defending thesis.

**Common evidence cues:** time-pressure markers ("we have 15 min left"),
asymmetric drilling, format switches mid-call, push-back moments.

---

## Dimension 2: Delivery Crispness

**What it measures:** Filler words ("kind of", "really", "definitely",
"pretty", "absolutely", "to be honest"), hedging, sentence economy.
Mechanical, countable.

**Scoring anchors:**
- **5 — Crisp.** Filler density <2/min. No hedging. Sentences end where
  they should. Govra/Sam call ≈ this.
- **3 — Adequate.** Filler density 3–6/min. Occasional hedge. Some
  sentences trail or restart.
- **1 — Cluttered.** Filler density >8/min. Hedging on most answers.
  Feltsense/Matt baseline ("really" x12, "kind of" x14) sits here.

**Common evidence cues:** raw filler counts from transcript; ending words
("…right?", "…I guess"); throat-clearing openers.

---

## Dimension 3: STAR Quality

**What it measures:** Story specificity, quantitative grounding,
structural integrity. The "good story" axis. About *whether the story
itself is well-built* — not whether it's the right one for the moment
(that's dim 4).

**Scoring anchors:**
- **5 — Sharp.** Concrete numbers, named outcomes, clear S→T→A→R arc, no
  hand-waving. ESPN $2M ad-bug story when delivered fully ≈ this.
- **3 — Adequate.** Specific enough but missing one element (often R or
  the quantitative anchor). Arc holds but soft on outcomes.
- **1 — Vague.** Process narration ("I would want to understand…");
  generic phrasing; no numbers; no clear result.

**Common evidence cues:** number density in answer; named-vs-generic
nouns; presence of "I" vs "we"; explicit outcome statement.

---

## Dimension 4: Applied Listening

**What it measures:** Picking the *right* story for what they just said.
Bridging the answer back to the question. The "in-the-moment matching"
axis. Distinct from dim 3 — a great story told in answer to the wrong
question scores high on dim 3, low on dim 4.

**Scoring anchors:**
- **5 — Tight match.** Story selected fits the specific framing of the
  question; explicit bridge ("you mentioned X — that maps to…");
  answer terminates where the question pointed.
- **3 — Adequate.** Story is in the right general territory; bridge is
  implicit; minor drift between question and answer.
- **1 — Mismatch.** Default story deployed regardless of question;
  ESPN/McKinsey defaulted when Zuora was asked; rehearsed answer pasted
  in without listening to the actual question. Formic "vague ownership"
  moment ≈ this.

**Common evidence cues:** repeating back the question's framing in your
answer; named bridge phrase; answer-terminator alignment with question.

---

## Dimension 5: Authenticity / Un-rehearsed Feel

**What it measures:** Actual-Nick voice vs polished-Nick voice. The
"polish-as-yellow-flag" axis from the LLM verification memory. About
whether the answer sounds like it was just thought of, not just played
back.

**Scoring anchors:**
- **5 — Authentic.** Answer has texture — pause, qualifier, surprise.
  Nick's voice. "Bug of building" line ≈ this.
- **3 — Adequate.** Mostly natural with one or two visibly-rehearsed
  phrases. Coached frame visible but not dominant.
- **1 — Over-rehearsed.** Answer sounds like a rehearsed track; phrasing
  identical to the prep cheat sheet; no in-the-moment texture; same
  framing reused across consecutive calls (Formic "expertise" framing
  reused from Govra ≈ this).

**Common evidence cues:** identical phrasings across calls; cheat-sheet-
quote density; absence of qualifier or in-the-moment correction.

---

## Interviewer Signal (NOT a self-rated dimension)

Recorded as a separate field per call. Three levels:
- **high** — drilling deeper, follow-up questions, lean-in cues, "tell me
  more about", positive verbal markers.
- **med** — neutral pacing, completes their script, no strong tells.
- **low** — disengaged, terse, transactional, accelerating to close.

One-line evidence required per call.

---

## Versioning

- **v0.9** — initial draft (this document). Criteria proposed by Claude
  from 5-transcript corpus + session files.
- **v1.0** — locked version once Nick edits criteria.
- Adding/removing a dimension = major bump (v1 → v2). Old scores frozen.
- Editing criteria within a dimension = minor bump (v1.0 → v1.1). Old
  scores stay; minor versions can churn.
```

- [ ] **Step 2.3: Verify**

Run:
```bash
test -f coaching/debrief-rubric.md && grep -c "^## Dimension" coaching/debrief-rubric.md
```
Expected: file exists; output `5` (five dimension headers).

- [ ] **Step 2.4: Commit**

```bash
git add coaching/debrief-rubric.md
git commit -m "$(cat <<'EOF'
feat(coaching): add debrief-rubric.md v0.9 (5 dimensions, awaiting Nick lock)

Per spec §2: hybrid-C authorship — Nick committed dimensions, Claude
proposed criteria from 5-transcript corpus. Awaits Nick edits to lock v1.

Dimensions: Format Resilience, Delivery Crispness, STAR Quality, Applied
Listening, Authenticity. Interviewer signal tracked as separate field.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: Author `coaching/hypotheses.md` with H1 seeded

**Files:**
- Create: `coaching/hypotheses.md`
- Read for context: `coaching/progress/2026-05-07-govra-arc-retrospective.md` (already articulates H1)

- [ ] **Step 3.1: Write the registry file**

Create `coaching/hypotheses.md`:

```markdown
# Hypothesis Registry

**Origin spec:** docs/superpowers/specs/2026-05-07-interview-knowledge-system-design.md
**Updated by:** `/debrief` (test log appends), Nick (status changes, registrations)

> Hypotheses about Nick's interview performance. Each carries claim +
> mechanism + boundary. Test log is append-only — no row is ever edited
> or deleted. Status is computed from the log + ladder position, not
> stated as a free-text field.
>
> Ladder: **Hunch → Active → Tested(n) → Confirmed → Promoted**
>
> Promoted hypotheses *change behavior* — they alter rubric criteria,
> pre-call read-forward, or skill workflows. A hypothesis that promotes
> without naming a behavior change is incomplete.

---

## H1: Format-fragility

**Registered:** 2026-05-07
**Origin:** `coaching/progress/2026-05-07-govra-arc-retrospective.md`

**Claim:** Scores on dimensions 1 (Format Resilience), 2 (Delivery
Crispness), and 4 (Applied Listening) degrade in time-compressed
asymmetric formats vs unstructured collaborative ones.

**Mechanism:** Compression denies time to think → Nick falls back to
rehearsed STAR → applied listening collapses → filler density rises as a
stalling tactic.

**Boundary:** Should hold for `structured-behavioral` and
`founder-vibe-check` formats. Should NOT hold for `technical-deep-dive`
(slower pace, depth-friendly) or `peer-screen` (collaborative framing
even when short). Should also NOT hold for `unstructured-chat` even
when stakes are high.

**Ladder state:** Active

**Promotion criteria:**
- n ≥ 5 tested calls (real, not drills)
- ≥ 4 verdicts of Support
- ≥ 0 Strong-Refute verdicts (1 Strong-Refute blocks promotion)

**Behavior change on Promote:**
- `/prep-interview` flags anticipated format and injects a "compression
  drill" if compressed-format expected (≥10 min before call).
- Rubric dim 1 criteria gain explicit weight on format-shift moments.

### Test log (append-only)

| Date | Call | Format | Pred (dims 1+2+4 avg) | Obs (dims 1+2+4 avg) | Verdict | Note |
|------|------|--------|-----------------------|----------------------|---------|------|
| 2026-05-05 | Govra/Sam | unstructured-chat | high (≥4) | TBD | Pending v0.9 rubric | Holistic 4.5/5; awaiting dimension scores |
| 2026-05-06 | Govra/Josh | founder-vibe-check | low (≤3) | TBD | Pending v0.9 rubric | Holistic 2.5/5; awaiting dimension scores |
| 2026-05-05 | Formic/Theresa | structured-behavioral | low (≤3) | TBD | Pending v0.9 rubric | Holistic 2.5/5; awaiting dimension scores |
| 2026-04-28 | TBV/Steven | unstructured-chat | high (≥4) | TBD | Pending — likely Refute | Holistic 2.5/5; **format predicts high but call scored low — possible refute, possible confound (caved-when-steered, volunteered negative). Capture the row regardless per append-only rule.** |
| 2026-04-20 | Feltsense/Matt | peer-screen | mid (3–4) | TBD | Pending v0.9 rubric | Holistic 3/5; peer-screen is boundary case |

> **Note on the Steven Lurie row:** preserved as a candidate refute. The
> append-only design exists specifically to protect rows like this from
> retcon. If anti-pattern confounds drove the low score (not format),
> the verdict column will say "Refute (confounded)" once dimension scores
> exist. Either way, the row stays.

---

## Hypothesis backlog (Hunches not yet registered)

> Patterns Claude has surfaced as numerically suggestive but not yet
> theorized. Nick promotes to a registered hypothesis when ready.

*(populated by `/debrief` cross-call correlation step)*

---

## Promoted hypotheses (behavior-change rules)

> Once a hypothesis hits Promoted, its behavior-change clause is
> mirrored here for fast lookup by `/prep-interview` and `/debrief`.

*(none yet — H1 is Active)*
```

- [ ] **Step 3.2: Verify**

Run:
```bash
test -f coaching/hypotheses.md && grep -c "^## H[0-9]" coaching/hypotheses.md
```
Expected: file exists; output `1` (H1 registered).

- [ ] **Step 3.3: Commit**

```bash
git add coaching/hypotheses.md
git commit -m "$(cat <<'EOF'
feat(coaching): add hypotheses.md registry seeded with H1 format-fragility

Per spec §4: claim+mechanism+boundary + append-only test log + promotion
ladder. Skip pre-registered decision rules (option 2) and Tetlock-style
forecasts (option 5) at small-N.

H1 seeded with 5 calls including the Steven Lurie candidate-refute row,
preserved per append-only design. Verdict columns marked Pending until
v0.9 rubric scoring runs.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: Format-tag the existing sessions

**Files:**
- Modify: each `coaching/progress/<date>-<call>.md` (11 sessions; `_summary.md` and the 2026-05-07 retrospective are skipped)
- Reference: existing session content for tag inference

**Approach:** Add a YAML-style metadata block at the top of each session file (between H1 and first content). Block format:

```markdown
<!-- session-metadata
format: <compound-tag>
time-pressure: <1|2|3>
structure: <1|2|3>
asymmetry: <1|2|3>
stage: <stage-tag>
holistic-rating: <X.Y/5>
v0.9-tagged-by: claude (awaiting Nick confirmation)
-->
```

Tag assignments (Claude's draft based on session notes — Nick confirms):

| File (date prefix) | Format | TP | Str | Asym | Stage |
|---|---|---|---|---|---|
| 2026-04-28-...steven-lurie | unstructured-chat | 1 | 1 | 2 | networking |
| 2026-04-20-...matt-wood | peer-screen | 2 | 2 | 2 | recruiter-screen |
| 2026-05-05-...sam-screen | unstructured-chat | 1 | 1 | 1 | recruiter-screen |
| 2026-05-05-...formic-theresa-screen | structured-behavioral | 3 | 3 | 3 | recruiter-screen |
| 2026-05-06-...govra-josh-founder | founder-vibe-check | 3 | 1 | 3 | founder-meet |
| 2026-05-05-...govra-opener-drill | drill | — | — | — | drill |
| 2026-05-06-...govra-josh-prep-drill | drill | — | — | — | drill |
| 2026-03-13-...belfiore-farr-quiz | drill | — | — | — | drill |
| 2026-03-13-...belfiore-farr-call | unstructured-chat | 1 | 1 | 2 | networking |
| 2026-03-13-...dusty-robotics-ceo | unstructured-chat | 2 | 2 | 2 | hiring-manager |
| 2026-03-10-...amae-health-so | drill | — | — | — | drill |
| 2026-05-07-govra-arc-retrospective | (skip — meta) | — | — | — | — |

Drill rows leave TP/Str/Asym blank (not applicable per spec §5.5).

- [ ] **Step 4.1: List session files**

Run:
```bash
ls coaching/progress/*.md
```
Expected: 13 files (11 session files + `_summary.md` + retrospective).

- [ ] **Step 4.2: Add metadata block to each session file**

For each session file (excluding `_summary.md` and the retrospective), prepend the metadata block right after the first H1 line. Example for the Sam screen:

```bash
# Read coaching/progress/2026-05-05-1215-govra-sam-screen.md
# Find first line starting with "# "
# Insert immediately after:
#
# <!-- session-metadata
# format: unstructured-chat
# time-pressure: 1
# structure: 1
# asymmetry: 1
# stage: recruiter-screen
# holistic-rating: 4.5/5
# v0.9-tagged-by: claude (awaiting Nick confirmation)
# -->
```

Use the Read+Edit pattern per file. Apply tags from the table above.

- [ ] **Step 4.3: Verify**

Run:
```bash
grep -l "session-metadata" coaching/progress/*.md | wc -l
```
Expected: 11 (every session file; `_summary.md` and the retrospective skipped).

- [ ] **Step 4.4: Commit**

```bash
git add coaching/progress/
git commit -m "$(cat <<'EOF'
feat(coaching): retroactively format-tag 10 existing sessions

Per spec §5: compound primary (5 named formats) + orthogonal secondary
(time-pressure, structure, asymmetry; 1-3 each). Drill sessions tagged
format=drill, orthogonal axes blank.

v0.9 tags drafted by Claude from session notes; awaiting Nick
confirmation on return.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: Upgrade `coaching/progress/_summary.md` schema

**Files:**
- Modify: `coaching/progress/_summary.md`

**Approach:** Restructure into the schema that supports M. Preserve all existing data. Add 5 dimension columns (with TBD until rubric is v1 and dimensional scoring runs), Format-Stratified View section, Hypothesis Status Board section. Declare Anti-Pattern Scorecard the canonical cross-call rollup.

- [ ] **Step 5.1: Read current state**

Read `coaching/progress/_summary.md` to capture all existing data (Anti-Pattern Scorecard rows, Session Index entries, Progress Notes).

- [ ] **Step 5.2: Rewrite the file**

The new schema (full content — preserve all existing data, add new sections):

```markdown
# Interview Coaching — Progress Summary

> **Canonical cross-call view.** Anti-Pattern Scorecard counts and trends
> are authoritative here (not in `anti-pattern-tracker.md`, which is now
> per-pattern detail). Updated by `/debrief` after each session.
>
> Computed sections (Anti-Pattern Scorecard, Format-Stratified View,
> Hypothesis Status Board, Overall Status) are recomputed and overwritten.
> Append-only sections (Session Index, Update Log) only gain new rows.

## Overall Status

| Metric | Current | Target |
|--------|---------|--------|
| Sessions completed (real) | 7 | — |
| Sessions completed (drill) | 3 | — |
| Avg. confidence rating | 3.0/5 | 4+ / 5 |
| Top recurring anti-pattern | Filler hedging (11 across sessions) | — |
| Last session | 2026-05-06 (Govra Josh founder, 2.5/5) | — |
| Rubric version | v0.9 (draft, awaiting Nick lock) | v1.0 locked |

## Per-Dimension Trend (Real Calls Only)

> Backfilled where transcripts permit; older sessions rated holistically only.
> Columns: dim 1 (Format Resilience), dim 2 (Delivery Crispness), dim 3 (STAR Quality),
> dim 4 (Applied Listening), dim 5 (Authenticity).

| Date | Call | Format | Dim 1 | Dim 2 | Dim 3 | Dim 4 | Dim 5 | Overall | Int. Signal |
|------|------|--------|-------|-------|-------|-------|-------|---------|-------------|
| 2026-05-06 | Govra/Josh | founder-vibe-check | TBD | TBD | TBD | TBD | TBD | 2.5/5 | low |
| 2026-05-05 | Formic/Theresa | structured-behavioral | TBD | TBD | TBD | TBD | TBD | 2.5/5 | med |
| 2026-05-05 | Govra/Sam | unstructured-chat | TBD | TBD | TBD | TBD | TBD | 4.5/5 | high |
| 2026-04-28 | TBV/Steven | unstructured-chat | TBD | TBD | TBD | TBD | TBD | 2.5/5 | med |
| 2026-04-20 | Feltsense/Matt | peer-screen | TBD | TBD | TBD | TBD | TBD | 3.0/5 | med |
| 2026-03-13 | Dusty/Tessa | unstructured-chat | TBD | TBD | TBD | TBD | TBD | 3.5/5 | high |
| 2026-03-13 | Belfiore/Farr | unstructured-chat | TBD | TBD | TBD | TBD | TBD | 2.5/5 | med |

> Dimension scores will populate once v1 rubric is locked and `/debrief` runs against new calls.
> Backfill of past calls against v1 rubric is optional and at Nick's discretion.

## Format-Stratified View

> Dimension averages grouped by compound format tag. Format-fragility (H1) test bed.

| Format | n (real) | Avg Overall | Avg Dim 1 | Avg Dim 2 | Avg Dim 4 |
|--------|----------|-------------|-----------|-----------|-----------|
| unstructured-chat | 4 | 3.25/5 | TBD | TBD | TBD |
| structured-behavioral | 1 | 2.5/5 | TBD | TBD | TBD |
| founder-vibe-check | 1 | 2.5/5 | TBD | TBD | TBD |
| peer-screen | 1 | 3.0/5 | TBD | TBD | TBD |
| technical-deep-dive | 0 | — | — | — | — |

## Hypothesis Status Board

> Pulled from `coaching/hypotheses.md`. Promoted hypotheses bolded.

| ID | Claim (short) | Ladder | n tested | Support | Refute |
|----|---------------|--------|----------|---------|--------|
| H1 | Format-fragility | Active | 5 | pending | pending |

## Anti-Pattern Scorecard (Canonical)

> Cross-call frequency rollup. Authoritative — not duplicated in `anti-pattern-tracker.md`.

| Anti-Pattern | Total Occurrences | Last Seen | Trend |
|--------------|-------------------|-----------|-------|
| Filler hedging ("kind of", "really", "definitely", "pretty", "absolutely") | 11 | 2026-05-05 | ▼→ (Govra clean — minimal density; Formic modest "kind of" creep but well below baseline) |
| Caved when steered | 1 | 2026-04-28 | — (clean across both 5/5 calls — held builder/operator framing) |
| Asking questions instead of answering / deflecting | 3 | 2026-03-13 | — |
| Gave a generic self-description (no differentiator) | 3 | 2026-05-05 | ▲ (NEW occurrence — Formic "expertise" answer reused Govra-call framing, less command on second telling) |
| Chronological career walkthrough | 4 | 2026-04-20 | — (clean across both 5/5 calls — descending-size frame held) |
| Over-committing to cover story (framing misalignment) | 3 | 2026-04-20 | — |
| Volunteered a negative unprompted | 2 | 2026-04-28 | — (clean across both 5/5 calls; Formic "passive aggressive communication" answer to "what aren't you good at" was honest but flagged self-protection lens — borderline, not classified as triggered) |
| Overclaiming experience | 1 | 2026-03-13 | — |
| Said "not really" / "no, I haven't" to a tech question | 0 | — | — |
| Over-explained technical details | 0 | — | — |
| Apologised instead of contextualising | 0 | — | — |
| Failed to give recruiter something memorable | 0 | — | — |
| Hesitated or waffled on rate/availability/logistics | 0 | — | — |
| Proper noun error under pressure ("Zora"/"Sora"/"GovRest") | 4 | 2026-05-05 | ▲ (Govra: "Zora" slip self-corrected to Zuora — caught in flight, less severe than prior. Cold-drill before Josh tomorrow) |
| **NEW (candidate):** Reused expertise framing across consecutive calls | 1 | 2026-05-05 | NEW |
| **NEW (candidate):** Default ESPN/McKinsey example when Zuora is the right one | 2 | 2026-05-05 | NEW |
| **NEW (candidate):** Vague ownership phrasing under direct ownership question | 1 | 2026-05-05 | NEW |

## Session Index (Append-Only)

> Newest first. Each row created by `/debrief`. Never deleted.

| Date | Target Role | Format | Stage | Rating | Key Anti-Patterns |
|------|-------------|--------|-------|--------|-------------------|
| 2026-05-06 | Govra — Josh Sandler founder vibe-check (REAL) | founder-vibe-check | founder-meet | 2.5/5 | (preserve from prior _summary if present) |
| 2026-05-05 1:15pm | Formic — Theresa Dobson CPO screen (REAL) | structured-behavioral | recruiter-screen | 2.5/5 | Reused expertise framing (NEW); Default ESPN/McKinsey not Zuora (NEW); Vague ownership phrasing (NEW); Logistics interruptions. |
| 2026-05-05 12:15pm | Govra — Sam Lazarus opener call (REAL) | unstructured-chat | recruiter-screen | 4.5/5 | Filler minimal; "Zora" self-corrected to Zuora; "Dream job in 4-6 years" generic. |
| 2026-05-05 11:00am | Govra — Sam Lazarus opener drill | drill | drill | 4/5 | Filler eliminated by final take (0); "Really" escalated mid-drill (0→3→0); Proper-noun slips. |
| 2026-04-28 2:00pm | Steven Lurie / Team Builder Ventures (REAL) | unstructured-chat | networking | 2.5/5 | Filler "kind of" x7; **Caved when steered**; Volunteered negative; Hedged on stage; Muddled comp delivery. |
| 2026-04-20 2:00pm | Feltsense — Matt Wood peer ops call (REAL) | peer-screen | recruiter-screen | 3/5 | Filler "really" x12 / "kind of" x14 (record); Chronological reversion; Cover story fragility; "Zora" slip. |
| 2026-03-13 1:30pm | Dusty Robotics — Tessa Lau CEO (REAL) | unstructured-chat | hiring-manager | 3.5/5 | Filler hedging ("kind of"); Cover story ("handed it off" re: Zuora). |
| 2026-03-13 11:00am | Belfiore — Farr Hariri (REAL) | unstructured-chat | networking | 2.5/5 | Chronological walkthrough; Over-committed framing. |
| 2026-03-13 10:00am | Belfiore Cheese — Farr pre-call quiz | drill | drill | 2.5/5 | Filler hedging x7; Question-dodging x3; Generic/vague x2. |
| 2026-03-10 | S&O, Amae Health drill | drill | drill | 3/5 | Generic opener; Volunteered negative. |

## Progress Notes (Append-Only)

> Free-form prose synthesis per session. Newest first.

(preserve existing Progress Notes content from prior _summary.md verbatim)

## Update Log (Append-Only)

| Date | Event | Notes |
|------|-------|-------|
| 2026-05-07 | Schema upgrade | `_summary.md` upgraded to M-layer schema. Dimension columns added (TBD pending v1 rubric lock). Format-Stratified View, Hypothesis Status Board added. Anti-Pattern Scorecard declared canonical. Folder collapsed (progress-recruiter + progress-interview → progress). |
```

- [ ] **Step 5.3: Verify**

Run:
```bash
grep -c "^## " coaching/progress/_summary.md
```
Expected: 8 sections (Overall Status, Per-Dimension Trend, Format-Stratified View, Hypothesis Status Board, Anti-Pattern Scorecard, Session Index, Progress Notes, Update Log).

- [ ] **Step 5.4: Commit**

```bash
git add coaching/progress/_summary.md
git commit -m "$(cat <<'EOF'
feat(coaching): upgrade _summary.md to M-layer schema

Per spec §3.3 + §6.3:
- Per-Dimension Trend table (5 dims, TBD until v1 rubric locked)
- Format-Stratified View (H1 test bed)
- Hypothesis Status Board (pulls from hypotheses.md)
- Anti-Pattern Scorecard declared canonical (was duplicated in
  anti-pattern-tracker.md; that file becomes per-pattern detail)
- Update Log section for append-only schema events

All prior data preserved.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 6: Reposition `coaching/anti-pattern-tracker.md`

**Files:**
- Modify: `coaching/anti-pattern-tracker.md`

**Approach:** This file becomes the per-pattern *detail view*. The Occurrences column stops being maintained here (canonical source: `_summary.md` Anti-Pattern Scorecard). Each pattern gets richer detail: mechanism, defense, history of how it's manifested across sessions.

- [ ] **Step 6.1: Read current state**

Read `coaching/anti-pattern-tracker.md` to capture existing patterns and notes.

- [ ] **Step 6.2: Rewrite the file**

Replace top of file with a new header explaining the repositioning. Keep all pattern entries but restructure each as: pattern name + status + mechanism + defense + history (where history aggregates the prior Notes column observations).

```markdown
# Anti-Pattern Tracker (Per-Pattern Detail View)

> **Canonical counts live in `coaching/progress/_summary.md` Anti-Pattern
> Scorecard.** This file is the *per-pattern detail view* — what the
> pattern is, why it happens, how to defend against it, and how it has
> manifested across sessions.
>
> Status values: `Persistent` | `Stable` | `Improving` | `Resolved`

---

## Active Anti-Patterns

### Filler hedging ("kind of", "really", "pretty", "definitely", "absolutely")

**Status:** Persistent
**Mechanism:** Filler density rises as a stalling tactic when Nick is
asked something he hasn't pre-rehearsed or when the format compresses.
Specific words shift over time — "really" replaced "kind of" replaced
"definitely" — but total density stays high. (See H1 in
`hypotheses.md`: filler is dimension 2 of the format-fragility theory.)
**Defense:** Cold drilling before each call to "0 fillers" target.
Govra opener drill 2026-05-05 showed the curve is non-linear — fillers
went 0→3→0 mid-drill. Multiple takes needed.
**History:**
- 2026-04-28 Steven Lurie: "kind of" x7, "absolutely" x1, "really" minimal — cleanest "really" count of any real call.
- 2026-04-20 Matt Wood (Feltsense): "really" x12, "kind of" x14 (record).
- 2026-05-05 Sam Lazarus drill: 0 fillers by final take.
- 2026-05-05 Formic Theresa: modest "kind of" creep but below baseline.

---

### Caved when steered

**Status:** Persistent (1 occurrence — promoted to Persistent on origin)
**Mechanism:** Opponent makes a credible-sounding reframe argument;
without a pre-written counter-thesis, Nick absorbs the frame instead of
defending his own. Steven Lurie 2026-04-28: "the two I have are CoS —
but they're basically biz ops" → Nick said "Right" and absorbed the
reframe.
**Defense:** Pre-call 3-sentence thesis (what I want / won't compromise
on / will consider) re-read 5 min before any live call.
**History:**
- 2026-04-28 Steven Lurie: original occurrence.

---

### Asking questions instead of answering / deflecting

**Status:** Persistent
**Mechanism:** When topic is unfamiliar, Nick over-questions rather than
showing his own diagnosis. EOS answer 3/17 listed 9 questions for Phil
instead of a hypothesis. Improved in Round 2 but still ended vaguely.
**Defense:** Hypothesis-first answer structure. State a position, then
ask for refinement — not the other way around.
**History:**
- 2026-03-17 Phil quiz: 3 instances, EOS first-month answer worst.

---

### Generic self-description (no differentiator)

**Status:** Persistent
**Mechanism:** "Strategic operator" / "love cheese" / "exploring options"
— no numbers, no specifics, nothing memorable. Recurs when Nick hasn't
sharpened his thesis for the specific audience.
**Defense:** Specific, named, quantified. Memorable hook required for
every "tell me about yourself" answer.
**History:**
- 2026-03-12 quiz: "strategic operator" baseline.
- 2026-03-13 Belfiore: "love cheese, exploring options".
- 2026-05-05 Formic: reused expertise framing from earlier Govra call (NEW candidate pattern: reused framing).

---

### Chronological career walkthrough

**Status:** Persistent
**Mechanism:** Default storytelling pattern (Duke→ESPN→Tuck→McKinsey→
CoS) reverts under pressure. Quiz-clean ≠ call-clean. Pattern breaks
under pressure with new interviewers.
**Defense:** McKinsey-first descending-size opening. Drill before every
real call.
**History:**
- 2026-04-20 Feltsense Matt Wood: partial reversion — mentioned Tuck before McKinsey.
- 2026-05-05 Govra Sam: descending-size frame held.
- 2026-05-06 Govra Josh: held.

---

### Over-committing to cover story

**Status:** Stable
**Mechanism:** Cover story phrasing drifts from coached frame under
probing. "Handed it off" re: Zuora is fragile. Departure answer
"11 months, wanted smaller startup" instead of coached "I took a leave
— fully cleared".
**Defense:** Cover stories must stay minimal and defensible. Coached
frame practiced verbatim before each call.
**History:**
- 2026-04-20 Feltsense: departure answer didn't use coached frame.
- 2026-03-13 Dusty: "handed it off" framing.
- 2026-03-13 Belfiore: farmstead framing caused mis-categorization.

---

### Volunteering negatives unprompted

**Status:** Persistent
**Mechanism:** Disclaimer reflex puts Nick in defensive position before
he's been challenged. Steven literally responded by reassuring him.
**Defense:** Don't volunteer. Wait for the question.
**History:**
- 2026-04-28 Steven Lurie: "I don't have that like zero-to-one experience" unprompted.
- 2026-03-12 quiz: Zuora negative volunteered.
- 2026-03-10 Amae: "lonely CoS".

---

### Essay structure — context before answer

**Status:** Stable
**Mechanism:** "I would start and structure this in a few ways" before
giving hypothesis. Throat-clearing variant. Pricing redo on 3/17 was
clean — pattern improving.
**Defense:** Lead with the hypothesis. Context after, only if needed.
**History:**
- 2026-03-17 Phil quiz pricing R1: throat-clearing.
- 2026-03-12 quiz: 1 instance.

---

### "To be honest with you" verbal tic

**Status:** Stable
**Mechanism:** Implies other statements might not be honest. Verbal tic.
**Defense:** Drop permanently from vocabulary.
**History:**
- 2026-03-12 quiz: 2 instances.

---

### Underselling the product/company

**Status:** Stable
**Mechanism:** "Paints on floor plans" undersells Dusty's 1/16-inch BIM
accuracy and core value prop.
**Defense:** Know the product deeply. Use the company's preferred framing.
**History:**
- 2026-03-12 quiz: Dusty undersell.

---

### Overclaiming experience

**Status:** Stable
**Mechanism:** "We have some experience in the cheese business" — making
goat cheese at home ≠ the cheese business.
**Defense:** Keep hobby framing honest. Don't inflate.
**History:**
- 2026-03-13 Belfiore quiz: cheese overclaim.

---

### Proper noun error under pressure

**Status:** Stable
**Mechanism:** "Zora" instead of "Zuora" in pressure moments. Pattern
recurs even when prep sheet flags it.
**Defense:** Write target proper nouns out longhand before every call.
Cold-drill 5 min before live.
**History:**
- 2026-04-20 Feltsense: "Zora" in pitch.
- 2026-05-05 Govra Sam: "Zora" slip self-corrected to Zuora.
- 2026-05-05 Govra Sam drill: "Sora", "GovRest" slips.

---

### Reused expertise framing across consecutive calls (NEW candidate)

**Status:** New (1 occurrence — promote on third occurrence)
**Mechanism:** Same framing deployed twice in one day with less command
on second use. Formic 2026-05-05: "bringing together data and
information... using data to better inform decisions" reused from
Govra-call earlier same day.
**Defense:** Vary framing per audience. Cold-rewrite the expertise
answer if same-day calls.
**History:**
- 2026-05-05 Formic Theresa: same-day-as-Govra reuse.

---

### Default ESPN/McKinsey example when Zuora is the right one (NEW candidate)

**Status:** New (2 occurrences — at threshold for promotion)
**Mechanism:** Default story selection bypasses applied listening (dim
4). Zuora is the directly-relevant story for AI/data ops questions but
ESPN/McKinsey gets deployed reflexively.
**Defense:** Pre-call decision rule: if Zuora is the example that
matches the question, use Zuora.
**History:**
- 2026-04-20 Feltsense Matt Wood.
- 2026-05-05 Formic Theresa.

---

### Vague ownership phrasing under direct ownership question (NEW candidate)

**Status:** New (1 occurrence)
**Mechanism:** Direct "what did you own?" gets answered with process-
narration: "I owned the whole kind of process of being able to drill
into..." Replace with concrete nouns/verbs.
**Defense:** Concrete answer template: "I owned X. The output was Y. The
business impact was Z."
**History:**
- 2026-05-05 Formic Theresa.

---

## Resolved Anti-Patterns

*None yet — populated as patterns are confirmed resolved across multiple sessions.*

---

## Update Log

> Per-pattern history changes are captured inline above. The cross-call
> Update Log lives in `coaching/progress/_summary.md`.
```

- [ ] **Step 6.3: Verify**

Run:
```bash
grep -c "^### " coaching/anti-pattern-tracker.md
```
Expected: ~14 patterns (counts may vary slightly depending on exact split).

- [ ] **Step 6.4: Commit**

```bash
git add coaching/anti-pattern-tracker.md
git commit -m "$(cat <<'EOF'
refactor(coaching): reposition anti-pattern-tracker.md as per-pattern detail

Per spec §6.3: cross-call counts are now canonical in
progress/_summary.md Anti-Pattern Scorecard. This file becomes the
per-pattern detail view (mechanism, defense, history).

All existing pattern entries preserved; structure changed from a single
table to per-pattern sections with richer detail.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 7: Rewrite `/debrief` skill

**Files:**
- Modify: `.claude/skills/debrief/SKILL.md`

**Approach:** Update the skill to enforce the Nick-first scoring gate + Claude annotation + ≥1pt disagreement reconciliation workflow per spec §3.1. Preserve existing Granola transcript handling.

- [ ] **Step 7.1: Read current skill**

Read `.claude/skills/debrief/SKILL.md` to understand existing structure and Granola integration.

- [ ] **Step 7.2: Rewrite the skill**

The new skill enforces this workflow:

```markdown
---
name: debrief
description: Debrief a real interview or drill — Nick-first cold scoring against the v0.9+ rubric, then Claude annotates, then ≥1pt disagreements trigger reconciliation. Updates progress/_summary.md, hypotheses.md, anti-pattern-tracker.md.
---

# /debrief — Cross-call interview debrief

## Purpose

Score a single interview call against the 5-dimension rubric, surface
anti-patterns and hypothesis evidence, and propagate updates to the
canonical cross-call view.

## Inputs

- A Granola transcript (live or pasted) OR a session note Nick wrote
- The call's date, target, and (best guess) format tag
- The rubric: `coaching/debrief-rubric.md`
- Active hypotheses: `coaching/hypotheses.md`
- Cross-call view: `coaching/progress/_summary.md`

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
submits.** This is the polish-anchoring defense.

Save Nick's scores to the per-call file under `## Nick's Cold Score`.

### Step 3: Claude annotates

Now read the transcript and rubric. For each dimension:
- Independently score (Claude's read).
- Surface specific evidence Nick may have missed.
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
`anti-pattern-tracker.md`. For each detected:
- Increment count in `_summary.md` Anti-Pattern Scorecard
- Append occurrence to the per-pattern History section in
  `anti-pattern-tracker.md`

For new patterns Nick names: add as `NEW (candidate)` row.

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
```

- [ ] **Step 7.3: Verify**

Run:
```bash
grep -c "^### Step " .claude/skills/debrief/SKILL.md
```
Expected: 10 (steps 1 through 10).

- [ ] **Step 7.4: Commit**

```bash
git add .claude/skills/debrief/SKILL.md
git commit -m "$(cat <<'EOF'
refactor(skills): rewrite /debrief for Nick-first scoring + disagreement trigger

Per spec §3.1: 10-step workflow enforces Nick-first cold scoring before
any Claude output (polish-anchoring defense), Claude annotates,
≥1pt divergences trigger reconciliation. Adds anti-pattern check,
hypothesis test log append, cross-call correlation surface, predictions-
for-next-session capture.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 8: Extend `/prep-interview` skill

**Files:**
- Modify: `.claude/skills/prep-interview/SKILL.md`

**Approach:** Add three new sections to the existing prep-interview output (cheat sheet, drilling, company/role/interviewer research stay as-is): active anti-patterns, promoted hypotheses for the call's format, last-session focus.

- [ ] **Step 8.1: Read current skill**

Read `.claude/skills/prep-interview/SKILL.md`. Note: file path may be `prep-interview` or similar — check `.claude/skills/` for the actual directory.

- [ ] **Step 8.2: Run discovery**

```bash
ls .claude/skills/ | grep -i prep
```

- [ ] **Step 8.3: Add three new sections to the skill output spec**

Edit the SKILL.md to add (after the existing sections describing cheat sheet / drilling / company research):

```markdown
## Section: Active Anti-Patterns to Watch For

> Pulled from `coaching/progress/_summary.md` Anti-Pattern Scorecard.
> Top 3 by total occurrences. For each: name, last seen, defense (one
> line from `coaching/anti-pattern-tracker.md`).

Example output:
```
### Top anti-patterns active right now

1. **Filler hedging** (11 occurrences, last seen 2026-05-05).
   Defense: cold drill 5 min pre-call to "0 fillers" target.

2. **Proper noun error under pressure** (4 occurrences, last seen 2026-05-05).
   Defense: write target proper nouns out longhand before every call.

3. **Chronological career walkthrough** (4 occurrences, last seen 2026-04-20).
   Defense: McKinsey-first descending-size opening.
```

## Section: Promoted Hypotheses for This Format

> Pulled from `coaching/hypotheses.md` where Ladder = Promoted AND the
> hypothesis's claim or boundary mentions this call's format tag. Inject
> the behavior-change clause directly into prep.

If no hypotheses are Promoted yet: skip this section. (At v1 launch H1
is Active, not Promoted, so this section will likely be empty for the
first batch of calls.)

## Section: Last Session's Focus

> Pulled from the most recent `coaching/progress/<date>-*.md` file's
> "## Predictions for Next Session" block.

Example output:
```
### What you said you'd focus on after the last call

From 2026-05-06 Govra/Josh debrief:
- Sharpen "what's not on your resume" — replace generic expertise framing
  with a named anecdote.
- Tighten "dream job in 4-6 years" answer — name a specific outcome.

→ Has this work happened? Drill those two answers before this call if not.
```
```

- [ ] **Step 8.4: Verify**

Run:
```bash
grep -c "^## Section: " .claude/skills/prep-interview/SKILL.md
```
Expected: 3 (the three new sections; pre-existing sections may use a different header pattern).

- [ ] **Step 8.5: Commit**

```bash
git add .claude/skills/prep-interview/SKILL.md
git commit -m "$(cat <<'EOF'
feat(skills): extend /prep-interview with cross-call read-forward

Per spec §3.2: pull active anti-patterns (top 3 from _summary.md),
promoted hypotheses for the call's format (from hypotheses.md), and
last-session predictions (from prior debrief's predictions block).

Closes Gap #5 (format-blind prep) and Gap #4 (action-loop closure).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Verification (post-execution)

After all 8 tasks complete, run:

```bash
echo "=== File existence ==="
test -f coaching/debrief-rubric.md && echo "OK rubric"
test -f coaching/hypotheses.md && echo "OK hypotheses"
test -f coaching/progress/_summary.md && echo "OK summary"
test -f coaching/anti-pattern-tracker.md && echo "OK tracker"
test ! -d coaching/progress-recruiter && echo "OK old folder gone"
test ! -d coaching/progress-interview && echo "OK old folder gone"

echo "=== Section presence ==="
grep -q "^## Dimension 1" coaching/debrief-rubric.md && echo "OK dim 1"
grep -q "^## Dimension 5" coaching/debrief-rubric.md && echo "OK dim 5"
grep -q "^## H1" coaching/hypotheses.md && echo "OK H1"
grep -q "^## Format-Stratified View" coaching/progress/_summary.md && echo "OK strat"
grep -q "^## Hypothesis Status Board" coaching/progress/_summary.md && echo "OK board"

echo "=== Format tags ==="
grep -l "session-metadata" coaching/progress/*.md | wc -l   # expect 11

echo "=== Skills ==="
grep -q "Nick-first" .claude/skills/debrief/SKILL.md && echo "OK debrief"
grep -q "Active Anti-Patterns" .claude/skills/prep-interview/SKILL.md && echo "OK prep"
```

All lines should print "OK …".

---

## Out of Scope (per spec §8)

- Pre-call format predictor
- Drill recommender
- Multi-pass independent review (full option C)
- Tetlock-style probabilistic forecasting
- Pre-registered decision rules
- Cross-folder integration (interview-stage gets same files when first real interview-stage call lands)
