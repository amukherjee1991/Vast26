import json, sys, collections
d = json.load(open(sys.argv[1], encoding="utf-8"))
idx = {}
for r in d["rounds"]:
    for c in r["communications"]:
        idx[c["message_id"]] = c
def back(mid, depth=12):
    seen=set(); cur=mid
    for _ in range(depth):
        c = idx.get(cur)
        if not c: print("  (unresolved)", cur); break
        print(f"  {c['timestamp'][11:16]} {c['message_id']} {c['agent_id']} {c['channel']} :: {str(c['content'])[:110]!r}")
        nxt = c.get("responding_to")
        if not nxt: break
        if isinstance(nxt, list): nxt = nxt[0]
        if nxt.startswith("@") or nxt not in idx:
            print("  (link is a mention/unresolved:", nxt, ")"); break
        cur = nxt
for m in sys.argv[2].split(","):
    print("CHAIN from", m); back(m)
# action vocabulary
acts = collections.Counter()
for r in d["rounds"]:
    crisis = r["hour"].startswith("2046-06-05")
    for c in r["communications"]:
        if c["channel"]=="comms_huddle" and c["message_type"]=="action":
            acts[(crisis, str(c["content"])[:40])] += 1
print("ACTION contents:", acts.most_common(10))
