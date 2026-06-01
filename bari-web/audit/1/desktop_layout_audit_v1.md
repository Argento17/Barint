# Desktop Layout Audit v1

Audit date: 2026-05-29  
Scope: why `/hashvaot/snacks` renders as a narrow mobile/phone-frame layout on desktop  
Mode: forensic audit only. No code changes.

## Verdict

The narrow desktop layout is intentional according to the frozen Comparison UI Reference v1 and the shared implementation. It is not a Snacks-only regression.

Classification: intended by frozen v1, but strategically wrong or unresolved if Bari now expects a production-grade desktop comparison experience.

## Implementation Evidence

`src/components/comparisons/comparison-shelf-page.tsx` renders the shared shelf shell for Snacks and Maadanim.

Relevant classes:

```tsx
<div className="min-h-screen bg-[#EFEFEB] flex justify-center py-0 sm:py-10" dir="rtl">
  <div className="w-full sm:max-w-[375px] bg-white sm:rounded-[2rem] sm:shadow-2xl overflow-hidden">
```

Effect:

- Mobile: `w-full`
- Desktop (`sm+`): `sm:max-w-[375px]`
- Desktop wrapper adds rounded corners and shadow.
- The page is centered with a phone-frame width.

Because Snacks uses `ComparisonShelfPage`, the same desktop limitation applies to `/hashvaot/snacks`.

## Reference Evidence

`docs/comparison_ui_reference_v1.md` explicitly defines this as the frozen design:

- "Top-to-bottom inside the phone frame (single column, RTL)"
- Desktop (`sm+`): `max-w-[375px]`, `rounded-[2rem]`, `shadow-2xl`, `py-10`
- "Phone frame: 375px max width — editorial shelf prototype, not full-bleed desktop table."
- "375px phone frame on desktop — Do not expand shelf to full desktop grid without a new reference version."

## Route Impact

| Route | Uses shared phone-frame shell? | Result |
|---|---:|---|
| `/hashvaot/maadanim` | Yes | Desktop phone frame. |
| `/hashvaot/snacks` | Yes | Desktop phone frame. |
| `/hashvaot/bread` | Yes, based on the shared wrapper pattern | Desktop phone frame expected. |

## Classification

| Classification option | Result |
|---|---|
| Intended but strategically wrong | Yes. The reference requires it, but the user's production observation shows it may no longer be acceptable. |
| Implementation bug | No evidence. The implementation matches the reference. |
| Regression | No evidence. The same shared shell is used by Maadanim and Snacks. |
| Unresolved product decision | Yes. If production desktop should not look like a phone prototype, a new reference/design decision is required. |

## Production Acceptability

The layout is compliant with Comparison UI Reference v1. It is not acceptable as a full desktop production comparison experience unless Bari explicitly accepts the phone-frame editorial prototype as production desktop behavior.

## Desktop Layout Verdict

Do not classify this as a Snacks implementation bug. Classify it as a stop-ship product/design decision: v1 intentionally freezes a 375px phone frame on desktop, and that constraint now conflicts with the observed production expectation.
