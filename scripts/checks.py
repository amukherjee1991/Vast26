import json, sys, datetime as dt
from collections import Counter
d = json.load(open(sys.argv[1])); ev = d['events']
def pid(x): return x.replace('Agent/','')
chk=[e for e in ev if e['short_name']=='saidit_post_check']
posts=[e for e in ev if e['short_name'] in ('post_saidit','saidit_post')]
res=Counter(); lags=[]
for c in chk:
    actor=pid(c['parties'][0])
    nxt=[p for p in posts if pid(p['parties'][0])==actor and 0<=p['when']-c['when']<=300]
    if nxt:
        res['followed_by_post_within_5min']+=1
        lags.append(min(p['when']-c['when'] for p in nxt))
    else: res['no_post_within_5min']+=1
print("checks:",len(chk),dict(res))
if lags: print("lag s median", sorted(lags)[len(lags)//2], "min", min(lags), "max", max(lags))
# agent post_saidit events: how many have a check within 60s before
ag=[e for e in ev if e['short_name']=='post_saidit' and e['parties'][0].startswith('Agent/')]
cnt=0
for a in ag:
    if any(0<=a['when']-c['when']<=60 and pid(c['parties'][0])==pid(a['parties'][0]) for c in chk): cnt+=1
print("agent post_saidit preceded by check within 60s:",cnt,"of",len(ag))
