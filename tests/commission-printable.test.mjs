import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

const html = readFileSync(new URL('../tools/car-salesman-commission-calculator/index.html', import.meta.url), 'utf8');
const inline = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);

test('one optional paid printable follows the result before newsletter and free tracker', () => {
  assert.equal((html.match(/class="commission-printable"/g) || []).length, 1);
  assert.match(html, /id="shareStatus"[\s\S]*?<\/section>\s*<aside class="commission-printable"/);
  assert.match(html, /<\/aside>\s*<div data-dod-mount="calculator"><\/div>\s*<div class="cta-box">/);
  assert.equal((html.match(/https:\/\/www.etsy.com\/listing\//g) || []).length, 1);
  assert.match(html, /Optional paid printable/);
  assert.match(html, /16-page PDF · US Letter \+ A4 · Digital download, no physical item/);
  assert.match(html, /our own Andromeda Kinship Etsy shop/);
  assert.match(html, /Current price and purchase terms on Etsy/);
  assert.match(html, /The calculator and web tracker stay free/);
  assert.match(html, /href="\/tracker\/">Open the free tracker/);
  assert.doesNotMatch(html, /\$9\.97|priceCurrency.*9\.97/);
});

test('paid link is accessible, opens safely, and transmits no calculator data', () => {
  assert.match(html, /href="https:\/\/www.etsy.com\/listing\/4538788064\/car-sales-commission-tracker-printable" target="_blank" rel="noopener noreferrer" aria-describedby="printable-link-note"/);
  assert.match(html, /aria-labelledby="commission-printable-title"/);
  assert.match(html, /id="printable-link-note">[^<]*Opens in a new tab/);
  assert.equal(inline.length, 1);
  assert.doesNotMatch(inline[0], /fetch\(|XMLHttpRequest|sendBeacon|localStorage|cookie|dataLayer|gtag|etsy/);
});

function calculator() {
  const values = { units:12,front:1800,back:0,rate:25,backRate:0,pack:0,base:0,miniThresh:1000,miniAmt:150 };
  const elements = {};
  const get = id => elements[id] ||= { value: String(values[id] ?? ''), textContent:'', attributes:{}, events:{}, classList:{toggle(){}}, setAttribute(k,v){this.attributes[k]=v}, addEventListener(k,fn){this.events[k]=fn} };
  vm.runInNewContext(inline[0], { document:{getElementById:get}, Intl, navigator:{} });
  return {
    get,
    set(values) { for (const [k,v] of Object.entries(values)) get(k).value=String(v); get('units').events.input(); },
    click(id) { get(id).events.click.call(get(id)); }
  };
}

test('free calculator retains baseline math, repeat edits, minis and back-end pay', () => {
  const c=calculator();
  assert.equal(c.get('outTotal').textContent,'$5,400');
  c.set({units:10,front:2000,pack:500,back:1000,backRate:5,base:1000});
  assert.equal(c.get('outTotal').textContent,'$5,250');
  c.set({front:900}); c.click('miniSw');
  assert.equal(c.get('miniSw').attributes['aria-checked'],true);
  assert.equal(c.get('outTotal').textContent,'$3,000');
  c.click('miniSw'); assert.equal(c.get('outTotal').textContent,'$2,500');
  c.set({units:0,base:0}); assert.equal(c.get('outTotal').textContent,'$0');
  c.set({units:-1}); assert.equal(c.get('outTotal').textContent,'$0');
});

test('copy/share fallback remains usable without clipboard or share APIs', () => {
  const c=calculator();
  c.click('copyEstimate'); assert.equal(c.get('shareStatus').textContent,'Copy was unavailable in this browser.');
  c.click('shareCalculator'); assert.equal(c.get('shareStatus').textContent,'Copy was unavailable in this browser.');
});
