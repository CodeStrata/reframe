// Renders every view of a review page with a stub DOM, to catch errors in the page's script without a browser.
// node tests/report/render.js <page.html> -> prints one JSON line per view: {"view", "ok", "error", "length", "text"}
const fs = require('fs');
const html = fs.readFileSync(process.argv[2], 'utf8');
const data = html.match(/<script id="data" type="application\/json">([\s\S]*?)<\/script>/)[1];
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const handlers = {};
function el(id) {
  return {id, innerHTML: '', textContent: '', value: '', hidden: false, className: '', dataset: {}, style: {},
    classList: {toggle() {}, add() {}, remove() {}}, addEventListener() {}, showModal() {}, close() {}, focus() {}, setSelectionRange() {},
    scrollIntoView() {}, closest() { return null; }};
}
const els = {};
global.document = {
  getElementById: id => id === 'data' ? {textContent: data.replace(/<\\\//g, '</')} : (els[id] || (els[id] = el(id))),
  addEventListener: (type, fn) => (handlers[type] = handlers[type] || []).push(fn),
  querySelector: () => null, activeElement: null, body: {appendChild() {}},
  createElement: () => el('x'),
};
global.location = {hash: ''};
global.window = {addEventListener() {}, scrollTo() {}};
global.localStorage = {store: {}, getItem(k) { return this.store[k] || null; }, setItem(k, v) { this.store[k] = String(v); }};
global.confirm = () => false; global.prompt = () => 'Tester';
global.URL = {createObjectURL: () => ''}; global.Blob = function () {};
const run = new Function(script + '\n;return {route, D, firstGroups: typeof firstGroups === "function" ? firstGroups : null};');
const out = [];
let api;
try { api = run(); } catch (e) { console.log(JSON.stringify({view: 'load', ok: false, error: String(e.stack)})); process.exit(0); }
const views = ['', '#/', '#/first', '#/d/0', '#/f/0', '#/c/0', '#/tech/requirements', '#/tech/rules', '#/tech/questions', '#/tech/sme', '#/tech/assessment', '#/search/the'];
for (const v of views) {
  location.hash = v;
  try { api.route(); out.push({view: v, ok: true, length: els.main.innerHTML.length, text: els.main.innerHTML}); }
  catch (e) { out.push({view: v, ok: false, error: String(e.stack)}); }
}
for (const o of out) console.log(JSON.stringify(o));
