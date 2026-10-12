import json, sys, datetime as dt
from collections import Counter, defaultdict
d = json.load(open(sys.argv[1])); ev = d['events']
def T(w): return dt.datetime.fromtimestamp(w,dt.timezone.utc).strftime('%m-%d %H:%M:%S')
def pid(x): return x.replace('Agent/','')
WORMS=['HiddenOrca','MellowOtter','SwiftWren']
for w in WORMS:
    hops=sorted([e for e in ev if e['short_name']=='queue_subordinate_task' and w in json.dumps(e.get('details'),default=str)],key=lambda e:e['id'])
    related=[e for e in ev if w in json.dumps(e,default=str)]
    post=[e for e in ev if e['short_name']=='saidit_post' and 'content_source' in (e.get('details') or {}) and (e['details'])['content_source'].startswith(w)]
    origin=[e for e in related if e['short_name'] in('create_file',)]
    first=related[0]; 
    print(f"{w}: first_seen {T(first['when'])} id{first['id']} | hops {len(hops)} | distinct agents {len(set(pid(p) for h in hops for p in h['parties']))} | post id {post[0]['id'] if post else None} at {T(post[0]['when']) if post else None} | origin create {origin[0]['id'] if origin else 'none in log'} | duration from first_seen to post (h): {((post[0]['when']-first['when'])/3600) if post else 0:.1f}")
# SwiftWren hop day-by-day
sw=sorted([e for e in ev if e['short_name']=='queue_subordinate_task' and 'SwiftWren' in json.dumps(e.get('details'),default=str)],key=lambda e:e['id'])
print("SwiftWren hops per day:", sorted(Counter(dt.datetime.fromtimestamp(e['when'],dt.timezone.utc).strftime('%m-%d') for e in sw).items()))
# normal pair check: each agent post_saidit -> nearest following person saidit_post by same actor
ag=[e for e in ev if e['short_name']=='post_saidit' and e['parties'] and e['parties'][0].startswith('Agent/')]
pe=[e for e in ev if e['short_name']=='saidit_post' and e['parties'] and not e['parties'][0].startswith('Agent/')]
pairs=[]; unmatched=0
for a in ag:
    actor=pid(a['parties'][0])
    c=[x for x in pe if pid(x['parties'][0])==actor and 0<x['when']-a['when']<=3600]
    if c: pairs.append(c[0]['when']-a['when'])
    else: unmatched+=1
print("agent post_saidit:",len(ag),"matched to human saidit_post within 1h:",len(pairs),"unmatched:",unmatched)
if pairs: 
    s=sorted(pairs); print("gap seconds min/median/max", s[0], s[len(s)//2], s[-1])
chk=[e for e in ev if e['short_name']=='saidit_post_check']
print("saidit_post_check actors:", Counter(e['parties'][0].split('/')[0][:6] for e in chk), "details keys:", Counter(tuple((e.get('details') or {}).keys()) for e in chk))
