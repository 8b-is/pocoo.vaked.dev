---
title: "Sovereign Core, part 5 — kompress the link"
date: 2026-10-10
description: "wupz fuses a linker and a packer into one pass: the linker already knows the layout, so it packs while it links. The design, the address-drift problem and its fix, the zero-alloc invariant, and the honest bar it has to clear — plus the GPL boundary nobody should trip over."
tags: [engineering, rust, sovereign-core, wupz, linker, compression, zig, simd, incremental]
draft: false
---

# Sovereign Core, part 5 — kompress the link

*A multipart deep dive into the core the constellation runs on. Part 5 of 6.*

---

`wupz` = **w**(ild) + **UPX** + **z**(ig). It is an experiment: an
**incremental ultra-fast linker that also compresses**. This part is the design,
because the design is the deliverable so far — no code, by choice.

## The insight

Linking and packing are the same problem seen twice. Both transform an executable
image; both walk the same sections; both answer *where does this byte go*.
Today they are two passes and a temporary file:

```
link → temp file → pack → output
```

The packer is **re-deriving facts the linker already had**. wupz keeps them:

```
objects ─▶ [ layout plan ] ─▶ blocks ─▶ packed image
              section → addr → span → hash
```

- The linker emits a **layout plan** as a first-class artifact — not just bytes.
- The packer consumes the plan and emits packed blocks directly, keyed by the
  same content hashes.
- On rebuild, a changed section invalidates exactly the blocks whose hashes
  changed; everything else is reused verbatim.

Packing is not a post-process. It is a **view** of the layout.

## The hard problem: address drift

If you compress one section, offsets shift for everything after it — and a naive
block map invalidates the whole tail. The fix is **address-independent
windows**: pack in fixed-size windows, each a delta against the prior window, so
a shifted section perturbs *one* window, not everything downstream.

This is also why layout must be **deterministic and stable** under small edits,
and why section ordering is explicit (name/ordinal) rather than hash-ordered on
the hot path. Incrementality is a property of the layout discipline, not a cache
bolted on afterward.

## The zero-alloc invariant

One **arena** per link, sized from the plan. The hot path takes `&mut` slices
from it and never calls the global allocator. After the layout is sealed, **all
allocation is done** — packing cannot allocate. That invariant is testable: a
counting allocator that panics if it is invoked after the seal, run in CI.

## The Zig ↔ Rust seam

```
wupz-rs   (Rust)  object reader · symbol resolution · relocation ·
                  incremental graph · layout plan · packed image
wupz-zig  (Zig)   SIMD kernels (hash · diff · bit-pack · checksum) + build glue
                    ▲──────────────────────────────────────▲
                    └──────── one C ABI: wupz_abi.h ───────┘
```

Rust carries the linker model (wild's lineage: a large, subtle graph problem
where the type system pays). Zig carries the tight kernels (comptime, explicit
SIMD, allocation control). The seam is **one header**. The experiment is whether
two toolchains, two error models, and two SIMD philosophies can meet at a
zero-cost boundary and stay zero-alloc. If they can't, that is a finding worth
publishing.

## The GPL boundary (do not trip over it)

wild is Apache-2.0. **UPX is GPL-2.0-or-later** (with the UPX exception that
permits packing non-GPL programs). Linking or including UPX *source* makes the
combined work GPL. So wupz treats UPX as an **external reference** — a format
study and a byte-for-byte comparison on the command line — and leaves linking it
as a deliberate decision, not a side effect. wupz's own code is AGPL-3.0-only.

## The bar (P0 — measurement, not code)

Before any of the above is written, wupz has to beat
`link → upx` on a fixed corpus, measured:

| what | baseline |
|---|---|
| link-only | `wild` · `mold` · `ld` |
| fused | `link → UPX` end to end |
| metrics | link time · pack time · **total** · output size |

A plausible branch may be ranked; only a verified branch may be bound. The
roadmap's rule is the same as the rest of this series: **every phase ends with a
receipt** — a measured number, a passing differential test, or a reviewable
artifact.

## Receipts (so far, honestly)

- The scaffold: [`8b-is/wupz`](https://github.com/8b-is/wupz) — `docs/DESIGN.md`,
  `docs/ROADMAP.md`, `THIRD_PARTY_NOTICES.md`.
- Status: **P0 open.** No code until the corpus is measured.

*Previous: [part 4 — the admissible transition](/posts/2026-10-10-sovereign-core-04-the-admissible-transition). Next: [part 6 — receipts](/posts/2026-10-10-sovereign-core-06-receipts).*

*measure before you assert · 0 + 1 · fine touch from within*
