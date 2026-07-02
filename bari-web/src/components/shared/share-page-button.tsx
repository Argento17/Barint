"use client";

// Share-page feature (TASK-467).
//
// Native Web Share API where available (fires directly in the click handler —
// user-gesture requirement). Falls back to a quiet, monochrome popover for
// desktop Chrome < 128 and all Firefox (zero navigator.share support there).
//
// No brand colors, no icon-soup — one quiet labeled button matching the
// footer's text/hover palette (#4E5663 / #2FAE82). RTL throughout.
//
// Analytics: every share action fires a consent-gated GA4 `share` event via
// `fireEvent` (src/lib/analytics.ts) — never UTM params on the shared URL
// itself (copy-forward misattribution risk).

import { useCallback, useEffect, useId, useLayoutEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";

import { fireEvent } from "@/lib/analytics";
import { buildShareText, buildWhatsAppShareUrl } from "@/lib/social-links";
import { cn } from "@/lib/utils";

export interface SharePageButtonProps {
  title: string;
  /**
   * Optional short title for share payloads (native share sheet, WhatsApp,
   * Telegram, and the `buildShareText` prefix). Use when `title` is the full
   * editorial headline and too long for a share message — falls back to
   * `title` when omitted.
   */
  shareTitle?: string;
  /** Defaults to the current page URL (window.location, query/hash stripped). */
  url?: string;
  className?: string;
}

function currentCanonicalUrl(): string {
  if (typeof window === "undefined") return "";
  return `${window.location.origin}${window.location.pathname}`;
}

function telegramShareUrl(title: string, url: string): string {
  return `https://t.me/share/url?url=${encodeURIComponent(url)}&text=${encodeURIComponent(
    buildShareText(title)
  )}`;
}

function facebookShareUrl(url: string): string {
  return `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`;
}

const ICON_CLASS = "size-4 shrink-0";

function ShareGlyph() {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.75"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={ICON_CLASS}
      aria-hidden
    >
      <circle cx="18" cy="5" r="3" />
      <circle cx="6" cy="12" r="3" />
      <circle cx="18" cy="19" r="3" />
      <line x1="8.6" y1="10.5" x2="15.4" y2="6.5" />
      <line x1="8.6" y1="13.5" x2="15.4" y2="17.5" />
    </svg>
  );
}

function LinkGlyph() {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.75"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={ICON_CLASS}
      aria-hidden
    >
      <path d="M9.5 14.5 14.5 9.5" />
      <path d="M11 6.5 12.7 4.8a3.6 3.6 0 0 1 5 5L16 11.5" />
      <path d="M13 17.5 11.3 19.2a3.6 3.6 0 0 1-5-5L8 12.5" />
    </svg>
  );
}

function WhatsAppGlyph() {
  return (
    <svg viewBox="0 0 24 24" fill="currentColor" className={ICON_CLASS} aria-hidden>
      <path d="M17.5 14.4c-.3-.1-1.6-.8-1.8-.9-.2-.1-.4-.1-.6.1-.2.2-.7.9-.8 1-.2.2-.3.2-.5.1-.3-.1-1.2-.4-2.2-1.4-.8-.7-1.4-1.6-1.5-1.9-.2-.3 0-.5.1-.6.1-.1.3-.3.4-.5.1-.1.2-.3.3-.4.1-.2 0-.4 0-.5s-.6-1.5-.8-2c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.5.1-.7.3-.2.2-.9.9-.9 2.2s1 2.6 1.1 2.7c.1.2 1.9 3 4.7 4.1.7.3 1.2.4 1.6.6.7.2 1.3.2 1.7.1.5-.1 1.6-.7 1.9-1.3.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.6-.3z" />
      <path d="M12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.5 1.3 5L2 22l5.2-1.3c1.4.8 3.1 1.2 4.8 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2zm0 18.2c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3.1.8.8-3-.2-.3C4 14.9 3.6 13.5 3.6 12c0-4.6 3.8-8.4 8.4-8.4s8.4 3.8 8.4 8.4-3.8 8.2-8.4 8.2z" />
    </svg>
  );
}

function TelegramGlyph() {
  return (
    <svg viewBox="0 0 24 24" fill="currentColor" className={ICON_CLASS} aria-hidden>
      <path d="M21.5 4.5 3.2 11.6c-1.2.5-1.2 1.2-.2 1.5l4.7 1.5 1.8 5.6c.2.6.4.8.9.8.5 0 .7-.2 1-.5l2.3-2.2 4.8 3.5c.9.5 1.5.2 1.7-.8l3.1-14.5c.3-1.2-.5-1.7-1.8-1z" />
    </svg>
  );
}

function FacebookGlyph() {
  return (
    <svg viewBox="0 0 24 24" fill="currentColor" className={ICON_CLASS} aria-hidden>
      <path d="M13.5 21v-7.4h2.5l.4-2.9h-2.9V8.9c0-.8.2-1.4 1.4-1.4h1.6V4.9c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 3.9v2h-2.6v2.9h2.6V21h3.2z" />
    </svg>
  );
}

interface AnchorRect {
  /** Distance from viewport top to the anchor's bottom edge (px). */
  top: number;
  /** Distance from viewport right edge to the anchor's right edge (px) — RTL: menu/toast align to the button's end (right) edge. */
  right: number;
}

/** Minimum gap kept between a portaled menu/toast and either viewport edge (px). */
const VIEWPORT_EDGE_MARGIN = 8;

const buttonClass =
  "inline-flex items-center gap-2 rounded-full border border-black/[0.08] bg-transparent px-4 py-2 text-sm font-semibold text-[#4E5663] transition-colors duration-200 hover:text-[#2FAE82] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#167A58]";

const menuItemClass =
  "flex w-full items-center gap-2.5 rounded-lg px-3 py-2.5 text-right text-sm font-medium text-[#4E5663] transition-colors duration-150 hover:bg-black/[0.04] hover:text-[#111318] focus-visible:outline-2 focus-visible:outline-offset-[-2px] focus-visible:outline-[#167A58]";

/**
 * A single quiet share button. Native OS share sheet where supported; a
 * minimal RTL popover fallback otherwise (copy link → WhatsApp → Telegram →
 * Facebook).
 */
export function SharePageButton({ title, shareTitle, url, className }: SharePageButtonProps) {
  // RT-2 fix: share payloads (native sheet, WhatsApp, Telegram, buildShareText)
  // use the short shareTitle when the caller provides one — title itself can be
  // a full editorial headline unfit for a share message. Falls back to title.
  const effectiveTitle = shareTitle ?? title;
  const [menuOpen, setMenuOpen] = useState(false);
  const [toastVisible, setToastVisible] = useState(false);
  const [canNativeShare, setCanNativeShare] = useState(false);
  const [mounted, setMounted] = useState(false);
  const [anchorRect, setAnchorRect] = useState<AnchorRect | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const menuRef = useRef<HTMLDivElement>(null);
  const toastRef = useRef<HTMLDivElement>(null);
  const toastTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const menuId = useId();

  // RT-1 fix: the popover/toast portal to document.body (see below), so they must
  // only render client-side post-mount — document.body isn't available during SSR.
  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- TASK-467: post-mount SSR-hydration-safe boot flag, same pattern as canNativeShare below
    setMounted(true);
  }, []);

  const updateAnchorRect = useCallback(() => {
    const el = buttonRef.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    setAnchorRect({ top: rect.bottom, right: window.innerWidth - rect.right });
  }, []);

  // RT-1-FOLLOWUP fix: `right` above anchors the portal to the button's end edge
  // with no awareness of the box's own width, so a button near the left viewport
  // edge (e.g. the blog footer's justify-between layout) pushes a fixed-width
  // menu — or the toast, whose width depends on its text — past x=0. Measure the
  // actual portaled element after it paints and clamp its `left` to keep an
  // 8px margin from both edges; re-clamp on scroll/resize alongside the anchor.
  // `anchorRectRight` is the original CSS `right` value the element was painted
  // with (from React state, not read back from `el.style`, which this function
  // itself mutates) — that keeps repeated calls idempotent.
  const clampToViewport = useCallback((el: HTMLElement | null, anchorRectRight: number) => {
    if (!el) return;
    const width = el.getBoundingClientRect().width;
    const naturalLeft = window.innerWidth - (anchorRectRight + width);
    const maxLeft = window.innerWidth - width - VIEWPORT_EDGE_MARGIN;
    const clampedLeft = Math.min(Math.max(naturalLeft, VIEWPORT_EDGE_MARGIN), Math.max(maxLeft, VIEWPORT_EDGE_MARGIN));
    if (clampedLeft !== naturalLeft) {
      el.style.left = `${clampedLeft}px`;
      el.style.right = "auto";
    } else {
      el.style.left = "auto";
      el.style.right = `${anchorRectRight}px`;
    }
  }, []);

  // Recompute the portal's anchor position whenever the menu or toast is shown,
  // and keep it in sync with scroll/resize while either is visible.
  useLayoutEffect(() => {
    if (!menuOpen && !toastVisible) return;
    updateAnchorRect();
    window.addEventListener("scroll", updateAnchorRect, true);
    window.addEventListener("resize", updateAnchorRect);
    return () => {
      window.removeEventListener("scroll", updateAnchorRect, true);
      window.removeEventListener("resize", updateAnchorRect);
    };
  }, [menuOpen, toastVisible, updateAnchorRect]);

  // Runs after `anchorRect` paints the portal at its naive `right`-anchored
  // position — measure the real element and clamp it inside the viewport.
  useLayoutEffect(() => {
    if (!anchorRect) return;
    const runClamp = () => {
      clampToViewport(menuRef.current, anchorRect.right);
      clampToViewport(toastRef.current, anchorRect.right);
    };
    runClamp();
    window.addEventListener("scroll", runClamp, true);
    window.addEventListener("resize", runClamp);
    return () => {
      window.removeEventListener("scroll", runClamp, true);
      window.removeEventListener("resize", runClamp);
    };
  }, [anchorRect, menuOpen, toastVisible, clampToViewport]);

  useEffect(() => {
    // Post-mount capability probe (matches src/components/shared/ga4-script.tsx's
    // established pattern for TASK-462): navigator.share is an external-platform
    // read, not state derivable from props, and SSR has no `navigator` at all —
    // this must run client-side, after mount, exactly once.
    // eslint-disable-next-line react-hooks/set-state-in-effect -- TASK-467: post-mount capability probe, SSR-hydration-safe by design
    setCanNativeShare(
      typeof navigator !== "undefined" && typeof navigator.share === "function"
    );
  }, []);

  useEffect(() => {
    if (!menuOpen) return;
    function handleClickAway(event: MouseEvent) {
      const target = event.target as Node;
      // Menu is portaled to document.body (RT-1 fix), so containment must check
      // both the trigger container AND the portaled menu element.
      if (
        !containerRef.current?.contains(target) &&
        !menuRef.current?.contains(target)
      ) {
        setMenuOpen(false);
      }
    }
    function handleEscape(event: KeyboardEvent) {
      if (event.key === "Escape") setMenuOpen(false);
    }
    document.addEventListener("mousedown", handleClickAway);
    document.addEventListener("keydown", handleEscape);
    return () => {
      document.removeEventListener("mousedown", handleClickAway);
      document.removeEventListener("keydown", handleEscape);
    };
  }, [menuOpen]);

  useEffect(() => {
    return () => {
      if (toastTimeoutRef.current) clearTimeout(toastTimeoutRef.current);
    };
  }, []);

  const resolveUrl = useCallback(() => url ?? currentCanonicalUrl(), [url]);

  const track = useCallback((method: string) => {
    fireEvent("share", {
      method,
      page_path: typeof window !== "undefined" ? window.location.pathname : "",
    });
  }, []);

  const showToast = useCallback(() => {
    setToastVisible(true);
    if (toastTimeoutRef.current) clearTimeout(toastTimeoutRef.current);
    toastTimeoutRef.current = setTimeout(() => setToastVisible(false), 3000);
  }, []);

  const handleShareClick = useCallback(async () => {
    const shareUrl = resolveUrl();

    if (canNativeShare) {
      const shareData = {
        title: buildShareText(effectiveTitle),
        text: buildShareText(effectiveTitle),
        url: shareUrl,
      };
      try {
        // canShare is optional on the Navigator type in some lib.dom versions —
        // guard defensively before calling it.
        const nav = navigator as Navigator & { canShare?: (data: ShareData) => boolean };
        if (typeof nav.canShare === "function" && !nav.canShare(shareData)) {
          setMenuOpen(true);
          return;
        }
        await navigator.share(shareData);
        track("native_share");
      } catch {
        // User cancelled the native sheet, or share failed silently — no fallback
        // needed here since the OS sheet already gave the user options.
      }
      return;
    }

    setMenuOpen((open) => !open);
  }, [canNativeShare, resolveUrl, effectiveTitle, track]);

  const handleCopyLink = useCallback(async () => {
    const shareUrl = resolveUrl();
    try {
      await navigator.clipboard.writeText(shareUrl);
      showToast();
      track("copy_link");
    } catch {
      // Clipboard API unavailable/denied — silently no-op; other menu options remain.
    }
    setMenuOpen(false);
  }, [resolveUrl, showToast, track]);

  const handleExternalShare = useCallback(
    (method: "whatsapp" | "telegram" | "facebook", href: string) => {
      track(method);
      setMenuOpen(false);
      window.open(href, "_blank", "noopener,noreferrer");
    },
    [track]
  );

  const shareUrl = resolveUrl();

  // RT-1 fix: the fallback popover and toast are portaled to document.body instead
  // of rendering inline. Both live inside comparison cards with `overflow-hidden`
  // (frozen design geometry — never weakened to fix this), which clips any
  // absolutely-positioned descendant past the card boundary. A `position: fixed`
  // portal escapes every current and future ancestor-clipping context. Position
  // is computed from the trigger button's rect and re-measured on scroll/resize.
  const menuPortal =
    mounted && !canNativeShare && menuOpen && anchorRect
      ? createPortal(
          <div
            ref={menuRef}
            id={menuId}
            role="menu"
            dir="rtl"
            aria-label="אפשרויות שיתוף"
            style={{ position: "fixed", top: anchorRect.top + 8, right: anchorRect.right }}
            className="z-[100] w-56 rounded-2xl border border-black/[0.08] bg-white p-1.5 shadow-lg shadow-black/[0.08]"
          >
            <button type="button" role="menuitem" onClick={handleCopyLink} className={menuItemClass}>
              <LinkGlyph />
              העתקת קישור
            </button>
            <button
              type="button"
              role="menuitem"
              onClick={() => handleExternalShare("whatsapp", buildWhatsAppShareUrl(effectiveTitle, shareUrl))}
              className={menuItemClass}
            >
              <WhatsAppGlyph />
              וואטסאפ
            </button>
            <button
              type="button"
              role="menuitem"
              onClick={() => handleExternalShare("telegram", telegramShareUrl(effectiveTitle, shareUrl))}
              className={menuItemClass}
            >
              <TelegramGlyph />
              טלגרם
            </button>
            <button
              type="button"
              role="menuitem"
              onClick={() => handleExternalShare("facebook", facebookShareUrl(shareUrl))}
              className={menuItemClass}
            >
              <FacebookGlyph />
              פייסבוק
            </button>
          </div>,
          document.body
        )
      : null;

  const toastPortal =
    mounted && toastVisible && anchorRect
      ? createPortal(
          <div
            ref={toastRef}
            role="status"
            aria-live="polite"
            dir="rtl"
            style={{ position: "fixed", top: anchorRect.top + 8, right: anchorRect.right }}
            className="z-[100] whitespace-nowrap rounded-full bg-[#111318] px-4 py-2 text-xs font-semibold text-white shadow-lg"
          >
            הקישור הועתק
          </div>,
          document.body
        )
      : null;

  return (
    <div ref={containerRef} className={cn("relative inline-block", className)}>
      <button
        ref={buttonRef}
        type="button"
        onClick={handleShareClick}
        className={buttonClass}
        aria-haspopup={canNativeShare ? undefined : "menu"}
        aria-expanded={canNativeShare ? undefined : menuOpen}
        aria-controls={canNativeShare ? undefined : menuId}
      >
        <ShareGlyph />
        שיתוף
      </button>

      {menuPortal}
      {toastPortal}
    </div>
  );
}
