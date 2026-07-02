import Image from "next/image";

import { NewsletterSignup } from "./newsletter-signup";
import { HomeContainer } from "./section-frame";

export function HomeNewsletter() {
  return (
    <section className="relative overflow-hidden bg-[#F7F7F2] py-20 md:py-24" id="newsletter">
      <div
        className="pointer-events-none absolute inset-0 bg-transparent"
        aria-hidden
      />
      <HomeContainer className="max-w-5xl">
        <div className="relative overflow-hidden rounded-[1.35rem] border border-black/8 bg-white p-10 text-center text-[#111318] shadow-[0_32px_100px_-60px_rgba(17,19,24,0.35)] md:p-14">
          <div
            className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_70%_20%,rgba(47,174,130,0.025),transparent_36%),linear-gradient(180deg,rgba(255,255,255,0.025),transparent_58%)]"
            aria-hidden
          />
          <div className="relative z-10">
          {/* NORI — the Ingredient Expert, reading BARI NEWS. Small transparent emblem. */}
          <Image
            src="/mascots/nori-newsletter.png"
            alt=""
            width={760}
            height={678}
            className="pointer-events-none mx-auto mb-4 h-auto w-44 md:w-52"
            aria-hidden
          />
          <div className="mx-auto mb-10 max-w-3xl text-center">
            <p className="text-xs font-bold uppercase tracking-[0.22em] text-[#167A58]">Bari intelligence updates</p>
            <h2 className="mt-3 text-balance text-3xl font-extrabold tracking-[-0.045em] text-[#111318] md:text-5xl">
              הצטרפו לקהילה שבוחרת טוב יותר
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-base leading-relaxed text-[#4E5663] md:text-lg">
              ניתוחים, דירוגים והשוואות מזון ישירות למייל.
            </p>
          </div>
          <NewsletterSignup source="homepage" />
          <p className="text-sm text-[#5E6560]">ללא ספאם. ביטול בכל עת.</p>
          </div>
        </div>
      </HomeContainer>
    </section>
  );
}
