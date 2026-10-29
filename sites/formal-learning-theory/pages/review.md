# Review: are the statements faithful?

For each headline: what the name, README or literature suggests, what the Lean actually says, and the gaps. None of
the headlines is sorry'd. Two kinds of qualification come up: **CONDITIONAL** (extra hypotheses) and **weaker than the
name**.

## 1. `fundamental_theorem`: CONDITIONAL, and partly weaker than the textbook

Theorem/PAC.lean lines 293–329. [Node](#/node/fundamental_theorem).

**What is right.**

- [PACLearnable](#/node/PACLearnable) is the standard realizable, distribution-free definition: L and the sample
  size mf(ε, δ) are chosen before the distribution D and the target c, and the sample really is i.i.d. (Mathlib's
  `Measure.pi`). The project documents an earlier, existentially-quantified version that made the notion trivial and
  was repaired (Criterion/PAC.lean lines 26–37).
- VC dimension, shattering and the growth function are the textbook notions.
- The PAC ⟹ finite VC direction needs only measurable singletons and works against an arbitrary (not necessarily
  measurable) learner.
- The compression conjunct is the genuine Moran–Yehudayoff theorem. The Rademacher conjunct is uniform over
  distributions, and its converse produces explicit distributions, so the integral's junk-value convention cannot
  make it vacuous.

**The measurability assumption (CONDITIONAL).** `[MeasurableConceptClass X C]` contains
`all_measurable : ∀ c : X → Bool, Measurable c` (Complexity/Measurability.lean line 65). That is: **every subset of X
is measurable.** It holds on countable domains with the discrete σ-algebra, and the separation witnesses on ℕ check
everything by hand. It fails on ℝⁿ with the Borel σ-algebra, as the file's own docstring says
(Complexity/Measurability.lean lines 125–140). So, read literally, the theorem does not cover thresholds, intervals or
half-spaces on ℝⁿ under Borel distributions. That is a real restriction compared with the textbook
(Shalev-Shwartz & Ben-David, Thm 6.7, which also glosses over measurability, and Blumer et al. 1989, which assume
well-behavedness). The README's measurability contributions (the Borel-analytic bridge and the separation from
Krapp–Wirth) concern the *other* field, `wellBehaved`, in Borel settings. They do not discharge `all_measurable`,
and no PAC theorem in the pinned source takes their weaker condition as its hypothesis. See
[the measurability group](#/node/exists_measTarget_separation).

To be fair, `all_measurable` is used because PACLearnable quantifies over arbitrary targets and arbitrary learner
outputs, whose disagreement sets must be measurable. Restricting to measurable targets and learners would be the
natural next step. As stated, the README's phrase "for a concept class C over a measurable space X" needs this
qualification.

**Weaker than the textbook.**

- **Realizable only.** No agnostic PAC, although `AgnosticPACLearnable` is defined.
- **Uniform convergence is not a conjunct.** It is proved inside the proof, not stated.
- **The "quantitative sandwich" is weak.** The lower bound ⌈(d − 1)/2⌉ has no ε (the classical bound is
  Ω((d + log(1/δ))/ε)). The "upper bound" is only "SampleComplexity ≤ the witness's mf", with no formula. The
  witness built in the proof needs about (16e(d+1)/ε²)^(d+1)/δ samples
  (Complexity/Symmetrization.lean line 2891), polynomial in 1/δ rather than logarithmic. That is fine for the
  qualitative equivalence, but it is not the classical sample complexity.
- **The ⌈(d − 1)/2⌉ docstring mismatch.** The docstring of `pac_lower_bound` (Theorem/PAC.lean lines 159–172)
  says "linear in d/ε" and "m ≥ ⌈(d−1)/(64ε)⌉", but the statement is ⌈(d − 1)/2⌉.

## 2. `vc_characterization`: CONDITIONAL (same measurability assumption)

Theorem/PAC.lean lines 127–132. [Node](#/node/vc_characterization). Faithful to "realizable PAC ⟺ finite VC" under
the measurability assumption above. The proof is the classical one (uniform convergence via symmetrization, then a
consistent learner; conversely a no-free-lunch argument on a shattered set).

## 3. `fundamental_vc_compression_with_info`: faithful, no extra hypotheses

Complexity/Compression.lean lines 1321–1326. [Node](#/node/fundamental_vc_compression_with_info). The structure
[CompressionSchemeWithInfo](#/node/CompressionSchemeWithInfo) matches Moran–Yehudayoff's "κ : LC(∞) → LC(k) × I, I
finite", with correctness only on C-realizable samples (which is what the paper requires). Purely combinatorial: no
measurability at all. The statement gives existence only, no size bound in d. The project is explicit that the
version without side information (Littlestone–Warmuth) remains open (`Open_NoInfoCompressionStrengthening` is a
`Prop`, not a theorem).

## 4. `littlestone_characterization`: faithful

Theorem/Online.lean lines 419–422. [Node](#/node/littlestone_characterization). Realizable mistake-bound model with
deterministic learners and arbitrary finite sequences, and Littlestone's path-wise tree definition. Also proved: the
optimal mistake bound equals the Littlestone dimension (lines 440–502). The domain is restricted to `X : Type`
(universe 0), which is harmless.

## 5. `gold_theorem`: faithful (strong form)

Theorem/Gold.lean lines 19–201. [Node](#/node/gold_theorem). Classes containing every finite set and one infinite set
are not identifiable in the limit from text, for arbitrary (non-computable) learners. Two modelling differences from
Gold (1967), neither weakening the result: convergence is to the concept as a function (no program indices), and a
text must emit a positive example at every step (no pause symbol, so the empty concept has no text). Countable X is
assumed, as usual.

## 6. `online_pac_gold_separation`: faithful

Theorem/Separation.lean lines 1358–1363. [Node](#/node/online_pac_gold_separation). Concrete witnesses on ℕ:
thresholds (PAC, not online), finite-set indicators (EX from text, not PAC). The companion `online_imp_pac` is under
`MeasurableConceptClass`. `ex_strictly_stronger_finite` (lines 1335–1342) proves only the inclusion, despite its name.

## Other things worth knowing

- **Names stronger than statements.** `occam_algorithm` does not use its description-length hypothesis and follows
  from an added VCDim < ⊤ hypothesis. `sauer_shelah` (Theorem/PAC.lean lines 153–157) is trivially true and labelled
  "legacy". `gold_does_not_imply_pac` (Complexity/Generalization.lean lines 1013–1016) has statement `True`.
  `baxter_full` proves only the n-independent bound. `nfl_fixed_sample` gives positive probability of failure, not
  the textbook constant. `pac_bayes_finite` uses cross-entropy instead of KL and needs finite H. In most cases the
  project's own docstrings say so.
- **Conditional results.** `exists_measTarget_separation` assumes an analytic non-Borel subset of ℝ. Several
  IndependentVC theorems are explicit reductions to named missing lemmas.
- **Mind changes.** `mind_change_characterization` is nearly definitional, because `MindChangeOrdinal` builds
  correct convergence into its definition. The README acknowledges this.
- **README numbers are out of date.** The table says 21,728 lines, 53 files and 354 theorems. The pinned library has
  about 29,900 lines in 102 files. The difference is mostly the IndependentVC/ folder.
- **Stale comments.** Several comments still talk about sorrys that are no longer in the code (for example
  Complexity/Symmetrization.lean lines 1015–1028, Complexity/Generalization.lean lines 2843–2845, Theorem/PAC.lean
  line 375, Theorem/Separation.lean lines 790–799). A comment-aware search finds no `sorry` in compiled code; see
  [Trust](#/trust).
