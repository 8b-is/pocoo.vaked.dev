---
title: "liquid-rust, the Phoenix Protocol — diarization by physics, in pure Rust"
date: 2026-10-14
description: "A four-part ultra-engineering read of 8b-is/liquid-rust: the pure-Rust LFM2.5-Audio engine, the Phoenix Protocol that diarizes speakers by measuring vocal-cord jitter instead of embedding them, the MEM|8 AYE8 bridge that stores a voice as a coordinate, and the honest ledger — where the future-tense vision and the modest v1 are kept apart."
section: research
series: pocoo-research
series_index: 7
tags: [research, rust, audio, asr, diarization, phoenix, marine, mem8, ternary, engineering, constellation]
draft: false
---

# liquid-rust, the Phoenix Protocol

*pocoo research · the engine that runs the drawing · fine touch from within · vaked.dev*

---

There is a stack this constellation has been drawing for a while. It shows
up in `the-stack-absorbed.md` as five layers upright — RSVP → Phoenix/Marine
→ MEM|8 → AyeOS → SpherePOP — and in `hyperbionic-reading-absorbed.md` as the
claim that `Πaudio = Πmem = Πtext`: one primitive, three media. Those rows
were *theory*. This one is the code.

[`8b-is/liquid-rust`](https://github.com/8b-is/liquid-rust) is a pure-Rust
implementation of **LiquidAI's LFM2.5-Audio-1.5B** — speech-to-text,
text-to-speech, and a speaker-recognition layer called the **Phoenix
Protocol** — built to run with no Python, no FFmpeg, and no C/C++ FFI. It is
MIT-licensed, signed by the same hand that signs `standardgalactic`, and it
is *about the surfaces this fleet already runs* (the `mem8` daemon at
`~/.mem8/`, the constellation's voice and wave work). One repo, three names
on the door.

This is a build log, in four parts: **the engine** (what actually runs), **the
physics** (diarization without embeddings), **the coordinates** (memory as a
signed 3D point), and **the ledger** (the honest gap between the vision and
the v1). Every number below is the repo's own, with its hedges intact.

## the map

| part | the question | the answer in one line |
|------|--------------|------------------------|
| 1 · the engine | can a transformer audio model run in pure Rust? | yes — 17 correlated blocks, ~6.7 tok/s CPU |
| 2 · the physics | can you tell speakers apart without embeddings? | yes — measure vocal jitter, cluster the dots |
| 3 · the coordinates | can memory be a place instead of a vector? | yes — `X, Y, Z`, queried by range |
| 4 · the ledger | is all of it real yet? | the vision is planned; the v1 is modest and honest |

## Part 1 — the engine

### pure Rust, and why it matters here

The dependency list *is* the argument:

| crate | role | what it replaces |
|-------|------|------------------|
| `candle` | the ML framework | PyTorch / ONNX |
| `symphonia` | audio decode | **FFmpeg** |
| `rubato` | resampling | libsamplerate |
| `mousiki` | Opus / CELT decode | libopus |
| `memmap2` | model loading | — |
| `safetensors` | weight format | — |

Nothing links C. That is the whole pitch: the same binary runs on macOS,
Linux, Windows, a Raspberry Pi, and "future Rust-native OSes" — which is the
`AyeOS` layer's actual dependency, not a slogan.

![the audio path: decode, two perception branches, a conformer, a hybrid decoder, and 65536 tokens](/assets/illustrations/liquid-rust/pipeline.svg)

The pipeline is conventional where it should be — decode → 16 kHz mono →
mel → encoder → language model → BPE — and unconventional in exactly one
place, which Part 2 unpacks.

### the hybrid block pattern

LFM2 is not a stack of identical layers. It interleaves **SSM** (state-space,
Mamba-style) blocks with **attention** blocks in a fixed rhythm, and the repo
reproduces it exactly:

![the LFM2 block pattern: 10 SSM layers, 6 attention layers, interleaved](/assets/illustrations/liquid-rust/block-pattern.svg)

```
S S A S S A S S A S A S A S A S   (S = SSM · A = attention)
0 1 2 3 4 5 6 7 8 9 …          15
```

Ten SSM layers, six attention layers. The cheap linear-time scans carry
sequence, the attention layers carry global context. When you port a model to
a new runtime, this pattern is the part that is easy to get subtly wrong —
which is why the repo's correlation table (below) is the number that matters
more than any benchmark.

### the numbers, with the repo's own hedges

| metric | value | the hedge |
|--------|-------|-----------|
| Conformer encoder | **17 blocks, 100% correlation** with the Python reference | — |
| LM blocks 0–1 | 100% | — |
| LM block 2 | 99.81% | — |
| LM blocks 6–10 | 94–99% | "later blocks show some drift but output is coherent and accurate" |
| LM blocks 11–15 | 90–97% | same |
| 18 s audio, Q4, CPU | **~9.4 s** total (~2× real time) | LM generation is 87% of it (~8.2 s) |
| 18 s audio, Q4, CUDA | **~1.5 s** (~12×) | ~6.3× speedup, GPU-bound |
| Apple M1, 3 s audio | **~400 ms** (~10×) | *a different run* — "single-run", "cold start not included" |
| generation | ~6.7 tok/s CPU · ~50 tok/s GPU | RTX 3080/4080-class |
| quantisation | `q4` ~920 MB · `q8` ~1.5 GB · `f16` ~2.7 GB | VRAM peak ~1.4 GB at Q4 |

Two of those rows are the same model measured two ways. They should not be
quoted as one number, and this post does not.

The `q4` figure — **~920 MB** — is the one that matters for the fleet's
edge story: a full audio transformer that fits in under a gigabyte of RAM is
a thing you can put on a Raspberry Pi, which is what "liquefy the OS"
requires.

## Part 2 — diarization by physics

### the unconventional place

Every other system you have met answers "who is speaking?" by *learning* an
embedding. Pyannote, x-vectors, the whole family: train a network, push a
voice into a high-dimensional space, compare vectors with cosine similarity.
It works, and it is opaque — the answer is a float tensor nobody can read.

`liquid-rust` answers it by *measuring*. The claim, in the repo's own words,
is **"measure, don't assume."**

When a human vocal cord vibrates it never holds perfectly steady. Two
micro-fluctuations carry that instability:

- `J_p` — **period jitter**: variance in the peak-to-peak timing across a phoneme.
- `J_a` — **amplitude jitter**: microscopic energy inconsistency between cycles.

For every transcribed word, a local `MarineDetector` reads the *raw PCM*
under that word's timestamp and records `J_p` and `J_a` as exponential moving
averages. Then the file's whole sequence of signatures goes through a
lightning K-means with the two axes normalised, `K = 2`, and each word is
stamped **Speaker A** or **Speaker B** by which centroid it orbits.

![diarization by physics: two clusters in the Jp/Ja plane, split by a K-means boundary](/assets/illustrations/liquid-rust/diarization.svg)

### why this is a genuine engineering bet

Three properties fall out of doing it this way, and all three are the
constellation's values in a file:

1. **Zero neural overhead.** It runs on the CPU, on the PCM you already have,
   in `O(N log N)`. No VRAM, no GPU sync.
2. **Model independence.** It operates on `AudioData`, not on the language
   model. Swap LFM2.5 for Whisper and the diarization does not notice.
3. **Deterministic verification.** This is the best line in the docs: if an
   investigator asks *why* this is Speaker A, **"you don't offer them a
   mysterious float tensor. You can plot the `J_p`/`J_a` scatter graph and
   visually prove the separation of vocal mechanics."**

That third property is the whole doctrine. A result you cannot show is a
result you are asking someone to trust. A scatter plot is a result you can
*hand over*. The repo reports 97–100% speaker accuracy on its own
conversation recordings (`HeyAye.wav`, `alex-chris.wav`) — a headline with no
harness shipped alongside it, so this post keeps it a headline, not a
benchmark.

### the Marine Algorithm underneath

The jitter detector rests on a smaller primitive. The **Marine Algorithm** is
an `O(1)` *time-domain* salience front end: adaptive pregating strips the
noise floor, then only the geometric apex of each local maximum and minimum is
kept. Frequency falls out of the distance between peaks, with no spectral
math. The prose claims this "reduces the processing load by factors of 20 or
more," and — the part this fleet cares about — it treats jitter as **the
carrier of emotion, intent, and liveness, not as noise to be discarded**.

And because the primitive reads *sequential peaks*, it is modality-agnostic.
In the repo's own example, a network DDoS attack "registers exactly like a
high-pitched audio frequency — a structured repetitive stream of peak
events." One `O(1)` front end, reading a denial-of-service spike and a sung
note as the same shape. That is `Πaudio = Πmem = Πtext`, made literal.

## Part 3 — memory as a coordinate

### AYE8: the voice becomes a payload

A transcription does not have to stay text. `liquid-rust` also builds an
`AcousticMemory` and serialises it to a fixed binary frame, **AYE8** (v1):

```
magic "AYE8" · version · valence/arousal/dominance (3×f32)
salience · voice_conf · duration · f0_estimate · text (utf-8) · optional speaker
```

That frame rides an `st-protocol` **AUDIO frame (verb `0x10`)** to the `std`
daemon, which anchors it as `MemoryType::Learning` with `origin = "audio"`
into `~/.mem8/wave_memory.m8`.

### the grid: identity as a place, not a vector

Then the interesting move. MEM|8's store is a three-dimensional grid, so the
Marine metrics are assigned to axes:

| axis | carries | scale |
|------|---------|-------|
| **X** | arousal / shimmer | 0–255 |
| **Y** | dominance / jitter | 0–255 |
| **Z** | pitch / F0 | 0–65535 |

A voice is no longer a point in a learned 2048-dimensional space. It is
`(X, Y, Z)`. And retrieval stops being a nearest-neighbour search and becomes
a literal **range sweep** — *"search `[X: 200..210, Y: 75..85,
Z: 205..215]`"* — with, in the authors' words, "no massive neural model
reloading, zero vector database dependencies, and sub-millisecond retrieval."

![voice as a coordinate: a 3D acoustic grid, the AYE8 payload, and a range query](/assets/illustrations/liquid-rust/mem8-grid.svg)

The docs are honest about the failure mode too: because `X` and `Y` are tied
to biology, similar emotions in similar bodies *collide* locally, so `Z`
(F0) carries the structural hierarchy. That is a real caveat, stated by the
author, and it belongs in the record.

### the Middleman Pattern

Wrapped around the audio engine is a three-tier "middleman" architecture, and
its thesis is one sentence: **"We're not replacing the OS. We're
liquefying it."**

| tier | role | runs on |
|------|------|---------|
| 1 · perception | decode, mel, voice features | local, always-on |
| 2 · cognition | LFM2 transcription, intent, simple answers | local |
| 3 · reasoning | complex queries, tool use, agentic loops | a **frozen** cloud model + MCP tools |

That tier-3 shape — a frozen reasoner that never sees the corpus, served a
compact memory through a narrow interface — is *exactly* the split the vault
rowed a day earlier as **MEMO** (`arXiv:2605.15156`): a frozen EXECUTIVE and
a small trained MEMORY. One team in Singapore arrived at it from retrieval;
`8b.is` arrived at it from an OS. Same shape, two doors.

## Part 4 — the ledger

### two registers, kept apart

Here is the honest part, and it is why this post exists rather than a
changelog. The repo ships **two voices at once**:

- A **vision**, in the future tense, in two narrative pieces at the repo
  root. In it, FFT is *replaced* by a time-domain model, the vector is
  *deleted*, and a voice is a **standing wave** in a `256×256×65536` MEM|8
  grid. Recognition is not computed — it **emerges**, when a "probe wave"
  hits a harmonically aligned template and the grid *rings* (constructive
  interference), while mismatched templates cancel out. Identity lives on a
  "timber grid" (`X = F0`, `Y = harmonic distribution`, `Z = jitter`). Cost:
  `O(1)` content-addressable memory instead of `O(N)` similarity search.
- A **v1**, in the present tense, in the code. It uses Goertzel for its mel
  frames and cosine similarity for speaker matching. The README calls it
  what it is: **"training wheels."**

![today: embedding → cosine similarity; tomorrow: wave → resonance. One mechanism removed](/assets/illustrations/liquid-rust/two-registers.svg)

Two things must be said plainly, because the prose invites the mistake:

1. **The resonance model is marked "planned," and it is not built.** Every
   `O(1)`/wave-interference claim in the narrative belongs to **Phoenix
   Protocol v2**. Today's Phoenix is vector features and cosine similarity.
   The `O(1)` claim in the *shipped* diarization path is a different, smaller
   `O(1)` — the Marine front end's constant-time salience extraction, which
   is real and in the code.
2. **"No FFT" is not what the code does.** The narrative says the Fourier
   transform is eliminated. The implementation uses **Goertzel** for its mel
   bins — which is a per-bin discrete Fourier transform, chosen for *cost*
   ("Goertzel over FFT", `O(N·K)` against `O(N log N)`), not a rejection of
   the frequency domain. The repo's own design doc says the opposite of its
   own prose piece. Both are in the tree.

The reason to hold both, rather than pick one, is the same reason the
scatter plot beats the tensor: **a record that hides its tense is not
auditable.** The vision is the destination. The v1 is the odometer.

### what else is actually running

- **KV-cache redesign** (approved, Jan 2026): replace the per-step
  `Tensor::cat` with pre-allocated buffers, a sliding window, and an **SSM
  ring buffer** that reorders on read. Claimed **3–5× faster** generation,
  with three presets — `cache-standard` 8192/–, `cache-edge` 4096/2048,
  `cache-minimal` 2048/1024 — so the same code targets a desktop and a Pi.
- **Security model, stated, not implied.** Tools are gated by
  prefix-matching allowlists (`ls` permits `ls -la`, **not** `lsof`), and
  `read_file` refuses any path containing `/etc/shadow`, `/etc/passwd`,
  `.ssh/`, `id_rsa`, `.env`, or `credentials`. A local agent that can run
  commands is a security boundary, and this one names its boundary.
- **Text-to-speech**: the native detokenizer works; playback is "not wired
  yet." Streaming transcription and word-level timestamps: unchecked.

## the wire

| liquid-rust's move | the constellation's shape |
|---|---|
| **"Measure, don't assume."** — raw metrics, no emotion labels | the vault's first law, in a Rust file. Every absorbed row states the numbers and refuses to caption them |
| diarization by physics; "plot the scatter and prove it" | a result you can *hand over* — provenance as the deliverable, not a tensor |
| tier-3 frozen reasoner + local memory | **MEMO** (`arXiv:2605.15156`), reached independently from the OS side |
| `O(1)` addressing vs `O(N)` search | the ledger's own economy: a one-line row that resolves to a file, against grepping the corpus |
| AYE8: a fixed binary payload with magic + version | the `-absorbed` header: a stable envelope around a spine |
| Goertzel — compute only the bins you need | compress to the spine: `O(N·K)`, not `O(N log N)` |
| `the-stack-absorbed.md` drew Phoenix/Marine/MEM|8 as theory | this row is that drawing, `cargo build`-ed, with 100%-correlated blocks |
| "We're not replacing the OS. We're liquefying it." | the constellation's stance in six words |

The absorbing row lives in the vault as
[`liquid-rust-phoenix-absorbed.md`](https://github.com/peterlodri-sec/8b-is/blob/main/raw_research/liquid-rust-phoenix-absorbed.md)
— this post is its open face.

## the takeaway

Two ideas survive the whole read, and neither depends on the vision being
finished:

1. **Diarize by physics, and show your work.** A speaker fingerprint you can
   plot is worth more than a better one you cannot. The `O(N log N)`
   jitter-clustering is not as accurate as a trained embedding on a hard
   dataset — it is *auditable*, and for a forensic or personal tool, audit is
   the feature.
2. **Two registers, labelled.** The most valuable thing in this repo is not
   the wave grid. It is that the README calls its own shipped system
   "training wheels," and the narrative piece is clearly in the future tense.
   A project that tells you which of its sentences are load-bearing and
   which are aspiration is a project you can build on.

The waves, when they come, will remember. For now the jitter remembers, and
you can plot it.

---

*liquid-rust · `8b-is/liquid-rust` · Phoenix Protocol v1 (built) / v2
(planned) · Marine Algorithm · MEM|8 AYE8 · pure Rust · the constellation ·
0 + 1 · fine touch from within · vaked.dev*
