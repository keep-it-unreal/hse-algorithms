class DSU:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra
            return True
        return False


def kruskal_mst(graph):
    edges = []
    for u in graph.edges:
        for v, w in graph.edges[u]:
            if u < v:
                edges.append((w, u, v))

    edges.sort()

    node_ids = list(graph.nodes.keys())
    node_to_idx = {node_id: idx for idx, node_id in enumerate(node_ids)}

    dsu = DSU(len(node_ids))
    mst = []

    for w, u, v in edges:
        if dsu.union(node_to_idx[u], node_to_idx[v]):
            mst.append((u, v, w))

    return mst
