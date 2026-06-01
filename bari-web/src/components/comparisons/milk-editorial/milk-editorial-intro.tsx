"use client";

import { motion, useReducedMotion } from "framer-motion";

import { HomeContainer } from "@/components/home/section-frame";
import { milkEditorialIntroParagraphs } from "@/lib/comparisons/milk-editorial-content";

function IntroParagraph({ text, index }: { text: string; index: number }) {
  const reduceMotion = useReducedMotion();

  return (
    <motion.p
      className="text-pretty text-[1.125rem] leading-[1.85] tracking-[-0.01em] text-[#3A413D] md:text-[1.2rem] md:leading-[1.9]"
      initial={reduceMotion ? false : { opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-10%" }}
      transition={{ duration: 0.65, delay: Math.min(index * 0.06, 0.3), ease: [0.22, 1, 0.36, 1] }}
    >
      {text}
    </motion.p>
  );
}

export function MilkEditorialIntro() {
  return (
    <section className="relative border-b border-black/[0.06] bg-[#F7F7F2] py-20 md:py-28">
      <div
        className="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-l from-transparent via-[#1F8F6A]/20 to-transparent"
        aria-hidden
      />
      <HomeContainer>
        <div className="mx-auto max-w-3xl space-y-8 text-right md:space-y-10">
          <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.28em] text-[#1F8F6A]/80">
            דוח עיתונאי
          </p>
          {milkEditorialIntroParagraphs.map((paragraph, index) => (
            <IntroParagraph key={index} text={paragraph} index={index} />
          ))}
        </div>
      </HomeContainer>
    </section>
  );
}
