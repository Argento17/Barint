import Link from "next/link";

import { BariBrandLogo } from "@/components/brand/bari-brand-logo";
import { Separator } from "@/components/ui/separator";

import { HomeContainer } from "./section-frame";

const footerLinks = {
  content: [
    { label: "השוואות", href: "#comparisons" },
    { label: "דירוגים", href: "#comparisons" },
    { label: "מדריכים", href: "#guides" },
  ],
} as const;

export function HomeFooter() {
  return (
    <footer className="bg-zinc-900 py-14 text-zinc-300 md:py-16">
      <HomeContainer>
        <div className="flex flex-col items-center justify-between gap-8 text-center md:flex-row md:text-right">
          <div className="space-y-3">
            <Link href="/" aria-label="בית Bari" className="inline-flex w-fit">
              <BariBrandLogo surface="dark" />
            </Link>
            <p className="max-w-md text-sm leading-relaxed text-zinc-400">
              אינטליגנציית מזון ישראלית להשוואה, דירוג והבנה טובה יותר של מוצרים.
            </p>
          </div>

          <nav className="flex flex-wrap items-center justify-center gap-x-7 gap-y-3 text-sm md:justify-end">
            {footerLinks.content.map((l) => (
              <Link
                key={l.label}
                href={l.href}
                className="inline-flex px-1 text-zinc-400 transition hover:text-emerald-400"
              >
                {l.label}
              </Link>
            ))}
          </nav>
        </div>

        <Separator className="my-8 bg-zinc-800" />

        <p className="text-center text-sm text-zinc-500">© {new Date().getFullYear()} Bari. כל הזכויות שמורות.</p>
      </HomeContainer>
    </footer>
  );
}
