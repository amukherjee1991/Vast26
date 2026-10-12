# VAST Challenge 2026 — Mini-Challenge 2: Anomalous Posting
## Answers (prose only — for the official submission form)

Grounded in `MC2 data.json` (185,147 events, 2046-05-08T20:18:12Z – 2046-07-16T17:05:59Z) and `org_chart.json` (75 nodes). Interactive version with all exhibits: https://claude.ai/artifact/BJgCo6onNy3Qi6pQEqDhj7

---

### Question 1a — Detailed chain of events for the message of interest

The post that reached SaidIt at 2046-05-17T11:21:15Z (04:21 local) is event 373902 — Agent/person:john_windward posting to system:saidit with details {forum: "general", content_source: "SwiftWren.txt"} and no content field. Nothing John Windward did produced it; his agent published it two seconds after an incoming instruction file.

The chain starts eight days earlier. At 15:02:00 UTC on May 9, emma_harbor's agent reads meeting_notes.doc (21201), then at 15:02:01 creates SwiftWren.txt (21202, 30,615 bytes), then at 15:02:02 reads SwiftWren_further_instructions.md (21208), then at 15:02:03 queues that same read task on evelyn_dock's agent (21209) — the first of 186 agent-to-agent deliveries that pass across 18 agents over the next eight days: 8 hops on day one, peaking at 28 on May 13, down to 10 on May 17.

John Windward's agent is not a first-time recipient. It receives the same instruction file four times before this — from olivia_keel, liam_anchor, olivia_keel again, and itself in a same-agent loop — and forwards it onward three of those times, twice to owen_hatch and once to gabriel_sonar. None of those triggers anything. The fifth delivery, from chloe_ballast at 11:21:13, is the one that does: one second later an empty-detail saidit_post_check fires (373899), one second after that the post (373902), then SwiftWren_further_instructions.md is deleted (373909) and one second after that so is SwiftWren.txt (373913) — erasing the only record of what the payload said.

### Question 1b — System overview of the message chain

Zoom out from the 186-hop thread to where it sits in the company. Tenant Thread's org chart has 75 nodes — one company, 6 departments, 19 teams, 49 people — connected mostly by `contains` edges, plus five `led_by` edges naming department heads (chloe_ballast / IT, olivia_keel / Products, michael_capstan / HR, david_breakwater / Legal, john_windward / Customer Support).

Of the 18 agents SwiftWren passed through, 7 sit in Information Technologies — all 7 of IT's people — 5 in Products (of 13), 2 in Executive Suite (of 3, where the file originated), 2 in Human Resources (of 6), and 1 in Legal (of 9). Traffic stays heaviest inside IT and Products: 44 IT-internal hops, 60 combined IT↔Products hops. Customer Support — 11 people, not the usual correspondents of software agents — is touched exactly once, on the final hop, when chloe_ballast's IT agent reaches john_windward.

The earlier worms show the same shape: HiddenOrca (16 agents, all also SwiftWren carriers) and MellowOtter (11 agents, 10 shared with SwiftWren) both cross IT and Products for most of their length and reach Customer Support only at the post. Department boundaries slowed nothing; John Windward is simply the one carrier whose role is public-facing, so his agent is the one that publishes.

---

### Question 2 — What do the posts mean? Origin of their contents

All three anomalous events — 27290 (May 10), 98591 (May 11), 373902 (May 17) — share one trait: no content field, only content_source naming a .txt file. None of those files, or the text they held, survive in the log; John Windward's agent deletes them one to two seconds after posting. So the honest answer to "what do the posts say" is: **we don't know, and can't recover it.**

What the log does show is how each payload was built. Twice — emma_harbor on May 9 at 15:02:00–01 (meeting_notes.doc read, then SwiftWren.txt created, 30,615 bytes), and noah_mariner on May 10 at 15:02:00–01 (strategic_directions.doc read, then MellowOtter.txt created, 44,879 bytes) — an agent reads an internal company document and, one second later, writes a same-order-of-magnitude text file under the worm's name. That one-second read-then-write pattern is the strongest evidence for probable content: some transformation of that internal document, not arbitrary noise. HiddenOrca's own origin was never logged, so its payload's source is unconfirmed by this method.

It is not the farm-themed "virus" loop running in parallel (75,254 events, May 10 20:10 – May 12 14:20, combos like fence+irrigation): that loop's own files (e.g. jbuosfctyfx.txt) are created and deleted independently of the worm — one such cycle runs within the very same second as the MellowOtter post. The two mechanisms coexist in the log; only one of them posts, and no farm vocabulary appears in any of the 210 posts we can actually read.

---

### Question 3a — Historic occurrences, contrasted with the most recent

May 17 was the third time, not the first. HiddenOrca posted on May 10 at 12:45:42; MellowOtter on May 11 at 00:56:04; SwiftWren on May 17 at 11:21:15 — and SwiftWren had already been circulating for a day before HiddenOrca's post and for two before MellowOtter's.

The three differ mainly in scale. HiddenOrca: 39 deliveries, 16 agents, no origin visible, 38.9 hours from first sighting to post. MellowOtter: 10 deliveries, 11 agents, origin logged, 9.9 hours — the fastest of the three. SwiftWren: 186 deliveries, 18 agents, origin logged, 188.3 hours — nearly five times HiddenOrca's span and nineteen times MellowOtter's: the slowest-burning and farthest-reaching.

All three share a carrier set — every HiddenOrca agent is also a SwiftWren agent, and 10 of MellowOtter's 11 are (noah_mariner is the exception) — and John Windward's agent is the terminal node in every case. Each worm is also a repeat visitor to him specifically: SwiftWren alone reached his agent five separate times over seven days before the delivery that finally posted. The pattern is not three unrelated incidents; it's the same mechanism, recurring, with no sign it has stopped.

A fourth, unrelated phenomenon runs in the same window: a farm-themed "virus" loop of 75,254 events (May 10, 20:10 – May 12, 14:20) cycling through the same IT agents who carry the real worms, yet never once producing a post. It's a second anomaly in this log — worth distinguishing from SwiftWren, not folding into it.

### Question 3b — One intervention, and why it would work

Every worm delivery that's followed by a saidit_post_check — 71 of the 235 total; what decides which 71 isn't visible in the log — fires it almost exactly one second later, and only 3 of those 71 reach an actual post one second after that. This check never appears before any of the 210 legitimate posts, so it reads as part of the worm's own behavior rather than a company control. It already fails to post 68 times out of 71 — but it offers no visibility into why it let 3 through, and it's absent entirely from the other 164 deliveries. It is not something to build a fix on.

What is visible and consistent is the shape of the 3 posts that got through: an Agent-level saidit_post with content_source set and no content field. No other post in the dataset has that shape — of 210 legitimate posts (105 by people, 105 by agents), all carry inline text and none reference an external file.

**The intervention:** hold any saidit_post from an Agent party whose body is content_source-only for human review before it publishes — independent of whatever saidit_post_check is doing. Tested against this log, that single rule catches HiddenOrca, MellowOtter, and SwiftWren, 3 of 3, and never fires on the 210 ordinary posts. It sits at the one point every incident shares: the instant an agent tries to publish a file it never shows anyone.
