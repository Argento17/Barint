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
    <header className="sticky top-0 z-50 border-b border-zinc-200/60 bg-white">
      <HomeContainer>
        <div className={cn("flex items-center justify-between gap-4", siteHeaderHeightClass)}>
          <Link href="/" aria-label="בית Bari" className="flex shrink-0 items-center">
            <BariBrandLogo />
          </Link>

          <nav className="hidden items-center gap-1 md:flex" aria-label="ניווט ראשי">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="rounded-xl px-3 py-2 text-sm font-medium text-zinc-600 transition hover:bg-emerald-50 hover:text-emerald-800"
              >
                {link.label}
              </Link>
            ))}
            <Button
              size="sm"
              className="ms-3 rounded-xl bg-emerald-600 px-4 font-semibold text-white shadow-sm shadow-emerald-600/15 hover:bg-emerald-700"
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
                className="rounded-xl text-zinc-700 md:hidden"
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
                    className="rounded-xl px-3 py-3 text-sm font-medium text-zinc-700 transition hover:bg-emerald-50 hover:text-emerald-800"
                  >
                    {link.label}
                  </Link>
                ))}
                <Link
                  href="/#newsletter"
                  className="mt-2 rounded-xl bg-emerald-600 px-3 py-3 text-center text-sm font-semibold text-white shadow-sm shadow-emerald-600/15 transition hover:bg-emerald-700"
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
