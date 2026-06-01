import type { Metadata } from "next";

import { NewsletterIcon, NewsletterSignup } from "@/components/home/newsletter-signup";
import { HomeContainer } from "@/components/home/section-frame";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

export const metadata: Metadata = {
  title: "הניוזלטר של Bari",
  description: "הרשמה לניוזלטר של Bari לקבלת ניתוחים, דירוגים והשוואות מזון ישירות למייל.",
};

export default function NewsletterPage() {
  return (
    <main className={cn("bg-[#F7F7F2] text-[#111318]", siteHeaderOffsetClass)}>
      <section className="relative overflow-hidden py-20 md:py-24">
        <div className="pointer-events-none absolute inset-0 bg-transparent" aria-hidden />
        <HomeContainer className="max-w-4xl">
          <div className="relative overflow-hidden rounded-[2rem] border border-black/[0.08] bg-[#FFFFFF]/68 p-10 text-center shadow-[0_36px_120px_-74px_rgba(17,19,24,0.78)] backdrop-blur-xl md:p-12">
            <div
              className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_70%_20%,rgba(47,174,130,0.025),transparent_36%),linear-gradient(180deg,rgba(255,255,255,0.025),transparent_58%)]"
              aria-hidden
            />
            <div className="relative z-10">
              <NewsletterIcon />
              <div className="mx-auto mb-10 max-w-3xl text-center">
                <p className="text-xs font-bold tracking-[0.16em] text-[#1F8F6A]/80">הניוזלטר של Bari</p>
                <h1 className="mt-3 text-balance text-3xl font-extrabold tracking-[-0.045em] text-[#111318] md:text-5xl">
                  הצטרפו לניוזלטר של Bari
                </h1>
                <p className="mx-auto mt-4 max-w-2xl text-base leading-relaxed text-[#4E5663] md:text-lg">
                  ניתוחים, דירוגים והשוואות מזון ישירות למייל, בלי לעזוב את הקו העריכתי של Bari.
                </p>
              </div>
              <NewsletterSignup source="newsletter_page" />
              <p className="text-sm text-[#7A817C]">ללא ספאם. ביטול בכל עת.</p>
            </div>
          </div>
        </HomeContainer>
      </section>
    </main>
  );
}
