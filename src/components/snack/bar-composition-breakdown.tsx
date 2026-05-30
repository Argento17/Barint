import type { SnackCompositionRow } from "@/lib/comparisons/snack-types";

export function BarCompositionBreakdown({ rows }: { rows: SnackCompositionRow[] }) {
  return (
    <div className="space-y-3">
      <p className="text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">מבנה החטיף</p>
      {rows.map((row) => (
        <article
          key={row.dimension}
          className="rounded-[0.85rem] border border-black/[0.06] bg-[#F7F7F2]/50 px-4 py-3"
        >
          <div className="flex items-baseline justify-between gap-3">
            <p className="text-sm font-bold text-[#111318]">{row.dimension}</p>
            <p className="text-sm text-[#4E5663]">{row.value}</p>
          </div>
          <p className="mt-2 text-sm leading-7 text-[#313834]">{row.effect_he}</p>
        </article>
      ))}
    </div>
  );
}
