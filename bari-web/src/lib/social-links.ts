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
  // WhatsApp Channel (owner-supplied 2026-07-02; Channel per TASK-467 research advisory)
  {
    id: "whatsapp",
    label: "וואטסאפ",
    href: "https://whatsapp.com/channel/0029VbDGpnr7j6g4xM62910s",
    platform: "whatsapp",
  },
  {
    id: "instagram",
    label: "אינסטגרם",
    href: "https://www.instagram.com/bari_nutrition/",
    platform: "instagram",
  },
  {
    id: "facebook",
    label: "פייסבוק",
    href: "https://www.facebook.com/profile.php?id=61591403370117",
    platform: "facebook",
  },
];

/** Community links with a real URL supplied. Renders nothing when empty. */
export function activeCommunityLinks(): CommunityLink[] {
  return communityLinks.filter((link) => link.href !== "");
}

/**
 * Share message builder. `title` is always the page's full editorial headline
 * (hero.title / article.title) — never a bare category name — so the template
 * uses the publisher-prefix idiom ("ברי בדקה: <headline>"), which stays
 * grammatical for statement, question, and multi-sentence headlines alike.
 *
 * Copy status: Content gate 1 signed off (TASK-467). Adversarial QA (gate 2)
 * still pending per CLAUDE.md "Content sign-off".
 */
export function buildShareText(title: string): string {
  return `ברי בדקה: ${title}`;
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
