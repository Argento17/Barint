// Glycemic-index bar chart — the guide's single highest-value visual (build brief item 1).
// Server-rendered (no hooks/state needed — the geometry is pure CSS).
// Plain divs, not a chart library: this is an RTL page, and the brief flags a documented
// past failure where a gauge rendered left-to-right on this RTL site while every geometry
// assertion passed. The fix is to control the physical CSS directly rather than trust
// `dir` to flip a library's internals.
//
// Geometry, explicitly: each bar is `position: absolute; right: 0; width: <pct>%` inside a
// relatively-positioned track. A block box with an explicit width and zero margins anchors
// to its containing block's PHYSICAL left edge regardless of `dir` — `dir` only changes
// flex/inline main-axis direction and text flow, not a plain block box's physical offset.
// Anchoring with the physical `right: 0` property (not a logical `inset-inline-end`, and
// not relying on flex) is what actually guarantees the bar starts at the right and grows
// left as the value increases, matching reading order on this Hebrew page. Verify by eye:
// the longest bar (sugar, 65) should visually start flush with the right edge of the track
// and reach furthest left; erythritol (0) should show no bar at all, just its number.
//
// The real data table remains in the DOM (sr-only) as the accessible/SEO fallback, per the
// brief. All copy — sweetener names, the GI numbers, the axis labels, the caption — is
// pulled from the signed-off data module; nothing here is invented text.

import type { SweetenerGlycemicRow } from "@/lib/guides/sweetener-guide-data";

const TRACK_HEIGHT = "1.75rem";

export function GlycemicBarChart({
  rows,
  columnNameLabel,
  columnGiLabel,
  caption,
}: {
  rows: SweetenerGlycemicRow[];
  /** Verbatim structuralStrings.giTable.columnName — reused as the chart's axis legend. */
  columnNameLabel: string;
  /** Verbatim structuralStrings.giTable.columnGi — reused as the chart's axis legend. */
  columnGiLabel: string;
  /** Verbatim structuralStrings.giTable.caption. */
  caption: string | null;
}) {
  const max = Math.max(...rows.map((r) => r.gi));

  return (
    <figure className="mt-4">
      <div className="rounded-lg border border-black/[0.08] bg-white px-4 py-4 sm:px-5">
        <div className="mb-3 flex items-center justify-between text-[10px] font-bold uppercase tracking-[0.14em] text-[#8A857A]">
          <span>{columnNameLabel}</span>
          <span>{columnGiLabel}</span>
        </div>
        <div className="space-y-3">
          {rows.map((row) => {
            const pct = max > 0 ? (row.gi / max) * 100 : 0;
            return (
              <div key={row.name} className="flex items-center gap-3">
                <span className="w-[4.5rem] shrink-0 text-[13px] font-semibold leading-tight text-[#111318] sm:w-20">
                  {row.name}
                </span>
                <div
                  className="relative min-w-0 flex-1 overflow-hidden rounded-full bg-[#F1F1EC]"
                  style={{ height: TRACK_HEIGHT }}
                  role="img"
                  aria-label={`${row.name}, ${columnGiLabel}: ${row.gi}`}
                >
                  {row.gi > 0 ? (
                    <div
                      className="absolute inset-y-0 rounded-full"
                      style={{
                        right: 0,
                        width: `${pct}%`,
                        background: "linear-gradient(155deg, #1E7A4F, #0F5C42)",
                      }}
                    />
                  ) : (
                    <div
                      aria-hidden="true"
                      className="absolute inset-y-0 my-auto size-[0.6rem] rounded-full bg-[#0F5C42]"
                      style={{ right: "0.3rem" }}
                    />
                  )}
                </div>
                <span className="w-7 shrink-0 text-left text-[13px] font-bold tabular-nums text-[#3E444A]">
                  {row.gi}
                </span>
              </div>
            );
          })}
        </div>
      </div>
      {caption ? (
        <figcaption className="mt-2 text-[11px] leading-[1.5] text-[#5E6560]">
          {caption}
        </figcaption>
      ) : null}

      {/* Accessible/SEO fallback — the real table, visually hidden. Not decorative: screen
          readers get proper <th scope> semantics the bar chart's aria-labels approximate
          but don't replace. */}
      <div className="sr-only">
        <table>
          <caption>{columnNameLabel}</caption>
          <thead>
            <tr>
              <th scope="col">{columnNameLabel}</th>
              <th scope="col">{columnGiLabel}</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.name}>
                <td>{row.name}</td>
                <td>{row.gi}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </figure>
  );
}
