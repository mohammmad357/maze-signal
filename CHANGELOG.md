# Changelog

## v1.1.0 — 2026-10-11

### Browser learning release
- Added a free interactive GitHub Pages demo with shared weighted maps, Dijkstra/A*, animation controls and explicit cost/move/expanded metrics.
- Verified JavaScript against 505 Python/C reference maps, with 1010 algorithm comparisons and a dedicated CI workflow.
- Added a silent 60-second tour and an illustrated English/Persian walkthrough explaining 140 versus 23 expansions and why this is not a runtime ratio.
- Added public GitHub issue forms for three-question feedback, reproducible bugs and return-use reports; the demo now links directly to them.
- Clarified terrain painting: Weight is enabled only for Terrain weight, with a nearby hint. Previously it appeared active for tools that ignored it.
- Preserved each panel's keyboard tab entry cell across renders. Previously every render moved the tab entry point back to cell zero.

The review was maintainer-side. Outside first-use review, physical phone testing and actual user-retention evidence are still pending. No user rating, adoption count or donated amount is claimed.

Demo: https://mohammmad357.github.io/maze-signal/
Walkthrough: https://mohammmad357.github.io/maze-signal/learn.html
Feedback: https://mohammmad357.github.io/maze-signal/feedback.html

Reproduce: `node docs/verify.cjs`. Counts in the walkthrough refer to the v1.1.0 solver, four-neighbor movement, entry costs 1–9 and the documented tie rule. Animation is presentation, not benchmarking. See `docs/VERIFICATION.md` and `results/RESULTS.md` for test conditions and separate Python/C timing data.

## v1.0.0 — 2026-10-11
- Python/C11 Dijkstra and A*, seeded correctness checks, reproducible machine-specific benchmarks, bilingual documentation and MIT license.
