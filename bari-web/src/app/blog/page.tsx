import type { Metadata } from "next";

import { BlogIndexPage } from "@/components/blog/blog-index-page";
import { blogIndex } from "@/lib/blog/blog-index-content";

export const metadata: Metadata = {
  title: "בלוג Bari · Bari Food Intelligence",
  description: `${blogIndex.subtitle} ${blogIndex.supporting}`,
};

export default function BlogIndexRoute() {
  return <BlogIndexPage />;
}
