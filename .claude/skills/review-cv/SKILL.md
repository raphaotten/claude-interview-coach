---
name: review-cv
description: Fast quality-gate review of a generated CV against its target role
argument-hint: <path-to-cv> [job-ad-url-or-path]
user-invocable: true
allowed-tools: Read(*), Glob(*), Grep(*), WebFetch
---

# Review CV — Fast Quality Gate

Run a focused quality check on a generated CV. This is designed to catch high-severity issues in ~30 seconds — not a deep analysis, but a pass/fail gate that ensures the CV meets minimum quality standards before submission.

## Arguments

- `$ARGUMENTS` (required): CV filename, optionally followed by the job ad (URL or file path).
  1. **CV filename** — just the filename (e.g., `20260209-draft.md`). The file is always read from the `output/` folder. Must be an actual CV/resume, not a cheat sheet or internal document.
  2. *(optional)* **Job ad** — a URL (e.g., upwork.com link) or a path to a file containing the job description
- Examples:
  - `/review-cv 20260209-draft.md https://www.upwork.com/project/example-id123`
  - `/review-cv 20260209-draft.md data/job-posting.txt`
  - `/review-cv 20260209-draft.md` *(structural checks only)*

If no job posting is provided, the review runs structural/language checks only (steps 3-6). If a job posting is provided, all steps run.

## Instructions

### Step 1: Load Context

1. Read the CV file from `output/<filename>` (prepend `output/` to the filename from `$ARGUMENTS`). **Validate it is an actual CV/resume** — not a cheat sheet, coaching notes, or other internal document. If the file contains tactical call notes, scripted answers, rate negotiation scripts, or headers indicating call preparation rather than CV content (e.g., "Cheat Sheet", "Answers for the Call" — in any language), **STOP and ask the user for the actual CV file**.
2. If a job ad was provided as a URL, fetch it using WebFetch to extract the posting text. If it's a file path, read it. **If WebFetch returns fewer than 500 characters or only JavaScript boilerplate** (`noscript`, "enable JavaScript"), the portal is JS-rendered — fall back to Playwright MCP if configured (see `framework/playwright-setup.md`), or ask the user to paste the job posting text directly. Parse to extract the **top 10 keywords** (technologies, product names, certifications, domain terms) that the CV must contain.
3. Read `data/certifications.md` to check certification status.

### Step 2: Keyword Match (requires job posting)

For each of the 10 extracted keywords:
- Check whether it appears in the CV (case-insensitive, but exact product names must match — "React Native" is not the same as "React").
- Flag any missing keyword as a **CRITICAL** issue.

**Special attention to technology sub-products:**
- If the posting specifies a product variant or sub-service, the CV must match that specificity — don't rely on the broader product name alone (e.g., if the posting says "PostgreSQL", the word "PostgreSQL" must appear, not just "SQL" or "database").
- If the posting names a specific cloud service, that exact service name must appear.

Output a keyword coverage table:

```
| Keyword       | Found? | Location |
|---------------|--------|----------|
| [Keyword 1]   | NO     | —        |
| [Keyword 2]   | Yes    | Title, Summary, Skills, Projects |
```

### Step 3: Claim Audit

Scan the CV for quantified claims and verify against source data:

1. **Experience years** in the skills table — cross-reference with project date ranges. Flag any skill where the claimed years exceed what the project dates support.
2. **Scale numbers** (devices, users, tenants, environments) — check against the relevant project file in `data/projects/`.
3. **"Across N projects"** — count the actual projects where the candidate worked *inside* the technology (not just alongside it).
4. **Certification status** — verify each listed certification against `data/certifications.md`. Flag any that are expired or renewal-pending but listed without qualification.

Flag issues as:
- **CRITICAL:** Claim is demonstrably inaccurate (years don't add up, certification expired)
- **IMPORTANT:** Claim is misleading by omission (counting API consumption as product experience, "global rollout" when deployment was limited to one region)

### Step 4: Structural Consistency Check

Scan for formatting issues:

1. **Project headers:** Do they all follow the same pattern (`Role — Description` or `Description — Role`)? Flag any that break the pattern.
2. **Bullet labels:** Within each project section, are bold labels applied consistently (all or none)? Flag mixed sections.
3. **Dates:** Does every project entry have a date range? Flag any missing dates (including "second engagement" or "additional work" without dates).
4. **Technology lists:** Are they formatted consistently across projects?
5. **Availability/location:** Is there an availability line in the header? (Check whether the target market expects it; recommended for all markets.)

Flag as **IMPORTANT** for consistency breaks, **MINOR** for style preferences.

### Step 5: Self-Sabotage Detection

Scan the CV text for patterns that undermine the candidate:

1. **Weakness admissions:** Search for hedging qualifiers that undermine claimed expertise — e.g. "currently expanding", "basic knowledge", "evaluated but not used", "learning", "aspiring", "growing", "exposure to", "introductory". Flag each occurrence as **CRITICAL**.
2. **Concurrent engagement gaps:** If any projects overlap in time, is there an explanation? Flag if missing as **IMPORTANT**.
3. **Lone-wolf impression:** Count collaboration signals (code reviews, training, team onboarding, sprint participation, coordination). If fewer than 2, flag as **IMPORTANT**.
4. **Native-language calques:** Check `data/profile.md` for the candidate's native language, then search for common false friends and literal translations from that language into English (e.g. German: "consequent" → consistent, "beamer" → projector; French: "résumé" → summary, "formation" → training; Spanish: "actually" → currently, "sensible" → sensitive; Dutch: "eventually" → possibly). Also check standard compound forms: "sub-contractors" should be "subcontractors". Flag each as **MINOR**.

### Step 6: Language & Tense Check

1. **Spelling variant consistency:** Is the CV consistently British or American English? Search for mixed indicators (e.g., "optimisation" + "organization"). Flag mixing as **IMPORTANT**.
2. **Tense correctness:** For any project dated "– present", check that the description uses present tense. For completed projects, check for past tense. Flag mismatches as **MINOR**.
3. **First/third person consistency:** Is the summary first person ("I") while project bullets avoid pronouns? This is acceptable, but flag if pronouns are mixed within a single section.

### Step 7: Output Report

Present results as a concise severity-grouped table:

```markdown
## CV Quality Gate — [CV filename]

**Target role:** [if provided]
**Keyword coverage:** X/10 matched
**Overall:** PASS / FAIL (fail if any CRITICAL issues)

### Issues Found

| # | Severity | Category | Issue | Location |
|---|----------|----------|-------|----------|
| 1 | CRITICAL | Keyword  | "PostgreSQL" not found in CV | — |
| 2 | IMPORTANT | Structure | Missing availability in header | Header |
| 3 | MINOR | Language | Non-standard English term detected | Line 51 |

### Summary
- X critical issues (must fix before submission)
- Y important issues (should fix)
- Z minor issues (nice to fix)
```

**PASS criteria:** Zero CRITICAL issues.
**FAIL criteria:** One or more CRITICAL issues.

If the CV fails, list the critical issues prominently with specific suggested fixes.
