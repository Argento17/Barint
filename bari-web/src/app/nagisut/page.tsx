import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "הצהרת נגישות — Bari",
  description: "הצהרת הנגישות של אתר Bari בהתאם לתקן ישראלי 5568.",
  robots: { index: false, follow: false },
};

// Body copy awaiting owner approval — DO NOT publish this placeholder.
const PLACEHOLDER = "[טקסט ממתין לאישור הבעלים — אין לפרסם]";

/**
 * TASK 2 — Accessibility statement shell (/nagisut).
 * Route is live so crawlers and assistive technology can discover it.
 * Final legal text must be inserted by the owner before go-live.
 * Israeli Standard IS 5568 requires a published accessibility statement.
 */
export default function NagisutPage() {
  return (
    <div dir="rtl" className="mx-auto max-w-2xl px-4 py-12 text-right">
      <h1 className="text-2xl font-extrabold tracking-[-0.03em] text-[#111318]">
        הצהרת נגישות
      </h1>
      <p className="mt-1 text-[13px] text-[#6B7070]">
        בהתאם לתקן ישראלי (ת&quot;י) 5568 ותקנות שוויון זכויות לאנשים עם מוגבלות
        (התאמות נגישות לשירות), תשע&quot;ג-2013.
      </p>

      <div className="mt-8 space-y-6 text-[14px] leading-relaxed text-[#4E5663]">
        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">מידע כללי</h2>
          <p>{PLACEHOLDER}</p>
        </section>

        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">רמת הנגישות</h2>
          <p>{PLACEHOLDER}</p>
        </section>

        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">רכיבים שאינם נגישים</h2>
          <p>{PLACEHOLDER}</p>
        </section>

        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">פניות ומשוב</h2>
          <p>{PLACEHOLDER}</p>
        </section>

        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">תאריך עדכון אחרון</h2>
          <p>{PLACEHOLDER}</p>
        </section>
      </div>
    </div>
  );
}
