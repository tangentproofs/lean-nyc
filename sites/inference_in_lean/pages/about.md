# About this site

## The project

[SamuelLess/inference_in_lean](https://github.com/SamuelLess/inference_in_lean) is a Lean 4 + Mathlib project by
**Norman Lohrer** and **Samuel Leßmann**, written during the course "Formalization in Lean" taught by Xavier Généreux
at LMU Munich in 2024/25 (README). In the README's words, it "formalizes the basics of first-order logic and proves
soundness of the common resolution rules in propositional and first-order logic", closely following Chapter 3 of the
lecture notes of LMU's [Automated Theorem Proving](https://www.tcs.ifi.lmu.de/lehre/ws-2024-25/atp_de.html) course.
The file and lemma names track the notes' section and lemma numbers (for example `three_three_seven` is Lemma 3.3.7).

## What the Lean covers

The library is about 2,200 lines in seven files, InferenceInLean/A_Syntax.lean to InferenceInLean/G_Examples.lean:

1. **Syntax** (A_Syntax.lean, notes §3.1). [Signatures](#/node/Syntax.Signature), [terms](#/node/Syntax.Term),
   [atoms and literals](#/node/Syntax.Atom), [formulas](#/node/Syntax.Formula), [clauses](#/node/Syntax.Clause),
   free variables, universal closure, and [substitutions](#/node/Syntax.Substitution), with the headline
   [σ is idempotent iff dom ∩ codom = ∅](#/node/Syntax.idempotent_iff_inter_empty).
2. **Semantics** (B_Semantics.lean, §3.2). [Interpretations and assignments](#/node/Semantics.Interpretation),
   [evaluation](#/node/Semantics.Formula.eval), and the headline that
   [a closed formula's value doesn't depend on the assignment](#/node/Semantics.Formula.eval_of_closed).
3. **Models** (C_Models.lean, §3.3). [Validity and satisfiability](#/node/Models.ValidIn),
   [entailment](#/node/Models.Entails), [clause-set entailment](#/node/Models.ClauseSetEntails), the
   [substitution lemma](#/node/Models.substitution_lemma) and [Lemmas 3.3.7–3.3.8](#/node/Models.three_three_seven).
4. **Unification** (D_Unification.lean). [Unifiers and mgus](#/node/Unification.Unifier), and the
   [main unification theorem](#/node/Unification.unifiable_iff_mgu_idempot), whose hard direction is `sorry`.
5. **Inference systems** (E_Inference.lean, §3.7). [Inferences](#/node/Inferences.Inference),
   [proofs](#/node/Inferences.Proof), [two notions of soundness](#/node/Inferences.Soundness), and the headline that
   [sound steps give sound proofs](#/node/Inferences.generalSoundness_of_soundness).
6. **Resolution** (F_Resolution.lean, §3.8 and §3.10). [Ground](#/node/Resolution.GroundResolution) and
   [general](#/node/Resolution.GeneralResolutionRule) resolution and [factorisation](#/node/Resolution.GeneralFactorizationRule),
   and the headlines [ground resolution is sound](#/node/Resolution.groundResolution_soundness) and
   [general resolution is sound](#/node/Resolution.generalResolution_soundness).
7. **Examples** (G_Examples.lean). A small Peano-arithmetic signature and interpretation on ℕ, with a formula evaluated
   by hand, and repeats of the Proposition 3.3.3 dualities. This site doesn't explain it node by node.

**Left out.** The InferenceInLean/Exercises folder (about 330 lines) has solutions to course exercise sheets 4 and 5
(finding models, Herbrand interpretations).
It isn't imported by the library root and isn't covered here. Neither is G_Examples.lean imported by the root file
InferenceInLean.lean, which imports only F_Resolution.lean (and through it A–E).

**Not covered by the project:** completeness of resolution, a unification algorithm, Herbrand's theorem, and
clause-normal-form transformation.

## Where to start

Read the [main headline](#/node/Resolution.generalResolution_soundness), then the definitions it rests on:
[ClauseSetEntails](#/node/Models.ClauseSetEntails) (what "true" means for a clause with variables) and
[Soundness](#/node/Inferences.Soundness). The [review](#/review) says how faithful each statement is to the notes.
