import { cn } from "@/lib/utils";
import { UpfInfographicFrame } from "@/components/blog/upf-infographic-frame";
import { upfArticle } from "@/lib/blog/upf-article-content";

/**
 * Infographic #3 -- SCHEMATIC ONLY, per the HARD RULE against inventing
 * product/nutrition data. "מוצר א׳" / "מוצר ב׳" are generic placeholders, not
 * real products; no barcode, brand, or numeric score is shown anywhere here --
 * only a directional "higher/lower" verdict, matching the owner-approved
 * infographic spec. The eyebrow and caption both say "המחשה" (illustration)
 * so this can never be mistaken for a live product comparison.
 */
export function UpfSchematicSplit() {
  const data = (
    upfArticle.infographics as unknown as {
      schematic: {
        eyebrow: string;
        title: string;
        band: string;
        products: {
          id: string;
          name: string;
          detail: string;
          highlight: string;
          direction: "up" | "down";
          verdict: string;
        }[];
        caption: string;
      };
    }
  ).schematic;

  return (
    <UpfInfographicFrame eyebrow={data.eyebrow} title={data.title} caption={data.caption}>
      <div className="mb-4 text-center">
        <span className="inline-flex items-center gap-2 rounded-full bg-black/[0.05] px-3.5 py-1.5 font-mono text-xs font-bold tracking-[0.03em] text-[#4E5663]">
          {data.band}
        </span>
      </div>
      <div className="grid grid-cols-1 gap-3.5 sm:grid-cols-2">
        {data.products.map((product) => {
          const isUp = product.direction === "up";
          return (
            <div
              key={product.id}
              className="flex flex-col gap-2.5 rounded-[0.85rem] border border-black/[0.07] p-4"
            >
              <p className="text-sm font-extrabold text-[#111318]">{product.name}</p>
              <p className="text-[13px] leading-[1.5] text-[#4E5663]">
                {product.detail}
                <br />
                <span className="font-semibold text-[#111318]">{product.highlight}</span>
              </p>
              <p className="text-center text-base leading-none text-[#8A8F98]" aria-hidden>
                {isUp ? "↑" : "↓"}
              </p>
              <p
                className={cn(
                  "rounded-lg px-2.5 py-2 text-center text-sm font-bold",
                  isUp ? "bg-[#E7F4EC] text-[#155C3C]" : "bg-[#FCEAD9] text-[#9A4012]",
                )}
              >
                {product.verdict}
              </p>
            </div>
          );
        })}
      </div>
    </UpfInfographicFrame>
  );
}
