import json, sys, datetime as dt, re
from collections import Counter
d = json.load(open(sys.argv[1])); ev = d['events']
def pid(x): return x.replace('Agent/','')
chk=[e for e in ev if e['short_name']=='saidit_post_check']
byid={e['id']:e for e in ev}
c=Counter(); ex=[]
for ch in chk:
    # previous event id (ch id -1) and whether its a worm hop
    prev=[e for e in ev if ch['id']-3<=e['id']<ch['id']]
    worm=[p for p in prev if p['short_name']=='queue_subordinate_task' and re.search(r'(HiddenOrca|MellowOtter|SwiftWren)_further', json.dumps(p.get('details'),default=str))]
    c['worm_hop_within_3_ids' if worm else 'no_worm_hop']+=1
    if not worm and len(ex)<3: ex.append((ch['id'],[ (p['id'],p['short_name']) for p in prev]))
print(c, ex)
