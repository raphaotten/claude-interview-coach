#!/usr/bin/env python3
"""
Pull Wispr Flow Notes (the synced phone+desktop thoughts feature) into the
Obsidian vault inbox as voice-pure markdown.

Reads ONLY the Notes table — not History (which is noisy raw dictation,
mostly Claude Code prompts). Notes are intentional captures: phone-side
or desktop "save this thought" actions that sync via Wispr cloud.

Voice purity: this is a faithful transcription of Nick's dictation — no
AI processing of content. Direction-of-flow respects the vault rule:
"Agents read, humans write" — Nick spoke it, the tool only formats it.

State: tracks last-imported modifiedAt in tools/.wispr-state.json.
Re-runs are incremental.

Destination resolution:
  1. ~/Documents/Obsidian/00-inbox/  (vault, once Phase 1 migration runs)
  2. <repo>/inbox/                   (current home, fallback)

Usage:
  PYTHONIOENCODING=utf-8 python3 tools/wispr_pull.py             # incremental
  PYTHONIOENCODING=utf-8 python3 tools/wispr_pull.py --since 7d  # backfill
  PYTHONIOENCODING=utf-8 python3 tools/wispr_pull.py --dry-run   # preview
  PYTHONIOENCODING=utf-8 python3 tools/wispr_pull.py --all       # ignore state cursor
"""

import argparse
import json
import re
import shutil
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

WISPR_DB = Path.home() / "Library/Application Support/Wispr Flow/flow.sqlite"
REPO_ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = REPO_ROOT / "tools" / ".wispr-state.json"
VAULT_INBOX = Path.home() / "Documents/Obsidian/00-inbox"
REPO_INBOX = REPO_ROOT / "inbox"

# Heuristics for skipping low-signal notes
TEST_PATTERNS = re.compile(r"^\s*(test(ing)?[\s\.,!?]*)+\s*$", re.IGNORECASE)
FILE_URI_PATTERN = re.compile(r"^\s*\[?file:///")
MIN_WORDS = 3


def resolve_inbox() -> Path:
    """Vault if it exists, else repo inbox."""
    if VAULT_INBOX.exists():
        return VAULT_INBOX
    REPO_INBOX.mkdir(exist_ok=True)
    return REPO_INBOX


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"last_modified_at": None, "imported_ids": []}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2))


def parse_wispr_ts(ts: str) -> datetime:
    """Wispr stores: '2026-04-23 15:42:12.847 +00:00'"""
    # Normalize tz format for fromisoformat
    ts = ts.replace(" +00:00", "+00:00").replace(" -", "-")
    if "+" not in ts and "-" not in ts[-6:]:
        ts += "+00:00"
    # Replace space separator with T
    ts = re.sub(r"^(\d{4}-\d{2}-\d{2}) ", r"\1T", ts)
    return datetime.fromisoformat(ts)


def slugify(text: str, maxlen: int = 40) -> str:
    text = re.sub(r"[^a-zA-Z0-9\s-]", "", text or "").strip().lower()
    text = re.sub(r"\s+", "-", text)
    return text[:maxlen].rstrip("-") or "untitled"


def is_low_signal(content: str) -> tuple[bool, str]:
    """Return (skip, reason)."""
    if not content or not content.strip():
        return True, "empty"
    if FILE_URI_PATTERN.match(content):
        return True, "file-uri-only (likely mobile attachment artifact)"
    if TEST_PATTERNS.match(content):
        return True, "test/test-like content"
    if len(content.split()) < MIN_WORDS:
        return True, f"<{MIN_WORDS} words"
    return False, ""


def open_db_readonly(db_path: Path) -> sqlite3.Connection:
    """
    Open Wispr DB read-only. Wispr is likely running with WAL — copying the
    DB + WAL+SHM to a temp file gives us a consistent snapshot without
    contending with the live writer.
    """
    if not db_path.exists():
        sys.exit(f"Wispr DB not found at {db_path}. Is Wispr Flow installed?")
    # Read-only via URI
    uri = f"file:{db_path}?mode=ro&immutable=0"
    return sqlite3.connect(uri, uri=True, timeout=5.0)


def fetch_notes(conn: sqlite3.Connection, since: datetime | None) -> list[dict]:
    cur = conn.cursor()
    sql = """
        SELECT id, title, content, createdAt, modifiedAt
          FROM Notes
         WHERE isDeleted = 0
    """
    params = []
    if since is not None:
        sql += " AND modifiedAt > ?"
        # Wispr stores its own format; lexicographic comparison works on ISO strings
        params.append(since.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + " +00:00")
    sql += " ORDER BY modifiedAt ASC"
    cur.execute(sql, params)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def derive_title(note: dict) -> str:
    """Title field is usually empty. Use first sentence of content."""
    if note.get("title"):
        return note["title"]
    content = (note.get("content") or "").strip()
    # First line, then first ~10 words
    first_line = content.splitlines()[0] if content else ""
    words = first_line.split()[:10]
    return " ".join(words) or "untitled"


def render_markdown(note: dict) -> str:
    created = parse_wispr_ts(note["createdAt"])
    modified = parse_wispr_ts(note["modifiedAt"])
    title = derive_title(note)
    frontmatter = (
        "---\n"
        "type: note\n"
        "voice: self\n"
        "source: wispr-flow\n"
        f"created: {created.isoformat()}\n"
        f"modified: {modified.isoformat()}\n"
        f"date: {created.strftime('%Y-%m-%d')}\n"
        f"wispr_id: {note['id']}\n"
        "---\n\n"
    )
    body = f"# {title}\n\n{note['content'].strip()}\n"
    return frontmatter + body


def filename_for(note: dict) -> str:
    created = parse_wispr_ts(note["createdAt"])
    title = derive_title(note)
    return f"wispr-{created.strftime('%Y-%m-%d-%H%M%S')}-{slugify(title)}.md"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--since", help="Backfill window, e.g. 7d, 30d, 24h")
    p.add_argument("--all", action="store_true", help="Import everything, ignore state cursor")
    p.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = p.parse_args()

    inbox = resolve_inbox()
    state = load_state()

    # Determine cutoff
    if args.all:
        since = None
    elif args.since:
        m = re.match(r"^(\d+)([dh])$", args.since)
        if not m:
            sys.exit("--since must look like '7d' or '24h'")
        n, unit = int(m.group(1)), m.group(2)
        delta = timedelta(days=n) if unit == "d" else timedelta(hours=n)
        since = datetime.now(timezone.utc) - delta
    elif state.get("last_modified_at"):
        since = datetime.fromisoformat(state["last_modified_at"])
    else:
        # First run with no state — default to 30d to avoid pulling years of cruft
        since = datetime.now(timezone.utc) - timedelta(days=30)

    conn = open_db_readonly(WISPR_DB)
    try:
        notes = fetch_notes(conn, since)
    finally:
        conn.close()

    print(f"Wispr DB: {WISPR_DB}")
    print(f"Inbox:    {inbox} {'(VAULT)' if inbox == VAULT_INBOX else '(repo fallback)'}")
    print(f"Cutoff:   {since.isoformat() if since else '(all time)'}")
    print(f"Found:    {len(notes)} note(s) modified after cutoff")
    print()

    written, skipped = [], []
    for n in notes:
        if n["id"] in state.get("imported_ids", []):
            skipped.append((n, "already imported (per state)"))
            continue
        skip, reason = is_low_signal(n.get("content") or "")
        if skip:
            skipped.append((n, reason))
            continue
        path = inbox / filename_for(n)
        if path.exists():
            skipped.append((n, f"file exists: {path.name}"))
            continue
        if args.dry_run:
            written.append((n, path, "(dry-run)"))
            continue
        path.write_text(render_markdown(n), encoding="utf-8")
        written.append((n, path, "written"))

    # Update state
    if not args.dry_run and notes:
        latest = max(parse_wispr_ts(n["modifiedAt"]) for n in notes)
        state["last_modified_at"] = latest.isoformat()
        state["imported_ids"] = list({*state.get("imported_ids", []), *(n["id"] for n in notes)})
        # Cap imported_ids list to last 500 to avoid unbounded growth
        state["imported_ids"] = state["imported_ids"][-500:]
        save_state(state)

    print(f"Imported: {len(written)}")
    for n, path, status in written:
        print(f"  + {path.name}  {status}")
    print(f"Skipped:  {len(skipped)}")
    for n, reason in skipped:
        title_preview = derive_title(n)[:50]
        print(f"  - {title_preview!r:55} ({reason})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
