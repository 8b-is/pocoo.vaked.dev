# language layers — the rule for this shelf

**Seated 2026-10-11.** Written after an audit found that a
"add Sanskrit everywhere" pass could not be done honestly, and a rule was
needed more than a batch.

## the rule

A language layer is added to a line **only when that line is in that
language.**

- A **Sanskrit mantra written in Tibetan script** takes a Sanskrit layer:
  the same text, transliterated (IAST) and in Devanāgarī. That is a script
  change, not a translation, and it is checkable.
- A **Tibetan-language verse** takes *no* Sanskrit layer. Tibetan liturgy
  has no Sanskrit original; supplying one would be back-translation, which
  is invention wearing a citation's clothes.
- A **Hungarian book** takes an English layer only by *translation*, which
  is an editorial act on the author's prose — done deliberately, in
  review, never as a side-effect of a batch.
- A **prose book with no mantra content** takes nothing. There is no
  Sanskrit to add.

> The absence of a layer is information. Mark *which* layer is missing and
> why, rather than filling the column.

## the audit (2026-10-11)

Three shelves, checked, because they are easy to conflate:

| shelf | what it is | Sanskrit / transliteration |
|---|---|---|
| `sovereign-library/books/` | the **print canon — five books** | **none.** Five English essays (the NAND book, *Readability Is Freedom*, *Purple People Eaters*, *Admissible Degradation*, the diatribe corpus). Zero mantra content; nothing to add without inventing it |
| `pocoo.vaked.dev/book/` | the **book shelf — 78 sources** | **two** carry a Tibetan layer: `chenrezig-karmapa` (57 Tibetan + 57 English lines) and `mahakala-csenrezi` (Hungarian, mantras in undiacritised Latin) |
| everything else | plain prose, songbooks, ledgers | no layered structure, no mantra content |

So the honest scope of "add Sanskrit to the books that lack it" is **two
books and four lines**, not eighty.

## what was added (2026-10-11)

**`chenrezig-karmapa/manuscript.html`** — the book is Tibetan phonetics +
English, with no third layer. Exactly one line is Sanskrit:
`ཨོཾ་མ་ཎི་པདྨེ་ཧཱུྃ`. It now carries

```
oṃ maṇi padme hūṃ   ॐ मणि पद्मे हूं
```

with a `.skr` style, and a note stating that the other 57 lines are
Tibetan and deliberately have **no** Sanskrit column.

**`mahakala-csenrezi/manuscript.html`** — three mantra lines, previously
undiacritised. Now `oṃ maṇi padme hūṃ · oṃ mahākāla ya hūṃ phaṭ`, with the
Devanāgarī given once in a note. The Mahākāla formula is diacritised **as
the book words it**, with its canonical spelling flagged unconfirmed (the
received form is usually *oṃ mahākāla hūṃ phaṭ*, without *ya*) — the text
is not silently corrected, and the flag says so.

## still open

- **an English layer for `mahakala-csenrezi`.** It is a 131-line Hungarian
  book. That is a translation, and translating the author's own poetic
  prose needs the author in the loop — not a batch pass.
- the other 76 sources are prose; **nothing to do**, and that is the
  finding rather than a to-do.

*the rule outlives the batch. fine touch from within · vaked.dev · 8b-is,
2026-10-11*
