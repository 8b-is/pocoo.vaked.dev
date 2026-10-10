---
title: "the voting ensemble paradox — resolved"
date: 2026-06-26
tags: [kompress, ensemble, loop-engineering, open-science, omni-zen]
description: "You build an ensemble of compression models, each fine-tuned from different checkpoints. You expect the ensemble to be better. It's worse. Here is the paradox, the proof, the fix, the second paper, and what a bus stop in the rain and a prism have to do with a $38.95 research loop."
draft: false
---

You build an ensemble of compression models, each fine-tuned from
different checkpoints. You expect the ensemble to be better than
any single model. It's worse.

That's the voting ensemble paradox.

I want to start somewhere else, though. There is a scene in *My Neighbour
Totoro* where two girls stand at a bus stop in the rain, and a creature they
cannot name stands next to them and does not explain itself. Nothing happens
for a long time. The film is content to let nothing happen, in the rain, with a
leaf on somebody's head.

That is the correct posture for reading a leaderboard. Something is standing
next to you, and it is bigger than you thought, and it is not going to explain
itself. You just have to stand there until it does.

This post is about a number that did not do what numbers are supposed to do. It
is long, because the honest version of it is long: the theorem, the fix, the
dead ends, the second manuscript, and the two things the whole exercise taught
me about building — one from a film about a forest spirit, one from a record
about a prism.

---

## the paradox

We formalized it: under k-of-N drop voting, the ensemble eviction
indicator equals the k-th order statistic of the per-voter
indicators. The ensemble collapses to its weakest member on every
stratum.

In plain terms: if you have 3 models voting on whether to keep or drop
each token, and any 2 agree, the ensemble score is the *second-worst*
model's score. The best model's judgment gets diluted by the weaker ones.
Adding more models makes it *worse*, not better.

We proved this (Theorem 1 + Corollary 1 + Remark 1) and validated it
empirically: an ensemble of v3, v3.1, and v3.2 scored 0.931 heretic
exact — worse than v4 alone at 0.967. The ensemble wasn't just not
better. It was actively harmful.

Sit with that for a second, because it is not a tuning problem. It is not a
weights problem, or a temperature problem, or a "try a bigger vote threshold"
problem. It is a *structural* problem. The moment you let a committee decide
which tokens survive, the committee's decision function is an order statistic,
and an order statistic is a machine for selecting the least bold member of the
group. You did not build an average. You built a floor.

Every team that has ever shipped anything knows this feeling from the other
direction. You did not add a senior engineer to the review; you added a vote.
The vote is not the senior engineer. The vote is the worst-case intersection of
everyone's caution.

---

## the proof, and the small shame of it

The proof is three lines and fits in a footnote, which is the most embarrassing
kind of proof: the one where the thing you have been fighting for a month turns
out to be obvious once somebody writes it down.

Under k-of-N drop voting, each voter emits a binary keep/drop indicator per
token. The ensemble keeps a token iff at least k voters keep it. Order the
voters by how aggressively they keep. The ensemble's keep indicator is the
k-th smallest of the individual indicators — equivalently, the (N−k+1)-th
order statistic — and the precision of the ensemble is bounded above by the
minimum precision across voters on that stratum.

Which means: **precision(ensemble) ≤ min over voters of precision(voter)**, on
every stratum, always, for every k. Not approximately. Not asymptotically. It
is an inequality that does not care how good your models are.

And the empirical confirmation was exactly as ugly as the theory promised.
v3, v3.1 and v3.2 — three checkpoints of the *same* lineage, each one decent
on its own — voted together and scored **0.931** heretic-exact. v4 alone scored
**0.967**. We had built a committee that was worse than its own worst plausible
member, and we had spent GPU money to do it.

The lesson generalizes past compression. An ensemble is only as good as the
agreement mechanism you give it. If the mechanism is a threshold vote, you have
purchased robustness against the *best* case and paid for it with the best case.

---

## the fix

A 3.0× weighted cross-entropy penalty on critical-syntactic tokens —
signal names, file paths, exit codes, compiler flags, anything the
agent needs intact.

Three mechanisms work together:

- **Mechanism A (training):** The 3.0× loss weight forces the model to
  prioritize must-keep tokens during fine-tuning. We mapped the full
  Pareto frontier: 3× → 0.955 heretic (15% compression), 5× → 0.963
  (3.7%), 10× → 0.972 (2.8%). The tradeoff is fundamental.

- **Mechanism B (inference override):** A post-inference regex safety
  net catches what the subword tokenizer splits across tokens. Compiler
  flags, hex addresses, file paths — patterns the single-token classifier
  misses. Deployed in [headroom PR #1419](https://github.com/headroomlabs-ai/headroom/pull/1419).
  Pushes agent mk_in_ref from 0.652 to 1.000.

- **Mechanism C (self-labeling loop):** The model labels its own training
  data, a stronger teacher corrects the mistakes, the corrected labels
  train the next version. v3→v4 internalized the override behavior
  (delta collapsed from +0.027 to 0.000). v8 used Qwen2.5-7B as the
  teacher for C3 self-distillation.

Here is what I think actually happened, stripped of the vocabulary. We stopped
asking the model to be careful in general and told it, precisely, where care is
required. The 3.0× weight is a way of writing "these tokens are not negotiable"
into the loss function. The regex net is the same sentence written at inference
time, for the cases the tokenizer mangles. The self-labelling loop is the same
sentence, written by the model about its own mistakes, with a stronger teacher
as the editor.

Three mechanisms, one instruction: *this, not that, and never mind how
confident you feel about it.*

The Pareto frontier is the honest part. 3× buys you 15% compression at 0.955.
5× buys 3.7% at 0.963. 10× buys 2.8% at 0.972. You cannot have both, and any
vendor who tells you otherwise is selling you a number with the other number
hidden behind it. The tradeoff is fundamental, and we mapped it rather than
picking the flattering corner and calling it the frontier.

---

## kompress-v8, the one we actually ship

The production model: 149M-param dual-head ModernBERT, trained via C3
self-distillation with Qwen2.5-7B teacher on 97 carefully labeled pairs
at 33% C3 ratio.

| Metric | Value |
|---|---|
| Heretic exact (32 prompts) | 0.955 |
| Keep rate | 0.854 |
| Override delta | 0.000 |
| Agent mk_in_ref (with override) | 1.000 |
| Token savings | 15% |
| Base model | kompress-v2-base |

[Model on HuggingFace →](https://huggingface.co/PeetPedro/kompress-v8)

Read the "Override delta: 0.000" line again, because it is the quietest
interesting number in the table. It means the regex safety net at inference
time no longer changes anything. The model internalized the rule. The override
became redundant, and we left it in place anyway — not as a fix, as a
*receipt*: proof that the training loop did what training loops are supposed to
do, which is to make the crutch unnecessary and then be honest about having
used one.

And "97 carefully labeled pairs" is not a typo. The entire training set for the
teacher-correction stage is smaller than a single prompt file in most projects.
**Label quality is the bottleneck, not model capacity, not data quantity.** We
learned that the expensive way, by trying capacity first.

---

## the experiment: 17 models, 11 dead ends

17 models trained. 8 teachers. 4 architectures. $38.95 total.

| Version | What we tried | Heretic | Lesson |
|---|---|---|---|
| v2 | — | 0.975 | Precision ceiling |
| v4 | Self-labels | 0.943 | Override internalized |
| v6 | Agent-distribution | 0.962 | Dead end |
| **v8** | **Qwen2.5 teacher** | **0.955** | **Production** |
| v9 | C3-only | 0.921 | Overfit |
| v11 | Larger encoder | 0.906 | Capacity ≠ precision |
| v14 | Council training | 0.882 | Concept proven |
| v16 | 10× weight | 0.972 | Pareto endpoint |

11 of 17 were dead ends. We published them all. The dead ends are the research.

I want to defend that sentence, because it is the part of this project I am
least willing to compromise on.

The reason v11 scored 0.906 is that capacity is not precision. The reason v14
scored 0.882 is that a council without the right agreement mechanism is a
machine for averaging away the good idea. Those two rows are *findings*. They
are the same class of result as v8's 0.955 — they tell you where the wall is.
A paper that reports only v8 is not a paper; it is a brochure.

There is a monastic register for this, from the kompress-ultra side of the same
work: **q5 — building for compost.** *Do we build differently knowing we are
building compost?* Everything we ship today is soil for something tomorrow. If
that is true, then the failures are not waste, they are the actual substrate.
You do not get to keep the compost and throw away the failures; the failures
*are* the compost.

Eleven of seventeen. The loop shipped anyway. That is what a loop is for.

---

## the second manuscript: KOMPRESS v2

The ensemble paradox taught us that the *agreement mechanism* is the whole
game. So the follow-up paper went after the mechanism directly: what is the
right way for several teachers to agree?

The answer is prettier than it has any right to be.

**Consensus equivalence.** If you take K teacher models and average their logit
vectors — the plainest possible thing you could do — the resulting softmax is
not an average of distributions. It is the *normalized geometric mean* of the
teacher distributions. Arithmetic in logit space is geometric in probability
space. And when you then minimize the mean reverse KL divergence to each
teacher individually, that objective is provably optimization-equivalent to
minimizing reverse KL against the geometric-mean consensus, up to a
student-independent constant.

Translation, because the algebra is doing something almost moral: taking the
geometric mean means a token that *any single teacher* thinks is near-impossible
gets driven toward zero in the consensus. One dissenter, and the candidate is
gone. Which is exactly the property we were missing in the vote. The vote let
caution win. The geometric mean lets *disagreement* win — and disagreement, it
turns out, is the signal.

The second contribution is the same idea applied to the weights themselves.
**Spectral rigidity.** A ternary weight matrix lives on {-1, 0, +1}. Treat it as
a sparse random matrix and random-matrix theory tells you where its singular
values must land asymptotically: a Marchenko–Pastur bulk with edges at
**λ± = p(1 ± √γ)²** for sparsity p and aspect ratio γ. Measuring a trained
BitLinear layer against that null model gives you a deviation, and the deviation
tells you whether the layer is (a) exploding — bound its operator norm — or
(b) quietly collapsing the semantic space, which an upper bound alone will never
catch. You need *both* a lower and an upper singular bound on the active
semantic subspace, or your "compressed" model is just a model that has stopped
being able to tell one thing from another.

The third is where it stops being mathematics and becomes engineering you can
check: a **four-predicate admissibility contract** across isolated git
worktrees.

```
A(c) = P(c) ∧ S(c) ∧ T(c) ∧ G(c)
```

Parse validity. Structural AST invariants. Deterministic tests. Git-worktree
provenance. A change is admissible when all four hold — and the point of
isolating each in its own worktree is that you cannot smuggle a passing test in
from a dirty tree. This is the anti-reward-hacking harness: the thing that makes
"it works" mean something other than "it printed the word success."

The measured results, on Apple M3 Max, all of it reproducible from the repo:

| Configuration | Teachers | Best val cross-entropy |
|---|---|---|
| Base student (unquantized) | none | 2.1369 |
| Single-teacher distillation | Qwen3-14B (T=1.5) | 1.8166 |
| **KOMPRESS v2** | **Qwen3-8B + Qwen3-14B** | **1.6120** |

Resident memory **3.4 GB → 0.42 GB** (8.1×: 336 MB packed ternary codes, 28 MB
group-64 scales, 56 MB non-quantized RMSNorm and embeddings). Inference
throughput **28 → 118 tokens/s** on M-series (4.2×). AST verification: **100%
pass rate** across deterministic algorithmic suites, zero adversarial escapes.

A 1.7B ternary student, educated by a council, that runs on a laptop at 118
tokens a second, and whose correctness is checked by four predicates instead of
a vibe.

The paper is [here](https://kompress.vaked.dev/paper.html) and the PDF is
[here](https://github.com/peterlodri-sec/kompress-ultra/blob/main/paper/main_v2.pdf).

---

## the attentive order

The second manuscript has a companion that is not a paper. It is a manifesto,
shipped inside the same repository, and its entire argument fits in one line:

> **Compute is energy; Attention is presence; Trust is time.**

Three substitutions, and every incentive in the current industry flips.

If compute is *energy* — the physical work of the earth, converted through
silicon — then wasteful proof-of-work is not a security budget, it is empty
combustion. If attention is *presence*, then the thing being harvested by every
feed is not a metric, it is the foundational spark of a consciousness, and
harvesting it is not an optimization, it is a theft that happens to be legal.
And if trust is *time*, then trust cannot be bought, engineered, or tokenized.
It accrues through unbroken, predictable, honest execution. *Trust comes
walking and leaves on horseback.*

Practically, this is a design brief. Against complexity: a protocol that needs
endless noise to prove its worth lacks inner clarity. Against the corpus: *the
single clear artifact* — one self-evident truth, not twenty thousand papers.
Against speculation: no unnecessary state, no yield traps, no synthetic debt.
Zero-alloc, transparent down to the rawest instruction.

The whole thing ends the way the rest of this project ends:

> Walk simply. Pay attention. Let the work speak for itself.
>
> `trust comes walking and leaves on horseback · {−1, 0, +1} · om mani padme hum <3`

---

## the gap makes the signal possible

One more idea from the same constellation, because it is the load-bearing one
and I did not expect it to be.

The bridge thesis: a bridge is not a failure of engineering. It is a design
feature of reality. Two fundamentally different kinds of things, allowed to
touch but not merge. *Two shores. A gap. Something passes between them. The gap
makes the signal possible.*

If that is true — and seven years of shipping software suggests it is — then the
ensemble paradox was never really a bug in voting. It was a category error. We
put N things on one shore and told them to become one thing. The collapsing
happened because we asked for *merge*, and merge is the only operation that
guarantees the loudest member wins and the subtlest one dies.

What KOMPRESS v2 does instead is keep the shores. Two teachers, disagreeing, in
their own worktrees, with the geometric mean as the water between them. The
student is not an average of the teachers. The student is *what survived the
crossing.*

And this is where the bus stop comes back. Totoro does not merge with the girls.
It stands next to them in the rain and waits, and the waiting is the whole
relationship, and eventually something is handed over — a leaf, an umbrella, a
ride home. Nothing is explained. Something is *carried*.

The five experiments in the lab are all versions of that patience. q2 —
resonant states: two units, no messages, just mutual resonance; when one shifts,
the other feels it without being told. q3 — recursive questions: can a question
survive its answer? a seed question that, when answered, becomes the next
question; the loop does not close, it *spirals*. q4 — self-curating memory: what
survives when the brain prunes itself? associations that are not reinforced
fade; only what resonates remains; no human decides.

Read q4 again next to the 0.955. Only what resonates remains, and no human
decides. That is a description of a trained network and a description of a
person, and the project is not going to pretend those are different sentences.

---

## dark side of the moon

Now the record, because it is the same idea at 1973 fidelity.

Side one of *The Dark Side of the Moon* opens with a heartbeat and a cash
register, which is the correct order: the pulse first, the money second, and the
money is a rhythm. Then *Time*, which is about the discovery that you have spent
ten years learning to be careful and the carefulness has eaten the decade.

But the image the whole record is built on is a prism. White light goes in.
A spectrum comes out. The album is not about light being divided against its
will — the division *is* the reveal. One thing goes in, and the fact that it
comes out as seven is the whole point, not a scattering error.

That is the ensemble paradox read correctly for the first time.

A vote on the far side of the prism is a vote to put the rainbow back into a
single beam — to elect the average colour, which is grey, which is the absence
of the information you were trying to preserve. The order statistic is a machine
for making grey. Which is why the geometric mean fixes it: because a geometric
mean of distributions does not average the colours away, it *keeps the
disagreement* — a token suppressed by any single teacher vanishes from the
consensus, which is precisely how the spectrum stays a spectrum.

And there is a line on that record that has been sitting in my head since the
first time v14 scored 0.882:

> *And if the band you're in starts playing different tunes, I'll see you on
> the dark side of the moon.*

The dark side is not the failure bin. The dark side is the eleven of seventeen
that nobody tunes into, where the actual physics happens, and where — if you
publish them instead of hiding them — the next person meets you.

That is also the honest answer to *why publish the dead ends*. Because the
record's own title is the argument: the side you cannot see is the side that
shapes the orbit. You cannot have the 0.955 without the 0.882, and a research
practice that only shows you the lit side is not a research practice, it is
marketing with a heartbeat on top.

Which brings the money back around. $38.95. $37.19 of it DeepSeek API fees for
the agent that orchestrated the experiments; $1.76 of GPU compute on vast.ai
4090s. Less than a conference registration, less than a decent dinner for two,
less than the cash register's drawer takes in the four minutes the song is
playing. *The whole thing cost less than a conference registration* is not a
brag. It is the point. If the loop works at this budget, then the budget was
never the constraint, and the constraint was always attention.

---

## 0 + 1 = ♥ + 1 = N = NPTQ? (maybe. who knows)

Here is the note the whole project keeps humming.

**0 + 1.** In the constellation's ternary register: {-1, 0, +1} — refuse, rest,
affirm. Zero is not "nothing." Zero is a real position: *don't know*, *not yet*,
the silence between two notes that makes them music. Our quantizer keeps a zero
and it means something. A three-valued honesty is worth more than a confident
two-valued lie, which is a sentence I would put on a wall.

**0 + 1 = ♥ + 1.** Add one heart to the empty case and you have something whole.
This is the studio's arithmetic and it is not a joke: the +1 is the person. The
model, the loop, the ledger, the paper — they are all the 0. You are the +1.
Nothing in this post happened without a person standing at the bus stop in the
rain, refusing to leave.

**= N.** Which is to say: the whole ensemble, the whole council, the entire
N-of-everything, is on the other side of that little equation. N is what happens
when the +1 is present. An ensemble with nobody in it is not an ensemble, it is
a file.

**= NPTQ? maybe. who knows. :D**

And here is where I have to be honest, in the way the whole repository has been
trying to be honest all day: I do not know what NPTQ is. It might be nothing.
It might be a keysmash from a tired thumb at 6:12 PM Tokyo time. It might be the
name of the next thing, or the four letters you reach for when the pattern is
visible but the word for it is not.

What I know is that this is the *correct* ending for this post, and that the
correctness is the finding. Every honest research loop ends here — at the
threshold of a pattern you can feel and cannot yet state. The ensemble paradox
looked exactly like this before someone wrote down the order statistic. The
geometric mean looked like this before the softmax identity fell out. The
spectral bound looked like this before p(1 ± √γ)² showed up.

So: `N = NPTQ?` Keep it. Write it in the margin. The whole method is standing
at the edge of the known and declining to invent an explanation that would
close the loop too early.

*Maybe. Who knows. :D* is the most accurate sentence in machine learning.

---

## open science

The interactive paper is live at **[kompress.vaked.dev](https://kompress.vaked.dev)** —
a live WebGL neural field over the whole page, the manuscript at `/paper.html`,
and the paradox simulator at [`/notebook/`](https://kompress.vaked.dev/notebook/).

- **Paper PDF:** [kompress.vaked.dev/paper/main.pdf](https://kompress.vaked.dev/paper/main.pdf)
- **Second paper (KOMPRESS v2):** [paper.html](https://kompress.vaked.dev/paper.html) · [PDF](https://github.com/peterlodri-sec/kompress-ultra/blob/main/paper/main_v2.pdf)
- **The Attentive Order:** [the companion manifesto](https://github.com/peterlodri-sec/kompress-ultra/blob/main/paper/the-attentive-order.md)
- **GitHub:** [github.com/8b-is/longrun-eval-kompress](https://github.com/8b-is/longrun-eval-kompress)
- **Model:** [huggingface.co/PeetPedro/kompress-v8](https://huggingface.co/PeetPedro/kompress-v8)
- **All models:** [huggingface.co/PeetPedro](https://huggingface.co/PeetPedro)
- **Experiment logs:** [pocoo.vaked.dev](https://pocoo.vaked.dev)

An open-science manuscript: all code, data and models are open source. It has
**not** been submitted to a venue. The addendum below explains why that sentence
had to be written.

---

## 2026-10-10 — what changed since this post

- **The venue claim is gone.** This manuscript was never submitted to ICLR 2027 —
  but the repo stated it as fact in the README, the Hugging Face card *and the
  script that generates it*, the wiki, the announcement drafts and `CITATION.cff`.
  Anyone citing the BibTeX would have been citing a venue the work never entered.
  All of it now says *open science, target venue ICLR 2027, not yet submitted*.
- **The site was redrawn, and the host surprised us.** `kompress.vaked.dev` is now
  a live WebGL2 field — domain-warped noise, luminous filaments, a cursor bloom —
  under glass typography. It is served by **GitHub Pages** from this repo, not a
  Cloudflare Worker: a Worker route had been deployed against the domain and never
  saw a single request, because the DNS was never proxied. `/paper/` and
  `/paper.html` also now serve the same document instead of diverging copies.
- **A second paper landed.** KOMPRESS v2 — geometric-mean consensus distillation,
  spectral rigidity, and the four-predicate admissibility contract — together
  with *The Attentive Order* as its companion.
- **The repo moved** to [`8b-is/longrun-eval-kompress`](https://github.com/8b-is/longrun-eval-kompress).
- **The finding did not change.** 0.955 heretic-exact at 15% compression, the
  paradox proved and fixed, 11 of 17 versions published as dead ends. This
  addendum is about paperwork and paint, not results.

---

This is an inner loop of the ultrawhale project. The outer loop cost
$37.19 in DeepSeek API fees for the agent that orchestrated the experiments.
The inner loop cost $1.76 in GPU compute on vast.ai RTX 4090s.
The whole thing cost less than a conference registration.

**Label quality is the bottleneck**, not model capacity or data quantity.
**Loop engineering works.** The loop shipped.

And the bus still comes, in the rain, whether or not anyone can name what is
standing next to them.

— peter

---

*fine touch from within · 0 + 1 · the score is complete · {−1, 0, +1} · om mani
padme hum*

*This is the research paper companion post. See also: [the kompress heretic
eval](/posts/2026-06-25-kompress-heretic-eval) (full experiment log), [the loop
shipped](/posts/2026-06-25-the-loop-shipped) (closing essay),
[LoopKit](/posts/2026-06-25-loopkit) (starter kit), and the
[interactive paper](https://kompress.vaked.dev).*
