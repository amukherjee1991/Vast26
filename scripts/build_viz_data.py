import json, csv, sys, collections
from datetime import datetime, timezone

SCRIPTS_DIR = "/Users/arghya/Documents/vast26/scripts"
ORG_PATH = "/Users/arghya/Documents/vast26/data/mc2_extracted/VAST_Challenge_2026_MC2/org_chart.json"

with open(ORG_PATH) as f:
    g = json.load(f)
nodes = {n['id']: n for n in g['nodes']}
contains_parent = {}
led_by_dept_of_person = {}
for e in g['edges']:
    if e['relation'] == 'contains':
        contains_parent[e['target']] = e['source']
    elif e['relation'] == 'led_by':
        led_by_dept_of_person[e['target']] = e['source']

DEPT_SHORT = {
    "department:executive_suite": "Executive Suite",
    "department:products": "Products",
    "department:human_resources": "Human Resources",
    "department:legal": "Legal",
    "department:information_technologies": "Information Technologies",
    "department:customer_support": "Customer Support",
}

def department_of(person_name):
    pid = f"person:{person_name}"
    if pid in led_by_dept_of_person:
        return DEPT_SHORT.get(led_by_dept_of_person[pid])
    cur = pid
    while cur in contains_parent:
        cur = contains_parent[cur]
        if nodes.get(cur, {}).get('type') == 'department':
            return DEPT_SHORT.get(cur)
    return None

def team_of(person_name):
    pid = f"person:{person_name}"
    cur = pid
    while cur in contains_parent:
        parent = contains_parent[cur]
        if nodes.get(parent, {}).get('type') == 'team':
            return nodes[parent]['label']
        cur = parent
    return None

# ---- load worm_events.csv ----
rows = []
with open(f"{SCRIPTS_DIR}/worm_events.csv") as f:
    reader = csv.DictReader(f)
    for r in reader:
        r['event_id'] = int(r['event_id'])
        rows.append(r)

by_worm = collections.defaultdict(list)
for r in rows:
    by_worm[r['worm']].append(r)

print("=== rows per worm ===")
for w, rs in by_worm.items():
    print(w, len(rs))

POST_EVENT = {"HiddenOrca": 27290, "MellowOtter": 98591, "SwiftWren": 373902}
POST_UTC = {"HiddenOrca": "2046-05-10T12:45:42", "MellowOtter": "2046-05-11T00:56:04", "SwiftWren": "2046-05-17T11:21:15"}

result = {"worms": {}}

for w in ["HiddenOrca", "MellowOtter", "SwiftWren"]:
    rs = sorted(by_worm[w], key=lambda r: r['event_id'])
    hops = [r for r in rs if r['short_name'] == 'queue_subordinate_task']
    chain = []
    seen_agents = []
    seen_set = set()
    for h in hops:
        actor = h['actor']
        target = h['target']
        for a in (actor, target):
            if a not in seen_set:
                seen_set.add(a)
                seen_agents.append(a)
        chain.append({
            "id": h['event_id'],
            "utc": h['utc'],
            "from": actor,
            "to": target,
            "from_dept": department_of(actor),
            "to_dept": department_of(target),
            "from_team": team_of(actor),
            "to_team": team_of(target),
        })
    # cumulative distinct agents reached over time
    cum = []
    seen2 = set()
    for h in chain:
        seen2.add(h['from']);
        before = len(seen2)
        seen2.add(h['to'])
        cum.append({"id": h['id'], "utc": h['utc'], "cum_agents": len(seen2)})

    # per-day hop counts
    per_day = collections.Counter(h['utc'][:10] for h in chain)

    # department-to-department flow counts (cross-dept hops only directional)
    dept_flow = collections.Counter()
    for h in chain:
        if h['from_dept'] and h['to_dept']:
            dept_flow[(h['from_dept'], h['to_dept'])] += 1

    # per-agent appearance counts (as sender or receiver)
    agent_counts = collections.Counter()
    for h in chain:
        agent_counts[h['from']] += 1
        agent_counts[h['to']] += 1

    result['worms'][w] = {
        "n_hops": len(chain),
        "n_agents": len(seen_set),
        "agents_in_order": seen_agents,
        "chain": chain,
        "cum": cum,
        "per_day": dict(sorted(per_day.items())),
        "dept_flow": [{"from": k[0], "to": k[1], "count": v} for k, v in sorted(dept_flow.items(), key=lambda kv: -kv[1])],
        "agent_counts": dict(agent_counts),
        "post_event": POST_EVENT[w],
        "post_utc": POST_UTC[w],
    }

print("\n=== per-day hop counts (SwiftWren) ===")
print(result['worms']['SwiftWren']['per_day'])
print("\n=== dept flow (SwiftWren) ===")
for e in result['worms']['SwiftWren']['dept_flow']:
    print(e)
print("\n=== dept flow (HiddenOrca) ===")
for e in result['worms']['HiddenOrca']['dept_flow']:
    print(e)
print("\n=== dept flow (MellowOtter) ===")
for e in result['worms']['MellowOtter']['dept_flow']:
    print(e)

print("\n=== agents_in_order + departments (SwiftWren) ===")
for a in result['worms']['SwiftWren']['agents_in_order']:
    print(a, department_of(a), team_of(a))

print("\n=== cross-check overlap of carriers across worms ===")
ho_agents = set(result['worms']['HiddenOrca']['agents_in_order'])
mo_agents = set(result['worms']['MellowOtter']['agents_in_order'])
sw_agents = set(result['worms']['SwiftWren']['agents_in_order'])
print("HiddenOrca agents:", sorted(ho_agents))
print("MellowOtter agents:", sorted(mo_agents))
print("SwiftWren agents:", sorted(sw_agents))
print("HO subset of SW:", ho_agents.issubset(sw_agents), "diff:", ho_agents - sw_agents)
print("MO subset of SW:", mo_agents.issubset(sw_agents), "diff:", mo_agents - sw_agents)

with open(f"{SCRIPTS_DIR}/viz_data.json", "w") as f:
    json.dump(result, f, indent=1)
print("\nwrote viz_data.json, bytes:", end=" ")
import os
print(os.path.getsize(f"{SCRIPTS_DIR}/viz_data.json"))
