#!/usr/bin/env python3
"""Count words and check that the skill files agree with each other.

Usage: check-skill.py <skill dir> [--strict]
<skill dir> holds SKILL.md and references/. Words are whitespace-separated tokens.
Always checks: every references/*.md is named in the "Reference map" of SKILL.md,
every file named there exists, and a heading listed in UNIQUE appears in one file only.
--strict also fails a file over its word budget (a growth guard: today's size plus 30).
--load prints, for five kinds of run, the words loaded now and before the slimming.
Failure lines: FAIL <file>:<line> | <what is wrong> | FIX: <what to do>. Last line: OK or FAILED n.
"""
import re
import sys
from pathlib import Path

OLD_SKILL_WORDS = 2434  # SKILL.md before review mode moved out and the text was cut
BUDGET = {
    "SKILL.md": 1385,
    "references/review.md": 470,
    "references/plan-format.md": 400,
    "references/accessibility.md": 904,
    "references/code-quality.md": 570,
    "references/copy-and-mock.md": 556,
    "references/design-craft.md": 1032,
    "references/design-systems.md": 1096,
    "references/fidelity-protocol.md": 1161,
    "references/project-adapter.md": 615,
    "references/responsive.md": 650,
    "references/stack-tailwind-static.md": 1116,
    "references/web-standards.md": 1044,
}
UNIQUE = ["Required in every reply"]
_COMMON = ["project-adapter", "accessibility", "responsive", "copy-and-mock"]
LOADS = {  # a run always loads SKILL.md plus these references
    "design": _COMMON + ["design-craft"],
    "code": _COMMON + ["code-quality", "web-standards"],
    "adopt": _COMMON + ["code-quality", "web-standards", "fidelity-protocol", "design-systems"],
    "adopt-preset": _COMMON + ["code-quality", "web-standards", "fidelity-protocol", "design-systems", "stack-tailwind-static"],
    "review": ["review", "accessibility", "responsive", "code-quality", "copy-and-mock", "web-standards", "design-craft"],
}


def fail(fails: list, where: str, what: str, fix: str) -> None:
    fails.append(f"FAIL {where} | {what} | FIX: {fix}")


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    strict = "--strict" in sys.argv
    if len(args) != 1:
        print("FAIL usage | need one folder | FIX: check-skill.py skills/reka-rupa [--strict]")
        return 1
    root = Path(args[0])
    skill = root / "SKILL.md"
    if not skill.is_file():
        print(f"FAIL {skill} | file not found | FIX: pass the folder that holds SKILL.md")
        return 1
    files = [skill] + sorted((root / "references").glob("*.md"))
    fails: list = []
    total = 0
    words_of: dict = {}
    for f in files:
        rel = f.relative_to(root).as_posix()
        words = len(f.read_text(encoding="utf-8", errors="replace").split())
        total += words
        words_of[f.stem] = words
        budget = BUDGET.get(rel)
        note = f" (budget {budget})" if budget else ""
        print(f"WORDS {rel} {words}{note}")
        if strict and budget and words > budget:
            fail(fails, rel, f"{words} words, budget is {budget}", f"cut {words - budget} words; remove repeats first")
    print(f"TOTAL {total}")
    if "--load" in sys.argv:
        for name, refs in LOADS.items():
            if any(r not in words_of for r in refs):
                continue
            extra = sum(words_of[r] for r in refs)
            now = words_of["SKILL"] + extra
            before = OLD_SKILL_WORDS + extra - (words_of["review"] if "review" in refs else 0)
            print(f"LOAD {name} now {now} before {before}")
        print("NOTE review rules are loaded only with --mode=review; before, they were always inside SKILL.md")

    lines = skill.read_text(encoding="utf-8", errors="replace").splitlines()
    start = next((i for i, ln in enumerate(lines) if ln.strip() == "## Reference map"), None)
    named: dict = {}
    if start is None:
        fail(fails, "SKILL.md", "no '## Reference map' section", "add the section that lists each reference file")
    else:
        for i in range(start + 1, len(lines)):
            if lines[i].startswith("## "):
                break
            for m in re.finditer(r"references/([\w.-]+\.md)", lines[i]):
                named.setdefault(m.group(1), i + 1)
    on_disk = {f.name for f in (root / "references").glob("*.md")}
    for name, ln in named.items():
        if name not in on_disk:
            fail(fails, f"SKILL.md:{ln}", f"map names references/{name}, which does not exist", "create the file or remove the map row")
    for name in sorted(on_disk - set(named)):
        fail(fails, f"references/{name}:1", "file is not in the Reference map of SKILL.md", f"add a map row for references/{name}")

    for title in UNIQUE:
        hits = []
        for f in files:
            for n, ln in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                if ln.startswith("#") and title in ln:
                    hits.append(f"{f.relative_to(root).as_posix()}:{n}")
        if len(hits) > 1:
            fail(fails, hits[1], f"heading '{title}' is defined {len(hits)} times ({', '.join(hits)})", "keep the first, point to it from the others")

    for line in fails:
        print(line)
    print("OK" if not fails else f"FAILED {len(fails)}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
