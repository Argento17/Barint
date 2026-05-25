"use client";

import { useState } from "react";
import { Mail } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
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
    <div className="mx-auto mb-4 max-w-xl">
      <form
        className="flex flex-col gap-3 sm:flex-row"
        onSubmit={handleSubmit}
        aria-label="הרשמה לניוזלטר"
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
          className="h-12 rounded-2xl border-black/[0.08] bg-[#FFFFFF]/80 text-left text-sm text-[#111318] shadow-inner shadow-slate-900/25 placeholder:text-[#7A817C] focus-visible:ring-[#1F8F6A]/25"
          disabled={isSubmitting}
          autoComplete="email"
          aria-invalid={feedback?.code === "invalid_email"}
        />
        <Button
          type="submit"
          size="lg"
          disabled={isSubmitting}
          className="newsletter-cta-attention h-12 shrink-0 rounded-2xl border border-[#1F8F6A]/10 bg-[#1F8F6A] px-8 font-semibold text-[#F7F7F2] shadow-md shadow-slate-900/10 transition-[transform,box-shadow,background-color] duration-500 ease-out hover:-translate-y-px hover:bg-[#1F8F6A] hover:shadow-lg hover:shadow-slate-900/25 disabled:cursor-wait disabled:animate-none disabled:opacity-80"
        >
          {isSubmitting ? "נרשמים..." : "הירשמו לניוזלטר"}
        </Button>
      </form>

      {feedback ? (
        <p
          className={`mt-3 text-sm ${feedback.ok ? "text-[#1F8F6A]" : "text-[#7A3434]"}`}
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
    <div className="mx-auto mb-6 flex size-16 items-center justify-center rounded-2xl border border-black/[0.08] bg-[#1F8F6A]/[0.035] text-[#1F8F6A] shadow-md shadow-slate-900/20">
      <Mail className="size-8" aria-hidden />
    </div>
  );
}
