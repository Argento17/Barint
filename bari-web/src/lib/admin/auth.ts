/**
 * Admin copy editor — authentication.
 *
 * Single-password login for one owner/editor. The password is never stored in
 * code — it comes from the ADMIN_PASSWORD env var (a Vercel secret). On success
 * we issue an HMAC-signed, HttpOnly session cookie; it can't be forged without
 * ADMIN_SESSION_SECRET, and it's never readable by client JS.
 *
 * Required env (set in Vercel, and .env.local for dev):
 *   ADMIN_PASSWORD        the editor login password
 *   ADMIN_SESSION_SECRET  a long random string used to sign sessions
 */
import crypto from "crypto";
import { cookies } from "next/headers";

export const SESSION_COOKIE = "bari_admin_session";
const MAX_AGE_SECONDS = 60 * 60 * 8; // 8 hours

function sessionSecret(): string {
  return process.env.ADMIN_SESSION_SECRET || "";
}

function timingSafeEqualStr(a: string, b: string): boolean {
  const ab = Buffer.from(a);
  const bb = Buffer.from(b);
  if (ab.length !== bb.length) return false;
  return crypto.timingSafeEqual(ab, bb);
}

/** Returns true only if a non-empty ADMIN_PASSWORD is set and matches input. */
export function checkPassword(input: string): boolean {
  const expected = process.env.ADMIN_PASSWORD || "";
  if (!expected) return false; // fail closed when unconfigured
  return timingSafeEqualStr(input, expected);
}

/** True when both required secrets are configured. */
export function isConfigured(): boolean {
  return Boolean(process.env.ADMIN_PASSWORD) && Boolean(sessionSecret());
}

export function createSessionToken(): string {
  const payload = Buffer.from(
    JSON.stringify({ v: 1, iat: Date.now() }),
  ).toString("base64url");
  const sig = crypto
    .createHmac("sha256", sessionSecret())
    .update(payload)
    .digest("base64url");
  return `${payload}.${sig}`;
}

export function verifySessionToken(token: string | undefined): boolean {
  if (!token || !sessionSecret()) return false;
  const [payload, sig] = token.split(".");
  if (!payload || !sig) return false;

  const expected = crypto
    .createHmac("sha256", sessionSecret())
    .update(payload)
    .digest("base64url");
  if (!timingSafeEqualStr(sig, expected)) return false;

  try {
    const parsed = JSON.parse(Buffer.from(payload, "base64url").toString());
    if (typeof parsed.iat !== "number") return false;
    if (Date.now() - parsed.iat > MAX_AGE_SECONDS * 1000) return false;
  } catch {
    return false;
  }
  return true;
}

/** Read the session cookie and verify it. */
export async function isAuthed(): Promise<boolean> {
  const store = await cookies();
  return verifySessionToken(store.get(SESSION_COOKIE)?.value);
}

export const sessionCookieOptions = {
  httpOnly: true,
  secure: process.env.NODE_ENV === "production",
  sameSite: "lax" as const,
  path: "/",
  maxAge: MAX_AGE_SECONDS,
};
