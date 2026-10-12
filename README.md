# Forensic Ledger — VAST Challenge 2026

Two incident reports on an agentic-AI system at TenantThread, built from the
IEEE VAST Challenge 2026 Mini-Challenge data:

- **MC1 — The HarborCrest Leak.** An embargoed merger surfaces 35 minutes
  early, posted from an AI legal agent's own account. Deliberate sabotage, or
  a system that broke under pressure?
- **MC2 — SwiftWren.** A gibberish post lands on a public forum at 4:21am.
  Underneath it: an agent-to-agent worm that moved through 18 agents over 8
  days before three gate checks out of 71 let a payload through.

## Repo layout

- `app/` — Vite + React 19 + TypeScript + D3 site, deployed to GitHub Pages.
- `pipeline/` — Python scripts that turn the raw challenge JSON into the
  processed JSON the app reads from `app/public/data/`.
- `data/` — downloaded challenge data (gitignored; see `data/README.md` if
  present, or re-download from the challenge repo).
- `plans/`, `answers/`, `scripts/` — the original analysis: verified causal
  chains, draft answer-sheet text, and the throwaway scripts used to confirm
  every fact against the raw event logs.
- `design-system/` — the "Forensic Ledger" token set and brand book this app
  is built from.
- `findings/`, `docs/` — longer-form write-ups and the build plan.

## Local dev

```sh
cd app
npm install
npm run dev
```

## Data pipeline

```sh
python3 -m venv .venv
.venv/bin/pip install -r pipeline/requirements.txt
.venv/bin/python pipeline/build_all.py
```

## Deploy

Push to `main`; GitHub Actions builds `app/` and publishes to GitHub Pages.
