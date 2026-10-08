# AGENTS.md — `pocoo.vaked.dev`

> **Static blog at pocoo.vaked.dev** — custom Node builder (`build.mjs`) → `dist/` → Cloudflare Pages (git integration on `main`).

## Publish pipeline (draft → live post)

Posts are long-form markdown in `posts/YYYY-MM-DD-slug.md`. The source drafts
for the Qwave performance series live in the separate `qwave` repo at
`blog-drafts/`; publishing means transforming a draft into a `posts/` file.

1. **Frontmatter** (exact keys the builder reads):
   ```yaml
   ---
   title: "Title Case Title"
   date: 2026-08-13
   description: "One-or-two-sentence summary (used for og:description, RSS, index)."
   tags: [swift, performance, ...]
   draft: false
   ---
   ```
   Drop `status`/`measured_on`/`corrections`; fold that nuance into the body.
2. **Body** starts `# Sentence-case title` then the byline, then `---`:
   `*qwave · <topic> · fine touch from within · vaked.dev*`
3. **Image paths are absolute and always live in `assets/qwave/`:**
   `![alt](/assets/qwave/<file>.svg)` — never a relative `assets/…`, never a
   filesystem path. Copy the SVG into `assets/qwave/` and validate with
   `xmllint --noout`.
4. **Cross-links to sister posts use `/posts/<slug>.html`**, not `.md` and not
   GitHub blob URLs.
5. **OG card:** each post's social card is `assets/og/<slug>.svg`. After
   adding or editing a post run `uv run scripts/generate_og_images.py`
   (manual step — a missing card 404s the post's `og:image`, and the build
   will not generate one for you).
6. **Build + deploy:**
   ```bash
   npm run build          # renders dist/, prints "N post(s), 0 draft(s) skipped"
   git add posts/ assets/ && git commit -m "post: …" && git push origin main
   ```
   Cloudflare Pages rebuilds on push to `main` (~20–30 s). Verify each
   `/posts/<slug>.html` returns 200.

## Sections — the `research` feed

A post may opt into a section with extra frontmatter keys; sections render
their own index page and are linked from the home header.

```yaml
section: research        # opt this post into /research/
series: pocoo-research   # optional: group related posts
series_index: 1          # optional: ordering within the series
```

`build.mjs` collects every post whose `meta.section === "research"` into
`dist/research/index.html` (`renderResearch`) and adds `/research/` to
`sitemap.xml`. The section index links posts with `../posts/<slug>` and
thumbnails with `../assets/og/<slug>.svg`, so the page must stay at the site
root. To start another section, point `renderResearch` at a new `section`
value and add the matching nav link + `mkdir`/`writeFile` in `main()`.

## Remotes — push to BOTH, or the site silently 404s

This repo has two remotes and they drift:

| Remote | URL | Role |
|--------|-----|------|
| `origin` | `https://github.com/peterlodri-sec/pocoo.vaked.dev.git` | **Cloudflare Pages builds from this one.** |
| `upstream` | `git@github-peterlodri-sec:8b-is/pocoo.vaked.dev.git` | org mirror (tracking branch for local `main`). |

Because local `main` tracks `upstream`, a plain `git push` goes to the mirror
and **the live site does not update** — Pages keeps serving the stale
`origin/main` tree. New pages 404 even though they are committed, built, and
present in `dist/`.

```bash
git push origin main && git push upstream main
```

Diagnose with `git log --oneline origin/main..main` — a non-empty list means the
live site is behind. The Cloudflare `_redirects` splat rules are *not* the
cause of book 404s; confirm deploy state before touching them.

## Illustrations (entheai)

Generated SVGs come from the entheai engine via the `vaked` provider — see the
global `entheai-bridge` skill ("Image / SVG generation") for the working
endpoint, the `deepseek/deepseek-v3.2` model choice, and the recurring
Google-Fonts `@import` XML-invalidity fix. Hand-polish layout after generation.

## Library catalog (demos/book) — generated, never hand-edited

`demos/book/index.html` is produced by `scripts/gen-catalog.mjs`: it scans
every `demos/book/*.html`, pulls title + seal, appends `html`/`pdf`/`epub`
links (siblings ≤20 MB — the Pages cap `build.mjs` enforces), and renders the
card head through `scripts/gen-catalog.wasm` (`render_book`).

- **Layout rule**: title/seal/entry/out are fixed scratch regions, reused per
  book. Nothing may advance with the book count — advancing buffers collided
  and corrupted titles (mojibake, template fragments) past the first few rows.
- Titles are HTML-escaped and cleaned (entities decoded, controls stripped,
  NFC, whitespace collapsed); fallback chain `<title>` → `<h1>` → filename.
- Rebuild the WASM after editing the `.wat`:
  `npx -y -p wabt wat2wasm scripts/gen-catalog.wat -o scripts/gen-catalog.wasm`
- `build.mjs` runs the generator **before** copying `demos/` to `dist/` —
  never reorder that pair, or dist ships a stale catalog.
- Skin: the constellation ink (`--pink #FF4D9D` on `--bg #1A0F1E`, mono,
  sha256 ledger rows), with a start-here link to the declaration.

## Conventions

- `markdown-it` is configured with `html: false` — no raw HTML in posts; use
  markdown image syntax for SVGs.
- Posts are sorted by `date` (then filename); multiple posts may share a date.
- **Commit promptly.** This repo and `qwave` have concurrent agents working the
  same files; uncommitted work is at risk of being clobbered by a `git reset`/`pull`.
