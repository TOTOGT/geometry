# Proposed replacement: book7/ch-hawking.html, Section I (draft, not applied)

Source of the hypotheses: Hawking and Ellis (1973), section 8.2, Theorems 1 and 2. Check the wording against the book before applying. Apply to both the PT and EN blocks; the PT text below is a draft for the author to correct.

## EN: replace the "Hawking-Penrose Condition" block and Theorem H.1

**Penrose's theorem (1965).** A space-time cannot be null geodesically complete if (1) R_ab K^a K^b >= 0 for every null vector K, (2) it has a non-compact Cauchy surface, and (3) it contains a closed trapped surface.

**Hawking-Penrose theorem (1970).** A space-time is not timelike and null geodesically complete if (1) R_ab K^a K^b >= 0 for every non-spacelike K, (2) the generic condition holds, (3) there are no closed timelike curves, and (4) there is a compact achronal set without edge, a closed trapped surface, or a point from which the null geodesics begin to reconverge.

Both proofs run through focusing along null geodesics (conjugate points) and a contradiction with compactness. They conclude that some inextendible geodesic is incomplete. They do not produce a point, a location or a unique object.

**Reading H.1 (the author's identification, not a theorem).** One can read the energy condition as playing the role of K and the trapped surface as playing the role of a contraction condition in the chain G = U o F o K o C. No contraction mapping is defined here, so no fixed-point theorem is invoked and no uniqueness is claimed. Whether such a map exists on a contact manifold is open.

## EN: other edits
- "Hawking was 29 when he proved this": delete, or replace with the verified age after checking.
- Lean-style comment block: "3 structural identifications verified" -> "3 structural identifications stated (no Lean file yet)".
- Relabel "Theorem H.2" and "Theorem H.3" as "Reading H.2" and "Reading H.3".
- Reith quotation: give the primary source or remove.
- "one of nine open sorrys": reconcile with Book V chapter 3 against the registry.

## PT: draft
**Teorema de Penrose (1965).** Um espaco-tempo nao pode ser nulo-geodesicamente completo se (1) R_ab K^a K^b >= 0 para todo vetor nulo K, (2) tem uma superficie de Cauchy nao compacta e (3) contem uma superficie aprisionada fechada.
**Teorema de Hawking-Penrose (1970).** Um espaco-tempo nao e tipo-tempo e nulo-geodesicamente completo se (1) R_ab K^a K^b >= 0 para todo K nao tipo-espaco, (2) vale a condicao generica, (3) nao ha curvas tipo-tempo fechadas e (4) existe um conjunto acronal compacto sem borda, uma superficie aprisionada fechada ou um ponto de onde as geodesicas nulas comecam a reconvergir.
**Leitura H.1 (identificacao do autor, nao um teorema).** Pode-se ler a condicao de energia como K e a superficie aprisionada como condicao de contracao na cadeia G = U o F o K o C. Nenhuma contracao e definida aqui; nao se invoca ponto fixo nem se afirma unicidade.
