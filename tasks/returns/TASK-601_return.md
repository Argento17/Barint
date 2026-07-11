# TASK-601 Return

Proposed status: RETURNED.

Created the authoritative BSIP0 capture manifest and replay baseline. The census derives
893 total captures from the manifest: 807 canonical, 86 explicitly superseded, and 652
distinct GTINs among canonical records. The served comparison files contain 359/757
products with a canonical capture and 398/757 without one; the full shelf breakdown is
in `03_operations/reports/task601_bsip0_census.md`.

Verification completed: all three scripts compile; manifest and baseline build succeeded;
the committed-baseline replay check exited 0; and the known-capture check confirmed
3075805 sodium `1,628` is `comma_ambiguous` while 5010029000061 fat replays with no flags.

Files changed (verify):

- `03_operations/bsip0/manifest/build_manifest.py`: membership, provenance, and dedup policy.
- `03_operations/bsip0/manifest/replay_harness.py`: canonical replay, diff gate, focused check.
- `03_operations/bsip0/manifest/build_census.py`: served-corpus census generator.
- `03_operations/bsip0/manifest/capture_manifest.json`: authoritative corpus artifact.
- `03_operations/bsip0/manifest/replay_baseline.jsonl`: committed flat replay baseline.
- `03_operations/reports/task601_bsip0_census.md`: coverage census and distribution marker.

```json
{
  "task": "TASK-601",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path":"03_operations/bsip0/manifest/build_manifest.py","action":"created","sha256":"f9d9595e9e262ce89cd185905a004a91b9d957a0387c6cafa7d2c3f0328588c8"},
    {"path":"03_operations/bsip0/manifest/replay_harness.py","action":"created","sha256":"19d95f4c14e2a8c80ebd07ed98e086871baad22207b6cf74659cc6bd35ace9a6"},
    {"path":"03_operations/bsip0/manifest/build_census.py","action":"created","sha256":"787516a24b814b4046290336b4ab140520259b072b5c63a31183fbaebd4b3334"},
    {"path":"03_operations/bsip0/manifest/capture_manifest.json","action":"created","sha256":"6602460d88642cef0d4d8407cbf36de88b081463651b69d261c7e89ba2b72c73"},
    {"path":"03_operations/bsip0/manifest/replay_baseline.jsonl","action":"created","sha256":"94d1330699dbd30de8d95514064a424f29b04fe90df83cfd0a975b0f41019d20"},
    {"path":"03_operations/reports/task601_bsip0_census.md","action":"created","sha256":"b1f0679087790fd608bd31513f913d7889925dc8a33df679cc224792429a53f9"}
  ],
  "counts": {
    "captures":"893/893 manifest records; canonical=807/893, superseded=86/893, distinct_gtins=652/807 canonical records",
    "served_coverage":"HAS_CANONICAL_CAPTURE=359/757 served products from 20 comparison JSON files; NO_CAPTURE=398/757",
    "retailer_distribution":"shufersal=242/893 captures; unknown=651/893 captures",
    "replay_distribution":"8070/8070 canonical-capture×field baseline rows; flagged=38/8070; histogram={comma_ambiguous:37,out_of_bound:1}; most_common=comma_ambiguous(37)"
  },
  "commands_run": [
    {"cmd":"python -m py_compile 03_operations/bsip0/manifest/build_manifest.py 03_operations/bsip0/manifest/replay_harness.py 03_operations/bsip0/manifest/build_census.py","exit_code":0},
    {"cmd":"python 03_operations/bsip0/manifest/build_manifest.py","exit_code":0},
    {"cmd":"python 03_operations/bsip0/manifest/replay_harness.py","exit_code":0},
    {"cmd":"python 03_operations/bsip0/manifest/replay_harness.py --check","exit_code":0},
    {"cmd":"python 03_operations/bsip0/manifest/replay_harness.py --self-check","exit_code":0},
    {"cmd":"python 03_operations/bsip0/manifest/build_census.py","exit_code":0}
  ],
  "not_done": [],
  "self_check":"Replay baseline check passed at 8070 rows; known-capture check passed for brined 3075805 sodium comma_ambiguous and cereals 5010029000061 fat with no flags."
}
```
