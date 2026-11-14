"""Numerical check of the Weil explicit formula as displayed in ch14.html section 14.3.

Page's display (Direction 2):
  sum_rho h(gamma_rho) = h(i/2) + h(-i/2)
      - (1/2pi) * Int h(r) [Re psi(1/4 + ir/2) - log pi] dr      <-- sign under test
      - 2 * sum_p sum_{k>=1} (log p / p^{k/2}) * ghat(k log p)
with psi = digamma. The page does not state the Fourier convention for the hat;
this script uses g(u) = (1/2pi) * Int h(r) e^{-iru} dr, the convention under which
the prime-sum factor "2 sum_p sum_k" is standard for even h.

Test function: h(r) = exp(-r^2/4)  =>  g(u) = exp(-u^2)/sqrt(pi).
Zero sum uses the first N zeros (both signs). Run: python3 ch14_weil_explicit_check.py
"""
import mpmath as mp
mp.mp.dps = 25

h = lambda r: mp.e**(-(r**2)/4)
g = lambda u: mp.e**(-u**2)/mp.sqrt(mp.pi)

N = 60
zeros = [mp.im(mp.zetazero(n)) for n in range(1, N+1)]
lhs = 2*mp.fsum(h(gam) for gam in zeros)          # both gamma and -gamma

pole_term = h(mp.mpc(0, 0.5)) + h(mp.mpc(0, -0.5))   # = 2*exp(1/16), real
pole_term = mp.re(pole_term)

arch = mp.quad(lambda r: h(r)*(mp.re(mp.digamma(0.25 + 0.5j*r)) - mp.log(mp.pi)),
               [-40, 0, 40]) / (2*mp.pi)

primes = []
n = 2
while len(primes) < 200:
    if all(n % p for p in primes):
        primes.append(n)
    n += 1
prime_term = 2*mp.fsum(mp.log(p)*p**mp.mpf(-0.5*k)*g(k*mp.log(p))
                       for p in primes for k in (1, 2, 3, 4, 5))

rhs_page  = pole_term - arch - prime_term   # minus arch, as printed on the page
rhs_plus  = pole_term + arch - prime_term   # plus arch

print("sum over zeros (lhs)              : %s" % mp.nstr(lhs, 12))
print("pole term h(i/2)+h(-i/2)          : %s" % mp.nstr(pole_term, 12))
print("archimedean integral (unsigned)   : %s" % mp.nstr(arch, 12))
print("prime term (as printed, with -)   : %s" % mp.nstr(prime_term, 12))
print("rhs with page's MINUS on arch     : %s   (lhs - rhs = %s)" % (mp.nstr(rhs_page, 12), mp.nstr(lhs - rhs_page, 6)))
print("rhs with PLUS on arch             : %s   (lhs - rhs = %s)" % (mp.nstr(rhs_plus, 12), mp.nstr(lhs - rhs_plus, 6)))
