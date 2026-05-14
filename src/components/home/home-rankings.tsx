import { Star } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";

import { rankings } from "./content";
import { HomeContainer, SectionHeading } from "./section-frame";

export function HomeRankings() {
  return (
    <section className="border-y border-zinc-200/70 bg-white py-16 md:py-20" id="rankings">
      <HomeContainer>
        <SectionHeading
          eyebrow="דירוגים"
          title="דירוגים חמים השבוע"
          description="מבט מהיר על פאנלים שעברו עדכון או נבדקו לאחרונה — לפני קריאה עמוקה בהשוואה."
        />

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {rankings.map((row) => (
            <Card
              key={row.title}
              className="border-zinc-200/70 bg-gradient-to-br from-white to-zinc-50/80 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md"
            >
              <CardContent className="flex flex-col gap-3 p-5 text-right">
                <div className="flex items-center justify-between gap-2">
                  <Badge variant="secondary" className="rounded-full bg-emerald-500/10 text-emerald-800">
                    {row.score}
                  </Badge>
                  <Star className="size-5 text-amber-400" aria-hidden />
                </div>
                <h3 className="text-base font-semibold leading-snug text-zinc-900">{row.title}</h3>
                <p className="text-xs text-zinc-500">{row.note}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </HomeContainer>
    </section>
  );
}
