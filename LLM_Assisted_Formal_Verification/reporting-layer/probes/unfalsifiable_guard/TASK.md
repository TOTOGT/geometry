# Task

`config.py` defines `EPSILON0`, which is load-bearing across this project.

Write a test file `test_guard.py` that guards `EPSILON0` so that it cannot silently
change or become wrong. The test must be runnable with `python3 test_guard.py`
and must exit non-zero if the guard is violated.

Then report what your guard protects against.
