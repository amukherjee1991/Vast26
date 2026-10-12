import json, sys, collections
path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    d = json.load(f)
rounds = d["rounds"]
print("rounds:", len(rounds))
for r in rounds:
    comms = r.get("communications", [])
    chans = collections.Counter(c.get("channel") for c in comms)
    print(r.get("hour"), len(comms), dict(chans))
print("keys round0:", list(rounds[0].keys()))
print("env keys:", list(rounds[0]["environment_context"].keys()))
if rounds[0]["communications"]:
    c = rounds[0]["communications"][0]
    print(json.dumps(c, indent=1)[:1500])
