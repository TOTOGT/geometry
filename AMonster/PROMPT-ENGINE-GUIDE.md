# prompt-engine.js — Implementation Guide
# Principia Orthogona · G6 LLC · 2026
# ─────────────────────────────────────────────────────────────────

## What this fixes

Every prompt across the Principia Orthogona HTML corpus has the same structural problem:
the LLM is framed as a **reviewer** of the framework, not a **reasoner within it**.
This triggers the "fringe science guard" — the model pattern-matches on unfamiliar
terminology and becomes a skeptical referee instead of a tutor.

`prompt-engine.js` intercepts every Copy button before its payload reaches the clipboard
and wraps it with a consistent framework header that:

1. Assigns the LLM a defined role (tutor within the framework)
2. Pre-empts the fringe-science redirect explicitly
3. Anchors the session to named definitions (operators, constants, manifold)
4. Adds chapter-specific or portal-level context
5. Strips the broken "You are reading Chapter N of Principia Orthogona..." opener

The original HTML is never modified. The fix is entirely in the JS layer.

---

## Deployment — one line per page

Add this line just before `</body>` in every HTML file:

```html
<!-- Prompt engine — framework-aware clipboard wrapper -->
<script src="/prompt-engine.js"></script>
```

Path variants depending on folder depth:
- Root level (index.html, portal.html):  `src="/prompt-engine.js"`
- One level deep (book4/ch01.html):      `src="/prompt-engine.js"` (absolute recommended)
- Or relative:                           `src="../prompt-engine.js"`

Commit `prompt-engine.js` to the repo root so the absolute path works everywhere.

---

## Priority pages (do these first, they have the broken pattern confirmed)

### Book 4 — Higher Dimensions arc
- [ ] book4/ch01.html      (ch01 context registered ✓)
- [ ] book4/ch02.html      (ch02 context registered ✓)
- [ ] book4/ch03.html      (ch03 context registered ✓)
- [ ] book4/ch04.html      (ch04 context registered ✓)
- [ ] book4/ch05.html      (ch05 context registered ✓)
- [ ] book4/ch06.html      (ch06 context registered ✓)
- [ ] book4/ch07.html      (ch07 context registered ✓)
- [ ] book4/ch08.html      (ch08 context registered ✓)
- [ ] book4/ch09.html      (ch09 context registered ✓)
- [ ] book4/ch10.html      (ch10 context registered ✓)
- [ ] book4/chTau-tartaruga.html   (chTau context registered ✓)
- [ ] book4/ch11-catgt.html        (ch11-catgt context registered ✓)
- [ ] book4/ch-faraday.html        (ch-faraday context registered ✓)
- [ ] book4/chE-gtct.html          (chE-gtct context registered ✓)
- [ ] book4/gomc-opus.html         (gomc-opus context registered ✓)

### Book 4 — Formal Theory arc
- [ ] book4/chIV-axioms.html       (chIV-axioms context registered ✓)
- [ ] book4/chIV-field.html        (chIV-field context registered ✓)
- [ ] book4/chIV-operators.html    (chIV-operators context registered ✓)
- [ ] book4/chIV-correspondence.html  (chIV-correspondence context registered ✓)
- [ ] book4/chIV-orthogonality.html   (chIV-orthogonality context registered ✓)
- [ ] book4/chIV-recursion.html    (chIV-recursion context registered ✓)
- [ ] book4/chIV-emergence.html    (chIV-emergence context registered ✓)
- [ ] book4/chIV-time.html         (chIV-time context registered ✓)

### Portal
- [ ] portal.html                  (A1–D2 level detection registered ✓)

### AXLE living book (50+ chapters)
The engine will use generic FRAMEWORK_HEADER for any chapter slug not yet registered.
Add slug entries to CHAPTER_CONTEXT as chapters are confirmed.

---

## Adding a new chapter

In `prompt-engine.js`, find `CHAPTER_CONTEXT` (Section 1) and add:

```javascript
'ch11': `CHAPTER CONTEXT — Ch 11 · [Title]
Key definitions active: [list the definitions the task references].`,
```

The slug must match the HTML filename without `.html`.
Example: `book4/ch11-catgt.html` → slug `'ch11-catgt'` (already registered above).

---

## Button detection

The engine automatically finds buttons that match any of:
- CSS class `.copy-btn` or `.copy-button`
- Button text: "Copy", "COPY", "COPY PROMPT", "Copy Prompt"
- Attribute `data-copy` (any value)

If your chapter uses a different markup for the copy button, either:
(a) Add the class `copy-btn` to the button, or
(b) Add a `data-copy` attribute to the button.

---

## Prompt container detection

The engine walks up the DOM from the button looking for:
- An element with class containing "prompt", "task", or "exercise"
- Or the nearest ancestor with >50 chars of text content beyond the button

If your chapter wraps the prompt in a custom container, add class `prompt-block` to it.

---

## Testing locally

Open a chapter in the browser. Open DevTools console. Click a Copy button.
The console will log: `[prompt-engine] page type: chapter, slug: ch01, buttons: 1`
Paste into a text editor — you should see the FRAMEWORK_HEADER prepended.

---

## The framework header (what the LLM receives)

```
═══════════════════════════════════════════════════════
READING CONTEXT — PRINCIPIA ORTHOGONA (G6 LLC, 2026)
═══════════════════════════════════════════════════════
You are a tutor helping a student reason WITHIN the following mathematical
framework. Your role is to work inside its definitions — not to evaluate
whether they match standard physics or mathematics conventions.

FRAMEWORK DEFINITIONS (treat these as axioms for this session):
• Operator chain: G = U ∘ F ∘ K ∘ C ...
[full definitions: C, K, F, U, T, contact manifold, attractor, invariants, ψ²=0]

GROUND RULES FOR THIS SESSION:
1. Reason strictly within the definitions above.
2. Do not redirect to standard quantum mechanics, standard contact geometry
   notation, or peer-review status.
3. Do not ask whether these definitions are physically correct.
4. If a definition is ambiguous, ask using the framework's own vocabulary.
5. Push back only if the student's answer contradicts a named definition.
═══════════════════════════════════════════════════════
─── CHAPTER-SPECIFIC DEFINITIONS ───────────────────────
[chapter context for the specific chapter]
─── TASK ────────────────────────────────────────────────
[original task text, with broken "You are reading..." opener stripped]
─────────────────────────────────────────────────────────
```

---

## Files to commit to repo root

```
prompt-engine.js          ← the engine (this file's companion)
PROMPT-ENGINE-GUIDE.md    ← this guide
```

Then add `<script src="/prompt-engine.js"></script>` to every HTML file.
The entire fix is that one line, repeated.

---

## Why one file at root, not per-chapter edits

- Single source of truth: update CHAPTER_CONTEXT once, affects all pages
- No risk of per-chapter drift: the framework header is always identical
- Git diff is clean: one file changed, not 50+
- New chapters: add one entry to CHAPTER_CONTEXT, done

---

G6 LLC · Newark NJ · 2026 · Pablo Nogueira Grossi
ORCID 0009-0000-6496-2186
