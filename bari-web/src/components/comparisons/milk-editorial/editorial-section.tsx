"use client";

import type { ReactNode } from "react";
import { motion, useReducedMotion } from "framer-motion";

import { HomeContainer } from "@/components/home/section-frame";
import { cn } from "@/lib/utils";

export function EditorialSection({
  id,
  eyebrow,
  title,
  description,
  children,
  tone = "light",
  fullWidth = false,
  className,
}: {
  id?: string;
  eyebrow?: string;
  title?: string;
  description?: string;
  children: ReactNode;
  tone?: "light" | "dark" | "canvas";
  fullWidth?: boolean;
  className?: string;
}) {
  const reduceMotion = useReducedMotion();
  const isDark = tone === "dark";

  const inner = (
    <>
      {(eyebrow || title || description) && (
        <header className="mb-8 max-w-2xl text-right md:mb-10">
          {eyebrow ? (
            <p
              className={cn(
                "font-mono text-[0.68rem] font-bold uppercase tracking-[0.28em]",
                isDark ? "text-[#1F8F6A]" : "text-[#1F8F6A]/85"
              )}
            >
              {eyebrow}
            </p>
          ) : null}
          {title ? (
            <h2
              className={cn(
                "mt-3 text-2xl font-extrabold tracking-[-0.04em] md:text-3xl",
                isDark ? "text-[#F7F7F2]" : "text-[#111318]"
              )}
            >
              {title}
            </h2>
          ) : null}
          {description ? (
            <p
              className={cn(
                "mt-3 text-base leading-relaxed md:text-lg",
                isDark ? "text-[#C8CDC9]" : "text-[#4E5663]"
              )}
            >
              {description}
            </p>
          ) : null}
        </header>
      )}
      {children}
    </>
  );

  const sectionClass = cn(
    "relative py-16 md:py-24",
    tone === "light" && "bg-[#F7F7F2] text-[#111318]",
    tone === "canvas" && "bg-[#FFFFFF] text-[#111318]",
    tone === "dark" && "bg-[#111318] text-[#F7F7F2]",
    className
  );

  return (
    <motion.section
      id={id}
      className={sectionClass}
      initial={reduceMotion ? false : { opacity: 0 }}
      whileInView={{ opacity: 1 }}
      viewport={{ once: true, margin: "-8%" }}
      transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
    >
      {fullWidth ? (
        <div className="px-5 sm:px-6">{inner}</div>
      ) : (
        <HomeContainer>{inner}</HomeContainer>
      )}
    </motion.section>
  );
}
