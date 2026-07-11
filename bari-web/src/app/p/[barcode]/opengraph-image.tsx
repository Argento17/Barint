/**
 * Dynamic per-product OG image for /p/[barcode] (TASK-471).
 *
 * DEGRADED template (documented, not a silent shortcut): this build renders the
 * score + grade + barcode on the Bari brand template using Latin letters and
 * digits ONLY — no Hebrew glyphs.
 *
 * Why: `ImageResponse` (next/og / @vercel/og) does not shape/render Hebrew with
 * the system default font (Geist, Latin-only) — Hebrew text comes out as blank
 * tofu boxes, not readable glyphs. This repo ships no embeddable Hebrew font
 * file (checked: no .ttf/.otf/.woff under public/ or elsewhere in the repo;
 * the site's own Hebrew body text relies on the OS/browser system font stack,
 * which ImageResponse's isolated renderer cannot reach). Per the task spec:
 * "if reliable Hebrew rendering proves impractical in this build pass, DEGRADE
 * to a clean branded template ... rather than shipping broken glyphs."
 *
 * What IS shown: the Bari wordmark (Latin), the numeric score, the grade
 * letter (A–E — already Latin), and the barcode digits. No product name (it's
 * Hebrew) is rendered into the image; the product name still appears correctly
 * as plain Hebrew text in the page's <title>/<meta> tags and on the page itself
 * — only the generated PNG is Latin/numeric-only.
 *
 * DISPLAY ONLY: score/grade are read verbatim from the same BariProductVM the
 * page renders — this file never computes or rounds a score.
 */

import { ImageResponse } from "next/og";
import { getProductByBarcode } from "@/lib/inventory/loader";

export const alt = "Bari product score";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

const GRADE_COLORS: Record<string, { bg: string; text: string; accent: string }> = {
  A: { bg: "#E7F4EC", text: "#155C3C", accent: "#1F8F6A" },
  B: { bg: "#EEF3E3", text: "#4B5E2E", accent: "#7DA33B" },
  C: { bg: "#FBF3E3", text: "#7A5A16", accent: "#C49A4A" },
  D: { bg: "#FBEBE3", text: "#8A4A26", accent: "#C77F5A" },
  E: { bg: "#FCE9E7", text: "#8A2A20", accent: "#C1503D" },
};

export default async function Image({
  params,
}: {
  params: Promise<{ barcode: string }>;
}) {
  const { barcode } = await params;
  const entry = getProductByBarcode(barcode);

  const score = entry?.detail.score ?? null;
  const grade = entry?.detail.grade ?? null;
  const palette = grade ? GRADE_COLORS[grade] : null;

  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          background: "#F7F7F2",
          padding: "64px",
          fontFamily: "sans-serif",
        }}
      >
        {/* Brand mark */}
        <div style={{ display: "flex", alignItems: "center" }}>
          <span
            style={{
              fontSize: 40,
              fontWeight: 800,
              color: "#111318",
              letterSpacing: "-0.02em",
            }}
          >
            Bari
          </span>
        </div>

        {/* Score block */}
        <div style={{ display: "flex", alignItems: "center", gap: 40 }}>
          {score != null && grade != null && palette ? (
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                width: 240,
                height: 240,
                borderRadius: 32,
                background: palette.bg,
                border: `4px solid ${palette.accent}`,
              }}
            >
              <span
                style={{
                  fontSize: 96,
                  fontWeight: 800,
                  color: palette.text,
                  lineHeight: 1,
                }}
              >
                {Math.round(score)}
              </span>
              <span
                style={{
                  fontSize: 44,
                  fontWeight: 800,
                  color: palette.text,
                  marginTop: 8,
                }}
              >
                Grade {grade}
              </span>
            </div>
          ) : (
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                width: 240,
                height: 240,
                borderRadius: 32,
                background: "#EEEEEA",
                border: "4px solid #9A9FA6",
              }}
            >
              <span style={{ fontSize: 64, fontWeight: 800, color: "#6B7280" }}>
                —
              </span>
            </div>
          )}

          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            <span style={{ fontSize: 28, fontWeight: 600, color: "#4E5663" }}>
              Product barcode
            </span>
            <span
              style={{
                fontSize: 40,
                fontWeight: 700,
                color: "#111318",
                fontFamily: "monospace",
                letterSpacing: "0.04em",
              }}
            >
              {barcode}
            </span>
          </div>
        </div>

        {/* Footer */}
        <div style={{ display: "flex", fontSize: 24, color: "#5E6560" }}>
          bari.digital
        </div>
      </div>
    ),
    { ...size }
  );
}
