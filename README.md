# reka-rupa

An Agent Skill that acts as a senior UI/UX designer and then writes the code.
It reads the project's own rules first, asks before it decides, matches a given
design exactly, and reviews UI without changing anything.

*Reka rupa* is Indonesian for "design" (literally, to devise a form).

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
`--fidelity=sketch|spec|pixel`, `--a11y=strict|default`, `--scope=<path>`,
`--no-save`.

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

Once this repository is published, the community `skills` CLI
([vercel-labs/skills](https://github.com/vercel-labs/skills)) can install it:

```bash
npx skills add <owner>/<repo> --skill reka-rupa
```

By its README the CLI detects the agents installed on your machine and lets
you choose which ones to install to (Claude Code, and others it supports);
`-a <agent>` picks one directly and `-g` installs for every project. It
collects anonymous usage data unless `DISABLE_TELEMETRY=1` is set. This is a
third-party tool, and its behaviour has not been verified against this
repository.

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
  references/         loaded on demand: project-adapter, design-craft,
                      accessibility, responsive, copy-and-mock, code-quality,
                      web-standards, fidelity-protocol
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

Not tested:
- Design mode against a live design tool such as Figma.
- Fidelity for icons, photos, shadows, web fonts and interactive states.
- Native mobile projects.
- Larger screens than a single list page.

The test sources and measurements were produced in a controlled setup (same
machine, system fonts); real-world screenshots will differ.

## License

MIT. See `LICENSE`.
