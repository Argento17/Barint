import { redirect } from "next/navigation";

import { SNACK_COMPARISON_HREF } from "@/lib/blog/snack-analysis-content";

export default function SnackBarsComparisonPage() {
  redirect(SNACK_COMPARISON_HREF);
}
