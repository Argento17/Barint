// Guide layer 2 headline (TASK-504B — Product D7 empty-shortlist ruling,
// supplement_guides_d7_cosign_v1.md §1).
//
// Rendered ONLY when the `clears_all` bucket is empty. Leads the products section,
// BEFORE the bucket table, with the honest "no product clears every bar" finding —
// then GuideProductTable promotes `passes_with_flag` immediately below it as the
// practical shortlist. This component renders Content-authored text VERBATIM; it does
// not compute, summarize, or paraphrase.

import { comparisonWebSectionPaddingClass } from "@/lib/design/bari-comparison-tokens";
import type { GuideHeadlineFinding as GuideHeadlineFindingVM } from "@/lib/view-models";
import { cn } from "@/lib/utils";

export function GuideHeadlineFinding({
  finding,
  wide = false,
}: {
  finding: GuideHeadlineFindingVM;
  wide?: boolean;
}) {
  return (
    <div
      className={cn("px-4 pb-4", wide && comparisonWebSectionPaddingClass())}
      dir="rtl"
      data-testid="guide-headline-finding"
    >
      <div
        className="rounded-2xl border p-4"
        style={{ borderColor: "#E7DDBE", background: "#FBF8EE" }}
      >
        <p className="text-[15px] font-extrabold leading-[1.4] text-[#3A3222]">
          {finding.title}
        </p>
        <div className="mt-2.5 space-y-2.5">
          {finding.body.map((paragraph, i) => (
            <p key={i} className="text-[13px] leading-[1.6] text-[#5C523A]">
              {paragraph}
            </p>
          ))}
        </div>
      </div>
    </div>
  );
}
