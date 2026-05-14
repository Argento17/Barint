import { ChevronLeft } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

import { community } from "./content";
import { HomeContainer, SectionHeading } from "./section-frame";

export function HomeCommunity() {
  return (
    <section className="bg-white py-16 md:py-20" id="community">
      <HomeContainer>
        <SectionHeading
          eyebrow="קהילה"
          title="מעבר לתוכן — מקום לשאלות ולדיון"
          description="שילוב בין עורכים לקוראים: דיונים מנוהלים, מדריכים קהילתיים וניוזלטר שמרכז עדכונים."
        />

        <div className="grid gap-5 md:grid-cols-3">
          {community.map((item) => {
            const Icon = item.icon;
            return (
              <Card
                key={item.title}
                className="border-zinc-200/70 bg-gradient-to-br from-white to-zinc-50/60 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md"
              >
                <CardHeader className="space-y-3">
                  <div className="flex size-11 items-center justify-center rounded-xl bg-emerald-500/10 text-emerald-700 ring-1 ring-emerald-500/15">
                    <Icon className="size-5" aria-hidden />
                  </div>
                  <CardTitle className="text-xl">{item.title}</CardTitle>
                  <CardDescription className="text-base leading-relaxed text-zinc-600">
                    {item.body}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Button variant="ghost" className="gap-1 px-0 font-semibold text-emerald-700 hover:text-emerald-800" asChild>
                    <a href={item.href}>
                      {item.cta}
                      <ChevronLeft className="size-4" aria-hidden />
                    </a>
                  </Button>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </HomeContainer>
    </section>
  );
}
