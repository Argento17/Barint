import { CheckCircle2, XCircle } from "lucide-react";

import { oliveOilArticle } from "@/lib/blog/olive-oil-article-content";
import { cn } from "@/lib/utils";

const ORIGIN_COLORS: Record<string, string> = {
  איטליה: "text-[#7A9450]",
  ספרד: "text-[#C8A830]",
  ישראל: "text-[#4A8FA0]",
};

const RETAILER_COLORS: Record<string, string> = {
  שופרסל: "bg-[#E8F4F0] text-[#1F8F6A]",
  יוחננוף: "bg-[#EEF2FB] text-[#3B5BAD]",
};

function Cell({ value }: { value: boolean }) {
  return value ? (
    <CheckCircle2 className="mx-auto size-4 text-[#1F8F6A]" aria-label="כן" />
  ) : (
    <XCircle className="mx-auto size-4 text-[#C0392B]/70" aria-label="לא" />
  );
}

export function OliveOilTransparencyMatrix() {
  const { transparencyMatrix } = oliveOilArticle;

  return (
    <section className="space-y-4">
      <header className="text-right">
        <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#1F8F6A]/85">
          שקיפות תווית
        </p>
        <h2 className="mt-1 text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
          {transparencyMatrix.title}
        </h2>
        <p className="mt-2 text-sm leading-relaxed text-[#4E5663] md:text-base">
          {transparencyMatrix.subtitle}
        </p>
      </header>

      <div className="overflow-x-auto rounded-[1.2rem] border border-black/[0.07]">
        <table className="w-full min-w-160 border-collapse text-sm">
          <thead>
            <tr className="border-b border-black/[0.07] bg-[#F7F7F2]">
              <th className="px-4 py-3 text-right text-[0.7rem] font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                מוצר
              </th>
              <th className="px-3 py-3 text-center text-[0.7rem] font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                רשת
              </th>
              <th className="px-3 py-3 text-center text-[0.7rem] font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                מקור
              </th>
              <th className="px-3 py-3 text-center text-[0.7rem] font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                תאריך קציר
              </th>
              <th className="px-3 py-3 text-center text-[0.7rem] font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                PDO / PGI
              </th>
              <th className="px-3 py-3 text-center text-[0.7rem] font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                דרגה בחזית
              </th>
            </tr>
          </thead>
          <tbody>
            {transparencyMatrix.products.map((product, i) => (
              <tr
                key={product.name}
                className={cn(
                  "border-b border-black/4 last:border-0",
                  i % 2 === 0 ? "bg-[#FFFFFF]" : "bg-[#F7F7F2]/50"
                )}
              >
                <td className="px-4 py-3 text-right text-sm font-semibold text-[#111318]">
                  {product.name}
                </td>
                <td className="px-3 py-3 text-center">
                  <span
                    className={cn(
                      "rounded-full px-2 py-0.5 text-[0.65rem] font-bold",
                      RETAILER_COLORS[product.retailer] ?? "bg-[#F0F0EC] text-[#7A817C]"
                    )}
                  >
                    {product.retailer}
                  </span>
                </td>
                <td className="px-3 py-3 text-center">
                  <span
                    className={cn(
                      "text-xs font-bold",
                      ORIGIN_COLORS[product.origin] ?? "text-[#4E5663]"
                    )}
                  >
                    {product.origin}
                  </span>
                </td>
                <td className="px-3 py-3 text-center">
                  <Cell value={product.harvestDate} />
                </td>
                <td className="px-3 py-3 text-center">
                  <Cell value={product.pdoPgi} />
                </td>
                <td className="px-3 py-3 text-center">
                  <Cell value={product.gradeOnFront} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <p className="text-right text-xs text-[#7A817C]">
        ✗ = לא מצוין על התווית שנסרקה · ✓ = מצוין בבירור · מקור: שופרסל (6 מותגים) + יוחננוף (4 מותגים) — 19 מוצרים סה"כ, סריקה מלאה, יוני 2026
      </p>
    </section>
  );
}
