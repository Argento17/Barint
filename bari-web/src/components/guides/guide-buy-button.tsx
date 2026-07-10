// Guide buy-button slot (TASK-504, plan §4).
//
// Mirrors the existing dormant buy-affordance treatment verbatim
// (src/components/inventory/product-table.tsx:239-278, the /catalog `buyUrl` precedent
// named in the plan) rather than importing it directly — that function is private to
// product-table.tsx and coupled to the inventory row's layout. Same visual language,
// exported so guides can reuse it.
//
// Governance (plan §4, mechanical separation): `buyUrl` is a standalone field on
// GuideProductVM, never derived from bars/bucket/defaultPick. This component takes
// ONLY `buyUrl` — it must never receive or branch on verdict data. Renders on every
// product row regardless of bucket; a missing buyUrl shows the dormant state, not a
// hidden button (missing link ≠ missing product).

import { Store } from "lucide-react";

export function GuideBuyButton({ buyUrl }: { buyUrl: string | null }) {
  if (buyUrl) {
    return (
      <a
        href={buyUrl}
        target="_blank"
        rel="noopener noreferrer nofollow"
        title="צפייה במוצר באתר הרשת"
        data-testid="guide-buy-button"
        className="inline-flex items-center gap-1.5 whitespace-nowrap rounded-full border px-3 py-1 text-xs font-semibold transition-colors"
        style={{
          borderColor: "rgba(23,111,83,0.28)",
          color: "var(--bari-green-deep, #176F53)",
          background: "#FAFAF8",
        }}
      >
        <Store className="h-3 w-3" aria-hidden />
        צפייה ברשת
      </a>
    );
  }

  return (
    <button
      type="button"
      disabled
      aria-disabled="true"
      title="בקרוב — צפייה במוצר באתר הרשת"
      data-testid="guide-buy-button-dormant"
      className="inline-flex items-center gap-1.5 whitespace-nowrap rounded-full border px-3 py-1 text-xs font-semibold cursor-not-allowed select-none"
      style={{
        borderColor: "rgba(17,19,24,0.10)",
        color: "var(--fg3, #5E6560)",
        background: "transparent",
      }}
    >
      <Store className="h-3 w-3 opacity-40" aria-hidden />
      צפייה ברשת
      <span className="text-[10px] opacity-60">· בקרוב</span>
    </button>
  );
}
