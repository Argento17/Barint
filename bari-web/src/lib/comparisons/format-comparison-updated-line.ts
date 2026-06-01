/** Shared "עודכן …" label for comparison hero stats. */
export function formatComparisonUpdatedLine(generatedAt: string): string {
  const parsed = /^(\d{4})-(\d{2})-(\d{2})/.exec(generatedAt);
  if (!parsed) return "עודכן לאחרונה";
  const [, y, mo, d] = parsed;
  const gen = new Date(Number(y), Number(mo) - 1, Number(d));
  const now = new Date();
  const diffDays = Math.floor((now.getTime() - gen.getTime()) / (1000 * 60 * 60 * 24));
  if (diffDays >= 0 && diffDays <= 7) return "עודכן השבוע";
  const dateHe = `${d}.${mo}.${y}`;
  return `עודכן ב-${dateHe}`;
}
