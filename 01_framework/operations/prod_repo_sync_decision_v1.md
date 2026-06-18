# Production Repo Sync — Decision Brief v1

**Date:** 2026-06-11  
**Author:** Product Agent  
**Deliverable to:** Owner  
**Status:** OWNER ENDORSED — EXECUTION AUTHORIZED (2026-06-11)  
**Inputs:** TASK-242 `close_reason` (closure record `a5b4171b`); release/prod-integrity-242 gate report; Full Cycle Health Audit Part 1 Stage R/S findings; live repo inspection (2026-06-11).

**Owner ruling (2026-06-11):** Option C endorsed. Four plan gaps identified and resolved below (§9). Phase 0 authorized for immediate dispatch. Re-point program task + Phase 2 route/version diff to be produced before §8 decisions are signed.

---

## 1. Situation

### 1.1 Corrected topology (TASK-242 close_reason finding)

| Repo | Host | Vercel project | Deploys? | Layout |
|---|---|---|---|---|
| `Argento17/bari` | bari/main (remote alias) | **bari** | **YES** — bari.digital | Standalone: `src/` at root |
| `Argento17/Barint` | origin/master (local) | None | **NEVER deployed** | Monorepo: `bari-web/src/` subtree |

Production has served every consumer visit in Bari's history from `Argento17/bari`. Barint has zero Vercel deployments. All active development has happened in Barint since the monorepo consolidation (commit `11c6ea4b`, TASK-134). The gap is structural, not just a merge lag.

### 1.2 Divergence magnitude

| Metric | Value |
|---|---|
| Diverged at | `11c6ea4b` (bari-web subtree add) |
| Barint master ahead by | 81 commits, 10,162 files changed |
| Path mismatch | Production: `src/` root. Barint: `bari-web/src/` subtree |

### 1.3 What is actually live (Argento17/bari @ `10cc84fa`)

**Routes serving consumers today:**

| Route | Data file | Known defect |
|---|---|---|
| `/hashvaot/breakfast-cereals` | `cereals_frontend_v1.json` | 9 OFF image URLs |
| `/hashvaot/granola` | `granola_frontend_v1.json` | 12 OFF image URLs |
| `/hashvaot/snacks` | `snacks_frontend_v2.json` | 12 of 18 products `verified` with null nutrition panel (DA-013; worse than Barint) |
| `/hashvaot/yogurts` | `yogurts_frontend_v2.json` | Silently OFF-derived per contamination audit; no literal strings |
| `/hashvaot/bread`, `/hashvaot/bread-comparison` | `bread_frontend_v2.json` | No known integrity defect |
| `/hashvaot/butter` | `butter_frontend_v1.json` (not v2) | Stale; Barint has v2 |
| `/hashvaot/cheese` | `cheese_frontend_v2.json` (not v3) | Stale; Barint has v3 |
| `/hashvaot/hummus`, `/hashvaot/maadanim`, etc. | various | No critical defects identified |

**Routes NOT in production (never launched):**

- `/hashvaot/salty-snacks` — does not exist in Argento17/bari
- `/hashvaot/hard-cheeses` — does not exist in Argento17/bari
- `/hashvaot/juices` — does not exist in Argento17/bari
- `/hashvaot/frozen-vegetables` — does not exist in Argento17/bari (confirmed: it was only in Barint, never shipped)

**Key implication:** The TASK-242 framing ("fabricated salty v3 was never live") is confirmed. Salty-snacks v3 with fake barcodes was never a consumer-facing defect — the route simply did not exist in production.

### 1.4 Barint master current state (undeployable)

Barint master (`origin/master`) has these routes built but is NOT safe to deploy as-is:

| Issue | Detail |
|---|---|
| `/hashvaot/salty-snacks` imports v3 | Fabricated identity (fake barcodes, dead image host). v4 exists only on `salty-snacks-v4` branch. |
| `/hashvaot/frozen-vegetables` present | Phase-1-locked, score-free, must not be live. |
| `cereals_frontend_v2.json` | 8 OFF image URLs (not yet de-OFF'd on master) |
| `granola_frontend_v1.json` | 9 OFF image URLs (not yet de-OFF'd on master) |
| `hard_cheeses_frontend_v2.json` | OFF image contamination (not yet de-OFF'd on master) |
| `yogurts_frontend_v3.json` | OFF-derived contamination |
| `snacks_frontend_v2.json` | Confidence inflation (DA-013 hotfix is on `salty-snacks-v4` and `release/prod-integrity-242`, not master) |

**The reference content** for fixing all of the above is validated, build-green, and recorded on `release/prod-integrity-242` (head `ab3f0c94`), retained as reference evidence per TASK-242 close_reason. It is not deployable from that branch (standalone layout mismatch) but provides the exact diffs to apply.

---

## 2. Option A — Full bari-web Tree Sync

**Definition:** Mirror the full contents of Barint's `bari-web/` tree into `Argento17/bari`'s `src/` tree in one operation.

### What goes live

| Category | Content | Status |
|---|---|---|
| salty-snacks | v4 (29 real products, first-ever launch) | **IF** `salty-snacks-v4` merged to master first |
| hard-cheeses | `hard_cheeses_frontend_v2.json` | First-ever launch |
| juices | `juices_frontend_v3.json` | First-ever launch |
| cheese | `cheese_frontend_v3.json` | Update to existing page |
| yogurts | `yogurts_frontend_v3.json` (de-OFF'd) | Update |
| cereals | `cereals_frontend_v2.json` (de-OFF'd) | Update |
| granola | `granola_frontend_v1.json` (de-OFF'd) | Update |
| butter | `butter_frontend_v2.json` | Update |
| snacks confidence | DA-013 hotfix | Update |
| Glass Box D4/D5/D6 | Feature-flagged | Live only if env var set |
| Blog posts (6+) | bread, milk, yogurt, snacks, hummus, shemen-zayit | First-ever publication |
| frozen-vegetables | **Must be excluded pre-sync** | Phase-1-locked; NOT to go live |

### Why this option is not viable as stated

The path structures are incompatible: a wholesale copy from `bari-web/` to `src/` is a mechanical flatten, not a git merge. There is no `git merge` path — `bari-web/` is a git subtree; the production repo has no `bari-web/` prefix anywhere. Executing Option A requires either:
- (a) A scripted rsync of all files with path translation — equivalent to Option B at full scope, with no review gate, and carrying every WIP file, dev route, and experimental component in Barint; or
- (b) Converting Argento17/bari to a monorepo with a `bari-web/` subtree — which is Option C in reverse and even more disruptive.

Barint master is also undeployable today (see §1.4) — a full sync of master as-is would ship fabricated salty-snacks v3 and frozen-vegetables. Even if salty-snacks-v4 is merged to master first, the OFF contamination and frozen-vegetables must be resolved before any sync.

**Verdict: Not recommended.** The scope is unbounded, the path structure makes it non-executable as a single clean operation, and it bypasses all per-launch review gates.

**Tripwire #2 sign-off required for Option A:**
- salty-snacks v4 (first-ever consumer launch — 29 products live)
- hard-cheeses (first-ever consumer launch)
- juices (first-ever consumer launch)
- blog posts (6 first-ever publications)
- yogurts update (de-OFF — visual placeholder regression; score unchanged but images disappear)
- cereals/granola update (same)
- Glass Box activation (already owner-authorized per `54d0c13f` — no new sign-off required if env var is unchanged)

---

## 3. Option B — Selective Category-by-Category Ports

**Definition:** Apply individual targeted patches from Barint/release-branch to `Argento17/bari` directly, translating paths as needed (`bari-web/src/X` → `src/X`).

### Immediate defect fixes (no launch gate needed)

| Fix | Source | Path translation | Complexity |
|---|---|---|---|
| Cereals OFF images | `release/prod-integrity-242:bari-web/src/data/comparisons/cereals_frontend_v2.json` → null | But prod uses v1 — import must also update `src/app/hashvaot/breakfast-cereals/page.tsx` | Low |
| Granola OFF images | Same pattern — `granola_frontend_v1.json` in place | In-place null replacement, same filename | Very low |
| Snacks confidence (DA-013) | Apply 4-row hotfix (snk-003/007/009/020 → partial) to `src/data/comparisons/snacks_frontend_v2.json` | Same filename | Very low |
| Yogurts contamination | Per the contamination audit — ruling required on whether yogurts_frontend_v2 can be fixed in place or requires v3 regeneration | Depends on ruling | Medium |

### Per-launch category ports

| Category | Files to port | Dependencies | Tripwire #2 |
|---|---|---|---|
| salty-snacks | 6 files (page-data, component, JSON, page, sodium bar component, view-model) | `comparison-metric-column.tsx` + `view-models/index.ts` also need porting | Yes |
| hard-cheeses | Comparison page + JSON + registry entry | Shared components clean | Yes |
| juices | Comparison page + JSON + registry entry | Shared components clean | Yes |
| cheese-v3 | JSON swap only | None | No (existing route) |
| yogurts-v3 | JSON swap (de-OFF'd) | OFF contamination ruling | Maybe |

### Assessment

Option B solves the immediate defects quickly and with surgical precision. It keeps the two-repo problem alive permanently — every future change in Barint must be re-ported to Argento17/bari, and the two repos will continue to drift. The cereals fix requires updating both the JSON and the page import (production uses v1, Barint has v2 — can't just drop v1 in place). Each category port requires a build verification in the standalone repo context where Barint's path aliases (`@/`) may resolve differently.

**Verdict: Valid for immediate defect remediation only; not viable as the durable strategy.** The two-repo drift will compound into a larger problem with every new category launch. Recommended only as the Phase 0 emergency fix while Option C is prepared.

**Tripwire #2 sign-off per category launch under Option B:** Same as Option A per-category (salty-snacks, hard-cheeses, juices each require sign-off; defect fixes do not).

---

## 4. Option C — Re-point Vercel to Barint (Recommended)

**Definition:** Change the Vercel project `bari` from `Argento17/bari` to `Argento17/Barint` with root directory set to `bari-web/`. All future deploys come from Barint master. The standalone repo is retained as a read-only fallback.

### Execution sequence

Option C requires a **master-clean gate** before the Vercel re-point. The gate is not optional — Barint master is currently undeployable (§1.4). The gate is the workstream; the re-point is the final flip.

**Phase 0 — Immediate defect patches to Argento17/bari (today)**
Apply the four critical fixes directly to production while the gate is in progress:
1. Granola OFF images → null (in-place, same filename)
2. Cereals: upgrade page import to v2 + null images (2 files)
3. Snacks: 4-row confidence hotfix (snk-003/007/009/020 → partial)
4. Yogurts: ruling + remediation (separate decision)

These are Option B surgical patches, executed once, then permanently superseded by Option C.

**Phase 1 — Barint master-clean gate**

Apply the reference content from `release/prod-integrity-242` to Barint master:

| Action | Source on release/prod-integrity-242 | Why not already on master |
|---|---|---|
| De-OFF cereals_v2 (8 hits) | `cereals_frontend_v2.json` null patch | Reference branch applied to production v1; Barint has v2 but un-de-OFF'd |
| De-OFF granola (9 hits) | `granola_frontend_v1.json` null patch | Same as above |
| De-OFF hard_cheeses_v2 | `hard_cheeses_frontend_v2.json` null patch | Same |
| De-OFF yogurts_v3 | `yogurts_frontend_v3.json` null patch | Same |
| Snacks confidence hotfix | `snacks_frontend_v2.json` 4-row patch | Release branch applied to master bytes; not merged to Barint master |
| Remove frozen-vegetables route | 9 file deletions + registry dewire | Frozen-veg is on Barint master; must go before re-point |
| OFF client hard-disable | `integrations/clients/open_food_facts.py` | Root-repo artifact; may already be on master — verify |
| CLAUDE.md OFF hard rule | `CLAUDE.md` | Already on Barint master — verify |

Merge `salty-snacks-v4` to Barint master:
- Upgrades salty import v3 → v4 (the critical safety fix)
- Lands sodium bar component + view-model addition
- Lands 29 real products (first-ever launch — requires owner tripwire #2 sign-off before merge)
- Gate: `tsc --noEmit` + `next build` green in bari-web/

**Phase 2 — Vercel re-point**

Vercel config changes:
- Project setting: Git Repository → `Argento17/Barint`
- Root Directory → `bari-web/`
- Production branch → `master`
- Preview branches → `salty-snacks-v4` and others as desired
- Environment variables: carry over any vars from the old project

Domain:
- `bari.digital` is already pointed to the Vercel project `bari`
- If re-pointing within the same project (edit repo): domain assignment survives
- If creating a new Vercel project and reassigning: brief window of domain unavailability (~1–2 min)
- **Preferred:** Edit existing project `bari` to point to Barint — no domain downtime

**Phase 3 — Subsequent category launches (post re-point)**

With Vercel serving from Barint master, each future category goes live by PR merge to master:
- hard-cheeses: already on master, goes live at re-point
- juices: already on master, goes live at re-point
- future categories: merge → auto-deploy, no porting

### What goes live at re-point (after Phase 1 gate + salty-snacks-v4 merge)

| Item | Status | Tripwire #2? |
|---|---|---|
| salty-snacks v4 (29 real products) | First-ever consumer launch | **YES — required** |
| hard-cheeses | First-ever consumer launch | **YES — required** |
| juices | First-ever consumer launch | **YES — required** |
| cheese-v3 | Update to existing live page | No |
| yogurts-v3 (de-OFF'd) | Update — images → placeholder | No (defect fix, not redesign) |
| cereals-v2 (de-OFF'd) | Update — images → placeholder | No |
| granola (de-OFF'd) | Update — images → placeholder | No |
| butter-v2 | Update to existing live page | No |
| snacks confidence fixed | Update — honesty correction | No |
| Glass Box D4/D5/D6 | Behind feature flag; live only if env var set | Already owner-authorized |
| Blog posts | First-ever publication (6 posts) | **YES — required** |
| frozen-vegetables | Removed before re-point | N/A |

### Vercel re-point domain risk

**Low.** The preferred path (edit existing Vercel project's repo pointer) keeps the custom domain assignment intact — no DNS change, no downtime window. If a new Vercel project is created instead, the risk is a 1–2 minute gap while domain is reassigned. Mitigation: execute during off-peak hours; keep the old project's domain assignment active until smoke test passes on the new project's preview URL.

---

## 5. Recommendation

**Option C — Re-point Vercel to Barint — phased.**

**Why:**

Option A is mechanically non-executable in its clean form and bypasses all launch review gates. Option B is the right emergency tool for today's defects but embeds a permanent structural debt — every future Barint commit requires a manual port to a standalone repo with path translation. That debt compounds with every new category.

Option C permanently closes the two-repo problem. Once Vercel points to Barint, all future work — scoring, content, new categories — deploys from the same repo where the work actually happens. No porting, no drift, no topology confusion. The rollback is trivial (single Vercel setting change). The gate before re-point (Phase 1) is necessary but bounded: it is the same remediation work that would be required under any option.

The only non-trivial risk in Option C is the bundle of first-ever launches (salty-snacks, hard-cheeses, juices) that go live together at re-point. This is manageable: each can be excluded from the master-clean gate (un-route or hold behind a flag) and launched individually after re-point, sequencing owner sign-off category by category. The de-OFF fixes and confidence fix are defect remediation and do not require tripwire #2 sign-off.

**Execution order:**
1. Phase 0: Port 4 defect fixes to Argento17/bari today (surgical Option B — no tripwire)
2. Phase 1: Clean Barint master gate (data-agent: de-OFF 4 JSONs, remove frozen-veg, snacks confidence; salty-snacks-v4 merge pending owner sign-off)
3. Phase 2: Owner sign-off on salty-snacks v4 launch + hard-cheeses + juices + blog posts (bundle or sequence — owner decides)
4. Phase 3: Vercel re-point (orchestrator executes, 15-minute operation; owner authorizes as irreversible platform change)
5. Phase 4: Smoke test against live URL; TASK-243 (image backfill) and TASK-244 (DA-013 structural fix) continue as fast-follows

---

## 6. Rollback Story

**Option C rollback:**
- Vercel project: revert the repository pointer back to `Argento17/bari` → immediate redeploy from old standalone repo
- Old standalone repo stays intact and untouched throughout; no changes are made to it (Phase 0 patches apply but are additive)
- All consumer URLs remain stable (same Vercel project, same domain)
- Time to rollback: ~2 minutes (Vercel build trigger)
- Trigger condition: smoke test failure after re-point; any broken route or data integrity issue on the live URL

**Phase 0 (Option B patch) rollback:**
- Each surgical patch is a standalone commit to Argento17/bari master
- Revert commit reverts the specific fix; no cross-dependencies
- Example: snacks confidence revert would restore inflated rows — acceptable temporarily

---

## 7. Tripwire #2 Sign-off List by Option

Tripwire #2: "ships something irreversible AND consumer-facing (category go-live, public claim, brand/positioning)."

### Option A
| Action | Tripwire #2? | Owner sign-off required |
|---|---|---|
| salty-snacks v4 — first-ever launch | **YES** | Required before execution |
| hard-cheeses — first-ever launch | **YES** | Required before execution |
| juices — first-ever launch | **YES** | Required before execution |
| blog posts (6) — first-ever publication | **YES** | Required before execution |
| yogurts/cereals/granola — de-OFF update | No (defect fix) | Not required |
| cheese-v3 / butter-v2 — update | No | Not required |
| Glass Box activation (if env var set) | Already authorized | No new sign-off |
| Frozen-vegetables removal | No (never was live) | Not required |

### Option B (per-action)
| Action | Tripwire #2? | Owner sign-off required |
|---|---|---|
| OFF image null patches (cereals/granola) | No | Not required |
| Snacks confidence hotfix | No | Not required |
| Yogurts remediation | No (defect fix) | Not required |
| Salty-snacks port (category launch) | **YES** | Required per-port |
| Hard-cheeses port | **YES** | Required per-port |
| Juices port | **YES** | Required per-port |
| Blog post publication | **YES** | Required |

### Option C (phased — recommended)
| Phase | Action | Tripwire #2? | Owner sign-off required |
|---|---|---|---|
| Phase 0 | 4 defect patches to Argento17/bari | No | Not required |
| Phase 1 | Barint master clean gate (de-OFF + frozen-veg + confidence) | No | Not required |
| Phase 2 | salty-snacks-v4 merge to Barint master | **YES** | **Required** |
| Phase 2 | hard-cheeses goes live at re-point | **YES** | **Required** (can exclude from re-point scope and hold behind route removal until separately authorized) |
| Phase 2 | juices goes live at re-point | **YES** | **Required** (same — holdable) |
| Phase 2 | blog posts publish | **YES** | **Required** |
| Phase 3 | Vercel re-point (platform change — irreversible unless rolled back) | **YES** | **Required** — platform-level decision |
| Phase 4 | TASK-243, TASK-244 (fast-follows) | No | Not required |

**Note on hard-cheeses and juices under Option C:** Both routes are on Barint master and would go live automatically at re-point unless explicitly removed from master first (or placed behind a feature flag). Product recommends: include them in the Phase 2 bundle sign-off — they are validated work, and a sequenced launch prevents the routes from being accidentally live without authorization. If the owner prefers incremental, exclude them from master before re-point and merge individually after.

---

## 8. Decision Requested

Owner decision required on:

1. **Approve Option C** as the strategic direction (Vercel re-point after gate).
2. **Authorize Phase 0** immediate defect patches to Argento17/bari (no tripwire — but owner awareness requested given we're touching production).
3. **Bundle vs sequence** the first-ever launches: does the owner want salty-snacks + hard-cheeses + juices in one go-live event (re-point), or sequenced merges after re-point?
4. **Blog posts**: included in re-point bundle, or separate authorization?
5. **Vercel re-point authorization** (Phase 3): this is an irreversible platform change (restorable via rollback, but still tripwire #2). Owner must explicitly authorize before execution.

Orchestrator will hold all execution until this brief is acknowledged. No production changes have occurred.

---

## 9. Gap Resolutions (owner-identified, 2026-06-11)

Four gaps identified by owner review before §8 decisions are signed. Each is resolved below and changes Phase 1/2/3 as noted.

### Gap 1 — Phase 1 leaves salty-snacks v3 in master (plan error)

**Problem:** Phase 1 as written (de-OFF + frozen-veg + snacks confidence) does not fix the v3→v4 import in `salty-snacks-page-data.ts`. At re-point, Barint master serves salty-snacks v3 (fabricated identity) publicly. The brief placed the v3→v4 flip in Phase 2 (behind salty-snacks-v4 merge sign-off), but that creates an unsafe intermediate state.

**Resolution:** Phase 1's source is `release/prod-integrity-242` merged wholesale into Barint master as a PR. That branch already contains the v3→v4 flip, the de-OFF of 4 JSONs, frozen-vegetables removal, snacks confidence hotfix, OFF client disable, and CLAUDE.md hard rule — all in one reviewed, build-green unit. No new porting work: the reference branch becomes the Phase 1 PR diff directly. The owner's note that TASK-242 said "do not merge the branch" applied to merging it to bari/main (which would have been a production action); merging to Barint master is a pre-production prep step under the new program and explicitly superseded by the Option C ruling (see Gap 3).

**Impact on phasing:**
- Phase 1 is now: open PR from `release/prod-integrity-242` → `master` (Barint), resolve any conflicts with Glass Box / later commits, gate green (`tsc --noEmit` + `next build` in `bari-web/`), merge.
- Phase 2 sign-off items no longer need to include the salty v3→v4 flip — it ships with Phase 1.
- Phase 2 is now purely the launch authorization bundle (salty-snacks first-ever live, hard-cheeses, juices, blog posts).
- Salty-snacks route must be included in the Phase 2 sign-off list explicitly, since the release branch includes its route and v4 data. If owner defers salty sign-off past re-point, the route must be de-wired from master before Phase 3.

### Gap 2 — Re-point payload understated; yogurts is a real decision

**Problem:** The brief sampled the payload. Everything on master ships at re-point: cheese v2→v3, yogurts v2→v3, hummus/maadanim/bread data versions, corpus.ts runtime gate, Glass Box state, blog/research routes. The brief named hard-cheeses and juices as the critical holdables but did not enumerate the full list.

**Yogurts specific issue (real decision, not formality):** Production serves `yogurts_frontend_v2.json` (OFF-derived corpus, no literal OFF strings). Barint master has `yogurts_frontend_v3.json`. The release branch de-OFF'd its images (nulled), but the contamination audit confirmed the entire corpus is OFF-derived — not just the images. Re-pointing ships OFF-derived yogurts data under either version unless the pull-vs-re-acquire ruling (pending continuation prompt 3) resolves first or the category is held at re-point.

**Resolution:** Owner will produce the exact route-and-version diff (Barint master bari-web/ vs bari/main) before §8 decisions are signed. §8 item 3 (bundle vs sequence) is not actionable until that enumerated list exists. Yogurts must be flagged as a hold candidate at Phase 2 pending the contamination ruling — it should not silently ship under the v3 label if the corpus is OFF-born.

**Impact:** §8 decisions 3 and 5 (launch bundle + Vercel re-point authorization) are blocked pending the full payload diff. Phase 0 is independent and unblocked.

### Gap 3 — Registry coherence: TASK-242 no-merge clause must be superseded

**Problem:** TASK-242 `close_reason` says "do not merge the branch." Phase 1 merges it. Without a registry record, this recreates the TASK-238-style contradiction (a closed task's ruling violated by a subsequent action with no audit trail).

**Resolution:** A new task (next free ID after TASK-244, tentatively **TASK-245**) is registered for the re-point program before any Phase 0 or Phase 1 execution. Its record:
- Explicitly states that it supersedes the TASK-242 no-merge clause for the purpose of merging `release/prod-integrity-242` into Barint master (Phase 1), citing the owner's Option C ruling from this document.
- Carries the Phase 0, Phase 1, Phase 2, Phase 3, and Phase 4 scope as sub-tasks.
- Is the authoritative registry record for the full re-point execution.
- Phase 0 sub-tasks may be registered as separate tasks (TASK-246, TASK-247) if scope warrants, or inline as sub-items of TASK-245.

### Gap 4 — Phase 3 needs a dress rehearsal, not just a rollback story

**Problem:** The brief's Phase 3 rollback story ("2-minute Vercel setting revert") addresses recovery but not pre-flight validation. Local build green ≠ Vercel-infra green. Risk factors: env vars not replicated (`NEXT_PUBLIC_GLASSBOX_D5D6` and others), Root Directory not set to `bari-web/`, production branch name mismatch (Barint uses `master`, not `main`), node/lockfile version differences.

**Resolution:** Before touching the production Vercel project `bari`, create a **throwaway second Vercel project** pointed at Argento17/Barint with Root Directory `bari-web/`, production branch `master`, and a copy of all env vars. This produces a full preview URL of the post-re-point production state on real infra, validates the build pipeline end-to-end, and confirms env var replication. Only after the throwaway project's preview URL passes the §4 smoke test checklist does Phase 3 proceed to edit the live `bari` project. The throwaway project is deleted after Phase 3 completes. This adds ~30 minutes of validation time but eliminates the infra-config risk class entirely.

---

## 10. Revised Phase Summary (post-gap resolution)

| Phase | Action | Blocking dependency | Tripwire #2 |
|---|---|---|---|
| **Task reg** | Register TASK-245 (re-point program) + Phase 0 sub-tasks; supersede TASK-242 no-merge clause | None | No |
| **Phase 0** | Port 4 defect fixes to Argento17/bari@main (OFF-image nulls: cereals/granola; snacks confidence 4-row; yogurts ruling TBD) | TASK-245 registered | No |
| **Phase 1** | PR: `release/prod-integrity-242` → Barint master; resolve conflicts; gate green (`tsc` + `next build`) | Phase 0 can run in parallel | No |
| **Phase 2 prep** | Produce full route/version diff (owner) | Phase 1 merged | None |
| **Phase 2** | Owner sign-off on enumerated launch payload (salty-snacks, hard-cheeses, juices, blog posts, yogurts ruling) | Diff in hand | **YES — each item** |
| **Phase 3a** | Throwaway Vercel project → Argento17/Barint, root `bari-web/`, preview URL smoke test | Phase 2 signed | No |
| **Phase 3b** | Edit live Vercel project `bari` → Argento17/Barint, root `bari-web/`, master branch | Phase 3a passes | **YES — platform** |
| **Phase 4** | TASK-243 (image backfill), TASK-244 (DA-013 structural fix) fast-follows | Phase 3b live | No |
