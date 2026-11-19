#!/usr/bin/env python3
"""Check that a draft final reply carries the items the skill requires.

Usage: check-reply.py <reply file> [--source] [--stack tailwind-static]
Always: the first 12 lines hold the two adapter lines ("Project:" and "Check:").
--source: a differences table exists: the header "Area | Source | Build" (or its Indonesian
labels), or, for a translated header, any table of 5 or more columns with a separator row.
--stack tailwind-static: the reply mentions mock-data.json and the mobile menu
(the preset's "Required in every reply" items): the words mobile menu, disclosure,
hamburger or navigation must appear.
The labels are accepted in English or Indonesian (see LABELS); to support another
language, add its words to LABELS. Bold or other marks around a label are ignored.
It proves that an item is PRESENT, not that it is right: reading the content stays your job.
Failure lines: FAIL <file>:<line> | <what is missing> | FIX: <what to add>. Last line: OK or FAILED n.
"""
import re
import sys
from pathlib import Path


LABELS = {  # English | Indonesian, matched case-insensitively
    "project": "Project|Proyek",
    "check": "Check|Pemeriksaan|Pengecekan|Cek",
    "source": "Source|Sumber",
    "build": "Build|Hasil|Implementasi",
    "menu": "mobile menu|disclosure|hamburger|navigation|menu seluler|menu mobile|navigasi",
}


def has_wide_table(lines: list) -> bool:
    """True when a header row of 5+ cells is followed by a separator row (any language)."""
    for i in range(len(lines) - 1):
        row = lines[i].strip()
        if row.startswith("|") and len([c for c in row.strip("|").split("|") if c.strip()]) >= 5:
            if re.match(r"^\s*\|?\s*:?-{2,}", lines[i + 1]):
                return True
    return False


def main() -> int:
    args, path, source, stack, i = sys.argv[1:], None, False, None, 0
    while i < len(args):
        if args[i] == "--source":
            source, i = True, i + 1
        elif args[i] == "--stack" and i + 1 < len(args):
            stack, i = args[i + 1], i + 2
        elif args[i].startswith("--") or path is not None:
            path = None
            break
        else:
            path, i = args[i], i + 1
    if path is None or stack not in (None, "tailwind-static"):
        print("FAIL usage | need one reply file; --stack takes tailwind-static | FIX: check-reply.py <file> [--source] [--stack tailwind-static]")
        return 1
    f = Path(path)
    if not f.is_file():
        print(f"FAIL {f} | file not found | FIX: write the draft reply to a file first")
        return 1
    text = f.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    fails: list = []
    head = lines[:12]
    missing = [w for w in ("Project:", "Check:") if not any(re.match(rf"^\W*(?:{LABELS[w[:-1].lower()]})\W*:", ln, re.I) for ln in head)]
    if missing:
        fails.append(f"FAIL {f}:1 | adapter line missing in the first 12 lines: {', '.join(missing)} | FIX: start the reply with the two lines from references/project-adapter.md (Project: ... and Check: ..., or Proyek: / Pemeriksaan: in Indonesian)")
    if source and not re.search(rf"\|\s*Area\s*\|\s*(?:{LABELS['source']})\s*\|\s*(?:{LABELS['build']})\s*\|", text, re.I) and not has_wide_table(lines):
        fails.append(f"FAIL {f}:1 | no differences table | FIX: add the table with header | Area | Source | Build | Why | Decision needed | (translate the words if you like, keep 5 columns; write 'None' only after a real comparison)")
    if stack == "tailwind-static":
        if "mock-data.json" not in text:
            fails.append(f"FAIL {f}:1 | no mock-data.json line | FIX: under Questions, propose mock-data.json (name the component and how many times it repeats), or say nothing repeats three or more times")
        if not re.search(LABELS["menu"], text, re.I):
            fails.append(f"FAIL {f}:1 | no mobile menu line | FIX: say the disclosure menu was added and is extrapolated, or that the navigation links fit at every width")
    for line in fails:
        print(line)
    print("OK" if not fails else f"FAILED {len(fails)}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
