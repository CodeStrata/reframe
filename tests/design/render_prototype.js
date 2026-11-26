// Renders every route of the prototype with a stub DOM, and runs an action, the legacy panel and the review panel on each
// screen, to catch errors in the page's script without a browser.
// node tests/design/render_prototype.js <index.html> -> one JSON line per route: {"route", "ok", "error", "html", "banner", "legacy", "review"}
const fs = require('fs');
const html = fs.readFileSync(process.argv[2], 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
function el(id) {
  return {id, innerHTML: '', textContent: '', value: '', hidden: true, dataset: {}, style: {}, addEventListener() {}, showModal() {}, close() {},
    focus() {}, scrollIntoView() {}, setAttribute() {}, closest() { return null; }};
}
const els = {};
global.document = {getElementById: id => els[id] || (els[id] = el(id)), addEventListener() {}, querySelector: () => null, title: '',
  body: {appendChild() {}}, createElement: () => el('x')};
global.CSS = {escape: s => s};
global.location = {hash: ''};
global.window = {addEventListener() {}, scrollTo() {}};
global.localStorage = {store: {}, getItem(k) { return this.store[k] || null; }, setItem(k, v) { this.store[k] = String(v); }};
global.URL = {createObjectURL: () => ''}; global.Blob = function () {};
let api;
try { api = new Function(script + '\n;return {render, act, legacyPanel, reviewPanel, rows, D, byId};')(); }
catch (e) { console.log(JSON.stringify({route: 'load', ok: false, error: String(e.stack)})); process.exit(0); }
const routes = [''].concat(api.D.screens.map(s => '#/' + s.id), ['#/journeys', '#/NO-SUCH-SCREEN']);
for (const r of routes) {
  location.hash = r;
  const out = {route: r, ok: true};
  try {
    api.render();
    out.html = els.main.innerHTML;
    const s = api.byId[decodeURIComponent(r.replace(/^#\/?/, ''))];
    if (s) {
      const button = s.components.find(c => c.type === 'button' && !c.goes_to) || {label: 'Go'};
      const required = s.components.filter(c => c.required).length;
      out.required = required;
      api.act(s, button);
      out.banner = els.banner.innerHTML;
      out.legacy = api.legacyPanel(s);
      out.review = api.reviewPanel(s);
    }
  } catch (e) { out.ok = false; out.error = String(e.stack); }
  console.log(JSON.stringify(out));
}
