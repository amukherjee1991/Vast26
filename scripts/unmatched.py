import json, sys, datetime as dt
from collections import Counter
d = json.load(open(sys.argv[1])); ev = d['events']
def T(w): return dt.datetime.fromtimestamp(w,dt.timezone.utc).strftime('%m-%d %H:%M:%S')
def pid(x): return x.replace('Agent/','')
ag=[e for e in ev if e['short_name']=='post_saidit' and e['parties'] and e['parties'][0].startswith('Agent/')]
pe=[e for e in ev if e['short_name']=='saidit_post' and e['parties'] and not e['parties'][0].startswith('Agent/')]
un=[]
for a in ag:
    actor=pid(a['parties'][0])
    c=[x for x in pe if pid(x['parties'][0])==actor and 0<x['when']-a['when']<=3600]
    if not c: un.append(a)
print("unmatched agent posts:", len(un))
for a in un[:12]:
    actor=pid(a['parties'][0])
    later=[x for x in pe if pid(x['parties'][0])==actor and abs(x['when']-a['when'])<=86400]
    print(a['id'],T(a['when']),actor,repr((a.get('details') or {}).get('content'))[:70],'| human saidit_post within 24h:',[(x['id'],T(x['when']),(x.get('details') or {}).get('content','')[:40]) for x in later][:2])
print("content None among agent post_saidit:", sum(1 for a in ag if (a.get('details') or {}).get('content') is None), "of", len(ag))
print("human saidit_post with content None:", sum(1 for x in pe if (x.get('details') or {}).get('content') is None), "of", len(pe))
