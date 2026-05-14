import Link from "next/link";

import { BariBrandLogo } from "@/components/brand/bari-brand-logo";
import { Separator } from "@/components/ui/separator";

import { HomeContainer } from "./section-frame";

const footerLinks = {
  content: [
    { label: "השוואות", href: "#comparisons" },
    { label: "דירוגים", href: "#rankings" },
    { label: "מדריך רכיבים", href: "#ingredients" },
    { label: "מאמרים", href: "#guides" },
  ],
  about: [
    { label: "מי אנחנו", href: "#methodology" },
    { label: "המתודולוגיה שלנו", href: "#methodology" },
    { label: "קהילה", href: "#community" },
  ],
  legal: [
    { label: "תנאי שימוש", href: "#" },
    { label: "מדיניות פרטיות", href: "#" },
  ],
} as const;

export function HomeFooter() {
  return (
    <footer className="bg-zinc-900 py-14 text-zinc-300 md:py-16">
      <HomeContainer>
        <div className="grid gap-10 md:grid-cols-4 md:gap-12">
          <div className="space-y-4">
            <Link href="/" aria-label="בית Bari" className="inline-flex w-fit">
              <BariBrandLogo surface="dark" />
            </Link>
            <p className="text-sm leading-relaxed text-zinc-400">המדריך הישראלי החכם למזון — השוואות, דירוגים ומדריכים.</p>
          </div>

          <div>
            <h4 className="mb-4 font-semibold text-white">תוכן</h4>
            <nav className="flex flex-col gap-2 text-sm">
              {footerLinks.content.map((l) => (
                <Link key={l.label} href={l.href} className="text-zinc-400 transition hover:text-emerald-400">
                  {l.label}
                </Link>
              ))}
            </nav>
          </div>

          <div>
            <h4 className="mb-4 font-semibold text-white">על Bari</h4>
            <nav className="flex flex-col gap-2 text-sm">
              {footerLinks.about.map((l) => (
                <Link key={l.label} href={l.href} className="text-zinc-400 transition hover:text-emerald-400">
                  {l.label}
                </Link>
              ))}
            </nav>
          </div>

          <div>
            <h4 className="mb-4 font-semibold text-white">משפטי</h4>
            <nav className="flex flex-col gap-2 text-sm">
              {footerLinks.legal.map((l) => (
                <a key={l.label} href={l.href} className="text-zinc-400 transition hover:text-emerald-400">
                  {l.label}
                </a>
              ))}
            </nav>
          </div>
        </div>

        <Separator className="my-8 bg-zinc-800" />

        <p className="text-center text-sm text-zinc-500">© {new Date().getFullYear()} Bari. כל הזכויות שמורות.</p>
      </HomeContainer>
    </footer>
  );
}
