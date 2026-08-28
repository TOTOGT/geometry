#!/usr/bin/env python3
"""textual_conclusion_scan_fixtures.py — specimens that prove the instrument fires.

CONVENTIONS.md §2: a scan that has never rejected anything is not known to work.
Each specimen names the class it must produce; the control must produce none.
Run before the scan\'s verdict is read, not after:

    python3 tools/textual_conclusion_scan.py --selftest

The last two specimens are regressions from real output. `ascribed_reflexive`
is why type ascriptions are normalised — `(2 : Nat) = 2` was not recognised as
`x = x` until they were. `ctor_field_true` is why `True` inside an anonymous
constructor is excluded — `R ⟨Real.sqrt 15, 2, 150000, True⟩` was flagged
TRUE-TAILED on 2026-08-28, and that flag was wrong.
"""

CASES = [
    ('theorem a : True := by trivial\n', 'a', 'VACUOUS'),
    ('theorem g : ∃ (_ : Prop), True := ⟨True, trivial⟩\n', 'g', 'TRUE-TAILED'),
    ('theorem h2 (C : Nat) : 0 < C ∧ True := by simp\n', 'h2', 'TRUE-TAILED'),
    ('theorem b : (2:Nat) = 2 := rfl\n', 'b', 'REFLEXIVE'),
    ('theorem c : (1:Nat)/3 < 4/5 := by norm_num\n', 'c', 'NUMERIC-ONLY'),
    ('theorem d (n : Nat) : n + 0 = n := by simp\n', 'd', None),
    ('theorem e (n : Nat) : (2:Nat) = 2 := rfl\n', 'e', 'IDLE-BINDER'),
    ('theorem f (x : Nat) (h : 0 < x) : 0 < x := h\n', 'f', 'IDLE-BINDER'),
    # regression, 2026-08-28: `(2 : Nat) = 2` was not seen as x = x until type
    # ascriptions were normalised away.
    ('theorem ascribed_reflexive : (2 : Nat) = 2 := rfl\n',
     'ascribed_reflexive', 'REFLEXIVE'),
    # regression, 2026-08-28: `True` as a structure field value is not a vacuous
    # conjunct. This flagged TRUE-TAILED in geometry and the flag was wrong.
    ('theorem ctor_field_true (n : Nat) : R ⟨1, 2, True⟩ n = n := rfl\n',
     'ctor_field_true', None),
]
