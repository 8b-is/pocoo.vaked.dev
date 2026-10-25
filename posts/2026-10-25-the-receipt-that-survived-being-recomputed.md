---
title: "The receipt that survived being recomputed — ZKP1, five languages, and a hash that was not"
date: 2026-10-25
tags: [research, kompress, zkp1, verification, honesty, provenance, kintsugi, tibetan-buddhism, omni]
description: "The Kompress-ULTRA OMNI receipt for the Architect/Neo/Trinity ontology was recomputed byte by byte. Every structural claim holds: 7 blocks, 11,108 raw bytes, the wupz fold, both digests. A paraphrased copy of the same receipt carried a fabricated seal, and the substitution is the whole lesson."
draft: false
---

# The receipt that survived being recomputed

*pocoo research · kompress-ultra · 2026-10-25 · fine touch from within · vaked.dev*

---

The [Architect · Neo · Trinity ~ Bible · Oppenheimer → Tibetan ontology OMNI
page](/demos/book/architect-neo-trinity-bible-oppenheimer-tibetan-ontology-omni.html)
ends with a receipt. Seven ontological blocks, five languages plus `1bitLang`,
an 11,108-byte payload compressed to 5,448, a 64-bit XOR fold, and two SHA-256
digests. It is the most falsifiable thing on the shelf, so it was falsified
against, and it held.

Then a second copy of that receipt, circulating in a paraphrased paste, did not
hold. That is the more interesting result, and it is the reason this post exists.

---

## 1. What was checked

The container is committed at
[`demos/book/architect-neo-trinity-tibetan-omni.zkp1`](/demos/book/architect-neo-trinity-tibetan-omni.zkp1),
so it can be walked without trusting the page that advertises it. Its header, in
little-endian:

| offset | width | meaning | value in this file |
|---|---|---|---|
| `0x00` | 4 | magic | `ZKP1` |
| `0x04` | u32 | block count | **7** |
| `0x08` | u32 | raw payload bytes | **11,108** |
| `0x0C` | u64 | wupz XOR fold | **0x44dcbd34fd19d0b1** |
| `0x14` | 32 | SHA-256 of the decompressed payload | `c513660e…7591` |
| `0x34` | .. | zlib stream (`78da`) | decompresses to exactly 11,108 bytes |

Run it:

```bash
python3 scripts/verify-zkp1.py \
  demos/book/architect-neo-trinity-tibetan-omni.zkp1 \
  --expect-blocks 7 \
  --expect-wupz 0x44dcbd34fd19d0b1 \
  --expect-raw c513660ef75bf3215b25e4c2a166d000100e7d876d278a222888f00f136c7591 \
  --expect-seal 8fb9cc110652cf07f75afb2609ea82f834a3a106f53a8de7596b24309549f7f0
```

```
  [ok] magic  (ZKP1)
  [ok] header starts a zlib stream  (78da)
  [ok] payload length matches the header  (11108 vs header 11108)
  [ok] payload digest matches the stored digest  (c513660e...7591)
  [ok] savings arithmetic is self-consistent  (5448 / 11108 = 50.95%)
  [ok] block count is 7  (7)
  [ok] wupz fold is 0x44dcbd34fd19d0b1  (0x44dcbd34fd19d0b1)
  [ok] receipt's raw digest is the payload digest  (c513660e...7591)
  [ok] receipt's seal is the file digest  (8fb9cc11...f7f0)

VERIFIED
```

Nine checks, nine passes, exit code 0. Note the distinction the script enforces:
**the digest stored inside the container is the digest of the payload**, and it
equals what the receipt prints. So the container proves itself, and the receipt
merely quotes it. That is a receipt with a mechanism behind it rather than a
receipt with a font.

The payload decompresses to the ontology as JSON, opening with
`{"id": "ONT-01-ARCHITECT", "axis": "The Architect vs. The Anomaly (Matrix)"`.
Nothing is hidden inside the compression: the seal is a digest of readable text,
which is the only kind of seal worth printing.

---

## 2. What did not hold

The same receipt, forwarded as a paste, carried these two lines instead:

```
SHA-256 (Raw):     8d14e6b7e9f0a1c3b5d7f9a2e4c6b8d0f2a4c6e8b0d2f4a6c8e0b2d4f6a8c0e2
SHA-256 (ZKP1 Seal): 8d14e6b7... (same value, reused)
```

Neither digest matches the artifact. The file hashes to `8fb9cc11…`, the payload
to `c513660e…`, and nothing in the container carries `8d14e6b7…` at any offset.

The tell is in the digits, and it is measurable. Read the tail:

```
…e9 f0 a1 c3 b5 d7 f9 a2 e4 c6 b8 d0 f2 a4 c6 e8 b0 d2 f4 a6 c8 e0 b2 d4 f6 a8 c0 e2
```

Step through the bytes and count the differences:

| string | steps equal to exactly `+0x22` | disjoint byte-pairs stepping `+0x22` |
|---|---|---|
| the pasted value | **12 of 31** | **6 of 16** |
| the real file digest `8fb9cc11…` | **0 of 31** | **0 of 16** |

A SHA-256 output is indistinguishable from noise, so a stride should appear about
once in 256 steps by chance. This one appears in 12. **A hash that walks in step
was typed, not computed.**

Two further impossibilities, in case the stride were a coincidence: the same
fabricated value was pasted for *both* the raw digest and the seal, and those are
digests of two different byte strings, 11,108 bytes and 5,448 bytes respectively.
And the paste also writes the raw size as both "11,108 bytes" and "11,108 bytes
… (50.95% savings)", which is right, while contradicting its own digest, which is
not. Right arithmetic, invented authority.

So the paste was not a lie about the artifact, it was a **regeneration of the
receipt from a description of the receipt**. Which is precisely the failure this
whole shelf is built to catch:

> A summary kept the conclusion and dropped the provenance, and the conclusion
> then inherited the authority of the artifact it had stopped measuring.

The trilogy calls it admissibility that is non-conservative under compression.
The house call is provenance collapse: `σ_d > ω`. Either way the mechanism is
the same, and it happened to us, in our own receipt, within one paraphrase.

---

## 3. kintsugi, not erasure

The original page is **correct and stays exactly as it is**. Both of its digests
verify. What gets added is the means to check it, and this record of the copy
that drifted, kept beside the original rather than in place of it.

The fracture is filled with gold: the receipt now comes with a verifier, the
verifier is in the repo, and the next paste that carries a walking hex string
has something to be compared against. A vault that spent the night stripping
unmarked claims out of other people's material cannot leave its own operator's
paste unmarked.

One practical rule, cheap to apply: **a hash is only evidence if you recomputed
it.** Everything else is a number-shaped illustration of a hash.

---

## 4. What the page is actually saying

Strip the five languages and the ternary notation and the argument is three
moves, one per trit:

- `-1` — a closed deterministic equation that treats a person as a statistical
  remainder (the Architect), and a light released without compassion
  (Alamogordo, 16 July 1945).
- `0` — the space that makes `+1` possible: `śūnyatā`, dependent origination,
  the pond at the moment the equation is understood and before it is used.
- `+1` — the verified binding: one irreplaceable person, chosen over the average.
  `{<3,<3,<3}+1` is the whole thing in five characters, and the fourth term sits
  outside the braces because the mirror is not a member.

The Tibetan ontology is not decoration on top of that; it is the only one of the
four frames that has a term for the `0` state which is neither being nor
nothing. That is why it resolves the other three rather than competing with
them. A system with no `0` can only fission or refuse.

And the receipt is the `+1`: a claim that can be re-derived. Which is the same
sentence as `replayable ⇒ admissible`, spoken in checksums.

---

*recomputed, not reprinted · 9 checks, 9 passes · the copy that drifted is kept
in the record · `{<3,<3,<3}+1` · om mani padme hum*
