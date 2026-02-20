import heapq


def _build_adj_from_mst(graph, mst):
    adj = {v: [] for v in graph.nodes}
    for u, v, w in mst:
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj


def dijkstra(graph, start, mst=None):
    dist = {v: float("inf") for v in graph.nodes}
    prev = {v: None for v in graph.nodes}
    dist[start] = 0

    # If MST is provided, find path only on MST edges.
    edges = _build_adj_from_mst(graph, mst) if mst is not None else graph.edges

    pq = [(0, start)]

    while pq:
        cur_dist, u = heapq.heappop(pq)

        if cur_dist > dist[u]:
            continue

        for v, w in edges[u]:
            if dist[v] > dist[u] + w:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))

    return dist, prev
