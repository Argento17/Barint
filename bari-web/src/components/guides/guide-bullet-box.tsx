// GuideBulletBox — TASK-577 (magnesium guide v3 STRUCTURAL rebuild).
//
// Generic heading + bullet-list presentational shell, reused for both the "מה גילינו"
// (what-we-found) box directly under the H1 and the "איך לקרוא תווית מגנזיום"
// (how-to-read-the-label) section after the products. Structure only — every heading
// and bullet string rendered through this component is either owner-dictated verbatim
// or an already gate-2-approved v2 string; this component authors none of it.
//
// Not yet reviewed by the Design Agent (no v3 visual spec exists yet — this task is a
// STRUCTURAL rebuild only, per the dispatch). Reuses the same neutral box idiom
// already shipped for the market-gaps box (guide-product-table.tsx: rounded-2xl
// border, #F7F8F6 background) rather than inventing a new visual treatment, so the
// page stays token-conformant pending that review.

import { comparisonWebSectionPaddingClass } from "@/lib/design/bari-comparison-tokens";
import { cn } from "@/lib/utils";

export function GuideBulletBox({
  heading,
  bullets,
  boxed = true,
  wide = false,
  testId,
}: {
  heading: string;
  bullets: string[];
  /** true (default) = the "מה גילינו" callout-box treatment; false = a plain
   *  heading+list section, matching GuideEducationSpine's own heading/body scale
   *  (used for the "how to read the label" section, which sits among the education
   *  content rather than as a standalone callout). */
  boxed?: boolean;
  wide?: boolean;
  testId?: string;
}) {
  if (bullets.length === 0) return null;

  const list = (
    <ul className="space-y-1.5" data-testid={testId}>
      {bullets.map((bullet, i) => (
        <li
          key={i}
          className="flex items-start gap-2 text-[13px] leading-[1.55] text-[#3E444A]"
        >
          <span aria-hidden className="mt-[7px] size-1 shrink-0 rounded-full bg-[#8A8F86]" />
          <span>{bullet}</span>
        </li>
      ))}
    </ul>
  );

  if (!boxed) {
    return (
      <div
        className={cn("px-4 py-4", wide && comparisonWebSectionPaddingClass())}
        dir="rtl"
        data-testid={testId ? `${testId}-section` : undefined}
      >
        <h2 className="text-[15px] font-extrabold tracking-[-0.02em] text-[#111318]">{heading}</h2>
        <div className="mt-2.5">{list}</div>
      </div>
    );
  }

  return (
    <div className={cn("px-4 pb-4", wide && comparisonWebSectionPaddingClass())} dir="rtl">
      <div
        className="rounded-2xl border p-4"
        style={{ borderColor: "#E2E5E2", background: "#F7F8F6" }}
        data-testid={testId ? `${testId}-box` : undefined}
      >
        <h2 className="text-[13px] font-extrabold text-[#111318]">{heading}</h2>
        <div className="mt-2.5">{list}</div>
      </div>
    </div>
  );
}
