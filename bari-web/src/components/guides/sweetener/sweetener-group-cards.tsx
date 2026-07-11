// "Three groups on the shelf" — build brief item 3. Turns §§2–4's prose into a scannable
// map. Headings are looked up live from the signed-off data module by section id (never
// re-typed); product-name tags are verified verbatim substrings from
// sweetener-guide-visuals.ts. No new copy is introduced by this component.

import { ScrollReveal } from "@/components/guides/sweetener/scroll-reveal";
import { SweetenerSectionIcon } from "@/components/guides/sweetener/section-icon";
import {
  SWEETENER_GROUP_CARDS,
  sectionHeadingById,
} from "@/lib/guides/sweetener-guide-visuals";

export function SweetenerGroupCards() {
  return (
    <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
      {SWEETENER_GROUP_CARDS.map((group, i) => (
        <ScrollReveal key={group.sectionId} delayMs={i * 80}>
          <a
            href={`#${group.sectionId}`}
            className="flex h-full flex-col gap-2.5 rounded-xl border border-black/[0.08] bg-white p-4 transition-colors hover:border-[#1E7A4F]/40"
          >
            <SweetenerSectionIcon icon={group.icon} />
            <h3 className="text-[13px] font-extrabold leading-tight tracking-[-0.01em] text-[#111318]">
              {sectionHeadingById(group.sectionId)}
            </h3>
            <ul className="mt-auto flex flex-wrap gap-1.5 pt-1">
              {group.productMentions.map((name) => (
                <li
                  key={name}
                  className="rounded-full bg-[#F1F1EC] px-2 py-0.5 text-[10.5px] font-medium leading-relaxed text-[#4E5663]"
                >
                  {name}
                </li>
              ))}
            </ul>
          </a>
        </ScrollReveal>
      ))}
    </div>
  );
}
