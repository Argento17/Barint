export function HeroProductStage() {
  return (
    <div className="relative w-full">
      {/*
       * De-boxed hero: no hard card border, no contrasting gradient fill.
       * The PNG has a light/white baked background — mix-blend-multiply blends
       * white areas into the page cream (#F7F7F2) so it reads as one scene.
       * object-contain preserves the FULL composition (score ring, radar, all packs)
       * with no crop; the de-boxed container lets any letterbox gaps fall on the page
       * cream so there's no visible rectangle.
       *
       * ASSET NOTE: The current PNG has a baked white background. mix-blend-multiply
       * handles it well on the cream page but cannot remove white halos perfectly at
       * every pixel. A transparent-background (.png with alpha) asset would give full
       * integration with zero visible rectangle. Flag to Design/Owner as an asset task.
       */}
      <div
        className="relative w-full overflow-hidden"
        style={{ minHeight: "480px" }}
      >
        {/* Soft green ambient glow — retained for depth */}
        <div
          className="pointer-events-none absolute right-0 top-0 h-72 w-72 rounded-full bg-[#2FAE82] opacity-[0.09] blur-[80px]"
          aria-hidden="true"
        />
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src="/home/hero-product-stage.png"
          alt="הדמיית ניתוח מוצרי מזון"
          aria-label="הדמיית ניתוח מוצרי מזון"
          className="relative z-10 h-full w-full object-contain"
          style={{
            minHeight: "480px",
            mixBlendMode: "multiply",
          }}
        />
      </div>
    </div>
  );
}
