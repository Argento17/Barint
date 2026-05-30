"use client";

import { useState } from "react";
import { ChevronDown } from "lucide-react";

import { SnackShelfProductImage } from "@/components/snack/snack-shelf-product-image";
import { SnackScoreChip } from "@/components/snack/snack-score-chip";
import type { SnackProduct } from "@/lib/comparisons/snack-types";
import { cn } from "@/lib/utils";

export type ComparisonMomentProps = {
  title: string;
  driverSentence: string;
  products: SnackProduct[];
  detailLines?: string[];
  spanLabel?: string;
};

export function ComparisonMoment({
  title,
  driverSentence,
  products,
  detailLines,
  spanLabel,
}: ComparisonMomentProps) {
  const [open, setOpen] = useState(false);
  const isTriple = products.length === 3;
  const isSpotlight = products.length === 1;

  return (
    <section className="py-14 md:py-20">
      <h2 className="text-right text-[1.45rem] font-semibold leading-snug tracking-[-0.03em] text-[#111318] md:text-[1.6rem]">
        {title}
      </h2>

      {spanLabel ? (
        <p className="mt-2 text-sm font-semibold text-[#1F8F6A]">{spanLabel}</p>
      ) : null}

      <div
        className={cn(
          "mt-10 grid gap-10",
          isSpotlight && "max-w-md",
          isTriple && "md:grid-cols-3",
          !isSpotlight && !isTriple && "md:grid-cols-2"
        )}
      >
        {products.map((product) => (
          <div key={product.id} className="flex flex-col items-center text-center">
            <SnackShelfProductImage product={product} variant="comparison" />
            <div className="mt-4">
              <SnackScoreChip
                score={product.score}
                grade={product.grade}
                displayable={product.displayable}
                variant="comparison"
              />
            </div>
            <p className="mt-4 max-w-[18rem] text-[0.95rem] font-semibold leading-snug text-[#111318]">
              {product.name_he}
            </p>
          </div>
        ))}
      </div>

      <p className="mx-auto mt-10 max-w-3xl text-center text-[1.03rem] leading-8 text-[#313834]">
        {driverSentence}
      </p>

      {detailLines?.length ? (
        <div className="mt-4 flex justify-center">
          <button
            type="button"
            onClick={() => setOpen((value) => !value)}
            className="inline-flex items-center gap-1.5 text-sm font-semibold text-[#1F8F6A]"
          >
            {open ? "סגור פרטים" : "פרטים נוספים"}
            <ChevronDown className={cn("size-4 transition-transform", open && "rotate-180")} />
          </button>
        </div>
      ) : null}

      {open && detailLines?.length ? (
        <ul className="mx-auto mt-4 max-w-xl space-y-2 text-sm leading-7 text-[#4E5663]">
          {detailLines.map((line) => (
            <li key={line} className="flex gap-2">
              <span className="mt-2 size-1.5 shrink-0 rounded-full bg-[#1F8F6A]" aria-hidden />
              <span>{line}</span>
            </li>
          ))}
        </ul>
      ) : null}
    </section>
  );
}
