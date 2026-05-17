import { NewsletterIcon, NewsletterSignup } from "./newsletter-signup";
import { HomeContainer } from "./section-frame";

export function HomeNewsletter() {
  return (
    <section className="relative overflow-hidden py-20 md:py-24" id="newsletter">
      <div
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_50%_20%,rgba(16,185,129,0.11),transparent_34%)]"
        aria-hidden
      />
      <HomeContainer className="max-w-4xl">
        <div className="relative overflow-hidden rounded-[2rem] border border-emerald-300/10 bg-white/[0.045] p-10 text-center text-white shadow-[0_36px_120px_-74px_rgba(0,0,0,0.95)] backdrop-blur-xl md:p-12">
          <div
            className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_70%_20%,rgba(16,185,129,0.12),transparent_34%),linear-gradient(180deg,rgba(255,255,255,0.055),transparent_58%)]"
            aria-hidden
          />
          <div className="relative z-10">
          <NewsletterIcon />
          <div className="mx-auto mb-10 max-w-3xl text-center">
            <p className="text-xs font-bold uppercase tracking-[0.22em] text-emerald-200/80">Bari intelligence updates</p>
            <h2 className="mt-3 text-balance text-3xl font-extrabold tracking-[-0.045em] text-white md:text-5xl">
              הצטרפו לקהילה שבוחרת טוב יותר
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-base leading-relaxed text-zinc-400 md:text-lg">
              ניתוחים, דירוגים והשוואות מזון ישירות למייל.
            </p>
          </div>
          <NewsletterSignup />
          <p className="text-sm text-zinc-500">ללא ספאם. ביטול בכל עת.</p>
          </div>
        </div>
      </HomeContainer>
    </section>
  );
}
