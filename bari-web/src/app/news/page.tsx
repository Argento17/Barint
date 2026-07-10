import type { Metadata } from "next";

import { NewsIndexPage } from "@/components/news/news-index-page";
import { newsIndex } from "@/lib/news/news-index-content";

export const metadata: Metadata = {
  title: "חדשות · Bari Food Intelligence",
  description: `${newsIndex.subtitle} ${newsIndex.supporting}`,
};

export default function NewsIndexRoute() {
  return <NewsIndexPage />;
}
