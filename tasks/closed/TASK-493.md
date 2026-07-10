---
id: TASK-493
title: bari-web security hardening (Fable one-shot scan -> 3 MEDIUM fixes)
owner: frontend-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-03
closed_at: 2026-07-03
close_reason: >
  Done + verified. All 3 MEDIUM fixes implemented on branch security/admin-hardening
  (commit a150cc6f), pushed, PR #68 opened vs master
  (https://github.com/Argento17/Barint/pull/68). Verified: npx tsc --noEmit clean;
  npm run build exit 0 (all routes compiled, Next 16.2.6 accepted the config). M-1
  allowlist derived from the actual image hosts in the data (incl. 5 supplement hosts
  that were only under the removed **.co.il wildcard) so no live image breaks. LOWs
  intentionally deferred. Awaiting owner merge of PR #68.
depends_on: []
blocks: []
category_id: null
summary: >
  One-shot defensive security scan of bari-web run with Claude Fable: no CRITICAL/HIGH; 3 MEDIUM + 3 LOW. Fixed the 3 MEDIUMs (M-1 image-optimizer SSRF via co.il wildcard -> explicit allowlist + cloudinary /shufersal/ scope; M-2 security headers + admin anti-framing CSP; M-3 per-IP login brute-force throttle). LOWs deferred. tsc + build pass.
---

# TASK-493 — bari-web security hardening (Fable one-shot scan -> 3 MEDIUM fixes)

## Origin
Follow-up from the 2026-07-03 evaluation of an AI-industry digest — the one item
worth acting on was a one-shot LLM security scan of the Next.js surface (never done
before). Run as a background agent pinned to **Claude Fable** (defensive review of
own codebase; no refusal).

## Scan result
Full pass over all 14 route handlers, admin auth core, data loaders, image config,
and rendering sinks. **No CRITICAL, no exploitable HIGH.** Clean: admin write path
(auth-gated + strict field allowlist → no prototype pollution / arbitrary write),
secrets (env-only, gitignored, verified via `git ls-files`), the single
`dangerouslySetInnerHTML` (JSON-LD, safely escaped), no `fs` usage in `src/` → no
path-traversal surface. Findings were **3 MEDIUM + 3 LOW** hardening gaps.

## Fixes shipped (PR #68, branch security/admin-hardening)
- **M-1** SSRF via `/_next/image` — `next.config.ts` `**.co.il` whole-TLD wildcard
  replaced with explicit host allowlist; `res.cloudinary.com` scoped to `/shufersal/**`.
  Allowlist derived from a grep of actual image-field hosts; the 5 supplement hosts
  (tinc/teva-call/solgar/biogaya/altman) that lived only under the wildcard were added
  explicitly so nothing breaks.
- **M-2** No security headers — added `headers()`: nosniff + Referrer-Policy + HSTS
  site-wide; `X-Frame-Options: DENY` + CSP `frame-ancestors 'none'` on `/admin/*` and
  `/api/admin/*` (clickjacking defense for the write-to-prod editor).
- **M-3** No login brute-force protection — new `src/lib/admin/rate-limit.ts`, wired into
  `POST /api/admin/login`: per-IP sliding window (5/15min → escalating lockout), 429 +
  Retry-After. Per-instance in-memory (documented; KV upgrade path noted).

## Deferred (LOW, non-blocking)
Non-revocable 8h session token; password-length timing side-channel; JSON-LD escaping
(scan reviewed and rated fine). Full site-wide `script-src` CSP also deferred — needs
live testing vs GA/fonts/Cloudinary.

## Decision authority
No tripwire — reversible hardening on a branch behind a PR; doesn't touch scores or
consumer content. Owner asked to push + open PR; done. Merge is the owner's.

## Follow-up
Confirm `ADMIN_PASSWORD` is long/random (the scan noted brute-force feasibility hinges
on password strength). Optional: KV-backed cross-instance rate limit; the deferred LOWs.
