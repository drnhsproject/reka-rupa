# Review mode

For `--mode=review`. Audit only; change nothing. Step 1 of `SKILL.md` applies; this file replaces Steps 2 to 7. Also load accessibility, responsive, code-quality, copy-and-mock, web-standards (web target), design-craft (focal point, decoration, layout), micro-interactions, fidelity-protocol (only with a source).

- Vague target ("the homepage"): choose it from the code; say what and why.
- Scope: target file; direct imports; deeper children holding its content or controls (row actions, pagers, modals, menus); shell and token files; API routes and data files only as far as the target's states depend on them. `--scope` overrides. Unopened files go under "Not opened".
- Every local file, route and image the target and its metadata point to must exist; a missing one or `href="#"` is a finding. External URLs and database paths go under "Not opened".
- Mark each checklist item pass, fail, N/A or UNVERIFIED. Fail needs located evidence.
- Partly verified (one theme computed): UNVERIFIED for the rest.
- Needs a running app, screenshot or computation you did not do: UNVERIFIED, never pass.
- Item that includes the project check, check not run: UNVERIFIED for that clause.
- Located failure plus an UNVERIFIED clause: Fail, naming the clause.
- Show a table: item, result, finding numbers. `--a11y=strict` adds a table, one row per `accessibility.md` section; `default` omits it.
- Colour: run `scripts/contrast.py` for every token pair (gradients, alpha, Sass: see `accessibility.md`).
- No screenshot possible: read class and style signals (fixed widths in a flex row without wrap, hover-only reveals, hard-coded counts, wide table without wrapper); Medium, "UNVERIFIED at runtime".
- Report disagreements between docs, manifest, tokens and language (two values for one token, `lang` against UI language); the manifest decides versions.
- Run the project check only when asked, else "check not run". Reply in the user's language. Merge findings with one cause.

Report order: adapter report, Not opened, findings by level, checklist table, Output (omit "awaiting approval" and "differences from the source").

| Level | Meaning |
|---|---|
| High | blocks or excludes users: broken or unnamed main-path control, text under 3 : 1, unreachable content, data loss |
| Medium | incomplete or silent state, behaviour or layout; normal text 3 to 4.5 : 1 (large text at 3 : 1 passes); non-text contrast under 3 : 1; dead secondary link; unverified risk or claim |
| Low | convention drift: raw values, structure, naming, polish |
| Info | what is right; what was not checked |

Token failure with no located element: Medium ("token risk"). Gradient stop at an unknown position: Medium, UNVERIFIED. Over 15 findings: High and Medium singly, Low grouped. Each finding: `file:line` (or screenshot), why, smallest fix. A fix that adds behaviour, copy (an accessible name counts) or tokens, or changes brand colour: "needs your go". No finding without evidence.
