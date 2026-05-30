"use client";

import { comparisonWebSectionPaddingClass } from "@/lib/design/bari-comparison-tokens";
import { cn } from "@/lib/utils";

export interface ShelfLensOption<TFilterId extends string = string> {
  id: TFilterId;
  label: string;
}

export function CategoryShelfLenses<TFilterId extends string = string>({
  activeFilters,
  onToggle,
  lensOptions,
  wide = false,
}: {
  activeFilters: TFilterId[];
  onToggle: (filter: TFilterId) => void;
  lensOptions: ShelfLensOption<TFilterId>[];
  wide?: boolean;
}) {
  return (
    <div className={cn("px-4 pb-2", wide && cn(comparisonWebSectionPaddingClass(), "lg:pb-3"))}>
      <div className="flex flex-wrap items-center gap-1.5">
        {lensOptions.map((option) => {
          const isActive = activeFilters.includes(option.id);
          return (
            <button
              key={option.id}
              type="button"
              onClick={() => onToggle(option.id)}
              className="rounded-full border px-3 py-1.5 text-[12px] font-medium transition-colors duration-150"
              style={{
                borderColor: isActive ? "#C9D8CF" : "#D9DDD7",
                backgroundColor: isActive ? "#EEF5F1" : "#FAFAF7",
                color: isActive ? "#295C49" : "#4E5663",
              }}
            >
              {option.label}
            </button>
          );
        })}
      </div>
    </div>
  );
}
