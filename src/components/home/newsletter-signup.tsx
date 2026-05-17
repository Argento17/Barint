"use client";

import { useState } from "react";
import { Mail } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export function NewsletterSignup() {
  const [sent, setSent] = useState(false);

  return (
    <form
      className="mx-auto mb-4 flex max-w-xl flex-col gap-3 sm:flex-row"
      onSubmit={(e) => {
        e.preventDefault();
        setSent(true);
      }}
      aria-label="הרשמה לניוזלטר"
    >
      <Input
        type="email"
        name="email"
        required
        dir="ltr"
        placeholder="you@example.com"
        className="h-12 rounded-2xl border-emerald-300/12 bg-zinc-950/60 text-left text-sm text-white shadow-inner shadow-black/25 placeholder:text-zinc-600 focus-visible:ring-emerald-300/25"
        disabled={sent}
        autoComplete="email"
      />
      <Button
        type="submit"
        size="lg"
        disabled={sent}
        className="newsletter-cta-attention h-12 shrink-0 rounded-2xl border border-emerald-300/12 bg-gradient-to-l from-emerald-700 via-emerald-800 to-zinc-950 px-8 font-semibold text-white shadow-md shadow-emerald-950/20 transition-[transform,box-shadow,background-color] duration-500 ease-out hover:-translate-y-px hover:shadow-lg hover:shadow-emerald-950/25 disabled:animate-none disabled:opacity-80"
      >
        {sent ? "תודה, נרשמתם" : "הירשמו לניוזלטר"}
      </Button>
    </form>
  );
}

export function NewsletterIcon() {
  return (
    <div className="mx-auto mb-6 flex size-16 items-center justify-center rounded-2xl border border-emerald-300/12 bg-emerald-300/[0.06] text-emerald-200 shadow-md shadow-black/20">
      <Mail className="size-8" aria-hidden />
    </div>
  );
}
