# Review: do the statements say what they claim?

This page compares each headline's Lean statement with what its name, the README or the lecture notes claim. Nothing
here was checked by building the Lean.

## generalResolution_soundness: complete, faithful, slightly restricted in form

- **Claim (README):** soundness of the resolution rules in first-order logic.
- **Statement:** for all A, B, C, D, σ, the two-inference list [general resolution, general factorisation] is
  [sound](#/node/Inferences.Soundness): when σ is an mgu of A ≐ B, the premises entail the conclusion, with each
  clause read as universally quantified ([ClauseSetEntails](#/node/Models.ClauseSetEntails)). That is the right notion.
- **Per instance.** An [inference system](#/node/Inferences.Inference) is a finite list of concrete inferences, so
  soundness is proved one instance at a time. Since every instance is covered, this is the same as soundness of the
  rule schemas. A theorem saying "every multi-step resolution derivation is sound" would combine this with
  [generalSoundness_of_soundness](#/node/Inferences.generalSoundness_of_soundness) for the list of instances used. That
  combination is easy but not written down.
- **Literal position.** The resolved literals must be the first elements of the clause lists. Semantically nothing is
  lost (clauses are disjunctions), but a derivation using a literal in the middle needs a reordering step that the
  project's inference systems don't include.
- **Stronger than stated.** The mgu condition is used only through Aσ = Bσ. Soundness holds for any unifier.
- **No renaming apart.** The rule doesn't require the premises to have disjoint variables. That is fine for soundness.

## groundResolution_soundness: complete, faithful

Ground resolution (A ∨ C, ¬A ∨ D ⟹ C ∨ D) and ground factorisation (A ∨ A ∨ C ⟹ A ∨ C) are sound, for variable-free
clauses (variable type `Empty`). Same remarks on per-instance form and literal position as above.

## generalSoundness_of_soundness: complete, faithful

"If each inference is sound, then N ⊢ C implies N ⊨ C", for any inference system given as a list, with proofs as
lists of clauses where each premise appears earlier. This is the standard argument.

## Formula.eval_of_closed: complete, faithful

A closed formula has the same value under every assignment (for a fixed interpretation). The proof goes through the
stronger [eval_of_many_free](#/node/Semantics.Formula.eval_of_closed), as the comments explain.

## idempotent_iff_inter_empty: complete, faithful

σ ∘ σ = σ iff dom(σ) ∩ codom(σ) = ∅. The project allows substitutions that move infinitely many variables; the
theorem still holds and is proved in that generality.

## unifiable_iff_mgu_idempot: PARTIAL (sorry)

The forward direction, "every unifiable problem has an idempotent mgu using only its own variables", is the real
content of the main unification theorem, and it is `sorry` (InferenceInLean/D_Unification.lean line 63). The authors say
so in a comment. The backward direction is trivial. So the name `main_unification_theorem` should be read as "the
statement of", not "a proof of". The resolution results don't depend on it.

## Modelling choices worth knowing

- **No arities.** [Signatures](#/node/Syntax.Signature) don't fix arities; interpretations act on lists of any
  length. This is a generalisation and doesn't affect soundness.
- **Universes can be empty, and are fixed per statement.** The universe type is a parameter of `Valid`, `Entails`,
  `Soundness` etc., rather than quantified inside them, and nothing requires it to be non-empty. All the theorems are
  stated for an arbitrary universe, so they hold for all of them.
- **Lemma 3.3.5 only for clauses.** `three_three_five` is the substitution lemma for clauses, not arbitrary formulas.
  That is enough for resolution.
- **Lemma 3.3.7 slightly stronger.** It doesn't require F to be closed (as the authors note).

## Surprises

None that affect correctness. The numbering of lemmas after the notes is helpful for anyone reading alongside them.
