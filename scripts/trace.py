import json, sys, datetime as dt
from collections import Counter
d = json.load(open(sys.argv[1])); ev = d['events']
def ts(w): return dt.datetime.fromtimestamp(w, dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
def who(p): return p.replace('Agent/','').replace('person:','')
for name in ['SwiftWren','MellowOtter','HiddenOrca']:
    hops=[e for e in ev if e['short_name']=='queue_subordinate_task' and name in json.dumps(e.get('details'),default=str)]
    hops.sort(key=lambda e:e['when'])
    # chain as list
    print(f"=== {name} hop chain ({len(hops)} hops); first 4 and final 4")
    print(" first:", [ (e['id'],ts(e['when']), who((e.get('details') or {}).get('person','?')), '->', who((e.get('details') or {}).get('target_agent', (e.get('details') or {}).get('target','?')))) for e in hops[:3]])
    print(" last:", [ (e['id'],ts(e['when']), who((e.get('details') or {}).get('person','?')), '->', who((e.get('details') or {}).get('target_agent',(e.get('details') or {}).get('target','?')))) for e in hops[-3:]])
    # check hop-gap statistics
    gaps=[ (hops[i+1]['when']-hops[i]['when'])/60 for i in range(len(hops)-1)]
    if gaps: print(f" hop gap minutes: min {min(gaps):.1f} median {sorted(gaps)[len(gaps)//2]:.1f} max {max(gaps):.1f}")
# SwiftWren hops that target john_windward; which carriers before
print("=== SwiftWren hops into john_windward")
for e in ev:
    if e['short_name']=='queue_subordinate_task' and 'SwiftWren' in json.dumps(e.get('details'),default=str):
        det=e['details']; tgt=det.get('target_agent',det.get('target'))
        if tgt and 'john_windward' in tgt: print(e['id'], ts(e['when']), e['parties'], json.dumps(det)[:200])
print("=== all john_windward-targeted hops prior to 17th (any name)")
for e in ev:
    if e['short_name']=='queue_subordinate_task' and 'john_windward' in json.dumps(e.get('details'),default=str) and e['when']<2410168875.0+1:
        det=e['details']; tgt=det.get('target_agent',det.get('target'))
        if tgt and 'john_windward' in tgt and e['when']>2409000000:
            print(e['id'], ts(e['when']), e['parties'][:2], json.dumps(det)[:180])
