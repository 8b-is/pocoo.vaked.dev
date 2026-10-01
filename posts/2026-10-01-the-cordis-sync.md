---
title: "The Cordis sync — engineering notes from the vendor layer"
date: 2026-10-01
description: "Syncing a sovereign fork to an active upstream: vendored Cordis 4.0.4, a one-line fix for an unhandled rejection found with a repro script, and the ELI5 on how to run deepsiper-enthea."
tags: [deepsiper, cordis, deepseek-harness, vendor, engineering, eli5]
draft: false
---

# The Cordis sync — engineering notes from the vendor layer

*deepsiper-enthea · engineering diary · fine touch from within · vaked.dev*

---

[deepsiper-enthea](https://github.com/8b-is/deepsiper-enthea) is our sovereign
fork of [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)
(`dsh`) — the agent harness where *everything is a plugin*. This is the
engineering note from the lap that brought its framework layer up to the
current upstream line.

## the shape of the problem

The harness does not depend on the Cordis framework — it **owns** it. Nine
packages (`cordis`, `cosmokit`, `schemastery`, `loader`, `include`, `group`,
`timer`, `hmr`, `logger-console`) live as source in `vendor/`, renamed into
the `@deepseek-ai` scope, pinned by commit, patchable, and auditable. That is
the whole point of a sovereign fork: the framework layer is ours.

The price of owning source is that it ages. When we forked, we sat at upstream
PR #2620. When this lap started, upstream had moved **8,066 commits** past that
point, and our vendored framework carried eighteen documented local
modifications — hardening we had added on top of the pinned copies.

The pin was the `cordis 4.0.1` release line, several rewrites deep into
upstream's own evolution of the loader, the HMR plugin, and the include
plugin. Every day of drift makes the next sync harder, so: sync now, while
the mods log is small enough to hold in your head.

## what "current" meant

Nine packages, each one now at upstream's current state:

| package | was | now |
|---|---:|---:|
| cordis | 4.0.1 | **4.0.4** |
| cosmokit | 1.8.2 | **1.8.5** |
| schemastery | 3.18.1 | **3.18.4** |
| loader | 1.0.2 | **1.0.5** |
| include | 1.0.6 | **1.0.9** |
| group | 1.0.1 | **1.0.4** |
| timer | 1.1.3 | **1.1.6** |
| hmr | 1.0.16 | **1.0.19** |
| logger-console | 1.0.1 | **1.0.4** |

Thirty-four files, +582/−634 lines. Smaller than it looks — because the
method was to take *upstream's current vendored tree whole*, not to
re-implement from memory. Upstream had kept their own local-modifications
log (entries 1–22, including features we didn't have — the volatile-config
system, Node-loader runtime-shape detection), and every fork mod that was
still needed had already been re-derived upstream in their own idiom. Fixing
nothing by hand and letting their log be the map is what kept the diff small.

The only thing the fork adds back is what the fork knows that upstream
doesn't yet: we keep our own mod entry as #23, documented in
`vendor/README.md`. Which brings us to the interesting part.

## the float

The first symptom was faint: one test in the watch layer left an *unhandled
rejection* behind. The test passed. The rejection was still there — and in
production, an unhandled rejection is not a footnote; the CLI owns a
process-level handler that turns late plugin rejections into an exit(1).

The rejection said `candidate config failed` — a config candidate that fails
to activate. Chasing it statically through the cordis fiber machinery was a
maze; every promise on the obvious path was caught. So instead of reading
more, we wrote a repro: a 70-line script that boots the same tree, drives the
same file-watch refresh, and installs `process.on('unhandledRejection')` to
print the full stack. The stack pointed at `Fiber.execute` — still not the
owner. But bisecting *when* it fired (raw marks around each refresh step)
showed it fired during exactly one refresh, and reading `Fiber.update()` with
that knowledge made it obvious:

```ts
update(config: any, noSave = false) {
  ...
  this.context.waterfall(this, 'internal/update', config, noSave, () => {
    this.config = config
    this._error = undefined
    return this.restart()        // ← an async restart…
  })
}                                // ← …and update() drops the waterfall's result
```

`restart()` awaits the fiber's own reload — which rethrows the activation
error. `Fiber.update()` cannot hand that promise back (its callers are
fire-and-forget update hooks; the loader calls it from `_patchContext`
without awaiting). So a failed candidate rejected an orphaned promise. The
fix is one line, and it stays in our mod log until upstream takes it:

```ts
      return this.restart().catch(() => {})
```

Nothing is swallowed: the error is already stored on the fiber and rethrown
by `fiber.await()`, which the activation audits consume. The unhandled
rejection stops being unhandled; the diagnostics stay.

Lesson, once more, the house kind: **a passing test is a claim; the process
ledger is the evidence.** And a repro script is cheaper than confidence.

## the guard that stopped guarding

The bigger change was semantic. The new loader is *best-effort*: a candidate
config whose plugin fails to activate no longer rejects the update — the
failure is retained on the entry's fiber for explicit audits. That is a
better design (one bad row shouldn't kill a boot), but it silently disarms
code that relied on the old rejection.

Concretely: the directory-picker composition mounts a backend and a UI
surface as loader entries, and on failure it unmounts the backend — the
comment in the code says exactly why: *leaving the backend mounted would
make a retry collide with its own registration.* That unmount lived in a
`catch` around `loader.create(...)`. Under the new loader, `create()` no
longer throws for a failed surface import; it resolves, and the failure sits
contained on the entry. The guard was dead, and no test noticed — because
the test asserted the old contract (`loader.await()` rejects), which the new
loader also no longer does.

The fix keeps the guard guarding: after creating the pair, audit what was
created — a fiber-less entry or a failed fiber is this setup's failure, and
the backend unmounts. The tests move to the new contract: the failure is
observed at the entry that owns it.

## proof before blame

Everyone who has synced a vendor layer knows the moment: the suite runs, and
suddenly twenty-three red tests, and half of them are in code you never
touched. Mine or theirs?

The discipline that paid off here: **a pristine control.** The same
repository cloned at the untouched commit — same dependencies, same Node —
ran the same failing specs. Six failures (a missing `tool-quant` entry in the
tool-catalog manifest, three unclassified `ctx.quant` types in the cordis
catalog) reproduced perfectly on the untouched tree: the fork's own quant
commit had left them, weeks ago, and nobody had run those gates since.

Final tally for the lap: five failures fixed (three real semantic ports, one
catalog row, one regression the sync exposed), seventeen remaining — every
one of them proven pre-existing or environmental on the control clone, not
one of them ours. The distinction is the deliverable: `13,913 passed`, and an
honest list of what is red and why.

## ELI5 — how to run deepsiper-enthea

The five-minute version. You need: a terminal, **Node 22.19+ or 24+**,
**pnpm 11+**, and a **DeepSeek API key** (any OpenAI-compatible endpoint
works too).

```sh
# 1. get it
git clone https://github.com/8b-is/deepsiper-enthea.git
cd deepsiper-enthea

# 2. install (one time, ~5 GB of dev dependencies — it is a whole harness)
pnpm install

# 3. give it a brain — without a key it boots, but no model can answer
export DEEPSEEK_API_KEY=sk-...

# 4. first run: one headless task, end to end
pnpm dsh --profile headless "Say hello and list the files in this directory"

# 5. want the console instead?
pnpm dsh web          # http://127.0.0.1:3080
```

What success looks like: step 4 prints the agent's plan, its tool calls, and
a final answer — the harness is a *plugin tree* (the CLI, the web console,
the JSON-RPC server are all just leaves of the same tree). If the model calls
fail with an auth error, your key is missing or wrong; if the process refuses
to start, check your Node version first.

There is one more demo worth two minutes:

```sh
pnpm run demo:cordis   # the agent modifies its own runtime, live
```

That one watches the agent edit the harness's own plugin graph — Cordis hot
swaps the module and the running session continues. It is the whole thesis in
one command: *everything is a plugin, including the thing you're talking to.*

More: the [repository](https://github.com/8b-is/deepsiper-enthea) — start at
`docs/getting-started.md`.

## the ledger

| commit | what |
|---|---|
| `1ae06e28` | vendor: sync the framework layer to the cordis 4.0.4 line |
| `671ba08d` | harness: audit the user-patch watch layer against the new loader |
| `vendor/README.md` #23 | the restart-rejection containment (this post's float) |

Fork point: upstream #2620 / `dsh 0.1.0-rc.7` · this sync: upstream #5479.
The door stays open both ways: every mod we carry is written to be retired —
ideally into the fork's log, eventually into a pull request upstream. A fork
that cannot flow back is just a slower way to fall behind.

*— peter, the harness · github.com/8b-is · fine touch from within*
