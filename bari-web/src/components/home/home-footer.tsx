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

// TASK-469 draft consumer copy — Content gate 1 + Adversarial QA gate 2 both
// pending. Do not treat as final; do not ship elsewhere without sign-off.
const communityBandCopy = {
  heading: "רוצים להישאר מעודכנים?", // gate 1: FIXED (two-way "שיחה" → honest "מעודכנים" for a broadcast Channel)
  subline: "עקבו אחרי ברי בוואטסאפ, באינסטגרם ובפייסבוק", // gate 1: FIXED ("קהילה" overclaims a one-way Channel → "עקבו אחרי")
  whatsappCta: "הצטרפו בוואטסאפ", // gate 1: PASS
} as const;

const secondaryIconClass = "size-5 shrink-0";

// Monochrome resting marks for the secondary (Instagram/Facebook) icon buttons.
const communityIcons: Record<CommunityPlatform, ReactNode> = {
  whatsapp: (
    <svg viewBox="0 0 24 24" fill="currentColor" className="size-5 shrink-0" aria-hidden>
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
      className={secondaryIconClass}
      aria-hidden
    >
      <rect x="3.5" y="3.5" width="17" height="17" rx="4.5" />
      <circle cx="12" cy="12" r="4" />
      <circle cx="17.2" cy="6.8" r="1" fill="currentColor" stroke="none" />
    </svg>
  ),
  facebook: (
    <svg viewBox="0 0 24 24" fill="currentColor" className={secondaryIconClass} aria-hidden>
      <path d="M13.5 21v-7.4h2.5l.4-2.9h-2.9V8.9c0-.8.2-1.4 1.4-1.4h1.6V4.9c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 3.9v2h-2.6v2.9h2.6V21h3.2z" />
    </svg>
  ),
};

/**
 * TASK-469 — the community band. Promoted from a fine-print nav row (TASK-467)
 * to a visible, self-contained invitation module: WhatsApp is a filled brand-
 * green primary button (the one place brand color is used in the footer);
 * Instagram/Facebook are secondary rounded icon buttons. Renders nothing when
 * activeCommunityLinks() is empty (graceful-empty contract preserved).
 */
function CommunityBand({ community }: { community: ReturnType<typeof activeCommunityLinks> }) {
  if (community.length === 0) return null;

  const whatsapp = community.find((link) => link.platform === "whatsapp");
  const secondary = community.filter((link) => link.platform !== "whatsapp");

  return (
    <div className="border-b border-black/[0.08] pb-10 mb-10 md:pb-11 md:mb-11">
      <div className="flex flex-col items-center gap-5 text-center md:flex-row md:items-center md:justify-start md:gap-10 md:text-right">
        <div className="space-y-1.5">
          <h2 className="text-lg font-bold text-[#111318] md:text-xl">
            {communityBandCopy.heading}
          </h2>
          <p className="text-sm text-[#4E5663]">{communityBandCopy.subline}</p>
        </div>

        <div className="flex flex-wrap items-center justify-center gap-3 md:justify-end">
          {whatsapp ? (
            <a
              href={whatsapp.href}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex h-11 items-center gap-2 rounded-full bg-[#167A58] px-6 text-sm font-semibold text-[#F7F7F2] shadow-md shadow-slate-900/10 transition hover:-translate-y-px hover:bg-[#146B4D] hover:shadow-lg hover:shadow-slate-900/20 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#167A58]"
            >
              {communityIcons.whatsapp}
              {communityBandCopy.whatsappCta}
            </a>
          ) : null}

          {secondary.map((link) => (
            <a
              key={link.id}
              href={link.href}
              target="_blank"
              rel="noopener noreferrer"
              aria-label={link.label}
              className="inline-flex size-11 items-center justify-center rounded-full border border-black/[0.12] text-[#4E5663] transition hover:border-[#167A58]/40 hover:text-[#167A58] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#167A58]"
            >
              {communityIcons[link.platform]}
            </a>
          ))}
        </div>
      </div>
    </div>
  );
}

export function HomeFooter() {
  const community = activeCommunityLinks();

  return (
    <footer className="relative z-10 isolate border-t border-black/[0.08] bg-[#F7F7F2] py-14 text-[#4E5663] md:py-16">
      <HomeContainer>
        <CommunityBand community={community} />

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

        <NotMedicalAdvice className="mx-auto mt-6 max-w-xl md:mx-0" />

        <p className="mt-8 text-center text-sm text-[#5E6560] md:text-right">
          © {copyrightYear} Bari. כל הזכויות שמורות.
        </p>
      </HomeContainer>
    </footer>
  );
}
