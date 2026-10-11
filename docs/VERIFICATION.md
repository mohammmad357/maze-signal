# Browser demo verification — 2026-10-11

## Search correctness

505 maps (5 fixed + 500 generated with Python seed 357), each with Dijkstra and A*, passed 1010 JavaScript comparisons with Python fixtures. Python fixtures were independently matched against C for cost, path and expanded count. JavaScript visitation order also matched Python. The original Python suite had already checked these cases against Bellman-Ford.

The standalone Node check additionally rejects eight invalid inputs, overlapping endpoints and unknown algorithms, and verifies cost 78 on the maximum-size 40 × 40 open demo grid.

The portable fixture generator rebuilt byte-identical data locally. The `browser-demo-parity` workflow checks committed fixtures, regenerates them from Python/C and rejects drift on pushes and pull requests.

## UI checks

The supported in-app browser was used for local and public HTTPS checks:

| Case | Observed outcome |
|---|---|
| Default weighted detour | Both cost 8, moves 8, expanded 9 |
| Block the bottom detour | Both cost 28, expanded 8 |
| Unreachable example | Both no route, expanded 6 |
| Open 10 × 14 grid | Cost 22 for both; Dijkstra 140 expanded, A* 23 |
| Change a terrain cell to 2 | Both cost 9; previous results cleared |
| Try start on goal | Clear rejection; endpoints remain distinct |
| Move both endpoints | Both panels show the same new endpoints |
| Keyboard navigation + Enter | Wall applied and reflected in the other panel |
| Pause/Resume | Paused state and Resume control shown |
| Reset while running | Animation cancelled; metrics cleared |
| Run again while running | Older animation replaced; final metrics correct |
| Clear walls and weights | Terrain cleared; start and goal retained |
| Mobile viewport 390 px wide | Effective content width 375 px with scrollbar; no horizontal overflow; default comparison worked |

Live HTTPS checks repeated the weighted detour, open grid and unreachable example in a fresh tab. The 60-second GIF loaded publicly at 1000 × 640. It contains 12 five-second scenes; durations sum to 60000 ms.

## Limits

The mobile check was a viewport check, not a physical Android/iOS test. Dragging and real touch gestures were not automated. A separate browser engine and an independent outside user's first-use review were not available during these automated checks. The checklist's first outside-user review remains a later task.

Animation speed is presentation only. No JavaScript-versus-Python/C timing claim is made. The GIF is generated from the actual Python search results and is not a screen recording.
