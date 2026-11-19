#!/usr/bin/env python3
"""Check a built web folder for the mechanical rules of references/web-standards.md.

Usage: check-web.py <folder> [--tokens <file>]...
Scans *.html and *.css (not node_modules, .git, dist, build). Checks: inline style="...", px in layout
properties (css and <style> blocks) and in Tailwind arbitrary values, <img> without
alt/width/height, loading="lazy" on the first image, href="#", not exactly one <h1>,
and a missing <title>. Media-query widths must be rem or em (px is flagged, as in
web-standards.md), also Tailwind min-[..px]: and max-[..px]: variants. Hairlines
(borders, outlines), shadows, 0px and 1px are allowed. A raw colour (#hex, rgb(), hsl()) in
a declaration, or in a Tailwind class such as bg-[#fff], is flagged unless the line defines a
custom property (--name: value); --tokens <file> skips that file's colours (your token file).
A file over 2 MB is not scanned (FAIL line). Failure lines: FAIL <file>:<line> | <what is wrong> | FIX: <what to do>. Last line: OK or FAILED n.
A FAIL that the design source or the project forces is reported in the differences table, not fixed.
"""
import bisect
import os
import re
import sys
from pathlib import Path

PX_PROP = re.compile(
    r"(?<![\w-])(margin|padding|gap|row-gap|column-gap|font-size|line-height|width|height|"
    r"min-width|max-width|min-height|max-height|border-radius|top|left|right|bottom)[\w-]*"
    r"\s*:\s*([^;{}]*)"
)
PX_VALUE = re.compile(r"(-?\d*\.?\d+)px")
MEDIA = re.compile(r"@media[^{]*")
TW_VARIANT = re.compile(r"(?<![\w-])((?:min|max)-\[(-?\d*\.?\d+)px\]):")
TW_ARB = re.compile(r"\[(-?\d*\.?\d+)px\]")
TW_PREFIX = re.compile(r"(?:[\w-]+:)*-?(?:m|p|gap|w|h|text|min-w|max-w|min-h|max-h|top|left|right|bottom|[mp][xytblr])-")
TOKEN = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_:-")
IMG_START = re.compile(r"<img\b", re.I)
MAX_BYTES = 2_000_000
COMMENT_LEAD = re.compile(r"^(?:/\*.*?\*/\s*)+")
DECL = re.compile(r"([\w-]+)\s*:\s*([^;{}]*)")
RAW = re.compile(r"#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?)\(")
TW_COLOUR = re.compile(r"(?:bg|text|border|fill|stroke|from|to|via|ring|shadow|outline|decoration|accent|caret)-\[[^\]]{0,80}\]")
NOT_COLOUR = re.compile(r"url\([^)]*\)|\"[^\"]*\"|'[^']*'")
FIX_COLOUR = "use a token (var(--...)) or propose a new token"


def raw_colours(value: str) -> list:
    """Raw colours in a value. rgb()/hsl() whose arguments start with var() are token colours."""
    value = NOT_COLOUR.sub("", value)
    found = []
    for c in RAW.finditer(value):
        if not c.group(0).startswith("#") and value[c.end():].lstrip().startswith("var("):
            continue  # hsl(var(--x)), rgb(var(--x) / .5): the colour comes from a token
        found.append(value[c.start():c.start() + 9].strip())
    return found


def line_finder(text: str):
    breaks = [i for i, c in enumerate(text) if c == "\n"]
    return lambda pos: bisect.bisect_left(breaks, pos) + 1


def tw_px(text: str):
    """Yield (position, token, px) for classes such as md:w-[350px], found without backtracking."""
    for m in TW_ARB.finditer(text):
        i = j = m.start()
        while j > 0 and text[j - 1] in TOKEN and i - j < 200:
            j -= 1
        if i - j < 200 and TW_PREFIX.fullmatch(text[j:i]):
            yield j, text[j:m.end()], m.group(1)


def style_blocks(text: str):
    """Yield (offset, css) for each <style> block; an unclosed block ends the search."""
    low, pos = text.lower(), 0
    while True:
        a = low.find("<style", pos)
        gt = low.find(">", a) if a >= 0 else -1
        end = low.find("</style", gt) if gt >= 0 else -1
        if end < 0:
            return
        yield gt + 1, text[gt + 1:end]
        pos = end


def find_imgs(text: str):
    """Yield (position, tag) for each <img> tag in one pass over the text."""
    pos = 0
    while True:
        m = IMG_START.search(text, pos)
        if not m:
            return
        i, quote = m.end(), None
        while i < len(text):
            c = text[i]
            if quote:
                if c == quote:
                    quote = None
            elif c in "\"'":
                quote = c
            elif c in "<>":
                break
            i += 1
        end = i + 1 if i < len(text) and text[i] == ">" else i
        yield m.start(), text[m.start():end]
        pos = max(end, m.end())


def rem(px: str) -> str:
    v = float(px) / 16
    return f"{v:g}rem"


def check_css(rel: str, text: str, base: int, fails: list, colour: bool = True) -> None:
    lines = text.splitlines()
    brace_next, cur = [False] * len(lines), False  # does the next non-blank line start with "{"?
    for i in range(len(lines) - 1, -1, -1):
        brace_next[i] = cur
        code = COMMENT_LEAD.sub("", lines[i].strip())  # blank and comment-only lines are skipped
        if code:
            cur = code.startswith("{")
    for n, ln in enumerate(lines, base):
        for q in MEDIA.finditer(ln):
            for v in PX_VALUE.finditer(q.group(0)):
                if abs(float(v.group(1))) > 1:
                    fails.append(f"FAIL {rel}:{n} | media query uses {v.group(0)} | FIX: write {rem(v.group(1))} (px / 16)")
        ln = MEDIA.sub("", ln)
        if colour:
            for d in DECL.finditer(ln):
                if d.group(1).startswith("--") or ln[d.end():d.end() + 1] == "{" or (
                    not ln[d.end():].strip() and brace_next[n - base]
                ):
                    continue  # a custom property, or a selector such as a:not(#id)
                for shown in raw_colours(d.group(2)):
                    fails.append(f"FAIL {rel}:{n} | raw colour {shown} in '{d.group(1)}' | FIX: {FIX_COLOUR}")
        for m in PX_PROP.finditer(ln):
            for v in PX_VALUE.finditer(m.group(2)):
                if abs(float(v.group(1))) <= 1:
                    continue
                fails.append(f"FAIL {rel}:{n} | '{m.group(1)}' uses {v.group(0)} | FIX: write {rem(v.group(1))} (px / 16)")


def main() -> int:
    args, folder, tokens, i = sys.argv[1:], None, set(), 0
    while i < len(args):
        if args[i] == "--tokens" and i + 1 < len(args):
            tokens.add(Path(args[i + 1]).resolve())
            i += 2
        elif args[i].startswith("--") or folder is not None:
            folder = None
            break
        else:
            folder, i = args[i], i + 1
    if folder is None:
        print("FAIL usage | need one folder, and --tokens needs a file | FIX: check-web.py <folder> [--tokens <file>]")
        return 1
    root = Path(folder)
    if not root.is_dir():
        print(f"FAIL {root} | not a folder | FIX: pass the folder that holds index.html")
        return 1
    skip = {"node_modules", ".git", "dist", "build"}
    files = []
    for cur, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in skip]
        files += [Path(cur) / n for n in names if n.endswith((".html", ".css"))]
    files.sort()
    fails: list = []
    n_html = n_css = n_img = 0
    for f in files:
        rel = f.relative_to(root).as_posix()
        if f.stat().st_size > MAX_BYTES:
            n_html += f.suffix == ".html"
            fails.append(f"FAIL {rel}:1 | file is {f.stat().st_size} bytes, too large to scan | FIX: check it by hand or split it")
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        line_of = line_finder(text)
        if f.suffix == ".css":
            n_css += 1
            check_css(rel, text, 1, fails, f.resolve() not in tokens)
            continue
        n_html += 1
        colour = f.resolve() not in tokens
        for m in re.finditer(r"\sstyle\s*=\s*[\"']", text):
            fails.append(f"FAIL {rel}:{line_of(m.start())} | inline style attribute | FIX: move the value to a class; only a value set at run time may use element.style.setProperty")
        for off, css in style_blocks(text):
            check_css(rel, css, line_of(off), fails, colour)
        if colour:
            for m in TW_COLOUR.finditer(text):
                if not raw_colours(m.group(0)):
                    continue
                fails.append(f"FAIL {rel}:{line_of(m.start())} | raw colour in class '{m.group(0)}' | FIX: {FIX_COLOUR}")
        for pos, token, px in tw_px(text):
            if abs(float(px)) > 1:
                fails.append(f"FAIL {rel}:{line_of(pos)} | '{token}' uses px | FIX: use [{rem(px)}] or a Tailwind scale class")
        for m in TW_VARIANT.finditer(text):
            if abs(float(m.group(2))) > 1:
                fails.append(f"FAIL {rel}:{line_of(m.start())} | '{m.group(1)}:' variant uses px | FIX: use [{rem(m.group(2))}] or a Tailwind breakpoint such as md:")
        imgs = list(find_imgs(text))
        n_img += len(imgs)
        for i, (pos, tag) in enumerate(imgs):
            ln = line_of(pos)
            for attr in ("alt", "width", "height"):
                if not re.search(rf"\s{attr}\s*=", tag, re.I):
                    fails.append(f"FAIL {rel}:{ln} | <img> has no {attr} | FIX: add {attr}" + (" that describes the image" if attr == "alt" else " with the real size"))
            if i == 0 and re.search(r"loading\s*=\s*[\"']lazy", tag, re.I):
                fails.append(f"FAIL {rel}:{ln} | the first image is lazy | FIX: remove loading=\"lazy\" from the image above the fold")
        for m in re.finditer(r"href\s*=\s*[\"']#[\"']", text):
            fails.append(f"FAIL {rel}:{line_of(m.start())} | placeholder link href=\"#\" | FIX: point it to a real page or list it under Questions")
        h1 = len(re.findall(r"<h1\b", text, re.I))
        if h1 != 1:
            fails.append(f"FAIL {rel}:1 | {h1} <h1> found | FIX: keep exactly one <h1>")
        if not re.search(r"<title>\s*\S", text, re.I):
            fails.append(f"FAIL {rel}:1 | no <title> | FIX: add a <title> in <head>")
    if n_html == 0:
        fails.append(f"FAIL {root} | no .html file found, nothing was checked | FIX: pass the folder that holds index.html")
    print(f"FILES {n_html} html, {n_css} css, {n_img} img")
    for line in fails:
        print(line)
    print("OK" if not fails else f"FAILED {len(fails)}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
