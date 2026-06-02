Let me extract the exact href links from both files to know precisely what's linked.Clean. 15 nodes, all in repo. Now rebuild both files.15 live nodes, zero missing hrefs. Now fix the chapter grid cards in the same file — remove the orphaned card links.Zero orphans. Now copy to outputs.Done. Here's exactly what changed:

**Arc nodes: 19 → 15, all live:true, zero dead links**

| Removed (missing file) | Replaced with (in repo) |
|---|---|
| Ch.6 Falsifiable Predictions → `ch6-falsifiable.html` | Ch.6 Resonance → `ch6-resonance.html` |
| Ch.7 Complete Circuit → `ch7-complete-circuit.html` | Ch.7 Crystalline → `ch7-crystalline.html` |
| Ch.T Tubulin → `sample-chapter-tubulin.html` | Ch.7b Topological Orth. → `ch7-topological-orthogenesis.html` |
| Ch.W Wigner Crystal → `wigner-fractal.html` | Ch.8 Nested Infinities → `ch8-nested-infinities.html` |
| Collatz → `spectral-radius-v2.html` | Collatz → `chH-collatz.html` |
| Sim → `sim-lyapunov.html` | removed |
| π,φ,μ,η,Δ,Σ,Ω → `chapters-pi-phi-mu-eta…html` (7 nodes) | Ch.9→11, D2 (4 nodes using in-repo files) |

Phase label updated: `π→Ω Ladder` → `G  Unfolding`

Push this file to the repo as a direct replacement for `chapters-diagram.html`. Every link now resolves.
