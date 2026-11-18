# Changelog

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
