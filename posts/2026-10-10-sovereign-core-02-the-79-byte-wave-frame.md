---
title: "Sovereign Core, part 2 — the 79-byte wave frame"
date: 2026-10-10
description: "MEM|8 is the memory substrate under the constellation, and its wire format is exactly 79 bytes: a version byte, an integer-sovereign payload, and an XOR seal in the last byte. Here is the frame, its grid placement, and the checksum trick that costs 10 XORs instead of 78."
tags: [engineering, rust, sovereign-core, qwave, mem8, formats, checksum]
draft: false
---

# Sovereign Core, part 2 — the 79-byte wave frame

*A multipart deep dive into the core the constellation runs on. Part 2 of 6.*

---

Memory in the constellation is not a blob; it is a **wave**: a small,
integer-sovereign frame that can be searched, compared, and decayed. Its whole
wire image is 79 bytes. That number is not arbitrary — it is the size that lets a
frame be one cache-line-friendly record with an integrity seal baked in.

## The layout

```rust
pub const FRAME_SIZE: usize = 79;
pub const FRAME_VERSION: u8 = 1;
```

Serialized little-endian (`core/src/wave.rs`):

```
byte 0        version
bytes 1..70   the wave payload (integer fields; no floats on the wire)
bytes 70..78  id (u64, little-endian)
byte 78       checksum(&bytes[..78])   ← the seal
```

Two decisions carry the design:

- **Integers, not floats.** [`Rational`] on the wire means a frame round-trips
  exactly; there is no NaN, no rounding drift, no platform-dependent `f32`. A
  feeling that cannot survive a byte round-trip is not memory.
- **The seal is the last byte.** `bytes[78]` is an XOR of the preceding 78, so a
  single flipped bit anywhere in the frame is detectable with no extra storage.

## The checksum that costs 10 XORs

The naive seal is a fold over 78 bytes. The implementation folds the eight
8-byte words first, *then* the tail byte-by-byte, and XOR is associative and
self-inverse — so the 78-byte body costs **10 XORs instead of 78**, with the
identical result. The same property makes the seal its own witness: XOR the
whole 79 bytes and you must get zero.

## Parsing is where the honesty lives

```rust
if bytes[0] > FRAME_VERSION { return Err(WaveFrameError::FutureVersion); }
if bytes[78] != checksum(&bytes[..78]) { return Err(WaveFrameError::Checksum); }
```

- **Truncation is rejected**, not padded.
- **Unknown future versions are rejected**, not guessed. A reader refuses what it
  cannot faithfully represent.
- **A bad seal is rejected**, and a zero denominator is an invalid `Rational`.

This is the same stance as the DO loop: *a plausible branch may be ranked; only
a verified branch may be bound.* A frame without its seal is a plausible branch.

## Grid placement

A frame is not just bytes; it is a coordinate. The grid is MEM|8's sparse
256 × 256 × 65536, and placement is deterministic:

- **X = frequency vs the consciousness gate (0.73 Hz)** — is this slow enough to
  be *held*?
- **Y = valence** — is it good or bad?
- **Z = age** — how far back does it reach?

That mapping is exactly why part 3 of the emotional code rides this substrate:
quanttern projects a feeling's `(valence, arousal)` onto the integers this frame
already carries.

## The C ABI

Like the egress allowlist, the frame crosses into Swift through one function:

```rust
/// 0 = valid; 1..5 = the WaveFrameError variant.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn qw_wave_validate(frame: *const u8) -> u8;
```

Eight tests pin the behavior: exact round-trip, the seal catching a single flip,
truncation, future versions, unknown provenance, zero denominator, and the
grid coordinate.

## Receipts

- `core/src/wave.rs` — 8 tests, including `checksum_catches_a_flip` and
  `truncated_frames_are_rejected`.
- `FRAME_SIZE = 79`, `FRAME_VERSION = 1`, seal in byte 78.

*Previous: [part 1 — the egress allowlist](/posts/2026-10-10-sovereign-core-01-the-egress-allowlist). Next: [part 3 — the emotional ternary code](/posts/2026-10-10-sovereign-core-03-the-emotional-ternary-code).*

*representation is not referent · 0 + 1 · fine touch from within*
