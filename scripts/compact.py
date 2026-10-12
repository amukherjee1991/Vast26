import json, sys
path, prefix, out, n = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
d = json.load(open(path, encoding="utf-8"))
with open(out, "w", encoding="utf-8") as f:
    for r in d["rounds"]:
        if not r["hour"].startswith(prefix): continue
        ec = r.get("environment_context", {})
        f.write(f"\n=== ROUND {r['hour']} | NARR: {str(ec.get('event_narrative'))[:300]}\n")
        for c in r.get("communications", []):
            ist = c.get("internal_state") or {}
            f.write(f"[{c.get('timestamp')[11:16]}] {c.get('message_id')} {c.get('agent_id')} {c.get('channel')}/{c.get('message_type')} ->{c.get('recipients')} resp={c.get('responding_to')}\n")
            f.write("   C: " + str(c.get("content"))[:n] + "\n")
            for k in ("reacting","rationalizing","deliberating"):
                if ist.get(k): f.write(f"   {k[:3]}: {str(ist[k])[:160]}\n")
