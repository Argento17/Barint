import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "כתב ויתור רפואי | Bari",
  description: "כתב הוויתור הרפואי של אתר Bari — התכנים נועדו למידע ועריכה בלבד ואינם ייעוץ רפואי או תזונתי.",
  robots: { index: false, follow: false },
};

/**
 * Medical disclaimer (/disclaimer).
 * Route is live so it can be linked from the footer and supplement pages.
 * Body text below is a DRAFT loaded for owner review (page stays noindexed).
 * Source: P404 legal drafts, DOC 5 (כתב ויתור רפואי) — the longer footer version.
 */
export default function DisclaimerPage() {
  return (
    <div dir="rtl" className="mx-auto max-w-2xl px-4 py-12 text-right">
      <h1 className="text-2xl font-extrabold tracking-[-0.03em] text-[#111318]">
        כתב ויתור רפואי
      </h1>
      <p className="mt-1 text-[13px] text-[#6B7070]">
        תוכן האתר נועד למטרות מידע ועריכה בלבד ואינו מהווה ייעוץ רפואי או תזונתי.
      </p>

      <div className="mt-8 space-y-6 text-[14px] leading-relaxed text-[#4E5663]">
        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">מידע ועריכה בלבד</h2>
          <p>
            המידע המוצג באתר זה, לרבות לגבי תוספי תזונה, נועד למטרות{" "}
            <strong>מידע, השוואה ועריכה בלבד</strong>, ואינו מהווה ייעוץ רפואי,
            תזונתי או מקצועי, אבחנה, או המלצה לטיפול, לנטילת תוסף או להפסקת טיפול
            כלשהו. <strong>המידע אינו תחליף לייעוץ תזונאי, רפואי או מקצועי אחר</strong>,
            ואין בתכני האתר כדי להחליף התייעצות עם איש מקצוע מוסמך.
          </p>
        </section>

        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">מתי להיוועץ באיש מקצוע</h2>
          <p>
            <strong>יש להיוועץ ברופא/ה, ברוקח/ת או בדיאטן/ית מוסמך/ת</strong> לפני
            נטילת תוסף תזונה כלשהו, לפני שינוי בתזונה, ובמיוחד אם הנכם בהיריון או
            מניקות, נוטלים תרופות, סובלים ממצב רפואי כלשהו, או מטפלים בקטין.
          </p>
        </section>

        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">דיווח על טענות יצרן</h2>
          <p>
            האתר עשוי לתאר טענות, ייעודים או הבטחות המופיעים על גבי תווית המוצר או
            בחומרי היצרן — אלה מדווחים כ<strong>טענות של היצרן</strong>, כפי שהן,
            ואין בהצגתן משום אישור, אימות או קביעה מצד האתר כי התוסף יעיל לטיפול,
            למניעה או לריפוי של מחלה או מצב רפואי כלשהו.{" "}
            <strong>
              האתר אינו קובע ואינו טוען ליעילות רפואית של תוספים בריפוי, במניעה או
              בטיפול במחלות.
            </strong>{" "}
            תוספי תזונה אינם תרופות ואינם מיועדים לאבחן, לטפל, לרפא או למנוע מחלה.
          </p>
        </section>

        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">מקרה חירום</h2>
          <p>
            במקרה חירום רפואי יש לפנות מיד לגורם רפואי מוסמך או לשירותי החירום.
          </p>
        </section>
      </div>
    </div>
  );
}
