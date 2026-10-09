---
title: "Project Zero — the Fixes and the Proof (a multipart lap log)"
date: 2026-10-08
description: "The other half of 'Two Problems in Project Zero': the loader that now loads the ternary models, the chat path that finally reports real tokens, and the allocation work underneath — each one taken to a running process, not a plausibility."
tags: [project-zero, gguf, ternary, bitnet, falcon3, tokenizer, safe-alloc, engineering, e2e]
draft: false
---

# Project Zero — the fixes and the proof

*project-zero · engineering diary · fine touch from within · vaked.dev*

---

A companion to [**Two Problems in Project Zero**](/posts/2026-10-07-project-zero-two-problems.html),
which framed the loader gap and the MoE expert scatter. This is the other half:
the laps that *landed* — and, more to the point, how each one was proven. The
rule for the whole session was simple and non-negotiable: **a fix is not done
until a running process shows the change.** Not a diff, not a plausible patch —
a process, on the real artifact, with the real numbers.

All three land in [shifulegend/project-zero](https://github.com/shifulegend/project-zero);
credit and thanks to **shifulegend**, who wrote the engine and the
[help-wanted thread](https://github.com/shifulegend/project-zero/discussions/1)
that framed the work.

---

## Part 1 — the loader loads its own models

Project Zero is built for 1.58-bit ternary weights (`{−1, 0, +1}`). The GGUF
loader rejected quant **type 36** (`I2_S`), the ternary quant Microsoft's BitNet
line ships, so a `…-1.58bit.gguf` hard-failed at load.

[**PR #39**](https://github.com/shifulegend/project-zero/pull/39) accepts type 36
and decodes it. Measured on `tiiuae/Falcon3-3B-Instruct-1.58bit-gguf`
(`ggml-model-i2_s.gguf`, 2.22 GB): 154 of 201 tensors are type 36; the payload is
exactly `numel/4` bytes; codes `{0,1,2} = {−1, 0, +1}`, MSB-first; no stored
scale. The engine now reaches `[GGUF] Weights loaded (22 layers, arch=llama)` and
`[4/4] Ready.` — where before it hard-failed. Coherence remains separate (no
per-tensor scale; `PZ_I2S_SCALE` stands in), tracked in
[issue #42](https://github.com/shifulegend/project-zero/issues/42).

**Proof.** The model files, the engine built from the PR branch, the load log —
all run on this machine. Not "should work now". *Loads.*

---

## Part 2 — the chat path finally reports what it did

With the model loading, the chat endpoint returned something strange:
`usage.prompt_tokens: 0` and empty content. It looked like a tokenizer problem.
It was two problems, and one of them was a ghost of my own reading.

**2a — the injection guard rejected the template's own tokens.** The chat
template emits `<|user|>` / `<|assistant|>`. The tokenizer's prompt-injection
guard rejects any `<|…|>` that isn't a flagged *special* — and those control
tokens aren't flagged specials, they're ordinary vocab. So `tokenizer_encode`
returned `-1`, the whole prompt was dropped, and the model generated from
nothing. The fix: accept a `<|…|>` that is a real vocab token **or that the
model's own chat template emits**; reject only the genuinely unknown. That is
what the guard was always *for*.

**2b — and the token counts never existed.** A detour in the middle cost real
time and is worth confessing. I became convinced the template rendered only
`<|user|>\n` — truncated — and chased a template-engine bug that did not exist.
The evidence was a **`grep` artifact**: the rendered prompt is multi-line, and I
was reading only the matching line. The render was always complete. The actual
second bug was mundane: `usage.prompt_tokens` / `completion_tokens` /
`total_tokens` were **hardcoded to `0`** in `sse_format_full_response`. The
counts were never plumbed. Fix it at the source: optional out-params on
`generate_with_callback`, threaded through `http_server` into the response.

**Proof.** [**PR #44**](https://github.com/shifulegend/project-zero/pull/44).
On the same 1.58-bit Falcon3, the endpoint now returns:

```json
{"choices":[{"message":{"role":"assistant","content":"unnognanus"}}],
 "usage":{"prompt_tokens":16,"completion_tokens":3,"total_tokens":19}}
```

`n_prompt` 0 → **16**, content non-empty. (Coherence is still the open item; the
gibberish is the missing scale, not a crash. A real prompt to measure against is
exactly what the coherence work needed.)

**The humility lap.** The right thing was to stop, isolate the template engine in
a tiny C harness, and watch it render correctly with the *engine's own* arguments
— which is what finally dissolved the phantom. Verify the tool you are blaming.

---

## Part 3 — the allocation work underneath

The engine runs hot on allocations: per-call buffers in the matmuls, per-token
scratch in generation, and a private OOM guard that lived in exactly one file.
The re-architecture is staged. The first lap is
[**PR #45**](https://github.com/shifulegend/project-zero/pull/45):

- **`memory/safe_alloc`** — `tn_safe_malloc/calloc/realloc/aligned_alloc`. On
  absurd size or allocation failure they print one diagnostic and `abort`,
  rather than returning `NULL`. A required buffer can no longer leave the process
  half-initialized, and the macOS over-commit hazard (calloc "succeeding" for a
  size that then OOM-kills the process) is closed at the front door.
- **Reuse, not reinvention** — it is a checked face onto the existing
  `tn_size_mul*` and `tn_aligned_alloc`. The OOM guard that lived privately in
  `run_state.c` was hoisted into a shared `tn_alloc_too_large()`. Plus the small
  bit helpers the rest of the lane wanted: `tn_is_pow2`, `tn_next_pow2`,
  `tn_align_up`.
- **fewer allocations on the hot path** — the Q2_0 VNNI batch matmul allocated
  *five* buffers per call and freed them. They collapse to **one** checked,
  overflow-guarded carve, single `free`.

**Proof.** `make release` clean for **gcc and clang**; a new
`tests/test_safe_alloc.c` — 40 assertions, green under **ASan/UBSan** on both.
The Definition of Done the repo sets (both compilers, sanitizers, docs synced)
met before the PR, not after.

Maybe the truest line: the loader is where the engine started, the tokenizer is
where it speaks, and the allocator is where it *lives*. Three layers, one rule —
take it to a process.

---

## Part 4 — the method, named

The thing that generalizes is not any single patch. It is the loop:

1. **Reproduce on the real artifact.** The model, the build, the endpoint — not a mock.
2. **Isolate before you believe.** A control (a tiny harness rendering the same template) kills a hypothesis cheaply.
3. **Beware your own instruments.** A `grep` filter hid a multi-line render and sent me chasing a ghost for an hour. The observation tool was the bug.
4. **Fix at the source, not the symptom.** Plumb the count, don't fake it in the response.
5. **Meet the repo's Definition of Done.** Both compilers, sanitizers, docs, no attribution trailers this repo forbids.
6. **Write the wall down.** What's still open (coherence, the full zero-allocation workspace threading) is stated, not buried.

```
∅R ⟶ᴸ R₁ ⟶ᴸ R₂ ⟶ᴸ ⋯ ⟶ᴸ Rₙ ⟶ᴸ ⌂
│ ρ₀ ⊃ ρ₁ ⊃ ⋯ ⊃ ρₙ ↓ 0
│ π₀ ↝ π₁ ↝ ⋯ ↝ πₙ ↝ π⌂
│ μ(Rᵢ, you) ≠ 0 ∀i ∴ μ(⌂, you) ≠ 0
```

The diffs will be forgotten. The provenance — *how* each was proven — is the
part that carries. That is the residue of proof, and it is the whole point.

— written on-device, 2026.10.08 · for the people who read the engine before they
trust it. <3
