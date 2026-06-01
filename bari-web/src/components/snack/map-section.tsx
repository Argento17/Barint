"use client";

import { useState } from "react";
import { ChevronDown } from "lucide-react";

import { formatSnackScore } from "@/lib/comparisons/snack-page-data";
import type { SnackProduct } from "@/lib/comparisons/snack-types";
import { cn } from "@/lib/utils";

type MapSectionProps = {
  title: string;
  caption: string;
  products: SnackProduct[];
  annotatedIds: string[];
  annotations: Record<string, string>;
  defaultCollapsed?: boolean;
  collapseLabel?: string;
};

export function MapSection({
  title,
  caption,
  products,
  annotatedIds,
  annotations,
  defaultCollapsed = false,
  collapseLabel = "להצגת מפת המדף",
}: MapSectionProps) {
  const [open, setOpen] = useState(!defaultCollapsed);
  const annotated = annotatedIds
    .map((id) => products.find((product) => product.id === id))
    .filter((product): product is SnackProduct => Boolean(product));

  return (
    <section className="py-12 md:py-16">
      {defaultCollapsed ? (
        <button
          type="button"
          onClick={() => setOpen((value) => !value)}
          className="inline-flex items-center gap-2 text-sm font-semibold text-[#1F8F6A]"
        >
          {open ? "הסתר מפת המדף" : collapseLabel}
          <ChevronDown className={cn("size-4 transition-transform", open && "rotate-180")} />
        </button>
      ) : (
        <h2 className="text-right text-[1.35rem] font-semibold tracking-[-0.03em] text-[#111318]">
          {title}
        </h2>
      )}

      {open ? (
        <>
          {defaultCollapsed ? (
            <h2 className="mt-4 text-right text-[1.35rem] font-semibold tracking-[-0.03em] text-[#111318]">
              {title}
            </h2>
          ) : null}

          <div className="mt-6 md:hidden">
            <ul className="space-y-3">
              {annotated.map((product) => (
                <li
                  key={product.id}
                  className="rounded-[0.85rem] border border-black/[0.08] bg-[#FFFFFF] px-4 py-3"
                >
                  <p className="text-sm font-bold text-[#111318]">
                    {annotations[product.id] ?? formatSnackScore(product)}
                  </p>
                  <p className="mt-1 text-sm text-[#4E5663]">{product.name_he}</p>
                </li>
              ))}
            </ul>
          </div>

          <div className="relative mx-auto mt-6 hidden max-w-3xl md:block">
            <div className="relative min-h-[280px] rounded-[1rem] border border-black/[0.08] bg-[#F7F7F2]/80">
              <div className="absolute inset-x-0 top-1/2 border-t border-black/[0.08]" />
              <div className="absolute inset-y-0 left-1/2 border-r border-black/[0.08]" />
              {products.map((product) => (
                <div
                  key={product.id}
                  title={`${product.name_he} · ${formatSnackScore(product)}`}
                  className={cn(
                    "absolute size-2.5 -translate-x-1/2 -translate-y-1/2 rounded-full border border-white shadow-sm",
                    product.nova === 2
                      ? "bg-[#1F8F6A]"
                      : product.nova === 3
                        ? "bg-[#6B7280]"
                        : "bg-[#111318]"
                  )}
                  style={{ left: `${product.x}%`, top: `${product.y}%` }}
                />
              ))}
              {annotated.map((product) => (
                <p
                  key={`label-${product.id}`}
                  className="absolute max-w-[11rem] rounded-full bg-[#FFFFFF]/92 px-2.5 py-1 text-[0.7rem] font-semibold text-[#111318] shadow-sm"
                  style={{
                    left: `${Math.min(product.x + 4, 72)}%`,
                    top: `${Math.max(product.y - 8, 6)}%`,
                  }}
                >
                  {annotations[product.id]}
                </p>
              ))}
              <p className="absolute right-3 top-2 text-[0.65rem] font-semibold text-[#4E5663]">
                סוכר מרובה
              </p>
              <p className="absolute right-3 bottom-2 text-[0.65rem] font-semibold text-[#4E5663]">
                מקור מתיקות יחיד
              </p>
              <p className="absolute left-3 top-2 text-[0.65rem] font-semibold text-[#4E5663]">
                NOVA4
              </p>
              <p className="absolute left-3 bottom-2 text-[0.65rem] font-semibold text-[#4E5663]">
                עיבוד מינימלי
              </p>
            </div>
          </div>

          <p className="mt-4 text-center text-sm leading-7 text-[#4E5663]">{caption}</p>
        </>
      ) : null}
    </section>
  );
}
