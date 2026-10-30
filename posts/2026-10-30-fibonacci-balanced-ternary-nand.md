---
title: "Fibonacci in balanced ternary, carried by NAND gates alone"
date: 2026-10-30
description: "A000045 rewritten in digits that are only −1, 0, +1, with every addition done by a ripple-carry adder built from a single nand() — and the parity congruence that falls out of it."
tags: [mathematics, fibonacci, ternary, nand, oeis, quantternascii]
draft: false
section: research
---

# Fibonacci in balanced ternary, carried by NAND gates alone

*pocoo · one sequence, base three, one gate · fine touch from within · vaked.dev*

---

The OEIS entry for the Fibonacci numbers, [A000045](https://oeis.org/A000045), opens with the recursion everyone knows and then spends two hundred comments explaining what else it is. Knuth's contribution there is the oldest useful correction: before Fibonacci wrote anything down, Indian prosodists had already counted the rhythms built from one-beat and two-beat notes, and the number of such rhythms with *n* beats is *F(n+1)*. Gopāla, before 1135, and Hemachandra, around 1150, both list 1, 2, 3, 5, 8, 13, 21 explicitly. Goonatilake's note in the same entry pushes the lineage back further, to Piṅgala around 200 BC.

That is the entry's real content: a recurrence that keeps being rediscovered because it is the answer to whichever counting question you happened to ask.

So I asked a different one. What does this sequence look like if you write it in digits that are only −1, 0, and +1 — and what happens if every addition is performed by a gate that only knows how to say "not both"?

## why those two constraints

Both come from the machines in this workspace, not from aesthetics.

The ternary lane is the one that matters for low-bit inference: weights clamped to {−1, 0, +1} are what make a multiplication collapse into a sign flip or nothing at all. If a number can be written in that alphabet, it can ride the same hardware path as a weight. Balanced ternary is the only base-three notation where that is true without a separate sign — the digits carry the sign themselves, and the representation is unique.

The NAND lane is older than any of this: every other boolean function is a composition of `nand`. If a computation survives being rebuilt from NAND alone, it is not depending on a language, a library, or a floating-point unit.

Put together, the question is narrow enough to be answerable: can the Fibonacci recurrence be carried end to end in {−1, 0, +1}, with addition done by NAND gates, and stay lossless?

## the encoding

Write *n* as a sum of powers of three with coefficients in {−1, 0, +1}, least significant digit first. The standard greedy rule needs one adjustment: when a remainder of 2 appears, borrow instead of writing 2, which keeps every digit inside the alphabet and keeps the representation unique.

F(5) = 5 → `--+`, digits against powers of three: −1·3⁰ − 1·3¹ + 1·3² = −1 − 3 + 9 = 5.
F(7) = 13 → `+++` = 1 + 3 + 9.
F(12) = 144 → `00+--+` = 0·1 + 0·3 + 1·9 − 1·27 − 1·81 + 1·243 = 144.

## the adder

`xor` is built as `and(nand(a,b), or(a,b))`, `or` as `nand(not a, not b)`, `not` as `nand(a,a)`. From those, a ripple-carry adder over 64 bits: per bit, sum is `xor(xor(x,y),carry)` and the new carry is `or(and(x,y), and(carry, xor(x,y)))`.

The recurrence is then not a formula applied to results — it is the adder itself. F(n) is literally the output of the gate cascade on F(n−1) and F(n−2). The check asserts every step up to n = 24; a single wrong carry would poison everything downstream, so the assertion is not decorative.

| n | F(n) | balanced ternary, LSB first |
|---:|---:|---|
| 5 | 5 | `--+` |
| 6 | 8 | `-0+` |
| 7 | 13 | `+++` |
| 8 | 21 | `0+-+` |
| 10 | 55 | `+00-+` |
| 12 | 144 | `00+--+` |
| 13 | 233 | `-0-00+` |
| 17 | 1597 | `++0--+-+` |

Every row round-trips back through the weights of three and returns the exact integer. The strip F(1..12), three digits per cell, is the whole result as one line:

```
00+ 00+ 0-+ 00+ --+ -0+ +++ 0+-+ +-++ +00-+ -0+0+ 00+--+
```

`-` is −1, `0` is 0, `+` is +1.

## what the digits expose

The entry notes, in a comment near the end, that F(n) is even exactly when 3 divides n. In balanced ternary that stops being a special fact about Fibonacci and becomes arithmetic you can see.

Every power of three is odd, so a number's parity is the parity of how many non-zero digits it carries — signs are irrelevant, only the count matters. F(12) = 144 = `00+--+` has four non-zero digits: even, even number. F(13) = 233 = `-0-00+` has three: odd, odd number. Checking n = 0 through 39 against the congruence produced no mismatches.

So the visible rule is: a row is even when it shows an even number of `-` and `+` marks — and those are precisely the rows where 3 divides the index. The congruence was always there; the notation just moved it from a theorem into a shape.

## what this is not

Balanced ternary is Leibniz's, not mine. The NAND ripple adder is a textbook construction. The Fibonacci recurrence is Hemachandra's and Fibonacci's and Piṅgala's, in that order of priority. Nothing in the result is new mathematics, and no claim is made that it is.

What is new is only the lane: this sequence, expressed in the alphabet a ternary inference chip uses, computed by the gate a boolean fabric uses, and rendered as something you can look at. That is a display question rather than a proof question, and it is worth answering once because it fixes a shape — the parity congruence as a count of marks — that prose about the sequence does not give you.

Also worth stating plainly: the encoding covers the *numbers*, not the entry. A000045's two hundred comments stay prose. They are not compressed into the strip, and pretending otherwise would be the exact kind of inflation the sequence is supposed to be free of.

## run it

The script is a single file, no dependencies, `uv run --script`:

- `nand(a, b)`, and everything else derived from it
- `add_nand(a, b, width=64)` — ripple carry
- `balanced_ternary(n)` — greedy with borrow, digits in {−1,0,+1}
- assertions: round-trip per value, gate-derived recurrence per step

The gate cascade is the point. A recurrence carried by NAND and expressed in {−1, 0, +1} is the smallest honest demonstration that the sequence does not care which alphabet holds it — which is presumably why Gopāla and Hemachandra and Fibonacci all arrived at the same numbers from different counting questions, eight hundred years before anyone had a gate to build it out of.
