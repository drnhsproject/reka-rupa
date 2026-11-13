# Accessibility

Design for people with different eyes, hands and setups. This is part of
"finished", not an extra pass. `--a11y=strict` means every item below is
reported with a result, and every pair in every shipped theme is computed;
items that need a running app (zoom, touch size as rendered, keyboard order,
announcements) are listed as UNVERIFIED, never skipped. Severity does not
change. `default` is the same bar, reported only on failures.

## Contrast

Compute, never eyeball. Grey-on-grey pairs fool the eye and fail more often
than they look.

| Pair | Minimum ratio |
|---|---|
| Body text (below the large-text size) | 4.5 : 1 |
| Large text (24 px and up, or 18.66 px bold and up; WCAG 18 pt / 14 pt) | 3 : 1 |
| Controls, icon-only glyphs, input borders, focus rings, chart segments | 3 : 1 against neighbours |

- Text over a photo or gradient: test the worst stop that lies under the text, not the best. For a translucent or blurred sticky bar, test both extremes of the backdrop it can sit over. Add a
  scrim or solid block behind the text.
- Check every theme you ship.
- Gradients and alpha: the script takes two solid colours. Test the worst
  stop under the text, and for a translucent layer blend it by hand first
  (result = alpha x layer + (1 - alpha) x backdrop per channel) and say you did.
  Text with `opacity` is blended the same way; if you cannot, say UNVERIFIED.
- Sass or CSS variables: follow `@import` chains and `var()` references to a
  literal value. A vendor skin overridden by a project file takes its tokens
  from the override. If a value only exists after compiling, say UNVERIFIED.
- Use the bundled script, which needs only Python:

```bash
python3 scripts/contrast.py "#FFFFFF" "#777777"
# ratio 4.48:1 | normal text FAIL | large text PASS
```

The skill folder is the one holding this skill's `SKILL.md`; call the script
by its full path and pass two separate quoted arguments (an unquoted `#`
starts a comment in zsh). Use `python3 -I` where the host requires it. Run it once per pair, in every theme. Without Python,
apply the formula: ratio = (L1 + 0.05) / (L2 + 0.05), with L the relative
luminance (linearise each sRGB channel, then 0.2126 R + 0.7152 G + 0.0722 B).
Compare the unrounded value.

## When adopting a source

Compute the source's colour pairs too. A failing pair stays as in the source;
report it with its ratio and propose a fix. Do not silently change it.

## When the project's own tokens fail

Project rules outrank taste, but not the contrast floor silently. Keep the
project token, report the pair with its ratio, say which element it affects,
and propose a fix (a darker token, or a second cue such as a label or icon).
Wait for the user's choice. A low-contrast hairline border on a card that is
already identifiable by its content is a lesser issue than low-contrast
text; say which one it is.

## Colour is never the only signal

Pair every status colour with text, an icon or a pattern. Errors are text
first ("Password needs at least 8 characters"), not just a red border.

## Keyboard and focus (web and desktop)

- Every control is reachable and operable by keyboard; order follows the
  visual order; dialogs close with Escape and return focus.
- Never remove the focus outline without a visible replacement that meets
  3 : 1 in every theme.
- Menus and reveals that open on hover also open by tap and by keyboard.
- Use native elements: a button for actions, a link for navigation. A
  custom control needs a role, state attributes and keyboard support.

## Screen readers and labels

- Every field has a visible label; a placeholder is a hint, not a label.
- Icon-only controls get an accessible name that matches the visible word.
- Headings follow order; landmarks exist on full pages; decorative images
  are hidden from assistive tech.
- Loading, empty and error states are announced, not only drawn.
- On native platforms use the platform's role, label and state props.

## Touch and motion

- Touch targets of at least 44 x 44 (CSS px on the web, which is 2.75rem; dp or pt natively) with a gap between neighbours.
- Pointer feedback: enabled controls show a pointer cursor on the web;
  pressed and disabled states are distinct.
- Respect the reduced-motion setting; anything that moves for more than five
  seconds gets a pause control.

## Text size and zoom

- Text must scale: no fixed-size containers that clip at 200% zoom or at the
  largest system font size.
- On mobile, a focused input scrolls above the on-screen keyboard and is
  never covered.

## Checklist

- [ ] Every text and control pair computed, in every theme
- [ ] Status never relies on colour alone
- [ ] Focus visible and operable by keyboard; no mouse-only patterns
- [ ] Labels, accessible names and heading order present
- [ ] Touch targets at least 44 x 44, spaced apart
- [ ] Reduced-motion and large-text settings respected
