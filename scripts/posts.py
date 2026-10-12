import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
for r in d["rounds"]:
    for c in r.get("communications", []):
        if c.get("channel") in ("official_post","anonymous_post","personal_post") :
            print(c["timestamp"], c["message_id"], c["agent_id"], c["channel"], c.get("message_type"), "resp=",c.get("responding_to"))
            print("   ", str(c.get("content"))[:500])
