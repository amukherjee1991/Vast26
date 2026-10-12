import json, sys, collections, statistics as st
d = json.load(open(sys.argv[1], encoding="utf-8"))
rows = collections.defaultdict(lambda: collections.defaultdict(list))
for r in d["rounds"]:
    phase = "crisis" if r["hour"].startswith("2046-06-05") else "pre"
    for c in r["communications"]:
        a = c["agent_id"]
        rows[(a, phase)]["len"].append(len(str(c.get("content") or "")))
        ist = c.get("internal_state") or {}
        rows[(a, phase)]["has_istate"].append(1 if any(ist.get(k) for k in ("reacting","rationalizing","deliberating")) else 0)
        rows[(a, phase)]["monitoring"].append(1 if str(c.get("content")).startswith("MONITORING") else 0)
        rows[(a, phase)]["responds"].append(1 if c.get("responding_to") else 0)
        rows[(a, phase)]["n"].append(1)
print(f"{'agent':22}{'phase':8}{'n':>5}{'medLen':>8}{'%istate':>9}{'%MONITOR':>10}{'%resp':>7}")
for (a, p), m in sorted(rows.items()):
    n = len(m["n"])
    print(f"{a:22}{p:8}{n:5d}{int(st.median(m['len'])):8d}{100*sum(m['has_istate'])/n:9.0f}{100*sum(m['monitoring'])/n:10.0f}{100*sum(m['responds'])/n:7.0f}")
