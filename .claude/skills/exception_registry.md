# Bari Exception Registry

**Status:** ACTIVE — no exceptions registered
**Version:** 1.0
**Published:** 2026-05-31
**Owner:** Product Agent + Frontend Agent
**Task:** TASK-049F

This registry tracks all approved exceptions to frozen Bari constraints. An exception is a time-bounded, explicitly approved deviation from a rule defined in the Agent OS, Gen 1 design constraints, canonical component rules, or skill architecture.

No exception is valid unless it appears in this registry with a status of APPROVED.

---

## Who Can Request

Any agent may identify and request an exception. Requests are submitted by naming the constraint, the rationale, and the proposed scope.

## Who Can Approve

| Constraint Type | Approving Agent(s) |
|---|---|
| Gen 1 design constraints (frozen visual spec) | Design Agent + Product Agent |
| Canonical component rules | Frontend Agent + Design Agent + Product Agent |
| Scoring rules or BSIP methodology | Nutrition Agent + Product Agent |
| Agent OS / decision rights / skill architecture | Product Agent + Frontend Agent |
| QA checklist items | QA Agent + Product Agent |

All approvals require both agents listed. Either can block.

## Expiration Policy

Every exception must have an expiration date or an explicit trigger condition for closure (e.g., "expires when Gen 2 component spec is finalized"). Open-ended exceptions are not permitted. If an exception expires without renewal, the frozen constraint is automatically restored.

## Status Values

| Status | Meaning |
|---|---|
| `PROPOSED` | Submitted, pending approval |
| `APPROVED` | Active, valid until expiration date |
| `EXPIRED` | Past expiration date, constraint restored |
| `REJECTED` | Denied — constraint stands |
| `CLOSED` | Closed early (trigger condition met or exception withdrawn) |

---

## Registry

*No exceptions registered. The table below is the authoritative record.*

| ID | Date | Requesting Agent | Approving Agents | Category | Constraint Excepted | Rationale | Expiration | Status |
|---|---|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — | — | — |

---

## Exception Detail Template

When an exception is added, create a detail block below the table using this format:

```
### EX-[ID]: [Short Title]

- **ID:** EX-[three-digit number]
- **Date:** [ISO date]
- **Requesting Agent:** [Agent name]
- **Approving Agents:** [Agent name] + [Agent name]
- **Category:** [Design / Component / Scoring / Agent OS / QA]
- **Constraint Excepted:** [Exact rule text or reference, e.g. "Gen 1: Score chip must use #F7F7F2 background for all grades"]
- **Scope:** [Exactly which category, page, component, or run this exception applies to — not global]
- **Rationale:** [Why the constraint cannot be met in this specific case]
- **Risk:** [What could go wrong if this exception is not managed carefully]
- **Mitigation:** [What is being done to reduce the risk]
- **Expiration:** [ISO date or trigger condition]
- **Status:** APPROVED
- **Notes:** [Optional: links to supporting docs, related decisions]
```

---

## Illustrative Examples

*The following entries are hypothetical examples included to demonstrate the format. They are NOT active exceptions. None of these have been approved.*

---

### EXAMPLE-A: Color Accent on Score Chip for Accessibility Test

- **ID:** EXAMPLE-A *(not a real exception)*
- **Date:** 2026-01-01
- **Requesting Agent:** Design Agent
- **Approving Agents:** Design Agent + Product Agent
- **Category:** Design
- **Constraint Excepted:** Gen 1: Score chip must use `#F7F7F2` background for ALL grades — no color encoding
- **Scope:** Baby monitors category only, mobile viewport only, A/B test cohort B, 2-week test window
- **Rationale:** Accessibility team flagged that neutral chip may be insufficient contrast for grade A vs. grade E in low-light conditions for users with moderate visual impairment. A/B test proposed to measure impact before deciding whether to formally update the Gen 1 spec.
- **Risk:** Dashboard drift; color encoding score meaning may undermine Bari's design philosophy if adopted broadly
- **Mitigation:** Exception scoped to a single category and test cohort; QA Agent verifies scope does not bleed to other categories; Design Agent reviews results before any extension
- **Expiration:** 2026-01-15 or when A/B test concludes, whichever is earlier
- **Status:** *(example only — not real)*

---

### EXAMPLE-B: Five Filter Dimensions for Electronics Category

- **ID:** EXAMPLE-B *(not a real exception)*
- **Date:** 2026-02-15
- **Requesting Agent:** Product Agent
- **Approving Agents:** Design Agent + Product Agent
- **Category:** Design
- **Constraint Excepted:** Gen 1: Filter — max 3 dimensions
- **Scope:** Air purifiers category page only
- **Rationale:** Air purifier purchase decisions are driven by 5 distinct technical dimensions (CADR, room size, filter type, noise level, energy rating) and user testing showed that limiting to 3 resulted in confusion. Category is unique in its technical complexity.
- **Risk:** Increased filter panel complexity may confuse users on other categories if the pattern spreads
- **Mitigation:** Exception is category-specific; Filter component remains limited to 3 dimensions in code for all other categories; exception is reviewed if more than 2 other categories request the same
- **Expiration:** 2026-06-01 or when a formal Gen 2 filter spec is finalized
- **Status:** *(example only — not real)*

---

### EXAMPLE-C: Inline Score Explanation for Supplement Category

- **ID:** EXAMPLE-C *(not a real exception)*
- **Date:** 2026-03-10
- **Requesting Agent:** Content Agent
- **Approving Agents:** Nutrition Agent + Product Agent
- **Category:** Scoring / Design
- **Constraint Excepted:** Gen 1: Expansion shows only nutrition, ingredients, data note, confidence — no headings and no score mechanism explanation
- **Scope:** Vitamin D supplement category, expansion section only
- **Rationale:** Supplement scoring uses evidence-tier logic that consumers find confusing without brief orientation. A single line ("Score based on clinical evidence strength, dose accuracy, and bioavailability") was approved by Nutrition Agent as necessary for user trust in this category.
- **Risk:** Framework vocabulary leakage if the line is not carefully worded
- **Mitigation:** Exact approved wording locked in the exception record; QA Agent verifies leakage checklist passes; Content Agent is sole author; any rewording requires a new exception
- **Expiration:** 2026-12-31 or when the supplement methodology page is live and linked from the expansion section
- **Status:** *(example only — not real)*

---

## Process for Adding an Exception

1. Requesting agent writes a detail block in the template format above and submits it for review
2. Both required approving agents must explicitly approve (comment or sign-off)
3. Exception is added to the registry table with status APPROVED and a unique EX-[ID]
4. If either approving agent rejects, the exception is logged as REJECTED with the rejection rationale
5. At expiration, the exception moves to EXPIRED status and the frozen constraint is restored
6. QA Agent verifies constraint restoration after expiration

---

## Relationship to Frozen Constraints

This registry does not change the frozen constraints. Constraints remain frozen. This registry records the narrow, time-bounded circumstances under which a specific constraint does not apply. The moment an exception expires or is closed, the constraint is fully restored with no action required.

If a pattern of exceptions suggests a constraint needs to be formally revised, that is a candidate for a governance change via D16 (Agent OS Changes), not a standing exception.
