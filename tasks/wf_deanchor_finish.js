export const meta = {
  name: 'deanchor-finish',
  description: 'Author remaining de-anchor flips (milk/juices/snacks) + independent QA on the not-yet-verified cats (cookies_coffee/milk/juices/snacks/cakes/bread)',
  phases: [{ title: 'Copy' }, { title: 'QA' }],
}

const SWEEP = 'C:/Users/HP/AppData/Local/Temp/claude/c--Bari/e2a5794f-5f0d-4695-a2e0-194500472e65/scratchpad/deanchor_sweep'
const DATA = 'C:/bari_deanchor_wt/bari-web/src/data/comparisons'
const STAG = 'C:/bari_deanchor_wt/_rescore_staging'

// needs_copy: flips to (re)author. qa: everyone gets an independent gate.
const CATS = [
  {
    shelf: 'milk', artifact: `${SWEEP}/milk_frontend_v1_deanchor.json`,
    live: `${DATA}/milk_frontend_v1.json`, traces: `${STAG}/milk/products`,
    copy: [{ barcode: '7290110325619', from: 'D', to: 'C', dir: 'UPWARD' }],
    note: 'GOLD-STANDARD content page (owner_milk_page_content_gold_standard). Upward flip must be publicly defensible; match the existing milk-page voice exactly.',
  },
  {
    shelf: 'juices', artifact: `${SWEEP}/juices_frontend_v3_deanchor.json`,
    live: `${DATA}/juices_frontend_v3.json`, traces: `${STAG}/juices/products`,
    copy: [{ barcode: '7290019056737', from: 'D', to: 'E', dir: 'DOWNWARD' }],
    note: '',
  },
  {
    shelf: 'snacks', artifact: `${SWEEP}/snacks_frontend_v5_deanchor.json`,
    live: `${DATA}/snacks_frontend_v5.json`, traces: `${STAG}/snacks/products`,
    copy: [
      { barcode: '7290011498986', from: 'E', to: 'D', dir: 'UPWARD' },
      { barcode: '7290011498900', from: 'E', to: 'D', dir: 'UPWARD' },
    ],
    note: 'wf1 QA (HIGH) found these 2 flips shipped BYTE-IDENTICAL copy — re-author so the row acknowledges the new D grade. The other 3 snacks flips were already authored.',
  },
  {
    shelf: 'cookies_coffee', artifact: `${SWEEP}/cookies_coffee_frontend_v2_deanchor.json`,
    live: `${DATA}/cookies_coffee_frontend_v2.json`, traces: `${STAG}/cookies_coffee/products`,
    copy: [], note: 'Copy already authored in wf1 (8 flips). wf1 QA agent ERRORED before emitting a verdict — this run is the independent gate.',
  },
  {
    shelf: 'cakes', artifact: `${SWEEP}/cakes_hard_cookies_frontend_v1_deanchor.json`,
    live: `${DATA}/cakes_hard_cookies_frontend_v1.json`, traces: `${STAG}/cakes/products`,
    copy: [], note: '0 grade flips, 44 score moves. Combined cakes+hard-cookies page. QA parity + score propagation only.',
  },
  {
    shelf: 'bread', artifact: `${SWEEP}/bread_frontend_v4_deanchor.json`,
    live: `${DATA}/bread_frontend_v4.json`, traces: `${STAG}/bread/products`,
    copy: [], note: '0 grade flips, 1 score move. QA parity + score propagation only.',
  },
]

const QA_SCHEMA = {
  type: 'object',
  required: ['shelf', 'verdict', 'de_anchor_scores_correct', 'parity_clean', 'flip_copy_honest', 'decisive_reason'],
  properties: {
    shelf: { type: 'string' },
    verdict: { type: 'string', enum: ['GO', 'GO_WITH_FIXES', 'NO_GO'] },
    de_anchor_scores_correct: { type: 'boolean' },
    parity_clean: { type: 'boolean' },
    flip_copy_honest: { type: 'boolean' },
    critical_findings: { type: 'array', items: { type: 'string' } },
    high_findings: { type: 'array', items: { type: 'string' } },
    preexisting_debt_flagged: { type: 'array', items: { type: 'string' } },
    decisive_reason: { type: 'string' },
  },
}

const results = await pipeline(
  CATS,
  // Stage 1 — author flips in place (only if this cat has copy work)
  async (c) => {
    if (!c.copy.length) return c
    const flipList = c.copy.map(f => `${f.barcode} ${f.from}->${f.to} (${f.dir})`).join('; ')
    await agent(
      `You are the Content Agent (Tom-Bari Hebrew editorial voice). The continuous red-label de-anchor changed grades on the ${c.shelf} page. Re-author EACH flipped product's verdict (rowVerdict + insightLine) to match its NEW grade. EDIT THE FILE IN PLACE.\n\n` +
      `Artifact (edit directly): ${c.artifact}\n` +
      `Traces (ground truth — use ONLY these numbers): ${c.traces}\n` +
      `Flips: ${flipList}\n` +
      (c.note ? `\nIMPORTANT: ${c.note}\n` : '') +
      `\nHARD RULES: every number traces to bsip2_trace.json L1_observed_signals; no framework/score-mechanic vocabulary in copy; no OFF; touch ONLY the flipped products' rowVerdict/insightLine — never score/grade/rank/nutrition, never a non-flipped product. UPWARD flips must be honestly defensible (name what genuinely improved). Verify JSON still parses. Return a 1-line-per-flip summary of what you wrote and why.`,
      { label: `copy:${c.shelf}`, phase: 'Copy' }
    )
    return c
  },
  // Stage 2 — independent adversarial QA
  async (c) => {
    const v = await agent(
      `Adversarial QA gate on the ${c.shelf} de-anchor artifact (part of the full de-anchor sweep -> ONE combined go-live PR). Verify independently; trust nothing; re-derive from ground truth.\n\n` +
      `Artifact: ${c.artifact}\n` +
      `Live baseline: ${c.live}\n` +
      `Traces (ground truth): ${c.traces}\n` +
      (c.note ? `\nContext: ${c.note}\n` : '') +
      `\nVERIFY: (V) every product score+grade matches its bsip2_trace final_score_estimate/grade_estimate; rank is a clean permutation with 0 inversions; barcode parity vs live is exact (0 add/drop/dup); the claimed flips are exactly present in the stated direction; non-flip products keep byte-identical copy. (C) each flip's re-authored copy is honest and defensible against the trace (especially UPWARD flips — is the improvement real?); no framework leakage; no OFF; superlative claims still true post-shift. Run run_gates.py with --run ${c.traces} --baseline ${c.live}. Confirm whether any gate FAIL is pre-existing (reproduce on live) vs de-anchor-caused. _meta was regenerated post-build (grade_distribution/score_statistics/reflow re-derived, source_paths repointed to the de-anchor staging traces) — verify it is now self-consistent with the product array; flag if not.\n\n` +
      `Return the structured verdict. GO only if scores/parity/copy are all clean and any remaining gate FAIL is confirmed pre-existing. GO_WITH_FIXES for non-blocking metadata/debt. NO_GO only for a real rendered-score/parity/copy defect.`,
      { label: `qa:${c.shelf}`, phase: 'QA', schema: QA_SCHEMA, agentType: 'Adversarial QA Agent' }
    )
    return v
  }
)

const all = results.filter(Boolean)
return {
  go: all.filter(v => v.verdict === 'GO'),
  go_with_fixes: all.filter(v => v.verdict === 'GO_WITH_FIXES'),
  no_go: all.filter(v => v.verdict === 'NO_GO'),
  all,
}
