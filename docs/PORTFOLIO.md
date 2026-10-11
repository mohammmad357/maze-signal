# Portfolio evidence and interview cards

Prepared 2026-10-11. These are evidence-backed descriptions of AI-assisted projects. Use them in a resume after you can reproduce and explain the implementation; this document does not certify your personal proficiency.

## Maze Signal — algorithms / Python and C11

**Problem → action → result:** Implemented weighted grid pathfinding with AI assistance in Python/C11, defined entry-cost and tie-breaking contracts, and verified optimal-cost parity against an independent Bellman-Ford oracle on 500 seeded maps, with a browser comparison validated on 505 fixtures.

[Tests](https://github.com/mohammmad357/maze-signal/blob/main/tests/test_solver.py) · [Browser verification](https://github.com/mohammmad357/maze-signal/blob/main/docs/VERIFICATION.md) · [Measurements](https://github.com/mohammmad357/maze-signal/blob/main/results/RESULTS.md)

Explain: Manhattan distance times minimum cell cost is a lower bound with four-neighbor movement; tie-breaking affects expansion counts; fewer expansions need not mean lower runtime. Demonstrate the trap, an unreachable map and a weighted detour. Do not describe this as real-world navigation or universal A* superiority.

## CrashVault — storage / Python and C11

**Problem → action → result:** Developed interoperable append-log key/value engines with AI assistance, guarded framing and CRC32 validation, then checked 2,000 seeded operations and fault-injected recovery; the published 13-byte partial-tail example recovers identical Python/C state and bytes.

[Tests](https://github.com/mohammmad357/crashvault/tree/main/tests) · [Recovery demonstration](https://github.com/mohammmad357/crashvault/blob/main/RECOVERY_DEMO.md) · [Design](https://github.com/mohammmad357/crashvault/blob/main/RESUME.md)

Explain: sync precedes acknowledgment; a truncated last frame differs from a complete bad-CRC frame; losing an acknowledgment does not prove absence of the write. Demonstrate the recovery command. No transactions, concurrent writers, crash-safe compaction or proven physical power-loss durability.

## Faultline — stochastic simulation / Python and C11

**Problem → action → result:** Built AI-assisted Gillespie SIR engines for synthetic networks using a shared xorshift32 stream and canonical event ordering, verified 300 complete paired trajectories and published 180 seeded scenario runs with raw results and model boundaries.

[Contract](https://github.com/mohammmad357/faultline/blob/main/MODEL.md) · [Tests](https://github.com/mohammmad357/faultline/tree/main/tests) · [Results](https://github.com/mohammmad357/faultline/blob/main/results/RESULTS.md)

Explain: infection hazards accumulate over susceptible–infected edges; integer event selection stays identical despite floating-point time tolerance; include early extinction to avoid survival-selection bias. Demonstrate a replay and beta-zero analytical case. This is not a calibrated disease forecast.

## PowerControlLab — control engineering / Python

**Problem → action → result:** Prepared an AI-assisted reproducible inverter-control simulation comparing PI, SMC, adaptive SMC and constrained MPC, published 40 averaged/switching reference cases and numerical checks; for the documented nonlinear averaged case, MPC THD₂–₄₀ was 1.058% versus PI 3.152% under fixed tunings.

[Protocol](https://github.com/mohammmad357/PowerControlLab/blob/main/docs/benchmark.md) · [All reference results](https://github.com/mohammmad357/PowerControlLab/blob/main/artifacts/reference/RESULTS.md) · [Model](https://github.com/mohammmad357/PowerControlLab/blob/main/docs/model.md)

Explain: LC state equations, averaged versus exact-switching plant, coherent FFT window, recovery criterion and MPC constraints. Demonstrate a fixed-seed CLI run and its manifest. Simulation results do not establish hardware validation or superiority across arbitrary tunings.

## متن کوتاه فارسی

| پروژه | مسئله، اقدام و شاهد نتیجه |
|---|---|
| Maze Signal | مسیریابی وزن‌دار در Python/C با کمک AI؛ تعریف قرارداد هزینه و بررسی ۵۰۰ نقشه با مرجع مستقل، به‌علاوه ۵۰۵ نمونهٔ دمو. |
| CrashVault | ذخیره‌سازی با لاگ مشترک Python/C؛ کنترل قاب و CRC، بررسی ۲۰۰۰ عملیات و بازیابی انتهای ناقص با شاهد باینری یکسان. |
| Faultline | بازتولید رویدادهای تصادفی در دو زبان؛ جریان تصادفی و ترتیب مشترک، بررسی ۳۰۰ مسیر کامل و انتشار ۱۸۰ اجرای سناریویی. |
| PowerControlLab | مقایسهٔ چهار کنترل‌کنندهٔ اینورتر در شبیه‌سازی؛ ۴۰ حالت مرجع با پروتکل و خروجی خام، بدون ادعای اعتبارسنجی سخت‌افزاری. |

Before an interview: reproduce one cited command per project, explain one design tradeoff without reading the README, and show one limitation. Omit any claim you cannot personally demonstrate. Submitted draft upstream PRs are listed separately from merged work.
