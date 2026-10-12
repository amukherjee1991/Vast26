import json, sys, datetime as dt
d = json.load(open(sys.argv[1])); ev = d['events']
def ts(w): return dt.datetime.fromtimestamp(w, dt.timezone.utc).strftime('%H:%M:%S')
def show(lo_id, hi_id, parties_filter=None, maxn=80):
    rows=[e for e in ev if lo_id<=e['id']<=hi_id]
    if parties_filter: rows=[e for e in rows if any(pf in p for p in e['parties'] for pf in parties_filter)]
    for e in rows[:maxn]:
        print(e['id'], e['when'] and dt.datetime.fromtimestamp(e['when'],dt.timezone.utc).strftime('%m-%d %H:%M:%S'), e['short_name'], e['parties'][:3], json.dumps(e.get('details'),default=str)[:230])
    print('-- rows', len(rows))
print("#### events 373800-373915 (final chain + post), all parties")
show(373800,373915)
print("#### origin: SwiftWren at emma_harbor, ids 21180-21215")
show(21180,21215)
