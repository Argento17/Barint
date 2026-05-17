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
    <header className="reveal-up sticky top-0 z-50 border-b border-zinc-200/20 bg-[#f7f8f6]/50 shadow-[0_1px_0_rgba(255,255,255,0.45)] backdrop-blur-xl">
      <HomeContainer>
        <div className={cn("flex items-center justify-between gap-10", siteHeaderHeightClass)}>
          <Link
            href="/"
            aria-label="בית Bari"
            className="group flex shrink-0 items-center transition-opacity duration-500 ease-out hover:opacity-90"
          >
            <BariBrandLogo />
          </Link>

          <nav className="hidden items-center gap-4 md:flex" aria-label="ניווט ראשי">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="inline-flex items-center rounded-2xl px-3.5 py-2 text-[0.95rem] font-semibold tracking-[-0.012em] text-zinc-500 transition-[color,background-color,opacity] duration-500 ease-out hover:bg-white/35 hover:text-zinc-900"
              >
                {link.label}
              </Link>
            ))}
            <Button
              size="sm"
              className="ms-5 h-9 rounded-2xl bg-zinc-950/95 px-4 text-[0.92rem] font-semibold tracking-[-0.012em] text-white shadow-sm shadow-zinc-950/10 transition-[background-color,opacity,transform,box-shadow] duration-500 ease-out hover:-translate-y-px hover:bg-zinc-900 hover:shadow-zinc-950/15"
              asChild
            >
              <Link href="/#newsletter">הירשמו לניוזלטר</Link>
            </Button>
          </nav>

          <Sheet>
            <SheetTrigger asChild>
              <Button
                variant="ghost"
                size="icon"
                className="rounded-2xl text-zinc-700 transition-[background-color,opacity] duration-500 ease-out hover:bg-white/35 md:hidden"
                aria-label="פתיחת תפריט"
              >
                <Menu className="size-5" />
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="gap-0 pt-14">
              <SheetHeader className="pb-4 text-right">
                <SheetTitle className="text-right">
                  <Link href="/" aria-label="בית Bari">
                    <BariBrandLogo />
                  </Link>
                </SheetTitle>
              </SheetHeader>
              <nav className="flex flex-col gap-1 p-4" aria-label="ניווט נייד">
                {navLinks.map((link) => (
                  <Link
                    key={link.href}
                    href={link.href}
                    className="inline-flex items-center rounded-2xl px-3 py-3 text-base font-semibold tracking-[-0.012em] text-zinc-700 transition-[background-color,color] duration-500 ease-out hover:bg-zinc-50 hover:text-zinc-950"
                  >
                    {link.label}
                  </Link>
                ))}
                <Link
                  href="/#newsletter"
                  className="mt-2 rounded-2xl bg-zinc-950 px-3 py-3 text-center text-sm font-semibold text-white shadow-sm shadow-zinc-950/10 transition-colors duration-500 ease-out hover:bg-zinc-800"
                >
                  הירשמו לניוזלטר
                </Link>
              </nav>
            </SheetContent>
          </Sheet>
        </div>
      </HomeContainer>
    </header>
  );
}
