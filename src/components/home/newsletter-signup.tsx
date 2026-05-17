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
        className="h-12 rounded-2xl border-zinc-300 bg-white text-left text-sm shadow-inner"
        disabled={sent}
        autoComplete="email"
      />
      <Button
        type="submit"
        size="lg"
        disabled={sent}
        className="h-12 shrink-0 rounded-2xl bg-gradient-to-l from-emerald-600 to-emerald-700 px-8 font-semibold text-white shadow-md"
      >
        {sent ? "תודה, נרשמתם" : "הירשמו עכשיו"}
      </Button>
    </form>
  );
}

export function NewsletterIcon() {
  return (
    <div className="mx-auto mb-6 flex size-16 items-center justify-center rounded-2xl bg-gradient-to-br from-emerald-500 to-emerald-600 shadow-md">
      <Mail className="size-8 text-white" aria-hidden />
    </div>
  );
}
