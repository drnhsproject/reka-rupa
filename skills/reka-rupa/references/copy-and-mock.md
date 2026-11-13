# Copy and mock data

Every visible string, in the design file and in committed code, is formal,
polite, natural and specific. The language and the level of formality follow
the project (see `project-adapter.md`): copy the register of the existing UI
text. If the project is silent, ask once.

## Voice

- Say what the thing does or what the user can do. Prefer concrete nouns and
  verbs over abstractions.
- Polite and calm: address the user respectfully, avoid slang, avoid shouting,
  avoid exclamation marks except for genuine celebration.
- Short sentences, sentence case, one idea each. Buttons start with a verb
  that names the result ("Save changes", "Simpan perubahan").
- Be consistent: one term per concept across every screen.
- Errors say what happened and what to do next, without blame.
- Empty states say why it is empty and offer the one action that fixes it.

## Avoid

- Hype and filler: "seamless", "powerful", "next level", "unlock",
  "revolutionary", and their equivalents in any language.
- Claims without evidence: "trusted by thousands", "industry leading".
- Vague attribution: "experts say", "studies show", with no source.
- Openers and closers that add nothing: "Let's dive in", "Here's the
  thing", "I hope this helps".
- Forced triplets, "not just X, it's Y", dramatic fragments, and slogans that
  fit any product.
- Fake candour ("Honestly?"), actorless passives ("mistakes were made"),
  and software that "understands" or "wants".
- Emoji and decorative symbols inside UI text.
- ALL CAPS emphasis and decorative dashes.
- Lorem ipsum, "Test 123", "John Doe", "example@email.com" in a place a real
  value belongs.

## Mock data

Mock data lets a design and a build look real before the backend does.

- Reuse the project's mock layer, shapes and field names. Never invent a
  parallel system.
- Make it realistic: believable names, places, dates, quantities and
  durations in the project's locale; varied lengths (short, long, missing);
  plausible ranges; no repeating patterns such as 10, 20, 30.
- Include edge cases: an empty list, a very long title, a single item, a
  large count, a failed state.
- Respect formality: names, titles and descriptions read as a real, polite
  organisation would write them.
- Keep it clearly mock where it could be mistaken for fact: stay inside the
  mock layer, never display invented statistics, testimonials, customer logos
  or prices as real. Deltas ("+12%") appear only with a real, named period.
- No personal data of real people. Use invented, plausible names.
- Do not leave fields blank in a screenshot just because it is hard; fill
  them. Do not ship mock data to production paths.

## Checklist

- [ ] Language and register match the project
- [ ] No hype, filler, unsourced claims or decorative emoji
- [ ] Buttons name results; errors and empty states give a next step
- [ ] Mock data is varied, realistic, locale-correct and inside the mock layer
- [ ] No invented metrics presented as real
