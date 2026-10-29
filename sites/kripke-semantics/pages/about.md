# About this project

**[Boarders/kripke-semantics](https://github.com/Boarders/kripke-semantics)** by Callan McGill is a Lean 4 +
Mathlib development of the semantics of **intuitionistic propositional logic**. The upstream README is a
single heading ("kripke"), so this page describes the project from its source. The commit history (March to
June 2026) is the author's own.

## What the Lean covers (at the pinned commit)

Intuitionistic logic is logic without the law of excluded middle. Its standard semantics, due to Kripke
(1965) and, earlier, Beth (1956), replaces "true or false" with "established at a state of knowledge, and
still established at every later state". The project formalises one proof system and two semantics, and
proves each semantics sound and complete for it.

1. **Logic/Syntax.lean.** [Formulas](#/node/Syntax.Tm), [contexts](#/node/Syntax.Ctxt) and
   [natural-deduction proofs](#/node/Syntax.Pf), plus [multicut](#/node/Syntax.Pf.multicut).
2. **Kripke/Frame.lean.** [Kripke frames](#/node/Kripke.Frame), [forcing](#/node/Kripke.at_world) and
   [semantic consequence](#/node/Kripke.SemEntails), with a semantic version of each proof rule.
3. **Kripke/Soundness.lean.** [Soundness](#/node/Kripke.soundness), then two countermodels:
   [consistency](#/node/Kripke.Consistency.consistency) and
   [excluded middle is not provable](#/node/Kripke.ExcludedMiddle.em_not_provable).
4. **Kripke/Completeness.lean.** The canonical model of [prime theories](#/node/Kripke.Canonical.ProvableFrom),
   the [prime extension lemma](#/node/Kripke.Canonical.prime_extension_avoiding) (Zorn), the
   [truth lemma](#/node/Kripke.Canonical.truth_lemma) and [completeness](#/node/Kripke.completeness).
5. **Beth/Coverage.lean and Beth/Semantics.lean.** A general version of Beth semantics phrased with
   [sieves](#/node/Beth.Sieve) and [coverages](#/node/Beth.Coverage) (the vocabulary of Grothendieck
   topologies), [Beth frames](#/node/Beth.BethFrame) and [Beth forcing](#/node/Beth.at_world).
6. **Beth/Soundness.lean and Beth/Completeness.lean.** [Beth soundness](#/node/Beth.soundness) and
   [Beth completeness](#/node/Beth.Completeness.completeness), the latter via a canonical model of finite
   consistent contexts, with no Zorn's lemma.
7. **Beth/BethTrees.lean and Beth/Examples.lean.** Classical Beth trees with
   [bars](#/node/Beth.BethTrees.BethTreeCoverage) as an instance; Kripke frames as Beth frames; and a
   binary-tree model where [P ∨ Q holds at the root](#/node/Beth.Examples.BinaryBitsTree.binaryBranchVal)
   though neither P nor Q does.
8. **Kripke/Examples.lean.** [Open sets of a topological space](#/node/Kripke.opensFrame) as a Kripke frame
   (construction only).

## Where to start

If you know some logic, go straight to [Kripke forcing](#/node/Kripke.at_world) and
[em_not_provable](#/node/Kripke.ExcludedMiddle.em_not_provable): together they show the whole idea in a
three-world picture. Then compare the two completeness proofs: [Kripke](#/node/Kripke.completeness) (infinite
prime theories, Zorn) and [Beth](#/node/Beth.Completeness.completeness) (finite contexts, a coverage generated
by provable disjunctions).

## What this site leaves out

- **Kripke/Syntax.lean**, an earlier fragment (∧, ⇒, true only) that nothing imports. It is mentioned on the
  [formulas](#/node/Syntax.Tm) page but has no nodes of its own.
- Most bookkeeping lemmas about snoc-lists in Beth/BethTrees.lean, and small helper lemmas such as
  `provable_merge`, `chain_member_for_ctxt` and the disjunction-of-a-list lemmas. They are described inside the
  nodes that use them.
- The top-level files Semantics.lean, Kripke.lean, Beth.lean and Logic.lean only import the others.
