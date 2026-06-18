import { redirect } from "next/navigation";
import type { Metadata } from "next";
import Link from "next/link";

import { GLASSBOX_W5_ON } from "@/lib/feature-flags";
import { BARI_COMPARISON_TOKENS } from "@/lib/design/bari-comparison-tokens";

// TASK-181Q — Glass Box W5 methodology page.
// Renders only when NEXT_PUBLIC_GLASSBOX_W5=on. Otherwise redirects to home.
// Content source: 01_framework/glass_box/methodology_glass_box_page_v1.md (authored by Content Agent).
// UX spec: 01_framework/glass_box/methodology_page_ux_spec_v1.md (authored by Design Agent).
// No new components — uses inline Tailwind + token values only (Gen 1 editorial page pattern).

export const metadata: Metadata = {
  title: "איך ברי בונה את הציון | Bari",
  description:
    "ברי תיקנה הנחה שמוצרים שנראים פחות מעובדים מוערכים בצורה אחרת. הסבר על השינוי ומה ברי בודקת עכשיו.",
};

// sectionEyebrow token value from bari-comparison-tokens.ts (typography.sectionEyebrow).
const EYEBROW_CLASS = BARI_COMPARISON_TOKENS.typography.sectionEyebrow;

// Separator used between all sections — same token as ExpansionSection divider.
const SECTION_BORDER = "border-t border-[rgba(17,19,24,0.06)]";

// Body text style shared across sections 2–3 — CategoryPrologue sentence style.
const BODY_TEXT = "text-[13px] leading-[1.55] tracking-[-0.008em] text-[#3E444A]";

export default function GlassBoxMethodologyPage() {
  // Flag gate: when OFF, redirect to home (do not expose in-progress content).
  if (!GLASSBOX_W5_ON) {
    redirect("/");
  }

  return (
    <div
      className="min-h-screen bg-[#EFEFEB] sm:py-8"
      dir="rtl"
    >
      <div className="mx-auto w-full max-w-[680px] overflow-hidden bg-white sm:rounded-[1.5rem] sm:shadow-xl">

        {/* ── Section 1: Lead ───────────────────────────────────────────────── */}
        <section className="px-4 pt-5 pb-4 sm:px-6">
          <p className={EYEBROW_CLASS}>שיטה · עדכון</p>
          <h1 className="mt-1 text-[1.35rem] font-semibold leading-tight tracking-[-0.028em] text-[#111318]">
            איך ברי בונה את הציון
          </h1>
          <p className={`mt-3 ${BODY_TEXT}`}>
            ברי עצרה את ההנחה שמזון שנראה פחות מעובד אוטומטית פחות בעייתי.
          </p>
          <p className={`mt-2 ${BODY_TEXT}`}>
            זו לא שאלה של נתונים טובים יותר — זו שאלה של עקביות. אם שילוב של שומן עם מלח, או שומן עם סוכר, סופר בצורה אחת בגלידה וסופר אחרת בחומוס — הציון משקר. ברי תיקנה את זה.
          </p>
        </section>

        {/* ── Section 2: מה השתנה ולמה ────────────────────────────────────── */}
        <section className={`${SECTION_BORDER} px-4 pt-4 pb-4 sm:px-6`}>
          <p className={BODY_TEXT}>
            שילוב של שומן עם מלח — ושילוב של שומן עם סוכר — קשור לקלות שבה אוכלים יותר מדי מאותו מוצר. ברי ספרה את השילוב הזה תמיד, אבל לא תמיד באותו משקל: מוצר שנראה פחות מעובד קיבל הנחה.
          </p>
          <p className={`mt-3 ${BODY_TEXT}`}>
            זו הייתה טעות. לא טעות בנתונים — טעות בעיקרון. המראה של מוצר אינו מקטין את ההשפעה של ההרכב שלו על הצלחת. ברי מפסיקה להתחשב במראה: אם התווית מראה את השילוב, הוא נספר באותו משקל בכל מוצר. מוצרים שנהנו מהנחה הזו ירדו בציון.
          </p>
        </section>

        {/* ── Section 3: מה ברי בודקת עכשיו ──────────────────────────────── */}
        {/* 4 × inline paragraphs with bold lead phrase. No card, no icon, no list. */}
        {/* D-dimension identifiers (D3/D4/D5/D6) do not appear in consumer strings. */}
        <section className={`${SECTION_BORDER} px-4 pt-4 pb-3 sm:px-6`}>
          <div className="space-y-4">
            <p className={BODY_TEXT}>
              <strong className="font-semibold text-[14px] text-[#2F3531]">מה כתוב על התווית</strong>
              <br />
              האם המוצר מגלה את כל רכיביו? ברי בודקת עד כמה התווית שקופה — שמות גנריים של תוספים, חומרים שלא מפורטים, מידע חסר.
            </p>
            <p className={BODY_TEXT}>
              <strong className="font-semibold text-[14px] text-[#2F3531]">כמה בטוחים אנחנו</strong>
              <br />
              לא כל מוצר נבדק באותה רמת ודאות. ברי מציגה את רמת הביטחון של כל ציון, ומאזנת אותה כלפי ניטרלי כשהמידע חלקי.
            </p>
            <p className={BODY_TEXT}>
              <strong className="font-semibold text-[14px] text-[#2F3531]">אילו תוספים נמצאים ומה ידוע עליהם</strong>
              <br />
              ברי מציגה את רשימת התוספים שבמוצר עם הסבר קצר על כל אחד — מה תפקידו, ומה המחקר אומר עליו עד היום. זה מידע להבנה, לא פסיקה. הרשימה הזו לא משנה כרגע את הציון הראשי.
            </p>
            <p className={BODY_TEXT}>
              <strong className="font-semibold text-[14px] text-[#2F3531]">אות עיבוד — בהתאם לביטחון</strong>
              <br />
              ברי בוחנת את דפוס הרכיבים של המוצר ומשווה אותו לנתונים ממחקרים גדולים על אוכלוסיות. כשהמידע על הרכב המוצר שלם, האות חזק. כשהמידע חלקי, האות נסוג לניטרלי — ברי לא ממציאה ביטחון שאין.
            </p>
          </div>
        </section>

        {/* ── Section 4: על הציונים שזעו ──────────────────────────────────── */}
        {/* Light register (#6A716E). Inline links — no buttons, no cards. */}
        <section className={`${SECTION_BORDER} px-4 pt-4 pb-3 sm:px-6`}>
          <p className="text-[13px] leading-[1.55] text-[#6A716E]">
            חלק מהמוצרים ירדו בציון. לא כעונש — אלא מפני שהנחה שלא הייתה אמורה להיות שם הוסרה. הפירוט המלא נמצא בדפי{" "}
            <Link
              href="/hashvaot/hummus"
              className="text-[#1F8F6A] underline underline-offset-2"
            >
              החומוס
            </Link>
            {" "}וה
            <Link
              href="/hashvaot/maadanim"
              className="text-[#1F8F6A] underline underline-offset-2"
            >
              מעדנים
            </Link>
            .
          </p>
        </section>

        {/* ── Section 5: תאריך ─────────────────────────────────────────────── */}
        {/* 11px / #AAAAAA — no heading, no border. Matches MethodologyFooter register. */}
        <section className="px-4 pt-3 pb-6 sm:px-6">
          <p className="text-[11px] leading-relaxed text-[#AAAAAA]">
            עדכון אחרון: 5 ביוני 2026
          </p>
        </section>

      </div>
    </div>
  );
}
