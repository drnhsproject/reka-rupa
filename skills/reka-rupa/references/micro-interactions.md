# Micro-interactions

Small responses that confirm an action, show a state or relate two things. They
orient and confirm; they never decorate or loop for attention. The project's own
motion tokens and rules win; the values below are defaults for a project that has
none, and a new token is proposed (stop-and-ask), never inlined.

## 1. Motion tokens

| Token | Default | Use |
|---|---|---|
| `--motion-fast` | 100 ms | hover, press, toggle |
| `--motion-base` | 150-200 ms | state change, focus ring, expand |
| `--motion-slow` | 250-300 ms | enter of a menu, modal, toast |
| `--ease-out` | cubic-bezier(0.2, 0, 0, 1) | things that enter |
| `--ease-in` | cubic-bezier(0.4, 0, 1, 1) | things that leave |

- Exit is shorter than enter. No transition exceeds 300 ms (a progress bar and a toast's dwell time are not transitions).
- Animate `transform` and `opacity` only (`web-standards.md`); never `transition: all`.
- Press: scale 0.97-0.98. Hover lift: at most 2 px with a shadow step. Not both on one element.

## 2. State baseline

Every interactive element has all four, distinct from each other:
- **Hover** (pointer only): token swap or a small lift; never the only path.
- **Press**: immediate, `--motion-fast`, smaller than rest.
- **Focus-visible**: appears instantly, no delay, never removed (`accessibility.md`).
- **Disabled**: no hover, no press, not focusable by pointer, still readable.

## 3. Component patterns

- **Button**: press scale; while busy, keep its width, show a busy label, ignore further clicks.
- **Link**: underline or colour change on hover; the underline stays on focus.
- **Input**: border and label shift on focus; error and help text appear without moving the field below by more than its own height.
- **Checkbox, toggle**: thumb or tick moves in `--motion-fast`; the new state is visible without motion.
- **Card**: lifts only when the whole card is the target; a card with several links does not lift.
- **Menu, modal**: enter with fade plus 8 px shift in `--motion-slow`; leave faster; focus moves in on open and back to the trigger on close.
- **Toast**: enters from its edge, stays 5 s or more, pauses on hover and focus, is announced.
- **Tab, accordion**: indicator slides with `transform`, and a panel reveals with `opacity` (or `grid-template-rows`, never `height`) in `--motion-base`; content is never hidden from keyboard before it finishes.

## 4. Feedback patterns

- **Submit**: disable the control, show a busy label; a spinner only after about 300 ms; then success, or an error with a retry that keeps the user's input.
- **Validation**: inline, on blur, not on every keystroke; the message names the fix.
- **Copy**: the control's label changes to a confirmation for about 2 s, then returns.
- **Optimistic update**: show the result at once, roll back with a visible message on failure.
- **Loading**: a skeleton matches the real layout; stale data stays visible while fresh data loads.

## 5. Reduced motion

Under `prefers-reduced-motion: reduce`, remove movement (shift, scale, slide) and
keep the state change (colour, opacity, icon swap). Tailwind: `motion-safe:` or
`motion-reduce:`. Anything moving more than five seconds gets a pause control
(`accessibility.md`).

## 6. Checklist

- [ ] Durations and easings come from tokens, not literals.
- [ ] Hover, press, focus-visible and disabled are distinct on every control.
- [ ] Only `transform` and `opacity` move; no `transition: all`.
- [ ] Busy, success and error are visible without motion.
- [ ] Reduced motion removes movement and keeps the state.
- [ ] Touch and keyboard get the same feedback as hover.
