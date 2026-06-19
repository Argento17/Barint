# Admin copy editor (`/admin`) — TASK-340

A login-gated, in-browser editor for the **sentences and captions** on the live
comparison pages. **Scores, grades and nutrition are never editable** — only
carry-safe copy fields are exposed.

## What you can edit

Per product, only the copy fields that the score-switch copy stage treats as
copy (so your edits survive the next re-score for grade-unchanged products):
`insightLine`, `rowVerdict`, `consumerTakeaway`, `consumerExplanation`,
`bestUseCases`, `expansion.comparisonContext`, `expansion.consumerExplanation`,
`expansion.bottomLine`, `expansion.caveats`, `expansion.unknowns`, and each
`bariInterpretation[].interpretation`.

The whitelist lives in [`src/lib/admin/fields.ts`](src/lib/admin/fields.ts).
Anything not on it — every score/grade/nutrition/confidence field — is rejected
server-side by `applyEdits`, so it cannot be written even via a crafted request.

## How it works

1. `/admin` shows a password wall. On success it sets an HMAC-signed, HttpOnly
   session cookie (8h).
2. The editor reads the **live** comparison JSON straight from the deploy repo
   (`Argento17/Barint`, branch `master`, dir `bari-web/src/data/comparisons`) so
   it always reflects what's deployed.
3. Save applies only whitelisted edits and **commits** the file back to the repo.
   Vercel rebuilds → live in ~2 minutes. The data file stays the single source
   of truth (no database, no drift).
4. Every save is a normal git commit, so any edit is reversible.

## Configuration (Vercel env / `.env.local`)

| Var | Purpose |
| --- | --- |
| `ADMIN_PASSWORD` | the editor login password |
| `ADMIN_SESSION_SECRET` | long random string used to sign sessions |
| `ADMIN_GITHUB_TOKEN` | GitHub fine-grained PAT, **Contents: read/write** on the deploy repo only |
| `ADMIN_GITHUB_REPO` | default `Argento17/Barint` |
| `ADMIN_GITHUB_BRANCH` | default `master` |

The editor **fails closed**: with no `ADMIN_PASSWORD`/secret, login is refused;
with no `ADMIN_GITHUB_TOKEN`, you can edit and preview but saving is blocked.

## Security notes

- The GitHub token is server-side only (route handlers); it is never sent to the
  browser. Scope it to **one repo, Contents only** — the minimum to commit copy.
- `/admin` is `noindex` (layout metadata) and disallowed in `robots.ts`.
- Login is timing-safe; the session cookie is HttpOnly + signed and cannot be
  forged without `ADMIN_SESSION_SECRET`.
