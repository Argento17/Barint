import type { SnackWhyLanded } from "@/lib/comparisons/snack-types";

export function WhyThisLandedHere({ sections }: { sections: SnackWhyLanded }) {
  return (
    <div className="space-y-5">
      <section>
        <p className="text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">מה שבלט</p>
        <p className="mt-2 text-sm leading-7 text-[#313834]">{sections.highlight_he}</p>
      </section>
      {sections.limit_he ? (
        <section>
          <p className="text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">מה שהגביל</p>
          <p className="mt-2 text-sm leading-7 text-[#313834]">{sections.limit_he}</p>
        </section>
      ) : null}
      {sections.uncertainty_he ? (
        <section>
          <p className="text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">
            מה שלא ניתן לאמת
          </p>
          <p className="mt-2 text-sm leading-7 text-[#313834]">{sections.uncertainty_he}</p>
        </section>
      ) : null}
    </div>
  );
}
