/**
 * TASK 2 — Reusable "not medical advice" disclaimer.
 * Add to any page that shows nutritional or supplement information.
 * Text is approved editorial boilerplate (structural only — no legal opinion).
 */

export function NotMedicalAdvice({ className }: { className?: string }) {
  return (
    <p
      dir="rtl"
      className={
        "text-[11px] leading-relaxed text-[#6B7070] " + (className ?? "")
      }
    >
      המידע באתר זה הוא לצורכי השכלה כללית בלבד ואינו מהווה ייעוץ רפואי,
      תזונתי או פרמקולוגי. לפני שינוי תזונה או נטילת תוספים, יש להתייעץ עם
      אנשי מקצוע בתחום הבריאות.
    </p>
  );
}
