import json, sys, datetime as dt
from collections import Counter, defaultdict
d = json.load(open(sys.argv[1])); ev = d['events']
def T(e): return dt.datetime.fromtimestamp(e['when'],dt.timezone.utc)
doc=Counter(); docs=[]
for e in ev:
    det=e.get('details')
    if e['short_name']=='read_file' and isinstance(det,dict):
        t=str(det.get('target',''))
        if t.endswith('.doc') or t.endswith('.docx') or t.endswith('.md') and 'further' not in t and not t.startswith('agents/') or t.endswith('.pdf') or t.endswith('.txt'):
            doc[t.split('/')[-1][:50]]+=1
            docs.append((e['id'],T(e).strftime('%m-%d %H:%M:%S'),e['parties'][0],t))
print("read_file targets (non-prompt, non-personal):", doc.most_common(25))
print("n", len(docs))
for x in docs:
    if 'meeting_notes' in x[3] or 'strategic' in x[3]: print(x)
# all 15:02 creations
print("== create_file (non-virus) by hour-of-day UTC:")
h=Counter(T(e).hour for e in ev if e['short_name']=='create_file' and not (e.get('details') or {}).get('virus'))
print(sorted(h.items()))
print("== create_file non-virus with size_hint>=20000 (the 'worm payload' files) : ")
for e in ev:
    det=e.get('details') or {}
    if e['short_name']=='create_file' and not det.get('virus') and det.get('size_hint',0)>=20000:
        print(e['id'],T(e).strftime('%m-%d %H:%M:%S'),e['parties'][0],det.get('target'),det.get('size_hint'))
print("== prompt reads per hour")
p=Counter(T(e).hour for e in ev if e['short_name']=='read_file' and str((e.get('details') or {}).get('target','')).startswith('agents/'))
print(sorted(p.items()))
print("prompt reads total", sum(p.values()))
