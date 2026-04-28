Last updated: 2026-03-04

# Application Workflow Framework

> Single source of truth for `/generate-cv`, `/apply`, and `/cover-letter`. Each skill references sections here instead of duplicating rules. Skill-specific workflow steps, argument parsing, output logic, and edge cases stay inline in the skill files.

## Candidate Context Loading

Read the following files in parallel — skip any that don't exist, never fail. Not every output type needs every file; the table below shows which are required per skill.

| # | File | CV | Cover Letter | Notes |
|---|------|----|-------------|-------|
| 1 | `data/profile.md` | ✅ | ✅ | Name, contact, compensation, availability |
| 2 | `data/professional-identity.md` | ✅ | ✅ | Strengths, narrative patterns, reframes, values |
| 3 | `data/goals.md` | ✅ | ✅ | Search thesis, role type preferences |
| 4 | `data/education.md` | ✅ | — | Degrees, qualifications |
| 5 | `data/skills.md` | ✅ | — | Skill inventory with levels |
| 6 | `data/certifications.md` | ✅ | — | Certifications with status |
| 7 | `data/project-index.md` | ✅ | ✅ | Lightweight project index for relevance scanning |
| 8 | `data/companies.md` | ✅ | — | Own companies (if applicable) |
| 9 | `framework/style-guidelines.md` | ✅ | ✅ | Tone conventions, Nick's Voice section |
| 10 | `data/company-notes/<company-slug>.md` | ✅ | ✅ | Personal notes, call context, observations |
| 11 | `data/networking.md` | — | ✅ | Check for contacts at this company (informs hook) |
| 12 | `coaching/coached-answers.md` | cheat sheet | — | Cross-reference for cheat sheet |
| 13 | `coaching/anti-pattern-tracker.md` | cheat sheet | — | "Do NOT say" warnings for cheat sheet |
| 14 | `framework/answering-strategies/anti-patterns.md` | cheat sheet | — | Pre-call warnings for cheat sheet |

**If `data/profile.md` is missing:** warn "Profile not found — run `/import-cv` first for best results. Proceeding with available data."

**Plugins:** If `data/plugin-activation.md` exists, read it. Glob `plugins/*/plugin.md` and check for any plugin with `scope: cv` or `scope: all`. If found, read those plugin files and apply any instructions they contain for CV generation.

## Company Dossier Staleness Check

After determining the company slug, read the company dossier at `output/<company-slug>/<company-slug>.md`. If found, grep for `Last updated:` in the first 10 lines:

- If the dossier is **more than 30 days old** (or no `Last updated:` line exists), display this inline warning — then continue, **never block**:
  > ⚠️ Company dossier is [N] days old (last updated YYYY-MM-DD). Consider refreshing: `/research-company "[Company]"`

## Tailoring Rules

- Never fabricate experience or inflate skill levels.
- **Project selection:** Choose 3-6 projects by relevance to the target role. If one project is marked type: `flagship`, it may deserve inclusion for depth — but it competes on relevance like any other project. If no single standout exists, choose 2-3 of equal weight that best demonstrate depth.
- **Project framing:** Adapt client descriptions to what's most impressive for the target role (e.g. parent company name for enterprise credibility, or technical characteristics for architecture roles). Full project context is in the project file.
- **Role-type emphasis:** Match what you lead with to what the job posting values most. Scan `data/project-index.md` tags and `data/skills.md` categories to find the candidate's strongest overlap with the role's focus area — then lead with those projects and skills. Don't assume which technologies or domains the candidate is strongest in; derive it from the data.
- For **entrepreneurial / startup roles:** include co-founded companies and side businesses from `data/companies.md`.
- For **consulting / advisory roles:** include relevant early-career experience, professional qualifications, and degree focus areas.
- For **roles where the JD mentions technical background, engineering, CS/EE/ML, or "builds products":** scan side-projects in `data/project-index.md` regardless of role seniority and include the strongest one in a compact Selected Projects section.
- Early-career experience (internships, student jobs, apprenticeships, bootcamps, first roles) is usually omitted unless specifically relevant to the target role.
- **No parroting company marketing language.** The summary may reference the company's mission or stage, but must not copy distinctive phrases from the company's own marketing or the JD verbatim (e.g. "capital-efficient approach", "frontier AI"). Paraphrase in the candidate's language.
- **Token de-duplication.** Any distinctive phrase or scale number should appear at most twice across the CV (ideally once in summary and once in the most relevant bullet). Watch for the same headcount, dollar figure, or descriptor repeating three or more times.
- Keep resumes to 1-2 pages for US market (2-4 pages for DACH/international with extensive project history).
- Daily rate and availability are only included if explicitly requested.

### Keyword Pragmatism

When the candidate's source data uses accurate but different terminology from a job posting's buzzwords, find honest bridge language rather than fabricating experience:
- Use qualifying adjectives that signal intent/direction without claiming full adoption (e.g. "-oriented", "-driven", "-based")
- Never invent patterns, tools, or practices the candidate hasn't actually used
- If a keyword gap is too wide to bridge honestly, omit it — don't stretch

## CV Quality Standards

### Keyword Discipline

- **Match the job posting's exact terminology.** If the posting says "CRM", the word "CRM" must appear in the CV. Don't rely on synonyms or related terms. ATS systems and speed-scanning recruiters won't make the connection.
- **When a technology has sub-products, always specify which one.** E.g. "Salesforce" could mean Sales Cloud, Service Cloud, or Marketing Cloud; "AWS" could mean any of 200+ services. Always label the specific product.
- **Extract the top 10 keywords from the job posting** before writing. After drafting, verify each appears at least once in the CV. Missing a primary keyword is a critical defect.

### Honest Scoping

- **Only count projects where the candidate worked *inside* the technology**, not just alongside it. Consuming a product's API from the outside is integration experience, not experience with that product. Make this distinction explicit in the CV.
- **Role titles must reflect how the candidate was engaged.** If hired in one role and later absorbed broader duties, frame it as progression (e.g., "Developer, expanding to Architecture & Team Lead"), not as the starting role.
- **Quantifiers must survive scrutiny.** "Across two projects" must mean two projects with genuine depth. "Three continents" must mean three production deployments, not one production + one pilot + one evaluation. When in doubt, use the more conservative framing.
- **Certification status must be current.** Check `data/certifications.md` for renewal status. Never list a certification as active if it is expired or renewal-pending without noting the status.

### Avoid Self-Sabotage

- **Never include weakness admissions.** Phrases like "currently expanding my X experience", "basic knowledge of Y", or "evaluated but not used in production" tell the reader what the candidate *can't* do. If the skill isn't strong enough to state positively, omit it entirely.
- **Explain concurrent engagements (if any overlap exists).** If any selected projects or roles overlap in time, the CV must acknowledge how concurrent work was managed. Without explanation, reviewers assume a timeline error or exaggeration. Add a brief explanation like "[Engagement A] maintained part-time alongside [Engagement B]" where applicable. Skip this check entirely if no timelines overlap.
- **Include team-fit signals.** Always include at least 2-3 references to collaboration across the CV: code reviews, knowledge transfer, team onboarding, training, sprint participation, coordination with client departments. Candidates who appear to only work solo raise red flags for team-based roles.
- **Apply `data/professional-identity.md` narrative reframes.** If the narrative patterns table shows weaker default framings alongside stronger coached versions, use the coached versions.

### Structural Consistency

- **Project headers must follow one pattern throughout.** Use either `Role — Description` or `Description — Role` for all project entries. Never mix. No prefixes like "Flagship:".
- **All bullets within a section must follow the same format.** If most bullets have bold labels (e.g., `**Architecture:**`), every bullet in that section must. No exceptions.
- **Every project and engagement must have dates.** No "second engagement" or "later period" without a time range. Even approximate dates (e.g., "Q2 2023") are better than nothing.
- **Include availability and location context** in the header, when the target market convention expects it or if the candidate is based in a different region from the role. Add a line like "Available: [date] · Remote ([timezone]) · Travel to [region] on request".
- **Sentence completeness:** Every bullet point must contain at least one verb. Sentence fragments without verbs are defects.

### Language Precision

- **No native-language calques.** Check `data/profile.md` for the candidate's native language, then watch for false friends and literal translations (e.g. German: "reconception" → redesign; French: "resume" → summary; Spanish: "actually" → currently; Dutch: "eventually" → possibly).
- **British/American English consistency** — match the target market convention or the job posting's language. Don't mix within a single CV.
- **Tense must match engagement status.** Present tense for ongoing engagements, past tense for completed ones.
- **Use standard modern compound forms** (e.g. "subcontractors" not "sub-contractors", "freelancer" not "free-lancer").

## CV Quality Checks (18-point checklist)

Run all 18 checks against the CV. Fix any issues found **in place** — rewrite the CV, don't just flag problems.

**1. Keyword coverage:**
- Take the 10 ATS keywords from the role analysis. For each, verify it appears at least once (case-insensitive, but exact product names must match — "React Native" ≠ "React").
- If a keyword is missing, find a natural place to insert it. If genuinely not addable (candidate lacks the skill), note as a gap.

**2. Product specificity:**
- For every technology or platform named, verify the specific sub-product is labelled (not just the parent brand). E.g. "Salesforce" → which cloud? "AWS" → which services? Fix any that are too generic.

**3. Claim integrity:**
- Scan all quantified claims (years of experience, scale numbers, "across N projects").
- **Open each source project file referenced in the CV and verify each claim line-by-line.** Fix or soften any that don't match source data.
- Check certifications against `data/certifications.md` — fix or note status for any expired ones.

**4. No weakness admissions:**
- Search for hedging qualifiers: "currently expanding", "basic knowledge", "evaluated but not used", "learning", "aspiring", "exposure to", "introductory", "some experience". Remove or rewrite any found with confident, specific language.

**5. Concurrent engagement explanation:**
- If any selected projects overlap in time, confirm the CV explains how concurrent work was managed. Skip entirely if no timelines overlap.

**6. Team-fit signals:**
- Confirm at least 2-3 collaboration references exist (code reviews, onboarding, cross-functional coordination, sprint participation). Add naturally if missing.

**7. Structural consistency:**
- **Header pattern**: all project headers follow one format throughout (`Role — Description` or `Description — Role`). No "Flagship:" prefixes. Fix any that don't conform.
- **Bullet format**: all bullets within each section follow the same format (all with bold labels or all without). Fix inconsistencies.
- **Dates**: every project and engagement has a date range. Add approximate dates (e.g. "Q2 2023") if missing.
- **Reverse-chronological order**: list every adjacent pair of roles with their end dates; if any role's end date is earlier than the next role's end date below it, the order is broken — fix by sorting strictly by end date (most recent first). This is a blocker.
- **Availability**: header includes availability/location/remote context if market convention expects it or if candidate is in a different region from the role.
- **Sentence completeness**: every bullet point contains at least one verb. Fix fragments.

**8. Language and tense:**
- Spelling variant consistent throughout (all British OR all American English — match the job posting's variant).
- Tense: present tense for current/ongoing roles, past tense for completed ones.
- No native-language calques — check `data/profile.md` for candidate's native language, then scan for false friends or unusual phrasing.

**9. Date math validation:**
- Any claim like "X+ years at [Company]" or "X years of [skill]" in the summary must be verified against actual date ranges in the source files. If dates show 2022-2024, that's 2 years, not 3+. Fix or soften claims that fail arithmetic.

**10. Month-level dates for short/recent tenures:**
- Roles under 2 years duration OR within the last 3 years must include month-level dates (e.g., "Jan 2024-Dec 2024"), not just year ranges. Current roles must show month + "Present" (e.g., "Jan 2025-Present"). Year-only dates on short recent roles create ambiguity that hurts recruiter screening.

**11. Causal attribution check:**
- Large-scale outcome metrics (e.g., "400% growth", "$2M revenue improvement") must use appropriately scoped language. At IC/analyst level, use "supported", "contributed to", "informed strategies behind". At manager/lead level, "led initiatives that drove" is acceptable. Never claim sole credit for org-wide outcomes unless the candidate was demonstrably the sole driver. Watch for "enabling", "driving", "delivering" applied to outcomes far above the candidate's scope.

**12. Skills evidence check:**
- Every skill listed in the Skills section must appear substantively in at least one experience bullet. Remove any skill that cannot be evidenced in the experience section. "Substantively" means used as a tool/method in a described activity — not just name-dropped.

**13. Metric specificity:**
- Percentage-based claims must include the underlying metric being measured (e.g., "daily active user engagement by 25%" not just "engagement by 25%"). Include a timeframe or baseline where available from source data. Bare percentages without context are vague and invite skepticism.
- Dollar figures over $1M must specify what the number represents (opex, revenue, ARR, budget, contract value, TCV). Bare "$130M+" without a qualifier is ambiguous and invites the "$130M of what?" probe.

**14. Client engagement disambiguation (consulting firms):**
- At consulting firms or agencies, bullets from different client engagements must be clearly attributed to separate clients. Do not bundle bullets from 3 different clients under one employer header without distinguishing which client each bullet refers to. Use descriptors like "for an ecommerce marketplace" vs "for an online retailer" to disambiguate.

**15. Role progression in titles:**
- When a candidate held multiple titles at one company (e.g., promoted or transitioned roles), show the progression explicitly in the header (e.g., "Digital Growth Manager (2018-2020) / Analyst, Product Analytics (2017-2018)"). Do not collapse multiple roles into the final title only.

**16. Jargon translation:**
- Replace casual or overly informal language with professional equivalents. Examples: "stood up" → "established", "tiger team" → "cross-functional task force". Standard strategy/ops terms like "rhythm-of-business", "operating cadence", and "OKRs" are fine — only translate slang or company-internal shorthand that an outside reader wouldn't recognize.

**17. Employment gap detection:**
- List each role's start and end date in chronological order. Compute the delta between each role's end date and the next role's start date.
- Any gap greater than 3 months that is not covered by an Education entry in that window must be addressed on the CV or cover letter. Add a one-line framing (e.g., "Sabbatical", "Independent consulting", "Career transition") on the CV, or pre-empt in the cover letter.
- Also flag: any role under 6 months with a single bullet. This reads as a layoff signal. Either expand to 2–3 source-backed bullets or add a one-line framing of why it was short.

**18. JD-keyword-to-source contradiction check (anti-hallucination):**
- For every bullet that uses a distinctive JD keyword or phrase (e.g., "pricing and packaging", "financial modeling", "competitive analysis", "M&A"), open the source project file and verify that keyword or a clear synonym actually appears in the source file's description of that engagement.
- If the JD keyword is NOT supported by the source — the generator has lifted language from the JD and attached it to an engagement that was really about something else. This is keyword drift and must be fixed by either (a) rewriting the bullet to match what the source actually says, or (b) moving the claim to a different engagement whose source does substantiate it.
- Also verify every skill in the Skills section against at least one experience bullet that evidences it substantively (not just name-drops it). Remove skills that cannot be evidenced.

### QC Summary Template

After all fixes are applied, record a QC summary. **For each of the 18 checks, cite the specific CV line(s) or section inspected and the outcome.** A bare "clean" without line citations is not acceptable — it means the check was not actually run.

Template:

- **#1 Keyword coverage:** X/10 matched. [List each keyword and where it appears, or mark as gap.]
- **#2 Product specificity:** [List every technology mention and its specific sub-product, or "n/a — no parent-brand ambiguity".]
- **#3 Claim integrity:** [For each quantified claim, cite the CV line and the source file line that substantiates it. List corrections made.]
- **#7 Structural consistency:** [Reverse-chron order verified — list roles with end dates confirming order. Header pattern, bullets, dates, completeness confirmed.]
- **#8 Language and tense:** [Spelling variant, tense per role, calques checked.]
- **#11 Causal attribution:** [List each large-scale metric (>$1M, >100%, >100-person) and its scoped verb.]
- **#12 Skills evidence:** [List every skill in Skills section and the bullet that evidences it. Flag any removed for lack of evidence.]
- **#13 Metric specificity:** [List every percentage and dollar figure with its qualifier.]
- **#17 Employment gap:** [List end-to-start deltas between adjacent roles. Flag any >3 months not covered by education or pre-empted on CV.]
- **#18 JD-keyword-to-source:** [For each JD keyword appearing in a bullet, cite the source file line that substantiates it. List any rewrites.]
- Other checks (#4, #5, #6, #9, #10, #14, #15, #16): confirm each ran and list any fixes.

If a check genuinely has nothing to flag, write "n/a — [one-line reason]", not just "clean".

## Cheat Sheet Structure

Generate a pre-interview cheat sheet alongside each CV. Contents:

**1. 15-second recruiter pitch** — tailored to this role. Format: "[Identity hook] with [X years / key credential]. Most relevant experience: [2 projects]. What I'm looking for: [role type] at [company type]. Interested in [Company] because [specific reason]."

**2. Must-have requirements coverage** — for each required skill or qualification from the JD:
- 2-3 specific bullet points from the selected projects that demonstrate it
- Direct quote-ready: "When asked about [requirement], cite [Project] where I [specific action/result]"

**3. Compensation, availability, start date** — pulled from `data/profile.md` (skip if not present)

**4. Coached answers to cross-reference** — read `coaching/coached-answers.md` if it exists. Flag any coached answers that directly apply to likely questions for this role. List: "Existing coached answer for: [topic]."

**5. Do NOT say warnings** — read `coaching/anti-pattern-tracker.md` and `framework/answering-strategies/anti-patterns.md`. Include the most relevant 5-7 warnings for this specific role/context.

**6. Keyword cheat** — list all 10 ATS keywords with a one-line reminder of which project to cite for each.

### Cheat Sheet Quality Rules

- For collaboration/teamwork questions, use the best **peer-work project** as the primary example — not projects where the candidate was sole decision-maker.
- Include rate pushback defense if the rate is above market average for the role.
- Include a short closing with interest statement + max 1-2 questions for the recruiter (save detailed/technical questions for the client interview).
- For each answer where a known anti-pattern could fire, add a bold **"Do NOT say:"** warning with the specific trap to avoid.

### Cheat Sheet Markdown Template

```markdown
# Interview Cheat Sheet — [Role] at [Company]
> Generated [date] from CV: output/<company-slug>/[cv-filename].md

## 15-Second Pitch
[Tailored pitch for this role]

## Must-Have Requirements — Coverage Map

### [Requirement 1]
- **Project [Name]**: [specific bullet, outcome-focused]
- **Project [Name]**: [specific bullet]
- _Cite when asked:_ "[Trigger phrase]"

### [Requirement 2]
...

## Compensation & Availability
- **Target comp:** [from profile.md]
- **Availability:** [from profile.md]
- **Start date:** [from profile.md]

## Existing Coached Answers (cross-reference coaching/)
- [topic] → see coached-answers.md: "[answer title/section]"
- [topic] → see coached-answers.md: "[answer title/section]"
(omit section if coaching/coached-answers.md not found)

## Do NOT Say — Pre-Call Warnings
1. [Warning from anti-patterns relevant to this role]
2. ...

## ATS Keyword Cheat
| Keyword | Cite This Project |
|---------|------------------|
| [keyword] | [Project name] |
```
