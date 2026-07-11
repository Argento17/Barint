// Bespoke gradient-tile section icons — white glyph on a green-gradient rounded tile,
// per the owner's documented icon preference (bari_icon_style_gradient_tile_preference):
// bespoke white-glyph-on-green-gradient tiles with subtle motion, never flat/line icons
// or emoji. Inline SVG, no external assets. Colors reuse existing tokens only:
// gradePalette.A accent (#1E7A4F) and the guide eyebrow green (#0F5C42) — no new palette.

import { ScrollReveal } from "@/components/guides/sweetener/scroll-reveal";
import type { SweetenerIconKey } from "@/lib/guides/sweetener-guide-visuals";

// Simple, topical, single-stroke-weight glyphs. Each reads clearly at 40px.
const GLYPHS: Record<SweetenerIconKey, React.ReactNode> = {
  // Opening: an open book — "what is a sweetener, what's really on the shelf".
  opening: (
    <path
      d="M20 14c-2.5-1.6-6-2-9-1.4v14c3-.6 6.5-.2 9 1.4 2.5-1.6 6-2 9-1.4v-14c-3-.6-6.5-.2-9 1.4Zm0 0v14"
      fill="none"
      stroke="white"
      strokeWidth={1.8}
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  ),
  // Polyols: a hexagon with an internal node — the shared chemical family.
  polyols: (
    <g fill="none" stroke="white" strokeWidth={1.7} strokeLinecap="round" strokeLinejoin="round">
      <path d="M20 10.5 27.5 15v10L20 29.5 12.5 25V15Z" />
      <circle cx="20" cy="20" r="2" fill="white" stroke="none" />
      <path d="M20 13.2V18M25.2 17.2 20.9 19.3M14.8 17.2l4.3 2.1M20 26.8V22M25.2 22.8l-4.3-2.1M14.8 22.8l4.3-2.1" />
    </g>
  ),
  // High-intensity: a bolt — sweetness intensity.
  "high-intensity": (
    <path
      d="M22 10 12.5 22h6l-1.5 8L27.5 18h-6.2Z"
      fill="white"
      stroke="white"
      strokeWidth={1.2}
      strokeLinejoin="round"
    />
  ),
  // Plant-derived: a leaf.
  "plant-derived": (
    <path
      d="M27 12c-8 0-15 6-15 15 9 0 15-7 15-15Z M12 27c3-6 8-10 15-11"
      fill="white"
      stroke="white"
      strokeWidth={1}
      strokeLinejoin="round"
      strokeLinecap="round"
    />
  ),
  // Erythritol headline: a heart with a small pulse tick — "the headline about the heart".
  "erythritol-headline": (
    <path
      d="M20 28.5 12.8 21.6c-2.4-2.3-2.4-5.9-.1-8.1 2.2-2.1 5.6-2 7.7.2l.6.6.6-.6c2.1-2.2 5.5-2.3 7.7-.2 2.3 2.2 2.3 5.8-.1 8.1L20 28.5Z M14.5 20h2.3l1.3-2.6 1.9 4.2 1.2-1.6h2.8"
      fill="none"
      stroke="white"
      strokeWidth={1.6}
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  ),
  // Not in products: a magnifying glass with a slash — names people expect, not found here.
  "not-in-products": (
    <g fill="none" stroke="white" strokeWidth={1.7} strokeLinecap="round" strokeLinejoin="round">
      <circle cx="18" cy="18" r="6" />
      <path d="M22.3 22.3 28 28" />
      <path d="M14.5 21.5l7-7" />
    </g>
  ),
  // Not yet known: a question mark.
  "not-yet-known": (
    <g fill="none" stroke="white" strokeWidth={1.9} strokeLinecap="round" strokeLinejoin="round">
      <path d="M16.8 16.2c.4-2.3 2.3-3.7 4.6-3.4 2.1.3 3.6 2 3.4 4-.2 1.8-1.5 2.6-2.8 3.4-1.1.7-1.8 1.3-1.9 2.7" />
      <circle cx="20" cy="27" r="0.9" fill="white" stroke="none" />
    </g>
  ),
};

export function SweetenerSectionIcon({
  icon,
  className,
}: {
  icon: SweetenerIconKey;
  className?: string;
}) {
  return (
    <ScrollReveal className={className}>
      <div
        aria-hidden="true"
        className="flex size-10 shrink-0 items-center justify-center rounded-xl shadow-[0_1px_2px_rgba(17,19,24,0.12)]"
        style={{
          background: `linear-gradient(155deg, #1E7A4F, #0F5C42)`,
        }}
      >
        <svg width="22" height="22" viewBox="0 0 40 40" role="presentation">
          {GLYPHS[icon]}
        </svg>
      </div>
    </ScrollReveal>
  );
}
