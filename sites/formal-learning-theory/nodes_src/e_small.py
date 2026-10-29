import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import node_maker, q

NODES = []
node = node_maker(NODES)

# Small supporting definitions that headline statements mention.


node("HypothesisSpace",
 "HypothesisSpace: the set a learner draws its guesses from",
 "Literally the same type as a concept class, a set of functions X → Y. The separate name marks the learner's side.",
 r"""## Plain English

**Definition (`HypothesisSpace`, Basic.lean line 76).** `Set (Concept X Y)`, identical to
[ConceptClass](#/node/ConceptClass). A [BatchLearner](#/node/BatchLearner) carries one and promises its outputs lie
in it. [HasUniformConvergence](#/node/HasUniformConvergence) is stated for a hypothesis space H, and the headlines
apply it with H = C.
""",
 [q("How is HypothesisSpace X Y defined?",
    ["As Set (Concept X Y), the same as ConceptClass", "As a list of concepts", "As a measure on concepts", "As a finite set"], 0,
    "Basic.lean line 76."),
  q("In the headlines, which hypothesis space is uniform convergence applied to?",
    ["The concept class C itself", "All functions", "A finite subset of C", "The empty set"], 0,
    "`vcdim_finite_imp_uc'` concludes `HasUniformConvergence X C` (Complexity/Symmetrization.lean line 2669)."),
  q("Does a BatchLearner's hypothesis space have to equal the target class?",
    ["No", "Yes", "Only for finite X", "Only in the agnostic case"], 0,
    "Nothing in Learner/Core.lean lines 29–35 or Criterion/PAC.lean lines 55–68 links them."),
 ])


node("EmpiricalError",
 "EmpiricalError: average loss on the sample",
 "The empirical error of h on a labelled sample of size m is the average of the loss over the m points (and 0 for the "
 "empty sample). With 0-1 loss it is the fraction of sample points h gets wrong.",
 r"""## Plain English

**Definition (`EmpiricalError`, Complexity/Generalization.lean lines 84–88).** For m > 0,
(1/m) Σᵢ loss(h(xᵢ), yᵢ); for m = 0 it is 0. With [zeroOneLoss](#/node/zeroOneLoss) it counts the fraction of
mistakes. It is a deterministic function of the sample, so no measurability issue arises here.
""",
 [q("What is the empirical error on the empty sample?",
    ["0, by convention", "1", "Undefined", "∞"], 0, "Complexity/Generalization.lean line 87: `if m = 0 then 0`."),
  q("With 0-1 loss, what is the empirical error of a hypothesis consistent with the sample?",
    ["0", "1", "1/2", "It depends on D"], 0, "Every term of the sum is 0; this is used in `uc_imp_pac` (lines 920–931)."),
  q("Does the empirical error depend on the distribution D?",
    ["No: only on h, the sample and the loss", "Yes", "Only through m", "Only for infinite X"], 0,
    "The definition (lines 84–88) has no measure argument."),
 ])


node("zeroOneLoss",
 "zeroOneLoss: 0 if right, 1 if wrong",
 "The 0-1 loss charges 1 for a wrong label and 0 for a right one. All the PAC headlines use it.",
 r"""## Plain English

**Definition (`zeroOneLoss`, Basic.lean lines 161–162).** `zeroOneLoss Y y₁ y₂ = if y₁ = y₂ then 0 else 1`. Used in
[EmpiricalError](#/node/EmpiricalError), [WellBehavedVC](#/node/WellBehavedVC) and
[HasUniformConvergence](#/node/HasUniformConvergence).
""",
 [q("What is zeroOneLoss Bool true false?", ["1", "0", "−1", "1/2"], 0, "The labels differ, so the loss is 1 (Basic.lean line 162)."),
  q("What does the average 0-1 loss on a sample measure?", ["The fraction of misclassified points", "The squared error", "The margin", "The log-likelihood"], 0,
    "Each misclassified point contributes 1, each correct one 0."),
  q("Which loss does the realizable PAC definition implicitly use?",
    ["0-1 loss (the D-probability of disagreement)", "Squared loss", "Hinge loss", "No loss"], 0,
    "PACLearnable measures `D { x | L.learn … x ≠ c x }` (Criterion/PAC.lean line 66)."),
 ])


node("TrueErrorReal",
 "TrueErrorReal: the probability of disagreement, as a real number",
 "The true error of h against target c under D is D{x | h(x) ≠ c(x)}. TrueErrorReal is that number converted from "
 "extended nonnegative reals to ℝ, so it can be subtracted from empirical errors.",
 r"""## Plain English

**Definitions (Complexity/Generalization.lean lines 169–179).** `TrueError X h c D = D {x | h x ≠ c x}` in `ENNReal`,
and `TrueErrorReal` is its `.toReal`. For a probability measure the value is finite, so nothing is lost (the
docstring notes that `toReal` would send ∞ to 0 in general).

If {x | h x ≠ c x} is not measurable, D of it is the outer measure. Under
[MeasurableConceptClass](#/node/MeasurableConceptClass) every such set is measurable.
""",
 [q("What does TrueErrorReal X h c D measure?",
    ["The D-probability that h and c disagree", "The empirical error", "The VC dimension of h", "The distance between h and c in sup norm"], 0,
    "Complexity/Generalization.lean lines 169–179."),
  q("Why convert to ℝ?", ["To take differences and absolute values with empirical errors", "For computability", "To allow negative errors", "It is not converted"], 0,
    "HasUniformConvergence uses `|TrueErrorReal … − EmpiricalError …|` (lines 819–821)."),
  q("Can TrueErrorReal exceed 1 for a probability measure D?", ["No", "Yes", "Only for infinite X", "Only if h is not measurable"], 0,
    "A probability measure gives every set measure at most 1."),
 ])


node("CompressionSchemeWithInfo0",
 "CompressionSchemeWithInfo0: the same scheme, tags in universe 0",
 "A technical abbreviation: a CompressionSchemeWithInfo whose tag type lives in Type 0. It exists only to get around "
 "a universe-elaboration problem.",
 r"""## Plain English

**Definition (`CompressionSchemeWithInfo0`, Complexity/Compression.lean lines 626–627).** The abbreviation
`CompressionSchemeWithInfo.{u, 0, 0} X Y C`. The docstring (lines 620–625) explains that the concrete tag type
`Fin T → Finset (Fin K)` is in `Type 0`, while Lean would otherwise infer `Info : Type u` from X. Mathematically it is
the same notion as [CompressionSchemeWithInfo](#/node/CompressionSchemeWithInfo).
""",
 [q("Is CompressionSchemeWithInfo0 a different mathematical notion?", ["No, only a universe pin", "Yes, it has no side information", "Yes, it is size 0", "Yes, it is unlabelled"], 0,
    "Complexity/Compression.lean lines 620–627."),
  q("What does the 0 refer to?", ["The universe of the Info type", "The kernel size", "The number of tags", "The sample size"], 0, "The `.{u, 0, 0}` universe arguments."),
  q("Which headline uses it?", ["The compression conjunct of the fundamental theorem", "The Littlestone characterization", "Gold's theorem", "PAC-Bayes"], 0,
    "Theorem/PAC.lean line 298."),
 ])


node("CompressionSchemeWithInfo.size",
 "CompressionSchemeWithInfo.size: kernel size plus number of tags",
 "The size of a scheme with side information is its kernel bound K plus the number of tags |I|.",
 r"""## Plain English

**Definition (`CompressionSchemeWithInfo.size`, Complexity/Structures.lean lines 246–249).** `kernelSize + Fintype.card Info`.
The docstring notes the paper uses K + log₂(|I| + 1) and that K + |I| is a simpler upper bound. In the headline the
size appears only as "∃ k, cs.size = k", which holds for every scheme, so the choice is irrelevant there. It does matter
in the reverse direction of [the compression theorem](#/node/fundamental_vc_compression_with_info), which uses
s = K + |I| to choose the size of the shattered set.
""",
 [q("What is size for a scheme with kernel size 3 and 4 tags?", ["7", "12", "3 + log₂ 5", "4"], 0, "3 + 4 (Complexity/Structures.lean lines 246–249)."),
  q("Does '∃ k, cs.size = k' add any condition beyond the scheme existing?", ["No: take k = cs.size", "Yes, k must be ≤ VCDim", "Yes, k must be 0", "Yes, k must be prime"], 0,
    "Any natural number equals itself."),
  q("Where does size matter in the proofs?", ["In compression ⟹ finite VC, to pick N = 2(s+1)²", "Nowhere", "In the PAC proof", "In Gold's theorem"], 0,
    "Complexity/Compression.lean lines 1229–1231."),
 ])


node("MistakeBounded",
 "MistakeBounded: some learner makes at most M mistakes",
 "MistakeBounded X Y C M says one online learner makes at most M mistakes on every finite sequence of points, for every "
 "target in C.",
 r"""## Plain English

**Definition (`MistakeBounded`, Criterion/Online.lean lines 32–36).** ∃ an [OnlineLearner](#/node/OnlineLearner) L,
∀ c ∈ C, ∀ seq, `L.mistakes c seq ≤ M`. [OnlineLearnable](#/node/OnlineLearnable) is "MistakeBounded for some M", and
`OptimalMistakeBound` (Complexity/Generalization.lean lines 72–75) is the least such M.
""",
 [q("Is M allowed to depend on the sequence length?", ["No: one M for all sequences", "Yes", "Only logarithmically", "Only for infinite X"], 0, "Criterion/Online.lean lines 34–36."),
  q("Is MistakeBounded C 0 possible for a class with two concepts that differ somewhere?", ["No: an adversary can ask the point where they differ", "Yes, always", "Only if X is finite", "Only for Bool labels"], 0,
    "One of the two answers is a mistake for some target."),
  q("What is the least M for which MistakeBounded holds (for nonempty C)?", ["The Littlestone dimension", "The VC dimension", "|C|", "log |C|"], 0,
    "`optimal_mistake_bound_eq_ldim`, Theorem/Online.lean lines 440–443."),
 ])


node("LTree",
 "LTree: complete binary trees of points",
 "LTree X n is a complete binary tree of depth n with a point of X at every internal node. Shattered LTrees define the "
 "Littlestone dimension.",
 r"""## Plain English

**Definition (`LTree`, Complexity/GameInfra.lean lines 35–37).** Either a `leaf` (depth 0) or a `branch x l r` with
x : X and two subtrees of depth n, giving depth n + 1. The depth is in the type, so every tree is complete. Read the
left subtree as "the answer at x was true", the right as "false". See [LittlestoneDim](#/node/LittlestoneDim).
""",
 [q("How many internal nodes does an LTree of depth 3 have?", ["7", "3", "8", "6"], 0, "1 + 2 + 4 = 7; the tree is complete."),
  q("Can points repeat in an LTree?", ["Yes, nothing forbids it", "No", "Only at leaves", "Only on one path"], 0, "The constructor (line 37) takes any x : X."),
  q("Which subtree corresponds to the answer 'true' at x?", ["The left one", "The right one", "Both", "Neither"], 0,
    "Complexity/GameInfra.lean line 45: `l.isShattered {c ∈ C | c x = true}`."),
 ])


node("versionSpace",
 "versionSpace: the concepts consistent with the history",
 "The version space of C after a history of labelled points is the set of concepts in C that agree with every one of "
 "them.",
 r"""## Plain English

**Definition (`versionSpace`, Complexity/GameInfra.lean lines 146–148).** `{c ∈ C | ∀ p ∈ history, c p.1 = p.2}`.
The [SOA](#/node/SOA) recomputes it at every step. With the empty history it is C itself.
""",
 [q("What is versionSpace C []?", ["C", "∅", "All functions", "A singleton"], 0, "With no data every concept is consistent; used at Theorem/Online.lean lines 401–404."),
  q("Can the version space only shrink as data arrives?", ["Yes: more constraints, fewer survivors", "No, it can grow", "It stays the same", "It doubles"], 0,
    "Adding a point adds a condition."),
  q("If the target c ∈ C labels the history, is c in the version space?", ["Yes", "No", "Only at the start", "Only if C is finite"], 0,
    "c agrees with its own labels."),
 ])


node("EmpiricalRademacherComplexity",
 "EmpiricalRademacherComplexity: correlation with random signs on a fixed sample",
 "For a fixed sample, average over all 2^m sign vectors σ the best correlation (1/m) Σ σᵢ h(xᵢ) (labels as ±1) "
 "achieved by any h ∈ C.",
 r"""## Plain English

**Definition (`EmpiricalRademacherComplexity`, Complexity/Rademacher.lean lines 206–212).** 0 if m = 0, else the
uniform average over σ ∈ {±1}ᵐ of sup_{h ∈ C} `rademacherCorrelation h σ xs`. It lies in [−1, 1] (and ≤ 1 is proved,
lines 214–246). [RademacherComplexity](#/node/RademacherComplexity) integrates it over samples.

A rich class can match any sign pattern on the sample, giving value 1. A single concept gives value 0 on average.
""",
 [q("What is the empirical Rademacher complexity when C shatters the sample's distinct points (m distinct points)?", ["1", "0", "1/2", "1/m"], 0,
    "For every σ some h matches it exactly, giving correlation 1."),
  q("What does it average over?", ["All 2^m sign vectors, uniformly", "Samples from D", "Concepts in C", "Labels from c"], 0, "Lines 209–212."),
  q("How is a Bool label turned into a number?", ["true ↦ 1, false ↦ −1", "true ↦ 1, false ↦ 0", "Via a sigmoid", "It is not"], 0,
    "`boolToSign` (Complexity/Rademacher.lean line 34)."),
 ])


node("DataStream",
 "DataStream: an infinite sequence of labelled examples",
 "A data stream is just a function from time steps ℕ to labelled examples.",
 r"""## Plain English

**Definition (`DataStream`, Data.lean lines 39–41).** One field, `observe : ℕ → X × Y`. A
[TextPresentation](#/node/TextPresentation) adds the conditions that make it an enumeration of a concept's positives.
""",
 [q("What is the type of observe?", ["ℕ → X × Y", "List (X × Y)", "X → Y", "Measure (X × Y)"], 0, "Data.lean line 41 (TimeStep is ℕ, line 33)."),
  q("Must a DataStream cover every point of X?", ["No, that is added by TextPresentation's exhaustive field", "Yes", "Only for finite X", "Only positives"], 0,
    "Data.lean lines 39–41 have no conditions."),
  q("Is a DataStream random?", ["No, it is a fixed sequence", "Yes, i.i.d.", "Yes, Markov", "It depends on the learner"], 0, "It is a plain function."),
 ])


node("dataUpTo",
 "dataUpTo: the first t + 1 observations",
 "dataUpTo T t is the list of observations at times 0, 1, …, t. Gold learners are judged on these growing prefixes.",
 r"""## Plain English

**Definition (`dataUpTo`, Criterion/Gold.lean lines 25–26).** `(List.range (t + 1)).map T.observe`. Note the + 1:
`DataStream.prefix T t` (Complexity/MindChange.lean lines 20–21) has only t observations, and
[mind_change_characterization](#/node/mind_change_characterization) bridges the two with an off-by-one shift.
""",
 [q("How many observations are in dataUpTo T 0?", ["1", "0", "2", "Infinitely many"], 0, "`List.range 1` has one element."),
  q("How does dataUpTo T t relate to DataStream.prefix T t?", ["It equals prefix T (t + 1)", "It equals prefix T t", "They are unrelated", "It equals prefix T (t − 1)"], 0,
    "Theorem/Gold.lean lines 214–215 (`bridge`)."),
  q("In what order are the observations listed?", ["By time, earliest first", "Latest first", "Sorted by x", "Random"], 0, "`List.range` is increasing."),
 ])


node("MindChangeOrdinal",
 "MindChangeOrdinal: number of mind changes, or ω if the learner fails",
 "MindChangeOrdinal is the number of times the learner changes its conjecture on the text, but only when there are "
 "finitely many changes and it ends at the target. Otherwise it is ω.",
 r"""## Plain English

**Definition (`MindChangeOrdinal`, Complexity/MindChange.lean lines 43–50).** Let `changes` be the set of times t
where the conjecture on the first t examples differs from that on the first t + 1. If `changes` is finite and the
conjecture is eventually always c, the value is the number of changes; otherwise it is ω. Correctness is built in,
which is why [mind_change_characterization](#/node/mind_change_characterization) is short.
""",
 [q("What is the value if the learner changes its mind finitely often but converges to the wrong concept?", ["ω", "The number of changes", "0", "Undefined"], 0,
    "Complexity/MindChange.lean lines 47–49: the inner `else Ordinal.omega0`."),
  q("Can MindChangeOrdinal take values above ω?", ["No: it is a natural number or ω", "Yes, any ordinal", "Yes, ω + 1", "Only ω²"], 0, "Lines 46–50."),
  q("Does the definition depend on the target c?", ["Yes, through the correctness test", "No", "Only through the text", "Only when changes is infinite"], 0,
    "Line 47: `∃ t₀, ∀ t ≥ t₀, L.conjecture (T.prefix t) = c`."),
 ])
