"use client";

import Link from "next/link";
import { Menu } from "lucide-react";

import { BariBrandLogo } from "@/components/brand/bari-brand-logo";
import { HomeContainer } from "@/components/home/section-frame";
import { Button } from "@/components/ui/button";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";

const navLinks = [
  { label: "השוואות", href: "/#comparisons" },
  { label: "דירוגים", href: "/#rankings" },
  { label: "רכיבים", href: "/#ingredients" },
  { label: "מדריכים", href: "/#guides" },
] as const;

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-50 border-b border-zinc-200/70 bg-white/85 backdrop-blur-xl supports-[backdrop-filter]:bg-white/75">
      <HomeContainer>
        <div className="flex h-16 items-center justify-between gap-4 sm:h-[4.25rem]">
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
              variant="outline"
              size="sm"
              className="ms-3 rounded-xl border-zinc-200 bg-white/80"
              asChild
            >
              <Link href="/products/demo">מסך הדגמה</Link>
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
              <SheetHeader className="border-b border-zinc-200/70 pb-4 text-right">
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
                  href="/products/demo"
                  className="rounded-xl px-3 py-3 text-sm font-semibold text-emerald-700 transition hover:bg-emerald-50"
                >
                  מסך הדגמה
                </Link>
              </nav>
            </SheetContent>
          </Sheet>
        </div>
      </HomeContainer>
    </header>
  );
}
