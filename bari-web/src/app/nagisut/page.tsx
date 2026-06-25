import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "הצהרת נגישות — Bari",
  description: "הצהרת הנגישות של אתר Bari בהתאם לתקן ישראלי 5568.",
  robots: { index: false, follow: false },
};

/**
 * TASK 2 — Accessibility statement (/nagisut).
 * Route is live so crawlers and assistive technology can discover it.
 * Body text below is a DRAFT loaded for owner review (page stays noindexed).
 * Tokens rendered as 【...】 mark facts the owner must still fill/verify.
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
          <h2 className="mb-2 text-base font-bold text-[#111318]">מחויבות להנגשה</h2>
          <p>
            אתר Bari (להלן: &quot;האתר&quot;, בכתובת bari.digital) רואה חשיבות רבה
            במתן שירות שוויוני לכלל המשתמשים, ופועל רבות לקידום הנגשת האתר לאנשים
            עם מוגבלות, מתוך מחויבות לזכותם לשוויון, לכבוד ולעצמאות. אנו משקיעים
            מאמצים ומשאבים כדי שכל אדם, לרבות אנשים עם מוגבלות, יוכל לגלוש באתר
            בנוחות, בכבוד ובעצמאות ולצרוך את תכניו.
          </p>
        </section>

        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">ההתאמות שבוצעו באתר</h2>
          <p>
            האתר נבנה ועוצב מתוך מחשבה על נגישות, ובין השאר יושמו בו ההתאמות הבאות:
          </p>
          <ul className="mt-2 list-disc space-y-1 pr-5">
            <li>ניווט מלא באמצעות המקלדת, ללא תלות בעכבר, לאורך כל דפי האתר.</li>
            <li>תאימות לתוכנות הקראת מסך (screen readers) הנפוצות.</li>
            <li>טקסט חלופי (alt text) בעברית לתמונות ולתכנים חזותיים נושאי משמעות.</li>
            <li>שמירה על ניגודיות צבעים בין טקסט לרקע ביחס של 4.5:1 לכל הפחות לטקסט רגיל.</li>
            <li>קישור דילוג לתוכן המרכזי (skip-link) בראש כל עמוד.</li>
            <li>
              מבנה עמוד היררכי וסמנטי (כותרות, אזורי ניווט ותגיות ARIA) התומך בניווט
              באמצעות טכנולוגיות מסייעות.
            </li>
            <li>התאמת האתר לגלישה ממגוון סוגי מסכים ומכשירים.</li>
          </ul>
        </section>

        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">עמידה בתקן ובדרישות הדין</h2>
          <p>
            האתר עומד בדרישות תקנות שוויון זכויות לאנשים עם מוגבלות (התאמות נגישות
            לשירות), התשע&quot;ג 2013. התאמות הנגישות בוצעו עפ&quot;י המלצות התקן
            הישראלי (ת&quot;י 5568) לנגישות תכנים באינטרנט ברמת AA, המבוסס על הנחיות
            הנגישות הבין-לאומיות WCAG 2.0.
          </p>
        </section>

        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">רכיבים ותכנים של צד שלישי</h2>
          <p>
            על אף מאמצינו לאפשר גלישה נגישה בכל דפי האתר, ייתכן ורכיבים מסוימים באתר
            לא הונגשו לגמרי או שטרם נמצא להם פתרון נגישות מיטבי. בכלל זה, ייתכן
            שתכנים, רכיבים או שירותים המוטמעים באתר ומקורם בצד שלישי (כגון כלי ניתוח
            ואנליטיקה, רכיבים מוטמעים או תכנים חיצוניים שאינם בשליטתנו המלאה) אינם
            נגישים במלואם. 【פרטו כאן מגבלות ידועות ספציפיות, אם קיימות — לדוגמה:
            רכיב אינטראקטיבי מסוים, סוג תוכן מסוים】. אנו ממשיכים לפעול לשיפור הנגישות
            באתר באופן שוטף, ונשמח לקבל פניות שיסייעו לנו לאתר ולתקן ליקויים.
          </p>
        </section>

        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">פרטי רכז/אחראי הנגישות</h2>
          <p>
            אם במהלך הגלישה באתר נתקלתם בקושי או במכשול נגישות, או אם ברצונכם לדווח
            על בעיה או לבקש התאמת נגישות, נשמח שתפנו אל רכז/אחראי הנגישות של האתר,
            ונעשה כמיטב יכולתנו לטפל בפנייתכם בהקדם:
          </p>
          <ul className="mt-2 list-disc space-y-1 pr-5">
            <li>שם רכז/אחראי הנגישות: תום בר-חיים</li>
            <li>דוא&quot;ל: tbarhaim@gmail.com</li>
            <li>טלפון: 054-2626673</li>
          </ul>
          <p className="mt-2">
            בפנייתכם, נודה אם תתארו את הבעיה שבה נתקלתם, את העמוד שבו אירעה, ואת סוג
            הדפדפן והטכנולוגיה המסייעת שבהם השתמשתם — פרטים אלה יסייעו לנו לטפל בפנייה
            במהירות וביעילות.
          </p>
        </section>

        <section>
          <h2 className="mb-2 text-base font-bold text-[#111318]">תאריך עדכון אחרון</h2>
          <p>תאריך עדכון אחרון של הצהרה זו: 25.06.2026.</p>
        </section>
      </div>
    </div>
  );
}
