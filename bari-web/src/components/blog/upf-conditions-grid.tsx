import { UpfInfographicFrame } from "@/components/blog/upf-infographic-frame";
import { upfArticle } from "@/lib/blog/upf-article-content";

/**
 * Infographic #1 -- the 7 named conditions from the Lancet series' first
 * paper, grouped by body system, labeled as an observational (cohort-study)
 * link. Data: upfArticle.infographics.conditions (ultra-processed-food.json),
 * grounded verbatim in the "מה הסדרה בפועל מצאה" section paragraph -- no
 * condition name here is invented; the copy itself says "בין היתר" (among
 * others), so the note states 7-of-12 rather than implying these are all 12.
 */
export function UpfConditionsGrid() {
  const data = (
    upfArticle.infographics as unknown as {
      conditions: {
        eyebrow: string;
        title: string;
        cells: { system: string; name: string }[];
        note: string;
        caption: string;
      };
    }
  ).conditions;

  return (
    <UpfInfographicFrame eyebrow={data.eyebrow} title={data.title} caption={data.caption}>
      <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
        {data.cells.map((cell) => (
          <div
            key={cell.name}
            className="flex items-baseline gap-2.5 rounded-[0.65rem] bg-[#EDF4EF] px-3 py-2.5"
          >
            <span className="shrink-0 rounded-full bg-[#FFFFFF]/70 px-1.5 py-0.5 font-mono text-[9.5px] font-bold uppercase tracking-[0.04em] text-[#167A58]">
              {cell.system}
            </span>
            <span className="text-sm font-semibold text-[#111318]">{cell.name}</span>
          </div>
        ))}
      </div>
      <p className="mt-3 text-center text-[13px] font-semibold text-[#4E5663]">{data.note}</p>
    </UpfInfographicFrame>
  );
}
