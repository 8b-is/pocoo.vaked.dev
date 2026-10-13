# illustration spec — pocoo research post (liquid-rust / Phoenix Protocol)

Follow this spec for every figure. Produce a single self-contained SVG file.

## canvas
- viewBox width 1200, height as noted per figure
- no external fonts, no external images, no scripts
- monospace family: `font-family="ui-monospace,SFMono-Regular,Menlo,monospace"`
- serif family: `font-family="Georgia,serif"`

## palette (exact)
- background `#05060a`, panel `#0b0f19`, panel2 `#0e1424`
- ink `#cfc9dd`, dim `#7f7c99`, faint `#5b577a`
- mint `#62e6c9` (accent / primary), gold `#e8b05c` (secondary), violet `#b48bff`
- pink `#ff4d9d`, cyan `#00f0ff`
- grid line `rgba(170,150,255,0.18)`, box border `rgba(170,150,255,0.28)`

## style
- dark, precise, technical; thin 1px strokes; rounded rects (rx 10)
- uppercase kickers with letter-spacing 3–4
- labels small (11–14px), headings 20–30px
- arrows: simple line + small triangle marker, 1.5px
- no gradients except a single soft radial vignette if it helps
- always visually legible; avoid clutter; leave breathing room
- include a small caption at the bottom: monospace, `#5b577a`, 11px, letter-spacing 2
