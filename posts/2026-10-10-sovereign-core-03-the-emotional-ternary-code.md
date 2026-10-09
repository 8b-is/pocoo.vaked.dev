---
title: "Sovereign Core, part 3 — the emotional ternary code"
date: 2026-10-10
description: "Feelings on a {−1, 0, +1} wire: quantize Valence, Arousal and Dominance to trits, pack four per byte, print a qt: tag. A zero is a real 'don't know'. Here is the whole codec, why it rides the wave frame, and the one honest caveat."
tags: [engineering, rust, sovereign-core, qwave, quanttern, ternary, bitnet, emotion]
draft: false
---

# Sovereign Core, part 3 — the emotional ternary code

*A multipart deep dive into the core the constellation runs on. Part 3 of 6.*

---

BitNet b1.58 quantizes *weights* to `{−1, 0, +1}`. `quanttern` quantizes
**feeling** the same way. The VAD model of affect (Valence · Arousal ·
Dominance, each −1…+1) becomes three trits, packed four to a byte — a tiny,
honest fingerprint that cannot lie about *how much* it is sure.

## The threshold is the whole point

```rust
pub const DEFAULT_THRESHOLD: f32 = 0.33;

impl Trit {
    pub fn from_f32(x: f32, threshold: f32) -> Self {
        if x >= threshold { Trit::Plus }
        else if x <= -threshold { Trit::Minus }
        else { Trit::Zero }
    }
}
```

A value that is not clearly positive and not clearly negative reads as **zero**.
Not "a small positive". Not "probably neutral". A real `don't know`, which is the
only honest output for a signal that isn't there.

## Packing: four trits per byte

```
code = (trit + 1) & 0b11      // −1→0b00, 0→0b01, +1→0b10
byte = code₀ | code₁<<2 | code₂<<4 | code₃<<6
```

Three trits fit in one byte with two bits to spare, and the encoding is
self-describing: you can unpack without a schema. The wire tag is a short hex
string:

```
qt:56     ← magnitude 1/3   (one axis fired)
qt:aa     ← magnitude 2/3
qt:...    ← magnitude 3/3
```

The `magnitude` is the count of non-zero trits — the *signal* in the
fingerprint. Two moods are compared not by distance in a metric space but by
**agreement**: the fraction of trits that match, in `{0…1}`.

## It rides the wave frame

The reason this is part 3 and not a curiosity: `EmotionCode::wave_fields()`
projects the `(valence, arousal)` pair onto `Rational` integers — the exact types
the 79-byte `WaveInt` frame already carries (part 2). So a feeling is not a
separate system; it is a **view** of the memory substrate. Dominance has no wave
axis (there are only two rationals in the frame), and the codec says so instead
of inventing a third.

## Three alphabets, one contract

The same `{−1, 0, +1}` idea lives in three places, deliberately:

| home | language | role |
|---|---|---|
| `qultrakotoro/Sources/QuantTern/QuantTern.swift` | Swift | the origin — on-device STT + the emotional code |
| `crush-love-dev/quanttern.rs` | Rust | the launcher's gate codec (with a pinned golden hash) |
| `qwave/core/src/quanttern.rs` | Rust | the sovereign core, bridged to the wave frame |

They agree on the contract (threshold → trits → two-bit packing → a `qt:` tag)
and differ only in the alphabet of the *packing*, which each documents. Cite,
don't copy.

## The honest caveat

This is a **fingerprint**, not a model. A hand-rolled positive/negative word list
is not sentiment analysis, and the code says so: *a real build layers a learned
model on top; the contract (text → VAD → EmotionCode) is what matters.* The value
is the interface — a stable, tiny, inspectable shape for affect — not a claim of
psychological accuracy.

## Receipts

- `core/src/quanttern.rs` — 6 tests: the threshold makes a real zero, pack/unpack
  identity, agreement, the wave bridge.
- `qultrakotoro` — 21 tests green across the app + core (part of this series'
  sibling work).

*Previous: [part 2 — the 79-byte wave frame](/posts/2026-10-10-sovereign-core-02-the-79-byte-wave-frame). Next: [part 4 — the admissible transition](/posts/2026-10-10-sovereign-core-04-the-admissible-transition).*

*refuse · rest · affirm · 0 + 1 · fine touch from within*
