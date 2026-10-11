# Maze Signal browser demo

Live demo: https://mohammmad357.github.io/maze-signal/

This buildless HTML/CSS/JavaScript editor runs entirely in the browser. Both panels edit the same map. Paint walls or terrain, move distinct endpoints, then run Dijkstra and A*.

## Controls and contract

- Click/tap or drag with Wall, Erase or Terrain weight. Use Start/Goal to move an endpoint; endpoints remain distinct and traversable.
- Arrow keys move focus between cells; Space/Enter applies the selected tool.
- Run comparison replaces an older run. Pause/Resume controls the presentation. Reset restores the chosen example; Clear removes walls and weights while preserving endpoints.
- Every edit cancels prior animation and invalidates old results. No route is a valid result, with an empty path.
- Four-neighbor movement, entry costs 1–9, initial start cost zero, Manhattan heuristic and tie order matching the Python/C implementation.
- The parser supports grids up to 40 × 40; the editor offers three preset sizes. The CLI supports up to 1024 × 1024. Custom-map import and grid resizing are not UI features in this version.

Expanded cells and path cost are the comparison metrics. Animation speed is not search performance; JavaScript browser behavior is not the repository's Python/C benchmark.

## Reproduce verification

The standalone search module uses no npm packages. Node.js is only needed for the development verification command:

```sh
node docs/verify.cjs
```

`fixtures.json` contains 5 fixed and 500 seed-357 random maps, generated from Python and cross-checked against C at source commit `ad47871694160f0a2efc45b9f4594b6405cff06d`. Verification compares JavaScript cost, route, expanded count and visitation order with Python; cost, route and expanded count were also matched against C. The existing Python test suite checks these map cases against an independent Bellman-Ford reference. Eight invalid inputs, overlapping endpoints and a maximum-size demo grid are also checked.

Local preview from the repository root:

```sh
python -m http.server 8000 --directory docs
```

Open http://localhost:8000. GitHub Pages serves `main` → `/docs`.

## One-minute introduction

[Watch the 60-second GIF](intro.gif). It has 12 five-second scenes, with a problem, search footprints, a changed wall, an open-grid comparison, a no-route case and the live URL. The illustration is generated from the real Python solver; it is not a screen recording. It is silent and repeats. The page links it separately so the animation does not load until requested.

English is the primary demo language; the page includes a Persian guide. MIT licensed. Development used AI coding assistance. Browser checks do not replace testing on physical phones or an independent outside-user review.
