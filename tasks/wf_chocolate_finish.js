export const meta = {
  name: 'chocolate-finish',
  description: 'Nutrition co-sign the new chocolate calorie regime + Content authors the 7 upward flips + Adversarial QA both chocolate shelves',
  phases: [{ title: 'Review' }, { title: 'QA' }],
}

const SWEEP = 'C:/Users/HP/AppData/Local/Temp/claude/c--Bari/e2a5794f-5f0d-4695-a2e0-194500472e65/scratchpad/deanchor_sweep'
const DATA = 'C:/bari_deanchor_wt/bari-web/src/data/comparisons'
const STAG = 'C:/bari_deanchor_wt/_rescore_staging'

const TABLETS = {
  shelf: 'chocolate_tablets', artifact: `${SWEEP}/chocolate_tablets_frontend_v1_deanchor.json`,
  live: `${DATA}/chocolate_tablets_frontend_v1.json`, traces: `${STAG}/chocolate_tablets/products`,
  flips: ['7296073382416 C->B', '7290112197467 C->B', '7290119500437 D->C', '7296073747819 D->C', '7610400075770 E->D', '7296073747802 E->D', '4000417025005 E->D'],
}
const BARS = {
  shelf: 'chocolate_bars', artifact: `${SWEEP}/chocolate_bars_frontend_v1_deanchor.json`,
  live: `${DATA}/chocolate_bars_frontend_v1.json`, traces: `${STAG}/chocolate_bars/products`,
}

const NUTR_SCHEMA = {
  type: 'object',
  required: ['verdict', 'calorie_regime_defensible', 'b_grades_defensible', 'all_e_bars_honest', 'reasoning'],
  properties: {
    verdict: { type: 'string', enum: ['CO_SIGN', 'CONCERNS', 'NO_GO'] },
    calorie_regime_defensible: { type: 'boolean' },
    b_grades_defensible: { type: 'boolean' },
    all_e_bars_honest: { type: 'boolean' },
    concerns: { type: 'array', items: { type: 'string' } },
    reasoning: { type: 'string' },
  },
}
const QA_SCHEMA = {
  type: 'object',
  required: ['shelf', 'verdict', 'scores_correct', 'parity_clean', 'flip_copy_honest', 'decisive_reason'],
  properties: {
    shelf: { type: 'string' },
    verdict: { type: 'string', enum: ['GO', 'GO_WITH_FIXES', 'NO_GO'] },
    scores_correct: { type: 'boolean' },
    parity_clean: { type: 'boolean' },
    flip_copy_honest: { type: 'boolean' },
    critical_findings: { type: 'array', items: { type: 'string' } },
    high_findings: { type: 'array', items: { type: 'string' } },
    preexisting_debt_flagged: { type: 'array', items: { type: 'string' } },
    decisive_reason: { type: 'string' },
  },
}

// Phase 1 — Nutrition regime co-sign + Content flip authoring (independent, parallel)
const [nutrition] = await parallel([
  () => agent(
    `You are the Nutrition Agent. Co-sign (or reject) the NEW chocolate scoring regime that Data implemented under TASK-455 — this is the one scoring decision not yet in your lane's sign-off.\n\n` +
    `What changed: chocolate was mis-classified as snack_bar_granola (scored against granola-bar caps). Data (a) added a 'chocolate' bucket to router_v2.py, (b) added a DEDICATED chocolate entry to CALORIE_DENSITY_TABLES in constants.py = [(420,85),(480,75),(530,62),(570,50),(610,38),(1e9,25)] calibrated from the real 58-product corpus (kcal 390-610, median ~510-545), and (c) added 'chocolate' to REDLABEL_ENDEMIC_SATFAT_CATEGORIES (EV-REDLABEL-013, already co-signed).\n\n` +
    `Result (all moves UPWARD): chocolate_bars 23/23 up, all stay grade E (scores 12.3-25.5); chocolate_tablets 35/35 up, 7 upward grade flips, 2 tablets now reach B (7296073382416 score 65.1, 7290112197467 score 65.8). New tablet dist B2/C6/D10/E17.\n\n` +
    `Read the traces (${TABLETS.traces} and ${BARS.traces}) and the constants.py chocolate calorie table. Judge:\n` +
    `1. Is the new chocolate CALORIE-DENSITY regime defensible (vs the old granola-bar table that flattened everything to 15-25)? Is [(420,85)...(610,38)] honestly calibrated, not too lenient?\n` +
    `2. Are the 2 new B-grade tablets defensible? Read their traces — what ARE they (high-cocoa dark? low-sugar? minimal ingredients?). Is B honest for a chocolate tablet, or too high?\n` +
    `3. Is 'all 23 bars = E' an honest clustering finding (genuine, per the butter-clustering principle — never manufacture differentiation) or does it hide real differences?\n` +
    `Return the structured verdict. CO_SIGN if the regime + grades are honestly defensible; CONCERNS for fixable issues; NO_GO if a grade is indefensible.`,
    { label: 'nutrition:regime', phase: 'Review', schema: NUTR_SCHEMA }
  ),
  () => agent(
    `You are the Content Agent (Tom-Bari Hebrew editorial voice). Chocolate was re-scored correctly (TASK-455) and 7 chocolate_tablets flipped grade UPWARD. Re-author each flipped product's verdict (rowVerdict + insightLine) to match its NEW, higher grade. EDIT THE FILE IN PLACE.\n\n` +
    `Artifact: ${TABLETS.artifact}\nTraces (ground truth): ${TABLETS.traces}\nFlips (all UPWARD): ${TABLETS.flips.join('; ')}\n\n` +
    `HARD RULES: every number traces to bsip2_trace.json L1_observed_signals; UPWARD flips must honestly name what genuinely improved (these are dark/higher-cocoa or cleaner tablets no longer mis-scored as granola bars — but do NOT overclaim; chocolate is still calorie-dense); no framework/score-mechanic vocabulary; no OFF; touch ONLY the 7 flipped products' rowVerdict/insightLine. Verify JSON parses. Return 1 line per flip.`,
    { label: 'copy:chocolate_tablets', phase: 'Review' }
  ),
])

// Phase 2 — Adversarial QA both shelves
const qa = await parallel([
  () => agent(
    `Adversarial QA gate on the chocolate_tablets de-anchor/correctness artifact (TASK-455 → chocolate go-live PR). Verify independently; trust nothing.\n\n` +
    `Artifact: ${TABLETS.artifact}\nLive baseline: ${TABLETS.live}\nTraces: ${TABLETS.traces}\n\n` +
    `Context: chocolate was re-classified from snack_bar_granola to a new 'chocolate' category (router_v2 Rule 4) with a new calorie table + endemic sat-fat carve-out. ALL 35 scores moved UPWARD; 7 upward grade flips (2 reach B). This is chocolate scored correctly for the first time, so large upward moves are EXPECTED — your job is to confirm they're trace-correct and the upward flips + B-grades are publicly defensible, not to flag the movement itself.\n\n` +
    `VERIFY: (V) all 35 score+grade match bsip2_trace final_score_estimate/grade_estimate; all 35 now category='chocolate' (not snack_bar_granola); rank clean permutation 0 inversions; barcode parity vs live exact; non-flip products keep byte-identical copy. (C) each of the 7 upward flips' re-authored copy is honest vs trace (especially the 2 C→B); the 2 B-grades survive scrutiny ("Bari gives a chocolate tablet a B" — defensible?); no framework leakage; no OFF; superlatives still true. Run run_gates.py --run ${TABLETS.traces} --baseline ${TABLETS.live}; confirm any FAIL is pre-existing (reproduce on live) vs introduced. Return structured verdict.`,
    { label: 'qa:chocolate_tablets', phase: 'QA', schema: QA_SCHEMA, agentType: 'Adversarial QA Agent' }
  ),
  () => agent(
    `Adversarial QA gate on the chocolate_bars de-anchor/correctness artifact (TASK-455 → chocolate go-live PR). Verify independently; trust nothing.\n\n` +
    `Artifact: ${BARS.artifact}\nLive baseline: ${BARS.live}\nTraces: ${BARS.traces}\n\n` +
    `Context: chocolate_bars re-classified from snack_bar_granola to 'chocolate' with a new calorie table + carve-out. All 23 scores moved UPWARD, 0 grade flips (all stay E). No copy changes (0 flips) — verdicts describe composition. Expected: large upward score moves, still all E.\n\n` +
    `VERIFY: (V) all 23 score+grade match trace; all 23 now category='chocolate'; rank clean 0 inversions; parity exact; ALL copy byte-identical to live (0 flips → no re-authoring). (C) is 'all 23 bars = E' honest clustering (genuine floor for candy-bar format) or does it hide real quality differences a consumer should see? no leakage; no OFF. Run run_gates.py --run ${BARS.traces} --baseline ${BARS.live}; confirm FAILs pre-existing. Return structured verdict.`,
    { label: 'qa:chocolate_bars', phase: 'QA', schema: QA_SCHEMA, agentType: 'Adversarial QA Agent' }
  ),
])

return { nutrition, qa_tablets: qa[0], qa_bars: qa[1] }
