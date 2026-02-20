import argparse
import random

from generator import generate_graph
from mst import kruskal_mst
from shortest_path import dijkstra, reconstruct_path
from visualize import visualize
from server import run_server


def run_visual_demo(seed=42, n=15, start=0, goal=8):
    random.seed(seed)

    graph = generate_graph(n=n)
    mst = kruskal_mst(graph)

    dist, prev = dijkstra(graph, start, mst)
    path = reconstruct_path(prev, start, goal)

    visualize(graph, mst=mst, path=path)


def main():
    parser = argparse.ArgumentParser(description="Graph app")
    subparsers = parser.add_subparsers(dest="command")

    visualize_parser = subparsers.add_parser("visualize", help="Run visualization demo")
    visualize_parser.add_argument("--seed", type=int, default=42)
    visualize_parser.add_argument("--n", type=int, default=15)
    visualize_parser.add_argument("--start", type=int, default=0)
    visualize_parser.add_argument("--goal", type=int, default=8)

    server_parser = subparsers.add_parser("server", help="Run HTTP server")
    server_parser.add_argument("--host", default="127.0.0.1")
    server_parser.add_argument("--port", type=int, default=8000)

    args = parser.parse_args()

    if args.command == "server":
        run_server(host=args.host, port=args.port)
        return

    run_visual_demo(
        seed=getattr(args, "seed", 42),
        n=getattr(args, "n", 15),
        start=getattr(args, "start", 0),
        goal=getattr(args, "goal", 8),
    )


if __name__ == "__main__":
    main()
