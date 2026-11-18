# reka-rupa

An Agent Skill that acts as a senior UI/UX designer and then writes the code.
It reads the project's own rules first, asks before it decides, matches a given
design exactly, and reviews UI without changing anything.

## What the name means

*Reka rupa* is Indonesian for "design". It is two words:

- ***reka***: to devise, plan or create. Indonesian dictionaries (KBBI) give
  *rekaan* as composition, something made, a design or a scheme, and *reka
  bentuk* as a design drawing.
- ***rupa***: form, shape, appearance. It comes from Sanskrit *rūpa* (form),
  which Indonesian and Sundanese both borrowed. It is also the root of *seni
  rupa* (visual arts).

Together: to devise a form, which is what a designer does. The name fits a
skill that designs an interface and then builds it.

## What a skill is

An Agent Skill is a folder of instructions (`SKILL.md`), reference notes and
optional scripts that an AI coding agent loads when a task matches. It does not
add a tool or a model. It gives the agent a repeatable method, so the same kind
of task is done the same way each time. This skill's task is UI/UX design and
front-end implementation.

## What it does

| Mode | Use it to |
|---|---|
| `--mode=both` (default) | Design a screen, component or flow, then build it |
| `--mode=design` | Produce the design only (in a connected design tool, or as a text spec) |
| `--mode=code` | Build from an existing design source |
| `--mode=review` | Audit a UI read-only and report ranked findings |

```
/reka-rupa review the homepage --mode=review --a11y=strict
/reka-rupa build the team page --mode=code --source=screenshot --fidelity=pixel
```

Flags: `--mode`, `--target=screen|component|flow`, `--source=tool|screenshot|none`,
`--fidelity=sketch|spec|pixel`, `--design-system=<path|url|name|none>`,
`--stack=project|tailwind-static`,
`--a11y=strict|default`, `--scope=<path>`, `--no-save`.

## Design tools and design systems

- **Any design-tool server.** The skill checks which server is connected and
  works from what it can do (read a design, read the design system, write a
  design), not from a product name. Figma is the only one tried so far; see
  the status below.
- **A design system you give it.** Pass `--design-system=` (a tokens file, a
  docs folder, a URL, a library in the connected tool) or name it in the
  request. It outranks the project's own tokens; conflicts are reported and
  asked, never merged silently. Values the system lacks are listed as gaps,
  not invented. Details in `references/design-systems.md`.

## How it differs from a style-guidance skill

Most UI skills push a visual taste. This one is a working method:

- **Follows the project, not its own habits.** Step 1 discovers tokens,
  components, language, tone and the project check. Project rules outrank the
  skill's taste.
- **Asks before deciding.** New colours, dependencies, copy and behaviour are
  proposals with approval checkpoints, not silent choices.
- **Identical to the source.** A design adopted from a screenshot or a design
  tool is measured, mapped to tokens, compared pixel by pixel, and every
  difference is reported.
- **Honest review.** Anything that needs a running app is `UNVERIFIED`, never
  `pass`. Contrast is computed, not judged by eye.
- **Web defaults.** rem units, images with alt, dimensions and lazy loading,
  and on-page SEO. Defaults only: project rules win.

## Install

Place the `skills/reka-rupa` folder where your agent loads skills.

Claude Code, one project:
```bash
cp -R skills/reka-rupa /path/to/project/.claude/skills/
```
Claude Code, every project:
```bash
cp -R skills/reka-rupa ~/.claude/skills/
```
Other agents that support the Agent Skills format use their own skills folder;
copy the same directory.

With the community `skills` CLI
([vercel-labs/skills](https://github.com/vercel-labs/skills)):

```bash
# see what the repository offers, without installing
npx skills add drnhsproject/reka-rupa --list

# install into the current project
npx skills add drnhsproject/reka-rupa --skill reka-rupa

# install for one agent, or for every project of yours
npx skills add drnhsproject/reka-rupa --skill reka-rupa -a claude-code
npx skills add drnhsproject/reka-rupa --skill reka-rupa -g
```

In a normal terminal the CLI detects the agents installed on your machine and
lets you choose where to install; `-a <agent>` skips that choice (`-a '*'` for
all). Checked on this repository: `--list` finds the skill, and
`--skill reka-rupa -a claude-code` copies all files (11 at the time of that check, before design-systems.md and stack-tailwind-static.md were added) to
`.claude/skills/reka-rupa/`, identical to this repository. Not checked: the
interactive agent prompt, and agents other than Claude Code.

The CLI collects anonymous usage data; set `DISABLE_TELEMETRY=1` to opt out.
It is a third-party tool. Skills run with your agent's permissions, so read
`SKILL.md` before installing any skill, this one included.

### Updating

Updates are manual; installed copies do not change on their own.

```bash
npx skills check          # is a newer version available?
npx skills update         # update installed skills (-g global, -p project)
```

The CLI records what it installed in `skills-lock.json` (commit it with your
project if you want teammates to get the same version). Changes are listed in
`CHANGELOG.md`, and releases are tagged (`v0.1.0`, ...).

## Requirements

None for the skill itself. Optional helpers in `skills/reka-rupa/scripts/`:

- `contrast.py`: Python 3 only (WCAG contrast, with alpha blending).
- `pixeldiff.py`: Python 3, Pillow and numpy (per-region screenshot diff).
- A design-tool server (for example Figma) is optional and only needed for
  design mode with a live source.

## Layout

```
skills/reka-rupa/
  SKILL.md            flow, gates, modes, quality checklist
  references/         loaded on demand: project-adapter, design-systems, design-craft,
                      accessibility, responsive, copy-and-mock, code-quality,
                      web-standards, fidelity-protocol, stack-tailwind-static
  scripts/            contrast.py, pixeldiff.py
```

## What has and has not been tested

Be aware of the limits before relying on it.

Tested, with a fresh agent following only the skill:
- Review mode on two real projects (a Vite admin app and a Next.js portfolio),
  read-only, repeated after fixes.
- Building one small screen from a screenshot at two widths, measured against
  the original: 0.000% of pixels differing after the third revision of the
  protocol (5.0% and 0.55% in earlier revisions, which drove the fixes).
- Converting that build's px values to rem left it at 0.000%.
- Design mode against a live design tool: a user ran it with the Figma MCP
  server and it produced a design in their own Figma workspace. This is a
  user-reported success; it was not measured (no fidelity numbers), and the
  reading direction (Figma to code) was not part of that test.

- Design mode with FigCraft (local MCP server): one page built end to end
  (new file, about 200 layers, images and imported SVG icons, saved and
  exported). User-visible result, compared by eye; not measured.

- Preset `--stack=tailwind-static`, one run from a generated screenshot of a
  small page (no browser, so nothing was rendered or measured). It produced
  `index.html` with no inline `style`, rem units, focus states and a question
  about Tailwind delivery, but it did not abstract the repeated cards and focus
  classes with `@apply` and did not propose `mock-data.json`. Treat the preset
  as only partly followed. After the rules for repeated elements and the
  `mock-data.json` proposal were made stricter, a second run (same screenshot)
  again left the repeated focus-ring classes inline and again did not propose
  `mock-data.json`; it did produce a `text/tailwindcss` block with theme colours.
  The stricter wording is not shown to change that behaviour.
  A third run, from a small design built in FigCraft and read through its MCP
  tools (`--source=tool`), followed the preset: repeated elements abstracted
  with `@apply` in a `text/tailwindcss` block, no inline `style`, reduced-motion
  overrides, and a `mock-data.json` proposal in the questions. Nothing was
  rendered by the agent (it had no browser). Rendered afterwards in headless
  Chrome at 1280 px and compared with the design's PNG export: 3.1% of pixels
  differ (max channel difference over 32), nearly all inside text, plus a build
  that sits about 2 px lower from the heading down. Block positions, widths,
  colours and card geometry match the design's measurements; the text and
  line-height differences come from Inter being drawn by two different font
  engines (the page loads Inter from Google Fonts). Only 1280 px was compared.
- Trigger queries: 24 queries run once each with a small model (haiku): 18
  pass. Five of the six failures also fail with the previous description and
  one (a component-card request) passed before and failed now, which a single
  run cannot tell apart from noise. The two slice queries: one passes, one
  (Indonesian) went to a different, installed Figma skill.

Not tested:
- Figma Console (community server), Claude Design and any other design-tool
  server: handled only by the generic rules in `design-systems.md`.
- FigCraft beyond one run: a landing page was built from a website and compared
  with a screenshot of it by eye only; no pixel measurement, and the fonts of
  the source were not installed.
- Following a design system given with `--design-system=` (added after the
  tests above, never run).
- Fidelity against a live Figma source (reading a Figma design and building
  code from it, compared pixel by pixel).
- Fidelity for icons, photos, shadows, web fonts and interactive states.
- Native mobile projects.
- Larger screens than a single list page.

The test sources and measurements were produced in a controlled setup (same
machine, system fonts); real-world screenshots will differ.

## License

MIT. See `LICENSE`.
