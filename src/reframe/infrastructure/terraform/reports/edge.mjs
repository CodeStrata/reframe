// Reframe reports: the AWS sign-in before any page (docs/sharing.md, section 5). A CloudFront viewer-request function.
// A request with a valid session (Cognito ID token: RS256 signature from the user pool's keys, issuer, audience, expiry)
// is served; any other request is sent to the sign-in (Cognito, federated with IAM Identity Center) with PKCE and a
// one-time state bound to a short-lived cookie. config.json holds the user pool, client, domain and identity provider.
import crypto from "node:crypto";
import { readFileSync } from "node:fs";

const C = JSON.parse(readFileSync(new URL("./config.json", import.meta.url), "utf8"));
const ISSUER = `https://cognito-idp.${C.region}.amazonaws.com/${C.pool}`;
const SESSION = "reframe_session";
const PENDING = "reframe_signin";
let keys = null;

const b64url = (text) => Buffer.from(text.replace(/-/g, "+").replace(/_/g, "/"), "base64");

async function signingKeys() {
  if (!keys) {
    const reply = await fetch(`${ISSUER}/.well-known/jwks.json`);
    keys = (await reply.json()).keys;
  }
  return keys;
}

export async function valid(token, now = Date.now()) {
  try {
    const [head, body, signature] = String(token).split(".");
    const header = JSON.parse(b64url(head));
    if (header.alg !== "RS256") return false;
    const key = (await signingKeys()).find((k) => k.kid === header.kid);
    if (!key) return false;
    const signed = crypto.verify("RSA-SHA256", Buffer.from(`${head}.${body}`), crypto.createPublicKey({ key, format: "jwk" }), b64url(signature));
    if (!signed) return false;
    const claims = JSON.parse(b64url(body));
    return claims.iss === ISSUER && claims.aud === C.client && claims.token_use === "id" && claims.exp * 1000 > now;
  } catch {
    return false;
  }
}

function cookies(headers) {
  const jar = {};
  for (const header of headers.cookie || []) {
    for (const part of header.value.split(";")) {
      const at = part.indexOf("=");
      if (at > 0) jar[part.slice(0, at).trim()] = part.slice(at + 1).trim();
    }
  }
  return jar;
}

const noStore = { "cache-control": [{ key: "Cache-Control", value: "no-store" }] };

function redirect(location, setCookies = []) {
  const headers = { location: [{ key: "Location", value: location }], ...noStore };
  if (setCookies.length) headers["set-cookie"] = setCookies.map((value) => ({ key: "Set-Cookie", value }));
  return { status: "302", statusDescription: "Found", headers };
}

function refuse(message) {
  return { status: "400", statusDescription: "Bad Request", headers: { "content-type": [{ key: "Content-Type", value: "text/plain; charset=utf-8" }], ...noStore }, body: message };
}

const safePath = (target) => (typeof target === "string" && target.startsWith("/") && !target.startsWith("//") && !target.includes("\\") ? target : "/");

export const handler = async (event) => {
  const request = event.Records[0].cf.request;
  const host = request.headers.host[0].value;
  const back = `https://${host}/_reframe/callback`;
  const jar = cookies(request.headers);

  if (request.uri === "/_reframe/callback") {
    const query = new URLSearchParams(request.querystring);
    const code = query.get("code");
    const state = query.get("state");
    const [expected, verifier, target] = (jar[PENDING] || "").split("|").map((part) => decodeURIComponent(part));
    if (!code || !state || !expected || state !== expected || !verifier) return refuse("The sign-in could not be checked. Open the report's link again.");
    const reply = await fetch(`https://${C.domain}/oauth2/token`, {
      method: "POST",
      headers: { "content-type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ grant_type: "authorization_code", client_id: C.client, code, redirect_uri: back, code_verifier: verifier }),
    });
    if (!reply.ok) return refuse("The sign-in did not complete. Open the report's link again.");
    const tokens = await reply.json();
    if (!(await valid(tokens.id_token))) return refuse("The sign-in could not be checked. Open the report's link again.");
    return redirect(safePath(target), [
      `${SESSION}=${tokens.id_token}; Path=/; Secure; HttpOnly; SameSite=Lax; Max-Age=3600`,
      `${PENDING}=; Path=/_reframe; Secure; HttpOnly; SameSite=Lax; Max-Age=0`,
    ]);
  }

  if (jar[SESSION] && (await valid(jar[SESSION]))) {
    if (request.uri.endsWith("/")) request.uri += "index.html";
    delete request.headers.cookie; // the session is not passed on to S3
    return request;
  }

  const state = crypto.randomBytes(16).toString("hex");
  const verifier = crypto.randomBytes(32).toString("base64url");
  const challenge = crypto.createHash("sha256").update(verifier).digest("base64url");
  const target = request.uri + (request.querystring ? `?${request.querystring}` : "");
  const params = new URLSearchParams({ response_type: "code", client_id: C.client, redirect_uri: back, scope: "openid email profile", state,
                                       code_challenge: challenge, code_challenge_method: "S256" });
  if (C.idp) params.set("identity_provider", C.idp);
  return redirect(`https://${C.domain}/oauth2/authorize?${params}`, [
    `${PENDING}=${[state, verifier, safePath(target)].map(encodeURIComponent).join("|")}; Path=/_reframe; Secure; HttpOnly; SameSite=Lax; Max-Age=900`,
  ]);
};
