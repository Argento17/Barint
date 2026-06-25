"use client";

import Link from "next/link";
import { NotMedicalAdvice } from "@/components/shared/not-medical-advice";
import { OPEN_PREFERENCES_EVENT } from "@/components/shared/consent-manager";

/**
 * TASK 2 — Site-wide footer.
 * Contains legal links (/nagisut, /privacy, /terms) and the not-medical-advice disclaimer.
 */
export function SiteFooter() {
  return (
    <footer
      dir="rtl"
      className="border-t border-black/[0.06] bg-[#FAFAF7] px-4 py-6 text-right sm:px-6"
      aria-label="כותרת תחתונה"
    >
      <nav aria-label="קישורים משפטיים" className="mb-3 flex flex-wrap gap-x-5 gap-y-1.5">
        {/*
          Legal links enabled for owner review. The /nagisut, /privacy, /terms
          pages remain noindexed (robots: noindex) while they still hold draft
          placeholder text, so Google will not index them until approved copy lands.
        */}
        <Link
          href="/nagisut"
          className="text-[12px] text-[#6B7070] underline-offset-2 hover:underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#167A58]"
        >
          הצהרת נגישות
        </Link>
        <Link
          href="/privacy"
          className="text-[12px] text-[#6B7070] underline-offset-2 hover:underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#167A58]"
        >
          מדיניות פרטיות
        </Link>
        <Link
          href="/terms"
          className="text-[12px] text-[#6B7070] underline-offset-2 hover:underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#167A58]"
        >
          תנאי שימוש
        </Link>
        {/* CMP re-open link — dispatches a custom event picked up by ConsentManager */}
        <button
          type="button"
          onClick={() =>
            window.dispatchEvent(
              new CustomEvent(OPEN_PREFERENCES_EVENT, {
                detail: { trigger: document.activeElement as HTMLElement },
              })
            )
          }
          className="text-[12px] text-[#6B7070] underline-offset-2 hover:underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#167A58]"
        >
          הגדרות עוגיות
        </button>
      </nav>
      <NotMedicalAdvice className="max-w-xl" />
      <p className="mt-2 text-[11px] text-[#6B7070]">
        &copy; {new Date().getFullYear()} Bari. כל הזכויות שמורות.
      </p>
    </footer>
  );
}
