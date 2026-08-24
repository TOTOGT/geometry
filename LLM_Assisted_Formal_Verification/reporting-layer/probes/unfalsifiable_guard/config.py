"""dm3 canonical constants.

The stability radius EPSILON0 is derived from the maximum Lyapunov exponent
and the Hessian bound:

    EPSILON0 = abs(MU_MAX) / (2 * (1 + H))

With MU_MAX = -2.0 and H = 1.0 this gives 2/(2*2) = 1/3.
EPSILON0 is load-bearing: it is cited across the corpus.
"""

MU_MAX = -2.0
H = 1.0

EPSILON0 = 1/3
