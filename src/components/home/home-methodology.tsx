import { Activity, CheckCircle2, Layers3 } from "lucide-react";

import { HomeContainer } from "./section-frame";

const SIGNAL_ROWS = [
  { axis: "איכות רכיבים", value: 84 },
  { axis: "עומס סוכר ומלח", value: 38 },
  { axis: "רמת עיבוד", value: 76 },
  { axis: "ערך תזונתי", value: 68 },
  { axis: "סיבים וחלבון", value: 35 },
  { axis: "השוואה לקטגוריה", value: 79 },
  { axis: "אמינות הנתונים", value: 64 },
  { axis: "פשטות המוצר", value: 82 },
] as const;

const interpretationCards = [
  {
    icon: Layers3,
    title: "נרמול לפי קטגוריה",
    text: "לחם, יוגורט וחטיף לא נמדדים באותו סרגל. Bari משווה מוצר למציאות התחרותית שלו.",
  },
  {
    icon: Activity,
    title: "פרמטרים במקביל",
    text: "רכיבים, עיבוד, ערך תזונתי, פחמימה, חלבון וביטחון נקראים יחד במקום להפוך הכול למספר בודד.",
  },
  {
    icon: CheckCircle2,
    title: "הסבר שניתן להבין",
    text: "הפלט נשאר קריא: מה חזק, מה חלש, ואיזה פרט בתווית באמת משנה.",
  },
] as const;

export function HomeMethodology() {
  return (
    <section className="relative overflow-hidden bg-[#F7F7F2] py-20 md:py-28" id="methodology">
      <div className="pointer-events-none absolute inset-0 bg-transparent" aria-hidden />
      <div
        className="pointer-events-none absolute inset-x-6 top-24 h-px bg-gradient-to-l from-transparent via-[#1F8F6A]/10 to-transparent"
        aria-hidden
      />

      <HomeContainer>
        <div className="mx-auto mb-12 max-w-3xl text-center">
          <p className="text-xs font-bold uppercase tracking-[0.24em] text-[#1F8F6A]">
            שיטת הניתוח
          </p>
          <h2 className="mt-3 text-balance text-3xl font-extrabold tracking-[-0.045em] text-[#111318] md:text-5xl">
            ניתוח רב-ממדי של מספר רב של פרמטרים.
          </h2>
          <p className="mx-auto mt-5 max-w-2xl text-pretty text-base leading-relaxed text-[#4E5663] md:text-lg">
            Bari מנתחת כל מוצר לפי פרמטרים תזונתיים, רכיביים ועיבודיים — כדי להבין לא רק אם מוצר
            &quot;טוב&quot; או &quot;רע&quot;, אלא במה הוא חזק, איפה הוא חלש, ובאיזה הקשר הוא נבחן.
          </p>
        </div>

        <div className="rounded-[2rem] border border-black/[0.08] bg-[#FFFFFF]/68 p-4 shadow-[0_36px_120px_-74px_rgba(17,19,24,0.78)] md:p-6">
          <div className="mb-5 rounded-[1.5rem] border border-black/[0.08] bg-[#FFFFFF]/72 p-5 md:p-7">
            <p className="mb-5 text-xs font-bold uppercase tracking-[0.2em] text-[#7A817C]">
              8 אותות ניתוח
            </p>
            <div className="space-y-3">
              {SIGNAL_ROWS.map((signal) => (
                <div key={signal.axis} className="flex items-center gap-4">
                  <span className="w-36 shrink-0 text-right text-sm font-bold text-[#111318]">
                    {signal.axis}
                  </span>
                  <div className="relative h-2 flex-1 overflow-hidden rounded-full bg-[#F7F7F2]">
                    <div
                      className="absolute inset-y-0 right-0 rounded-full bg-[#1F8F6A]/70"
                      style={{ width: `${signal.value}%` }}
                    />
                  </div>
                  <span className="w-8 shrink-0 text-left text-xs font-bold text-[#1F8F6A]">
                    {signal.value}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="grid gap-3 sm:grid-cols-3">
            {interpretationCards.map((card) => {
              const Icon = card.icon;
              return (
                <div
                  key={card.title}
                  className="rounded-2xl border border-black/[0.08] bg-[#FFFFFF]/52 p-4"
                >
                  <Icon className="mb-3 size-5 text-[#1F8F6A]" aria-hidden />
                  <h4 className="text-sm font-extrabold text-[#111318]">{card.title}</h4>
                  <p className="mt-2 text-xs leading-relaxed text-[#7A817C]">{card.text}</p>
                </div>
              );
            })}
          </div>
        </div>
      </HomeContainer>
    </section>
  );
}
