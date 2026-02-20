import heapq


def _build_adj_from_mst(graph, mst):
    adj = {v: [] for v in graph.nodes}
    for u, v, w in mst:
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj


def dijkstra(graph, start, mst=None):
    if start not in graph.nodes:
        raise ValueError(f"Start node {start} does not exist in graph")

    dist = {v: float("inf") for v in graph.nodes}
    prev = {v: None for v in graph.nodes}
    dist[start] = 0

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


def reconstruct_path(prev, start, goal):
    if goal not in prev:
        return []

    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()

    if not path or path[0] != start:
        return []

    return path
