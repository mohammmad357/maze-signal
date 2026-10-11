"""Rebuild fixed maps, SVG comparison, raw timings and Markdown report."""
import argparse
import csv
import json
import math
from pathlib import Path
import platform
import os
import random
import statistics
import subprocess
import sys
from time import process_time, perf_counter

ROOT = Path(__file__).resolve().parents[1]
CLOCK = perf_counter if os.name == "nt" else process_time
sys.path.insert(0, str(ROOT / "python"))
from solver import parse, solve


def make_map(size, kind, seed=357):
    rng = random.Random(seed)
    grid = [["." for _ in range(size)] for _ in range(size)]
    if kind == "weighted":
        grid = [[rng.choice("...123999#") for _ in range(size)] for _ in range(size)]
    elif kind == "barriers":
        for x in range(3, size-1, 4):
            gap = size-2 if (x // 4) % 2 == 0 else 1
            for y in range(size):
                if y != gap:
                    grid[y][x] = "#"
    # Weighted benchmark has a guaranteed route; its costs remain random.
    if kind == "weighted":
        for i in range(size):
            if grid[0][i] == "#": grid[0][i] = "."
            if grid[i][-1] == "#": grid[i][-1] = "."
    grid[0][0], grid[-1][-1] = "S", "G"
    return f"{size} {size}\n" + "\n".join("".join(row) for row in grid) + "\n"


def svg(rows, start, goal):
    width = len(rows[0]); scale = 12; panel = width * scale
    content = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{2*panel+100}" height="{panel+160}" viewBox="0 0 {2*panel+100} {panel+160}">',
               '<rect width="100%" height="100%" fill="#0b1220"/>',
               '<g font-family="Arial,sans-serif" fill="#eef6ff">',
               '<text x="28" y="34" font-size="25" font-weight="bold">MAZE SIGNAL</text>',
               '<text x="28" y="57" font-size="13" fill="#9bb1cc">Same optimal route. Different search footprints.</text>']
    for k, algorithm in enumerate(("dijkstra", "astar")):
        result = solve(rows, start, goal, algorithm)
        seen, path = set(result["visited"]), set(result["path"])
        offset = 28 + k * (panel + 40)
        content.append(f'<text x="{offset}" y="86" font-size="17">{algorithm.upper()} · {result["expanded"]} expanded · cost {result["cost"]}</text>')
        for r, row in enumerate(rows):
            for c, cell in enumerate(row):
                i = r * width + c
                color = "#172238" if cell == "#" else "#273b50"
                if i in seen: color = "#277b93"
                if i in path: color = "#ffca62"
                if cell == "S": color = "#4ee1a0"
                if cell == "G": color = "#ff647c"
                content.append(f'<rect x="{offset+c*scale}" y="{100+r*scale}" width="11" height="11" rx="1" fill="{color}"/>')
    content.append(f'<text x="28" y="{panel+130}" font-size="12" fill="#9bb1cc">Teal: expanded cells · Gold: optimal path · Green: start · Pink: goal</text></g></svg>')
    (ROOT / "assets" / "search.svg").write_text("\n".join(content), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--size", type=int, default=160)
    parser.add_argument("--repeat", type=int, default=30)
    parser.add_argument("--samples", type=int, default=5)
    args = parser.parse_args()
    if not 2 <= args.size <= 1024 or not 1 <= args.repeat <= 10000 or not 1 <= args.samples <= 100:
        parser.error("size 2..1024; repeat 1..10000; samples 1..100")
    binary = args.binary.resolve()
    records = []
    for kind in ("open", "barriers", "weighted"):
        path = ROOT / "maps" / f"{kind}.txt"
        path.write_text(make_map(args.size, kind), encoding="ascii")
        rows, start, goal = parse(path.read_text())
        costs = set()
        for algorithm in ("dijkstra", "astar"):
            solve(rows, start, goal, algorithm)  # warmup
            calibration = json.loads(subprocess.check_output([str(binary), str(path), algorithm, "100"], text=True))
            native_repeat = min(10000, max(args.repeat, math.ceil(0.2 / max(calibration["seconds"], 0.00001))))
            for language in ("Python", "C"):
                for sample in range(args.samples):
                    if language == "Python":
                        begin = CLOCK()
                        for _ in range(args.repeat):
                            result = solve(rows, start, goal, algorithm)
                        seconds = (CLOCK() - begin) / args.repeat
                    else:
                        result = json.loads(subprocess.check_output([str(binary), str(path), algorithm, str(native_repeat)], text=True))
                        seconds = result["seconds"]
                    costs.add(result["cost"])
                    records.append(dict(map=kind, language=language, algorithm=algorithm, sample=sample+1, repeats=args.repeat if language == "Python" else native_repeat,
                                        cost=result["cost"], expanded=result["expanded"], milliseconds=seconds*1000))
        assert len(costs) == 1, "algorithms disagree"
        print(f"Measured {kind}", flush=True)
    with (ROOT / "results" / "raw.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(records[0]))
        writer.writeheader(); writer.writerows(records)
    metadata = dict(platform=platform.platform(), processor=platform.processor(), python=sys.version,
                    compiler=subprocess.check_output(["gcc", "--version"], text=True).splitlines()[0],
                    size=args.size, seed=357, repeats=args.repeat, samples=args.samples,
                    clock="Wall time on Windows (perf_counter / CRT clock); CPU time on Linux (process_time / clock)",
                    flags="-std=c11 -O3 -Wall -Wextra -Wpedantic")
    (ROOT / "results" / "environment.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    lines = ["# Measured results", "", f"Maps: {args.size} × {args.size}; seed 357; median of {args.samples} batches after warmup. Python uses {args.repeat} solves per batch. C uses at least that many, calibrated toward 200 ms per batch (maximum 10,000); actual counts are in raw.csv.", "",
             "| Map | Language | Algorithm | Optimal cost | Expanded | Median ms |", "|---|---|---|---:|---:|---:|"]
    for kind in ("open", "barriers", "weighted"):
        for language in ("Python", "C"):
            for algorithm in ("dijkstra", "astar"):
                group = [r for r in records if (r["map"], r["language"], r["algorithm"]) == (kind, language, algorithm)]
                lines.append(f'| {kind} | {language} | {algorithm} | {group[0]["cost"]} | {group[0]["expanded"]} | {statistics.median(r["milliseconds"] for r in group):.3f} |')
    lines += ["", "## Interpretation", "", "The open map favors A*: Manhattan distance is exact and ties favor larger g. Barriers force detours the heuristic cannot foresee. Random terrain weakens the lower bound because it assumes every move costs only one.", "", "All four implementations agree on cost. Expansion counts are deterministic; timings depend on machine, compiler and clock. These are three illustrative workloads, not a universal speed claim.", "", "Parsing, process startup and JSON output are excluded. Search allocation and Python's visited-list collection are included. Windows measurements use wall time for both languages (Python perf_counter and Windows CRT clock); Linux uses process CPU time. Windows C clock has coarser resolution, so batches amortize quantization. Raw samples and environment details are committed alongside this report.", "", "See [raw.csv](raw.csv) and [environment.json](environment.json)."]
    (ROOT / "results" / "RESULTS.md").write_text("\n".join(lines)+"\n", encoding="utf-8")
    preview = make_map(31, "open")
    (ROOT / "maps" / "demo.txt").write_text(preview, encoding="ascii")
    svg(*parse(preview))


if __name__ == "__main__":
    main()
