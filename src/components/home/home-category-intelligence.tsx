import Link from "next/link";
import { ChevronLeft } from "lucide-react";

import { HomeContainer } from "./section-frame";

const CATEGORIES = [
  {
    id: "bread",
    label: "לחם וקמח",
    hint: "256 מוצרים נסרקו · 31 נבחרו לדוח · מחמצת, דגנים ושקיפות",
    href: "/compare/bread-comparison",
    status: "זמין",
  },
  {
    id: "cereals",
    label: "דגנים וחטיפי בוקר",
    hint: "סוכר מוסתר, סיבים, שיווק ילדים",
    href: "/hashvaot",
    status: "בקרוב",
  },
  {
    id: "bars",
    label: "חטיפי גרנולה וחלבון",
    hint: "חלבון על האריזה מול מבנה בפועל",
    href: "/hashvaot",
    status: "בקרוב",
  },
  {
    id: "dairy",
    label: "חלב ותחליפים",
    hint: "18 מוצרים · ניתוח מלא זמין",
    href: "/blog/milk-analysis",
    status: "זמין",
  },
  {
    id: "protein",
    label: "מוצרי חלבון",
    hint: "העשרה, עיבוד, הבטחות על האריזה",
    href: "/hashvaot",
    status: "בקרוב",
  },
  {
    id: "ingredients",
    label: "חקירות מרכיב",
    hint: "סוכר, שמנים, תוספי מרקם",
    href: "/#methodology",
    status: "מתודולוגיה",
  },
] as const;

export function HomeCategoryIntelligence() {
  return (
    <section className="border-y border-black/[0.06] bg-[#FFFFFF] py-14 md:py-20" id="categories">
      <HomeContainer>
        <div className="mx-auto mb-10 max-w-3xl text-center">
          <p className="text-xs font-bold uppercase tracking-[0.24em] text-[#1F8F6A]">
            מפת קטגוריות
          </p>
          <h2 className="mt-3 text-balance text-3xl font-extrabold tracking-[-0.045em] text-[#111318] md:text-4xl">
            מודיעין מזון על פני קטגוריות — לא רק חלב
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-pretty text-base leading-relaxed text-[#4E5663]">
            Bari בונה פרופיל השוואה לכל קטגוריה. מדף החלב הוא הניתוח המוביל היום; שאר
            הקטגוריות נפתחות בהדרגה.
          </p>
        </div>

        <ul className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {CATEGORIES.map((cat) => (
            <li key={cat.id}>
              <Link
                href={cat.href}
                className="group flex h-full flex-col rounded-[1.2rem] border border-black/[0.08] bg-[#F7F7F2]/40 p-5 transition hover:border-[#1F8F6A]/22 hover:bg-[#FFFFFF]"
              >
                <div className="flex items-start justify-between gap-2">
                  <h3 className="text-lg font-extrabold text-[#111318]">{cat.label}</h3>
                  <span
                    className={
                      cat.status === "זמין"
                        ? "shrink-0 rounded-full bg-[#1F8F6A] px-2 py-0.5 text-[0.65rem] font-bold text-[#F7F7F2]"
                        : "shrink-0 rounded-full border border-black/[0.08] bg-[#FFFFFF] px-2 py-0.5 text-[0.65rem] font-bold text-[#7A817C]"
                    }
                  >
                    {cat.status}
                  </span>
                </div>
                <p className="mt-2 flex-1 text-sm leading-relaxed text-[#4E5663]">{cat.hint}</p>
                <p className="mt-4 flex items-center gap-1 text-xs font-bold text-[#1F8F6A] opacity-80 group-hover:opacity-100">
                  {cat.status === "זמין" ? "לניתוח" : "למידע"}
                  <ChevronLeft className="size-3.5" aria-hidden />
                </p>
              </Link>
            </li>
          ))}
        </ul>
      </HomeContainer>
    </section>
  );
}
