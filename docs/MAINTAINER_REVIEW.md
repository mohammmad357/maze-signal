# Maintainer review for v1.1.0 — 2026-10-11

This is an internal first-use review, not feedback from independent users.

| Obstacle | Before | After | Retest |
|---|---|---|---|
| Feedback required guessing what to write | Footer opened the generic issue list | Feedback page links three-question, reproducible-bug and return-use forms | Open all three GitHub issue forms without submitting a fake report |
| Weight control appeared to apply to any paint tool | Weight stayed enabled for Wall, Start and Goal although ignored | Disabled except for Terrain weight; nearby hint explains when it applies | Wall → weight disabled; Terrain weight → enabled; paint 2, run trap, both cost 9 |
| Keyboard entry point forgot the last focused cell | Every render set only cell zero to tabindex=0 | Each panel remembers its focused cell and resets focus index when changing examples | Arrow to a cell, paint, leave and re-enter with Tab; one tab stop per panel and last cell retained |

Search semantics and Python/C benchmarks are unchanged. These three obstacles were selected by the maintainer for first-use clarity and accessibility; no frequency or external severity score is claimed.
