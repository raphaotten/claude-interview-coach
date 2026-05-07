# Nick's Voice — Empirical Reference

> **Source corpus:** 37 emails labeled `Job Search/voice-ref` in Gmail (Nick's sent emails, Jan 2025 – Mar 2026). Pulled via `tools/voice_extract.py`. Saved to `data/voice-corpus/` (gitignored).
>
> **Methodology:** Validated by 2026-04-28 background research agent against stylometry / authorship-attribution literature and LLM style-transfer practice. Key principle: **rules alone underperform; rules + verbatim exemplars beats both.** This file contains both.
>
> **Last extracted:** 2026-04-28
> **Last validated:** 2026-04-28 — leave-one-out (3 unread emails) + quantitative analysis via `tools/voice_features.py` (37 emails, 4,319 words, 224 sentences). Report at `data/voice-features-report.md`, raw data at `data/voice-features.json`.
> **Re-extract trigger:** quarterly (next: 2026-07-28) or after recurring corrections in drafts.
>
> **How to use this file:** Email-drafting skills (`/cold-outreach`, `/follow-up`, `/draft-email`, `/apply`) should read this file alongside `framework/style-guidelines.md`. The rules describe Nick's voice; the exemplars anchor it. Do not generate drafts from rules alone.

---

## 1. Voice signature — measurable patterns

### Structure

**Standard cold outreach is 4 paragraphs:**
1. **Greeting + warmth opener** (1 sentence — pleasantry common but not universal; see openers below)
2. **Why this company / role** (2-3 sentences, mission-aware)
3. **Background pitch** (paragraph or 3-bullet structure with quantified outcomes)
4. **Ask + calendar link** (1-2 sentences)

**Bullet structures appear in ~50% of cold outreach.** Format: 3 bullets, often with bold/italic markdown emphasis (e.g. `*Driving valuable business outcomes:*`). Each bullet is a quantified claim or distinct dimension.

**Length (validated 2026-04-28):** average **117 words/email** across the corpus, range 15-314. Cold outreach 200-300 words; follow-up nudges and short replies 50-150; brief logistics replies under 50.

**Mode varies by email type — pleasantries are not universal:**
- **Cold outreach** → opens with pleasantry (`Hope your week is going well!`)
- **Follow-up nudge** → opens direct (`Following up on my previous email...` / `Bumping this back to the top of your inbox`)
- **Logistics / time-sensitive** → opens with the apology or ask (`Apologize for the late notice...` then the request)
- **Post-call thank-you** → opens with thanks + specific reference (`Thanks for taking the time to chat this morning! I really enjoyed digging into <specific topic>`)

### Opener patterns (validated against 37-email corpus)

1. **`Hi <FirstName>,`** — universal first line. **3/3 leave-one-out hits.**
2. **`Hope your week is going well!`** / **`Hope you are doing well!`** — generic pleasantry, common in cold outreach.
3. **Personalized pleasantry** — stronger than generic. Examples from corpus: `Hope the prep for tomorrow's board meeting is going well`, `Hope you have a great vacation next week!`. **Use when you know something specific about the recipient's week.**
4. **`I [recently/just] [came across/saw/applied for] <thing>`** — typical cold-outreach lead-in.
5. **`I noticed we're both <connection>`** — for alumni/network ties (`I noticed we're both Tuck MBA grads - small world!`).
6. **`Thanks for [taking the time/the chat/considering]`** — post-call or post-application.
7. **`Following up on my previous email...`** / **`Bumping this back to the top of your inbox`** — direct nudge, no pleasantry.
8. **`Wanted to follow up about <specific item>`** — thread continuation with explicit purpose.
9. **`Appreciate the connect, I'm glad <introducer> thought of...`** — warm-intro acknowledgment.
10. **`Apologize for the late notice...`** — when there's a real reason to apologize. **NOT for "reaching out" — only for actual disruptions.**

### Closer patterns (validated — 37 emails, distribution counts)

1. **`Best,\nNick`** — **22/37 (59%)**. Most common. Bare first name, no signature block.
2. **`Thanks,\nNick`** — **6/37 (16%)**. When grateful for time given.
3. **`Thanks!\nNick`** — slightly warmer variant.
4. **`Thanks for considering,\nNick`** — **2/37**. Applications.
5. **`Thanks for your understanding,\nNick`** — **1/37**. When asking for accommodation (rescheduling, late notice).
6. **`Looking forward to <X>!\nBest,\nNick`** — when next step is set.

### Sentence-level rhythm (validated 2026-04-28)

- **Sentence length:** mean **16.4 words** (median 16). Range 5-35. Varies. Pleasantries short; pitch sentences are long compound clauses with `and`/`but`.
- **Compound sentences are common** — joined by `and`, `but`, `as`. Semicolons absent.
- **Lists for structure** — when comparing items or pitching multiple strengths, breaks into bullets rather than running prose.

### Punctuation profile (per 100 words, validated)

| Pattern | Per 100 words | Status |
|---|---|---|
| Comma | 4.75 | Heavy use; compound sentences |
| `*asterisk*` (italic emphasis) | 0.16 | In 3-bullet structures |
| Inline ` - ` (hyphen with spaces) | 0.86 | **Signature** — substitutes for em-dash |
| Exclamation | 0.72 | Pleasantries and warm closes |
| Question | 0.26 | Mostly direct asks |
| Em-dash (—) | **0** | Never. Confirmed across 37 emails. |
| Semicolon (;) | **0** | Confirmed never used. |

- **Signature substitution:** Where most writers use em-dashes, Nick uses ` - ` (space-hyphen-space). Example: `My sweet spot is sitting at the intersection of data, operations, and customer experience - exactly where it sounds like you need help right now.`
- **Exclamation points used freely** in pleasantries (`Hope your week is going well!`, `small world!`) and warm closes — but not aggressive overall.

### Vocabulary signatures (validated counts across 37 emails)

| Phrase | Count | Notes |
|---|---|---|
| `particularly` | 10 | Top emphasis word — often `particularly drawn to`, `particularly impressed by` |
| `just` | 7 | Time/intensifier (`Just got a text...`, `I just applied...`) — NOT a hedge |
| `i'd love` | 7 | Standard ask phrasing (`I'd love to grab a coffee`, `I'd love to learn more`) |
| `really` | 6 | Emphasis (`really enjoyed`, `really resonated`, `really appreciated`) |
| `translating` | 6 | Describes the synthesis work Nick does |
| `intersection of` | 4 | Self-pitch (`intersection of data, operations, and customer experience`) |
| `drawn to` | 4 | Mission alignment |
| `roll up my sleeves` | 4 | Ops/execution willingness |
| `what particularly` | 4 | Template (`What particularly draws me to...`) |
| `resonates` | 3 | Mission language |
| `happy to` | 3 | Service offer (`Happy to share anything helpful...`) |
| `sweet spot` | 2 | Self-pitch (`My sweet spot is sitting at...`) |
| `what excites me` | 2 | Template (`What excites me most about <Company>`) |
| `energizing` | 2 | Enthusiasm marker |
| `small world!` | 1 | When alumni/network connection surfaces |

### Pronoun distribution (validated 2026-04-28)

- **`I/me/my` ~66%** — heavily first-person. This is a pitch context.
- **`you/your` ~30%** — addresses the recipient directly.
- **`we/us/our` ~3%** — barely used. Initial intuition (15%) was wrong; collaborative framing only emerges once relationship is established.

**Implication:** drafts that lean on "we" framing for cold outreach will sound off. Save it for follow-ups after a real conversation.

### Hedging (validated)

- **`really`** — 6 occurrences. Used for emphasis in writing (`really enjoyed`, `really resonated`). Acceptable in voice; **NOT a hedge in writing** the way it is in spoken delivery.
- **`particularly`** / **`specifically`** — 10/0 occurrences. True precision modifiers, not hedges. Keep but watch for over-use (10 in 37 emails ≈ 1 every 3-4 emails — acceptable but on the edge).
- **`just`** — 7 occurrences as time/intensifier (`Just got a text from my dad...`, `I just applied...`). NOT hedging. Keep.
- **`kind of`** — **0 hedge instances** (validated via disambiguation regex; the one literal occurrence in the corpus is type-use: `the kind of innovation I'm passionate about`). Written voice does not hedge with `kind of`. Strong signal.
- **`kinda`** — 0 occurrences.

---

## 2. Anti-patterns (zero or near-zero in corpus)

These constructions are **absent from Nick's voice**. Drafts that include them are flattened.

- **Em-dashes (—)** — never use. **0 in 37 emails.** Use ` - ` (hyphen with spaces) or restructure.
- **Semicolons (;)** — never use. **0 in 37 emails.**
- **`Just wanted to...`** — absent. He doesn't hedge intent.
- **`Just checking in`** / **`circling back`** — absent. He gives a reason every time he reaches out.
- **`To be honest`** / **`Honestly`** as preface — absent.
- **`Synergy`** / **`Stakeholders`** as buzzwords without context — absent.
- **`kind of`** / **`kinda`** as hedges — **0 hedge instances** (the one literal occurrence is type-use, validated by disambiguation regex).
- **Generic professional prefacing** like `As discussed,` or `Per our conversation,` — absent.
- **Last-name signoffs** or formal signatures — absent. Always bare `Nick`.

### AI-sounding phrasings (avoid in thank-yous and outreach)

These phrases read as Claude voice, not Nick voice. Migrated from legacy `style-guidelines.md` 2026-05-07; not corpus-extracted but consistent with the corpus.

- ❌ `exactly the kind of work I want to be doing`
- ❌ `deeply aligned with my values`
- ❌ `I believe I could` / `I think I might` / `hoping to` — weakens the line; cut.
- ❌ `genuinely` / `truly` as emphasis adverbs. (Note: `really` is in voice — keep that one. See Section 1 vocabulary.)

### Apologies — narrow rule (corrected 2026-04-28)

Earlier draft said "no apologies" categorically. **That was wrong.** Corrected:

- ❌ **No apologies for *reaching out* or *taking time*.** Don't open with "Sorry to bother you" or "Apologies for the cold email."
- ✅ **Apologies for actual disruptions are in voice.** Example: `Apologize for the late notice, any chance you are still free tomorrow at 2:30...` (corpus 2025-04-16, rescheduling due to vet appointment). When there's a real reason, apologize cleanly, give the reason, ask for the accommodation.

### Patterns to ADD (discovered in validation)

- **Personalized pleasantries** beat generic ones. `Hope the prep for tomorrow's board meeting is going well` > `Hope your week is going well!` when you know specifics.
- **Sharing a relevant resource** when continuing a thread adds value beyond the ask. Example: `I saw this climate resilience event at the 9zero coworking space (right near your office) and thought you might be interested.` Use sparingly; only when genuinely useful.
- **`fellow Tuckie`** — warm/informal variant of `fellow Tuck alum`. Use in casual-fit threads where the recipient is clearly already a peer.
- **`Looking forward to staying in touch!\n\nBest,\nNick`** — relationship-build closer when there's no specific next step (post-coffee thank-you, networking follow-up).
- **Forwards to friends/family** use 1-2 word intros (`Example outreach`, `Here's my follow up`). No formal greeting, no signoff.

---

## 3. Things to keep vs reconsider (flagged for Nick's judgment)

These are patterns IN your corpus that may or may not be voice you want going forward. **The drafting skills should default to keeping them unless you mark "remove" here.**

| Pattern | Frequency | Status (Nick to set) |
|---|---|---|
| `I hope this email finds you well!` | 1+ occurrences | **CONFLICTS WITH GLOBAL RULE.** CLAUDE.md says don't use this filler, but it's in your actual voice. Keep, drop, or replace? |
| `Hope your week is going well!` | ~50% of cold outreach | Warmer than "I hope this finds you well." Likely keep. Confirm. |
| `Hope you are doing well!` | Common | Same as above. Confirm. |
| `particularly` used 3-5x per email | Heavy | Distinctive but repetitive. Keep, reduce, or vary? |
| Heavy mission-language (`work that matters`, `tangible impact`, `meaningful problems`) | Most cold outreach | Genuine for you, but reads as boilerplate to recruiters who see hundreds of MBA candidates. Keep, dial back, or flag for case-by-case? |
| `My sweet spot is sitting at the intersection of...` | Recurring template phrase | Distinctive signature. Keep unless it feels overused. |
| **Mark each row above** with **Keep / Drop / Vary** as you read this. The drafting skills will honor your annotations. |

### Reconciliation from legacy `style-guidelines.md` (2026-05-07)

These rules lived in the demoted "Nick's Voice — Outreach & Email" section. Categorized against the 37-email corpus.

| Legacy rule | Corpus evidence | Verdict |
|---|---|---|
| Open with `Hi [Name],` | 100% match in corpus | **KEEP** (already canonical in Section 1) |
| Close with `Thanks!` (not `Best,`) | `Best,` 22/37 (59%), `Thanks!` rare | **DROP** — `Best,` is dominant; `Thanks,` for grateful contexts |
| `Wanted to follow up here` (not `Wanted to bump this up`) | Corpus uses `Bumping this back to the top of your inbox` as a real follow-up opener | **DROP** — bumping is in voice |
| `Exploring my next move` (not `job search`) | Soft framing; corpus uses both (`on the hunt for my next full time bizops role` appears verbatim in Exemplar 1) | **VARY** — soft framing for warm/peer contacts; direct framing acceptable for founder/recruiter |
| Specific ask, not generic (`Would Wrecking Ball work?` not `grab coffee`) | Consistent with corpus calendly+specificity pattern | **KEEP** |
| Drop `genuinely`, `truly`, `really` | `really` × 6 in voice for emphasis; `genuinely`/`truly` absent | **VARY** — drop `genuinely`/`truly`; `really` allowed sparingly (≤1 per email) |
| Short sentences, no filler, no hedge | Mean 16.4 words/sentence with compound clauses; no hedge words | **KEEP** (with nuance — pitch sentences run long) |
| No `I believe I could` / `I think I might` / `hoping to` | Absent from corpus | **KEEP** (added to Section 2 anti-patterns) |
| No essay structure (answer first, context second) | Cold outreach actually uses why-them → pitch → ask, which is essay-ish | **VARY** — applies to replies and follow-ups; cold outreach has its own 4-paragraph structure (Section 1) |
| No em dashes (—) in outreach | 0/37 in corpus | **KEEP** (canonical) |
| Spaced hyphen ` - ` is em-dash circumvention, also banned | Corpus shows ` - ` is the **signature substitution** (0.86/100 words) | **DROP for outreach** — ` - ` is the voice. Rule still applies to CVs (see CV format section). |
| Thank-you: one specific callback to interviewer's words | Consistent with Exemplar 3 ("when you described X" pattern) | **KEEP** |
| Thank-you: avoid AI-sounding phrases (`exactly the kind of work I want to be doing`, `deeply aligned with my values`) | Not corpus-extractable but corpus has nothing like them | **KEEP** (migrated to Section 2 anti-patterns) |
| Thank-you: `That really resonated` is in voice | Corpus: `really resonated` confirmed | **KEEP** |
| Thank-you under 75 words, three sentences max | Conflicts with Exemplar 3 (substantive post-call follow-up runs longer) | **VARY** — applies to brief post-screen thank-yous; substantive post-call follow-ups run 200+ words |
| Subject line short, human (`Thanks for today`) | No corpus evidence on subjects (Gmail label includes bodies only) | **KEEP** (heuristic, not contradicted) |

**Result:** legacy section is now fully reconciled. Drafting skills should default to the canonical rules in Sections 1-2 of this file. Items marked KEEP above are already reflected; DROP items must not be re-introduced; VARY items use the qualifier in the verdict column.

---

## 4. Verbatim exemplars

These are full-body emails, copied verbatim. **Drafting skills must include 2-3 of these in their prompt context** (per research finding: rules alone underperform; rules + exemplars beats both).

### Exemplar 1: Cold outreach to founder (warm thread via parent)

*Used as exemplar for: warm intros, network connections, founder direct messages.*

```
Hi Randy,

Hope you are doing well! Just got a text from my dad, Eric, about the great
conversation you had about your company Launchpad. He mentioned that he
shared my profile with you and I wanted to reach out to potentially set up
a quick call to connect (My up to date calendar is here
https://calendly.com/nickmagnuson/coffee-chat).

I watched your marketing mix platform demo and was particularly impressed
by the AI-driven agent that enables natural language queries for data
analysis. This is right up my alley from my ESPN days, where I revamped
reporting frameworks and used analytics APIs to derive actionable insights
across our platforms. The ability to transform marketing data into
immediate insights through conversational AI is exactly the kind of
innovation I'm passionate about.

I am currently on the hunt for my next full time bizops role and with an
analytics & consulting background it would be great to learn more about
Launchpad and discuss how I might be able to help in launchpad's next stage
of growth.

Hope you have a great vacation next week!

Best,
Nick
```

### Exemplar 2: Cold outreach to peer hiring manager (Tuck connection)

*Used as exemplar for: alumni connections, peer outreach, mid-stage interview parallel asks.*

```
Hi Elissa,

I noticed we're both Tuck MBA grads - small world! I applied for the BizOps
Manager role at Point last week and had a good chat with Brian earlier this
week. I'm looking forward to talking with Jason on Monday and wanted to
reach out to you as well.

Looking at your background, I couldn't help but notice our similar paths
through media. Your journey from Wall Street Journal to Zillow to Point is
fascinating. I've been on a somewhat parallel track - at ESPN where I
managed digital analytics and grew audience 400%, then McKinsey working
with online marketplaces, and most recently at Yahoo Sports building out
their business intelligence function.

Point's mission really resonates with me. I've been reflecting on what
makes work meaningful beyond dashboards and growth metrics, and the idea of
helping people access wealth in their homes while making homeownership more
accessible feels like work that matters.

Would you be up for a quick 15-minute chat? I'd love to hear about your
product vision and how BizOps collaborates with your team. My up-to-date
calendar is here https://calendly.com/nickmagnuson/coffee-chat.

Thanks,
Nick
```

### Exemplar 3: Substantive follow-up after a call

*Used as exemplar for: post-call thank-yous, building on something specific they said.*

```
Hi Dan,

Thanks for taking the time to chat this morning! I really enjoyed digging
into Stand's approach of using physics-based modeling to rethink wildfire
risk assessment. As someone who's dealt with these issues firsthand, I'm
excited about how you're bringing structural integrity into the equation
rather than just relying on historical data.

Having led data analytics teams at ESPN and Yahoo, plus implementing
operational changes at McKinsey, I think I could add immediate value as you
scale up from your launch last month. My sweet spot is sitting at the
intersection of data, operations, and customer experience - exactly where
it sounds like you need help right now.

The customer qualification bottleneck is an energizing challenge. I see a
clear opportunity to:

 - Drive the customer discovery process to deeply understand what gets
   prospects to become policyholders
 - Turn those insights into systematic, repeatable processes that
   maintain your high-touch approach
 - Support the applied science team in prioritizing and processing
   inbound prospects

Looking forward to meeting you and Jason in person on Friday to dig deeper
into this. Thanks for letting me know a few times that work!

Best,
Nick
```

### Exemplar 4: Application follow-up to recruiter

*Used as exemplar for: post-application nudges to alumni recruiters / direct application channels.*

```
Hi Marisa,

Wanted to follow up on my application for the Manager, Business Operations
role, submitted through the McKinsey alumni network on February 27.

I'm excited about Headway's model for expanding insurance-accepted mental
health access, and the operational complexity of scaling a 48,000+ provider
network is exactly where my background in cross-functional ops and
structured problem-solving fits.

Happy to share anything helpful for the review process. Available anytime.

Thanks!
Nick
```

---

## 5. Validation notes

**Methodology limitation:** corpus is 37 emails over 14 months, with the most substantive samples concentrated in Feb-Apr 2025. Voice rules above are stable across that window but may not reflect 2026 evolution. Re-extract quarterly.

**Leave-one-out spot check (informal):** I read 12 emails for synthesis; the rules above predict the structure and vocabulary signatures of the remaining 25 — opener pattern, closer pattern, mission language, ` - ` punctuation, calendly link inclusion all match.

**What's NOT validated empirically yet:**
- Quantified function-word frequency deltas vs a baseline corpus (research recommends doing this; deferred to next iteration with `tools/voice_features.py`)
- Burrow's Delta or other formal stylometric distance metric
- Validation that an LLM with these rules + exemplars actually generates emails Nick would recognize as his own (predict-test on a held-out email)

**To improve:** label 5-10 more recent emails (Q1 2026) and re-run extraction, then compare for drift.

---

## 6. Drafting checklist for AI-assisted emails

When drafting a cold outreach or follow-up:

- [ ] Open with `Hi <FirstName>,` then a warmth pleasantry (unless a brief follow-up)
- [ ] Lead with why-this-specific-company before pitching self
- [ ] Mission language only when authentic to the role/company
- [ ] Use ` - ` (space-hyphen-space) where you'd want an em-dash
- [ ] Quantified outcomes in the pitch (numbers, not adjectives)
- [ ] 3-bullet structure if pitching multiple strengths
- [ ] Calendly link if asking for time: `https://calendly.com/nickmagnuson/coffee-chat`
- [ ] Close with `Best,` or `Thanks,` + bare `Nick`
- [ ] Zero em-dashes (—)
- [ ] No `Just wanted to...` / `Just checking in` / `circling back`
- [ ] Length: 200-300 words for cold; 50-150 for replies
- [ ] **Read 2-3 exemplars above before drafting** — rules alone underperform
