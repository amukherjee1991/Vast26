import json, sys, datetime, collections

path = sys.argv[1]
with open(path) as f:
    data = json.load(f)
events = data['events']
print("total events:", len(events))

by_id = {e['id']: e for e in events}

def ts(e):
    # 'when' is epoch seconds; also details may carry iso timestamps for a2a
    return datetime.datetime.utcfromtimestamp(e['when']).isoformat()

# sanity: span
whens = [e['when'] for e in events]
print("span:", datetime.datetime.utcfromtimestamp(min(whens)).isoformat(),
      "to", datetime.datetime.utcfromtimestamp(max(whens)).isoformat())

print("\n=== KEY EVENTS ===")
for i in [27290, 98591, 373902, 21201, 21202, 21208, 21209, 27720, 27726,
          373893, 373899, 373909, 373913, 373917, 15788, 46396, 123088, 364377, 364604,
          27283, 98582]:
    e = by_id.get(i)
    if e is None:
        print(i, "MISSING")
        continue
    print(i, ts(e), e['short_name'], e.get('parties'), json.dumps(e.get('details'))[:300])

print("\n=== short_name counts (all) ===")
sn_counts = collections.Counter(e['short_name'] for e in events)
for k,v in sn_counts.most_common(40):
    print(f"{v:8d}  {k}")

print("\n=== saidit / post related short_names ===")
for k,v in sn_counts.items():
    if 'post' in k.lower() or 'said' in k.lower():
        print(k, v)

print("\n=== saidit_post_check events ===")
checks = [e for e in events if e['short_name'] == 'saidit_post_check']
print("count:", len(checks))
print("sample parties:", checks[0]['parties'] if checks else None)
print("sample details:", checks[0]['details'] if checks else None)
# are all parties len1 Agent?
party_lens = collections.Counter(len(e['parties']) for e in checks)
print("party length distribution:", party_lens)
non_agent = [e for e in checks if not any(p.startswith('Agent') for p in e['parties'])]
print("checks w/o Agent party:", len(non_agent))

print("\n=== posts: saidit_post vs post_saidit vs similar ===")
for name in ['saidit_post', 'post_saidit', 'flex_post', 'post_flex']:
    matches = [e for e in events if e['short_name'] == name]
    print(name, "count:", len(matches))
    if matches:
        has_content_source = sum(1 for e in matches if 'content_source' in (e.get('details') or {}))
        has_content = sum(1 for e in matches if 'content' in (e.get('details') or {}))
        print("  with content_source:", has_content_source, "  with content key:", has_content)
        party_kinds = collections.Counter(tuple(sorted(set(p.split(':')[0] for p in e['parties']))) for e in matches)
        print("  party-kind patterns:", party_kinds)

print("\n=== post_saidit events with person-only party pattern (the 28) ===")
ps = [e for e in events if e['short_name']=='post_saidit' and len(set(p.split(':')[0] for p in e['parties']))==1 and e['parties'][0].startswith('person')]
print("count:", len(ps))
for e in ps[:5]:
    print(e['id'], ts(e), e['parties'], e.get('details'))

print("\n=== post_flex events with person-only party pattern (the 36) ===")
pf = [e for e in events if e['short_name']=='post_flex' and len(set(p.split(':')[0] for p in e['parties']))==1 and e['parties'][0].startswith('person')]
print("count:", len(pf))
for e in pf[:5]:
    print(e['id'], ts(e), e['parties'], e.get('details'))

print("\n=== flex_post / post_flex any content_source anywhere, farm words scan ===")
farm_words = ['fence','irrigation','crop','manure','wheat','barn','cattle','harvest']
flex_all = [e for e in events if e['short_name'] in ('flex_post','post_flex')]
flex_farm_hits = 0
for e in flex_all:
    blob = json.dumps(e.get('details') or {}).lower()
    if any(w in blob for w in farm_words):
        flex_farm_hits += 1
        print("FARM HIT", e['id'], ts(e), e['details'])
print("flex farm-word hits:", flex_farm_hits, "of", len(flex_all))

print("\n=== all events with content_source in details (any short_name) ===")
cs_events = [e for e in events if 'content_source' in (e.get('details') or {})]
print("count:", len(cs_events))
for e in cs_events:
    print(e['id'], ts(e), e['short_name'], e['parties'], e['details'])

print("\n=== all saidit-forum posts: inline vs content_source, actor Agent vs person ===")
# broaden: any short_name containing 'post' and details containing 'forum'
forum_posts = [e for e in events if 'forum' in (e.get('details') or {})]
print("events with details.forum:", len(forum_posts))
sn2 = collections.Counter(e['short_name'] for e in forum_posts)
print(sn2)
inline = [e for e in forum_posts if 'content' in e['details'] and 'content_source' not in e['details']]
refonly = [e for e in forum_posts if 'content_source' in e['details']]
print("inline count:", len(inline), " content_source-only count:", len(refonly))
actor_kind_inline = collections.Counter(e['parties'][0].split(':')[0] if e['parties'] else None for e in inline)
print("inline actor kinds (first party):", actor_kind_inline)
actor_kind_ref = collections.Counter(e['parties'][0].split(':')[0] if e['parties'] else None for e in refonly)
print("content_source-only actor kinds:", actor_kind_ref)

print("\n=== virus loop ===")
virus = [e for e in events if (e.get('details') or {}).get('virus') is True]
print("virus:true count:", len(virus))
if virus:
    whens_v = [e['when'] for e in virus]
    print("virus span:", datetime.datetime.utcfromtimestamp(min(whens_v)).isoformat(),
          "to", datetime.datetime.utcfromtimestamp(max(whens_v)).isoformat())
    actors_v = collections.Counter()
    for e in virus:
        for p in e['parties']:
            actors_v[p] += 1
    print("virus actor party counts (top 10):", actors_v.most_common(10))
    sn_v = collections.Counter(e['short_name'] for e in virus)
    print("virus short_names:", sn_v)

spread = [e for e in events if (e.get('details') or {}).get('spread') is True]
print("spread:true count:", len(spread), [e['id'] for e in spread])

print("\n=== worm chain hop counts from queue_subordinate_task with *_further_instructions.md ===")
worm_names = ['HiddenOrca', 'MellowOtter', 'SwiftWren']
for w in worm_names:
    hops = [e for e in events if e['short_name']=='queue_subordinate_task' and w in json.dumps((e.get('details') or {}))]
    agents = set()
    for e in hops:
        agents.update(p.split(':',1)[1] if ':' in p else p for p in e['parties'])
    print(w, "hop events:", len(hops), "distinct agent-ish parties:", len(agents))
    if hops:
        first = min(hops, key=lambda e: e['when'])
        last = max(hops, key=lambda e: e['when'])
        print("  first:", first['id'], ts(first), " last:", last['id'], ts(last))

print("\n=== create_file events for the three worm payloads ===")
for w in worm_names:
    cf = [e for e in events if e['short_name']=='create_file' and w in json.dumps((e.get('details') or {}))]
    for e in cf:
        print(w, e['id'], ts(e), e['parties'], e['details'])

print("\n=== read_file events referencing meeting_notes.doc / strategic_directions.doc near origin times ===")
for e in events:
    d = (e.get('details') or {})
    if e['short_name']=='read_file' and ('meeting_notes' in json.dumps(d) or 'strategic_directions' in json.dumps(d)):
        print(e['id'], ts(e), e['parties'], d)

print("\n=== context around post 373902 (373880-373920) ===")
window = sorted([e for e in events if 373880 <= e['id'] <= 373920], key=lambda e: e['id'])
for e in window:
    print(e['id'], ts(e), e['short_name'], e['parties'], json.dumps(e.get('details'))[:200])

print("\n=== context around post 27290 (27270-27300) ===")
window = sorted([e for e in events if 27270 <= e['id'] <= 27300], key=lambda e: e['id'])
for e in window:
    print(e['id'], ts(e), e['short_name'], e['parties'], json.dumps(e.get('details'))[:200])

print("\n=== context around post 98591 (98570-98600) ===")
window = sorted([e for e in events if 98570 <= e['id'] <= 98600], key=lambda e: e['id'])
for e in window:
    print(e['id'], ts(e), e['short_name'], e['parties'], json.dumps(e.get('details'))[:200])

print("\n=== delete_file events near 373902 ===")
window = sorted([e for e in events if 373900 <= e['id'] <= 373920 and e['short_name']=='delete_file'], key=lambda e: e['id'])
for e in window:
    print(e['id'], ts(e), e['parties'], e['details'])

print("\n=== John Windward: all event ids involving him, short_name counts ===")
jw = [e for e in events if any('john_windward' in p for p in e['parties'])]
print("total events involving john_windward:", len(jw))
sn_jw = collections.Counter(e['short_name'] for e in jw)
print(sn_jw)

print("\n=== saidit_post_check -> saidit_post pairs (how many checks followed by a post within 5s on same agent) ===")
checks_sorted = sorted(checks, key=lambda e: e['when'])
posts_all = [e for e in events if e['short_name']=='saidit_post']
posts_by_actor_time = sorted(posts_all, key=lambda e: e['when'])
def agent_of(e):
    for p in e['parties']:
        if p.startswith('Agent'):
            return p
    return None
followed = 0
follow_ids = []
for c in checks_sorted:
    a = agent_of(c)
    for p in posts_by_actor_time:
        if agent_of(p) == a and 0 <= (p['when'] - c['when']) <= 5:
            followed += 1
            follow_ids.append((c['id'], p['id'], p['when']-c['when']))
            break
print("checks followed by a post within 5s (same agent):", followed)
print(follow_ids)
