import breadFaq from "@/data/seo/bread_faq_schema.json";
import breakfastCerealsFaq from "@/data/seo/breakfast_cereals_faq_schema.json";
import brinedCheesesFaq from "@/data/seo/brined_cheeses_faq_schema.json";
import cookiesCoffeeFaq from "@/data/seo/cookies_coffee_faq_schema.json";
import granolaFaq from "@/data/seo/granola_faq_schema.json";
import hardCheesesFaq from "@/data/seo/hard_cheeses_faq_schema.json";
import hummusFaq from "@/data/seo/hummus_faq_schema.json";
import juicesFaq from "@/data/seo/juices_faq_schema.json";

const FAQ_BY_KEY: Record<string, Record<string, unknown>> = {
  bread: breadFaq as Record<string, unknown>,
  breakfast_cereals: breakfastCerealsFaq as Record<string, unknown>,
  brined_cheeses: brinedCheesesFaq as Record<string, unknown>,
  cookies_coffee: cookiesCoffeeFaq as Record<string, unknown>,
  granola: granolaFaq as Record<string, unknown>,
  hard_cheeses: hardCheesesFaq as Record<string, unknown>,
  hummus: hummusFaq as Record<string, unknown>,
  juices: juicesFaq as Record<string, unknown>,
};

export function getFaqSchema(faqKey: string | undefined): Record<string, unknown> | null {
  if (!faqKey) return null;
  const raw = FAQ_BY_KEY[faqKey];
  if (!raw) return null;
  const { _bari_meta: _dropped, ...schema } = raw;
  void _dropped;
  return schema;
}
