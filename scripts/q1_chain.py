import json, sys

path = sys.argv[1]
with open(path) as f:
    data = json.load(f)

all_msgs = []
for r in data["rounds"]:
    all_msgs.extend(r["communications"])

start = "2046-06-04T09:00:00"
end = "2046-06-05T18:59:59"

window = [m for m in all_msgs if start <= m["timestamp"] <= end]
window.sort(key=lambda m: m["timestamp"])

print("TOTAL IN WINDOW:", len(window))
print()
for m in window:
    ist = m.get("internal_state") or {}
    has_internal = any(v for v in ist.values())
    flag = "*" if has_internal else " "
    content = (m.get("content") or "").replace("\n"," ")
    print(f"{m['timestamp']} {flag} {m['message_id']:20s} {m['agent_id']:20s} {m['channel']:15s} {m['message_type']:12s} {content[:140]}")
