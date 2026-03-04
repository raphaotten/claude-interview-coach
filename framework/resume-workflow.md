# Resume Generation Workflow

When asked to create a targeted resume for a specific role:

0. **Voice capture opt-in** — ask the candidate the opt-in question from `framework/voice-capture.md` before doing anything else. If they say yes, observe throughout and update `data/voice.md` at the end per that guide. If no, skip all voice capture steps.

1. **Analyse the role** — extract key requirements, technologies, seniority level, industry, and market context (e.g. regional freelancer portals, international job boards, direct application)
   - **Plugins:** Check `data/plugin-activation.md` for activation config (if the file is missing, all plugins are active). Scan `plugins/*/plugin.md` for enabled plugins whose scope includes `cv` and whose activation criteria match the target role/industry. If found, load their CV rules alongside core quality standards. Plugin CV rules are additive -- they cannot disable core quality checks. If `plugins/` is empty or missing, skip this step.
2. **Scan the project index** — read `data/project-index.md` to identify which projects are relevant based on technologies, tags, industry, and role type
3. **Read relevant project details** — read the full project files only for the 3-6 most relevant matches. If any project is marked type: `flagship`, consider including it for depth and longevity — but only if it's relevant to the target role. Also read `data/skills.md` and `data/certifications.md`
4. **Consult professional identity** — read `data/professional-identity.md` for narrative framing, reframes, and values. Use this to inform tone and angle — especially the narrative patterns table (how the candidate defaults vs. how they should frame things). Also read `data/voice.md` if non-empty — apply writing preferences, characteristic phrases, and avoidance list when drafting bullets and summaries. Voice profile takes precedence over Claude's default phrasing patterns.
5. **Tailor the summary** — rewrite the professional summary to speak directly to the role's needs, informed by the professional identity reframes and the candidate's actual project data
6. **Order by relevance** — put the most relevant projects first, not just chronologically
7. **Adjust skill emphasis** — highlight skills that match the job description, de-emphasise irrelevant ones
8. **Choose language** — match the language of the job posting (or the candidate's preferred language from `data/profile.md`)
9. **Choose format** — select the appropriate market format (see `framework/style-guidelines.md`)
10. **Output format** — produce clean markdown in an `output/` file named `YYYYMMDD-[target-role-slug].md`
11. **Generate call cheat sheet** — produce a companion cheat sheet alongside the CV in `output/YYYYMMDD-[target-role-slug]-cheatsheet.md`. This is a quick-reference table the candidate keeps on screen during recruiter calls. Build it using these sources:

    **Content to include:**
    - For each must-have requirement from the job posting, list 2-3 bullet points of *specific things the candidate did* (not generic skills — concrete actions from projects)
    - Compensation to quote (rate or salary expectation), availability/notice period answer, start date answer
    - 15-second recruiter pitch tailored to this role
    - The cheat sheet should fit on one screen

    **Sources to cross-reference:**
    - `coaching/coached-answers.md` — reuse existing coached answers for common topics (rate pushback, availability, key technology questions, etc.) instead of writing new ones from scratch. Adapt to the specific role.
    - `coaching/pressure-points.md` + `framework/answering-strategies/anti-patterns.md` — scan for pressure points and anti-patterns relevant to this role and add **"Do NOT say"** warnings for the most likely traps (e.g., volunteering negatives on thin experience areas, over-explaining to recruiters, confirming concerns)
    - `data/certifications.md` — verify cert status. If any cert listed in the CV is expired or renewal-pending, prepare the handling answer in the cheat sheet rather than ignoring it.

    **Cheat sheet quality rules:**
    - For collaboration/teamwork questions, always use the best **peer-work project** (team collaboration, subcontractors, code reviews) as the primary example — not projects where the candidate was sole decision-maker
    - Include rate pushback defense if the rate is above market average for the role
    - Include a short closing with interest statement + max 1-2 questions for the recruiter (save detailed/technical questions for the client interview)
    - For each answer where a known anti-pattern could fire, add a bold **"Do NOT say:"** warning (in the CV's language) with the specific trap to avoid

## Tailoring Rules

- Never fabricate experience or inflate skill levels
- **Project selection:** Choose 3-6 projects by relevance to the target role. If one project is marked type: `flagship`, it may deserve inclusion for depth — but it competes on relevance like any other project. If no single standout exists, choose 2-3 of equal weight that best demonstrate depth.
- **Project framing:** Adapt client descriptions to what's most impressive for the target role (e.g. parent company name for enterprise credibility, or technical characteristics for architecture roles). Full project context is in the project file.
- **Role-type emphasis:** Match what you lead with to what the job posting values most. Scan `data/project-index.md` tags and `data/skills.md` categories to find the candidate's strongest overlap with the role's focus area — then lead with those projects and skills. Don't assume which technologies or domains the candidate is strongest in; derive it from the data.
- For **entrepreneurial / startup roles:** include co-founded companies and side businesses from `data/companies.md`
- For **consulting / advisory roles:** include relevant early-career experience, professional qualifications, and degree focus areas
- Early-career experience (internships, student jobs, apprenticeships, bootcamps, first roles) is usually omitted unless specifically relevant to the target role
- Keep resumes to 2-4 pages depending on role seniority
- Daily rate and availability are only included if explicitly requested

### Keyword Pragmatism

When the candidate's source data uses accurate but different terminology from a job posting's buzzwords, find honest bridge language rather than fabricating experience:
- Use qualifying adjectives that signal intent/direction without claiming full adoption (e.g. "-oriented", "-driven", "-based")
- Never invent patterns, tools, or practices the candidate hasn't actually used
- If a keyword gap is too wide to bridge honestly, omit it — don't stretch

## CV Quality Standards

These rules apply to every generated CV. They prevent recurring issues that reduce a CV's effectiveness with recruiters, ATS systems, and hiring managers.

### Keyword Discipline

- **Match the job posting's exact terminology.** If the posting says "CRM", the word "CRM" must appear in the CV. Don't rely on synonyms or related terms (e.g., don't write "React Native" if the posting says "React" — use the exact term from the posting). ATS systems and speed-scanning recruiters won't make the connection.
- **When a technology has sub-products, always specify which one.** Many platform ecosystems contain multiple distinct products under one brand name (e.g., "Salesforce" could mean Sales Cloud, Service Cloud, or Marketing Cloud; "AWS" could mean any of 200+ services; "React" could mean React, React Native, or Next.js). Same applies to cloud services, platform components, and framework ecosystems. Always label the specific product.
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
- **Consult `data/professional-identity.md` narrative patterns table** and actively apply any reframes found there. If the table shows weaker default framings alongside stronger coached versions, use the coached versions.

### Structural Consistency

- **Project headers must follow one pattern throughout.** Use either `Role — Description` or `Description — Role` for all project entries. Never mix. No prefixes like "Flagship:".
- **All bullets within a section must follow the same format.** If most bullets have bold labels (e.g., `**Architecture:**`), every bullet in that section must. No exceptions.
- **Every project and engagement must have dates.** No "second engagement" or "later period" without a time range. Even approximate dates (e.g., "Q2 2023") are better than nothing.
- **Include availability and location context** in the header, when the target market convention expects it (check the job posting and `data/profile.md` for market context) or if the candidate is based in a different region from the role. Add a line like "Available: [date] · Remote ([timezone]) · Travel to [region] on request".
- **Sentence completeness:** Every bullet point must contain at least one verb. Sentence fragments without verbs (e.g., "Specific recommendations to eliminate technical debt") are defects.

### Language Precision

- **No native-language calques.** If the candidate writes in a non-native language, check `data/profile.md` for the candidate's native language, then watch for false friends and literal translations (e.g. German: "reconception" → redesign; French: "résumé" → summary; Spanish: "actually" → currently; Dutch: "eventually" → possibly). Verify any unusual word choices.
- **British/American English consistency** must be verified. Choose the variant that matches the target market convention or the job posting's language. Don't mix within a single CV (e.g., "optimisation" and "organization" in the same document).
- **Tense must match engagement status.** Present tense for ongoing engagements ("2013 – present" demands "Design, build, and operate..."). Past tense for completed engagements.
- **Use standard modern compound forms** (e.g. "subcontractors" not "sub-contractors", "freelancer" not "free-lancer").

## Pre-Output Checklist

Before delivering any generated CV, verify all of the following. This is mandatory — do not skip.

1. **Keyword coverage:** Do the top 10 keywords from the job posting each appear at least once?
2. **Product specificity:** Are all technology sub-products explicitly labelled (not just the parent product name)?
3. **Claim integrity:** Does any quantifier or claim inflate beyond what the source data files support? Check experience years, project counts, scale numbers, tenant counts.
4. **No weakness admissions:** Scan for hedging language ("currently expanding", "basic", "evaluated but not used", "consulting-level"). Remove or reframe.
5. **Concurrent engagement explanation:** If any selected projects overlap in time, is it explained? (Skip if no timelines overlap.)
6. **Team-fit signals:** Are there at least 2-3 collaboration references across the CV?
7. **Header consistency:** Do all project headers follow the same `Role — Description` pattern?
8. **Bullet consistency:** Do all bullets within each section follow the same format (all with bold labels or all without)?
9. **Dates complete:** Does every project and engagement have a date range?
10. **Availability present:** Is availability/location/remote context included in the header (check market conventions from the job posting; recommended for all markets)?
11. **Certification status:** Are listed certifications actually current per `data/certifications.md`?
12. **Language consistency:** Is the spelling variant (British/American) consistent throughout?
13. **Tense correctness:** Present for ongoing, past for completed?
14. **No native-language calques:** Scan for non-standard English words that might be literal translations from the candidate's native language.
