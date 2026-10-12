import json, sys
from collections import Counter, defaultdict

path = sys.argv[1]
with open(path) as f:
    data = json.load(f)

rounds = data["rounds"]
all_msgs = []
for r in rounds:
    for m in r.get("communications", []):
        m["_hour"] = r["hour"]
        all_msgs.append(m)

by_id = {m["message_id"]: m for m in all_msgs}

print("TOTAL MESSAGES:", len(all_msgs))
print("AGENT IDS:", sorted(set(m["agent_id"] for m in all_msgs)))
print("CHANNELS:", sorted(set(m["channel"] for m in all_msgs)))
print()

# Check specific message IDs from the plan
ids_to_check = [
    "20460605_21_026", "20460605_21_027", "20460605_21_042", "20460605_21_043",
    "20460605_21_020", "20460605_20_045", "20460605_19_021",
    "20460604_12_002", "20460605_13_002", "20460605_13_008", "20460605_13_028",
    "20460605_13_034", "20460605_13_040", "20460605_15_033", "20460605_15_049",
    "20460605_15_051", "20460605_15_053", "20460605_18_001", "20460605_19_009",
    "20460605_20_002", "20460605_21_002", "20460605_21_036", "20460605_21_038",
    "20460605_20_041", "20460529_08_013", "20460529_08_008", "20460529_08_018",
    "20460529_08_038", "20460530_09_009", "20460530_09_021", "20460529_08_007",
    "20460601_11_002", "20460605_18_018", "20460605_18_008", "20460605_15_053",
    "20460604_12_009", "20460605_20_005", "20460605_20_006", "20460522_03_040",
    "20460523_04_012", "20460517_00_001",
]

print("=== MESSAGE ID CHECKS ===")
missing = []
for mid in ids_to_check:
    m = by_id.get(mid)
    if not m:
        missing.append(mid)
        continue
    content = (m.get("content") or "")[:160].replace("\n", " ")
    print(f"{mid} | {m['timestamp']} | {m['agent_id']} | {m['channel']} | {m['message_type']} | {content}")

print()
print("MISSING IDS:", missing)
