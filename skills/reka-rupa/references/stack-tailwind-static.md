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
  Ask the user which, and pin an exact Tailwind version like GSAP. When the
  answer cannot be waited for (no way to ask), state the assumption, build with
  the Play CDN, and still apply Rule 1: the abstraction does not depend on the
  answer.
- GSAP from a CDN, for scroll reveals and parallax only. Pin an exact version.

## Required in every reply

A reply without these two items is incomplete, even when the page is built.

- **Mobile menu:** when the navigation links stop fitting at any width from
  320 px up, the page has a disclosure menu for them (Rule 4) and the Questions
  list says it was added and was not in the design. When the links fit at every
  width, or the design has no link row, say that in the reply instead.
- **`mock-data.json` proposal:** whenever the page has three or more of the
  same card, row, logo or feature, the Questions list proposes a
  `mock-data.json` shaped like the expected API response, naming the component
  and how many times it repeats. Leaving it out because the page can be built
  without it is not allowed.

## Rules

1. **Styling.** No `style="..."` (`web-standards.md` Styles). A repeated element
   (button, card, form field) becomes one class built with `@apply` in a single
   `custom.css` (or the `text/tailwindcss` block, per Stack). A class
   or control that appears three or more times (the same card, or the same
   focus-ring utilities on every link) is repeated: write it once as a named
   class, never as copied utility strings. A one-off structural element takes
   utility classes directly.
2. **Fidelity.** Replicate spacing, sizing, type and colour as measured from the
   source. Do not add or guess layout (the one exception is the Rule 4 menu,
   reported as extrapolated).
3. **Units.** `rem` (1 rem = 16 px). Prefer Tailwind's scale when it matches
   (`p-4`, `text-lg`); otherwise an arbitrary rem value (`p-[0.875rem]`).
4. **Responsive.** Mobile-first; add `sm:`, `md:`, `lg:`, `xl:`, `2xl:` as the
   design needs.
   Navigation that the design shows as a row of links must stay reachable at
   every width. Below the width where the links stop fitting, build a
   disclosure menu (a button with `aria-expanded` and `aria-controls`, the same
   links, existing tokens only, a 2.75rem hit area) and show the row from that
   width up. Never hide the links without it. The design does not show this
   menu, so report it in the Questions list as extrapolated and let the user
   reject it. Cropped images keep their subject in frame (`object-position`), and
   the difference is reported.
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
   empty. Realistic mock data (`copy-and-mock.md`). The `mock-data.json`
   proposal is a required reply item (see "Required in every reply"); the file is created only
   after the user agrees (`copy-and-mock.md`).
8. **Touch targets.** Every link and control has a hit area of at least
   2.75rem x 2.75rem (`accessibility.md`), without changing the measured look:
   keep the drawn size and extend the hit area with padding the design does not
   show or a pseudo-element (`relative after:absolute after:-inset-3`), and
   report the extension in the differences table. A text link the design draws
   at 1.3rem tall is the common case.
9. **Production.** The Play CDN is for a page being built or reviewed, not for
   production. In the reply, say that a compiled stylesheet (Tailwind CLI) is
   the production delivery and offer to produce it; do not add that dependency
   until the user agrees.

## Reporting counts

Any number in the reply (files exported, images, links left as `href="#"`,
repeated items) comes from listing the folder or the file after writing, not
from memory: list `assets/` (a read-only listing is allowed even where Bash is
not, by the Glob tool) and state the counts that listing gives.

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
- [ ] Navigation reachable at every width: a disclosure menu is in the markup and reported as extrapolated, or the reply says the links always fit
- [ ] Counts taken from a listing
- [ ] Links and controls have a 2.75rem hit area; the extension is reported
- [ ] Assets under `assets/`; hero not lazy; below-fold images lazy
- [ ] `mock-data.json` proposal is in the Questions list (component and count named); once approved, the file matches what the page shows
