# P466 / TASK-462 rework of P465: two lint fixes introduced SSR hydration mismatches (route: C1-CURSOR)

## 1. Context
- Worktree `C:\bari_wt_t462b`, branch `ci/task462-green-eslint`, on top of your commit `b562e4d7`. P465 was verified good EXCEPT two files. Never touch `C:\Bari`. Commit here; NO push/PR.
- The defect (orchestrator verification): you replaced effect-based boot reads with lazy `useState` initializers that read `localStorage` during first render:
  - `bari-web/src/components/shared/consent-manager.tsx` — server renders `null` (`view` starts "hidden", line ~146 `if (view === "hidden") return null`), but the client's hydration render computes `"banner"` for any visitor without stored consent → **hydration mismatch for every first-time visitor**.
  - `bari-web/src/components/shared/ga4-script.tsx` — server renders `null` (`granted` false), client hydration render computes `granted=true` for consented returning visitors (line ~80 `if (!GA_ID || !granted) return null`) → **hydration mismatch for every consented visitor**.

## 2. Objective
Restore hydration safety in BOTH files: the first client render must equal the server render (state starts `"hidden"` / `false`; the localStorage read happens after mount, as the original code did). Then satisfy `react-hooks/set-state-in-effect` WITHOUT a render-time localStorage read. Preferred: the original mount-effect pattern with a targeted
`// eslint-disable-next-line react-hooks/set-state-in-effect -- TASK-462: post-mount boot read from localStorage, SSR-hydration-safe by design`
(the P465 spec explicitly permits tagged disables where the compliant refactor is unsafe). If you instead use `useSyncExternalStore`, its `getServerSnapshot` MUST return the server value ("hidden"/false) and you must keep the existing `onConsentChange` semantics intact. No other files.

## 3. Gates (all in `bari-web\`, exit codes in return)
1. `npm run lint` exit 0. 2. `npx tsc --noEmit` exit 0. 3. `npm run build` exit 0. 4. Prove hydration-safety by inspection in the return: quote the initial-state lines and state explicitly that no render path reads browser-only APIs before mount.

## 4. Return
`tasks\returns\P466_contract.md` (NOT P466_return.md). Full Return Contract v1 JSON, real sha256s for the 2 files, every eslint-disable listed (file:line + rule + tag). Self-gate: `python 03_operations\validators\validate_return.py --md tasks\returns\P466_contract.md --root C:\bari_wt_t462b` exit 0 (PowerShell). Commit code + contract. You are the EXECUTOR — do NOT spawn subagents. Propose RETURNED.
