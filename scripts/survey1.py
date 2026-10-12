import json, sys, datetime as dt
from collections import Counter, defaultdict
d = json.load(open(sys.argv[1]))
ev = d['events']
print("n events", len(ev), "| desc:", d['description'][:200])
def ts(w): return dt.datetime.fromtimestamp(w, dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
ws=[e['when'] for e in ev]; print("range", ts(min(ws)), ts(max(ws)))
keys=defaultdict(Counter)
for e in ev: keys[e['short_name']].update((e.get('details') or {}).keys())
for k,v in sorted(keys.items()): print(k, dict(v))
seen=set()
for e in ev:
    s=e['short_name']
    if s in seen: continue
    seen.add(s)
    print("\nSAMPLE", s, e['id'], ts(e['when']), e['parties'])
    print(json.dumps(e.get('details'),default=str)[:400])
