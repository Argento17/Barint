"use client";

/**
 * MobileActionBar — Ynet-style bottom quick-action bar.
 *
 * Mobile-only (hidden md+), fixed to the viewport bottom. Hidden near the top of the
 * page, slides in once the reader has scrolled past the hero (~400px). Actions: back,
 * share (native share sheet with clipboard fallback), WhatsApp share, bookmark/save
 * (persisted to localStorage, scoped per-URL).
 *
 * Mounted once per page-type template (comparison pages, blog articles, guides, news) —
 * see call sites. Not used on the homepage or hub/index pages.
 *
 * Presentation-only: does not read from BariProductVM or any BSIP/scoring module.
 */

import { useCallback, useEffect, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import { ArrowRight, Bookmark, Share2 } from "lucide-react";

import { cn } from "@/lib/utils";

const SCROLL_SHOW_THRESHOLD = 400;
const BOOKMARKS_STORAGE_KEY = "bari:bookmarks";
const TOAST_DURATION_MS = 1600;

function WhatsAppIcon({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 24 24"
      className={className}
      fill="currentColor"
      aria-hidden
    >
      <path d="M12.04 2c-5.52 0-10 4.48-10 10 0 1.77.46 3.45 1.27 4.9L2 22l5.25-1.38a9.94 9.94 0 0 0 4.79 1.22h.01c5.52 0 10-4.48 10-10s-4.48-10-10.01-10Zm0 18.2h-.01a8.2 8.2 0 0 1-4.18-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.19 8.19 0 0 1-1.26-4.35c0-4.53 3.69-8.2 8.24-8.2 2.2 0 4.27.86 5.82 2.41a8.16 8.16 0 0 1 2.41 5.8c0 4.53-3.69 8.2-8.23 8.2Zm4.51-6.14c-.25-.12-1.47-.72-1.7-.81-.23-.08-.39-.12-.56.13-.16.24-.64.81-.78.97-.15.16-.29.18-.54.06-.25-.12-1.05-.39-2-1.23-.74-.66-1.24-1.47-1.39-1.72-.14-.24-.02-.38.11-.5.11-.11.25-.29.37-.43.12-.15.16-.25.24-.41.08-.16.04-.31-.02-.43-.06-.12-.56-1.35-.77-1.85-.2-.48-.4-.42-.56-.42-.14-.01-.31-.01-.47-.01a.9.9 0 0 0-.66.31c-.22.24-.86.85-.86 2.06 0 1.22.89 2.4 1.01 2.56.12.16 1.75 2.67 4.24 3.74.59.26 1.06.41 1.42.52.6.19 1.14.16 1.57.1.48-.07 1.47-.6 1.68-1.18.21-.58.21-1.07.14-1.18-.06-.1-.22-.16-.47-.28Z" />
    </svg>
  );
}

interface MobileActionBarProps {
  /** Page title used for share text. Defaults to document.title at click time. */
  title?: string;
}

export function MobileActionBar({ title }: MobileActionBarProps) {
  const pathname = usePathname();
  const router = useRouter();

  const [visible, setVisible] = useState(false);
  const [saved, setSaved] = useState(false);
  const [toast, setToast] = useState<string | null>(null);

  // Scroll-driven slide in/out.
  useEffect(() => {
    const handleScroll = () => {
      setVisible(window.scrollY > SCROLL_SHOW_THRESHOLD);
    };
    handleScroll();
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // Read the saved state for the current URL on mount (and on client-side route change).
  useEffect(() => {
    if (typeof window === "undefined") return;
    const checkSaved = () => {
      try {
        const raw = window.localStorage.getItem(BOOKMARKS_STORAGE_KEY);
        const bookmarks: string[] = raw ? JSON.parse(raw) : [];
        setSaved(bookmarks.includes(window.location.href));
      } catch {
        // Corrupt/unavailable storage — treat as not-saved.
        setSaved(false);
      }
    };
    checkSaved();
  }, [pathname]);

  useEffect(() => {
    if (!toast) return;
    const t = setTimeout(() => setToast(null), TOAST_DURATION_MS);
    return () => clearTimeout(t);
  }, [toast]);

  const handleBack = useCallback(() => {
    if (typeof window === "undefined") return;
    if (window.history.length > 1) {
      window.history.back();
      return;
    }
    // No history to go back to — navigate to a sensible parent route.
    const segments = pathname.split("/").filter(Boolean);
    const parent = segments.length > 1 ? `/${segments[0]}` : "/";
    router.push(parent);
  }, [pathname, router]);

  const handleShare = useCallback(async () => {
    if (typeof window === "undefined") return;
    const shareTitle = title ?? document.title;
    const url = window.location.href;
    if (navigator.share) {
      try {
        await navigator.share({ title: shareTitle, url });
      } catch {
        // User cancelled the native share sheet — no-op.
      }
      return;
    }
    try {
      await navigator.clipboard.writeText(url);
      setToast("הועתק");
    } catch {
      setToast("לא ניתן להעתיק");
    }
  }, [title]);

  const handleWhatsApp = useCallback(() => {
    if (typeof window === "undefined") return;
    const shareTitle = title ?? document.title;
    const text = encodeURIComponent(`${shareTitle} ${window.location.href}`);
    window.open(`https://wa.me/?text=${text}`, "_blank", "noopener,noreferrer");
  }, [title]);

  const handleBookmark = useCallback(() => {
    if (typeof window === "undefined") return;
    const url = window.location.href;
    try {
      const raw = window.localStorage.getItem(BOOKMARKS_STORAGE_KEY);
      const bookmarks: string[] = raw ? JSON.parse(raw) : [];
      const isSaved = bookmarks.includes(url);
      const next = isSaved
        ? bookmarks.filter((b) => b !== url)
        : [...bookmarks, url];
      window.localStorage.setItem(BOOKMARKS_STORAGE_KEY, JSON.stringify(next));
      setSaved(!isSaved);
      setToast(isSaved ? "הוסר מהשמורים" : "נשמר");
    } catch {
      setToast("שמירה נכשלה");
    }
  }, []);

  return (
    <nav
      aria-label="פעולות מהירות"
      dir="rtl"
      className={cn(
        "md:hidden fixed inset-x-0 bottom-0 z-40",
        "transition-transform duration-300 ease-out motion-reduce:transition-none motion-reduce:duration-0",
        visible ? "translate-y-0" : "translate-y-full"
      )}
    >
      {toast ? (
        <div className="pointer-events-none flex justify-center pb-2">
          <span className="rounded-full bg-[#111318] px-3 py-1.5 text-xs font-semibold text-white shadow-lg">
            {toast}
          </span>
        </div>
      ) : null}

      <div
        className="flex items-center justify-around border-t border-black/[0.08] bg-white/95 px-2 pt-2 shadow-[0_-4px_16px_-8px_rgba(17,19,24,0.15)] backdrop-blur-sm"
        style={{ paddingBottom: "max(0.5rem, env(safe-area-inset-bottom))" }}
      >
        <button
          type="button"
          onClick={handleBack}
          aria-label="חזרה"
          className="flex flex-col items-center gap-1 rounded-lg px-3 py-1.5 text-[#4E5663] transition-colors hover:text-[#111318] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#167A58]"
        >
          <ArrowRight className="size-5" aria-hidden />
          <span className="text-[10px] font-semibold">חזרה</span>
        </button>

        <button
          type="button"
          onClick={handleShare}
          aria-label="שיתוף"
          className="flex flex-col items-center gap-1 rounded-lg px-3 py-1.5 text-[#4E5663] transition-colors hover:text-[#111318] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#167A58]"
        >
          <Share2 className="size-5" aria-hidden />
          <span className="text-[10px] font-semibold">שיתוף</span>
        </button>

        <button
          type="button"
          onClick={handleWhatsApp}
          aria-label="שיתוף בוואטסאפ"
          className="flex flex-col items-center gap-1 rounded-lg px-3 py-1.5 text-[#4E5663] transition-colors hover:text-[#111318] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#167A58]"
        >
          <WhatsAppIcon className="size-5" />
          <span className="text-[10px] font-semibold">וואטסאפ</span>
        </button>

        <button
          type="button"
          onClick={handleBookmark}
          aria-label={saved ? "הסרה מהשמורים" : "שמירה"}
          aria-pressed={saved}
          className={cn(
            "flex flex-col items-center gap-1 rounded-lg px-3 py-1.5 transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#167A58]",
            saved ? "text-[#167A58]" : "text-[#4E5663] hover:text-[#111318]"
          )}
        >
          <Bookmark className="size-5" aria-hidden fill={saved ? "currentColor" : "none"} />
          <span className="text-[10px] font-semibold">{saved ? "שמור" : "שמירה"}</span>
        </button>
      </div>
    </nav>
  );
}
