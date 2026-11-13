#!/usr/bin/env python3
"""WCAG 2.x contrast ratio for two sRGB hex colours.

Usage: contrast.py "<foreground>" "<background>"
Colours accept #RGB, #RRGGBB or #RRGGBBAA, with or without the leading #.
Quote each colour as its own argument: an unquoted # starts a comment in zsh.
A foreground with alpha (#RRGGBBAA) is blended over the background first and
the blended colour is printed. Prints the ratio and the verdict for normal and
large text (normal 4.5, large text and controls 3.0).
"""
import sys


def parse(value: str) -> tuple[int, int, int, float]:
    text = value.strip().lstrip("#")
    if len(text) == 3:
        text = "".join(ch * 2 for ch in text)
    if len(text) not in (6, 8) or any(ch not in "0123456789abcdefABCDEF" for ch in text):
        raise ValueError(f"not a hex colour: {value!r}")
    alpha = int(text[6:8], 16) / 255 if len(text) == 8 else 1.0
    return int(text[0:2], 16), int(text[2:4], 16), int(text[4:6], 16), alpha


def blend(fg: tuple[int, int, int, float], bg: tuple[int, int, int]) -> tuple[int, int, int]:
    a = fg[3]
    return tuple(round(a * f + (1 - a) * b) for f, b in zip(fg[:3], bg))


def linearise(channel: int) -> float:
    c = channel / 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb: tuple[int, int, int]) -> float:
    r, g, b = (linearise(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(f"expected 2 colour arguments, got {len(argv) - 1}; quote each colour separately.")
        print(__doc__)
        return 2
    try:
        fg, bg = parse(argv[1]), parse(argv[2])
        if bg[3] < 1.0:
            raise ValueError("the background must be opaque; blend layers by hand first")
        bg_rgb = bg[:3]
        fg_rgb = blend(fg, bg_rgb) if fg[3] < 1.0 else fg[:3]
        value = ratio(fg_rgb, bg_rgb)
    except ValueError as error:
        print(error)
        return 2
    if fg[3] < 1.0:
        print("blended foreground #%02X%02X%02X" % fg_rgb)
    verdict = lambda limit: "PASS" if value >= limit else "FAIL"
    print(
        f"ratio {value:.2f}:1 | normal text {verdict(4.5)} (4.5) "
        f"| large text and controls {verdict(3.0)} (3.0)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
