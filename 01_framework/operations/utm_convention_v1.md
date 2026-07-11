# UTM Convention v1 (social posting)

Owner: Frontend Agent (measurement infra) / Marketing Agent (posting practice).
Scope: every outbound link posted from a Bari-controlled social account
(Facebook, Instagram, WhatsApp). Purpose: make GA4 acquisition reports able to
attribute a session to the actual post that drove it, instead of collapsing
everything into `(direct)` or `(referral)`.

## The rule

Every social link carries three UTM parameters:

| Parameter | Value | Notes |
|---|---|---|
| `utm_source` | `facebook` \| `instagram` \| `whatsapp` | The platform the click came from. Lowercase, no spaces. |
| `utm_medium` | `social` (organic post) or `paid_social` (boosted/ad) | Distinguishes organic reach from paid spend. |
| `utm_campaign` | `<post-slug>-<YYYYMMDD>` | A short kebab-case slug describing the post, plus the publish date. e.g. `magnesium-guide-20260710`. One slug per distinct post/creative, reused across platforms if the same creative runs on more than one. |

Do not add `utm_content` or `utm_term` unless a specific A/B test needs it —
the three params above are the floor for every link, not a menu.

## Deep-link, don't home-link

Every social link points at the **specific comparison or guide page** the
post is about (`/hashvaot/<category-slug>`), never the homepage. A post about
the magnesium guide links to `/hashvaot/magnesium`, not `/`. The whole point
of the post is to shorten the path from "saw the claim" to "read Bari's
evidence" — a homepage link forces the reader to re-navigate and loses most
of the click-through. (If a dedicated `/madrichim/` guides section is live by
the time you post, deep-link into that instead — same rule, different path
prefix.)

## Example URLs (bari.digital)

```
https://bari.digital/hashvaot/brined-cheeses?utm_source=facebook&utm_medium=social&utm_campaign=brined-cheese-launch-20260708

https://bari.digital/hashvaot/magnesium?utm_source=instagram&utm_medium=social&utm_campaign=magnesium-guide-20260710

https://bari.digital/hashvaot/yogurt?utm_source=whatsapp&utm_medium=social&utm_campaign=yogurt-fat-quality-20260712
```

A boosted (paid) version of the same creative:

```
https://bari.digital/hashvaot/brined-cheeses?utm_source=facebook&utm_medium=paid_social&utm_campaign=brined-cheese-launch-20260708
```

## Why this exists

GA4 is consent-gated (strict opt-in, PPA Feb-2026 posture — see
`ga4-script.tsx`), so it undercounts total traffic, but for the subset of
sessions it does see, UTM-tagged links are the only way to tell "the
magnesium guide post worked" from "someone typed the URL in." Vercel Web
Analytics (the cookieless topline counter) does not do source attribution —
it counts page views, not campaigns — so UTM tagging is a GA4-side practice
specifically, and complements rather than duplicates the Vercel number.
