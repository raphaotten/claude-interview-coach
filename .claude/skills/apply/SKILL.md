---
name: apply
description: Generate tailored CV + cover letter and add to pipeline in one command — the complete apply bundle
argument-hint: "<job-url-or-jd> [context]"
user-invocable: true
allowed-tools: Read(*), Glob(data/*), Glob(framework/*), Glob(plugins/*), Write(output/**), Write(data/job-pipeline.md), WebFetch, WebSearch
---

# Apply — One-Command Application Bundle

Generate a tailored CV, companion cheat sheet, and cover letter for a specific role — then add (or update) the company in the pipeline. Replaces the 3-command flow of `/generate-cv` + `/cover-letter` + `/pipe add`.

## Arguments

- **`<job-url-or-jd>`** (required) — URL to the job posting, or pasted job description text
- **`[context]`** (optional) — additional instructions, e.g. `"emphasize McKinsey"`, `"US format, 1 page"`, `"warm tone, mention coffee chat with Alex"`
- **`--deep-review`** or **`--deep`** (optional flag) — after generating the bundle, automatically run `/review-cv-deep` against the saved CV. Produces a six-perspective audit (Recruiter / Hiring Manager / Competitor / Skeptic / Copy Editor / Source Auditor) saved to `output/<slug>/MMDDYY-[role-slug]-DEEP-REVIEW.md`. Use for high-stakes applications where the ~5-minute cost is justified.

Examples:
- `/apply https://jobs.impossible.com/cos-role` — full bundle from URL
- `/apply "Chief of Staff, Ripple Foods..." "emphasize food/FMCG experience"` — pasted JD with context
- `/apply https://jobs.lever.co/amae/xyz "warm tone, mention coffee chat with Alex"`

If no arguments provided:
```
Usage: /apply <job-url-or-jd> [context]

Examples:
  /apply https://company.com/jobs/role
  /apply "Job description text..." "emphasize operations experience"
  /apply https://company.com/job "US format, keep to 1 page"
```

## Instructions

### Step 1: Parse Arguments & Fetch JD

Parse `$ARGUMENTS`:
1. **Detect `--deep-review` or `--deep` flag** anywhere in the argument string. If present, set `deep_review = true` and strip the flag from the remaining arguments before further parsing.
2. If the first remaining token contains `http` or a recognisable domain, treat it as a URL. Use WebFetch to retrieve the job posting. If fetch fails, ask user to paste the JD directly.
3. Otherwise treat the full first argument (before any quoted context string) as pasted JD text.
4. Extract any quoted or trailing string as the `[context]` override.

### Step 2: Profile Guard

Check that both `data/profile.md` and `data/goals.md` exist and contain real content (not just TODO placeholders):
- If `data/profile.md` is missing or has only TODOs: "⚠️ `data/profile.md` is missing or incomplete. Run `/import-cv` first."
- If `data/goals.md` is missing or has only TODOs: "⚠️ `data/goals.md` is missing or incomplete. Run `/setup-goals` first."
- Do not proceed until both files have real content.

### Step 3: Load Candidate Context (parallel)

Read all files listed in `framework/application-workflow.md` § Candidate Context Loading (both "CV" and "Cover Letter" columns — `/apply` needs the superset). Skip any that don't exist, never fail.

Check for plugins per the § Candidate Context Loading plugin instructions.

### Step 4: Analyse the Role

From the job posting text, extract:

- **Company name** and generate a slug (lowercase, hyphens — e.g. `impossible-foods`)
- **Role title** and a role slug (e.g. `chief-of-staff`)
- **Required skills** (must-haves)
- **Nice-to-have skills**
- **Seniority level**
- **Top 10 ATS keywords** — the most important terms for ATS passage
- **Market** — US / UK / DACH / international (default US if unclear)
- **Industry** — infer from company and role
- **Mission / core challenge** — what problem does this company solve? What's the role's primary mandate?
- **Top 3 required qualities** — the most important attributes beyond just skills
- **Tone signals** from the JD

Now read:
- `data/company-notes/<company-slug>.md` — personal notes (skip if doesn't exist)
- `data/networking.md` — check for any contact at this company (informs cover letter hook)
- Company dossier at `output/<company-slug>/<company-slug>.md` — run the **Company Dossier Staleness Check** from `framework/application-workflow.md` § Company Dossier Staleness Check

### Step 5: Select Projects

1. Read `data/project-index.md` — scan all entries for relevance to the role's required skills, industry, seniority level, and company type.
2. Select **3–6 most relevant projects**. Criteria: skill overlap with required skills > industry/domain match > seniority match > recency.
3. **Side-project trigger:** if the JD mentions technical background, engineering, CS/EE/ML, applied AI, or "builds products," scan side-projects (type: `side-project`) in the project-index regardless of seniority and include the strongest one in a compact Selected Projects section on the CV.
4. Read the full project files for each selected project from `data/projects/`.
5. **NEVER read or use files from `data/project-background/`.**
6. Note the rationale for each selected project (used in the cheat sheet).

### Step 6: Generate the CV

Apply all **Tailoring Rules** and **CV Quality Standards** from `framework/application-workflow.md`:

- **Professional summary** — 3–4 lines tailored to this specific role. Opens with a hook tied to the company's mission or the role's core challenge.
- **Experience ordering** — strict reverse-chronological (most recent first). Do NOT reorder by relevance — non-chronological CVs are flagged by ATS systems and confuse recruiters. Tailor through bullet selection and emphasis, not ordering.
- **Skills section** — emphasise skills that appear in the JD. Lead with required skills the candidate has.
- **ATS keyword coverage** — verify all 10 extracted keywords appear at least once in the CV text.
- **Format** — based on market:
  - US: 1–2 pages, no photo, no DOB, concise bullet points
  - UK: 2 pages, CV (not resume), more narrative allowed
  - DACH: Photo optional, more formal structure
- **Achievements over responsibilities** — lead bullets with quantified outcomes where possible.

### Step 6b: Inline CV Quality Review (mandatory — do NOT skip)

Run all 18 checks from `framework/application-workflow.md` § CV Quality Checks. Fix issues in place — never just flag.

After all fixes, record a QC summary using the template in `framework/application-workflow.md` § QC Summary Template. The template requires per-check line citations — a bare "clean" without evidence is not acceptable.

### Step 7: Generate the Cover Letter (Problem-Solution Format)

Use the **Problem-Solution** structure — leads with their challenge, proves you've solved it, bridges to what you'd do for them. Total target: **250-350 words**. The resume covers the past; the cover letter addresses the future. Never summarize the CV.

**Section 1 — The Hook (2-3 sentences)**
- Open with something specific to this company: a challenge they face (from JD language, dossier, or news), a recent event, or a personal connection from `data/networking.md`.
- Name the company in the first sentence. Always.
- The uniqueness test: could another applicant send this same opener to a different company? If yes, rewrite.
- Never open with: "I'm writing to apply for...", "I've always been passionate about...", "I'm a [trait] professional with X years..."

**Section 2 — The Proof (3-5 sentences)**
- Present 1-2 specific examples of how you've solved a problem similar to the company's challenge.
- Lead with the problem you faced, then action, then quantified result.
- Frame as analogy: "When [Company/Project] faced [similar problem], I [action] which resulted in [outcome]."
- Do NOT reproduce CV bullet points verbatim — synthesize into narrative.
- Choose proof points that complement (not duplicate) the CV's top bullets.

**Section 3 — The Bridge (2-3 sentences)**
- Connect your capability to their specific needs: "At [Company], I'd apply this approach to [their specific challenge]."
- Reference 1-2 concrete priorities from the JD or research.
- Position as thought partner, not task executor (especially for senior roles).

**Section 4 — The Close (1-2 sentences)**
- Express genuine enthusiasm tied to something specific about this company.
- Direct ask that advances the conversation: "I'd welcome the chance to discuss how [specific approach] maps to [Company]'s [specific challenge]."

**Cover letter quality gates:**
- **Uniqueness test:** each section must be specific enough that it can't be sent to another company unchanged.
- **Resume separation:** the letter must add what the CV can't (the "why", connective tissue, future vision).
- **Length:** 250-350 words. Hard ceiling 400. If over 350, trim section 2 to one proof point.
- **Anti-patterns:** no hedging ("I believe I could", "hoping to"), no filler openers, no em dashes, no trait claims without evidence, no generic enthusiasm.
- **ATS:** 3-5 key JD terms woven naturally into the letter body.
- **Company name** appears at least twice and is spelled correctly.
- **Language variant** consistent (US/UK — match the JD).

Apply any `[context]` overrides: `"emphasize [project]"`, `"more informal tone"`, `"keep to 200 words"`, `"mention coffee chat with [name]"`, etc.

### Step 8: Generate Companion Cheat Sheet

Generate a pre-interview cheat sheet following the structure, quality rules, and markdown template in `framework/application-workflow.md` § Cheat Sheet Structure.

### Step 9: Determine Output Filenames

- Date prefix: `MMDDYY` (today's date)
- Company subfolder: `output/<company-slug>/`
- CV: `output/<company-slug>/MMDDYY-[role-slug].md`
- Cheat sheet: `output/<company-slug>/MMDDYY-[role-slug]-cheatsheet.md`
- Cover letter: `output/<company-slug>/MMDDYY-cover-letter.md`
- If any file already exists at that path: append `-v2`, `-v3` etc.

### Step 10: Save Output Files

Write all three files:
1. **CV** → `output/<company-slug>/MMDDYY-[role-slug].md`
2. **Cheat sheet** → `output/<company-slug>/MMDDYY-[role-slug]-cheatsheet.md`
3. **Cover letter** → `output/<company-slug>/MMDDYY-cover-letter.md`

### Step 10b: Deep Review (only if `deep_review = true`)

If the `--deep-review` or `--deep` flag was set in Step 1, invoke `/review-cv-deep` against the just-saved CV before updating the pipeline. Pass two arguments: the CV filename (just the filename — the skill reads from `output/`) and the JD (pass the URL if one was provided; otherwise write the JD text to a temp file and pass that path).

The deep-review skill produces `output/<company-slug>/MMDDYY-[role-slug]-DEEP-REVIEW.md` — a six-perspective audit with CRITICAL / IMPORTANT / MINOR / NITPICK findings and a Top 5 Highest-Impact Changes table.

Wait for deep-review to complete before proceeding to Step 11. Capture the key verdicts (Recruiter phone-screen decision, Hiring Manager interview decision, Competitor shortlist rank, Top 3 critical issues) for the Step 12 summary display.

If the flag was not set, skip this step entirely.

### Step 11: Update Pipeline

1. Read `data/job-pipeline.md`.
2. Search for the company name (case-insensitive substring match).
3. **If found:** Update the entry:
   - Set **CV Used** to the CV filename (just the filename, not full path)
   - Append the cover letter filename to **CV Used** (separate with `, `)
   - If the stage is `Researching`: update it to `Applied`
4. **If not found:** Add a new row to the Active section:
   - Stage: `Applied`
   - Date Added: today
   - Date Updated: today
   - CV Used: [cv filename]
   - Notes: `Added by /apply on [today's date]`
5. Write `data/job-pipeline.md`.

### Step 12: Display Summary

```markdown
## Application Bundle Ready — [Role Title] at [Company]

### Files Saved
- **CV:** `output/<company-slug>/MMDDYY-[role-slug].md`
- **Cheat sheet:** `output/<company-slug>/MMDDYY-[role-slug]-cheatsheet.md`
- **Cover letter:** `output/<company-slug>/MMDDYY-cover-letter.md`

### CV Quality Summary
- **Keyword coverage:** N/10 matched [list any unfixable gaps]
- **Claims verified:** N checked, N corrected
- **Issues fixed:** [list or "none"]
- **Language consistency:** clean / N items fixed

### Deep Review Verdict (only if `--deep-review` was used)
- **Deep review file:** `output/<company-slug>/MMDDYY-[role-slug]-DEEP-REVIEW.md`
- **Recruiter (phone invite?):** Yes / No / Maybe
- **Hiring Manager (interview?):** Yes / No / Maybe
- **Competitor shortlist rank:** N of 8
- **Top 3 critical issues surfaced:** [one-line each]
- **Recommendation:** [one-line — proceed, fix before submitting, or reconsider]

### Cover Letter
- **Word count:** N words [within target / over — consider trimming]
- **Hook angle:** [one-line summary]
- **Proof points:** [projects used]

### Pipeline
[✅ Pipeline updated — [Company] stage: Applied, CV Used set] OR [✅ New pipeline entry added — [Company] / [Role] / Applied]

### Projects Selected
1. [Project name] — [one-line rationale]
2. ...

### Suggested Next Step
- Review the CV: `/review-cv output/<company-slug>/MMDDYY-[role-slug].md`
- When ready to interview: `/prep-interview "[Company]"`
- To export as PDF: close any open PDF with the same name first, then run:
  `python tools/md_to_pdf.py output/<company-slug>/MMDDYY-[role-slug].md`
```

## Edge Cases

- **URL fetch fails:** Ask user to paste the JD directly. Do not attempt to reconstruct.
- **Too few projects:** If fewer than 3 relevant projects exist, use all available. Note in summary.
- **Missing profile.md:** Proceed without personal details. Leave name/contact as placeholders in cover letter. Flag in summary.
- **Cover letter > 350 words:** Flag in summary with suggestion to trim paragraph 2 to 2 evidence points.
- **Personal connection in networking.md:** Mention in the cover letter hook paragraph — "After speaking with [First Name]..."
- **Existing pipeline entry already at Applied or later:** Do not regress the stage. Only update CV Used field.
- **Keyword not coverable:** If a keyword can't be added naturally (candidate lacks the skill), flag as `⚠️ Gap — omit` in the ATS coverage table.
- **Company dossier stale (>30 days):** Surface inline warning (see Step 4) but continue.
