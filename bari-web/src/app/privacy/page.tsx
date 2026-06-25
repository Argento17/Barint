import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "מדיניות פרטיות — Bari",
  description: "מדיניות הפרטיות של אתר Bari.",
  robots: { index: false, follow: false },
};

// Body copy awaiting owner approval — DO NOT publish this placeholder.
const PLACEHOLDER = "[טקסט ממתין לאישור הבעלים — אין לפרסם]";

/**
 * TASK 2 — Privacy notice shell (/privacy).
 * Route must be reachable before go-live (linked from cookie notice).
 * Final legal text must be inserted by the owner.
 */
export default function PrivacyPage() {
  return (
    <div dir="rtl" className="mx-auto max-w-2xl px-4 py-12 text-right">
      <h1 className="text-2xl font-extrabold tracking-[-0.03em] text-[#111318]">
        מדיניות פרטיות
      </h1>
      <p className="mt-1 text-[13px] text-[#6B7070]">תאריך עדכון אחרון: {PLACEHOLDER}</p>

      <div className="mt-8 space-y-6 text-[14px] leading-relaxed text-[#4E5663]">
        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">אילו נתונים אנו אוספים</h2>
          <p>{PLACEHOLDER}</p>
        </section>

        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">כיצד אנו משתמשים במידע</h2>
          <p>{PLACEHOLDER}</p>
        </section>

        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">עוגיות (Cookies)</h2>
          <p>{PLACEHOLDER}</p>
        </section>

        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">שיתוף מידע עם צדדים שלישיים</h2>
          <p>{PLACEHOLDER}</p>
        </section>

        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">זכויות המשתמש</h2>
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
