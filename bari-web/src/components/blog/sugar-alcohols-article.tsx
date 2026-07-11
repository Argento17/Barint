"use client";

import Link from "next/link";
import { ArrowRight, ChevronLeft } from "lucide-react";
import { motion, useReducedMotion } from "framer-motion";

import { HomeContainer } from "@/components/home/section-frame";
import { SugarAlcoholsChart1 } from "@/components/blog/sugar-alcohols-chart1";
import { SugarAlcoholsChart2 } from "@/components/blog/sugar-alcohols-chart2";
import { SugarAlcoholsEfsaCard } from "@/components/blog/sugar-alcohols-efsa-card";
import { SugarAlcoholsFrontVsBack } from "@/components/blog/sugar-alcohols-front-vs-back";
import { MobileActionBar } from "@/components/shared/mobile-action-bar";
import {
  hero,
  mechanism,
  catchSection,
  takeaway,
  PROTEIN_BARS_HREF,
  HASHVAOT_HREF,
} from "@/lib/blog/sugar-alcohols-article-content";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

// ---------------------------------------------------------------------------
// Hero
// ---------------------------------------------------------------------------
function ArticleHero() {
  return (
    <header className="relative overflow-hidden border-b border-black/6 bg-[#FFFFFF]">
      <HomeContainer className="flex flex-col py-8 md:py-12">
        <Link
          href="/blog"
          className="mb-2 inline-flex shrink-0 items-center gap-2 text-sm font-semibold text-[#4E5663] hover:text-[#111318]"
        >
          <ArrowRight className="size-4" aria-hidden />
          חזרה לבלוג
        </Link>

        <div className="flex max-w-3xl flex-col justify-center text-right">
          <p className="text-xs font-bold uppercase tracking-[0.24em] text-[#167A58]">
            {hero.eyebrow}
          </p>
          <h1 className="mt-3 text-balance text-3xl font-extrabold leading-[1.1] tracking-tighter text-[#111318] md:text-4xl lg:text-5xl">
            {hero.title}
          </h1>
          <p className="mt-3 max-w-2xl text-pretty text-base leading-relaxed text-[#4E5663] md:text-lg">
            {hero.standfirst}
          </p>
          <p className="mt-2 text-sm text-[#7A817C]">{hero.meta}</p>

          <div className="mt-6 flex gap-8 border-t border-black/6 pt-5">
            <div>
              <p className="text-2xl font-extrabold tracking-tight text-[#C0392B]">
                {hero.stat.value}
              </p>
              <p className="mt-0.5 text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                {hero.stat.label}
              </p>
            </div>
          </div>
        </div>
      </HomeContainer>
    </header>
  );
}

// ---------------------------------------------------------------------------
// Body paragraph with fade-in
// ---------------------------------------------------------------------------
function BodyParagraph({ text, index = 0 }: { text: string; index?: number }) {
  const reduceMotion = useReducedMotion();
  return (
    <motion.p
      initial={reduceMotion ? false : { opacity: 0, y: 8 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-30px" }}
      transition={{ duration: 0.45, delay: index * 0.04 }}
      className="text-base leading-[1.85] text-[#111318] md:text-lg"
    >
      {text}
    </motion.p>
  );
}

// ---------------------------------------------------------------------------
// Mechanism section
// ---------------------------------------------------------------------------
function MechanismSection() {
  return (
    <section id="mechanism" className="border-t border-black/6 bg-[#FFFFFF] py-14 md:py-20">
      <HomeContainer>
        <div className="mx-auto max-w-3xl">
          <header className="mb-8 text-right">
            <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#7A9450]/85">
              הסבר המנגנון
            </p>
            <h2 className="mt-2 text-3xl font-extrabold tracking-tighter text-[#111318] md:text-4xl">
              {mechanism.heading}
            </h2>
          </header>
          <div className="space-y-5">
            {mechanism.body.map((p, i) => (
              <BodyParagraph key={i} text={p} index={i} />
            ))}
          </div>
        </div>
      </HomeContainer>
    </section>
  );
}

// ---------------------------------------------------------------------------
// Catch section ("where it gets more complex")
// ---------------------------------------------------------------------------
function CatchSectionBlock() {
  return (
    <section id="catch" className="border-t border-black/6 bg-[#F7F7F2] py-14 md:py-20">
      <HomeContainer>
        <div className="mx-auto max-w-3xl">
          <header className="mb-8 text-right">
            <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#7A9450]/85">
              מה שכדאי לדעת
            </p>
            <h2 className="mt-2 text-3xl font-extrabold tracking-tighter text-[#111318] md:text-4xl">
              {catchSection.heading}
            </h2>
          </header>
          <div className="space-y-5">
            {catchSection.body.map((p, i) => (
              <BodyParagraph key={i} text={p} index={i} />
            ))}
          </div>
        </div>
      </HomeContainer>
    </section>
  );
}

// ---------------------------------------------------------------------------
// Takeaway section
// ---------------------------------------------------------------------------
function TakeawaySection() {
  return (
    <section id="takeaway" className="border-t border-black/6 bg-[#FFFFFF] py-14 md:py-20">
      <HomeContainer>
        <div className="mx-auto max-w-3xl">
          <header className="mb-8 text-right">
            <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#7A9450]/85">
              לסיכום
            </p>
            <h2 className="mt-2 text-3xl font-extrabold tracking-tighter text-[#111318] md:text-4xl">
              {takeaway.heading}
            </h2>
          </header>
          <div className="space-y-5">
            {takeaway.body.map((p, i) => (
              <BodyParagraph key={i} text={p} index={i} />
            ))}
          </div>

          {/* CTA */}
          <div className="mt-10 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-end">
            <Link
              href={PROTEIN_BARS_HREF}
              className="inline-flex items-center justify-center gap-2 rounded-full bg-[#167A58] px-6 py-3 text-sm font-bold text-[#F7F7F2] shadow-md shadow-[#1F8F6A]/25 transition-[transform,box-shadow] duration-300 hover:-translate-y-0.5"
            >
              לניתוח חטיפי החלבון
              <ChevronLeft className="size-4" aria-hidden />
            </Link>
            <Link
              href={HASHVAOT_HREF}
              className="inline-flex items-center justify-center gap-2 rounded-full border border-[#1F8F6A]/30 bg-transparent px-6 py-3 text-sm font-bold text-[#167A58] transition-colors duration-200 hover:bg-[#1F8F6A]/8"
            >
              כל קטגוריות בארי
              <ChevronLeft className="size-4" aria-hidden />
            </Link>
          </div>
        </div>
      </HomeContainer>
    </section>
  );
}

// ---------------------------------------------------------------------------
// Root orchestrator
// ---------------------------------------------------------------------------
export function SugarAlcoholsArticle() {
  return (
    <div className={cn("bg-[#F7F7F2] text-[#111318]", siteHeaderOffsetClass)}>
      <MobileActionBar />
      <article>
        {/* 1. Hero */}
        <ArticleHero />

        {/* 2. Mechanism */}
        <MechanismSection />

        {/* 3. Catch */}
        <CatchSectionBlock />

        {/* 3b. EFSA credibility card — corroborates the lower-glucose finding */}
        <div className="border-t border-black/6 bg-[#FFFFFF] py-14 md:py-20">
          <HomeContainer>
            <div className="mx-auto max-w-3xl">
              <SugarAlcoholsEfsaCard />
            </div>
          </HomeContainer>
        </div>

        {/* 4. Chart 1 — polyol family */}
        <div className="bg-[#F7F7F2] py-14 md:py-20">
          <HomeContainer>
            <div className="mx-auto max-w-3xl">
              <SugarAlcoholsChart1 />
            </div>
          </HomeContainer>
        </div>

        {/* 5. Chart 2 — two routes to a low number */}
        <div className="border-t border-black/6 bg-[#FFFFFF] py-14 md:py-20">
          <HomeContainer>
            <div className="mx-auto max-w-4xl">
              <SugarAlcoholsChart2 />
            </div>
          </HomeContainer>
        </div>

        {/* 5b. Front vs. back — three real bars (CLIMAX, S-47..S-51) */}
        <SugarAlcoholsFrontVsBack />

        {/* 6. Takeaway */}
        <TakeawaySection />

        {/* Footer nav */}
        <HomeContainer className="pb-14">
          <footer className="mx-auto flex max-w-3xl flex-wrap items-center justify-between gap-4 border-t border-black/6 pt-8">
            <Link
              href={HASHVAOT_HREF}
              className="inline-flex items-center gap-2 text-sm font-semibold text-[#167A58] hover:underline"
            >
              כל ניתוחי המדף
              <ChevronLeft className="size-4" aria-hidden />
            </Link>
            <Link
              href="/blog"
              className="text-sm font-semibold text-[#4E5663] hover:text-[#111318]"
            >
              חזרה לבלוג
            </Link>
          </footer>
        </HomeContainer>
      </article>
    </div>
  );
}
