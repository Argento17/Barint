# Bari Claude Skills

Version-controlled internal skills for Claude Code operating on the Bari project.

Skills live in `C:\Bari\.claude\skills\` and are loaded by the Claude Code harness when the agent is invoked inside the Bari project.

---

## Skills Index

### 1. `bari-category-factory`

**What it does:** Guides Claude through the full Bari category creation and promotion pipeline — from shelf mapping and corpus filtering through BSIP gates, enrichment, QA, and frontend packaging.

**When it activates:**
- User asks to create, modify, or audit a category
- User references shelf mapping, corpus filtering, or any BSIP stage
- User asks to package a category for the frontend
- Trigger phrases: "build a category", "run category pipeline", "add a shelf", "prepare for frontend"

**How to test it:**
```
Prompt: "Build a new category for air purifiers. Start from shelf mapping."
Expected: Claude runs through each pipeline stage in order, produces structured JSON artifacts, and halts at any gate failure.
```

**Stages covered:** Shelf Mapping → Corpus Filter → BSIP0 Gate → BSIP1 Enrichment → QA Gate → BSIP2 Readiness → Frontend Packaging

---

### 2. `bari-bsip2-scoring-governance`

**What it does:** Enforces governance rules whenever scoring logic is proposed or modified. Requires evidence registry references, label observability, category activation scope, rollback plans, and prevents rule accumulation.

**When it activates:**
- User proposes a new scoring rule
- User wants to modify existing scoring weights or thresholds
- User asks Claude to review a scoring PR or config change
- Trigger phrases: "add a scoring rule", "change the score for", "tune the algorithm", "update scoring weights", "modify BSIP2"

**How to test it:**
```
Prompt: "Add a scoring boost for products with warranty longer than 2 years."
Expected: Claude asks for evidence registry reference, checks label observability for the warranty label, requires category scope definition, and requests a rollback plan before approving.
```

**Governance checks:** Evidence Registry → Label Observability → Category Activation Scope → Rollback Plan → Rule Accumulation Check

---

### 3. `bari-qa-audit`

**What it does:** Guides Claude through QA validation — running the QA runner, checking traceability of products/labels/scores, classifying hard fails and warnings, freezing baselines after clean runs, and invalidating bad runs.

**When it activates:**
- User asks to run QA validation on a category
- User wants to review QA results or determine promotion eligibility
- User wants to freeze a QA baseline or investigate a failure
- Trigger phrases: "run QA", "check QA results", "validate category quality", "freeze baseline", "investigate QA failure", "invalidate this run"

**How to test it:**
```
Prompt: "Run QA on the refrigerator category enrichment output from run ID 2025-08-14-001."
Expected: Claude walks through traceability check, identifies hard fails and warnings, produces a structured audit report, and either blocks promotion or confirms baseline freeze eligibility.
```

**Stages covered:** QA Runner → Traceability → Hard Fails → Warnings → Baseline Freeze → Run Invalidation

---

### 4. `bari-frontend-ui`

**What it does:** Guides Claude for all Bari website UI work — enforcing comparison page structure, Hebrew RTL layout correctness, accessibility (WCAG 2.1 AA), component library consistency, and explicitly blocking generic AI UI patterns.

**When it activates:**
- User is building or reviewing a comparison page
- User is implementing or fixing Hebrew RTL layout
- User is working on a UI component or reviewing a frontend PR
- Trigger phrases: "build a comparison page", "fix the RTL layout", "add a component", "make it accessible", "review the UI"

**How to test it:**
```
Prompt: "Build a comparison page for baby monitors with a filter panel and product grid."
Expected: Claude produces a structured UI design following comparison page rules, with RTL layout, accessible markup, no hardcoded data, and no generic AI UI patterns. Any violations are flagged explicitly.
```

**Checks covered:** Comparison Structure → Data Traceability → RTL Layout → Accessibility → Component Consistency → Generic AI UI Prevention

---

## Why Third-Party Skills Are Not Installed Yet

Bari Claude Skills v1 uses only internal, markdown-based skills for the following reasons:

1. **Security boundary.** Third-party skills are executable code from external sources. Until Bari has a formal skill vetting process, no external code is authorized to run inside the Claude agent.

2. **Project specificity.** Generic third-party skills do not know about Bari's BSIP pipeline, evidence registry, label registry, or RTL-first design system. Internal skills encode Bari-specific rules that no external skill can provide.

3. **Auditability.** Every instruction Claude follows is version-controlled in this repository and reviewable by the team. External skills would introduce behavior that is not auditable in the project's git history.

4. **Stability.** Third-party skills can change between versions. Internal skills are pinned to the project and only change when the team decides to change them.

**Third-party skills will be considered in v2** after the following are in place:
- A skill vetting and approval process
- Sandboxed skill execution
- A documented integration test protocol for each external skill

---

## Adding or Modifying Skills

- All skill changes must be reviewed by the skill's designated owner
- Skills must remain markdown-only — no executable scripts in `.claude/skills/`
- Update this README when adding a new skill or changing activation triggers
- Skill versioning follows the project's standard git workflow — no separate versioning scheme
