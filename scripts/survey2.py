import json, sys, datetime as dt
from collections import Counter
d = json.load(open(sys.argv[1])); ev = d['events']
def ts(w): return dt.datetime.fromtimestamp(w, dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
POST={'post_saidit','saidit_post','post_flex','flex_post','saidit_post_check'}
print("== posts: all saidit/flex events by content ==")
for e in ev:
    if e['short_name'] in POST and e['short_name']!='saidit_post_check':
        det=e.get('details') or {}
        c=det.get('content')
        print(e['id'], ts(e['when']), e['short_name'], e['parties'][:2], repr(c)[:140], det.get('forum',''), det.get('timestamp',det.get('time','')))
