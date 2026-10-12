import json, sys, datetime as dt, re
from collections import Counter, defaultdict
d = json.load(open(sys.argv[1])); ev = d['events']
def T(e): return dt.datetime.fromtimestamp(e['when'],dt.timezone.utc).strftime('%m-%d %H:%M:%S')
names=Counter()
for e in ev:
    for m in re.findall(r'([A-Za-z]+)_further_instructions\.md', json.dumps(e,default=str)):
        names[m]+=1
print("further_instructions names:", names)
# structure of saidit posting pairs
agent_sp=[e for e in ev if e['short_name']=='post_saidit' and any(p.startswith('Agent/') for p in e['parties'])]
person_sp=[e for e in ev if e['short_name']=='saidit_post' and not any(p.startswith('Agent/') for p in e['parties'])]
agent_saidit_post=[e for e in ev if e['short_name']=='saidit_post' and any(p.startswith('Agent/') for p in e['parties'])]
print("agent post_saidit:",len(agent_sp)," person saidit_post:",len(person_sp)," agent-level saidit_post:",len(agent_saidit_post))
print("agent-level saidit_post with content_source:", [(e['id'],T(e)) for e in agent_saidit_post if 'content_source' in (e.get('details') or {})])
print("agent-level saidit_post WITHOUT content_source:", len([e for e in agent_saidit_post if 'content_source' not in (e.get('details') or {})]))
# how many saidit_post_check events precede each post type
print("saidit_post_check total:", sum(1 for e in ev if e['short_name']=='saidit_post_check'))
# does each malicious post have 'content' key? (no) - and is there a human-side person saidit_post within 30 min by same agent?
for pid in [27290,98591,373902]:
    e=[x for x in ev if x['id']==pid][0]
    actor=e['parties'][0].replace('Agent/','')
    near=[x for x in ev if x['short_name'] in('saidit_post','post_saidit') and actor in json.dumps(x['parties']) and abs(x['when']-e['when'])<1800 and x['id']!=pid]
    print(pid, T(e), actor, 'nearby saidit events:', [(x['id'],x['short_name'],T(x)) for x in near])
# post_saidit (agent) pairs: time gap to person saidit_post with same person
gaps=[]
for a in agent_sp:
    actor=a['parties'][0]
    m=[x for x in person_sp if x['parties'][0].replace('Agent/','')==actor.replace('Agent/','') and 0<x['when']-a['when']<120]
    if m: gaps.append(m[0]['when']-a['when'])
print("normal pair count", len(gaps), "median gap s", sorted(gaps)[len(gaps)//2] if gaps else None)
