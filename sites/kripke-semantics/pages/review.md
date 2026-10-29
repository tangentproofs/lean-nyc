# Review: are the headline statements faithful?

This page checks, for each headline, that the Lean statement says what its name suggests. The Lean was
**not built** for this review; see [Trust](#/trust). The upstream README makes no claims, so the comparison is
with the standard textbook theorems.

## Kripke.soundness

**Faithful.** If Γ ⊢ φ in natural deduction, then in every Kripke frame (any type, any universe), every world
forcing Γ forces φ (Kripke/Soundness.lean lines 11–46). This is the textbook statement. Forcing
(Kripke/Frame.lean lines 16–23) uses the standard clauses, with implication quantifying over all future
worlds. The proof system (Logic/Syntax.lean lines 30–43) is standard NJ for the full propositional language
(∧, ∨, ⇒, ⊤, ⊥), with ¬φ defined as φ ⇒ ⊥.

## Kripke.completeness

**Faithful, as finite-premise ("weak") completeness.** If Γ ⊨ φ over all Kripke frames whose worlds form an
ordinary type (universe 0), then Γ ⊢ φ (Kripke/Completeness.lean lines 501–503). Points to note:

- Γ is a finite list. Completeness for infinite sets of premises (strong completeness) is not stated, though
  the proof's machinery (theories as sets) is almost there.
- The universe restriction to level 0 is natural, and it makes the hypothesis *weaker* (fewer frames to
  check), so it is not a cheat.
- The proof is classical (Zorn's lemma, `open Classical` at line 7). This is the standard canonical-model
  proof, not a constructive one.
- No finite-model property or decidability result is claimed.

## Kripke.ExcludedMiddle.em_not_provable

**Faithful.** The specific formula variable 0 ∨ (variable 0 ⇒ ⊥) has no proof from no assumptions
(Kripke/Soundness.lean lines 123–137). One instance suffices to show that excluded middle is not a derivable
schema. The argument is the standard countermodel; only two of its three worlds are needed.

## Beth.soundness

**Faithful, for a generalised notion of Beth model.** Here a "Beth frame" (Beth/Semantics.lean lines 11–13) is a
Kripke frame plus a coverage (sieves, as in a Grothendieck topology on a preorder), with the valuation
satisfying a sheaf condition and covers required to be non-empty. Classical Beth trees with bars are shown to
be an instance (Beth/BethTrees.lean lines 289–305), and so are Kripke frames (Beth/Examples.lean lines 21–32).
So this soundness theorem covers Beth's original models. The ∨ clause (Beth/Semantics.lean lines 25–26) is the
standard "some bar/cover decides it" clause.

## Beth.Completeness.completeness

**Faithful, as finite-premise completeness for the generalised Beth frames.** If Γ ⊨ φ over all Beth frames in
universe 0, then Γ ⊢ φ (Beth/Completeness.lean lines 289–297).

- The canonical frame is built from finite consistent contexts, and its coverage is *defined* from provable
  disjunctions (lines 82–92). That is legitimate: completeness only needs one frame in the class where all
  unprovable sequents fail. But it means the theorem does **not** say "complete for Beth *trees*". The
  canonical frame is not shown to be a tree, so completeness with respect to tree models specifically is not
  proved.
- No Zorn's lemma. Classical case splits on provability (lines 163, 243, 291) and choice in `sheaf_term`
  (Beth/Semantics.lean line 71) are used, so the proof is not constructive either.

## A possible compile problem

Reading Beth/Coverage.lean line 33 (inside `pullback`), the proof of the "bounded" field returns a name that
is not bound anywhere visible. If this is a typo, Beth/Coverage.lean does not compile at the pinned commit,
and so neither does anything in the Beth half (both Beth headlines depend on it). The intended proof is
evident from the neighbouring binder. This site did not build the Lean and cannot confirm either way.

## Smaller observations

- Soundness theorems are declared as `def` rather than `theorem`. Their types are propositions, so this changes
  nothing mathematically.
- The comment that P ∨ Q fails at the root of the binary tree "in the underlying Kripke frame"
  (Beth/Examples.lean line 49) is not proved in Lean. Neither is the agreement between Beth forcing and Kripke
  forcing in the Kripke-as-Beth frame.
- Kripke/Syntax.lean is an unused earlier fragment with its own, different formula type.
