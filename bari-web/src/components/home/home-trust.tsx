import { HomeContainer } from "./section-frame";

const TRUST_ITEMS = [
  {
    title: "מידע, לא המלצה",
    text: "Bari מפרקת מבנה ונתונים — לא אומרת מה «כדאי» לאכול.",
  },
  {
    title: "ציון Bari",
    text: "מדד מבנה: רכיבים, עיבוד, תרומה תזונתית והקשר קטגוריאלי — בהשוואה למוצרים דומים.",
  },
  {
    title: "בלוג מול השוואה",
    text: "הבלוג מספר סיפור עיתונאי; מנוע ההשוואה מציג את כל המוצרים בפירוט אינטראקטיבי.",
  },
] as const;

export function HomeTrust() {
  return (
    <section className="bg-[#F7F7F2] py-12 md:py-16" id="trust">
      <HomeContainer>
        <div className="mx-auto max-w-3xl text-center">
          <p className="text-xs font-bold uppercase tracking-[0.24em] text-[#1F8F6A]">
            שקיפות
          </p>
          <h2 className="mt-3 text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
            עצמאית, אנליטית, ללא אג׳נדה שיווקית
          </h2>
        </div>
        <ul className="mt-8 grid gap-4 md:grid-cols-3">
          {TRUST_ITEMS.map((item) => (
            <li
              key={item.title}
              className="rounded-[1.2rem] border border-black/[0.08] bg-[#FFFFFF] p-5 text-right"
            >
              <h3 className="text-sm font-extrabold text-[#111318]">{item.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-[#4E5663]">{item.text}</p>
            </li>
          ))}
        </ul>
        <p className="mx-auto mt-6 max-w-2xl text-center text-xs leading-relaxed text-[#5E6560]">
          הנתונים נאספים ממקורות ציבוריים ומתוויות מוצר; הציון משקף את מודל Bari ואינו
          תחליף לייעוץ רפואי או תזונתי אישי.
        </p>
      </HomeContainer>
    </section>
  );
}
