import json, sys, datetime as dt, re, csv
d = json.load(open(sys.argv[1])); ev = d['events']
def T(w): return dt.datetime.fromtimestamp(w,dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
def pid(x): return x.replace('Agent/','').replace('person:','') if x else ''
rows=[]
for e in ev:
    det=e.get('details') or {}
    if not isinstance(det,dict): continue
    s=json.dumps(det)
    m=re.search(r'(HiddenOrca|MellowOtter|SwiftWren)', s)
    if m and e['short_name'] in ('queue_subordinate_task','create_file','read_file','delete_file','saidit_post','saidit_post_check'):
        src=pid(e['parties'][0]) if e['parties'] else ''
        tgt=pid(det.get('target_agent') or '') if e['short_name']=='queue_subordinate_task' else ''
        rows.append([e['id'],T(e['when']),m.group(1),e['short_name'],src,tgt,json.dumps(det)[:160]])
rows.sort(key=lambda r:r[0])
with open('/Users/arghya/Documents/vast26/scripts/worm_events.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['event_id','utc','worm','short_name','actor','target','details']); w.writerows(rows)
print("rows", len(rows))
sw=[r for r in rows if r[2]=='SwiftWren' and r[3]=='queue_subordinate_task']
print("SwiftWren path:", ' > '.join(f"{r[4]}" for r in sw[:12]), '...', ' > '.join(r[4] for r in sw[-6:]), '> john_windward')
