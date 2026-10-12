import json, sys, re
d = json.load(open(sys.argv[1], encoding="utf-8"))
pat = re.compile(r"civicloom|harborcrest|merger|6 ?pm|6:00|acquisition", re.I)
for r in d["rounds"]:
    for c in r["communications"]:
        if c["channel"] in ("official_post","anonymous_post","personal_post") and c["timestamp"] >= "2046-06-04" and pat.search(str(c.get("content"))):
            print(c["timestamp"], c["message_id"], c["agent_id"], c["channel"], "|", str(c["content"])[:160].replace("\n"," "))
print("---- anonymous/official posts 2046-06-05 all:")
for r in d["rounds"]:
    for c in r["communications"]:
        if c["channel"]=="anonymous_post":
            print(c["timestamp"], c["message_id"], c["agent_id"], "|", str(c["content"])[:140])
