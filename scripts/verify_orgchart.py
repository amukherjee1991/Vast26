import json, sys, collections

path = sys.argv[1]
with open(path) as f:
    g = json.load(f)

nodes = g['nodes']
edges = g['edges']
print("nodes:", len(nodes), "edges:", len(edges))
type_counts = collections.Counter(n['type'] for n in nodes)
print("node types:", type_counts)

edge_rel_counts = collections.Counter(e.get('relation', e.get('label','?')) for e in edges)
print("edge keys sample:", edges[0], edges[1] if len(edges)>1 else None)

node_by_id = {n['id']: n for n in nodes}

# build contains parent map: parent -contains-> child  (source contains target probably)
contains_edges = [e for e in edges if e.get('relation')=='contains' or e.get('type')=='contains']
print("contains edges count (guess key):", len(contains_edges))
print(json.dumps(edges[:8], indent=2))
