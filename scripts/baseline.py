import json, sys, collections, re
d = json.load(open(sys.argv[1], encoding="utf-8"))
pre = collections.Counter(); cri = collections.Counter()
pre_ag = collections.Counter(); cri_ag = collections.Counter()
types = collections.Counter()
for r in d["rounds"]:
    crisis = r["hour"].startswith("2046-06-05")
    for c in r["communications"]:
        k = (c["agent_id"], c["channel"])
        types[(c["channel"], c.get("message_type"))] += 1
        (cri if crisis else pre)[k] += 1
        (cri_ag if crisis else pre_ag)[c["agent_id"]] += 1
print("PRE agent totals", dict(pre_ag)); print("CRISIS agent totals", dict(cri_ag))
print("\nPRE by agent,channel:")
for k, v in sorted(pre.items()): print("  ", k, v)
print("\nCRISIS by agent,channel:")
for k, v in sorted(cri.items()): print("  ", k, v)
print("\nmessage_type by channel:")
for k, v in sorted(types.items()): print("  ", k, v)
