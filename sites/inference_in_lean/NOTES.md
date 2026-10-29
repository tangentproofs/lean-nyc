# NOTES for the coordinator (not published)

## Time spent

About 1.5 hours: reading all ~2,540 lines of Lean (library and exercises), writing 45 nodes and three pages, plus
build iterations.

## Decisions I made (no questions asked)

- **Authors.** The README says "Created by Norman Lohrer and Samuel Leßmann during the course 'Formalization in Lean'
  taught by Xavier Généreux at LMU in 2024/25". I set `authors` to "Norman Lohrer and Samuel Leßmann". `members` was
  left as given ("Samuel Leßmann").
- **Licence.** The LICENSE file is present and the README says GPL v3, so I left `license` unchanged. Short verbatim
  proof lines are used in walkthroughs.
- **Roots.** Only A_Syntax … G_Examples. The Exercises folder (course sheet solutions, ~330 lines) is left out; the
  About page says so. G_Examples is scanned but has no nodes.
- **Headlines (6).** generalResolution_soundness, groundResolution_soundness, generalSoundness_of_soundness,
  Formula.eval_of_closed, idempotent_iff_inter_empty, unifiable_iff_mgu_idempot (labelled PARTIAL, sorry).
- **Small nodes.** Several minor statement-set definitions (domain, codomain, Idempotent, EqualityProblem, …) got short
  stub nodes in nodes_src/z_extra.py, which point to the grouped node that explains them. z_extra.py also holds extra
  quiz questions, which the other files load and append. The remaining "no explainer" warnings (Variables, Universes,
  EntailsInterpret, Term.eval, Atom.eval, bigForall, freeVars, …) are all explained inside grouped nodes.

## What was hard

- Explaining why the soundness statement is "per inference instance": `InferenceSystem` is a finite `List` of concrete
  inferences, so a rule schema like resolution can't be one system. I explained it as "for all A, B, C, D, σ the two
  instances are sound", which is equivalent to soundness of the rules. I also noted that the combination with
  generalSoundness_of_soundness for multi-step derivations isn't stated as a single theorem.
- Keeping the two entailment notions straight (`Entails`: one shared assignment; `ClauseSetEntails`: each clause
  universally quantified on its own).

## Where I am least sure

- **Resolution.generalResolutionRuleSound / generalResolution_soundness, "only the unifier part of the mgu is
  used".** I read `hBσeqAσ … := by aesop` (F_Resolution.lean lines 174–175) as the only use of `hmgu`, and the
  factorisation proof's final `aesop` likewise. Without a build I can't confirm aesop doesn't use something else, but
  mathematically a unifier is clearly enough.
- **Syntax.Term / trust page.** `Term.induction` (A_Syntax.lean lines 36–51) is proved by calling itself recursively
  inside a tactic block. I assume Lean accepts the termination argument, since the project presumably builds, but I
  didn't check.
- **Trust page, "G_Examples and Exercises are not built by default".** Based on InferenceInLean.lean importing only
  F_Resolution and the lakefile using the default lib roots. If the authors build those files another way, this remark
  is wrong but harmless.
- **unifiable_iff_mgu_idempot.** I call the forward direction true classically (Robinson). With this project's
  definitions (substitutions with infinite domain allowed; MoreGeneral as equality of functions on all variables), I
  believe it is still true but didn't work through the edge cases.
- **Models.ValidIn, "universe fixed per statement".** Correct reading of the `variable {univ}` section variables, I
  believe. I present it as a modelling choice, not a flaw.
- **Inferences.generalSoundness_of_soundness, base case.** I wrote "Index 0: an assumption, or an inference with no
  earlier premises". That is my reading of what `aesop` must handle at E_Inference.lean lines 78–79.

## Anything the author might object to

- Calling the main unification theorem PARTIAL and saying its name should be read as "statement of". That is accurate,
  and their own comment admits it, but it is visible.
- The remarks that the resolved literal must be at the front of the clause list, that premises aren't renamed apart,
  and that the multi-step soundness corollary isn't stated. These are framed as scope notes, not errors.
- The remark that the Exercises header mentions AI assistance for one exercise (About page). It is factual and
  quoted from the source, but the authors may not want it highlighted. It is easy to drop.

## Engine notes

No engine bugs hit. The build prints "built _site/inference_in_lean" with 20 minor "no explainer yet" warnings.
