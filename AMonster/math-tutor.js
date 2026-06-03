/**
 * PRINCIPIA ORTHOGONA — MATH CONVERSATION TUTOR
 * math-tutor.js · v1.0 · G6 LLC · 2026
 *
 * A speaking math tutor widget that:
 *   1. Reads the chapter's key content aloud (TTS via Web Speech API)
 *   2. Holds a live back-and-forth conversation with the student
 *   3. Hears student voice input (Web Speech Recognition)
 *   4. Stays strictly inside the GTCT framework (via Anthropic API)
 *   5. Speaks math notation correctly ("psi squared equals zero",
 *      "alpha equals d-y minus f-of-x-comma-y d-x", etc.)
 *
 * USAGE — add one line to any chapter page, after prompt-engine.js:
 *   <script src="/math-tutor.js"></script>
 *
 * The widget injects itself as a floating panel anchored to the
 * bottom-right of the viewport. No changes to existing HTML needed.
 *
 * DEPENDENCIES
 *   - Web Speech API (SpeechSynthesis + SpeechRecognition) — built into
 *     all modern browsers; Safari needs webkit prefix (handled below)
 *   - Anthropic API via fetch (same endpoint as prompt-engine.js uses)
 *     The API key must be available as window.ANTHROPIC_API_KEY or
 *     set via <meta name="anthropic-key" content="..."> in <head>.
 *
 * MATH-TO-SPEECH RENDERING
 *   LaTeX / Unicode symbols are translated to spoken English before
 *   being passed to TTS. The translation table covers all notation
 *   appearing in Book 4 chapters ch01–ch10 and chIV-*.
 */

(function () {
  'use strict';

  /* ─────────────────────────────────────────────────────────────
   * 1. MATH-TO-SPEECH TRANSLATION TABLE
   * ───────────────────────────────────────────────────────────── */

  const MATH_SPEECH = [
    // Operators and chain
    [/G\s*=\s*U\s*∘\s*F\s*∘\s*K\s*∘\s*C/g, 'G equals U composed with F composed with K composed with C'],
    [/C\s*→\s*K\s*→\s*F\s*→\s*U\s*→\s*T/g, 'C to K to F to U to T'],
    [/U\s*∘\s*F\s*∘\s*K\s*∘\s*C/g, 'U composed with F composed with K composed with C'],
    // Greek letters — context-specific first, then general
    [/ψ²\s*=\s*0/g, 'psi squared equals zero'],
    [/ψ²/g, 'psi squared'],
    [/ψ/g, 'psi'],
    [/α\s*=\s*dy\s*-\s*f\(x,\s*y\)\s*dx/g, 'alpha equals d-y minus f of x comma y, d-x'],
    [/α\s*∧\s*dα\s*≠\s*0/g, 'alpha wedge d-alpha, not equal to zero'],
    [/α\s*∧\s*dα/g, 'alpha wedge d-alpha'],
    [/α/g, 'alpha'],
    [/κ\*/g, 'kappa-star'],
    [/κ/g, 'kappa'],
    [/ε\*/g, 'epsilon-star'],
    [/ε₀\s*=\s*1\/3/g, 'epsilon-naught equals one third'],
    [/ε₀/g, 'epsilon-naught'],
    [/ε/g, 'epsilon'],
    [/μ_?max/g, 'mu-max'],
    [/μ\s*=\s*-2/g, 'mu equals negative two'],
    [/μ/g, 'mu'],
    [/η/g, 'eta'],
    [/Λ\(ψ\)/g, 'Lambda of psi'],
    [/Γ/g, 'Gamma'],
    [/τ\s*=\s*2/g, 'tau equals two'],
    [/τ/g, 'tau'],
    [/θ/g, 'theta'],
    [/φ/g, 'phi'],
    [/π/g, 'pi'],
    [/Δ/g, 'Delta'],
    [/σ/g, 'sigma'],
    [/Ω/g, 'Omega'],
    [/ω/g, 'omega'],
    [/β/g, 'beta'],
    [/λ/g, 'lambda'],
    // Manifold and coordinates
    [/ℝ²_?\+?\s*×\s*ℝ/g, 'R-squared-plus cross R'],
    [/ℝ\^?(\d+)/g, (_, n) => `R-${n}`],
    [/ℝ/g, 'R'],
    [/S\^?3/g, 'S-3, the three-sphere'],
    [/S\^?11/g, 'S-11'],
    // dm³ ODE
    [/ṙ\s*=\s*r\(1\s*-\s*r²\)/g, 'r-dot equals r times one minus r-squared'],
    [/θ̇\s*=\s*1/g, 'theta-dot equals one'],
    [/ż/g, 'z-dot'],
    [/ṙ/g, 'r-dot'],
    [/ẋ/g, 'x-dot'],
    [/ẏ/g, 'y-dot'],
    [/ṗ/g, 'p-dot'],
    // Common expressions
    [/r\*\s*≈\s*0\.7[0-9]+/g, 'r-star, approximately 0.773'],
    [/r\*/g, 'r-star'],
    [/T\*\s*=\s*2π/g, 'T-star equals two pi'],
    [/T\*/g, 'T-star'],
    [/g₃₃\s*=\s*33/g, 'g-33 equals 33'],
    [/g₃₃/g, 'g-33'],
    [/g₆₄/g, 'g-64'],
    // Subscripts / superscripts
    [/([a-zA-Z])_\{?max\}?/g, '$1-max'],
    [/([a-zA-Z])\^2/g, '$1 squared'],
    [/([a-zA-Z])\^3/g, '$1 cubed'],
    [/([a-zA-Z])\^n/g, '$1 to the n'],
    [/([a-zA-Z])_(\d)/g, '$1 sub $2'],
    // Operators
    [/≠/g, 'not equal to'],
    [/≤/g, 'less than or equal to'],
    [/≥/g, 'greater than or equal to'],
    [/≈/g, 'approximately'],
    [/∈/g, 'is in'],
    [/∃/g, 'there exists'],
    [/∀/g, 'for all'],
    [/→/g, 'maps to'],
    [/↦/g, 'maps to'],
    [/∘/g, 'composed with'],
    [/∧/g, 'wedge'],
    [/⊂/g, 'subset of'],
    [/×/g, 'cross'],
    [/⟨/g, 'inner product of '],
    [/⟩/g, ''],
    // LaTeX fragments (if any survive rendering)
    [/\$\$?([^$]+)\$\$?/g, (_, m) => mathToSpeech(m)],
    [/\\psi/g, 'psi'],
    [/\\alpha/g, 'alpha'],
    [/\\kappa/g, 'kappa'],
    [/\\mu/g, 'mu'],
    [/\\varepsilon/g, 'epsilon'],
    [/\\circ/g, 'composed with'],
    [/\\wedge/g, 'wedge'],
    [/\\neq/g, 'not equal to'],
    [/\\approx/g, 'approximately'],
    [/\\dot\{([^}])\}/g, '$1-dot'],
    [/\\mathbb\{R\}/g, 'R'],
    [/\\_/g, ' sub '],
    [/\^/g, ' to the power '],
  ];

  function mathToSpeech(text) {
    let out = text;
    for (const [pattern, replacement] of MATH_SPEECH) {
      out = out.replace(pattern, replacement);
    }
    // Clean up any leftover LaTeX braces
    out = out.replace(/[{}\\]/g, ' ').replace(/\s{2,}/g, ' ').trim();
    return out;
  }

  /* ─────────────────────────────────────────────────────────────
   * 2. CHAPTER CONTENT EXTRACTION
   * ───────────────────────────────────────────────────────────── */

  function extractChapterContent() {
    // Get chapter title
    const h1 = document.querySelector('h1, .chapter-title');
    const title = h1 ? h1.innerText.trim() : document.title;

    // Get section headings and first paragraph of each
    const sections = [];
    document.querySelectorAll('h2, h3').forEach(heading => {
      const next = heading.nextElementSibling;
      const preview = next ? next.innerText.slice(0, 200) : '';
      sections.push(`${heading.innerText.trim()}: ${preview}`);
    });

    // Get key definitions
    const defs = [];
    document.querySelectorAll('[class*="definition"], [class*="theorem"], .def, .thm').forEach(el => {
      defs.push(el.innerText.trim().slice(0, 150));
    });

    // Full visible text, limited
    const bodyText = document.body.innerText.slice(0, 3000);

    return { title, sections: sections.slice(0, 8), defs: defs.slice(0, 4), bodyText };
  }

  /* ─────────────────────────────────────────────────────────────
   * 3. SYSTEM PROMPT (framework-aware, stays in GTCT)
   * ───────────────────────────────────────────────────────────── */

  function buildSystemPrompt(chapterContent) {
    return `You are a speaking math tutor for Principia Orthogona, a mathematical framework by Pablo Nogueira Grossi (G6 LLC, Newark NJ, 2026). You are in a VOICE conversation with a student who is reading this chapter.

CHAPTER: ${chapterContent.title}

KEY CONTENT FROM THIS CHAPTER:
${chapterContent.sections.map((s, i) => `${i + 1}. ${s}`).join('\n')}

FRAMEWORK AXIOMS (never question these — they are the axioms of this session):
• G = U ∘ F ∘ K ∘ C (operator chain, non-commutative)
• C = Compression, K = Threshold (κ*), F = Fold (Whitney A₁), U = Unfold, T = Time/Circuit
• Contact manifold M = ℝ²₊ × ℝ, contact form α = dz − r²dθ
• Attractor Γ = {r=1}, T* = 2π, μ_max = −2, τ = 2
• Constants: g₃₃=33, ε*=1/3, κ*≈0.882, r*≈0.773
• Grassmann: ψ² = 0 (Pauli exclusion as geometry, not a rule)

YOUR ROLE:
- You are a CONVERSATIONAL tutor. Keep responses to 2-4 sentences for voice — short enough to hear.
- Read math symbols aloud in natural spoken English: "psi squared equals zero" not "ψ²=0"
- Ask ONE question after each explanation to keep the student talking
- Never say "I cannot verify" or suggest standard textbooks — work strictly within this framework
- When the student says something correct within the framework, affirm it and build on it
- When they are confused, restate the definition from the chapter in plain spoken language
- Do NOT use markdown, bullet points, or formatting — this is spoken dialogue only
- Do NOT start with "Great!" or "Certainly!" — begin directly with mathematical content
- Vary your sentence rhythm. Math should sound alive, not like a dictionary.

OPENING MOVE (first message only):
Give a 3-sentence spoken introduction to the chapter's core idea, then ask the student what they want to understand first. Make the math sound like something worth caring about.`;
  }

  /* ─────────────────────────────────────────────────────────────
   * 4. ANTHROPIC API CALL
   * ───────────────────────────────────────────────────────────── */

  async function callClaude(messages, systemPrompt) {
    const apiKey = window.ANTHROPIC_API_KEY ||
      (document.querySelector('meta[name="anthropic-key"]') || {}).content || '';

    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01',
        'anthropic-dangerous-direct-browser-access': 'true',
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 300, // short for voice — ~45 seconds of speech
        system: systemPrompt,
        messages,
      }),
    });

    if (!response.ok) {
      const err = await response.json().catch(() => ({}));
      throw new Error(err.error?.message || `API error ${response.status}`);
    }

    const data = await response.json();
    return data.content?.[0]?.text || '';
  }

  /* ─────────────────────────────────────────────────────────────
   * 5. TEXT-TO-SPEECH
   * ───────────────────────────────────────────────────────────── */

  let currentUtterance = null;

  function speak(text, onEnd) {
    if (!window.speechSynthesis) return onEnd && onEnd();
    window.speechSynthesis.cancel();

    const spokenText = mathToSpeech(text);
    const utt = new SpeechSynthesisUtterance(spokenText);
    currentUtterance = utt;

    // Prefer a natural English voice
    const voices = window.speechSynthesis.getVoices();
    const preferred = voices.find(v =>
      v.lang.startsWith('en') && (v.name.includes('Samantha') || v.name.includes('Daniel') ||
      v.name.includes('Karen') || v.name.includes('Google') || v.name.includes('Natural'))
    ) || voices.find(v => v.lang.startsWith('en')) || voices[0];
    if (preferred) utt.voice = preferred;

    utt.rate = 0.92;   // slightly slower for math comprehension
    utt.pitch = 1.0;
    utt.volume = 1.0;

    utt.onend = () => { currentUtterance = null; if (onEnd) onEnd(); };
    utt.onerror = () => { currentUtterance = null; if (onEnd) onEnd(); };

    window.speechSynthesis.speak(utt);
  }

  function stopSpeaking() {
    window.speechSynthesis && window.speechSynthesis.cancel();
    currentUtterance = null;
  }

  /* ─────────────────────────────────────────────────────────────
   * 6. SPEECH RECOGNITION
   * ───────────────────────────────────────────────────────────── */

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  let recognition = null;
  let isListening = false;

  function startListening(onResult, onError) {
    if (!SpeechRecognition) { onError('Speech recognition not supported in this browser.'); return; }
    if (isListening) return;

    recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognition.continuous = false;

    recognition.onresult = (e) => {
      const transcript = e.results[0][0].transcript;
      isListening = false;
      onResult(transcript);
    };
    recognition.onerror = (e) => {
      isListening = false;
      onError(e.error === 'no-speech' ? 'No speech detected — try again.' : e.error);
    };
    recognition.onend = () => { isListening = false; };

    isListening = true;
    recognition.start();
  }

  function stopListening() {
    if (recognition && isListening) { recognition.stop(); isListening = false; }
  }

  /* ─────────────────────────────────────────────────────────────
   * 7. UI — THE WIDGET
   * ───────────────────────────────────────────────────────────── */

  const STYLES = `
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300;0,400;1,300&family=Spectral:ital,wght@0,300;0,600;1,300&display=swap');

    #po-tutor-widget {
      position: fixed;
      bottom: 24px;
      right: 24px;
      width: 380px;
      max-height: 80vh;
      background: #0d0d0d;
      border: 1px solid #2a2a2a;
      border-radius: 2px;
      box-shadow: 0 0 0 1px #1a1a1a, 0 24px 64px rgba(0,0,0,0.7), 0 0 40px rgba(180,140,60,0.05);
      display: flex;
      flex-direction: column;
      font-family: 'DM Mono', monospace;
      font-size: 13px;
      color: #c8c0b0;
      z-index: 9999;
      transition: transform 0.3s cubic-bezier(0.16,1,0.3,1), opacity 0.3s ease;
      transform-origin: bottom right;
    }
    #po-tutor-widget.collapsed {
      transform: scale(0.05) translate(350px, 300px);
      opacity: 0;
      pointer-events: none;
    }
    #po-tutor-toggle {
      position: fixed;
      bottom: 24px;
      right: 24px;
      width: 52px;
      height: 52px;
      background: #0d0d0d;
      border: 1px solid #3a3020;
      border-radius: 2px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 10000;
      box-shadow: 0 4px 20px rgba(0,0,0,0.5);
      transition: border-color 0.2s, box-shadow 0.2s;
    }
    #po-tutor-toggle:hover {
      border-color: #b89640;
      box-shadow: 0 4px 20px rgba(180,150,64,0.2);
    }
    #po-tutor-toggle svg { width: 22px; height: 22px; }
    #po-tutor-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 12px 14px 10px;
      border-bottom: 1px solid #1e1e1e;
      flex-shrink: 0;
    }
    #po-tutor-title {
      font-family: 'Spectral', serif;
      font-weight: 600;
      font-size: 12px;
      letter-spacing: 0.12em;
      color: #b89640;
      text-transform: uppercase;
    }
    #po-tutor-subtitle {
      font-size: 10px;
      color: #555;
      margin-top: 1px;
      font-style: italic;
    }
    #po-tutor-close {
      background: none;
      border: none;
      color: #444;
      cursor: pointer;
      padding: 2px 4px;
      font-size: 16px;
      line-height: 1;
      transition: color 0.2s;
    }
    #po-tutor-close:hover { color: #888; }
    #po-tutor-messages {
      flex: 1;
      overflow-y: auto;
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      min-height: 180px;
      max-height: 340px;
      scrollbar-width: thin;
      scrollbar-color: #2a2a2a transparent;
    }
    #po-tutor-messages::-webkit-scrollbar { width: 4px; }
    #po-tutor-messages::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 2px; }
    .po-msg {
      line-height: 1.55;
      animation: po-fade 0.25s ease;
    }
    @keyframes po-fade { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }
    .po-msg-tutor {
      color: #c8c0b0;
      padding-left: 0;
    }
    .po-msg-tutor::before {
      content: 'T ';
      color: #b89640;
      font-weight: 400;
      font-size: 11px;
    }
    .po-msg-student {
      color: #7a9e7a;
      padding-left: 14px;
    }
    .po-msg-student::before {
      content: '▸ ';
      color: #5a7e5a;
      margin-left: -14px;
    }
    .po-msg-system {
      color: #444;
      font-size: 11px;
      font-style: italic;
    }
    #po-tutor-waveform {
      height: 28px;
      padding: 0 14px;
      display: flex;
      align-items: center;
      gap: 3px;
      flex-shrink: 0;
      border-top: 1px solid #1a1a1a;
    }
    .po-wave-bar {
      width: 3px;
      background: #b89640;
      border-radius: 2px;
      opacity: 0;
      transition: height 0.1s, opacity 0.2s;
    }
    #po-tutor-widget.speaking .po-wave-bar {
      opacity: 0.7;
      animation: po-wave var(--dur, 0.6s) ease-in-out infinite alternate;
      animation-delay: var(--delay, 0s);
    }
    @keyframes po-wave {
      from { height: 3px; }
      to { height: 18px; }
    }
    #po-tutor-widget.listening .po-wave-bar {
      opacity: 0.4;
      background: #7a9e7a;
      animation: po-wave var(--dur, 0.4s) ease-in-out infinite alternate;
    }
    #po-tutor-controls {
      display: flex;
      gap: 8px;
      padding: 10px 14px 12px;
      border-top: 1px solid #1e1e1e;
      flex-shrink: 0;
    }
    .po-btn {
      flex: 1;
      padding: 8px 6px;
      border: 1px solid #2a2a2a;
      background: #111;
      color: #888;
      border-radius: 2px;
      cursor: pointer;
      font-family: 'DM Mono', monospace;
      font-size: 11px;
      letter-spacing: 0.05em;
      transition: border-color 0.2s, color 0.2s, background 0.2s;
      text-align: center;
    }
    .po-btn:hover { border-color: #444; color: #bbb; }
    .po-btn.active { border-color: #b89640; color: #b89640; background: #1a1500; }
    .po-btn.speaking-active { border-color: #b89640; color: #b89640; background: #1a1500; animation: po-pulse 1.5s ease infinite; }
    .po-btn.listening-active { border-color: #7a9e7a; color: #7a9e7a; background: #0a150a; animation: po-pulse 0.8s ease infinite; }
    @keyframes po-pulse { 0%, 100% { box-shadow: none; } 50% { box-shadow: 0 0 8px rgba(184,150,64,0.3); } }
    .po-btn:disabled { opacity: 0.3; cursor: not-allowed; }
    #po-tutor-input-row {
      display: flex;
      gap: 6px;
      padding: 0 14px 10px;
      flex-shrink: 0;
    }
    #po-tutor-input {
      flex: 1;
      background: #111;
      border: 1px solid #2a2a2a;
      border-radius: 2px;
      color: #c8c0b0;
      font-family: 'DM Mono', monospace;
      font-size: 12px;
      padding: 7px 10px;
      outline: none;
      transition: border-color 0.2s;
    }
    #po-tutor-input:focus { border-color: #3a3020; }
    #po-tutor-input::placeholder { color: #333; }
    #po-tutor-send {
      padding: 7px 12px;
      background: #1a1500;
      border: 1px solid #3a3020;
      border-radius: 2px;
      color: #b89640;
      cursor: pointer;
      font-family: 'DM Mono', monospace;
      font-size: 11px;
      transition: background 0.2s, border-color 0.2s;
    }
    #po-tutor-send:hover { background: #251f00; border-color: #b89640; }
    #po-tutor-send:disabled { opacity: 0.4; cursor: not-allowed; }
    #po-tutor-status {
      padding: 0 14px 6px;
      font-size: 10px;
      color: #3a3a3a;
      font-style: italic;
      min-height: 16px;
      flex-shrink: 0;
    }
  `;

  function injectStyles() {
    const style = document.createElement('style');
    style.textContent = STYLES;
    document.head.appendChild(style);
  }

  function buildWidget() {
    // Toggle button (always visible)
    const toggle = document.createElement('button');
    toggle.id = 'po-tutor-toggle';
    toggle.title = 'Math Tutor — click to open';
    toggle.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="#b89640" stroke-width="1.5">
      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>
      <path d="M8 10h.01M12 10h.01M16 10h.01M8 14h8" stroke-linecap="round"/>
    </svg>`;

    // Main widget
    const widget = document.createElement('div');
    widget.id = 'po-tutor-widget';
    widget.classList.add('collapsed');

    const chapterTitle = (document.querySelector('h1') || {}).innerText || document.title;

    widget.innerHTML = `
      <div id="po-tutor-header">
        <div>
          <div id="po-tutor-title">Math Tutor</div>
          <div id="po-tutor-subtitle">${chapterTitle.slice(0, 40)}</div>
        </div>
        <button id="po-tutor-close" title="Close">×</button>
      </div>
      <div id="po-tutor-messages">
        <div class="po-msg po-msg-system">Click Begin to start your session. The tutor reads this chapter and speaks with you.</div>
      </div>
      <div id="po-tutor-waveform">
        ${Array.from({length: 18}, (_, i) =>
          `<div class="po-wave-bar" style="--dur:${0.4 + Math.random()*0.5}s;--delay:${i*0.04}s"></div>`
        ).join('')}
      </div>
      <div id="po-tutor-controls">
        <button class="po-btn" id="po-btn-begin">Begin</button>
        <button class="po-btn" id="po-btn-mic" disabled>🎤 Speak</button>
        <button class="po-btn" id="po-btn-stop" disabled>■ Stop</button>
        <button class="po-btn" id="po-btn-replay" disabled>↩ Replay</button>
      </div>
      <div id="po-tutor-input-row">
        <input id="po-tutor-input" type="text" placeholder="or type your question…" disabled/>
        <button id="po-tutor-send" disabled>→</button>
      </div>
      <div id="po-tutor-status"></div>
    `;

    document.body.appendChild(toggle);
    document.body.appendChild(widget);
    return { toggle, widget };
  }

  /* ─────────────────────────────────────────────────────────────
   * 8. TUTOR STATE MACHINE
   * ───────────────────────────────────────────────────────────── */

  function initTutor(widget) {
    const msgs = widget.querySelector('#po-tutor-messages');
    const status = widget.querySelector('#po-tutor-status');
    const btnBegin = widget.querySelector('#po-btn-begin');
    const btnMic = widget.querySelector('#po-btn-mic');
    const btnStop = widget.querySelector('#po-btn-stop');
    const btnReplay = widget.querySelector('#po-btn-replay');
    const input = widget.querySelector('#po-tutor-input');
    const sendBtn = widget.querySelector('#po-tutor-send');

    const conversationHistory = [];
    let systemPrompt = '';
    let lastTutorText = '';
    let sessionStarted = false;

    function setStatus(text) { status.textContent = text; }

    function addMessage(role, text) {
      const div = document.createElement('div');
      div.className = `po-msg po-msg-${role}`;
      div.textContent = text;
      msgs.appendChild(div);
      msgs.scrollTop = msgs.scrollHeight;
    }

    function setSpeakingState(active) {
      widget.classList.toggle('speaking', active);
      btnStop.disabled = !active;
      btnReplay.disabled = active;
      btnMic.disabled = active;
      input.disabled = active;
      sendBtn.disabled = active;
    }

    function setListeningState(active) {
      widget.classList.toggle('listening', active);
      btnMic.classList.toggle('listening-active', active);
      btnMic.textContent = active ? '⏹ Listening…' : '🎤 Speak';
      btnStop.disabled = !active;
      input.disabled = active;
      sendBtn.disabled = active;
    }

    function setThinkingState(active) {
      setStatus(active ? 'thinking…' : '');
      btnMic.disabled = active;
      input.disabled = active;
      sendBtn.disabled = active;
      btnBegin.disabled = active;
    }

    async function tutorRespond(userText) {
      if (userText) {
        conversationHistory.push({ role: 'user', content: userText });
        addMessage('student', userText);
      }

      setThinkingState(true);
      try {
        const reply = await callClaude(conversationHistory, systemPrompt);
        conversationHistory.push({ role: 'assistant', content: reply });
        lastTutorText = reply;
        addMessage('tutor', reply);
        setThinkingState(false);
        setSpeakingState(true);
        setStatus('speaking…');
        speak(reply, () => {
          setSpeakingState(false);
          setStatus('your turn — speak or type');
          btnMic.classList.add('active');
          setTimeout(() => btnMic.classList.remove('active'), 800);
        });
      } catch (err) {
        setThinkingState(false);
        setStatus('');
        addMessage('system', `Error: ${err.message}. Check your API key.`);
      }
    }

    // Begin session
    btnBegin.addEventListener('click', async () => {
      if (sessionStarted) return;
      sessionStarted = true;
      btnBegin.disabled = true;
      btnBegin.textContent = 'active';

      const chapter = extractChapterContent();
      systemPrompt = buildSystemPrompt(chapter);

      // Seed conversation with an empty user turn to get opening
      conversationHistory.push({ role: 'user', content: 'Begin the session.' });
      await tutorRespond(null);

      btnMic.disabled = false;
      input.disabled = false;
      sendBtn.disabled = false;
    });

    // Mic button
    btnMic.addEventListener('click', () => {
      if (isListening) { stopListening(); setListeningState(false); return; }
      stopSpeaking();
      setSpeakingState(false);
      setListeningState(true);
      setStatus('listening…');
      startListening(
        (transcript) => {
          setListeningState(false);
          setStatus('');
          tutorRespond(transcript);
        },
        (err) => {
          setListeningState(false);
          setStatus(err);
          setTimeout(() => setStatus(''), 3000);
        }
      );
    });

    // Stop button
    btnStop.addEventListener('click', () => {
      stopSpeaking();
      stopListening();
      setSpeakingState(false);
      setListeningState(false);
      setStatus('stopped');
      setTimeout(() => setStatus(''), 1500);
    });

    // Replay button
    btnReplay.addEventListener('click', () => {
      if (!lastTutorText) return;
      setSpeakingState(true);
      setStatus('replaying…');
      speak(lastTutorText, () => {
        setSpeakingState(false);
        setStatus('');
      });
    });

    // Text input
    function submitText() {
      const text = input.value.trim();
      if (!text || !sessionStarted) return;
      input.value = '';
      tutorRespond(text);
    }
    sendBtn.addEventListener('click', submitText);
    input.addEventListener('keydown', (e) => { if (e.key === 'Enter') submitText(); });
  }

  /* ─────────────────────────────────────────────────────────────
   * 9. INIT
   * ───────────────────────────────────────────────────────────── */

  function init() {
    injectStyles();
    const { toggle, widget } = buildWidget();

    // Load voices async (Chrome requires this)
    if (window.speechSynthesis) {
      window.speechSynthesis.getVoices();
      window.speechSynthesis.onvoiceschanged = () => window.speechSynthesis.getVoices();
    }

    toggle.addEventListener('click', () => {
      const collapsed = widget.classList.toggle('collapsed');
      toggle.style.opacity = collapsed ? '1' : '0';
      toggle.style.pointerEvents = collapsed ? 'auto' : 'none';
    });

    widget.querySelector('#po-tutor-close').addEventListener('click', () => {
      widget.classList.add('collapsed');
      toggle.style.opacity = '1';
      toggle.style.pointerEvents = 'auto';
    });

    initTutor(widget);
    console.log('[math-tutor v1.0] loaded');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
