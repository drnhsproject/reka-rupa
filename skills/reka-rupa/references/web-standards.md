# Web standards

Defaults for any web target (HTML, CSS, a web framework). They are defaults:
the project's own rules outrank them (see Conflicts). Native apps do not use
this file.

## Units: rem, not px

- Margin, padding, gap, font size, radius, container widths and line-height
  offsets are written in `rem`, so they follow the user's font-size setting.
  Keep the root at `100%` (16 px). Do not shrink it (`62.5%`) to make maths
  easier; that breaks the user's setting.
- Allowed in `px`: hairlines (1 px borders, outlines), shadows, and
  `outline-offset`. Media queries use `em` or `rem`, so breakpoints follow
  the font size as well.
- A px value from a design converts at 16 px per rem (`44px` becomes `2.75rem`),
  so this rule does not conflict with pixel fidelity. Token files hold rem.
- Framework scales that compile to rem (Tailwind spacing and `text-*`, `md:`
  in Tailwind v4) pass. Check arbitrary values (`min-w-[350px]`, `text-[10px]`,
  `min-[640px]:`) and custom CSS; a `min-width` on a card counts as a width.
- A project that already works in px keeps its tokens as they are; propose the
  move, do not do it silently.

## Styles

- No `style="..."` attribute. Styling lives in classes and tokens. The only
  exception is a value that is truly dynamic at run time (a computed width, a
  progress percentage), set with `element.style.setProperty` or the framework's
  own style binding, never as a literal attribute holding fixed values.
- Write base styles for the smallest width first, then widen with `min-width`
  queries (or the framework's breakpoint prefixes). A project that is already
  desktop-first keeps its approach; propose the move, do not do it silently.

## Images

- Reserve the space: give every image `width` and `height` attributes that
  match its aspect ratio (intrinsic or the rendered size), or an `aspect-ratio`,
  so nothing jumps when it loads. With a framework component, width and height
  may be the rendered size; flag the ratio only when the crop is unintended.
- Size by container, not by fixed pixels: `max-width: 100%; height: auto`, or a
  wrapper with `aspect-ratio` and the image at `width: 100%; height: 100%;
  object-fit: cover` (`contain` when nothing may be cropped).
- Responsive sources: `srcset` and `sizes`, with WebP or AVIF and a fallback
  when the project's audience needs one. Never ship a 3000 px photo for a
  400 px slot.
- **Alt text is required.** An informative image gets text that says what it
  shows or does ("Sari Rahmawati, project lead"). A decorative image gets
  `alt=""`. Never "image", "logo" or a file name. A linked image's alt names
  the destination.
- Icons in controls: the control carries the name, the glyph is hidden.

## Loading

- Below the first screen: `loading="lazy"` and `decoding="async"` on images
  and iframes.
- The largest visible image (hero, banner), above the fold: never lazy. Mark
  it `fetchpriority="high"` and preload it when the framework allows (Next.js:
  the `priority` prop). Render it once: the same image in a desktop branch and
  a mobile branch, both prioritised, is requested twice.
- Use the framework's image component when the project has one (it usually
  handles `srcset`, lazy loading and dimensions) and do not mix it with raw
  `<img>` in the same list, unless remote or user-uploaded hosts force it
  (then the raw `<img>` still gets `loading`, `decoding` and dimensions).
- Fonts: `font-display: swap`, a system fallback with similar metrics, and only
  the weights in use. No layout shift from late fonts, ads or embeds.
- Animations use `transform` and `opacity`. Respect reduced motion.

## Findability (SEO and search visibility)

What a page can do for itself. Ranking also depends on content quality, links
from other sites and domain history; never promise a position.

- One `<title>` per page, specific, 50 to 60 characters; one meta
  description, 120 to 160 characters, written for a person.
- Exactly one `<h1>` that states the page's subject; headings follow order
  without skipping, and are not chosen for their size.
- Semantic landmarks (`header`, `nav`, `main`, `footer`) and real lists,
  buttons and links. Link text says where it goes; "click here" is a finding.
- Real, crawlable `<a href>` for navigation; no navigation behind click
  handlers only. Content that matters is in the HTML the server sends, not
  only drawn after a script runs (a client-side fetch for main content is
  Medium and needs the user's go to restructure).
- `lang` on `<html>` matches the page language; the `viewport` meta is
  present (some frameworks, such as Next.js, inject it; do not flag those).
- Share metadata: `og:title`, `og:description`, `og:image` (the file exists),
  a canonical URL, and structured data (JSON-LD) when the page is an article,
  product, organisation or similar. Do not invent facts for it.
- Speed is a ranking input: images and fonts follow the rules above, and the
  first screen does not wait on third-party scripts.
- Out of scope here (name them, do not do them): sitemap, robots rules,
  redirects, analytics, paid search campaigns. For an advertising landing page,
  also check that the page's message matches the ad and that it loads fast.

## Review signals

Report as findings with `file:line`. Severity: missing local og or download
file, or a missing `alt` on an informative image, is Medium (High when it is
the primary action); generic alt, lazy-loading or dimension gaps, px in a rem
project and title or description length outside the ranges are Low. The
length ranges are guidelines, not limits.

Signals to look for:

- An `<img>` without `alt`, or with a generic or file-name alt.
- Fixed `width: Npx` on a fluid image.
- A hero image with `loading="lazy"`, or below-fold images without it.
- Missing `width`/`height` on images.
- px sizes for text, padding or radius in a rem project.
- A `style="..."` attribute holding static values (Low).
- More than one `<h1>`, or none.
- Missing title or description.
- `href="#"` navigation.

## Conflicts

A project rule that contradicts a default here wins; report the trade-off once.
Examples: a px-based design system, a CMS that controls the markup, an email
template where `rem` and modern attributes are unsupported.
Order of precedence: see Precedence in `SKILL.md`.
