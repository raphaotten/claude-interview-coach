<!-- This file is the orchestration brain — Claude reads it on every session.
     Personal details live in data/profile.md (gitignored).
     Everything else works as-is. -->

# AI Job Search System

End-to-end job search OS. See [README.md](README.md) for description, `docs/usage.md` for skill reference.

## Hard Rules

- **Profile guard.** Before any generative or research skill, verify `data/profile.md` and `data/goals.md` exist with real content (not TODOs). If either is missing or all TODOs, stop and tell the user to run `/import-cv` (profile) or fill `data/goals.md` from `framework/templates/goals.md`. Never fall back to generic candidate context.
- **No em dashes** (—) in any output Nick will send. Use commas, periods, or hyphens.
- **`data/project-background/` is sealed.** Contents never appear in CVs, cover letters, recruiter prep, voice exports, networking notes, or any external-facing artifact.
- **Personal facts** live in gitignored files (`data/profile.md`, `data/goals.md`, `data/professional-identity.md`). Public-fork-safe.

## Self-Improvement Loop

After any user correction:
1. Add a row to `memory/lessons.md` Active Rules: pattern, rule, date.
2. If correction refines an existing rule, update that row instead of duplicating.
3. Scan `memory/lessons.md` at the start of any session involving skill edits, data ops, or CV generation.

**Email/outreach corrections:** capture the delta in `memory/lessons.md` Section 2. New pattern → Occurrences=1, Promoted=No. Recurring → increment Occurrences. If Occurrences ≥ 2 and Promoted=No → update `framework/style-guidelines.md` "Nick's Voice" section, set Promoted=Yes.

## Repository Structure

```
framework/         Workflows, methodologies, style guides, templates
coaching/          coached-answers/, pressure-points/, anti-pattern-tracker.md, progress-recruiter/
data/              Owner data (profile.md, goals.md, professional-identity.md gitignored)
  ├─ company-notes/, industry-notes/, projects/
  ├─ project-background/   Sensitive — never in output
  ├─ reflections/          Snapshots of Nick's processing (date-prefixed)
  └─ workbooks/            Reusable frameworks (no date prefix)
.claude/skills/    27 slash-command skill definitions
memory/            MEMORY.md (auto-loaded, <100 lines), lessons.md, archives
tools/             Python scripts (PDF, preprocessing, atomic writes, n8n)
output/            Generated outputs — company-first hierarchy
```

## Output Conventions

**Company-first hierarchy.** Every named entity gets `output/<slug>/` (slug = lowercase-hyphens). Dossier matches folder name (`output/<slug>/<slug>.md`, no date). All other files date-prefixed `MMDDYY-[descriptor].md`. Flat `output/MMDDYY-*.md` only for entity-less one-offs.

`data/company-notes/<slug>.md` and `data/industry-notes/<slug>.md` hold free-form personal context. Append `## YYYY-MM-DD | [context]` entries. Generative skills read these automatically.

## Data Files

### Write-Only Files (use Write or atomic scripts, not Edit)

Edit silently fails on rows >500 chars. Mutate via:

- `data/job-todos.md` → `tools/todo_write.py`
- `data/job-pipeline.md` → `tools/pipe_write.py`
- All `output/**/*.md` dossiers → re-read and Write full content

PostToolUse hook warns when Edit hits an affected file.

### Personal Exploration — Four Kinds

Snapshots get `YYYY-MM-DD-` prefixes; living docs don't. Dividing question: *does this update over time?*

| Kind | Lifecycle | Location |
|---|---|---|
| Source-of-truth identity docs | Living, single canonical version | Top-level `data/` (`profile.md`, `professional-identity.md`, `goals.md`, future `conviction.md`) |
| Sensitive captures (therapy, family, mental health) | Frozen at capture; never in any output | `data/project-background/` |
| Reflections (Nick's own processing) | Frozen at writing; new session = new file | `data/reflections/` |
| Workbooks / frameworks | Updated over time | `data/workbooks/` |

Files in `data/project-background/` open with a boundary header forbidding use in any external-facing artifact. Reflections inform guidance but are never source-of-truth — they capture how Nick was thinking on a date, not what's currently true.

**Therapy docs use a two-tier pattern.** Per-session files (`YYYY-MM-DD-therapy-{therapist}-transcript.md`) are frozen and contain transcript + session-specific themes. The undated aggregate (`therapy-themes-job-search.md`) is the living cross-session synthesis. When a new session adds themes that recur, refine, or contradict prior themes, promote them into the aggregate as a new dated supplement section; session-specific themes that don't generalize stay in the per-session file only.

### Three Identity Docs — Sharp Boundaries

Three layers, not three versions. Different consumers, different cadences. Drift is a problem; collapse would be worse (every weekly goals tweak would touch the file voice/positioning skills read).

| Doc | Holds | Update cadence |
|---|---|---|
| `profile.md` | **Facts.** Career history, education, skills, availability. | Rarely (when a fact changes). |
| `professional-identity.md` | **Self-understanding.** Strengths, growth edges, work style, values, narrative patterns, conditions for thriving. | Occasionally (after major reflection). |
| `goals.md` | **Direction.** Thesis, target criteria, comp, phase, weekly focus, success metrics. | Frequently (weekly review, search shifts). |

**Boundary rules:**
- Comp facts (floor, target, equity) → `goals.md` only.
- Work style and conditions for thriving → `professional-identity.md` only.
- Target industries and role types → `goals.md` only (they shift). `professional-identity.md` describes *what kind of work Nick is drawn to*, not which sectors are on the list this month.

### Workbook Outputs Update Existing Docs

Outputs from `data/workbooks/*.md` update existing source-of-truth structures. The workbook is the instrument; the existing docs are the canon.

| Workbook output | Destination |
|---|---|
| Conviction doc (3 paragraphs) | New top-level `data/conviction.md` (only genuinely new artifact) |
| Sharpened achievement bullets (Part 4 STAR factual content) | `Key Achievements` in `data/projects/<name>.md` |
| Spoken STAR delivery (Part 4) | `coaching/coached-answers/<question-type>.md` |
| One-sentence value statement | `goals.md` thesis or `professional-identity.md` summary |
| Conditions Statement (Part 2) | `professional-identity.md` Work Style |
| Green/red flags + screen questions (Part 3) | `goals.md` Non-Negotiables |
| Two-sentence Zuora chapter | `professional-identity.md` Career Direction + `coaching/coached-answers/why-did-you-leave.md` |
| "What worked / didn't / learned" doc (Part 1) | New dated file in `data/reflections/` |

### Resume Bullets vs Spoken STAR Stories — Different Artifacts

Same underlying experience, different forms. Do not conflate.

- **Resume bullets** → `data/projects/<name>.md` → `Key Achievements`. Written, scannable. Used by `/generate-cv`, `/apply`, `/cover-letter`. Optimized for the 6-second resume scan.
- **Spoken STAR stories** → `coaching/coached-answers/<question-type>.md`. Conversational, practiced. Used by `/prep-interview`, `/voice-export`, `/debrief`. Optimized for spoken delivery — pacing, hedging-removal, emotional arc.

Never use a CV bullet as an interview answer or a spoken story as a CV bullet.

### Projects

`data/projects/*.md` follows `framework/templates/project.md`: Period, Role, Client, Industry, Location, Type, Description, Responsibilities, Key Achievements, Technologies, Tags.

Type values: `flagship` | `consulting` | `contract` | `employment` | `co-founded` | `internship` | `side-project`.

## Research Dossiers

**Two-speed reading design:**
1. **Executive Summary** — thesis, opportunity rating, top reasons/risks, next action. Scan in 2 min.
2. **Full dossier** — every section opens with bold **BLUF** sentence. Scan all BLUFs in 60 sec.

**Evidence rules:**
- Source tiers: A (primary/official), B (reputable secondary), C (aggregator/crowd — flag).
- High-impact claims tagged `[Confidence: High|Med|Low, as of YYYY-MM]`.
- Contradictions: show both sources, mark `[Needs verification]`.
- Self-reported metrics: always qualify ("they report" / "self-reported"). Never present as independently verified.
- Both `/research-company` and `/research-industry` include Evidence Summary Table and contradiction audit.

**Refresh:** Fresh dossier (<14 days) — offer "view existing" or "refresh." On refresh, include `## What Changed`. Flow: `/research-industry` → `/research-company` → `/cold-outreach` or `/follow-up`.

## Resume Generation & Interview Training

- Resume standards (tailoring, 16-point checklist, cheat sheet) → `framework/application-workflow.md`. Used by `/generate-cv`, `/apply`, `/cover-letter`.
- Interview workflow, coaching rules, progress logging → `framework/interview-workflow.md`.
- Six answering strategies in `framework/answering-strategies/` (blank-mind, gap reframing, pressure defense, question-back, anti-patterns, direct answer structure).
- Voice simulation: `/voice-export` (generate prompt) → practice in Claude App → `/debrief` (analyze).

## Tools & Environment

Python 3.8+. `pip install -r requirements.txt` for PDF features. **All `tools/*.py` scripts require `PYTHONIOENCODING=utf-8` prefix or they crash on Unicode.**

**Atomic write scripts** (return JSON):

| Script | Purpose |
|---|---|
| `todo_write.py` | add/done/clear/sync `data/job-todos.md` |
| `pipe_write.py` | add/update/remove `data/job-pipeline.md` (`--repo-root .` before subcommand) |
| `networking_write.py` | add/log/remove `data/networking.md`; `log` auto-detects replies and updates `data/outreach-log.md` |
| `remember_apply.py` | route notes to 8 destinations |
| `act_apply.py` | pipeline-add / contact-add / notes-add for inbox routing |
| `md_to_pdf.py` | CV markdown → PDF |
| `convert_pdfs.py` | extract text from PDFs in `files/` |

`todo_write.py` accepts `--repo-root` anywhere; `pipe_write.py` and `networking_write.py` require it before the subcommand.

**Email drafts.** Use `tools/open_draft.py` (Google MCP lacks draft-creation permissions). Write `tools/.pending-draft.txt`:

```
TO: recipient@example.com
SUBJECT: Subject line
BODY:
Email body here
```

Then `PYTHONIOENCODING=utf-8 python tools/open_draft.py` opens Gmail compose pre-filled.

**Post-interview workflow:**
1. `data/company-notes/<slug>.md` — call intel, newest at top
2. `pipe_write.py` — stage, next-action, notes
3. `networking_write.py log` — interaction
4. `todo_write.py add` — follow-up task
5. `tools/open_draft.py` — thank-you email
6. If a mock session preceded the call: update `coaching/progress-recruiter/`

**Gotchas:**
- Filter separator-row noise from script output: `[e for e in entries if e.get("task") != "---"]`.
- Edit-safety hook (`.claude/settings.json`) runs `tools/check_edit_safety.py` on every `.md` Edit.

**Background automation (n8n).** Start via `tools\run_n8n.bat` (`NODES_EXCLUDE=[]` required; bare `n8n start` breaks Execute Command). Dashboard: http://localhost:5678

| Workflow | Schedule | Effect |
|---|---|---|
| Gmail Fetch | Every 15 min | `gmail_fetch.py` → `inbox/` |
| Standup Cache Warm | Weekdays 8am | preprocessor scripts → `tools/.cache/` |
| Follow-up Nudge + Dossier Freshness | Daily 9am | inbox items if overdue/stale |
| Weekly Review Reminder | Friday 4pm | reminder to `inbox/` |

## Memory Hygiene

MEMORY.md is loaded every conversation — keep under 100 lines.

**Archive to `memory/archive-YYYY-MM.md`** when:
- Skill change / bug fix / migration is completed and merged (codebase is source of truth)
- Search lead resolved (move with outcome)
- "New feature" note has been stable >2 weeks
- Session-specific reminders past their date

**Keep in MEMORY.md:** active search context, stable architectural patterns, known unfixed bugs, user preferences, critical personal context (employment status, framing rules).

## Style

See `framework/style-guidelines.md` for tone, language, CV format.
