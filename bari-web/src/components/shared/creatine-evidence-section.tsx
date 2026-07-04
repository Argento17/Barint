"use client";

// TASK-492C FIX 1 (design-critic C1): evidence prose relocated out of the pre-table
// categoryNote (was ~772 words, buried the comparison below the first desktop viewport)
// into a dedicated section that renders BELOW the product comparison tables. Every
// sentence is copied verbatim from creatine-page-data.ts's original categoryNote —
// no rewording, relocation only.
//
// Collapsible per-topic subsections, one open at a time — mirrors the collapsible
// pattern already used by MagnesiumSafetyBox (magnesium-safety-box.tsx): plain button
// + chevron toggle, no sheet/modal/overlay (ExpansionSection rule extended to this
// inline-only pattern by convention).

import { useState } from "react";
import { ChevronDown } from "lucide-react";

import type { CreatineEvidenceTopic } from "@/lib/comparisons/creatine-page-data";
import { cn } from "@/lib/utils";

function EvidenceTopicRow({
  topic,
  open,
  onToggle,
}: {
  topic: CreatineEvidenceTopic;
  open: boolean;
  onToggle: () => void;
}) {
  return (
    <div className="border-b border-[rgba(17,19,24,0.08)] last:border-b-0">
      <button
        type="button"
        onClick={onToggle}
        aria-expanded={open}
        className="flex w-full items-center justify-between gap-2 py-3 text-start focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#167A58]"
      >
        <span className="text-[13px] font-bold leading-[1.3] text-[#111318]">
          {topic.heading}
        </span>
        <ChevronDown
          strokeWidth={1.75}
          aria-hidden
          className={cn(
            "size-[16px] shrink-0 text-[#B5BBB6] transition-transform duration-200 motion-reduce:transition-none",
            open && "rotate-180 text-[#9A9FA6]"
          )}
        />
      </button>
      {open ? (
        <div className="flex flex-col gap-2 pb-3">
          {topic.paragraphs.map((para, i) => (
            <p
              key={i}
              className="text-[12.5px] leading-[1.6] text-[#4E5663]"
            >
              {para}
            </p>
          ))}
        </div>
      ) : null}
    </div>
  );
}

export function CreatineEvidenceSection({
  sections,
}: {
  sections: CreatineEvidenceTopic[];
}) {
  const [openId, setOpenId] = useState<string | null>(null);

  return (
    <div dir="rtl" className="border-t border-[rgba(17,19,24,0.08)] pt-3">
      <h2 className="mb-1 font-mono text-[11px] font-bold uppercase tracking-[0.1em] text-[#6E756D]">
        העדות המדעית והרקע המלא
      </h2>
      <div>
        {sections.map((topic) => (
          <EvidenceTopicRow
            key={topic.id}
            topic={topic}
            open={openId === topic.id}
            onToggle={() => setOpenId((cur) => (cur === topic.id ? null : topic.id))}
          />
        ))}
      </div>
    </div>
  );
}
