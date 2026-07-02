/**
 * Bari community links — single source of truth (TASK-467).
 *
 * `href` values ship as empty placeholders. The owner supplies real
 * community links later. Every consumer of `communityLinks` MUST filter
 * out entries with an empty `href` so nothing renders until links land:
 *
 *   communityLinks.filter((l) => l.href !== "")
 *
 * Platform is restricted to the three approved channels (WhatsApp is
 * primary — ~99% penetration in Israel; Instagram/Facebook are secondary).
 * No X/Twitter, no email, no icon-soup rows — see TASK-467 design direction.
 */

export type CommunityPlatform = "whatsapp" | "instagram" | "facebook";

export interface CommunityLink {
  id: string;
  /** Hebrew display label. */
  label: string;
  /** Destination URL. Empty string = not yet supplied by the owner. */
  href: string;
  platform: CommunityPlatform;
}

export const communityLinks: CommunityLink[] = [
  { id: "whatsapp", label: "וואטסאפ", href: "", platform: "whatsapp" },
  { id: "instagram", label: "אינסטגרם", href: "", platform: "instagram" },
  { id: "facebook", label: "פייסבוק", href: "", platform: "facebook" },
];

/** Community links with a real URL supplied. Renders nothing when empty. */
export function activeCommunityLinks(): CommunityLink[] {
  return communityLinks.filter((link) => link.href !== "");
}

/**
 * Share message builder — DRAFT COPY, gate-pending (owner content sign-off +
 * Adversarial QA two-gate; see CLAUDE.md "Content sign-off"). Do not treat
 * this string as final consumer-facing copy; it is a functional placeholder
 * so the share feature is testable before copy is approved.
 */
export function buildShareText(title: string): string {
  return `בדיקת ${title} של ברי`;
}

/**
 * Builds a `wa.me` share URL: draft share text + a line break (`%0A`) + the
 * page URL, each percent-encoded independently so the literal `%0A` line
 * break is preserved (encodeURIComponent must not touch it).
 */
export function buildWhatsAppShareUrl(title: string, url: string): string {
  const encodedText = encodeURIComponent(buildShareText(title));
  const encodedUrl = encodeURIComponent(url);
  return `https://wa.me/?text=${encodedText}%0A${encodedUrl}`;
}
