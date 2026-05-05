#!/usr/bin/env python3
"""
personal_todo_write.py — Atomic mutations for the vault personal-todos.md.

Slim sibling of tools/todo_write.py — no pipeline sync, no daily log, no
cross-references. Personal todos live in the Obsidian vault, not the
job-search project.

Default file: ~/Documents/Obsidian/30-projects/personal/data/personal-todos.md
Override with --file <path>.

Commands:
  add <task> <priority> <due> <notes>  — append row to Active section
  done <task_fragment>                 — move matching row to Done
  clear                                — move Done/Withdrawn rows to Done section

Output: JSON to stdout
  Success: {"status": "ok", "action": "...", "summary": "...", ...extra}
  Failure: {"status": "error", "message": "..."}

Usage:
  PYTHONIOENCODING=utf-8 python3 tools/personal_todo_write.py add "Task" Med 2026-05-15 "Notes"
  PYTHONIOENCODING=utf-8 python3 tools/personal_todo_write.py done "task fragment"
  PYTHONIOENCODING=utf-8 python3 tools/personal_todo_write.py clear
"""
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

DEFAULT_TODOS_FILE = Path.home() / "Documents/Obsidian/30-projects/personal/data/personal-todos.md"
DONE_HEADER = "| Task | Completed | Notes |"
DONE_SEP = "| --- | --- | --- |"


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

def read_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError):
        return ""


def write_atomic(path: Path, content: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    os.replace(tmp, path)


def out_ok(action: str, summary: str, **extra) -> None:
    d = {"status": "ok", "action": action, "summary": summary}
    d.update(extra)
    print(json.dumps(d, ensure_ascii=False))


def out_error(message: str) -> None:
    print(json.dumps({"status": "error", "message": message}, ensure_ascii=False))
    sys.exit(1)


# ---------------------------------------------------------------------------
# Table row helpers
# ---------------------------------------------------------------------------

def is_data_row(line: str) -> bool:
    if not line.startswith("|"):
        return False
    if re.match(r"^\|\s*:?-+:?\s*\|", line):
        return False
    if line.startswith("| Task"):
        return False
    return True


def parse_cols(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def fmt_active(task: str, priority: str, due: str, status: str, notes: str) -> str:
    return f"| {task} | {priority} | {due} | {status} | {notes} |"


def fmt_done(task: str, completed: str, notes: str) -> str:
    return f"| {task} | {completed} | {notes} |"


# ---------------------------------------------------------------------------
# Section navigation
# ---------------------------------------------------------------------------

def find_section(lines: list[str], header: str) -> tuple[int, int]:
    start = -1
    for i, line in enumerate(lines):
        if line.strip() == header:
            start = i
            break
    if start == -1:
        return (-1, -1)
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    return (start, end)


def table_insert_pos(lines: list[str], sec_start: int, sec_end: int) -> int:
    last = -1
    for i in range(sec_start, sec_end):
        if is_data_row(lines[i]):
            last = i
    if last != -1:
        return last + 1
    for i in range(sec_start, sec_end):
        if lines[i].startswith("|") and "---" in lines[i]:
            return i + 1
    for i in range(sec_start, sec_end):
        if lines[i].startswith("|"):
            return i + 1
    return sec_end


def insert_into_done(lines: list[str], row: str) -> None:
    """Append a row to the Done section, creating it if absent."""
    sec_start, sec_end = find_section(lines, "## Done")
    if sec_start == -1:
        lines.append("")
        lines.append("## Done")
        lines.append("")
        lines.append(DONE_HEADER)
        lines.append(DONE_SEP)
        lines.append(row)
    else:
        pos = table_insert_pos(lines, sec_start, sec_end)
        lines.insert(pos, row)


# ---------------------------------------------------------------------------
# File load / save
# ---------------------------------------------------------------------------

def load_todos(path: Path) -> tuple[str, list[str]]:
    content = read_file(path)
    if not content:
        out_error(f"File not found or empty: {path}")
    lines = [ln.rstrip("\n").rstrip("\r") for ln in content.splitlines(keepends=True)]
    return content, lines


def save_lines(path: Path, lines: list[str], original_content: str) -> None:
    content = "\n".join(lines)
    if original_content.endswith("\n"):
        content += "\n"
    write_atomic(path, content)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_add(args: list[str], todos_path: Path) -> None:
    if not args:
        out_error("Usage: add <task> [priority] [due] [notes]")

    task = args[0]
    priority = args[1] if len(args) > 1 and args[1] not in ("--", "-", "") else "Med"
    due = args[2] if len(args) > 2 and args[2] not in ("--", "-", "") else "—"
    notes = args[3] if len(args) > 3 and args[3] not in ("--", "-", "") else "—"

    if priority not in ("High", "Med", "Low"):
        priority = "Med"

    content, lines = load_todos(todos_path)

    act_start, act_end = find_section(lines, "## Active")
    if act_start == -1:
        out_error("Could not find ## Active section in personal-todos.md")

    warning = None
    task_lower = task.lower()
    for i in range(act_start, act_end):
        if is_data_row(lines[i]):
            cols = parse_cols(lines[i])
            if cols and cols[0] and task_lower in cols[0].lower():
                warning = f"Similar task already exists: {cols[0]}"
                break

    pos = table_insert_pos(lines, act_start, act_end)
    lines.insert(pos, fmt_active(task, priority, due, "Pending", notes))
    save_lines(todos_path, lines, content)

    result: dict = {
        "status": "ok", "action": "added",
        "summary": f"Added: {task} [{priority}]",
        "task": task, "priority": priority, "due": due,
    }
    if warning:
        result["warning"] = warning
    print(json.dumps(result, ensure_ascii=False))


def cmd_done(args: list[str], todos_path: Path) -> None:
    if not args:
        out_error("Usage: done <task_fragment>")

    fragment = args[0].lower()
    today_str = date.today().strftime("%Y-%m-%d")

    content, lines = load_todos(todos_path)

    act_start, act_end = find_section(lines, "## Active")
    if act_start == -1:
        out_error("Could not find ## Active section in personal-todos.md")

    matches = []
    for i in range(act_start, act_end):
        if not is_data_row(lines[i]):
            continue
        cols = parse_cols(lines[i])
        if cols and cols[0] and fragment in cols[0].lower():
            matches.append((i, cols))

    if not matches:
        out_error(f"No task found matching: {args[0]}")
    if len(matches) > 1:
        options = "\n".join(f"  - {c[0]}" for _, c in matches)
        out_error(f"Multiple matches — be more specific:\n{options}")

    row_idx, cols = matches[0]
    task = cols[0]
    notes = " | ".join(cols[4:]) if len(cols) > 4 else "—"

    suffix = f"Completed {today_str}"
    completed_notes = suffix if notes in ("—", "") else f"{suffix} | {notes}"

    lines.pop(row_idx)
    insert_into_done(lines, fmt_done(task, today_str, completed_notes))
    save_lines(todos_path, lines, content)

    act_s, act_e = find_section(lines, "## Active")
    remaining = sum(1 for i in range(act_s, act_e) if is_data_row(lines[i])) if act_s != -1 else 0

    out_ok("done", f"Completed: {task}", task=task, remaining_active=remaining)


def cmd_clear(todos_path: Path) -> None:
    today_str = date.today().strftime("%Y-%m-%d")

    content, lines = load_todos(todos_path)

    act_start, act_end = find_section(lines, "## Active")
    if act_start == -1:
        out_error("Could not find ## Active section in personal-todos.md")

    to_move = []
    for i in range(act_start, act_end):
        if not is_data_row(lines[i]):
            continue
        cols = parse_cols(lines[i])
        if len(cols) >= 4 and cols[3] in ("Done", "Withdrawn"):
            to_move.append((i, cols))

    if not to_move:
        out_ok("clear", "No Done or Withdrawn items to archive", archived=0, done=0, withdrawn=0)
        return

    done_count = sum(1 for _, c in to_move if c[3] == "Done")
    withdrawn_count = sum(1 for _, c in to_move if c[3] == "Withdrawn")

    done_rows = []
    for _, cols in to_move:
        task = cols[0]
        status = cols[3] if len(cols) > 3 else "Done"
        notes = " | ".join(cols[4:]) if len(cols) > 4 else "—"
        completed_date = today_str if status == "Done" else f"Withdrawn {today_str}"
        done_rows.append(fmt_done(task, completed_date, notes))

    for idx, _ in reversed(to_move):
        lines.pop(idx)

    for row in done_rows:
        insert_into_done(lines, row)

    save_lines(todos_path, lines, content)

    parts = []
    if done_count:
        parts.append(f"{done_count} Done")
    if withdrawn_count:
        parts.append(f"{withdrawn_count} Withdrawn")
    out_ok("clear", f"Archived: {' + '.join(parts)}",
           done=done_count, withdrawn=withdrawn_count, archived=done_count + withdrawn_count)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    argv = sys.argv[1:]
    todos_path = DEFAULT_TODOS_FILE
    filtered = []
    i = 0
    while i < len(argv):
        if argv[i] == "--file" and i + 1 < len(argv):
            todos_path = Path(argv[i + 1]).expanduser()
            i += 2
        else:
            filtered.append(argv[i])
            i += 1

    if not filtered:
        out_error("Usage: personal_todo_write.py <add|done|clear> [args...]")

    cmd = filtered[0].lower()
    extra_args = filtered[1:]

    if cmd == "add":
        cmd_add(extra_args, todos_path)
    elif cmd == "done":
        cmd_done(extra_args, todos_path)
    elif cmd == "clear":
        cmd_clear(todos_path)
    else:
        out_error(f"Unknown command: {cmd}. Use: add, done, clear")


if __name__ == "__main__":
    main()
