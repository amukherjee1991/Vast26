import json, sys

org_path = sys.argv[1]
with open(org_path) as f:
    g = json.load(f)

nodes = {n['id']: n for n in g['nodes']}
contains_parent = {}  # child -> parent
led_by = []
for e in g['edges']:
    if e['relation'] == 'contains':
        contains_parent[e['target']] = e['source']
    elif e['relation'] == 'led_by':
        led_by.append(e)

print("=== led_by edges ===")
for e in led_by:
    print(e['source'], '->', e['target'])

def department_of(person_id):
    cur = person_id
    seen = []
    while cur in contains_parent:
        cur = contains_parent[cur]
        seen.append(cur)
        if nodes.get(cur, {}).get('type') == 'department':
            return cur, seen
    return None, seen

def team_of(person_id):
    cur = person_id
    while cur in contains_parent:
        parent = contains_parent[cur]
        if nodes.get(parent, {}).get('type') == 'team':
            return parent
        cur = parent
    return None

carriers = ["chloe_ballast","gabriel_sonar","levi_signal","lily_anchorline","owen_hatch","victoria_rigging",
            "zoey_drydock","evelyn_dock","henry_sail","james_stern","mia_fender","olivia_keel",
            "emma_harbor","liam_anchor","daniel_gangway","michael_capstan","david_breakwater","john_windward",
            "noah_mariner"]

print("\n=== department + team per carrier ===")
for c in carriers:
    pid = f"person:{c}"
    if pid not in nodes:
        print(c, "NOT FOUND AS NODE")
        continue
    dept, chain = department_of(pid)
    team = team_of(pid)
    dept_label = nodes[dept]['label'] if dept else None
    team_label = nodes[team]['label'] if team else None
    print(f"{c:20s} team={team_label!s:30s} dept={dept_label}")

print("\n=== all department labels & their direct team children ===")
dept_nodes = [n for n in g['nodes'] if n['type']=='department']
for d in dept_nodes:
    children = [e['target'] for e in g['edges'] if e['relation']=='contains' and e['source']==d['id']]
    print(d['id'], d['label'], '->', children)
