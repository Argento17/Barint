"use client";

import { motion, useReducedMotion } from "framer-motion";
import {
  BrainCircuit,
  CircleGauge,
  FlaskConical,
  Leaf,
  MessageSquareText,
  Scale,
  Sparkles,
} from "lucide-react";

import { HomeContainer } from "./section-frame";

const observedSignals = [
  {
    icon: Leaf,
    title: "מרכיבים אמיתיים",
    text: "כמה המוצר קרוב למזון אמיתי לעומת רכיבים מעובדים",
    tags: ["רמת ביטחון: גבוהה", "NOVA 2–4"],
  },
  {
    icon: CircleGauge,
    title: "עומס סוכר ומלח",
    text: "כמות הסוכר, המלח והאנרגיה בהשוואה למה שמומלץ",
    tags: ["סוכר גבוה", "רמת ביטחון: גבוהה"],
  },
  {
    icon: FlaskConical,
    title: "פשטות המוצר",
    text: "כמה המוצר פשוט וברור לעומת מורכב ומתועש",
    tags: ["תוספים רבים", "רמת ביטחון: בינונית"],
  },
] as const;

const engineSignals = ["ערך תזונתי", "איכות מרכיבים", "השפעה", "ביטחון והסבר", "השוואה לקטגוריה", "השפעה על שובע"] as const;

const outputs = [
  {
    icon: Scale,
    label: "RELATIVE SCORE",
    title: "דירוג יחסי בקטגוריה",
    result: "C · 65 / 100",
    text: "בהשוואה למוצרים דומים בקטגוריה",
  },
  {
    icon: Sparkles,
    label: "TRADEOFFS",
    title: "יתרונות מול חסרונות",
    result: "חוזקות: סיבים · שומן איכותי",
    text: "לשיפור: סוכר גבוה · עיבוד מתקדם",
  },
  {
    icon: MessageSquareText,
    label: "WHY IT MATTERS",
    title: "למה זה חשוב?",
    result: "ניתוח מבוסס הקשר",
    text: "המוצר מספק ערך תזונתי מסוים, אך הוא מעובד ומכיל כמות סוכר גבוהה יחסית — מה שמשפיע על איכות התזונה הכוללת.",
  },
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

function SignalModule({
  signal,
  index,
  reduceMotion,
}: {
  signal: (typeof observedSignals)[number];
  index: number;
  reduceMotion: boolean;
}) {
  const Icon = signal.icon;

  return (
    <motion.div
      initial={reduceMotion ? false : { opacity: 0, x: 26, y: 8 }}
      whileInView={reduceMotion ? undefined : { opacity: 1, x: 0, y: 0 }}
      viewport={{ once: true, amount: 0.4 }}
      transition={{
        delay: reduceMotion ? 0 : index * 0.14,
        duration: reduceMotion ? 0 : 0.68,
        ease: [0.22, 1, 0.36, 1],
      }}
      whileHover={reduceMotion ? undefined : { y: -3 }}
      className="group relative flex min-h-[10.75rem] overflow-hidden rounded-[1.45rem] border border-emerald-300/10 bg-white/[0.045] p-5 text-white shadow-[0_24px_78px_-62px_rgba(0,0,0,0.95)] backdrop-blur-xl transition-colors duration-500 hover:border-emerald-300/24 lg:h-[10.75rem]"
    >
      <div
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_82%_14%,rgba(16,185,129,0.1),transparent_36%),linear-gradient(180deg,rgba(255,255,255,0.06),transparent_55%)]"
        aria-hidden
      />
      <motion.div
        animate={reduceMotion ? undefined : { opacity: [0.65, 0.95, 0.65] }}
        transition={{ duration: 5 + index * 0.4, repeat: Infinity, ease: "easeInOut" }}
        className="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-l from-transparent via-emerald-300/20 to-transparent"
        aria-hidden
      />
      <div className="relative z-10 flex w-full flex-col justify-between">
        <div className="flex items-start justify-between gap-3">
          <div>
            <h3 className="text-2xl font-extrabold tracking-[-0.045em] text-white">{signal.title}</h3>
            <p className="mt-3 max-w-[16rem] text-sm leading-relaxed text-zinc-300">{signal.text}</p>
          </div>
          <div className="relative grid size-12 shrink-0 place-items-center rounded-full border border-emerald-300/14 bg-emerald-300/[0.045] text-emerald-200">
            <Icon className="size-5" aria-hidden />
            <motion.span
              animate={reduceMotion ? undefined : { opacity: [0.25, 0.85, 0.25], scale: [1, 1.35, 1] }}
              transition={{ duration: 3.5 + index * 0.25, repeat: Infinity, ease: "easeInOut" }}
              className="absolute inset-0 rounded-full border border-emerald-300/20"
              aria-hidden
            />
          </div>
        </div>
        <div className="mt-4 flex flex-wrap gap-2">
          {signal.tags.map((tag) => (
            <span
              key={tag}
              className="rounded-full border border-emerald-300/10 bg-white/[0.035] px-2.5 py-1 text-[0.68rem] font-semibold text-zinc-300 transition-colors duration-300 group-hover:border-emerald-300/20 group-hover:text-emerald-100"
            >
              {tag}
            </span>
          ))}
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
      className="relative h-full overflow-hidden rounded-[2rem] border border-emerald-300/12 bg-zinc-950 p-5 text-white shadow-[0_36px_120px_-74px_rgba(0,0,0,0.95)] md:p-7"
    >
      <div
        className="pointer-events-none absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.025)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.025)_1px,transparent_1px),radial-gradient(circle_at_50%_42%,rgba(16,185,129,0.18),transparent_34%),radial-gradient(circle_at_74%_18%,rgba(16,185,129,0.12),transparent_34%),radial-gradient(circle_at_18%_84%,rgba(255,255,255,0.07),transparent_32%)] bg-[size:28px_28px,28px_28px,100%_100%,100%_100%,100%_100%]"
        aria-hidden
      />
      <div className="relative z-10">
        <div className="mb-6 flex items-center justify-between gap-4">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.24em] text-emerald-200">BARI ENGINE</p>
            <h3 className="mt-2 text-3xl font-extrabold tracking-[-0.05em]">מנוע אותות</h3>
            <p className="mt-2 text-sm font-medium text-zinc-400">
              ניתוח רב־ממדי • חישוב דינמי • הסבר שקוף
            </p>
          </div>
          <motion.div
            animate={reduceMotion ? undefined : { scale: [1, 1.04, 1], opacity: [0.9, 1, 0.9] }}
            transition={{ duration: 3.8, repeat: Infinity, ease: "easeInOut" }}
            className="grid size-12 place-items-center rounded-2xl border border-emerald-300/15 bg-white/5"
          >
            <BrainCircuit className="size-6 text-emerald-200" aria-hidden />
          </motion.div>
        </div>

        <div className="relative mx-auto aspect-[1.25] max-w-[32rem]">
          <svg className="size-full overflow-visible" viewBox="0 0 440 330" role="img" aria-label="מנוע אותות אנליטי של Bari">
            <defs>
              <radialGradient id="bari-engine-center" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stopColor="rgba(52,211,153,0.95)" />
                <stop offset="100%" stopColor="rgba(52,211,153,0.16)" />
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
                  stroke={index < 3 ? "rgba(167,243,208,0.24)" : "rgba(255,255,255,0.12)"}
                  strokeWidth={index < 3 ? 1.15 : 0.9}
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
                    fill={index % 2 === 0 ? "rgba(52,211,153,0.88)" : "rgba(236,253,245,0.72)"}
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

            <motion.circle
              cx="228"
              cy="154"
              r="34"
              fill="url(#bari-engine-center)"
              opacity="0.18"
              animate={reduceMotion ? undefined : { r: [30, 38, 30], opacity: [0.12, 0.2, 0.12] }}
              transition={{ duration: 4.2, repeat: Infinity, ease: "easeInOut" }}
            />
            {engineNodes.map(([cx, cy, radius], index) => {
              const isCenter = cx === 228 && cy === 154;
              return (
                <motion.circle
                  key={`${cx}-${cy}`}
                  cx={cx}
                  cy={cy}
                  r={radius}
                  fill={isCenter ? "rgba(52,211,153,0.94)" : "rgba(236,253,245,0.78)"}
                  stroke={isCenter ? "rgba(167,243,208,0.4)" : "rgba(255,255,255,0.16)"}
                  strokeWidth={isCenter ? 1.5 : 0.8}
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
              className="rounded-full border border-emerald-300/[0.08] bg-white/[0.026] px-3 py-2 text-center text-[0.66rem] font-semibold text-zinc-400"
            >
              {signal}
            </motion.div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}

function OutputCard({
  item,
  index,
  reduceMotion,
}: {
  item: (typeof outputs)[number];
  index: number;
  reduceMotion: boolean;
}) {
  const Icon = item.icon;

  return (
    <motion.div
      initial={reduceMotion ? false : { opacity: 0, x: -28 }}
      whileInView={reduceMotion ? undefined : { opacity: 1, x: 0 }}
      viewport={{ once: true, amount: 0.4 }}
      transition={{ delay: reduceMotion ? 0 : 0.25 + index * 0.12, duration: reduceMotion ? 0 : 0.65, ease: [0.22, 1, 0.36, 1] }}
      whileHover={reduceMotion ? undefined : { y: -3 }}
      className="group relative flex min-h-[10.75rem] overflow-hidden rounded-[1.45rem] border border-emerald-300/10 bg-white/[0.045] p-5 text-white shadow-[0_24px_78px_-62px_rgba(0,0,0,0.95)] backdrop-blur-xl transition-colors duration-500 hover:border-emerald-300/24 lg:h-[10.75rem]"
    >
      <div
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_20%_16%,rgba(16,185,129,0.12),transparent_34%),linear-gradient(180deg,rgba(255,255,255,0.055),transparent_55%)]"
        aria-hidden
      />
      <motion.div
        animate={reduceMotion ? undefined : { opacity: [0.55, 0.9, 0.55] }}
        transition={{ duration: 5.4 + index * 0.35, repeat: Infinity, ease: "easeInOut" }}
        className="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-l from-transparent via-emerald-300/18 to-transparent"
        aria-hidden
      />
      <div className="relative z-10 flex w-full flex-col justify-between">
        <div className="mb-3 flex items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <span className="grid size-12 place-items-center rounded-full border border-emerald-300/14 bg-emerald-300/[0.045] text-emerald-200">
              <Icon className="size-4" aria-hidden />
            </span>
            <div>
              <p className="text-[0.62rem] font-bold uppercase tracking-[0.18em] text-emerald-200/80">{item.label}</p>
              <h3 className="mt-1 text-2xl font-extrabold tracking-[-0.045em] text-white">{item.title}</h3>
            </div>
          </div>
          <motion.span
            animate={reduceMotion ? undefined : { opacity: [0.45, 1, 0.45] }}
            transition={{ duration: 3.4 + index * 0.25, repeat: Infinity, ease: "easeInOut" }}
            className="size-1.5 rounded-full bg-emerald-300"
            aria-hidden
          />
        </div>
        <div>
          <p className="mb-2 text-xs font-bold text-emerald-100/90">{item.result}</p>
          <p className="text-sm leading-relaxed text-zinc-300">{item.text}</p>
        </div>
      </div>
    </motion.div>
  );
}

export function HomeAnalysisEngine() {
  const shouldReduceMotion = useReducedMotion();
  const reduceMotion = Boolean(shouldReduceMotion);

  return (
    <section className="relative overflow-hidden bg-[#050706] py-20 text-white md:py-28" id="analysis-engine">
      <div
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_80%_10%,rgba(16,185,129,0.14),transparent_32%),radial-gradient(circle_at_10%_78%,rgba(16,185,129,0.08),transparent_34%),linear-gradient(180deg,rgba(255,255,255,0.035),transparent_42%)]"
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
          <p className="text-xs font-bold uppercase tracking-[0.22em] text-emerald-200/80">Analysis engine</p>
          <h2 className="mt-3 text-balance text-3xl font-extrabold tracking-[-0.045em] text-white md:text-5xl">
            איך Bari הופכת מוצרים לתובנות
          </h2>
          <p className="mx-auto mt-5 max-w-2xl text-pretty text-base leading-relaxed text-zinc-400 md:text-lg">
            מוצרים דומים נכנסים למערכת, Bari מזהה אותות תזונתיים ודפוסי רכיבים — ומחזירה דירוג יחסי,
            הסבר והשוואה ברורה.
          </p>
        </motion.div>

        <div className="relative grid gap-5 lg:min-h-[35.25rem] lg:grid-cols-[minmax(0,0.9fr)_minmax(380px,1.25fr)_minmax(0,0.9fr)] lg:items-stretch">
          <motion.svg
            className="pointer-events-none absolute inset-0 z-0 hidden size-full overflow-visible lg:block"
            viewBox="0 0 1200 520"
            preserveAspectRatio="none"
            aria-hidden
          >
            <motion.path
              d="M1010 130 C880 130 760 180 640 232"
              fill="none"
              stroke="rgba(16,185,129,0.18)"
              strokeLinecap="round"
              strokeWidth="1"
              initial={{ pathLength: 0, opacity: 0 }}
              whileInView={{ pathLength: 1, opacity: 1 }}
              viewport={{ once: true }}
              transition={{ duration: reduceMotion ? 0 : 1.2, ease: "easeOut" }}
            />
            <motion.path
              d="M640 288 C500 322 360 374 190 374"
              fill="none"
              stroke="rgba(16,185,129,0.16)"
              strokeLinecap="round"
              strokeWidth="1"
              initial={{ pathLength: 0, opacity: 0 }}
              whileInView={{ pathLength: 1, opacity: 1 }}
              viewport={{ once: true }}
              transition={{ delay: reduceMotion ? 0 : 0.25, duration: reduceMotion ? 0 : 1.2, ease: "easeOut" }}
            />
            {!reduceMotion ? (
              <>
                <motion.circle r="3" fill="rgba(52,211,153,0.75)" animate={{ opacity: [0, 1, 0] }} transition={{ duration: 3.8, repeat: Infinity, ease: "easeInOut" }}>
                  <animateMotion dur="8s" repeatCount="indefinite" path="M1010 130 C880 130 760 180 640 232" />
                </motion.circle>
                <motion.circle r="3" fill="rgba(52,211,153,0.65)" animate={{ opacity: [0, 1, 0] }} transition={{ delay: 1, duration: 4.2, repeat: Infinity, ease: "easeInOut" }}>
                  <animateMotion dur="9s" repeatCount="indefinite" path="M640 288 C500 322 360 374 190 374" />
                </motion.circle>
              </>
            ) : null}
          </motion.svg>

          <div className="relative z-10 order-1 flex flex-col gap-4 lg:order-none lg:col-start-1 lg:row-start-1 lg:h-full lg:justify-between">
            <p className="text-sm font-extrabold text-zinc-300">מה אנחנו רואים במוצר</p>
            {observedSignals.map((signal, index) => (
              <SignalModule key={signal.title} signal={signal} index={index} reduceMotion={reduceMotion} />
            ))}
          </div>

          <div className="relative z-20 order-2 lg:order-none lg:col-start-2 lg:row-start-1">
            <EngineNetwork reduceMotion={reduceMotion} />
          </div>

          <div className="relative z-10 order-3 flex flex-col gap-4 lg:order-none lg:col-start-3 lg:row-start-1 lg:h-full lg:justify-between">
            <p className="text-sm font-extrabold text-zinc-300">מה בארי מבין מהמוצר</p>
            {outputs.map((item, index) => (
              <OutputCard key={item.title} item={item} index={index} reduceMotion={reduceMotion} />
            ))}
          </div>
        </div>
      </HomeContainer>
    </section>
  );
}
