# Measured results

Maps: 160 × 160; seed 357; median of 5 batches after warmup. Python uses 30 solves per batch. C uses at least that many, calibrated toward 200 ms per batch (maximum 10,000); actual counts are in raw.csv.

| Map | Language | Algorithm | Optimal cost | Expanded | Median ms |
|---|---|---|---:|---:|---:|
| open | Python | dijkstra | 318 | 25600 | 135.747 |
| open | Python | astar | 318 | 319 | 2.018 |
| open | C | dijkstra | 318 | 25600 | 2.098 |
| open | C | astar | 318 | 319 | 0.035 |
| barriers | Python | dijkstra | 6284 | 18777 | 87.354 |
| barriers | Python | astar | 6284 | 18439 | 112.239 |
| barriers | C | dijkstra | 6284 | 18777 | 0.537 |
| barriers | C | astar | 6284 | 18439 | 1.451 |
| weighted | Python | dijkstra | 467 | 23060 | 125.805 |
| weighted | Python | astar | 467 | 17645 | 129.908 |
| weighted | C | dijkstra | 467 | 23060 | 2.778 |
| weighted | C | astar | 467 | 17645 | 3.588 |

## Interpretation

The open map favors A*: Manhattan distance is exact and ties favor larger g. Barriers force detours the heuristic cannot foresee. Random terrain weakens the lower bound because it assumes every move costs only one.

All four implementations agree on cost. Expansion counts are deterministic; timings depend on machine, compiler and clock. These are three illustrative workloads, not a universal speed claim.

Parsing, process startup and JSON output are excluded. Search allocation and Python's visited-list collection are included. Windows measurements use wall time for both languages (Python perf_counter and Windows CRT clock); Linux uses process CPU time. Windows C clock has coarser resolution, so batches amortize quantization. Raw samples and environment details are committed alongside this report.

See [raw.csv](raw.csv) and [environment.json](environment.json).
