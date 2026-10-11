# When 4 = 2 + 2 was missing from a search

2026-10-11 · An early week-ten content task · AI-assisted reproduction and proposed fix.

The function `goldbach()` in TheAlgorithms/Python searched for two prime numbers whose sum is an even input. On upstream source `215c1f0710f610aaf5ebaeab04edacec3f5308cd`, inputs **4** and **6** raised `AssertionError` instead of returning `[2, 2]` and `[3, 3]`.

The inner loop began at `j = i + 1`: it could inspect different primes but never pair a prime with itself. Changing the initial index to `j = i` includes repeated-prime pairs while preserving all subsequent pairs. The proposed change is one line in one algorithm file.

| Input | Before | Proposed fix |
|---|---|---|
| 4 | AssertionError | [2, 2] |
| 6 | AssertionError | [3, 3] |
| 8 | [3, 5] | [3, 5] |

The scoped check covered **249 even inputs from 4 through 500**. For each returned pair, an independent trial-division oracle checked primality and the sum; **19 existing related doctests passed**.

**Test boundary matters:** Python 3.13.7 could not import the entire module because an unrelated dependency uses newer exception syntax. The harness executed the unchanged AST bodies of four real functions (`goldbach`, `get_prime_numbers`, `is_prime`, `is_even`) with their math dependency. It did not replace them with mocks. Full upstream testing and linting remain pending, including the repository's requested interpreter checks.

The proposal is [draft PR #15555](https://github.com/TheAlgorithms/Python/pull/15555), head `aa7558f378a7a714a3792bc372533eeed31aa05d`. At the 2026-10-11 snapshot it was open, unmerged, with no review comments. This is a submitted proposed fix, not an accepted upstream contribution or user feedback story.

**Engineering lesson:** when an algorithm enumerates pairs, explicitly decide whether equal elements are legal. Test the smallest valid inputs before measuring performance. Neither these finite checks nor this patch prove Goldbach's conjecture.

**فارسی:** شروع حلقه از `i+1` زوج‌های تکراری مثل ۲+۲ و ۳+۳ را حذف می‌کرد. اصلاح پیشنهادی از `i` شروع می‌شود. آزمون محدود اجرا شده و PR هنوز پیش‌نویس است؛ پذیرش و بررسی کامل در اختیار نگهدارندگان پروژه است.
