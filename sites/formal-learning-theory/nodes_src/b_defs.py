import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import node_maker, q, walk, S, NOT_BUILT, MEAS

NODES = []
node = node_maker(NODES)


node("Concept",
 "Concept: a classifier X → Y",
 "A concept is just a function from the domain X to the labels Y. For binary classification Y = Bool, so a concept is "
 "the same thing as a subset of X (the points labelled true).",
 r"""## Plain English

**Definition (`Concept`, Basic.lean line 37).** `Concept X Y` is `X → Y`. Nothing more: no measurability, no
computability. In every headline Y = Bool, and a concept c is read as the set {x | c x = true}.

The library also has `Hypothesis` and `HypothesisSpace` (Basic.lean lines 76–81) as **the same type** under another
name, to mark the difference between the truth (concept) and a learner's guess (hypothesis).
""",
 [q("What is a Concept X Bool?",
    ["Any function X → Bool, with no further conditions",
     "A measurable function X → Bool",
     "A computable function X → Bool",
     "A finite subset of X"], 0,
    "Basic.lean line 37: `def Concept (X : Type u) (Y : Type v) := X → Y`."),
  q("How do Concept and Hypothesis differ as Lean types?",
    ["They are the same type; the different names only signal intent",
     "Hypotheses must be measurable",
     "Hypotheses are finite",
     "Concepts are sets, hypotheses are functions"], 0,
    "Basic.lean line 81: `abbrev Hypothesis (X : Type u) (Y : Type v) := Concept X Y`."),
  q("Which subset of X does a binary concept c correspond to?",
    ["{x | c x = true}",
     "{x | c x = false}",
     "The range of c",
     "There is no corresponding subset"], 0,
    "Standard reading; e.g. Gold's theorem talks about `Set.Infinite { x | c x = true }` (Theorem/Gold.lean line 22)."),
 ])


node("ConceptClass",
 "ConceptClass: a set of concepts",
 "A concept class is any set of classifiers. Every learnability notion and every complexity measure in the library "
 "is a property of a ConceptClass X Bool.",
 r"""## Plain English

**Definition (`ConceptClass`, Basic.lean line 46).** `ConceptClass X Y` is `Set (Concept X Y)`, a set of functions
X → Y. Examples used in the proofs:

- thresholds {x ↦ (x ≤ n)} on ℕ (`thresholdClass`, Theorem/Separation.lean lines 1013–1018);
- indicators of finite subsets of ℕ (Theorem/Separation.lean line 1240);
- `Set.univ`, all functions, used for the no-free-lunch results (Theorem/PAC.lean lines 341–379).

No measurability is built in. That is added separately by
[MeasurableConceptClass](#/node/MeasurableConceptClass) when measure theory needs it.
""",
 [q("Is every set of functions X → Bool a ConceptClass?",
    ["Yes: ConceptClass X Bool is just Set (X → Bool)",
     "No: it must be finite",
     "No: it must be measurable",
     "No: it must be nonempty"], 0,
    "Basic.lean line 46: `abbrev ConceptClass (X : Type u) (Y : Type v) := Set (Concept X Y)`."),
  q("Can a ConceptClass be empty?",
    ["Yes, and several proofs treat the empty case separately",
     "No, Lean forbids empty sets",
     "Only if X is empty",
     "Only for online learning"], 0,
    "e.g. `vcdim_finite_imp_pac` handles `¬ C.Nonempty` at Theorem/PAC.lean lines 86–88."),
  q("Where does measurability of concepts come in?",
    ["As a separate typeclass (MeasurableConceptClass), not in the definition of ConceptClass",
     "It is part of ConceptClass",
     "It is never needed",
     "Through the Bool type"], 0,
    "Complexity/Measurability.lean lines 60–67."),
 ])


node("BatchLearner",
 "BatchLearner: from a finite labelled sample to a hypothesis",
 "A batch learner maps a labelled sample of any size m to a classifier, which must lie in the learner's declared "
 "hypothesis space. It need not be computable or measurable, and it may be improper (its hypothesis space can be "
 "bigger than C).",
 r"""## Plain English

**Definition (`BatchLearner`, Learner/Core.lean lines 29–35).** A batch learner has

- `hypotheses`, a [HypothesisSpace](#/node/Concept) (a set of concepts);
- `learn`, which for every m takes a sample `Fin m → X × Y` (m labelled points) and returns a concept;
- `output_in_H`, a proof that the output is always in `hypotheses`.

In [PACLearnable](#/node/PACLearnable) the hypothesis space is existentially chosen together with the learner, so
the requirement is harmless: take `hypotheses = Set.univ` and any learner is allowed. In other words PAC learning
here is **improper** unless you add more. The learner used in the proof of
[vc_characterization](#/node/vc_characterization) happens to be proper (it outputs elements of C).

There is no measurability requirement. A separate class `MeasurableBatchLearner` (Learner/Core.lean lines 81–85)
records joint measurability of (sample, x) ↦ learn(sample)(x), which some extended results use.
""",
 [q("Must a BatchLearner be computable?",
    ["No: learn is an arbitrary Lean function, often defined with Classical.choice",
     "Yes, it must be a program",
     "Yes, in polynomial time",
     "Only for finite X"], 0,
    "Learner/Core.lean lines 29–35 put no such condition. `uc_imp_pac` uses `h.choose` (Complexity/Generalization.lean line 857)."),
  q("Does PACLearnable force the learner's output to lie in C?",
    ["No: the learner's hypothesis space is chosen freely, so improper learners are allowed",
     "Yes, always",
     "Only when C is finite",
     "Only in the agnostic case"], 0,
    "PACLearnable (Criterion/PAC.lean lines 55–68) only says ∃ L; nothing links L.hypotheses to C."),
  q("What is the type of a sample of size m?",
    ["Fin m → X × Y, an indexed list of m labelled points",
     "A Finset of points",
     "A probability measure",
     "A List of points without labels"], 0,
    "Learner/Core.lean line 33: `learn : {m : ℕ} → (Fin m → X × Y) → Concept X Y`."),
 ])


node("PACLearnable",
 "PACLearnable: realizable PAC learning with the true i.i.d. product measure",
 "One learner and one sample size mf(ε, δ) must work for every distribution D and target c ∈ C: on mf(ε, δ) i.i.d. "
 "draws from D labelled by c, the learner's error under D is ≤ ε with probability ≥ 1 − δ. The standard realizable, "
 "distribution-free definition.",
 r"""## Plain English

**Definition (`PACLearnable`, Criterion/PAC.lean lines 55–68).** There exist a [BatchLearner](#/node/BatchLearner)
L and a function mf : ℝ → ℝ → ℕ such that for all ε > 0, δ > 0, every probability measure D on X and every c ∈ C,
with m = mf(ε, δ):

  Dᵐ { xs ∈ Xᵐ : D{ x : L(xs labelled by c)(x) ≠ c(x) } ≤ ε } ≥ 1 − δ.

Here Dᵐ is Mathlib's product measure `Measure.pi`, so the m sample points really are independent draws from D.

### Faithfulness checklist

- **Quantifier order is right.** L and mf come first; D and c come after. The sample size depends only on (ε, δ):
  it is **distribution-free**. The docstring (lines 26–37) explains that an earlier version, with the sample
  distribution existentially chosen, made every class on a finite X trivially learnable, and was repaired.
- **Realizable.** Labels are c(xs i) for a target c ∈ C. The agnostic version, `AgnosticPACLearnable`
  (lines 79–92), is defined but not characterized by the headlines.
- **No computational efficiency.** Nothing about running time; mf can be any function.
- **Outer measure.** If the success set is not measurable, `Measure.pi` returns its outer measure (lines 39–44).
  That makes "≥ 1 − δ" slightly easier to satisfy than for a measurable event. The theorems that *construct*
  learners prove it under [MeasurableConceptClass](#/node/MeasurableConceptClass). The theorem that *refutes*
  learnability ([vcdim_infinite_not_pac](#/node/vcdim_infinite_not_pac)) works against this weaker notion, which
  makes it stronger.
""",
 [q("Can the sample size m depend on the distribution D?",
    ["No: mf is chosen before D and depends only on ε and δ",
     "Yes, m may depend on D",
     "Yes, m may depend on c",
     "There is no sample size; the learner sees all of X"], 0,
    "Criterion/PAC.lean lines 57–61: `∃ L mf, ∀ ε δ, … ∀ D, … ∀ c ∈ C, let m := mf ε δ`."),
  q("How are the sample points distributed?",
    ["i.i.d. from D: the sample distribution is the product measure Measure.pi (fun _ => D)",
     "Chosen adversarially",
     "Any distribution on Xᵐ that the learner likes",
     "Uniformly on X"], 0,
    "Criterion/PAC.lean line 63, and the design note at lines 26–37."),
  q("Is this definition realizable or agnostic?",
    ["Realizable: the sample is labelled by a target concept c ∈ C",
     "Agnostic: labels can be arbitrary",
     "Both at once",
     "Neither: there are no labels"], 0,
    "Line 66: the learner sees `fun i => (xs i, c (xs i))`. The agnostic definition is separate (lines 79–92)."),
  q("What is the error being bounded?",
    ["D-probability that the learner's hypothesis disagrees with c",
     "The number of mistakes on the sample",
     "The squared loss",
     "The KL divergence from c"], 0,
    "Line 66: `D { x | L.learn (…) x ≠ c x } ≤ ENNReal.ofReal ε`."),
 ],
 caveats=["Realizable, distribution-free, information-theoretic PAC. No agnostic setting and no running-time bound."])


node("MeasurableConceptClass",
 "MeasurableConceptClass: the regularity assumptions behind the PAC theorems",
 "This typeclass bundles three assumptions: every concept in C is measurable, every Bool-valued function on X is "
 "measurable, and the double-sample bad event is null-measurable. The second is very strong: it forces every subset "
 "of X to be measurable, which fails for Borel ℝ.",
 r"""## Plain English

**Definition (`MeasurableConceptClass`, Complexity/Measurability.lean lines 60–67).** A class with three fields:

1. `mem_measurable`: every h ∈ C is measurable;
2. `all_measurable`: **every** function c : X → Bool is measurable;
3. `wellBehaved`: [WellBehavedVC](#/node/WellBehavedVC) X C, a null-measurability condition on the
   "ghost sample" bad event used in symmetrization.

### How strong is field 2?

Bool carries the σ-algebra of all subsets, so "every c : X → Bool is measurable" means **every subset of X is
measurable**. Field 1 then follows from it. This holds:

- for countable X with the discrete σ-algebra (all the separation witnesses on ℕ);
- for any X carrying the σ-algebra of all subsets (`UniversallyMeasurableSpace`, lines 144–170, gives the instance
  automatically there).

It fails for ℝ, ℝⁿ or any uncountable standard Borel space with its Borel σ-algebra, as the docstring says
(lines 125–140). So the PAC theorems in this library, read literally, do **not** cover the classic textbook examples
(intervals, half-spaces, axis-aligned rectangles in ℝⁿ under arbitrary Borel distributions).

The README's measurability results (the Borel-analytic bridge, the Krapp–Wirth separation) are about field 3 in
Borel settings. They are not plugged back into the headline theorems: those still require field 2. See
[the measurability results](#/node/exists_measTarget_separation).

### Why is field 2 there?

The proofs need sets like {x | h x ≠ c x} to be measurable for **every** target c, and PACLearnable quantifies over
all targets in C and the learner's arbitrary outputs. Requiring all of X → Bool to be measurable is the bluntest
way to get that. A sharper version would restrict the targets and learners.
""",
 [q("What does `all_measurable : ∀ c : Concept X Bool, Measurable c` amount to?",
    ["Every subset of X is measurable",
     "Every concept in C is measurable",
     "Singletons are measurable",
     "Borel sets are measurable"], 0,
    "A function to Bool (with its discrete σ-algebra) is measurable iff the preimage of {true} is measurable; ranging over all c gives all subsets. Complexity/Measurability.lean line 65."),
  q("Which domain satisfies MeasurableConceptClass for every C (given WellBehavedVC)?",
    ["ℕ with the discrete σ-algebra",
     "ℝ with the Borel σ-algebra",
     "[0, 1] with Lebesgue measurable sets",
     "Any Polish space"], 0,
    "Countable discrete spaces make every set measurable; the docstring at lines 119–132 lists exactly this and rules out ℝⁿ/Borel."),
  q("Do the Borel-analytic results in the README discharge this typeclass for Borel-parameterized classes on ℝ?",
    ["No: they establish a null-measurability property (WellBehavedVCMeasTarget), but all_measurable still fails on Borel ℝ",
     "Yes, completely",
     "Yes, but only for finite classes",
     "They show the typeclass is inconsistent"], 0,
    "Complexity/BorelAnalyticBridge.lean lines 213–234 conclude `WellBehavedVCMeasTarget`, not `MeasurableConceptClass`."),
 ],
 caveats=[MEAS])


node("WellBehavedVC",
 "WellBehavedVC: the ghost-sample bad event is null-measurable",
 "For every distribution, target, sample size and ε, the set of pairs of samples on which some h ∈ C has a ghost-sample "
 "error gap of at least ε/2 must be null-measurable. This is what symmetrization needs in order to integrate over "
 "the bad event when C is uncountable.",
 r"""## Plain English

**Definition (`WellBehavedVC`, Complexity/Symmetrization.lean lines 1005–1013).** For every probability measure D,
every target c, every m and every ε, the set

  { (S, S′) ∈ Xᵐ × Xᵐ : ∃ h ∈ C, err_{S′}(h) − err_S(h) ≥ ε/2 }

is a `NullMeasurableSet` for Dᵐ ⊗ Dᵐ. Here err_S is the [empirical error](#/node/HasUniformConvergence) on the
sample S labelled by c, and S′ is the "ghost" sample of the symmetrization argument.

### Why it is needed

The union over the uncountably many h ∈ C need not be measurable. The textbooks either assume it away
("permissible" classes, Pollard 1984; "image-admissible Suslin", Dudley 1999) or ignore it. The README highlights
that the project only needs **null**-measurability here, weaker than the MeasurableSet hypothesis in Krapp & Wirth
(2024, arXiv:2410.10243), and that this weakening is strict
(see [the measurability results](#/node/exists_measTarget_separation)).

For countable C, or countable X with discrete σ-algebra, it holds automatically. The proof of
[online_pac_gold_separation](#/node/online_pac_gold_separation) checks it by hand for thresholds on ℕ.
""",
 [q("What kind of measurability does WellBehavedVC ask for?",
    ["NullMeasurableSet (measurable up to a null set) for the product of two sample measures",
     "MeasurableSet for the Borel σ-algebra",
     "Measurability of every concept",
     "Measurability of the learner"], 0,
    "Complexity/Symmetrization.lean line 1008: `MeasureTheory.NullMeasurableSet {…} ((Measure.pi …).prod (Measure.pi …))`."),
  q("Why can the bad event fail to be measurable?",
    ["It is an existential (union) over possibly uncountably many hypotheses h ∈ C",
     "Because the samples are finite",
     "Because ε is real",
     "Because Bool has two elements"], 0,
    "The set is `{p | ∃ h ∈ C, …}` (line 1009). Countable unions of measurable sets are measurable; uncountable ones need not be."),
  q("Is WellBehavedVC part of the fundamental theorem's hypotheses?",
    ["Yes, as the wellBehaved field of MeasurableConceptClass",
     "No, it is proved for every class",
     "Only in the compression conjunct",
     "Only for the Rademacher conjunct"], 0,
    "Complexity/Measurability.lean line 67: `wellBehaved : WellBehavedVC X C`."),
 ])


node("Shatters",
 "Shatters: C realizes every labelling of a finite set",
 "A finite set S is shattered by C if every one of the 2^|S| ways of labelling S is matched by some concept in C.",
 r"""## Plain English

**Definition (`Shatters`, Complexity/VCDimension.lean lines 22–23).** For a finite set S ⊆ X, `Shatters X C S` means:
for every labelling f : S → Bool there is c ∈ C with c(x) = f(x) for all x ∈ S.

Examples: thresholds (x ≤ n) on ℕ shatter every single point but no pair {a < b} (the labelling a ↦ false,
b ↦ true is impossible). Indicators of finite sets shatter every finite set.

The library bridges this to Mathlib's `Finset.Shatters` / `Finset.vcDim` in Bridge.lean, so that Mathlib's
Sauer–Shelah lemma can be used.
""",
 [q("How many labellings must C realize to shatter a 4-point set?",
    ["16", "4", "8", "5"], 0, "Every function S → Bool, so 2⁴ = 16 (Complexity/VCDimension.lean line 23)."),
  q("Do thresholds x ↦ (x ≤ n) on ℕ shatter the pair {1, 2}?",
    ["No: the labelling 1 ↦ false, 2 ↦ true cannot be realized",
     "Yes",
     "Only if n ≥ 2",
     "The question is ill-posed"], 0,
    "A threshold that is true at 2 is true at 1. This is why VCDim(thresholds) = 1."),
  q("Is the empty set shattered by a nonempty class?",
    ["Yes: there is exactly one labelling of ∅ and any concept realizes it",
     "No, never",
     "Only if C = Set.univ",
     "Only if X is empty"], 0,
    "With S = ∅, the condition `∀ x : S, …` is vacuous, so any c ∈ C works."),
 ])


node("VCDim",
 "VCDim: the size of the largest shattered set (possibly ⊤)",
 "The VC dimension of C is the supremum of |S| over finite sets S shattered by C, valued in ℕ ∪ {⊤}. 'VCDim X C < ⊤' "
 "is the combinatorial side of every characterization in the fundamental theorem.",
 r"""## Plain English

**Definition (`VCDim`, Complexity/VCDimension.lean lines 27–28).** `VCDim X C` is

  ⨆ over finite S with [Shatters](#/node/Shatters) X C S, of |S|,

computed in `WithTop ℕ` (ℕ with an extra top element ⊤). So VCDim X C < ⊤ means there is a finite bound on the
size of shattered sets.

Edge cases: for the empty class nothing is shattered, so the supremum over the empty family is 0. For a nonempty
class the empty set is shattered, so VCDim ≥ 0 anyway. (Contrast [LittlestoneDim](#/node/LittlestoneDim), which
uses an extra ⊥ for the empty class.)

`vcdim_univ_infinite` (Theorem/PAC.lean lines 341–367) proves the class of **all** functions on an infinite X has
VCDim = ⊤. Hence, by [vc_characterization](#/node/vc_characterization), it is not PAC learnable
(`nfl_theorem_infinite`, lines 370–379: a no-free-lunch theorem).
""",
 [q("What is VCDim of thresholds on ℕ?",
    ["1", "0", "2", "⊤"], 0,
    "Singletons are shattered, pairs are not (see Shatters). Theorem/Separation.lean docstring at line 1012."),
  q("What does VCDim X C = ⊤ mean?",
    ["For every n there is a shattered set with at least n points",
     "X is infinite",
     "C is infinite",
     "Some infinite set is shattered"], 0,
    "It is a supremum over finite sets (Complexity/VCDimension.lean line 28); ⊤ means unbounded finite sizes. That is weaker than shattering an infinite set."),
  q("What does the library prove about Set.univ on an infinite X?",
    ["VCDim = ⊤, so it is not PAC learnable (no free lunch)",
     "VCDim = |X|",
     "It is PAC learnable",
     "Nothing"], 0,
    "Theorem/PAC.lean lines 341–379 (`vcdim_univ_infinite`, `nfl_theorem_infinite`). Lines 331–338 note that the finite-X version would be false."),
 ])


node("GrowthFunction",
 "GrowthFunction: how many labellings C induces on m points",
 "The growth function π_C(m) is the largest number of distinct labellings that C induces on any m-point set. "
 "Sauer–Shelah: if VCDim = d it is at most Σ_{i ≤ d} (m choose i), polynomial in m; otherwise it is 2^m for every m.",
 r"""## Plain English

**Definition (`GrowthFunction`, Complexity/VCDimension.lean lines 38–41).** For each m, take the supremum over all
m-element sets S ⊆ X of the number of functions S → Bool that are restrictions of concepts in C.

The fifth conjunct of the [fundamental theorem](#/node/fundamental_theorem) says VCDim(C) < ⊤ iff there is a d with
π_C(m) ≤ Σ_{i=0}^{d} (m choose i) for all m ≥ d. Its two directions:

- `vcdim_finite_imp_growth_bounded` (Complexity/Generalization.lean lines 648–767): Sauer–Shelah, via the bridge to
  Mathlib's `card_shatterer_le_sum_vcDim`;
- `growth_bounded_imp_vcdim_finite` (lines 2190–2259): a shattered set of size m forces π_C(m) = 2^m, which exceeds
  the binomial sum for m > d.

In the uniform convergence proof the growth function at 2m is what multiplies the Hoeffding tail
(see [vcdim_finite_imp_uc'](#/node/vcdim_finite_imp_uc')).

**Lean detail.** The count is `Set.ncard` and the supremum is `sSup` on ℕ. Both have junk values (ncard of an
infinite set is 0; sSup of an unbounded set is 0), but here every count is at most 2^m, so they are harmless.
""",
 [q("What is the growth function of a class that shatters some m-point set?",
    ["2^m at m", "m", "m choose d", "0"], 0,
    "All 2^m labellings appear on the shattered set, and no set can have more."),
  q("What does Sauer–Shelah give when VCDim = d and m ≥ d?",
    ["π_C(m) ≤ Σ_{i=0}^{d} (m choose i), polynomial in m",
     "π_C(m) ≤ d",
     "π_C(m) = 2^d",
     "π_C(m) ≥ 2^m"], 0,
    "Theorem/PAC.lean lines 144–150 (`sauer_shelah_quantitative`) and conjunct 5 of `fundamental_theorem`."),
  q("Why are the ncard/sSup junk values harmless here?",
    ["Each count is a number of functions S → Bool, at most 2^m, so finite and bounded",
     "Lean has no junk values",
     "Because X is finite",
     "They are not harmless"], 0,
    "For fixed m the family of counts is bounded by 2^m, so sSup is a true maximum."),
 ])


node("RademacherComplexity",
 "RademacherComplexity: how well C correlates with random signs",
 "The Rademacher complexity at sample size m is the expected (over samples from D and uniform random signs) best "
 "correlation between a concept in C and the signs. Conjunct 3 of the fundamental theorem says it goes to 0 "
 "uniformly over all distributions exactly when VCDim is finite.",
 r"""## Plain English

**Definitions (Complexity/Rademacher.lean lines 178–252).**

- `rademacherCorrelation h σ xs` = (1/m) Σᵢ σᵢ · h(xᵢ), with Bool mapped to ±1 (lines 178–181).
- `EmpiricalRademacherComplexity X C xs` = the average over all 2^m sign vectors σ of
  sup_{h ∈ C} rademacherCorrelation h σ xs (lines 206–212).
- `RademacherComplexity X C D m` = the integral of the empirical version over xs ~ Dᵐ (lines 248–252).

These are the standard definitions (without absolute value, which is one of the two textbook conventions).

### The characterization

[fundamental_rademacher](#/node/fundamental_rademacher) proves: PAC learnable ⟺ for every ε > 0 there is m₀ with
RademacherComplexity X C D m < ε for **all** probability measures D and all m ≥ m₀. The m₀ must not depend on D.

**Lean detail.** The outer integral is a Bochner integral. If the integrand is not integrable, Mathlib's convention
makes the integral 0. That would make "vanishing" easier, not harder. But the converse direction of the theorem
constructs, for every m, a distribution with Rademacher complexity at least 1/2 when VCDim = ⊤
(`rademacher_lower_bound_on_shattered`, lines 1217–1572). That distribution is uniform on a finite set, where the
integral is a genuine finite average. So the equivalence carries real content.
""",
 [q("What does Rademacher complexity average over?",
    ["Samples xs ~ Dᵐ and uniformly random sign vectors σ",
     "Only over signs, for a fixed sample",
     "Over all concepts in C",
     "Over all distributions D"], 0,
    "Lines 206–212 average over all σ; lines 248–252 integrate that over Dᵐ."),
  q("In conjunct 3, can m₀ depend on the distribution D?",
    ["No: ∃ m₀ comes before ∀ D",
     "Yes",
     "Only for continuous D",
     "There is no m₀"], 0,
    "Theorem/PAC.lean lines 266–268: `∀ ε > 0, ∃ m₀, ∀ D, IsProbabilityMeasure D → ∀ m ≥ m₀, …`."),
  q("Why is the integral's junk value (0 for non-integrable integrands) not a loophole?",
    ["The hard direction exhibits explicit finite-support distributions with complexity ≥ 1/2 whenever VCDim = ⊤",
     "Because Lean has no junk values",
     "Because all functions are integrable",
     "It is a loophole that makes the theorem vacuous"], 0,
    "Complexity/Rademacher.lean lines 1217–1222 state `rademacher_lower_bound_on_shattered`, used at Theorem/PAC.lean line 288."),
 ])


node("SampleComplexity",
 "SampleComplexity: the least sample size that achieves (ε, δ)",
 "SampleComplexity(ε, δ) is the smallest m such that some learner achieves error ≤ ε with probability ≥ 1 − δ on m "
 "samples, for every distribution and target. When no m works the Lean value is 0, by the convention for sInf of "
 "the empty set.",
 r"""## Plain English

**Definition (`SampleComplexity`, Complexity/Generalization.lean lines 35–44).** The infimum (`sInf` on ℕ) of the
set of m for which there exists a [BatchLearner](#/node/BatchLearner) L with

  Dᵐ{ error of L ≤ ε } ≥ 1 − δ for every probability measure D and every c ∈ C.

This is the textbook m_C(ε, δ) of the realizable setting.

**Lean detail.** `sInf ∅ = 0` in ℕ. So if C is not PAC learnable at (ε, δ), SampleComplexity is 0, not ∞. The
theorems about it always come with a PAC witness or a VC assumption, so this does not create false conclusions,
but it means a lower bound on SampleComplexity alone says nothing unless the set is nonempty.

### What is proved

- Upper: for any PAC witness (L, mf), SampleComplexity(ε, δ) ≤ mf(ε, δ) (Theorem/PAC.lean lines 190–207). This is
  immediate from the definition.
- Lower: with VCDim = d ≥ 1, ε ≤ 1/4, δ ≤ 1/7, SampleComplexity(ε, δ) ≥ ⌈(d − 1)/2⌉
  (`sample_complexity_lower_bound`, Complexity/GeneralizationResults.lean lines 230–257). The textbook lower bound
  is Ω((d + log(1/δ))/ε). This one is linear in d but has no ε.
""",
 [q("What is SampleComplexity when no sample size works?",
    ["0, because sInf of the empty set of naturals is 0",
     "⊤ (infinity)",
     "It is undefined and Lean rejects it",
     "1"], 0,
    "Complexity/Generalization.lean line 37 uses `sInf` on ℕ, and Mathlib sets `sInf ∅ = 0`."),
  q("How does the proved lower bound depend on ε?",
    ["It does not: ⌈(d − 1)/2⌉ for every ε ≤ 1/4",
     "Like 1/ε",
     "Like log(1/ε)",
     "Like 1/ε²"], 0,
    "Theorem/PAC.lean line 179: `Nat.ceil ((d - 1 : ℝ) / 2) ≤ SampleComplexity X C ε δ`."),
  q("Is SampleComplexity distribution-free?",
    ["Yes: one learner must work for every D at that m",
     "No, it depends on D",
     "Only for finite X",
     "It is defined per target c"], 0,
    "Lines 37–40: `∃ L, ∀ D, … ∀ c ∈ C, …`."),
 ])


node("CompressionSchemeWithInfo",
 "CompressionSchemeWithInfo: keep a few sample points plus a finite tag",
 "A compression scheme with side information keeps at most K labelled points of any sample, plus a tag from a fixed "
 "finite set, and must rebuild a classifier correct on the whole sample whenever the sample is realizable by C. "
 "Its size is K plus the number of tags.",
 r"""## Plain English

**Definition (`CompressionSchemeWithInfo`, Complexity/Structures.lean lines 215–238).** The data:

- `Info`, a type with a `Fintype` instance (the finite set of tags);
- `compress`, mapping any sample S (of any size m) to a pair (Z, i): a Finset Z of labelled points and a tag i;
- `reconstruct`, mapping (Z, i) to a classifier X → Y;
- `kernelSize` K;

and three laws: |Z| ≤ K; Z ⊆ the points of S; and **correctness**: if some c ∈ C agrees with all labels of S, then
reconstruct(Z, i) agrees with every point of S.

`CompressionSchemeWithInfo.size` (lines 246–249) is K + |Info|, and `CompressionSchemeWithInfo0`
(Complexity/Compression.lean lines 626–627) is the same structure with Info in `Type 0`, a technical universe fix.

### Faithfulness

This matches the Moran–Yehudayoff notion "κ : LC(∞) → LC(k) × I with I finite" (as the docstring at lines 205–207
says). The guard "only on realizable samples" is essential: without it no scheme exists for nonempty X, and the
docstring of `CompressionScheme` (lines 30–39) records that bug and its fix. The scheme without side information,
`CompressionScheme`, is lines 40–56.
""",
 [q("Can the kernel size K grow with the sample size m?",
    ["No: K and the tag set are fixed for the scheme; compress must work for every m",
     "Yes, like log m",
     "Yes, linearly",
     "Only the tag set is fixed"], 0,
    "`kernelSize : ℕ` and `Info` are fields of the structure, and `compress_small` holds `∀ {m}` (Complexity/Structures.lean lines 226–229)."),
  q("Where must the kept points come from?",
    ["From the sample itself",
     "Anywhere in X",
     "From a fixed finite subset of X",
     "From the tag set"], 0,
    "`compress_sub : ↑(compress S).1 ⊆ Set.range S` (lines 231–232)."),
  q("What is CompressionSchemeWithInfo.size?",
    ["kernelSize + the number of tags",
     "kernelSize · log₂(number of tags)",
     "The number of tags only",
     "The sample size"], 0,
    "Complexity/Structures.lean lines 246–249; the docstring notes the paper's k + log₂(|I|+1) and that k + |I| is a simpler upper bound."),
 ])


node("HasUniformConvergence",
 "HasUniformConvergence: empirical errors are uniformly close to true errors",
 "C has uniform convergence if, for every ε, δ, one sample size m₀ (independent of distribution and target) ensures "
 "that with probability ≥ 1 − δ every h ∈ C has empirical error within ε of its true error. This is the bridge "
 "between finite VC dimension and PAC learning.",
 r"""## Plain English

**Definition (`HasUniformConvergence`, Complexity/Generalization.lean lines 811–822).** For all ε, δ > 0 there is
m₀ such that for every probability measure D, every target c and every m ≥ m₀,

  Dᵐ { xs : for all h ∈ H, |TrueErr_D(h, c) − EmpErr_xs(h, c)| < ε } ≥ 1 − δ.

- `TrueErrorReal` (lines 176–179) is D{x | h x ≠ c x}, as a real number.
- `EmpiricalError` (lines 84–88) is the average 0-1 loss on the sample (and 0 when m = 0).

**The quantifier order matters.** The docstring (lines 800–810) records a repair: m₀ originally depended on D and
c, which made `uc_imp_pac` unprovable. Now m₀ comes before ∀ D, ∀ c, which is what "uniform" means.

This is a lemma-level notion: it is not one of the five conjuncts of the fundamental theorem, but it is the middle
step of the hard direction:
[VCDim < ⊤](#/node/vcdim_finite_imp_uc') ⟹ uniform convergence ⟹ [PAC](#/node/uc_imp_pac).

Note the target c is arbitrary here, not just c ∈ C. That is harmless (the statement is stronger).
""",
 [q("In HasUniformConvergence, can m₀ depend on the distribution D?",
    ["No: ∃ m₀ comes before ∀ D",
     "Yes",
     "Only through ε",
     "Only through the target c"], 0,
    "Complexity/Generalization.lean lines 814–815."),
  q("What must hold on the good samples?",
    ["Every h ∈ H simultaneously has |true error − empirical error| < ε",
     "Some h ∈ H has small error",
     "The learner's output has small error",
     "The empirical error is 0"], 0,
    "Lines 818–821: `∀ h ∈ H, |TrueErrorReal … − EmpiricalError …| < ε`."),
  q("Is uniform convergence one of the conjuncts of fundamental_theorem?",
    ["No: it is proved and used inside the proof only",
     "Yes, the first",
     "Yes, the last",
     "It is assumed as a hypothesis"], 0,
    "The five conjuncts are listed at Theorem/PAC.lean lines 297–322."),
 ])


node("OnlineLearner",
 "OnlineLearner: predict, see the label, update",
 "An online learner has an internal state, a prediction rule and an update rule. It predicts a label for each new "
 "point, then sees the true label and updates its state. Mistakes are counted along the way.",
 r"""## Plain English

**Definition (`OnlineLearner`, Learner/Core.lean lines 38–46).** A state type `State : Type`, an initial state
`init`, `predict : State → X → Y` and `update : State → X → Y → State`.

`OnlineLearner.mistakes L c seq` (Criterion/Online.lean lines 19–28) runs L along the list of points `seq`, with
labels given by c, and counts how often the prediction differs from c(x).

The learner is deterministic. That is standard for the mistake-bound model: a deterministic learner facing a fixed
sequence is equivalent to facing an adaptive adversary, because the adversary can simulate it.
""",
 [q("When does the learner see the true label of x?",
    ["After it has predicted on x (the update step receives the label)",
     "Before predicting",
     "Never",
     "Only at the end"], 0,
    "Learner/Core.lean lines 44–46: `predict : State → X → Y`, then `update : State → X → Y → State`."),
  q("Is the online learner allowed to randomize?",
    ["No: predict is a deterministic function",
     "Yes, it gets random bits",
     "Only in the first round",
     "Only for infinite X"], 0,
    "Nothing random appears in the structure (lines 38–46)."),
  q("What does OnlineLearner.mistakes count?",
    ["The number of points in seq where the prediction differs from c",
     "The number of state updates",
     "The length of seq",
     "The number of distinct predictions"], 0,
    "Criterion/Online.lean lines 21–28."),
 ])


node("OnlineLearnable",
 "OnlineLearnable: some learner has a finite mistake bound",
 "C is online learnable if there is an M and an online learner that makes at most M mistakes on every finite sequence "
 "of points, whatever the target in C. This is Littlestone's mistake-bound model, realizable case.",
 r"""## Plain English

**Definitions (Criterion/Online.lean lines 32–40).**

- `MistakeBounded X Y C M`: there is an [OnlineLearner](#/node/OnlineLearner) L such that for every c ∈ C and every
  list of points `seq`, L makes at most M mistakes.
- `OnlineLearnable X Y C`: MistakeBounded for some M ∈ ℕ.

So the bound is uniform over targets and sequences. [littlestone_characterization](#/node/littlestone_characterization)
says this happens exactly when [LittlestoneDim](#/node/LittlestoneDim) is finite, and
`optimal_mistake_bound_eq_ldim` says the best M **is** the Littlestone dimension.
""",
 [q("Can the mistake bound M depend on the target c?",
    ["No: M and the learner come first, then ∀ c ∈ C",
     "Yes",
     "Only through the sequence length",
     "M is always 1"], 0,
    "Criterion/Online.lean lines 34–36 and 40."),
  q("Is this the agnostic (regret) setting?",
    ["No: labels always come from a target c ∈ C (realizable)",
     "Yes",
     "Both",
     "Neither: there are no labels"], 0,
    "`mistakes c seq` uses c to label the points (lines 19–28). Regret is a separate definition (lines 61–66)."),
  q("Does online learnability imply PAC learnability in this library?",
    ["Yes, under MeasurableConceptClass: online_imp_pac",
     "No",
     "Only for finite classes",
     "Only in the agnostic case"], 0,
    "Theorem/Separation.lean lines 132–146."),
 ])


node("LittlestoneDim",
 "LittlestoneDim: the depth of the deepest shattered mistake tree",
 "The Littlestone dimension is the largest n such that some complete binary tree of depth n, labelled by points of X, "
 "is shattered path-wise: every root-to-leaf path of yes/no answers is consistent with some concept in C. The empty "
 "class gets ⊥, any other class a value in ℕ ∪ {⊤}.",
 r"""## Plain English

**Definitions (Complexity/GameInfra.lean lines 35–80).**

- `LTree X n`: a complete binary tree of depth n with a point of X at every internal node (lines 35–37).
- `LTree.isShattered C T` (lines 41–46), recursively: a leaf is shattered by C if C is **nonempty**. A node with
  point x and subtrees l, r is shattered if C has a concept with c(x) = true and one with c(x) = false, l is
  shattered by {c ∈ C | c x = true}, and r is shattered by {c ∈ C | c x = false}.
- `LittlestoneDim X C` (lines 73–80): the supremum of n over shattered trees of depth n, in `WithBot (WithTop ℕ)`.

### Why "path-wise"

The concepts available in a subtree are those **consistent with the answers so far**. That is Littlestone's
definition. The README says an earlier "branch-wise" definition (Complexity/Littlestone.lean lines 43–53) admitted a
counterexample and was replaced.

### Examples

- Thresholds on ℕ: Ldim = ⊤ (any depth can be shattered by choosing points in binary-search order;
  `threshold_shattered_all_depths`, Theorem/Separation.lean), although VCDim = 1.
- VCDim ≤ Ldim is classical. The library proves it for the old branch-wise definition
  (`BranchWiseLittlestoneDim_ge_VCDim`, Complexity/Littlestone.lean lines 107–108), but for the path-wise
  definition it is only recorded as a conditional reduction (`hasse_open_reduction`,
  Complexity/IndependentVC/StructureClosures.lean lines 654–665). The online ⟹ PAC theorem goes around it, via
  "mistake bound M ⟹ VCDim ≤ M" (Theorem/Separation.lean lines 116–128).
""",
 [q("At an internal node with point x, which concepts are available for the left (true) subtree?",
    ["Those concepts in C with c(x) = true",
     "All of C",
     "Those with c(x) = false",
     "Only one fixed concept"], 0,
    "Complexity/GameInfra.lean line 45: `l.isShattered {c ∈ C | c x = true}`."),
  q("Why is LittlestoneDim valued in WithBot (WithTop ℕ)?",
    ["So the empty class can have value ⊥, below 0, while infinite dimension is ⊤",
     "Because trees can have negative depth",
     "For computability",
     "It is a typo"], 0,
    "Lines 71–72: 'returns WithBot (WithTop ℕ) so Ldim(∅) = ⊥'. A leaf is shattered only by a nonempty class."),
  q("What is the Littlestone dimension of thresholds on ℕ?",
    ["⊤ (infinite)", "1", "2", "0"], 0,
    "`ldim_threshold_top` in Theorem/Separation.lean, used at line 1230. This is why thresholds are PAC- but not online-learnable."),
 ])


node("SOA",
 "SOA: the Standard Optimal Algorithm",
 "The SOA remembers all labelled points so far and predicts, for a new x, the label whose consistent sub-class has the "
 "larger Littlestone dimension. Every mistake then strictly lowers the Littlestone dimension of what is left, so it "
 "makes at most Ldim(C) mistakes.",
 r"""## Plain English

**Definition (`SOA`, Complexity/GameInfra.lean lines 151–158).** State = the list of labelled points seen. To predict
on x, let V be the version space (concepts of C consistent with the history; `versionSpace`, lines 146–148), and
compare LittlestoneDim{c ∈ V | c x = true} with LittlestoneDim{c ∈ V | c x = false}. Predict true if the first is
at least the second, otherwise false. Update by appending (x, label).

### Why it works

If the SOA predicts y and the truth is the other label, the true side had Littlestone dimension **strictly smaller**
than the current version space's (if both sides had dimension ≥ the current value d, x would root a shattered tree
of depth d + 1). So each mistake lowers the version space's Ldim by at least 1, and it starts at Ldim(C). This is
`soa_mistakes_bounded` (Theorem/Online.lean lines 322–386).

Like every learner here, it is not computable in general: it compares Littlestone dimensions of infinite classes.
""",
 [q("How many mistakes does the SOA make on a class with Littlestone dimension d?",
    ["At most d", "At most 2^d", "At most d²", "Exactly d always"], 0,
    "Theorem/Online.lean lines 389–413 (`backward_direction`) use the SOA with bound d."),
  q("What does the SOA's state store?",
    ["The full list of labelled points seen so far",
     "Only the last point",
     "A probability distribution on C",
     "A counter of mistakes"], 0,
    "Complexity/GameInfra.lean lines 152–153 and 158: `State := List (X × Bool)`, update appends."),
  q("Is the SOA an algorithm you can run?",
    ["Not in general: it compares Littlestone dimensions, which are suprema over infinitely many trees",
     "Yes, in linear time",
     "Yes, by native_decide",
     "Only on ℕ"], 0,
    "`LittlestoneDim` is a noncomputable supremum (lines 73–80); the SOA is `noncomputable def` (line 151)."),
 ])


node("EXLearnable",
 "EXLearnable: identification in the limit from text",
 "C is EX-learnable if one learner, given longer and longer prefixes of any enumeration of the positive examples of "
 "any c ∈ C, eventually outputs exactly c and never changes its mind again.",
 r"""## Plain English

**Definition (`EXLearnable`, Criterion/Gold.lean lines 31–36).** There is a [GoldLearner](#/node/GoldLearner) L such
that for every c ∈ C and every [text](#/node/TextPresentation) T for c, there is a time t₀ after which
L(data up to t) = c for all t ≥ t₀.

`dataUpTo T t` (lines 25–26) is the list of the first t + 1 observations.

### Comparison with Gold (1967)

- **Positive data only** (text), not informant (positive and negative data). Correct for Gold's theorem.
- **Extensional convergence.** The conjecture must equal c as a function. There are no program indices, so this
  sits between Gold's EX (syntactic convergence to one index) and BC (behaviourally correct) learning. The file
  also defines `BCLearnable` (lines 40–45), which asks for pointwise agreement and so is equivalent by function
  extensionality.
- **No computability.** Learners are arbitrary functions.
""",
 [q("What data does an EX-learner receive?",
    ["Growing prefixes of an enumeration of the positive examples of the target",
     "Random labelled samples",
     "All of X labelled",
     "Membership queries"], 0,
    "Criterion/Gold.lean lines 33–36 with `TextPresentation` (Data.lean lines 46–52)."),
  q("After convergence, how many more times may the learner change its conjecture?",
    ["None: for all t ≥ t₀ the conjecture equals c",
     "Finitely many",
     "Infinitely many, as long as each is correct",
     "One"], 0,
    "Line 36: `∀ t ≥ t₀, L.conjecture (dataUpTo T.toDataStream t) = c`."),
  q("Does EXLearnable require a computable learner?",
    ["No", "Yes", "Only for finite C", "Only for countable X"], 0,
    "GoldLearner (Learner/Core.lean lines 50–52) is any function."),
 ],
 caveats=["Extensional convergence (to c as a function), not convergence to a fixed program index as in Gold's original model."])


node("GoldLearner",
 "GoldLearner: a conjecture for every finite data list",
 "A Gold-style learner is any function from finite lists of labelled examples to concepts: after each new example it "
 "outputs its current guess.",
 r"""## Plain English

**Definition (`GoldLearner`, Learner/Core.lean lines 50–52).** One field, `conjecture : List (X × Y) → Concept X Y`.

The three learner types (batch, online, Gold) are deliberately kept separate. The README argues that a common
parent type would erase the feature each characterization theorem relies on: the distribution-free sample size
(batch), commitment before seeing the label (online), and stabilization on growing prefixes (Gold).
""",
 [q("What does a GoldLearner output?",
    ["A full concept X → Y after each finite data list",
     "A single label",
     "A probability",
     "A natural number index"], 0, "Learner/Core.lean line 52."),
  q("Is a GoldLearner required to be consistent with the data it has seen?",
    ["No, any function is allowed",
     "Yes, always",
     "Only after convergence",
     "Only for finite concepts"], 0,
    "There is no consistency field in the structure (lines 50–52)."),
  q("Why doesn't the library unify BatchLearner, OnlineLearner and GoldLearner?",
    ["Each characterization depends on a structural feature specific to its learner type",
     "Lean cannot express a common type",
     "Because of universe levels",
     "They are unified"], 0,
    "Learner/Core.lean lines 20–23 and README section 'Why the learner types cannot unify'."),
 ])


node("TextPresentation",
 "TextPresentation: an enumeration of the positive examples",
 "A text for c is an infinite stream of examples, all positive, all genuinely in c, in which every positive example of "
 "c appears at least once.",
 r"""## Plain English

**Definition (`TextPresentation`, Data.lean lines 46–52).** Extends a `DataStream` (a function ℕ → X × Bool,
lines 39–41) with three laws:

- `positive`: every observation's label is true;
- `correct`: every observed point x has c(x) = true;
- `exhaustive`: every x with c(x) = true is observed at some time.

Repetitions are allowed. Since the stream must emit a positive example at **every** time step, a concept with no
positive examples has no text at all. Classical texts allow a pause symbol for this case. It does not affect the
headlines.
""",
 [q("Can a text repeat an example?",
    ["Yes: nothing forbids it", "No", "Only finitely often", "Only the first example"], 0,
    "Data.lean lines 46–52 require only positivity, correctness and exhaustiveness."),
  q("Does a text contain negative examples?",
    ["No: every label is true", "Yes", "Only finitely many", "Exactly one"], 0, "`positive : ∀ t, (observe t).2 = true` (line 48)."),
  q("Does the empty concept (no positives) have a text?",
    ["No: a text must emit a positive example at every step",
     "Yes, the empty stream",
     "Yes, any stream",
     "Only for finite X"], 0,
    "`correct` at line 50 would need some x with c x = true at time 0."),
 ])
