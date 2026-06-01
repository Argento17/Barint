"use client";

import { useState } from "react";
import { ChevronDown } from "lucide-react";

import type {
  SnackEngineFilters,
  SnackGrade,
  SnackNOVA,
  SnackProduct,
} from "@/lib/comparisons/snack-types";
import { SNACK_SEGMENTS } from "@/lib/comparisons/snack-types";
import { cn } from "@/lib/utils";

const GRADES: SnackGrade[] = ["B", "C", "D", "E"];
const NOVA_OPTIONS: SnackNOVA[] = [2, 3, 4];

export const defaultSnackEngineFilters: SnackEngineFilters = {
  grades: [],
  nova: [],
  segment: null,
  scoreMin: 0,
  scoreMax: 100,
};

export function FilterPanel({
  filters,
  onApply,
  onClear,
}: {
  filters: SnackEngineFilters;
  onApply: (next: SnackEngineFilters) => void;
  onClear: () => void;
}) {
  const [open, setOpen] = useState(false);
  const [draft, setDraft] = useState(filters);

  function toggleGrade(grade: SnackGrade) {
    setDraft((current) => ({
      ...current,
      grades: current.grades.includes(grade)
        ? current.grades.filter((item) => item !== grade)
        : [...current.grades, grade],
    }));
  }

  function toggleNova(nova: SnackNOVA) {
    setDraft((current) => ({
      ...current,
      nova: current.nova.includes(nova)
        ? current.nova.filter((item) => item !== nova)
        : [...current.nova, nova],
    }));
  }

  return (
    <div className="relative">
      <button
        type="button"
        onClick={() => setOpen((value) => !value)}
        className="inline-flex items-center gap-2 rounded-full border border-black/[0.1] bg-[#FFFFFF] px-4 py-2 text-sm font-semibold text-[#111318]"
      >
        סינון
        <ChevronDown className={cn("size-4 transition-transform", open && "rotate-180")} />
      </button>

      {open ? (
        <div className="absolute right-0 z-20 mt-2 w-[min(100vw-2rem,22rem)] rounded-[1rem] border border-black/[0.08] bg-[#FFFFFF] p-4 shadow-lg">
          <p className="text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">דרגה</p>
          <div className="mt-2 flex flex-wrap gap-2">
            {GRADES.map((grade) => (
              <button
                key={grade}
                type="button"
                onClick={() => toggleGrade(grade)}
                className={cn(
                  "rounded-full border px-3 py-1.5 text-sm font-semibold",
                  draft.grades.includes(grade)
                    ? "border-[#1F8F6A] bg-[#E8F5EF] text-[#176F53]"
                    : "border-black/[0.08] text-[#4E5663]"
                )}
              >
                {grade}
              </button>
            ))}
          </div>

          <p className="mt-4 text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">NOVA</p>
          <div className="mt-2 flex flex-wrap gap-2">
            {NOVA_OPTIONS.map((nova) => (
              <button
                key={nova}
                type="button"
                onClick={() => toggleNova(nova)}
                className={cn(
                  "rounded-full border px-3 py-1.5 text-sm font-semibold",
                  draft.nova.includes(nova)
                    ? "border-[#1F8F6A] bg-[#E8F5EF] text-[#176F53]"
                    : "border-black/[0.08] text-[#4E5663]"
                )}
              >
                {nova}
              </button>
            ))}
          </div>

          <p className="mt-4 text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">קטגוריה</p>
          <select
            value={draft.segment ?? ""}
            onChange={(event) =>
              setDraft((current) => ({
                ...current,
                segment: event.target.value || null,
              }))
            }
            className="mt-2 w-full rounded-lg border border-black/[0.08] bg-[#FFFFFF] px-3 py-2 text-sm"
          >
            <option value="">כל הקטגוריות</option>
            {SNACK_SEGMENTS.map((segment) => (
              <option key={segment} value={segment}>
                {segment}
              </option>
            ))}
          </select>

          <p className="mt-4 text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">ציון</p>
          <div className="mt-2 space-y-2">
            <input
              type="range"
              min={0}
              max={100}
              value={draft.scoreMin}
              onChange={(event) =>
                setDraft((current) => ({
                  ...current,
                  scoreMin: Number(event.target.value),
                }))
              }
              className="w-full"
            />
            <input
              type="range"
              min={0}
              max={100}
              value={draft.scoreMax}
              onChange={(event) =>
                setDraft((current) => ({
                  ...current,
                  scoreMax: Number(event.target.value),
                }))
              }
              className="w-full"
            />
            <p className="text-center text-sm text-[#4E5663]">
              {draft.scoreMin} – {draft.scoreMax}
            </p>
          </div>

          <div className="mt-4 flex gap-2">
            <button
              type="button"
              onClick={() => {
                onApply(draft);
                setOpen(false);
              }}
              className="flex-1 rounded-full bg-[#1F8F6A] px-4 py-2 text-sm font-bold text-white"
            >
              החל
            </button>
            <button
              type="button"
              onClick={() => {
                setDraft(defaultSnackEngineFilters);
                onClear();
                setOpen(false);
              }}
              className="rounded-full border border-black/[0.08] px-4 py-2 text-sm font-semibold text-[#4E5663]"
            >
              נקה
            </button>
          </div>
        </div>
      ) : null}
    </div>
  );
}

export function snackMatchesEngineFilters(product: SnackProduct, filters: SnackEngineFilters) {
  if (!product.displayable) return false;
  if (filters.grades.length && (!product.grade || !filters.grades.includes(product.grade))) {
    return false;
  }
  if (filters.nova.length && (product.nova == null || !filters.nova.includes(product.nova))) {
    return false;
  }
  if (filters.segment && product.segment !== filters.segment) {
    return false;
  }
  if (product.score != null) {
    if (product.score < filters.scoreMin || product.score > filters.scoreMax) {
      return false;
    }
  }
  return true;
}
