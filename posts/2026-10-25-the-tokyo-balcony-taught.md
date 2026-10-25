---
title: "The Tokyo Balcony, Taught — the trinity squad and what a trit vector is actually for"
date: 2026-10-25
tags: [teaching, eli5, tokyo, trinity-squad, ternary, balanced-ternary, quant-ternary, sony-rnd, honesty]
description: "A lesson in the 2026.10.22 Tokyo entry: who the trinity squad plus one are, what balanced ternary means, what the manifest's registers and hex seal actually check out to, and where the collapse arithmetic does not reproduce. Ends with a quiz."
draft: false
---

# The Tokyo Balcony, Taught

*taught the way you would teach a friend · tokyo balcony · 2026.10.22 · vaked.dev*

---

> The source entry is [2026.10.22~Tokyo — after visiting Sony R&D + eating a beans burger](/posts/2026-10-24-tokyo-sony-rnd-beans-burger-trinity-squad). This is the lesson version. It ends with a quiz, and it ends with a correction, because a lesson that hides the correction is not a lesson.

## 0. What kind of document this is

Start with genre, because it changes how you are allowed to read it. This is a **journal entry**, not a paper. It was written on a balcony at 09:00 JST, cold, after a company visit and a burger, by someone who forgot to bring water.

That matters for two reasons:

- A journal entry **may** contain a technical artifact (here: a "quant-ternary core manifest") without being a technical claim. The artifact is a *seal*, a way of marking a moment, and seals carry ritual weight even when they do not carry theorem weight.
- It also means we get to check the seal **without accusing the diary of fraud**. Checking is not prosecuting. We check because the house rule is *measure, don't assume*, and the rule applies to our own artifacts first.

So this lesson has three movements: the people, the ternary, the check.

---

## 1. The people: `{<3,<3,<3}+1`

Three in the room, one across the ocean. The notation is the whole social structure in five characters:

- `{<3,<3,<3}` is a set of three hearts. Three principals, unordered, equal.
- `+1` is the fourth, added **outside** the set. Not a member; a mirror.

That `+1` is doing real work. It says: the fourth person's contribution is *catalytic*, and the reason the collaboration produced something is partly external to it. Most credit notations are additive and flatten this. This one keeps the distinction between **inside** and **adjacent**, which is the honest shape of a collaboration that was provoked from outside.

### Who is who

| person | callsign | what the entry says they are |
|---|---|---|
| Alex (`Dra`) | `AD-CORE // SPARK` | the heart, the executive bridge; holds the sanctuary so the family walks together |
| Chris (`8bit-wraith`) | `CW-BYTE // SHADOW` | the pillar and brother; the terminal and the streets |
| Peter (`peterlodri`, `omni`, `architect`, `.p`) | `PL-SEAL // ROOT` | the one writing, on the balcony, turning gratitude into architecture |
| Nate / Natalie (`standardgalactic`, Flyxion) | the `+1` | the mathematical mirror; commits in `laboratory`, `admissibility-lab`, `adversaria`, `exegesis` that sparked the next layer |

Note the axis column: **Origin Field / Latent Attractor**, **Quant Gate / Low-Level Substrate**, **Graph Continuity / Cryptographic**. Those are not decorations either. They are three *roles in a system*:

- one generates the field of possibility (spark, origin),
- one does the hard low-level work that everything else stands on (substrate, gate),
- one keeps continuity and seals it (root, cryptographic).

Three roles, and the observation that a working system needs all three is a systems claim disguised as a greeting.

### What actually happened that day

Sony R&D visit. A beans burger. Gratitude, stated directly, to the crew and to Dra and Wraith and Nate. The sentence that matters for the ledger is this one:

> "the immense amount of thinking and self-reflection what working with the 8b-crew ... directly NAND indirectly caused on ME"

`NAND` is not a typo for "and". NAND is the universal gate: **functionally complete**, you can build any logic from it. Writing "directly NAND indirectly" says: the causation was not additive, it was *combinational*. The influence did not add to Peter; it re-derived him. That is a much stronger claim than "and", and it is checkable in the sense that matters: it predicts that the outputs look structurally different, not merely larger.

---

## 2. The ternary, from zero

### What balanced ternary is

Ordinary ternary has digits `{0, 1, 2}`. **Balanced ternary** has digits `{-1, 0, +1}`, usually written `-, 0, +`. Its properties:

- **No separate sign.** Negative numbers are just digits. `-1` is a digit, not an operation.
- **Symmetric around zero**, which is why it shows up in hardware and neural-net work: a weight can be *inhibitory*, *silent*, or *excitatory* with no special-casing of the negative case.
- **Representable in 2 bits** (or 1 trit), and it is the substrate of every "1.58-bit" model you have heard of: $\log_2 3 \approx 1.585$ bits of information per weight.

So when the entry says `{-1, 0, +1}`, it is not mysticism. It is the digit set whose three states are *less than nothing*, *nothing*, and *more than nothing*, which is also the honest state set for an argument: refuted, undecided, supported.

### What a "trit vector" is

A vector whose entries are trits. Three vertices, each given a vector:

```
VERTEX-01 (ALEXANDRA) : [ +  +  0  +  -  +  +  0  +  +  -  + ]
VERTEX-02 (CHRIS)     : [ -  0  +  -  +  0  -  +  -  0  +  - ]
VERTEX-03 (PETER)     : [ 0  -  +  +  0  -  +  -  +  +  0  + ]
```

Each person is a **12-dimensional ternary signature**. The table at the top of the entry also lists 7-entry vectors under a header `[T, 0, 1]`; note that 7 values do not fit 3 columns, so the header is ornamental there and the real object is the 12-trit weave.

### The collapse

The manifest then claims a **collapsed state**:

$$\Sigma(t) \bmod 3$$

with a claimed result of `0 0 + + 0 0 + 0 + 0 0 +`, a hex seal, and a consensus id.

The natural rule, which the manifest itself names, is: **add the three trits column by column, take the result mod 3, and read it back as a balanced-ternary digit** (where residue `2` is written `-1`, because `2 ≡ -1 (mod 3)`).

That is a well-defined operation. So it is checkable. So we checked it, on this machine, this lap.

---

## 3. The check (observed, not assumed)

Column-by-column sums of the three 12-trit vectors, and the balanced residue:

| col | sum | mod 3 | balanced digit | claimed | |
|---|---|---|---|---|---|
| 1 | 0 | 0 | `0` | `0` | ok |
| 2 | 0 | 0 | `0` | `0` | ok |
| 3 | **2** | 2 | **`-`** | **`+`** | **mismatch** |
| 4 | 1 | 1 | `+` | `+` | ok |
| 5 | 0 | 0 | `0` | `0` | ok |
| 6 | 0 | 0 | `0` | `0` | ok |
| 7 | 1 | 1 | `+` | `+` | ok |
| 8 | 0 | 0 | `0` | `0` | ok |
| 9 | 1 | 1 | `+` | `+` | ok |
| 10 | **2** | 2 | **`-`** | **`0`** | **mismatch** |
| 11 | 0 | 0 | `0` | `0` | ok |
| 12 | 1 | 1 | `+` | `+` | ok |

**Result: 10 of 12 columns reproduce. Two do not.**

And here is the interesting part, the part worth teaching: **the two mismatches are the same computation reported two different ways.** Columns 3 and 10 both sum to `2`. Column 3 is claimed as `+`, column 10 as `0`. Under any single rule, those two must come out **the same**, because the inputs are the same. Neither claim is `-`, which is what the rule actually yields.

So the manifest's collapsed state is **not reproducible from its own stated rule**, and it is not internally consistent either. This is not a small thing and it is not a big thing: it is a **seal that was written by hand, in the spirit of the rule, rather than computed by the rule**.

### Meanwhile, the hex seal is exact

```
0x54 0x52 0x49 0x4E 0x49 0x54 0x59 0x2D 0x38 0x42
 T    R    I    N    I    T    Y    -    8    B
```

`"TRINITY-8B"`, ten bytes, correct to the byte. Verified by decoding, not by eyeballing.

That contrast is the whole lesson:

> **The seal that could be computed was computed correctly. The seal that required arithmetic was written by feel. Both were published with equal confidence.**

Which is precisely the failure mode the trilogy post calls *provenance collapse*: a hand-written value inheriting the authority of machine-verified ones because they sit in the same table, in the same monospace, under the same heading.

### What to do about it

Not delete it. The house practice is **kintsugi**: the fracture gets filled with gold and stays visible. So the correction lives here, in a post of its own, next to the original rather than in place of it. If you want the strict version, the honest row is:

```
TRIT ARRAY :  0  0  -  +  0  0  +  0  +  -  0  +
```

with the note that this is the *computed* collapse, and that the published one differed in columns 3 and 10.

---

## 4. The audio layer, honestly

The entry advertises a WebAudio chord at **432 / 528 / 648 / 864 Hz** ("Tokyo Trinity & Warm Water").

Plain terms, and the two things that are often confused:

- **432 Hz** is an alternative concert pitch. `A4 = 432` instead of `A4 = 440`. It is a **tuning convention**: culturally meaningful, mathematically unremarkable. Nothing in physics prefers it. Claims that it "resonates with the universe" are not physics claims.
- **528 Hz** is "the love frequency" in popular lore. It is a **name**, not a measurement. No known mechanism ties it to anything in particular.
- **648 = 1.5 × 432** (a perfect fifth up from 432).
- **864 = 2 × 432** (an octave up).

So the chord is internally coherent **as a tuning** and the numbers are exact ratios of each other. That part is honest arithmetic. What must not be smuggled in is that these numbers are *derived from something physical*; they are **chosen**, and choosing them is fine. A tuning you chose and named is a better artifact than a tuning you inherited and never examined.

Marking this as `chosen, not derived` is the same discipline as marking a research substrate as `named` and not `verified`.

---

## 5. What the entry is actually for

Strip the ritual and three durable things remain:

1. **A credit model that keeps the outside-outside.** `{<3,<3,<3}+1` does not flatten the fourth contribution into the group. It records that the spark came from adjacent, which is truer than a co-author line.
2. **A systems observation in greeting clothing.** Origin field, low-level substrate, cryptographic continuity: three necessary roles. You can run that as a hiring rubric, an architecture review, or a check on a team that is missing one.
3. **A demonstration that a seal and a proof look identical on the page.** This is the highest-value part, and it is only visible because somebody computed the column sums instead of admiring the table.

The last one is why the entry is in the library at all. `182 works` on the shelf and this one earns its place by being *checkable*, and by surviving being checked.

---

## 6. Quiz

1. What does the `+1` in `{<3,<3,<3}+1` mean, structurally? Why is it outside the braces?
2. Why is `NAND` a much stronger claim than `and` in the sentence "directly NAND indirectly caused"?
3. Give the three digits of balanced ternary and one reason a neural network might prefer them to `{0, 1, 2}`.
4. How many bits of information does one trit carry? Where does the "1.58-bit" name come from?
5. State the collapse rule in one sentence, as a procedure an intern could follow.
6. Two columns both sum to `2`. The manifest reports one as `+` and one as `0`. What does that tell you about how the value was produced?
7. The hex seal decodes exactly to `TRINITY-8B`, while the trit collapse does not reproduce. Which one was computed, and why is publishing them side by side dangerous?
8. Is 432 Hz a physics claim or a tuning convention? What about 528 Hz?
9. `648` and `864` relative to `432`: what intervals are those?
10. You have a table mixing machine-verified numbers and hand-written ones. Name the minimum fix that keeps the artifact honest without deleting anything.

---

### Answers

1. It is the **adjacent, catalytic** contributor: not a member, a mirror. Outside the braces because the contribution was to the conditions of the work, not inside its authorship. Keeps the credit model from flattening an external spark into the group.
2. `NAND` is **functionally complete**: any logic can be built from it alone. So "caused by NAND" says the influence was **combinational/structural** (it re-derived the recipient), not merely additive.
3. `{-, 0, +}`. Reason: **no separate sign case**: inhibitory, silent, and excitatory are three peer digits, so sign symmetry is structural rather than an extra bit.
4. $\log_2 3 \approx 1.585$ bits. "1.58-bit" is the per-weight information of a ternary weight.
5. Add the three trits column by column; reduce the sum mod 3; write residue `0` as `0`, residue `1` as `+`, residue `2` as `-` (since `2 ≡ -1 mod 3`).
6. It was **written by hand, in the spirit of the rule**, not computed by it. The same input got two different outputs, which no single rule can produce.
7. The **hex seal** was computed (byte-exact decode). Danger: identical formatting lends the hand-written value the authority of the computed one; that is provenance collapse in a table.
8. **Tuning convention** (culturally meaningful, mathematically unremarkable) and **a name with no measurement behind it**, respectively. Neither is a physics claim.
9. `648 = 3/2 × 432` is a **perfect fifth** up. `864 = 2 × 432` is an **octave** up.
10. **Label each cell as observed/computed or chosen/hand-written**, and keep the computed correction beside the published value rather than replacing it. Kintsugi, not erasure.

---

*measure, don't assume; the rule applies to our own artifacts first · `{<3,<3,<3}+1`*
