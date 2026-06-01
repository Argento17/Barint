# Bari Agent Decision Rights Matrix v1

**Status:** FROZEN â€” Agent OS v1
**Frozen:** 2026-05-31
**Owner:** Head of Product
**Task:** TASK-049D

This matrix defines who can initiate, recommend, approve, implement, and audit each class of decision in the Bari system. When two agents have the same right on a decision, the one listed first has precedence.

---

## Legend

| Code | Meaning |
|---|---|
| **I** | Can Initiate â€” may start this process or request |
| **R** | Can Recommend â€” may propose a course of action; cannot proceed without approval |
| **A** | Can Approve â€” required sign-off; process cannot proceed without this agent's approval |
| **M** | Can Implement â€” executes the approved decision |
| **U** | Can Audit / Verify â€” independently validates the outcome |
| **â€”** | No standing in this decision |

---

## Decision Domains

### D1 â€” Category Pipeline Initiation

*Deciding to begin building a new product category.*

| Agent | Right | Notes |
|---|---|---|
| Product Agent | **I, A** | Sole authority to initiate a new category; approves the launch brief |
| Data Agent | R | May surface readiness conditions; cannot self-initiate |
| Nutrition Agent | R | Must confirm a scoring approach exists for the category |
| Research Agent | R | Provides market landscape to inform the decision |
| QA Agent | U | Audits that initiation criteria were met |
| Frontend Agent | â€” | Receives brief after initiation; does not initiate |
| Design Agent | â€” | Consulted on page type after initiation |
| Content Agent | â€” | Activated post-BSIP2 |
| Marketing Agent | â€” | Activated post-launch |

---

### D2 â€” Shelf Mapping

*Assigning shelf slugs to a category definition.*

| Agent | Right | Notes |
|---|---|---|
| Data Agent | **I, M** | Executes shelf mapping; owns the shelf registry |
| Product Agent | **A** | Approves the mapping before corpus filter proceeds |
| Nutrition Agent | R | May flag categories with structural ambiguity |
| QA Agent | U | Verifies no duplicate shelf-to-category assignments |
| Research Agent | â€” | |
| Frontend Agent | â€” | |
| Design Agent | â€” | |
| Content Agent | â€” | |
| Marketing Agent | â€” | |

---

### D3 â€” Corpus Filter Configuration

*Defining the product corpus for a category.*

| Agent | Right | Notes |
|---|---|---|
| Data Agent | **I, M** | Configures and runs the filter |
| Nutrition Agent | R | May recommend category-specific filter constraints |
| Product Agent | **A** | Approves filter spec before BSIP0 gate |
| QA Agent | U | Verifies corpus size meets minimum threshold |
| Research Agent | R | May surface corpus composition insights |
| Frontend Agent | â€” | |
| Design Agent | â€” | |
| Content Agent | â€” | |
| Marketing Agent | â€” | |

---

### D4 â€” BSIP0 Gate (Category Entry)

*Pass/fail decision allowing a category to proceed to enrichment.*

| Agent | Right | Notes |
|---|---|---|
| Data Agent | M | Runs the gate check |
| Product Agent | **A** | Final pass/fail approval; may override a conditional pass |
| Nutrition Agent | R | Must confirm scoring approach is viable |
| QA Agent | **U** | Independent verification of gate criteria |
| Research Agent | â€” | |
| Frontend Agent | â€” | |
| Design Agent | â€” | |
| Content Agent | â€” | |
| Marketing Agent | â€” | |

---

### D5 â€” BSIP1 Enrichment Execution

*Running attribute extraction, label assignment, and dimension selection.*

| Agent | Right | Notes |
|---|---|---|
| Data Agent | **I, M** | Executes enrichment pipeline |
| Nutrition Agent | **A** | Must approve enrichment configuration for new categories |
| Product Agent | R | Monitors coverage thresholds |
| QA Agent | U | Audits enrichment coverage stats and label distribution |
| Research Agent | R | May provide category-specific enrichment guidance |
| Frontend Agent | â€” | |
| Design Agent | â€” | |
| Content Agent | â€” | |
| Marketing Agent | â€” | |

---

### D6 â€” Scoring Rule Proposal

*Proposing a new scoring rule or modification to existing rules.*

| Agent | Right | Notes |
|---|---|---|
| Nutrition Agent | **I, R** | Primary proposer of new scoring rules |
| Research Agent | R | May surface evidence that motivates a new rule |
| Data Agent | R | May flag implementation feasibility of proposed rules |
| Product Agent | â€” | Does not propose rules; approves or blocks them (D7) |
| Frontend Agent | â€” | |
| Design Agent | â€” | |
| QA Agent | â€” | |
| Content Agent | â€” | |
| Marketing Agent | â€” | |

---

### D7 â€” Scoring Rule Approval

*Approving, blocking, or sending back a scoring rule proposal.*

| Agent | Right | Notes |
|---|---|---|
| Product Agent | **A** | Final approval authority â€” business and scope impact |
| Nutrition Agent | **A** | Scientific validity â€” both approvals required |
| Data Agent | R | Must confirm implementability before approval |
| QA Agent | U | Verifies governance checklist was completed (evidence ref, observability, rollback plan) |
| Research Agent | â€” | |
| Frontend Agent | â€” | |
| Design Agent | â€” | |
| Content Agent | â€” | |
| Marketing Agent | â€” | |

**Note:** A scoring rule requires BOTH Product Agent and Nutrition Agent approval. Either can block. If they conflict, escalate to the owner (see Agent OS escalation paths).

---

### D8 â€” Scoring Rule Implementation

*Coding and deploying an approved scoring rule.*

| Agent | Right | Notes |
|---|---|---|
| Data Agent | **M** | Implements approved rules in the pipeline |
| Nutrition Agent | U | Verifies implementation matches approved specification |
| QA Agent | U | Verifies score propagation after implementation |
| Product Agent | â€” | Approves rules, not implementation |
| Frontend Agent | â€” | |
| Design Agent | â€” | |
| Content Agent | â€” | |
| Marketing Agent | â€” | |

---

### D9 â€” QA Baseline Freeze

*Freezing a QA baseline after a clean run.*

| Agent | Right | Notes |
|---|---|---|
| QA Agent | **I, A, M** | Sole authority to freeze a baseline |
| Data Agent | M | Provides the run ID and run artifacts |
| Product Agent | R | May be notified; does not co-approve |
| Nutrition Agent | â€” | |
| Frontend Agent | â€” | |
| Design Agent | â€” | |
| Content Agent | â€” | |
| Marketing Agent | â€” | |

**Note:** QA Agent cannot freeze over a run with unresolved hard fails. That is a technical constraint, not a decision right.

---

### D10 â€” Category Rollout / Go-Live Decision

*Approving a category for public launch.*

| Agent | Right | Notes |
|---|---|---|
| Product Agent | **A** | Final go/no-go authority |
| QA Agent | **U** | Must deliver PASS verdict before Product Agent can approve |
| Frontend Agent | R | Confirms build passes and route is reachable |
| Nutrition Agent | R | Confirms scoring is correct for live category |
| Design Agent | R | Confirms visual QA pass |
| Content Agent | R | Confirms copy is complete and reviewed |
| Data Agent | R | Confirms frontend JSON is current and correct |
| Marketing Agent | â€” | Activates after launch; does not gate it |
| Research Agent | â€” | |

---

### D11 â€” Frontend Implementation

*Writing, modifying, or deploying code in `C:\bari-web\src\`.*

| Agent | Right | Notes |
|---|---|---|
| Frontend Agent | **I, M** | Sole implementation authority |
| Design Agent | **A** | Must approve visual spec before any new component is built |
| Product Agent | A | Approves scope; Frontend Agent does not self-scope |
| QA Agent | U | Verifies implementation post-build |
| Nutrition Agent | â€” | |
| Research Agent | â€” | |
| Data Agent | â€” | |
| Content Agent | â€” | |
| Marketing Agent | â€” | |

---

### D12 â€” Design Spec Approval

*Approving the visual specification for a new component or page section.*

| Agent | Right | Notes |
|---|---|---|
| Design Agent | **I, A** | Primary spec authority |
| Product Agent | A | Must approve scope additions or spec exceptions |
| Nutrition Agent | R | For content and hierarchy of nutrition-facing sections |
| Frontend Agent | R | For technical feasibility |
| QA Agent | U | Validates final implementation against the approved spec |
| Research Agent | â€” | |
| Data Agent | â€” | |
| Content Agent | â€” | |
| Marketing Agent | â€” | |

---

### D13 â€” Content Publication

*Publishing consumer-facing copy to a category page (hero, prologue, insight lines, methodology).*

| Agent | Right | Notes |
|---|---|---|
| Content Agent | **I, M** | Writes and submits copy for review |
| Nutrition Agent | **A** | Approves nutrition-facing claims and insight line language |
| Product Agent | A | Approves copy that makes product-level claims or positions Bari |
| QA Agent | U | Verifies copy fields are present and non-empty in frontend JSON |
| Frontend Agent | M | Integrates approved copy into frontend JSON |
| Design Agent | R | Confirms copy fits within page hierarchy and length constraints |
| Research Agent | R | May be consulted for factual accuracy |
| Marketing Agent | â€” | Marketing copy (campaigns) is distinct from category page copy |

---

### D14 â€” Marketing Campaign Launch

*Initiating a marketing campaign or SEO initiative.*

| Agent | Right | Notes |
|---|---|---|
| Marketing Agent | **I, M** | Initiates and executes campaigns |
| Product Agent | **A** | Approves campaigns that make product claims or affect roadmap perception |
| Content Agent | M | Provides copy for campaigns that require editorial content |
| Research Agent | R | Provides market intelligence to support campaign planning |
| QA Agent | U | Verifies that campaign landing pages or linked pages are functional |
| Nutrition Agent | â€” | |
| Data Agent | â€” | |
| Frontend Agent | â€” | Implements campaign landing pages if needed |
| Design Agent | R | Reviews campaign creative for design system compliance |

---

### D15 â€” New Skill Installation

*Adding a new skill to `C:\Bari\.claude\skills\`.*

| Agent | Right | Notes |
|---|---|---|
| Frontend Architect | **I, A** | Infrastructure owner of the skill system |
| Product Agent | **A** | Must approve the capability gap justification |
| Any agent | I | May identify and request a new skill |
| QA Agent | U | Validates installation: source, content, activation test |
| All agents | â€” | May not self-install skills without the above approvals |

---

### D16 â€” Agent OS / Skill Architecture Changes

*Modifying `agent_os_v1.md`, `capability_stack_matrix.md`, or `decision_rights_matrix.md`.*

| Agent | Right | Notes |
|---|---|---|
| Product Agent | **A** | Architecture governance authority |
| Frontend Architect | **A** | Infrastructure owner |
| Any agent | R | May propose a change by identifying a capability gap or conflict |
| QA Agent | U | Validates that the change is internally consistent |
| All agents | â€” | May not self-modify these documents |

---

## Combined Rights Overview

Rows = Decision Domain. Columns = Agent. Codes: I=Initiate, R=Recommend, A=Approve, M=Implement, U=Audit/Verify.

| Decision | Product | Nutrition | Research | Data | Frontend | Design | QA | Content | Marketing |
|---|---|---|---|---|---|---|---|---|---|
| D1 Category Initiation | I,A | R | R | R | â€” | â€” | U | â€” | â€” |
| D2 Shelf Mapping | A | R | â€” | I,M | â€” | â€” | U | â€” | â€” |
| D3 Corpus Filter | A | R | R | I,M | â€” | â€” | U | â€” | â€” |
| D4 BSIP0 Gate | A | R | â€” | M | â€” | â€” | U | â€” | â€” |
| D5 BSIP1 Enrichment | R | A | R | I,M | â€” | â€” | U | â€” | â€” |
| D6 Scoring Proposal | â€” | I,R | R | R | â€” | â€” | â€” | â€” | â€” |
| D7 Scoring Approval | **A** | **A** | â€” | R | â€” | â€” | U | â€” | â€” |
| D8 Scoring Implementation | â€” | U | â€” | M | â€” | â€” | U | â€” | â€” |
| D9 QA Baseline Freeze | R | â€” | â€” | M | â€” | â€” | I,A,M | â€” | â€” |
| D10 Rollout Go-Live | **A** | R | â€” | R | R | R | U | R | â€” |
| D11 Frontend Implementation | A | â€” | â€” | â€” | I,M | A | U | â€” | â€” |
| D12 Design Spec | A | R | â€” | â€” | R | I,A | U | â€” | â€” |
| D13 Content Publication | A | A | R | â€” | M | R | U | I,M | â€” |
| D14 Campaign Launch | A | â€” | R | â€” | M | R | U | M | I,M |
| D15 Skill Installation | A | â€” | â€” | â€” | I,A | â€” | U | â€” | â€” |
| D16 Agent OS Changes | A | â€” | â€” | â€” | A | â€” | U | â€” | â€” |

---

## Conflict Resolution Protocol

When two A-right agents disagree on a decision:

1. **D7 (Scoring Rule):** Nutrition Agent and Product Agent must reach consensus. If unresolved after one round, the owner escalates to an explicit exception review. No rule is deployed in a disputed state.
2. **D11 (Frontend Implementation):** Product Agent approves scope; Design Agent approves spec. If they conflict, the conflict is about scope vs. design â€” Product Agent governs scope, Design Agent governs appearance. Neither overrides the other's domain.
3. **D13 (Content):** Nutrition Agent and Product Agent both hold approval on content. Nutrition Agent governs accuracy; Product Agent governs positioning. Content Agent must satisfy both independently.
4. **All other conflicts:** Escalate to Product Agent with both positions stated. Product Agent issues a decision within one work session.
