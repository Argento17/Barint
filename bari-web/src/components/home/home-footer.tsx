"use client";

import type { ReactNode } from "react";
import Link from "next/link";

import { BariBrandLogo } from "@/components/brand/bari-brand-logo";
import { OPEN_PREFERENCES_EVENT } from "@/components/shared/consent-manager";
import { NotMedicalAdvice } from "@/components/shared/not-medical-advice";
import { activeCommunityLinks, type CommunityPlatform } from "@/lib/social-links";

import { HomeContainer } from "./section-frame";

const legalLinks = [
  { label: "הצהרת נגישות", href: "/nagisut" },
  { label: "מדיניות פרטיות", href: "/privacy" },
  { label: "תנאי שימוש", href: "/terms" },
  { label: "מדיניות עוגיות", href: "/cookies" },
  { label: "כתב ויתור רפואי", href: "/disclaimer" },
] as const;

const copyrightYear = 2026;

const communityIconClass = "size-4 shrink-0";

// Monochrome inline marks — same register as the legal-links row, never brand-colored.
const communityIcons: Record<CommunityPlatform, ReactNode> = {
  whatsapp: (
    <svg viewBox="0 0 24 24" fill="currentColor" className={communityIconClass} aria-hidden>
      <path d="M17.5 14.4c-.3-.1-1.6-.8-1.8-.9-.2-.1-.4-.1-.6.1-.2.2-.7.9-.8 1-.2.2-.3.2-.5.1-.3-.1-1.2-.4-2.2-1.4-.8-.7-1.4-1.6-1.5-1.9-.2-.3 0-.5.1-.6.1-.1.3-.3.4-.5.1-.1.2-.3.3-.4.1-.2 0-.4 0-.5s-.6-1.5-.8-2c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.5.1-.7.3-.2.2-.9.9-.9 2.2s1 2.6 1.1 2.7c.1.2 1.9 3 4.7 4.1.7.3 1.2.4 1.6.6.7.2 1.3.2 1.7.1.5-.1 1.6-.7 1.9-1.3.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.6-.3z" />
      <path d="M12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.5 1.3 5L2 22l5.2-1.3c1.4.8 3.1 1.2 4.8 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2zm0 18.2c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3.1.8.8-3-.2-.3C4 14.9 3.6 13.5 3.6 12c0-4.6 3.8-8.4 8.4-8.4s8.4 3.8 8.4 8.4-3.8 8.2-8.4 8.2z" />
    </svg>
  ),
  instagram: (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.75"
      className={communityIconClass}
      aria-hidden
    >
      <rect x="3.5" y="3.5" width="17" height="17" rx="4.5" />
      <circle cx="12" cy="12" r="4" />
      <circle cx="17.2" cy="6.8" r="1" fill="currentColor" stroke="none" />
    </svg>
  ),
  facebook: (
    <svg viewBox="0 0 24 24" fill="currentColor" className={communityIconClass} aria-hidden>
      <path d="M13.5 21v-7.4h2.5l.4-2.9h-2.9V8.9c0-.8.2-1.4 1.4-1.4h1.6V4.9c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 3.9v2h-2.6v2.9h2.6V21h3.2z" />
    </svg>
  ),
};

export function HomeFooter() {
  const community = activeCommunityLinks();

  return (
    <footer className="relative z-10 isolate border-t border-black/[0.08] bg-[#F7F7F2] py-14 text-[#4E5663] md:py-16">
      <HomeContainer>
        <div className="space-y-3 text-center md:text-right">
          <Link href="/" aria-label="בית Bari" className="inline-flex w-fit">
            <BariBrandLogo surface="dark" />
          </Link>
          <p className="max-w-md text-sm leading-relaxed text-[#4E5663]">
            אינטליגנציית מזון ישראלית להשוואה, דירוג והבנה טובה יותר של מוצרים.
          </p>
        </div>

        <nav
          aria-label="קישורים משפטיים"
          className="mt-8 flex flex-wrap items-center justify-center gap-x-7 gap-y-3 text-sm md:justify-end"
        >
          {legalLinks.map((l) => (
            <Link
              key={l.label}
              href={l.href}
              className="inline-flex px-1 text-[#4E5663] transition hover:text-[#2FAE82]"
            >
              {l.label}
            </Link>
          ))}
          <button
            type="button"
            onClick={() =>
              window.dispatchEvent(
                new CustomEvent(OPEN_PREFERENCES_EVENT, {
                  detail: { trigger: document.activeElement as HTMLElement },
                })
              )
            }
            className="inline-flex px-1 text-[#4E5663] transition hover:text-[#2FAE82]"
          >
            הגדרות עוגיות
          </button>
        </nav>

        {/* TASK-467: community links — renders nothing while communityLinks
            hrefs are unset (placeholder state). Secondary nav weight, same
            register as the legal-links row above; monochrome, no brand colors. */}
        {community.length > 0 ? (
          <nav
            aria-label="הקהילות של ברי"
            className="mt-5 flex flex-wrap items-center justify-center gap-x-6 gap-y-3 text-sm md:justify-end"
          >
            <span className="text-[#8A908B]">הקהילות של ברי</span>
            {community.map((link) => (
              <a
                key={link.id}
                href={link.href}
                target="_blank"
                rel="noopener noreferrer"
                aria-label={link.label}
                className="inline-flex items-center gap-1.5 px-1 text-[#4E5663] transition hover:text-[#2FAE82]"
              >
                {communityIcons[link.platform]}
                {link.label}
              </a>
            ))}
          </nav>
        ) : null}

        <NotMedicalAdvice className="mx-auto mt-6 max-w-xl md:mx-0" />

        <p className="mt-8 text-center text-sm text-[#5E6560] md:text-right">
          © {copyrightYear} Bari. כל הזכויות שמורות.
        </p>
      </HomeContainer>
    </footer>
  );
}
