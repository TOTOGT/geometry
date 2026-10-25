# Pre-registration 2 (supersedes one clause of prereg-rh-criteria.md)

Date: 2026-10-25 (US Eastern). Written after the first run of T1 and before any rerun.

What happened. In the first run of T1 the Robin control (right side multiplied by 0.99) reported
0 violations in n <= 10**7. The tightest relative margin of Robin's inequality in that range is
1.418e-2 (n = 10080), so a 1% reduction cannot be detected there. As registered, that control is
VACUOUS, and the first T1 result is not to be used. This is a fault in the control I chose, not a
finding about Robin's inequality.

Change. The Robin control factor is 0.98 (a 2% reduction, larger than the observed tightest margin).
Everything else in prereg-rh-criteria.md stands: the Lagarias control (x0.95) behaved as registered
(25 violations, first at n = 12). Outcome rule unchanged: PASS needs both controls to fire and no
violation of either real inequality.
