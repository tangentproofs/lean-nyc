import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import node_maker, q, walk, S, NOT_BUILT, MEAS

NODES = []
node = node_maker(NODES)


node("fundamental_theorem",
 "Headline: the fundamental theorem of statistical learning (five conjuncts)",
 "On a domain where every subset is measurable, finite VC dimension is equivalent to realizable PAC learnability, to "
 "finite compression with side information, to uniformly vanishing Rademacher complexity and to Sauer–Shelah growth. "
 "Another conjunct adds a weak sample-complexity sandwich. No sorry.",
 r"""## Plain English

**Theorem (`fundamental_theorem`, Theorem/PAC.lean lines 293–329).** Let X be a measurable space whose singletons
are measurable, and let C be a set of yes/no classifiers on X ([ConceptClass](#/node/ConceptClass)) satisfying the
regularity package [MeasurableConceptClass](#/node/MeasurableConceptClass). Then all of the following hold:

1. **PAC ⟺ finite VC.** C is [PAC learnable](#/node/PACLearnable) exactly when its
   [VC dimension](#/node/VCDim) is finite. This is [vc_characterization](#/node/vc_characterization).
2. **Finite VC ⟺ compression.** VCDim(C) < ∞ exactly when C has a sample-compression scheme with finite side
   information ([CompressionSchemeWithInfo](#/node/CompressionSchemeWithInfo)). This is the Moran–Yehudayoff theorem,
   [fundamental_vc_compression_with_info](#/node/fundamental_vc_compression_with_info). It needs no measure theory.
3. **Finite VC ⟺ vanishing Rademacher complexity.** For every ε > 0 there is an m₀ such that, for **every**
   probability distribution D and every m ≥ m₀, the [Rademacher complexity](#/node/RademacherComplexity) of C at
   sample size m is below ε. See [fundamental_rademacher](#/node/fundamental_rademacher).
4. **A sample-complexity sandwich.** If C is PAC learnable, some witness learner L with sample-size function mf
   satisfies the PAC guarantee, [SampleComplexity](#/node/SampleComplexity)(ε, δ) ≤ mf(ε, δ), and, when VCDim(C) = d ≥ 1,
   ε ≤ 1/4 and δ ≤ 1/7, both are at least ⌈(d − 1)/2⌉. See
   [pac_sample_complexity_sandwich](#/node/pac_sample_complexity_sandwich).
5. **Finite VC ⟺ Sauer–Shelah growth.** VCDim(C) < ∞ exactly when there is a d with
   [GrowthFunction](#/node/GrowthFunction)(m) ≤ Σ_{i ≤ d} (m choose i) for every m ≥ d.

So conjuncts 1, 2, 3 and 5 are four equivalent descriptions of "finite VC dimension". Conjunct 4 is a one-way
add-on, not an equivalence.

### How it compares with the textbook

The textbook statement (Shalev-Shwartz & Ben-David, *Understanding Machine Learning*, Thm 6.7) lists uniform
convergence, agnostic PAC, realizable PAC, ERM success and finite VC dimension as equivalent, and Thm 6.8 gives
sample complexity Θ((d + log(1/δ))/ε) in the realizable case. This Lean theorem differs:

- **Realizable PAC only.** [PACLearnable](#/node/PACLearnable) labels the sample with a target c ∈ C. The agnostic
  notion `AgnosticPACLearnable` is defined (Criterion/PAC.lean lines 79–92) but is **not** part of this theorem.
- **Uniform convergence is used, not stated.** [HasUniformConvergence](#/node/HasUniformConvergence) is proved on
  the way (see [vcdim_finite_imp_uc'](#/node/vcdim_finite_imp_uc')), but it is not one of the five conjuncts.
- **The sample-complexity part is weak.** The lower bound ⌈(d − 1)/2⌉ has no ε in it, and no explicit upper bound
  in terms of d, ε and δ appears in the statement (the proof's own bound is polynomial in 1/δ, not logarithmic).
- **Compression and Rademacher are extras.** They are not in the textbook theorem; including them is the
  project's own packaging ("BP₅" in its comments).
- **Strong measurability assumption.** See the caveats.

### Proof

The proof is a one-screen assembly of five component theorems (lines 324–329); the work is in the components. The
deepest path is conjunct 1's hard direction: [vcdim_finite_imp_uc'](#/node/vcdim_finite_imp_uc') (Sauer–Shelah +
symmetrization + Hoeffding, about 3,000 lines in Complexity/Symmetrization.lean) and then
[uc_imp_pac](#/node/uc_imp_pac). The other long path is conjunct 2's forward direction, the Moran–Yehudayoff
construction in Complexity/Compression.lean.

See the [Roadmap](#/roadmap) for the whole proof in dependency order.
""",
 [q("Which notion of PAC learning does conjunct 1 use?",
    ["Realizable PAC: samples are labelled by a target concept c in C",
     "Agnostic PAC: samples come from an arbitrary distribution on X × Bool",
     "Both, as two separate conjuncts",
     "Exact learning with membership queries"], 0,
    "`PACLearnable` (Criterion/PAC.lean lines 55–68) labels each sample point xs i with c (xs i) for c ∈ C. The agnostic definition (lines 79–92) is not used by `fundamental_theorem`."),
  q("What does conjunct 4 (the sample-complexity sandwich) bound SampleComplexity below by, when VCDim = d?",
    ["⌈(d − 1)/2⌉, with no dependence on ε",
     "(d − 1)/(64ε)",
     "(d + log(1/δ))/ε",
     "d · log(1/ε)"], 0,
    "Theorem/PAC.lean lines 315–319: `Nat.ceil ((d - 1 : ℝ) / 2) ≤ SampleComplexity X C ε δ`. The docstring of `pac_lower_bound` (lines 159–172) mentions (d−1)/(64ε), but the proved statement has no ε."),
  q("Which of these is NOT one of the five conjuncts?",
    ["Uniform convergence of empirical errors (HasUniformConvergence)",
     "Existence of a compression scheme with finite side information",
     "Uniformly vanishing Rademacher complexity",
     "A Sauer–Shelah bound on the growth function"], 0,
    "Uniform convergence is proved and used inside the proof (Complexity/Symmetrization.lean lines 2665–2935) but is not part of the statement at Theorem/PAC.lean lines 297–322."),
  q("Does the theorem, as stated, apply to thresholds on ℝ with the Borel σ-algebra?",
    ["No: MeasurableConceptClass requires every Bool-valued function on X to be measurable, which fails for Borel ℝ",
     "Yes: MeasurableSingletonClass is all that is needed",
     "Yes: the Borel-analytic bridge supplies the instance",
     "Only when the distribution D is continuous"], 0,
    "Complexity/Measurability.lean lines 60–67: the field `all_measurable : ∀ c : Concept X Bool, Measurable c`. The docstring at lines 125–140 says ℝⁿ with the Borel σ-algebra does not satisfy this."),
  q("How many of the five conjuncts are genuine equivalences with 'VCDim C < ⊤'?",
    ["Four (PAC, compression, Rademacher, growth); the sample-complexity conjunct is a one-way implication",
     "All five",
     "Three",
     "Only the PAC conjunct"], 0,
    "Conjunct 4 (lines 303–319) is `PACLearnable X C → ∃ L mf, …`, an implication. The others are `↔`."),
 ],
 caveats=[NOT_BUILT, MEAS,
  "Faithfulness: the name suggests the textbook theorem, but this statement is realizable-only, does not include "
  "agnostic PAC or uniform convergence as conjuncts, and its sample-complexity conjunct is much weaker than the "
  "textbook Θ((d + log(1/δ))/ε). The added compression and Rademacher conjuncts are genuine extra content.",
  "The PAC success event is measured with `Measure.pi` applied to a set that need not be measurable, which in "
  "Mathlib means outer measure (Criterion/PAC.lean lines 39–44 say so). Learners are not required to be measurable."],
 widgets=walk("How the proof goes (Theorem/PAC.lean, lines 293-329)", [
   S("Conjunct 1 is vc_characterization: PAC ⟺ VCDim < ⊤.", "vc_characterization", "⟨vc_characterization X C,"),
   S("Conjunct 2 is the Moran–Yehudayoff compression equivalence (through its Theorem/PAC.lean wrapper fundamental_vc_compression).",
     "fundamental_vc_compression_with_info", "fundamental_vc_compression X C,"),
   S("Conjunct 3: chain VCDim < ⊤ ⟺ PAC (conjunct 1, reversed) with PAC ⟺ vanishing Rademacher complexity.",
     "fundamental_rademacher", "(vc_characterization X C).symm.trans (fundamental_rademacher X C),"),
   S("Conjunct 4: the sample-complexity sandwich attached to any PAC witness.", "pac_sample_complexity_sandwich",
     "pac_sample_complexity_sandwich X C,"),
   S("Conjunct 5: Sauer–Shelah in one direction (VCDim = d gives the binomial-sum bound), and in the other a shattered "
     "set of size m forcing growth 2^m, which beats the binomial sum.", "GrowthFunction",
     "⟨vcdim_finite_imp_growth_bounded X C, growth_bounded_imp_vcdim_finite X C⟩⟩"),
 ]))


node("vc_characterization",
 "Headline: PAC learnable ⟺ finite VC dimension",
 "A class is (realizably) PAC learnable exactly when its VC dimension is finite. The hard direction goes through "
 "about 3,000 lines of symmetrization to uniform convergence, then a consistent learner. The easy direction defeats "
 "any learner on a large shattered set.",
 r"""## Plain English

**Theorem (`vc_characterization`, Theorem/PAC.lean lines 127–132).** For a measurable space X with measurable
singletons and a concept class C with the [MeasurableConceptClass](#/node/MeasurableConceptClass) package,

  [PACLearnable](#/node/PACLearnable) X C ⟺ [VCDim](#/node/VCDim) X C < ⊤.

This is the heart of the [fundamental theorem](#/node/fundamental_theorem) (its first conjunct).

### The two directions

- **VC finite ⟹ PAC** (`vcdim_finite_imp_pac`, Theorem/PAC.lean lines 74–88). If C is empty, PAC learnability
  holds vacuously. Otherwise:
  1. [vcdim_finite_imp_uc'](#/node/vcdim_finite_imp_uc') shows C has
     [uniform convergence](#/node/HasUniformConvergence): with enough samples, empirical error is close to true
     error **simultaneously for every h ∈ C**, for every distribution.
  2. [uc_imp_pac](#/node/uc_imp_pac) turns that into a PAC learner: output any h ∈ C consistent with the sample.
     Its empirical error is 0, so its true error is small.
- **PAC ⟹ VC finite** (`pac_imp_vcdim_finite`, Theorem/PAC.lean lines 106–113). By contradiction, using
  [vcdim_infinite_not_pac](#/node/vcdim_infinite_not_pac): if VCDim = ⊤, fix ε = δ = 1/4 and the learner's sample
  size m. Take a shattered set T with more than 2m points and the uniform distribution on T. A counting argument
  finds a target in C on which the learner fails too often.

Note the asymmetry the README stresses: the second direction needs only
`[MeasurableSingletonClass X]`, not the full measurability package. Only the "VC finite ⟹ PAC" direction uses
`MeasurableConceptClass`.
""",
 [q("Which direction of vc_characterization needs the MeasurableConceptClass assumptions?",
    ["Only VC finite ⟹ PAC (through uniform convergence)",
     "Only PAC ⟹ VC finite",
     "Both directions equally",
     "Neither; they are only there for style"], 0,
    "`pac_imp_vcdim_finite` (Theorem/PAC.lean lines 106–113) has only `[MeasurableSingletonClass X]`. `vcdim_finite_imp_pac` (lines 74–88) pulls `hmeas_C`, `hc_meas` and `hWB` out of the class."),
  q("What learner does the VC ⟹ PAC direction build?",
    ["A learner that outputs some hypothesis in C consistent with the sample (falling back to a fixed element of C)",
     "The Standard Optimal Algorithm",
     "A majority vote over a compression scheme",
     "A Bayesian posterior sampler"], 0,
    "`uc_imp_pac` (Complexity/Generalization.lean lines 855–858) defines `learnFn` by choosing h₀ ∈ C agreeing with all sample labels if one exists, else `hC.some`."),
  q("In the PAC ⟹ VC direction, what distribution defeats the learner?",
    ["The uniform distribution on a shattered set with more than 2m points",
     "A point mass at one element",
     "A Gaussian",
     "The distribution chosen by the learner"], 0,
    "Complexity/Generalization.lean lines 2790–2853: fix ε = δ = 1/4, m = mf(1/4, 1/4), pick a shattered T with |T| > 2m, and use the uniform measure on T."),
 ],
 caveats=[NOT_BUILT, MEAS,
  "Realizable PAC only; see [PACLearnable](#/node/PACLearnable). The textbook theorem also covers agnostic PAC."],
 widgets=walk("How the proof goes (Theorem/PAC.lean, lines 74-132)", [
   S("VC ⟹ PAC: unpack the three measurability facts from the typeclass.", "MeasurableConceptClass",
     "have hWB := MeasurableConceptClass.hWB C"),
   S("If C is nonempty: uniform convergence (Symmetrization.lean), then a consistent learner is PAC.",
     "vcdim_finite_imp_uc'", "· exact uc_imp_pac X C hne (vcdim_finite_imp_uc' X C hC hmeas_C hc_meas hWB)"),
   S("If C is empty, the PAC condition 'for all c ∈ C' is vacuous; any learner works.", "PACLearnable"),
   S("PAC ⟹ VC: assume VCDim = ⊤ and contradict PAC learnability with the hard-distribution argument.",
     "vcdim_infinite_not_pac", "exact absurd hC (vcdim_infinite_not_pac X C (le_antisymm le_top h))"),
   S("Package the two directions as an iff.", None,
     "⟨pac_imp_vcdim_finite X C, fun hC => vcdim_finite_imp_pac X C hC⟩"),
 ]))


node("fundamental_vc_compression_with_info",
 "Headline: finite VC dimension ⟺ compression with side info (Moran–Yehudayoff)",
 "Finite VC dimension ⟺ every realizable sample can be cut down to a bounded number of its own points plus a tag "
 "from a fixed finite set, from which a classifier correct on the whole sample is rebuilt. Purely combinatorial; the "
 "proof uses multiplicative-weights approximate minimax.",
 r"""## Plain English

**Theorem (`fundamental_vc_compression_with_info`, Complexity/Compression.lean lines 1321–1326).** For any type X
and any concept class C ⊆ (X → Bool):

  [VCDim](#/node/VCDim) X C < ⊤ ⟺ there is a [compression scheme with finite side information](#/node/CompressionSchemeWithInfo) for C.

(The right side is written "∃ k cs, cs.size = k", which just says that a scheme `cs` exists: take k = cs.size. The
`0` in `CompressionSchemeWithInfo0` only fixes a universe level, Complexity/Compression.lean lines 620–627.)

A scheme picks, from any sample S, a sub-multiset of at most K labelled points of S and a tag from a fixed
finite set I. A reconstruction map turns (points, tag) into a classifier, which must agree with **every** point of
S whenever S is labelled by some c ∈ C. K and I are fixed for the class, independent of the sample size.

This is Moran & Yehudayoff, *Sample compression schemes for VC classes* (J. ACM 2016, arXiv:1503.06960), which
proved Littlestone and Warmuth's 1986 question in the version **with** side information. The version with no side
information is still open and is recorded as a `Prop`, not a theorem: `Open_NoInfoCompressionStrengthening`
(Complexity/Structures.lean lines 268–271).

### The two directions

- **Compression ⟹ finite VC** (`compression_with_info_imp_vcdim_finite`, lines 1214–1317). Pigeonhole: on a
  shattered set T of size n, every one of the 2ⁿ labellings is realizable, and correctness forces different
  labellings to compress differently. But there are at most polynomially many (points, tag) pairs. At
  n = 2(s+1)² with s = K + |I| the exponential wins, so no such T is shattered.
- **Finite VC ⟹ compression** (`vcdim_finite_imp_compression_with_info`, lines 1120–1143). The Moran–Yehudayoff
  construction, routed through `moran_yehudayoff_forward_construction` (lines 805–1105):
  1. a *proper finite-support learner* that, from a bounded subsample, outputs a hypothesis in C with low error
     on any distribution supported on the sample (lines 189–305);
  2. a finite "agreement game" between subsamples and sample points; **approximate minimax by multiplicative
     weights** (PureMath/ApproxMinimax.lean) gives a mixed strategy that does well against every point;
  3. a VC ε-approximation (PureMath/FiniteVCApprox.lean) sparsifies that mixture to T hypotheses;
  4. the kernel is the union of their witness subsamples, the side information records which kernel points belong
     to which hypothesis, and reconstruction is a **majority vote**.

The README credits the replacement of Sion's exact minimax by MWU, and the specific margin 13/24, as original to
this formalization.
""",
 [q("What does the side information in the scheme have to be?",
    ["An element of a fixed finite type, the same for every sample size",
     "Any natural number",
     "A real number encoding the whole sample",
     "Nothing: there is no side information"], 0,
    "`CompressionSchemeWithInfo` (Complexity/Structures.lean lines 215–238) has `Info : Type*` with `info_finite : Fintype Info`, fixed once for the scheme."),
  q("When must the reconstructed classifier be correct on the sample?",
    ["Whenever the sample is labelled by some concept in C",
     "On every sample, even inconsistent ones",
     "Only on samples of size at most K",
     "Only with high probability"], 0,
    "The field `correct` (Complexity/Structures.lean lines 235–238) is guarded by `∃ c ∈ C, ∀ i, c (S i).1 = (S i).2`. The docstring at lines 30–39 explains that the unguarded version was uninhabited."),
  q("Does this theorem settle the Littlestone–Warmuth sample compression conjecture (no side information, size O(d))?",
    ["No: that stronger statement is only defined as a Prop, Open_NoInfoCompressionStrengthening",
     "Yes, with size exactly d",
     "Yes, with size 2^d",
     "It shows the conjecture is false"], 0,
    "Complexity/Structures.lean lines 265–271 state it as an open `def … : Prop`, not a theorem."),
  q("Which measurability hypotheses does this theorem need?",
    ["None: it is purely combinatorial",
     "MeasurableConceptClass",
     "StandardBorelSpace X",
     "MeasurableSingletonClass X"], 0,
    "The statement (Complexity/Compression.lean lines 1321–1326) has only `(X : Type u) (C : ConceptClass X Bool)`. The module docstring (lines 30–35) says the forward theorem uses no MeasureTheory."),
 ],
 caveats=[NOT_BUILT,
  "The statement only asserts existence of some finite K and I. It gives no size bound (Moran–Yehudayoff get "
  "size exp(O(d)) in terms of the VC dimension d), and `size` is defined as K + |I| rather than the paper's "
  "K + log₂(|I|+1) (Complexity/Structures.lean lines 242–249). Neither matters for the existence statement."],
 widgets=walk("How the proof goes (Complexity/Compression.lean, lines 1120-1326)", [
   S("Forward, nonempty C: get a proper finite-support learner from finite VC dimension.", None,
     "obtain ⟨L, _⟩ := vcdim_finite_imp_proper_finite_support_learner X C hne hC"),
   S("Run the Moran–Yehudayoff construction: MWU approximate minimax on the agreement game, ε-approximation, "
     "kernel + incidence side information, majority-vote reconstruction (lines 805–1105).", None,
     "exact moran_yehudayoff_forward_construction X C hne L hC L.sampleBound"),
   S("Forward, empty C: no sample is realizable, so the trivial scheme (empty kernel, one tag) works.", None),
   S("Reverse: if VCDim = ⊤, take a shattered set of size N = 2(s+1)² where s = kernel size + |Info|.", None,
     "obtain ⟨T₀, hT₀_shatt, hT₀_card⟩ := h_large N"),
   S("Correctness makes compression injective on the 2^N labellings of T, but there are fewer than 2^N "
     "(kernel, tag) pairs: contradiction (lines 1150–1317).", None),
   S("Combine.", None, "fun ⟨k, cs, hk⟩ => compression_with_info_imp_vcdim_finite X C ⟨k, cs, hk⟩⟩"),
 ]))


node("littlestone_characterization",
 "Headline: online learnable ⟺ finite Littlestone dimension",
 "A class has an online learner with a finite mistake bound (for every target and question sequence) exactly when "
 "its Littlestone dimension, the depth of the deepest shattered mistake tree, is finite. The learner is the Standard "
 "Optimal Algorithm.",
 r"""## Plain English

**Theorem (`littlestone_characterization`, Theorem/Online.lean lines 419–422).** For X : Type and a class C,

  [OnlineLearnable](#/node/OnlineLearnable) X Bool C ⟺ [LittlestoneDim](#/node/LittlestoneDim) X C < ⊤.

*Online learnable* means some [online learner](#/node/OnlineLearner) makes at most M mistakes, for some fixed M,
whatever the target c ∈ C and whatever finite list of points it is asked about. The *Littlestone dimension* is
the largest n such that a complete binary tree of depth n, with a point at each internal node, is shattered by C
along every root-to-leaf path.

### The two directions

- **Online ⟹ finite Ldim** (`forward_direction`, Theorem/Online.lean lines 27–49). If Ldim = ⊤, pick a shattered
  tree deeper than the mistake bound M. The adversary (`adversary_core`, Complexity/GameInfra.lean lines 95–122)
  walks down the tree, always revealing the label the learner did **not** predict. Shattering guarantees a
  concept in C still fits all those answers, so the learner makes more than M mistakes.
- **Finite Ldim ⟹ online** (`backward_direction`, Theorem/Online.lean lines 389–413). Run the
  [Standard Optimal Algorithm](#/node/SOA): predict the label whose surviving version space has the larger
  Littlestone dimension. Each mistake strictly lowers the Ldim of the version space (`soa_mistakes_bounded`,
  Theorem/Online.lean lines 322–386), so there are at most d = Ldim(C) mistakes.

The same file also proves `optimal_mistake_bound_eq_ldim` (lines 440–502): for nonempty C, the best possible
mistake bound **equals** the Littlestone dimension.

### A definition repair

The README reports that the "branch-wise" tree definition first tried gave a false theorem, and that the
**path-wise** definition used here (`LTree.isShattered`, Complexity/GameInfra.lean lines 41–46) fixes it: each
subtree only has to be shattered by the concepts consistent with the label on the path so far. The old
definition survives as `BranchWiseLittlestoneDim` (Complexity/Littlestone.lean lines 52–53).
""",
 [q("In OnlineLearnable, who chooses the question sequence?",
    ["The statement quantifies over every target c ∈ C and every finite list of points",
     "The learner chooses which points to ask about",
     "The points are drawn i.i.d. from a distribution",
     "The sequence is fixed to be an enumeration of X"], 0,
    "`MistakeBounded` (Criterion/Online.lean lines 32–36): `∀ c ∈ C, ∀ seq : List X, L.mistakes c seq ≤ M`. Because the learner is deterministic, a fixed sequence is as strong as an adaptive adversary."),
  q("How does the SOA choose its prediction on x?",
    ["It predicts the label whose consistent sub-class has the larger Littlestone dimension",
     "It predicts the majority label among consistent concepts",
     "It predicts at random",
     "It always predicts true"], 0,
    "Complexity/GameInfra.lean lines 151–158: compare `LittlestoneDim X {c ∈ V | c x = true}` with the `false` side and predict the larger (ties go to true)."),
  q("What does LTree.isShattered require at a leaf?",
    ["That the remaining sub-class is nonempty",
     "Nothing (True)",
     "That the remaining sub-class has exactly one concept",
     "That the leaf's point is labelled true"], 0,
    "Complexity/GameInfra.lean line 42: `| .leaf => C.Nonempty`, with the comment that it used to be True."),
  q("Is the theorem stated for domains in every universe?",
    ["No: X : Type (universe 0), because OnlineLearner's state lives in Type",
     "Yes, X : Type u",
     "Only for finite X",
     "Only for X = ℕ"], 0,
    "Theorem/Online.lean line 419 has `(X : Type)`. This is a harmless restriction for applications."),
 ],
 caveats=[NOT_BUILT,
  "Realizable (mistake-bound) online learning only; no regret bounds for the agnostic online setting are part "
  "of this theorem (RegretBounded is defined in Criterion/Online.lean lines 61–66 but not characterized)."],
 widgets=walk("How the proof goes (Theorem/Online.lean, lines 27-422)", [
   S("Forward: assume a mistake bound M and Ldim = ⊤.", "OnlineLearnable", "intro ⟨M, L, hL⟩"),
   S("Find a shattered tree of depth n > M.", "LittlestoneDim",
     "have hunbounded : ∃ n, n > M ∧ ∃ T : LTree X n, T.isShattered C := by"),
   S("The adversary walks the tree and forces a mistake at every level.", None,
     "obtain ⟨seq, c, hcC, hcount⟩ := adversary_core L L.init T hTshat hne"),
   S("Backward: with Ldim ≤ d, use the SOA as the learner with bound d.", "SOA",
     "refine ⟨d, SOA X C, fun c hcC seq => ?_⟩"),
   S("Each SOA mistake lowers the version space's Ldim, so at most d mistakes.", None,
     "have hmf := soa_mistakes_bounded c hcC [] (by simp) d hle hfin seq"),
   S("Combine.", None, "⟨forward_direction X C, backward_direction X C⟩"),
 ]))


node("gold_theorem",
 "Headline: Gold's theorem (no learning in the limit from positive data)",
 "If a class on a countable domain contains every finite set and at least one infinite set, no learner can identify "
 "every member in the limit from positive examples alone. The proof builds a locking sequence: an adversarial text "
 "for the infinite set on which the learner keeps settling on finite sets.",
 r"""## Plain English

**Theorem (`gold_theorem`, Theorem/Gold.lean lines 19–201).** Let X be countable with decidable equality, and let C
be a class of concepts (read: subsets of X) that

- contains the indicator of **every finite set** S ⊆ X, and
- contains at least one concept c_inf whose set of positives is **infinite**.

Then C is **not** [EXLearnable](#/node/EXLearnable): no [Gold learner](#/node/GoldLearner) identifies every
c ∈ C in the limit from every [text](#/node/TextPresentation) (an enumeration of the positive examples of c).

This is Gold (1967), *Language identification in the limit*: "superfinite" classes are not learnable from text.

### Proof idea (the locking-sequence argument)

1. **Infrastructure** (lines 26–55). Enumerate the positives of c_inf and build finite sets
   S₀ ⊆ S₁ ⊆ S₂ ⊆ … whose union is all of them. Each Sₙ is in C (it is finite) and differs from c_inf.
2. **Lock onto a finite set** (`conv_ext`, lines 56–112). Any finite list σ of positive examples from Sₙ can be
   extended to a longer list on which the learner's conjecture is exactly Sₙ. (Otherwise the text "σ, then Sₙ
   repeated forever" would be a text for Sₙ on which the learner never converges to Sₙ.)
3. **Locking sequence** (lines 113–159). Chain these extensions for n = 0, 1, 2, … into ever-longer prefixes.
4. **Adversarial text** (lines 160–187). The limit of the chain is a text for c_inf.
5. **Contradiction** (lines 188–201). On that text the learner outputs Sₙ ≠ c_inf at infinitely many times, so
   it never converges to c_inf.

### What "learner" means here

A Gold learner is any function from finite data lists to concepts. There is no computability requirement.
Gold's theorem holds for arbitrary learners, so this is faithful (it is the stronger, information-theoretic form).
""",
 [q("Which classes does gold_theorem say are not EX-learnable from text?",
    ["Classes containing every finite set and at least one infinite set",
     "Every infinite class",
     "Classes with infinite VC dimension",
     "Classes containing the empty set"], 0,
    "The hypotheses `h_finite` and `h_infinite`, Theorem/Gold.lean lines 21–22."),
  q("Does the theorem restrict learners to computable ones?",
    ["No: a GoldLearner is any function from data lists to concepts",
     "Yes, it requires a Turing machine",
     "Yes, it requires primitive recursive learners",
     "It restricts to learners with finitely many mind changes"], 0,
    "`GoldLearner` (Learner/Core.lean lines 50–52) is just `conjecture : List (X × Y) → Concept X Y`. Gold's argument works for every function, so this is the strong form."),
  q("What does a text presentation for c contain?",
    ["Only positive examples, and every positive example of c appears at some time",
     "Every point of X with its label",
     "A random sample from a distribution",
     "Only negative examples"], 0,
    "`TextPresentation` (Data.lean lines 46–52): `positive`, `correct` and `exhaustive`."),
 ],
 caveats=[NOT_BUILT,
  "EXLearnable asks the conjecture to become **equal as a function** to c and stay so. Gold's original notion "
  "converges to a single *index* (grammar); with no indices here, this is closer to behaviourally-correct "
  "learning. For the negative result this is if anything a stronger statement (learning is easier, yet still "
  "impossible).",
  "A TextPresentation must output a positive example at every step, so the empty concept has no text at all. "
  "Classical presentations use a pause symbol. This does not affect `gold_theorem`, whose infinite concept has texts."],
 widgets=walk("How the proof goes (Theorem/Gold.lean, lines 19-201)", [
   S("Assume a learner L that EX-learns C; take the infinite concept c_inf.", "EXLearnable",
     "obtain ⟨c_inf, hc_inf_mem, hc_inf_inf⟩ := h_infinite"),
   S("Build finite sets S n increasing to the positives of c_inf, each different from c_inf.", None,
     "have hS_ne : ∀ n, (fun x => decide (x ∈ S n)) ≠ c_inf := by"),
   S("Key lemma: any positive list inside S m extends to a longer one on which L conjectures S m.", None,
     "have conv_ext : ∀ (m : ℕ) (σ : List (X × Bool))"),
   S("Chain the extensions into a locking sequence and read off an adversarial text for c_inf.", "TextPresentation",
     "-- === ADVERSARIAL TEXT ==="),
   S("L converges to c_inf on that text from some t₀, but at the locking times it conjectures S n ≠ c_inf.", None,
     "exact hS_ne n (by rw [← hlock_conj n, hconv'])"),
 ]))


node("online_pac_gold_separation",
 "Headline: the three paradigms separate (PAC ⇏ online, Gold ⇏ PAC)",
 "There is a class on ℕ that is PAC learnable but not online learnable (thresholds), and a class on ℕ that is "
 "learnable in the limit from text but not PAC learnable (indicators of finite sets). Together with online ⟹ PAC, "
 "this places the three learning paradigms in a strict picture.",
 r"""## Plain English

**Theorem (`online_pac_gold_separation`, Theorem/Separation.lean lines 1358–1363).** Both of these hold:

1. **PAC does not imply online** (`pac_not_implies_online`, lines 1175–1231). There is a measurable space X and a
   class C on it with C [PAC learnable](#/node/PACLearnable) but not [online learnable](#/node/OnlineLearnable).
   Witness: X = ℕ with the σ-algebra of all subsets, and C = **thresholds** {x ↦ (x ≤ n) : n ∈ ℕ}
   (`thresholdClass`, lines 1013–1018). Its VC dimension is 1, so it is PAC learnable. Its Littlestone dimension is
   infinite (an adversary can binary-search the threshold), so by
   [littlestone_characterization](#/node/littlestone_characterization) it is not online learnable.
2. **Gold does not imply PAC** (`ex_not_implies_pac`, lines 1237–1313). Witness: X = ℕ, C = indicators of all
   **finite** subsets. The learner "say yes exactly to what you have seen" [EX-learns](#/node/EXLearnable) every
   finite set from text. But C shatters every finite set, so VCDim = ⊤, and
   [vcdim_infinite_not_pac](#/node/vcdim_infinite_not_pac) says it is not PAC learnable.

The companion `online_imp_pac` (lines 132–146) proves the positive arrow: a mistake bound M forces VCDim ≤ M
(an adversary on a shattered set forces a mistake per point), hence PAC learnability under
[MeasurableConceptClass](#/node/MeasurableConceptClass). `online_strictly_stronger_pac` (lines 1316–1324) packages
the two.

### Why the witnesses are honest

Both witnesses are concrete classes on ℕ. In the PAC half, the project proves by hand that on ℕ with the discrete
σ-algebra every set of sample pairs is measurable (lines 1180–1226), so the measurability hypotheses needed by the
VC ⟹ PAC theorem genuinely hold. Nothing is assumed.
""",
 [q("What is the witness class for 'PAC but not online'?",
    ["Thresholds x ↦ (x ≤ n) on ℕ",
     "All finite subsets of ℕ",
     "Singletons on ℕ",
     "Half-spaces in ℝ²"], 0,
    "Theorem/Separation.lean lines 1013–1018 (`thresholdClass`) and line 1178, `refine ⟨ℕ, ⊤, thresholdClass, ?_, ?_⟩`."),
  q("Why are indicators of finite subsets of ℕ not PAC learnable?",
    ["They shatter every finite set, so the VC dimension is infinite",
     "They are not measurable",
     "They have no text presentation",
     "Because ℕ is infinite, nothing is PAC learnable"], 0,
    "Theorem/Separation.lean lines 1287–1313: `Finset.range (n+1)` is shattered for every n, so `VCDim ℕ C = ⊤`, and `vcdim_infinite_not_pac` applies."),
  q("Does the separation theorem itself prove online ⟹ PAC?",
    ["No: that is the separate theorem online_imp_pac; this one only gives the two non-implications",
     "Yes, as its first conjunct",
     "Yes, but only for finite X",
     "No, because online ⟹ PAC is false"], 0,
    "Lines 1358–1363 contain two existential conjuncts. `online_imp_pac` is at lines 132–146."),
 ],
 caveats=[NOT_BUILT,
  "Both witnesses live on ℕ with the discrete σ-algebra, where all the measurability issues disappear. That is "
  "the natural setting for these classical examples."],
 widgets=walk("How the proof goes (Theorem/Separation.lean, lines 1175-1363)", [
   S("PAC half: X = ℕ with ⊤ σ-algebra, C = thresholds.", None, "refine ⟨ℕ, ⊤, thresholdClass, ?_, ?_⟩"),
   S("Show the double-sample bad event is measurable: on countable ℕ the product σ-algebra is everything.",
     "WellBehavedVC", "have hprod_top : (inferInstance : MeasurableSpace ((Fin m → ℕ) × (Fin m → ℕ))) = ⊤ := by"),
   S("VCDim(thresholds) < ⊤, so PAC via uniform convergence.", "vcdim_finite_imp_uc'",
     "exact vcdim_finite_imp_pac_via_uc' ℕ thresholdClass vcdim_threshold_finite"),
   S("Not online: Littlestone dimension of thresholds is ⊤.", "LittlestoneDim", "rw [ldim_threshold_top] at hfin"),
   S("Gold half: the learner answers true exactly on points seen so far.", "EXLearnable",
     "refine ⟨⟨fun data => fun x => data.any (fun p => decide (p.1 = x))⟩, ?_⟩"),
   S("Not PAC: VCDim = ⊤ for finite-set indicators.", "vcdim_infinite_not_pac", "apply vcdim_infinite_not_pac"),
   S("Assemble.", None, "exact ⟨pac_not_implies_online, ex_not_implies_pac⟩"),
 ]))
