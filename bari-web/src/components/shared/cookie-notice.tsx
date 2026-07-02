"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

const STORAGE_KEY = "bari_cookie_notice_dismissed";

/**
 * TASK 2 — Cookie notice banner.
 * Soft notice only (not a hard consent gate).
 * Dismissal persisted in localStorage.
 * Body copy is a placeholder pending owner approval.
 */

// Body text awaiting owner-approved final copy.
const PLACEHOLDER_NOTICE =
  "[טקסט ממתין לאישור הבעלים — אין לפרסם]";

export function CookieNotice() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    try {
      if (!localStorage.getItem(STORAGE_KEY)) {
        setVisible(true);
      }
    } catch {
      // localStorage unavailable (private browsing, SSR edge case) — skip silently.
    }
  }, []);

  function dismiss() {
    try {
      localStorage.setItem(STORAGE_KEY, "1");
    } catch {
      // ignore
    }
    setVisible(false);
  }

  if (!visible) return null;

  return (
    <div
      role="banner"
      aria-label="הודעת עוגיות"
      dir="rtl"
      className="fixed bottom-0 inset-x-0 z-50 flex items-center gap-3 border-t border-black/[0.07] bg-[#FAFAF7] px-4 py-3 shadow-[0_-4px_24px_-8px_rgba(17,19,24,0.10)] sm:px-6"
    >
      <p className="flex-1 text-[12px] leading-relaxed text-[#4E5663]">
        {PLACEHOLDER_NOTICE}{" "}
        <Link
          href="/privacy"
          className="font-semibold text-[#167A58] underline underline-offset-2 hover:no-underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#167A58]"
        >
          מדיניות הפרטיות
        </Link>
      </p>
      <button
        type="button"
        onClick={dismiss}
        aria-label="סגור הודעת עוגיות"
        className="shrink-0 rounded-full border border-black/[0.08] bg-[#FFFFFF] px-3 py-1.5 text-[11px] font-semibold text-[#3E444A] transition hover:border-black/[0.14] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#167A58]"
      >
        הבנתי
      </button>
    </div>
  );
}
