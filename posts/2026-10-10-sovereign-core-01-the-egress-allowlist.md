---
title: "Sovereign Core, part 1 — the egress allowlist: a hot path that allocates nothing"
date: 2026-10-10
description: "A browser that proves what it sends needs an allowlist you can read and trust. Here is the whole thing: four hosts, byte slices, a length gate, and zero heap on the decision path — with the micro-optimization that made it cleaner, not just faster."
tags: [engineering, rust, sovereign-core, qwave, simd, zero-alloc, performance]
draft: false
---

# Sovereign Core, part 1 — the egress allowlist

*A multipart deep dive into the core the constellation runs on. Part 1 of 6.*

---

A privacy browser's most load-bearing claim is also its smallest piece of code:
**the set of hosts its own code is allowed to contact**. If you cannot read that
list in one breath, "prove what it sends" is a slogan. In Qwave it is
`core/src/egress.rs` — 137 lines, four hosts, one C ABI.

## The whole policy

```rust
pub const HOSTS: [&str; 4] = [
    "github.com",      // auto-update feed (Sparkle), user-consented
    "api.x.ai",        // the remote AI provider's default endpoint (off by default)
    "duckduckgo.com",  // omnibox autocomplete (off by default)
    "ac.ecosia.org",
];
```

That is the entire Category-A surface. Favicon and remote-markdown fetches are
*deliberately absent* — their host is whatever page you navigated to, so they
cannot be allowlisted to a fixed set. The absence is the security property.

## The decision is a byte comparison

No regex, no DNS, no `format!`, no heap. `permits(host)` folds once, then walks
four entries doing slice equality and a boundary-aware suffix check:

```rust
pub fn permits(host: &str) -> bool {
    let bytes = host.trim().as_bytes();
    if bytes.is_empty() || !bytes.is_ascii() { return false; }

    let mut folded = [0u8; 253];                 // max hostname, on the stack
    if bytes.len() > folded.len() { return false; }
    folded[..bytes.len()].copy_from_slice(bytes);
    folded[..bytes.len()].make_ascii_lowercase();
    let folded = &folded[..bytes.len()];

    HOSTS.iter().any(|allowed| {
        let a = allowed.as_bytes();
        if folded == a { return true; }
        folded.len() > a.len() && {              // length gate first
            let start = folded.len() - a.len() - 1;
            folded[start] == b'.' && &folded[start + 1..] == a
        }
    })
}
```

Three properties worth naming:

1. **Zero allocation.** The folded host lives in a fixed 253-byte stack buffer
   (the DNS name limit), not the heap. The hot decision never touches the
   allocator.
2. **Length-gated.** A host shorter than an entry can never suffix-match it, so
   the slice arithmetic is skipped before any bytes are compared.
3. **Boundary-aware.** The subdomain rule requires the separator `.` — which is
   why `objects.githubusercontent.com` is correctly *rejected* (it ends in
   `.githubusercontent.com`, not `.github.com`). That exact counterexample is a
   test, not a comment.

## The micro-optimization that made it cleaner

The original fold was a hand-rolled loop:

```rust
for (i, b) in bytes.iter().enumerate() { folded[i] = b.to_ascii_lowercase(); }
```

We replaced it with a bulk copy plus the slice method:

```rust
folded[..bytes.len()].copy_from_slice(bytes);
folded[..bytes.len()].make_ascii_lowercase();
```

`make_ascii_lowercase` on a slice is the vectorizable primitive, and the code
got *simpler* — fewer moving parts, no index management. Performance work that
makes the code easier to read is the only kind worth committing here.

## The ABI

The Swift side does not re-implement any of this. One C function:

```rust
#[unsafe(no_mangle)]
pub unsafe extern "C" fn qw_egress_permits(host: *const c_char) -> bool;
```

Null, empty, and non-UTF8 hosts are never permitted. The core is a zero-dependency
staticlib; the policy lives in Rust; the app asks a question and gets a boolean.

## Receipts

- `core/src/egress.rs` — 6 tests: exact matches, subdomains-not-lookalikes,
  the `githubusercontent` counterexample, empty/garbage, the departed VPN host,
  Ecosia autocomplete.
- The whole core: **44 tests green**, `cargo fmt`-clean.
- The hot path allocates nothing — a property asserted by construction (stack
  buffer) and by the test suite.

*Next: [part 2 — the 79-byte wave frame](/posts/2026-10-10-sovereign-core-02-the-79-byte-wave-frame).*

*prove it, don't assert it · 0 + 1 · fine touch from within*
