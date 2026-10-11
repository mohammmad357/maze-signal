# Contributing to maze-signal

Thanks for helping make this weighted pathfinding project easier to inspect and reproduce.
Small documentation fixes and reproducible bug reports are useful contributions.

## Before changing behavior

Read the README, input/model contract and measured-results report. Open an issue for a
substantial behavior or format change so the scope can be discussed first. These are
educational engineering projects; production readiness is not established.

## Report a bug

Include: Map dimensions and cells, selected algorithm, expected minimum cost, actual JSON output and Python/compiler versions.

Use the smallest synthetic input that reproduces the problem. State expected and actual
behavior, and include the exact command and commit/version. Screenshots may supplement
text output, but should not replace a reproducible command.

## Development checks

Follow the README build instructions for your OS, then run:

```sh
python -m unittest discover -s tests -v
```

Keep C11 builds warning-free using the flags in the README. Linux CI also runs address
and undefined-behavior sanitizers. A documentation-only change needs a link/command
review; a behavior change needs a regression check that exercises the changed behavior.

Example entry point (run from the repository root):

```sh
python python/solver.py maps/trap.txt astar
```

## Evidence required for behavior changes

A cost-preserving change must keep optimality and deterministic tie behavior, or explicitly document and test a changed contract. Compare with the independent reference and verify path adjacency and cost.

For performance claims, retain the raw samples, workload, environment, measurement
boundary and reproduction command. Do not generalize one workload into a universal
speedup. Avoid committing large generated files unless they are an agreed reference.

## Starter ideas

### Compare tie policies

Run two explicitly defined heap tie policies on identical seeded maps; report path cost and expanded nodes separately from timings.

### Improve first-use examples

Add a tiny weighted map with a hand-calculated optimum, plus an unreachable map and expected JSON behavior.

These are suggestions, not assigned tasks or promised roadmap commitments. Check open
issues before starting. A pull request should explain the problem, change, validation
and limitations. Keep unrelated edits separate and respond respectfully to review.

AI-assisted contributions are welcome when the author checks the code and can explain
the implementation and evidence. Contributions are made under this repository's MIT license.
