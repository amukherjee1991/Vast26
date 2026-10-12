import json, sys, datetime as dt
from collections import Counter
d = json.load(open(sys.argv[1])); ev = d['events']
byid={e['id']:e for e in ev}
def f(e): return f"{e['id']} {dt.datetime.fromtimestamp(e['when'],dt.timezone.utc).strftime('%m-%d %H:%M:%S')} {e['short_name']} {e['parties'][:3]} {json.dumps(e.get('details'),default=str)[:200]}"
print("## MellowOtter origin context (27700-27735)")
for e in ev:
    if 27700<=e['id']<=27735: print(f(e))
print("## HiddenOrca first hop context (15770-15790)")
for e in ev:
    if 15770<=e['id']<=15790: print(f(e))
print("## meeting_notes.doc mentions")
c=Counter()
for e in ev:
    s=json.dumps(e.get('details'),default=str)
    if 'meeting_notes' in s:
        c[(e['short_name'], e['parties'][0] if e['parties'] else '')]+=1
print(c.most_common(10))
print("## emails with subject containing 'Quarterly planning'")
sub=Counter()
for e in ev:
    det=e.get('details') or {}
    if isinstance(det,dict) and 'subject' in det: sub[det['subject']]+=1
print(sub.most_common(15))
print("## number of distinct subjects", len(sub))
