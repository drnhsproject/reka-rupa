# Code quality

The code must look like the project's own team wrote it: same structure, same
naming, same tools, and less of it than you first think you need.

## Fit the project

- Follow the project's layering (routes versus features versus shared
  modules), naming and file layout. Discover them first; do not import your
  own.
- Use the project's tokens for colours, spacing, radii, type. No raw hex
  values, magic spacing numbers or duplicated font sizes. If a token is
  missing, propose it; do not inline.
- Reuse existing components before writing new ones. A new shared primitive
  is justified only when two or more places need it; a one-off stays next to
  its feature.
- Use the project's data and state tools; do not add a parallel mechanism.
- Add a dependency only with the user's approval.

## Structure

- One component, one job. Split when a file mixes data loading, layout and
  business rules, or grows past what is comfortable to read in one sitting.
- DRY applied with judgement: extract when three real uses exist; do not
  extract after one. Two similar blocks are cheaper than the wrong abstraction.
- SOLID in practice: small components with a single reason to change; props
  for variation instead of copies; depend on the interface a component needs,
  not on a concrete parent; compose rather than deeply inherit or nest.
- Guard clauses and flat control flow over deep nesting.
- Presentation components receive data through props; side effects and data
  access live in hooks or service modules.
- Prefer clear names over comments. A boolean reads like a question
  (`isLoading`), an event handler like an action (`onSubmit`).
- No dead code, unused props, commented-out blocks, or speculative options.

## Complete, not just pretty

- Every state is handled: loading, empty, error, partial, offline where it
  matters.
- Every control does what it claims, or is removed or marked unavailable.
- Accessible names, roles and focus behaviour are in the code, not only in
  the design.
- Layout uses flexible units and holds at every target width.

## Comments

Comment the reason, never the obvious.

- Keep: business rules, non-obvious constraints, workarounds, edge cases,
  protocol or API quirks, security and performance trade-offs.
- Cut: restating the next line, step-by-step narration, banners made of
  repeated characters, empty labels ("main logic"), signature-echoing docs,
  decorative emoji, end-of-block markers.
- One line, sentence case, natural voice. Two lines only when the second
  carries a new fact. A TODO names a concrete task or does not exist.

## Tests and project check


- Add or update tests the way the project does (co-located, same query
  style), covering states and the main interaction.
- Run the project check; red means the work is not done. (In review mode, report gaps and run nothing unless asked.)
- Format with the project's formatter after editing.

## Checklist

- [ ] Matches the project's structure, naming and tools
- [ ] Tokens and shared components reused; nothing hard-coded
- [ ] No duplication, dead code or speculative abstraction
- [ ] All states and behaviours present; accessible and responsive
- [ ] Comments carry reasons only
- [ ] Tests updated; project check green with real output reported
