# P466 Contract — TASK-462 rework: restore SSR hydration safety in consent/GA4 boot reads

**Worktree:** `C:\bari_wt_t462b` (branch `ci/task462-green-eslint`)
**Status proposed:** RETURNED

## Summary

Reverted P465 lazy useState initializers that read localStorage during the first render (hydration mismatch). Both files now start with SSR-safe initial state (hidden / false); the localStorage read runs post-mount in useEffect, with tagged eslint-disable-next-line react-hooks/set-state-in-effect per TASK-462 spec.

## Hydration safety (inspection)

| file | initial state line | browser API before mount? |
|------|-------------------|---------------------------|
| consent-manager.tsx | const [view, setView] = useState<CMPView>("hidden"); (line 68) | No — getStoredConsent() only in useEffect boot (line 76+) |
| ga4-script.tsx | const [granted, setGranted] = useState(false); (line 45) | No — getStoredConsent() only in useEffect (line 69+) |

Server and client first render both emit null for these components; banner/GA4 script appear only after mount effect.

## eslint-disable additions

| file:line | rule | tag |
|-----------|------|-----|
| bari-web/src/components/shared/consent-manager.tsx:78 | react-hooks/set-state-in-effect | TASK-462: post-mount boot read from localStorage, SSR-hydration-safe by design |
| bari-web/src/components/shared/ga4-script.tsx:71 | react-hooks/set-state-in-effect | TASK-462: post-mount boot read from localStorage, SSR-hydration-safe by design |

## Gate outputs

| # | command | exit |
|---|---------|-----:|
| 1 | npm run lint (in bari-web/) | 0 |
| 2 | npx tsc --noEmit (in bari-web/) | 0 |
| 3 | npm run build (in bari-web/) | 0 |

## Files changed

| file | action |
|------|--------|
| bari-web/src/components/shared/consent-manager.tsx | modified — restore mount-effect boot + tagged disable |
| bari-web/src/components/shared/ga4-script.tsx | modified — restore mount-effect boot + tagged disable |

```json
{
  "task": "P466",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "bari-web/src/components/shared/consent-manager.tsx", "action": "modified", "sha256": "94a8b3f16146cecd892a80ed2dda83a41b3095fd1507e93c11616ff92b96390d"},
    {"path": "bari-web/src/components/shared/ga4-script.tsx", "action": "modified", "sha256": "38645fafd780121cc760fe44f8aa906e9fff2afae10b251eafba689eb799f62b"}
  ],
  "counts": {
    "eslint_disable_additions": "2/2 (consent-manager.tsx:78, ga4-script.tsx:71; rule react-hooks/set-state-in-effect; tag TASK-462)",
    "eslint_errors_after": "0/0 (npm run lint in bari-web/; 18 warnings remain, 0 errors)",
    "files_touched": "2/2 (P466 scope: consent-manager.tsx, ga4-script.tsx only)"
  },
  "commands_run": [
    {"cmd": "npm run lint (in bari-web/)", "exit_code": 0},
    {"cmd": "npx tsc --noEmit (in bari-web/)", "exit_code": 0},
    {"cmd": "npm run build (in bari-web/)", "exit_code": 0},
    {"cmd": "python 03_operations\\validators\\validate_return.py --md tasks\\returns\\P466_contract.md --root C:\\bari_wt_t462b", "exit_code": 0}
  ],
  "not_done": [],
  "self_check": "Initial state is hidden/false with no render-time localStorage read; npm run lint exits 0; build succeeds"
}
```
