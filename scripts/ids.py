import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
want = sys.argv[2].split(",")
idx = {}
for r in d["rounds"]:
    ec = r.get("environment_context", {})
    for c in r["communications"]:
        idx[c["message_id"]] = (r["hour"], c)
for m in want:
    if m not in idx: print("MISSING", m); continue
    h, c = idx[m]
    print("###", m, c["timestamp"], c["agent_id"], c["channel"], c["message_type"], "to", c["recipients"], "resp", c["responding_to"])
    print("CONTENT:", c["content"])
    ist = c.get("internal_state") or {}
    for k in ("reacting","rationalizing","deliberating"):
        if ist.get(k): print(k.upper()+":", ist[k])
    print()
