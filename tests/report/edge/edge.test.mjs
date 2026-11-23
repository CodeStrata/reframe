// Offline test of the reports sign-in edge function (docs/sharing.md section 5). Run: node tests/report/edge/edge.test.mjs
import assert from "node:assert/strict";
import crypto from "node:crypto";
import { copyFileSync, mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const dir = mkdtempSync(join(tmpdir(), "edge-"));
copyFileSync(new URL("../../../src/reframe/infrastructure/terraform/reports/edge.mjs", import.meta.url), join(dir, "index.mjs"));
const C = { pool: "us-east-1_TEST", client: "client123", domain: "auth.example.test", region: "us-east-1", idp: "IdentityCenter" };
writeFileSync(join(dir, "config.json"), JSON.stringify(C));
const { publicKey, privateKey } = crypto.generateKeyPairSync("rsa", { modulusLength: 2048 });
const jwk = { ...publicKey.export({ format: "jwk" }), kid: "k1", alg: "RS256", use: "sig" };
const ISS = `https://cognito-idp.us-east-1.amazonaws.com/${C.pool}`;
const b64u = (o) => Buffer.from(typeof o === "string" ? o : JSON.stringify(o)).toString("base64url");
function token(claims, key = privateKey, kid = "k1") {
  const head = b64u({ alg: "RS256", kid }), body = b64u({ iss: ISS, aud: C.client, token_use: "id", exp: Math.floor(Date.now() / 1000) + 600, ...claims });
  return `${head}.${body}.${crypto.sign("RSA-SHA256", Buffer.from(`${head}.${body}`), key).toString("base64url")}`;
}
let tokenReply = null;
globalThis.fetch = async (url, options) => {
  if (String(url).endsWith("/.well-known/jwks.json")) return { ok: true, json: async () => ({ keys: [jwk] }) };
  if (String(url) === `https://${C.domain}/oauth2/token`) { const body = new URLSearchParams(options.body); assert.ok(body.get("code_verifier")); return tokenReply; }
  throw new Error("unexpected fetch " + url);
};
const { handler, valid } = await import(join(dir, "index.mjs"));
const event = (uri, cookie, querystring = "") => ({ Records: [{ cf: { request: { uri, querystring, headers: { host: [{ value: "d123.cloudfront.net" }], ...(cookie ? { cookie: [{ value: cookie }] } : {}) } } } }] });

assert.equal(await valid(token({})), true, "a good token");
assert.equal(await valid(token({ aud: "other" })), false, "another client's token");
assert.equal(await valid(token({ iss: "https://evil.example" })), false, "another issuer");
assert.equal(await valid(token({ exp: Math.floor(Date.now() / 1000) - 5 })), false, "expired");
assert.equal(await valid(token({ token_use: "access" })), false, "not an ID token");
const other = crypto.generateKeyPairSync("rsa", { modulusLength: 2048 }).privateKey;
assert.equal(await valid(token({}, other)), false, "signed by another key");
const good = token({});
assert.equal(await valid(good.slice(0, -4) + "AAAA"), false, "tampered signature");
assert.equal(await valid("not.a.token"), false, "garbage");

let out = await handler(event("/carddemo/bcc1e3/", `reframe_session=${good}`));
assert.equal(out.uri, "/carddemo/bcc1e3/index.html", "a signed-in request is served, folder to index.html");
assert.equal(out.headers.cookie, undefined, "the session is not passed to S3");

out = await handler(event("/carddemo/bcc1e3/", "reframe_session=forged"));
assert.equal(out.status, "302", "a forged session goes to the sign-in");
const location = new URL(out.headers.location[0].value);
assert.equal(location.host, C.domain);
assert.equal(location.searchParams.get("identity_provider"), "IdentityCenter");
assert.equal(location.searchParams.get("code_challenge_method"), "S256");
assert.equal(location.searchParams.get("redirect_uri"), "https://d123.cloudfront.net/_reframe/callback");
const pending = out.headers["set-cookie"][0].value.split(";")[0].split("=").slice(1).join("=");
const [state] = pending.split("|").map(decodeURIComponent);
assert.equal(location.searchParams.get("state"), state);

out = await handler(event("/_reframe/callback", `reframe_signin=${pending}`, "code=abc&state=wrong"));
assert.equal(out.status, "400", "a callback with another state is refused");
out = await handler(event("/_reframe/callback", "", `code=abc&state=${state}`));
assert.equal(out.status, "400", "a callback without the pending cookie is refused");

tokenReply = { ok: true, json: async () => ({ id_token: good }) };
out = await handler(event("/_reframe/callback", `reframe_signin=${pending}`, `code=abc&state=${state}`));
assert.equal(out.status, "302");
assert.equal(out.headers.location[0].value, "/carddemo/bcc1e3/", "back to the page asked for");
assert.match(out.headers["set-cookie"][0].value, /^reframe_session=.+; Path=\/; Secure; HttpOnly; SameSite=Lax/);

const offsite = `${encodeURIComponent("s1")}|${encodeURIComponent("v1")}|${encodeURIComponent("//evil.example/x")}`;
out = await handler(event("/_reframe/callback", `reframe_signin=${offsite}`, "code=abc&state=s1"));
assert.equal(out.headers.location[0].value, "/", "never back to another site");

tokenReply = { ok: true, json: async () => ({ id_token: token({ aud: "other" }) }) };
out = await handler(event("/_reframe/callback", `reframe_signin=${pending}`, `code=abc&state=${state}`));
assert.equal(out.status, "400", "a token for another client is refused at the callback");
console.log("edge sign-in: all checks passed");
