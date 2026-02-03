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
