// Pull-quote — build brief item 5. Renders a verbatim sentence, lifted from a paragraph
// already published in the data module, set large to break the text rhythm. The quote
// text itself is supplied by the caller from sweetener-guide-visuals.ts, which verifies
// verbatim-ness against the data module at import time; this component does not author or
// alter the string in any way (no truncation, no punctuation changes).

export function SweetenerPullQuote({ quote }: { quote: string }) {
  return (
    <p
      className="my-5 border-r-[3px] border-[#1E7A4F] py-1 pr-4 text-[1.15rem] font-bold leading-[1.45] tracking-[-0.015em] text-[#111318] sm:text-[1.3rem]"
      dir="rtl"
    >
      {quote}
    </p>
  );
}
