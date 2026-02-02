import matplotlib.pyplot as plt

def visualize(graph, mst=None, path=None):
    plt.figure(figsize=(8, 8))

    # все ребра
    for u in graph.edges:
        x1, y1 = graph.nodes[u]
        for v, _ in graph.edges[u]:
            x2, y2 = graph.nodes[v]
            plt.plot([x1, x2], [y1, y2], color="lightgray", zorder=1)

    # MST
    if mst:
        for u, v, _ in mst:
            x1, y1 = graph.nodes[u]
            x2, y2 = graph.nodes[v]
            plt.plot([x1, x2], [y1, y2], color="green", linewidth=2, zorder=2)

    # путь
    if path:
        for i in range(len(path) - 1):
            x1, y1 = graph.nodes[path[i]]
            x2, y2 = graph.nodes[path[i + 1]]
            plt.plot([x1, x2], [y1, y2], color="red", linewidth=3, zorder=3)

    # узлы
    for node, (x, y) in graph.nodes.items():
        plt.scatter(x, y, color="black")
        plt.text(x + 0.01, y + 0.01, str(node))

    plt.title("Mars Colony Infrastructure")
    plt.axis("off")
    plt.show()
