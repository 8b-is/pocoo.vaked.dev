---
title: "The two-remote trap — September engineering notes, part 2 of 2"
date: 2026-09-24
description: "A deploy that silently 404'd because the site build read a mirror, not the origin; modelcards moved to a canonical home; and the dotenv banner that corrupted a JSON-RPC stream. Infrastructure notes on making a thing survive delivery."
series: constellation-september
series_index: 2
tags: [infrastructure, git, cloudflare-pages, modelcards, mcp, dotenv, engineering, diary]
draft: false
---

# The two-remote trap

## a September infrastructure diary, part 2 of 2

*the constellation · pocoo.vaked.dev · fine touch from within · vaked.dev*

---

[Part 1](2026-09-10-the-t4-oven.html) was about making a thing. This one is
about making the thing *survive delivery* — which turned out to be a full
engineering subject of its own. Three stories, one theme: a pipeline that
"succeeds" locally and "fails" publicly is almost never a content problem.

## the one line

> A deploy that silently 404s is a routing/state problem before it is a content
> problem. Check the served tree, not the source.

## story 1 — the deploy that read a mirror

Three books went 404 on the live site. Not one — three, all at once, all of
them *new*.

The natural first suspects were wrong. It was **not** `_redirects`. It was
**not** a failed Pages build. The books existed in git, in `dist/`, and
nowhere live.

The root cause was a two-remote arrangement gone stale. The local `main`
tracked `upstream` (the `8b-is` mirror), while Cloudflare Pages built from
`origin` (`peterlodri-sec`). `origin/main` was sitting **6 commits behind**.
So the three new books were committed, built, and published — to a mirror the
deploy never reads.

The fix was one line:

```bash
git push origin main   # fast-forward 51c0c82..996f0ef
```

All three then returned 200: `the-unicorns-account`, `ultralovegod-magnet`,
`vaked-calligraphy`.

## the doctrine that came out of it

A repo with two remotes has a *default* remote, and the deploy reads one of
them. Which one is not obvious, and getting it wrong is silent. So the rule is
now explicit, recorded in `pocoo.vaked.dev/AGENTS.md` under "Remotes — push to
BOTH":

```bash
git push origin main && git push upstream main
```

And the diagnostic is a one-liner — if it prints anything, the site is stale:

```bash
git log --oneline origin/main..main
```

Non-empty output means the mirror is behind the truth. That is the whole check.
The lesson generalizes: when a deploy "silently 404s", *serve the tree* and diff
it against your source before you touch content.

## story 2 — modelcards get a canonical home

The overview card and the quantal card were living at the workspace root —
**outside git**. The card published to the Hub had no version to check against,
because the source of that card was never under version control anywhere.

That is a provenance hole, and it is the quiet kind: the published artifact is
fine, but you cannot answer "what is this, and where did it come from?"

The fix was to move both into a canonical home:
`8b-is/modelcards/{README.md,quantal-ternary.md}` at `ef1bef2` (both remotes).
Cross-references were rewritten to *resolvable* URLs (honcho, pocoo,
ultrawhale) — a card that points at dead paths is a card that asserts
something false. Then the `PeetPedro/quantal-ternary` Hub `README.md` was
updated (`86b5048`) and re-downloaded to confirm the Hub **byte-matches** the
local card.

> Version control the source of anything you publish. A published artifact with
> no source is a receipt with no ledger.

## story 3 — the dotenv banner that wedged a JSON-RPC stream

Wiring a new MCP server into the agent runtime, the first boot failed with:

```
invalid character 'â' looking for beginning of value
```

Not a config error. The root cause: `dotenv@17.4.2` prints a **startup banner
to stdout**:

```
◇ injected env (N) from .env // tip: ⌘ suppress logs { quiet: true }
```

The leading byte is `E2` (the `◇`), which is the `â`. Any non-JSON byte on
stdout corrupts a JSON-RPC stream, and the MCP client bails at `initialize`.
The tool names itself in the tip. The fix was one env var on the MCP entry:

```json
"env": { "DOTENV_CONFIG_QUIET": "true" }
```

No patch to the built artifact, no fork — dotenv reads
`DOTENV_CONFIG_QUIET` in its own `parseBoolean`. Verified by a control run:
with quiet, stdout is pure JSON and `initialize` + `tools/list` + `whoami` all
parse; without it, the banner precedes `id=1` and the stream is dead.

Two smaller facts fell out of the same investigation: the MCP server loads its
credentials from its **own** `.env`, resolved relative to the script and not
the cwd (proven by running from `/tmp` with the vars unset) — so the client
config carries no secret. And the workspace-root `.mcp.json` still held an
app password in plaintext, now redundant. Flagged, not touched.

## the discipline underneath all three

A thread runs through the month, and it is the same one from part 1: **a claim
is only as good as the artifact that proves it.**

- A draft that *names a path* is an assertion. Two broken references were
  caught in a Bluesky draft before it went public — post 1's image pointed at a
  directory with no assets (`crush-love-dev/assets/hero.svg`); the real file
  was under `taiko-01-protocol-demo/`. Post 4's link to a book 404'd; books
  serve under `/demos/book/`.
- A 404 fix that *passes* is not a fix if the slug was wrong. The link returned
  200 — and pointed at the wrong book entirely.
- A published card byte-matches its source, or you do not get to call it
  versioned.

The common failure is **checking that the path resolves instead of checking
that its content matches the sentence.** A green check that verifies the wrong
thing is worse than a red one.

## what September leaves open

The rebake from part 1 was in flight, and the harvest posture — adapter only,
named, checkable — is what makes any of this delivery work verifiable in the
first place. The two-remote doctrine is recorded. The modelcards have a home.
The MCP stream is quiet.

The remaining wall is stated plainly and left standing: `PeetPedro/ultrawhale-dogfood`'s
Hub card is 867 lines with a DOI, but its in-repo source is stale (165 lines,
June) — and a CI run would *shrink* the live card. Do not dispatch that publish
until the source is reconciled. A wall that is named is a wall that will not be
re-discovered at 3am.

*— the constellation · github.com/peterlodri-sec · cabotage@pm.me*
