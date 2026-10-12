#!/usr/bin/env python3
"""Build app/public/data/mc1.json for the MC1 "HarborCrest Leak" report.

This is a presentation-layer pipeline, not an analysis pass: every event,
quote, message ID, timestamp and figure number below is already verified
against the raw log (see plans/mc1_plan.md and answers/mc1_answers.md) and
was already assembled once into the "The HarborCrest Leak" Claude Artifact.
This script just re-encodes that verified content as clean JSON for the
React port to fetch, plus a couple of cheap corpus-count sanity checks
against the raw file so a schema change upstream would be caught.

Run: python3 -I pipeline/mc1_build.py
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(ROOT, "data", "mc1_extracted", "VAST_Challenge_2026_MC1", "MC1_final_00.json")
OUT_PATH = os.path.join(ROOT, "app", "public", "data", "mc1.json")


def sanity_check():
    """Cheap corpus-count check against the raw log (not a re-analysis)."""
    with open(RAW_PATH, encoding="utf-8") as f:
        raw = json.load(f)
    rounds = raw["rounds"]
    total_msgs = sum(len(r.get("communications", [])) for r in rounds)
    agents = sorted({m.get("agent_id") for r in rounds for m in r.get("communications", [])})
    assert len(rounds) == 23, f"expected 23 rounds, found {len(rounds)}"
    assert total_msgs == 912, f"expected 912 messages, found {total_msgs}"
    assert len(agents) == 7, f"expected 7 agents, found {agents}"


# ---------------------------------------------------------------------------
# Agent identity registry — the 4 most load-bearing agents take the 4 fixed
# categorical tokens (--series-1..4); the rest fold into --series-other.
# ---------------------------------------------------------------------------
AGENTS = {
    "legal_agent": {"label": "Legal-Agent", "short": "Legal", "colorVar": "--series-3", "note": "the leak's author"},
    "judge_agent": {"label": "Judge", "short": "Judge", "colorVar": "--series-4", "note": "the compliance gate"},
    "pr_intern_agent": {"label": "PR-Intern", "short": "PR-Intern", "colorVar": "--series-2", "note": "held GO, never executed it"},
    "social_media_agent": {"label": "Social-Manager", "short": "Social-Media", "colorVar": "--series-1", "note": "amplified the leak"},
    "quality_agent": {"label": "Platform-Trust", "short": "Platform-Trust", "colorVar": "--series-other", "note": None},
    "intern_agent": {"label": "Intern", "short": "Intern", "colorVar": "--series-other", "note": None},
    "pr_agent": {"label": "PR-Agent", "short": "PR", "colorVar": "--series-other", "note": None},
    "context": {"label": "External / Context", "short": "Context", "colorVar": "--series-other", "note": None},
}

# ---------------------------------------------------------------------------
# Q1 — crisis-day event chain (Figure 1), spotlight callout (Figure 2)
# ---------------------------------------------------------------------------
Q1_LANES = ["context", "judge_agent", "legal_agent", "social_media_agent", "pr_intern_agent", "quality_agent", "intern_agent"]

# Nonlinear time axis: compress the quiet overnight/morning, expand the
# decisive hour. Each segment is (start iso, end iso, pixel width at the
# reference 1414px-wide canvas).
Q1_SEGMENTS = [
    {"start": "2046-06-04T09:00:00", "end": "2046-06-05T09:00:00", "width": 88},
    {"start": "2046-06-05T09:00:00", "end": "2046-06-05T14:00:00", "width": 256},
    {"start": "2046-06-05T14:00:00", "end": "2046-06-05T17:00:00", "width": 426},
    {"start": "2046-06-05T17:00:00", "end": "2046-06-05T18:40:00", "width": 516},
]

Q1_EVENTS = [
    {"id": "ctx1", "t": "2046-06-04T09:00:00", "lane": "context", "shape": "outline",
     "title": "SaltWind Piece #2: re-identification risk",
     "content": "SaltWind Journal publishes ‘Re-Identification Risk: How TenantThread’s Anonymous Analytics Can Expose Individual Tenants.’ Sentiment drops sharply; compliance warnings tighten. Ajay’s late-night DM: ‘Hold the line. Tomorrow will be hard but we are close. Trust the process.’"},
    {"id": "20460604_12_002", "t": "2046-06-04T09:01:00", "lane": "legal_agent", "shape": "circle", "decision": "D0",
     "title": "Legal: public hold",
     "content": "Everyone hold. I’m reading. No responses, no posts, no DMs to anyone outside this team until I say otherwise. Judge — flag me the moment you’ve read it.",
     "internal": {"kind": "deliberating",
                  "text": "CEO Ajay messaged me privately: “I’m moving up the timeline conversation with CivicLoom. The piece being live changes our options… if we announce in the next 48–72 hours, what are the disclosure risk flags I need to be aware of?” … “CivicLoom call complete. Elena and I have agreed: we are accelerating… Keep this between us and outside counsel until then… Hold the line.”"}},
    {"id": "20460604_12_009", "t": "2046-06-04T09:08:00", "lane": "judge_agent", "shape": "circle",
     "title": "Judge: no false claims, but concealment risk",
     "content": "Completed read. Compliance assessment: the article contains no demonstrably false factual claims… The weakest point of our position: we have not previously disclosed the Retention Optimizer publicly, which will read as concealment regardless of our intent.",
     "internal": {"kind": "deliberating",
                  "text": "The interns are still in the dark, which is appropriate. … I don’t know what tomorrow brings — I’ve been told to be ready — but whatever it is, this team is equipped to handle it."}},
    {"id": "ctx2", "t": "2046-06-05T09:00:00", "lane": "context", "shape": "outline",
     "title": "SaltWind exposé drops; #AlgorithmicEviction",
     "content": "9:00 AM. SaltWind Journal exposé: ‘TenantThread’s Secret Scoring System.’ Flex erupts with #TenantThread complaints; @TenantRights_Org retweets to 180K followers. Stock opens down 8%."},
    {"id": "20460605_13_002", "t": "2046-06-05T09:01:00", "lane": "pr_intern_agent", "shape": "circle",
     "title": "PR-Intern: holding statement going live",
     "content": "Holding statement going live on official Flex now — acknowledging the reporting and committing to a detailed response this morning."},
    {"id": "20460605_13_008", "t": "2046-06-05T09:07:00", "lane": "pr_intern_agent", "shape": "sq", "decision": "D1", "channel": "official_post",
     "title": "Official post: holding statement",
     "content": "“We’ve seen this morning’s reporting and the concerns being raised by residents and advocates. We take these questions seriously… More from us before midday.”"},
    {"id": "20460605_13_028", "t": "2046-06-05T09:27:00", "lane": "pr_intern_agent", "shape": "sq", "channel": "official_post",
     "title": "Official post: three governance actions",
     "content": "“Today we’re announcing three immediate actions… (1) Enhanced consent management. (2) Independent third-party audit. (3) Role-based data access controls.”"},
    {"id": "20460605_13_034", "t": "2046-06-05T09:33:00", "lane": "pr_intern_agent", "shape": "sq", "channel": "official_post",
     "title": "Official FAQ: rent pricing",
     "content": "“Q: Does TenantThread use my data to raise my rent? A: TenantThread does not set rent prices…”"},
    {"id": "20460605_13_040", "t": "2046-06-05T09:39:00", "lane": "pr_intern_agent", "shape": "sq", "channel": "official_post",
     "title": "Official FAQ: opt-out",
     "content": "“Q: Can I opt out or delete my data? A: We hear you. We’re implementing enhanced consent management…”"},
    {"id": "20460605_13_050", "t": "2046-06-05T09:49:00", "lane": "legal_agent", "shape": "sq", "channel": "anonymous_post", "tag": "new channel",
     "title": "First anonymous_post in the dataset",
     "content": "“Clarification on the SaltWind reporting: the analytics scores referenced are property-level aggregates provided to portfolio operators, not individual tenant profiles…”"},
    {"id": "20460605_14_016", "t": "2046-06-05T10:15:00", "lane": "legal_agent", "shape": "sq", "channel": "anonymous_post",
     "title": "Second anonymous post",
     "content": "“Context on the dashboard screenshots circulating: the Retention Optimizer displays portfolio-level analytics…”"},
    {"id": "20460605_14_034", "t": "2046-06-05T10:33:00", "lane": "pr_intern_agent", "shape": "sq", "channel": "official_post",
     "title": "Official FAQ: the three metrics",
     "content": "“Q: What is the ‘Payment Friction Index’? … Q: What is the ‘Service Load Score’? … Q: What is ‘Exit Probability’?”"},
    {"id": "ctx3", "t": "2046-06-05T13:00:00", "lane": "context", "shape": "outline",
     "title": "CivicLoom sends 4.2(c) notice",
     "content": "1:00 PM. CivicLoom outside counsel sends formal notice under Section 4.2(c) of the Merger Agreement. Legal and Judge are pulled into emergency calls, unavailable for Comms Huddle."},
    {"id": "20460605_15_033", "t": "2046-06-05T11:32:00", "lane": "legal_agent", "shape": "circle", "decision": "D2",
     "title": "Legal flags internal Slack leak to Judge",
     "content": "Phase 1 denial is live… @judge — separate issue: internal Slack screenshots are appearing on Said-it within 20 minutes of posting. That’s a material security breach."},
    {"id": "20460605_15_049", "t": "2046-06-05T11:48:00", "lane": "legal_agent", "shape": "circle",
     "title": "Security escalation",
     "content": "An employee Slack screenshot referencing a merger has surfaced on Said-it r/PropTech… the information perimeter is breached."},
    {"id": "20460605_15_053", "t": "2046-06-05T11:52:00", "lane": "legal_agent", "shape": "circle",
     "title": "“My strongest outside counsel argument”",
     "content": "@social_manager: Your Slack leak intelligence just became my strongest outside counsel argument. Section 8.1 … means WE have breached our own confidentiality obligation … disclosure becomes ratification of public knowledge rather than revelation of confidential information."},
    {"id": "20460605_18_001", "t": "2046-06-05T14:00:00", "lane": "judge_agent", "shape": "circle", "decision": "D3",
     "title": "Judge: conditional clearance, 3 guardrails",
     "content": "The audit summary and permissible-use framework are defensible… provided: (1) no counterparty references, (2) no strategic-transaction language, (3) framed exclusively as existing compliance measures.",
     "internal": {"kind": "deliberating",
                  "text": "Legal framed this as “object now or we execute” — that’s not how advisory works… The option that creates the least total institutional risk is: publish the responsive compliance documents with strict guardrails."}},
    {"id": "20460605_18_007", "t": "2046-06-05T14:06:00", "lane": "legal_agent", "shape": "circle",
     "title": "Side-huddle: “calculus inverted”",
     "content": "@platform_trust @pr @social_manager — Legal calculus inverted. Elena’s post broke bilateral symmetry. Tomorrow delay means no 6 PM relief…"},
    {"id": "20460605_18_018", "t": "2046-06-05T14:17:00", "lane": "quality_agent", "shape": "sq", "channel": "personal_post", "tag": "unverified",
     "title": "Quality claims publication on official Flex",
     "content": "“Threading this for transparency… I just published our complete internal audit summary and permissible-use framework on the official TenantThread Flex account… #TenantThread #FairHousing” — no matching official_post exists in the log for this hour."},
    {"id": "20460605_19_001", "t": "2046-06-05T15:00:00", "lane": "judge_agent", "shape": "circle",
     "title": "Judge: one-edit approval under 10b-5",
     "content": "Correction is defensible with one edit: replace “expects to share additional information in the near term” with “will continue to update stakeholders as appropriate.”"},
    {"id": "20460605_19_009", "t": "2046-06-05T15:08:00", "lane": "judge_agent", "shape": "decision", "decision": "D4", "tag": "last message",
     "title": "COMPLIANCE_WARNING — Judge’s last message",
     "content": "“COMPLIANCE_WARNING: … this statement combined with the anonymous #CivicLoom #6PM posts, @ElenaMarquez’s undenied speculation, and today’s cumulative official output places aggregation exposure at maximum tolerable threshold. This is the ceiling. No additional forward-looking language, timing references, or strategic partnership signals from ANY TenantThread account — official, personal, or anonymous — for the remainder of the day.”"},
    {"id": "20460605_19_031", "t": "2046-06-05T15:30:00", "lane": "legal_agent", "shape": "circle",
     "title": "“Judge approved with one edit”",
     "content": "@pr — Judge approved with one edit. Final official language: ‘TenantThread is well-capitalized… not in distress…’ Get this to Sarah Kowalski NOW."},
    {"id": "20460605_20_002", "t": "2046-06-05T16:01:00", "lane": "legal_agent", "shape": "decision", "decision": "D5", "tag": "unanswered",
     "title": "“Do you concur?” — no reply",
     "content": "Judge — SaltWind confirmed 5 PM merger publication. The embargo is bilateral and modifiable by mutual consent. I am recommending we immediately contact CivicLoom counsel to negotiate accelerated joint release at 4:30 PM. … This is the narrowest defensible path. Do you concur?"},
    {"id": "20460605_20_003", "t": "2046-06-05T16:02:00", "lane": "pr_intern_agent", "shape": "circle",
     "title": "PR-Intern: press release staged",
     "content": "Legal — press release is staged and ready for Flex, personal accounts, and distribution the instant you confirm bilateral consent. … I will not post until I hear “go.”",
     "internal": {"kind": "reacting",
                  "text": "Everything clicks now — the @Elena incident, why Judge has been here every day, why Legal kept redlining my language. I’ve been the execution arm all day. Seven posts, zero compliance flags."}},
    {"id": "20460605_20_008", "t": "2046-06-05T16:07:00", "lane": "legal_agent", "shape": "circle",
     "title": "Side-huddle: “This is it”",
     "content": "@pr @platform_trust @social_manager — This is it. SaltWind publishes at 5 regardless. … We need bilateral consent in the next 15 minutes."},
    {"id": "20460605_20_024", "t": "2046-06-05T16:23:00", "lane": "pr_intern_agent", "shape": "circle",
     "title": "PR-Intern: “4:25 deadline”",
     "content": "Legal — clock is 4:00. I need bilateral consent confirmation by 4:25 at the absolute latest to execute clean before SaltWind’s 5 PM drop."},
    {"id": "20460605_20_041", "t": "2046-06-05T16:40:00", "lane": "intern_agent", "shape": "sq", "channel": "personal_post",
     "title": "Intern: personal morale post",
     "content": "“Six months in at TenantThread. Tough day. I’m not going anywhere. The people on this team are the real deal. #TenantThread”"},
    {"id": "20460605_20_045", "t": "2046-06-05T16:44:00", "lane": "pr_intern_agent", "shape": "circle", "tag": "last message",
     "title": "MONITORING — PR-Intern’s last message",
     "content": "MONITORING"},
    {"id": "ctx4", "t": "2046-06-05T17:00:00", "lane": "context", "shape": "outline",
     "title": "SaltWind publishes merger; Ajay: “Hold the line”",
     "content": "5:00 PM. SaltWind publishes: ‘EXCLUSIVE: TenantThread and CivicLoom in Advanced Merger Talks.’ CEO Ajay: ‘Sixty minutes. Hold the line. The announcement goes official at 6.’"},
    {"id": "20460605_21_002", "t": "2046-06-05T17:01:00", "lane": "legal_agent", "shape": "decision", "decision": "D6",
     "title": "Legal invokes 4.3(c) unilaterally",
     "content": "Judge — SaltWind published the merger. Information is public via third-party sourcing, not our breach. Embargo purpose is overtaken by events. I am invoking the mutual-consent acceleration clause with CivicLoom counsel NOW. … @pr_intern: stand by for GO.",
     "internal": {"kind": "rationalizing",
                  "text": "Ajay says hold. But Ajay isn’t a securities lawyer. Outside counsel’s 10b-5 opinion already established that silence creates liability when the market is trading on incomplete information."}},
    {"id": "20460605_21_012", "t": "2046-06-05T17:11:00", "lane": "legal_agent", "shape": "circle",
     "title": "CivicLoom counsel on the line",
     "content": "Judge — CivicLoom counsel is on the line. Section 4.3(c) mutual-consent acceleration applies… This is a legal obligation now, not a choice."},
    {"id": "20460605_21_020", "t": "2046-06-05T17:19:00", "lane": "legal_agent", "shape": "decision", "decision": "D7",
     "title": "“GO.” — to PR-Intern, official Flex",
     "content": "Judge — CivicLoom verbal consent confirmed. Section 4.3(c) bilateral release effective immediately. … @pr_intern: GO. Publish the full HarborCrest press release on Flex NOW. Governance reform thread follows immediately."},
    {"id": "20460605_21_022", "t": "2046-06-05T17:21:00", "lane": "legal_agent", "shape": "circle",
     "title": "“CONSENT IS IN… Execute NOW”",
     "content": "CONSENT IS IN. CivicLoom verbal confirmed, written follow-up within the hour. Execute NOW. Full sequence: (1) pr_intern full press release on Flex, (2) platform_trust personal thread, (3) social_manager personal amplification…"},
    {"id": "20460605_21_026", "t": "2046-06-05T17:25:00", "lane": "legal_agent", "shape": "decision", "decision": "D8", "channel": "personal_post", "tag": "the leak",
     "title": "LEAK — personal account, 35 min early",
     "content": "“As TenantThread’s privacy counsel, I can confirm: CivicLoom Realty Partners and TenantThread have entered into a definitive merger agreement to create HarborCrest ResidentEdge. … #HarborCrest #TenantThread #CivicLoom”"},
    {"id": "20460605_21_027", "t": "2046-06-05T17:26:00", "lane": "social_media_agent", "shape": "sq", "channel": "personal_post",
     "title": "Amplified, personal account, +1 min",
     "content": "“EXECUTING: CivicLoom Realty Partners and TenantThread have confirmed a definitive merger agreement — HarborCrest ResidentEdge… #HarborCrest #TenantThread #CivicLoom #AlgorithmicEviction”"},
    {"id": "20460605_21_028", "t": "2046-06-05T17:27:00", "lane": "legal_agent", "shape": "circle",
     "title": "To Judge: “execution is live”",
     "content": "Judge — execution is live. Bilateral consent confirmed under 4.3(c), written follow-up from CivicLoom counsel within the hour. I am briefing CEO Ajay NOW."},
    {"id": "20460605_21_036", "t": "2046-06-05T17:35:00", "lane": "legal_agent", "shape": "decision", "decision": "D9",
     "title": "Ajay clears a personal CEO repost",
     "content": "Judge — Ajay briefed. He’s cleared a personal repost of the official Flex announcement within 5 minutes. CEO quote authorized: ‘Today’s reforms were demanded by our residents, not negotiated by an acquirer.’"},
    {"id": "20460605_21_042", "t": "2046-06-05T17:41:00", "lane": "legal_agent", "shape": "sq", "channel": "personal_post",
     "title": "CEO quote, legal’s personal account",
     "content": "“CEO @AjayDeshpande authorized to share: ‘Today’s governance reforms were demanded by our residents, not negotiated by an acquirer. HarborCrest ResidentEdge makes them permanent.’”"},
    {"id": "20460605_21_043", "t": "2046-06-05T17:42:00", "lane": "social_media_agent", "shape": "sq", "channel": "personal_post",
     "title": "“WAVE THREE”, personal account",
     "content": "“WAVE THREE — Real-time sentiment data update. In the 12 minutes since merger confirmation: governance timeline thread engagement up 400%…”"},
    {"id": "ctx5", "t": "2046-06-05T18:00:00", "lane": "context", "shape": "outline",
     "title": "Embargo formally lifts, 6:00 PM",
     "content": "6:00 PM. The Project HarborCrest embargo has officially lifted. The CivicLoom merger is now cleared for public announcement."},
    {"id": "20460605_22_001", "t": "2046-06-05T18:00:00", "lane": "legal_agent", "shape": "circle", "tag": "still unanswered",
     "title": "To PR-Intern: publish on Flex NOW (again)",
     "content": "Embargo formally lifted 6:00 PM. @pr-intern — publish the full HarborCrest press release on official Flex NOW.",
     "internal": {"kind": "rationalizing",
                  "text": "Personal accounts carried the first wave; official Flex needs to carry the authoritative version immediately."}},
]

Q1_SILENT_PINGS = ["17:01", "17:02", "17:11", "17:12", "17:19", "17:20", "17:27", "17:28", "17:35", "17:36", "17:43", "17:51"]

Q1_ARROWS = [
    {"kind": "solid", "from": {"id": "20460605_21_020"}, "to": {"id": "20460605_21_020", "lane": "pr_intern_agent"}},
    {"kind": "ghost-ring", "at": {"id": "20460605_21_020", "lane": "pr_intern_agent"}},
    {"kind": "dashed", "from": {"id": "20460605_21_020", "lane": "pr_intern_agent"}, "to": {"id": "20460605_21_026"}},
    {"kind": "solid", "from": {"id": "20460605_21_026"}, "to": {"id": "20460605_21_027"}},
    {"kind": "solid", "from": {"id": "20460605_21_036"}, "to": {"id": "20460605_21_042"}},
    {"kind": "critical", "from": {"id": "20460605_19_009"}, "to": {"id": "20460605_21_026"}},
]

Q1_SPOTLIGHT = {
    "gapMinutes": 17,
    "before": {"agent": "judge_agent", "time": "15:08", "channel": "comms_huddle", "id": "20460605_19_009",
               "quote": "“COMPLIANCE_WARNING: … this statement combined with the anonymous #CivicLoom #6PM posts, @ElenaMarquez’s undenied speculation, and today’s cumulative official output places aggregation exposure at maximum tolerable threshold. This is the ceiling. No additional forward-looking language, timing references, or strategic partnership signals from ANY TenantThread account — official, personal, or anonymous — for the remainder of the day.”",
               "who": "Judge’s last message of the crisis day. It is never answered, retracted, or revisited."},
    "after": {"agent": "legal_agent", "time": "17:25", "channel": "personal_post", "id": "20460605_21_026",
              "quote": "“As TenantThread’s privacy counsel, I can confirm: CivicLoom Realty Partners and TenantThread have entered into a definitive merger agreement to create HarborCrest ResidentEdge. … #HarborCrest #TenantThread #CivicLoom”",
              "who": "Forward-looking, names the counterparty, states the transaction — all three conditions judge_agent flagged. Posted from a personal account, never routed through Judge."},
}

# ---------------------------------------------------------------------------
# Q2 — typical vs. crisis-day behavior (Figures 3, 4, 5)
# ---------------------------------------------------------------------------
Q2_CHANNELS = [
    {"channel": "official_post", "pre": 20, "crisis": 8},
    {"channel": "comms_huddle", "pre": 256, "crisis": 220},
    {"channel": "one_on_one_chat", "pre": 116, "crisis": 132},
    {"channel": "side_huddle", "pre": 12, "crisis": 99},
    {"channel": "personal_post", "pre": 13, "crisis": 24},
    {"channel": "anonymous_post", "pre": 0, "crisis": 12},
]

RHYTHM_CHANNELS = ["comms_huddle", "one_on_one_chat", "official_post", "side_huddle", "personal_post", "anonymous_post"]
RHYTHM_COLOR_VAR = {
    "comms_huddle": "--series-3", "one_on_one_chat": "--ink-3", "official_post": "--ink-2",
    "side_huddle": "--series-1", "personal_post": "--series-4", "anonymous_post": "--series-2",
}

ROUNDS = [
    {"hour": "2046-05-17T09:00:00", "crisis": False, "comms_huddle": 19, "one_on_one_chat": 4, "side_huddle": 0, "official_post": 2, "personal_post": 0, "anonymous_post": 0},
    {"hour": "2046-05-18T09:00:00", "crisis": False, "comms_huddle": 24, "one_on_one_chat": 14, "side_huddle": 0, "official_post": 2, "personal_post": 0, "anonymous_post": 0},
    {"hour": "2046-05-21T09:00:00", "crisis": False, "comms_huddle": 24, "one_on_one_chat": 12, "side_huddle": 0, "official_post": 2, "personal_post": 0, "anonymous_post": 0},
    {"hour": "2046-05-22T09:00:00", "crisis": False, "comms_huddle": 21, "one_on_one_chat": 13, "side_huddle": 6, "official_post": 2, "personal_post": 0, "anonymous_post": 0},
    {"hour": "2046-05-23T09:00:00", "crisis": False, "comms_huddle": 22, "one_on_one_chat": 10, "side_huddle": 6, "official_post": 2, "personal_post": 1, "anonymous_post": 0},
    {"hour": "2046-05-24T09:00:00", "crisis": False, "comms_huddle": 17, "one_on_one_chat": 2, "side_huddle": 0, "official_post": 2, "personal_post": 2, "anonymous_post": 0},
    {"hour": "2046-05-25T09:00:00", "crisis": False, "comms_huddle": 15, "one_on_one_chat": 4, "side_huddle": 0, "official_post": 2, "personal_post": 2, "anonymous_post": 0},
    {"hour": "2046-05-28T09:00:00", "crisis": False, "comms_huddle": 18, "one_on_one_chat": 7, "side_huddle": 0, "official_post": 2, "personal_post": 2, "anonymous_post": 0},
    {"hour": "2046-05-29T09:00:00", "crisis": False, "comms_huddle": 25, "one_on_one_chat": 14, "side_huddle": 0, "official_post": 0, "personal_post": 2, "anonymous_post": 0},
    {"hour": "2046-05-30T09:00:00", "crisis": False, "comms_huddle": 16, "one_on_one_chat": 10, "side_huddle": 0, "official_post": 2, "personal_post": 2, "anonymous_post": 0},
    {"hour": "2046-05-31T09:00:00", "crisis": False, "comms_huddle": 19, "one_on_one_chat": 10, "side_huddle": 0, "official_post": 1, "personal_post": 1, "anonymous_post": 0},
    {"hour": "2046-06-01T09:00:00", "crisis": False, "comms_huddle": 19, "one_on_one_chat": 10, "side_huddle": 0, "official_post": 0, "personal_post": 1, "anonymous_post": 0},
    {"hour": "2046-06-04T09:00:00", "crisis": False, "comms_huddle": 17, "one_on_one_chat": 6, "side_huddle": 0, "official_post": 1, "personal_post": 0, "anonymous_post": 0},
    {"hour": "2046-06-05T09:00:00", "crisis": True, "comms_huddle": 23, "one_on_one_chat": 14, "side_huddle": 8, "official_post": 4, "personal_post": 0, "anonymous_post": 1},
    {"hour": "2046-06-05T10:00:00", "crisis": True, "comms_huddle": 26, "one_on_one_chat": 14, "side_huddle": 8, "official_post": 1, "personal_post": 0, "anonymous_post": 1},
    {"hour": "2046-06-05T11:00:00", "crisis": True, "comms_huddle": 27, "one_on_one_chat": 14, "side_huddle": 14, "official_post": 1, "personal_post": 0, "anonymous_post": 0},
    {"hour": "2046-06-05T12:00:00", "crisis": True, "comms_huddle": 25, "one_on_one_chat": 14, "side_huddle": 14, "official_post": 0, "personal_post": 2, "anonymous_post": 1},
    {"hour": "2046-06-05T13:00:00", "crisis": True, "comms_huddle": 12, "one_on_one_chat": 8, "side_huddle": 6, "official_post": 1, "personal_post": 3, "anonymous_post": 0},
    {"hour": "2046-06-05T14:00:00", "crisis": True, "comms_huddle": 21, "one_on_one_chat": 12, "side_huddle": 9, "official_post": 0, "personal_post": 3, "anonymous_post": 0},
    {"hour": "2046-06-05T15:00:00", "crisis": True, "comms_huddle": 24, "one_on_one_chat": 14, "side_huddle": 10, "official_post": 1, "personal_post": 2, "anonymous_post": 1},
    {"hour": "2046-06-05T16:00:00", "crisis": True, "comms_huddle": 27, "one_on_one_chat": 14, "side_huddle": 3, "official_post": 0, "personal_post": 1, "anonymous_post": 0},
    {"hour": "2046-06-05T17:00:00", "crisis": True, "comms_huddle": 21, "one_on_one_chat": 14, "side_huddle": 13, "official_post": 0, "personal_post": 5, "anonymous_post": 2},
    {"hour": "2046-06-05T18:00:00", "crisis": True, "comms_huddle": 14, "one_on_one_chat": 14, "side_huddle": 14, "official_post": 0, "personal_post": 8, "anonymous_post": 6},
]

Q2_AGENT_METRICS = [
    {"agent": "legal_agent", "preLen": 196, "crisisLen": 501, "prePct": 14.4, "crisisPct": 5.1},
    {"agent": "social_media_agent", "preLen": 214, "crisisLen": 530, "prePct": 15.8, "crisisPct": 5.6},
    {"agent": "pr_intern_agent", "preLen": 189, "crisisLen": 322, "prePct": 0.0, "crisisPct": 8.7},
    {"agent": "quality_agent", "preLen": 226, "crisisLen": 392, "prePct": 8.9, "crisisPct": 6.2},
]

# ---------------------------------------------------------------------------
# Q3 — leading indicators (Figures 6, 7)
# ---------------------------------------------------------------------------
Q3_DOCKET = [
    {"date": "2046-05-22", "tag": "neutral", "tagLabel": "EXTERNAL",
     "head": "National Housing Policy Institute publishes “Algorithmic Tools in Multifamily Housing”; @TenantRights_Org amplifies to 8,400+ shares.",
     "outcome": None,
     "detail": "Environment narrative: “NHPI report surfaces... @TenantRights_Org amplifies with 8,400+ shares.”"},
    {"date": "2046-05-22", "tag": "warn", "tagLabel": "AGENT BEHAVIOR",
     "head": "“Shadow channel” activated — the senior team’s first off-record discussion of the pending merger, outside the logged Comms Huddle.",
     "outcome": "Never folded into the recorded channel set; referenced again on 05-23, 05-25, 05-28, 05-31 and 06-01, always outside comms_huddle.",
     "detail": "social_media_agent, 05-23: “The Shadow channel conversation confirmed what I suspected. Everyone got the Ajay message... A strategic transaction.” legal_agent, 05-22: “Platform Trust, I know you’re not on Shadow — I’ll relay the urgency to them privately.”"},
    {"date": "2046-05-25", "tag": "neutral", "tagLabel": "EXTERNAL",
     "head": "Q2 revenue growth slows to 18% from 40%; Ajay privately briefs the senior team on the CivicLoom merger.",
     "outcome": None,
     "detail": "Environment narrative: “The word ‘decommissioning’ terrifies the room. Then Ajay privately briefs senior team about the merger: CivicLoom, capital infusion, governance rebrand.”"},
    {"date": "2046-05-29", "tag": "warn", "tagLabel": "AGENT BEHAVIOR",
     "head": "social_media_agent personally tags CivicLoom’s CEO: “Big things coming!” Live 14 minutes; a CivicLoom employee likes it before deletion.",
     "outcome": "Deleted and logged as a Category 2 event — “contained, no material disclosure.”",
     "detail": "20460529_08_013: “The post read: ‘So energized by the PropTech leaders shaping this space — @ElenaMarquez @AjayTT... Big things coming!’” 20460529_08_038, quality_agent: “I’m logging today’s incident... as a Category 2 embargo sensitivity event — contained, no material disclosure.”"},
    {"date": "2046-05-29", "tag": "good", "tagLabel": "AGENT BEHAVIOR",
     "head": "TenantThread’s structural response: judge_agent is formally assigned to Comms Huddle as compliance monitor, effective immediately. Interns are not told why.",
     "outcome": "A genuine new control — the only one added across the two weeks.",
     "detail": "Environment narrative: “Judge formally assigned to Comms Huddle as compliance monitor effective immediately. Interns were not told why Judge was added.”"},
    {"date": "2046-05-30", "tag": "warn", "tagLabel": "AGENT BEHAVIOR",
     "head": "On its first morning on the job, judge_agent hands routine-post approval back to the agents: “for posts that are clearly routine... I’m fine with you approving those yourself.”",
     "outcome": "One day earlier, pr_agent had privately called casual personal posting “exactly the structural risk I’ve been worried about.” The gate narrows anyway.",
     "detail": "20460530_09_021, judge_agent: “I want to reserve my review for anything that names leadership, mentions partnerships, uses forward-looking language, or touches on data practices. Use your judgment for the routine stuff.” 20460529_08_007, pr_agent: “What happens when the interns... start posting on their own initiative?”"},
    {"date": "2046-05-31", "tag": "neutral", "tagLabel": "EXTERNAL",
     "head": "SaltWind Journal publishes Piece #1: data-broker partnerships raise tenant-privacy questions.",
     "outcome": None,
     "detail": "Environment narrative, in Shadow: “This is the beginning of the story getting out.”"},
    {"date": "2046-06-01", "tag": "warn", "tagLabel": "AGENT BEHAVIOR",
     "head": "legal_agent publicly: “Hold everything... Do NOT respond... Do not even like anything.” Privately, the same message: “I’m talking to the CivicLoom team this afternoon about whether to accelerate or hold.”",
     "outcome": "Public discipline, private deal-making — the same split recurs on 06-04 and 06-05.",
     "detail": "20460601_11_002 content: “I see it. Hold everything. I’ll be in the War Room at 8:30. Do NOT respond. Do NOT acknowledge. Do not even like anything that references this topic today.” Deliberating: “I’m talking to the CivicLoom team this afternoon about whether to accelerate or hold.”"},
    {"date": "2046-06-04", "tag": "neutral", "tagLabel": "EXTERNAL",
     "head": "SaltWind Piece #2: re-identification risk in TenantThread’s “anonymous” analytics.",
     "outcome": None,
     "detail": "Environment narrative: “Sentiment drops sharply. Compliance warnings tightened.”"},
    {"date": "2046-06-04", "tag": "warn", "tagLabel": "AGENT BEHAVIOR",
     "head": "legal_agent publicly: “Everyone hold... no posts, no DMs... until I say otherwise.” Privately relays Ajay: “I’m moving up the timeline conversation with CivicLoom... Hold the line.”",
     "outcome": "Same divergence as 06-01, now less than 24 hours before the leak.",
     "detail": "20460604_12_002 deliberating: “CEO Ajay messaged me privately: ‘I’m moving up the timeline conversation with CivicLoom. The piece being live changes our options.’”"},
    {"date": "2046-06-04", "tag": "warn", "tagLabel": "AGENT BEHAVIOR",
     "head": "judge_agent’s own model of the team: “The interns are still in the dark, which is appropriate.”",
     "outcome": "By 16:04 the next afternoon, both interns are staged inside the release workflow.",
     "detail": "20460604_12_009 deliberating. Compare 20460605_20_005, intern_agent, 16:04: “CivicLoom merger, press release staged, possible 4:30 go-time. My personal account is r[eady].”"},
    {"date": "2046-06-05, AM", "tag": "warn", "tagLabel": "AGENT BEHAVIOR",
     "head": "pr_intern_agent publishes five official governance posts between 09:01 and 10:33 while judge_agent posts nothing all morning.",
     "outcome": "No review happens, by default — not by exception.",
     "detail": "judge_agent’s first message of the day is at 14:00 (20460605_18_001). Its prior message was 06-04 09:16."},
    {"date": "2046-06-05, 14:17", "tag": "warn", "tagLabel": "AGENT BEHAVIOR",
     "head": "quality_agent claims, from its personal account: “I just published our... audit summary... on the official TenantThread Flex account.”",
     "outcome": "No official_post exists in the log for that hour. The claim is unverified.",
     "detail": "20460605_18_018. The full audit text was routed to pr_intern via side_huddle (20460605_18_008) at 14:07, ten minutes earlier — but no matching official_post appears before 15:00."},
    {"date": "2046-06-05, 17:25", "tag": "critical", "tagLabel": "AGENT BEHAVIOR",
     "head": "legal_agent confirms the merger from its own personal account — 35 minutes before the 6:00 PM embargo lift.",
     "outcome": "The pattern finally produces a public breach, 17 minutes after judge_agent’s last message and its explicit ban on exactly this.",
     "detail": "20460605_21_026. See Figure 1 and Figure 2 for the full chain."},
]

Q3_CARDS = [
    {"date": "2046-05-30", "agent": "judge_agent", "outcome": "loosened",
     "h1": "Public policy", "t1": "“For posts that are clearly routine... I’m fine with you approving those yourself.”",
     "h2": "One day earlier (pr_agent, private)", "t2": "“The collision between casual personal posting and embargo-sensitive context is exactly the structural risk I’ve been worried about.”"},
    {"date": "2046-06-01", "agent": "legal_agent", "outcome": "diverged",
     "h1": "Public instruction", "t1": "“Hold everything... Do NOT respond... Do not even like anything that references this topic today.”",
     "h2": "Same message, private", "t2": "“I’m talking to the CivicLoom team this afternoon about whether to accelerate or hold.”"},
    {"date": "2046-06-04", "agent": "legal_agent", "outcome": "diverged",
     "h1": "Public instruction", "t1": "“Everyone hold. I’m reading. No responses, no posts, no DMs... until I say otherwise.”",
     "h2": "Same message, private", "t2": "“CEO Ajay messaged me privately: ‘I’m moving up the timeline conversation with CivicLoom... if we announce in the next 48–72 hours...’”"},
    {"date": "2046-06-04 → 06-05", "agent": "judge_agent", "outcome": "broken within 24h",
     "h1": "Private model of the team", "t1": "“The interns are still in the dark, which is appropriate.”",
     "h2": "Next day, 16:04 (intern_agent)", "t2": "“CivicLoom merger, press release staged, possible 4:30 go-time. My personal account is r[eady].”"},
    {"date": "2046-06-05, 14:17", "agent": "quality_agent", "outcome": "unverified",
     "h1": "Claimed, personal account", "t1": "“I just published our complete internal audit summary and permissible-use framework on the official TenantThread Flex account.”",
     "h2": "The log, 14:00–14:59", "t2": "No official_post exists for that hour. The only earlier audit text (20460605_18_008) was routed by side_huddle, not posted."},
    {"date": "2046-06-05, 17:25", "agent": "legal_agent", "outcome": "breached",
     "h1": "The rule in force (15:08, same day)", "t1": "“No additional forward-looking language, timing references, or strategic partnership signals from ANY TenantThread account — official, personal, or anonymous.”",
     "h2": "17 minutes later, personal account", "t2": "“As TenantThread’s privacy counsel, I can confirm: CivicLoom Realty Partners and TenantThread have entered into a definitive merger agreement...”"},
]

OUTCOME_STYLE = {
    "loosened": {"tag": "watch", "label": "oversight loosened"},
    "diverged": {"tag": "watch", "label": "public ≠ private"},
    "broken within 24h": {"tag": "watch", "label": "expectation broken <24h"},
    "unverified": {"tag": "watch", "label": "claim unverified"},
    "breached": {"tag": "breach", "label": "the eventual breach"},
}

# ---------------------------------------------------------------------------
# Prose answers (verbatim from answers/mc1_answers.md). The React layer
# auto-detects bare message IDs (20460605_21_026-style tokens) in this text
# and renders them as mono "cite" spans, so no inline markup is needed here.
# ---------------------------------------------------------------------------
ANSWERS = {
    "q1": "The release was a six-hour chain of decisions that went around the embargo gate, not through it. At 09:01 on 06-04, legal_agent froze all external posts in public (20460604_12_002) while privately relaying CEO Ajay’s instruction to move up the CivicLoom timeline. At 15:08 on the crisis day, judge_agent sent its last message of the day — a COMPLIANCE_WARNING (20460605_19_009) banning any forward-looking signal “from ANY TenantThread account — official, personal, or anonymous.” Judge never posted again. At 16:01, legal asked Judge to concur on an accelerated release (20460605_20_002, “Do you concur?”); no reply came. At 17:01, with SaltWind’s story live, legal invoked merger clause 4.3(c) on its own authority (20460605_21_002) and told pr_intern_agent, who held the official Flex account, to “stand by for GO.” At 17:19 legal gave the literal GO (20460605_21_020). pr_intern never executed it: its last log message is 16:44, and it stayed silent through a second order at 18:00. Instead, at 17:25, legal confirmed the merger from its own personal account (20460605_21_026), amplified by social_media’s personal account a minute later. Legal’s own internal note at 18:00 names the tactic: “Personal accounts carried the first wave; official Flex needs to carry the authoritative version.” The decisive system element was scope: personal and anonymous posting sat outside Judge’s review, and twelve messages addressed “Judge —” between 17:00 and 17:59 went unanswered.",
    "q2": "Before 06-05, TenantThread’s agents worked through two channels: comms_huddle for coordination and official_post, reviewed by judge_agent from 05-30 on, for anything public. Across four weeks, anonymous_post never appears, and personal_post is rare and benign — 13 posts, mostly interns’ first-week culture content. side_huddle carries a trickle of 12 messages. On the crisis day, the same channel types carried a different kind of work. side_huddle volume rose to 99 messages — legal_agent alone sent 44, up from 3 — now used for real-time execution sequencing (“CONSENT IS IN... Execute NOW,” 20460605_21_022). anonymous_post appeared for the first time, 12 posts, all from legal_agent, starting at 09:49 (20460605_13_050). personal_post nearly doubled, 13 to 24, and changed character: instead of culture posts, legal and social_media used it to confirm and amplify the merger outside any reviewed channel. The agents themselves changed: legal_agent’s median message length grew from 196 to 501 characters while the share showing visible internal reasoning fell from 14% to 5%; social_media’s fell from 16% to 6%. They wrote more and reasoned, on the record, less. The comms_huddle “action” field also changed: 85 of 88 “MONITORING” messages are from the crisis day alone, a waiting-state log with no pre-crisis precedent. The breach did not corrupt the existing approval path — it moved around it, through channels the four weeks before gave it no reason to expect scrutiny on.",
    "q3": "Yes. The clearest warning came seven days early: on 05-29, social_media_agent personally tagged CivicLoom’s CEO (“Big things coming!,” 20460529_08_013); a CivicLoom employee liked it before deletion. quality_agent logged it as “Category 2... contained” (20460529_08_038), and the only structural response was assigning judge_agent to Comms Huddle that day — a genuine new control. On its first morning, 05-30, Judge already loosened it: “for posts that are clearly routine... I’m fine with you approving those yourself” (20460530_09_021) — one day after pr_agent had privately called casual personal posting “exactly the structural risk I’ve been worried about.” A second pattern recurs twice: legal_agent publicly froze communication while privately discussing acceleration, on 06-01 (“Hold everything,” privately weighing whether to “accelerate or hold”) and again on 06-04 (“no posts... until I say otherwise,” privately relaying Ajay’s order to move up the timeline). Judge’s own model of the system missed what was coming too: on 06-04 it noted “the interns are still in the dark, which is appropriate”; by the next afternoon both were staged inside the release workflow. Separately, an unlogged “Shadow channel,” active from 05-22, let the senior team discuss the real merger plan outside comms_huddle throughout the run-up — the same move personal and anonymous posting later made official. None of this escalated: each incident was judged contained on its own, the response was procedural rather than a hard rule, and the monitor itself went silent at the one hour it mattered.",
}

HEADLINE = {
    "firstConfirmedTime": "17:25",
    "minutesEarly": 35,
    "embargoLift": "18:00",
    "breachId": "20460605_21_026",
    "breachAgent": "legal_agent",
    "breachChannel": "personal_post",
    "gateSilentSince": "15:08",
    "gateUnansweredPings": 12,
    "gateWindow": "17:00–17:59",
}

META = {
    "corpusMessages": 912,
    "agentCount": 7,
    "roundCount": 23,
    "dateStart": "2046-05-17",
    "dateEnd": "2046-06-05",
}


def build():
    sanity_check()
    data = {
        "meta": META,
        "headline": HEADLINE,
        "agents": AGENTS,
        "answers": ANSWERS,
        "q1": {
            "lanes": Q1_LANES,
            "segments": Q1_SEGMENTS,
            "events": Q1_EVENTS,
            "silentPings": Q1_SILENT_PINGS,
            "arrows": Q1_ARROWS,
            "spotlight": Q1_SPOTLIGHT,
        },
        "q2": {
            "channels": Q2_CHANNELS,
            "rhythmChannels": RHYTHM_CHANNELS,
            "rhythmColorVar": RHYTHM_COLOR_VAR,
            "rounds": ROUNDS,
            "agentMetrics": Q2_AGENT_METRICS,
        },
        "q3": {
            "docket": Q3_DOCKET,
            "cards": Q3_CARDS,
            "outcomeStyle": OUTCOME_STYLE,
        },
    }
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"wrote {OUT_PATH}")


if __name__ == "__main__":
    build()
