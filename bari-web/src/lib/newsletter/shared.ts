export const NEWSLETTER_MESSAGES = {
  success: "נרשמת בהצלחה לניוזלטר של Bari",
  duplicate: "האימייל כבר רשום לניוזלטר",
  error: "אירעה שגיאה. נסו שוב.",
  invalidEmail: "הכניסו כתובת אימייל תקינה.",
} as const;

export const NEWSLETTER_SOURCES = ["homepage", "newsletter_page"] as const;

export type NewsletterSource = (typeof NEWSLETTER_SOURCES)[number];

export type NewsletterSubscribeResponse = {
  ok: boolean;
  message: string;
  code: "success" | "duplicate" | "invalid_email" | "error";
};

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function normalizeEmail(email: string) {
  const asString = typeof email === "string" ? email : String(email ?? "");
  const compact = asString.replace(/\s+/g, "").trim();
  const withoutArtifact = compact.replace(/^undefined(?=[^@]+@)/i, "");

  return withoutArtifact.toLowerCase();
}

export function isValidEmail(email: string) {
  return EMAIL_PATTERN.test(normalizeEmail(email));
}

export function isNewsletterSource(value: string): value is NewsletterSource {
  return NEWSLETTER_SOURCES.includes(value as NewsletterSource);
}

export function maskEmailForLogs(email: string) {
  const normalized = normalizeEmail(email);
  const [localPart = "", domain = ""] = normalized.split("@");

  if (!localPart || !domain) {
    return normalized;
  }

  const visibleStart = localPart.slice(0, 2);
  return `${visibleStart}${"*".repeat(Math.max(localPart.length - 2, 1))}@${domain}`;
}
