import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, copyFile, writeFile, readFile, symlink, rm } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = fileURLToPath(new URL('../', import.meta.url));
test('build exports frontmatter metadata and preserves citations after static copy', async () => {
  const fixture = await mkdtemp(path.join(root, '.citation-test-'));
  try {
    for (const dir of ['posts', 'assets', 'scripts', '.well-known']) {
      await mkdir(path.join(fixture, dir));
    }
    await copyFile(path.join(root, 'build.mjs'), path.join(fixture, 'build.mjs'));
    await symlink(path.join(root, 'node_modules'), path.join(fixture, 'node_modules'), 'dir');
    // Catalog generation is unrelated to citation exports; keep this test bounded.
    await writeFile(path.join(fixture, 'scripts/gen-catalog.mjs'), '// fixture catalog stub\n');
    await writeFile(path.join(fixture, '.well-known/security.txt'), 'fixture security contact');
    await writeFile(path.join(fixture, 'posts/published.md'), `---
title: "Citation fixture"
date: 2025-02-03
description: "A metadata regression fixture"
tags: [test]
draft: false
---
# Citation fixture
`);
    await writeFile(path.join(fixture, 'posts/draft.md'), `---
title: "Unpublished fixture"
date: 2025-03-04
draft: true
---
Draft.
`);
    execFileSync(process.execPath, ['build.mjs'], { cwd: fixture, timeout: 15000, stdio: 'pipe' });
    const bib = await readFile(path.join(fixture, 'dist/citations.bib'), 'utf8');
    assert.match(bib, /title = \{Citation fixture\}/);
    assert.match(bib, /year = \{2025\}/);
    assert.match(bib, /month = \{feb\}/);
    assert.doesNotMatch(bib, /undefined|Unpublished fixture/);
    const citations = JSON.parse(await readFile(path.join(fixture, 'dist/.well-known/citations.json'), 'utf8'));
    assert.equal(citations.works.length, 1);
    assert.equal(citations.works[0].headline, 'Citation fixture');
    assert.equal(citations.works[0].datePublished, '2025-02-03');
    assert.equal(citations.works[0].description, 'A metadata regression fixture');
    assert.equal(await readFile(path.join(fixture, 'dist/.well-known/security.txt'), 'utf8'), 'fixture security contact');
  } finally {
    await rm(fixture, { recursive: true, force: true });
  }
});
