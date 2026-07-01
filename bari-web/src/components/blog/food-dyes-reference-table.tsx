import { AlertTriangle, Minus } from "lucide-react";

import { foodDyesArticle } from "@/lib/blog/food-dyes-article-content";
import { cn } from "@/lib/utils";

function WarningCell({ value }: { value: boolean }) {
  return value ? (
    <span className="mx-auto inline-flex items-center gap-1 rounded-full bg-amber-50 px-2 py-0.5 text-[0.65rem] font-bold text-[#9A6A00]">
      <AlertTriangle className="size-3" aria-hidden />
      אזהרה
    </span>
  ) : (
    <Minus className="mx-auto size-4 text-[#B7BDB5]" aria-label="ללא אזהרה" />
  );
}

export function FoodDyesReferenceTable() {
  const { dyeTable } = foodDyesArticle;

  return (
    <section className="space-y-4">
      <header className="text-right">
        <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#1F8F6A]/85">
          טבלת ייחוס
        </p>
        <h2 className="mt-1 text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
          {dyeTable.title}
        </h2>
        <p className="mt-2 text-sm leading-relaxed text-[#4E5663] md:text-base">
          {dyeTable.subtitle}
        </p>
      </header>

      <div className="overflow-x-auto rounded-[1.2rem] border border-black/[0.07]">
        <table className="w-full min-w-160 border-collapse text-sm">
          <thead>
            <tr className="border-b border-black/[0.07] bg-[#F7F7F2]">
              <th className="px-4 py-3 text-right text-[0.7rem] font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                שם אמריקאי (FD&amp;C)
              </th>
              <th className="px-3 py-3 text-right text-[0.7rem] font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                שם נפוץ
              </th>
              <th className="px-3 py-3 text-center text-[0.7rem] font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                מספר E
              </th>
              <th className="px-3 py-3 text-center text-[0.7rem] font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                תווית אזהרה באיחוד האירופי
              </th>
              <th className="px-4 py-3 text-right text-[0.7rem] font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                הערה
              </th>
            </tr>
          </thead>
          <tbody>
            {dyeTable.rows.map((row, i) => (
              <tr
                key={row.eNumber}
                className={cn(
                  "border-b border-black/4 last:border-0",
                  "highlight" in row && row.highlight
                    ? "bg-[#FBEEEC]"
                    : i % 2 === 0
                      ? "bg-[#FFFFFF]"
                      : "bg-[#F7F7F2]/50"
                )}
              >
                <td className="px-4 py-3 text-right text-sm font-semibold text-[#111318]">
                  {row.usName}
                </td>
                <td className="px-3 py-3 text-right text-xs text-[#4E5663]">
                  {row.common}
                </td>
                <td className="px-3 py-3 text-center">
                  <span className="font-mono text-xs font-bold text-[#167A58]">
                    {row.eNumber}
                  </span>
                </td>
                <td className="px-3 py-3 text-center">
                  <WarningCell value={row.euWarning} />
                </td>
                <td className="px-4 py-3 text-right text-xs leading-relaxed text-[#7A817C]">
                  {row.note}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <p className="rounded-[0.85rem] border border-black/6 bg-[#FFFFFF]/60 px-4 py-3 text-right text-xs leading-relaxed text-[#7A817C]">
        {dyeTable.caveat}
      </p>
    </section>
  );
}
