import { generateLlmsTxtBody } from "@/lib/seo/llms-content";

export const revalidate = 86400;

export function GET() {
  const body = generateLlmsTxtBody();
  return new Response(body, {
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "public, max-age=3600",
    },
  });
}
