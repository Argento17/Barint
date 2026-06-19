"use client";

// TASK-179T — Glass Box W2 additive panel component.
//
// Disclosure/transparency surface only. No score field, no score movement.
// DEC-006 constraints (all binding):
//   - No alarm icons for any tier (no ⚠, !, 🔴, skull).
//   - No E-numbers as the primary visible label (E-number in parentheses only).
//   - No attribution of manufacturer intent ("הסתיר", "ניסה", "הוסיף בכוונה").
//   - No Gen 0 patterns (no dimension bars, no score attribution, no card grid).
//   - No "safe"/"unsafe" binary labels.
//
// Hebrew strings in expansion_he come from TASK-179U Content sign-off.
// Until 179U is complete, draft strings from additive_prototype_set_v1.md are used.

import {
  useCallback,
  useEffect,
  useId,
  useRef,
  useState,
} from "react";

import { fireEvent } from "@/lib/analytics";
import type { AdditiveEntry, AdditiveTier } from "@/lib/view-models";

// ─── Tier chip configuration ─────────────────────────────────────────────────
// Frozen per spec (w2_engagement_gate_spec_v1.md §5.5, TASK-179T).
// Do not adjust without Design co-sign.

interface TierVisual {
  label: string;
  bg: string;
  color: string;
  /** Dashed border for disclosure-gap (spec §5.5 "visually empty"). */
  dashed?: boolean;
}

const TIER_VISUALS: Record<AdditiveTier, TierVisual> = {
  // Labels frozen per spec §5.5 (w2_engagement_gate_spec_v1.md). RT-1 fix.
  functional: {
    label: "תפקיד טכנולוגי",
    bg: "#E8F5E9",
    color: "#1B5E20",
  },
  "likely-neutral": {
    label: "ניטרלי בדרך כלל",
    bg: "#F5F5F5",
    color: "#424242",
  },
  "dose-dependent": {
    label: "תלוי במינון",
    bg: "#FFF3E0",
    color: "#E65100",
  },
  contested: {
    label: "קיים ויכוח מדעי",
    bg: "#FFF8E1",
    color: "#F57F17",
  },
  "disclosure-gap": {
    label: "לא פורט",
    bg: "#F3E5F5",
    color: "#4A148C",
    dashed: true,
  },
  unclassified: {
    label: "לא מסווג",
    bg: "#FAFAFA",
    color: "#9E9E9E",
  },
};

// Tier severity order for display priority (§5.1: contested first, then dose-dependent).
const TIER_SEVERITY: Record<AdditiveTier, number> = {
  contested: 0,
  "disclosure-gap": 1,
  "dose-dependent": 2,
  "likely-neutral": 3,
  functional: 4,
  unclassified: 5,
};

// Max additive rows shown before "הצג עוד" overflow link (spec §5.1).
const MAX_VISIBLE_ROWS = 3;

// ─── TierChip ────────────────────────────────────────────────────────────────
// 24px height, 8px h-padding, 11px font, border-radius 4px (spec §5.5).
// Rectangular — NOT the circular score chip. Must not be confused with grade chips.

// Polish 1 (TASK-181Q): TierChip font size 11px → 12px, height 24px → 26px.
// Improves Hebrew legibility at 375px. H-padding (8px) unchanged.
function TierChip({ tier }: { tier: AdditiveTier }) {
  const visual = TIER_VISUALS[tier] ?? TIER_VISUALS.unclassified;
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        height: "26px",
        paddingLeft: "8px",
        paddingRight: "8px",
        borderRadius: "4px",
        fontSize: "12px",
        fontWeight: 600,
        lineHeight: 1,
        whiteSpace: "nowrap",
        flexShrink: 0,
        backgroundColor: visual.bg,
        color: visual.color,
        border: visual.dashed
          ? "1px dashed rgba(0,0,0,0.18)"
          : "1px solid rgba(0,0,0,0.06)",
      }}
    >
      {visual.label}
    </span>
  );
}

// ─── Explanation truncation helper ───────────────────────────────────────────
// Copy doc (w2_additive_copy_v1.md) uses ";" as a natural clause break:
// first clause = "what it is", second clause = safety/controversy context.
// Prefer cutting at the semicolon so the preview always shows a complete thought.
// Hard fallback: last word boundary near maxChars, with "…" suffix.

function truncate(text: string, maxChars: number): string {
  if (text.length <= maxChars) return text;
  const semiIdx = text.indexOf(";");
  if (semiIdx > 0 && semiIdx < maxChars) return text.slice(0, semiIdx + 1);
  const slice = text.slice(0, maxChars);
  const lastSpace = slice.lastIndexOf(" ");
  const cut = lastSpace > 0 ? slice.slice(0, lastSpace) : slice;
  return cut.trimEnd() + "…";
}

// ─── AdditiveRow ─────────────────────────────────────────────────────────────

function AdditiveRow({
  entry,
  onTierExpand,
  fullExplanation = false,
}: {
  entry: AdditiveEntry;
  onTierExpand?: (tier: AdditiveTier) => void;
  /** When true, render explanation_he in full (dropdown sub-panel). */
  fullExplanation?: boolean;
}) {
  const detailsRef = useRef<HTMLDetailsElement>(null);

  const handleToggle = useCallback(() => {
    if (detailsRef.current?.open) {
      onTierExpand?.(entry.tier);
    }
  }, [entry.tier, onTierExpand]);

  // RT-3 crash guard: explanation_he may be absent at runtime before TASK-179U
  // joins the field from w2_additive_copy_v1.md (TypeScript says required but
  // the data path can be missing). Fall back to empty string defensively.
  const explanationText = entry.explanation_he ?? "";
  const displayedExplanation = fullExplanation
    ? explanationText
    : truncate(explanationText, 120);

  return (
    <div
      style={{
        minHeight: "64px",
        padding: "10px 0",
        borderBottom: "1px solid rgba(17,19,24,0.05)",
      }}
    >
      {/* Line 1: tier chip + Hebrew name (E-number secondary) */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "8px",
          flexWrap: "wrap",
        }}
      >
        <TierChip tier={entry.tier} />
        <span
          style={{
            fontSize: "14px",
            fontWeight: 600,
            color: "#2F3531",
            lineHeight: 1.3,
          }}
        >
          {entry.name_he}
        </span>
        <span
          style={{
            fontSize: "12px",
            color: "#9A9FA6",
            lineHeight: 1.3,
            direction: "ltr",
          }}
        >
          ({entry.e_number})
        </span>
      </div>

      {/* Line 2: explanation — complete first clause (up to ";"), 120-char hard limit */}
      <p
        style={{
          margin: "4px 0 0",
          fontSize: "13px",
          lineHeight: 1.45,
          color: "#6E756F",
        }}
      >
        {displayedExplanation}
      </p>

      {/* "עוד" expand sub-row — function_he shown on expand */}
      <details
        ref={detailsRef}
        onToggle={handleToggle}
        style={{ marginTop: "4px" }}
      >
        <summary
          style={{
            // Min touch target 44x44px (spec §5.3): negative margin trick preserves layout.
            display: "inline-flex",
            alignItems: "center",
            minHeight: "44px",
            minWidth: "44px",
            cursor: "pointer",
            fontSize: "12px",
            fontWeight: 600,
            color: "#5E8B6F",
            listStyle: "none",
            userSelect: "none",
            marginTop: "-10px",
            paddingTop: "10px",
            paddingBottom: "10px",
          }}
        >
          עוד
        </summary>
        <p
          style={{
            margin: "0 0 4px",
            fontSize: "13px",
            lineHeight: 1.5,
            color: "#4E5663",
          }}
        >
          {entry.function_he}
        </p>
      </details>
    </div>
  );
}

// ─── Public props ─────────────────────────────────────────────────────────────

export interface AdditivePanelProps {
  /** D4 additive tier entries. Empty array or undefined → empty state rendered. */
  additives: AdditiveEntry[];
  /** Category ID for analytics context (anonymous — no user ID). */
  category?: string;
  /** Product shelf position ID for analytics context (anonymous shelf position). */
  productId?: string;
}

// ─── AdditivePanel ────────────────────────────────────────────────────────────
// Collapsed on load. Expands inline (no modal, no route change).
// Mobile-first, 375px primary viewport. No horizontal scroll.
// Gen 1 patterns only — no Gen 0.

export function AdditivePanel({
  additives,
  category = "unknown",
  productId = "unknown",
}: AdditivePanelProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [showAll, setShowAll] = useState(false);
  const panelId = useId();

  // Impression: fires once per mount when the entry point is visible for ≥ 2 seconds.
  const impressionFiredRef = useRef(false);
  const entryPointRef = useRef<HTMLDivElement>(null);

  // Time-open: records when the panel opened so close event can report time_open_ms.
  const openTimeRef = useRef<number | null>(null);

  // Sort by tier severity (contested first) — spec §5.1.
  const sorted = [...additives].sort(
    (a, b) => (TIER_SEVERITY[a.tier] ?? 99) - (TIER_SEVERITY[b.tier] ?? 99)
  );
  const hasOverflow = sorted.length > MAX_VISIBLE_ROWS;
  const visible = showAll ? sorted : sorted.slice(0, MAX_VISIBLE_ROWS);

  // ── Event 6: additive_panel_impression (spec §3.1) ──
  // Fires once per page session when the entry point is in viewport for ≥ 2 seconds.
  useEffect(() => {
    const el = entryPointRef.current;
    if (!el || impressionFiredRef.current) return;

    let timer: ReturnType<typeof setTimeout> | null = null;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !impressionFiredRef.current) {
          timer = setTimeout(() => {
            if (!impressionFiredRef.current) {
              impressionFiredRef.current = true;
              fireEvent("additive_panel_impression", { category, product_id: productId });
            }
          }, 2000);
        } else {
          if (timer) { clearTimeout(timer); timer = null; }
        }
      },
      { threshold: 0.5 }
    );

    observer.observe(el);
    return () => {
      observer.disconnect();
      if (timer) clearTimeout(timer);
    };
  }, [category, productId]);

  // ── Event 5: scroll_past_additive_panel (spec §3.1) ──
  // Fires when the entry point leaves the viewport scrolling down while panel is closed.
  useEffect(() => {
    const el = entryPointRef.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting && entry.boundingClientRect.top < 0 && !isOpen) {
          fireEvent("scroll_past_additive_panel", { category, product_id: productId });
        }
      },
      { threshold: 0 }
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, [category, productId, isOpen]);

  // ── Event 1: additive_panel_open (spec §3.1) ──
  const handleOpen = useCallback(() => {
    openTimeRef.current = Date.now();
    setIsOpen(true);
    fireEvent("additive_panel_open", { category, product_id: productId });
  }, [category, productId]);

  // ── Event 2: additive_panel_close (spec §3.1) — includes time_open_ms ──
  const handleClose = useCallback(() => {
    const timeOpen = openTimeRef.current != null ? Date.now() - openTimeRef.current : 0;
    openTimeRef.current = null;
    setIsOpen(false);
    fireEvent("additive_panel_close", {
      category,
      product_id: productId,
      time_open_ms: timeOpen,
    });
  }, [category, productId]);

  // ── Event 3: tier_card_expand (spec §3.1) — fires when "עוד" opens ──
  const handleTierExpand = useCallback(
    (tier: AdditiveTier) => {
      fireEvent("tier_card_expand", { category, product_id: productId, tier });
    },
    [category, productId]
  );

  // ── Entry point row ──────────────────────────────────────────────────────────
  // Spec §5.2: collapsed on load, single tap-target row, right-pointing chevron.
  // 44px min height (mobile tap target spec §5.3).
  // Subtle top border + bg-surface-secondary tint (same as nutrition table divider).
  //
  // RT-3 (spec §5.6): when additives.length === 0 the empty state is a static
  // one-line paragraph — NOT behind a button. No expand/collapse. No panel.
  //
  // RT-2 (spec §5.2): when additives.length > 0 the entry point shows a TierChip
  // for the highest severity tier present before the count text, so shoppers see
  // the worst-case tier at a glance without opening the panel.

  const count = additives.length;

  // Highest severity tier for the collapsed entry point chip (RT-2).
  // sorted is already ordered by TIER_SEVERITY (lowest index = highest severity).
  const highestSeverityTier: AdditiveTier | null =
    sorted.length > 0 ? sorted[0].tier : null;

  // RT-3: empty state renders as a plain static line — not an expandable panel.
  if (count === 0) {
    return (
      <div
        ref={entryPointRef}
        dir="rtl"
        style={{
          borderTop: "1px solid rgba(17,19,24,0.06)",
          backgroundColor: "#F9F9F9",
          padding: "12px 16px",
        }}
      >
        {/* spec §5.6: one calm line, no chip, no icon, no checkmark — state the fact plainly */}
        <p
          style={{
            margin: 0,
            fontSize: "13px",
            lineHeight: 1.5,
            color: "#5E6560",
          }}
        >
          לא זוהו תוספי מזון שכיחים — המוצר מבוסס על רכיבים מזוהים בלבד.
        </p>
      </div>
    );
  }

  return (
    <div
      ref={entryPointRef}
      dir="rtl"
      style={{
        borderTop: "1px solid rgba(17,19,24,0.06)",
        backgroundColor: "#F9F9F9",
      }}
    >
      {!isOpen ? (
        // ── Collapsed state ────────────────────────────────────────────────────
        // RT-2: chip for highest severity tier + count text (spec §5.2).
        <button
          type="button"
          aria-expanded={false}
          aria-controls={panelId}
          onClick={handleOpen}
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            width: "100%",
            minHeight: "44px",
            padding: "0 16px",
            background: "transparent",
            border: "none",
            cursor: "pointer",
            textAlign: "right",
            gap: "8px",
          }}
        >
          {/* Left group: tier chip + label text */}
          <span
            style={{
              display: "flex",
              alignItems: "center",
              gap: "8px",
              flex: 1,
              minWidth: 0,
            }}
          >
            {highestSeverityTier !== null && (
              <TierChip tier={highestSeverityTier} />
            )}
            {/* Polish 2 (TASK-181Q): fontWeight 600 → 500 on the count+action label.
                Restores hierarchy: TierChip (600) = signal, label (500) = affordance. */}
            <span
              style={{
                fontSize: "13px",
                fontWeight: 500,
                color: "#3C443F",
              }}
            >
              {`${count} תוספים זוהו — הצג פירוט`}
            </span>
          </span>
          {/* Right-pointing chevron — signals expandability */}
          <span
            aria-hidden
            style={{
              display: "inline-block",
              color: "#B5BBB6",
              fontSize: "16px",
              lineHeight: 1,
              flexShrink: 0,
              transform: "scaleX(-1)", // rtl: chevron points LEFT visually = forward direction
            }}
          >
            ‹
          </span>
        </button>
      ) : (
        // ── Expanded state ─────────────────────────────────────────────────────
        <div id={panelId}>
          {/* Expanded header row (button that collapses) */}
          <button
            type="button"
            aria-expanded={true}
            aria-controls={panelId}
            onClick={handleClose}
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              width: "100%",
              minHeight: "44px",
              padding: "0 16px",
              background: "transparent",
              border: "none",
              borderBottom: "1px solid rgba(17,19,24,0.06)",
              cursor: "pointer",
              textAlign: "right",
            }}
          >
            <span
              style={{
                fontSize: "13px",
                fontWeight: 600,
                color: "#3C443F",
              }}
            >
              {`${count} תוספים זוהו`}
            </span>
            <span
              style={{
                fontSize: "12px",
                color: "#9A9FA6",
                fontWeight: 500,
              }}
            >
              סגור
            </span>
          </button>

          {/* Expanded panel body */}
          <div
            style={{
              padding: "0 16px",
              overflowY: "auto",
              // Cap panel height so long lists don't push page content off screen.
              // Users scroll within the panel, not the whole page, for deep lists.
              maxHeight: "480px",
            }}
          >
            {/* count > 0 guaranteed here (empty state returns early above — RT-3) */}
            <>
              {visible.map((entry) => (
                <AdditiveRow
                  key={entry.e_number}
                  entry={entry}
                  onTierExpand={handleTierExpand}
                />
              ))}

              {hasOverflow && !showAll ? (
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    setShowAll(true);
                  }}
                  style={{
                    display: "block",
                    minHeight: "44px",
                    padding: "10px 0",
                    fontSize: "13px",
                    fontWeight: 600,
                    color: "#5E8B6F",
                    background: "transparent",
                    border: "none",
                    cursor: "pointer",
                    width: "100%",
                    textAlign: "right",
                  }}
                >
                  {`הצג עוד ${sorted.length - MAX_VISIBLE_ROWS} תוספים`}
                </button>
              ) : null}
            </>
          </div>
        </div>
      )}
    </div>
  );
}

// ─── NewAdditivePanel ─────────────────────────────────────────────────────────
// TASK-346: spec §3.5 sub-dropdown — used by the redesigned expansion-section.
//
// Has-additives state: amber-tinted icon + count pill + expandable list.
// Clean state: green-tinted icon + "ללא" pill + non-clickable static header.
//
// Independent open state; default closed. Same grid-rows technique as parent expansion.
// Polish: R-08 border-radius 10px tile; R-11 opacity fade on reveal.
// Reduced-motion: transitions disabled under prefers-reduced-motion: reduce.

interface NewAdditivePanelProps {
  additives: { name: string; function: string }[] | AdditiveEntry[];
  category?: string;
  productId?: string;
}

function isAdditiveEntry(
  entry: { name: string; function: string } | AdditiveEntry
): entry is AdditiveEntry {
  return "tier" in entry && "e_number" in entry;
}

export function NewAdditivePanel({
  additives,
}: NewAdditivePanelProps) {
  const [open, setOpen] = useState(false);
  const panelId = useId();
  const clean = additives.length === 0;

  const richEntries = additives.filter(isAdditiveEntry);
  const hasRichEntries = richEntries.length === additives.length && richEntries.length > 0;
  const sortedRichEntries = hasRichEntries
    ? [...richEntries].sort(
        (a, b) => (TIER_SEVERITY[a.tier] ?? 99) - (TIER_SEVERITY[b.tier] ?? 99)
      )
    : [];

  // Legacy simple shape fallback: { name, function } only.
  const simpleItems = hasRichEntries
    ? []
    : additives.map((a) => {
        if ("name" in a && "function" in a) {
          return {
            name: (a as { name: string; function: string }).name,
            fn: (a as { name: string; function: string }).function,
          };
        }
        const ae = a as AdditiveEntry;
        return { name: ae.name_he, fn: ae.function_he };
      });

  return (
    <div
      style={{
        border: "1px solid var(--hairline-soft)",
        borderRadius: "var(--radius-xl)",
        overflow: "hidden",
        background: "var(--surface)",
      }}
    >
      {/* Header: static (clean) or button (has additives) */}
      {clean ? (
        /* Clean state — non-interactive, no button role (spec §3.5, §6) */
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "11px",
            padding: "13px 15px",
          }}
          aria-label="אין תוספי מזון"
        >
          {/* Icon tile — green — R-08: border-radius 10px, icon 17px */}
          <span
            style={{
              width: "30px",
              height: "30px",
              // R-08: calc(var(--radius-md) + 2px) = 10px
              borderRadius: "calc(var(--radius-md) + 2px)",
              display: "grid",
              placeItems: "center",
              flexShrink: 0,
              background: "#E8F5EF",
              color: "var(--bari-green-deep)",
            }}
          >
            {/* Checkmark SVG — 17px per R-08 */}
            <svg width="17" height="17" viewBox="0 0 16 16" aria-hidden>
              <path
                d="M4 8.3l2.4 2.4L12 5.2"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.7"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </span>

          <span style={{ flex: 1, minWidth: 0 }}>
            <span
              style={{
                display: "block",
                fontFamily: "var(--font-heading)",
                fontWeight: 800,
                fontSize: "13px",
                letterSpacing: "-0.01em",
                color: "var(--fg1)",
              }}
            >
              תוספי מזון
            </span>
            <span
              style={{
                display: "block",
                fontSize: "11px",
                color: "var(--fg3)",
                marginTop: "2px",
              }}
            >
              לא זוהו תוספים — רכיבים מזוהים בלבד
            </span>
          </span>

          {/* Count pill "ללא" — green tint */}
          <span
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: "11px",
              fontWeight: 700,
              padding: "3px 9px",
              borderRadius: "999px",
              letterSpacing: "0.04em",
              background: "#E8F5EF",
              color: "var(--bari-green-deep)",
              flexShrink: 0,
            }}
          >
            ללא
          </span>
        </div>
      ) : (
        /* Has-additives state — expandable button */
        <>
          <button
            type="button"
            aria-expanded={open}
            aria-controls={panelId}
            onClick={() => setOpen((o) => !o)}
            style={{
              width: "100%",
              display: "flex",
              alignItems: "center",
              gap: "11px",
              padding: "13px 15px",
              background: "transparent",
              border: "none",
              cursor: "pointer",
              fontFamily: "inherit",
              textAlign: "inherit",
              transition: "background var(--dur) var(--ease-out-soft)",
            }}
            className="hover:bg-[#FBFBF9]"
          >
            {/* Icon tile — amber — R-08: border-radius 10px, icon 17px */}
            <span
              style={{
                width: "30px",
                height: "30px",
                borderRadius: "calc(var(--radius-md) + 2px)",
                display: "grid",
                placeItems: "center",
                flexShrink: 0,
                background: "#F4F1EA",
                color: "#8F6600",
              }}
            >
              {/* Dots SVG — 17px per R-08 */}
              <svg width="17" height="17" viewBox="0 0 16 16" aria-hidden>
                <circle cx="8" cy="8" r="2" fill="none" stroke="currentColor" strokeWidth="1.4" />
                <circle cx="3" cy="8" r="1.3" fill="currentColor" />
                <circle cx="13" cy="8" r="1.3" fill="currentColor" />
              </svg>
            </span>

            <span style={{ flex: 1, minWidth: 0 }}>
              <span
                style={{
                  display: "block",
                  fontFamily: "var(--font-heading)",
                  fontWeight: 800,
                  fontSize: "13px",
                  letterSpacing: "-0.01em",
                  color: "var(--fg1)",
                }}
              >
                תוספי מזון
              </span>
              <span
                style={{
                  display: "block",
                  fontSize: "11px",
                  color: "var(--fg3)",
                  marginTop: "2px",
                }}
              >
                לחצו לפירוט התוספים ותפקידם
              </span>
            </span>

            {/* Count pill — amber tint */}
            <span
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: "11px",
                fontWeight: 700,
                padding: "3px 9px",
                borderRadius: "999px",
                letterSpacing: "0.04em",
                background: "#F4ECD8",
                color: "#8F6600",
                flexShrink: 0,
              }}
            >
              {hasRichEntries ? sortedRichEntries.length : simpleItems.length}
            </span>

            {/* Chevron — rotates 180° when open (spec §4) */}
            <svg
              width="15"
              height="15"
              viewBox="0 0 16 16"
              aria-hidden
              style={{
                flexShrink: 0,
                color: "var(--fg3)",
                transition: "transform var(--dur-fast) var(--ease-out-soft)",
                transform: open ? "rotate(180deg)" : "rotate(0deg)",
              }}
              className="motion-reduce:transition-none"
            >
              <path
                d="M4 6l4 4 4-4"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </button>

          {/* Collapsible body — grid-rows 0fr→1fr (spec §4) — R-11: opacity fade */}
          <div
            id={panelId}
            style={{
              display: "grid",
              gridTemplateRows: open ? "1fr" : "0fr",
              transition: "grid-template-rows var(--dur-fast) var(--ease-out-soft)",
            }}
            className="motion-reduce:transition-none"
          >
            <div style={{ overflow: "hidden" }}>
              {/* R-11: opacity fade on the inner content */}
              <div
                style={{
                  padding: "2px 15px 14px",
                  opacity: open ? 1 : 0,
                  transition: "opacity var(--dur-fast) var(--ease-out-soft)",
                }}
                className="motion-reduce:transition-none"
              >
                {hasRichEntries
                  ? sortedRichEntries.map((entry) => (
                      <AdditiveRow
                        key={entry.e_number}
                        entry={entry}
                        fullExplanation
                      />
                    ))
                  : simpleItems.map((item, i) => (
                      <div
                        key={i}
                        style={{
                          display: "grid",
                          gridTemplateColumns: "1fr auto",
                          alignItems: "center",
                          gap: "12px",
                          padding: "10px 0",
                          borderTop: "1px solid var(--hairline-faint)",
                        }}
                      >
                        <span
                          style={{
                            fontSize: "13px",
                            color: "var(--fg1)",
                            fontWeight: 600,
                          }}
                        >
                          {item.name}
                        </span>
                        <span
                          style={{
                            fontFamily: "var(--font-mono)",
                            fontSize: "10.5px",
                            letterSpacing: "0.04em",
                            color: "var(--fg3)",
                            background: "#F6F6F1",
                            padding: "3px 9px",
                            borderRadius: "999px",
                            whiteSpace: "nowrap",
                          }}
                        >
                          {item.fn}
                        </span>
                      </div>
                    ))}
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
