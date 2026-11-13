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
`--skill reka-rupa -a claude-code` copies all 11 files to
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
