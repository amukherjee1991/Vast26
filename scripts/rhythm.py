import json, sys
from collections import Counter

path = sys.argv[1]
with open(path) as f:
    data = json.load(f)

CHANNELS = ["comms_huddle","one_on_one_chat","side_huddle","official_post","personal_post","anonymous_post"]

rows = []
for r in data["rounds"]:
    hour = r["hour"]
    counts = Counter(m["channel"] for m in r["communications"])
    row = {"hour": hour, "total": len(r["communications"])}
    for c in CHANNELS:
        row[c] = counts.get(c, 0)
    rows.append(row)

print("const ROUNDS = [")
for row in rows:
    parts = ", ".join(f'"{c}":{row[c]}' for c in CHANNELS)
    is_crisis = "true" if row["hour"].startswith("2046-06-05") else "false"
    print(f'  {{"hour":"{row["hour"]}", "crisis":{is_crisis}, {parts}}},')
print("];")
