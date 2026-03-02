---
name: scan-jobs
description: Scan a job portal for matching projects/roles, assess fit against profile, track evaluated ads
argument-hint: <portal-url-or-name> [search query]
user-invocable: true
allowed-tools: WebFetch(*), Read(*), Edit(.claude/skills/scan-jobs/cache.md), Write(.claude/skills/scan-jobs/cache.md)
---

# Scan Job Portal

Scan a job portal for projects/roles matching the candidate's profile, deduplicate against a persistent cache of already-evaluated ads, assess fit for new listings, and output a ranked table with links.

## Arguments

- `$ARGUMENTS`: `<portal> [search query]`
  - **Portal** (required): Domain or URL of the job portal to scan (e.g. `upwork.com`, `indeed.com`, or a full search URL)
  - **Search query** (optional): Search terms. If omitted, derive a default query from the candidate's top skills.

Examples:
- `/scan-jobs upwork.com` — scan with auto-derived query
- `/scan-jobs upwork.com "project manager" OR "product owner"`
- `/scan-jobs indeed.com "data engineer" remote`
- `/scan-jobs https://www.example.com/jobs?q=frontend&type=contract` — full search URL

## Instructions

### Step 1: Load Profile

Read the candidate's profile to build a matching baseline. Read in parallel:
- `data/project-index.md` — project overview for matching
- `data/skills.md` — skill inventory with experience levels
- `data/certifications.md` — active certifications
- `data/profile.md` — languages, location, availability, rates

**Build a mental profile summary** from these files:
- Core technologies (Expert + Advanced rated skills)
- Active certifications
- Domain experience (from project industries)
- Languages spoken
- Location and availability constraints
- Contract type preferences (if stated in profile)

**Derive disqualifiers** from the profile:
- Languages not spoken by the candidate
- Technologies marked as absent or not listed at all
- Contract types not matching (e.g., if profile says "freelance only", skip permanent positions)

If no search query was provided, **derive a default query** from the top 2-3 Expert-rated skills, joined with OR.

### Step 2: Read Cache & Calculate Lookback Window

Read the evaluated ads cache:
```
.claude/skills/scan-jobs/cache.md
```

**Parse two things:**
1. **Already-evaluated ads:** Build a list from the table. The dedup key is the **Title + Company** combination (case-insensitive, fuzzy — e.g. "Senior Software Engineer / Backend" matches "Senior Software Engineer/Backend").
2. **Lookback window:** Read the "Last updated" date from the top of the cache file. Calculate the number of days between that date and today, then **add 1 day as buffer**. Use this for any date-based filter the portal supports. Minimum: 1 day. Maximum: 14 days. If the cache has no date or is unparseable, default to 7 days.

### Step 3: Navigate the Portal

**If a full search URL was provided:** Fetch it directly.

**If only a portal domain was provided:**
1. Fetch the portal's job search or browse page
2. Identify the URL structure and search parameters
3. Construct a search URL applying relevant filters:
   - Contract type: match the candidate's preferences from `data/profile.md` (e.g. freelance, contract, permanent — if the portal supports this filter)
   - Remote work: match the candidate's work-model preference from `data/profile.md` (remote, hybrid, onsite — if the portal supports this filter)
   - Region: match the candidate's profile location/target market
   - Recency: filter to the lookback window if the portal supports date filtering
   - Query: use the provided or auto-derived search terms

**WebFetch prompt — use this exact prompt to maximise data extraction:**
```
Extract ALL project/job listings from this page as a structured list. For each listing extract:
1. EXACT project title
2. Company/intermediary name
3. Start date
4. Duration
5. Location and remote percentage
6. ALL skills/technologies mentioned
7. Daily/hourly rate if shown
8. Industry/sector
9. The href URL path for the project detail page (look for <a> tags linking to detail pages)

Number each listing. Extract every single one on the page.
```

**Playwright Fallback** — If the WebFetch response is under 500 characters, or contains only JavaScript boilerplate (`noscript`, "enable JavaScript", "JavaScript is required"), the portal is JS-rendered and WebFetch cannot read it. In that case:

1. **If Playwright MCP is configured** (see `framework/playwright-setup.md`): use the Playwright browser tools to navigate to the URL, wait for the page to finish rendering, then take a snapshot and extract the listings from the rendered content. Note "(via Playwright)" in the scan output header.
2. **If Playwright MCP is not configured**: inform the user that this portal requires a real browser, point them to `framework/playwright-setup.md` for setup instructions, and offer these alternatives:
   - Provide a direct search URL with results already visible
   - Paste the job listing text directly

If the portal's structure is too complex to parse or requires authentication, inform the user and suggest they provide a direct search URL with results visible.

### Step 4: Deduplicate Against Cache

Compare each ad from the search results against the cache (match by Title + Company, case-insensitive, fuzzy). If already evaluated, skip it entirely.

Report: "Found X total, Z already in cache, **N new ads to evaluate**."

If there are zero new ads, report that and stop — do not re-evaluate cached ads.

### Step 4b: Fetch Detail Pages

For each new (non-cached) ad, fetch its detail page to read the **actual listing text**. Do NOT assess fit based only on the search result tags — the detail page contains the real requirements, which often differ from the tag summary.

**Fetch all detail pages in parallel** (they are independent). Use this WebFetch prompt:
```
Extract the COMPLETE listing text in the original language. Include every section: description, tasks/responsibilities, requirements/qualifications, nice-to-haves, location/remote details, and any other content. Do not summarize — reproduce the full text. Also extract: contract type, start date, duration, rate if shown, and language requirements.
```

Apply the same **Playwright Fallback** as Step 3 if any detail page returns a JS shell. If Playwright is not configured and the detail page is unreadable, assess fit from the search result summary only and note the limitation.

If a detail URL was not extracted from the search results, skip that ad's detail fetch — assess it from search results only (note this limitation in the assessment).

### Step 5: Assess Fit for New Ads

For each new (uncached) ad, assess fit against the candidate's profile **using the detail page text from Step 4b**:

**Fit scoring guidelines:**
- **80-100%:** Core stack match, relevant domain, matching contract type → **shortlisted**
- **60-79%:** Strong partial match, one gap is learnable or minor → **maybe** (leaning yes)
- **40-59%:** Some overlap but significant gaps or wrong emphasis → **maybe** (leaning no)
- **20-39%:** Marginal overlap, mostly wrong stack/domain → **skip**
- **0-19%:** No meaningful overlap → **skip**

**Automatic disqualifiers (mark as skip regardless of tech match):**
- Requires languages the candidate doesn't speak
- Contract type mismatch (permanent when freelance-only, employee leasing, etc.)
- Primary stack is a technology the candidate has no experience with
- Requires deep expertise in tools the candidate doesn't know

**Status values:**
- `applied` — application sent
- `shortlisted` — worth applying, high fit
- `maybe` — borderline, worth exploring
- `skip` — not a match
- `dead` — was a match but disqualified (e.g. requirement discovered later)

### Step 6: Output Results Table

Present results as a markdown table:

```markdown
## Job Scan — [portal] — [date]

Query: [query] | Period: last N days | Filter: [filters applied]
Found: X total | Z cached | **N new**

### New Listings

| # | Role | Company | Start | Duration | Key Skills | Fit | Status | Link |
|---|------|---------|-------|----------|------------|-----|--------|------|
| 1 | ... | ... | ... | ... | ... | 80% | shortlisted | [Details](URL) |

### Shortlist (including previously cached high-fit ads)

| Priority | Role | Company | Fit | Status | Link |
|----------|------|---------|-----|--------|------|
| 1 | ... | ... | 80% | shortlisted | [Details](URL) |
```

The **Shortlist** section should include ALL ads with status `shortlisted` or `applied` from both new evaluations AND the cache — this gives a running view of actionable opportunities.

### Step 7: Update Cache

Append all newly evaluated ads to the cache file. Use the Edit tool to add rows to the table in `cache.md`.

**Important:**
- Preserve all existing cache entries
- Add new entries at the bottom of the table
- Update the "Last updated" date at the top
- Use the **ad's posting date** (from the listing) for the "Ad Date" column, not the scan date
- Store the **detail page URL** in the "URL" column as a markdown link. Use `—` if no URL was extracted.
- If an existing cached ad needs a status change (e.g., user says "I applied to this one"), update that row

### Step 8: Summary

End with a brief summary:
- How many new ads found
- How many worth applying to
- Any notable trends, but only if the lookback window covers multiple days (e.g., "strong demand for [skill] this week", "thin market for [technology]-only roles"). Skip trend observations for short lookback windows where the sample is too small.
- Remind user they can update ad status with: "mark [title] as applied"
