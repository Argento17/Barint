import "server-only";

import {
  isValidEmail,
  maskEmailForLogs,
  NEWSLETTER_MESSAGES,
  type NewsletterSource,
  type NewsletterSubscribeResponse,
} from "@/lib/newsletter/shared";

const BEEHIIV_API_BASE = "https://api.beehiiv.com/v2";

function getBeehiivConfig() {
  const apiKey = process.env.BEEHIIV_API_KEY;
  const publicationId = process.env.BEEHIIV_PUBLICATION_ID;

  if (!apiKey || !publicationId) {
    throw new Error("Missing Beehiiv environment variables.");
  }

  const normalizedPublicationId = publicationId.startsWith("pub_") ? publicationId : `pub_${publicationId}`;

  return { apiKey, publicationId: normalizedPublicationId };
}

async function parseBeehiivJson(response: Response) {
  try {
    return await response.json();
  } catch {
    return null;
  }
}

function getBeehiivErrorMessage(payload: unknown) {
  if (!payload || typeof payload !== "object") {
    return "";
  }

  const errors = "errors" in payload ? payload.errors : null;
  if (Array.isArray(errors)) {
    return errors
      .map((error) => {
        if (!error || typeof error !== "object") {
          return "";
        }

        return "message" in error && typeof error.message === "string" ? error.message : "";
      })
      .filter(Boolean)
      .join(" ");
  }

  return "";
}

function looksLikeDuplicateError(message: string) {
  const normalized = message.toLowerCase();
  return (
    normalized.includes("already") ||
    normalized.includes("exists") ||
    normalized.includes("duplicate") ||
    normalized.includes("subscribed")
  );
}

async function getExistingSubscription(email: string) {
  const { apiKey, publicationId } = getBeehiivConfig();
  const lookupUrl = `${BEEHIIV_API_BASE}/publications/${publicationId}/subscriptions/by_email/${encodeURIComponent(email)}`;

  const response = await fetch(lookupUrl, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      Accept: "application/json",
    },
    cache: "no-store",
  });

  if (response.status === 200) {
    return "exists" as const;
  }

  if (response.status === 404) {
    return "missing" as const;
  }

  return "unknown" as const;
}

function logSignupEvent(event: string, details: Record<string, unknown>) {
  console.info(`[newsletter] ${event}`, details);
}

export async function subscribeEmailToBeehiiv({
  email,
  source,
  origin,
}: {
  email: string;
  source: NewsletterSource;
  origin?: string;
}): Promise<NewsletterSubscribeResponse> {
  if (!isValidEmail(email)) {
    return {
      ok: false,
      code: "invalid_email",
      message: NEWSLETTER_MESSAGES.invalidEmail,
    };
  }

  const normalizedEmail = email.trim().toLowerCase();
  const maskedEmail = maskEmailForLogs(normalizedEmail);

  try {
    const existingSubscription = await getExistingSubscription(normalizedEmail).catch((error) => {
      console.warn("[newsletter] beehiiv_lookup_failed", {
        email: maskedEmail,
        source,
        error: error instanceof Error ? error.message : String(error),
      });
      return "unknown" as const;
    });

    if (existingSubscription === "exists") {
      logSignupEvent("duplicate", { email: maskedEmail, source });
      return {
        ok: false,
        code: "duplicate",
        message: NEWSLETTER_MESSAGES.duplicate,
      };
    }

    const { apiKey, publicationId } = getBeehiivConfig();
    const subscribeUrl = `${BEEHIIV_API_BASE}/publications/${publicationId}/subscriptions`;

    const response = await fetch(subscribeUrl, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({
        email: normalizedEmail,
        reactivate_existing: false,
        send_welcome_email: false,
        utm_source: "bari_website",
        utm_medium: "newsletter_form",
        utm_campaign: source,
        referring_site: origin,
      }),
      cache: "no-store",
    });

    if (response.ok) {
      logSignupEvent("subscribed", { email: maskedEmail, source });
      return {
        ok: true,
        code: "success",
        message: NEWSLETTER_MESSAGES.success,
      };
    }

    const payload = await parseBeehiivJson(response);
    const upstreamMessage = getBeehiivErrorMessage(payload);

    if (response.status === 400 && looksLikeDuplicateError(upstreamMessage)) {
      logSignupEvent("duplicate", { email: maskedEmail, source });
      return {
        ok: false,
        code: "duplicate",
        message: NEWSLETTER_MESSAGES.duplicate,
      };
    }

    console.error("[newsletter] beehiiv_subscribe_failed", {
      email: maskedEmail,
      source,
      status: response.status,
      upstreamMessage,
    });

    return {
      ok: false,
      code: "error",
      message: NEWSLETTER_MESSAGES.error,
    };
  } catch (error) {
    console.error("[newsletter] subscribe_unhandled_error", {
      email: maskedEmail,
      source,
      error: error instanceof Error ? error.message : String(error),
    });

    return {
      ok: false,
      code: "error",
      message: NEWSLETTER_MESSAGES.error,
    };
  }
}
