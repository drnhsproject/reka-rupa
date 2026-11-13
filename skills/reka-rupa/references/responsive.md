# Responsive design

A small-screen layout is its own design, not the large one shrunk. Design
and verify across the whole width range, not at two sample points.

## Principles

- Mobile first: design the narrowest state deliberately, then add structure as
  room appears.
- Breakpoints sit where the content stops working (a column gets too narrow
  to read, a card row cramps), not at a device list.
- Expect at least three states: single column, an intermediate state
  (roughly 600 to 1024 px, tablets and small laptops), and the wide layout.
  The middle band must be designed, not inherited by accident.
- Native apps: treat window size classes (phone, large phone, tablet, split
  screen, landscape) the same way.

## Test widths

Check every design and every build at roughly: 320, 360, 390, 430, 600, 768,
1024, 1280 and 1440 px (or points), plus landscape on a phone. Drag through the
range once; look for the width where something breaks.

## Scale

- Give small screens their own size step: smaller type scale, tighter
  section padding, smaller gaps. Desktop-sized padding on a phone creates
  empty deserts.
- Use fluid sizing for type where the platform allows it, or a smaller step
  at the breakpoint.
- Do not use full-viewport heights for sections by default; let content set
  height. Where a full-height section is intended, use the dynamic viewport
  unit on the web and safe-area aware sizing natively.

## Grids and stacking

- Columns collapse and stack; none may be left as slivers.
- Use flexible tracks (min/max, auto-fit) instead of fixed pixel columns.
- Columns follow the content: a phone usually wants one, sometimes two.
- Children are allowed to shrink: no fixed widths that outgrow the parent;
  long words and URLs wrap or truncate with intent.

## Overflow

- Zero horizontal scroll at every tested width.
- Wide tables get a reflow layout or a clearly scrollable container.
- Do not hide problems with `overflow: hidden`; clip only when cropping is the
  design (a thumbnail), never to hide text or controls.

## Touch and navigation

- Targets at least 44 x 44 (CSS px on the web, which is 2.75rem; dp or pt natively) with spacing between neighbours.
- Hover-only interactions need a tap equivalent.
- Collapse a top bar into a bottom bar for a few primary destinations, or a
  labelled menu for the rest. A bare, unlabelled menu icon hides the only
  way around the app.
- Fixed bars (bottom navigation, sticky headers) stay compact and reserve their
  height in the content so the last item is reachable. Respect safe areas
  (notch, home indicator, system bars).
- Keyboard-aware screens: the focused field stays visible above the keyboard.

## Content resilience

- Long names, long translations, very large numbers, missing images, and
  one-item or hundred-item lists all keep the layout intact.
- Text honours the user's font-size setting without clipping.

## Reviewing without a running app

Read the code for the signals that predict a break, and mark the result
UNVERIFIED at runtime: fixed widths (`w-250px`, `min-w-[350px]`) inside a
flex row without wrap or inside `overflow: hidden`; hard-coded `colSpan` or
column counts; absolute offsets that centre by luck of text width; `100vh`
sections; hover-only reveals; wide tables without a scroll wrapper.

## Checklist

- [ ] A distinct small-screen state exists, with its own scale
- [ ] The intermediate width band is designed, not accidental
- [ ] Grids stack; nothing collides, clips or scrolls sideways
- [ ] Targets 44 x 44 or more, spaced; hover-only actions have a tap path
- [ ] Navigation reflowed; fixed bars never cover content; safe areas honoured
- [ ] Verified by screenshot at each test width, not assumed
