---
name: skill-gap
description: Analyse skill gaps against a target role and produce a prioritised short-term learning plan
argument-hint: <job-ad-url-or-file> [--days 30|60|90]
user-invocable: true
allowed-tools: Read(*), Glob(*), WebFetch
---

# Skill Gap Analysis

Compare the candidate's current skill inventory against a target role, identify
gaps, distinguish between true gaps and reframeable adjacent experience, and
produce a prioritised short-term learning plan.

## Arguments

- `$ARGUMENTS` (required): The target role — one of:
  - A URL to a live job posting
  - A file path to a saved job description
  - A pasted job description (if no argument, prompt the candidate to paste it)
- `--days 30|60|90` (optional): Planning horizon for the learning plan. Default: 90.

Examples:
- `/skill-gap https://www.example.com/jobs/cto-123`
- `/skill-gap data/target-role.txt --days 60`
- `/skill-gap` *(will prompt for job description)*

---

## Instructions

### Step 1: Load Candidate Profile

Read in parallel:
- `data/skills.md` — full skill inventory with experience levels and self-ratings
- `data/profile.md` — career direction, target roles, and stated preferences
- `data/professional-identity.md` — strengths, growth edges, and career trajectory
- `data/certifications.md` — active and lapsed certifications

Build a mental map of:
- **Core strengths**: Expert-rated skills
- **Developing skills**: Advanced-rated skills
- **Present but thin**: Intermediate or below
- **Adjacent experience**: Skills not listed but likely held based on project history
- **Career direction**: What roles the candidate is targeting and what they are not

Also read `data/project-index.md` to identify domain experience that could transfer to unlisted skills.

---

### Step 2: Load Job Posting

If a URL was provided, fetch it with WebFetch using this prompt:
```
Extract the complete job posting text. Include every section: title, description,
responsibilities, required qualifications, preferred qualifications, and any
stated nice-to-haves. Do not summarise — reproduce the full text.
```

If a file path was provided, read the file. If neither was provided, ask the
candidate to paste the job description.

---

### Step 3: Extract Role Requirements

Parse the posting into three tiers:

**Must-haves** — explicitly required, likely used in screening:
- Hard requirements ("required", "must have", "minimum X years of")
- Technologies and tools stated as essential
- Certifications explicitly required
- Scope or seniority indicators (team size, budget, P&L responsibility)

**Preferred** — stated as preferred, desired, or advantageous:
- Technologies and tools listed as "preferred" or "a plus"
- Domain experience that isn't mandatory
- Certifications listed as preferred

**Nice-to-haves** — implied by the role or listed as optional:
- Industry experience that matches but isn't specified
- Tools mentioned once without emphasis
- Soft skills and leadership qualities

**Note on job posting inflation:** Many postings list 10-15 "required" skills but
are actually screening on 5-6. When a must-have list is unusually long, note this
and focus analysis on the skills most likely to be screened for (mentioned first,
mentioned repeatedly, or matching the role's core function).

---

### Step 4: Cross-Reference Against Candidate Profile

For each must-have and preferred requirement, assess the candidate's current state:

| Status | Definition |
|---|---|
| **Covered** | Skill present at required level or above |
| **Upskill needed** | Skill present but below required level |
| **Adjacent** | Not listed, but candidate has directly transferable experience |
| **Gap** | Not present and no obvious transfer path |
| **Reframeable** | Different technology/tool, same concept (e.g., AWS expertise when Azure is required) |

For **Adjacent** and **Reframeable** statuses, note specifically what experience
bridges the gap. These are framing opportunities for the resume and interview,
not just learning tasks.

---

### Step 5: Score Each Gap

For every **Upskill needed** or **Gap** item:

**Criticality**
- `Blocker`: A must-have that would likely cause automatic screening rejection
- `Material`: A must-have or preferred skill whose absence weakens the application
- `Minor`: A preferred or nice-to-have skill with limited screening impact

**Closability** (within the planning horizon)
- `Fast`: Can reach working proficiency quickly given existing adjacent knowledge
- `Medium`: Requires structured learning over weeks
- `Long`: Requires significant time investment or practical experience to develop
- `Certification-dependent`: Primarily closed by obtaining a specific certification

**Strategic fit**
- `Core`: Aligns with the candidate's target role direction; worth investing in
- `Role-specific`: Useful for this role but not broadly transferable; lower priority
- `Divergent`: Outside the candidate's stated career direction; flag before recommending

---

### Step 6: Output — Gap Analysis

Present a structured analysis:

```markdown
## Skill Gap Analysis — [Role Title] at [Company]

**Planning horizon:** [N] days
**Must-haves assessed:** X  |  **Preferred assessed:** Y

### Coverage Summary

| Skill | Tier | Current State | Status |
|---|---|---|---|
| [Skill] | Must-have | Advanced | Covered |
| [Skill] | Must-have | Not present | Gap — Blocker |
| [Skill] | Must-have | Intermediate | Upskill needed |
| [Skill] | Must-have | AWS Expert | Reframeable (cloud platform transfer) |
| [Skill] | Preferred | Not listed | Adjacent (project history covers this) |

### Critical Path (address before applying)

Gaps and upskill items rated **Blocker** that would likely cause screening rejection:

1. **[Skill]** — [why it's a blocker] — [Fast/Medium/Long to close]
2. **[Skill]** — [why it's a blocker] — [Fast/Medium/Long to close]

*If the critical path is empty: no blockers identified — this role is within reach now.*

### Transferable Experience (reframing opportunities)

Skills where adjacent or reframeable experience can be presented rather than learned:

- **[Required skill]**: [Candidate's adjacent experience and how to frame it]
```

---

### Step 7: Output — Learning Plan

Produce a prioritised learning plan within the requested horizon.

Order by: Criticality first, then Closability (fastest wins first within each
criticality tier), then Strategic fit (Core before Role-specific).

```markdown
## [N]-Day Learning Plan

### Close First (Blockers)

These are must-haves likely used in screening. Address before applying if possible.

**[Skill]** — [N] days estimated
- What to reach: [specific proficiency target, not vague "familiarity"]
- Starting point: [what the candidate already knows that helps]
- Path: [type of resource — official docs / hands-on project / structured course /
  certification — without specifying URLs that may go stale]
- Done when: [concrete test of readiness — e.g., "can explain X, has built Y"]

### Build in Parallel (Material gaps)

Preferred skills and material must-haves that strengthen the application.

**[Skill]** — [N] days estimated
- [same structure]

### If Time Permits (Minor gaps)

Lower-priority skills worth adding if the critical path and material gaps are covered.

**[Skill]** — [N] days estimated
- [same structure]

### Skip for This Role

Skills listed in the posting that are not worth investing time in given the
candidate's career direction or the role's actual screening weight:

- **[Skill]**: [reason — e.g., "listed once, not core to the role", or
  "outside stated career direction"]
```

---

### Step 8: Offer to Save

Ask whether the candidate wants the learning plan saved:

> Want me to save this to `data/learning-plan.md`? I'll include the role,
> the date, and the full plan so you can track progress.

If yes, write the plan to `data/learning-plan.md` with the role title, analysis
date, and complete output from steps 6 and 7.

If a `data/learning-plan.md` already exists, append the new plan below the
existing content with a dated header — do not overwrite previous plans.
