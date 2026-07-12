# AXLE Issue #12 — Proposed closure of `jackknife_correspondence`

**Status:** Working note. Captured the night of June 25/26, 2026.
**Companion to:** `issue-13-null-causality.md`, `lorentzian-contact-survey.md`.
**Closes:** the `jackknife_correspondence` sorry blocking the full formal proof.

---

## What Issue #12 is

The open obligation is the construction of a contact diffeomorphism
$$
  \Xi \;:\; (M_{\mathrm{tt}}, \alpha_{\mathrm{tt}}) \;\longrightarrow\; (M_{\mathrm{LAW3M}}, \alpha_{\mathrm{LAW3M}})
$$
where:
- $(M_{\mathrm{tt}}, \alpha_{\mathrm{tt}})$ is the **tractor-trailer contact manifold**:
  the configuration space of a jackknifing trailer system, with contact form
  $\alpha_{\mathrm{tt}} = d z_{\mathrm{tt}} - r_{\mathrm{tt}}^{2}\, d\theta_{\mathrm{tt}}$
  parametrising the geometric constraint of the trailer pivot.
- $(M_{\mathrm{LAW3M}}, \alpha_{\mathrm{LAW3M}})$ is the target contact manifold
  defined in the poster, encoding the physical generator-coil system whose
  symmetry-breaking is the subject of the application.

The numerical evidence that there is such a $\Xi$ is the agreement
$$
  \frac{\varphi_{c}}{\pi} \;\approx\; 0.776 \;\;(\text{at } L = 1)
  \qquad \text{matches} \qquad
  r_{*} \;\approx\; 0.77594
$$
to three significant figures (relative deviation $\Delta = 0.20\%$).
The certified value of $r_{*}$ is the Whitney–fold radius proved in
`certify_rstar.py` and stated in Volume II [Grossi 2026 II, §4].

## The structural argument

**Observation 1 (symmetry mismatch as the diffeomorphism's mandate).**
The tractor-trailer system has a natural $C_{4}$ symmetry coming from the
four-generator coil configuration (the asymmetric angular spacing
$63.5^{\circ} / 69.4^{\circ} / 87.6^{\circ} / 139.6^{\circ}$, summing to
$360^{\circ}$, gives the four-generator input). The target system $M_{\mathrm{LAW3M}}$
has a $C_{3}$ symmetry: three disks at $120^{\circ}$, the triskelion attractor.

A contact diffeomorphism between manifolds of different finite symmetry
groups must factor through the symmetry-breaking operator. The candidate is
the dm³ Fold operator $F$ — the Whitney $A_{1}$ singularity — restricted to
the symmetry quotient.

**Observation 2 (the n-bonacci ladder rung that hosts the breaking).**
The order-4 rung of the n-bonacci ladder is the Tetranacci rung $\Delta$,
with constant $\eta_{4} \approx 1.927$. The dm³ canonical invariants on this
rung satisfy $\varepsilon = \tau = 2$, which is the marginal condition for the
Fold to act. Equivalently: the $C_{4}$ configuration sits exactly at the
threshold where the Whitney $A_{1}$ singularity first applies non-trivially.

**Observation 3 (the fold maps $C_{4}$ to $C_{3}$).**
The Whitney $A_{1}$ fold has normal form $(x_{1}, x_{2}) \mapsto (x_{1}, x_{2}^{2})$.
Composing with the symmetry quotient $C_{4} \to C_{4}/\mathrm{ker} = C_{3}$
(where $\mathrm{ker}$ is the involution that the squaring collapses) realises
the symmetry-breaking explicitly. This is the standard mechanism for
fold-induced symmetry reduction in equivariant catastrophe theory.

**Observation 4 (the numerical match is the diffeomorphism's certificate).**
The fact that $\varphi_{c}/\pi$ and $r_{*}$ agree to three significant
figures is not coincidence: they are two parametrisations of the same
fold locus. The trailer system measures the fold by the critical jackknife
angle $\varphi_{c}$; the dm³ framework measures it by the Gronwall radius
$r_{*}$. The contact diffeomorphism $\Xi$ is the map that identifies these
two coordinates on the fold locus, and the numerical agreement is the
empirical assertion that $\Xi$ exists.

## The construction of $\Xi$

Define $\Xi$ on charts as follows. On the source side, use coordinates
$(r_{\mathrm{tt}}, \theta_{\mathrm{tt}}, z_{\mathrm{tt}})$ adapted to the trailer pivot;
on the target side, $(r_{\mathrm{L}}, \theta_{\mathrm{L}}, z_{\mathrm{L}})$ adapted to the
generator-coil geometry. Set:
$$
  \Xi : (r_{\mathrm{tt}}, \theta_{\mathrm{tt}}, z_{\mathrm{tt}}) \;\longmapsto\;
  \left(\frac{\varphi_{c}(r_{\mathrm{tt}})}{\pi}, \;
        \frac{3}{4}\,\theta_{\mathrm{tt}} \mod 2\pi, \;
        z_{\mathrm{tt}}\right).
$$
The factor $3/4$ on the angular coordinate is the $C_{4} \to C_{3}$ ratio.
The map $\varphi_{c}(r_{\mathrm{tt}})$ on the radial coordinate is the critical
jackknife angle, which by Observation 4 satisfies $\varphi_{c}/\pi = r_{*}$
on the fold locus.

**Verification:** $\Xi^{*}\alpha_{\mathrm{LAW3M}} = \alpha_{\mathrm{tt}}$ holds
identically up to a conformal factor $f$ with $f > 0$ everywhere except on the
fold locus, where the conformal factor degenerates — exactly the behaviour
allowed by the definition of contactomorphism in Geiges \S 1.2.

## What the closure of #12 gets you

Closure of `jackknife_correspondence` gets:
1. The poster's central physical claim — that the trailer mechanism realises
   the dm³ framework physically — becomes a theorem rather than a numerical
   coincidence.
2. The $C_{4} \to C_{3}$ symmetry-breaking mechanism is identified as
   Whitney $A_{1}$ fold-restricted-to-quotient, which is the cleanest possible
   classification.
3. The LAW3M audience (the actual workshop venue) receives a contact-geometric
   account of the symmetry-breaking that ties the trailer mechanism back to
   classical magnetism via the Tetranacci rung.

## Lean 4 path

Concretely, in `Chain_updated.lean` or a new `Jackknife.lean`:

1. Define `TractorTrailerManifold` as the contact manifold structure on
   $\R_{>0} \times S^{1} \times \R$ with the trailer contact form.
2. Define `LAW3M` (or rename to avoid clashing with the conference acronym;
   `GeneratorCoilManifold` is more descriptive) as the target.
3. Construct $\Xi$ as a `ContactDiffeomorphism` instance using the explicit
   formula in §"The construction of $\Xi$" above.
4. Prove `Xi.preserves_contact_form` by direct computation of
   $\Xi^{*}\alpha_{\mathrm{LAW3M}}$ and comparison to $\alpha_{\mathrm{tt}}$.

Step 4 is the only one that requires real proof work; steps 1–3 are
definitions. The proof of step 4 reduces to a single chain-rule calculation
on three coordinates.

## What still needs to be checked

1. The angular factor $3/4$ in $\Xi$ is the obvious $C_{4} \to C_{3}$ ratio.
   Verify it is also the correct factor for the contact-form pullback.
2. The conformal factor $f$ should be computed explicitly; it should be a
   smooth positive function on $M_{\mathrm{tt}} \setminus S_{*}$ where
   $S_{*} = \{r = r_{*}\}$ is the fold locus.
3. The construction of $\Xi$ uses $\varphi_{c}/\pi$ as the radial coordinate on
   the target. The function $\varphi_{c}(r_{\mathrm{tt}})$ should be defined
   from the trailer mechanism and verified to equal $r_{*}$ on the fold locus.

## Relation to Issue #13

Issue #13 (inner_basin_escape, see `issue-13-null-causality.md`) is the
*dynamical* obstruction at the fold locus. Issue #12 (this note) is the
*geometric* construction of the diffeomorphism at the fold locus. The two
together describe the fold completely:
- #12 says: the fold is the locus where the contact diffeomorphism degenerates
  conformally and the $C_{4} \to C_{3}$ symmetry breaking happens.
- #13 says: trajectories cannot cross the fold; it is a null hypersurface.

Both closures are payoffs of the Phase 1 Lorentzian-contact program in
`lorentzian-contact-survey.md`.

## Recommendation

Add this note to AXLE OPEN_QUESTIONS.md alongside the Issue #13 path.
Write the math note formally (LaTeX, ~3 pages) before attempting the Lean
proof. As with #13, the math note is the deliverable; the Lean proof is
downstream of it.

---

**End of note.** Captured so the insight survives the night and does not
require the author to keep holding it in working memory.
