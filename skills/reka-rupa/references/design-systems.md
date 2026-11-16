# Design systems and design-tool servers

Goal: build with the design system the user means, and talk to whichever
design-tool server is connected, without assuming one product. Nothing here
is a licence to invent tokens or components the system does not have.

## 1. Which design system applies

Resolve in this order and say which one you chose in the adapter report.

1. **`--design-system=` or one the user named or pasted** in the request: a
   path (tokens file, a docs folder, a Storybook), a URL, pasted tokens or
   rules, or a library in a connected design tool. The user's explicit choice
   wins.
2. **The project's own** tokens, components and rules (`project-adapter.md`
   steps 1 to 4).
3. **None**: say so, and ask before inventing a palette or scale
   (`design-craft.md`).

When 1 and 2 both exist and disagree (for example the given system has
`--space-4: 16px` and the project has `spacing.4 = 12px`), do not merge them
silently. Report the conflict and ask which wins. Until answered, build to the
project (the code already ships) and mark the design-system value in the
differences table. If the user said "this project should adopt system X",
system X wins and the project's divergent tokens are listed as a migration
note, not changed without a go.

`--design-system=none` ignores option 1 and uses the project's own.

## 2. Reading the design system

Read only what the task needs, in this order of trust (most to least):

1. Machine-readable tokens (JSON, CSS variables, Tailwind/theme config,
   Style Dictionary output, Figma variables).
2. Component source or library (names, variants, props, states).
3. Written guidelines (usage, do and don't, voice, spacing and type rules).
4. Screenshots or published examples. These show, they do not define: record
   values as **estimated** (`fidelity-protocol.md` §1).

Record, in a short table, only what you will use: colour roles (and light and
dark), type scale, spacing, radii, elevation, motion, breakpoints, and the
components with their variants and states. Note rules that restrict use ("the
accent appears once per screen", "no gradients").

If the system is a URL or a long document, read the relevant sections, not the
whole of it, and list what you did not open.

## 3. Applying it

- Use the system's names, not look-alikes. A colour is `color.action.primary`,
  not a nearby hex.
- Prefer a system component over composing one. Use its variants and states
  as defined. If a needed variant does not exist, say so and ask: extend it,
  compose it locally, or add it to the system (never edit the system's files
  without a go).
- Honour the system's restrictions even where your own taste differs; mention
  the trade-off once (`project-adapter.md`, "Conflicts").
- In a design tool, create or bind nodes to the system's variables, styles and
  library components rather than raw values, when the tool supports it. Raw
  values are a last resort, reported.
- In code, map system tokens to the project's token layer (for example CSS
  variables or the theme file). Where the project has no token layer, ask
  where to put one (`project-adapter.md`, "When something is missing").
- **No match**: a needed value or component the system lacks is a gap, not
  permission to invent. List it under Questions with the nearest existing
  option and the consequence of each choice (use nearest, add to the system,
  inline locally).
- Run contrast on the system's actual pairs (`scripts/contrast.py`). A pair
  that fails in the system itself is reported, not silently fixed
  (`accessibility.md`, "When the project's own tokens fail").

## 4. Design-tool servers

The skill is tool-agnostic. A tool counts as connected when it is listed as
available, even if its schemas load on demand. Prefer the tool's own skills or
instructions for how to call it; this skill decides what to do, not the exact
calls.

Capabilities to look for, whatever the product is called:

| Need | Look for a tool that can |
|---|---|
| Read a design | return the node tree, properties and a screenshot of a frame |
| Read the design system | list variables, styles, libraries and components |
| Write a design | create or edit frames, components and variables |
| Code mapping | link design components to code components |

Rules that apply to any server:

- Check what the connected tool can do before promising a workflow. If it
  cannot read the design system, ask for tokens another way (a file, pasted
  values, a screenshot labelled estimated).
- Confirm the target file or frame before writing, and write only inside it
  (`SKILL.md`, non-negotiable 8 and Hard stops).
- After writing, read the result back (a screenshot or node read) and inspect
  it yourself before showing it.
- A failing or partial tool call is reported with what succeeded and what did
  not; do not claim a design that was not created.

### Status by tool (what has actually been verified)

| Tool | Status |
|---|---|
| Figma MCP (official), writing a design | One user-reported success; not measured |
| Figma MCP, a later run in a Starter-plan file | Read calls worked; the plan's call limit then blocked every tool, so writing was not possible |
| Figma MCP, reading a design or its variables into code | Not tested |
| FigCraft (local MCP, headless and attached modes) | One real run: created a new file, built a 1440 px landing page of about 200 layers (auto layout, images, imported SVG icons, shadows), read it back, screenshotted, saved and exported. Compared by eye against a screenshot of the source; not measured pixel by pixel. Attached mode (`figcraft-app`) not written to |
| Figma Console (community server), Claude Design, other servers | Not tested; handled only by the generic rules above |

Facts learned in the FigCraft run: missing fonts render with a fallback and drop their weight, and font download is switched on only by the user; very large command batches are better sent from a script than pasted into chat; vector icons can be taken from the source page's inline SVG and imported.

Update this table only after a real run, with the evidence.

## 5. Report

Add one line to the adapter report:

> Design system: `<name or source>` (`<given by user | project | none>`);
> tokens read from `<path or library>`; not opened: `<list>`.

Conflicts and gaps go on the caveats line or under Questions.
