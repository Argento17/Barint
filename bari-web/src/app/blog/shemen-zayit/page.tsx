import type { Metadata } from "next";

import { OliveOilArticle } from "@/components/blog/olive-oil-article";

export const metadata: Metadata = {
  title: "13 שמני זית. כולם מקבלים אותו ציון. | Bari",
  description:
    "בדקנו את כל שמני הזית הכתיים במדף שופרסל. אף מוצר לא מצהיר על תאריך קציר. הניתוח מסביר למה — ומה כדאי לחפש.",
};

export default function OliveOilBlogPage() {
  return <OliveOilArticle />;
}
