import pathlib
import re

path = pathlib.Path(r"C:\Bari\bari-web\src\components\home\home-methodology.tsx")
text = path.read_text(encoding="utf-8")

text = re.sub(
    r"\nfunction clampPercent\(value: number\) \{\n  return Math\.min\(96, Math\.max\(4, value\)\);\n\}\n",
    "\n",
    text,
    count=1,
)

radial_and_row = """
function ringCircumference(radius: number) {
  return 2 * Math.PI * radius;
}

const RING_SIZE = 52;
const RING_CENTER = RING_SIZE / 2;
const OUTER_RADIUS = 22;
const INNER_RADIUS = 15.5;
const OUTER_CIRC = ringCircumference(OUTER_RADIUS);
const INNER_CIRC = ringCircumference(INNER_RADIUS);

function RadialScoreRing({
  value,
  category,
  inView,
  reduceMotion,
  delayMs,
}: {
  value: number;
  category: number;
  inView: boolean;
  reduceMotion: boolean;
  delayMs: number;
}) {
  const outerOffset = OUTER_CIRC * (1 - value / 100);
  const innerOffset = INNER_CIRC * (1 - category / 100);
  const transition = reduceMotion
    ? { duration: 0 }
    : { duration: 1.1, ease: "easeOut" as const, delay: delayMs / 1000 };

  return (
    <div className="relative shrink-0" style={{ width: RING_SIZE, height: RING_SIZE }}>
      <svg
        width={RING_SIZE}
        height={RING_SIZE}
        viewBox={`0 0 ${RING_SIZE} ${RING_SIZE}`}
        className="-rotate-90"
        role="img"
        aria-label={`ציון מוצר ${value} מתוך 100, ממוצע קטגוריה ${category}`}
      >
        <circle
          cx={RING_CENTER}
          cy={RING_CENTER}
          r={OUTER_RADIUS}
          fill="none"
          stroke="#ECECE7"
          strokeWidth={4}
        />
        <circle
          cx={RING_CENTER}
          cy={RING_CENTER}
          r={INNER_RADIUS}
          fill="none"
          stroke="#ECECE7"
          strokeWidth={2.5}
        />
        <motion.circle
          cx={RING_CENTER}
          cy={RING_CENTER}
          r={INNER_RADIUS}
          fill="none"
          stroke="#9AA09B"
          strokeWidth={2.5}
          strokeLinecap="round"
          strokeDasharray={INNER_CIRC}
          initial={{ strokeDashoffset: INNER_CIRC }}
          animate={{ strokeDashoffset: inView ? innerOffset : INNER_CIRC }}
          transition={transition}
        />
        <motion.circle
          cx={RING_CENTER}
          cy={RING_CENTER}
          r={OUTER_RADIUS}
          fill="none"
          stroke="#1F8F6A"
          strokeWidth={4}
          strokeLinecap="round"
          strokeDasharray={OUTER_CIRC}
          initial={{ strokeDashoffset: OUTER_CIRC }}
          animate={{ strokeDashoffset: inView ? outerOffset : OUTER_CIRC }}
          transition={transition}
        />
      </svg>
      <div
        className="pointer-events-none absolute inset-0 flex items-center justify-center text-sm font-extrabold text-[#1F8F6A]"
        aria-hidden
      >
        {value}
      </div>
    </div>
  );
}

function SignalBenchmarkRow({
  index,
  inView,
  reduceMotion,
  row,
}: {
  index: number;
  inView: boolean;
  reduceMotion: boolean;
  row: (typeof benchmarkRows)[number];
}) {
  const delay = 180 + index * 130;

  return (
    <motion.div
      className="group rounded-2xl border border-black/[0.08] bg-[#FFFFFF]/68 px-3 py-2.5 shadow-sm shadow-slate-900/20 backdrop-blur-sm transition-[border-color,box-shadow,background-color] duration-500 ease-out hover:border-[#1F8F6A]/20 hover:bg-[#FFFFFF]/82 hover:shadow-md hover:shadow-slate-900/10"
      whileHover={reduceMotion ? undefined : { y: -2 }}
      transition={{ duration: 0.45, ease: "easeOut" }}
    >
      <div className="flex items-center gap-3">
        <RadialScoreRing
          value={row.value}
          category={row.category}
          inView={inView}
          reduceMotion={reduceMotion}
          delayMs={delay}
        />
        <div className="min-w-0 flex-1">
          <div className="text-sm font-bold text-[#111318] transition-colors duration-300 group-hover:text-[#1F8F6A]">
            {row.label}
          </div>
          <div className="mt-0.5 text-xs text-[#5E6560] transition-colors duration-300 group-hover:text-[#4E5663]">
            {row.note}
          </div>
          <div className="mt-1.5 flex items-center gap-1.5 text-[0.68rem] font-medium text-[#5E6560]">
            <span className="size-1.5 shrink-0 rounded-full bg-[#9AA09B]" aria-hidden />
            <span>
              קו קטגוריה · {row.category}
            </span>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
"""

pattern = r"function SignalBenchmarkRow\(\{[\s\S]*?\n\}\n\nfunction SignalBenchmarkBars"
if not re.search(pattern, text):
    raise SystemExit("SignalBenchmarkRow pattern not found")
text = re.sub(pattern, radial_and_row.strip() + "\n\nfunction SignalBenchmarkBars", text, count=1)

text = text.replace('className="space-y-4"', 'className="space-y-2.5"', 1)

path.write_text(text, encoding="utf-8")
print("patched ok")
