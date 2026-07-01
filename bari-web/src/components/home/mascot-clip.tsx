"use client";

import { useEffect, useRef } from "react";

import { cn } from "@/lib/utils";

type MascotClipProps = {
  /** Path under /public, e.g. "/mascots/clips/atom-molecule.mp4" */
  src: string;
  /** Classes for the outer stage (size, aspect, position). */
  className?: string;
  /** Classes for the rendered media element. */
  videoClassName?: string;
  /**
   * Borderless "bleed" mode: the warm studio backdrop is keyed out per-frame on
   * a canvas so the mascot renders with a real transparent background and blends
   * perfectly on any surface (no tile, no border, no soft shadow halo).
   * Without it, the clip renders inside a bounded rounded tile.
   */
  bleed?: boolean;
  /**
   * "plain" mode: the clip is already mastered on a flat backdrop that matches the
   * host section's color, so it plays straight through with no keyer and no tile —
   * the background blends invisibly. Cheapest path; preferred for clips authored on
   * the exact page color. Takes precedence over `bleed`.
   */
  plain?: boolean;
};

// Processing width for the keyer — the clips are 1280×720 but display small,
// so we downscale for a cheap per-frame loop.
const PROC_W = 360;
// Cap processing to ~30fps to keep the flood-fill cheap.
const FRAME_MS = 33;

/**
 * Decorative mascot animation. Source clips are opaque MP4s on a warm beige
 * studio backdrop. In `bleed` mode we luma/saturation-key that backdrop away on
 * a canvas (keeping the green/olive character and dark limbs) for a clean float;
 * otherwise the clip sits in a rounded tile.
 * Autoplays muted+looping; freezes on the first frame under prefers-reduced-motion.
 */
export function MascotClip({
  src,
  className,
  videoClassName,
  bleed = false,
  plain = false,
}: MascotClipProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Boxed + plain modes: simple looping video, pause under reduced motion.
  useEffect(() => {
    if (bleed) return;
    const video = videoRef.current;
    if (!video) return;
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    const apply = () => {
      if (mq.matches) {
        video.pause();
        video.currentTime = 0;
      } else {
        void video.play().catch(() => {});
      }
    };
    apply();
    mq.addEventListener("change", apply);
    return () => mq.removeEventListener("change", apply);
  }, [bleed]);

  // Bleed mode: draw + key each frame onto the canvas.
  useEffect(() => {
    if (!bleed) return;
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (!video || !canvas) return;
    const ctx = canvas.getContext("2d", { willReadFrequently: true });
    if (!ctx) return;

    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    let raf = 0;
    let last = 0;
    // Reusable buffers, sized on first frame.
    let visited: Uint8Array | null = null;
    let stack: Int32Array | null = null;

    const keyFrame = (w: number, h: number) => {
      const frame = ctx.getImageData(0, 0, w, h);
      const d = frame.data;
      const n = w * h;
      if (!visited || visited.length !== n) {
        visited = new Uint8Array(n);
        stack = new Int32Array(n);
      } else {
        visited.fill(0);
      }
      // Classify each pixel: character (green or dark) vs backdrop candidate.
      // We store a soft "background-ness" alpha for candidates; only those
      // reachable from the frame border (flood fill) are actually cleared, so
      // the character's own light highlights stay opaque.
      const bgAlpha = new Uint8Array(n); // 255 = keep, lower = more transparent
      for (let p = 0, i = 0; p < n; p++, i += 4) {
        const r = d[i];
        const g = d[i + 1];
        const b = d[i + 2];
        const mx = r > g ? (r > b ? r : b) : g > b ? g : b;
        const mn = r < g ? (r < b ? r : b) : g < b ? g : b;
        const sat = mx === 0 ? 0 : (mx - mn) / mx;
        const isGreen = g - r > 14 && g - b > 8; // olive body, leaf, scan glow
        const isDark = mx < 82; // limbs, eyes, rim, stem
        if (isGreen || isDark) {
          bgAlpha[p] = 255;
        } else {
          // Soft ramp: sat < 0.15 → fully background, > 0.34 → fully character.
          const t = (0.34 - sat) / 0.19;
          bgAlpha[p] = t <= 0 ? 255 : t >= 1 ? 0 : Math.round(255 * (1 - t));
        }
      }
      // Flood fill from the border through background candidates.
      const st = stack!;
      const vis = visited!;
      let sp = 0;
      const push = (p: number) => {
        if (!vis[p] && bgAlpha[p] < 250) {
          vis[p] = 1;
          st[sp++] = p;
        }
      };
      for (let x = 0; x < w; x++) {
        push(x);
        push((h - 1) * w + x);
      }
      for (let y = 0; y < h; y++) {
        push(y * w);
        push(y * w + w - 1);
      }
      while (sp > 0) {
        const p = st[--sp];
        const x = p % w;
        d[p * 4 + 3] = bgAlpha[p]; // clear/soften reachable background
        if (x > 0) push(p - 1);
        if (x < w - 1) push(p + 1);
        if (p >= w) push(p - w);
        if (p < n - w) push(p + w);
      }
      ctx.putImageData(frame, 0, 0);
    };

    const drawFrame = (ts: number) => {
      raf = requestAnimationFrame(drawFrame);
      if (ts - last < FRAME_MS) return;
      last = ts;
      if (video.readyState >= 2 && video.videoWidth > 0) {
        const h = Math.round((PROC_W * video.videoHeight) / video.videoWidth);
        if (canvas.width !== PROC_W || canvas.height !== h) {
          canvas.width = PROC_W;
          canvas.height = h;
        }
        ctx.drawImage(video, 0, 0, PROC_W, h);
        keyFrame(PROC_W, h);
      }
    };

    const start = () => {
      if (mq.matches) {
        video.pause();
      } else {
        void video.play().catch(() => {});
      }
    };
    start();
    mq.addEventListener("change", start);
    raf = requestAnimationFrame(drawFrame);
    return () => {
      cancelAnimationFrame(raf);
      mq.removeEventListener("change", start);
    };
  }, [bleed]);

  if (plain) {
    // Clip is mastered on the host section's color — play it straight, no tile.
    return (
      <div className={cn("pointer-events-none relative", className)} aria-hidden>
        <video
          ref={videoRef}
          src={src}
          muted
          loop
          playsInline
          autoPlay
          preload="auto"
          tabIndex={-1}
          className={cn("size-full object-contain", videoClassName)}
        />
      </div>
    );
  }

  if (bleed) {
    return (
      <div className={cn("pointer-events-none relative", className)} aria-hidden>
        <video
          ref={videoRef}
          src={src}
          muted
          loop
          playsInline
          autoPlay
          preload="auto"
          tabIndex={-1}
          style={{ position: "absolute", width: 1, height: 1, opacity: 0, pointerEvents: "none" }}
        />
        <canvas ref={canvasRef} className={cn("size-full object-contain", videoClassName)} />
      </div>
    );
  }

  return (
    <div
      className={cn(
        "relative overflow-hidden rounded-2xl border border-black/8 bg-white shadow-[0_1px_3px_rgba(17,19,24,0.06),0_1px_2px_rgba(17,19,24,0.04)]",
        className
      )}
      aria-hidden
    >
      <video
        ref={videoRef}
        src={src}
        muted
        loop
        playsInline
        autoPlay
        preload="metadata"
        tabIndex={-1}
        className={cn("pointer-events-none size-full object-cover", videoClassName)}
      />
    </div>
  );
}
