import json, sys, datetime as dt
from collections import Counter
d = json.load(open(sys.argv[1])); ev = d['events']
def ts(w): return dt.datetime.fromtimestamp(w, dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
for name in ['HiddenOrca','MellowOtter','SwiftWren']:
    print("=====", name)
    for e in ev:
        s=json.dumps(e,default=str)
        if name in s and e['short_name'] in ('create_file','read_file','saidit_post','delete_file','saidit_post_check','check_in'):
            print(e['id'], ts(e['when']), e['short_name'], e['parties'], json.dumps(e.get('details'),default=str)[:400])
print("===== virus-flag sample per short_name (2 each)")
seen=Counter()
for e in ev:
    det=e.get('details')
    if isinstance(det,dict) and det.get('virus') and seen[e['short_name']]<2:
        seen[e['short_name']]+=1
        print(e['id'], ts(e['when']), e['short_name'], e['parties'][:2], json.dumps(det,default=str)[:300], '| full keys:', list(e.keys()))
print("===== combo distribution (check_in virus=True)")
cb=Counter()
for e in ev:
    det=e.get('details')
    if e['short_name']=='check_in' and isinstance(det,dict):
        cb[tuple(det.get('combo') or [])]+=1
print(len(cb), cb.most_common(10))
print("===== create_file action/target for virus-flagged")
ct=Counter()
for e in ev:
    det=e.get('details')
    if e['short_name']=='create_file' and isinstance(det,dict) and det.get('virus'):
        ct[(det.get('action'), str(det.get('target'))[:40], det.get('word_count'), det.get('size_hint'))]+=1
print(ct.most_common(12))
