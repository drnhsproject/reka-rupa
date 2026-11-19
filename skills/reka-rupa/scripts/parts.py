#!/usr/bin/env python3
"""List the parts of a split design request, read from the plan files themselves.

Usage:
  parts.py list [--series <name>]   every part: [x] DONE, [ ] open, with its status
  parts.py next [--series <name>]   the first part not DONE, or ALL DONE
Option --dir <path> (before the command) sets the plans folder; default
.agents/plans/design. The plan files are the only record: mark a part finished by
setting its header to `Status: DONE`. Bad input prints: FAIL ... | FIX: ...
"""
import re
import sys
from pathlib import Path

USAGE = "parts.py [--dir <path>] list|next [--series <name>]"


def die(what: str, fix: str = USAGE) -> int:
    print(f"FAIL parts | {what} | FIX: {fix}")
    return 1


def read_parts(folder: Path, series: str | None) -> list[tuple]:
    found = []
    skipped = []
    for f in sorted(folder.rglob("*.md")):
        head = f.read_text(encoding="utf-8", errors="replace")[:1500]
        part = re.search(r"^.*\bPart:\s*(\d+)\s+of\s+(\d+)", head, re.M)
        name = re.search(r"Series:\s*([\w.-]+)", head)
        status = re.search(r"^Status:\s*([A-Z ]+?)\s*(?:·|$)", head, re.M)
        title = re.search(r"^# Plan:\s*(.+)$", head, re.M)
        if not (part and name and status):
            if re.search(r"^Status:", head, re.M) or "Part:" in head:
                skipped.append(f)
            continue
        if series and name.group(1) != series:
            continue
        found.append((name.group(1), int(part.group(1)), int(part.group(2)), status.group(1), title.group(1) if title else f.stem, f))
    for f in skipped:
        print(f"WARN {f} | header unreadable (need Status:, Part: n of m, Series:) | FIX: correct the header", file=sys.stderr)
    return sorted(found, key=lambda x: (x[0], x[1]))


def run() -> int:
    argv = sys.argv[1:]
    folder = Path(".agents/plans/design")
    if argv[:1] == ["--dir"]:
        if len(argv) < 2:
            return die("--dir needs a path")
        folder, argv = Path(argv[1]), argv[2:]
    if not argv or argv[0] not in ("list", "next"):
        return die("need the command list or next")
    series = None
    if argv[1:2] == ["--series"]:
        if len(argv) < 3:
            return die("--series needs a name")
        series = argv[2]
    elif len(argv) > 1:
        return die(f"unexpected '{argv[1]}'")
    if not folder.is_dir():
        print("NO PARTS")
        return 0
    parts = read_parts(folder, series)
    if not parts:
        print("NO PARTS")
    elif argv[0] == "list":
        for s, n, m, st, title, f in parts:
            print(f"[{'x' if st == 'DONE' else ' '}] {s} {n}/{m} {st} | {title} | {f}")
    else:
        for s, n, m, st, title, f in parts:
            if st != "DONE":
                print(f"NEXT {s} {n}/{m} {st} | {title} | {f}")
                break
        else:
            print("ALL DONE")
    return 0


if __name__ == "__main__":
    sys.exit(run())
