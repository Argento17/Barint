"use client";

import { useState } from "react";
import { Mail } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { fireEvent } from "@/lib/analytics";
import {
  isValidEmail,
  NEWSLETTER_MESSAGES,
  normalizeEmail,
  type NewsletterSource,
  type NewsletterSubscribeResponse,
} from "@/lib/newsletter/shared";

type NewsletterSignupProps = {
  source: NewsletterSource;
};

export function NewsletterSignup({ source }: NewsletterSignupProps) {
  const [email, setEmail] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [feedback, setFeedback] = useState<NewsletterSubscribeResponse | null>(null);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const normalizedEmail = normalizeEmail(email);

    if (!isValidEmail(normalizedEmail)) {
      setFeedback({
        ok: false,
        code: "invalid_email",
        message: NEWSLETTER_MESSAGES.invalidEmail,
      });
      return;
    }

    setIsSubmitting(true);
    setFeedback(null);

    try {
      const response = await fetch("/api/newsletter/subscribe", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: normalizedEmail,
          source,
        }),
      });

      const result = (await response.json()) as NewsletterSubscribeResponse;
      setFeedback(result);

      if (result.ok) {
        setEmail("");
        // Fired only on a confirmed-successful subscribe response — not on
        // form_start/click — so it is distinguishable from GA4's automatic
        // (and here, unreliable) form_submit signal.
        fireEvent("newsletter_signup", { source });
      }
    } catch {
      setFeedback({
        ok: false,
        code: "error",
        message: NEWSLETTER_MESSAGES.error,
      });
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="relative mx-auto mb-4 max-w-xl">
      <form
        className="flex flex-col gap-3 sm:flex-row sm:items-stretch"
        onSubmit={handleSubmit}
        aria-label="הרשמה לניוזלטר"
        dir="rtl"
      >
        <Input
          type="email"
          name="email"
          required
          dir="ltr"
          inputMode="email"
          placeholder="you@example.com"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          className="h-14 flex-1 rounded-full border-black/8 bg-white px-5 text-left text-sm text-[#111318] placeholder:text-[#7A817C] focus-visible:border-[#1F8F6A]/40 focus-visible:ring-[#1F8F6A]/25"
          disabled={isSubmitting}
          autoComplete="email"
          aria-invalid={feedback?.code === "invalid_email"}
        />
        <Button
          type="submit"
          size="lg"
          disabled={isSubmitting}
          className="newsletter-cta-attention h-14 shrink-0 rounded-full border border-[#1F8F6A]/10 bg-[#1F8F6A] px-7 font-semibold text-white shadow-[inset_0_1px_0_rgba(255,255,255,0.2),0_14px_40px_-16px_rgba(31,143,106,0.58)] transition-[transform,box-shadow,background-color] duration-500 ease-out hover:-translate-y-px hover:bg-[#176F53] hover:shadow-[inset_0_1px_0_rgba(255,255,255,0.2),0_18px_44px_-16px_rgba(31,143,106,0.66)] disabled:cursor-wait disabled:animate-none disabled:opacity-80"
        >
          {isSubmitting ? "נרשמים..." : "הירשמו לניוזלטר"}
        </Button>
      </form>

      {feedback ? (
        <p
          className={`mt-3 text-sm ${feedback.ok ? "text-[#167A58]" : "text-[#7A3434]"}`}
          role="status"
          aria-live="polite"
        >
          {feedback.message}
        </p>
      ) : null}
    </div>
  );
}

export function NewsletterIcon() {
  return (
    <div className="mx-auto mb-6 flex size-16 items-center justify-center rounded-xl border border-black/8 bg-[#1F8F6A]/[0.06] text-[#1F8F6A] shadow-sm">
      <Mail className="size-8" strokeWidth={1.75} aria-hidden />
    </div>
  );
}
