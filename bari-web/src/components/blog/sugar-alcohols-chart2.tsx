"use client";

import Image from "next/image";
import { useState } from "react";

import { chart2 } from "@/lib/blog/sugar-alcohols-article-content";

type Bar = (typeof chart2.groupA.bars)[number] | (typeof chart2.groupB.bars)[number];

function ProductCard({ bar }: { bar: Bar }) {
  const [imgError, setImgError] = useState(false);

  return (
    <li className="rounded-[1rem] border border-black/[0.07] bg-[#FFFFFF] overflow-hidden">
      {/* Image area */}
      {!imgError && bar.imageUrl ? (
        <div className="relative h-32 w-full bg-[#F7F7F2]">
          <Image
            src={bar.imageUrl}
            alt={bar.name}
            fill
            className="object-contain p-3"
            onError={() => setImgError(true)}
            sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
          />
        </div>
      ) : (
        <div className="flex h-32 w-full items-center justify-center bg-[#F7F7F2]">
          <span className="text-[0.65rem] text-[#7A817C]">תמונה לא זמינה</span>
        </div>
      )}

      {/* Card body */}
      <div className="px-4 py-4 text-right">
        <p className="text-xs font-bold leading-snug text-[#111318]">{bar.displayName}</p>

        {/* Sugar label */}
        <p className="mt-2 text-[0.65rem] font-bold uppercase tracking-[0.1em] text-[#7A817C]">
          {bar.sugarLabel}
        </p>

        {/* Score + grade */}
        <div className="mt-2 flex items-center justify-end gap-2">
          <span className="rounded-[0.4rem] bg-[#F7F7F2] px-2 py-0.5 text-[0.65rem] font-bold tracking-[0.05em] text-[#111318]">
            {bar.scoreLabel}
          </span>
        </div>

        {/* Verdict line */}
        <p className="mt-3 text-[0.7rem] leading-relaxed text-[#4E5663]">{bar.line}</p>
      </div>
    </li>
  );
}

export function SugarAlcoholsChart2() {
  return (
    <section id="chart2" className="space-y-6">
      <header className="text-right">
        <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#1F8F6A]/85">
          מהמדף · שישה חטיפים
        </p>
        <h2 className="mt-1 text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
          {chart2.title}
        </h2>
        <p className="mt-2 text-sm leading-relaxed text-[#4E5663] md:text-base">
          {chart2.subtitle}
        </p>
      </header>

      {/* Group A */}
      <div className="rounded-[1.2rem] border border-black/[0.07] bg-[#FFF8F8] px-5 py-5 md:px-6 md:py-6">
        <p className="mb-4 text-right text-sm font-extrabold text-[#111318]">
          {chart2.groupA.heading}
        </p>
        <ul className="grid gap-4 sm:grid-cols-3">
          {chart2.groupA.bars.map((bar) => (
            <ProductCard key={bar.id} bar={bar} />
          ))}
        </ul>
      </div>

      {/* Group B */}
      <div className="rounded-[1.2rem] border border-black/[0.07] bg-[#F0FAF6] px-5 py-5 md:px-6 md:py-6">
        <p className="mb-4 text-right text-sm font-extrabold text-[#111318]">
          {chart2.groupB.heading}
        </p>
        <ul className="grid gap-4 sm:grid-cols-3">
          {chart2.groupB.bars.map((bar) => (
            <ProductCard key={bar.id} bar={bar} />
          ))}
        </ul>
      </div>

      <p className="rounded-[0.75rem] border border-amber-200/60 bg-amber-50/60 px-4 py-3 text-right text-xs leading-relaxed text-[#7A6A00]">
        <span className="font-bold">שימו לב · </span>
        {chart2.caveat}
      </p>
    </section>
  );
}
