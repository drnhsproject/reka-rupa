# Preset: tailwind-static

Used only with `--stack=tailwind-static`. A fixed stack for a static page
built from a design, for projects that have no front-end conventions of their
own. Passing the flag is the user's approval for Tailwind CSS and GSAP, and
nothing else: it does not approve a new colour, font or token, and a value
the source shows that the project lacks is proposed first (`design-craft.md` §3,
Hard stops). When the project already has a stack, say so and ask whether
to follow the project (`code-quality.md`) or this preset; do not choose silently. Everything in
`web-standards.md`, `accessibility.md` and `fidelity-protocol.md` still applies.

## Stack (fixed within this preset)

- Semantic HTML5.
- Tailwind CSS: utility classes on one-off elements, `@apply` for repeated ones.
  `@apply` only works when Tailwind compiles the CSS, so name the delivery
  method before building: the Tailwind CLI producing a stylesheet that
  `index.html` links, or the Play CDN with the `@apply` rules inside a
  `<style type="text/tailwindcss">` block (then `custom.css` is not linked).
  Ask the user which, and pin an exact Tailwind version like GSAP.
- GSAP from a CDN, for scroll reveals and parallax only. Pin an exact version.

## Rules

1. **Styling.** No `style="..."` (`web-standards.md` Styles). A repeated element
   (button, card, form field) becomes one class built with `@apply` in a single
   `custom.css` (or the `text/tailwindcss` block, per Stack). A one-off
   structural element takes utility classes directly.
2. **Fidelity.** Replicate spacing, sizing, type and colour as measured from the
   source. Do not add or guess layout.
3. **Units.** `rem` (1 rem = 16 px). Prefer Tailwind's scale when it matches
   (`p-4`, `text-lg`); otherwise an arbitrary rem value (`p-[0.875rem]`).
4. **Responsive.** Mobile-first; add `sm:`, `md:`, `lg:`, `xl:`, `2xl:` as the
   design needs.
5. **Interaction.** Hover, active and focus transitions on every interactive
   element (`design-craft.md` §9). CSS transitions that move an element carry
   `motion-reduce:` overrides (or sit under `motion-safe:`); colour and state
   changes stay. GSAP reveals and parallax are added only where the design
   shows them, inside
   `gsap.matchMedia().add('(prefers-reduced-motion: no-preference)', ...)`
   so that reduced motion disables them. Without that condition the animation
   runs for everyone. Animate `transform` and `opacity` only.
6. **Assets.** Images, icons and SVGs live under `assets/` (for example
   `assets/images/`, `assets/icons/`) and are referenced by relative path from
   `index.html`. Every `<img>` has a descriptive `alt` and `width`/`height`.
   `loading="lazy"` goes on images below the first screen only, never on the hero
   (`web-standards.md` Loading).
7. **Content.** No empty text block, list or table unless the design shows it
   empty. Realistic mock data (`copy-and-mock.md`). Repeating components get a proposed
   `mock-data.json`, shaped like the expected API response, created only after the
   user agrees (`copy-and-mock.md`).

## Output

```
index.html       semantic HTML, Tailwind classes, GSAP init at the bottom,
                 links custom.css (Tailwind CLI) or inlines the
                 text/tailwindcss block (Play CDN), and assets/
custom.css       the @apply abstractions and any custom CSS; created with the
                 Tailwind CLI only, the Play CDN keeps them in the inline block
mock-data.json   dummy data for the repeating components (after approval)
assets/          images, icons, SVGs in subfolders
```

## Checklist

- [ ] No inline `style`; repeated elements abstracted once in `custom.css`
- [ ] rem throughout; mobile-first breakpoints
- [ ] Hover, active and focus states present; reduced motion honoured
- [ ] Assets under `assets/`; hero not lazy; below-fold images lazy
- [ ] `mock-data.json` proposed, approved, and matches what the page shows
