"use client";

import { motion, useReducedMotion } from "framer-motion";

export function MilkAnalysisInsightBlock({
  quote,
  index = 0,
}: {
  quote: string;
  index?: number;
}) {
  const reduceMotion = useReducedMotion();

  return (
    <motion.blockquote
      initial={reduceMotion ? false : { opacity: 0, x: 12 }}
      whileInView={{ opacity: 1, x: 0 }}
      viewport={{ once: true, margin: "-40px" }}
      transition={{ duration: 0.5, delay: index * 0.05 }}
      className="relative border-r-4 border-[#1F8F6A] bg-[#FFFFFF] px-6 py-5 md:px-8"
    >
      <p className="text-lg font-semibold leading-snug tracking-[-0.02em] text-[#111318] md:text-xl">
        {quote}
      </p>
    </motion.blockquote>
  );
}
