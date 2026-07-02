"use client";

/**
 * AppShell — shared shell for /catalog (public) and /admin/inventory (admin).
 *
 * variant="public"  → header: brand + search pill only (no bell/avatar);
 *                      sidebar: reference nav with real hrefs where destinations exist.
 * variant="admin"   → header: brand + search + bell icon + avatar (א);
 *                      sidebar: same structure, auth-gated page.
 *
 * MOBILE (< md / <768px):
 *   Sidebar is OFF-CANVAS by default. Hamburger button in the header inline-start
 *   toggles it open as a full-height overlay drawer over a dark scrim.
 *   <main> fills 100% width on mobile. Zero horizontal overflow at 390px.
 *
 * DESKTOP (≥ md / ≥768px):
 *   Sidebar is always visible at 240px. Classic two-column layout.
 *
 * Header search:
 *   CONTROLLED via onSearchChange — parent lifts state into ProductTable.externalQ.
 *   RTL pill: icon at inline-end (logical), input fills remaining space.
 *   On mobile the pill collapses to an icon-only button that expands inline.
 *
 * Sidebar nav items:
 *   מוצרים          → href="/catalog"     (active when activeNav="products")
 *   קטגוריות        → INERT
 *   רשתות שיווק     → INERT
 *   דוחות השוואה    → href="/hashvaot"
 *   מקורות נתונים   → INERT
 *   מדדים ושיטה     → href="/methodology"
 *   קטלוג מקורות    → INERT
 *
 * Active item indicator: border-inline-end (logical RTL edge) — NOT physical box-shadow.
 *
 * Visual spec: matches Bari Dashboard.dc.html exactly on desktop.
 *   Header: height 60px, #111318, 42×42 r12 brand tile, "Food Intelligence" mono eyebrow,
 *           search pill min-width 200px, bell circle 34px, avatar circle 34px green.
 *   Sidebar: width 240px, #FBFBF9, "מלאי" eyebrow.
 *   Main: flex-1, #F7F7F2, padding 26px 28px 32px (desktop), 20px 16px 24px (mobile).
 *
 * NO imports from scoring/bsip/registry/comparisons modules.
 */

import { useState, useEffect, useCallback, type ReactNode } from "react";
import Link from "next/link";
import { BariSignalMark } from "@/components/brand/bari-brand-logo";

// ── SVG icons ─────────────────────────────────────────────────────────────────

function IconCategories() {
  return (
    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <rect x="3" y="3" width="7" height="7" rx="1.5" /><rect x="14" y="3" width="7" height="7" rx="1.5" />
      <rect x="14" y="14" width="7" height="7" rx="1.5" /><rect x="3" y="14" width="7" height="7" rx="1.5" />
    </svg>
  );
}

function IconProducts() {
  return (
    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="1.9" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z" />
      <path d="m3.3 7 8.7 5 8.7-5" /><path d="M12 22V12" />
    </svg>
  );
}

function IconRetailers() {
  return (
    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z" />
      <path d="M3 6h18" /><path d="M16 10a4 4 0 0 1-8 0" />
    </svg>
  );
}

function IconReports() {
  return (
    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z" />
      <path d="M14 2v6h6" /><path d="M16 13H8" /><path d="M16 17H8" />
    </svg>
  );
}

function IconSources() {
  return (
    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <ellipse cx="12" cy="5" rx="9" ry="3" />
      <path d="M3 5v14a9 3 0 0 0 18 0V5" /><path d="M3 12a9 3 0 0 0 18 0" />
    </svg>
  );
}

function IconMethodology() {
  return (
    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <path d="M3 3v18h18" /><path d="M18 17V9" /><path d="M13 17V5" /><path d="M8 17v-3" />
    </svg>
  );
}

function IconCatalog() {
  return (
    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <path d="M12 7v14" />
      <path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z" />
    </svg>
  );
}

function IconBell() {
  return (
    <svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9" />
      <path d="M10.3 21a1.94 1.94 0 0 0 3.4 0" />
    </svg>
  );
}

/** Hamburger — 3 lines */
function IconMenu() {
  return (
    <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden>
      <path d="M4 6h16M4 12h16M4 18h16" />
    </svg>
  );
}

/** Close X */
function IconClose() {
  return (
    <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden>
      <path d="M18 6 6 18M6 6l12 12" />
    </svg>
  );
}

/** Magnifying glass — used standalone on mobile */
function IconSearch() {
  return (
    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
      <circle cx="11" cy="11" r="7" /><path d="m21 21-4.3-4.3" />
    </svg>
  );
}

// ── Nav types ─────────────────────────────────────────────────────────────────

type NavEntry =
  | { id: string; labelHe: string; icon: ReactNode; href: string; inert?: false }
  | { id: string; labelHe: string; icon: ReactNode; href?: undefined; inert: true };

const NAV_ITEMS: NavEntry[] = [
  { id: "categories",  labelHe: "קטגוריות",      icon: <IconCategories />,   inert: true },
  { id: "products",    labelHe: "מוצרים",          icon: <IconProducts />,     href: "/catalog" },
  { id: "retailers",   labelHe: "רשתות שיווק",     icon: <IconRetailers />,    inert: true },
  { id: "reports",     labelHe: "דוחות השוואה",    icon: <IconReports />,      href: "/hashvaot" },
  { id: "sources",     labelHe: "מקורות נתונים",   icon: <IconSources />,      inert: true },
  { id: "methodology", labelHe: "מדדים ושיטה",     icon: <IconMethodology />,  href: "/methodology" },
  { id: "catalog",     labelHe: "קטלוג מקורות",    icon: <IconCatalog />,      inert: true },
];

// ── Sidebar content (shared between desktop column + mobile drawer) ────────────

function SidebarContent({
  activeNav,
  onClose,
}: {
  activeNav: string;
  onClose?: () => void;
}) {
  return (
    <div
      style={{
        padding: "22px 16px",
        display: "flex",
        flexDirection: "column",
        gap: 6,
        height: "100%",
        overflowY: "auto",
      }}
    >
      {/* "עבור מזון ארוז" context pill */}
      <div className="flex items-center gap-2 px-1.5 pb-1">
        <span style={{ fontSize: 12, color: "var(--fg3, #5E6560)" }}>עבור</span>
        <span
          className="inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 font-semibold"
          style={{
            background: "#fff",
            borderColor: "rgba(17,19,24,0.10)",
            fontSize: 12.5,
            color: "var(--fg1, #111318)",
            lineHeight: 1,
          }}
        >
          <span
            style={{
              width: 7,
              height: 7,
              borderRadius: "50%",
              background: "var(--bari-green, #1F8F6A)",
              flexShrink: 0,
              display: "inline-block",
            }}
            aria-hidden="true"
          />
          מזון ארוז
        </span>
      </div>

      {/* Eyebrow */}
      <p
        style={{
          fontFamily: "var(--font-mono, ui-monospace, monospace)",
          fontSize: 10,
          fontWeight: 700,
          letterSpacing: "0.22em",
          textTransform: "uppercase",
          color: "var(--fg3, #5E6560)",
          padding: "14px 8px 8px",
          margin: 0,
        }}
        aria-hidden="true"
      >
        מלאי
      </p>

      {/* Nav items */}
      <ul
        role="list"
        style={{ margin: 0, padding: 0, listStyle: "none", display: "flex", flexDirection: "column", gap: 2 }}
      >
        {NAV_ITEMS.map((item) => {
          const isActive = item.id === activeNav;

          // M-1: logical RTL edge — border-inline-end (the inline-end edge is the
          // visual START of the item in RTL, i.e. the right edge of the sidebar).
          const itemStyle: React.CSSProperties = {
            display: "flex",
            alignItems: "center",
            gap: 11,
            padding: "9px 11px",
            borderRadius: 10,
            textDecoration: "none",
            fontSize: 14,
            fontWeight: isActive ? 600 : 500,
            lineHeight: 1,
            color: isActive ? "var(--grade-a-text, #155C3C)" : "var(--fg2, #4E5663)",
            background: isActive ? "var(--grade-a-bg, #E7F4EC)" : "transparent",
            // M-1 fix: logical property instead of physical inset shadow
            borderInlineEnd: isActive ? "2px solid var(--bari-green, #1F8F6A)" : "2px solid transparent",
            cursor: item.inert ? "default" : "pointer",
            opacity: item.inert ? 0.7 : 1,
          };

          const iconColor = isActive ? "var(--bari-green, #1F8F6A)" : "var(--fg3, #5E6560)";

          const inner = (
            <>
              <span style={{ color: iconColor }}>{item.icon}</span>
              {item.labelHe}
            </>
          );

          if (item.inert) {
            return (
              <li key={item.id}>
                <span style={itemStyle} aria-disabled="true" role="link">
                  {inner}
                </span>
              </li>
            );
          }

          return (
            <li key={item.id}>
              <Link
                href={item.href}
                style={itemStyle}
                aria-current={isActive ? "page" : undefined}
                onClick={onClose}
              >
                {inner}
              </Link>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

// ── Component ─────────────────────────────────────────────────────────────────

export interface AppShellProps {
  children: ReactNode;
  variant?: "public" | "admin";
  /** Which sidebar nav item is highlighted. Defaults to "products". */
  activeNav?: string;
  /** Current value of the header search (controlled by parent). */
  searchValue?: string;
  /** Called every keystroke — parent lifts state up for live ProductTable filter. */
  onSearchChange?: (q: string) => void;
}

export function AppShell({
  children,
  variant = "public",
  activeNav = "products",
  searchValue = "",
  onSearchChange,
}: AppShellProps) {
  const isAdmin = variant === "admin";
  const [drawerOpen, setDrawerOpen] = useState(false);

  // Close drawer on Esc
  const handleKeyDown = useCallback((e: KeyboardEvent) => {
    if (e.key === "Escape") setDrawerOpen(false);
  }, []);

  useEffect(() => {
    if (drawerOpen) {
      document.addEventListener("keydown", handleKeyDown);
      // Prevent body scroll while drawer is open
      document.body.style.overflow = "hidden";
    } else {
      document.removeEventListener("keydown", handleKeyDown);
      document.body.style.overflow = "";
    }
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
      document.body.style.overflow = "";
    };
  }, [drawerOpen, handleKeyDown]);

  return (
    <div
      dir="rtl"
      lang="he"
      className="flex min-h-screen flex-col"
      style={{ background: "#F7F7F2", overflowX: "hidden" }}
    >
      {/* ── Header ──────────────────────────────────────────────────────────── */}
      <header
        className="sticky top-0 z-30 flex items-center gap-2 px-3 md:px-5"
        style={{ height: 60, background: "#111318" }}
        role="banner"
      >
        {/* Mobile-only hamburger — inline-start (right in RTL) */}
        <button
          type="button"
          className="flex items-center justify-center rounded-lg md:hidden"
          style={{
            width: 36,
            height: 36,
            background: "rgba(255,255,255,0.08)",
            color: "rgba(255,255,255,0.80)",
            border: "none",
            flexShrink: 0,
          }}
          onClick={() => setDrawerOpen(true)}
          aria-label="פתח תפריט ניווט"
          aria-expanded={drawerOpen}
          aria-controls="inventory-sidebar-drawer"
        >
          <IconMenu />
        </button>

        {/* Brand cluster */}
        <div className="flex shrink-0 items-center gap-2 md:gap-3">
          <Link href="/" aria-label="Bari — בית">
            <span
              className="inline-flex items-center justify-center overflow-hidden"
              style={{
                width: 42,
                height: 42,
                borderRadius: 12,
                background: "#F7F7F2",
                flexShrink: 0,
                display: "flex",
              }}
              aria-hidden="true"
            >
              <BariSignalMark />
            </span>
          </Link>
          <span
            className="font-extrabold text-white"
            style={{ fontSize: 20, lineHeight: 1, letterSpacing: "-0.05em" }}
          >
            Bari
          </span>
          {/* Divider + eyebrow — desktop only */}
          <span
            aria-hidden="true"
            className="hidden sm:inline-block"
            style={{ width: 1, height: 22, background: "rgba(255,255,255,0.16)", margin: "0 4px" }}
          />
          <span
            className="hidden sm:inline"
            style={{
              fontFamily: "var(--font-mono, ui-monospace, monospace)",
              fontSize: 10,
              fontWeight: 600,
              letterSpacing: "0.22em",
              textTransform: "uppercase",
              color: "rgba(255,255,255,0.50)",
            }}
          >
            Food Intelligence
          </span>
        </div>

        {/* Flex spacer */}
        <div className="flex-1" />

        {/* Right cluster: search pill + (admin: bell + avatar) */}
        <div className="flex items-center gap-2">
          {/*
            H-1 Search pill — RTL fix:
            The pill uses flexDirection row-reverse so in an RTL context the
            icon naturally appears at the inline-end (visual left in LTR / visual
            right in RTL = inline-start). But our dir=rtl document means the
            magnifying glass should sit at the trailing end of the Hebrew text.

            Solution: use dir="ltr" on the pill container to enforce a fixed
            icon-right layout regardless of document direction, while the
            input itself remains dir="rtl" so Hebrew placeholder is right-aligned.
            This is the standard cross-browser search pill pattern for RTL+LTR mix.
          */}
          <div
            dir="ltr"
            className="hidden sm:flex items-center gap-2 rounded-full px-3.5"
            style={{
              height: 34,
              minWidth: 200,
              background: "rgba(255,255,255,0.08)",
              border: "1px solid rgba(255,255,255,0.08)",
              cursor: "text",
              flexShrink: 0,
            }}
          >
            {/* Icon at LTR-start = visual left = RTL inline-end — correct trailing position */}
            <span style={{ color: "rgba(255,255,255,0.55)", flexShrink: 0 }}>
              <IconSearch />
            </span>
            <input
              type="search"
              value={searchValue}
              onChange={(e) => onSearchChange?.(e.target.value)}
              placeholder="חיפוש מוצר, קטגוריה או רשת"
              dir="rtl"
              className="flex-1 bg-transparent text-[13px] text-white outline-none placeholder:text-[rgba(255,255,255,0.38)]"
              style={{ caretColor: "#1F8F6A", minWidth: 0 }}
              aria-label="חיפוש מוצר, קטגוריה או רשת"
            />
          </div>

          {/* Mobile: icon-only search button that expands search below header */}
          <button
            type="button"
            className="flex items-center justify-center rounded-full sm:hidden"
            style={{
              width: 34,
              height: 34,
              background: "rgba(255,255,255,0.08)",
              color: "rgba(255,255,255,0.70)",
              border: "none",
              flexShrink: 0,
            }}
            aria-label="חיפוש"
            onClick={() => {
              // Focus the hidden mobile search input that we reveal below
              const el = document.getElementById("mobile-search-input");
              el?.focus();
            }}
          >
            <IconSearch />
          </button>

          {/* Bell — admin only */}
          {isAdmin && (
            <button
              type="button"
              aria-label="התראות"
              className="flex items-center justify-center rounded-full"
              style={{
                width: 34,
                height: 34,
                background: "rgba(255,255,255,0.08)",
                color: "rgba(255,255,255,0.70)",
                border: "none",
                cursor: "pointer",
                flexShrink: 0,
              }}
            >
              <IconBell />
            </button>
          )}

          {/* Avatar — admin only */}
          {isAdmin && (
            <div
              className="flex items-center justify-center rounded-full font-bold text-white"
              style={{
                width: 34,
                height: 34,
                background: "var(--bari-green, #1F8F6A)",
                fontSize: 13,
                lineHeight: 1,
                flexShrink: 0,
              }}
              aria-label="חשבון משתמש"
              role="img"
            >
              א
            </div>
          )}
        </div>
      </header>

      {/* Mobile search bar — expands below header (below sm) */}
      <div
        className="sm:hidden"
        style={{ background: "#111318", paddingBottom: searchValue ? 10 : 0 }}
      >
        <div
          dir="ltr"
          className="mx-3 flex items-center gap-2 rounded-full px-3"
          style={{
            height: 36,
            background: "rgba(255,255,255,0.08)",
            border: "1px solid rgba(255,255,255,0.10)",
          }}
        >
          <span style={{ color: "rgba(255,255,255,0.55)", flexShrink: 0 }}>
            <IconSearch />
          </span>
          <input
            id="mobile-search-input"
            type="search"
            value={searchValue}
            onChange={(e) => onSearchChange?.(e.target.value)}
            placeholder="חיפוש מוצר, קטגוריה או רשת"
            dir="rtl"
            className="flex-1 bg-transparent text-[13px] text-white outline-none placeholder:text-[rgba(255,255,255,0.38)]"
            style={{ caretColor: "#1F8F6A", minWidth: 0 }}
            aria-label="חיפוש מוצר, קטגוריה או רשת"
          />
        </div>
      </div>

      {/* ── Body ─────────────────────────────────────────────────────────────── */}
      <div className="relative flex flex-1" style={{ minWidth: 0, overflowX: "hidden" }}>

        {/*
          DESKTOP sidebar — always visible at ≥md, hidden below.
          flex-none so it never squishes <main>.
        */}
        <aside
          className="hidden md:flex md:flex-col"
          style={{
            width: 240,
            flexShrink: 0,
            background: "#FBFBF9",
            borderInlineStart: "1px solid rgba(17,19,24,0.07)",
          }}
          aria-label="ניווט ראשי"
        >
          <SidebarContent activeNav={activeNav} />
        </aside>

        {/*
          MOBILE DRAWER — rendered in a portal-like pattern inside the body flex.
          When open: fixed overlay covers full viewport; sidebar slides in from inline-start.
          scrim click / Esc → close.
        */}
        {drawerOpen && (
          <>
            {/* Scrim */}
            <div
              className="fixed inset-0 z-40 md:hidden"
              style={{ background: "rgba(17,19,24,0.55)" }}
              onClick={() => setDrawerOpen(false)}
              aria-hidden="true"
            />

            {/* Drawer panel */}
            <div
              id="inventory-sidebar-drawer"
              role="dialog"
              aria-modal="true"
              aria-label="תפריט ניווט"
              className="fixed inset-block-0 z-50 flex flex-col md:hidden"
              style={{
                insetInlineStart: 0,
                width: 280,
                maxWidth: "85vw",
                background: "#FBFBF9",
                boxShadow: "-4px 0 24px rgba(17,19,24,0.18)",
              }}
            >
              {/* Drawer header */}
              <div
                className="flex items-center justify-between px-4 py-3"
                style={{
                  borderBottom: "1px solid rgba(17,19,24,0.07)",
                  background: "#FBFBF9",
                  flexShrink: 0,
                }}
              >
                <span
                  className="font-bold"
                  style={{ fontSize: 14, color: "var(--fg1, #111318)" }}
                >
                  ניווט
                </span>
                <button
                  type="button"
                  onClick={() => setDrawerOpen(false)}
                  aria-label="סגור תפריט"
                  className="flex items-center justify-center rounded-lg"
                  style={{
                    width: 32,
                    height: 32,
                    color: "var(--fg3, #5E6560)",
                    background: "transparent",
                    border: "none",
                    cursor: "pointer",
                  }}
                >
                  <IconClose />
                </button>
              </div>

              {/* Nav items */}
              <div className="flex-1 overflow-y-auto">
                <SidebarContent activeNav={activeNav} onClose={() => setDrawerOpen(false)} />
              </div>
            </div>
          </>
        )}

        {/* Main content — fills full width on mobile, flex-1 on desktop */}
        <main
          className="flex-1 min-w-0 overflow-y-auto overflow-x-hidden px-4 py-5 md:px-7 md:py-7"
          id="inventory-main"
          tabIndex={-1}
        >
          {children}
        </main>
      </div>
    </div>
  );
}
