# Bari Third-Party Skill Activation Guide

**Status:** Wave 2 complete — 14 skills installed, agent assignments mapped (TASK-049C)
**Last updated:** 2026-05-31
**Owner:** Frontend Architect

This guide documents when each approved third-party skill should activate, how it maps to Bari workflows, example prompts, overlaps, and exclusion zones.

> Note: Entries marked SOURCE_REQUIRED still have inferred activation triggers. All INSTALLED entries have confirmed triggers from source content.

---

## Bari Agent → Skill Assignment Map

| Bari Agent | Assigned Skills |
|---|---|
| **Frontend Architect** | `frontend-design`, `web-design-guidelines`, `react-best-practices`, `composition-patterns`, `webapp-testing` |
| **Design Director** | `frontend-design`, `web-design-guidelines`, `ui-ux-pro-max` |
| **Research Analyst** | `content-research-writer`, `file-document-processing`, `marketing/content-strategy`, `marketing/seo-audit` |
| **Head of Product** | `marketing/copywriting`, `marketing/marketing-ideas`, `marketing/content-strategy`, `content-research-writer` |
| **QA & Audit Lead** | `webapp-testing`, `file-document-processing` |
| **Chief Nutrition Officer** | `content-research-writer`, `file-document-processing` |
| **All agents** | `skill-creator` (meta-skill), `find-skills` (discovery) |

---

## 1. Anthropic Frontend Design

**When it should activate:**
- Building UI components that should follow Anthropic's design conventions
- Reviewing frontend code for design system compliance

**Bari use cases:**
- Informing the Bari design system with established accessibility and visual patterns
- Cross-referencing Bari component decisions against Anthropic's documented design rationale

**Example prompts:**
- "Review this component against Anthropic's frontend design guidelines."
- "Does this button pattern follow Anthropic's design conventions?"

**Overlap with other skills:**
- Overlaps with `bari-frontend-ui` — if both activate, `bari-frontend-ui` takes precedence for Bari-specific rules; this skill provides supplementary design rationale

**Do NOT use when:**
- Building purely data/pipeline work
- The task has no UI component
- Source is not yet verified (SOURCE_REQUIRED status)

---

## 2. Vercel Web Design Guidelines

**When it should activate:**
- Designing page layouts for the Bari website
- Evaluating visual hierarchy and spacing decisions
- Choosing typography or color system conventions

**Bari use cases:**
- Applying proven web design patterns from Vercel's documented conventions to Bari comparison pages
- Validating that Bari's layout choices align with modern web standards

**Example prompts:**
- "Apply Vercel's web design guidelines to this comparison page layout."
- "Does this page structure follow Vercel's design conventions?"

**Overlap with other skills:**
- Overlaps with `bari-frontend-ui` (Bari-specific) and Anthropic Frontend Design (design patterns)
- If conflict: `bari-frontend-ui` > Vercel Web Design > Anthropic Frontend Design for Bari-specific decisions

**Do NOT use when:**
- Working on backend, pipeline, or scoring tasks
- Source is not yet verified

---

## 3. Vercel React Best Practices

**When it should activate:**
- Writing React components for the Bari website
- Implementing data fetching in a Next.js or React Server Components context
- Reviewing React code for performance or pattern issues

**Bari use cases:**
- Enforcing RSC patterns on Bari comparison pages
- Guiding data fetching strategy for category and product data
- Code review of React component structure

**Example prompts:**
- "Review this React component for Vercel best practices."
- "How should I fetch category data in this RSC context?"
- "Refactor this component to follow Vercel's React patterns."

**Overlap with other skills:**
- Overlaps with Vercel Composition Patterns — composition is a subset of React best practices; use both together
- Overlaps with `bari-frontend-ui` for component structure

**Do NOT use when:**
- Working on non-React parts of the stack
- Source is not yet verified

---

## 4. Vercel Composition Patterns

**When it should activate:**
- Designing how components compose together
- Deciding between component patterns (compound components, render props, slots)
- Reviewing component API design

**Bari use cases:**
- Designing the composition of the comparison drawer, filter panel, and product grid
- Ensuring reusable Bari components follow composable patterns

**Example prompts:**
- "How should the filter panel and product grid compose in this layout?"
- "Review the composition pattern for the comparison drawer component."

**Overlap with other skills:**
- High overlap with Vercel React Best Practices — use together; this skill focuses specifically on composition
- Overlaps with `bari-frontend-ui` component consistency rules

**Do NOT use when:**
- Source is not yet verified

---

## 5. UI/UX Pro Max

**When it should activate:**
- Deep UX analysis of user flows
- Evaluating interaction design quality beyond basic accessibility
- Proposing UX improvements to existing features

**Bari use cases:**
- Evaluating the comparison flow from product discovery to decision
- Identifying UX friction in the filter panel or comparison drawer

**Example prompts:**
- "Analyze the UX of the comparison flow for friction points."
- "What UX improvements would you recommend for the filter panel?"

**Overlap with other skills:**
- Overlaps with `bari-frontend-ui` — this skill adds UX depth; `bari-frontend-ui` enforces Bari rules
- Overlaps with Anthropic Frontend Design for design principles

**Do NOT use when:**
- Task is purely technical implementation with no UX dimension
- Source is not yet verified
- Community origin requires extra scrutiny — review source content before first use

---

## 6. Vercel React Native Skills

**When it should activate:**
- If Bari ever builds a React Native mobile application

**Bari use cases:**
- Currently none — Bari is a web-only platform
- Reserved for a future mobile track if one is initiated

**Example prompts:**
- N/A for current Bari scope

**Overlap with other skills:**
- No overlap with current Bari skill set

**Do NOT use when:**
- Any task on the current Bari web platform
- Source is not yet verified
- **Recommend deferring this installation until a mobile track is formally initiated**

---

## 7. Superpowers

**When it should activate:**
- Unknown — skill name is too generic to infer activation without source content

**Bari use cases:**
- Unknown until source is reviewed

**Example prompts:**
- Cannot recommend prompts for an unverified skill

**Overlap with other skills:**
- Unknown

**Do NOT use when:**
- Source is not verified — this skill is BLOCKED from use until source content is reviewed
- This skill requires the highest priority security review due to its vague name and unknown scope

---

## 8. Using Git Worktrees

**When it should activate:**
- User wants to work on a feature branch in isolation without affecting the main working tree
- User wants to run two branches side by side
- User asks to "create a worktree" or "work in parallel on branches"

**Bari use cases:**
- Working on a category pipeline change while keeping main branch clean
- Running a QA validation on one branch while developing on another
- Isolating a risky BSIP2 scoring change for review

**Example prompts:**
- "Create a worktree for the air-purifier category work."
- "Set up a parallel branch so I can test the scoring change without touching main."

**Overlap with other skills:**
- No direct overlap with Bari-specific skills
- Note: Claude Code has built-in `EnterWorktree`/`ExitWorktree` native support — confirm this skill adds meaningful guidance beyond native behavior

**Do NOT use when:**
- Source is not yet verified
- The task does not require branch isolation

---

## 9. Tapestry

**When it should activate:**
- Unknown — "Tapestry" is ambiguous without source clarification

**Bari use cases:**
- Cannot determine without knowing what Tapestry refers to

**Example prompts:**
- Cannot recommend until clarified

**Overlap with other skills:**
- Unknown

**Do NOT use when:**
- Source and purpose are not clarified
- **Action required:** Owner must clarify what "Tapestry" refers to before this skill can be evaluated

---

## 10. Content Research Writer

**When it should activate:**
- Writing category descriptions, product summaries, or comparison page copy
- Researching a product category before writing content about it
- Drafting SEO-oriented content for Bari category pages

**Bari use cases:**
- Writing the introductory copy for new category pages
- Researching what attributes matter to consumers in a new category
- Drafting comparison criteria descriptions

**Example prompts:**
- "Research and write a category description for air purifiers on Bari."
- "Draft comparison criteria descriptions for the baby monitor category."

**Overlap with other skills:**
- Overlaps with `bari-category-factory` for category setup tasks — use Content Research Writer for copy, `bari-category-factory` for pipeline
- Overlaps with Marketing Skills for promotional copy

**Do NOT use when:**
- Source is not yet verified
- Task is technical pipeline work with no content output

---

## 11. Firecrawl (MCP Server)

**When it should activate:**
- Scraping competitor product data for category research
- Crawling a manufacturer's website to extract product attributes
- Fetching structured data from web pages for enrichment

**Bari use cases:**
- Seeding a new category corpus with product data crawled from retail sites
- Researching attribute patterns on competitor comparison platforms
- Extracting product specifications from manufacturer pages

**Example prompts:**
- "Crawl this product page and extract specifications."
- "Scrape the top 20 products from this category URL."

**Overlap with other skills:**
- Works alongside `bari-category-factory` — Firecrawl feeds the corpus, factory processes it
- Works alongside Content Research Writer — Firecrawl fetches data, writer produces content

**Do NOT use when:**
- Crawling sites that prohibit scraping in their ToS without legal review
- API key is not configured
- Task does not require web data — do not use for tasks already covered by existing Bari data

**Configuration required:** See `skill_registry.md` for MCP setup instructions.

---

## 12. Webapp Testing

**When it should activate:**
- Running end-to-end or integration tests on the Bari website
- Validating that a UI change did not break existing functionality
- Automating QA validation of frontend behavior

**Bari use cases:**
- Testing comparison page rendering after a category packaging update
- Validating RTL layout correctness in an automated test run
- Running regression tests after a frontend component change

**Example prompts:**
- "Run webapp tests against the comparison page for refrigerators."
- "Test that the filter panel works correctly after the RTL fix."

**Overlap with other skills:**
- Overlaps with `bari-qa-audit` for QA validation — `bari-qa-audit` covers data/pipeline QA; this skill covers frontend/webapp testing
- They are complementary, not redundant

**Do NOT use when:**
- Source is not yet verified
- Running tests against production without explicit approval
- Task is pipeline or data work, not frontend behavior

---

## 13. Skill Creator

**When it should activate:**
- Building a new Bari-specific skill
- Documenting a recurring workflow that should be encoded as a skill
- Reviewing an existing skill for completeness

**Bari use cases:**
- Creating future Bari v2 skills (BSIP3 readiness, internationalization, etc.)
- Encoding new pipeline steps as skills as the Bari architecture evolves

**Example prompts:**
- "Create a skill for the Bari internationalization workflow."
- "Help me write a SKILL.md for the BSIP3 readiness check."

**Overlap with other skills:**
- Meta-skill — no direct overlap with domain skills
- Any skill produced by this skill must go through the same security review as any other third-party skill

**Do NOT use when:**
- Source is not yet verified
- Creating a skill to bypass an existing Bari governance rule
- Skills created must be reviewed by the skill's designated owner before use

---

## 14. Supermemory (MCP Server)

**When it should activate:**
- Persisting context across Claude Code sessions for long-running Bari work
- Storing category research notes that need to survive session resets
- Building a shared memory layer across team members

**Bari use cases:**
- Remembering category pipeline progress across multiple sessions
- Storing category-specific scoring rationale for reference in future sessions

**Example prompts:**
- "Save this category research to supermemory for the next session."
- "Recall what we decided about the air purifier scoring weights."

**Overlap with other skills:**
- Complements all other skills by providing cross-session persistence
- Does not overlap functionally with any Bari domain skill

**Do NOT use when:**
- Storing sensitive Bari business data without confirming data residency policy
- API key is not configured
- Storing BSIP scoring decisions — those belong in the evidence registry, not external memory

**Configuration required:** See `skill_registry.md` for MCP setup instructions.

---

## 15. File / PDF Document Processing ✅ INSTALLED

**Assigned to:** Research Analyst, QA & Audit Lead, Chief Nutrition Officer

**When it should activate:**
- Extracting text or tables from PDF documents
- Merging, splitting, or rotating PDF files
- Creating PDFs programmatically
- OCR of scanned documents
- Filling PDF forms

**Bari use cases:**
- Ingesting manufacturer product spec sheets (PDF) into the corpus pipeline
- Extracting attribute tables from comparison PDFs
- Processing bulk product data exports
- Generating PDF reports from Bari data

**Example prompts:**
- "Extract the product specifications table from this manufacturer PDF."
- "Merge these three product data PDFs into one."
- "OCR this scanned product catalog and extract all text."
- "Create a PDF report from this category enrichment data."

**Overlap with other skills:**
- Works alongside `bari-category-factory` for corpus preparation (Firecrawl fetches, this skill processes the files)
- Works alongside `content-research-writer` for summarizing document content after extraction

**Do NOT use when:**
- Writing output files outside the Bari project directory
- Task does not involve PDF or document processing

---

## 16. Marketing Skills ✅ INSTALLED (4 subskills)

### 16a. Copywriting

**Assigned to:** Head of Product

**When it should activate:**
- Writing or rewriting any page copy
- Headlines, CTAs, value propositions, hero sections
- Any text that needs to persuade or convert

**Bari use cases:**
- Launch copy for new Bari category pages
- Writing the Bari value proposition and homepage copy
- Crafting CTAs for comparison page calls-to-action

**Example prompts:**
- "Write the hero copy for the Bari homepage."
- "Rewrite this category page headline — it's too generic."
- "Give me 3 CTA button options for the comparison drawer."

**Overlap with other skills:**
- `content-research-writer` — research first with that skill, then write copy with this one
- `bari-frontend-ui` — for on-site copy format requirements; for marketing copy language, use this skill
- Distinct from `marketing/content-strategy` — strategy decides what to write; this skill writes it

**Do NOT use when:**
- Hebrew website copy — requires category team review after generation
- Task involves technical pipeline or scoring work

### 16b. Marketing Ideas

**Assigned to:** Head of Product

**When it should activate:**
- Brainstorming growth tactics
- Stuck on how to grow or promote Bari
- Exploring new marketing channels

**Bari use cases:**
- Planning Bari's go-to-market for new categories
- Exploring growth tactics for the Israeli consumer market
- Identifying programmatic SEO opportunities for category expansion

**Example prompts:**
- "What marketing ideas would work for Bari's baby monitor category launch?"
- "Give me 5 low-budget growth ideas for the Bari comparison platform."
- "Brainstorm marketing strategies for reaching Israeli first-time parents."

**Overlap with other skills:**
- `marketing/content-strategy` — use Ideas for discovery, Strategy for planning
- `marketing/copywriting` — Ideas tells you what channels; Copywriting executes the copy

**Do NOT use when:**
- Task is technical pipeline, scoring, or frontend implementation
- You need execution — these are idea seeds, not finished plans

### 16c. Content Strategy

**Assigned to:** Head of Product, Research Analyst

**When it should activate:**
- Planning what content to create for Bari
- Deciding which categories need supporting content
- Building content pillars and topic clusters
- Planning the editorial calendar

**Bari use cases:**
- Building a content pillar around each Bari product category
- Identifying Hebrew-language keyword opportunities for category pages
- Planning content to support new category launches in the BSIP pipeline

**Example prompts:**
- "Help me plan a content strategy for Bari's air purifier category."
- "What content pillars should Bari build around home appliances?"
- "Which blog topics would drive traffic to the refrigerator comparison page?"

**Overlap with other skills:**
- `marketing/seo-audit` — Strategy plans content; SEO Audit diagnoses technical issues
- `content-research-writer` — Strategy plans what to write; that skill writes it
- `bari-category-factory` — Content strategy should align with pipeline-approved categories

**Do NOT use when:**
- Executing writing (use `content-research-writer` for that)
- Technical pipeline or scoring tasks

### 16d. SEO Audit

**Assigned to:** Head of Product, Research Analyst

**When it should activate:**
- Auditing Bari's SEO health
- Diagnosing ranking or traffic issues
- Reviewing hreflang configuration for Hebrew locale
- Core Web Vitals analysis

**Bari use cases:**
- Auditing hreflang for Bari's Hebrew (`he`) locale
- Diagnosing why category pages are not ranking
- Core Web Vitals audit for comparison pages
- Crawlability check after a site migration or structural change

**Example prompts:**
- "Audit Bari's SEO — why aren't the category pages ranking?"
- "Review the hreflang configuration for the Hebrew locale."
- "Check the Core Web Vitals for the comparison page."
- "We migrated the site — audit the crawl and index status."

**Overlap with other skills:**
- `marketing/content-strategy` — SEO Audit finds technical gaps; Content Strategy plans what to create to fill them
- `web-design-guidelines` — complementary: design guidelines + SEO audit together cover both UX and SEO quality

**Do NOT use when:**
- Task is about content planning (use `content-strategy`)
- Task is about writing copy (use `copywriting` or `content-research-writer`)

---

## Wave 2 New Skills (TASK-049C additions)

### Webapp Testing ✅ INSTALLED

**Assigned to:** Frontend Architect, QA & Audit Lead

**When it should activate:**
- Writing or running E2E tests for the Bari website
- Automating browser interactions
- Visual regression testing
- API mocking for test environments

**Bari use cases:**
- E2E tests for comparison page flows (filter → select → compare)
- RTL layout tests for Hebrew locale using browser automation
- Visual regression after a comparison drawer component change
- Mocking category API responses in test environments

**Example prompts:**
- "Write a Playwright E2E test for the Bari comparison flow."
- "Test the filter panel in Hebrew RTL mode using mobile emulation."
- "Set up visual regression tests for the comparison drawer."
- "Mock the product API and test the empty state behavior."

**Overlap with other skills:**
- `bari-qa-audit` — `bari-qa-audit` covers data/pipeline QA; this skill covers frontend/browser testing. Complementary.
- `web-design-guidelines` — design review before testing; this skill automates validation after

**Do NOT use when:**
- Running tests against production without explicit approval
- Pipeline or data QA tasks (use `bari-qa-audit`)

### Skill Creator ✅ INSTALLED

**Assigned to:** All agents (meta-skill)

**When it should activate:**
- Creating a new Bari internal skill
- Writing a SKILL.md file
- Reviewing or improving an existing skill's structure
- Learning best practices for skill authoring

**Bari use cases:**
- Creating new Bari pipeline skills (e.g., `bari-bsip3-readiness`)
- Improving descriptions and trigger phrases on existing skills
- Encoding new Bari workflows as reusable skills

**Example prompts:**
- "Create a skill for the Bari internationalization workflow."
- "Help me write a SKILL.md for the BSIP3 readiness check."
- "Improve the trigger description on the `bari-qa-audit` skill."

**Overlap with other skills:**
- No domain overlap — meta-skill for creating other skills

**Do NOT use when:**
- Creating a skill to bypass an existing Bari governance rule
- Skills created must be reviewed by the designated owner

---

## Priority Tier Classification (Updated TASK-049C)

Based on the Bari product roadmap, current workflow needs, and agent assignments:

### High-frequency (expect daily use)

| Skill | Assigned Agent | Reason |
|---|---|---|
| `react-best-practices` | Frontend Architect | Every React/Next.js frontend task |
| `composition-patterns` | Frontend Architect | Component design is ongoing |
| `webapp-testing` | Frontend Architect, QA Lead | Every frontend change needs E2E validation |
| `content-research-writer` | Research Analyst, Head of Product, CNO | Every new category needs copy and research |
| `file-document-processing` | Research Analyst, QA Lead, CNO | Corpus ingestion from PDFs is routine |

### Medium-frequency (weekly or per-initiative use)

| Skill | Assigned Agent | Reason |
|---|---|---|
| `web-design-guidelines` | Frontend Architect, Design Director | During layout and design review cycles |
| `frontend-design` | Frontend Architect, Design Director | During design review and new component builds |
| `ui-ux-pro-max` | Design Director | UX audits and flow reviews |
| `marketing/content-strategy` | Head of Product, Research Analyst | Per new category launch or marketing initiative |
| `marketing/copywriting` | Head of Product | Per category launch or campaign |
| `marketing/seo-audit` | Head of Product, Research Analyst | Per site audit or traffic issue investigation |
| `marketing/marketing-ideas` | Head of Product | Per planning cycle |
| `skill-creator` | All agents | When encoding new Bari workflows as skills |
| `find-skills` | All agents | When discovering new third-party skills |

### Rarely-used (situational)

| Skill | Assigned Agent | Reason |
|---|---|---|
| `supermemory` (MCP — not installed) | — | Useful for long-running research; pending MCP config + data policy |
| Firecrawl (MCP — not installed) | — | Used during corpus seeding; pending MCP config |
| Vercel React Native Skills | — | No current mobile track — defer installation |
| Superpowers | — | Unknown purpose — BLOCKED pending review |
| Tapestry | — | Unknown purpose — BLOCKED pending clarification |
| Git Worktrees | — | SOURCE_REQUIRED — no verified source provided yet |
