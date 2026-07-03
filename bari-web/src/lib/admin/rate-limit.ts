/**
 * Admin login brute-force throttle.
 *
 * The admin editor authenticates with a single shared password whose success
 * grants write-to-prod access, so unlimited guessing is the main risk. This is
 * an in-process, per-IP sliding-window limiter with escalating lockout.
 *
 * LIMITATION (by design, no infra dependency): state lives in the module's
 * memory, so it is per-serverless-instance and resets on cold start. It stops
 * the common single-source scripted attack and adds cost to a distributed one,
 * but it is NOT a globally-consistent limiter. Upgrade to a shared store
 * (Vercel KV / Upstash) if the threat model needs cross-instance guarantees.
 */

const WINDOW_MS = 15 * 60 * 1000; // rolling window for counting failures
const MAX_FAILURES = 5; // failures allowed in the window before lockout
const BASE_LOCK_MS = 5 * 60 * 1000; // first lockout duration
const MAX_LOCK_MS = 60 * 60 * 1000; // cap on escalated lockout
const PRUNE_AFTER_MS = 2 * 60 * 60 * 1000; // drop idle entries

type Attempt = {
  failures: number[]; // timestamps of recent failures (within window)
  lockedUntil: number; // epoch ms; 0 when not locked
  lockStreak: number; // consecutive lockouts, for exponential backoff
  lastSeen: number;
};

const attempts = new Map<string, Attempt>();

function prune(now: number): void {
  for (const [ip, a] of attempts) {
    if (now - a.lastSeen > PRUNE_AFTER_MS) attempts.delete(ip);
  }
}

function get(ip: string, now: number): Attempt {
  let a = attempts.get(ip);
  if (!a) {
    a = { failures: [], lockedUntil: 0, lockStreak: 0, lastSeen: now };
    attempts.set(ip, a);
  }
  a.lastSeen = now;
  return a;
}

/**
 * Extract a best-effort client IP from the request. On Vercel the real client
 * IP is the first entry of x-forwarded-for. Falls back to a shared bucket so a
 * missing header never disables throttling entirely.
 */
export function clientIp(request: Request): string {
  const xff = request.headers.get("x-forwarded-for");
  if (xff) {
    const first = xff.split(",")[0]?.trim();
    if (first) return first;
  }
  return request.headers.get("x-real-ip")?.trim() || "unknown";
}

/** Call BEFORE checking the password. Returns whether the attempt may proceed. */
export function checkRateLimit(
  ip: string,
  now: number = Date.now(),
): { allowed: boolean; retryAfterSec: number } {
  prune(now);
  const a = get(ip, now);
  if (a.lockedUntil > now) {
    return { allowed: false, retryAfterSec: Math.ceil((a.lockedUntil - now) / 1000) };
  }
  return { allowed: true, retryAfterSec: 0 };
}

/** Call AFTER a failed password check. May trip a lockout. */
export function recordFailure(ip: string, now: number = Date.now()): void {
  const a = get(ip, now);
  a.failures = a.failures.filter((t) => now - t < WINDOW_MS);
  a.failures.push(now);
  if (a.failures.length >= MAX_FAILURES) {
    a.lockStreak += 1;
    const lock = Math.min(BASE_LOCK_MS * 2 ** (a.lockStreak - 1), MAX_LOCK_MS);
    a.lockedUntil = now + lock;
    a.failures = []; // reset window; the lockout now governs
  }
}

/** Call AFTER a successful login to clear the IP's throttle state. */
export function recordSuccess(ip: string): void {
  attempts.delete(ip);
}
