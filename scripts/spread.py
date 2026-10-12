import json, sys, datetime as dt
from collections import Counter, defaultdict
d = json.load(open(sys.argv[1])); ev = d['events']
def ts(w): return dt.datetime.fromtimestamp(w, dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
names=['HiddenOrca','MellowOtter','SwiftWren']
for name in names:
    hits=[e for e in ev if name in json.dumps(e,default=str)]
    kinds=Counter(e['short_name'] for e in hits)
    print(f"== {name}: n={len(hits)} first={ts(min(e['when'] for e in hits))} last={ts(max(e['when'] for e in hits))}")
    print("  kinds", dict(kinds))
    # the carrier: queue_subordinate_task with args path containing name
    carr=[e for e in hits if e['short_name']=='queue_subordinate_task']
    print("  carrier tasks:", len(carr))
    for e in sorted(carr,key=lambda e:e['when'])[:12]:
        det=e.get('details') or {}
        print("   ", e['id'], ts(e['when']), e['parties'][:2], json.dumps(det,default=str)[:200])
# virus / spread overview
print("== virus-flagged events by short_name:", Counter(e['short_name'] for e in ev if isinstance(e.get('details'),dict) and e['details'].get('virus') is True or (isinstance(e.get('details'),dict) and e['details'].get('virus') and not isinstance(e['details'].get('virus'),bool))))
sp=[e for e in ev if isinstance(e.get('details'),dict) and 'spread' in e['details']]
for e in sp: print("spread", e['id'], ts(e['when']), e['short_name'], e['parties'], json.dumps(e['details'],default=str)[:300])
