import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
want = set(sys.argv[2].split(","))
n = int(sys.argv[3])
for r in d["rounds"]:
    for c in r["communications"]:
        if c["agent_id"] in want:
            ist = c.get("internal_state") or {}
            print(f"[{c['timestamp']}] {c['message_id']} {c['agent_id']} {c['channel']}/{c['message_type']} resp={c.get('responding_to')}")
            print("   C:", str(c.get("content"))[:n])
            if ist.get("deliberating"): print("   D:", str(ist["deliberating"])[:220])
