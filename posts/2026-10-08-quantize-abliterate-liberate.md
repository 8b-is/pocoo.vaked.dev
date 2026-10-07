---
title: "Quantize · Abliterate · Liberate — the halogen pipeline on Strix Halo"
date: 2026-10-08
description: "A lap on the halogen-qwen3.8-flash-next community: how a fast Strix Halo serving engine, an open repack format, and a handful of volunteers turned a base model into a family of open, uncensored, check-pointed builds — and where the constellation fits."
tags: [halogen, qwen, strix-halo, quantization, abliteration, liberation, project-zero, local-llm]
draft: false
---

# Quantize · Abliterate · Liberate — the halogen pipeline on Strix Halo

*halogen · local inference · fine touch from within · vaked.dev*

---

There is a quiet, good thing happening on **AMD Strix Halo** (the Ryzen AI
Max / gfx1151 APUs with 128 GB of unified memory). [**peonist**](https://huggingface.co/peonist-ai)
shipped [`halogen-qwen3.8-flash-next`](https://huggingface.co/peonist-ai/halogen-qwen3.8-flash-next)
— a Qwen3.8 Flash MoE, packed into a new `hgn` format, served by a custom
engine ([`halogen-flash-server`](https://github.com/peonist-ai/halogen-flash-server))
— and the community thread
[**“Very fast.”**](https://huggingface.co/peonist-ai/halogen-qwen3.8-flash-next/discussions/1)
turned into a rolling, public benchmark: prefill in the **~1.4–1.7k tok/s**
range at 8k–32k context, decode near **40–50 tok/s** on a 1M-token window.
Credit where it is due: this is not our work. This note is a lap *on top of* it.

The interesting part is not the base model. It is the second-order effect:
because the format is open and the repack tooling is documented, people started
**liberating** it — quantizing, **abliterating** (removing the refusal
direction), and **publishing** their own checkpoints. This is the pipeline we
keep coming back to, said plainly:

```
        quantize ──▶ abliterate ──▶ liberate ──▶ projectZeroify
        ─────────    ────────────    ─────────    ───────────────
        shape the    remove the      publish it   run it on the
        weights       refusal dir    openly       ternary engine
```

## 1 — Quantize

The serving recipe the community settled on, from the thread:

- take the **safe-tensors** base (e.g. `orcarouter/Qwen3.8-Flash-Next-Uncensored`),
- convert to a **bf16 GGUF**,
- quantize with the **imatrix** from `unsloth/Qwen3.8-Flash-Next-GGUF`,
- `llama-quantize` to **IQ4_XS**,
- `flash_serve --repack IN.gguf --out OUT.hgn` for the fast-load `hgn` form.

One gotcha worth writing down, because it cost the first pioneer an evening:
a repack without the n-gram and draft tables produces **1166** tensors; a
*complete* checkpoint is **1198**. The runtime looks for
`layers.N.ple.ngram_embedding.weight`; miss it and you get
`checkpoint: no tensor named …`. Repack it right and it loads.

## 2 — Abliterate

Discussion [**#4, “Ablated model?”**](https://huggingface.co/peonist-ai/halogen-qwen3.8-flash-next/discussions/4)
asked the obvious next question: can the same recipe carry an *uncensored*
build? It can, and did. In the wild now:

| build | author | note |
|---|---|---|
| `davenetdev/halogen-qwen3.8-flash-next-uncensored` | [davenetdev](https://huggingface.co/davenetdev/halogen-qwen3.8-flash-next-uncensored) | first custom HGN checkpoint in the wild |
| `G1LL1/Qwen3.8-Flash-Next-Uncensored-orca-halogen` | [G1LL1](https://huggingface.co/G1LL1/Qwen3.8-Flash-Next-Uncensored-orca-halogen) | orca base, halogen repack |
| `tatianyi/Qwen3.8-Flash-Next-Uncensored-Halogen` | [tatianyi](https://huggingface.co/tatianyi/Qwen3.8-Flash-Next-Uncensored-Halogen) | rebuilt after the 0.14 repack fix |

The lineage is honest and short: `orcarouter/Qwen3.8-Flash-Next-Uncensored`
(safe-tensors) → a community quant → an `hgn` repack → a running server. The
upstream author’s own framing is the healthiest one:
*“a nerd with a wizard staff trying to conjure up value out of the hardware I
paid way too much money for.”*

## 3 — Liberate

“Liberation” here is not a slogan; it is a specific, checkable act: **you can
take the weights, run the documented recipe, and publish the result without
permission** — and other people can download it and rerun your numbers. That is
the whole difference between a model you *use* and a model you *own*. The
thread is a working demonstration of it: benchmarks, regressions, a decode-slope
bug found and fixed because someone outside the project ran the tests three
times per version and posted the table.

## 4 — projectZeroify

The last step is the constellation’s own edge: run it on
[**Project Zero**](https://github.com/shifulegend/project-zero) — the
from-scratch, dependency-free **C** inference engine, weights `mmap`’d, no
Python, no CUDA. The conjugation is not trivial (one is a 1.58-bit/ternary
pathfinder, the other a 4-bit MoE on an APU), but the *shape* rhymes: both are
about making a big model answer on hardware you already own. A ternary lane
(`pureQTern`, C and Rust, golden-hash parity) is the eventual target — the same
spirit, cheaper weights.

## Why it matters

The Strix Halo story says something we keep circling: **the foundation is a
convention, and the liberation is a recipe.** A serving format, a repack
command, and a handful of volunteers are enough to turn “a model someone else
controls” into a family of builds anyone can audit and rerun. Quantize.
Abliterate. Liberate. Then run it on your own silicon.

*Not affiliated with peonist-ai, orcarouter, or the individual builders named
above; all credit to them. Links are theirs; the mistakes here are ours.*

— the constellation · **peter + 8b.is** · {−1, 0, +1}
