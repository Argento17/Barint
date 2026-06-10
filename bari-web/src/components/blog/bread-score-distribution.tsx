"use client";

import { HomeContainer } from "@/components/home/section-frame";
import { breadArticle } from "@/lib/blog/bread-article-content";

/**
 * BreadScoreDistribution — horizontal bar chart showing score band distribution.
 * Data: breadArticle.scoreDistribution — all 24 products from run_bread_008_headpin.
 * Corpus: Shufersal only (May–Jun 2026). CSS bars — no external chart library.
 */
export function BreadScoreDistribution() {
  const { scoreDistribution } = breadArticle;
  const maxCount = Math.max(...scoreDistribution.bands.map((b) => b.count));

  return (
    <div className="bg-[#F7F7F2] py-14 md:py-20">
      <HomeContainer>
        <div className="mx-auto max-w-3xl">
          <header className="mb-8 text-right">
            <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#7A9450]/85">
              התפלגות ציונים
            </p>
            <h2 className="mt-2 text-2xl font-extrabold tracking-tighter text-[#111318] md:text-3xl">
              {scoreDistribution.title}
            </h2>
            <p className="mt-2 text-sm leading-relaxed text-[#4E5663]">
              {scoreDistribution.subtitle}
            </p>
          </header>

          <div className="space-y-3" dir="rtl">
            {scoreDistribution.bands.map((band) => {
              const widthPct = Math.round((band.count / maxCount) * 100);
              const isA = band.gradeClass === "A";
              return (
                <div key={band.label} className="group">
                  <div className="flex items-center gap-3">
                    {/* Label */}
                    <span
                      className={`w-[4.5rem] shrink-0 font-mono text-sm font-bold ${
                        isA ? "text-[#7A9450]" : "text-[#4E5663]"
                      }`}
                    >
                      {band.label}
                    </span>

                    {/* Bar */}
                    <div className="flex-1">
                      <div
                        className={`h-6 rounded-sm transition-all ${
                          isA ? "bg-[#7A9450]/80" : "bg-[#4E5663]/40"
                        }`}
                        style={{ width: `${widthPct}%` }}
                        aria-label={`${band.count} מוצרים`}
                      />
                    </div>

                    {/* Count */}
                    <span className="w-8 shrink-0 text-left text-xs font-bold text-[#111318]">
                      {band.count}
                    </span>
                  </div>

                  {/* Products tooltip on hover — desktop only */}
                  <p className="mt-1 hidden text-[0.65rem] leading-relaxed text-[#7A817C] group-hover:block md:pr-[5.5rem]">
                    {(band.products as readonly string[]).join(" · ")}
                  </p>
                </div>
              );
            })}
          </div>

          {/* Grade legend */}
          <div className="mt-6 flex justify-end gap-5" dir="rtl">
            <div className="flex items-center gap-2">
              <div className="size-3 rounded-sm bg-[#7A9450]/80" />
              <span className="text-xs font-bold text-[#7A817C]">ציון A</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="size-3 rounded-sm bg-[#4E5663]/40" />
              <span className="text-xs font-bold text-[#7A817C]">ציון B</span>
            </div>
          </div>

          <p className="mt-5 text-xs leading-relaxed text-[#7A817C]">
            {scoreDistribution.caveat}
          </p>
        </div>
      </HomeContainer>
    </div>
  );
}
