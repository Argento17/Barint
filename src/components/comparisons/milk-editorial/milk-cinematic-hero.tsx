"use client";

import Link from "next/link";
import { motion, useReducedMotion } from "framer-motion";
import { ArrowRight } from "lucide-react";

import { MilkOrbitVisual } from "@/components/shared/milk-orbit-visual";
import { HomeContainer } from "@/components/home/section-frame";
import { milkEditorialHero } from "@/lib/comparisons/milk-editorial-content";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

export function MilkCinematicHero() {
  const reduceMotion = useReducedMotion();

  return (
    <header
      className={cn(
        "relative overflow-hidden bg-[#FFFFFF] text-[#111318]",
        siteHeaderOffsetClass,
        "max-h-[70vh]"
      )}
    >
      <div
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_70%_45%_at_50%_30%,rgba(31,143,106,0.04),transparent_70%)]"
        aria-hidden
      />

      <HomeContainer className="flex max-h-[70vh] flex-col pt-3 pb-5 md:pt-4 md:pb-6">
        <Link
          href="/hashvaot"
          className="mb-2 inline-flex w-fit shrink-0 items-center gap-2 text-sm font-semibold text-[#4E5663] hover:text-[#111318]"
        >
          <ArrowRight className="size-4" aria-hidden />
          חזרה להשוואות
        </Link>

        <div className="grid min-h-0 flex-1 items-center gap-4 md:grid-cols-2 md:gap-8 lg:gap-10">
          <div className="order-2 flex flex-col justify-center text-right md:order-none">
            <motion.p
              className="text-sm font-bold text-[#1F8F6A]"
              initial={reduceMotion ? false : { opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              {milkEditorialHero.eyebrow}
            </motion.p>
            <motion.h1
              className="mt-2 text-balance text-3xl font-extrabold leading-[1.12] tracking-[-0.05em] md:text-4xl lg:text-[2.75rem]"
              initial={reduceMotion ? false : { opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.06 }}
            >
              {milkEditorialHero.title}
            </motion.h1>
            <motion.p
              className="mt-2 max-w-xl text-pretty text-base leading-relaxed text-[#4E5663] md:text-lg"
              initial={reduceMotion ? false : { opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.1 }}
            >
              {milkEditorialHero.subtitle}
            </motion.p>
            <motion.p
              className="mt-2 text-sm text-[#7A817C]"
              initial={reduceMotion ? false : { opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.14 }}
            >
              {milkEditorialHero.meta}
            </motion.p>
            <motion.p
              className="mt-3 text-sm font-semibold text-[#1F8F6A]"
              initial={reduceMotion ? false : { opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.18 }}
            >
              <Link href="/blog/milk-analysis" className="hover:underline">
                קראו את הניתוח העיתונאי בבלוג
              </Link>
            </motion.p>
          </div>

          <div className="order-1 flex min-h-0 items-center justify-center md:order-none">
            <MilkOrbitVisual
              caption="אותו מדף — סיפורים שונים"
              className="h-[clamp(9rem,20vh,11.5rem)] md:h-[clamp(10rem,24vh,13rem)]"
            />
          </div>
        </div>
      </HomeContainer>

      <div
        className="pointer-events-none absolute inset-x-0 bottom-0 z-10 h-8 bg-gradient-to-t from-[#F7F7F2] to-transparent"
        aria-hidden
      />
    </header>
  );
}
