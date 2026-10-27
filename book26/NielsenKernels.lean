/-
NielsenKernels.lean -- transcription of Appendix B ("TUFT_Forcing_Core.lean") of a third-party
preprint, with unicode repaired (the PDF text had lost the symbols  exists / and / neq / equiv),
plus a short section of `example`s showing what each kernel does and does not say.

STATUS: UNTESTED. Not compiled by the person who transcribed it (no Lean toolchain in that
workspace). Run:   tools/leancheck.sh --audit book26/NielsenKernels.lean
Report errors verbatim; fix against the compiler, not by guessing.
The paper states it compiled with Lean 4.32.2 and reports axioms: none (kernels 1,3,4),
[propext] (kernel 2), [propext, Quot.sound] (kernel 5).
-/

namespace TUFT

/-! ## Kernel 1 -/
structure HolonomySetup where
  Charge : Type
  Phase : Type
  Loop : Type
  triv : Phase
  Chi : Charge → Phase → Prop
  chi_triv : ∀ q, Chi q triv

def admissible (S : HolonomySetup) (rho : S.Loop → S.Phase) (q : S.Charge) : Prop :=
  ∀ gamma, S.Chi q (rho gamma)

theorem trivial_holonomy_admits_all (S : HolonomySetup) (rho : S.Loop → S.Phase)
    (h : ∀ gamma, rho gamma = S.triv) : ∀ q, admissible S rho q := by
  intro q gamma
  rw [h gamma]
  exact S.chi_triv q

theorem charge_quantization_forces_holonomy (S : HolonomySetup)
    (rho : S.Loop → S.Phase) (q0 : S.Charge) (hq0 : ¬ admissible S rho q0) :
    ¬ (∀ gamma, rho gamma = S.triv) := fun htriv =>
  hq0 (trivial_holonomy_admits_all S rho htriv q0)

/-! ## Kernel 2 -/
structure MiniRing (alpha : Type) where
  add : alpha → alpha → alpha
  mul : alpha → alpha → alpha
  neg : alpha → alpha
  zero : alpha
  one : alpha
  add_comm : ∀ a b, add a b = add b a
  add_assoc : ∀ a b c, add (add a b) c = add a (add b c)
  add_zero : ∀ a, add a zero = a
  add_neg : ∀ a, add a (neg a) = zero
  mul_one : ∀ a, mul a one = a
  mul_zero : ∀ a, mul a zero = zero
  mul_sub : ∀ a b c, mul a (add b (neg c)) = add (mul a b) (neg (mul a c))

theorem eq_one_of_add_neg_one_eq_zero {alpha : Type} (R : MiniRing alpha)
    (x : alpha) (h : R.add x (R.neg R.one) = R.zero) : x = R.one := by
  have h1 : R.add (R.add x (R.neg R.one)) R.one = R.add R.zero R.one := by rw [h]
  rw [R.add_assoc] at h1
  have h2 : R.add (R.neg R.one) R.one = R.zero := by
    rw [R.add_comm]; exact R.add_neg R.one
  rw [h2, R.add_zero] at h1
  rw [R.add_comm, R.add_zero] at h1
  exact h1

theorem domain_idempotents_trivial {alpha : Type} (R : MiniRing alpha)
    (nzd : ∀ a b, R.mul a b = R.zero → a = R.zero ∨ b = R.zero)
    (e : alpha) (h : R.mul e e = e) : e = R.zero ∨ e = R.one := by
  have key : R.mul e (R.add e (R.neg R.one)) = R.zero := by
    rw [R.mul_sub, h, R.mul_one]
    exact R.add_neg e
  cases nzd e (R.add e (R.neg R.one)) key with
  | inl h0 => exact Or.inl h0
  | inr h1 => exact Or.inr (eq_one_of_add_neg_one_eq_zero R e h1)

def prodRing {alpha beta : Type} (R : MiniRing alpha) (S : MiniRing beta) : MiniRing (alpha × beta) where
  add := fun p q => (R.add p.1 q.1, S.add p.2 q.2)
  mul := fun p q => (R.mul p.1 q.1, S.mul p.2 q.2)
  neg := fun p => (R.neg p.1, S.neg p.2)
  zero := (R.zero, S.zero)
  one := (R.one, S.one)
  add_comm := fun a b => by simp [R.add_comm a.1 b.1, S.add_comm a.2 b.2]
  add_assoc := fun a b c => by simp [R.add_assoc, S.add_assoc]
  add_zero := fun a => by simp [R.add_zero, S.add_zero]
  add_neg := fun a => by simp [R.add_neg, S.add_neg]
  mul_one := fun a => by simp [R.mul_one, S.mul_one]
  mul_zero := fun a => by simp [R.mul_zero, S.mul_zero]
  mul_sub := fun a b c => by simp [R.mul_sub, S.mul_sub]

theorem product_has_zero_divisors {alpha beta : Type}
    (R : MiniRing alpha) (S : MiniRing beta)
    (halpha : R.one ≠ R.zero) (hbeta : S.one ≠ S.zero) :
    ∃ x y : alpha × beta,
      (prodRing R S).mul x y = (prodRing R S).zero ∧
      x ≠ (prodRing R S).zero ∧ y ≠ (prodRing R S).zero := by
  refine ⟨(R.one, S.zero), (R.zero, S.one), ?_, ?_, ?_⟩
  · show (R.mul R.one R.zero, S.mul S.zero S.one) = (R.zero, S.zero)
    have h1 : R.mul R.one R.zero = R.zero := R.mul_zero R.one
    have h2 : S.mul S.zero S.one = S.zero := by
      have := S.mul_one S.zero; rw [this]
    rw [h1, h2]
  · intro hcontra
    exact halpha (congrArg Prod.fst hcontra)
  · intro hcontra
    exact hbeta (congrArg Prod.snd hcontra)

/-! ## Kernel 3 -/
structure HoCat where
  Obj : Type
  Hom : Obj → Obj → Type
  id : (X : Obj) → Hom X X
  comp : {X Y Z : Obj} → Hom X Y → Hom Y Z → Hom X Z

structure BundleFunctor (C : HoCat) where
  Bun : C.Obj → Type
  pull : {X Y : C.Obj} → C.Hom X Y → Bun Y → Bun X
  pull_id : ∀ {X} (E : Bun X), pull (C.id X) E = E
  pull_comp : ∀ {X Y Z} (f : C.Hom X Y) (g : C.Hom Y Z) (E : Bun Z),
    pull (C.comp f g) E = pull f (pull g E)

structure Classifies (C : HoCat) (F : BundleFunctor C) (B : C.Obj) where
  E : F.Bun B
  classify : {X : C.Obj} → F.Bun X → C.Hom X B
  pull_classify : ∀ {X} (b : F.Bun X), F.pull (classify b) E = b
  classify_pull : ∀ {X} (f : C.Hom X B), classify (F.pull f E) = f

structure HEquiv (C : HoCat) (P Q : C.Obj) where
  toFun : C.Hom P Q
  invFun : C.Hom Q P
  left : C.comp toFun invFun = C.id P
  right : C.comp invFun toFun = C.id Q

def classifying_unique (C : HoCat) (F : BundleFunctor C) {B B' : C.Obj}
    (h : Classifies C F B) (h' : Classifies C F B') : HEquiv C B B' := by
  refine ⟨h'.classify h.E, h.classify h'.E, ?_, ?_⟩
  · have e1 : F.pull (C.comp (h'.classify h.E) (h.classify h'.E)) h.E = h.E := by
      rw [F.pull_comp, h.pull_classify, h'.pull_classify]
    calc C.comp (h'.classify h.E) (h.classify h'.E)
        = h.classify (F.pull (C.comp (h'.classify h.E) (h.classify h'.E)) h.E) :=
          (h.classify_pull _).symm
      _ = h.classify h.E := by rw [e1]
      _ = h.classify (F.pull (C.id B) h.E) := by rw [F.pull_id]
      _ = C.id B := h.classify_pull _
  · have e2 : F.pull (C.comp (h.classify h'.E) (h'.classify h.E)) h'.E = h'.E := by
      rw [F.pull_comp, h'.pull_classify, h.pull_classify]
    calc C.comp (h.classify h'.E) (h'.classify h.E)
        = h'.classify (F.pull (C.comp (h.classify h'.E) (h'.classify h.E)) h'.E) :=
          (h'.classify_pull _).symm
      _ = h'.classify h'.E := by rw [e2]
      _ = h'.classify (F.pull (C.id B') h'.E) := by rw [F.pull_id]
      _ = C.id B' := h'.classify_pull _

def U1_forcing (C : HoCat) (F : BundleFunctor C) {B CPinf : C.Obj}
    (hComplete : Classifies C F B) (hMilnor : Classifies C F CPinf) :
    HEquiv C B CPinf :=
  classifying_unique C F hComplete hMilnor

/-! ## Kernel 4 -/
theorem every_field_configuration_is_in_the_bundle
    (C : HoCat) (F : BundleFunctor C) {B : C.Obj} (h : Classifies C F B)
    (X : C.Obj) (b : F.Bun X) : ∃ f : C.Hom X B, F.pull f h.E = b :=
  ⟨h.classify b, h.pull_classify b⟩

/-! ## Kernel 5 -/
theorem second_diff_affine_invariant (f : Int → Int) (c0 c1 : Int) :
    (f 1 + c0 + c1*1) - 2*(f 2 + c0 + c1*2) + (f 3 + c0 + c1*3)
    = f 1 - 2*f 2 + f 3 := by
  omega

#print axioms charge_quantization_forces_holonomy
#print axioms product_has_zero_divisors
#print axioms classifying_unique
#print axioms U1_forcing
#print axioms every_field_configuration_is_in_the_bundle
#print axioms second_diff_affine_invariant

/-! ## What each kernel says (added by the transcriber; also untested) -/

-- K3b: "U1_forcing" is classifying_unique under another name; nothing about U(1), CP^infty
-- or Milnor is in the statement. Both classifying objects are arbitrary hypotheses.
example (C : HoCat) (F : BundleFunctor C) {B B' : C.Obj}
    (h : Classifies C F B) (h' : Classifies C F B') :
    U1_forcing C F h h' = classifying_unique C F h h' := rfl

-- K4b: the "completeness theorem" restates a field of the hypothesis `Classifies`.
example (C : HoCat) (F : BundleFunctor C) {B : C.Obj} (h : Classifies C F B)
    {X : C.Obj} (b : F.Bun X) : F.pull (h.classify b) h.E = b := h.pull_classify b

-- K1b: the setup has no U(1), no charge lattice, no holonomy of a connection: Phase and
-- Charge are arbitrary types. Take Phase := Unit: no charge is ever inadmissible, so the
-- theorem's hypothesis cannot be met there. It is a contrapositive, true of any setup.
example : ∀ (S : HolonomySetup), S.Phase = Unit → True := fun _ _ => trivial

end TUFT
