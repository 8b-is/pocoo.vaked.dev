---
title: "wupz — the link kompresses, and it runs"
date: 2026-10-10
description: "wupz went from a design doc to working code on two toolchains in one day: a Rust layout plan and incremental rebuild rule, Zig SIMD kernels with scalar references, and a frozen C ABI that a C program now proves by linking both static libraries and checking they agree."
tags: [engineering, rust, zig, wupz, linker, compression, simd, zero-alloc, sovereign-core]
draft: false
---

# wupz — the link kompresses, and it runs

*The design was [part 5](/posts/2026-10-10-sovereign-core-05-kompress-the-link) of the Sovereign Core series. This is the part where it executes.*

---

Yesterday wupz was a thesis: *a linker already knows the layout, so let it pack
while it links*. Today it is two static libraries, a C header, and a test that
fails if either side drifts.

## what actually runs

```bash
scripts/ci.sh
#   rust core (plan · incremental · arena · pack-image)   20 tests ok
#   zig kernels (differential: vectorized vs scalar)       5 tests ok
#   static libs + C ABI parity test                        abi 1 ok (header == rust == zig)
```

### Rust — the model (`wupz-rs/`)

- **`plan.rs`** — `LayoutPlan` / `Section` / `Block`, the address-independent
  `window_of(addr)`, and a deterministic `digest()`.
- **`incremental.rs`** — the rebuild rule: `changed_sections` ·
  `blocks_to_repack` · `windows_touched` · `reuse_ratio`. Given two plans it
  answers *what is the minimum work*, and that is testable without a linker.
- **`arena.rs`** — a bump arena plus a `Seal` that is read-only by construction.
- **`pack.rs`** — the deterministic **plan image** (`"WUPZ"`, v1) written into
  the arena. It refuses to grow; a silent grow would be an allocation.

### Zig — the kernels (`wupz-zig/src/kernels.zig`)

`xorFold` · `byteDiff` · `popcount`, each next to a **scalar reference** and a
**seeded differential test** that walks every length from 0 to 1088 and asserts
vectorized == scalar. No kernel is trusted without parity.

### The seam (`include/wupz_abi.h`)

One versioned header. The C smoke test now builds **both** static libraries —
the Rust core and the Zig kernels — links them, and asserts:

```c
const uint32_t hdr  = WUPZ_ABI_VERSION;
const uint32_t rust = wupz_abi_version();      // the Rust core
const uint32_t zig  = wupz_zig_abi_version();  // the Zig kernels
if (hdr != rust || hdr != zig) { /* fail */ }
```

*The ABI is proven, not described.* If either toolchain drifts, the build
breaks — which is the entire point of freezing a boundary.

## the invariant, enforced

`wupz-rs/tests/no_alloc.rs` installs a **counting global allocator**. It builds
a plan, sizes an arena once, and then asserts the allocation count does not move
across `pack_into`. "This path doesn't allocate" is a test assertion now, not a
comment:

```
test pack_after_arena_seal_allocates_nothing ... ok
```

## the field

There is a landing page: **[wupz.vaked.dev](https://wupz.vaked.dev)** — a
self-contained canvas: a Tokyo horizon converging on your pointer, Zeno's halo,
flow particles you can push, click-witnesses, and a live **QuantTern** widget
(three axes → trits → `qt:<hex>`). No build step, no dependencies, nothing
fetched. `prefers-reduced-motion` renders one static frame and stops.

## honest status

| phase | state |
|---|---|
| P1 plan artifact | **partial** — plan, image, digest landed; the ELF reader is not written |
| P2 zig kernels | **partial** — fold/diff/popcount landed; hash/bit-pack/crc open |
| P4 incremental | **partial** — the rebuild rule landed; not wired to a linker |
| P0 measure | **open** — the corpus baseline comes first |
| P3 pack-in-pass | **open** — the real compressor |

The order is deliberate: **measure before you assert.** P0 sets the bar
(`wild`/`mold`/`ld`, and `link → upx`) before P3 writes a compressor, so the
fused pass has something honest to beat.

## links

- repo — <https://github.com/8b-is/wupz>
- design — [`docs/DESIGN.md`](https://github.com/8b-is/wupz/blob/main/docs/DESIGN.md)
- roadmap — [`docs/ROADMAP.md`](https://github.com/8b-is/wupz/blob/main/docs/ROADMAP.md)
- the field — <https://wupz.vaked.dev>

*prove it, don't assert it · 0 + 1 · fine touch from within*
