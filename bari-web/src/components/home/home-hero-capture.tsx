import { NewsletterSignup } from "./newsletter-signup";
import { HomeContainer } from "./section-frame";

/**
 * Above-the-fold email capture, placed directly under the hero for
 * ad-landing traffic (homepage is the primary social-ad destination — see
 * HomeHero). The existing newsletter capture (HomeNewsletter, id="newsletter")
 * sits several sections down the page and is easy to miss for a visitor who
 * doesn't scroll.
 *
 * Reuses the canonical NewsletterSignup component and copy strings verbatim
 * from the existing /newsletter page (src/app/newsletter/page.tsx) — no new
 * marketing copy is introduced here, so this does not require Content/QA
 * sign-off. source="hero" keeps submissions from this placement attributable
 * separately from source="homepage" (HomeNewsletter) and source="newsletter_page".
 */
export function HomeHeroCapture() {
  return (
    <section className="border-y border-black/[0.06] bg-[#F7F7F2] py-10 md:py-12">
      <HomeContainer className="max-w-xl text-center">
        <p className="text-xs font-bold tracking-[0.16em] text-[#167A58]">
          הניוזלטר של Bari
        </p>
        <h2 className="mt-3 text-balance text-xl font-extrabold tracking-[-0.045em] text-[#111318] md:text-2xl">
          הצטרפו לניוזלטר של Bari
        </h2>
        <p className="mx-auto mt-3 max-w-md text-sm leading-relaxed text-[#4E5663]">
          ניתוחים, דירוגים והשוואות מזון ישירות למייל, בלי לעזוב את הקו העריכתי של Bari.
        </p>
        <div className="mt-6">
          <NewsletterSignup source="hero" />
        </div>
        <p className="text-sm text-[#5E6560]">ללא ספאם. ביטול בכל עת.</p>
      </HomeContainer>
    </section>
  );
}
