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

- Preset `--stack=tailwind-static`, read from two small designs built in
  FigCraft and read through its MCP tools (`--source=tool`): a landing page
  (header, hero, three repeated cards) and a sign-up page (form with labels,
  inputs, repeated feature rows). Both builds abstracted repeated elements with
  `@apply` in a `text/tailwindcss` block, had no inline `style`, used rem,
  carried reduced-motion overrides, proposed `mock-data.json` instead of
  creating it, and noted that the Play CDN is not a production delivery. The
  second design also got labelled inputs with `autocomplete`, and the nav link
  got a 44 px hit area by padding (reported as a difference). Rendered afterwards
  in headless Chrome at 1280 px and compared with each design's PNG export:
  3.1% to 4.5% of pixels differ for the landing page and 6.7% for the sign-up
  page, inside text. Block positions, widths, colours and geometry match the
  design's measurements; the text differences come from Inter being drawn by two
  font engines (so a heading can wrap on a different word). At 768 px and at
  320 px the landing page was inspected by eye: no horizontal overflow. Earlier
  runs from a plain screenshot, before the rules were tightened, followed the
  preset only partly (repeated classes left inline, no `mock-data.json`
  proposal), so give the agent a structured source or a clear screenshot and
  read its Questions list.
- Preset on a larger design: a 1440 x 2691 px landing page built in FigCraft
  (hero, tabs, 13 icon cards, 12 client logos, illustrations, footer), one run.
  The agent exported its own assets (44 files, all referenced, none missing),
  gave every image an `alt` and dimensions, used no inline `style` and no px
  values, and reported the design's low button contrast (about 1.6:1 and 2.5:1)
  instead of fixing it silently. Rendered in headless Chrome and compared with
  the design's PNG: 6.1% of pixels differ at 1440 px, mostly text and a drift of
  about 10 px downward from the hero onward; the layout is otherwise the same.
  Gaps found: below desktop width the main navigation disappears with no menu
  replacement, the hero illustration is cropped at 320 px, 29 links are left as
  `href="#"` (reported), no `mock-data.json` proposal was made for the repeated
  cards, and the agent's file count (50) did not match the folder (44). Widths
  between 320 and 1440 were not compared with a design.
  Rules for a mobile menu, a `mock-data.json` proposal and counts taken from a
  folder listing were then added to the preset and to Step 7 of `SKILL.md`. Two
  more runs of the same design: the file counts became consistent with the
  folder (one run still gave three different counts before the Step 7 line was
  added), but neither run proposed a mobile menu or `mock-data.json`, so treat
  those two as unreliable and check the Questions list for them. Every run also
  used one Bash call that had been disallowed. One run per variant; no
  statistics.
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
- Pages much larger than the one above, real client sites, and pages with forms that submit or scripts beyond a reveal.

The test sources and measurements were produced in a controlled setup (same
machine, system fonts); real-world screenshots will differ.

## License

MIT. See `LICENSE`.
