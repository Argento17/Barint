import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "מדיניות עוגיות | Bari",
  description: "הודעת העוגיות (Cookies) של אתר Bari — אילו עוגיות נשמרות ולשם מה, וכיצד לבטל או לחסום אותן.",
};

/**
 * Cookie notice (/cookies).
 * Route is live so it can be linked from the footer and privacy policy.
 * Body text below is a DRAFT loaded for owner review. Page is indexable
 * (inherits `index, follow` from the root layout; no robots override here).
 * Tokens rendered as 【...】 mark facts/decisions the owner must still resolve.
 * Source: P404 legal drafts, DOC 3 (הודעת עוגיות) — the full in-page section.
 * The A/B consent-mechanism choice is left open by the draft and surfaced as a
 * visible 【...】 note for the owner/lawyer to decide.
 */
export default function CookiesPage() {
  return (
    <div dir="rtl" className="mx-auto max-w-2xl px-4 py-12 text-right">
      <h1 className="text-2xl font-extrabold tracking-[-0.03em] text-[#111318]">
        מדיניות עוגיות
      </h1>
      <p className="mt-1 text-[13px] text-[#6B7070]">
        היידוע נגזר מחובת היידוע לפי סעיף 11 לחוק הגנת הפרטיות, התשמ&quot;א-1981.
      </p>

      <div className="mt-8 space-y-6 text-[14px] leading-relaxed text-[#4E5663]">
        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">שימוש בעוגיות (Cookies)</h2>
          <p>
            האתר עושה שימוש ב&quot;עוגיות&quot; — קבצי טקסט קטנים הנשמרים בדפדפן
            שלכם — לצורך תפעול תקין ולצורך מדידת השימוש באתר.
          </p>
        </section>

        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">אילו עוגיות נשמרות ולשם מה</h2>
          <p>
            האתר משתמש בעיקר בעוגיות של שירות Google Analytics (GA4), ובהן:
          </p>
          <ul className="mt-2 list-disc space-y-1 pr-5">
            <li>
              <code>_ga</code> — משמשת להבחנה בין משתמשים שונים; תוקפה האופייני הוא
              עד כשנתיים.
            </li>
            <li>
              <code>_ga_*</code> — משמשת לשמירת מצב מדידת ה-Session עבור האתר.
            </li>
          </ul>
          <p className="mt-2">
            עוגיות אלה משמשות אותנו לניתוח סטטיסטי של אופן השימוש באתר ולשיפורו,
            ואינן משמשות לזיהוי אישי יזום שלכם.
          </p>
        </section>

        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">מדידה שאינה מבוססת עוגיות</h2>
          <p>
            בנוסף לשירות Google Analytics, האתר משתמש ב-<strong>Vercel Web
            Analytics</strong> — כלי מדידה שאינו שומר עוגיות במכשירכם ואינו אוסף
            מידע אישי מזהה. הכלי מודד נתונים מצטברים בלבד (כגון מספר צפיות בעמודים
            ומקורות הפניה לאתר), ומאחר שאינו עושה שימוש בעוגיות ואינו מצריך הסכמה
            מוקדמת, הוא אינו נכלל בבאנר העוגיות.
          </p>
        </section>

        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">כיצד ניתן לבטל או לחסום עוגיות</h2>
          <p>באפשרותכם לשלוט בעוגיות ולמחוק אותן בכל עת:</p>
          <ul className="mt-2 list-disc space-y-1 pr-5">
            <li>
              דרך <strong>הגדרות הדפדפן</strong> שלכם, שבהן ניתן לחסום או למחוק
              עוגיות (האפשרות זמינה בכל הדפדפנים הנפוצים).
            </li>
            <li>
              באמצעות <strong>תוסף ההסתלקות (opt-out) הרשמי של Google Analytics</strong>{" "}
              לדפדפן, הזמין בכתובת: https://tools.google.com/dlpage/gaoptout
            </li>
            <li>
              דרך מסך <strong>&quot;ניהול העדפות&quot;</strong>{" "}
              של באנר העוגיות באתר.
            </li>
          </ul>
          <p className="mt-2">
            חסימת עוגיות לא תמנע מכם לצרוך את תכני האתר, אך עשויה לפגוע ביכולתנו
            למדוד ולשפר את השירות. לפרטים נוספים על אופן הטיפול במידע, ראו את מדיניות
            הפרטיות המלאה של האתר.
          </p>
        </section>

        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">מנגנון ההסכמה לעוגיות</h2>
          <p>
            אתר זה מיישם מנגנון <strong>הסכמה אקטיבית (opt-in)</strong>: עוגיות אנליטיקה ושיווק, לרבות Google Analytics, נטענות אך ורק לאחר שנתתם הסכמה מפורשת. בכניסה לאתר מוצג באנר עוגיות עם שלוש אפשרויות — &quot;קבל הכל&quot;, &quot;דחה הכל&quot; ו&quot;ניהול העדפות&quot;. עד למתן הסכמה, עוגיות שאינן הכרחיות אינן נטענות. ניתן לשנות או לבטל את ההסכמה בכל עת דרך &quot;הגדרות עוגיות&quot; בתחתית האתר.
          </p>
        </section>
      </div>
    </div>
  );
}
