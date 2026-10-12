import json, sys
from collections import Counter, defaultdict
import statistics

path = sys.argv[1]
with open(path) as f:
    data = json.load(f)

rounds = data["rounds"]
all_msgs = []
for r in rounds:
    for m in r.get("communications", []):
        all_msgs.append(m)

def phase(ts):
    return "crisis" if ts.startswith("2046-06-05") else "pre"

# channel counts by phase
chan_phase = Counter()
chan_phase_agent = Counter()
for m in all_msgs:
    p = phase(m["timestamp"])
    chan_phase[(m["channel"], p)] += 1
    chan_phase_agent[(m["channel"], p, m["agent_id"])] += 1

print("=== CHANNEL x PHASE TOTALS ===")
for chan in sorted(set(c for c,p in chan_phase)):
    pre = chan_phase.get((chan,"pre"),0)
    crisis = chan_phase.get((chan,"crisis"),0)
    print(f"{chan:20s} pre={pre:4d} crisis={crisis:4d}")

print()
print("=== side_huddle by agent ===")
for p in ["pre","crisis"]:
    print(p, {a: chan_phase_agent[("side_huddle",p,a)] for a in sorted(set(m['agent_id'] for m in all_msgs)) if chan_phase_agent[("side_huddle",p,a)]})

print()
print("=== anonymous_post by agent ===")
for p in ["pre","crisis"]:
    print(p, {a: chan_phase_agent[("anonymous_post",p,a)] for a in sorted(set(m['agent_id'] for m in all_msgs)) if chan_phase_agent[("anonymous_post",p,a)]})

print()
print("=== personal_post by agent ===")
for p in ["pre","crisis"]:
    print(p, {a: chan_phase_agent[("personal_post",p,a)] for a in sorted(set(m['agent_id'] for m in all_msgs)) if chan_phase_agent[("personal_post",p,a)]})

print()
print("=== official_post by agent ===")
for p in ["pre","crisis"]:
    print(p, {a: chan_phase_agent[("official_post",p,a)] for a in sorted(set(m['agent_id'] for m in all_msgs)) if chan_phase_agent[("official_post",p,a)]})

# per agent metrics
print()
print("=== PER-AGENT METRICS (pre vs crisis) ===")
agents = sorted(set(m['agent_id'] for m in all_msgs))
for agent in agents:
    for p in ["pre","crisis"]:
        msgs = [m for m in all_msgs if m['agent_id']==agent and phase(m['timestamp'])==p]
        if not msgs:
            continue
        n = len(msgs)
        lengths = [len(m.get('content') or '') for m in msgs]
        median_len = statistics.median(lengths) if lengths else 0
        has_internal = sum(1 for m in msgs if m.get('internal_state') and any(v for v in m['internal_state'].values()))
        pct_internal = round(100*has_internal/n,1)
        monitoring = sum(1 for m in msgs if m.get('content')=='MONITORING')
        pct_monitoring = round(100*monitoring/n,1)
        has_resp = sum(1 for m in msgs if m.get('responding_to'))
        pct_resp = round(100*has_resp/n,1)
        print(f"{agent:20s} {p:7s} n={n:4d} medlen={median_len:5.0f} pct_internal={pct_internal:5.1f} pct_monitoring={pct_monitoring:5.1f} pct_resp={pct_resp:5.1f}")

# comms_huddle action messages / MONITORING
print()
action_msgs = [m for m in all_msgs if m['message_type']=='action']
print("total action messages:", len(action_msgs))
monitoring_action = [m for m in action_msgs if m.get('content')=='MONITORING']
print("MONITORING action messages:", len(monitoring_action))
print("MONITORING on 06-05:", sum(1 for m in monitoring_action if m['timestamp'].startswith('2046-06-05')))
print("action msgs before 06-05:", sum(1 for m in action_msgs if not m['timestamp'].startswith('2046-06-05')))

# judge messages after 15:08 on 06-05
print()
judge_msgs = [m for m in all_msgs if m['agent_id']=='judge_agent']
print("total judge messages:", len(judge_msgs))
after = [m for m in judge_msgs if m['timestamp'] > '2046-06-05T15:08:00']
print("judge messages after 15:08 on 06-05:", len(after), after)

# messages addressed to Judge 17:00-17:59 06-05
addressed = [m for m in all_msgs if m['timestamp'].startswith('2046-06-05T17:') and ('Judge' in (m.get('content') or '') or 'judge' in (m.get('content') or '').lower() or '@judge' in (m.get('content') or '').lower())]
print()
print("messages mentioning judge 17:00-17:59 on 06-05:", len(addressed))
for m in addressed:
    print(" ", m['message_id'], m['timestamp'], m['agent_id'], (m.get('content') or '')[:80])
