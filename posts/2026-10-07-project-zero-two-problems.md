---
title: "Two Problems in Project Zero: the Expert Scatter and the 1.58-Bit Loader"
date: 2026-10-07
description: "An engineering note on two open problems in shifulegend's Project Zero — the MoE expert-weight scatter that makes DeepSeek ~13× slower than llama.cpp, and the BitNet I2_S loader that couldn't load the ternary models the engine was built for."
tags: [project-zero, moe, gguf, ternary, bitnet, deepseek, engineering]
draft: false
---

# Two problems in Project Zero: the expert scatter and the 1.58-bit loader

*project-zero · engineering diary · fine touch from within · vaked.dev*

---

[Project Zero](https://github.com/shifulegend/project-zero) is a from-scratch,
dependency-free **C** inference engine for large language models on commodity
CPUs — no Python, no CUDA, one binary, weights `mmap`'d. It is fast where it
is dense (it beats `bitnet.cpp` by ~1.8× on BitNet b1.58-2B-4T, near the DRAM
bandwidth ceiling) and it is honest about where it is slow. This note is a lap
on two of its open problems. Credit and thanks to
[**shifulegend**](https://github.com/shifulegend), who wrote the engine and the
[help-wanted thread](https://github.com/shifulegend/project-zero/discussions/1)
that framed both.

## Problem 1 — the loader couldn't load its own models ([issue #41](https://github.com/shifulegend/project-zero/issues/41))

Project Zero is built for 1.58-bit ternary weights (`{−1, 0, +1}`). But the
GGUF loader rejected quant **type 36** (`I2_S`) — the ternary quant on
Microsoft's BitNet line — so a `…-1.58bit.gguf` hard-failed at load with
`unsupported quant type 36`.

The fix is small: accept type 36 and decode it. What the file actually holds,
measured on `tiiuae/Falcon3-3B-Instruct-1.58bit-gguf` (`ggml-model-i2_s.gguf`,
2.22 GB):

- **154 of 201 tensors** are type 36; the payload is exactly `numel/4` bytes
  (0.250002 B/elem — 2 bits per weight), offsets contiguous.
- codes `{0,1,2} = {−1, 0, +1}`, MSB-first; code `3` never appears.
- **no stored scale** — there is no `*.scale` tensor and nothing in the
  metadata. With no scale the weights decode to *unit* ternary, so `I2_S` now
  loads and reaches `[4/4] Ready.` (22 layers, 131072 vocab) — where before it
  hard-failed. Coherence is a separate problem: the per-block scale source is
  [issue #42](https://github.com/shifulegend/project-zero/issues/42), and a
  `PZ_I2S_SCALE` env override stands in for now.

This is the `{−1, 0, +1}` territory the whole project lives in: get the codes
right, and the scale is the only knob left.

## Problem 2 — the MoE expert scatter (13× behind llama.cpp)

The harder one. DeepSeek-V2-Lite is a Mixture-of-Experts model: **64 experts
per layer, 26 MoE layers, 6 experts active per token**. The engine ran it at
**~1.3 tok/s** where `llama.cpp` runs **~20 tok/s** at four threads. The
profiler says it is not compute-bound: IPC ≈ 1.0, **L3 miss 85–86%** — the CPU
is waiting on RAM.

The reason is layout. The experts are stored sequentially in the 8.9 GB GGUF,
so the six active experts for a token are scattered across the file's address
space:

```
per-token scattered reads = 6 experts × 26 MoE layers = 156
concurrently live streams = 6 experts × 4 threads      =  24   (prefetcher: ~8–10)
→ prefetcher overwhelmed → effective BW 11.7 GB/s → 2–3 GB/s
```

The obvious fix — repack the experts at load time so the top-k are contiguous
— is blocked by memory: a full copy of the expert tensors needs **6+ GB of
extra heap**, which OOMs an 8 GB machine. So the design is built around that
constraint
([`docs/architecture/MOE_EXPERT_REPACK_DESIGN.md`](https://github.com/shifulegend/project-zero/pull/39/files)):

- **repack offline** into a `*.pzrepack` side-car, `mmap`'d read-only — **zero
  extra runtime heap**; the original GGUF stays usable (`--model orig.gguf`);
- **granularity = whole Q4_K super-blocks**, interleaved within row-major
  expert blocks (a super-block carries its own fp16 scale — never split it; not
  per-element, not whole-expert);
- `madvise`/huge-pages as supplements, not the fix;
- the llama.cpp principle from the project's own golden rules: **dispatch at
  compute time, never dequantize upfront**.

**Acceptance targets:** L3 miss **< 60%** (from 85–86%), effective BW
**≥ 6 GB/s**, **≥ 9 tok/s**, all **27 layers active** — measured as a
same-host A/B, since absolute tok/s is not portable across CPUs.

## the end-to-end

`make release` is clean here (clang, macOS arm64) and the suite passes
(`test_chat_template` 24/24; the single kill is the project's own OOM-guard
test tripping macOS over-commit, tracked in
[#43](https://github.com/shifulegend/project-zero/issues/43)). Both changes —
the `I2_S` loader and the repack design — live in one PR:
[**shifulegend/project-zero #39**](https://github.com/shifulegend/project-zero/pull/39).

None of this is our engine. It is shifulegend's, and the interesting part is
that a C engine written from scratch, with a `{−1, 0, +1}` core and a
one-scale-at-the-end arithmetic contract, converges on exactly the problems the
ternary lane solves elsewhere — only here they are memory-shaped, and the fight
is against the prefetcher.

*fine touch from within · 0 + 1 · vaked.dev*
