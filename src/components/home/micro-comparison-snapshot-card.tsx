"use client";

import Image from "next/image";
import Link from "next/link";
import { ChevronLeft } from "lucide-react";

import type { ResolvedMicroSnapshot } from "@/lib/home/micro-comparison-snapshots";
import { cn } from "@/lib/utils";

function ProductColumn({
  product,
  strengths,
  side,
}: {
  product: ResolvedMicroSnapshot["left"];
  strengths: [string, string];
  side: "left" | "right";
}) {
  const title = product.displayTitle ?? product.shortName;
  const brand = product.brandLine ?? product.productTypeLabel;

  return (
    <div
      className={cn(
        "flex flex-1 flex-col gap-2 rounded-xl border border-black/[0.06] bg-[#F7F7F2]/50 p-3",
        side === "right" && "bg-[#FFFFFF]"
      )}
    >
      <div className="flex items-start gap-2.5">
        <div className="relative h-14 w-10 shrink-0">
          {product.image_url ? (
            <Image
              src={product.image_url}
              alt=""
              fill
              className="object-contain"
              sizes="40px"
            />
          ) : null}
        </div>
        <div className="min-w-0 flex-1 text-right">
          <p className="text-[0.6rem] font-bold text-[#1F8F6A]">{brand}</p>
          <p className="line-clamp-2 text-xs font-extrabold leading-snug text-[#111318]">
            {title}
          </p>
        </div>
      </div>
      <div className="flex items-baseline gap-2">
        <span className="text-2xl font-extrabold tabular-nums tracking-[-0.04em] text-[#111318]">
          {product.score}
        </span>
        <span className="text-[0.65rem] font-semibold text-[#7A817C]">ציון Bari</span>
      </div>
      <ul className="space-y-1">
        {strengths.map((s) => (
          <li
            key={s}
            className="text-[0.65rem] font-semibold leading-snug text-[#4E5663] before:ml-1 before:text-[#1F8F6A] before:content-['·']"
          >
            {s}
          </li>
        ))}
      </ul>
    </div>
  );
}

export function MicroComparisonSnapshotCard({ snapshot }: { snapshot: ResolvedMicroSnapshot }) {
  return (
    <Link
      href={snapshot.href}
      className="group block h-full min-h-[17rem] w-[84vw] max-w-[32rem] shrink-0 snap-center rounded-[1.5rem] border border-black/[0.08] bg-[#FFFFFF] p-4 shadow-[0_20px_60px_-48px_rgba(17,19,24,0.2)] transition-[border-color,box-shadow,transform] duration-300 hover:-translate-y-0.5 hover:border-[#1F8F6A]/22 hover:shadow-[0_24px_64px_-40px_rgba(31,143,106,0.2)] sm:w-[30rem] md:min-h-[18rem] md:p-5"
    >
      <div className="flex items-start justify-between gap-3 border-b border-black/[0.05] pb-3">
        <div className="text-right">
          <p className="text-xs font-bold text-[#1F8F6A]">{snapshot.category}</p>
          <h3 className="mt-1 text-lg font-extrabold leading-tight tracking-[-0.03em] text-[#111318] md:text-xl">
            {snapshot.title}
          </h3>
        </div>
        <span className="shrink-0 rounded-full bg-[#E8F5EF] px-2.5 py-1 text-[0.65rem] font-bold text-[#1F8F6A]">
          השוואה
        </span>
      </div>

      <div className="mt-4 flex items-center gap-2">
        <ProductColumn
          product={snapshot.left}
          strengths={snapshot.leftStrengths}
          side="left"
        />
        <span
          className="shrink-0 text-xs font-extrabold text-[#7A817C]"
          aria-hidden
        >
          מול
        </span>
        <ProductColumn
          product={snapshot.right}
          strengths={snapshot.rightStrengths}
          side="right"
        />
      </div>

      <div className="mt-4 rounded-lg border-r-[3px] border-[#1F8F6A] bg-[#F7F7F2]/80 px-3 py-2.5">
        <p className="text-[0.65rem] font-bold text-[#1F8F6A]">פער מרכזי</p>
        <p className="mt-1 text-sm font-medium leading-relaxed text-[#111318]">
          {snapshot.tradeoff}
        </p>
      </div>

      <p className="mt-3 flex items-center justify-end gap-1 text-xs font-bold text-[#1F8F6A] opacity-80 transition-opacity group-hover:opacity-100">
        לפרטים
        <ChevronLeft className="size-3.5" aria-hidden />
      </p>
    </Link>
  );
}
