# Design craft

Avoiding generic output is the floor. The goal is a design that looks
intentional, calm and finished. Every decision should have a reason you can
say in one sentence; "it is the usual thing" is not a reason.

## 1. Direction first

Set three dials before drawing, from the brief or the existing product:

| Dial | Low | Mid | High |
|---|---|---|---|
| Energy | quiet, utilitarian | polished, confident | expressive, editorial |
| Rhythm | uniform sections | consistent with a few breaks | varied compositions |
| Motion | none beyond state feedback | transitions and reveals | choreographed |

Hold the same values from the first screen to the last. A product with no
stated direction gets low/low/low and is labelled a draft.

## 2. Hierarchy

- One focal point per screen; everything else defers to it.
- Differentiate by size, weight and colour deliberately, never randomly.
- Whitespace is structure: use it to group and to separate, not as leftover.
- Group related things closer than unrelated things (proximity before borders).
- Use a spacing scale and vary the steps; identical gaps everywhere flatten
  the page, random gaps look sloppy.

## 3. Colour

- Roles first: a neutral base, one or two supporting colours, one accent,
  plus semantic colours (success, warning, error, info).
- The accent appears at the key moment only. No accent is sterile; an
  accent everywhere stops being one.
- Take colours from the project's identity and tokens. Propose a new colour
  to the user; do not slip one in.
- Dark mode is a decision: ship it when the project supports it, and
  design both themes, not an inversion.
- Pick tints and shades from one family so surfaces feel related.

## 4. Typography

- Choose type for readability and character, with a reason. A popular
  default font is fine when it fits; it is not fine merely because it was
  the first one that came to mind.
- A small scale (about five to seven steps) with clear roles: display,
  title, body, caption, label.
- Comfortable line length and line height; avoid thin weights on small text.
- Avoid wide-tracked uppercase labels and monospace as decoration.

## 5. Shape, depth and decoration (doses)

| Element | Rule |
|---|---|
| Radius | a few values from the scale, applied by role (input, card, sheet); not one pill shape on everything |
| Shadow | marks elevation only; most surfaces sit flat |
| Glow | at most one or two focus accents, otherwise none |
| Glass / blur | an accent on one or two surfaces, never every surface |
| Gradient | only when it separates hierarchy, with the reason known; never the default blue-to-purple wash |
| Patterns and grids as background | only when they are part of the product's identity |
| Left colour stripe | only when it encodes a real state |
| Status dot | only when it marks a real state; no glow, no endless pulse |

## 6. Layout

- Build from the content and the job of the screen: name the one decision the
  user makes here, then arrange the screen around it.
- Do not paste a stock template (hero, feature trio, testimonials, pricing,
  footer; or sidebar, stat row, chart, table) unless this product truly has
  that content.
- Vary card size only to reflect real weight; do not make every item an
  identical card with an icon.
- Tables and lists: choose columns from the decision they support and put the
  deciding field early.
- Charts answer a question: put the question in the title, or write a
  sentence instead.

## 7. Icons and imagery

- Icons earn their place by relevance. If none fits, use the label alone.
- One consistent icon family, weight and size scale.
- No sparkle or robot glyphs as a stand-in for "smart"; no emoji as
  decoration in UI text.
- Illustrations and photos must relate to the content; otherwise omit them.

## 8. States

Design all of them, not just the happy path:

- Loading: says what is loading; a skeleton must match the real layout.
- Empty: says why it is empty and offers the one action that fills it.
- Error: says what failed and what to do next.
- Interactive: default, pressed, focused, disabled, selected.
- Long content, missing images and very small or very large numbers.

## 9. Motion

- Purpose first: orient, confirm, or relate. Never loop for attention.
- Short durations for feedback, slightly longer for transitions; respect the
  user's reduced-motion setting.
- Not everything moves; let the primary element lead.
- Every interactive element answers hover, press and focus with a short
  transition on `transform` and `opacity` (a colour change is a state swap
  through a token, not an animation). Hover is never the only
  path: touch and keyboard get the same feedback, and reduced motion removes
  the movement but keeps the state change.

## 10. Tidiness

- Everything aligns to a grid or a shared edge; optical alignment is
  checked, not assumed.
- Consistent padding inside similar containers; consistent icon sizes.
- Names for layers, frames and components in the design file are
  meaningful, and reusable parts are components, not copies.

## 11. Honesty

Controls do what they say, navigation leads somewhere real, and unbuilt
features are labelled or omitted. A screen that only looks interactive is a
defect, not a style.

## 12. Text spec template (when no design tool is available)

1. Job and focal point, in two lines.
2. Structure top to bottom: element, token or value, behaviour.
3. States: default, loading, empty, error, interactive, edge cases, each with
   its mock data.
4. Tokens used, light and dark, and any token that is missing.
5. Contrast results from the script, one line per pair, both themes.
6. Per-width layout: narrow, intermediate, wide, landscape.
7. Accessibility: label text, roles, targets, focus.
8. Open questions for the user.
