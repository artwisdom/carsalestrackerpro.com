import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

const source = readFileSync(new URL('../assets/newsletter.js', import.meta.url), 'utf8');

class FakeElement {
  constructor(tag) {
    this.tagName = tag.toUpperCase();
    this.attributes = {};
    this.children = [];
    this.listeners = {};
    this.parentNode = null;
    this.textContent = '';
    this.disabled = false;
  }

  setAttribute(name, value) { this.attributes[name] = String(value); }
  getAttribute(name) { return this.attributes[name] ?? null; }
  appendChild(child) {
    child.parentNode = this;
    this.children.push(child);
    return child;
  }
  addEventListener(type, listener) {
    (this.listeners[type] ||= []).push(listener);
  }
  fire(type) {
    const event = {
      type,
      defaultPrevented: false,
      preventDefault() { this.defaultPrevented = true; }
    };
    for (const listener of this.listeners[type] || []) listener.call(this, event);
    return event;
  }
  replaceWith(replacement) {
    const index = this.parentNode.children.indexOf(this);
    replacement.parentNode = this.parentNode;
    this.parentNode.children.splice(index, 1, replacement);
    this.parentNode = null;
  }
  insertAdjacentElement(_where, element) {
    this.inserted = element;
    element.parentNode = this;
    this.children.push(element);
  }
  querySelector() { return null; }
}

function descendants(root) {
  const found = [];
  (function visit(node) {
    if (!(node instanceof FakeElement)) return;
    found.push(node);
    node.children.forEach(visit);
  })(root);
  return found;
}

function createFixture() {
  const mount = new FakeElement('div');
  mount.setAttribute('data-dod-mount', 'landing');
  const head = new FakeElement('head');
  const timers = [];
  const document = {
    readyState: 'complete',
    head,
    createElement: tag => new FakeElement(tag),
    createTextNode: text => ({ nodeType: 3, textContent: text, parentNode: null }),
    addEventListener() {},
    querySelector(selector) {
      if (selector === '[data-dod-mount]') return mount;
      return null;
    }
  };
  const context = {
    document,
    location: { pathname: '/brief/', href: 'http://127.0.0.1:4175/brief/' },
    setTimeout(callback, delay) {
      timers.push({ callback, delay });
      return timers.length;
    }
  };
  vm.runInNewContext(source, context, { filename: 'assets/newsletter.js' });
  const nodes = () => descendants(mount.inserted);
  return {
    mount,
    timers,
    nodes,
    find: predicate => nodes().find(predicate),
    findAll: predicate => nodes().filter(predicate)
  };
}

test('uses the real Buttondown endpoint in a visible provider-owned tab', () => {
  const page = createFixture();
  const form = page.find(node => node.tagName === 'FORM');
  const inputs = page.findAll(node => node.tagName === 'INPUT');

  assert.equal(form.getAttribute('action'), 'https://buttondown.com/api/emails/embed-subscribe/dealeropsdaily');
  assert.equal(form.getAttribute('method'), 'post');
  assert.equal(form.getAttribute('target'), '_blank');
  assert.match(form.getAttribute('rel'), /noopener/);
  assert.equal(inputs.find(input => input.getAttribute('name') === 'email').getAttribute('required'), '');
  assert.equal(inputs.find(input => input.getAttribute('name') === 'tag').getAttribute('value'), 'web-landing');
  assert.equal(inputs.find(input => input.getAttribute('name') === 'referrer_url').getAttribute('value'), 'http://127.0.0.1:4175/brief/');
  assert.equal(page.find(node => node.tagName === 'IFRAME'), undefined);
});

test('a blocked provider request cannot produce a false confirmation claim', () => {
  const page = createFixture();
  const form = page.find(node => node.tagName === 'FORM');
  const submit = form.fire('submit');

  // No provider response occurs in this fixture. Run any fallback timers anyway.
  page.timers.forEach(timer => timer.callback());

  assert.equal(submit.defaultPrevented, false, 'native form submission must continue');
  assert.ok(page.nodes().includes(form), 'the form must remain available after an unverifiable outcome');
  assert.equal(page.find(node => node.getAttribute('role') === 'status').textContent,
    'Finish in the Buttondown tab. If it did not open, use “Open signup again.”');
  assert.notEqual(page.find(node => node.tagName === 'BUTTON').disabled, true);
  assert.equal(page.timers.length, 0, 'no timer may claim provider success');
});

test('the visitor can retry without losing the email form', () => {
  const page = createFixture();
  const form = page.find(node => node.tagName === 'FORM');

  form.fire('submit');
  form.fire('submit');

  assert.ok(page.nodes().includes(form));
  assert.equal(page.find(node => node.tagName === 'BUTTON').textContent, 'Open signup again');
  assert.equal(page.findAll(node => node.getAttribute('role') === 'status').length, 1);
});
