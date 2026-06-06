# Decisions Ledger — C:\Bari\decisions\

**Authoritative source:** `decisions.json` (append-only)  
**Architectural decisions:** `adr/` subdirectory  
**Schema reference:** this file

---

## Two-tier decision record

| Tier | What it captures | File |
|---|---|---|
| **Operational decisions** | Task-gating, go/no-go, calibration sign-offs, scope rulings | `decisions.json` |
| **Architectural decisions** | Why a design principle, agent lane, or system contract was chosen | `adr/ADR-NNN.md` |

Operational decisions are short-lived (PENDING → DECIDED → optionally RETIRED).  
ADRs are permanent — the record of reasoning survives even after the code changes.

---

## decisions.json — enhanced schema (applies to all new entries)

Required fields:

```jsonc
{
  "id": "DEC-NNN",                  // Next sequential DEC id
  "title": "...",                   // One-line title
  "type": "go_nogo_gate|calibration_signoff|scope_definition|provenance_exception|governance_posture|routing_rule",
  "required_from": "<agent-slug>",  // Who holds decision authority
  "status": "PENDING|DECIDED|RETIRED",
  "options": ["A — ...", "B — ..."],
  "recommendation": "Option X — <agent> (<TASK-NNN>): one-line rationale",
  "decided_at": "YYYY-MM-DD",       // null while PENDING
  "decision": "...",                // The ruling, verbatim
  "urgency": "NOW|THIS_WEEK|THIS_SPRINT|BACKLOG",
  "blocking": ["TASK-NNN", "..."],

  // --- Enhanced fields (required from DEC-007 onwards) ---
  "authority_tier": "owner|product-agent|cc-agent|nutrition-agent|other",
                                    // Who actually holds the decision right
  "tripwire_eval": {                // Was a strategic tripwire evaluated?
    "fired": false,                 // true if any of the 5 tripwires fired
    "wire": null,                   // 1–5 or null
    "reasoning": "No wire fired — reversible behind flag, internal only."
  },
  "reasoning_chain": [              // Ordered steps that led to the decision
    "Constraint: ...",
    "Option A risk: ...",
    "Option B risk: ...",
    "Tiebreaker: ..."
  ],
  "reversibility": "two-way|one-way",
                                    // two-way = flag/PR/draft; one-way = public/shipped
  "rollback_path": "...",           // What undoes this if wrong (null if one-way)
  "related_adr": null,              // ADR-NNN if an ADR was also written
  "created_at": "YYYY-MM-DD",
  "notes": "..."
}
```

Legacy fields (DEC-001–DEC-006) are retained as-is. Do not retroactively amend them.

---

## When to write an ADR vs. a DEC entry

| Situation | Write |
|---|---|
| Task-gating: does X go-live? | DEC entry |
| Calibration sign-off: accept these numbers? | DEC entry |
| Go/no-go on a program wave | DEC entry |
| Why BSIP2 uses this scoring architecture | ADR |
| Why the CC Agent holds closing authority (not Product) | ADR |
| Why the autonomy-default rule replaced the escalation default | ADR |
| Why the red-team agent is separate from QA | ADR |
| Why decisions.json is append-only | ADR |

Rule of thumb: if someone will ask "why did we design it this way?" six months from now, write an ADR. If they'll ask "what was decided about this task?" write a DEC entry.

---

## ADR format

See `adr/ADR-000-template.md` for the canonical template.

ADR status lifecycle: `Proposed → Accepted → Superseded (by ADR-NNN) → Deprecated`

ADRs are **never deleted** — if a decision is reversed, the old ADR is superseded, not removed.

---

## Append-only rule

`decisions.json` is append-only. To update:
- **Status change** (PENDING → DECIDED): add `decided_at` + `decision` fields to the existing entry in-place — this is the one permitted mutation.
- **Retirement** (DECIDED → RETIRED): add `retired_at` + `retired_by` + `retirement_note` to the existing entry.
- **Never delete** an entry. Never re-use a DEC-NNN id.

The dashboard generator reads `decisions.json` — any structural break will surface as a parse error at next regen.

---

## ID allocation

- DEC-NNN: next sequential from the current maximum in decisions.json
- ADR-NNN: next sequential from the current maximum in adr/
- Never skip or reuse an id from either sequence.
