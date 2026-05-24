"use client";

import Link from "next/link";
import { motion, useReducedMotion } from "framer-motion";
import { ChevronLeft } from "lucide-react";

import { milkAnalysisArticle } from "@/lib/blog/milk-analysis-content";

export function MilkAnalysisRecent() {
  const { recentAnalyses } = milkAnalysisArticle;
  const reduceMotion = useReducedMotion();

  return (
    <section id="recent-analyses" className="scroll-mt-24 border-t border-black/[0.06] pt-14 md:pt-16">
      <header className="mb-8">
        <h2 className="text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
          {recentAnalyses.title}
        </h2>
        <p className="mt-3 max-w-2xl text-base leading-relaxed text-[#4E5663]">
          {recentAnalyses.subtitle}
        </p>
      </header>

      <div className="grid gap-4 sm:grid-cols-2">
        {recentAnalyses.items.map((item, i) => (
          <motion.article
            key={item.slug}
            initial={reduceMotion ? false : { opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.04 }}
            className="flex flex-col rounded-[1.1rem] border border-black/[0.07] bg-[#FFFFFF] p-5"
          >
            <p className="text-[0.65rem] font-bold text-[#1F8F6A]">{item.category}</p>
            <h3 className="mt-2 text-base font-extrabold leading-snug text-[#111318]">
              {item.title}
            </h3>
            <p className="mt-2 flex-1 text-sm leading-relaxed text-[#4E5663]">
              {item.description}
            </p>
            <p className="mt-3 text-xs font-semibold text-[#7A817C]">{item.readTime}</p>
            {item.comingSoon ? (
              <span className="mt-3 inline-flex text-sm font-bold text-[#7A817C]">בקרוב</span>
            ) : (
              <Link
                href={item.href}
                className="mt-3 inline-flex items-center gap-1 text-sm font-bold text-[#1F8F6A] hover:underline"
              >
                {item.cta}
                <ChevronLeft className="size-4" aria-hidden />
              </Link>
            )}
          </motion.article>
        ))}
      </div>

      <Link
        href="/blog"
        className="mt-8 inline-flex items-center gap-2 text-sm font-bold text-[#1F8F6A] hover:underline"
      >
        לכל הניתוחים בבלוג
        <ChevronLeft className="size-4" aria-hidden />
      </Link>
    </section>
  );
}
