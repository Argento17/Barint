// Chocolate-bar hero card — build brief item 2 (§3 / "high-intensity" section). Self-hosted
// product image + a compact label-breakdown key, derived only from that section's signed-off
// text: the bar declares three sweeteners: two sugar alcohols the law reaches (the statutory
// warning), one (sucralose) it does not. Group headings are looked up live from the data
// module; sweetener names and captions are reused/verified constants from
// sweetener-guide-visuals.ts. No new copy.

import Image from "next/image";

import {
  SWEETENER_CHOC_BAR_IMAGE,
  SWEETENER_CHOC_LABEL_BREAKDOWN,
  sectionHeadingById,
} from "@/lib/guides/sweetener-guide-visuals";

export function ChocolateBarHeroCard() {
  return (
    <figure className="mt-4 overflow-hidden rounded-xl border border-black/[0.08] bg-white">
      <div className="flex gap-4 p-4 sm:p-5">
        <div className="relative size-20 shrink-0 overflow-hidden rounded-lg border border-black/[0.06] bg-[#F7F7F2] sm:size-24">
          <Image
            src={SWEETENER_CHOC_BAR_IMAGE}
            alt={sectionHeadingById("high-intensity")}
            fill
            sizes="96px"
            className="object-contain p-1.5"
          />
        </div>
        <div className="min-w-0 flex-1 space-y-2.5">
          {SWEETENER_CHOC_LABEL_BREAKDOWN.map((group) => (
            <div key={group.headingSectionId}>
              <div className="flex flex-wrap items-center gap-1.5">
                {group.sweetenerNames.map((name) => (
                  <span
                    key={name}
                    className="inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-[11px] font-bold"
                    style={
                      group.lawReaches
                        ? { background: "#FCEAD9", borderColor: "#B0451033", color: "#9A4012" }
                        : { background: "#E7F4EC", borderColor: "#1E7A4F33", color: "#155C3C" }
                    }
                  >
                    <span
                      aria-hidden="true"
                      className="size-1.5 rounded-full"
                      style={{ background: group.lawReaches ? "#B04510" : "#1E7A4F" }}
                    />
                    {name}
                  </span>
                ))}
              </div>
              <p className="mt-1 text-[11px] leading-[1.5] text-[#5E6560]">{group.caption}</p>
            </div>
          ))}
        </div>
      </div>
    </figure>
  );
}
