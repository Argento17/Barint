import { cn } from "@/lib/utils";
import { UpfInfographicFrame } from "@/components/blog/upf-infographic-frame";
import { upfArticle } from "@/lib/blog/upf-article-content";

/**
 * Infographic #2 -- two claims from the Milbank Quarterly paper at two
 * different confidence levels: the industrial-design-parallel claim (medium
 * confidence) and the addiction/nicotine-equivalence claim (low confidence).
 * Bar fill widths are a visual/ordinal encoding of "medium" vs "low" (mirrors
 * the owner-approved infographic spec) -- no percentage number is rendered as
 * text, so nothing here reads as a fabricated statistic.
 */
const LEVEL_STYLES = {
  medium: { fill: "w-[58%] bg-[#2F6146]", text: "text-[#155C3C]" },
  low: { fill: "w-[20%] bg-[#9A4012]", text: "text-[#9A4012]" },
} as const;

export function UpfConfidenceLadder() {
  const data = (
    upfArticle.infographics as unknown as {
      confidence: {
        eyebrow: string;
        title: string;
        claims: { id: string; text: string; level: "medium" | "low"; levelLabel: string }[];
        caption: string;
      };
    }
  ).confidence;

  return (
    <UpfInfographicFrame eyebrow={data.eyebrow} title={data.title} caption={data.caption}>
      <div className="flex flex-col gap-5">
        {data.claims.map((claim) => {
          const style = LEVEL_STYLES[claim.level];
          return (
            <div key={claim.id}>
              <div className="mb-1.5 flex items-baseline justify-between gap-3">
                <span className="text-sm font-semibold text-[#111318]">{claim.text}</span>
                <span
                  className={cn(
                    "shrink-0 font-mono text-[11px] font-bold tracking-[0.02em] whitespace-nowrap",
                    style.text,
                  )}
                >
                  {claim.levelLabel}
                </span>
              </div>
              <div className="h-[9px] w-full overflow-hidden rounded-full bg-black/[0.06]">
                <div className={cn("h-full rounded-full", style.fill)} />
              </div>
            </div>
          );
        })}
      </div>
    </UpfInfographicFrame>
  );
}
