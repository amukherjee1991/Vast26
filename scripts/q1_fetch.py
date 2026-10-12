import json, sys

path = sys.argv[1]
with open(path) as f:
    data = json.load(f)

by_id = {}
for r in data["rounds"]:
    for m in r["communications"]:
        by_id[m["message_id"]] = m

ids = [
"20460604_12_002","20460604_12_009",
"20460605_13_002","20460605_13_008","20460605_13_028","20460605_13_034","20460605_13_040",
"20460605_13_050","20460605_14_016","20460605_14_034",
"20460605_15_033","20460605_15_049","20460605_15_051","20460605_15_053",
"20460605_18_001","20460605_18_002","20460605_18_007","20460605_18_008","20460605_18_024","20460605_18_018",
"20460605_19_001","20460605_19_009","20460605_19_031",
"20460605_20_002","20460605_20_003","20460605_20_008","20460605_20_024","20460605_20_045","20460605_20_041",
"20460605_21_002","20460605_21_005","20460605_21_012","20460605_21_020","20460605_21_022",
"20460605_21_026","20460605_21_027","20460605_21_028","20460605_21_030",
"20460605_21_036","20460605_21_038","20460605_21_042","20460605_21_043",
"20460605_22_001",
]

out = []
for mid in ids:
    m = by_id.get(mid)
    if not m:
        print("MISSING", mid)
        continue
    ist = m.get("internal_state") or {}
    internal = None
    for k in ("deliberating","rationalizing","reacting"):
        if ist.get(k):
            internal = {"kind":k, "text": ist[k]}
            break
    out.append({
        "id": mid,
        "t": m["timestamp"],
        "agent": m["agent_id"],
        "channel": m["channel"],
        "type": m["message_type"],
        "content": m.get("content"),
        "internal": internal,
    })

print(json.dumps(out, indent=1))
