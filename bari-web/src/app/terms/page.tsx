import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "תנאי שימוש — Bari",
  description: "תנאי השימוש באתר Bari.",
  robots: { index: false, follow: false },
};

// Body copy awaiting owner approval — DO NOT publish this placeholder.
const PLACEHOLDER = "[טקסט ממתין לאישור הבעלים — אין לפרסם]";

/**
 * TASK 2 — Terms of use shell (/terms).
 * Route is live so it can be linked before final copy is approved.
 * Final legal text must be inserted by the owner before go-live.
 */
export default function TermsPage() {
  return (
    <div dir="rtl" className="mx-auto max-w-2xl px-4 py-12 text-right">
      <h1 className="text-2xl font-extrabold tracking-[-0.03em] text-[#111318]">
        תנאי שימוש
      </h1>
      <p className="mt-1 text-[13px] text-[#6B7070]">תאריך עדכון אחרון: {PLACEHOLDER}</p>

      <div className="mt-8 space-y-6 text-[14px] leading-relaxed text-[#4E5663]">
        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">כללי</h2>
          <p>{PLACEHOLDER}</p>
        </section>

        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">השימוש באתר</h2>
          <p>{PLACEHOLDER}</p>
        </section>

        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">הגבלת אחריות</h2>
          <p>{PLACEHOLDER}</p>
        </section>

        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">קניין רוחני</h2>
          <p>{PLACEHOLDER}</p>
        </section>

        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">שינויים בתנאים</h2>
          <p>{PLACEHOLDER}</p>
        </section>

        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">יצירת קשר</h2>
          <p>{PLACEHOLDER}</p>
        </section>
      </div>
    </div>
  );
}
