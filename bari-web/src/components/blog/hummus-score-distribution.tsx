"use client";

import { HomeContainer } from "@/components/home/section-frame";
import { hummusArticle } from "@/lib/blog/hummus-article-content";

const GRADE_COLORS: Record<string, string> = {
  A: "#1F8F6A",
  B: "#7A9450",
  C: "#B8860B",
  D: "#9B3A2A",
};

export function HummusScoreDistribution() {
  const { scoreDistribution } = hummusArticle;
  const maxCount = Math.max(...scoreDistribution.bands.map((b) => b.count));

  return (
    <section className="py-14 md:py-20">
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

          {/* Grade distribution bars */}
          <ul className="space-y-4">
            {scoreDistribution.bands.map((band) => {
              const barWidth = Math.round((band.count / maxCount) * 100);
              const color = GRADE_COLORS[band.grade] ?? "#7A817C";
              return (
                <li key={band.grade} className="rounded-[1rem] border border-black/[0.07] bg-[#FFFFFF] px-5 py-5">
                  <div className="flex items-center justify-between gap-4">
                    <div className="flex items-center gap-3 text-right">
                      <span
                        className="flex size-9 shrink-0 items-center justify-center rounded-full text-sm font-extrabold text-white"
                        style={{ backgroundColor: color }}
                      >
                        {band.grade}
                      </span>
                      <div>
                        <p className="text-sm font-extrabold text-[#111318]">
                          ציון {band.range}
                        </p>
                        <p className="text-xs text-[#7A817C]">
                          {band.count} מוצרים · {band.percent}%
                        </p>
                      </div>
                    </div>
                    <div className="flex-1">
                      <div className="h-2 w-full overflow-hidden rounded-full bg-[#F7F7F2]">
                        <div
                          className="h-full rounded-full transition-all duration-700"
                          style={{
                            width: `${barWidth}%`,
                            backgroundColor: color,
                          }}
                        />
                      </div>
                    </div>
                  </div>
                  <p className="mt-3 text-sm leading-relaxed text-[#4E5663] text-right">
                    {band.description}
                  </p>
                </li>
              );
            })}
          </ul>

          <p className="mt-5 rounded-[0.85rem] border border-black/6 bg-[#FFFFFF]/60 px-5 py-4 text-right text-xs leading-relaxed text-[#7A817C]">
            {scoreDistribution.note}
          </p>
        </div>
      </HomeContainer>
    </section>
  );
}
