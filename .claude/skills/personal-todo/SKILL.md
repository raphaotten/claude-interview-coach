---
name: personal-todo
description: Lightweight to-do list for personal life (admin, household, family, finances, errands) — sibling of /todo, scoped outside the job search.
argument-hint: [add|done|clear <task> [priority] [due] [notes]]
user-invocable: true
allowed-tools: Read(*), Bash(python3 tools/personal_todo_write.py:*), Bash(PYTHONIOENCODING=utf-8 python3 tools/personal_todo_write.py:*)
---

# Personal To-Do Manager

Lightweight to-do list for personal life — admin, household, family, finances, errands. Mirrors the schema of `/todo` (job-todos) but writes to the vault file, not the project.

**Data file:** `~/Documents/Obsidian/30-projects/personal/data/personal-todos.md`

## Arguments

- `$ARGUMENTS`: Optional. If empty, show active to-dos.
  - `add <task> [priority] [due] [notes]` — add a new to-do
  - `done <task>` — mark a to-do as complete and archive it
  - `clear` — move all Done/Withdrawn rows to the Done section

Examples:
- `/personal-todo` — show active personal to-dos sorted by priority
- `/personal-todo add "Renew driver's license" High 2026-06-30` — high priority with due date
- `/personal-todo add "Buy birthday gift for Christen"` — default Med priority, no due
- `/personal-todo done "Renew driver's license"` — mark complete (fuzzy match)
- `/personal-todo clear` — archive all completed/withdrawn items

## Instructions

### Command: Show To-Dos (no arguments)

1. Read `~/Documents/Obsidian/30-projects/personal/data/personal-todos.md`.
2. If file is empty or has no entries in the Active section, display:
   ```
   No personal to-dos yet. Add your first one:
     /personal-todo add <task> [High|Med|Low] [YYYY-MM-DD]
   ```
3. If entries exist, display Active sorted by priority (High → Med → Low), then by due date (soonest first, no-date last):
   ```markdown
   ## Personal To-Dos — [date]

   **Active: N** | High: X | Med: X | Low: X | Overdue: X

   1. Task description [Priority | Due: date | Status]
      Notes: ...

   2. Task description [Priority | Due: date | Status]
   ```
4. Flag overdue items (due date < today) with a warning marker.

### Command: `add <task> [priority] [due] [notes]`

1. Parse `$ARGUMENTS`:
   - **Task** (required) — to-do description
   - **Priority** (optional, default: `Med`) — `High`, `Med`, or `Low`
   - **Due** (optional, default: `--`) — `YYYY-MM-DD`
   - **Notes** (optional, default: `--`) — free text
2. Run the write script (substitute extracted values; use `--` for missing args):
   ```bash
   PYTHONIOENCODING=utf-8 python3 tools/personal_todo_write.py add "TASK" "PRIORITY" "DUE" "NOTES"
   ```
3. Parse JSON result:
   - If `status: error`, show the message and stop.
   - If `warning` key is present, display: `⚠ Note: {warning}`
   - On success, confirm:
     ```
     ✓ Added: TASK [PRIORITY | Due: DUE]
     ```

### Command: `done <task>`

1. Extract the task fragment from `$ARGUMENTS`.
2. Run the write script:
   ```bash
   PYTHONIOENCODING=utf-8 python3 tools/personal_todo_write.py done "FRAGMENT"
   ```
3. Parse JSON result:
   - If `status: error` mentions "Multiple matches", show options and ask to be more specific. Stop.
   - If `status: error` mentions "No task found", show the error and stop.
   - If `status: ok`, confirm:
     ```
     ✓ Completed: TASK
     N tasks remaining active.
     ```

### Command: `clear`

1. Run the write script:
   ```bash
   PYTHONIOENCODING=utf-8 python3 tools/personal_todo_write.py clear
   ```
2. Parse JSON result:
   - If `archived: 0`, display: `Nothing to archive — no Done or Withdrawn items in Active section.`
   - Otherwise:
     ```
     Archived N items: X Done, Y Withdrawn.
     ```

## Priority Levels

- **High** — time-sensitive or blocking (renewals, disputes with deadlines, medical)
- **Med** — important but not urgent (gifts, household upgrades, scheduling)
- **Low** — nice-to-have (organize, declutter, optional admin)

## Status Values

- **Pending** — not started
- **In Progress** — actively being worked on
- **Done** — actually completed
- **Withdrawn** — cancelled, deprioritized, or made irrelevant — does NOT count as a completion

## Differences from `/todo`

- **No pipeline sync** — personal todos don't connect to the job pipeline.
- **No daily log** — personal velocity isn't tracked here. Use `/checkout` for the job-search daily log.
- **No cross-references** — task text isn't matched against pipeline/networking. Personal life is its own graph.
- **Vault-located** — file lives in the Obsidian vault, accessed by absolute path. Override with `--file <path>` if needed.

## Wispr / Capture Routing

When `/wispr` or `/remember` classifies a chunk as a personal action item ("I need to call Chase", "set up Lift Pink", "buy a gift for X"), route it here via:

```bash
PYTHONIOENCODING=utf-8 python3 tools/personal_todo_write.py add "TASK" "PRIORITY" "DUE" "Source: [[wispr-...]] (Wispr HH:MM)"
```

Always include the source backref in Notes so the to-do traces back to the moment of intent.
