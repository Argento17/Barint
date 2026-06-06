"use client";

import { useState } from "react";
import { ExternalLink, Play } from "lucide-react";

import { oliveOilArticle } from "@/lib/blog/olive-oil-article-content";

export function OliveOilExternalResearch() {
  const { externalResearch } = oliveOilArticle;
  const [videoLoaded, setVideoLoaded] = useState(false);
  const { ucDavisStudy, youtubeVideo } = externalResearch;
  const thumbnailUrl = `https://img.youtube.com/vi/${youtubeVideo.videoId}/maxresdefault.jpg`;
  const embedUrl = `https://www.youtube-nocookie.com/embed/${youtubeVideo.videoId}?autoplay=1&rel=0`;

  return (
    <section className="space-y-6">
      <header className="text-right">
        <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#1F8F6A]/85">
          מחקר בינלאומי
        </p>
        <h2 className="mt-1 text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
          {externalResearch.title}
        </h2>
        <p className="mt-2 text-sm leading-relaxed text-[#4E5663] md:text-base">
          {externalResearch.subtitle}
        </p>
      </header>

      {/* UC Davis stat card */}
      <div className="rounded-[1.2rem] border border-black/[0.07] bg-[#FFFFFF] px-6 py-7 md:px-8 md:py-8">
        <div className="flex flex-col gap-6 md:flex-row md:items-start md:gap-10">
          {/* Big number */}
          <div className="shrink-0 text-center md:text-right">
            <p className="text-[5rem] font-extrabold leading-none tracking-[-0.06em] text-[#C0392B]">
              {ucDavisStudy.headline}
            </p>
            <p className="mt-1 max-w-[10rem] text-center text-xs font-bold uppercase tracking-[0.1em] text-[#4E5663] md:text-right">
              {ucDavisStudy.headlineLabel}
            </p>
          </div>

          {/* Description */}
          <div className="flex-1 text-right">
            <p className="text-sm font-bold uppercase tracking-[0.12em] text-[#7A817C]">
              {ucDavisStudy.source}
            </p>
            <p className="mt-2 text-base leading-relaxed text-[#111318] md:text-lg">
              {ucDavisStudy.description}
            </p>
            <blockquote className="mt-4 border-r-4 border-[#C0392B]/40 pr-4">
              <p className="text-sm italic leading-relaxed text-[#4E5663]">
                {ucDavisStudy.quote}
              </p>
              <cite className="mt-1 block text-xs text-[#7A817C] not-italic">
                {ucDavisStudy.quoteAttribution}
              </cite>
            </blockquote>
            <a
              href={ucDavisStudy.sourceUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-4 inline-flex items-center gap-1.5 text-xs font-semibold text-[#1F8F6A] hover:underline"
            >
              למחקר המלא (PDF)
              <ExternalLink className="size-3.5" aria-hidden />
            </a>
          </div>
        </div>

        <p className="mt-5 rounded-[0.75rem] border border-amber-200/60 bg-amber-50/60 px-4 py-3 text-right text-xs leading-relaxed text-[#7A6A00]">
          <span className="font-bold">הגבלת הממצאים · </span>
          {ucDavisStudy.caveat}
        </p>
      </div>

      {/* YouTube embed */}
      <div className="rounded-[1.2rem] border border-black/[0.07] bg-[#111318] p-5 md:p-6">
        <div className="mb-4 text-right">
          <p className="text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">
            {youtubeVideo.attribution}
          </p>
          <h3 className="mt-1 text-lg font-extrabold tracking-[-0.03em] text-[#F7F7F2]">
            {youtubeVideo.title}
          </h3>
          <p className="mt-1 text-sm leading-relaxed text-[#C8CDC9]">
            {youtubeVideo.description}
          </p>
        </div>

        <div className="relative overflow-hidden rounded-[0.85rem] bg-black" style={{ paddingTop: "56.25%" }}>
          {videoLoaded ? (
            <iframe
              className="absolute inset-0 h-full w-full"
              src={embedUrl}
              title={youtubeVideo.title}
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          ) : (
            <button
              type="button"
              onClick={() => setVideoLoaded(true)}
              className="absolute inset-0 flex items-center justify-center"
              aria-label={`הפעל סרטון: ${youtubeVideo.title}`}
            >
              <img
                src={thumbnailUrl}
                alt={youtubeVideo.title}
                className="absolute inset-0 h-full w-full object-cover opacity-70"
              />
              <span className="relative flex h-16 w-16 items-center justify-center rounded-full bg-[#FF0000] shadow-lg shadow-black/40 transition-transform hover:scale-110">
                <Play className="size-7 fill-white text-white" aria-hidden />
              </span>
            </button>
          )}
        </div>
      </div>
    </section>
  );
}
