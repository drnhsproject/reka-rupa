# Changelog

## 0.2.0

Goal: a skill that is light on tokens and works the same on a strong and on an ordinary model,
without losing the design and code rules. Method: shorter `SKILL.md`, one order for clashing
rules, mechanical checks moved into scripts with plain failure lines, big requests split into parts.
The reference files were deliberately kept whole: their lines carry subtle rules.

Changed:
- `SKILL.md` went from 2,434 to 1,289 words (-47%). The 8 non-negotiables, 9 flags and the gates are kept.
- One **Precedence** block decides every clash: the user's words and flags, the stop-and-ask
  list, the project's rules, the design source, then this skill's defaults. Gates are never
  skipped at any level. The per-file "Conflicts" notes and the adoption rule now point to it.
- One checklist of 8 lines, with one tie-break: an item the source does not show is answered
  `no, because the source` and reported.
- Review mode moved to `references/review.md`, loaded only with `--mode=review`.
- The front-matter `description`, loaded in every session, went from 110 to 69 words; all nine
  trigger phrases are kept.
- The size gate (Step 2b): more than one screen, six components or one flow is split into parts,
  each with its own gate, tracked in `.agents/reka-rupa/parts.json`.
- Step 7 runs the scripts below and reruns until `OK`. A failure that the project or the source
  forces goes in the differences table.
- References: two stale "Hard stops" citations now say "Stop and ask"; three files point to
  Precedence. Three lines added, two replaced, none removed.

Added (all Python 3, standard library only; every failure line reads
`FAIL <file>:<line> | <what is wrong> | FIX: <what to do>`, last line `OK` or `FAILED n`):
- `scripts/check-web.py`: inline `style`, px in layout and media queries, `<img>` without
  alt, width or height, a lazy first image, `href="#"`, not exactly one `<h1>` or `<title>`,
  raw colours (`--tokens <file>` skips the token file), files over 2 MB.
- `scripts/check-reply.py`: the final reply carries the adapter lines, the differences table
  and, with `--stack tailwind-static`, the mock-data and mobile-menu items; English or
  Indonesian labels. It proves presence, not correctness.
- `scripts/parts.py`: `add`, `list`, `next`, `done`, so a new session continues a split request.
- `scripts/check-skill.py`: a growth guard for the skill's own files (`--strict`) and a load
  report (`--load`).
- `evals/fixtures/` with good and bad examples for each checker; 4 more trigger queries (28).

Measured (`check-skill.py --load`, words loaded per kind of run, now / before):
- design 4,903 / 6,048 (-19%); code 5,462 / 6,607 (-17%); adopt a design 7,680 / 8,825 (-13%);
  adopt with the preset 8,769 / 9,914 (-12%); review 6,339 / 7,017 (-10%).
- The folder as a whole is not smaller (references 8,482 words, `review.md` 467): the saving is
  per run, not in total.

Tested:
- Each script on its fixtures and on hostile input (the slowest case now ends in under 1 s).
- Trigger evals, haiku, one run per query, 28 queries: 18 pass with the new 69-word description
  (15 of the 24 old queries). The same run with the 0.1.2 description of 110 words, on the same
  day: also 18 of 28 (14 of 24). Four queries flipped, two each way, so the shorter description
  shows no measurable loss. The 18 of 24 recorded for 0.1.2 did not repeat today, even with its
  own description: one run per query is noisy and other installed skills compete for the same
  queries. The misses are cases where the model explored with `Glob` or `Grep` instead of
  calling the skill; the 11 queries that must not trigger all passed.
- Parts 1 to 3 each had an independent review, and QA rounds followed: 29 issues in the scripts
  and in `SKILL.md` were found and fixed before this release (false positives such as
  `hsl(var(--x))`, English-only reply labels, quadratic regexes, a lost rule in Step 7).

Known limits:
- Design runs with a small model (the menu and `mock-data.json` bar of 0.1.2, 3 of 3 runs on the
  largest design) were not repeated for 0.2.0; until they are, `check-reply.py` is the only guard for
  those two items. The trigger evals are one run per query, not statistics.
- `check-web.py` does not read SVG attributes or a comment that spans lines between a selector
  and its brace. `check-reply.py` accepts any table of 5 or more columns.
- The scripts need Python 3; without it the steps are done by hand and said so.

## 0.1.2

Changed:
- `tailwind-static`: when navigation no longer fits, the agent builds a disclosure
  menu (button with `aria-expanded` and `aria-controls`, the same links) and
  reports it as extrapolated, instead of only asking and leaving the links
  wrapped.
- A "Required in every reply" block at the top of the preset names the mobile
  menu and the `mock-data.json` proposal (three or more of the same component,
  with its name and count). `SKILL.md` Step 6 and Step 7 name the block, and the
  checklist lines are split so each states one fact.

Tested (details in the README):
- Two independent runs on page 1 of a design with 1440 and 390 px frames: both
  built the menu and both proposed `mock-data.json`. Two runs, one design.

Known limits:
- Two runs are not statistics. The design that failed in 0.1.1 was not re-run.
- Where the menu appears is the agent's choice (one run used 24rem, one 360 px).
- The disallowed Bash call reported in 0.1.1 was not looked at in these runs and is not addressed here.

## 0.1.1

Added:
- `--stack=tailwind-static`, an opt-in preset (`references/stack-tailwind-static.md`)
  for a static page built from a design: Tailwind with `@apply`, GSAP only where
  the design shows motion, `assets/`, a 2.75rem hit area on links and controls,
  and a note that the Play CDN is not a production delivery. Choosing the flag
  approves Tailwind and GSAP and nothing else.
- Four rules adopted from an external Figma-slicing skill: no static inline
  `style`, mobile-first styles, hover/active/focus feedback with reduced-motion
  overrides, and a `mock-data.json` proposal when a project has no mock layer.
- `references/design-systems.md` and the `--design-system=` flag: a design system
  the user gives outranks the project's tokens, and conflicts and gaps are
  reported. Design-tool servers are handled by capability, not by product.
- Two slice queries in `evals/triggers.json` and a `--skill` option for the
  trigger runner.

Changed:
- The skill description is English-only and mentions slicing and tidying a layout.
- `fidelity-protocol.md`: a live site is not adopted from its source text alone.
- Step 7 of `SKILL.md`: with `--stack` set, the preset's checklist is reopened
  before replying, and counts in the reply come from a folder listing.

Tested (details and numbers in the README):
- The preset on three FigCraft designs (a landing page, a sign-up form, and a
  1440 x 2691 px page with images and icons), rendered in headless Chrome:
  3.1% to 6.7% of pixels differ at 1440 px, inside text and small vertical drift.
- Trigger queries: 18 of 24 passed with a small model, one run each; five of the
  six misses also miss with the previous description. The two slice queries
  passed once each.
- Design mode with FigCraft and with a user-reported Figma MCP run.

Known limits:
- Not run against a real Figma file or a client project; one run per design.
- In two runs on the largest design the agent did not propose a mobile menu or
  a `mock-data.json`, and it used one Bash call it was not allowed. Read the
  agent's Questions list for those.
- Widths between 320 and 1440 px were not compared with a design.
- Figma Console, Claude Design and following a design system given with
  `--design-system=` were never run.

## 0.1.0

First public version. Design, code, both and review modes; project adapter;
pixel-fidelity protocol with `pixeldiff.py`; web standards; WCAG contrast
script with alpha blending. Tested on review mode (two projects) and one
screenshot-to-code build; design mode with a live design tool was untested at that release.
