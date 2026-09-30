# Engineering & science coverage map (DOE preparation)

Dated 2026-09-30. Requested by the author: calculus, statics, dynamics, strength of materials, stress chain, hydraulics, fluid dynamics, thermodynamics, electric fields, circuits, nature and property of materials, particle and aggregate structure to properties, beltdraulic vs hydraulic, plus optics, heat transfer, soil mechanics, electronics. Target: the author's DOE-received zeolite pore-selectivity grant (section 3; program identity not in the repository). No DOE-facing document exists in the repository; the closest are HVEH/ResilientNJ_HVEH_Grant_Narrative.pages (state programme, not read here, .pages format) and Orthogenesis/NASA.md.

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

## 3. Update 2026-09-30: the target is the author's zeolite pore-selectivity grant

The author states that the DOE is running a job-type apprenticeship (levels G-9 to G-5, science and engineering) that he does not qualify for as a self-taught researcher, and that the DOE has received his grant on zeolite pore selectivity. So the map is re-ordered around that grant, not around a general engineering curriculum. Recorded as stated by the author; the program's rules, its exact name and whether the level range means federal GS grades were **not** checked here.

What the corpus already holds on zeolites: `ch18-zeolite-noncommutativity.html` (MFI/ZSM-5, apertures about 5.3 x 5.6 and 5.1 x 5.5 angstrom, as the page states them), `ch20-saf-noncommutativity.html` (pore size and acid-site density controlling dehydration and oligomerization), `ch-catgt-zeolite.html`, `book6/wp53-facet-as-gate.html` (a different material, iron oxide), and the patent-side tracks (B-MCM-22, operator-order index). It holds **no** page on adsorption isotherms, diffusion in confinement, or a pore-selectivity calculation: "Langmuir", "Knudsen" and "Fickian" occur 0 times, "diffusivity" twice, "adsorption isotherm" once, "shape selectivity" on about 10 pages (as a phrase, not as a derivation).

Re-ranked by what a pore-selectivity proposal needs (the author's list, in this order):

1. **Nature and property of materials; particle and aggregate structure to properties.** Framework topology (MFI, MCM-22), aperture geometry, crystal versus aggregate (external surface, intercrystalline pores). Existing: ch18, book4 lattice chapters ch16 to ch20.
2. **Thermodynamics.** Adsorption equilibrium: Henry regime, Langmuir, isosteric heat, selectivity as a ratio of equilibrium constants. Gibbs/Clapeyron page exists (book7/ch-clapeyron-gibbs.html) but is not about adsorption.
3. **Fluid dynamics and hydraulics, at the pore scale.** Knudsen versus configurational diffusion, Fick's law, Thiele modulus for intracrystalline transport; then bed-scale flow and pressure drop.
4. **Heat transfer.** Adsorption and reaction exotherm in a pellet, intraparticle temperature rise.
5. **Electric fields.** Framework and cation electrostatics acting on polar or quadrupolar guests (CO2, N2). Maxwell/Faraday pages exist but are not about this.
6. **Calculus**, as the language for 2 to 4; **strength of materials, statics, stress chain, dynamics** matter only at the reactor and pellet-strength end (crush strength, bed load); **soil mechanics, optics, electronics, circuits** are not needed for this grant and can wait; **beltdraulic** is undefined (below).

First scripts to write (R24, before prose), each re-derivable and each stating its source:
- aperture against kinetic diameter for a small set of guest molecules, from tabulated literature values (source to be named on the page; I will not use a value I have not read);
- Henry and Langmuir selectivity from given equilibrium constants;
- Arrhenius/Fick: diffusivity ratio from two activation energies, and the Thiele modulus.

## 4. Open (R9, left to the author)

- **Beltdraulic** is not in the repository. Please define it before I write about it.
- **Which DOE program received the grant**, its identifier, and what the proposal already states (aims, guests, framework). The proposal text is not in the repository; sharing it lets the primer match it instead of guessing.
- **Eligibility** for the apprenticeship: not assessed here; I have not read the program's requirements.
- **HVEH power claim:** 10-20 kW per module is a MODEL figure on the page; the map does not endorse it. It is off the zeolite path.
- **Hooks** in section 2 are proposals, not proved; the "standard" ones are textbook facts and can be cited, the rest are conjectures.
- ResilientNJ_HVEH_Grant_Narrative.pages was not opened.
