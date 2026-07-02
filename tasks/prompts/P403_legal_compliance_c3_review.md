# P403 / Israeli legal & compliance review for Bari go-live (route: C3)

You are an independent expert reviewer (C3). The orchestrator is consulting you for a second opinion. The site owner is himself a licensed Israeli lawyer — so do NOT give "consult a lawyer" boilerplate. He wants the REGULATIONS and the RISKS, precisely and independently. Return evidence and analysis only; you do not decide or close anything.

## Context
"Bari" (bari.digital) is a Hebrew, consumer-facing EDITORIAL ratings site for food products and dietary supplements (תוספי תזונה), targeting Israeli consumers. It rates/scores named commercial products on a published methodology (nutrition data from direct product label scrapes → an editorial score/grade). No e-commerce, no user accounts, no payments. It runs Google Analytics (GA4). It is about to go live.

## Your task — independently verify, correct, and extend the following first-pass legal map. Where our first pass is wrong, say so and cite the correct authority.

Our first-pass findings (verify each; flag errors, missing obligations, and over/under-statements):

1. **Accessibility** — חוק שוויון זכויות לאנשים עם מוגבלות 1998 + תקנות התאמות נגישות לשירות 2013 (reg' 35) + ת"י 5568 (≈WCAG 2.0 AA). We believe: an accessibility statement (הצהרת נגישות) + actual WCAG 2.0 AA compliance is mandatory; no size exemption applies to a company; plaintiff can sue without proving harm. We found CONFLICTING statutory-damages figures (₪50,000 vs ₪300,000 without proof of damage). Which is correct, and under which section? What exactly must the הצהרת נגישות contain, and is a מתאם נגישות (coordinator) legally required to be named?

2. **Privacy** — חוק הגנת הפרטיות 1981 + תיקון 13 (in force 14 Aug 2025) + תקנות אבטחת מידע 2017. We believe a Hebrew privacy policy is mandatory once GA4 runs (IP + cookies = personal data, cross-border transfer to Google US). Is database registration (רישום מאגר) triggered for an analytics-only site? Is a privacy officer (ממונה הגנת פרטיות) mandatory at small scale? What does תיקון 13 specifically newly require for disclosure/consent, and what are the new penalty ceilings?

3. **Cookies/consent** — Is a consent banner legally MANDATORY in Israel for GA4 (vs the EU ePrivacy regime), or only PPA-guidance/best-practice? What is the minimum legally-defensible posture for an Israeli-only audience?

4. **Supplement & health content** — הוראות בריאות הציבור (מזון)(איסור ייחוס סגולות מרפא למזון) 1978; consumer-protection law 1981; MoH advertising rules. Where is the legal line between (a) permitted editorial/nutritional-fact/comparative claims and (b) prohibited therapeutic/disease claims, for a THIRD-PARTY rater (not the manufacturer)? Does the 1978 prohibition bind an editorial third party, or only advertisers/manufacturers?

5. **Defamation / product disparagement** — חוק איסור לשון הרע 1965 applied to PUBLISHING LOW SCORES / negative verdicts about named commercial products. How strong is the "fair opinion" defense (s.15) and the truth+public-interest defense (s.14) for a methodology-based rating? What is the website-operator notice-and-takedown exposure? What concretely lowers the risk (fact/opinion separation, sourced data, dispute channel)?

## Deliverable
- A corrected, citation-grounded regulation-and-risk map (statute + section + the specific obligation/penalty). Cite real Israeli authorities; if you are unsure of a specific number or section, say "unverified" rather than inventing it (this shop bans fabricated citations).
- Rank the risks by real-world enforcement likelihood × severity for THIS site at launch.
- Name anything our first pass MISSED entirely (e.g. terms-of-use contractual posture, IP/scraping exposure from using retailer product data & images, comparative-advertising law, MoH supplement-registration interplay, minors, English-vs-Hebrew governing text).
- Flag any claim where Israeli law genuinely differs from the common GDPR/US intuition.
