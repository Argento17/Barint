# P458 / TASK-458 catalog go-live package: port /catalog to origin/master + nav + og:image + barcode search (route: C1-CURSOR)

## 1. Repo / paths / baseline
- Repo: `C:\Bari` (monorepo; website at `bari-web\`, Next.js App Router, Hebrew RTL).
- **Work in an ISOLATED WORKTREE — never touch the main working tree** (it is on `feature/homepage-mascots` and shared):
  ```
  git -C C:\Bari fetch origin
  git -C C:\Bari worktree add C:\bari_wt_t458 -b golive/catalog-task458 origin/master
  ```
  Record the origin/master SHA you branched from. All edits/builds/commits happen inside `C:\bari_wt_t458`.
- Read FIRST: `C:\Bari\tasks\TASK-458.md`. Context: the LIVE site advertises `/catalog` in its sitemap but the route 404s — the catalog feature exists only on the local `feature/homepage-mascots` branch. This dispatch ships it properly.

## 2. Objective — four pieces, one branch, separate commits
**(a) Port the catalog feature** from `feature/homepage-mascots` into the worktree: the `/catalog` route (`bari-web/src/app/catalog/`), the inventory lib (`bari-web/src/lib/inventory/`), the product-table components it imports, and ONLY their true dependencies. Cherry-pick or copy file-precise — do NOT drag mascot images, homepage changes, or any unrelated diff from that branch. The public variant only (admin surfaces stay out unless the public page imports them).

**(b) Header nav:** add a "קטלוג" entry to the site header/nav linking to `/catalog` (match existing nav item styling/order conventions; RTL-correct).

**(c) Sharing/OG fixes (highest-ROI SEO items):**
- Blog posts currently emit NO `og:image` — add one (use each post's existing thumbnail/hero asset if present; otherwise the site's default OG card). Verify on at least `/blog/food-dyes`.
- Comparison pages fall back to the site-generic `og:title`/`og:description` despite unique `<title>` — make each `/hashvaot/[category]` page emit its own og:title/og:description consistent with its metadata. Do NOT author new copy: derive from existing page metadata strings only.

**(d) Barcode search:** add `sku` to the catalog search haystack (`product-table.tsx` search fields) so a pasted EAN-13 finds the product. Trim/normalize whitespace on the query for the numeric case. No UI redesign.

**Build oracle:** inside the worktree run `npx tsc --noEmit` and the production build (`npm run build`) — both must pass. Run lint. Confirm `/catalog` renders (dev server or build output) and the sitemap entry now matches a real route.

## 3. Boundaries / guards
- **OFF ban absolute (TASK-238):** the catalog is registry-driven display-only — introduce NO new data source, NO external lookups, no Open Food Facts anywhere.
- Do NOT invent or edit product data, scores, or nutrition fields. Do NOT author new consumer-facing copy — if a string is needed (e.g., nav label uses existing conventions), keep it minimal and list every consumer-facing string you added/changed in the return: they go to the Content + Adversarial QA two-gate after you. FLAG (do not fix) the known honesty issue: the catalog title claims "כל המוצרים שבארי בדקה" while covering 7 of 17+ live categories — list it for the Content pass.
- 7 canonical components only; no new design patterns; frozen design tokens (see `bari-web/.claude/` if present).
- Commit locally on the worktree branch, one commit per piece (a)–(d); **do NOT push, do NOT open a PR, do NOT deploy.** Two gates + the owner sit between you and production.
- Do not modify the main tree, the registry, or the dispatch board.
- If the port surfaces a hard dependency on something not on origin/master, stop and return `proposed_status: BLOCKED` with the exact missing pieces — do not improvise substitutes.

## 4. Return format
Write your return to `C:\Bari\tasks\returns\P458_return.md`: per-commit summary (SHA, files), build/tsc/lint outputs (exit codes), the ported-file census (every file, its source commit on feature/homepage-mascots), the consumer-facing-strings list, the OG verification evidence (rendered meta tags for a blog post + a comparison page + /catalog), and anything not done. **Do not close the task — propose RETURNED** (or BLOCKED per above).

## 5. Machine-readable contract (mandatory, last block of the return)
```json
{
  "task": "P458",
  "proposed_status": "RETURNED | BLOCKED",
  "artifacts": [{"path": "...", "action": "created|modified|deleted", "sha256": "..."}],
  "counts": {"claim": "N/M (denominator source)"},
  "commands_run": [{"cmd": "...", "exit_code": 0}],
  "not_done": [],
  "self_check": "npm run build exit 0 AND npx tsc --noEmit exit 0 in the worktree: observed result here"
}
```
Rules of `01_framework\operations\return_contract_v1.md` apply: every file in `artifacts` with sha256, counts trace-derived with the deriving command in `commands_run`.
