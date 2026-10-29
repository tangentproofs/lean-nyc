NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]

NOT_BUILT = ("Not built for this site: \"proved\" means the source contains a complete-looking proof, and a text "
             "search of the project finds no `sorry`, `admit` or `axiom`. Lean's kernel was not run here.")


node("Neighbour",
 "Neighbour: datasets that differ by one added or removed record",
 "Datasets are lists of records, and two lists are neighbours when one is obtained from the other by inserting or "
 "deleting a single record at any position. Every privacy guarantee in SampCert compares a mechanism's behaviour on "
 "neighbours.",
 r"""## Plain English

`Neighbour l₁ l₂` (DifferentialPrivacy/Neighbours.lean lines 21–23) holds in two cases:

- **Addition**: l₁ = a ++ b and l₂ = a ++ [n] ++ b (l₂ has one extra record n);
- **Deletion**: l₁ = a ++ [n] ++ b and l₂ = a ++ b.

This is the "add/remove one person" ("unbounded") notion of neighbouring datasets. Replacing a record is two steps.
The relation is symmetric (`Neighbour_symm`, lines 29–34). Datasets are lists, so order is part of the data, but
the inserted record can go anywhere.
""",
 [q("Are [1,2,3] and [1,3] neighbours?", ["Yes (delete 2)", "No", "Only if 2 is the last element", "Only under bounded DP"], 0,
    "Deletion with a = [1], n = 2, b = [3] (Neighbours.lean line 23)."),
  q("Are [1,2] and [1,5] neighbours?", ["No: that is a replacement, which takes a deletion and an addition", "Yes", "Only if 5 > 2", "Yes, by symmetry"], 0,
    "Neighbours.lean lines 21–23 allow only one insertion or one deletion."),
 ])


node("sensitivity",
 "sensitivity: how much one record can move a query",
 "An integer-valued query has sensitivity Δ if adding or removing one record changes its answer by at most Δ. "
 "Noise mechanisms scale their noise by Δ.",
 r"""## Plain English

`sensitivity q Δ` (DifferentialPrivacy/Sensitivity.lean lines 26–27): for all [neighbouring](#/node/Neighbour) lists
l₁, l₂, |q(l₁) − q(l₂)| ≤ Δ. Here q maps lists to integers and Δ is a natural number.

Examples in the project: a count has sensitivity 1 (`exactCount_1_sensitive`); a sum of values clipped at U has
sensitivity U (`exactBoundedSum_sensitivity`, Queries/BoundedSum/Properties.lean lines 26–55); a histogram bin count
has sensitivity 1 (`exactBinCount_sensitivity`).
""",
 [q("A query counts the records equal to 7. What is its sensitivity?", ["1", "7", "0", "Unbounded"], 0,
    "Adding or removing one record changes the count by at most 1."),
  q("Is sensitivity defined for real-valued queries here?", ["No, only for queries returning integers", "Yes", "Only for natural numbers", "Only for rationals"], 0,
    "Sensitivity.lean line 26: q : List T → ℤ."),
 ])


node("privComposeAdaptive",
 "Mechanisms and the ways to combine them",
 "A mechanism maps a dataset (a list) to a probability distribution over outputs. SampCert builds private "
 "programs from four combinators: adaptive composition, plain composition, post-processing and constants.",
 r"""## Plain English

In DifferentialPrivacy/Generic.lean:

- `Query T U` (line 20) is a plain function List T → U, and **`Mechanism T U`** (line 22) is List T → SPMF U:
  for each dataset, a [probability distribution](#/node/probBind) over outputs.
- **`privComposeAdaptive nq1 nq2`** (lines 27–30): on input l, sample A from nq1 l, then B from nq2 A l, and
  return (A, B). The second mechanism may depend on the first one's output.
- `privCompose nq1 nq2` (lines 35–36): the same, with nq2 ignoring A.
- `privPostProcess nq pp` (lines 41–43): apply a function pp to the output (no new access to the data).
- `privConst u` (line 48): ignore the data and return u.
- `privParCompose m1 m2 f` (lines 53–57): split the list by a predicate f and run m1 and m2 on the two parts
  (parallel composition).

The chain rule `privComposeChainRule` (lines 154–158) says P((u, v)) = P_{nq1 l}(u) · P_{nq2 u l}(v).

Every [DP system](#/node/DPSystem) must prove that composition adds privacy costs, that post-processing is free and
that constants cost nothing.
""",
 [q("What is the output of privComposeAdaptive nq1 nq2 on l?",
    ["The pair (A, B) where A ~ nq1 l and B ~ nq2 A l", "Only B", "A + B", "nq2 applied to nq1's distribution"], 0,
    "Generic.lean lines 27–30."),
  q("Does post-processing look at the data again?", ["No: it only transforms the mechanism's output", "Yes", "Only the first record", "Only in zCDP"], 0,
    "privPostProcess (lines 41–43) applies pp to the sampled A."),
 ])


node("privNoisedQuery",
 "privNoisedQuery: the discrete Gaussian mechanism",
 "To release an integer query with sensitivity Δ, add discrete Gaussian noise of scale Δ·ε₂/ε₁ centred at the true answer.",
 r"""## Plain English

`privNoisedQuery query Δ ε₁ ε₂ l` (DifferentialPrivacy/ZeroConcentrated/Mechanism/Code.lean lines 21–22) returns a
sample from `DiscreteGaussianGenPMF (Δ·ε₂) ε₁ (query l)`. That is the verified
[discrete Gaussian sampler](#/node/DiscreteGaussianSample), with σ = Δε₂/ε₁, shifted by the true answer
query(l).

It is the noise function of the [zCDP system](#/node/zCDPSystem). Its privacy is the headline
[privNoisedQuery_zCDP](#/node/privNoisedQuery_zCDP).

The pure-DP counterpart `privNoisedQueryPure` (Pure/Mechanism/Code.lean lines 19–20) uses the
[discrete Laplace](#/node/DiscreteLaplaceSample) sampler with scale Δε₂/ε₁ instead.
""",
 [q("Where is the noise centred?", ["At the true answer query(l)", "At 0", "At Δ", "At ε₁/ε₂"], 0,
    "The last argument of DiscreteGaussianGenPMF is the mean, here query l (DifferentialPrivacy/ZeroConcentrated/Mechanism/Code.lean line 22)."),
 ])


node("PureDP",
 "PureDP: ε-differential privacy",
 "A mechanism is ε-DP if, for neighbouring datasets, the probability of any set of outputs changes by at most a "
 "factor e^ε. SampCert proves this is equivalent to the same bound for single outputs.",
 r"""## Plain English

`DP m ε` (DifferentialPrivacy/Pure/DP.lean lines 20–22): for all [neighbouring](#/node/Neighbour) l₁, l₂ and every
set S of outputs,

  P(m(l₁) ∈ S) / P(m(l₂) ∈ S) ≤ e^ε.

`PureDP m ε` (lines 24–25) is the same for ε ≥ 0. The division is in [0, ∞], where x/0 = ∞ for x > 0, so the bound
also forces any event impossible under l₂ to be impossible under l₁.

Because outputs are discrete, it is enough to check single outputs: `event_eq_singleton` (lines 67–71) shows DP is
equivalent to `DP_singleton` (lines 27–29), P(m(l₁) = x)/P(m(l₂) = x) ≤ e^ε. Most proofs, including
[AboveThreshold](#/node/sv9_aboveThresh_pmf_DP), use this form.

Pure DP implies (ε, δ)-DP for every δ (`pure_ApproximateDP`, lines 117–124) and ½ε²-zCDP
([ofDP](#/node/ofDP)).
""",
 [q("Is it enough to check the bound on single outputs?", ["Yes, for discrete outputs (event_eq_singleton)", "No, sets are needed", "Only for finite outputs", "Only for ε < 1"], 0,
    "Pure/DP.lean lines 67–71."),
  q("If P(m(l₂) = x) = 0 but P(m(l₁) = x) > 0, does the ε-DP bound hold?", ["No: the ratio is ∞", "Yes", "Only if ε = 0", "It depends on δ"], 0,
    "In ℝ≥0∞ a positive number over 0 is ∞, which exceeds e^ε."),
 ])


node("ApproximateDP",
 "ApproximateDP: (ε, δ)-differential privacy",
 "A mechanism is (ε, δ)-DP if for neighbouring datasets and every set S of outputs, "
 "P(m(l₁) ∈ S) ≤ δ + e^ε·P(m(l₂) ∈ S). This is the common currency SampCert converts every other notion into.",
 r"""## Plain English

`DP' m ε δ` (DifferentialPrivacy/Approximate/DP.lean lines 21–23) and its synonym `ApproximateDP` (lines 28–29): for
all [neighbouring](#/node/Neighbour) l₁, l₂ and all sets S of outputs,

  P(m(l₁) ∈ S) ≤ δ + e^ε · P(m(l₂) ∈ S).

With δ = 0 this is pure ε-DP. For δ ≥ 1 it holds for every mechanism (`ApproximateDP_gt1`, lines 34–54). The
[DPSystem](#/node/DPSystem) interface requires each privacy notion to imply this one.
""",
 [q("What does δ allow?", ["An additive slack of δ in every event's probability bound", "A multiplicative factor", "A fraction δ of datasets to be unprotected", "Nothing; δ is always 0"], 0,
    "Approximate/DP.lean line 23."),
  q("Why is (ε, δ)-DP trivial for δ ≥ 1?", ["Every probability is at most 1 ≤ δ", "Because ε is then 0", "Lean defines it so", "It is not trivial"], 0,
    "ApproximateDP_gt1 (lines 34–54)."),
 ])


node("RenyiDivergence",
 "RenyiDivergence: the divergence behind zCDP",
 "The Rényi divergence of order α between distributions p and q is (1/(α−1))·log Σ p(x)^α q(x)^{1−α}. It measures "
 "how distinguishable p is from q, and zCDP bounds it linearly in α.",
 r"""## Plain English

- `RenyiDivergence_def p q α` (DifferentialPrivacy/RenyiDivergence.lean lines 58–59) is
  (α − 1)⁻¹ · log(Σ_x p(x)^α · q(x)^{1−α}), computed in the extended reals (so it can be +∞).
- `RenyiDivergence p q α` (lines 712–713) converts it to [0, ∞] with `ENNReal.ofEReal` (Util/Log.lean
  lines 189–195), which sends negative values to 0. For α > 1 the divergence is nonnegative anyway, provided p is
  absolutely continuous with respect to q (`RenyiDivergence_def_nonneg`, lines 631–652).
- `AbsCts p q` (line 27): whenever q(x) = 0, also p(x) = 0.

The file also proves the facts the privacy proofs need: Jensen's inequality for these sums (`Renyi_Jensen_*`,
lines 241–629, used for post-processing) and that the divergence is 0 exactly when p = q
(`RenyiDivergence_aux_zero`, lines 720–735).
""",
 [q("What happens if q(x) = 0 but p(x) > 0 for some x?", ["The divergence (for α > 1) is +∞", "It is 0", "It is undefined and Lean crashes", "It is negative"], 0,
    "q(x)^{1−α} is ∞ when q(x) = 0 and α > 1, so the sum is ∞. zCDP also asks for absolute continuity separately."),
  q("Why does zCDP use the [0, ∞]-valued version?", ["So bounds can be stated in ℝ≥0∞ alongside probabilities; negative values are clipped to 0", "Because Rényi divergence is always finite", "Because log is undefined on reals", "No reason"], 0,
    "RenyiDivergence.lean lines 712–713."),
 ])


node("zCDP",
 "zCDP: zero-concentrated differential privacy",
 "zCDP m ρ says neighbouring datasets give output distributions with the same support whose Rényi divergence of "
 "every order α > 1 is at most ρ·α. That is Bun and Steinke's ρ-zCDP.",
 r"""## Plain English

In DifferentialPrivacy/ZeroConcentrated/DP.lean:

- `zCDPBound q ε` (lines 46–48): for all α > 1 and neighbouring l₁, l₂,
  [RenyiDivergence](#/node/RenyiDivergence)(q l₁, q l₂, α) ≤ ε·α.
- `ACNeighbour q` (line 53): q l₁ is [absolutely continuous](#/node/RenyiDivergence) with respect to q l₂ for
  all neighbours.
- **`zCDP q ε`** (line 58): both.

The parameter, called ε in the code, is what Bun and Steinke call ρ (arXiv:1605.02065, Definition 1.1:
D_α(M(x) ‖ M(x′)) ≤ ρα). The Gaussian mechanism with sensitivity Δ and scale σ has ρ = Δ²/(2σ²), and pure ε-DP
implies ρ = ε²/2. That is why "½ε²" appears throughout.

Some docstrings call `zCDP q ε` "(ε²/2)-zCDP". That is a different naming convention, where the zCDP level is
written as ε²/2. The Lean definition itself is unambiguous: the Rényi divergence is bounded by (second argument) × α.

zCDP composes additively ([privComposeAdaptive_zCDP](#/node/privComposeAdaptive_zCDP)), survives post-processing
(`privPostProcess_zCDP`, DifferentialPrivacy/ZeroConcentrated/Postprocessing.lean lines 570–577) and implies
[(ε′, δ)-DP](#/node/zCDP_ApproximateDP).
""",
 [q("What does zCDP m ρ bound?", ["The Rényi divergence of every order α > 1, by ρ·α", "The KL divergence, by ρ", "The max divergence, by ρ", "The total variation, by ρ"], 0,
    "zCDPBound, ZeroConcentrated/DP.lean lines 46–48."),
  q("What does the extra ACNeighbour condition require?", ["Neighbouring inputs give output distributions where anything impossible under l₂ is impossible under l₁", "The mechanism is continuous", "Neighbours have equal outputs", "Nothing"], 0,
    "Line 53 with AbsCts (RenyiDivergence.lean line 27)."),
  q("If m is ε-DP, what zCDP parameter does SampCert prove?", ["½ε²", "ε", "2ε", "ε²"], 0,
    "ofDP, ZeroConcentrated/DP.lean lines 2098–2101."),
 ],
 caveats=["Naming: the code calls the zCDP parameter ε, docstrings sometimes say \"(ε²/2)-zCDP\", and this site "
          "calls it ρ (Bun–Steinke). All refer to the same definition: Rényi divergence ≤ (parameter)·α."])


node("zCDP_of_adp",
 "zCDP_of_adp: the ρ needed for a target (ε′, δ)",
 "zCDP_of_adp δ ε′ is the zCDP parameter ρ that guarantees (ε′, δ)-DP: ρ = x²/2 where x ≥ 0 solves "
 "x²/2 + x√(2 ln(1/δ)) = ε′.",
 r"""## Plain English

In DifferentialPrivacy/ZeroConcentrated/DP.lean:

- `zCDP_of_adp_def.D δ` (line 594) is √(2 ln(1/δ)).
- `zCDP_of_adp_def.ε ε′ δ` (line 596) is the nonnegative root of ½x² + D·x − ε′ = 0, written with Mathlib's
  `discrim` (the quadratic formula): x = −D + √(D² + 2ε′).
- `zCDP_of_adp δ ε′` (line 646) is ½x².

The lemma `zCDP_of_adp_def.eqε` (lines 598–639) checks that x really is a root, for 0 < δ < 1. With ρ = x²/2 the
root equation reads ε′ = ρ + 2√(ρ ln(1/δ)), the standard zCDP-to-(ε, δ) conversion.

The [zCDP system](#/node/zCDPSystem) uses this function to meet the [DPSystem](#/node/DPSystem) requirement
`of_app_dp`, and the headline [zCDP_ApproximateDP](#/node/zCDP_ApproximateDP) shows it works.
""",
 [q("As δ gets smaller (stronger guarantee), what happens to the ρ needed for a fixed ε′?", ["It gets smaller", "It gets larger", "It stays the same", "It becomes negative"], 0,
    "D = √(2 ln(1/δ)) grows, so the root x = −D + √(D² + 2ε′) shrinks, and ρ = x²/2 with it."),
 ])


node("DPSystem",
 "DPSystem and DPNoise: one interface for every privacy notion",
 "SampCert abstracts a privacy notion as a typeclass: a predicate 'mechanism m is ε-private' with proofs that it "
 "implies (ε′, δ)-DP, is monotone, composes adaptively by addition, survives post-processing and holds for constants. "
 "A DPNoise instance adds a noise mechanism with its privacy guarantee.",
 r"""## Plain English

**`DPSystem T`** (DifferentialPrivacy/Abstract.lean lines 46–84) packages:

- `prop m ε`: "m is ε-private" in this system;
- `of_app_dp` and `prop_adp`: for δ > 0 and target ε′, a level that implies [(ε′, δ)-DP](#/node/ApproximateDP);
- `prop_mono`: a larger ε is weaker;
- `adaptive_compose_prop`: ε₁ and ε₂ [compose adaptively](#/node/privComposeAdaptive) to ε₁ + ε₂;
- `postprocess_prop` and `const_prop`.

The output types must be discrete (`DiscProbSpace`, lines 25–29: measurable, countable, discrete, inhabited).

**`DPNoise dps`** (lines 117–133) adds `noise q Δ εn εd` (a mechanism that noises a query), a relation `noise_priv`
between its parameters and the privacy level, and `noise_prop`: if `noise_priv εn εd ε` holds and q has
[sensitivity](#/node/sensitivity) Δ, the noised query is ε-private.

**`DPPar`** (lines 136–138) adds parallel composition (the cost is the max of the two levels).

Queries such as the [histogram](#/node/privNoisedHistogram_DP) are written once against this interface. There are
two instances: [PureDPSystem](#/node/PureDPSystem) (Laplace) and [zCDPSystem](#/node/zCDPSystem) (Gaussian).
""",
 [q("Why abstract the privacy notion into a typeclass?", ["So a query and its privacy proof can be written once and used with pure DP or zCDP", "For speed", "Because Lean requires it", "To avoid proofs"], 0,
    "Abstract.lean lines 43–84; instances in Pure/System.lean and ZeroConcentrated/System.lean."),
  q("What must every DPSystem prove about composition?", ["Adaptive composition adds the levels", "Composition takes the max", "Composition multiplies the levels", "Nothing"], 0,
    "adaptive_compose_prop, Abstract.lean lines 69–73."),
 ])


node("PureDPSystem",
 "PureDPSystem: pure DP with discrete Laplace noise",
 "The pure-DP instance of the DP interface: the property is ε-DP, the noise is the verified discrete Laplace sampler "
 "with scale Δε₂/ε₁, and its privacy level is exactly ε₁/ε₂.",
 r"""## Plain English

`PureDPSystem` (DifferentialPrivacy/Pure/System.lean lines 25–35) instantiates [DPSystem](#/node/DPSystem) with
[PureDP](#/node/PureDP). Its fields are proved by:

- adaptive composition: `PureDP_ComposeAdaptive'` (Pure/AdaptiveComposition.lean lines 21–84);
- post-processing: `PureDP_PostProcess` (Pure/Postprocessing.lean lines 49–52);
- constants: `PureDP_privConst` (Pure/Const.lean lines 35–37);
- conversion to (ε′, δ)-DP: `pure_ApproximateDP` (no loss: the level is ε′ itself).

`laplace_pureDPSystem` (lines 37–41) adds the noise `privNoisedQueryPure` (discrete Laplace of scale Δε₂/ε₁) with
`laplace_pureDP_noise_priv ε₁ ε₂ ε := ε₁/ε₂ = ε` (Pure/Mechanism/Properties.lean line 121). The guarantee is
`privNoisedQueryPure_DP` (lines 126–132): a Δ-sensitive query noised this way is ε₁/ε₂-DP.

`PureDPParSystem` (lines 43–44) adds parallel composition (`pureDP_priv_Par`, Pure/Par.lean lines 135–137).
""",
 [q("With Laplace scale Δε₂/ε₁, what pure-DP level does a Δ-sensitive query get?", ["ε₁/ε₂", "Δε₁/ε₂", "½(ε₁/ε₂)²", "ε₂/ε₁"], 0,
    "privNoisedQueryPure_DP with laplace_pureDP_noise_priv (Pure/Mechanism/Properties.lean lines 121–132)."),
 ],
 caveats=[NOT_BUILT])


node("zCDPSystem",
 "zCDPSystem: zCDP with discrete Gaussian noise",
 "The zCDP instance of the DP interface: the property is ρ-zCDP, the noise is the verified discrete Gaussian with "
 "scale Δε₂/ε₁, and any ρ ≥ ½(ε₁/ε₂)² is achieved.",
 r"""## Plain English

`zCDPSystem` (DifferentialPrivacy/ZeroConcentrated/System.lean lines 28–49) instantiates
[DPSystem](#/node/DPSystem) with [zCDP](#/node/zCDP):

- conversion to (ε′, δ)-DP: [zCDP_of_adp](#/node/zCDP_of_adp) and [zCDP_ApproximateDP](#/node/zCDP_ApproximateDP);
- adaptive composition: [privComposeAdaptive_zCDP](#/node/privComposeAdaptive_zCDP);
- post-processing: `privPostProcess_zCDP` (ZeroConcentrated/Postprocessing.lean lines 570–577), which uses
  Jensen's inequality for Rényi divergences;
- constants: `privConst_zCDP` (ZeroConcentrated/Const.lean lines 46–51).

`gaussian_zCDPSystem` (lines 56–65) adds the noise [privNoisedQuery](#/node/privNoisedQuery) with
`gaussian_zCDP_noise_priv ε₁ ε₂ ε := ½(ε₁/ε₂)² ≤ ε` (line 51). The guarantee is the headline
[privNoisedQuery_zCDP](#/node/privNoisedQuery_zCDP) plus monotonicity.

The top-level file SampCert.lean uses both instances to state that the bounded-mean query is private under
each (`combineConcentrated`, `combinePure`).
""",
 [q("Which inequality must the Gaussian noise parameters satisfy for level ρ?", ["½(ε₁/ε₂)² ≤ ρ", "ε₁/ε₂ = ρ", "ε₁ ≤ ε₂", "Δ ≤ ρ"], 0,
    "gaussian_zCDP_noise_priv, ZeroConcentrated/System.lean line 51."),
 ],
 caveats=[NOT_BUILT])


node("ofDP",
 "Key lemma: ε-DP implies ½ε²-zCDP",
 "Any pure ε-DP mechanism is also ½ε²-zCDP. This is Bun–Steinke's Proposition 1.4, and its Lean proof is one of the "
 "longest in the project (about 1,400 lines of hyperbolic-function inequalities).",
 r"""## Plain English

**Lemma (`ofDP`, DifferentialPrivacy/ZeroConcentrated/DP.lean lines 2098–2101).** If q is
[PureDP](#/node/PureDP) at level ε, then q is [zCDP](#/node/zCDP) with ρ = ½ε².

Absolute continuity is easy (`ACNeighbour_of_DP`, lines 673–682): pure DP forbids an outcome being possible on one
side and impossible on the other. The Rényi bound (`ofDP_bound`, lines 1843–2091) is hard. When ε·α is large
(> 2) a crude bound suffices (`ofDP_bound_large_εα`, line 1675). Otherwise the proof follows Bun and Steinke's argument.
It builds auxiliary two-point distributions on Bool from the likelihood ratios (`β`, `A_pmf`, `B`, lines 693–1236),
applies a Jensen-type bound, and reduces to the inequality sinh(x) − sinh(y) ≤ sinh(x − y)·e^{xy/2} for 0 ≤ y < x ≤ 2 (`sinh_inequality`, lines
1662–1673). That inequality is in turn proved by calculus on tanh (lines 1239–1660).

The paper mapping in the repository lists it as the appendix lemma "DP implies zCDP".
""",
 [q("What zCDP level does ε-DP give?", ["½ε²", "ε", "ε²", "2ε"], 0, "ZeroConcentrated/DP.lean line 2098."),
  q("Which part of the proof is the hard one?", ["The Rényi divergence bound, via a hyperbolic-sine inequality", "Absolute continuity", "Monotonicity", "Composition"], 0,
    "ofDP_bound (lines 1843–2091) and its helper lemmas from line 1239 on."),
 ],
 caveats=[NOT_BUILT,
          "The names `A_pmf`, `B`, `β`, `C` and `t` defined in this file are generic. This site's text scanner sometimes "
          "mistakes local variables with the same names elsewhere (for example the bins `B` of a histogram) for these "
          "definitions, so dependency lists may show spurious links to them."])


EXTRA = {
 "Neighbour": [q("Is Neighbour symmetric?", ["Yes (Neighbour_symm)", "No", "Only for equal lengths", "Only for empty lists"], 0,
    "Neighbours.lean lines 29–34.")],
 "sensitivity": [q("What is the sensitivity of a sum of values each clipped at U?", ["U", "1", "The list length", "Unbounded"], 0,
    "exactBoundedSum_sensitivity, Queries/BoundedSum/Properties.lean lines 26–55.")],
 "privComposeAdaptive": [q("What is a Mechanism T U?", ["A function from lists of T to SPMFs over U", "A list of samples", "A query U → T", "A proof of privacy"], 0,
    "Generic.lean line 22.")],
 "privNoisedQuery": [q("Which sampler supplies the noise?", ["The verified discrete Gaussian sampler", "A floating-point Gaussian", "The Laplace sampler", "A uniform sampler"], 0,
    "DiscreteGaussianGenPMF wraps DiscreteGaussianGenSample, which calls DiscreteGaussianSample."),
   q("Does privNoisedQuery's noise depend on the data?", ["Only through the centre query(l); the scale depends only on Δ, ε₁, ε₂", "Yes, the scale grows with the list", "No, not even the centre", "Only on the list length"], 0,
    "ZeroConcentrated/Mechanism/Code.lean line 22.")],
 "PureDP": [q("Is ε here allowed to be negative?", ["No: PureDP takes ε : ℝ≥0", "Yes", "Only for constants", "Only in zCDP"], 0,
    "Pure/DP.lean line 24.")],
 "ApproximateDP": [q("Does pure DP imply approximate DP?", ["Yes, for every δ (pure_ApproximateDP)", "No", "Only for δ ≥ 1", "Only for finite outputs"], 0,
    "Pure/DP.lean lines 117–124.")],
 "RenyiDivergence": [q("Is the Rényi divergence of p from itself zero?", ["Yes (RenyiDivergence_refl_zero)", "No, it is 1", "It is ∞", "Undefined"], 0,
    "RenyiDivergence.lean line 654.")],
 "zCDP_of_adp": [q("What is D δ?", ["√(2 ln(1/δ))", "ln δ", "2δ", "1/δ"], 0, "ZeroConcentrated/DP.lean line 594."),
   q("For which δ is the root identity eqε proved?", ["0 < δ < 1", "All δ", "δ = 1", "δ > 1"], 0, "Lines 598 (hypotheses H0, H1).")],
 "DPSystem": [q("What does DPNoise add to a DP system?", ["A noise mechanism and a proof that noising a Δ-sensitive query is private", "A random seed", "A composition rule", "A dataset"], 0,
    "Abstract.lean lines 117–133.")],
 "PureDPSystem": [q("Does PureDPSystem lose anything when converting to (ε′, δ)-DP?", ["No: it uses level ε′ itself (pure_of_adp)", "Yes, a factor 2", "Yes, it needs ε′²", "It cannot convert"], 0,
    "pure_of_adp ignores δ and returns ε′ (Pure/DP.lean line 112)."),
   q("Which extra capability does PureDPParSystem provide?", ["Parallel composition at cost max(ε₁, ε₂)", "Faster sampling", "zCDP", "Approximate DP"], 0,
    "Pure/System.lean lines 43–44 and Abstract.lean lines 136–138.")],
 "zCDPSystem": [q("Which fact proves zCDP survives post-processing?", ["privPostProcess_zCDP, via Jensen's inequality", "It is assumed", "privConst_zCDP", "ofDP"], 0,
    "ZeroConcentrated/Postprocessing.lean lines 570–577."),
   q("Is gaussian_zCDP_noise_priv an equality or an inequality?", ["An inequality: any ρ at least ½(ε₁/ε₂)² is allowed", "An equality", "Neither", "It is always true"], 0,
    "ZeroConcentrated/System.lean line 51; monotonicity (prop_mono) closes the gap.")],
 "ofDP": [q("Is the converse true: does ½ε²-zCDP imply ε-DP?", ["No; zCDP is weaker, and the docstring of zCDPBound says so", "Yes", "Only for ε < 1", "Only for Gaussians"], 0,
    "ZeroConcentrated/DP.lean lines 40–45.")],
}
for n in NODES:
    n["quiz"] += EXTRA.get(n["id"], [])
