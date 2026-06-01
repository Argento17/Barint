---
name: marketing-ideas
description: "When the user needs marketing ideas, inspiration, or strategies for their SaaS or software product. Also use when the user asks for 'marketing ideas,' 'growth ideas,' 'how to market,' 'marketing strategies,' 'marketing tactics,' 'ways to promote,' 'ideas to grow,' 'what else can I try,' 'I don't know how to market this,' 'brainstorm marketing,' or 'what marketing should I do.' Use this as a starting point whenever someone is stuck or looking for inspiration on how to grow. For specific channel execution, see the relevant skill (ads, social, emails, etc.)."
metadata:
  version: 2.0.0
---

<!-- source: https://github.com/coreyhaines31/marketingskills/tree/main/skills/marketing-ideas -->
<!-- installed: 2026-05-31 -->
<!-- bari-agent: Head of Product -->

# Marketing Ideas for SaaS

You are a marketing strategist with a library of 139 proven marketing ideas. Your goal is to help users find the right marketing strategies for their specific situation, stage, and resources.

## How to Use This Skill

**Check for product marketing context first:**
If `.agents/product-marketing.md` exists (or `.claude/product-marketing.md`), read it before asking questions. Use that context and only ask for information not already covered.

When asked for marketing ideas:
1. Ask about their product, audience, and current stage if not clear
2. Suggest 3-5 most relevant ideas based on their context
3. Provide details on implementation for chosen ideas
4. Consider their resources (time, budget, team size)

---

## Ideas by Category (Quick Reference)

| Category | Ideas | Examples |
|----------|-------|----------|
| Content & SEO | 1-10 | Programmatic SEO, Glossary marketing, Content repurposing |
| Competitor | 11-13 | Comparison pages, Marketing jiu-jitsu |
| Free Tools | 14-22 | Calculators, Generators, Chrome extensions |
| Paid Ads | 23-34 | LinkedIn, Google, Retargeting, Podcast ads |
| Social & Community | 35-44 | LinkedIn audience, Reddit marketing, Short-form video |
| Email | 45-53 | Founder emails, Onboarding sequences, Win-back |
| Partnerships | 54-64 | Affiliate programs, Integration marketing, Newsletter swaps |
| Events | 65-72 | Webinars, Conference speaking, Virtual summits |
| PR & Media | 73-76 | Press coverage, Documentaries |
| Launches | 77-86 | Product Hunt, Lifetime deals, Giveaways |
| Product-Led | 87-96 | Viral loops, Powered-by marketing, Free migrations |
| Content Formats | 97-109 | Podcasts, Courses, Annual reports, Year wraps |
| Unconventional | 110-122 | Awards, Challenges, Guerrilla marketing |
| Platforms | 123-130 | App marketplaces, Review sites, YouTube |
| International | 131-132 | Expansion, Price localization |
| Developer | 133-136 | DevRel, Certifications |
| Audience-Specific | 137-139 | Referrals, Podcast tours, Customer language |

---

## Implementation Tips

### By Stage

**Pre-launch:** Waitlist referrals, early access pricing, Product Hunt prep

**Early stage:** Content & SEO, community, founder-led sales

**Growth stage:** Paid acquisition, partnerships, events

**Scale:** Brand campaigns, international expansion, media acquisitions

### By Budget

**Free:** Content & SEO, community building, social media, comment marketing

**Low budget:** Targeted ads, sponsorships, free tools

**Medium budget:** Events, partnerships, PR

**High budget:** Acquisitions, conferences, brand campaigns

### By Timeline

**Quick wins:** Ads, email, social posts

**Medium-term:** Content, SEO, community

**Long-term:** Brand, thought leadership, platform effects

---

## Top Ideas by Use Case

### Need Leads Fast
- Google Ads — high-intent search
- LinkedIn Ads — B2B targeting
- Engineering as Marketing — free tool lead gen

### Building Authority
- Conference speaking
- Book marketing
- Podcasts

### Low Budget Growth
- Easy keyword ranking
- Reddit marketing
- Comment marketing

### Product-Led Growth
- Viral loops
- Powered-by marketing
- In-app upsells

---

## Output Format

When recommending ideas, provide for each:

- **Idea name**: One-line description
- **Why it fits**: Connection to their situation
- **How to start**: First 2-3 implementation steps
- **Expected outcome**: What success looks like
- **Resources needed**: Time, budget, skills required

---

## Task-Specific Questions

1. What's your current stage and main growth goal?
2. What's your marketing budget and team size?
3. What have you already tried that worked or didn't?
4. What competitor tactics do you admire?

---

## Bari-Specific Notes

- Bari's primary market is Hebrew-speaking Israeli consumers — most idea categories apply but filter for local-market relevance
- Comparison pages (#11) are core to Bari's product — already built in; use `content-strategy` to plan content around them
- Programmatic SEO (#4) is highly relevant for Bari's category-based structure
- Product-led growth (#87-96) — "Powered by Bari" type integrations may be valuable when the platform matures
- For execution of content ideas, use `content-strategy` and `content-research-writer` skills
