/-
  Geometry of Legal Possibility: Lean specification (core Lean 4 only, no Mathlib).
  STATUS: UNTESTED. Written 2026-11-26 with no Lean toolchain available to the author.
  These are statements about a CONSTRUCTED model. They do not establish any substantive law.
  Hypotheses are explicit; no conclusion appears among them.
-/
namespace Jur

/-! ### Procedural system with legality, cost, lag, and a means-test predicate -/
structure ProcSys (S R : Type) where
  legal : Nat → R → S → S → Prop        -- rule system L at fixed jurisdiction j: step r from s to s' at day t
  cost  : R → Nat                         -- resource consumed
  lag   : R → Nat                         -- duration
  elig  : R → Nat → Prop                  -- eligibility given current resource level b (means tests)

variable {S R : Type} (Y : ProcSys S R)

/-- A: admissible (legally permitted) trajectories; resources and eligibility ignored. -/
inductive Adm : S → Nat → S → Nat → Prop
  | refl {s : S} {t : Nat} : Adm s t s t
  | step {s s' s2 : S} {t t2 : Nat} (r : R) (hl : Y.legal t r s s')
      (hrest : Adm s' (t + Y.lag r) s2 t2) : Adm s t s2 t2

/-- B: accessible trajectories: legal steps that the agent can pay for and is eligible for. -/
inductive Acc : Nat → S → Nat → S → Nat → Prop
  | refl {b : Nat} {s : S} {t : Nat} : Acc b s t s t
  | step {b : Nat} {s s' s2 : S} {t t2 : Nat} (r : R) (hl : Y.legal t r s s')
      (hc : Y.cost r ≤ b) (he : Y.elig r b)
      (hrest : Acc (b - Y.cost r) s' (t + Y.lag r) s2 t2) : Acc b s t s2 t2

/-- Property 1. Accessible trajectories are admissible. (Structural: the accessibility
semantics requires a legal step at every move, so it cannot create legal powers.) -/
theorem acc_sub_adm {b : Nat} {s s2 : S} {t t2 : Nat} (h : Acc Y b s t s2 t2) :
    Adm Y s t s2 t2 := by
  induction h with
  | refl => exact Adm.refl
  | step r hl _ _ _ ih => exact Adm.step r hl ih

/-- Property 2. Resource monotonicity, UNDER the explicit assumption that eligibility is
upward closed in resources (no means tests). The counterexample without it is in the Python demo. -/
theorem acc_mono (hup : ∀ r b b', b ≤ b' → Y.elig r b → Y.elig r b')
    {b : Nat} {s s2 : S} {t t2 : Nat} (h : Acc Y b s t s2 t2) :
    ∀ b', b ≤ b' → Acc Y b' s t s2 t2 := by
  induction h with
  | refl => intro b' _; exact Acc.refl
  | @step b s s' s2 t t2 r hl hc he _ ih =>
      intro b' hb
      exact Acc.step r hl (Nat.le_trans hc hb) (hup r b b' hb he)
        (ih (b' - Y.cost r) (by omega))

/-- Remedy availability (legal) versus reachability (practical). -/
def Available (G : S → Prop) (s0 : S) (t0 : Nat) : Prop :=
  ∃ s t, Adm Y s0 t0 s t ∧ G s

def Reachable (G : S → Prop) (b : Nat) (s0 : S) (t0 : Nat) : Prop :=
  ∃ s t, Acc Y b s0 t0 s t ∧ G s

/-- Obstruction: legally available but not reachable with resources b. -/
def Obstructed (G : S → Prop) (b : Nat) (s0 : S) (t0 : Nat) : Prop :=
  Available Y G s0 t0 ∧ ¬ Reachable Y G b s0 t0

/-- Property 6. Reachable implies available, so obstruction is exactly the available-minus-reachable set. -/
theorem reachable_imp_available {G : S → Prop} {b : Nat} {s0 : S} {t0 : Nat}
    (h : Reachable Y G b s0 t0) : Available Y G s0 t0 := by
  obtain ⟨s, t, hacc, hg⟩ := h
  exact ⟨s, t, acc_sub_adm Y hacc, hg⟩

/-- An accessibility-expanding intervention (more resources, same legal system) cannot leave
the admissible set and cannot lose reachable remedies (under upward-closed eligibility). -/
theorem intervention_expands {G : S → Prop} {b b' : Nat} {s0 : S} {t0 : Nat}
    (hup : ∀ r b b', b ≤ b' → Y.elig r b → Y.elig r b') (hb : b ≤ b')
    (h : Reachable Y G b s0 t0) : Reachable Y G b' s0 t0 ∧ Available Y G s0 t0 := by
  obtain ⟨s, t, hacc, hg⟩ := h
  exact ⟨⟨s, t, acc_mono Y hup hacc b' hb, hg⟩, reachable_imp_available Y ⟨s, t, hacc, hg⟩⟩

/-! ### Hohfeldian positions: correlatives and opposites kept distinct -/
inductive Pos
  | claim | duty | privilege | noClaim | power | liability | immunity | disability
  deriving DecidableEq, Repr

def Pos.cor : Pos → Pos
  | .claim => .duty | .duty => .claim | .privilege => .noClaim | .noClaim => .privilege
  | .power => .liability | .liability => .power | .immunity => .disability | .disability => .immunity

def Pos.opp : Pos → Pos
  | .claim => .noClaim | .noClaim => .claim | .privilege => .duty | .duty => .privilege
  | .power => .disability | .disability => .power | .immunity => .liability | .liability => .immunity

theorem cor_cor : ∀ p : Pos, p.cor.cor = p := by
  intro p; cases p <;> decide
theorem opp_opp : ∀ p : Pos, p.opp.opp = p := by
  intro p; cases p <;> decide
theorem cor_opp_comm : ∀ p : Pos, p.cor.opp = p.opp.cor := by
  intro p; cases p <;> decide
/-- Correlatives are never opposites, and neither is the identity. -/
theorem cor_ne_opp : ∀ p : Pos, p.cor ≠ p.opp := by
  intro p; cases p <;> decide
theorem cor_ne_self : ∀ p : Pos, p.cor ≠ p := by
  intro p; cases p <;> decide
theorem opp_ne_self : ∀ p : Pos, p.opp ≠ p := by
  intro p; cases p <;> decide
/-- The Klein four-group {id, cor, opp, cor∘opp} acts freely: all four images are distinct. -/
theorem free_klein : ∀ p : Pos, p ≠ p.cor ∧ p ≠ p.opp ∧ p ≠ p.cor.opp ∧
    p.cor ≠ p.opp ∧ p.cor ≠ p.cor.opp ∧ p.opp ≠ p.cor.opp := by
  intro p; cases p <;> decide

/-- A directed normative relation between two subjects; descriptive facts are a separate type. -/
structure NormRel (Agent Act : Type) where
  pos : Pos
  holder : Agent
  other : Agent
  act : Act

def NormRel.flip {Agent Act : Type} (r : NormRel Agent Act) : NormRel Agent Act :=
  { pos := r.pos.cor, holder := r.other, other := r.holder, act := r.act }

theorem flip_flip {Agent Act : Type} (r : NormRel Agent Act) : r.flip.flip = r := by
  cases r with
  | mk p h o a => simp [NormRel.flip, cor_cor]

end Jur
