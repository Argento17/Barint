import { NextResponse } from "next/server";

import {
  checkPassword,
  createSessionToken,
  isConfigured,
  SESSION_COOKIE,
  sessionCookieOptions,
} from "@/lib/admin/auth";
import {
  checkRateLimit,
  clientIp,
  recordFailure,
  recordSuccess,
} from "@/lib/admin/rate-limit";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function POST(request: Request) {
  if (!isConfigured()) {
    return NextResponse.json({ ok: false, error: "not_configured" }, { status: 503 });
  }

  // Throttle brute-force guessing before doing any password work.
  const ip = clientIp(request);
  const limit = checkRateLimit(ip);
  if (!limit.allowed) {
    return NextResponse.json(
      { ok: false, error: "rate_limited" },
      { status: 429, headers: { "Retry-After": String(limit.retryAfterSec) } },
    );
  }

  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ ok: false, error: "bad_request" }, { status: 400 });
  }

  const password =
    body && typeof body === "object" && "password" in body && typeof (body as { password: unknown }).password === "string"
      ? (body as { password: string }).password
      : "";

  if (!checkPassword(password)) {
    recordFailure(ip);
    return NextResponse.json({ ok: false, error: "invalid" }, { status: 401 });
  }

  recordSuccess(ip);
  const res = NextResponse.json({ ok: true });
  res.cookies.set(SESSION_COOKIE, createSessionToken(), sessionCookieOptions);
  return res;
}
