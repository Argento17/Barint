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
        className="h-12 rounded-2xl border-black/[0.08] bg-[#FFFFFF]/80 text-left text-sm text-[#111318] shadow-inner shadow-slate-900/25 placeholder:text-[#7A817C] focus-visible:ring-[#1F8F6A]/25"
        disabled={sent}
        autoComplete="email"
      />
      <Button
        type="submit"
        size="lg"
        disabled={sent}
        className="newsletter-cta-attention h-12 shrink-0 rounded-2xl border border-[#1F8F6A]/10 bg-[#1F8F6A] px-8 font-semibold text-[#F7F7F2] shadow-md shadow-slate-900/10 transition-[transform,box-shadow,background-color] duration-500 ease-out hover:-translate-y-px hover:bg-[#1F8F6A] hover:shadow-lg hover:shadow-slate-900/25 disabled:animate-none disabled:opacity-80"
      >
        {sent ? "תודה, נרשמתם" : "הירשמו לניוזלטר"}
      </Button>
    </form>
  );
}

export function NewsletterIcon() {
  return (
    <div className="mx-auto mb-6 flex size-16 items-center justify-center rounded-2xl border border-black/[0.08] bg-[#1F8F6A]/[0.035] text-[#1F8F6A] shadow-md shadow-slate-900/20">
      <Mail className="size-8" aria-hidden />
    </div>
  );
}
