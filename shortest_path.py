import heapq


def _build_adj_from_mst(node_ids, mst):
    adj = {v: [] for v in node_ids}
    for u, v, w in mst:
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj


def dijkstra(start, mst):
    node_ids = set(x[0] for x in mst) | set(x[1] for x in mst)
    if start not in node_ids:
        raise ValueError(f"Start node {start} does not exist in graph")

    dist = {v: float("inf") for v in node_ids}
    prev = {v: None for v in node_ids}
    dist[start] = 0

    edges = _build_adj_from_mst(node_ids, mst)

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
