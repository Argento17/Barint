// Responsive 16:9 video embed slot — build brief item 6. Uses youtube-nocookie.com (no
// tracking cookie until playback starts). `videoId` is a single swappable prop; the page
// currently passes the placeholder constant SWEETENER_VIDEO_ID ("VIDEO_ID_PENDING") from
// sweetener-guide-visuals.ts — trivial to swap once a real ID is supplied: the moment
// `videoId !== PENDING_ID`, this component switches from the placeholder branch to the
// real iframe branch automatically, no other call-site change needed.
//
// Placeholder state (coordinator fix, post-render review): the first cut rendered a black
// box with the raw string "VIDEO_ID_PENDING" — read as broken on the screenshot. Replaced
// with an in-brand "video will live here" card: same white rounded-card style as every
// other visual on this page, a centered green-gradient tile (same gradient formula as the
// section icons / bar chart fill) with a white play-triangle glyph, and one small muted
// line of UI chrome underneath. That line ("סרטון בקרוב") is NOT consumer/article copy —
// it is a build-status marker in the same class as the page's existing draft banner
// (role="status", same treatment), not a signed-off editorial string, and only ever shows
// while the placeholder ID is in place.

const PENDING_ID = "VIDEO_ID_PENDING";

export function SweetenerVideoEmbed({
  videoId,
  title,
}: {
  videoId: string;
  /** Accessible iframe title — pass an existing verbatim heading, not new copy. */
  title: string;
}) {
  const isPending = videoId === PENDING_ID;

  if (isPending) {
    return (
      <div className="mt-4 overflow-hidden rounded-xl border border-black/[0.08] bg-white">
        <div className="relative flex aspect-video flex-col items-center justify-center gap-3 bg-[#F7F7F2]">
          <div
            aria-hidden="true"
            className="flex size-14 items-center justify-center rounded-2xl shadow-[0_1px_2px_rgba(17,19,24,0.12)]"
            style={{ background: "linear-gradient(155deg, #1E7A4F, #0F5C42)" }}
          >
            <svg width="24" height="24" viewBox="0 0 24 24" role="presentation">
              <path d="M8 5.5v13l11-6.5-11-6.5Z" fill="white" />
            </svg>
          </div>
          {/* UI chrome, not article copy — same status-marker class as the draft banner. */}
          <span role="status" className="text-[11px] font-semibold tracking-[0.02em] text-[#8A857A]">
            סרטון בקרוב
          </span>
        </div>
      </div>
    );
  }

  return (
    <div className="mt-4 overflow-hidden rounded-xl border border-black/[0.08] bg-white">
      <div className="relative aspect-video">
        <iframe
          className="absolute inset-0 size-full"
          src={`https://www.youtube-nocookie.com/embed/${videoId}`}
          title={title}
          loading="lazy"
          allow="accelerometer; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
        />
      </div>
    </div>
  );
}
