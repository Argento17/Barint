/**
 * Bari Consent Management — PPA Feb-2026 strict opt-in posture.
 *
 * Storage key: "bari-cookie-consent"
 * Schema: { version: 1, analytics: boolean, ts: number }
 *
 * GA4 / any analytics provider MUST NOT fire until `analytics === true`.
 * Essential cookies (session, security) are always implicitly on and are
 * not stored here — they need no consent under the ePrivacy directive.
 */

export const CONSENT_STORAGE_KEY = "bari-cookie-consent";
export const CONSENT_VERSION = 1;

export interface ConsentRecord {
  version: number;
  analytics: boolean;
  ts: number;
}

/** Returns the stored consent record, or null if the user has not yet chosen. */
export function getStoredConsent(): ConsentRecord | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(CONSENT_STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as Partial<ConsentRecord>;
    if (parsed.version !== CONSENT_VERSION) return null; // stale schema → re-ask
    return parsed as ConsentRecord;
  } catch {
    return null;
  }
}

/** Persists the user's choice and fires all registered listeners. */
export function saveConsent(analytics: boolean): ConsentRecord {
  const record: ConsentRecord = {
    version: CONSENT_VERSION,
    analytics,
    ts: Date.now(),
  };
  try {
    localStorage.setItem(CONSENT_STORAGE_KEY, JSON.stringify(record));
  } catch {
    // private browsing — consent is still applied in-memory for this session
  }
  // Notify all listeners (e.g. GA4Script component)
  for (const fn of listeners) {
    fn(record);
  }
  return record;
}

type ConsentListener = (record: ConsentRecord) => void;
const listeners: ConsentListener[] = [];

/** Register a callback that fires whenever consent is updated. Returns an unsubscribe fn. */
export function onConsentChange(fn: ConsentListener): () => void {
  listeners.push(fn);
  return () => {
    const idx = listeners.indexOf(fn);
    if (idx !== -1) listeners.splice(idx, 1);
  };
}
