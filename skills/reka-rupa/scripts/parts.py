#!/usr/bin/env python3
"""Track the parts of a big request so a new session can carry on.

Usage:
  parts.py add "<name> | <outcome>"     append a part
  parts.py list                          show all parts, [x] done, [ ] open
  parts.py next                          print the first open part, or ALL DONE
  parts.py done <n>                      mark part n done
Option --file <path> (before the command) sets the state file;
default .agents/reka-rupa/parts.json. Bad input prints: FAIL ... | FIX: ...
"""
import json
import os
import re
import sys
from pathlib import Path

DEFAULT = ".agents/reka-rupa/parts.json"
USAGE = 'parts.py [--file <path>] add "<name> | <outcome>" | list | next | done <n>'


def die(what: str, fix: str = USAGE) -> int:
    print(f"FAIL parts | {what} | FIX: {fix}")
    return 1


def run() -> int:
    argv = sys.argv[1:]
    path = Path(DEFAULT)
    if argv[:1] == ["--file"]:
        if len(argv) < 2:
            return die("--file needs a path")
        path, argv = Path(argv[1]), argv[2:]
    if not argv:
        return die("no command")
    cmd, rest = argv[0], argv[1:]
    try:
        parts = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else []
    except (OSError, ValueError):
        return die(f"{path} is not valid JSON", f"fix or delete {path}")
    if not isinstance(parts, list) or not all(
        isinstance(p, dict) and {"name", "outcome", "done"} <= p.keys() and isinstance(p["done"], bool)
        for p in parts
    ):
        return die(f"{path} is not a list of parts", f"fix or delete {path}")

    def save() -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_name(path.name + ".tmp")
        tmp.write_text(json.dumps(parts, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        os.replace(tmp, path)

    if cmd == "add":
        if len(rest) != 1 or "|" not in rest[0]:
            return die('add needs one quoted text "<name> | <outcome>"')
        name, outcome = (s.strip() for s in rest[0].split("|", 1))
        if not name or not outcome:
            return die("name and outcome must both be filled")
        parts.append({"name": name, "outcome": outcome, "done": False})
        save()
        print(f"ADDED {len(parts)} | {name}")
    elif cmd == "list":
        for i, p in enumerate(parts, 1):
            print(f"[{'x' if p['done'] else ' '}] {i} {p['name']} | {p['outcome']}")
        if not parts:
            print("NO PARTS")
    elif cmd == "next":
        for i, p in enumerate(parts, 1):
            if not p["done"]:
                print(f"NEXT {i} {p['name']} | {p['outcome']}")
                break
        else:
            print("ALL DONE" if parts else "NO PARTS")
    elif cmd == "done":
        if len(rest) != 1 or not re.fullmatch(r"[0-9]+", rest[0]) or not 1 <= int(rest[0]) <= len(parts):
            return die(f"done needs a part number from 1 to {len(parts)}")
        parts[int(rest[0]) - 1]["done"] = True
        save()
        print(f"DONE {rest[0]}")
    else:
        return die(f"unknown command '{cmd}'")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(run())
    except OSError as e:
        sys.exit(die(f"cannot write the state file ({e.strerror})", "check the folder permissions or pass --file <path>"))
