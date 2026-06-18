"use client";

import { HomeContainer } from "@/components/home/section-frame";
import { yogurtArticle } from "@/lib/blog/yogurt-article-content";

const GRADE_COLORS: Record<string, string> = {
  A: "#7A9450",
  B: "#4A90A4",
  C: "#C08040",
  D: "#C0392B",
};

const CLUSTER_LABELS: Record<string, string> = {
  "high-protein": "עשיר בחלבון",
  plain: "לבן פשוט",
  greek: "יווני",
  flavored: "ממותק / תוספות",
};

export function YogurtScoreChart() {
  const { scoreDistribution } = yogurtArticle;
  const items = [...scoreDistribution.items].sort((a, b) => b.score - a.score);
  const maxScore = 100;

  return (
    <div className="bg-[#F7F7F2] py-14 md:py-20">
      <HomeContainer>
        <div className="mx-auto max-w-3xl">
          <header className="mb-8 text-right">
            <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#7A9450]/85">
              התפלגות ציונים
            </p>
            <h2 className="mt-2 text-3xl font-extrabold tracking-tighter text-[#111318] md:text-4xl">
              {scoreDistribution.title}
            </h2>
            <p className="mt-3 text-base leading-relaxed text-[#4E5663]">
              {scoreDistribution.subtitle}
            </p>
          </header>

          {/* Grade distribution summary */}
          <div className="mb-8 grid grid-cols-4 gap-3 rounded-[1rem] border border-black/[0.07] bg-[#FFFFFF] px-5 py-5">
            {(["A", "B", "C", "D"] as const).map((grade) => (
              <div key={grade} className="text-center">
                <p
                  className="text-2xl font-extrabold"
                  style={{ color: GRADE_COLORS[grade] }}
                >
                  {scoreDistribution.gradeDistribution[grade]}
                </p>
                <p className="mt-0.5 text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                  דרגה {grade}
                </p>
              </div>
            ))}
          </div>

          {/* Horizontal bar chart */}
          <ul className="space-y-2">
            {items.map((item) => {
              const barWidth = (item.score / maxScore) * 100;
              const color = GRADE_COLORS[item.grade];

              return (
                <li
                  key={item.name}
                  className="rounded-[0.75rem] border border-black/[0.05] bg-[#FFFFFF] px-4 py-3"
                >
                  <div className="mb-1.5 flex items-start justify-between gap-2 text-right">
                    <span
                      className="shrink-0 rounded-full px-2 py-0.5 text-[0.6rem] font-bold uppercase tracking-[0.1em] text-white"
                      style={{ backgroundColor: color }}
                    >
                      {item.grade}
                    </span>
                    <div className="flex-1 text-right">
                      <p className="text-xs font-semibold leading-snug text-[#111318]">
                        {item.name}
                      </p>
                      <p className="mt-0.5 text-[0.6rem] text-[#7A817C]">
                        {CLUSTER_LABELS[item.cluster]} · {item.retailer}
                      </p>
                    </div>
                    <span className="shrink-0 font-mono text-sm font-bold text-[#111318]">
                      {item.score}
                    </span>
                  </div>
                  <div className="h-1.5 w-full overflow-hidden rounded-full bg-black/[0.06]">
                    <div
                      className="h-full rounded-full transition-all duration-500"
                      style={{
                        width: `${barWidth}%`,
                        backgroundColor: color,
                      }}
                    />
                  </div>
                </li>
              );
            })}
          </ul>

          <p className="mt-5 rounded-[0.85rem] border border-black/6 bg-[#FFFFFF]/60 px-5 py-4 text-right text-xs leading-relaxed text-[#7A817C]">
            {scoreDistribution.caveat}
          </p>
        </div>
      </HomeContainer>
    </div>
  );
}
