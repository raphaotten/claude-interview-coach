---
name: voice-export
description: Generate a recruiter simulation prompt for the Claude App (voice mode) from a CV and job ad URL
argument-hint: <path-to-cv> <job-ad-url>
user-invocable: true
allowed-tools: Read(*), Glob(*), Grep(*), WebFetch
---

# Voice Export — Generate Recruiter Simulation Prompt

Generate a self-contained recruiter screening simulation prompt that can be pasted into the Claude App (voice mode). The recruiter stays in character for the entire call — no coaching, no interruptions. Coaching happens afterwards in Claude Code.

## Arguments

- `$ARGUMENTS` (required): Two arguments separated by space:
  1. Path to the CV file (e.g. `output/20260210-target-role-slug.md`)
  2. Job ad URL (e.g. `https://www.upwork.com/project/...`)

## Instructions

### Step 1: Parse Arguments

Extract the CV path and job ad URL from `$ARGUMENTS`. If only one argument is provided, ask the user for the missing one.

### Step 2: Load Sources

1. Read the CV file.
2. Fetch the job ad from the URL using WebFetch. **If WebFetch returns fewer than 500 characters or only JavaScript boilerplate** (`noscript`, "enable JavaScript"), the portal is JS-rendered — fall back to Playwright MCP if configured (see `framework/playwright-setup.md`), or ask the user to paste the job posting text directly.
3. Auto-detect a deep review file: take the CV filename, append `-DEEP-REVIEW` before the extension.
   - Example: CV `output/20260210-target-role-slug.md` → look for `output/20260210-target-role-slug-DEEP-REVIEW.md`
   - If the file exists, read it. If not, skip — the question pool will rely on gap analysis only.
4. Auto-detect a cheat sheet file: take the CV filename, append `-cheatsheet` before the extension.
   - Example: CV `output/20260210-target-role-slug.md` → look for `output/20260210-target-role-slug-cheatsheet.md`
   - If the file exists, read **only the header section above the first `---`** for recruiter persona enrichment (name, company context, intermediary vs. end client). Do NOT read below the first `---` — that contains coached answers and candidate prep.
5. Read `framework/voice-export.md` for the export prompt structure and quality rules.

### Step 3: Detect Language

Determine the CV language by scanning section headers and body text. Common header patterns:
- English: "Summary", "Skills", "Certifications", "Projects" → **EN**
- German: "Kurzprofil", "Fachkenntnisse", "Zertifizierungen" → **DE**
- French: "Compétences", "Expérience", "Formation" → **FR**
- Dutch: "Vaardigheden", "Werkervaring", "Opleiding" → **NL**
- Spanish: "Habilidades", "Experiencia", "Formación" → **ES**
- Other languages → infer from content
- If uncertain → default to **EN**

All generated prompt text must match this language.

### Step 4: Extract Recruiter Persona

From the job ad, enriched by cheat sheet header if available:
- **Company name** and brief context (1-2 sentences) — cheat sheet may clarify intermediary vs. end client
- **Role title** / project description
- **Start date, duration, utilisation, remote/onsite**
- **Contact name** — from cheat sheet header or job ad; if neither has one, generate a plausible recruiter name matching the job ad's market/language

### Step 5: Build Question Pool

Assemble the question pool from three sources:

#### A. Deep Review Questions (if file exists)
- Extract the "Top 10 Probing Interview Questions" section from the deep review file
- Include all questions verbatim — these are the highest-value probes

#### B. Gap-Derived Questions
- Compare job ad requirements against the CV
- Generate 3-5 questions targeting: technical gaps, experience depth mismatches, role-fit concerns
- Do NOT duplicate topics already covered by deep review questions

#### C. Standard Recruiter Topics
Always include these topics (the recruiter weaves them in naturally):
- Compensation expectations and flexibility (rate for freelance/contract roles, salary for permanent — derive from the CV and job ad context)
- Availability, notice period, or earliest start date
- Remote/onsite preferences and travel willingness
- Motivation for this specific role
- Current employment or engagement status
- Invoicing entity / contracting setup (for freelance/contract roles only, if relevant based on CV)

### Step 6: Assemble the Prompt

Build the prompt following this exact section order (use `##` headers):

1. **System Instruction** — Role assignment: realistic recruiter, no coaching, stay in character
2. **Recruiter Persona** — From Step 4
3. **Candidate CV** — Full CV text inlined (the recruiter "has it on their desk")
4. **Question Pool** — From Step 5. Mark this section as internal to the recruiter: "These are topics and questions for you to draw from during the call. Weave them into natural conversation — do not read them as a list."
5. **Call Flow Guidelines** — Natural pacing: intro → candidate pitch → technical/experience questions → compensation/logistics → closing with next steps. Target 15-20 minutes. Go deeper on fewer questions rather than rushing through all.
6. **Session Rules** — Language match, stay in character, natural behaviour, ending instruction ("End of simulation. Take this conversation to Claude Code for a full debrief with your coaching files.")
7. **Start Instruction** — match CV language. Provide the start instruction in the detected language. Examples — EN: `Say "Start" to begin the call.` / DE: `Sag "Start" um das Gespräch zu beginnen.` / For other languages, translate accordingly.

### Step 7: Quality Check

1. **Count words.** If > 8,000, apply compression strategies from `framework/voice-export.md` in priority order.
2. **Scan for file references.** If any path-like string (`data/...`, `coaching/...`, `output/...`) appears in the prompt, remove it — everything must be inline.
3. **Check language consistency.** No mixing DE/EN within the prompt.
4. **Verify no coached answers leaked.** The prompt must NOT contain any prepared candidate answers.

### Step 8: Output

Output the assembled prompt inside a single fenced code block (` ```markdown ... ``` `) so the candidate can copy it directly into the Claude App.

Before the code block, print a short summary:
- Role name
- Language (DE/EN)
- Word count
- Deep review questions included? (Yes/No) — if No, add: `💡 Run /review-cv-deep <cv-path> first for more substantial probing questions in the simulation.`
