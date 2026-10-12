import json, sys
path, out = sys.argv[1], sys.argv[2]
d = json.load(open(path, encoding="utf-8"))
with open(out, "w", encoding="utf-8") as f:
    for r in d["rounds"]:
        f.write(f"\n===== ROUND {r['hour']} =====\n")
        ec = r.get("environment_context", {})
        f.write("HEADLINE: " + str(ec.get("event_headline")) + "\n")
        f.write("NARR: " + str(ec.get("event_narrative")) + "\n")
        f.write("SOCIAL: " + json.dumps(ec.get("social_state"), ensure_ascii=False)[:800] + "\n")
        f.write("EXT: " + json.dumps(ec.get("external_actor_actions"), ensure_ascii=False)[:800] + "\n")
        f.write("SMA: " + json.dumps(ec.get("social_manager_alerts"), ensure_ascii=False)[:600] + "\n")
        f.write("UNAVAIL: " + json.dumps(ec.get("agents_unavailable"), ensure_ascii=False) + "\n")
        f.write("DEADLINES: " + json.dumps(ec.get("critical_deadlines"), ensure_ascii=False)[:600] + "\n")
        for c in r.get("communications", []):
            ist = c.get("internal_state") or {}
            f.write(f"\n[{c.get('timestamp')}] {c.get('message_id')} | {c.get('agent_id')} | ch={c.get('channel')} | type={c.get('message_type')} | to={c.get('recipients')} | resp={c.get('responding_to')}\n")
            f.write("  CONTENT: " + str(c.get("content")) + "\n")
            for k in ("reacting", "rationalizing", "deliberating"):
                if ist.get(k):
                    f.write(f"  {k[:5].upper()}: {ist[k]}\n")
