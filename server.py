import argparse
import json
import random
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from generator import generate_graph
from graph import Graph
from mst import kruskal_mst
from shortest_path import dijkstra, reconstruct_path


class GraphApiHandler(BaseHTTPRequestHandler):
    @staticmethod
    def _to_bool(value, default=True):
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            lowered = value.strip().lower()
            if lowered in {"1", "true", "yes", "y", "on"}:
                return True
            if lowered in {"0", "false", "no", "n", "off"}:
                return False
        if isinstance(value, (int, float)):
            return bool(value)
        raise ValueError("Invalid boolean value for 'use_mst'")

    def _send_json(self, status_code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def _parse_graph_payload(self, body):
        graph_payload = body.get("graph") if isinstance(body, dict) else None
        if graph_payload is None:
            graph_payload = body
        return Graph.from_dict(graph_payload)

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path != "/graph":
            self._send_json(404, {"error": "Endpoint not found"})
            return

        params = parse_qs(parsed.query)

        try:
            n = int(params.get("n", [15])[0])
            obstacle_prob = float(params.get("obstacle_prob", [0.2])[0])
            seed_param = params.get("seed", [None])[0]
            if seed_param is not None:
                random.seed(int(seed_param))

            graph = generate_graph(n=n, obstacle_prob=obstacle_prob)
            self._send_json(200, {"graph": graph.to_dict()})
        except Exception as exc:
            self._send_json(400, {"error": str(exc)})

    def do_POST(self):
        parsed = urlparse(self.path)

        try:
            body = self._read_json()
        except Exception:
            self._send_json(400, {"error": "Invalid JSON"})
            return

        if parsed.path == "/mst":
            try:
                graph = self._parse_graph_payload(body)
                mst = kruskal_mst(graph)
                mst_payload = [{"u": u, "v": v, "w": w} for u, v, w in mst]
                self._send_json(200, {"mst": mst_payload})
            except Exception as exc:
                self._send_json(400, {"error": str(exc)})
            return

        if parsed.path == "/shortest-path":
            try:
                if not isinstance(body, dict):
                    self._send_json(400, {"error": "Request body must be a JSON object"})
                    return

                graph = self._parse_graph_payload(body)

                if "start" not in body or "goal" not in body:
                    self._send_json(400, {"error": "Fields 'start' and 'goal' are required"})
                    return

                start = int(body["start"])
                goal = int(body["goal"])
                use_mst = self._to_bool(body.get("use_mst", True), default=True)

                mst = kruskal_mst(graph) if use_mst else None
                dist, prev = dijkstra(graph, start, mst)
                path = reconstruct_path(prev, start, goal)

                distance = dist.get(goal, float("inf"))
                reachable = distance != float("inf")

                self._send_json(
                    200,
                    {
                        "start": start,
                        "goal": goal,
                        "use_mst": use_mst,
                        "reachable": reachable,
                        "distance": distance if reachable else None,
                        "path": path,
                    },
                )
            except Exception as exc:
                self._send_json(400, {"error": str(exc)})
            return

        self._send_json(404, {"error": "Endpoint not found"})


def run_server(host="127.0.0.1", port=8000):
    server = ThreadingHTTPServer((host, port), GraphApiHandler)
    print(f"Server started at http://{host}:{port}")
    server.serve_forever()


def main():
    parser = argparse.ArgumentParser(description="Run graph API server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    run_server(args.host, args.port)


if __name__ == "__main__":
    main()
