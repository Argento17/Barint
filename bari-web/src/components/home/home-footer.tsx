"use client";

import Link from "next/link";

import { BariBrandLogo } from "@/components/brand/bari-brand-logo";
import { OPEN_PREFERENCES_EVENT } from "@/components/shared/consent-manager";
import { NotMedicalAdvice } from "@/components/shared/not-medical-advice";

import { HomeContainer } from "./section-frame";

const legalLinks = [
  { label: "הצהרת נגישות", href: "/nagisut" },
  { label: "מדיניות פרטיות", href: "/privacy" },
  { label: "תנאי שימוש", href: "/terms" },
  { label: "מדיניות עוגיות", href: "/cookies" },
  { label: "כתב ויתור רפואי", href: "/disclaimer" },
] as const;

const copyrightYear = 2026;

export function HomeFooter() {
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

        <NotMedicalAdvice className="mx-auto mt-6 max-w-xl md:mx-0" />

        <p className="mt-8 text-center text-sm text-[#5E6560] md:text-right">
          © {copyrightYear} Bari. כל הזכויות שמורות.
        </p>
      </HomeContainer>
    </footer>
  );
}
