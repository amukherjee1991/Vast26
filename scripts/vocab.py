import json, sys, datetime as dt, re
from collections import Counter
d = json.load(open(sys.argv[1])); ev = d['events']
def T(w): return dt.datetime.fromtimestamp(w,dt.timezone.utc).strftime('%m-%d %H:%M')
words=['fence','irrigation','crop','harvest','wheat','manure','barn','cattle']
c=Counter(); tot=0
for e in ev:
    if e['short_name'] in ('post_saidit','saidit_post','post_flex','flex_post'):
        tot+=1
        cont=(e.get('details') or {}).get('content') or ''
        for w in words:
            if re.search(w, cont, re.I): c[w]+=1
print("post events with content:", tot, "farm-term hits in posts:", dict(c))
v=[e for e in ev if isinstance(e.get('details'),dict) and e['details'].get('virus')]
print("virus-flag events", len(v), "first", T(min(e['when'] for e in v)), "last", T(max(e['when'] for e in v)))
print("virus-flag events by actor type:", Counter(e['parties'][0].split(':')[0] for e in v))
