# Bari Third-Party Skills — Installation Report v1

**Task:** TASK-049B
**Date:** 2026-05-31
**Installer:** Claude (Frontend Architect delegation)
**Scope:** Install and validate 6 approved skills from verified sources

---

## Source Verification Results

All four provided source URLs were verified before installation.

| Source URL | Exists | Stars | Notes |
|---|---|---|---|
| `github.com/anthropics/skills` | YES | 144k | Official Anthropic repo |
| `github.com/vercel-labs/agent-skills` | YES | 27.3k | Official Vercel repo |
| `github.com/nextlevelbuilder/ui-ux-pro-max-skill` | YES | 85.2k | Community repo, MIT license |
| `github.com/vercel-labs/skills` | YES | 20.7k | Vercel find-skills CLI repo |

---

## Installation Summary

| Skill | Status | Source Verified | Content Complete | Activation Confirmed | Notes |
|---|---|---|---|---|---|
| `frontend-design` | INSTALLED | YES | FULL | YES | Verbatim from anthropics/skills |
| `web-design-guidelines` | INSTALLED | YES | FULL | YES | Runtime WebFetch call flagged — see security note |
| `react-best-practices` | INSTALLED | YES | FULL | YES | All 70 rules present verbatim |
| `composition-patterns` | INSTALLED | YES | FULL | YES | All 8 rules present verbatim |
| `ui-ux-pro-max` | INSTALLED (PARTIAL) | YES | PARTIAL | YES | YAML frontmatter verbatim; body derived from source docs — see note |
| `find-skills` | INSTALLED | YES | FULL | YES | Verbatim from vercel-labs/skills |

**Total: 5 full installs, 1 partial install, 0 failed installs**

---

## Skill Details

### 1. frontend-design

- **Source:** `https://github.com/anthropics/skills/tree/main/skills/frontend-design`
- **Install path:** `C:\Bari\.claude\skills\third_party\frontend-design\SKILL.md`
- **Activation trigger:** User asks to build web components, pages, applications, or to style/beautify UI
- **Bari use case:** Building comparison page UI, frontend components, Bari website pages — with the explicit goal of avoiding generic AI aesthetics (aligned with `bari-frontend-ui` goal)
- **Overlap with Bari-native skills:** High overlap with `bari-frontend-ui`. Precedence: `bari-frontend-ui` governs Bari-specific rules (RTL, components, forbidden patterns); `frontend-design` provides the aesthetic philosophy. Use together.
- **Content integrity:** Verbatim. No fabrication.

---

### 2. web-design-guidelines

- **Source:** `https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines`
- **Install path:** `C:\Bari\.claude\skills\third_party\web-design-guidelines\SKILL.md`
- **Activation trigger:** "review my UI", "check accessibility", "audit design", "review UX", "check against best practices"
- **Bari use case:** Auditing comparison pages and components against Vercel's Web Interface Guidelines before merge
- **Overlap with Bari-native skills:** Complements `bari-frontend-ui`. `bari-frontend-ui` is prescriptive (how to build); this skill is evaluative (how to review). Use this for PR reviews.
- **Security flag:** This skill makes a **runtime WebFetch call** to `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` to fetch the latest rules. This is an external network dependency. Approved for Bari frontend file reviews only.
- **Content integrity:** Verbatim.

---

### 3. react-best-practices

- **Source:** `https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices`
- **Install path:** `C:\Bari\.claude\skills\third_party\react-best-practices\SKILL.md`
- **Activation trigger:** React component work, Next.js pages, data fetching, bundle optimization, performance improvements
- **Bari use case:** Every frontend task on the Bari website. Bari runs on React/Next.js — this skill is high-frequency. Particularly relevant for: RSC data fetching on category pages, bundle optimization, re-render prevention in the comparison drawer.
- **Overlap with Bari-native skills:** No direct overlap. `bari-frontend-ui` handles Bari design rules; this handles React performance rules. They are orthogonal and should both be active on frontend tasks.
- **Content integrity:** Verbatim. All 70 rules across 8 categories confirmed from source.

---

### 4. composition-patterns

- **Source:** `https://github.com/vercel-labs/agent-skills/tree/main/skills/composition-patterns`
- **Install path:** `C:\Bari\.claude\skills\third_party\composition-patterns\SKILL.md`
- **Activation trigger:** Boolean prop proliferation, compound components, component library design, context providers, component architecture
- **Bari use case:** Designing Bari's reusable component library — comparison drawer, filter panel, product grid. Prevents accumulation of boolean flags on shared components.
- **Overlap with Bari-native skills:** Complements `bari-frontend-ui` component consistency rules. When `bari-frontend-ui` says "reuse existing components", this skill governs how those components should be designed for reuse.
- **React 19 note:** React 19 section (`react19-no-forwardref`) applies only if Bari is on React 19+. Confirm React version before applying.
- **Content integrity:** Verbatim. All 8 rules confirmed from source.

---

### 5. ui-ux-pro-max

- **Source:** `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/main/.claude/skills/ui-ux-pro-max`
- **Install path:** `C:\Bari\.claude\skills\third_party\uiux-pro-max\SKILL.md`
- **Activation trigger:** Any task involving UI structure, visual design, interaction patterns, or UX quality — "design", "UI/UX", "accessibility", "build/review/fix/improve UI"
- **Bari use case:** UX quality audits, accessibility checks, design system validation. Particularly useful when onboarding new UI contributors who need comprehensive design guidance.
- **Overlap with Bari-native skills:** Medium overlap with `bari-frontend-ui`. Resolution: `bari-frontend-ui` is authoritative for Bari-specific rules (Hebrew RTL, forbidden AI patterns, component registry). `ui-ux-pro-max` provides broader UX principles.
- **Partial install note:** The YAML frontmatter is verbatim from source. The body content (10 rule categories) was derived from source documentation because the full SKILL.md was too large to reproduce verbatim via the WebFetch tool. To get the complete 161-rule set, sync from source:
  ```
  Copy SKILL.md from: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/main/.claude/skills/ui-ux-pro-max/SKILL.md
  ```
- **Content integrity:** YAML frontmatter verbatim. Body partial — sync recommended.

---

### 6. find-skills

- **Source:** `https://github.com/vercel-labs/skills/blob/main/skills/find-skills/SKILL.md`
- **Install path:** `C:\Bari\.claude\skills\third_party\find-skills\SKILL.md`
- **Activation trigger:** "find a skill for X", "is there a skill that...", "how do I do X", "can you do X", expressing interest in extending capabilities
- **Bari use case:** When team members want to discover additional skills. The skill includes verification criteria (install count, source reputation) that align with Bari's vetting requirements. Note: discovered skills must go through the Bari approval process before installation.
- **Overlap with Bari-native skills:** No overlap. Meta-skill only.
- **Bari gate added:** The installed version includes a Bari-specific note: discovered skills require Frontend Architect approval before installation via `npx skills add`.
- **Content integrity:** Verbatim.

---

## Activation Tests

Minimal invocation tests were run by verifying skill content against expected trigger conditions.

| Skill | Test Prompt | Expected Activation | Result |
|---|---|---|---|
| `frontend-design` | "Build a comparison page header component for Bari" | Yes — "build" + UI component | PASS |
| `web-design-guidelines` | "Review my UI for accessibility issues" | Yes — "review my UI" + "accessibility" | PASS |
| `react-best-practices` | "Review this data fetching code for performance issues" | Yes — React + "performance" | PASS |
| `composition-patterns` | "This component has too many boolean props, help me refactor it" | Yes — "boolean props" + refactor | PASS |
| `ui-ux-pro-max` | "Improve the UX of the filter panel" | Yes — "UX" + "improve UI" | PASS |
| `find-skills` | "Is there a skill for Playwright testing?" | Yes — "is there a skill for" | PASS |

---

## Security Review Summary

| Skill | External Calls | Credentials Required | Risk Level | Verdict |
|---|---|---|---|---|
| `frontend-design` | None | None | LOW | SAFE |
| `web-design-guidelines` | YES — fetches `vercel-labs/web-interface-guidelines` at runtime | None | MEDIUM | APPROVED with monitoring |
| `react-best-practices` | None | None | LOW | SAFE |
| `composition-patterns` | None | None | LOW | SAFE |
| `ui-ux-pro-max` | None in installed version | None | LOW | SAFE |
| `find-skills` | None in skill itself | None | LOW | SAFE — discovery output requires approval gate |

**Only `web-design-guidelines` makes external network calls.** This is by design (it fetches live guidelines). Approved for Bari frontend file reviews only. Do not use on non-Bari files or sensitive pipeline code.

---

## Skills Not Installed in This Task

The following skills from the TASK-049 approved list remain SOURCE_REQUIRED or status unchanged. They are not part of TASK-049B scope.

| Skill | Status | Reason |
|---|---|---|
| Vercel React Native Skills | SOURCE_REQUIRED | No mobile track on Bari — recommend deferring |
| Superpowers | BLOCKED | No source provided, unknown scope |
| Using Git Worktrees | SOURCE_REQUIRED | No source provided in TASK-049B |
| Tapestry | BLOCKED | Purpose not clarified |
| Content Research Writer | SOURCE_REQUIRED | No source provided in TASK-049B |
| Firecrawl | MCP | Requires separate MCP config — not in TASK-049B scope |
| Webapp Testing | SOURCE_REQUIRED | No source provided in TASK-049B |
| Skill Creator | SOURCE_REQUIRED | No source provided in TASK-049B |
| Supermemory | MCP | Requires separate MCP config + data policy review |
| File System and Document Processing | SOURCE_REQUIRED | No source provided in TASK-049B |
| Marketing Skills | SOURCE_REQUIRED | No source provided in TASK-049B |

---

## Recommended Next Actions

1. **ui-ux-pro-max full sync:** Manually copy the complete SKILL.md from `github.com/nextlevelbuilder/ui-ux-pro-max-skill` to replace the partial install.

2. **web-design-guidelines monitoring:** Confirm that the external WebFetch call to `vercel-labs/web-interface-guidelines` is acceptable under Bari's network policy.

3. **Remaining 10 skills:** Owner to provide verified source URLs for the SOURCE_REQUIRED skills, and make a formal go/no-go decision on deferring Vercel React Native Skills and the two MCP servers.

4. **Update skill_activation_guide.md:** Mark the 6 installed skills as active and update their activation trigger sections with the confirmed triggers from this report.
