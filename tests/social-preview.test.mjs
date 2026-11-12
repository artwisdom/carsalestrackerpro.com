import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import test from 'node:test';

const root = new URL('../', import.meta.url);
const cardUrl = 'https://carsalestrackerpro.com/assets/og-card-brand-v2.png';
const read = path => readFileSync(new URL(path, root));

test('share-card source embeds the exact existing app logo', () => {
  const svg = read('assets/og-card.svg').toString();
  const embedded = svg.match(/href="data:image\/png;base64,([A-Za-z0-9+/=]+)"/);
  assert.ok(embedded, 'The existing logo must be embedded, not approximated');
  assert.deepEqual(Buffer.from(embedded[1], 'base64'), read('assets/icon.png'));
  assert.equal((svg.match(/<image\b/g) || []).length, 1);
  assert.match(svg, /clip-path="url\(#app-icon-corners\)"/);
});

test('versioned and compatibility PNGs are the same 1200 by 630 card', () => {
  const png = read('assets/og-card-brand-v2.png');
  assert.deepEqual(png.subarray(0, 8), Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]));
  assert.equal(png.readUInt32BE(16), 1200);
  assert.equal(png.readUInt32BE(20), 630);
  assert.ok(png.length < 500_000, 'Keep the share image small enough to fetch quickly');
  assert.deepEqual(read('assets/og-card.png'), png);
});

function htmlFiles(directory) {
  return readdirSync(new URL(directory, root), { withFileTypes: true }).flatMap(entry => {
    if (entry.name.startsWith('.')) return [];
    const path = join(directory, entry.name);
    return entry.isDirectory() ? htmlFiles(path + '/') : path.endsWith('.html') ? [path] : [];
  });
}

test('all shared-brand pages use the versioned image and complete preview metadata', () => {
  let sharedCards = 0;
  for (const path of htmlFiles('')) {
    const html = read(path).toString();
    assert.ok(!html.includes('https://carsalestrackerpro.com/assets/og-card.png'), `${path}: stale image URL`);
    if (!html.includes(cardUrl)) continue;
    sharedCards++;
    for (const tag of [
      `<meta property="og:image" content="${cardUrl}">`,
      '<meta property="og:image:width" content="1200">',
      '<meta property="og:image:height" content="630">',
      '<meta property="og:image:type" content="image/png">',
      `<meta name="twitter:image" content="${cardUrl}">`,
    ]) assert.equal(html.split(tag).length - 1, 1, `${path}: ${tag}`);
    assert.match(html, /<meta property="og:image:alt" content="CarSales Tracker Pro car-and-arrow logo\./);
    assert.match(html, /<meta name="twitter:image:alt" content="CarSales Tracker Pro car-and-arrow logo\./);
  }
  assert.ok(sharedCards >= 32, 'Cover the homepage, guides, tracker, tools, and invite pages');
});
