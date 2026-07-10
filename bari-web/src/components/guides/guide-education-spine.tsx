// Guide layer 3 — education spine (TASK-504, plan §3 item 3).
// Generic section renderer: heading + body paragraphs. Content (what it does, forms
// explained, safety, FAQ-grade depth) is authored separately per guide — this component
// carries structure only, no guide-specific copy.

import { comparisonWebSectionPaddingClass } from "@/lib/design/bari-comparison-tokens";
import type { GuideEducationSection } from "@/lib/view-models";
import { cn } from "@/lib/utils";

export function GuideEducationSpine({
  sections,
  wide = false,
}: {
  sections: GuideEducationSection[];
  wide?: boolean;
}) {
  if (sections.length === 0) return null;

  return (
    <section
      className={cn("px-4 py-6", wide && cn(comparisonWebSectionPaddingClass(), "lg:py-8"))}
      dir="rtl"
      data-testid="guide-education-spine"
    >
      <div className="space-y-6">
        {sections.map((section, i) => (
          <div key={`${i}-${section.heading.slice(0, 12)}`}>
            <h2 className="text-[15px] font-extrabold tracking-[-0.02em] text-[#111318]">
              {section.heading}
            </h2>
            <div className="mt-2 space-y-2">
              {section.body.map((paragraph, j) => (
                <p key={j} className="text-[13px] leading-[1.6] text-[#3E444A]">
                  {paragraph}
                </p>
              ))}
            </div>
            {/* TASK-575 — structured source list (copy package Slot 8), rendered as
                clickable links rather than bare citation text. */}
            {section.sources && section.sources.length > 0 ? (
              <ul className="mt-3 space-y-3" data-testid="guide-education-sources">
                {section.sources.map((source, k) => (
                  <li key={k} className="text-[13px] leading-[1.6] text-[#3E444A]">
                    <p>{source.label}</p>
                    <a
                      href={source.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      dir="ltr"
                      className="mt-0.5 inline-block break-all text-[12px] font-semibold text-[#167A58] underline underline-offset-2"
                    >
                      {source.url}
                    </a>
                  </li>
                ))}
              </ul>
            ) : null}
          </div>
        ))}
      </div>
    </section>
  );
}
