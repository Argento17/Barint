import { NextResponse } from "next/server";

import { subscribeEmailToBeehiiv } from "@/lib/newsletter/beehiiv";
import {
  isNewsletterSource,
  NEWSLETTER_MESSAGES,
  normalizeEmail,
  type NewsletterSubscribeResponse,
} from "@/lib/newsletter/shared";

export async function POST(request: Request) {
  let body: unknown;

  try {
    body = await request.json();
  } catch {
    const response: NewsletterSubscribeResponse = {
      ok: false,
      code: "error",
      message: NEWSLETTER_MESSAGES.error,
    };
    return NextResponse.json(response, { status: 400 });
  }

  if (!body || typeof body !== "object") {
    const response: NewsletterSubscribeResponse = {
      ok: false,
      code: "error",
      message: NEWSLETTER_MESSAGES.error,
    };
    return NextResponse.json(response, { status: 400 });
  }

  const rawEmail = "email" in body && typeof body.email === "string" ? body.email : "";
  const rawSource = "source" in body && typeof body.source === "string" ? body.source : "homepage";

  if (!isNewsletterSource(rawSource)) {
    const response: NewsletterSubscribeResponse = {
      ok: false,
      code: "error",
      message: NEWSLETTER_MESSAGES.error,
    };
    return NextResponse.json(response, { status: 400 });
  }

  const result = await subscribeEmailToBeehiiv({
    email: normalizeEmail(rawEmail),
    source: rawSource,
    origin: request.headers.get("origin") ?? new URL(request.url).origin,
  });

  const status =
    result.code === "success" ? 200 : result.code === "duplicate" ? 409 : result.code === "invalid_email" ? 400 : 500;

  return NextResponse.json(result, { status });
}
