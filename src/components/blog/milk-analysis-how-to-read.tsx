"use client";

import { motion, useReducedMotion } from "framer-motion";

import { milkAnalysisArticle } from "@/lib/blog/milk-analysis-content";

export function MilkAnalysisHowToRead() {
  const { howToRead } = milkAnalysisArticle;
  const reduceMotion = useReducedMotion();

  return (
    <section id="how-to-read" className="scroll-mt-24">
      <h2 className="text-xl font-extrabold tracking-[-0.03em] text-[#111318] md:text-2xl">
        {howToRead.title}
      </h2>
      <p className="mt-3 max-w-2xl text-base leading-relaxed text-[#111318] font-medium">
        {howToRead.lead}
      </p>

      <div className="mt-6 overflow-hidden rounded-[1.15rem] border border-black/[0.07] bg-[#FFFFFF]">
        <table className="w-full text-right text-sm">
          <tbody>
            {howToRead.rows.map((row, i) => (
              <motion.tr
                key={row.label}
                initial={reduceMotion ? false : { opacity: 0 }}
                whileInView={{ opacity: 1 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.05 }}
                className="border-b border-black/[0.05] last:border-0"
              >
                <th className="w-[28%] bg-[#F7F7F2]/80 px-4 py-4 align-top text-xs font-extrabold text-[#1F8F6A] md:px-5">
                  {row.label}
                </th>
                <td className="px-4 py-4 leading-relaxed text-[#4E5663] md:px-5">
                  {row.text}
                </td>
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
