"use client";

import { motion, useReducedMotion } from "framer-motion";
import {
  BrainCircuit,
  CircleGauge,
  FlaskConical,
  GitCompareArrows,
  Leaf,
  Scale,
  ShieldCheck,
} from "lucide-react";

import { HomeContainer } from "./section-frame";

type InsightItem = {
  icon: typeof Leaf;
  title: string;
  text: string;
};

const leftInsights = [
  {
    icon: Leaf,
    title: "איכות רכיבים",
    text: "עד כמה רשימת הרכיבים פשוטה ומבוססת רכיבים מוכרים",
  },
  {
    icon: FlaskConical,
    title: "רמת עיבוד",
    text: "עד כמה המוצר עבר עיבוד תעשייתי",
  },
  {
    icon: Scale,
    title: "איזון תזונתי",
    text: "איזון בין חלבון, סיבים, סוכר, שומן וערכים נוספים",
  },
] as const satisfies readonly InsightItem[];

const rightInsights = [
  {
    icon: GitCompareArrows,
    title: "יתרונות מול חסרונות",
    text: "נקודות חיוביות לצד דברים שכדאי לשים לב אליהם",
  },
  {
    icon: CircleGauge,
    title: "השוואה למוצרים דומים",
    text: "איך המוצר עומד ביחס למוצרים דומים בקטגוריה",
  },
  {
    icon: ShieldCheck,
    title: "איכות מידע",
    text: "עד כמה הניתוח מבוסס על מידע מלא ואמין",
  },
] as const satisfies readonly InsightItem[];

const engineSignals = [
  "איכות רכיבים",
  "רמת עיבוד",
  "איזון תזונתי",
  "יתרונות מול חסרונות",
  "השוואה למוצרים דומים",
  "איכות מידע",
] as const;

const enginePaths = [
  "M52 82 C112 52 152 102 212 76 S318 42 388 92",
  "M44 178 C112 124 158 212 226 154 S320 118 396 184",
  "M72 268 C138 220 178 284 242 238 S326 214 382 282",
  "M92 124 C150 128 168 70 218 86 C272 104 286 154 340 148",
  "M104 230 C156 202 178 184 224 202 C276 224 294 266 354 246",
  "M136 64 L228 154 L318 68",
  "M126 292 L228 154 L336 300",
  "M40 130 C116 100 168 142 228 154 S340 198 406 146",
  "M44 230 C124 252 152 118 228 154 S320 232 402 236",
] as const;

const engineNodes = [
  [52, 82, 4],
  [124, 58, 3.5],
  [212, 76, 4],
  [318, 42, 3.5],
  [388, 92, 4],
  [44, 178, 3.5],
  [146, 190, 4],
  [228, 154, 8],
  [318, 118, 4],
  [396, 184, 3.5],
  [72, 268, 3.5],
  [242, 238, 4],
  [382, 282, 3.5],
] as const;

const fadeUp = {
  hidden: { opacity: 0, y: 18 },
  visible: { opacity: 1, y: 0 },
};

function InsightCard({
  item,
  index,
  direction,
  reduceMotion,
}: {
  item: (typeof leftInsights)[number];
  index: number;
  direction: "left" | "right";
  reduceMotion: boolean;
}) {
  const Icon = item.icon;

  return (
    <motion.div
      initial={reduceMotion ? false : { opacity: 0, x: direction === "left" ? 22 : -22, y: 8 }}
      whileInView={reduceMotion ? undefined : { opacity: 1, x: 0, y: 0 }}
      viewport={{ once: true, amount: 0.4 }}
      transition={{
        delay: reduceMotion ? 0 : index * 0.1,
        duration: reduceMotion ? 0 : 0.62,
        ease: [0.22, 1, 0.36, 1],
      }}
      className="relative flex min-h-[10.75rem] flex-col rounded-[1.45rem] border border-black/[0.08] bg-[#FFFFFF]/88 p-5 text-[#111318] shadow-[0_18px_42px_-42px_rgba(17,19,24,0.16)] backdrop-blur-sm md:p-6 lg:h-[10.75rem]"
    >
      <div className="flex items-start justify-between gap-4">
        <div className="max-w-[15.5rem]">
          <h3 className="text-2xl font-extrabold tracking-[-0.045em] text-[#111318]">{item.title}</h3>
          <p className="mt-3 text-sm leading-relaxed text-[#5A6170]">{item.text}</p>
        </div>
        <div className="grid size-10 shrink-0 place-items-center rounded-full border border-black/[0.08] bg-[#F7F7F2] text-[#1F8F6A]">
          <Icon className="size-[1.125rem]" aria-hidden />
        </div>
      </div>
    </motion.div>
  );
}

function EngineNetwork({ reduceMotion }: { reduceMotion: boolean }) {
  return (
    <motion.div
      initial={reduceMotion ? false : { opacity: 0, scale: 0.96, y: 12 }}
      whileInView={reduceMotion ? undefined : { opacity: 1, scale: 1, y: 0 }}
      viewport={{ once: true, amount: 0.45 }}
      transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
      className="relative h-full overflow-hidden rounded-[2rem] border border-black/[0.08] bg-[#FFFFFF] p-5 text-[#111318] shadow-[0_28px_80px_-58px_rgba(17,19,24,0.24)] md:p-7"
    >
      <div
        className="pointer-events-none absolute inset-0 bg-[linear-gradient(rgba(17,19,24,0.022)_1px,transparent_1px),linear-gradient(90deg,rgba(17,19,24,0.022)_1px,transparent_1px),radial-gradient(circle_at_50%_42%,rgba(47,174,130,0.035),transparent_36%),radial-gradient(circle_at_74%_18%,rgba(47,174,130,0.025),transparent_36%),radial-gradient(circle_at_18%_84%,rgba(247,247,242,0.72),transparent_32%)] bg-[size:28px_28px,28px_28px,100%_100%,100%_100%,100%_100%]"
        aria-hidden
      />
      <div className="relative z-10">
        <div className="mb-6 flex items-center justify-between gap-4">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.24em] text-[#1F8F6A]">מנוע הניתוח של Bari</p>
            <h3 className="mt-2 text-3xl font-extrabold tracking-[-0.05em]">המנוע של ברי</h3>
            <p className="mt-2 text-sm font-medium text-[#4E5663]">
              ניתוח רב־ממדי • חישוב דינמי
            </p>
          </div>
          <motion.div
            animate={reduceMotion ? undefined : { scale: [1, 1.04, 1], opacity: [0.9, 1, 0.9] }}
            transition={{ duration: 3.8, repeat: Infinity, ease: "easeInOut" }}
            className="grid size-12 place-items-center rounded-2xl border border-black/[0.08] bg-[#FFFFFF]/60"
          >
            <BrainCircuit className="size-6 text-[#1F8F6A]" aria-hidden />
          </motion.div>
        </div>

        <div className="relative mx-auto aspect-[1.25] max-w-[32rem]">
          <svg className="size-full overflow-visible" viewBox="0 0 440 330" role="img" aria-label="המנוע של ברי">
            <defs>
              <radialGradient id="bari-engine-center" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stopColor="rgba(31,143,106,0.68)" />
                <stop offset="100%" stopColor="rgba(47,174,130,0.06)" />
              </radialGradient>
              <filter id="bari-engine-soft-glow" x="-60%" y="-60%" width="220%" height="220%">
                <feGaussianBlur stdDeviation="4" result="blur" />
                <feMerge>
                  <feMergeNode in="blur" />
                  <feMergeNode in="SourceGraphic" />
                </feMerge>
              </filter>
            </defs>

            <g fill="none" strokeLinecap="round" strokeLinejoin="round">
              {enginePaths.map((path, index) => (
                <motion.path
                  key={path}
                  d={path}
                  stroke={index < 3 ? "rgba(31,143,106,0.46)" : "rgba(17,19,24,0.22)"}
                  strokeWidth={index < 3 ? 1.8 : 1.35}
                  initial={{ pathLength: 0, opacity: 0 }}
                  whileInView={{ pathLength: 1, opacity: 1 }}
                  viewport={{ once: true, amount: 0.6 }}
                  transition={{
                    delay: reduceMotion ? 0 : index * 0.11,
                    duration: reduceMotion ? 0 : 1.35,
                    ease: [0.22, 1, 0.36, 1],
                  }}
                />
              ))}
            </g>

            {!reduceMotion
              ? enginePaths.map((path, index) => (
                  <motion.circle
                    key={`pulse-${path}`}
                    r="3.2"
                    fill={index % 2 === 0 ? "rgba(31,143,106,0.78)" : "rgba(17,19,24,0.38)"}
                    filter="url(#bari-engine-soft-glow)"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: [0, 0.95, 0] }}
                    transition={{
                      delay: 0.8 + index * 0.45,
                      duration: 3.6,
                      repeat: Infinity,
                      ease: "easeInOut",
                    }}
                  >
                    <animateMotion dur={`${7.2 + index * 0.55}s`} repeatCount="indefinite" path={path} />
                  </motion.circle>
                ))
              : null}

            <circle
              cx="228"
              cy="154"
              r="34"
              fill="url(#bari-engine-center)"
              opacity="0.14"
            />
            {engineNodes.map(([cx, cy, radius], index) => {
              const isCenter = cx === 228 && cy === 154;
              return (
                <motion.circle
                  key={`${cx}-${cy}`}
                  cx={cx}
                  cy={cy}
                  r={radius}
                  fill={isCenter ? "rgba(31,143,106,0.78)" : "rgba(255,255,255,0.96)"}
                  stroke={isCenter ? "rgba(31,143,106,0.32)" : "rgba(17,19,24,0.26)"}
                  strokeWidth={isCenter ? 1.7 : 1.15}
                  filter={isCenter ? "url(#bari-engine-soft-glow)" : undefined}
                  initial={reduceMotion ? false : { opacity: 0, scale: 0.6 }}
                  whileInView={reduceMotion ? undefined : { opacity: 1, scale: 1 }}
                  animate={
                    reduceMotion
                      ? undefined
                      : {
                          opacity: isCenter ? [0.86, 1, 0.86] : [0.48, 0.86, 0.48],
                        }
                  }
                  viewport={{ once: true }}
                  transition={{
                    delay: reduceMotion ? 0 : 0.25 + index * 0.045,
                    duration: reduceMotion ? 0 : 2.8 + (index % 4) * 0.3,
                    repeat: reduceMotion ? 0 : Infinity,
                    ease: "easeInOut",
                  }}
                />
              );
            })}
          </svg>
        </div>

        <div className="mt-6 grid gap-2 sm:grid-cols-3">
          {engineSignals.map((signal, index) => (
            <motion.div
              key={signal}
              initial={reduceMotion ? false : { opacity: 0, y: 8 }}
              whileInView={reduceMotion ? undefined : { opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: reduceMotion ? 0 : 0.55 + index * 0.08, duration: reduceMotion ? 0 : 0.45 }}
              className="rounded-full border border-black/[0.08] bg-[#FFFFFF]/46 px-3 py-2 text-center text-[0.66rem] font-semibold text-[#4E5663]"
            >
              {signal}
            </motion.div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}

export function HomeAnalysisEngine() {
  const shouldReduceMotion = useReducedMotion();
  const reduceMotion = Boolean(shouldReduceMotion);

  return (
    <section
      className="relative overflow-hidden border-t border-black/[0.06] bg-[#F7F7F2] py-20 text-[#111318] md:py-28"
      id="analysis-engine"
    >
      <div
        className="pointer-events-none absolute inset-0 bg-transparent"
        aria-hidden
      />
      <HomeContainer>
        <motion.div
          initial={reduceMotion ? false : "hidden"}
          whileInView={reduceMotion ? undefined : "visible"}
          viewport={{ once: true, amount: 0.35 }}
          variants={fadeUp}
          transition={{ duration: reduceMotion ? 0 : 0.7, ease: [0.22, 1, 0.36, 1] }}
          className="relative z-10 mx-auto mb-12 max-w-3xl text-center"
        >
          <p className="text-sm font-bold text-[#1F8F6A]">מנוע הניתוח</p>
          <h2 className="mt-3 text-balance text-3xl font-extrabold tracking-[-0.045em] text-[#111318] md:text-5xl">
            איך Bari מנתחת מוצרים
          </h2>
          <p className="mx-auto mt-5 max-w-2xl text-pretty text-base leading-relaxed text-[#4E5663] md:text-lg">
            Bari משווה בין מוצרים דומים כדי לזהות הבדלים אמיתיים ברכיבים, בערכים התזונתיים וברמת העיבוד.
          </p>
        </motion.div>

        <div className="relative grid gap-5 lg:min-h-[35.25rem] lg:grid-cols-[minmax(0,0.9fr)_minmax(380px,1.25fr)_minmax(0,0.9fr)] lg:items-stretch">
          <div className="relative z-10 order-1 flex flex-col gap-4 lg:order-none lg:col-start-1 lg:row-start-1 lg:h-full lg:justify-between">
            {leftInsights.map((item, index) => (
              <InsightCard key={item.title} item={item} index={index} direction="left" reduceMotion={reduceMotion} />
            ))}
          </div>

          <div className="relative z-20 order-2 lg:order-none lg:col-start-2 lg:row-start-1">
            <EngineNetwork reduceMotion={reduceMotion} />
          </div>

          <div className="relative z-10 order-3 flex flex-col gap-4 lg:order-none lg:col-start-3 lg:row-start-1 lg:h-full lg:justify-between">
            {rightInsights.map((item, index) => (
              <InsightCard key={item.title} item={item} index={index} direction="right" reduceMotion={reduceMotion} />
            ))}
          </div>
        </div>
      </HomeContainer>
    </section>
  );
}
