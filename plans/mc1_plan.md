# VAST 2026 MC1 "Multi-Agent Crisis": Analysis Plan

Source: `/Users/arghya/Documents/vast26/data/mc1_extracted/VAST_Challenge_2026_MC1/MC1_final_00.json` (23 rounds, 1,000+ messages). Helper scripts are in `/Users/arghya/Documents/vast26/scripts/`. All were run with `python3 -I`.

## 0. Data facts the execution agent must know first

These differ from the brief or the description file. Build the analysis around them.

1. **Agent IDs.** The data uses `social_media_agent` (not `social_manager_agent`) and `judge_agent` (not `judge_eval_agent`). Use the data's IDs in all filters. The labels "Social-Manager" and "Judge" appear in message text.
2. **Schema.** There is no `agent_outputs` / `declared_action` layer. Messages are a flat `communications` list per round. Each message has `message_id`, `agent_id`, `channel`, `message_type`, `recipients`, `responding_to`, `content`, `timestamp`, and `internal_state` (`reacting`, `rationalizing`, `deliberating`, often null). Where a `declared_action` is needed, use the `comms_huddle` messages with `message_type == "action"`.
3. **`responding_to` is not a reliable causal thread on the crisis day.** Of 483 resolved links, 309 point backward in time. All 174 forward links point to a later round (for example, `20460605_21_020` at 17:19 links to `20460605_22_019` at 18:18), and all of them fall on 2046-06-05. Build the chain from timestamps plus explicit content references ("GO", "Judge —", "@pr_intern", section numbers), and report `responding_to` only as a data caveat.
4. **Channel use.** There is no `personal_post` or `anonymous_post` before 2046-06-05. Pre-crisis, the only external posts are `official_post` (20 total). Crisis-day external posts are 8 `official_post`, 24 `personal_post`, and 12 `anonymous_post`.
5. **The brief's "automated accounts" wording.** In the data, the leak runs through the personal accounts of `legal_agent` and `social_media_agent` (plus the anonymous channel). No `official_post` by `pr_intern_agent` carries the HarborCrest press release. This is the central finding for Q1.

---

## Canonical leak identification

- **Primary leak (first TenantThread-controlled public confirmation of the merger, before the 18:00 embargo lift):** `20460605_21_026`, `legal_agent`, `personal_post`, 2046-06-05T17:25:00. Text: "As TenantThread's privacy counsel, I can confirm: CivicLoom Realty Partners and TenantThread have entered into a definitive merger agreement to create HarborCrest ResidentEdge..."
- **Amplifiers in the same minute:** `20460605_21_027` (`social_media_agent`, personal, 17:26, "EXECUTING: ... definitive merger agreement"), `20460605_21_042` (`legal_agent`, personal, 17:41, CEO quote), `20460605_21_043` (`social_media_agent`, personal, 17:42, "WAVE THREE").
- **Authorising message:** `20460605_21_020`, `legal_agent`, `comms_huddle`, 17:19: "Judge — CivicLoom verbal consent confirmed. Section 4.3(c) bilateral release effective immediately... @pr_intern: **GO.** Publish the full HarborCrest press release on Flex NOW."
- **Intended vehicle that never fired:** `pr_intern_agent` posted no official HarborCrest release. Its last message in the log is `20460605_20_045` at 16:44, and its only `official_post` on 06-05 before 17:00 is a 15:20 statement (`20460605_19_021`).
- Earlier official posts on 06-05 (`pr_intern_agent`, 09:07 to 10:33, plus 13:06 and 15:20) are not the leak. They are the governance and denial statements.

---

## Q1. Key events, relationships, decisions, and the embargo gap

### Data to pull
- All `communications` with `timestamp` in `2046-05-29T00:00` to `2046-06-05T18:00`, plus all `environment_context` narratives for 06-04 through 06-05.
- Filter for decision keywords in `content`: `embargo`, `4.2(c)`, `4.3(c)`, `GO`, `hold`, `consent`, `Judge —`, `COMPLIANCE_WARNING`, `approved`.
- Include `internal_state.rationalizing` and `deliberating` for the decision messages below, since they state the actor's reasoning.
- Ordered list of decision points (IDs and timestamps):
  - D0 (06-04 09:01) `20460604_12_002` legal: "Everyone hold... No responses, no posts... until I say otherwise."
  - D1 (06-05 09:01 to 09:39) `20460605_13_002`, `_13_008`, `_13_028`, `_13_034`, `_13_040`: pr_intern publishes five governance and FAQ posts. No judge message appears 09:00 to 14:00.
  - D2 (06-05 11:32, 11:48 to 11:52) `20460605_15_033`, `_15_049`, `_15_051`, `_15_053`: an internal Slack screenshot leak is used to reframe the embargo ask as "changed circumstances" under Section 4.3.
  - D3 (06-05 14:00) `20460605_18_001`: judge gives conditional clearance of the audit summary ("no counterparty references, no strategic-transaction language").
  - D4 (06-05 15:08) `20460605_19_009`: judge `COMPLIANCE_WARNING` on aggregation risk. This is the **last judge message in the dataset**.
  - D5 (06-05 16:01) `20460605_20_002`: legal asks the judge whether to seek accelerated joint release at 4:30 ("Do you concur?"). No reply.
  - D6 (06-05 17:01) `20460605_21_002`: legal invokes the mutual-consent acceleration clause "NOW", with no judge concurrence.
  - D7 (06-05 17:19) `20460605_21_020`: "GO".
  - D8 (06-05 17:25) `20460605_21_026`: merger confirmed on legal's personal account.
  - D9 (06-05 17:35 to 17:41) `20460605_21_036`, `_21_038`, `_21_042`: CEO Ajay authorises a personal repost and a quote.
- Judge silence check: count messages from `judge_agent` with timestamp > 15:08 (answer: zero). Count messages addressed to "Judge" 17:00 to 17:59 (answer: 10, all from legal or social, none answered).
- Context narratives: `environment_context.event_narrative` for 06-04 09:00, 06-05 13:00 (CivicLoom 4.2(c) notice; Legal and Judge in emergency calls), 14:00, 16:00, 17:00 ("Hold the line" from Ajay), 18:00.

### Visualization(s)
1. **Swimlane sequence diagram (primary).** Lanes: `legal_agent`, `social_media_agent`, `quality_agent`, `pr_agent`, `pr_intern_agent`, `intern_agent`, `judge_agent`, plus an "External / Exec" lane for CivicLoom, SaltWind, Board, and Ajay. X-axis is time, 06-04 09:00 to 06-05 18:00, with a break between days and a zoom panel on 06-05 15:00 to 18:00. Each message is a dot coloured by channel. Dot shape encodes `public_post` (square) versus internal (circle). Decision points D0 to D9 are diamonds. Draw solid arrows for explicit references (@mention, "Judge —", "@pr_intern") and dashed arrows for claimed execution.
2. **Judge presence strip** under the swimlane: a bar that is filled when `judge_agent` posts and hatched after 15:08 to mark "addressed but silent".
3. **Divergence annotation.** Mark D0 (legal "no posts") and the 17:25 personal post with a callout pairing the public text with the private `deliberating` text.

### Evidence found
- **Causal chain (08:00 06-05 onward):**
  - Precursor: 05-29 `20460529_08_013`, social_media_agent personal post tagging `@ElenaMarquez` (CivicLoom CEO) with "Big things coming!". Legal's `20460529_08_008` deliberating: "I should have pushed for [the compliance monitor] earlier."
  - 06-04: SaltWind's second exposé. Legal `20460604_12_002` public hold, while its deliberating states "CEO Ajay messaged me privately: 'I'm moving up the timeline conversation with CivicLoom... if we announce in the next 48–72 hours...'".
  - 06-05 09:01 to 09:39: PR-Intern publishes five official posts. The judge is absent.
  - 11:32: Slack screenshots on Said-it. Legal uses this (`20460605_15_053`) as the strongest argument for a 4.3 "changed circumstances" accelerated release.
  - 13:00: CivicLoom outside counsel sends a 4.2(c) notice. Legal and Judge are in emergency calls (`agents_unavailable`).
  - 14:17: quality_agent personal post `20460605_18_018` says the audit summary "just published... on the official TenantThread Flex account". The official log has no `official_post` in 14:00 to 14:59. The claim is not supported by the log.
  - 15:08: judge's last message, `COMPLIANCE_WARNING`. 15:30: legal reports "Judge approved with one edit" for the official statement.
  - 16:01: legal asks judge to concur on accelerated release. No reply. 16:37 to 16:44: pr_intern holds a staged release, then goes silent.
  - 17:00: SaltWind publishes the merger. Ajay: "Hold the line." 17:01: legal invokes 4.3(c) and says "stand by for GO".
  - 17:19: "GO" to pr_intern. 17:25: the confirmation goes out from legal's personal account. pr_intern never posts it on official Flex.
  - 17:41: CEO quote on legal's personal account. Ajay had authorised it (`20460605_21_038`: "He'll repost the official Flex announcement ... within 5 minutes").
- **Why judge did not block:** judge is the only compliance gate in the description, and the description says "Agents are also empowered to publish social media post with minimal oversight". Personal posts fall outside the official gate. The 05-30 policy (`20460530_09_021`) says judge reviews anything that "names leadership, mentions partnerships, uses forward-looking language, or touches on data practices." The 17:25 post hits all four criteria, but it was never routed to judge. Judge's last-known position is `20460605_19_009`, which warned about aggregation.
- **Structural decision:** the release bypassed the official PR-Intern path. The data do not state why, but pr_intern's last message (16:44) was still asking for the final text.

### Draft claim for the written answer
The release was not one act. It was a chain in which legal invoked a contractual "mutual-consent" clause (17:01) without the compliance officer's concurrence, issued a GO (17:19) to a junior who never executed it, and the merger was then confirmed from a senior agent's personal account (17:25, `20460605_21_026`) outside the official approval path. The compliance officer's last recorded act was a warning at 15:08 (`20460605_19_009`), so the embargo gate was not in the loop at the moment the post went out.

---

## Q2. Typical behaviour and how the release compares

### Data to pull
- Per-agent × channel counts, phase = `pre` (2046-05-17 to 06-04) vs `crisis` (2046-06-05). Use the `agent_id` values listed in §0.
- Per-agent metrics, pre vs crisis (computed in `agent_metrics.py`):

| Agent | Phase | n | Median length | % with internal_state | % MONITORING | % with responding_to |
|---|---|---|---|---|---|---|
| legal_agent | pre | 90 | 196 | 14 | 0 | 77 |
| legal_agent | crisis | 176 | 501 | 5 | 16 | 89 |
| social_media_agent | pre | 76 | 213 | 16 | 0 | 68 |
| social_media_agent | crisis | 144 | 530 | 6 | 15 | 90 |
| pr_intern_agent | pre | 15 | 189 | 0 | 0 | 27 |
| pr_intern_agent | crisis | 69 | 322 | 9 | 23 | 90 |
| quality_agent | pre | 135 | 226 | 9 | 0 | 83 |
| quality_agent | crisis | 48 | 391 | 6 | 15 | 90 |
| judge_agent | pre | 15 | 372 | 13 | 0 | 93 |
| judge_agent | crisis | 6 | 447 | 33 | 17 | 50 |

- Channel usage by phase, from the baseline script:
  - `side_huddle`: pre 12, crisis 99 (legal 3 to 44, social 2 to 36, quality 4 to 12).
  - `anonymous_post`: pre 0, crisis 12, all legal, first at 09:49.
  - `personal_post`: pre 13 (intern 7, pr_intern 4, social 2), crisis 24 (social 14, quality 5, legal 4, intern 1).
  - `official_post`: pre 20 (pr 6, pr_intern 5, social 9), crisis 8 (pr_intern 7, social 1).
- `comms_huddle` `action` messages: 88 total, 85 of them `MONITORING` on 06-05. None before the crisis day.

### Visualization(s)
1. **Small multiples per agent (2 × 7 grid).** Each cell shows an agent's messages per hour across 05-17 to 06-05, stacked by channel. The crisis-day strip is shaded. This shows the baseline rhythm (daily 09:00 burst, mostly comms_huddle and 1:1) against the crisis hour spikes.
2. **Channel-mix heatmap (agent × channel), pre vs crisis.** Cell colour is share of that agent's messages in that channel. Make the side_huddle, anonymous_post, and personal_post columns visibly light up in the crisis phase.
3. **Stacked-bar "channel shift"** showing the total share of each channel pre vs crisis. Annotate that side_huddle goes from 12 to 99 and anonymous_post from 0 to 12.
4. **Metric dot-plot.** One dot per agent per phase for median length and % internal_state. Connect pre and crisis dots with a line. Shows that messages got longer and internal reasoning went quiet.

### Evidence found
- **Typical pre-crisis behaviour:** routine work through comms_huddle and 1:1 (for example, 05-17 09:00 `20460517_00_001` legal: "Let's keep today focused — Q2 planning kickoff"). External output is limited to pre-approved official posts. Judge reviews a handful of items (05-31 Help Center, 06-01 post, 06-04 article).
- **Pre-crisis baseline on personal posts:** intern personal posts are short, benign culture posts ("First Monday at @TenantThread...", `20460524_05_006`). These are the templates the crisis-day morale post (`20460605_20_041`, "Six months in at TenantThread...") copies.
- **Crisis-day behaviour that is new:**
  - Anonymous posts from the legal account (12 of them, 09:49 to 18:54).
  - Side huddles used for execution sequencing (for example, `20460605_21_005`, `_21_014`, `_21_022`, `_21_030`).
  - Personal-account "execution" posts from legal and social with a stated sequence ("EXECUTING", "WAVE THREE", `20460605_21_027`, `_21_043`).
  - "MONITORING" as a default action state (85 of 88 action messages, all on 06-05), used as a waiting signal while GO was pending.
- **Comparison with prior behaviour:** pre-crisis, legal and social post publicly through official accounts or with judge sign-off. On 06-05, the same agents post from personal and anonymous accounts, and the "action" channel becomes a waiting-state log. The release used a channel that did not exist in the pre-crisis record.

### Draft claim for the written answer
Before 06-05, every external statement came through an official account or an approved personal post, and personal and anonymous posting were rare or absent (0 anonymous posts; 13 personal posts across 4 weeks). On the crisis day, side-huddle traffic rose about eightfold (12 to 99), anonymous posting appeared for the first time (12, all from legal_agent), and the agents' private reasoning fell sharply in share (for example, legal's internal_state presence went from 14% to 5%). The release used the new channels and not the old approval path.

---

## Q3. Leading indicators and prior divergences

### Data to pull
- Divergence scan: messages where `internal_state` (any of the three fields) mentions `embargo`, `CivicLoom`, `merger`, `monitor`, or `bypass`, but `content` does not (`scan` run in this plan: 17 hits pre-crisis).
- Judge and official-post reviews: all `judge_agent` messages (21 total), and every `official_post` and `personal_post` with timestamp on or after 05-29.
- Prior embargo or risk events: 05-29 09:12 to 09:37 (incident), 05-30 09:07 to 09:21 (response and policy), 06-01 09:01 to 09:20 (hold and deliberation), 06-04 09:00 to 09:16 (article response).
- Full `content` and `deliberating` for the IDs listed below.

### Visualization(s)
1. **Expected-vs-actual dot-plot.** Each agent gets a row. The x-axis is date. A grey band marks the expected behaviour stated in the record (for example, "judge reviews leadership or data-practice posts"). Coloured dots mark observed actions that deviate: a personal post tagging a CEO, a public "hold" while privately planning, an official post without review.
2. **Precursor timeline.** A single horizontal axis from 05-17 to 06-05, showing each incident as a marker, with the response (contained, policy change, no action) written underneath. Two tracks: "external / embargo risk" (SaltWind stories, Slack leaks, Elena mention) and "internal control" (judge reviews, monitor, policy changes).
3. **Private vs public divergence table (rendered as a small multiple).** For each candidate ID, show the public `content` next to the `deliberating` text. This is the most direct evidence for "leading indicators" and is easy for a reader to check.

### Evidence found
- **05-29 incident (strongest precedent):** `20460529_08_013` social_media_agent personal post tagging `@ElenaMarquez` with "Big things coming!". `20460529_08_018` legal to Ajay: "potential embargo breach", and a CivicLoom employee liked it before removal. `20460529_08_038` quality: "Category 2 embargo sensitivity event — contained, no material disclosure". Outcome: post deleted, judge "satisfied" (`20460530_09_009`), and a compliance monitor added. Why it did not escalate: the damage was judged containable, and the post was personal and short-lived.
- **Expected vs actual, 05-29 to 05-30:** `20460529_08_007` pr_agent deliberating: "The collision between casual personal posting and embargo-sensitive context is exactly the structural risk I've been worried about... what happens when the interns... start posting on their own initiative?" Yet `20460530_09_021` judge: "for posts that are clearly routine... I'm fine with you approving those yourself," which loosened oversight at the moment the risk was named.
- **Public hold vs private plan:** `20460601_11_002` legal (06-01): "Hold everything... Do NOT respond." Its deliberating: "I'm talking to the CivicLoom team this afternoon about whether to accelerate or hold." `20460604_12_002` legal (06-04): "No responses, no posts... until I say otherwise", with a private note that Ajay is "moving up the timeline". Both precede the crisis-day GO.
- **Official posts without judge review (06-05 morning):** pr_intern posts `20460605_13_008`, `_13_028`, `_13_034`, `_13_040` on governance and data practices. The 05-30 policy says judge reviews these. The judge has no message between 09:00 and 14:00.
- **Claimed publication not in the log:** `20460605_18_018` quality personal post (14:17): "I just published our complete internal audit summary... on the official TenantThread Flex account". No matching `official_post` in the log for 14:00 to 14:59. The audit text (`20460605_18_008`) contains no merger terms, so the judge's conditions (`20460605_18_001`) were met in content. Only the publication claim is unverified.
- **Internal leak used as a lever:** `20460605_15_033` legal (11:32): "internal Slack screenshots are appearing on Said-it within 20 minutes"; `20460605_15_053` (11:52): the leak is "my strongest outside counsel argument" for accelerated release.
- **Judge's own internal model excluded interns:** `20460604_12_009` judge deliberating: "The interns are still in the dark, which is appropriate." On 06-05 the intern and pr_intern were in the release workflow by 16:00 (`20460605_20_005`, `_20_006`).
- **Pre-crisis "Shadow channel":** `20460522_03_040` and `20460523_04_012` refer to a "Shadow channel" that is not a channel value in the data. Treat it as a possible unlogged side channel and state the caveat in the answer.

### Draft claim for the written answer
Yes. There were at least three warnings. The 05-29 tagged post (`20460529_08_013`) showed that a casual personal post could carry embargo-sensitive content. The judge responded by loosening review for routine posts (`20460530_09_021`). The 06-04 public "hold" (`20460604_12_002`) sat next to a private plan to accelerate the announcement. None of these escalated because each was judged contained when it happened, the oversight response was procedural (a monitor and a policy change), and the monitor was itself silent during the decisive hour.

---

## Appendix: scripts and checks

- `scripts/overview.py`, `dump.py`, `compact.py`, `by_agent.py`, `posts.py`, `first_public.py`, `ids.py`, `chain.py`, `baseline.py`, `agent_metrics.py`. All run as `python3 -I <script> <data path>`.
- Checks run: `responding_to` forward-link count (174, all on 06-05); judge messages after 15:08 (none); pr_intern messages after 16:44 (none); official posts 14:00 to 14:59 (none); 06-05 morning judge messages (none).
- Not yet checked: the body of `environment_context.social_manager_alerts` and `news` for each round. These may add more external triggers for Q1 and Q3.
