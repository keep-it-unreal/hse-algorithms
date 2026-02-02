import random
import math
import heapq
import matplotlib.pyplot as plt
from generator import *
from shortest_path import *
from visualize import *
from mst import *

if __name__ == "__main__":
    random.seed(42)

    graph = generate_graph(n=15)
    mst = kruskal_mst(graph)

    start, goal = 0, 10
    dist, prev = dijkstra(graph, start)

    # восстановление пути
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()

    visualize(graph, mst=mst, path=path)
