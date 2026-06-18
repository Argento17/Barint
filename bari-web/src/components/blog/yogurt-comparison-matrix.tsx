import { CheckCircle2, Minus, XCircle } from "lucide-react";

import { HomeContainer } from "@/components/home/section-frame";
import { yogurtArticle } from "@/lib/blog/yogurt-article-content";

const GRADE_COLORS: Record<string, string> = {
  A: "#7A9450",
  B: "#4A90A4",
  C: "#C08040",
  D: "#C0392B",
};

function SugarCell({ value }: { value: number | null }) {
  if (value === null) {
    return (
      <span className="inline-flex items-center gap-1 text-xs text-[#7A817C]">
        <Minus className="size-3" aria-hidden />
        <span>לא זמין</span>
      </span>
    );
  }
  const isHigh = value > 7;
  return (
    <span
      className={`text-xs font-semibold ${isHigh ? "text-[#C0392B]" : "text-[#111318]"}`}
    >
      {value}g
    </span>
  );
}

function AdditivesCell({ value }: { value: string }) {
  const isClean = value === "ללא" || value === "לא זוהו";
  return isClean ? (
    <span className="inline-flex items-center gap-1 text-xs font-semibold text-[#7A9450]">
      <CheckCircle2 className="size-3.5" aria-hidden />
      {value}
    </span>
  ) : (
    <span className="inline-flex items-center gap-1 text-xs font-semibold text-[#C0392B]">
      <XCircle className="size-3.5" aria-hidden />
      {value}
    </span>
  );
}

export function YogurtComparisonMatrix() {
  const { plainVsFlavoredMatrix } = yogurtArticle;

  return (
    <HomeContainer className="py-10 md:py-14">
      <div className="mx-auto max-w-4xl">
        <header className="mb-6 text-right">
          <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#7A9450]/85">
            השוואה ישירה
          </p>
          <h2 className="mt-2 text-3xl font-extrabold tracking-tighter text-[#111318] md:text-4xl">
            {plainVsFlavoredMatrix.title}
          </h2>
          <p className="mt-3 text-base leading-relaxed text-[#4E5663]">
            {plainVsFlavoredMatrix.subtitle}
          </p>
        </header>

        {/* Scrollable on mobile */}
        <div className="overflow-x-auto rounded-[1rem] border border-black/[0.07]">
          <table
            className="w-full min-w-[40rem] text-right text-sm"
            dir="rtl"
          >
            <thead>
              <tr className="border-b border-black/[0.06] bg-[#F7F7F2]">
                <th className="px-4 py-3 text-right text-[0.65rem] font-bold uppercase tracking-[0.18em] text-[#7A817C]">
                  מוצר
                </th>
                <th className="px-4 py-3 text-center text-[0.65rem] font-bold uppercase tracking-[0.18em] text-[#7A817C]">
                  סוג
                </th>
                <th className="px-4 py-3 text-center text-[0.65rem] font-bold uppercase tracking-[0.18em] text-[#7A817C]">
                  ציון
                </th>
                <th className="px-4 py-3 text-center text-[0.65rem] font-bold uppercase tracking-[0.18em] text-[#7A817C]">
                  סוכר ל-100ג
                </th>
                <th className="px-4 py-3 text-center text-[0.65rem] font-bold uppercase tracking-[0.18em] text-[#7A817C]">
                  חלבון ל-100ג
                </th>
                <th className="px-4 py-3 text-center text-[0.65rem] font-bold uppercase tracking-[0.18em] text-[#7A817C]">
                  תוספי מזון
                </th>
                <th className="px-4 py-3 text-center text-[0.65rem] font-bold uppercase tracking-[0.18em] text-[#7A817C]">
                  רשת
                </th>
              </tr>
            </thead>
            <tbody>
              {plainVsFlavoredMatrix.products.map((product, i) => (
                <tr
                  key={product.id}
                  className={`border-b border-black/[0.04] ${
                    i % 2 === 0 ? "bg-[#FFFFFF]" : "bg-[#FAFAFA]"
                  }`}
                >
                  <td className="px-4 py-3 text-right">
                    <p className="text-xs font-semibold text-[#111318]">
                      {product.name}
                    </p>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <span className="rounded-full bg-black/[0.06] px-2 py-0.5 text-[0.65rem] font-semibold text-[#111318]">
                      {product.type}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <span
                      className="rounded-full px-2.5 py-0.5 text-xs font-extrabold text-white"
                      style={{
                        backgroundColor: GRADE_COLORS[product.grade],
                      }}
                    >
                      {product.score}/{product.grade}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <SugarCell value={product.sugar} />
                  </td>
                  <td className="px-4 py-3 text-center">
                    <span className="text-xs font-semibold text-[#111318]">
                      {product.protein}g
                    </span>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <AdditivesCell value={product.additives} />
                  </td>
                  <td className="px-4 py-3 text-center">
                    <span className="text-[0.65rem] text-[#7A817C]">
                      {product.retailer}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <p className="mt-4 text-right text-xs leading-relaxed text-[#7A817C]">
          {plainVsFlavoredMatrix.caveat}
        </p>
      </div>
    </HomeContainer>
  );
}
