# Project adapter

Goal: learn how this project wants UI built, in as few reads as possible.
Never assume; never invent a convention the project does not have.

## Read order (stop when the picture is complete)

1. **Entry docs**: `CLAUDE.md`, `AGENTS.md`, `README.md`, and any
   `.agents/`, `.claude/skills/`, `docs/` or `rules/` folder they point to (a
   project-local skill about design counts as a UI rule). Look for UI,
   design-token, component and testing rules.
2. **Manifest**: `package.json` (framework, UI libraries, scripts such as
   `lint`, `typecheck`, `test`, `check`) and the framework config file.
3. **Tokens**: the theme file (names like `theme`, `tokens`, `colors`,
   `design-system`, a Tailwind config, CSS variables). Record colour roles,
   spacing scale, radii, type scale, light/dark handling.
4. **Shared components**: the folder holding buttons, inputs, cards, badges,
   state components (empty, error, skeleton). List what exists before
   proposing anything new.
5. **Structure**: where routes/pages live versus feature folders versus
   shared libraries. Note the layering rule, if any (for example "routes
   only in the routes folder").
6. **Mock layer**: any `mock`, `fixtures`, `seed` or `__mocks__` folder, and
   how screens consume it.
7. **Language and tone**: sample existing UI strings (labels, buttons,
   empty states, errors). Note language, formality, and terminology.
8. **Design tools**: check which design tool servers are connected
   (a tool listed as available counts as connected, even if its schema loads on demand). Prefer a connected tool for design
   work; fall back to screenshots or a text spec. Any server counts, not only
   Figma (`design-systems.md` §4).
9. **Design system**: one the user named or passed with `--design-system=`
   outranks the project's own tokens; read `design-systems.md` and report
   conflicts instead of merging.
10. **Tests and project check**: the command that must be green before work
   counts as done, and how existing UI tests query elements. If there are
   several (lint, build), name them all; if none, say "none defined".
11. **Theme vendors and modes**: a vendor template (Bootstrap or admin
    skins) usually keeps tokens in Sass variables plus a project override file;
    follow the import chain. Note app modes switched by env vars.

## Find fast

```bash
ls                                   # top-level shape
grep -rIl -i 'theme\|tokens' . --exclude-dir=node_modules \
  --include='*.ts' --include='*.tsx' --include='*.js' --include='*.jsx' \
  --include='*.css' --include='*.scss' --include='*.json' | head
find . -type d -iname 'components' -not -path '*/node_modules/*' | head
```

Single-quote any user-supplied keyword in shell commands.

## Report (two lines, at the top of the reply)

> Project: `<framework>`, tokens in `<path>`, shared components in `<path>`,
> mock layer `<path or none>`, UI language `<language, tone>`.
> Check: `<command(s) or none defined>`; design tool: `<connected tool or none>`;
> design system: `<source, or none>`.

Caveats (missing docs, conflicts, unopened files) go on a separate line
after these two.

## When something is missing

| Missing | Do this |
|---|---|
| No token file | Ask whether to create one; do not scatter raw values |
| No shared components | Ask where new ones should live |
| No mock layer | Ask before creating one; keep sample data local and clearly labelled |
| No stated language | Ask, or follow the language of existing strings |
| No project check | Ask which check proves the work (in review, say "none defined"), and say what you ran instead |
| No design tool connected | Use screenshots or write a text spec; say so |

## Conflicts

Project rules outrank this skill's taste. If a project rule produces a
weaker design, follow the rule and mention the trade-off once; do not
quietly work around it.
