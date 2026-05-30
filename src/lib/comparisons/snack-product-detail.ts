import type {
  SnackCompositionRow,
  SnackProduct,
  SnackScoreDriverRow,
  SnackWhyLanded,
} from "@/lib/comparisons/snack-types";

export function buildSnackWhyLanded(product: SnackProduct): SnackWhyLanded {
  const highlight_he = product.key_observation_he;

  const limit_he =
    product.score != null && product.score < 60
      ? product.caps_applied.length
        ? `מגבלות שהופעלו: ${product.caps_applied.join(" · ")}`
        : `עומק עיבוד (${product.nova ? `NOVA${product.nova}` : "—"}) ו${product.sweetener_pattern} ממתיקים הגבילו את הציון.`
      : undefined;

  const uncertainty_he =
    product.confidence_level === "partial"
      ? "חלק מנתוני הרכיבים חסרים או לא אומתו במלואם — הפרשנות מסומנת כחלקית."
      : product.confidence_level === "insufficient"
        ? "אין מספיק נתוני רכיבים לפרשנות מלאה."
        : undefined;

  return { highlight_he, limit_he, uncertainty_he };
}

export function buildSnackComposition(product: SnackProduct): SnackCompositionRow[] {
  return [
    {
      dimension: "מקור בסיס",
      value: product.structural_base,
      effect_he:
        product.structural_base === "בסיס שלם"
          ? "בסיס שלם תמך בציון."
          : product.structural_base === "בסיס מעובד"
            ? "בסיס מעובד הוריד את התקרה."
            : "בסיס מהונדס משך את המוצר לקצה התחתון.",
    },
    {
      dimension: "ארכיטקטורת סוכר",
      value: product.sweetener_pattern,
      effect_he:
        product.sweetener_pattern === "מקור יחיד"
          ? "מקור מתיקות יחיד — יציב יותר."
          : product.sweetener_pattern === "2 מקורות"
            ? "שני מקורות ממתיקים — בינוני."
            : "3+ מקורות ממתיקים — דפוס מחליש.",
    },
    {
      dimension: "עומק עיבוד",
      value: product.nova ? `NOVA${product.nova}` : "—",
      effect_he:
        product.nova === 2
          ? "עיבוד מינימלי."
          : product.nova === 3
            ? "עיבוד בינוני."
            : "NOVA4 — תקרת ציון D–E.",
    },
    {
      dimension: "עומס תוספות",
      value: product.additive_load,
      effect_he:
        product.additive_load === "0–2"
          ? "עומס תוספות נמוך."
          : product.additive_load === "3–4"
            ? "עומס תוספות בינוני."
            : "5+ תוספות פונקציונליות.",
    },
    {
      dimension: "התאמת שם למבנה",
      value: product.positioning,
      effect_he:
        product.positioning === "טבעי/תמרים" && product.nova === 4
          ? "פער מיצוב: 'תמרים' מול NOVA4."
          : product.positioning === "פרוטאין" || product.positioning === "פיטנס"
            ? "מיצוב לא עקף את מגבלות העיבוד."
            : "השם על האריזה תואם יחסית למבנה.",
    },
  ];
}

export function buildSnackScoreDrivers(product: SnackProduct): SnackScoreDriverRow[] {
  const drivers: SnackScoreDriverRow[] = product.explainability_tags.map((tag) => ({
    driver: tag,
    impact_he: tag.includes("NOVA4") || tag.includes("תוספות") || tag.includes("ממתיקים")
      ? "מחליש"
      : tag.includes("לא נוקד")
        ? "לא ניתן לניקוד"
        : "תומך",
  }));

  product.caps_applied.forEach((cap) => {
    drivers.push({ driver: cap, impact_he: "תקרה" });
  });

  return drivers;
}
