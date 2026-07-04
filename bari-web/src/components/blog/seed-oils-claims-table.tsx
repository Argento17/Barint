import { seedOilsArticle } from "@/lib/blog/seed-oils-article-content";

/**
 * SeedOilsClaimsTable — optional second visual (TASK-492A Fix 4): breaks up the
 * institutional section with a scannable claims-vs-evidence table. Rows are
 * drawn ONLY from the already-approved copy in the "institutions"/"distinction"/
 * "frying" sections (src/data/blog/seed-oils.json -> claimsTable) — no new
 * claims, no new sources beyond what the article already cites.
 */
export function SeedOilsClaimsTable() {
  const { claimsTable } = seedOilsArticle as unknown as {
    claimsTable?: {
      eyebrow: string;
      title: string;
      rows: { id: string; claim: string; evidence: string; source: string }[];
    };
  };

  if (!claimsTable) return null;

  return (
    <section className="space-y-4">
      <header className="text-right">
        <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#1F8F6A]/85">
          {claimsTable.eyebrow}
        </p>
        <h3 className="mt-1.5 text-xl font-extrabold tracking-[-0.02em] text-[#111318] md:text-2xl">
          {claimsTable.title}
        </h3>
      </header>

      <div className="overflow-x-auto rounded-[1.2rem] border border-black/[0.07]">
        <table className="w-full min-w-[36rem] border-collapse text-sm" dir="rtl">
          <thead>
            <tr className="border-b border-black/[0.07] bg-[#F7F7F2]">
              <th className="px-4 py-3 text-right text-[0.7rem] font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                הטענה ברשת
              </th>
              <th className="px-3 py-3 text-right text-[0.7rem] font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                מה הראיות אומרות
              </th>
              <th className="px-4 py-3 text-right text-[0.7rem] font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                מקור
              </th>
            </tr>
          </thead>
          <tbody>
            {claimsTable.rows.map((row, i) => (
              <tr
                key={row.id}
                className={i % 2 === 0 ? "border-b border-black/4 bg-[#FFFFFF] last:border-0" : "border-b border-black/4 bg-[#F7F7F2]/50 last:border-0"}
              >
                <td className="px-4 py-3 text-right text-sm font-semibold text-[#111318]">
                  {row.claim}
                </td>
                <td className="px-3 py-3 text-right text-xs leading-relaxed text-[#4E5663]">
                  {row.evidence}
                </td>
                <td className="px-4 py-3 text-right text-xs leading-relaxed text-[#7A817C]">
                  {row.source}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
