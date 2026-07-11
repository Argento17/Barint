"use client";

// Subtle scroll-in reveal wrapper — owner-preferred "a little motion where it earns
// attention" (icon-style preference note). Fades + scales content in once it enters the
// viewport, using IntersectionObserver (no scroll listener). Fully inert — renders
// visible/static content immediately — when the browser reports `prefers-reduced-motion:
// reduce`, per the accessibility hard rule.
//
// `prefers-reduced-motion` is read via useSyncExternalStore (React's canonical hook for
// subscribing to external browser state) rather than an effect that calls setState in its
// synchronous body — the latter trips the react-hooks/set-state-in-effect rule and, more to
// the point, is exactly the cascading-render pattern that rule exists to catch.

import { useEffect, useRef, useState, useSyncExternalStore } from "react";

import { cn } from "@/lib/utils";

function subscribeReducedMotion(callback: () => void) {
  const mql = window.matchMedia("(prefers-reduced-motion: reduce)");
  mql.addEventListener("change", callback);
  return () => mql.removeEventListener("change", callback);
}
function getReducedMotionSnapshot() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}
function getReducedMotionServerSnapshot() {
  return false;
}

export function ScrollReveal({
  children,
  className,
  delayMs = 0,
}: {
  children: React.ReactNode;
  className?: string;
  /** Optional stagger, e.g. for a row of cards. */
  delayMs?: number;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const [revealed, setRevealed] = useState(false);
  const reducedMotion = useSyncExternalStore(
    subscribeReducedMotion,
    getReducedMotionSnapshot,
    getReducedMotionServerSnapshot
  );

  useEffect(() => {
    // Reduced-motion: skip the observer entirely; `effectiveRevealed` below shows the
    // content immediately without any state transition.
    if (reducedMotion) return;
    const node = ref.current;
    if (!node) return;
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            setRevealed(true);
            observer.disconnect();
          }
        }
      },
      { threshold: 0.25, rootMargin: "0px 0px -10% 0px" }
    );
    observer.observe(node);
    return () => observer.disconnect();
  }, [reducedMotion]);

  const effectiveRevealed = revealed || reducedMotion;

  return (
    <div
      ref={ref}
      className={cn(
        "transition-[opacity,transform] duration-500 ease-out",
        effectiveRevealed
          ? "translate-y-0 scale-100 opacity-100"
          : "translate-y-2 scale-[0.92] opacity-0",
        className
      )}
      style={{ transitionDelay: effectiveRevealed ? `${delayMs}ms` : "0ms" }}
    >
      {children}
    </div>
  );
}
