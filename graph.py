class Graph:
    def __init__(self):
        self.nodes = {}   # id -> (x, y)
        self.edges = {}   # id -> list of (neighbor, weight)
        self.obstacles = {}  # id -> (x, y)

    def add_node(self, node_id, x, y):
        self.nodes[node_id] = (x, y)
        self.edges[node_id] = []

    def add_edge(self, u, v, w):
        self.edges[u].append((v, w))
        self.edges[v].append((u, w))

    def add_obstacle(self, obstacle_id, x, y):
        self.obstacles[obstacle_id] = (x, y)

    def to_dict(self):
        unique_edges = []
        for u in self.edges:
            for v, w in self.edges[u]:
                if u < v:
                    unique_edges.append({"u": u, "v": v, "w": w})

        return {
            "nodes": [
                {"id": node_id, "x": x, "y": y}
                for node_id, (x, y) in self.nodes.items()
            ],
            "edges": unique_edges,
            "obstacles": [
                {"id": obstacle_id, "x": x, "y": y}
                for obstacle_id, (x, y) in self.obstacles.items()
            ],
        }

    @staticmethod
    def from_dict(data):
        g = Graph()

        nodes_data = data.get("nodes", [])
        if isinstance(nodes_data, dict):
            for node_id, coords in nodes_data.items():
                g.add_node(int(node_id), coords[0], coords[1])
        else:
            for node in nodes_data:
                g.add_node(int(node["id"]), node["x"], node["y"])

        seen_edges = set()
        for edge in data.get("edges", []):
            u = int(edge["u"])
            v = int(edge["v"])
            w = edge["w"]
            key = (min(u, v), max(u, v))
            if key in seen_edges:
                continue
            seen_edges.add(key)
            g.add_edge(u, v, w)

        obstacles_data = data.get("obstacles", [])
        if isinstance(obstacles_data, dict):
            for obstacle_id, coords in obstacles_data.items():
                g.add_obstacle(str(obstacle_id), coords[0], coords[1])
        else:
            for obstacle in obstacles_data:
                g.add_obstacle(str(obstacle["id"]), obstacle["x"], obstacle["y"])

        return g
