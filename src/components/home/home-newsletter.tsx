import { NewsletterIcon, NewsletterSignup } from "./newsletter-signup";
import { HomeContainer, SectionHeading } from "./section-frame";

export function HomeNewsletter() {
  return (
    <section className="bg-white py-20 md:py-24" id="newsletter">
      <HomeContainer className="max-w-4xl">
        <div className="relative overflow-hidden rounded-3xl border border-zinc-200/60 bg-gradient-to-br from-zinc-50 to-emerald-50/40 p-10 text-center shadow-lg md:p-12">
          <NewsletterIcon />
          <SectionHeading
            title="הצטרפו לקהילה שבוחרת טוב יותר"
            description="קבלו ניתוחים, דירוגים והשוואות ישירות למייל — עדכונים שבועיים על מוצרים ומחקרים חדשים."
          />
          <NewsletterSignup />
          <p className="text-sm text-zinc-600">ללא ספאם. ביטול בכל עת.</p>
        </div>
      </HomeContainer>
    </section>
  );
}
