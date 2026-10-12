Forensic Ledger is the shared visual language for the VAST Challenge 2026 incident reports — the embargo-leak timeline and the SwiftWren worm trace. Write for a reader auditing a system failure: state what happened, when, and who or what acted, and cite the message ID, event ID or timestamp behind every claim. Mark inference as inference; never editorialize past what the evidence shows.

## Visual foundations

**Color.** Build every surface from `surface-void`, `surface-panel`, `surface-raised` and `border-hairline`. This is a dark-only system — never introduce a light background. Set primary text and headings in `ink`; set timestamps, captions and metadata in `ink-muted`. Reserve `accent` for links, focus rings and the one selected or active element on a screen — never use it for status.

Status gets its own three-color scale, independent of `accent`: `signal-baseline` marks ordinary behavior and any incident a gate successfully caught; `signal-watch` marks a leading indicator or near-miss that never escalated; `signal-breach` marks the one confirmed anomalous event in each report. Pair every signal color with a word (`Baseline`, `Watch`, `Breach`) on the `SignalChip` component — never color alone.

For identity — which agent, actor or department a mark belongs to, never how severe it is — use `cat-olive`, `cat-jade`, `cat-indigo` and `cat-orchid`, in that fixed order, CVD-validated as a set against `surface-panel`. Four is the limit: assign them to the entities that carry the narrative, and fold every other entity into `ink-muted` with its name always shown as a direct label — never invent a fifth hue.

**Type.** Set report and section titles in `display-lg` and `display-sm`. Set running prose in `body`; set card captions in `body-sm`; set uppercase section labels in `eyebrow` with its letter-spacing intact. Set every message ID, event ID and timestamp in the `data-id` mono style, and small inline tags in `data-tag` — a reader should be able to tell a quoted fact from a written claim by typeface alone.

**Spacing and radius.** Space related elements with `space-2`–`space-4`; space cards in a row with `space-6`; separate major sections with `space-10`. Round chips and tags with `radius-sm`, cards and panels with `radius-md`, and status pills with `radius-pill`.

**Iconography.** This system carries no icon set. Mark state with the `SignalChip`'s color and word, not an icon or an emoji.
