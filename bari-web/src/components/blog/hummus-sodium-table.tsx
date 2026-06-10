"use client";

import { HomeContainer } from "@/components/home/section-frame";
import { hummusArticle } from "@/lib/blog/hummus-article-content";

const GRADE_COLORS: Record<string, string> = {
  A: "#1F8F6A",
  B: "#7A9450",
  C: "#B8860B",
  D: "#9B3A2A",
};

function SodiumBar({ value, max }: { value: number; max: number }) {
  const width = Math.round((value / max) * 100);
  const color =
    value < 100
      ? "#1F8F6A"
      : value < 350
        ? "#7A9450"
        : value < 600
          ? "#B8860B"
          : "#9B3A2A";
  return (
    <div className="flex items-center gap-2">
      <div className="h-2 w-24 overflow-hidden rounded-full bg-[#F7F7F2]">
        <div
          className="h-full rounded-full"
          style={{ width: `${width}%`, backgroundColor: color }}
        />
      </div>
      <span className="min-w-[3rem] text-right text-xs font-bold text-[#111318]">
        {value}
      </span>
    </div>
  );
}

export function HummusSodiumTable() {
  const { sodiumVarianceTable } = hummusArticle;
  const maxSodium = Math.max(...sodiumVarianceTable.products.map((p) => p.sodium));

  return (
    <section className="py-10 md:py-14">
      <HomeContainer>
        <div className="mx-auto max-w-4xl">
          <header className="mb-6 text-right">
            <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#7A9450]/85">
              שונות נתרן
            </p>
            <h2 className="mt-2 text-2xl font-extrabold tracking-tighter text-[#111318] md:text-3xl">
              {sodiumVarianceTable.title}
            </h2>
            <p className="mt-3 text-base leading-relaxed text-[#4E5663]">
              {sodiumVarianceTable.subtitle}
            </p>
          </header>

          <div className="overflow-x-auto">
            <table className="w-full min-w-[560px] border-collapse text-right">
              <thead>
                <tr className="border-b border-black/[0.07]">
                  <th className="pb-3 pr-2 text-right text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                    מוצר
                  </th>
                  <th className="pb-3 pr-2 text-right text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                    סוג
                  </th>
                  <th className="pb-3 pr-2 text-center text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                    ציון / דרגה
                  </th>
                  <th className="pb-3 text-right text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                    נתרן (מ&quot;ג ל-100 גרם)
                  </th>
                </tr>
              </thead>
              <tbody>
                {sodiumVarianceTable.products.map((product, i) => {
                  const gradeColor = GRADE_COLORS[product.grade] ?? "#7A817C";
                  return (
                    <tr
                      key={i}
                      className="border-b border-black/[0.04] last:border-0"
                    >
                      <td className="py-3 pr-2 text-sm font-semibold text-[#111318]">
                        {product.name}
                      </td>
                      <td className="py-3 pr-2 text-xs text-[#7A817C]">
                        {product.type}
                      </td>
                      <td className="py-3 pr-2 text-center">
                        <span
                          className="inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-bold text-white"
                          style={{ backgroundColor: gradeColor }}
                        >
                          {product.score}/{product.grade}
                        </span>
                      </td>
                      <td className="py-3">
                        <SodiumBar value={product.sodium} max={maxSodium} />
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          <p className="mt-5 rounded-[0.85rem] border border-black/6 bg-[#FFFFFF]/60 px-5 py-4 text-right text-xs leading-relaxed text-[#7A817C]">
            {sodiumVarianceTable.caveat}
          </p>
        </div>
      </HomeContainer>
    </section>
  );
}
