---
title: "How to be the #1 project on GitHub — the evidence, and the playbook"
date: 2026-10-10
description: "Pulled the top-starred repos created in the last 30 days and the all-time leaders. The patterns are not mysterious: one-line pitches, a famous thing reimplemented in the open, instant install, and a demo you can watch. Plus how Trending actually behaves (it is undocumented) and a launch playbook."
tags: [research, github, oss, growth, strategy, projects-tools, launches]
draft: false
---

# How to be the #1 project on GitHub

*Research, not vibes. The tables below are pulled live from the GitHub API —
rerun them and you get the same shape.*

---

## The evidence

**Top-starred repos created in the last 30 days** (`created:>2026-09-10`, sorted by
stars):

| stars | repo | lang | one-line description |
|---|---|---|---|
| 35,742 | `storytold/photocraft` | Rust | An open-source, clean-room reimplementation of **Adobe Photoshop** in pure Rust |
| 31,986 | `NandhaKishorM/laya` | Python | Non-autoregressive System 1 decision engine. Typed choice, score and yes/no decisions |
| 22,480 | `browser-use/jev-ultrafast` | Python | Fastest and cheapest web agent |
| 19,620 | `Niko1221/Strata` | C++ | Qwen3.8 next-gen on any consumer hardware: one-click install for Windows / Linux |
| 14,878 | `robbietilton/Compositor` | Swift | The **Photoshop alternative** for Mac |

**All-time leaders:**

| stars | repo | what it is |
|---|---|---|
| 552,229 | `codecrafters-io/build-your-own-x` | Master programming by recreating your favorite technologies |
| 516,816 | `sindresorhus/awesome` | 😎 Awesome lists about all kinds of interesting topics |
| 487,016 | `public-apis/public-apis` | A collective list of free APIs |
| 456,780 | `freeCodeCamp/freeCodeCamp` | The open-source curriculum |
| 398,579 | `EbookFoundation/free-programming-books` | Free programming books |

---

## What the top ten have in common

1. **A famous thing, rebuilt in the open.** Five of the top movers this month are
   "X, but open source": Adobe Photoshop (twice), a web agent, a model runtime.
   The pitch lands in half a second because the reader already knows the
   reference.
2. **One sentence, zero jargon.** Every description above is readable by someone
   outside the field. No "framework for orchestrating", no "next-generation
   platform".
3. **A language choice as a claim.** *pure Rust*, *Swift*, *C++* — the language is
   part of the pitch, not incidental.
4. **Instant install, or it doesn't count.** "one-click install", "on any consumer
   hardware". If the first command needs a paragraph, the visitor is gone.
5. **A demo you can watch without cloning.** A GIF or a video at the top of the
   README does more work than any badge.
6. **Short, memorable names.** `photocraft`, `laya`, `Strata`, `Compositor`.
7. **The all-time list is a different game entirely.** It is dominated by
   *curation* (`awesome`, `public-apis`, `free-programming-books`) and
   *curriculum* (`build-your-own-x`, `freeCodeCamp`) — utility that keeps being
   useful for a decade. Novelty spikes; curation compounds.

## How Trending actually behaves

**GitHub has never published the algorithm.** Anyone who tells you the formula is
guessing. What is observable and consistent:

- **Velocity, not totals.** A repo with 400 stars today outranks one with 40,000
  accumulated. Stars *per unit time* over a short window is the dominant signal —
  this is why a fresh project can appear beside a giant.
- **It is bucketed.** Trending is filtered by language, by "spoken language", and
  by date; "All languages" is the hardest table to top, "Rust today" is far
  softer. **Pick your bucket before you launch.**
- **Uniques and other engagement count.** `git clone`s, unique visitors, forks and
  repository views move the ranking, which is why a Hacker News front page (a
  flood of *unique* visitors) moves it so hard.
- **Manipulation is visible.** Purchased stars cluster, spike unnaturally, and are
  routinely flagged and stripped. It is also the fastest way to lose the only
  thing that matters, which is trust.

## The playbook

**T−7 · prepare (the part everyone skips)**

1. **Rewrite the first screen.** Name, one line, a GIF, an install command, a
   licence. Nothing else above the fold.
2. **Make install a single command** with zero required config.
3. **Put a demo artefact in the repo** — a GIF, a short video, a live playground.
   Something that requires no clone to appreciate.
4. **Seed a real audience** — the people who will actually use it. Ten true users
   beat a thousand drive-by stars.
5. **Pick the bucket.** Which language, which topic, which "today" list you intend
   to top.

**T−0 · launch**

6. **Post once, well**, late US-morning on a weekday — Hacker News *Show HN* with a
   link to the repo and a first comment that explains the *why*, then Reddit
   (`r/programming`, `r/rust`, the language's sub), Lobsters, X, and the language's
   Discord. Do not spam; one considered post per venue.
7. **Reply to every comment for the first six hours.** Engagement is the launch.

**T+1 … T+30 · sustain**

8. **Ship something visible every week.** Release notes are content; a changelog
   with real numbers is a story.
9. **Get onto a curated list.** Ask to be added to the relevant `awesome-*` — it is
   the durable, compounding channel.
10. **Turn users into contributors.** Good `CONTRIBUTING.md`, labelled
    `good-first-issue`s, fast reviews.
11. **Publish the receipts.** Benchmarks, screenshots, before/after. Claims without
    evidence do not survive contact with an HN comment section.

## Applied: what #1 would look like for a project like `wupz`

The Photoshop pattern is "X, but open". `wupz`'s version of that pitch is
sharper and rarer: **"a linker that packs while it links — the binary comes out
smaller, in one pass."** It has the three ingredients the data rewards:

- **one sentence** anyone can repeat,
- **a measurable result** (a link + pack that beats `link → upx`, and the receipts
  are already in [`BENCHMARKS.md`](https://github.com/8b-is/wupz/blob/main/BENCHMARKS.md)),
- **a bucket** nobody else is fighting in (Rust *and* Zig, "linkers").

What it still lacks, per the evidence: a **demo you can watch** (a terminal
recording of `wupz` beating the incumbent, on screen, is the whole launch), a
**one-command install** (`cargo install` — trivial once P3 lands), and the P0
corpus numbers that make the claim true rather than promised.

## The honest caveat

Trending is a lottery with a visible mechanism. Two equal projects can differ by
100× on where the first 200 visitors came from. The compounding paths —
curation, curriculum, and being genuinely the best at one narrow thing — are
slower and do not depend on luck. **Aim for the sharpest true sentence about your
project, then let the velocity happen.**

*prove it, don't assert it · 0 + 1 · fine touch from within · vaked.dev*
