# archive/book — sources pulled from the live shelf

These `book/` directories were listed by `scripts/gen-book-index.mjs` but
had **no renderable manuscript**, so each produced a card whose link
(`./<slug>/`) resolved to nothing on the published site. They are kept
here, in the repo, out of the deployed tree (`build.mjs` copies `book/`
into `dist/book/`, so anything left in `book/` ships).

## archived

| slug | why it was dead | what is under it |
|------|-----------------|------------------|
| `chlo` | no `manuscript.html`; card → `./chlo/` → 404 | `chapters/*.md` + `ULTRA-SENSITIVE.md`: a complete markdown book. **Intimate third-party content** (a real person, with handle); it was publicly reachable at `/book/chlo/ULTRA-SENSITIVE.md` despite the card 404. Pulling it out of `book/` unpublishes it. |
| `cosmic-game-epub` | no `manuscript.html` | an EPUB skeleton (`OEBPS/nadasdy-voice.html`, `META-INF/`, `mimetype`) — packaging, not a manuscript |
| `cosmic-game-fanout` | no `manuscript.html` | the generation manifest `cosmic-game.toml` plus `cosmic-game-run.html` (a run/instructions page, not a book) |
| `flyxion-seeds` | no `manuscript.html` | `scaffold.toml` + an empty `chapters/` — never generated |
| `humm-flow` | no `manuscript.html` | `scaffold.toml` + `README.md` + an empty `chapters/` — never generated |

Rendered copies of `cosmic-game-fanout` still live under `demos/book/`
(html/epub/pdf); that surface is separate from `book/` and untouched.

## not archived — they actually serve

Two of the seven candidates resolve on the live site and were left in place:

| slug | card | live |
|------|------|------|
| `hn-five` | `./hn-five/` → `hn-five/index.html` | **200** (a standalone field page, "THE FIELD, TONIGHT") |
| `oreg-dimenziósakk` | `./oreg-dimenziósakk/manuscript.html` | **200** (title `AZ ÖREG ÉS A DIMENZIÓSAKK`) |

Declaring either an orphan would have broken a working link, so they stay.
After the move the index has 73 books and **0 dead links** (checked).

*pocoo.vaked.dev · the sovereign library · 2026-10-13*
