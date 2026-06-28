import homepageMarketingJson from "@/data/site-content/homepage-marketing.json";

export const homepageMarketing = homepageMarketingJson as {
  hero: { badgeLink: string };
  heroTrust: string[];
  trust: { eyebrow: string; title: string; footnote: string };
  comparisons: { title: string; subtitle: string };
  methodology: { title: string };
};
