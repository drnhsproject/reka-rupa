# Changelog

## Unreleased

Adopted the universal rules of an external Figma-slicing skill: no static inline `style`, mobile-first styles, hover/active/focus feedback, and a `mock-data.json` proposal when a project has no mock layer. Added the opt-in `--stack=tailwind-static` preset (Tailwind `@apply`, GSAP, `assets/`) in `references/stack-tailwind-static.md`. Run against two designs built in FigCraft (see the README test notes); not run against a Figma file or a real project. The description now mentions slicing, and `evals/triggers.json` has two slice queries that passed once each (2/2, one run); the other 22 queries were not re-run.

Added `references/design-systems.md` and the `--design-system=` flag: a design
system the user gives outranks the project's tokens, conflicts and gaps are
reported, and design-tool servers are handled by capability rather than by
product. Not run against any real design system or any server other than
Figma; Figma Console and Claude Design remain untested.

First real run with FigCraft (a local MCP design tool): built a landing page
from a website, then rebuilt it from a reference screenshot after the first
version, made from the page's HTML and CSS alone, did not look like the site.
`fidelity-protocol.md` now says not to adopt a live site from source text alone.
Compared by eye, not measured.

SKILL.md description: trigger phrases are English only. Not re-measured.

Docs only: design mode with a live design tool (Figma MCP) is now reported as
working by a user, who created a design in their own Figma workspace. Not
measured; Figma-to-code fidelity remains untested.

## 0.1.0

First public version. Design, code, both and review modes; project adapter;
pixel-fidelity protocol with `pixeldiff.py`; web standards; WCAG contrast
script with alpha blending. Tested on review mode (two projects) and one
screenshot-to-code build; design mode with a live design tool was untested at that release.
