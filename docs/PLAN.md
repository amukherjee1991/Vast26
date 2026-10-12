# Build plan

## Done

- MC1 and MC2 causal chains fully verified against raw data (see `plans/`,
  `answers/`, `scripts/`).
- "Forensic Ledger" design system: tokens, brand book, CVD-validated
  categorical palette (`design-system/forensic-ledger-tokens.json`).
- App scaffold: Vite + React 19 + TS + D3 + react-router-dom, tokens ported
  into `app/src/styles/tokens.css`, GitHub Actions → Pages workflow.

## Open

- [ ] `pipeline/mc1_build.py` — bake `MC1_final_00.json` + the verified
      chain/baseline/leading-indicator findings into `app/public/data/mc1.json`.
- [ ] `pipeline/mc2_build.py` — bake `MC2 data.json` / `worm_events.csv` +
      the verified SwiftWren/HiddenOrca/MellowOtter findings into
      `app/public/data/mc2.json`.
- [ ] `app/src/pages/MC1.tsx` + `app/src/pages/mc1/*` — port the MC1 Claude
      Artifact's visuals (crisis-day swimlane, baseline-vs-crisis comparison,
      leading-indicators timeline) into React/D3 components.
- [ ] `app/src/pages/MC2.tsx` + `app/src/pages/mc2/*` — port the MC2 Claude
      Artifact's visuals (SwiftWren hop chain, org-chart overlay, 3-worm
      small-multiples, intervention funnel) into React/D3 components.
- [ ] Author placeholders in `submission/MC*.md` (name, affiliation, hours).
- [ ] First deploy + visual QA pass against both themes/breakpoints.
