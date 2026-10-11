"""Optimal four-way weighted grid search; standard library only."""
from __future__ import annotations

import argparse
import heapq
import json
import os
from pathlib import Path
from time import process_time, perf_counter

CLOCK = perf_counter if os.name == "nt" else process_time


def parse(text: str) -> tuple[list[str], int, int]:
    lines = text.splitlines()
    if not lines:
        raise ValueError("empty map")
    dimensions = lines[0].split()
    if len(dimensions) != 2:
        raise ValueError("expected height width")
    height, width = map(int, dimensions)
    rows = lines[1:]
    if not (1 <= height <= 1024 and 1 <= width <= 1024):
        raise ValueError("dimensions must be in 1..1024")
    if len(rows) != height or any(len(row) != width for row in rows):
        raise ValueError("map dimensions do not match")
    flat = "".join(rows)
    if set(flat) - set("#.SG123456789"):
        raise ValueError("allowed cells: # . S G 1..9")
    if flat.count("S") != 1 or flat.count("G") != 1:
        raise ValueError("expected exactly one S and one G")
    return rows, flat.index("S"), flat.index("G")


def solve(rows: list[str], start: int, goal: int, algorithm: str = "astar") -> dict:
    if algorithm not in ("astar", "dijkstra"):
        raise ValueError("unknown algorithm")
    width = len(rows[0])
    cells = "".join(rows)
    size = len(cells)
    distance = [float("inf")] * size
    parent = [-1] * size
    closed: set[int] = set()
    visited = []

    def heuristic(node: int) -> int:
        return (abs(node // width - goal // width) + abs(node % width - goal % width)
                if algorithm == "astar" else 0)

    distance[start] = 0
    frontier = [(heuristic(start), 0, start)]
    while frontier:
        _, negative_cost, current = heapq.heappop(frontier)
        cost = -negative_cost
        if current in closed or cost != distance[current]:
            continue
        closed.add(current)
        visited.append(current)
        if current == goal:
            path = [goal]
            while path[-1] != start:
                path.append(parent[path[-1]])
            return {"cost": cost, "expanded": len(visited), "path": path[::-1], "visited": visited}
        row, col = divmod(current, width)
        for dr, dc in ((-1, 0), (0, -1), (0, 1), (1, 0)):
            nr, nc = row + dr, col + dc
            if not (0 <= nr < len(rows) and 0 <= nc < width):
                continue
            neighbor = nr * width + nc
            cell = cells[neighbor]
            if cell == "#":
                continue
            candidate = cost + (int(cell) if cell.isdigit() else 1)
            if candidate < distance[neighbor]:
                distance[neighbor] = candidate
                parent[neighbor] = current
                heapq.heappush(frontier, (candidate + heuristic(neighbor), -candidate, neighbor))
    return {"cost": None, "expanded": len(visited), "path": [], "visited": visited}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("map", type=Path)
    parser.add_argument("algorithm", choices=("astar", "dijkstra"), nargs="?", default="astar")
    parser.add_argument("--repeat", type=int, default=1)
    args = parser.parse_args()
    if not 1 <= args.repeat <= 10000:
        parser.error("repeat must be in 1..10000")
    try:
        rows, start, goal = parse(args.map.read_text(encoding="ascii"))
    except (ValueError, OSError) as error:
        parser.error(str(error))
    begin = CLOCK()
    for _ in range(args.repeat):
        result = solve(rows, start, goal, args.algorithm)
    elapsed = (CLOCK() - begin) / args.repeat
    result.pop("visited")
    result["seconds"] = elapsed
    print(json.dumps(result))


if __name__ == "__main__":
    main()
