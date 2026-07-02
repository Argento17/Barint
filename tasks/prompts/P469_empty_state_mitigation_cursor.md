# P469 / TASK-463 frontend mitigation: never assert "no material limiting factors" from absent data (route: C1-CURSOR)

## 1. Context
- You are ALREADY in isolated worktree `C:\bari_wt_t463`, branch `fix/task463-empty-state-mitigation`, cut from origin/master `346e74fa`. Never touch `C:\Bari`. Commit here; NO push/PR. Run `npm ci` in `bari-web\` first.
- Live defect (owner-caught, orchestrator-verified, root-caused in `C:\Bari\tasks\reports\task463_limitingfactors_rootcause_2026-07-02.md` — read it first): 100/580 live products carry EMPTY `expansion.limitingFactors` (bread 23/23 + cheese 47/47 wholesale — their explanation step never ran; plus low-grade partials down to E 33.7). The shared renderer `bari-web/src/components/shared/expansion-section.tsx` (~line 585-600) shows a green check + "אין גורמים מגבילים מהותיים" whenever the array is empty — a false positive claim for a D/E product, live on comparison pages AND /catalog (catalog reuses the same VMs). Additionally `positiveSignals` is empty on 262/580 products.

## 2. Objective — one uniform display rule: absent data says NOTHING
In `expansion-section.tsx`:
1. **Limiting-factors column:** when `limitingFactors` is empty → render NO claim. Collapse that column/panel content entirely (no green check, no text). Keep layout sane when the sibling positives column still has content (and vice versa); if BOTH sides are empty, collapse the whole assessment block (there is already a `hasAssessment` notion ~line 1182 — extend it so empty-empty renders nothing rather than two hollow columns).
2. **Positives column:** check its empty-state (~same section). If it asserts anything when `positiveSignals` is empty, apply the same say-nothing collapse. If it already renders nothing, leave it and note that in the return.
3. **Uniform rule, no carve-outs:** no per-category or per-product exceptions (uniform-baseline doctrine). Yes, this also hides the line for genuinely-clean top-A products — asserting from data we cannot distinguish is worse; the data fix post-freeze restores richer states.
4. Section header behavior: if "מה מגביל את הציון?" (or equivalent heading) would now sit above nothing, it must not render either. Verify by real render, not just code reading: `npm run dev` or a build + local serve, open one bread product expansion (all-empty), one cheese D product, one hummus product (has factors — must be UNCHANGED), and the /catalog expansion for a bread product. Screenshot or DOM-quote each in the return.

## 3. Boundaries
- **Component logic ONLY. Do NOT edit any JSON data file, any product copy, any Hebrew string content** (removing a rendered element is allowed; changing/adding consumer wording is NOT — owner description freeze in force).
- No changes to any other component unless the collapse forces a minimal prop-type touch (list every file). No visual redesign — spacing/geometry of the remaining content stays as-is.
- OFF ban absolute. You are the EXECUTOR — do NOT spawn subagents.

## 4. Gates + return
`npm run lint` exit 0, `npx tsc --noEmit` exit 0, `npm run build` exit 0 (all in `bari-web\`). Return to `tasks\returns\P469_contract.md` (NOT P469_return.md): the render-verification evidence (4 cases above), files touched with real sha256s, counts with denominators. Full Return Contract v1 JSON. Self-gate: `python 03_operations\validators\validate_return.py --md tasks\returns\P469_contract.md --root C:\bari_wt_t463` exit 0 (PowerShell). Commit code + contract. Propose RETURNED.
