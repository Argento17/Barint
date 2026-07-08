// Bari internal-traffic detection (TASK-522).
//
// Purpose: let both measurement layers (Vercel Web Analytics `beforeSend`
// and the GA4 `traffic_type` config param) exclude owner/agent/dev traffic
// from the numbers the owner reads, without touching consent posture or
// adding a new provider. Read-only signal — never blocks rendering, never
// gates a feature, never sent as a user identifier.
//
// Detection is either of:
//   1. Automatic: localhost / 127.0.0.1 / *.vercel.app preview hostnames —
//      always internal, no flag needed.
//   2. Manual, persistent: visiting with `?bari_internal=1` sets a localStorage
//      flag that survives future visits without the query param (e.g. a
//      bookmarked owner link); `?bari_internal=0` clears it again.
//
// Client-only. Server/SSR calls return false (no window → no signal to read).

const INTERNAL_FLAG_KEY = "bari-internal-traffic";

/** Applies the `?bari_internal=` query flag as a side effect. Idempotent —
 * safe to call on every page view / beforeSend invocation. */
function applyQueryFlag(): void {
  if (typeof window === "undefined") return;
  const params = new URLSearchParams(window.location.search);
  const flag = params.get("bari_internal");
  if (flag === "1") {
    try {
      localStorage.setItem(INTERNAL_FLAG_KEY, "1");
    } catch {
      // private browsing — flag just won't persist; this page load is still
      // covered by the automatic hostname check below if applicable.
    }
  } else if (flag === "0") {
    try {
      localStorage.removeItem(INTERNAL_FLAG_KEY);
    } catch {
      // no-op
    }
  }
}

function isInternalHostname(): boolean {
  if (typeof window === "undefined") return false;
  const host = window.location.hostname;
  return host === "localhost" || host === "127.0.0.1" || host.endsWith(".vercel.app");
}

function hasInternalFlag(): boolean {
  if (typeof window === "undefined") return false;
  try {
    return localStorage.getItem(INTERNAL_FLAG_KEY) === "1";
  } catch {
    return false;
  }
}

/**
 * Returns true if the current client should be treated as internal
 * (owner/agent/dev) traffic and excluded from reported numbers.
 */
export function isInternalTraffic(): boolean {
  applyQueryFlag();
  return isInternalHostname() || hasInternalFlag();
}
