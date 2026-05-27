"use client";

import Link from "next/link";
import { motion, useReducedMotion } from "framer-motion";
import { ChevronLeft } from "lucide-react";

import { BreadShelfProductImage } from "@/components/bread/bread-shelf-product-image";
import {
  BREAD_REPORT_STATS,
  breadComparisonPairs,
  breadHeroProducts,
} from "@/lib/comparisons/bread-page-data";
import { cn } from "@/lib/utils";

type Props = {
  href: string;
  description: string;
};

export function FeaturedBreadIntelligenceCardLite({ href, description }: Props) {
  const reduceMotion = useReducedMotion();

  return (
    <Link
      href={href}
      className={cn(
        "group relative block overflow-hidden rounded-[1.35rem] border border-[#1A1D24]/[0.08]",
        "bg-[linear-gradient(135deg,#FDFDF8_0%,#F4F6F3_42%,#EEF5F1_100%)]",
        "shadow-[0_32px_100px_-60px_rgba(17,19,24,0.35)] ring-1 ring-[#FFFFFF]/80",
        "transition-[transform,box-shadow,border-color] duration-500 ease-out",
        "hover:-translate-y-1 hover:border-[#1F8F6A]/30",
        "hover:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      )}
    >
      <div
        className="pointer-events-none absolute inset-0 opacity-[0.12]"
        style={{
          backgroundImage:
            "linear-gradient(rgba(17,19,24,0.06) 1px, transparent 1px), linear-gradient(90deg, rgba(17,19,24,0.06) 1px, transparent 1px)",
          backgroundSize: "24px 24px",
        }}
        aria-hidden
      />

      <div className="relative z-[1] flex flex-col md:grid md:grid-cols-[minmax(0,2fr)_minmax(0,0.95fr)] md:items-stretch">
        <div className="order-2 flex flex-col justify-center px-6 pb-10 pt-8 sm:px-8 md:order-none lg:px-11 lg:py-11">
          <div className="flex flex-wrap items-center gap-x-3 gap-y-2">
            <span className="rounded-md border border-[#1F8F6A]/14 bg-[#1F8F6A]/[0.06] px-2 py-0.5 text-[0.58rem] font-extrabold tracking-wide text-[#1F8F6A]">
              דוח חדש
            </span>
            <span className="text-[0.62rem] font-bold uppercase tracking-[0.22em] text-[#8A928A]">
              Bari Intel
            </span>
            <span className="h-px w-5 bg-[#1F8F6A]/15" aria-hidden />
            <span className="text-[0.65rem] font-semibold tracking-wide text-[#4E5663]">
              לחם · פיתה · קרקרים
            </span>
          </div>

          <h3 className="mt-5 text-balance text-2xl font-extrabold leading-[1.12] tracking-[-0.045em] text-[#12151A] sm:text-[1.75rem] lg:text-[2rem] lg:tracking-[-0.05em]">
            מה באמת יש בלחם שלכם?
          </h3>

          <p className="mt-3 max-w-2xl text-pretty text-sm leading-[1.7] text-[#4E5663] sm:text-[0.95rem] lg:mt-4">
            {description}
          </p>

          <div className="mt-5 flex flex-wrap gap-x-3 gap-y-1.5 border-t border-black/[0.05] pt-5 text-[0.62rem] font-medium tabular-nums leading-relaxed text-[#8A918B]">
            <span>
              <strong className="font-bold text-[#5C645E]">{BREAD_REPORT_STATS.scanned}</strong> מוצרים
              שנסרקו
            </span>
            <span className="text-[#D5DAD6]" aria-hidden>
              ·
            </span>
            <span>
              <strong className="font-bold text-[#5C645E]">{BREAD_REPORT_STATS.sufficient}</strong> עם
              נתונים מספיקים
            </span>
            <span className="text-[#D5DAD6]" aria-hidden>
              ·
            </span>
            <span>
              <strong className="font-bold text-[#5C645E]">{breadComparisonPairs.length}</strong> זוגות
              השוואה
            </span>
          </div>

          <span className="mt-7 inline-flex items-center gap-2 rounded-2xl border border-[#1F8F6A]/38 bg-[#1F8F6A] px-6 py-3.5 text-sm font-bold text-[#FAFAFA] shadow-[0_14px_40px_-16px_rgba(31,143,106,0.58)]">
            פתיחת דוח ההשוואה
            <ChevronLeft className="size-[1.125rem] transition-transform duration-300 group-hover:-translate-x-0.5" />
          </span>
        </div>

        <div className="relative isolate order-1 min-h-[280px] border-b border-black/[0.055] px-7 pb-5 pt-5 md:order-none md:border-b-0 md:border-s md:border-black/[0.06] lg:min-h-[340px] lg:px-8 lg:pb-6">
          <div className="rounded-[1.65rem] border border-black/[0.06] bg-[#FFFFFF]/85 p-5">
            <div className="flex items-end justify-between gap-2 overflow-x-auto pb-2">
              {breadHeroProducts.map((product, index) => (
                <motion.div
                  key={product.id}
                  animate={reduceMotion ? undefined : { y: [0, -4, 0] }}
                  transition={{ repeat: Infinity, duration: 6 + index * 0.4, ease: "easeInOut" }}
                  className="min-w-[4.5rem] shrink-0"
                >
                  <BreadShelfProductImage product={product} size="lg" className="mx-auto" />
                </motion.div>
              ))}
            </div>
            <div className="mt-3 h-2 rounded-full bg-[#D7D2C7]/50" aria-hidden />
          </div>
        </div>
      </div>
    </Link>
  );
}
