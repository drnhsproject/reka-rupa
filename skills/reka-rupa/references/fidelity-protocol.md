# Fidelity protocol

When asked to adopt a design, the result is identical to the source, whether
the source arrives through a design-tool connection or as a screenshot. A
close match is not a match. Anything that cannot be matched is reported.

## 1. Capture the source

Prefer, in this order:

1. **Design-tool connection**: read the node tree and properties (size,
   position, auto-layout direction, gap, padding, fills, strokes, radii,
   shadows, fonts, weights, line heights, letter spacing, opacity, icon names
   and sizes, component and variant names, variables or styles in use).
2. **Exported image at known scale**: use it for visual comparison; measure
   by pixel, noting the scale factor.
3. **Screenshot from the user**: ask for scale or device size if unknown;
   state which values are measured and which are estimated.

With an image source, the image is the reference; confirm its scale and
viewport width first. With a tool source, take a reference screenshot at the
target size before writing code. Keep it for comparison. When you capture
screenshots yourself, make sure the viewport really is the width you think:
headless browsers enforce a minimum window width and silently lay the page out
wider; render inside an iframe of the exact width instead.

From pixels alone, line height, letter spacing and font weight cannot be read,
only inferred. Probe candidates (ink width at a known size, cap height,
baselines) and label each **estimated**. When several values match, give the
matching range, keep the simplest, and say the pick is not unique.

## 2. Build a measurement table

For each distinct element, record the facts, not impressions:

| Element | Size | Gap / padding | Radius | Colour | Font, size, weight, line height | Notes |
|---|---|---|---|---|---|---|

Include the states shown in the source and any variants. Record the order and
alignment of items.

## 3. Map to tokens, honestly

- Match each value to the nearest project token. If it matches exactly, use the
  token.
- If no token matches exactly, **do not round silently.** Report it:
  "source 14 px; nearest token 16 px". Then ask whether to (a) add a token,
  (b) use the nearest token and accept the difference, or (c) inline the
  exact value. Until the user decides, build with the nearest token (never
  edit the token file) and keep the measured source value visible in the
  differences table. This applies to categories the project tokenises
  (colour, font size, spacing, radius).
- **Dimensions no token category covers** (control and avatar sizes,
  container widths, line-height ratios), and a font size with no neighbour in
  the scale whose rounding would change an element's geometry, break the
  layout if rounded, because one wrong size shifts every neighbour. Declare the measured value once as a
  named custom property in the component's own file (`--avatar-size: 2.75rem` on the web),
  never in the token file and never as scattered numbers, and list it under
  Questions as a proposed token. State whether a container width is
  content-box or border-box. Do not disguise it with a `calc()` of
  unrelated tokens. If the project's rules say explicitly that such values
  must come from tokens, the project wins: use the nearest token and report.
- Media-query breakpoints cannot use `var()`; a raw breakpoint is allowed,
  flagged as estimated when the source shows fewer frames than needed.
- Reuse existing components when they already render the source exactly;
  otherwise extend or compose them without changing the behaviour for current
  users.
- Icons, images and fonts: use the exact asset. If it is missing or not
  licensed for the project, say so instead of substituting.

## 4. Build, then compare

1. Build the component or screen.
2. Screenshot the build at the same size as the reference, with the same data
   (use mock data that matches the source's text).
3. Compare side by side, region by region: spacing, alignment, sizes, colours,
   text wrapping, icon sizes, radii, shadows, states.
4. Fix differences, then compare again. Stop when no difference remains or
   the remaining ones are reported.
5. Measure; do not eyeball. `scripts/pixeldiff.py` reports differing pixels
   per region for two same-size screenshots; pass explicit regions for the
   elements you care about (run it with `python3 -I <skill folder>/scripts/pixeldiff.py`).
   Attribute each remaining difference to a region, and inspect that region
   (crop both images, compare ink widths and edge positions) before naming its
   cause. The tool counts pixels; it cannot tell a 1 px shift from a wrong
   colour. A cause you assumed is not a cause you found. If a small offset has no
   found cause, try the other centring methods (flex, grid, line-height) first;
   a measured compensation is allowed only with a code comment, and is listed
   in the differences table as "cause not found".

Target widths are the source frames, plus extras: one narrower than the
narrowest (320), one in between, one wider than the widest. If your capture
method cannot reach a width, say "unverified". Extras are extrapolation
awaiting approval. Fidelity outranks
content resilience: a truncation shown in the source stays; report that it
breaks at narrow widths.

## 5. Differences report (mandatory)

End every adoption with a table, even if short:

| Area | Source | Build | Why | Decision needed |
|---|---|---|---|---|

"None" is a valid answer only after a real side-by-side comparison. Never write
"matches" for something you did not compare.

## 6. Adoption overrides the checklist

The source decides what exists. Anything the checklist asks for that the
source does not show is a **proposal**, not a requirement: loading, empty and
error states, behaviour for a control whose action is unknown, tests when the
project has none. Keep the source element, do not invent behaviour, and list
each such checklist answer as "no, because the source" in the differences
table. Do not answer "yes" to make the checklist green.

## 7. Do not

- Redesign while adopting (improvements are proposals), or merge, drop or
  reorder source elements to make code easier.
- Replace the source's text with your own wording. If the source text is
  weak, propose a change; keep the source text in the build until approved.
- Treat platform defaults (font rendering, scroll bars, safe areas) as
  excuses; name them as the cause in the report.
