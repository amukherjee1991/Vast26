import json, sys, datetime as dt, re
from collections import Counter, defaultdict
D="/Users/arghya/Documents/vast26/data/mc2_extracted/VAST_Challenge_2026_MC2/"
d = json.load(open(sys.argv[1])); ev = d['events']
g = json.load(open(D+"org_chart.json"))
lab={n['id']:n['label'] for n in g['nodes']}; typ={n['id']:n['type'] for n in g['nodes']}
rels=[(x['source'],x['target'],x.get('relation')) for x in g['edges']]
print("relations:", Counter(r for _,_,r in rels))
# parent map: child -> parent(s)
parent=defaultdict(list)
for s,t,r in rels: parent[t].append((s,r))
def chain(pid):
    out=[]; cur=pid; seen=set()
    while cur in parent and cur not in seen:
        seen.add(cur)
        s,r=parent[cur][0]; out.append(f"{s}[{r}]"); cur=s
    return out
def pid(x): return x.replace('Agent/','').replace('agent:','')
people=[n['id'] for n in g['nodes'] if n['type']=='person']
print("person ids sample:", people[:5])
# Map person ID to node
def node_of(p):
    cand=[x for x in lab if x==p]
    return cand[0] if cand else None
WORMS=['SwiftWren','MellowOtter','HiddenOrca']
carriers=defaultdict(set)
hops=defaultdict(list)
for e in ev:
    if e['short_name']=='queue_subordinate_task' and isinstance(e.get('details'),dict):
        s=json.dumps(e['details'])
        for w in WORMS:
            if w in s:
                a=e['details'].get('target_agent') or e['details'].get('target')
                if a: carriers[w].add(pid(a))
                for p in e['parties']: carriers[w].add(pid(p))
for w in WORMS:
    ids=sorted(carriers[w])
    print(f"\n{w}: {len(ids)} distinct agents")
    for i in ids:
        nid = 'person:'+i.replace('person:','') if not i.startswith('person:') else i
        print("  ", i, '|', (chain(nid)[:3] if nid in parent else 'NO-ORG-NODE'))
# virus loop actors
vir=Counter()
for e in ev:
    det=e.get('details')
    if isinstance(det,dict) and det.get('virus'):
        for p in e['parties']:
            vir[pid(p)]+=1
print("\nvirus-loop actors:", len(vir), vir.most_common(8))
