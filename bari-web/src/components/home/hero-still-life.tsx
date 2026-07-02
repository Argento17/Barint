"use client";

import { useState } from "react";
import { CAROUSEL_PRODUCT_FALLBACK } from "@/lib/home/homepage-carousel-schema";
import { HERO_STAGE_PRODUCTS, HERO_STAGE_SCORE } from "@/lib/home/hero-still-life-products";
import type { StageProduct } from "@/lib/home/hero-still-life-products";
import { HeroDecorativeRadar } from "@/components/home/hero-decorative-radar";
import { HeroDecorativeScoreRing } from "@/components/home/hero-decorative-score-ring";

const DROP_SHADOW = "drop-shadow(0 12px 24px rgba(17,19,24,0.13))";

function StagePack({ product }: { product: StageProduct }) {
  const [loaded, setLoaded] = useState(false);
  const [errored, setErrored] = useState(false);
  const src = errored ? CAROUSEL_PRODUCT_FALLBACK : product.imageUrl;

  return (
    <div
      className="pointer-events-none absolute"
      style={{
        top: product.layout.top,
        left: product.layout.left,
        width: product.layout.width,
        zIndex: product.layout.zIndex,
        transform: "rotate(-4deg)",
        filter: DROP_SHADOW,
      }}
    >
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src={src}
        alt={product.imageAlt}
        className={`h-auto w-full object-contain mix-blend-multiply transition-opacity duration-500 ${
          loaded ? "opacity-100" : "opacity-0"
        }`}
        onLoad={() => setLoaded(true)}
        onError={() => {
          setErrored(true);
          setLoaded(true);
        }}
      />
    </div>
  );
}

export function HeroStillLife() {
  return (
    <div
      className="relative mx-auto w-full max-w-[30rem] sm:max-w-[32rem]"
      aria-hidden
    >
      {/* Main canvas -- one large rounded cream card */}
      <div className="relative overflow-hidden rounded-3xl border border-black/[0.06] bg-gradient-to-b from-[#FAFAF7] to-[#F2F2EC] shadow-[0_24px_60px_-20px_rgba(17,19,24,0.14)]">
        <div className="relative aspect-[4/5] min-h-[22rem] sm:min-h-[26rem]">

          {/* Soft oval platform */}
          <div
            className="absolute inset-x-[8%] bottom-[7%] h-[20%] rounded-[50%] bg-gradient-to-b from-[#E6EDE8]/70 to-[#DDE4DF]/40 blur-[3px]"
            style={{ zIndex: 0 }}
          />
          <div
            className="absolute inset-x-[13%] bottom-[9%] h-[15%] rounded-[50%] border border-[#1F8F6A]/8 bg-[radial-gradient(ellipse_at_center,rgba(255,255,255,0.82),rgba(247,247,242,0.1))]"
            style={{ zIndex: 0 }}
          />

          {/* Products -- consistent -4deg angle */}
          {HERO_STAGE_PRODUCTS.map((product) => (
            <StagePack key={product.id} product={product} />
          ))}

          {/* Score ring anchored near vitabix */}
          <div className="absolute" style={{ top: "8%", left: "62%", zIndex: 10 }}>
            <HeroDecorativeScoreRing
              score={HERO_STAGE_SCORE.score}
              grade={HERO_STAGE_SCORE.grade}
            />
          </div>

          {/* Radar card top-start corner */}
          <HeroDecorativeRadar className="absolute start-3 top-3 z-20 sm:start-4 sm:top-4" />

          {/* Ingredient quality pill */}
          <div className="absolute end-3 bottom-[26%] z-20 rounded-full border border-[#1F8F6A]/20 bg-white/92 px-3 py-1.5 text-[11px] font-bold text-[#167A58] shadow-[0_6px_20px_-8px_rgba(17,19,24,0.16)] backdrop-blur-sm">
            איכות רכיבים
          </div>

          {/* Minimal processing pill */}
          <div className="absolute start-3 bottom-[16%] z-20 rounded-full border border-[#1F8F6A]/20 bg-white/92 px-3 py-1.5 text-[11px] font-bold text-[#167A58] shadow-[0_6px_20px_-8px_rgba(17,19,24,0.16)] backdrop-blur-sm">
            עיבוד מינימלי
          </div>
        </div>
      </div>
    </div>
  );
}
