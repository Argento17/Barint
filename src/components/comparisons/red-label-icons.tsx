"use client";

import { cn } from "@/lib/utils";

const RED_LABEL_COPY: Record<string, string> = {
  sugar: "סוכר",
  saturated_fat: "שומן רווי",
  sodium: "נתרן",
};

export function RedLabelIcons({
  labels,
  className,
}: {
  labels: string[];
  className?: string;
}) {
  if (!labels.length) {
    return (
      <span className={cn("text-xs text-[#7A817C]", className)}>ללא תווית אדומה</span>
    );
  }

  return (
    <div className={cn("flex flex-wrap gap-1.5", className)}>
      {labels.map((label) => (
        <span
          key={label}
          className="inline-flex items-center gap-1 rounded-md border border-[#C62828]/25 bg-[#C62828]/[0.06] px-2 py-0.5 text-[0.65rem] font-bold text-[#C62828]"
          title={`תווית אדומה ישראלית: ${RED_LABEL_COPY[label] ?? label}`}
        >
          <span
            className="inline-flex size-3.5 items-center justify-center rounded-sm bg-[#C62828] text-[0.5rem] font-black text-white"
            aria-hidden
          >
            !
          </span>
          {RED_LABEL_COPY[label] ?? label}
        </span>
      ))}
    </div>
  );
}
