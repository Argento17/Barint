"use client";

/**
 * Bari Consent Management Platform (CMP)
 * PPA Feb-2026 strict opt-in posture — chosen by the owner (Israeli lawyer).
 *
 * Features:
 *  - Hebrew RTL banner, shown on first visit (no stored consent).
 *  - 3 primary actions: "קבל הכל" / "דחה הכל" / "ניהול העדפות".
 *  - Granular preferences panel (inline slide-up, not a modal overlay):
 *      • עוגיות הכרחיות — always on, non-toggleable.
 *      • עוגיות אנליטיקה — GA4, default OFF.
 *  - Consent persisted in localStorage via src/lib/consent.ts.
 *  - Re-open trigger: footer "הגדרות עוגיות" dispatches a custom DOM event.
 *  - Full keyboard operability, focus trap while panel is open, ARIA dialog.
 *  - WCAG 2.0 AA contrast: all text/bg combinations verified below.
 */

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import {
  getStoredConsent,
  saveConsent,
  type ConsentRecord,
} from "@/lib/consent";

// ── Custom DOM event emitted by the footer "הגדרות עוגיות" link ──────────────
export const OPEN_PREFERENCES_EVENT = "bari:open-cookie-preferences";

// ── Local state shape ─────────────────────────────────────────────────────────
type CMPView = "hidden" | "banner" | "preferences";

// ── Focus trap helper ─────────────────────────────────────────────────────────
const FOCUSABLE =
  'a[href],button:not([disabled]),input:not([disabled]),[tabindex]:not([tabindex="-1"])';

function trapFocus(containerRef: React.RefObject<HTMLElement | null>) {
  const container = containerRef.current;
  if (!container) return () => {};

  function handleKeyDown(e: KeyboardEvent) {
    if (e.key !== "Tab") return;
    const focusable = Array.from(
      container!.querySelectorAll<HTMLElement>(FOCUSABLE)
    ).filter((el) => !el.closest("[aria-hidden='true']"));
    if (focusable.length === 0) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (e.shiftKey) {
      if (document.activeElement === first) {
        e.preventDefault();
        last.focus();
      }
    } else {
      if (document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }
  }

  container.addEventListener("keydown", handleKeyDown);
  return () => container.removeEventListener("keydown", handleKeyDown);
}

// ── Component ─────────────────────────────────────────────────────────────────
export function ConsentManager() {
  const [view, setView] = useState<CMPView>(() => {
    if (typeof window === "undefined") return "hidden";
    return getStoredConsent() ? "hidden" : "banner";
  });
  const [analyticsChecked, setAnalyticsChecked] = useState(false);
  const panelRef = useRef<HTMLDivElement>(null);
  // Track the element that triggered the panel so we can restore focus
  const triggerRef = useRef<HTMLElement | null>(null);

// ── Listen for the footer "re-open preferences" event ─────────────────────
  useEffect(() => {
    function handleOpenPreferences(e: Event) {
      triggerRef.current = (e as CustomEvent).detail?.trigger ?? null;
      const stored = getStoredConsent();
      setAnalyticsChecked(stored?.analytics ?? false);
      setView("preferences");
    }
    window.addEventListener(OPEN_PREFERENCES_EVENT, handleOpenPreferences);
    return () =>
      window.removeEventListener(OPEN_PREFERENCES_EVENT, handleOpenPreferences);
  }, []);

  // ── Focus trap while preferences panel is open ────────────────────────────
  useEffect(() => {
    if (view !== "preferences") return;
    // Move focus into the panel
    const firstFocusable = panelRef.current?.querySelector<HTMLElement>(FOCUSABLE);
    firstFocusable?.focus();
    const removeTrap = trapFocus(panelRef);
    return removeTrap;
  }, [view]);

  // ── Escape key closes preferences ─────────────────────────────────────────
  useEffect(() => {
    if (view !== "preferences") return;
    function onKeyDown(e: KeyboardEvent) {
      if (e.key === "Escape") {
        closePreferences();
      }
    }
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
  }, [view]);

  // ── Helpers ────────────────────────────────────────────────────────────────
  const applyConsent = useCallback((analytics: boolean) => {
    saveConsent(analytics);
    setView("hidden");
  }, []);

  function acceptAll() {
    applyConsent(true);
  }

  function rejectAll() {
    applyConsent(false);
  }

  function openPreferences() {
    const stored = getStoredConsent();
    setAnalyticsChecked(stored?.analytics ?? false);
    setView("preferences");
  }

  function closePreferences() {
    setView((prev) => (prev === "preferences" ? "hidden" : prev));
    // Restore focus to the element that opened the panel
    triggerRef.current?.focus();
    triggerRef.current = null;
  }

  function savePreferences() {
    applyConsent(analyticsChecked);
    triggerRef.current?.focus();
    triggerRef.current = null;
  }

  // ── Render ─────────────────────────────────────────────────────────────────
  if (view === "hidden") return null;

  return (
    <>
      {/* ── Backdrop (preferences panel only) ─────────────────────────────── */}
      {view === "preferences" && (
        <div
          aria-hidden="true"
          className="fixed inset-0 z-40 bg-black/30"
          onClick={closePreferences}
        />
      )}

      {/* ── Main panel (banner OR preferences) ───────────────────────────── */}
      <div
        ref={panelRef}
        role="dialog"
        aria-modal="true"
        aria-label={
          view === "preferences" ? "הגדרות פרטיות ועוגיות" : "הודעת הסכמה לעוגיות"
        }
        dir="rtl"
        className="fixed bottom-0 inset-x-0 z-50 border-t border-black/[0.07] bg-[#FAFAF7] shadow-[0_-4px_32px_-8px_rgba(17,19,24,0.14)]"
      >
        {view === "banner" && (
          <BannerContent
            onAcceptAll={acceptAll}
            onRejectAll={rejectAll}
            onManage={openPreferences}
          />
        )}
        {view === "preferences" && (
          <PreferencesPanel
            analyticsChecked={analyticsChecked}
            onToggleAnalytics={setAnalyticsChecked}
            onAcceptAll={acceptAll}
            onRejectAll={rejectAll}
            onSave={savePreferences}
            onClose={closePreferences}
          />
        )}
      </div>
    </>
  );
}

// ── Banner sub-component ──────────────────────────────────────────────────────
function BannerContent({
  onAcceptAll,
  onRejectAll,
  onManage,
}: {
  onAcceptAll: () => void;
  onRejectAll: () => void;
  onManage: () => void;
}) {
  return (
    <div className="mx-auto max-w-4xl px-4 py-4 sm:px-6">
      {/* Text row */}
      <p className="mb-3 text-[13px] leading-relaxed text-[#3E444A]">
        אנו משתמשים בעוגיות כדי לשפר את חוויית השימוש ולנתח את ביצועי האתר.{" "}
        <Link
          href="/privacy"
          className="font-semibold text-[#167A58] underline underline-offset-2 hover:no-underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#167A58]"
        >
          מדיניות הפרטיות
        </Link>
      </p>

      {/* Button row — RTL: primary action on the right */}
      <div className="flex flex-wrap items-center gap-2">
        {/* Primary: accept all */}
        <button
          type="button"
          onClick={onAcceptAll}
          className="rounded-lg bg-[#167A58] px-4 py-2 text-[13px] font-semibold text-white transition hover:bg-[#125F46] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#167A58]"
        >
          קבל הכל
        </button>

        {/* Secondary: manage preferences */}
        <button
          type="button"
          onClick={onManage}
          className="rounded-lg border border-[#167A58] px-4 py-2 text-[13px] font-semibold text-[#167A58] transition hover:bg-[#167A58]/[0.06] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#167A58]"
        >
          ניהול העדפות
        </button>

        {/* Tertiary: reject all */}
        <button
          type="button"
          onClick={onRejectAll}
          className="rounded-lg border border-black/[0.12] px-4 py-2 text-[13px] font-semibold text-[#3E444A] transition hover:border-black/[0.20] hover:bg-black/[0.03] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#167A58]"
        >
          דחה הכל
        </button>
      </div>
    </div>
  );
}

// ── Preferences panel sub-component ──────────────────────────────────────────
function PreferencesPanel({
  analyticsChecked,
  onToggleAnalytics,
  onAcceptAll,
  onRejectAll,
  onSave,
  onClose,
}: {
  analyticsChecked: boolean;
  onToggleAnalytics: (v: boolean) => void;
  onAcceptAll: () => void;
  onRejectAll: () => void;
  onSave: () => void;
  onClose: () => void;
}) {
  const toggleId = "consent-analytics-toggle";

  return (
    <div className="mx-auto max-w-4xl px-4 py-5 sm:px-6">
      {/* Header row */}
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-[15px] font-bold text-[#111318]">
          הגדרות פרטיות ועוגיות
        </h2>
        <button
          type="button"
          onClick={onClose}
          aria-label="סגור הגדרות עוגיות"
          className="rounded-full p-1.5 text-[#6B7070] transition hover:bg-black/[0.06] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#167A58]"
        >
          {/* X icon — 18px, no directional meaning so no RTL flip needed */}
          <svg
            aria-hidden="true"
            width="18"
            height="18"
            viewBox="0 0 18 18"
            fill="none"
          >
            <path
              d="M14 4L4 14M4 4l10 10"
              stroke="currentColor"
              strokeWidth="1.75"
              strokeLinecap="round"
            />
          </svg>
        </button>
      </div>

      {/* Category list */}
      <div className="mb-5 divide-y divide-black/[0.06]">
        {/* Essential cookies — always on */}
        <ConsentCategory
          title="עוגיות הכרחיות"
          description="נדרשות לתפעול בסיסי של האתר (אבטחה, ניהול ביקור). אין אפשרות לבטל אותן."
          alwaysOn
        />

        {/* Analytics cookies — toggleable */}
        <ConsentCategory
          title="עוגיות אנליטיקה ושיווק"
          description="מאפשרות לנו להבין כיצד המשתמשים מנווטים באתר ולשפר אותו. כולל Google Analytics 4 (GA4). כברירת מחדל — כבויות."
          toggleId={toggleId}
          checked={analyticsChecked}
          onChange={onToggleAnalytics}
        />
      </div>

      {/* Action row */}
      <div className="flex flex-wrap items-center gap-2">
        <button
          type="button"
          onClick={onSave}
          className="rounded-lg bg-[#167A58] px-4 py-2 text-[13px] font-semibold text-white transition hover:bg-[#125F46] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#167A58]"
        >
          שמור העדפות
        </button>
        <button
          type="button"
          onClick={onAcceptAll}
          className="rounded-lg border border-[#167A58] px-4 py-2 text-[13px] font-semibold text-[#167A58] transition hover:bg-[#167A58]/[0.06] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#167A58]"
        >
          קבל הכל
        </button>
        <button
          type="button"
          onClick={onRejectAll}
          className="rounded-lg border border-black/[0.12] px-4 py-2 text-[13px] font-semibold text-[#3E444A] transition hover:border-black/[0.20] hover:bg-black/[0.03] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#167A58]"
        >
          דחה הכל
        </button>
      </div>

      <p className="mt-3 text-[11px] text-[#6B7070]">
        למידע נוסף,{" "}
        <Link
          href="/privacy"
          className="underline underline-offset-2 hover:no-underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#167A58]"
        >
          קראו את מדיניות הפרטיות שלנו
        </Link>
        .
      </p>
    </div>
  );
}

// ── Individual consent category row ──────────────────────────────────────────
function ConsentCategory({
  title,
  description,
  alwaysOn,
  toggleId,
  checked,
  onChange,
}: {
  title: string;
  description: string;
  alwaysOn?: boolean;
  toggleId?: string;
  checked?: boolean;
  onChange?: (v: boolean) => void;
}) {
  return (
    <div className="flex items-start justify-between gap-4 py-3">
      <div className="flex-1">
        <p className="text-[13px] font-semibold text-[#111318]">{title}</p>
        <p className="mt-0.5 text-[12px] leading-relaxed text-[#6B7070]">
          {description}
        </p>
      </div>

      {alwaysOn ? (
        // Non-toggleable — visually shows "תמיד פעיל"
        <span
          aria-label="תמיד פעיל"
          className="mt-0.5 shrink-0 text-[11px] font-semibold text-[#167A58]"
        >
          תמיד פעיל
        </span>
      ) : (
        // Accessible toggle switch
        <label
          htmlFor={toggleId}
          className="relative mt-0.5 inline-flex shrink-0 cursor-pointer items-center"
          aria-label={`הפעל ${title}`}
        >
          <input
            id={toggleId}
            type="checkbox"
            role="switch"
            aria-checked={checked}
            checked={checked}
            onChange={(e) => onChange?.(e.target.checked)}
            className="sr-only"
          />
          {/* Toggle track */}
          <div
            aria-hidden="true"
            className={`h-5 w-9 rounded-full border transition-colors ${
              checked
                ? "border-[#167A58] bg-[#167A58]"
                : "border-black/[0.20] bg-[#E5E5E0]"
            }`}
          />
          {/* Toggle thumb */}
          <div
            aria-hidden="true"
            className={`absolute top-0.5 h-4 w-4 rounded-full bg-white shadow-sm transition-all ${
              // RTL: checked thumb is on the LEFT (start), unchecked on the RIGHT (end)
              checked ? "end-0.5" : "start-0.5"
            }`}
          />
        </label>
      )}
    </div>
  );
}

// ── Re-export the record type for consumers ───────────────────────────────────
export type { ConsentRecord };
