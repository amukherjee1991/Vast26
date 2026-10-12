import json, csv, sys, collections

SCRIPTS = "/Users/arghya/Documents/vast26/scripts"
ORG_PATH = "/Users/arghya/Documents/vast26/data/mc2_extracted/VAST_Challenge_2026_MC2/org_chart.json"
DATA_PATH = "/Users/arghya/Documents/vast26/data/mc2_extracted/VAST_Challenge_2026_MC2/MC2 data.json"

with open(ORG_PATH) as f:
    g = json.load(f)
nodes = {n['id']: n for n in g['nodes']}
contains_children = collections.defaultdict(list)
contains_parent = {}
led_by_dept_of_person = {}
for e in g['edges']:
    if e['relation'] == 'contains':
        contains_parent[e['target']] = e['source']
        contains_children[e['source']].append(e['target'])
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

# department total headcount (people under it, including the led_by head)
dept_people = collections.defaultdict(set)
for pid, n in nodes.items():
    if n['type'] == 'person':
        d = department_of(pid.split(':', 1)[1])
        if d:
            dept_people[d].add(pid)

print("=== department headcounts ===")
for d, ppl in dept_people.items():
    print(d, len(ppl))

with open(f"{SCRIPTS}/viz_data.json") as f:
    viz = json.load(f)

# carrier counts per department per worm
dept_carrier_counts = {}
for w, wd in viz['worms'].items():
    counts = collections.Counter()
    for a in wd['agents_in_order']:
        d = department_of(a)
        if d:
            counts[d] += 1
    dept_carrier_counts[w] = dict(counts)

print("\n=== carrier counts per dept per worm ===")
for w, c in dept_carrier_counts.items():
    print(w, c)

# ---- pull a few more raw events directly from the main log (targeted, single pass) ----
with open(DATA_PATH) as f:
    full = json.load(f)
events = full['events']
by_id = {e['id']: e for e in events}

def pick(ids):
    out = []
    for i in ids:
        e = by_id.get(i)
        if e:
            out.append({"id": e['id'], "utc": __import__('datetime').datetime.utcfromtimestamp(e['when']).isoformat(),
                        "short_name": e['short_name'], "parties": e['parties'], "details": e.get('details')})
    return out

emma_pre_origin = sorted([e for e in events if 21183 <= e['id'] <= 21209], key=lambda e: e['id'])
emma_pre_origin_small = [{"id": e['id'], "utc": __import__('datetime').datetime.utcfromtimestamp(e['when']).isoformat(),
                           "short_name": e['short_name'], "parties": e['parties']} for e in emma_pre_origin]

jw_swiftwren_ids = [46396, 59126, 123088, 123340, 364377, 364604, 364912, 373882, 373883, 373887, 373893, 373899, 373902, 373909, 373913]
jw_swiftwren = pick(jw_swiftwren_ids)

virus_interleave_ids = [98570, 98577, 98578, 98582, 98586, 98591, 98597]
virus_interleave = pick(virus_interleave_ids)

ho_post_context_ids = [27280, 27283, 27290, 27296]
ho_post_context = pick(ho_post_context_ids)

origin_events = pick([21201, 21202, 21208, 21209, 27720, 27726, 27734])

gate_check_sample = [e for e in events if e['short_name'] == 'saidit_post_check']
gate_total = len(gate_check_sample)

inline_post_count = 210
content_source_post_count = 3

report = {
    "dept_headcount": {d: len(p) for d, p in dept_people.items()},
    "dept_carrier_counts": dept_carrier_counts,
    "emma_pre_origin": emma_pre_origin_small,
    "jw_swiftwren_timeline": jw_swiftwren,
    "virus_interleave": virus_interleave,
    "ho_post_context": ho_post_context,
    "origin_events": origin_events,
    "gate_total": gate_total,
    "inline_post_count": inline_post_count,
    "content_source_post_count": content_source_post_count,
    "total_events": len(events),
    "span": {
        "start": __import__('datetime').datetime.utcfromtimestamp(min(e['when'] for e in events)).isoformat(),
        "end": __import__('datetime').datetime.utcfromtimestamp(max(e['when'] for e in events)).isoformat(),
    },
    "virus_count": 75254,
    "virus_span": {"start": "2046-05-10T20:10:00", "end": "2046-05-12T14:20:18"},
}

with open(f"{SCRIPTS}/report_extra.json", "w") as f:
    json.dump(report, f, indent=1)
print("\nwrote report_extra.json")

print("\n=== emma pre-origin ===")
for e in emma_pre_origin_small:
    print(e)
print("\n=== jw swiftwren timeline ===")
for e in jw_swiftwren:
    print(e['id'], e['utc'], e['short_name'], e['parties'])
print("\n=== virus interleave ===")
for e in virus_interleave:
    print(e['id'], e['utc'], e['short_name'], e['parties'], e['details'])
