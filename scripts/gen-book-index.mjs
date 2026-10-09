// gen-book-index.mjs — build book/index.html from the book/ manuscripts.
//
// The book/ folder is the standalone HTML library: each child is a self-
// contained manuscript.html. Nothing indexed it, so /book/ was a 404 with
// 70 orphaned surfaces. This lists them, so every book has a door.
import { readdirSync, readFileSync, writeFileSync, existsSync, statSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const BOOK_DIR = path.join(ROOT, "book");
const OUT = path.join(BOOK_DIR, "index.html");

function decode(s) {
  return s
    .replace(/&(amp|lt|gt|quot|#39|nbsp|mdash|ndash);/g, (_, e) =>
      ({ amp: "&", lt: "<", gt: ">", quot: '"', "#39": "'", nbsp: " ", mdash: "—", ndash: "–" }[e]))
    .replace(/<[^>]*>/g, "")
    .replace(/\s+/g, " ")
    .trim();
}
function esc(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
function titleOf(dir, slug) {
  const man = path.join(dir, "manuscript.html");
  if (existsSync(man)) {
    const html = readFileSync(man, "utf8");
    const t = html.match(/<title>([\s\S]*?)<\/title>/i);
    if (t && decode(t[1])) return decode(t[1]).split(" — ")[0].split(" · ")[0];
    const h = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
    if (h && decode(h[1])) return decode(h[1]);
  }
  return slug.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}
function subOf(dir) {
  const man = path.join(dir, "manuscript.html");
  if (!existsSync(man)) return "";
  const html = readFileSync(man, "utf8");
  const t = html.match(/<title>([\s\S]*?)<\/title>/i);
  if (!t) return "";
  const parts = decode(t[1]).split(/\s+—\s+|\s+·\s+/);
  return parts.slice(1).join(" · ");
}

const entries = [];
for (const name of readdirSync(BOOK_DIR)) {
  if (name === "index.html") continue;
  const dir = path.join(BOOK_DIR, name);
  if (!statSync(dir).isDirectory()) continue;
  const man = path.join(dir, "manuscript.html");
  const href = existsSync(man) ? `./${name}/manuscript.html` : `./${name}/`;
  entries.push({ slug: name, title: titleOf(dir, name), sub: subOf(dir), href });
}
entries.sort((a, b) => a.title.localeCompare(b.title));

const cards = entries
  .map(
    (e) => `      <a class="card" href="${esc(e.href)}">
        <div class="t">${esc(e.title)}</div>
        ${e.sub ? `<div class="s">${esc(e.sub)}</div>` : ""}
        <div class="slug">${esc(e.slug)}</div>
      </a>`,
  )
  .join("\n");

const html = `<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>the sovereign library · ${entries.length} books · pocoo.vaked.dev</title>
<meta name="description" content="The standalone HTML book library of pocoo.vaked.dev — ${entries.length} sovereign books, each a self-contained manuscript.">
<style>
  :root{--bg:#05060a;--ink:#cfc9dd;--dim:#7f7c99;--gold:#e8b05c;--mint:#62e6c9;--line:rgba(170,150,255,.18)}
  *{box-sizing:border-box}
  body{margin:0;background:radial-gradient(ellipse at 50% -10%,#0d1220 0%,var(--bg) 60%);color:var(--ink);font-family:Georgia,serif;min-height:100vh}
  header{max-width:1000px;margin:0 auto;padding:48px 20px 8px;text-align:center}
  .kicker{font-family:ui-monospace,monospace;font-size:.7rem;letter-spacing:.36em;text-transform:uppercase;color:var(--dim)}
  h1{font-family:ui-monospace,monospace;font-size:1.5rem;letter-spacing:.32em;color:var(--gold);font-weight:600;margin:.5rem 0}
  .sub{color:var(--dim);font-style:italic;font-size:.92rem}
  main{max-width:1000px;margin:0 auto;padding:24px 20px 90px;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}
  .card{display:block;text-decoration:none;color:inherit;border:1px solid var(--line);border-radius:12px;padding:14px 16px;background:rgba(255,255,255,.02);transition:border-color .15s,transform .15s}
  .card:hover{border-color:var(--mint);transform:translateY(-1px)}
  .card .t{font-family:ui-monospace,monospace;font-size:.82rem;letter-spacing:.02em;color:#e9e4f5;line-height:1.35}
  .card .s{color:var(--dim);font-size:.78rem;margin-top:4px;font-style:italic}
  .card .slug{font-family:ui-monospace,monospace;font-size:.62rem;color:#5b577a;margin-top:8px;letter-spacing:.06em}
  footer{text-align:center;padding:0 20px 60px;font-family:ui-monospace,monospace;font-size:.68rem;color:var(--dim);letter-spacing:.2em}
  footer a{color:var(--mint);text-decoration:none}
</style>
</head>
<body>
<header>
  <div class="kicker">pocoo.vaked.dev</div>
  <h1>THE SOVEREIGN LIBRARY</h1>
  <div class="sub">${entries.length} standalone books · each a self-contained manuscript</div>
</header>
<main>
${cards}
</main>
<footer>
  the sovereign library · <a href="https://pocoo.vaked.dev/demos/book/">demos/book catalog</a> · 0 + 1 · fine touch from within · om mani padme hum
</footer>
</body>
</html>
`;

writeFileSync(OUT, html);
console.log(`book index: ${entries.length} books → book/index.html`);
