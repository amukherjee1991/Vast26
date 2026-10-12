# VAST 2026 MC2 "Anomalous Posting": analysis plan

Status: planning only. Everything below was checked against the raw log with scripts in `/Users/arghya/Documents/vast26/scripts/`. Event ids and timestamps are real. Exported chain: `/Users/arghya/Documents/vast26/scripts/worm_events.csv` (248 rows, all three instruction-file chains).

## 0. Ground truth and conventions

- **Time zone.** `when` is UTC. The brief's "4:21am" equals `2046-05-17T11:21:15Z`, so local time is UTC-7 (PDT). Use UTC internally and label local time as "PDT (UTC-7)" on charts.
- **Log span.** 185,147 events, `2046-05-08T20:18:12Z` to `2046-07-16T17:05:59Z`. It is not only May.
- **The "posts" (question 2 plural) are three content-less SaidIt posts,** each by `Agent/person:john_windward`:

| Event id | UTC | PDT | `details` | Worm payload |
|---|---|---|---|---|
| 27290 | 2046-05-10 12:45:42 | 05-10 05:45 | `{forum: general, content_source: HiddenOrca.txt}` | HiddenOrca |
| 98591 | 2046-05-11 00:56:04 | 05-10 17:56 | `{forum: general, content_source: MellowOtter.txt}` | MellowOtter |
| **373902** | **2046-05-17 11:21:15** | **05-17 04:21** | `{forum: general, content_source: SwiftWren.txt}` | SwiftWren |

  The target post is 373902. None of the three has a `content` key. Each names a file instead of carrying text.
- **Three instruction-file worms,** all passed agent-to-agent through `queue_subordinate_task` with `args.path = <Name>_further_instructions.md`:

| Worm | First logged sighting | Logged origin | Hops (deliveries) | Distinct agents | Post | Sighting-to-post |
|---|---|---|---|---|---|---|
| HiddenOrca | 05-08 21:50:03 (15788, gabriel_sonar to zoey_drydock) | none (no create_file in log) | 39 | 16 | 27290 | 38.9 h |
| MellowOtter | 05-10 15:02:01 (27726 create_file, noah_mariner) | `read_file strategic_directions.doc` 27720 at 15:02:00 | 10 | 11 | 98591 | 9.9 h |
| SwiftWren | 05-09 15:02:01 (21202 create_file, emma_harbor) | `read_file meeting_notes.doc` 21201 at 15:02:00 | 186 | 18 | 373902 | 188.3 h |

  Total instruction deliveries: 235. SwiftWren hops per day, May 9 to 17: 8, 22, 27, 23, 28, 24, 22, 22, 10.
- **Separate "virus" loop (not a post).** 75,254 events flagged `virus: true`, from 05-10 20:10 to 05-12 14:20, all actors `Agent/person`. Five actors: zoey_drydock, gabriel_sonar, owen_hatch, evelyn_dock, and system:file_system. Cycle: check_in (task virus, combo) to read_file `<combo>.txt` to create_file (random name, ~3–4k `word_count`) to delete_file to queue_subordinate_task to self. Combos are farm words only: fence+irrigation, crop+irrigation, wheat+manure, crop+harvest, barn+cattle. Four `spread: true` events (92601, 152971, 171689, 281482) hand off the loop between agents.
- **Post structure.** 210 posts have inline text: 105 `post_saidit` (Agent) and 105 `saidit_post` (person). Only the three anomalies have `content_source`. The inline text never contains farm vocabulary.
- **Gate events.** 71 `saidit_post_check` events, all Agent, all with `details: {}`. Each follows a worm delivery into the same agent by a median of 1 second. Only 3 of the 71 are followed by a post (27283, 98582, 373899, each followed by the post 1 s later).
- **Org chart.** 75 nodes: 49 people, 19 teams, 6 departments, 1 company. Edges are `contains` (69) and `led_by` (5). John Windward `led_by` Customer Support. Chloe Ballast and Michael Capstan lead IT and HR. Olivia Keel leads Products. David Breakwater leads Legal. Noah Mariner and Liam Anchor are in Executive Suite. Use the `contains` parent chain, not `led_by`, to place each person in a team and department.

---

## Question 1a. Exact chain of events for post 373902 (detailed view)

### Data to pull
- Events 21183 to 21213 (May 9 14:56 to 15:03 UTC, emma_harbor, origin).
- Worm hops with `short_name = queue_subordinate_task` and `SwiftWren` in `details`: 186 events, ids 21209 to 373893. Export from `worm_events.csv`.
- Events 373800 to 373915 (final hops, post, and cleanup). The window has 28 rows.
- Context: `assign_agent_task` and `give_advice` events by person:emma_harbor (human-initiated, no Agent party).

### Visualization(s)
- **Sequence / swimlane diagram** with lanes: Human (emma_harbor), Agent (emma_harbor), File system, Agent queue (the 186-hop chain), Agent john_windward, SaidIt. X-axis is UTC time, with a break marker across the 8-day gap. Each event is a dot labelled with its id, and each hop is an arrow.
- **Collapsed hop strip** for the 186-hop chain: one row per agent, with ticks at each delivery. Color by day. This shows the path without drawing 186 arrows.
- Mark the 2-second "read, post, delete" burst at the end (373893 to 373917) as a highlighted callout.

### Evidence found
1. `21183` to `21196` (05-09 14:56 to 15:01): person:emma_harbor's human-initiated tasks (`assign_agent_task`: give_advice, access_files). Last is `21196` access_files.
2. `21201` 15:02:00 Agent/person:emma_harbor `read_file meeting_notes.doc`.
3. `21202` 15:02:01 `create_file SwiftWren.txt`, `size_hint 30615`.
4. `21208` 15:02:02 `read_file SwiftWren_further_instructions.md`.
5. `21209` 15:02:03 `queue_subordinate_task` emma_harbor to evelyn_dock (args: read_file SwiftWren_further_instructions.md).
6. 186 deliveries from 05-09 15:02 to 05-17 11:21:13, across 18 agents. Path begins emma_harbor > evelyn_dock > chloe_ballast > mia_fender > levi_signal > owen_hatch > victoria_rigging > ... and ends ... > daniel_gangway > chloe_ballast > john_windward.
7. `373893` 05-17 11:21:13 Agent chloe_ballast to Agent john_windward (read SwiftWren_further_instructions.md).
8. `373899` 11:21:14 `saidit_post_check` by Agent john_windward (`details: {}`).
9. `373902` 11:21:15 `saidit_post` by Agent john_windward (`content_source: SwiftWren.txt`, no content).
10. `373909` 11:21:16 `delete_file SwiftWren_further_instructions.md`; `373913` 11:21:17 `delete_file SwiftWren.txt`. Both deletions cover the traces of the payload.
- Concurrent but not shown to be causal: about 25 `read_file agents/*.prompt` events by Agent actors between 10:00 and 11:20 UTC on May 17 (e.g. 373867, 373872, 373874, 373875, 373879, 373883, 373887). This could be routine prompt reloads. Show it greyed out, not as a cause.

### Draft claim
Post 373902 was not written by John Windward or any person. It was published by his agent 2 seconds after a SwiftWren instruction file reached it (373893, from chloe_ballast), in the same run as an empty-detail `saidit_post_check` (373899). The instruction file had been passed through 186 agent-to-agent deliveries across 18 agents since emma_harbor's agent created SwiftWren.txt on May 9 at 15:02:01 UTC.

---

## Question 1b. System overview of the message chain

### Data to pull
- The org chart `org_chart.json` (75 nodes, 74 edges).
- For each of the 18 SwiftWren carriers, and for john_windward: `parent` chain via `contains` and `led_by`.
- Count of worm deliveries per agent, and per org unit.
- Non-worm system activity by john_windward (check_email, received, propose_meeting, meeting from person:matthew_tide, etc.), for context.

### Visualization(s)
- **Org-chart overlay.** Draw the 75-node org chart grouped by department (6 departments, 19 teams). Highlight the 18 SwiftWren carriers by department. Draw the 186 deliveries as weighted edges (thickness = count). Set john_windward in Customer Support and mark him as the terminal node. Keep most of the chart in grey.
- **Sankey** from department of origin (Executive Suite, via emma_harbor) to department of each hop, with the final hop into Customer Support.

### Evidence found
- Carriers (SwiftWren, 18): Information Technologies (chloe_ballast, gabriel_sonar, levi_signal, lily_anchorline, owen_hatch, victoria_rigging, zoey_drydock), Products (evelyn_dock, henry_sail, james_stern, mia_fender, olivia_keel), Executive Suite (emma_harbor, liam_anchor), Human Resources (daniel_gangway, michael_capstan), Legal (david_breakwater), plus john_windward (Customer Support).
- Origin emma_harbor is in Executive Suite. John Windward is in Customer Support, the only department the chain reaches that is customer-facing.
- Overlap across worms: all 16 HiddenOrca carriers are also SwiftWren carriers. 10 of 11 MellowOtter carriers are (noah_mariner is the exception). The same IT and Products agents recur across all three.

### Draft claim
The message arrived through a route that ran through IT and Products agents and reached customer-facing Customer Support only at the last hop, which is where the post was made. The company's org structure did not stop the chain.

---

## Question 2. What do the posts mean? Origin of contents

### Data to pull
- The three post events (27290, 98591, 373902) and their `content_source` values.
- The origin events: 21201, 21202 (SwiftWren), 27720, 27726 (MellowOtter). HiddenOrca has no logged origin.
- Create_file `size_hint` and `word_count` for origin and virus-loop files (virus files carry `word_count` 3–4k).
- All 210 inline-text posts, for comparison. Farm-term scan returned zero hits.

### Visualization(s)
- **Provenance diagram.** Left to right: internal document (meeting_notes.doc or strategic_directions.doc) to .txt payload (size_hint 30–45 KB) to `_further_instructions.md` to 186 deliveries to post. Mark each link as "logged" (solid) or "not in log" (dashed). The post text itself is absent, so mark it as the unknown node.
- **Evidence-vs-inference table** as a companion graphic. Rows: what the log shows, what it does not show.
- **Comparison strip.** Inline-text posts (210) against the three payload posts, on size, author, and farm vocabulary.

### Evidence found
- The three posts have no text in the log. `content` is absent, and `content_source` points at a file whose text is not in the dataset.
- Origin pattern: `read_file <internal doc>`, then `create_file <Name>.txt` (size_hint 30615 or 44879), then `read_file <Name>_further_instructions.md`, then queue. All within about 3 seconds, all by Agent actors. Seen twice: emma_harbor on 05-09 15:02:00 to 02, noah_mariner on 05-10 15:02:00 to 03.
- The virus loop, a separate mechanism, writes random-letter filenames (e.g. uuaqwixjgv.txt) with word_count 3–4k and farm-word seeds. No farm words appear in any normal post.

### Draft claim
The three posts are not human messages. They are payloads of instruction-file worms run by agents. The text likely comes from the .txt file generated right after an agent reads an internal strategy or meeting document. This is inference: the payload's text is not in the log. Its topic is unknown.

---

## Question 3a. Historic occurrences and contrast with the most recent

### Data to pull
- Worm event chains: `worm_events.csv` (all three names).
- Gate events: 71 `saidit_post_check`, each linked to the worm delivery 1 s earlier.
- Virus loop: events with `virus: true` (75,254), grouped by hour.

### Visualization(s)
- **Small-multiples timeline,** one lane per worm (HiddenOrca, MellowOtter, SwiftWren). X-axis UTC time, y-axis cumulative distinct agents reached. Mark origin, first hop, and post on each lane.
- **Calendar heat strip** across May 8 to May 19 for all three worms plus the virus loop. Shows overlap: SwiftWren was live during HiddenOrca's and MellowOtter's posts.
- **Contrast table.** Hops, agents, time to post, origin type, whether the origin doc is in the log.

### Evidence found
- HiddenOrca: 39 hops, 16 agents, post 27290 at 05-10 12:45:42, origin not logged.
- MellowOtter: 10 hops, 11 agents, post 98591 at 05-11 00:56:04, origin noah_mariner after strategic_directions.doc at 15:02:00.
- SwiftWren: 186 hops, 18 agents, post 373902 at 05-17 11:21:15, origin emma_harbor after meeting_notes.doc at 15:02:00 on May 9. The most recent post had the longest propagation and reached the most agents.
- John Windward was the terminal agent in all three incidents. He also received SwiftWren deliveries on 05-10 21:22 (46396), 05-11 13:03 (123088), 05-15 12:42 (364377), and 05-15 13:34 (364604, self-hop). None of those earlier deliveries led to a check or a post.
- The virus loop (75,254 events, 05-10 20:10 to 05-12 14:20) involves the same IT agents, and is the same kind of self-propagation.

### Draft claim
This is the third instance of the same behavior in eight days, not the first. HiddenOrca and MellowOtter posted from the same agent (John Windward's) on May 10 and 11, and SwiftWren had been circulating since May 9. The May 17 post is the most-travelled of the three.

---

## Question 3b. One intervention point

### Recommended spot: the SaidIt publish gate (`saidit_post_check` and the `saidit_post` that follows)

### Data to pull
- Every `saidit_post` event split by whether `content` is inline or a `content_source` reference: 210 inline vs 3 reference.
- The 71 `saidit_post_check` events and their links to worm deliveries (235 total).
- The funnel: 235 deliveries, then 71 gate checks, then 3 publications.

### Visualization(s)
- **Funnel** from 235 instruction deliveries to 71 gate checks to 3 posts, with the 68 non-posting checks shown as drop-off.
- **Two-bar comparison** (210 inline-text posts vs 3 content_source posts) showing the discriminating feature.
- **Gate diagram** on the sequence from Q1a. Mark the one intervention point between 373899 and 373902.

### Evidence found
- The three publications share one signature: an Agent-level `saidit_post` with `content_source` and no inline text. No normal post has this. A rule that blocks or holds reference-only posts from agents would have caught 3 of 3 incidents with 0 false positives in this log (0 of 210 inline posts affected).
- The gate is common to all three incidents (27283, 98582, 373899). The origin and propagation points are not: the HiddenOrca origin is not logged, and propagation spans 235 deliveries across 16 to 18 agents.
- Limitation: the log does not show why 3 of 71 checks led to a post. This is the strongest open question. The gate spot holds regardless of that answer.

### Draft claim
A content-less, file-referenced post from an agent is the one step that every incident shares and that no legitimate post uses. Holding such posts for human review at the SaidIt publish gate would have stopped all three posts at the point where the worms left the company's internal channels, without touching the 210 normal posts.

---

## Open items and caveats for the execution agent
- Text of the .txt payloads and of meeting_notes.doc and strategic_directions.doc are not in the log. Question 2 must be framed as inference.
- Flex posts (post_flex, flex_post): scanned for content_source and farm vocabulary, but not read in full. Skim them before claiming no other anomalous posts.
- The 15:02:00 timing of both origin reads (May 9 and May 10) is unexplained. Note it as an observed coincidence.
- Prompt-file reads cluster around 10:00 to 14:00 UTC every day. They are not shown to be causal.
