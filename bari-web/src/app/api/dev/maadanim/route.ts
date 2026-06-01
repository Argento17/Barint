import { getComparisonCategoryCorpusPayload } from "@/lib/comparisons/registry";

export async function GET() {
  try {
    const payload = getComparisonCategoryCorpusPayload("maadanim");

    if (!Array.isArray(payload.products)) {
      return Response.json(
        { error: "Corpus is missing products array" },
        { status: 500 }
      );
    }

    return Response.json(payload);
  } catch (error) {
    return Response.json(
      {
        error: "Failed to load maadanim corpus",
        details: error instanceof Error ? error.message : String(error),
      },
      { status: 500 }
    );
  }
}
