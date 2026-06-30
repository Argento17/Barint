export function HeroProductStage() {
  return (
    <div className="relative w-full">
      {/* Outer shell ? large rounded card, gradient bg, soft shadow */}
      <div
        className="relative overflow-hidden rounded-[38px] border border-black/[0.06] bg-gradient-to-b from-[#FAFAF7] to-[#F0F2EC] shadow-[0_32px_80px_-24px_rgba(17,19,24,0.18)]"
        style={{ minHeight: "520px", display: "flex", alignItems: "center", justifyContent: "center" }}
      >
        {/* Green glow blob top-right (::before equivalent) */}
        <div
          className="pointer-events-none absolute right-0 top-0 h-72 w-72 rounded-full bg-[#2FAE82] opacity-[0.12] blur-[64px]"
          aria-hidden="true"
        />
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src="/home/hero-product-stage.png"
          alt="הדמיית ניתוח מוצרי מזון"
          aria-label="הדמיית ניתוח מוצרי מזון"
          className="relative z-10 h-auto w-full object-contain"
          style={{ maxHeight: "520px" }}
        />
      </div>
    </div>
  );
}
