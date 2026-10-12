import json, sys, datetime as dt
d = json.load(open(sys.argv[1])); ev = d['events']
byid={e['id']:e for e in ev}
def ts(w): return dt.datetime.fromtimestamp(w, dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
t0=dt.datetime(2046,5,17,11,21,15,tzinfo=dt.timezone.utc).timestamp()
print("== target 373902 ==")
print(json.dumps(byid[373902], indent=1, default=str)[:3000])
print("== content_source events ==")
for e in ev:
    det=e.get('details') or {}
    if 'content_source' in det or (e['short_name']=='saidit_post' and 'content_source' in det):
        print(e['id'], ts(e['when']), e['short_name'], e['parties'], json.dumps(det,default=str)[:600])
print("== events with parties involving john_windward, 2046-05-10 .. 2046-05-17 11:30 UTC (non-post) ==")
lo=dt.datetime(2046,5,10,tzinfo=dt.timezone.utc).timestamp()
cnt=0
for e in ev:
    if lo<=e['when']<=t0+600 and any('john_windward' in p for p in e['parties']) and e['short_name'] not in ('saidit_post','post_saidit','flex_post','post_flex'):
        cnt+=1
        if cnt<=60: print(e['id'], ts(e['when']), e['short_name'], e['parties'], json.dumps(e.get('details'),default=str)[:300])
print("count", cnt)
