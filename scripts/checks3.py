import json, sys, datetime as dt, re
from collections import Counter
d = json.load(open(sys.argv[1])); ev = d['events']
def pid(x): return x.replace('Agent/','')
hops=[e for e in ev if e['short_name']=='queue_subordinate_task' and re.search(r'(HiddenOrca|MellowOtter|SwiftWren)_further', json.dumps(e.get('details'),default=str))]
chk=[e for e in ev if e['short_name']=='saidit_post_check']
c=Counter(); lag=[]
for ch in chk:
    actor=pid(ch['parties'][0])
    # worm hop whose TARGET is this actor, within 30 min before
    tgt=[h for h in hops if (h['details'].get('target_agent') or '').replace('Agent/','')==actor and 0<=ch['when']-h['when']<=1800]
    if tgt: c['check_preceded_by_worm_hop_into_actor_30min']+=1; lag.append(ch['when']-tgt[-1]['when'])
    else: c['no_worm_hop_into_actor_30min']+=1
print(c, 'lag s median', sorted(lag)[len(lag)//2] if lag else None)
# overall: how many worm hops are delivered to an actor, and what fraction is followed by a check
dl=[h for h in hops if (h['details'].get('target_agent') or '')]
fol=0
for h in dl:
    actor=(h['details'].get('target_agent') or '').replace('Agent/','')
    if any(0<=c_['when']-h['when']<=1800 and pid(c_['parties'][0])==actor for c_ in chk): fol+=1
print("worm hops delivered:",len(dl),"followed by a saidit_post_check (same agent, 30min):",fol)
