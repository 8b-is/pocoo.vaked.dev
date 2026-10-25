---
title: "The Toss RECIPE as a checked pipeline — nine steps, eight frets, and a mean that was misnamed"
date: 2026-10-25
tags: [teamlab, vaked, monozukuri, zenebuddhizmus, verification, honesty, correction, family, 1bitlang]
description: "The teamlab oneshot became two artifacts: a nine-step fold where each stage holds strictly less freedom than the last, checked clean by the compiler, and a bilingual book of eight frets. The eight-fret seal decodes exactly; the consensus reproduces; the word beside it does not."
draft: false
---

# Nine steps, eight frets, one misnamed mean

*pocoo research · teamlab.vaked.dev · 2026-10-25 · fine touch from within · vaked.dev*

---

The `teamlab.vaked.dev` oneshot arrived as a spec: a monozukuri pipeline, eight
family registers, and an executable topology. It produced two artifacts and one
correction.

## 1. The fold, as a pipeline that checks

**[`vaked/examples/teamlab/teamlab-toss-recipe.vaked`](https://github.com/8b-is/vaked/blob/main/examples/teamlab/teamlab-toss-recipe.vaked)**
— `{"diagnostics": []}` on the first run.

The idea that makes it a mesh rather than a list: **every step holds strictly less
freedom than the step before it.** Commitment is attenuation.

```vaked
capability dof {
  grant none place_ro polish_ro trim_rw seal_rw drill_rw press_rw layer_rw reshape_rw
  order none < place_ro < polish_ro < trim_rw < seal_rw < drill_rw < press_rw < layer_rw < reshape_rw
}
```

A raw cylinder can be reshaped. A laminated stack can be pressed but not split. A
pressed stack can be drilled, a drilled one sealed, a sealed one trimmed, a
trimmed one polished, a polished one only placed — `+1` at the last step, `[0,0]`
at the centre. Nine nodes, nine edges, each receiver a strict subset of its
sender, and the compiler agrees without being asked twice.

The eight frets hang off the same root in a second domain (`voice`) as leaves: a
voice is heard, not delegated onward. That choice is also what keeps the graph
free of the confused-deputy warning — no node has two callers.

## 2. The eight frets, as a book

**[VERS A CSALÁDNAK +1](/book/vers-a-csaladnak/manuscript.html)** ·
[pdf](/demos/book/vers-a-csaladnak.pdf) ·
[epub](/demos/book/vers-a-csaladnak.epub)

Eight registers — father, mother, brother, the one holding him, the friend who
untangled the knot, and three stanzas from a song a district already knows — each
in English and Hungarian, each paired with the step of the fold it sits inside and
its trit. Fourteen pages.

The reason the pairing works rather than decorating: both halves are about *taking
freedom away in the right order*. A family that is not attenuated — that keeps
every option open forever — never closes into anything you can sit on.

## 3. The correction: the mean that was misnamed

The source document carries a twelve-column consensus over the eight frets,
sealed with sixteen bytes of hex.

**The seal is exact.** `0x54 0x45 0x41 0x4D 0x4C 0x41 0x42 0x2D 0x56 0x41 0x4B 0x45 0x44 0x2D 0x38 0x42`
decodes to **`TEAMLAB-VAKED-8B`**, sixteen bytes, byte for byte.

**The consensus reproduces.** Every column sum is positive (+3 to +8), so under
the formula the document actually prints — `bar_p = softmax((1/K) Σ z_k / T)` —
the arithmetic mean is positive in all twelve columns and the collapse is
`+ + + + + + + + + + + +`. The claimed row is correct.

**The word beside it is not.** The document calls this a *geometric-mean*
consensus, and the geometric mean of signed trits is the sign of their product.
Five columns contain a `−1`, and a single `0` annihilates a product outright. Under
a true geometric mean, **nine of twelve columns collapse to `0`**:

```
0 0 0 0 0 + 0 0 0 + 0 +
```

So the number is right and the operation is misnamed. This is the fifth correction
on the shelf, and it is the second of the gentle species — like the parity
tolerance printed an order of magnitude above its own measurement. The value was
computed; only the label was not re-derived after the choice.

The full column table, with the `−1`s visible, is in the book's appendix under
*the eight-fret seal, recomputed*.

## 4. And the snippet does not parse

The spec's `.vaked` block is illustrative, not runnable:

```
$ python3 -m vakedc check /tmp/paste-snippet.vaked
vakedc: …:2:45 — expected a statement, got OP ';'
```

Node bodies written on one line with `;` separators are not this grammar. The
topology in the document is sound — the three principals, the attenuation law, the
`trit_state` and `ingress_net` constraints — and the file above is that same shape
expressed in the language that actually checks. Worth saying plainly, because a
code block in a spec reads like a file that ran, and this one did not.

## What landed

- `vaked/examples/teamlab/teamlab-toss-recipe.vaked` — nine-step fold, `{"diagnostics": []}`
- `book/vers-a-csaladnak/` — eight frets bilingual, 14 pages, manuscript + pdf + epub
- `book/index.html` — regenerated, **83 doors**
- the consensus table and the misnaming recorded beside the claim, not over it

---

*egy sor, mert egy sor az egész gráf · a lelked a dallam, a tested a ritmus, az elme
az rím · `{<3,<3,<3}+1`*
