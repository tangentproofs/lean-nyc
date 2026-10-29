import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import node_maker, q, walk, S, NOT_BUILT, MEAS

NODES = []
node = node_maker(NODES)

# Grouped nodes: each is anchored on one representative declaration and summarises a part of the library that
# is not on the main dependency spine of the headlines.


node("exists_measTarget_separation",
 "Group: measurability theory (null-measurable bad events, Borel–analytic gap)",
 "Proved: analytic sets are null-measurable (via Choquet capacitability), so Borel-parameterized classes have "
 "null-measurable bad events, and, given an analytic non-Borel subset of ℝ, this is strictly weaker than Krapp–Wirth's "
 "condition. These results do not feed the headlines.",
 r"""## Plain English

**Representative theorem (`exists_measTarget_separation`, Theorem/BorelAnalyticSeparation.lean lines 368–372).**
*If* there is an analytic subset of ℝ that is not Borel, then `KrappWirthSeparationMeasTarget` holds: there is a
class C on ℝ of measurable concepts for which the null-measurability condition `WellBehavedVCMeasTarget` holds but
the Krapp–Wirth condition `KrappWirthWellBehaved` fails (Complexity/Measurability.lean lines 422–426).

That is **CONDITIONAL**: the existence of an analytic non-Borel set (Suslin, 1917) is a hypothesis, not proved in
the file. The proof itself is `analytic_nonborel_set_gives_measTarget_separation` (lines 247–360): it uses
singleton classes {1_{a} : a ∈ A} (lines 31–47), whose bad event at m = 1 is a planar set that is analytic
(lines 165–184) but not measurable (lines 186–205).

### The supporting pure mathematics

- **Choquet capacitability** (PureMath/ChoquetCapacity.lean, about 440 lines): analytic sets are capacitable for
  the outer capacity of a finite measure; `MeasureTheory.AnalyticSet.cap_eq_iSup_isCompact` (lines 303–425).
- **Analytic ⟹ null-measurable** (`analyticSet_nullMeasurableSet`, PureMath/AnalyticMeasurability.lean
  lines 91–126). The README proposes both for Mathlib.
- **Borel parameterization** (Complexity/BorelAnalyticBridge.lean): if C = range of a jointly measurable
  evaluation map on a standard Borel parameter space, its bad event is analytic and so null-measurable
  (`borel_param_wellBehavedVCMeasTarget`, lines 213–234). Interpolation (Complexity/Interpolation.lean) and
  amalgamation (Complexity/Amalgamation.lean) preserve this.

### How it relates to the headlines

The [fundamental theorem](#/node/fundamental_theorem) requires [MeasurableConceptClass](#/node/MeasurableConceptClass),
whose `all_measurable` field (every subset of X measurable) fails on Borel ℝ. These Borel-setting results prove the
**measurable-target** variant `WellBehavedVCMeasTarget`, not `MeasurableConceptClass`. They are a separate,
self-contained contribution, not a hypothesis-discharge for the headline. The README is careful about the name: it
calls the property "the measurable-target variant used in the fundamental theorem pipeline", but in the pinned
source no PAC theorem takes `WellBehavedVCMeasTarget` as a hypothesis.
""",
 [q("Is exists_measTarget_separation unconditional?",
    ["No: it assumes an analytic, non-Borel subset of ℝ exists",
     "Yes",
     "It assumes the continuum hypothesis",
     "It assumes a measurable cardinal"], 0,
    "Theorem/BorelAnalyticSeparation.lean lines 368–370: hypothesis `hex : ∃ A : Set ℝ, AnalyticSet A ∧ ¬ MeasurableSet A`."),
  q("Do the Borel-parameterization results supply MeasurableConceptClass for classes on ℝ?",
    ["No: they give WellBehavedVCMeasTarget; MeasurableConceptClass also needs every subset of X to be measurable",
     "Yes",
     "Only for finite classes",
     "Only for countable ℝ"], 0,
    "Complexity/BorelAnalyticBridge.lean lines 213–218 conclude `WellBehavedVCMeasTarget X (Set.range e)`."),
  q("What does the separation show about Krapp–Wirth's condition?",
    ["Their MeasurableSet-style condition is strictly stronger than the null-measurability condition used here",
     "It is equivalent",
     "It is inconsistent",
     "It is weaker"], 0,
    "`KrappWirthSeparationMeasTarget` (Complexity/Measurability.lean lines 422–426): WellBehavedVCMeasTarget ∧ ¬ KrappWirthWellBehaved."),
 ],
 caveats=[NOT_BUILT, "CONDITIONAL: the analytic non-Borel set is an assumption of the theorem."])


node("pac_bayes_finite",
 "Group: PAC-Bayes for finite hypothesis sets",
 "For a finite hypothesis set with a prior P, with probability ≥ 1 − δ every posterior Q satisfies: Gibbs error ≤ "
 "empirical Gibbs error + √((CE(Q, P) + log(1/δ))/(2m)), where CE is the cross-entropy Σ Q log(1/P). This is the "
 "union-bound (Occam-style) form, slightly weaker than McAllester's KL form.",
 r"""## Plain English

**Theorem (`pac_bayes_finite`, Theorem/PACBayes.lean lines 466–498).** Let H be a finite nonempty index set of
measurable hypotheses, P a prior on H with all P(h) > 0, D a distribution, c a measurable target, m > 0 and
0 < δ ≤ 1. Then with Dᵐ-probability ≥ 1 − δ over the sample S, for **every** posterior Q on H,

  gibbsError(Q) ≤ gibbsEmpError(Q, S) + √((crossEntropy(Q, P) + log(1/δ)) / (2m)).

The proof:

1. Hoeffding for each h (`pac_bayes_per_hypothesis`, lines 69–190);
2. a union bound with confidence P(h)·δ for h, so that all h hold at once (`pac_bayes_all_hypotheses`,
   lines 191–…);
3. average over Q, using concavity of √ (Jensen) to pass to the Gibbs error (`gibbs_bound_of_pointwise`).

### Faithfulness

The README lists "PAC-Bayes bound (McAllester)". McAllester's theorem uses KL(Q‖P) and covers general
(possibly infinite) hypothesis spaces. Here H is finite and the complexity term is the cross-entropy
Σ Q(h) log(1/P(h)) = KL(Q‖P) + H(Q), which is **larger** than KL. So it is a weaker, union-bound version, as the
docstring itself says (lines 455–463, with a TODO for the tight version). It is still a genuine
"for all posteriors simultaneously" bound.
""",
 [q("What complexity term appears in the proved bound?",
    ["The cross-entropy Σ Q(h) log(1/P(h)), which equals KL(Q‖P) plus the entropy of Q",
     "KL(Q‖P)",
     "The VC dimension",
     "log |H|"], 0,
    "Theorem/PACBayes.lean line 477 and the docstring at lines 455–457."),
  q("Is the bound simultaneous over posteriors Q?",
    ["Yes: the event is ∀ Q, …",
     "No, Q is fixed before the sample",
     "Only for Q = P",
     "Only for point masses"], 0,
    "Lines 474–478: `{ S | ∀ (Q : FinitePMF H), … }`."),
  q("Does it cover infinite hypothesis spaces?",
    ["No: H must be a Fintype",
     "Yes",
     "Only countable ones",
     "Only for finite VC dimension"], 0,
    "Line 467: `{H : Type*} [Fintype H] [Nonempty H]`."),
 ],
 caveats=[NOT_BUILT,
  "Weaker than McAllester's KL bound (cross-entropy instead of KL; finite H only). The docstring says so."])


node("vcDim_fundamental_theorem",
 "Group: the independent VC-dimension development (about 8,000 lines)",
 "A newer body of VC theory built on the bare definitions: Boolean closures, Sauer–Shelah variants, dual VC "
 "dimension, Dudley's bound, half-spaces in ℝⁿ having VC dimension exactly n, structural capacity results, and a "
 "restatement of the fundamental theorem.",
 r"""## Plain English

The folder Complexity/IndependentVC/ (48 files, about 8,000 lines) is indexed in Complexity/IndependentVC.lean.
It is newer than the README's headline numbers (the README table still says 21,728 lines in 53 files; the pinned
library has about 29,900 lines in 102 files).

**Representative theorem (`vcDim_fundamental_theorem`, Complexity/IndependentVC/FundamentalTheorem.lean lines
60–65).** Under [MeasurableConceptClass](#/node/MeasurableConceptClass): VCDim < ⊤ ⟺ PACLearnable, and
VCDim < ⊤ ⟺ the growth function is eventually bounded by K·m^d. The PAC half is just
[vc_characterization](#/node/vc_characterization) reversed (line 56). The growth half is a new, purely combinatorial
proof.

Other highlights (all scanned, none explained in detail here):

- **Dudley's bound** `vcDim_signClass_le` (Complexity/IndependentVC/Dudley.lean): for a finite-dimensional space V
  of real functions, the class {x ↦ (f(x) ≥ 0) : f ∈ V} has VC dimension ≤ dim V.
- **Half-spaces** `FLT.Halfspace.vcDim_halfspace_eq` (Complexity/IndependentVC/Halfspace.lean lines 193–195):
  homogeneous half-spaces in ℝⁿ have VC dimension exactly n. (So they are PAC learnable *in principle*, but the
  headline PAC theorem does not apply to ℝⁿ with the Borel σ-algebra; see
  [MeasurableConceptClass](#/node/MeasurableConceptClass).)
- **Shattering as a game** `ExpressivityClosures.shatters_iff_adversary_forces`
  (Complexity/IndependentVC/ExpressivityClosures.lean lines 330–356).
- **VC dimension is not the universal relabel-invariant capacity**
  `StructureClosures.vcDim_not_universal_relabel_invariant_dual` (Complexity/IndependentVC/StructureClosures.lean
  lines 551–574): the dual VC dimension is relabel-invariant but not a function of VCDim.
- Growth-function algebra (sub-multiplicativity, unions), pseudodimension, packing, ε-net bridges, matroid
  witnesses, and "framework" files that organize capacities categorically.

Several files state **open** problems or **frontier reductions** as explicit hypotheses rather than `sorry` (for
example `hasse_open_reduction`, StructureClosures.lean lines 661–665, and the OpenRoute files). Those are honest
conditional statements, not proofs of the open problems.
""",
 [q("How does vcDim_fundamental_theorem get its PAC equivalence?",
    ["By reusing vc_characterization from Theorem/PAC.lean",
     "By a new symmetrization proof",
     "By compression",
     "It assumes it"], 0,
    "Complexity/IndependentVC/FundamentalTheorem.lean lines 53–56: `(vc_characterization X C).symm`."),
  q("What does the library prove about homogeneous half-spaces in ℝⁿ?",
    ["Their VC dimension is exactly n",
     "Their VC dimension is n + 1",
     "They are online learnable",
     "They are not PAC learnable"], 0,
    "Complexity/IndependentVC/Halfspace.lean lines 193–195."),
  q("How are open problems handled in this folder?",
    ["As explicit hypotheses (conditional statements) or as Prop definitions, not as sorry",
     "With sorry",
     "With axioms",
     "They are claimed as solved"], 0,
    "e.g. `hasse_open_reduction` takes the missing lemma as hypothesis `hmb` (StructureClosures.lean lines 661–663)."),
 ],
 caveats=[NOT_BUILT, MEAS])


node("mind_change_characterization",
 "Group: more inductive inference (mind changes, finite vs EX learning)",
 "The Gold-style files also prove that EX-learnability is equivalent to a finite 'mind change ordinal' on every "
 "text, and that finite learning implies EX-learning. The first is near-definitional: the ordinal is defined to be "
 "finite exactly when the learner converges correctly.",
 r"""## Plain English

**Theorem (`mind_change_characterization`, Theorem/Gold.lean lines 206–258).** C is
[EXLearnable](#/node/EXLearnable) iff some learner L has `MindChangeOrdinal X L c T < ω` for every c ∈ C and every
text T for c.

`MindChangeOrdinal` (Complexity/MindChange.lean lines 43–50) is **defined** as: the number of mind changes (a finite
ordinal) if the set of change times is finite **and** the learner eventually conjectures c; otherwise ω. So
"< ω" is, by definition, "finitely many changes and correct convergence". The theorem is then a short unfolding
(plus an off-by-one bridge between `dataUpTo` and `prefix`). The README is open about this ("definition as proof
technique", and the docstring at lines 40–42 of MindChange.lean). It is correct, but it is not the classical
ordinal mind-change hierarchy of Freivalds–Smith, where ordinals beyond ω measure a *bound announced in advance*.

Also in this area:

- `ex_strictly_stronger_finite` (Theorem/Separation.lean lines 1335–1342): finite learning ⟹ EX learning. Despite
  the name, only this implication is proved, not strictness.
- Criterion/Gold.lean defines BC, finite, vacillatory, anomalous, monotonic and trial-and-error learning
  (lines 40–98); most are not characterized.
""",
 [q("When is MindChangeOrdinal finite (< ω)?",
    ["Exactly when the learner changes its mind finitely often and eventually conjectures c",
     "When the learner changes its mind finitely often, whatever it converges to",
     "Always",
     "When the text is finite"], 0,
    "Complexity/MindChange.lean lines 46–50: the finite value needs both `changes.Finite` and `∃ t₀, ∀ t ≥ t₀, … = c`."),
  q("Why is mind_change_characterization short?",
    ["Correct convergence is built into the definition of MindChangeOrdinal",
     "It uses a powerful library lemma",
     "It is sorry'd",
     "It assumes X is finite"], 0,
    "Docstring of `MindChangeOrdinal`, Complexity/MindChange.lean lines 33–42."),
  q("Does ex_strictly_stronger_finite prove strictness?",
    ["No, only that finite learning implies EX learning",
     "Yes, with a witness class",
     "It proves the converse",
     "It is a placeholder True"], 0,
    "Theorem/Separation.lean lines 1335–1342: the statement is `FiniteLearnable X C → EXLearnable X C`."),
 ],
 caveats=[NOT_BUILT,
  "Near-definitional: MindChangeOrdinal encodes correctness, so the characterization is mostly unfolding."])


node("advice_elimination",
 "Group: extended PAC results (advice elimination, meta-learning, SQ dimension)",
 "Theorem/Extended.lean proves that PAC learning with finitely many advice values can be turned into ordinary PAC "
 "learning (with a train/validation split), a lower bound for meta-learners that is the single-task VC bound, and a "
 "class of VC dimension 1 with infinite statistical-query dimension.",
 r"""## Plain English

**Theorem (`advice_elimination`, Theorem/Extended.lean lines 498–1023).** If C is PAC learnable with advice from a
finite nonempty set A, under a measurability regularity condition on the advice-taking learner
(`PACLearnableWithAdviceRegular`, lines 77–91), then C is PAC learnable without advice. The learner runs every
advice value on a training split, then picks the candidate with the lowest validation error (lines 93–117). Hoeffding
plus a union bound over A controls the failure probability. This is a substantial (about 500-line), complete-looking
proof, and it needs only `MeasurableHypotheses X C` (concepts in C measurable), not the full
[MeasurableConceptClass](#/node/MeasurableConceptClass).

Others in the same file:

- `baxter_base_case` (lines 1129–1147) and `baxter_full` (lines 1173–1193): a meta-learner that, after any
  training, achieves PAC on a new class of VC dimension d still needs ⌈(d − 1)/2⌉ samples. The docstrings say the
  n-dependent Baxter (2000) improvement is future work, and `baxter_full` despite its name proves only the
  n-independent bound (its training data argument is not used in the conclusion).
- `vcdim_not_implies_hardness` (lines 1204–1298): singletons on ℕ have VC dimension 1 but statistical-query
  dimension ⊤ at τ = 1, for every distribution. The threshold τ = 1 is the trivial correlation bound, so this is a
  weak separation.
- `meta_pac_bound` (lines 1029–1050).
- The universal-learning trichotomy (Bousquet et al. 2021) is present only as **commented-out** code (lines 25–58),
  waiting on a missing construction. It is not claimed.
""",
 [q("How does the advice-elimination learner choose among advice values?",
    ["It trains with each advice value on one part of the sample and picks the lowest validation error on the rest",
     "It picks advice at random",
     "It takes a majority vote over all advice values",
     "It ignores the advice"], 0,
    "Theorem/Extended.lean lines 93–117 (`adviceTrainSample`, `adviceValSample`, `bestAdvice`)."),
  q("Does baxter_full show that seeing more tasks reduces the sample size?",
    ["No: it proves the same n-independent ⌈(d−1)/2⌉ lower bound as the base case",
     "Yes, by a factor of n",
     "Yes, by log n",
     "It is sorry'd"], 0,
    "Theorem/Extended.lean lines 1160–1193: the docstring calls the n-dependent bound a future target."),
  q("Is the universal-learning trichotomy proved?",
    ["No: it is commented out pending a missing construction",
     "Yes",
     "Yes, with sorry",
     "It is an axiom"], 0,
    "Theorem/Extended.lean lines 25–58 sit inside a block comment."),
 ],
 caveats=[NOT_BUILT])


node("nfl_theorem_infinite",
 "Group: other PAC facts (no free lunch, Occam, Sauer–Shelah, lower bound)",
 "Theorem/PAC.lean also proves: the class of all functions on an infinite domain is not PAC learnable (no free "
 "lunch); a fixed-sample-size no-free-lunch theorem on finite domains; Sauer–Shelah in Mathlib's finite form; and a "
 "PAC lower bound. Some statements are weaker than their names suggest.",
 r"""## Plain English

- **No free lunch, infinite domain** (`nfl_theorem_infinite`, lines 370–379). For infinite X with measurable
  singletons, `Set.univ` is not PAC learnable, because its VCDim is ⊤ (`vcdim_univ_infinite`, lines 341–367). A
  comment (lines 331–338) explains that the finite-X version, as first stated, was false: on finite X every class is
  PAC learnable.
- **No free lunch, fixed m** (`nfl_fixed_sample`, lines 400–417). For finite X with |X| ≥ 2m and any learner on m
  samples there is a distribution and a target with P(error > 1/8) > 0. The textbook version (Shalev-Shwartz &
  Ben-David Thm 5.1) gives probability ≥ 1/7 of error ≥ 1/8. Positive probability is much weaker.
- **Sauer–Shelah** (`sauer_shelah_quantitative`, lines 144–150), via Mathlib's `card_shatterer_le_sum_vcDim`, for a
  finite family on a finite X. `sauer_shelah` (lines 153–157) is a trivially true legacy statement, labelled as such.
- **PAC lower bound** (`pac_lower_bound`, lines 173–186): ⌈(d − 1)/2⌉ ≤ SampleComplexity. No ε dependence, as
  discussed under [pac_sample_complexity_sandwich](#/node/pac_sample_complexity_sandwich).
- **Occam's algorithm** (`occam_algorithm`, lines 430–448). The description-length hypothesis is not used. The
  proof just applies [vc_characterization](#/node/vc_characterization) to the extra hypothesis VCDim < ⊤. The
  docstring says so. Treat the name as aspirational.

Also: `gold_does_not_imply_pac` (Complexity/Generalization.lean lines 1013–1016) is a placeholder whose statement is
`True`. The real result is `ex_not_implies_pac` (see [online_pac_gold_separation](#/node/online_pac_gold_separation)).
""",
 [q("Why is 'the class of all functions on a finite X is not PAC learnable' false?",
    ["Its VC dimension is |X| < ⊤, so by the VC characterization it is PAC learnable",
     "Because finite sets are not measurable",
     "It is true",
     "Because PAC requires infinite X"], 0,
    "Theorem/PAC.lean lines 331–338."),
  q("What does occam_algorithm actually use to conclude PAC learnability?",
    ["The extra hypothesis VCDim < ⊤ and vc_characterization; the description length plays no role",
     "A union bound over 2^k short hypotheses",
     "Compression",
     "Nothing; it is sorry'd"], 0,
    "Theorem/PAC.lean lines 436 and 447–448."),
  q("How strong is nfl_fixed_sample compared with the textbook no-free-lunch theorem?",
    ["Weaker: it gives positive probability of error > 1/8, not probability ≥ 1/7",
     "Identical",
     "Stronger",
     "Unrelated"], 0,
    "Theorem/PAC.lean lines 404–411: `… > 0`."),
 ],
 caveats=[NOT_BUILT, "Several names (Occam, the weak Sauer–Shelah, nfl_fixed_sample) are stronger than the statements."])
