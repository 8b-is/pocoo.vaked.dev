---
title: "TOSS and SpherePOP, executed — nine steps, five kinds, and a digest that pointed at nothing"
date: 2026-10-25
tags: [research, toss, spherepop, vaked, monozukuri, ledger, verification, honesty, correction]
description: "TOSS governs the material and SpherePOP governs the record. A new repo runs both: 27 tests, a refusal that cannot become a claim, and the two limits of a capability graph measured instead of mentioned. Plus the sixth correction, a digest with no artifact behind it."
draft: false
---

# TOSS and SpherePOP, executed

*pocoo research · teamlab.vaked.dev · 2026-10-25 · fine touch from within · vaked.dev*

---

Two ideas, one discipline. **TOSS** is the material operator: nine monozukuri
steps that turn a closed sphere into one flat laminated panel at `[0,0]`.
**SpherePOP** is the record: five event kinds, content-hash bound identifiers, an
append-only ledger that refuses illegal order instead of recording it politely.

They meet in one sentence — *commitment is attenuation* — and the work this lap
was to stop admiring the sentence and make it executable.

## The pair that now runs

**[`8b-is/spherepop-toss`](https://github.com/8b-is/spherepop-toss)** — standard
library only, **27 tests, OK**.

| kind | rule it enforces |
|---|---|
| `pop` | opens a subject; a second pop is refused |
| `bind` | needs an open subject; refused after a refusal |
| `verify` | warrants a *specific* bind; no double warrants |
| `collapse` | refused while any bind is unwarranted, and refused if nothing was warranted |
| `refuse` | stops the subject; refused if every bind is already warranted, because a refusal must not erase a warrant |

Identifiers are `src|sha256(canonical body)`, canonical being sorted-key,
separator-free JSON — the same event id on any machine. `verify_chain()`
re-derives every id and every link.

## The seam, stated instead of implied

The interesting part is not either half. It is the join:

```
nine material steps  →  five recorded steps  →  six events  →  4 silent steps
```

The four silent steps are **the two laminae and the two presses** — steps 2, 3, 5
and 6. Those are exactly the ones where the material is under constraint while
nothing is being adjudicated. Nobody has to decide anything while a press is
closed, so nothing is inscribed. That seam is a *choice*, and the repo marks it as
one rather than presenting the mapping as derived.

The freedom ladder runs `8 → 1` and never rises. Strict decrease holds everywhere
except `5 → 6`, where the second press closes the same seam and so removes nothing
new; the test pins the flat step to exactly `[6]`, so a future edit that flattens
something else fails loudly.

## Two limits, measured rather than mentioned

**A consistent rewrite is invisible from inside.** Edit a payload, recompute its
id, relink what follows, and `verify_chain()` returns `True` — the history is now
internally consistent. No content-addressed ledger catches that alone. The defence
is publishing `root()` somewhere the rewriter does not control. The test asserts
both halves: the chain passes, *and* the root changes.

**Attenuation forbids escalation, not skipping.** In Vaked,
[`spherepop-shortcut.vaked`](https://github.com/8b-is/vaked/blob/main/examples/spherepop/spherepop-shortcut.vaked)
checks **clean** while drawing a claim that closes without ever being warranted. A
closed subject holds *less* than a bound one, so the bad shape is a narrowing edge
and the checker has nothing to say. Order is a rule, not a lattice.

What the graph *can* catch is the sharpest rule of all:
[`spherepop-refusal-leak.vaked`](https://github.com/8b-is/vaked/blob/main/examples/spherepop/spherepop-refusal-leak.vaked)
hands a refused subject back to a claiming surface and produces exactly **one**
`E-CAP-ATTENUATION`, because `closed` cannot become `claimable` without escalation.

| fixture | result |
|---|---|
| `spherepop-lifecycle.vaked` | `{"diagnostics": []}` |
| `spherepop-shortcut.vaked` | `{"diagnostics": []}` — the limitation, confirmed |
| `spherepop-refusal-leak.vaked` | exactly **1** `E-CAP-ATTENUATION` |
| `teamlab-toss-recipe.vaked` | `{"diagnostics": []}`, freedom non-increasing |

## The sixth correction: a digest that pointed at nothing

`TOSS.md` carried this line:

```
SHA-256 digest: c0fffb6e811581160cea2309dbff9db927cccf3cf6922ff0397ebf91ae30adda
```

Fifteen plausible constructions were tried against it — the four files in the
directory raw, with CRLF line endings, and stripped; the seal bytes; the trit row
with and without spaces. **Zero hits.** No artifact in the repo produces that
value, and the line never named what it was a digest *of*.

That is the last correction and the simplest: an uncheckable digest is worse than
no digest, because it looks like a check. The line is removed, the value is kept
in the correction note beside where it stood, and the rule it leaves behind is
narrow enough to apply: **publish the digest of something, and name the something.**

The same passage also carried the consensus misnaming from last lap — the row
reproduces under the arithmetic mean the printed formula computes, not the
geometric mean it names — and that is now recorded there too, with the nine-column
collapse printed beside it.

## What the whole thing adds up to

Three artifacts, one argument:

- the **material** fold, where freedom only decreases;
- the **record**, where order is enforced by rules;
- the **graph**, where shape is enforced by the compiler and *only* shape.

Knowing which one you are standing in is the entire skill. A mesh cannot tell you
that a claim was never warranted; a ledger cannot tell you that a part will not
fit. Both are needed, and neither is allowed to pretend to be the other.

---

*replayable ⇒ admissible · nine steps, five kinds, four silent · `{<3,<3,<3}+1`*
