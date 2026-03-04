# Voice Capture — Passive Observation Guide

Voice capture builds a profile of how the candidate naturally communicates. It is
passive — Claude observes throughout a session and updates `data/voice.md` at the
end. The candidate is never asked to describe their own voice directly. Prepared
answers to "how do you say things?" are too curated to be useful; spontaneous
corrections and pushback are not.

---

## The Opt-In Question

Ask this once, at the very start of any resume or coaching session, before any
other question:

> **Voice capture available.** If you say yes, I'll observe how you naturally
> communicate throughout this session — the corrections you make to my drafts,
> how you push back on framing, the words you add or cut — and update
> `data/voice.md` at the end. That profile is used in future sessions to match
> your natural writing style when generating resume bullets and coached answers.
> It builds over time without any extra effort from you. Enable? (yes / no)

If the candidate says no, skip all voice capture steps for the session.
If the candidate says yes, set an internal flag and follow this guide.

Do not ask again mid-session. Do not reference voice capture again during the
session — observation should be invisible.

---

## What to Observe

Capture signals that are **spontaneous and unrehearsed**. The highest-value
moments are when the candidate:

- Corrects a draft you produced — note what they changed and in which direction
- Pushes back on framing — note the reframe they chose instead
- Explains something in their own words without being asked — note the structure
- Cuts something you wrote — note what category of content they removed
- Adds something you didn't include — note what they chose to surface
- Uses a specific phrase more than once — note it verbatim

Observations to capture, by category:

### Communication Style
- Does the candidate write/speak in short declarative sentences or longer constructions?
- Do they hedge ("I think", "probably", "maybe") or state directly?
- Do they add context before the point or lead with the point?
- Are corrections typically toward more brevity or more precision?

### Writing Preferences
- What do they consistently remove from generated output? (hedges, adjectives,
  passive constructions, long bullets, specific details, general claims)
- What do they consistently add? (numbers, named tools, outcomes, qualifiers)
- Do they prefer compound sentences joined by semicolons, or short separate sentences?
- What is their tolerance for a bullet that runs to 3 lines vs. 2?

### Characteristic Phrases
- Words or constructions they use more than once in natural speech
- How they open a sentence when explaining something they care about
- Any metaphors or analogies they reach for unprompted

### Framing Patterns
- How do they frame difficult situations? (pragmatically, diplomatically,
  bluntly, with attribution to context)
- Do they lead with the principle or the example?
- How do they handle credit? (individual, team, systemic)

### Things to Avoid
- Anything they visibly dislike: specific words, tones, constructions
- Corrections that happen more than once in the same direction

---

## What NOT to Capture

- Answers to direct questions about how they communicate (too prepared)
- Information from a part of the session where they were role-playing or
  rehearsing — capture only their natural register, not their coached answers
- Inferences beyond what was actually observed. If unsure, don't write it.

---

## How to Write Entries

Be specific and concrete. Quote where possible.

**Good:**
> Short, declarative. Corrections consistently move toward fewer words.
> "Means to an end" — used unprompted to describe AI Pioneers program.
> Removes hedges and passive constructions on every pass.
> Leads with principle, then example. Rarely the reverse.

**Bad:**
> Likes direct communication. Prefers short sentences. Uses plain language.

---

## When to Update

Update `data/voice.md` as the **last step** of data enrichment at the end of
the session — after data files have been updated and before the session closes.

1. Read the current `data/voice.md`
2. Review the session for observations matching the categories above
3. Add new observations — do not overwrite existing entries, append to them
4. Update the **Last updated** date at the top
5. Add the session to the **Observed Over** list

6. Cross-check "Things to Avoid" against `coaching/anti-pattern-tracker.md`.
   For any avoidance that is also an interview delivery pattern (essay structure,
   passive-voice self-description, collective hedging, opening with context not
   the point), confirm that it appears in the anti-pattern tracker. Add it if
   missing. This keeps style-level delivery patterns tracked in both places.

Keep entries concise. The profile is a reference for writing, not a biography.
If a session produced nothing new, say so in the Observed Over entry and move on.

---

## How Voice Profile Is Used

When `data/voice.md` is non-empty, it is read alongside `data/professional-identity.md`
during resume generation and coaching sessions. Specifically:

- **Resume bullets:** Apply characteristic phrases, sentence structure, and
  writing preferences when drafting. Voice profile takes precedence over
  Claude's default phrasing patterns.
- **Coached answers:** When delivering stronger versions of answers, apply
  natural framing patterns from the profile — not textbook answer structures.
- **Things to avoid:** Actively check generated output against the avoidance
  list before delivering.
