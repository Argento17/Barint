import { SNACK_REPORT_STATS } from "@/lib/comparisons/snack-page-data";

export function SnackShelfStatBar() {
  return (
    <div className="flex flex-wrap gap-x-6 gap-y-2 border-y border-black/[0.06] py-4 text-sm text-[#4E5663]">
      <span>
        <strong className="text-[#111318]">{SNACK_REPORT_STATS.scraped}</strong> נסרקו
      </span>
      <span>
        <strong className="text-[#111318]">{SNACK_REPORT_STATS.scored}</strong> קיבלו ציון
      </span>
      <span>
        טווח <strong className="text-[#111318]">{SNACK_REPORT_STATS.scoreRange}</strong>
      </span>
      <span>
        <strong className="text-[#111318]">{SNACK_REPORT_STATS.displayed}</strong> מוצגים
      </span>
      <span>{SNACK_REPORT_STATS.retailer}</span>
      <span>{SNACK_REPORT_STATS.snapshotDate}</span>
    </div>
  );
}
