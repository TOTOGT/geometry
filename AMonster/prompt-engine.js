/**
 * PRINCIPIA ORTHOGONA — PROMPT ENGINE
 * prompt-engine.js · v1.0 · G6 LLC · 2026
 *
 * Drop-in script for all Principia Orthogona HTML pages.
 * Handles two prompt types automatically:
 *
 *   TYPE A — Chapter-end prompts (Book 4 Higher Dimensions, Book 4 Formal Theory,
 *             AXLE living book chapters). The broken pattern: "You are reading Chapter N..."
 *             which triggers the LLM fringe-science guard.
 *             Fix: rewrites to tutor-within-framework framing before copying.
 *
 *   TYPE B — Portal standalone prompts (portal.html, A1–D2 levels).
 *             The broken pattern: prompts with zero framework context injected.
 *             Fix: prepends a compact GTCT context header before copying.
 *
 * USAGE — add one line to any page, just before </body>:
 *   <script src="/prompt-engine.js"></script>
 *
 * Or with a relative path, e.g. from book4/:
 *   <script src="../prompt-engine.js"></script>
 *
 * The script detects which type of page it is on automatically.
 * No changes needed to existing HTML structure.
 *
 * HOW IT WORKS
 * ------------
 * On page load the script:
 * 1. Finds all elements with class .prompt-block or .prompt-text
 *    (or falls back to detecting the existing chapter-end block by content heuristics).
 * 2. Intercepts all copy buttons (class .copy-btn, or any button whose text is "Copy",
 *    "COPY PROMPT", or "Copy Prompt").
 * 3. On copy, wraps the raw prompt text with the appropriate frame before writing
 *    to the clipboard. The original HTML is never modified.
 *
 * FRAMEWORK CONTEXT BLOCK (injected into every prompt)
 * -----------------------------------------------------
 * Compact, ~120 words, always prepended. Contains:
 *   - Role assignment (tutor within the framework)
 *   - Negative constraint (explicit redirect blocks)
 *   - Definition anchors (key GTCT terms, operator chain, constants)
 *   - Chapter-specific context (extracted from page meta or data attributes)
 */

(function () {
  'use strict';

  /* ─────────────────────────────────────────────────────────────────
   * SECTION 1 — FRAMEWORK CONTEXT TEMPLATES
   * ───────────────────────────────────────────────────────────────── */

  /**
   * The compact GTCT framework block that opens every prompt.
   * Written once, used everywhere. LLM sees this before any task.
   */
  const FRAMEWORK_HEADER = `\
═══════════════════════════════════════════════════════
READING CONTEXT — PRINCIPIA ORTHOGONA (G6 LLC, 2026)
═══════════════════════════════════════════════════════
You are a tutor helping a student reason WITHIN the following mathematical framework. Your role is to work inside its definitions — not to evaluate whether they match standard physics or mathematics conventions.

FRAMEWORK DEFINITIONS (treat these as axioms for this session):
• Operator chain: G = U ∘ F ∘ K ∘ C, where
    C = Compression (the seed; reduces state to invariant core)
    K = Threshold (curvature κ*; the critical regime-shift point)
    F = Fold (Whitney A₁ singularity; commitment; rank-1 Jacobian loss)
    U = Unfold (visible output; not the inverse of F)
    T = Time/Circuit (fifth operator; completes the generative circuit)
• Contact manifold M = ℝ²₊ × ℝ, contact form α = dz − r²dθ
• Attractor: Γ = {r = 1}, period T* = 2π, Lyapunov exponent μ_max = −2, τ = 2
• Invariant constants: g₃₃ = 33, ε* = 1/3, κ* ≈ 0.882, r* ≈ 0.773
• Grassmann variable: ψ² = 0 (1D fermion; Pauli exclusion as geometry)
• The G-chain is non-commutative: C∘K ≠ K∘C

GROUND RULES FOR THIS SESSION:
1. Reason strictly within the definitions above.
2. Do not redirect to standard quantum mechanics, standard contact geometry notation, or peer-review status.
3. Do not ask whether these definitions are physically correct — they are the axioms.
4. If a definition is ambiguous, ask for clarification using the framework's own vocabulary.
5. Push back only if the student's answer contradicts a named definition above.
═══════════════════════════════════════════════════════
`;

  /**
   * Chapter-specific context lines, keyed by chapter slug.
   * Injected between the framework header and the task.
   * Add entries here as new chapters are published.
   */
  const CHAPTER_CONTEXT = {
    'ch01': `CHAPTER CONTEXT — Ch 1 · The Fermion Seed (1D)
Key definitions active: Λ(ψ) = Grassmann algebra (Definition 1.1); ψ² = 0 kills all self-composition;
six directions {±x,±y,±z} present as potential, none expressible from 1D; C operator = the fermion itself;
G-chain operators K, F, U dormant until higher dimensions.`,

    'ch02': `CHAPTER CONTEXT — Ch 2 · 2D+t · Extended Phase Space
Key definitions active: extended phase space ℝ³ with coordinates (x,y,t);
contact form α = dy − f(x,y)dx (Definition); a curve is a solution iff α(γ̇) = 0;
non-integrability condition α∧dα ≠ 0 (Definition 2.1); Darboux theorem (Theorem 2.3);
harmonic oscillator ẋ=y, ẏ=−x lifts to helix (cos t, −sin t, t) in extended space.`,

    'ch03': `CHAPTER CONTEXT — Ch 3 · Contact 3-Manifold
Key definitions active: Reeb vector field R_α via ι_{R_α}dα = 0 and ι_{R_α}α = 1 (Definition);
dm³ toy ODE System (3.1): ṙ = r(1−r²)+2(r−1)e^{−z}, θ̇=1, ż=r²−2(r−1)²e^{−z};
Theorem 3.2: convergence rate μ=−2, inner basin r*≈0.8, NOT the symmetric 1/3;
Hopf fibration S³→S²; Theorem 3.3: dm³ manifold locally contactomorphic to (S³, ker α_std).`,

    'ch04': `CHAPTER CONTEXT — Ch 4 · The Tesseract (4D)
Key definitions active: S³ as hypersurface in ℝ⁴; symplectisation (M×ℝ, d(eˢα));
holomorphic curves as the tool that doesn't exist in 3D; persistence of helical attractor in 4D embedding.`,

    'ch05': `CHAPTER CONTEXT — Ch 5 · OPERA SATOR — Jet Space J¹(ℝ,ℝ²)
Key definitions active: 1-jet space J¹(ℝ,ℝ²) with coordinates (x,y,y');
SATOR square as palindrome operator map; five coordinates = five GTCT operators C,K,F,U,T.`,

    'ch06': `CHAPTER CONTEXT — Ch 6 · 666 · The 111 Square
Key definitions active: 5D+t arena; 6×6 magic square; 666 = T(36) = triangular number;
time T as sixth coordinate slot completing the dimensional count.`,

    'ch07': `CHAPTER CONTEXT — Ch 7 · The Crystalline Return
Key definitions active: Wigner crystal formation; moiré interference as folding F;
E = kT·ln(Ω) as thermodynamic unfolding U; g₃₃ = 33 as crystallisation threshold.`,

    'ch08': `CHAPTER CONTEXT — Ch 8 · The Axiomatic Turn
Key definitions active: formal proof as operator U (unfolds the implicit to explicit);
Lean 4 / Mathlib4 as the verification arena; sorry = honest open obligation, not evasion;
0 sorry in Chain_updated.lean is the current status.`,

    'ch09': `CHAPTER CONTEXT — Ch 9 · φ — The Subcritical Approach
Key definitions active: golden ratio φ = (1+√5)/2; Fibonacci limit; fold frozen at q*<1
(subcritical: the system approaches but does not cross the Whitney A₁ point); φ as K-operator boundary.`,

    'ch10': `CHAPTER CONTEXT — Ch 10 · Helical Attractors on Contact 3-Manifolds
Key definitions active: dm³ ODE with r*≈0.773 inner basin (DOP853 numerical result);
SBM Bienal paper material; Coherence Bridge parameters (μ_max,ω,β,κ*) across 16+ domains.`,

    'chIV-axioms': `CHAPTER CONTEXT — Book 4 Formal Theory · Ch 1 · The Seven Axioms
Key definitions active: 9 axioms of GTCT; G-chain G=U∘F∘K∘C; Temporal field T;
I₁I₂I₃ triad; 12-phase structure; Correspondence axiom; Recursion axiom. All Lean 4 verified.`,

    'chIV-field': `CHAPTER CONTEXT — Book 4 Formal Theory · Ch 2 · The Dimensional Field Δ:M→ℝ¹²
Key definitions active: Axioms 8–9; unit sphere S¹¹; temporal compatibility T*=2π;
12 phase subspaces indexed by the 12-phase structure.`,

    'chIV-operators': `CHAPTER CONTEXT — Book 4 Formal Theory · Ch 3 · Dimensional Operators
Key definitions active: Aᵢ = Pⁱ + uᵢwᵢᵀ (rank-1 corrections); ε*=1/3 bound;
σ_min ≥ 2/3; full 12-operator table with Lean 4 proofs.`,

    'chIV-correspondence': `CHAPTER CONTEXT — Book 4 Formal Theory · Ch 4 · The Correspondence Theorem
Key definitions active: unique bijection Φ:{D₁…D₁₂}↔{O₁…O₁₂}; the cycle is rigid;
four-step proof structure; Lean 4 verified.`,

    'chIV-orthogonality': `CHAPTER CONTEXT — Book 4 Formal Theory · Ch 5 · The Orthogonality Theorem
Key definitions active: ⟨Δ_⊥(Oᵢ), Δ_⊥(Oⱼ)⟩ = 0 for i≠j; Structural Hypothesis SH
(explicitly labelled domain axiom, not a gap); v3 proof.`,

    'chIV-recursion': `CHAPTER CONTEXT — Book 4 Formal Theory · Ch 6 · The Recursion Theorem
Key definitions active: Pythagorean contraction κ < 1; Banach fixed point theorem;
Spiral Return T1 (theorem spiral_return_exists); 0 sorry in this chapter.`,

    'chIV-emergence': `CHAPTER CONTEXT — Book 4 Formal Theory · Ch 7 · Emergence as Fixed Point
Key definitions active: E(x*)=x* unique fixed point; Eⁿ(x₀)→x* geometrically;
identity as dynamic invariant; g₃₃ and g₆₄ as regime markers.`,

    'chIV-time': `CHAPTER CONTEXT — Book 4 Formal Theory · Ch 8 · The Nature of Time in GTCT
Key definitions active: 9 readings of T (constraint, generator, memory, resolver, identity,
irreversibility, bridge, present, emergence). Time is not background — it is the fifth operator.`,

    'chTau-tartaruga': `CHAPTER CONTEXT — Ch τ · The Cosmic Tortoise / Tartaruga Cósmica
Key definitions active: τ = 2 (embodiment threshold, contact ratio);
τ as the ratio at which the stochastic regime concentrates below the attractor radius;
bilingual EN/PT — use whichever language the student prefers.`,

    'ch11-catgt': `CHAPTER CONTEXT — Ch 11 · CatGT — Catalytic Generative Theory
Key definitions active: catalytic extension of GTCT; plasma coherence bridge;
categorical morphisms fᵢⱼ:Xᵢ→Xⱼ as the formal statement that domains are objects in dm³.`,

    'chE-gtct': `CHAPTER CONTEXT — Ch E · GTCT for Everyone
Key definitions active: 9 axioms · 12 operators · 4 theorems · time as 5 properties.
Accessible framing — the framework's full logical content, no prerequisites assumed.`,

    'ch-faraday': `CHAPTER CONTEXT — Ch Faraday · Hidden Geometry of EM Forces
Key definitions active: Maxwell equations rewritten in contact-geometric language;
Faraday tensor as folding operator F; dm³ embedding of electromagnetic field structure.`,

    'gomc-opus': `CHAPTER CONTEXT — GOMC Opus · CatGT + Plasma + Coherence Bridge
Key definitions active: GOMC operator algebra (G,O,M,C extended ring);
plasma reconnection as dm³ instantiation; Coherence Bridge parameters for plasma domain
(μ_max=−0.42, ω=0.015, β=1.8, κ*≈5×10⁻⁴ km⁻¹).`,
  };

  /**
   * Portal-level context lines, keyed by CEFR level.
   * Injected for portal.html prompts.
   */
  const PORTAL_CONTEXT = {
    'A1': `PORTAL LEVEL — A1 · Operator C (Compression) · First Contact
The student is at the seed. They have not yet seen algebra. Use one concrete example from nature.
Do not introduce G-chain notation yet — name the operators in plain language only.`,

    'A2': `PORTAL LEVEL — A2 · Operator K (Curvature) · Pattern Recognition · Day 21 threshold
The student can identify patterns, cause-and-effect, and invariants.
Science begins here. Introduce g₃₃ = 33 as an analogy from sport or skill acquisition.`,

    'B1': `PORTAL LEVEL — B1 · Operators K→F · Constrain and Begin to Fold
The student can follow extended argument and generate research questions.
Introduce the operator chain C→K→F→U by name. Use ε* = 1/3 as the constraint constant.`,

    'B2': `PORTAL LEVEL — B2 · Operator F (Fold) · Domain Fluency
The student reads unsimplified academic text and generates multi-step argument.
Cross-domain transfer is the key move. Use τ = 2 and the lemniscate/analemma example if relevant.`,

    'C1': `PORTAL LEVEL — C1 · Operator U (Unfolding) · Research Generation
The student generates knowledge that did not exist before. Push back on vague claims.
The student should produce falsifiable statements naming the invariant being protected.`,

    'D1': `PORTAL LEVEL — D1 · g₃₃ = 33 cycles completed · Individual Fixed Point
The operator chain is now automatic for the student. Test whether C→K→F→U has become
unconscious. The fixed point criterion: x* = G(x*) — the student's thinking is self-consistent.`,

    'D2': `PORTAL LEVEL — D2 · Collective Threshold · Θ = g₃₃ + N×M
The student is an operator of collective intelligence. N agents × M interactions ≥ Θ.
The open horizon: χ(H*(X⁶)) = 33 ∀n — one honest sorry in AXLE v6.1.`,
  };

  /* ─────────────────────────────────────────────────────────────────
   * SECTION 2 — PAGE DETECTION
   * ───────────────────────────────────────────────────────────────── */

  /**
   * Detect which chapter or portal level this page belongs to.
   * Returns { type: 'chapter'|'portal'|'unknown', slug: string }
   */
  function detectPage() {
    const path = window.location.pathname;
    const filename = path.split('/').pop().replace('.html', '');

    // Portal page
    if (filename === 'portal') {
      return { type: 'portal', slug: null };
    }

    // Chapter pages — match known slugs
    const knownChapters = Object.keys(CHAPTER_CONTEXT);
    for (const slug of knownChapters) {
      if (filename === slug || filename.startsWith(slug)) {
        return { type: 'chapter', slug };
      }
    }

    // Fallback: any page with a prompt block gets generic treatment
    return { type: 'chapter', slug: null };
  }

  /* ─────────────────────────────────────────────────────────────────
   * SECTION 3 — PROMPT TEXT EXTRACTION
   * ───────────────────────────────────────────────────────────────── */

  /**
   * Extract the raw prompt text from a prompt block element.
   * Handles multiple markup patterns found across the books.
   */
  function extractPromptText(container) {
    // Pattern 1: explicit .prompt-text child
    const explicit = container.querySelector('.prompt-text');
    if (explicit) return explicit.innerText.trim();

    // Pattern 2: the container itself holds the text (portal.html pattern)
    // Find the text node that isn't the button
    const clone = container.cloneNode(true);
    // Remove all button elements from clone
    clone.querySelectorAll('button, .copy-btn').forEach(el => el.remove());
    const text = clone.innerText.trim();
    if (text.length > 20) return text;

    // Pattern 3: sibling paragraph before the copy button
    const btn = container.querySelector('button, .copy-btn');
    if (btn) {
      const prev = btn.previousElementSibling;
      if (prev) return prev.innerText.trim();
    }

    return container.innerText.trim();
  }

  /**
   * Detect the portal level from context (parent heading or data attribute).
   */
  function detectPortalLevel(btn) {
    // Walk up the DOM looking for a heading that names the level
    let el = btn;
    for (let i = 0; i < 10; i++) {
      el = el.parentElement;
      if (!el) break;
      const heading = el.querySelector('h3, h4, [class*="level"]');
      if (heading) {
        const text = heading.innerText.toUpperCase();
        for (const level of Object.keys(PORTAL_CONTEXT)) {
          if (text.includes('LEVEL ' + level) || text.includes(level + ' ·') || text.startsWith(level)) {
            return level;
          }
        }
      }
      // Check data attribute
      if (el.dataset && el.dataset.level) return el.dataset.level.toUpperCase();
    }
    return null;
  }

  /* ─────────────────────────────────────────────────────────────────
   * SECTION 4 — PROMPT ASSEMBLY
   * ───────────────────────────────────────────────────────────────── */

  /**
   * The broken pattern in chapter-end prompts:
   *   "You are reading Chapter N of Principia Orthogona Book 4..."
   * This line is the primary fringe-science guard trigger.
   * We strip it and replace with the framework header.
   */
  function stripBrokenFrame(text) {
    // Remove the "You are reading..." opener and everything before the task line
    return text
      .replace(/You are reading Chapter[\s\S]*?(?=Your task:|$)/i, '')
      .replace(/^[\s\n]+/, '');
  }

  /**
   * Assemble the final wrapped prompt for a chapter page.
   */
  function assembleChapterPrompt(rawText, slug) {
    const chapterCtx = slug && CHAPTER_CONTEXT[slug]
      ? CHAPTER_CONTEXT[slug]
      : 'CHAPTER CONTEXT — [chapter not yet registered in prompt-engine.js]';

    const task = stripBrokenFrame(rawText);

    return [
      FRAMEWORK_HEADER,
      '─── CHAPTER-SPECIFIC DEFINITIONS ───────────────────────',
      chapterCtx,
      '',
      '─── TASK ────────────────────────────────────────────────',
      task,
      '─────────────────────────────────────────────────────────',
    ].join('\n');
  }

  /**
   * Assemble the final wrapped prompt for a portal page.
   */
  function assemblePortalPrompt(rawText, level) {
    const portalCtx = level && PORTAL_CONTEXT[level]
      ? PORTAL_CONTEXT[level]
      : 'PORTAL LEVEL — [level not detected; treat student as intermediate]';

    return [
      FRAMEWORK_HEADER,
      '─── PORTAL LEVEL CONTEXT ────────────────────────────────',
      portalCtx,
      '',
      '─── PROMPT ──────────────────────────────────────────────',
      rawText,
      '─────────────────────────────────────────────────────────',
    ].join('\n');
  }

  /* ─────────────────────────────────────────────────────────────────
   * SECTION 5 — BUTTON INTERCEPTION
   * ───────────────────────────────────────────────────────────────── */

  const { type: pageType, slug: pageSlug } = detectPage();

  /**
   * Find all copy buttons on the page.
   * Matches: .copy-btn, button[data-copy], any button whose text is
   * "Copy", "COPY", "COPY PROMPT", "Copy Prompt".
   */
  function findCopyButtons() {
    const candidates = Array.from(document.querySelectorAll('button, [data-copy]'));
    return candidates.filter(el => {
      const text = (el.innerText || el.textContent || '').trim().toUpperCase();
      const isCopyText = ['COPY', 'COPY PROMPT', 'COPY PROMPT', 'COPY TEXT'].includes(text);
      const hasCopyClass = el.classList.contains('copy-btn') || el.classList.contains('copy-button');
      const hasCopyData = el.hasAttribute('data-copy');
      return isCopyText || hasCopyClass || hasCopyData;
    });
  }

  /**
   * Given a copy button, find the prompt container it belongs to.
   * Walks up the DOM looking for .prompt-block, .prompt-wrapper,
   * or a div/section that contains both text and the button.
   */
  function findPromptContainer(btn) {
    let el = btn.parentElement;
    for (let i = 0; i < 8; i++) {
      if (!el) break;
      const cls = el.className || '';
      if (cls.includes('prompt') || cls.includes('task') || cls.includes('exercise')) {
        return el;
      }
      // Container has substantial text content (>50 chars) beyond just the button
      const clone = el.cloneNode(true);
      clone.querySelectorAll('button').forEach(b => b.remove());
      if (clone.innerText.trim().length > 50) {
        return el;
      }
      el = el.parentElement;
    }
    return btn.parentElement;
  }

  /**
   * Intercept a copy button: wrap its payload with the framework header,
   * then write to clipboard.
   */
  function interceptButton(btn) {
    btn.addEventListener('click', async function (e) {
      e.stopPropagation();
      e.preventDefault();

      const container = findPromptContainer(btn);
      const rawText = extractPromptText(container);

      let wrapped;
      if (pageType === 'portal') {
        const level = detectPortalLevel(btn);
        wrapped = assemblePortalPrompt(rawText, level);
      } else {
        wrapped = assembleChapterPrompt(rawText, pageSlug);
      }

      try {
        await navigator.clipboard.writeText(wrapped);
        // Visual feedback — preserve original button text
        const original = btn.innerText;
        btn.innerText = '✓ Copied with framework';
        btn.style.background = '#1a3a1a';
        btn.style.color = '#a8d5a2';
        setTimeout(() => {
          btn.innerText = original;
          btn.style.background = '';
          btn.style.color = '';
        }, 2000);
      } catch (err) {
        // Fallback for browsers that block clipboard API
        fallbackCopy(wrapped);
        btn.innerText = '✓ Copied';
        setTimeout(() => { btn.innerText = btn.dataset.originalText || 'Copy'; }, 2000);
      }
    }, true); // capture phase so we run before any existing listeners
  }

  /**
   * Fallback copy using textarea trick (for older Safari, HTTP contexts).
   */
  function fallbackCopy(text) {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); } catch (_) {}
    document.body.removeChild(ta);
  }

  /* ─────────────────────────────────────────────────────────────────
   * SECTION 6 — INIT
   * ───────────────────────────────────────────────────────────────── */

  function init() {
    const buttons = findCopyButtons();
    buttons.forEach(interceptButton);

    // Also handle dynamically added buttons (for pages with lazy rendering)
    const observer = new MutationObserver(() => {
      const newButtons = findCopyButtons().filter(b => !b.dataset.peIntercepted);
      newButtons.forEach(btn => {
        btn.dataset.peIntercepted = '1';
        interceptButton(btn);
      });
    });
    observer.observe(document.body, { childList: true, subtree: true });

    // Always log so you can confirm the engine loaded
    console.log(`[prompt-engine v1.0] type:${pageType} slug:${pageSlug || 'none'} buttons:${buttons.length}`);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
