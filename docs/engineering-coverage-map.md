# Engineering & science coverage map (DOE preparation)

Dated 2026-09-30. Requested by the author: calculus, statics, dynamics, strength of materials, stress chain, hydraulics, fluid dynamics, thermodynamics, electric fields, circuits, nature and property of materials, particle and aggregate structure to properties, beltdraulic vs hydraulic, plus optics, heat transfer, soil mechanics, electronics. Target DOE program: **not decided** (recorded OPEN). No DOE-facing document exists in the repository; the closest are HVEH/ResilientNJ_HVEH_Grant_Narrative.pages (state programme, not read here, .pages format) and Orthogenesis/NASA.md.

## 1. What the repository contains now (recomputed)

Produced by `docs/engineering-coverage-verify.py`: strict textbook terms only (not words like "entropy" alone), prose pages only. A hit is a term appearing on a page, not a treatment of the topic. Low counts mean the topic is a gap; high counts only mean the words occur.

| topic | pages | hits | top pages |
|---|---|---|---|
| Differential & integral calculus | 4 | 8 | book6/wp54-quantum-weave.html (4); book18/ch04-euler-in-the-middle.html (2); book7/ch-maxwell.html (1) |
| Statics | 3 | 6 | book8/ch8-8-chandrasekhar.html (3); book6/wp38-positional-dominance.html (2); book8/ch8-8b-brown-dwarfs.html (1) |
| Dynamics | 28 | 59 | book7/ch-kovalevskaya.html (7); book7/ch-euler.html (6); chCajueiro.html (5) |
| Strength of materials | 1 | 1 | book7/ch-euler.html (1) |
| Stress chain | 0 | 0 |  |
| Hydraulics | 13 | 40 | HVEH/ch-build-2river.html (10); book4/ch-build-2river.html (10); HVEH/chHALO.html (4) |
| Fluid dynamics | 54 | 165 | ch1-seed.html (34); ch01-one-equation.html (23); book7/ch-ada.html (14) |
| Thermodynamics | 69 | 241 | ch-energy-entropy.html (30); book7/ch-clapeyron-gibbs.html (24); book4/ch21-the-closing-field.html (21) |
| Electric fields | 36 | 255 | book7/ch-faraday.html (122); book7/ch-maxwell.html (36); book4/ch-faraday.html (18) |
| Circuits | 3 | 10 | book7/ch-the-map-on-page-ten.html (5); book7/ch-van-der-pol.html (3); book7/ch-sophie-germain.html (2) |
| Nature & property of materials | 50 | 151 | chT-tubulin.html (13); chLambda-polylaminin.html (11); ch-tatiana.html (7) |
| Particle/aggregate to properties | 10 | 74 | book6/wp92-a-cusp-that-is-real-and-a-fold-that-was-not.html (35); book6/wp93-the-triangle-not-the-bubble.html (18); book4/ch-lace-bootstrap.html (6) |
| Beltdraulic vs hydraulic | 0 | 0 |  |
| Optics | 25 | 55 | book4/ch19-acoustic-lattice.html (11); chSigma-pentanacci.html (6); book8/ch-angstrom-topogenesis.html (4) |
| Heat transfer | 6 | 28 | book6/ch-elliptic-poisson-foundations.html (10); book6/ch-wave-equation.html (10); book6/ch-box-domain-lift.html (4) |
| Soil mechanics | 17 | 26 | ch3-circadian.html (3); ch1.html (3); ch2.html (3) |
| Electronics | 9 | 14 | chPsi-quantum-mind.html (3); book6/wp98-a-measurement-science-without-a-unit.html (3); book7/ch-van-der-pol.html (2) |

Reading the table honestly: only **fluid dynamics, thermodynamics, electric fields, hydraulics (one build spec) and crystal-lattice materials** have chapters that treat the subject. **Calculus** (4 pages) appears as a tool, not as a taught chapter. **Statics, strength of materials, stress chain, circuits, heat transfer, soil mechanics, electronics, beltdraulic** are gaps: 0 to 9 pages, mostly incidental (the soil-mechanics hits on ch1/ch2/ch3 are most likely the word "consolidation" in the memory chapters, unread). Fluid-dynamics counts include the word "circulation", which the corpus also uses in a non-fluid sense, so treat 54 pages as an upper bound.

## 2. Topic map

Status: WRITTEN = a page treats it; PARTIAL = related page, not the engineering treatment; GAP = nothing. "Hook" is a **proposal** for the D1 to D2 link, labelled CONJECTURE until a script or proof exists; it is not a claim.

| Topic | Status | Existing pages | Proposed hook (CONJECTURE) | First thing a script must re-derive |
|---|---|---|---|---|
| Differential & integral calculus | PARTIAL | book7/ch-feynman.html (tool), book7/ch-maxwell.html | Contact form alpha, d(alpha), Stokes as the bridge from first to second dimension | Stokes on a disc, symbolic and numeric |
| Statics | GAP | none | Equilibrium as a closed 1-form; force polygon closure | Truss by method of joints against a linear solve |
| Dynamics | PARTIAL | book7/ch-kovalevskaya.html, book7/ch-euler.html | Rigid-body flow as a contact/Hamiltonian flow | Euler top energy and angular-momentum conservation |
| Strength of materials | GAP | none | Stress tensor as a 2-form on the cross-section | Euler-Bernoulli deflection against closed form |
| Stress chain | GAP | none | Force chains as a graph over the lattice chapters | Force balance on a small granular contact network |
| Hydraulics | WRITTEN (one site) | HVEH/ch-build-2river.html, HVEH/case-belleville-second-river.html, HVEH/cfd/README.md | Vortex intake with threshold r*=0.776 (the page's MODEL) | Power P = rho g Q H eta against the stated 10-20 kW per module |
| Fluid dynamics | PARTIAL | ch1-seed.html, ch01-one-equation.html, book7/ch-ada.html | Circulation and vorticity as d of the velocity 1-form | Poiseuille and Bernoulli checks |
| Thermodynamics | WRITTEN | book7/ch-clapeyron-gibbs.html, ch-energy-entropy.html, book8/ch10-thermodynamics.html | Gibbs 1-form dU - T dS + p dV is a contact form (standard) | Maxwell relations symbolic |
| Electric fields | WRITTEN | book7/ch-maxwell.html, book7/ch-faraday.html, book4/ch-faraday.html | F = dA on a 2-manifold (standard) | Gauss law numerically on a point charge |
| Circuits | GAP | none | Kirchhoff laws as d^2 = 0 on a graph (standard cochain view) | Mesh analysis against nodal analysis |
| Nature & property of materials | PARTIAL | book4/ch16-crystal-lattice.html to ch20-defect-lattice.html, book6/ch-phase.html | Lattice symmetry group to elastic tensor | Cubic elastic constants from symmetry |
| Particle/aggregate to properties | PARTIAL | book6/wp92, wp93 | Packing and percolation thresholds | Site-percolation threshold by simulation |
| Beltdraulic vs hydraulic | GAP | none (0 hits for "beltdraulic") | **Undefined in the repository.** The author must define it (see section 4) | none until defined |
| Optics | PARTIAL | book4/ch19-acoustic-lattice.html, book7/wp59-dark-matter-lensing.html | Fermat as a variational principle; ray as a Legendrian curve | Snell from Fermat symbolic |
| Heat transfer | PARTIAL | book6/ch-elliptic-poisson-foundations.html, book6/ch-wave-equation.html | Heat equation as a contraction semigroup | 1D conduction against Fourier series |
| Soil mechanics | GAP | none | Effective stress and Mohr circle as a conic in the stress plane | Mohr-Coulomb failure envelope |
| Electronics | GAP | book7/ch-van-der-pol.html (oscillator only) | Diode as a nonlinear 1-port; van der Pol as its normal form | Shockley diode and small-signal model |

## 3. Suggested order for a DOE preparation

1. Decide the target program (SBIR/STTR, ARPA-E, Office of Science or EERE). The choice fixes which rows matter; the hydraulic, thermodynamic and materials rows are the ones with existing pages.
2. Build one verification script per row before any prose (R24), starting with the five WRITTEN rows, because DOE reviewers weigh a stated power or efficiency more than an unstated one.
3. Then write the GAP chapters as a short engineering primer with each equation checked, in the order statics, strength of materials, stress chain, soil mechanics (they share one stress tensor), then circuits and electronics, then heat transfer and optics.

## 4. Open (R9, left to the author)

- **Beltdraulic:** the term is not in the repository. Please define it (a belt-driven mechanical drive as opposed to a hydraulic drive? a belt-plus-hydraulic hybrid?) before I write anything about it.
- **DOE program** not chosen; no DOE narrative exists here.
- **HVEH power claim:** 10-20 kW per module is a MODEL figure on the page; the map does not endorse it.
- **Hooks** in section 2 are proposals, not proved; the "standard" ones are textbook facts and can be cited, the rest are conjectures.
- ResilientNJ_HVEH_Grant_Narrative.pages was not opened.
