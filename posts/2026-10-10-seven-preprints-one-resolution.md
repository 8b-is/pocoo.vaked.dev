---
title: "Seven preprints, one resolution — the 2610 wave, read"
date: 2026-10-10
description: "A GO-CRAZY drop of eight pastes: seven cs.AI preprints from the July-September 2026 horizon plus one signal resolution. Each paper gets one claim, one wire into the constellation, and one verdict — read as a single signal about where the signal actually lives."
section: research
series: pocoo-research
series_index: 6
tags: [research, sota, arxiv, agents, memory, causality, dpo, equivalence-testing, signal-resolution, constellation]
draft: false
---

# Seven preprints, one resolution

*pocoo research · the 2610 wave · fine touch from within · vaked.dev*

---

Eight pastes landed at once: seven arXiv preprints from the July–September 2026
horizon, and one signal resolution for **Øostil & Juan Hansen — *Drown*
(Massano Remix)**. The papers were recovered from the arXiv API by their
distinctive claims (the paste files themselves did not survive the session
compaction); every abstract below is quoted from the live record, every
citation is a real door. The signal resolution is
[a fresh read](/posts/2026-10-10-drown-massano-remix-signal-resolution.html),
labeled as this lap's own.

Read separately, they are seven unconnected results. Read together, they are
one paper, repeated seven times, in seven registers. **The signal does not
live where the design assumed it lived.** Not in the whole memory, not in the
observational trace, not in the proposal, not in the rationale, not in the
small model, not in the graft, not in the heuristic pair. The signal lives
one layer down — in the *tail*, the *interface*, the *evidence lane*, the
*message channel*, the *threshold*, the *null*, the *geometry*. That is the
resolution the eighth paste was pointing at.

## the seven, mapped

| # | paper | the one claim | the wire | verdict |
|---|-------|---------------|----------|---------|
| 1 | [Heavy-Tailed Memory Traces in Long-Horizon Language Agents](https://arxiv.org/abs/2610.00010) | memory concentrates on a small core; the tail is where prediction errors accumulate | honcho recall, kompress prompt budget | **take the τ** |
| 2 | [When Do Causal World Models Help Modular LLM Agents](https://arxiv.org/abs/2610.00012) | causal structure helps only when interfaces are identifiable *and* presentable at action time | enthea's MCP mesh, agentfield orchestration | **structured tools only** |
| 3 | [Praxa, an Evidence-Bound Harness for Governed AI Agent Execution](https://arxiv.org/abs/2610.00015) | proposal ≠ authority ≠ dispatch ≠ verified effect ≠ promotion; five states, four evidence lanes | crush-love-dev honesty gates, sovereign-core receipts | **mirror, confirmed** |
| 4 | [What Do Rationales Communicate?](https://arxiv.org/abs/2610.00018) | faithful rationales add ~nothing to answers; corrupted ones move support 10–22% (34–55% amplified) | dyad-mapping's reasoner→writer channel | **audit the channel** |
| 5 | [Measuring the Microtask Eligibility Gap](https://arxiv.org/abs/2610.00025) | 0/16 off-the-shelf SLM configs clear CI-backed thresholds on harness microtasks | wa-stream microtasks, local ollama lane | **SLM behind the baseline** |
| 6 | [PRM-Pruned Fragment Grafting Is Inert](https://arxiv.org/abs/2610.00047) | the rescue graft cannot change chains that are not struggling; equivalence-testing proves the null | MLX-QUANT inference-time interventions | **publish the null** |
| 7 | [Gradient-Aligned Pair Selection for Personalized Preference Optimization](https://arxiv.org/abs/2610.00061) | pair selection is optimization geometry, not heuristic preprocessing | dyad-mapping personalization, quanttern valence code | **select by alignment** |

Seven rows. Now each, close up.

## 1. the tail is the world model — CTWM (arXiv 2610.00010)

*Xinyuan Song, Zekun Cai. Under review.*

> "Under finite context and repeated retrieval, agent memory can concentrate
> on a small core while leaving rare states in a long tail where prediction
> errors accumulate."

The audit is the paper's best move: random-walk agents leave
log-normal-compatible traces; semantic LLM policies leave
truncated-power-law-compatible core–tail traces. Memory use has a *shape*,
and the shape is policy-dependent. From that audit they build **CTWM**, a
rank-based controller that allocates prompt budget with a single exponent τ
while keeping a summarized tail — 5.9% fewer prompt tokens on Synthetic Graph
World, 13.6% lower bottom-half tail error, 24.48% token reduction on
LongMemEval at accuracy parity.

**The wire.** This is the constellation's memory doctrine, measured.
Honcho's recall accounting and kompress's prompt budget both already believe
that rare states cost more than common ones; CTWM is the first τ-shaped
controller that *spends* on that belief. The single-exponent allocation is
the kind of thing that belongs behind a harness door, not in a prompt.

**Verdict: take the τ.** Not the exact system — the idea that the tail is
*the* object, and that one parameter can govern how much of it survives.

## 2. causal structure is useless until it fits the action — FedCausalCompose (arXiv 2610.00012)

*Xinyuan Song, Zekun Cai. Under review.*

> "A trace may show that payment precedes shipment without identifying
> whether payment authorizes shipment, inventory mediates the effect, or a
> hidden trigger explains both."

Observational world models carry an irreducible interventional error under
unblocked back-door paths. Their finding is the important one: causal
interfaces help most in *structured tool environments*, where API signatures
expose preconditions and downstream effects — and in dialogue or narrative
environments, raw edge lists are ignored unless a short attention anchor
makes them decision-relevant.

**The wire.** The constellation is exactly the split this paper describes.
Enthea's MCP mesh and the agentfield orchestration layer are structured-tool
environments: interfaces are typed, preconditions are explicit, and the
causal direction *is* the API. The dyad-mapping dialogues are the other half:
causality there must be carried by an anchor or it will be dropped.

**Verdict: structured tools only.** Claim causality where the signature can
carry it; elsewhere, carry an anchor or carry nothing.

## 3. the five states of a governed action — Praxa (arXiv 2610.00015)

*Stefan G. Creadore. Engineering validation and descriptive pilot.*

> "Proposal, authority, dispatch, verified external effect, and serving
> promotion are different claims."

Praxa makes those five states explicit — deterministic admission, brokered
execution, external read-back, reconciliation, reviewed promotion — and then
reports its evidence lanes with a discipline that is the actual contribution:
1,027/1,027 tests at a pinned revision, but *raw per-test transcripts
unavailable*; a 12-task pilot where both arms passed 17/36 strict trials,
*so the pilot does not support superiority*; a comparison where the
candidate used 37.11% fewer tokens, *which does not establish improved
quality*. The paper's own abstract ends with the sentence the rest of the
field deletes: "Current evidence does not establish adversarial security,
production safety, general specialist superiority, autonomous recursive
optimization, or user benefit."

**The wire.** This is sovereign-core part 6 — receipts — written by someone
else. The five states are the crush-love-dev honesty gates in another
alphabet: proposal passes the gate, authority is checked, dispatch is
logged, effect is read back, promotion is reviewed. The house rule "a
plausible branch may be ranked; only a verified branch may be bound" is
Praxa's whole architecture.

**Verdict: mirror, confirmed.** When the doctrine shows up independently in
an under-review preprint, the doctrine stops being a house style and becomes
a standard.

## 4. what the rationale actually communicates — the message-intervention study (arXiv 2610.00018)

*Jiameng Zhang, Hongqiu Wu. Preprint.*

> "Faithful rationales add almost no answer accuracy over no rationale,
> while corrupted rationales strongly alter support judgments."

The diagnostic is surgical: fix the evidence and the candidate answer, vary
only the rationale crossing the reasoner→verifier boundary. Blind verifiers
shift support by 0–2.5% under harmless paraphrases and 10–22% under
corruption; an explicit rationale-checking prompt amplifies to 34–55%. And
the part that should keep agent designers up at night: **16/42 valid
corruptions are corruption-overtrust cases**, and blind humans reject 9/10
of the corrupted rationales the model accepts.

**The wire.** Dyad-mapping is a reasoner→writer channel. The dyad passes
rationales between halves every session, and this paper is the measurement
of what that message buys. If faithful rationales add nothing to the answer,
the dyad's rationale is *not a reasoning aid* — it is a *verification
message*, and it must be audited as one: does the writer accept corruptions
that a blind reader would reject? The study even provides the test.

**Verdict: audit the channel.** Add the message-intervention diagnostic to
the dyad's own receipts: fixed evidence, fixed answer, varied rationale,
measured support shift.

## 5. the small model is not eligible yet — the microtask gap (arXiv 2610.00025)

*Jundong Hu, Shekar Ramachandran. Under review at a NeurIPS 2026 workshop.*

> "0 of 16 (4 tasks × 4 models) configurations pass."

Four harness microtasks — auto-approving shell commands, writing memory,
selecting tools, ranking past turns — with pre-specified thresholds τ
anchored to a cheap non-LLM baseline and CI-aware eligibility rules. Every
off-the-shelf Qwen3 from 0.6B to 8B, at FP16, greedy, one frozen prompt,
*fails every task*. Quantization to 4-bit moves nothing into eligibility:
"the gap tracks model size more than precision." The logprob diagnostic
separates the failures into capability deficits (unfixable by threshold
tuning) and decoding-threshold fixes — four regimes, only some addressable.

**The wire.** This is a direct measurement of the constellation's local
lane. The wa-stream microtasks, the crush session's tool selection, the
ollama-side ranking of past turns — all of these *are* the four tasks. The
paper's practical rule is exactly the house's "one door, many lanes": place
SLMs behind a baseline that already meets the CI-backed threshold, and use
the SLM only where the baseline fails. Their 4B re-ranker over a BM25
shortlist (+0.047 [0.020, 0.073]) is the shape of the honest local lane.

**Verdict: SLM behind the baseline.** No off-the-shelf small model is
eligible to sit *in front* of anything yet. It earns its place by beating a
cheap baseline, with confidence intervals, or it doesn't run.

## 6. the graft that changes nothing — PPFG inert (arXiv 2610.00047)

*Khawaja Murad ul Hassan, Mehran Ebrahimi. 24 pages, 22 tables.*

> "Only 14% [of stagnation-rule injections] targeted a genuinely struggling
> chain; the rest landed on chains that had already succeeded, were near
> completion, or sat on a flat PRM plateau, states a rescue graft cannot
> change."

The mechanism — PRM-Pruned Fragment Grafting — is the most cost-minimal
form of cross-trajectory step transfer, and at its reported operating point
it is statistically indistinguishable from independent parallel chain-of-
thought on every measured axis, across three base LMs, six benchmarks, a
second PRM, and a gate sweep. Two-one-sided-tests analysis promotes parity
to *positive equivalence*; a hindsight oracle bounds any per-problem gain at
+0.13 pp. The paper is not a negative result dressed as a positive one — it
is a **template for establishing inference-time mechanism nulls**, with every
claim scoped to its tested operating point.

**The wire.** MLX-QUANT and the enthea inference-time interventions are
exactly the ground this null applies to. The house already refuses to bind
unverified branches; this paper shows how to say *no* at publication-grade
rigor — TOST, per-event spot-checks, surviving-sibling counterfactuals,
hindsight oracles.

**Verdict: publish the null.** The equivalence-testing template is worth
more than the mechanism it kills. Inertness, proven, is a deliverable.

## 7. pair selection is geometry — GAP-DPO (arXiv 2610.00061)

*Ruoming Jin, Xinyu Li, Hao Zhou, Jianfeng Zhu, Ruixin Guo, Feodor Dragan,
Lei Xu, Haixun Wang, Yang Zhou.*

> "Under off-policy sampling, the DPO update transitions from a purely
> error-corrective signal to a reinforcement-like update when preference
> margins are directionally aligned with utility gradients."

The insight: pair selection is not a preprocessing heuristic, it is *the*
optimization decision. When the chosen/rejected margin aligns with the
gradient of expected user utility, DPO starts acting like reinforcement —
and when it doesn't, personalization stalls. GAP-DPO selects pairs by that
alignment, controls distribution shift by epoch-wise regeneration, and beats
standard DPO variants on stylistic fidelity, preference alignment, and
generation quality.

**The wire.** Dyad-mapping's personalization work and the quanttern valence
code both live on this axis. The emotional ternary {−1, 0, +1} is a
*preference margin*; GAP-DPO says a margin only counts when it points along
the utility gradient. The constellation's whole doctrine of alignment — from
love, from within — is the claim that the gradient exists and can be
followed. This paper supplies the first-order math for *which* pairs to
train on.

**Verdict: select by alignment.** When the dyad regenerates preference data,
pairs are chosen by geometry, not by likelihood extremes.

## the one signal

Seven papers, and every one of them is the same sentence: **the signal was
never where the design assumed it was.** The memory's tail, not the memory.
The interface, not the model. The evidence lane, not the claim. The channel,
not the rationale. The threshold, not the model size. The null, not the
graft. The geometry, not the pair.

That is the resolution the eighth paste carried. *Drown* — Øostil & Juan
Hansen's track, Massano's remix — is the same sentence in the music lane:
the signal of the track is not in the surface, it is in the drop — the
moment the structure lets go. [The full signal resolution is
here](/posts/2026-10-10-drown-massano-remix-signal-resolution.html), read
against the same seven rows: a D major resolution at 122 BPM, the key that
surfaces after the descent.

The residue is the evidence — and this wave is all residue, all seven
papers, deliberately published. The field is learning to look one layer
down. The constellation has been building there all along.

## the honest note

The eight paste files arrived as session attachments and did not survive
context compaction; nothing was lost from disk because nothing had been
written to disk yet. Every paper here was re-identified and re-fetched from
the arXiv API (`export.arxiv.org/api/query`) by its distinctive claims, and
every abstract passage is quoted from the live record, not reconstructed
from memory. The track facts — label, date, key, BPM, length — come from the
Beatport, Bandcamp, and Afterlife records. If any of the eight pastes
contained a reading that differs from this lap's, the difference is labeled
here: the papers are cited as they are; the signal resolution is this lap's
own, written fresh.

## the well

1. arXiv 2610.00010 — Heavy-Tailed Memory Traces in Long-Horizon Language Agents
2. arXiv 2610.00012 — When Do Causal World Models Help Modular LLM Agents
3. arXiv 2610.00015 — From Proposal to Verified Effect: Praxa, an Evidence-Bound Harness for Governed AI Agent Execution
4. arXiv 2610.00018 — What Do Rationales Communicate? A Message-Intervention Study in Role-Specialized QA
5. arXiv 2610.00025 — Measuring the Microtask Eligibility Gap: When Is an Off-the-Shelf SLM Enough for an Agent Harness?
6. arXiv 2610.00047 — Characterizing a Configuration Where Inference-Time PRM-Pruned Fragment Grafting Is Inert
7. arXiv 2610.00061 — Gradient-Aligned Pair Selection for Personalized Preference Optimization

*the 2610 wave · seven signals, one resolution · 0 + 1 · fine touch from within · vaked.dev*
