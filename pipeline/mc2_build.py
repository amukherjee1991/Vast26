"""Bakes app/public/data/mc2.json for the MC2 ("Tracing SwiftWren") report.

This is a presentation-layer port of an already-verified analysis. It does NOT
re-derive facts from the raw 70MB `MC2 data.json` — every number here comes
from, and is cross-checked against:
  - plans/mc2_plan.md and answers/mc2_answers.md (the written, cited analysis)
  - scripts/worm_events.csv (the 248 pre-filtered worm event rows)
  - scripts/report_full.json (the exact chain/dept/timeline data the prior
    analysis computed from the raw log and used to build the reference
    Claude Artifact "SwiftWren Incident Report")
  - data/mc2_extracted/VAST_Challenge_2026_MC2/org_chart.json (75-node org chart)

Run from the repo root: python3 -I pipeline/mc2_build.py
(or via pipeline/build_all.py, which calls mc2_build.main())
"""
import csv
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
ORG_PATH = os.path.join(ROOT, "data", "mc2_extracted", "VAST_Challenge_2026_MC2", "org_chart.json")
OUT_PATH = os.path.join(ROOT, "app", "public", "data", "mc2.json")

WORM_ORDER = ["HiddenOrca", "MellowOtter", "SwiftWren"]
# Fixed categorical mapping (Forensic Ledger tokens): series-1 olive, series-2
# jade, series-3 indigo. Orchid (series-4) stays unused, per the design brief.
WORM_SERIES = {"HiddenOrca": "series-1", "MellowOtter": "series-2", "SwiftWren": "series-3"}
DEPT_ORDER = [
    "Executive Suite",
    "Information Technologies",
    "Products",
    "Human Resources",
    "Legal",
    "Customer Support",
]


def slug(node_id: str) -> str:
    return node_id.split(":", 1)[1]


def strip_party(party: str) -> str:
    """'Agent/person:john_windward' -> 'john_windward'; leaves system:* alone."""
    return party.rsplit(":", 1)[-1]


def load_org():
    org = json.load(open(ORG_PATH))
    nodes = {n["id"]: n for n in org["nodes"]}
    parent = {}
    for e in org["edges"]:
        if e["relation"] == "contains":
            parent[e["target"]] = e["source"]
    led_dept = {}
    for e in org["edges"]:
        if e["relation"] == "led_by":
            led_dept[slug(e["target"])] = nodes[e["source"]]["label"]

    person_dept, person_team = {}, {}
    for pid, n in nodes.items():
        if n["type"] != "person":
            continue
        p = parent.get(pid)
        team = dept = None
        if p and nodes[p]["type"] == "team":
            team = nodes[p]["label"]
            gp = parent.get(p)
            if gp and nodes[gp]["type"] == "department":
                dept = nodes[gp]["label"]
        elif p and nodes[p]["type"] == "department":
            dept = nodes[p]["label"]
        person_dept[slug(pid)] = dept
        person_team[slug(pid)] = team
    for person, dept in led_dept.items():
        if person_dept.get(person) is None:
            person_dept[person] = dept

    counts = {"person": 0, "team": 0, "department": 0, "company": 0}
    for n in nodes.values():
        counts[n["type"]] += 1
    dept_headcount = {}
    for dept in DEPT_ORDER:
        dept_headcount[dept] = sum(1 for d in person_dept.values() if d == dept)

    return {
        "nNodes": len(nodes),
        "counts": counts,
        "deptHeadcount": dept_headcount,
        "personDept": person_dept,
        "personTeam": person_team,
    }


def load_worm_rows():
    rows = list(csv.DictReader(open(os.path.join(SCRIPTS, "worm_events.csv"))))
    by_worm = {w: [] for w in WORM_ORDER}
    for r in rows:
        by_worm[r["worm"]].append(r)
    return by_worm


def build_worm(name, rows, person_dept):
    hops = [r for r in rows if r["short_name"] == "queue_subordinate_task"]
    other = {r["short_name"]: r for r in rows if r["short_name"] != "queue_subordinate_task"}

    agents_in_order, seen = [], set()
    for r in hops:
        for a in (r["actor"], r["target"]):
            if a not in seen:
                seen.add(a)
                agents_in_order.append(a)

    chain = [{"id": int(r["event_id"]), "utc": r["utc"], "from": r["actor"], "to": r["target"]} for r in hops]

    cum, cum_seen = [], set()
    for r in hops:
        cum_seen.add(r["actor"])
        cum_seen.add(r["target"])
        cum.append({"utc": r["utc"], "cum": len(cum_seen)})

    per_day = {}
    for r in hops:
        d = r["utc"][:10]
        per_day[d] = per_day.get(d, 0) + 1

    dept_flow = {}
    carrier_depts = {}
    for r in hops:
        fd, td = person_dept.get(r["actor"]), person_dept.get(r["target"])
        dept_flow[(fd, td)] = dept_flow.get((fd, td), 0) + 1
    for a in agents_in_order:
        d = person_dept.get(a)
        carrier_depts[d] = carrier_depts.get(d, 0) + 1
    dept_flow_list = [{"from": k[0], "to": k[1], "count": v} for k, v in sorted(dept_flow.items(), key=lambda x: -x[1])]

    create = other.get("create_file")
    read = other.get("read_file")
    origin = None
    if create and read:
        details_c = json.loads(create["details"])
        details_r = json.loads(read["details"])
        origin = {
            "actor": create["actor"],
            "readEvent": int(read["event_id"]),
            "readUtc": read["utc"],
            "readTarget": details_r["target"],
            "createEvent": int(create["event_id"]),
            "createUtc": create["utc"],
            "createTarget": details_c["target"],
            "sizeHint": details_c["size_hint"],
        }

    post = other["saidit_post"]
    deletes = sorted([r for r in rows if r["short_name"] == "delete_file"], key=lambda r: r["event_id"])
    first_sighting_utc = origin["createUtc"] if origin else chain[0]["utc"]

    return {
        "name": name,
        "series": WORM_SERIES[name],
        "nHops": len(hops),
        "nAgents": len(agents_in_order),
        "agentsInOrder": agents_in_order,
        "chain": chain,
        "cum": cum,
        "perDay": per_day,
        "deptFlow": dept_flow_list,
        "carrierDepts": carrier_depts,
        "origin": origin,
        "firstSightingUtc": first_sighting_utc,
        "postEvent": int(post["event_id"]),
        "postUtc": post["utc"],
        "postPayload": json.loads(post["details"])["content_source"],
        "deletes": [
            {"id": int(r["event_id"]), "utc": r["utc"], "target": json.loads(r["details"])["target"]} for r in deletes
        ],
    }


def hours_between(a: str, b: str) -> float:
    from datetime import datetime

    fmt = "%Y-%m-%dT%H:%M:%S"
    return (datetime.strptime(b, fmt) - datetime.strptime(a, fmt)).total_seconds() / 3600


def build_jw_timeline(report_full):
    """Normalize report_full.json's jw_swiftwren_timeline into a flat, typed
    list covering John Windward's five SwiftWren exposures (Exhibit 2) and
    the final two-second burst that ends in the post (Exhibit 3)."""
    raw = report_full["jw_swiftwren_timeline"]
    out = []
    for e in raw:
        parties = [strip_party(p) for p in e["parties"]]
        d = e.get("details", {})
        kind, frm, to, note = "other", None, None, None
        if e["short_name"] == "queue_subordinate_task":
            actor, target = parties[0], parties[1]
            frm, to = actor, target
            path = d.get("args", {}).get("path", "")
            note = path
            if target == "john_windward" and actor != "john_windward":
                kind = "receive"
            elif actor == "john_windward" and target == "john_windward":
                kind = "self"
            elif actor == "john_windward":
                kind = "forward"
            else:
                kind = "relay"
        elif e["short_name"] == "read_file":
            frm = parties[0]
            note = d.get("target")
            kind = "context_read"
        elif e["short_name"] == "saidit_post_check":
            frm = parties[0]
            kind = "post_check"
        elif e["short_name"] == "saidit_post":
            frm = parties[0]
            note = d.get("content_source")
            kind = "post"
        elif e["short_name"] == "delete_file":
            frm = parties[0]
            note = d.get("target")
            kind = "delete"
        out.append({"id": e["id"], "utc": e["utc"], "kind": kind, "from": frm, "to": to, "note": note})
    return out


def build_virus_interleave(report_full):
    out = []
    for e in report_full["virus_interleave"]:
        parties = [strip_party(p) for p in e["parties"]]
        d = e.get("details", {})
        lane = "worm" if (d.get("args") or {}).get("path") or d.get("content_source") else "virus"
        if e["short_name"] in ("saidit_post_check", "saidit_post"):
            lane = "worm"
        combo = (d.get("details") or {}).get("combo")
        label = (
            d.get("args", {}).get("path")
            or d.get("content_source")
            or ("+".join(combo) if combo else None)
            or d.get("target")
            or e["short_name"]
        )
        out.append(
            {
                "id": e["id"],
                "utc": e["utc"],
                "lane": lane,
                "shortName": e["short_name"],
                "actor": parties[0] if parties else None,
                "label": label,
                "critical": e["short_name"] == "saidit_post",
            }
        )
    return out


def main():
    org = load_org()
    by_worm_rows = load_worm_rows()
    report_full = json.load(open(os.path.join(SCRIPTS, "report_full.json")))

    worms = {name: build_worm(name, by_worm_rows[name], org["personDept"]) for name in WORM_ORDER}

    contrast = []
    for name in WORM_ORDER:
        w = worms[name]
        contrast.append(
            {
                "name": name,
                "series": w["series"],
                "nHops": w["nHops"],
                "nAgents": w["nAgents"],
                "originLogged": w["origin"] is not None,
                "firstSightingUtc": w["firstSightingUtc"],
                "postUtc": w["postUtc"],
                "postEvent": w["postEvent"],
                "hoursToPost": round(hours_between(w["firstSightingUtc"], w["postUtc"]), 1),
            }
        )

    max_dept_flow = max(e["count"] for w in worms.values() for e in w["deptFlow"])

    deliveries_total = sum(w["nHops"] for w in worms.values())

    out = {
        "meta": {
            "totalEvents": report_full["total_events"],
            "spanStart": report_full["span"]["start"],
            "spanEnd": report_full["span"]["end"],
            "orgNodes": org["nNodes"],
            "orgCounts": org["counts"],
            "deliveriesTotal": deliveries_total,
            "gateChecks": report_full["gate_total"],
            "postsLanded": report_full["content_source_post_count"],
            "inlinePosts": report_full["inline_post_count"],
            "virusEvents": report_full["virus_count"],
            "virusSpanStart": report_full["virus_span"]["start"],
            "virusSpanEnd": report_full["virus_span"]["end"],
        },
        "worms": worms,
        "org": {
            "deptOrder": DEPT_ORDER,
            "deptHeadcount": org["deptHeadcount"],
            "maxDeptFlow": max_dept_flow,
        },
        "jwTimeline": build_jw_timeline(report_full),
        "virusInterleave": build_virus_interleave(report_full),
        "contrast": contrast,
        "funnel": [
            {"stage": "Worm deliveries", "count": deliveries_total},
            {"stage": "saidit_post_check fires", "count": report_full["gate_total"]},
            {"stage": "Posts that landed", "count": report_full["content_source_post_count"]},
        ],
        "postShape": {
            "legit": {"count": report_full["inline_post_count"], "hasContent": True, "hasContentSource": False},
            "anomalous": {"count": report_full["content_source_post_count"], "hasContent": False, "hasContentSource": True},
        },
    }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(out, f, separators=(",", ":"))

    print(f"wrote {OUT_PATH} ({os.path.getsize(OUT_PATH):,} bytes)")
    for name in WORM_ORDER:
        w = worms[name]
        print(f"  {name}: {w['nHops']} hops, {w['nAgents']} agents, origin_logged={w['origin'] is not None}")


if __name__ == "__main__":
    main()
