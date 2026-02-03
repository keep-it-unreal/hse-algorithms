import random
import math
from graph import *

def generate_graph(n, obstacle_prob=0.2):
    g = Graph()

    # создаем узлы
    for i in range(n):
        x, y = random.random(), random.random()
        g.add_node(i, x, y)

    # соединяем близкие узлы
    for i in g.nodes:
        for j in g.nodes:
            if i >= j:
                continue

            x1, y1 = g.nodes[i]
            x2, y2 = g.nodes[j]
            dist = math.hypot(x1 - x2, y1 - y2)

            if random.random() > obstacle_prob:
                cost = dist * random.uniform(0.8, 1.2)
                g.add_edge(i, j, cost)
            else:
                # препятствие, не добавляем ребро
                g.add_obstacle("Obstacle_{}_{}".format(i, j), (x1 + x2) / 2, (y1 + y2) / 2)

    return g
