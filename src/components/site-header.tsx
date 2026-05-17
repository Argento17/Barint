"use client";

import Link from "next/link";
import { Menu } from "lucide-react";

import { BariBrandLogo } from "@/components/brand/bari-brand-logo";
import { HomeContainer } from "@/components/home/section-frame";
import { Button } from "@/components/ui/button";
import { siteHeaderHeightClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";

const navLinks = [
  { label: "השוואות", href: "/#comparisons" },
  { label: "דירוגים", href: "/#comparisons" },
  { label: "מדריכים", href: "/#guides" },
] as const;

export function SiteHeader() {
  return (
    <header className="reveal-up sticky top-0 z-50 border-b border-emerald-300/10 bg-[#050706]/72 shadow-[0_1px_0_rgba(16,185,129,0.08)] backdrop-blur-xl">
      <HomeContainer>
        <div className={cn("flex items-center justify-between gap-10", siteHeaderHeightClass)}>
          <Link
            href="/"
            aria-label="בית Bari"
            className="group flex shrink-0 items-center transition-opacity duration-500 ease-out hover:opacity-90"
          >
            <BariBrandLogo surface="dark" />
          </Link>

          <nav className="hidden items-center gap-4 md:flex" aria-label="ניווט ראשי">
            {navLinks.map((link) => (
              <Link
                key={`${link.label}-${link.href}`}
                href={link.href}
                className="inline-flex items-center rounded-2xl px-3.5 py-2 text-[0.95rem] font-semibold tracking-[-0.012em] text-zinc-400 transition-[color,background-color,opacity] duration-500 ease-out hover:bg-white/[0.045] hover:text-zinc-100"
              >
                {link.label}
              </Link>
            ))}
            <Button
              size="sm"
              className="nav-newsletter-cta ms-5 h-9 rounded-full border border-white/10 bg-neutral-950 px-4 text-[0.92rem] font-semibold tracking-[-0.012em] text-white shadow-sm shadow-zinc-950/10 transition-[background-color,border-color,opacity,transform] duration-500 ease-out hover:-translate-y-px hover:border-emerald-400/30 hover:bg-zinc-900"
              asChild
            >
              <Link href="/#newsletter">
                <span className="relative z-10 inline-flex items-center gap-2">
                  הרשמו לניוזלטר
                  <span className="size-1.5 rounded-full bg-emerald-400/80" aria-hidden />
                </span>
              </Link>
            </Button>
          </nav>

          <Sheet>
            <SheetTrigger asChild>
              <Button
                variant="ghost"
                size="icon"
                className="rounded-2xl text-zinc-200 transition-[background-color,opacity] duration-500 ease-out hover:bg-white/[0.055] md:hidden"
                aria-label="פתיחת תפריט"
              >
                <Menu className="size-5" />
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="gap-0 border-emerald-300/10 bg-zinc-950 pt-14 text-white">
              <SheetHeader className="pb-4 text-right">
                <SheetTitle className="text-right">
                  <Link href="/" aria-label="בית Bari">
                    <BariBrandLogo surface="dark" />
                  </Link>
                </SheetTitle>
              </SheetHeader>
              <nav className="flex flex-col gap-1 p-4" aria-label="ניווט נייד">
                {navLinks.map((link) => (
                  <Link
                    key={`${link.label}-${link.href}`}
                    href={link.href}
                    className="inline-flex items-center rounded-2xl px-3 py-3 text-base font-semibold tracking-[-0.012em] text-zinc-300 transition-[background-color,color] duration-500 ease-out hover:bg-white/[0.055] hover:text-white"
                  >
                    {link.label}
                  </Link>
                ))}
                <Link
                  href="/#newsletter"
                  className="nav-newsletter-cta mt-2 rounded-full border border-white/10 bg-neutral-950 px-3 py-3 text-center text-sm font-semibold text-white shadow-sm shadow-zinc-950/10 transition-[background-color,border-color] duration-500 ease-out hover:border-emerald-400/30 hover:bg-zinc-800"
                >
                  <span className="relative z-10 inline-flex items-center justify-center gap-2">
                    הרשמו לניוזלטר
                    <span className="size-1.5 rounded-full bg-emerald-400/80" aria-hidden />
                  </span>
                </Link>
              </nav>
            </SheetContent>
          </Sheet>
        </div>
      </HomeContainer>
    </header>
  );
}
