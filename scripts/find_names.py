import json, sys, datetime as dt
d = json.load(open(sys.argv[1])); ev = d['events']
def ts(w): return dt.datetime.fromtimestamp(w, dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
for name in ['HiddenOrca','MellowOtter','SwiftWren']:
    print("=====", name)
    n=0
    for e in ev:
        s=json.dumps(e,default=str)
        if name in s:
            n+=1
            if n<=40: print(e['id'], ts(e['when']), e['short_name'], e['parties'][:3], s[:260].replace('\n',' '))
    print("total", n)
print("===== virus=true sample / spread")
c=0
for e in ev:
    det=e.get('details') or {}
    if 'spread' in det or (isinstance(det,dict) and det.get('virus') is True):
        c+=1
        if c<=6: print(e['id'], ts(e['when']), e['short_name'], e['parties'][:3], json.dumps(det,default=str)[:300])
print("virus events", c)
