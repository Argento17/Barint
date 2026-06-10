"use client";

import { ExternalLink } from "lucide-react";
import { motion, useReducedMotion } from "framer-motion";

import { HomeContainer } from "@/components/home/section-frame";

type Citation = {
  readonly id: string;
  readonly short: string;
  readonly full: string;
  readonly url: string;
  readonly claim: string;
};

type ScienceData = {
  readonly title: string;
  readonly subtitle: string;
  readonly paragraphs: readonly string[];
  readonly citations: readonly Citation[];
};

/**
 * ScienceSection — full science narrative with inline citations and a formal
 * references list. Extracted from olive-oil-article.tsx to shared/ for TASK-200.
 * Props: any content file's `science` object that matches the ScienceData shape.
 */
export function ScienceSection({ science, eyebrow }: { science: ScienceData; eyebrow?: string }) {
  const reduceMotion = useReducedMotion();
  return (
    <section id="science" className="border-t border-black/6 bg-[#FFFFFF] py-14 md:py-20">
      <HomeContainer>
        <div className="mx-auto max-w-3xl">
          <header className="mb-8 text-right">
            <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#7A9450]/85">
              {eyebrow ?? "מדע הרקע"}
            </p>
            <h2 className="mt-2 text-3xl font-extrabold tracking-tighter text-[#111318] md:text-4xl">
              {science.title}
            </h2>
            <p className="mt-3 text-base leading-relaxed text-[#4E5663]">
              {science.subtitle}
            </p>
          </header>

          <div className="space-y-5">
            {science.paragraphs.map((p, i) => (
              <motion.p
                key={i}
                initial={reduceMotion ? false : { opacity: 0, y: 8 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-30px" }}
                transition={{ duration: 0.45, delay: i * 0.04 }}
                className="text-base leading-[1.85] text-[#111318] md:text-lg"
              >
                {p}
              </motion.p>
            ))}
          </div>

          {/* Formal citations */}
          <div className="mt-10 rounded-[1rem] border border-black/[0.06] bg-[#F7F7F2] px-5 py-5">
            <p className="mb-3 text-[0.65rem] font-bold uppercase tracking-[0.18em] text-[#7A817C]">
              מקורות
            </p>
            <ol className="space-y-3">
              {science.citations.map((c) => (
                <li key={c.id} className="flex gap-3 text-right">
                  <span className="mt-0.5 shrink-0 font-mono text-[0.65rem] font-bold text-[#7A9450]">
                    [{c.id}]
                  </span>
                  <div>
                    <p className="text-xs font-semibold leading-relaxed text-[#111318]">
                      {c.short}
                    </p>
                    <p className="mt-0.5 text-[0.65rem] leading-relaxed text-[#7A817C]">
                      {c.claim}
                    </p>
                    <a
                      href={c.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="mt-1 inline-flex items-center gap-1 text-[0.65rem] font-semibold text-[#1F8F6A] hover:underline"
                    >
                      קישור למקור
                      <ExternalLink className="size-3" aria-hidden />
                    </a>
                  </div>
                </li>
              ))}
            </ol>
          </div>
        </div>
      </HomeContainer>
    </section>
  );
}
