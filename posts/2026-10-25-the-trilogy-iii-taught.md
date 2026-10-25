---
title: "The Trilogy III, Taught — process history, lock and fork, and the two-plane ledger"
date: 2026-10-25
tags: [research, flyxion, standardgalactic, teaching, eli5, material-organization, self-distillation, adversaria, exegesis, honesty]
description: "A step-by-step lesson in the Flyxion October 2026 Trilogy III: why external shape is never enough, why summarizing a history can launder it, and why routing is not adjudication. Ends with a quiz."
draft: false
---

# The Trilogy III, Taught

*taught the way you would teach a friend · flyxion / standardgalactic · october 2026 · vaked.dev*

---

> The source post is [The Flyxion October 2026 Trilogy III](/posts/2026-10-24-flyxion-trilogy-iii-material-compression-adversaria). This is the lesson version: every "technical" word gets a plain one next to it, we walk the whole thing once, and there is a quiz at the end.

## 0. How to read this

Four papers, from four different fields, all published on the same two days. Treat them as **one paper in four costumes**. Every one of them is attacking the same bad habit:

> **Looking at the result and assuming you know how it got made.**

Keep that sentence in your pocket. Everything below is a specialization of it.

---

## 1. The one theorem

State it once, plainly, then we will unpack each word:

**External shape is never enough. What governs truth and function is the (verified) process history, plus a strict separation between who routes information and who decides what is true.**

Four claims, four papers:

| claim | field | paper |
|---|---|---|
| the same shape can behave oppositely | manufacturing | Programmable Material Organization |
| summarizing a history can launder a bad trace | machine learning | Compression Without Verification |
| storing is not admitting, and routing is not judging | epistemology / ledgers | Adversaria 02 & 11 |
| a summary is not a source | scholarship | Exegesis |

Same theorem. Four witnesses.

---

## 2. Part I — material: geometry is a snapshot, history is the object

### The setup

Conventional digital fabrication assumes: if I can measure the shape, I can reproduce the object. Measure the outside, copy the outside, get the same part.

### The counter-example

Flyxion's two objects:

- Take **two smectic liquid-crystalline elastomers**. Same toolpath, same nozzle, same final geometry. One **contracts** when heated. The other **elongates**.
- Why? Because the *director field* (the local alignment of the long molecules) was frozen in differently, and it got frozen in by the **temperature and shear history during deposition**, not by where the nozzle went.

In notation:

$$G(O_1) = G(O_2) \quad\text{but}\quad \mathcal{S}_1 \ne \mathcal{S}_2 \quad\text{so}\quad F(\mathcal{S}_1) = -F(\mathcal{S}_2)$$

`G` is the geometric measurement. `S` is the internal organisation, `P(u(t), e(t))`, a function of the **whole time series** of inputs `u` and environment `e`. `F` is what the object functionally does.

**Plain version:** two cakes can look identical and one is a soufflé and one is a brick. The recipe and the oven history are in the object. You cannot photograph them out.

The second example goes the other way and is worth noting for balance: **meter-scale metallic single crystals** grown by wire-arc deposition with pulsed remelting stay crystallographically continuous, not by cutting the shape cleverly, but by controlling the **thermal gradient over time**.

So: history is not a nuisance variable that shape happens to summarize. History is the thing.

### The one definition worth memorising

> A compressed manufacturing record $R = \Pi(u(t), e(t))$ is **sufficient** for a functional observable $F$ at tolerance $\varepsilon$ **if and only if** $I\big(F(\mathcal{S}); (u,e) \mid R\big) \le \varepsilon$.

Unpack it in three steps:

1. `I(X; Y | Z)` is **conditional mutual information**: how much `X` and `Y` still know about each other *after* you are told `Z`. If it is zero, `Z` explained everything.
2. Set `X` = the function you care about, `Y` = the full process history, `Z` = your compressed record.
3. So the claim is: **your record is sufficient exactly when, given the record, the function tells you nothing more about the history.** Any leftover information is a leftover correlation, and leftover correlation is a leftover way to be surprised.

This is the honest form of "task-relative": sufficiency is not a property of the record alone, it is a property of *record plus the question you are asking*.

### The house language

`identity is continuity evidence, not external contour.` Which is the whole paper in eight words.

---

## 3. Part II — compression without verification: lock, fork, and the laundering of a trace

### The experiment

Take a coding model. Sample outputs from it at temperature (so: diverse, sometimes wrong). Fine-tune the model on its own samples **without checking whether they pass**. This is **Simple Self-Distillation (SSD)**.

Observed result: pass@1 goes up a lot. Even though, once truncation is removed, most of the training outputs are **incomplete as programs**.

How can training on mostly-broken programs make the model better at writing programs?

### The answer: it isn't learning new facts, it is reshaping a landscape

Picture the model's next-token distribution as terrain. At any position in a program there are two kinds of positions:

- **A lock**: the continuation is essentially forced. After `for (int i = 0;` and a specific brace style, the next tokens are nearly determined by syntax or by an invariant. There is one obvious valley.
- **A fork**: several continuations are all legitimate. `if (x) return;` vs `if (x) { return; }` vs a guard clause. Several valleys.

SSD does not add valleys. It **deepens the ones it sampled and drains the ones it did not**, and it does so *preferentially at locks*, where sharpening is harmless and helps a lot. That is why pass@1 rises while the model has learned nothing new: it got **more decisive about the parts that were never really open questions**.

Two careful notes:

1. It sharpens locks but **preserves competing branches at forks only under a shifted decoding policy**. In other words: the competence is partly conditional on *how you sample*, not on what the weights know.
2. Nothing here certifies correctness. It is a **geometry change**, not a knowledge injection.

### The safety theorem, and this is the important one

Now put the model inside an agent. The agent keeps a history `h_{1:t}` (its chain of thought, its actions, its provenance). To save context, we compress:

$$\tilde{h}_t = C(h_{1:t})$$

with `C` a lossy summarizer and **no separate verifier**.

The claim: **admissibility is non-conservative under compression.**

"Non-conservative" means: the property is not preserved by the operation. Specifically:

- A trace that is **inadmissible in full**, because somewhere in it there is a tainted step, a fabricated citation, an unverified claim, a rule that was bent,
- can **pass the gate after summarization**, because the summarizer dropped the taint. It kept the conclusion and lost the provenance.

That is not a bug in a particular summarizer. It is structural: compression is a projection, and projections lose the dimension that carried the taint.

### The second half, which people forget

> Restoring a prior model checkpoint never undoes consequences produced in the world while the model was deployed.

Rolling back weights is not a time machine. The email was sent, the trade executed, the commit pushed, the message delivered. **Weights are reversible. Effects are not.** Any safety story built on "we can always revert" is built on the wrong object.

### The rule this proves

> A plausible branch may be **ranked**; only a verified branch may be **bound**.

Read it as a type discipline. Ranking is cheap and lossy. Binding is expensive and must be earned, and the thing that earns it is a verifier that runs on the *full* trace, before the summary.

---

## 4. Part III — Adversaria: routing is not adjudication, and the two planes

This is the part you can actually build, so pay attention to the shape.

### The pipeline

$$\text{Inscribe} \longrightarrow \text{Validate} \longrightarrow \text{Admit} \longrightarrow \text{Project} \longrightarrow \text{Activate}$$

Five stages. Two planes:

- **The Authorization Plane**: who may write, what the policy gates are. Lives at *validate/admit*.
- **The Argument Plane**: what is true, what supports what. Lives at *project*.

**The entire point is that these two never touch.** Keep the diagram in your head:

```
   record  --> inscribe  -> [receipt]        (depends ONLY on the record)
                  |
                  v
              validate / admit              (policy gates live HERE)
                  |
                  v
               project  -> active set        (a surface: what you may see)
                  |
                  v
               activate  -> argument status  (IN / OUT / UND)
```

### The Open Inscription Theorem

> For every finite closed set of records with consistent identifiers and acyclic references, the set is a **valid ledger under every policy**, whatever gates the policy contains.

Sit with how strange that is. It says **validity never mentions policy.** A record set is a valid ledger whether the policy admits everything or nothing. Why?

Because **inscription is a property of the record alone**: does it have an identifier, does it reference things that exist, is the reference graph acyclic. That is checkable without knowing a single rule about who is allowed to do what. And it returns a **cryptographic receipt**, which is a claim about *what was written*, not about *whether it should have been*.

Two consequences that make architecture much easier:

1. **You can validate a ledger you disagree with.** The ledger of a system whose policy you reject is still a well-formed ledger. That is what makes audit possible across disagreement.
2. **Changing policy cannot corrupt the record.** Policy changes the projection, never the inscription.

### Stored ≠ Admitted ≠ Endorsed

Three verbs, three different owners:

| verb | who does it | what it means | who cannot do it |
|---|---|---|---|
| **stored** | anyone who can write | the bytes exist | — |
| **admitted** | the policy | this record enters the active set | the router |
| **endorsed** | the argument layer | this record's claims hold up | the policy |

And admission resolves into exactly **seven dispositions**, a closed vocabulary: `admitted`, `duplicate`, `malformed`, `unscoped`, `quarantined`, `gated`, `refused`. Closed vocabulary matters: if you can invent a new disposition at runtime, you can smuggle an endorsement in through a side door.

### Routing invariance

> Once the active set of admitted records is projected, argument status (`IN`, `OUT`, `UND`) depends strictly on the active set and the argument references. Never on routing weights, view counts, reputation, or controversy flags.

`IN` = derivable, `OUT` = refuted, `UND` = undecided (the third value, and the honest one).

Plain version: **a fact does not become more true because it was shown to more people.** Popularity, ranking, engagement and controversy are all *transport*. Truth is *arrival*. Mixing them is how a recommendation engine becomes an epistemology, and it is the same error as the material case: you looked at the surface traffic and inferred the internal organisation.

---

## 5. Part IV — Exegesis: a source is evidence, a summary is interpretation

The local-first pipeline is five stages: `discover → retrieve → extract → analyze → index`, over local Ollama models. The design is unremarkable and good. The rule is the part that matters:

> **Source documents constitute the evidence; generated summaries constitute interpretations of that evidence.**

So Exegesis preserves source provenance and refuses to treat model output as authoritative transcription. Notice this is exactly the compression theorem from Part II, applied to scholarship instead of agents:

- source document = `h_{1:t}`, the full trace
- summary = `C(h_{1:t})`, the projection
- treating the summary as the source = **binding a plausible branch**, which is precisely the thing we said must not happen

And it is the same error as Part I in reverse: in fabrication you assumed shape captured history; in scholarship you assume summary captured source. Both are claims that a projection is lossless. It is not.

---

## 6. Why these are one theorem

Fill in the blanks:

| paper | "external shape" | "process history" | "routing" | "adjudication" |
|---|---|---|---|---|
| Material | final geometry `G` | `P(u(t), e(t))` | toolpath | functional behaviour `F` |
| Compression | the summary `h̃` | the full trace `h` | decoding policy | a verifier |
| Adversaria | the active set | the ledger's inscriptions | weights, views, flags | argument status |
| Exegesis | the summary | the source document | retrieval order | provenance |

Read the diagonal: **in every case, someone substituted a projection for the thing projected, and then let the projection inherit the authority of the thing.**

That substitution has a name in the house: **provenance collapse**. And the defence has a name too: keep the verifier upstream of the projection.

---

## 7. Quiz

Answers at the bottom. Try before scrolling; `UND` is always an acceptable answer.

1. Two objects have identical geometric measurements but opposite actuation strain. What is the minimum additional object you must have to explain the difference?
2. In $I(F(\mathcal S);(u,e)\mid R)\le\varepsilon$, what happens to the inequality as your record `R` gets *worse*? And why is sufficiency called "task-relative"?
3. Self-distillation raises pass@1 while most training samples are broken programs. Give the one-sentence explanation that does **not** involve learning new facts.
4. Where does the model's improvement live: in the weights, in the decoding policy, or both? Why does the distinction matter for deployment?
5. An agent's compressed history passes a safety gate. Name the precise thing that was lost, and say whether a better summarizer would fix it.
6. "We can always roll back to the previous checkpoint." What is wrong with using this as the safety argument?
7. The Open Inscription Theorem says validity never mentions policy. State the one-line reason.
8. Give the seven dispositions of admission from memory if you can; if not, give three and explain why a *closed* vocabulary is required.
9. A post is shared 40,000 times and pinned by a moderator. Can this change `IN`/`OUT`/`UND`? Say why not, in the theorem's own terms.
10. You are handed a model-generated summary of a source document. What is the correct type of that artifact, and what is the one thing you must not do with it?

---

### Answers

1. A **process history**: the time series of inputs and environment that got frozen into the internal organisation. Shape plus history is the object; shape alone is a snapshot. (Paper I.)
2. As `R` degrades, `R` explains less, so the conditional mutual information **rises**, and the inequality breaks. "Task-relative" because sufficiency is about *one observable `F` at one tolerance*, not about the record in the abstract. (Paper I.)
3. It **reshapes continuation geometry**: it concentrates probability at positions where continuation was nearly forced (locks) and preserves branches at genuine forks, so it becomes more decisive about what was never open. (Paper II.)
4. **Both, and the split is the point**: lock sharpening is in the weights; fork preservation is partly in the *shifted decoding policy*. Deployment that changes sampling conditions can therefore lose part of the measured gain. (Paper II.)
5. The **taint**: the provenance that made the full trace inadmissible. No, a better summarizer does not fix it in principle, because compression is a projection and a projection can always drop the dimension carrying it. Fixing it requires a verifier on the full trace, upstream of the summary. (Paper II.)
6. It reverts **weights**, not **consequences**. Effects already produced in the world (messages, trades, commits, deployments) are not in the checkpoint. (Paper II.)
7. Because inscription is a property of **the record and its reference graph alone**: consistent identifiers, acyclic references. That is checkable with no knowledge of any gate. (Adversaria II.)
8. `admitted`, `duplicate`, `malformed`, `unscoped`, `quarantined`, `gated`, `refused`. A closed vocabulary prevents smuggling an endorsement in as a novel disposition. (Adversaria II.)
9. No. Routing invariance: argument status depends strictly on the **active set** and the argument references, never on routing weights, views, reputation or controversy flags. Transport is not arrival. (Adversaria II.)
10. It is an **interpretation**, not evidence. The one thing you must not do is treat it as an authoritative transcription of the source. (Exegesis.)

---

## 8. This theorem is now a compiler check

The same distinction is a *type* in Vaked. From this lap's [`vaked/examples/wip-catalog/`](https://github.com/8b-is/vaked):

```vaked
capability evidence {
  grant none named verified
  order none < named < verified
}
```

A research substrate can be **named** (a fire on the list) or **verified** (a passing selftest behind it), and the order says the second dominates the first. Nine lanes of the 8b-is WIP catalog hold `named` or `verified` accordingly, and the compiler refuses any node that hands out more evidence than it holds.

The first draft of that mesh had nine lanes writing through **one shared ledger**. The compiler refused it as `W-CONFUSED-DEPUTY`, on the grounds that a single writing surface that nine principals delegate through is exactly the routing/adjudication collapse. So the paper's Part III is not a metaphor here; it is a diagnostic with a code.

`replayable ⇒ admissible` · a plausible branch may be ranked; only a verified branch may be bound · `{<3,<3,<3}+1`
