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
    <header className="reveal-up sticky top-0 z-50 border-b border-black/[0.08] bg-[#F7F7F2]/82 shadow-[0_1px_0_rgba(255,255,255,0.04)] backdrop-blur-xl">
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
                className="inline-flex items-center rounded-2xl px-3.5 py-2 text-[0.95rem] font-semibold tracking-[-0.012em] text-[#4E5663] transition-[color,background-color,opacity] duration-500 ease-out hover:bg-[#FFFFFF]/68 hover:text-[#111318]"
              >
                {link.label}
              </Link>
            ))}
            <Button
              size="sm"
              className="nav-newsletter-cta ms-5 h-9 rounded-full border border-black/[0.08] bg-[#FFFFFF] px-4 text-[0.92rem] font-semibold tracking-[-0.012em] text-[#111318] shadow-sm shadow-slate-900/10 transition-[background-color,border-color,opacity,transform] duration-500 ease-out hover:-translate-y-px hover:border-[#1F8F6A]/30 hover:bg-[#FFFFFF]"
              asChild
            >
              <Link href="/#newsletter">
                <span className="relative z-10 inline-flex items-center gap-2">
                  הרשמו לניוזלטר
                  <span className="nav-newsletter-dot size-1.5 rounded-full bg-[#1F8F6A]" aria-hidden />
                </span>
              </Link>
            </Button>
          </nav>

          <Sheet>
            <SheetTrigger asChild>
              <Button
                variant="ghost"
                size="icon"
                className="rounded-2xl text-[#111318] transition-[background-color,opacity] duration-500 ease-out hover:bg-[#FFFFFF]/58 md:hidden"
                aria-label="פתיחת תפריט"
              >
                <Menu className="size-5" />
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="gap-0 border-black/[0.08] bg-[#FFFFFF] pt-14 text-[#111318]">
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
                    className="inline-flex items-center rounded-2xl px-3 py-3 text-base font-semibold tracking-[-0.012em] text-[#4E5663] transition-[background-color,color] duration-500 ease-out hover:bg-[#F7F7F2]/80 hover:text-[#111318]"
                  >
                    {link.label}
                  </Link>
                ))}
                <Link
                  href="/#newsletter"
                  className="nav-newsletter-cta mt-2 rounded-full border border-black/[0.08] bg-[#FFFFFF] px-3 py-3 text-center text-sm font-semibold text-[#111318] shadow-sm shadow-slate-900/10 transition-[background-color,border-color] duration-500 ease-out hover:border-[#1F8F6A]/30 hover:bg-[#FFFFFF]"
                >
                  <span className="relative z-10 inline-flex items-center justify-center gap-2">
                    הרשמו לניוזלטר
                    <span className="nav-newsletter-dot size-1.5 rounded-full bg-[#1F8F6A]" aria-hidden />
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
