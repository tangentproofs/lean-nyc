NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]

NOT_BUILT = ("Not built for this site: \"proved\" means the source contains a complete-looking proof, and a text "
             "search of the project finds no `sorry`, `admit` or `axiom`. Lean's kernel was not run here.")


node("DiscreteGaussianSample_apply",
 "Headline: the discrete Gaussian sampler is exactly right",
 "The program DiscreteGaussianSample, built only from random bytes, rejection loops and a discrete Laplace "
 "sampler, gives every integer x exactly the discrete Gaussian probability exp(−x²/2σ²) / Σ_z exp(−z²/2σ²), with "
 "σ = num/den. Exact, not approximate.",
 r"""## Plain English

**Theorem (`DiscreteGaussianSample_apply`, Samplers/Gaussian/Properties.lean lines 238–240).** For positive
integers *num* and *den* and any natural number *mix*, the probability that the program
[DiscreteGaussianSample](#/node/DiscreteGaussianSample) `num den mix` returns the integer *x* is

  [discrete_gaussian](#/node/discrete_gaussian)(σ, 0, x) = exp(−x²/(2σ²)) / Σ over all integers z of exp(−z²/(2σ²)),

where σ = num/den.

What makes this a strong statement:

- **It is about the actual sampling program.** The left-hand side is the probability that the
  [SLang](#/node/probBind) program puts on *x*. That program draws uniform random bytes, does Bernoulli trials,
  runs a discrete Laplace sampler and then a rejection loop. The right-hand side is the textbook formula. The
  theorem says they agree **exactly, for every x**, with no floating point and no truncation of the tails.
- **The loops are unbounded.** The sampler uses `probUntil` (repeat until accepted), whose meaning is a limit
  over ever longer unrollings ([probWhile](#/node/probWhile)). The proof has to compute that limit.
- **`mix` does not matter.** *mix* only chooses which of two equivalent discrete Laplace samplers runs inside
  the loop (see [DiscreteLaplaceSampleMixed_apply](#/node/DiscreteLaplaceSampleMixed_apply)). It is a
  performance knob, and the theorem shows the output distribution is the same either way.

The algorithm is the one from Canonne, Kamath and Steinke, *The Discrete Gaussian for Differential Privacy*
(arXiv:2004.00010), which the README cites.

### Why the rejection step gives a Gaussian

Let t = ⌊σ⌋ + 1. The loop body ([DiscreteGaussianSampleLoop](#/node/DiscreteGaussianSample)) draws a candidate Y
from the discrete Laplace distribution with scale t, so P(Y = y) ∝ exp(−|y|/t). It then accepts with probability
exp(−(|y| − σ²/t)² / (2σ²)). Multiplying the two and expanding the square gives

  exp(−|y|/t) · exp(−(|y| − σ²/t)²/(2σ²)) = exp(−y²/(2σ²)) · exp(−σ²/(2t²)).

The last factor does not depend on y, so after rejection the accepted value has probability proportional to
exp(−y²/(2σ²)): the discrete Gaussian. The proof is this computation done carefully in extended nonnegative reals.
""",
 [q("What does the theorem say about the sampler's output distribution?",
    ["Its probability at every integer x equals the discrete Gaussian formula exactly",
     "It is close to a discrete Gaussian in total variation distance",
     "Its mean is 0 and its variance is σ²",
     "It passes a Kolmogorov–Smirnov test"], 0,
    "Lines 238–240 are an equation between the program's probability at x and `discrete_gaussian (num/den) 0 x`, for every x. (The KS tests in Tests/ are separate, empirical checks.)"),
  q("What role does the argument `mix` play?",
    ["It picks one of two Laplace sub-samplers; the output distribution is the same for every value",
     "It sets the mean of the Gaussian",
     "It is the random seed",
     "It is the number of loop iterations allowed"], 0,
    "`mix` is passed to `DiscreteLaplaceSampleMixed` (Samplers/Gaussian/Code.lean line 26), which picks a sampler by comparing num with den·mix. The right-hand side of the theorem does not mention mix."),
  q("Is σ = num/den exactly the variance of the output?",
    ["No: σ is the scale parameter in exp(−x²/2σ²); the discrete Gaussian's variance is close to, but not exactly, σ²",
     "Yes, by definition",
     "No: the variance is num/den, not its square",
     "The theorem does not fix any parameter"], 0,
    "The theorem fixes the formula exp(−x²/(2σ²)) / Σ. Some docstrings call (num/den)² the variance; for the discrete Gaussian that is only approximately true (it is at most σ²)."),
  q("Does the theorem show the compiled executable produces this distribution?",
    ["No: it is about the Lean meaning of the program; the compiled code replaces the primitives with C++ (ffi.cpp), and that link is trusted, not proved",
     "Yes: Lean proves properties of the machine code",
     "Yes: because the program is marked `@[extern]`",
     "No: the theorem is only about the Laplace sampler"], 0,
    "SLang.lean marks probPure, probBind, probUniformByte and probWhile `@[extern ...]` (lines 65, 71, 83, 143). Compiled code runs the C++ versions; the theorem is about the Lean definitions."),
 ],
 caveats=[NOT_BUILT,
  "The theorem is about the mathematical meaning of the SLang program (a function from outcomes to probabilities). "
  "When SampCert is compiled, the primitives probPure, probBind, probUniformByte and probWhile are replaced by C++ "
  "implementations in ffi.cpp (via `@[extern]`), with randomness from /dev/urandom. That the C++ matches the Lean "
  "definitions is not proved. SampCert also has a separate extractor that translates the samplers to Dafny/Python.",
  "σ = num/den is the Gaussian's scale parameter. Docstrings in Samplers/Gaussian/Code.lean say \"variance\"; the "
  "exact variance of a discrete Gaussian is slightly less than σ².",
 ],
 widgets=walk("How the proof goes (Samplers/Gaussian/Properties.lean, lines 238-355)", [
  {"text": "Unfold the target formula into exp(−(x−0)²/(2σ²)) over its sum (lines 241–243), then unfold the sampler: one probUntil around the loop body, then take the first component (line 244).",
   "link": "discrete_gaussian", "lean": "unfold discrete_gaussian"},
  {"text": "The loop body is a proper distribution (DiscreteGaussianSampleLoop_normalizes, line 245), so the closed form for a rejection loop applies: P(output = a) = P(body = a, accepted) / P(accepted) (probUntil_apply_norm, line 252).",
   "link": "probUntil", "lean": "rw [probUntil_apply_norm _ _ _ A]"},
  {"text": "Substitute the probability of an accepted candidate n: the Laplace weight times the Bernoulli acceptance weight (DiscreteGaussianSampleLoop_apply_true, used at lines 255–257).",
   "link": "DiscreteGaussianSample"},
  {"text": "In the sum over candidates, only n = x contributes to output x; split it off and show the rest is zero (lines 258–265).",
   "lean": "rw [ENNReal.tsum_eq_add_tsum_ite x]"},
  {"text": "The algebraic heart (helper `alg_auto`, lines 151–225): Laplace weight × acceptance weight = exp(−σ²/(2t²)) × exp(−x²/(2σ²)). The constant factor appears in both numerator and denominator and cancels (line 296), as does the Laplace normalising constant (lines 267–276).",
   "lean": "rw [ENNReal.mul_inv_cancel A B]"},
  {"text": "Rewrite the remaining exponent into the form −x²/(2·(num/den)²) (alg_auto', line 302) and move the sum inside ENNReal.ofReal, using that the Gaussian terms are summable (lines 303–316).",
   "lean": "rw [← ENNReal.ofReal_tsum_of_nonneg]"},
  {"text": "Lines 317–355 discharge side conditions: the exponentials are positive and finite, and the normalisers are nonzero, so the divisions and cancellations above were legitimate."},
 ]))


node("privNoisedQuery_zCDP",
 "Headline: the discrete Gaussian mechanism is ½(ε₁/ε₂)²-zCDP",
 "If an integer-valued query changes by at most Δ when one record is added or removed, then releasing it plus "
 "discrete Gaussian noise of scale σ = Δ·ε₂/ε₁ satisfies zero-concentrated differential privacy with parameter "
 "ρ = ½(ε₁/ε₂)². The noise is the verified sampler itself, not an idealised Gaussian.",
 r"""## Plain English

**Theorem (`privNoisedQuery_zCDP`, DifferentialPrivacy/ZeroConcentrated/Mechanism/Properties.lean lines 132–133).**
Let *query* map a list of records to an integer, and suppose it has [sensitivity](#/node/sensitivity) Δ: for any
two [neighbouring](#/node/Neighbour) lists (one record added or removed), the answers differ by at most Δ. Then the
mechanism [privNoisedQuery](#/node/privNoisedQuery) `query Δ ε₁ ε₂`, which returns query(l) plus a sample from the
discrete Gaussian with scale σ = Δ·ε₂/ε₁, is [zCDP](#/node/zCDP) with parameter

  ρ = ½ · (ε₁/ε₂)².

Here ε₁, ε₂ are positive integers, so the privacy level ε₁/ε₂ is any positive rational.

### What zCDP with parameter ρ means here

[zCDP](#/node/zCDP) `m ρ` asks two things for every pair of neighbouring lists l₁, l₂:

1. the output distributions have the same support (**absolute continuity**, `ACNeighbour`); and
2. for every order α > 1, the [Rényi divergence](#/node/RenyiDivergence) of order α between m(l₁) and m(l₂) is at
   most ρ·α.

This is Bun and Steinke's ρ-zCDP (arXiv:1605.02065). The theorem gives the standard answer for the Gaussian
mechanism, ρ = Δ²/(2σ²). With σ = Δε₂/ε₁ that is ½(ε₁/ε₂)², so Δ cancels.

### Why it holds

Shifting a discrete Gaussian by an integer does not change its normalising constant. So the Rényi divergence of
order α between discrete Gaussians centred at μ and ν is at most α·(μ−ν)²/(2σ²)
([discrete_GaussianGenSample_ZeroConcentrated](#/node/discrete_GaussianGenSample_ZeroConcentrated)). Sensitivity
gives |μ − ν| ≤ Δ, and the rest is algebra.
""",
 [q("Which noise scale does privNoisedQuery use?",
    ["σ = Δ·ε₂/ε₁", "σ = ε₁/ε₂", "σ = Δ", "σ = 1/ε₁"], 0,
    "ZeroConcentrated/Mechanism/Code.lean line 22 calls DiscreteGaussianGenPMF with num = Δ·ε₂ and den = ε₁, i.e. σ = Δε₂/ε₁."),
  q("What is the zCDP parameter ρ in the conclusion?",
    ["½(ε₁/ε₂)²", "(Δε₂/ε₁)²", "ε₁/ε₂", "Δ²/2"], 0,
    "Line 133 gives (1/2)·(ε₁/ε₂)². The docstring at line 130 says \"(Δε₂/ε₁)^2-zCDP\", which does not match the statement; the statement is the standard Δ²/(2σ²)."),
  q("What does the hypothesis `sensitivity query Δ` say?",
    ["On any two lists that differ by adding or removing one record, the query's answers differ by at most Δ",
     "The query's answers are between −Δ and Δ",
     "The query reads at most Δ records",
     "Changing any one record changes the answer by at most Δ"], 0,
    "Sensitivity.lean lines 26–27 quantify over `Neighbour` lists, which are insertion/deletion neighbours (Neighbours.lean lines 21–23), not replacement."),
  q("Is the zCDP bound required for all Rényi orders α > 1, or just one?",
    ["All α > 1", "Only α = 2", "Only the limit α → ∞", "Only α = 1"], 0,
    "zCDPBound (ZeroConcentrated/DP.lean lines 46–48) quantifies over every real α with 1 < α."),
 ],
 caveats=[NOT_BUILT,
  "The docstrings at lines 23 and 130 describe the result as \"(Δε₂/ε₁)^2-zCDP\"; the Lean statement says "
  "ρ = ½(ε₁/ε₂)², which is the correct Gaussian-mechanism value. Trust the statement, not the comment.",
  "Neighbouring means adding or removing one record (\"unbounded\" DP), not replacing one.",
 ],
 widgets=walk("How the proof goes (ZeroConcentrated/Mechanism/Properties.lean, lines 132-138, with lines 25-127)", [
  {"text": "zCDP is a conjunction; split it (lines 134–135).", "link": "zCDP", "lean": "apply And.intro"},
  {"text": "Absolute continuity: every integer has positive probability under a discrete Gaussian, so no outcome has probability 0 under one input and positive probability under another (privNoisedQuery_AC, lines 111–127, using discrete_gaussian_pos).",
   "lean": "· exact privNoisedQuery_AC query Δ ε₁ ε₂"},
  {"text": "The Rényi bound (privNoisedQuery_zCDPBound, lines 25–97). First apply the Gaussian Rényi bound: divergence ≤ α·(q(l₁) − q(l₂))² / (2σ²) (line 29).",
   "link": "discrete_GaussianGenSample_ZeroConcentrated"},
  {"text": "Use sensitivity to replace (q(l₁) − q(l₂))² by Δ² (lines 34–60).", "link": "sensitivity"},
  {"text": "Lines 61–97 are cast bookkeeping (between ℕ+, ℝ≥0, ℝ and ℝ≥0∞) ending in the real identity α·Δ²/(2(Δε₂/ε₁)²) = ½(ε₁/ε₂)²·α, closed by field_simp (line 97)."},
 ]))


node("privComposeAdaptive_zCDP",
 "Headline: adaptive composition of zCDP mechanisms adds their ρ's",
 "Run a ρ₁-zCDP mechanism, let a second mechanism depend on its output, and release both answers: the "
 "result is (ρ₁ + ρ₂)-zCDP, provided the second mechanism is ρ₂-zCDP whatever the first output was.",
 r"""## Plain English

**Theorem (`privComposeAdaptive_zCDP`, DifferentialPrivacy/ZeroConcentrated/AdaptiveComposition.lean lines 177–179).**
Let nq1 be a mechanism with outputs in U, and for each u ∈ U let nq2 u be a mechanism with outputs in V. If
nq1 is [zCDP](#/node/zCDP) with parameter ρ₁, and **every** nq2 u is zCDP with parameter ρ₂, then
[privComposeAdaptive](#/node/privComposeAdaptive) nq1 nq2, which samples u from nq1(l), then v from (nq2 u)(l), and
returns (u, v), is zCDP with parameter ρ₁ + ρ₂.

"Adaptive" is the important word: the second analysis may be chosen after seeing the first noisy answer. This is
how real DP pipelines work, and the same rule makes it possible to build larger mechanisms (such as the
[histogram](#/node/privNoisedHistogram_DP)) out of small ones.

The output types must be discrete: the section assumes U is inhabited and countable with measurable singletons,
and V is countable with measurable singletons (lines 30–32). The project's privacy notions are all for
discrete distributions.

### The idea

For Rényi divergence, the divergence of a joint distribution (u, v) splits as the divergence of the first
component plus the worst case, over u, of the divergence of the second component given u
(`privComposeAdaptive_renyi_bound`, lines 37–124). Bounding each part by ρ₁α and ρ₂α gives (ρ₁+ρ₂)α.
""",
 [q("What may the second mechanism depend on?",
    ["The output u of the first mechanism (and the same input list)", "Nothing: it must be fixed in advance",
     "The first mechanism's random bits", "A different, unrelated database"], 0,
    "privComposeAdaptive (Generic.lean lines 27–30) passes the sampled A to nq2 together with the same list l."),
  q("What must hold of the second mechanism?",
    ["For every possible first output u, nq2 u is ρ₂-zCDP", "nq2 is ρ₂-zCDP on average over u",
     "nq2 u is ρ₂-zCDP for the u that actually occurs", "Nothing beyond being a distribution"], 0,
    "The hypothesis h' at line 178 is ∀ u, zCDP (nq2 u) ε₂."),
  q("What does the composed mechanism release?",
    ["Both outputs, as a pair (u, v)", "Only v", "Only the sum u + v", "Only u"], 0,
    "privComposeAdaptive returns (A, B) (Generic.lean line 30). Releasing less is covered by post-processing."),
 ],
 caveats=[NOT_BUILT,
  "In this file the zCDP parameters are named ε₁, ε₂, but they play the role of Bun–Steinke's ρ (the bound is "
  "Rényi divergence ≤ ε·α). See [zCDP](#/node/zCDP).",
  "Requires discrete (countable) output types; this is the setting of the whole library.",
 ],
 widgets=walk("How the proof goes (ZeroConcentrated/AdaptiveComposition.lean, lines 177-183, with lines 37-172)", [
  {"text": "Unfold zCDP into its two conjuncts for the hypotheses and the goal (lines 180–181).", "link": "zCDP",
   "lean": "simp [zCDP] at *"},
  {"text": "Absolute continuity of the composition (privComposeAdaptive_AC, lines 158–172): if the pair (u, v) has probability 0 under l₂, then either u has probability 0 under nq1 l₂ or v has probability 0 under nq2 u l₂, and in each case the same holds under l₁.",
   "lean": "· apply privComposeAdaptive_AC <;> aesop"},
  {"text": "Rényi bound (privComposeAdaptive_zCDPBound, lines 129–152): the supremum over u of the second-stage divergences is at most ρ₂α (lines 139–140)."},
  {"text": "Add the two bounds: ρ₁α + ρ₂α = (ρ₁+ρ₂)α (lines 141–151)."},
  {"text": "The key inequality, divergence(joint) ≤ divergence(first) + sup over u of divergence(second | u), is privComposeAdaptive_renyi_bound (lines 37–124), applied at line 152. It is proved by writing the joint probabilities with the chain rule (privComposeChainRule, Generic.lean lines 154–159) and bounding the inner sums by their supremum."},
 ]))


node("zCDP_ApproximateDP",
 "Headline: zCDP implies (ε, δ)-differential privacy",
 "A ρ-zCDP mechanism is (ε′, δ)-differentially private for every δ > 0, where ε′ = ρ + 2√(ρ·ln(1/δ)). The Lean "
 "statement runs this backwards: given a target (ε′, δ) it computes the ρ that suffices.",
 r"""## Plain English

**Theorem (`zCDP_ApproximateDP`, DifferentialPrivacy/ZeroConcentrated/DP.lean lines 651–653).** Let δ > 0 and ε′ ≥ 0.
If a mechanism m (with countable output type) is [zCDP](#/node/zCDP) with parameter
ρ = [zCDP_of_adp](#/node/zCDP_of_adp) δ ε′, then m is [(ε′, δ)-approximately differentially private](#/node/ApproximateDP):
for neighbouring lists l₁, l₂ and **every** set S of outputs,

  P(m(l₁) ∈ S) ≤ δ + e^{ε′} · P(m(l₂) ∈ S).

### Which ρ?

`zCDP_of_adp δ ε′` is ½x², where x ≥ 0 solves x²/2 + x·√(2 ln(1/δ)) = ε′. Writing ρ = x²/2, this is exactly

  ε′ = ρ + 2√(ρ · ln(1/δ)),

the standard conversion of Bun and Steinke (Proposition 1.3 of arXiv:1605.02065). The underlying forward theorem
is `ApproximateDP_of_zCDP` (same file, lines 574–590): ρ = ε²/2 gives (ε²/2 + ε√(2 ln(1/δ)), δ)-DP.

This result is what lets SampCert treat zCDP and pure DP uniformly: both are instances of
[DPSystem](#/node/DPSystem), whose interface requires a way to turn the system's guarantee into (ε′, δ)-DP.
""",
 [q("For which δ does the theorem apply?",
    ["Every δ > 0 (for δ ≥ 1 the conclusion is trivial)", "Only δ = 0", "Only δ < 1/n", "Only δ = 1/2"], 0,
    "The hypothesis is 0 < δ (line 652). Lines 655–656 dispose of δ ≥ 1 with ApproximateDP_gt1, since then the bound is automatic."),
  q("What kind of guarantee is the conclusion?",
    ["For every set S of outputs, P(m(l₁) ∈ S) ≤ δ + e^{ε′}·P(m(l₂) ∈ S)",
     "For every single output x, P(m(l₁) = x) ≤ e^{ε′}·P(m(l₂) = x)",
     "The Rényi divergence is at most ε′",
     "The outputs are within δ of each other"], 0,
    "ApproximateDP unfolds to DP' (Approximate/DP.lean lines 21–23), which quantifies over all sets S."),
  q("Roughly how does ε′ relate to ρ?",
    ["ε′ = ρ + 2√(ρ ln(1/δ))", "ε′ = ρ", "ε′ = √ρ", "ε′ = ρ·ln(1/δ)"], 0,
    "zCDP_of_adp_def.eqε (lines 598–639) shows ε′ = x²/2 + x·√(2 ln(1/δ)) with ρ = x²/2, which rearranges to ρ + 2√(ρ ln(1/δ))."),
 ],
 caveats=[NOT_BUILT,
  "The statement fixes ρ as an explicit (and slightly opaque) function of (δ, ε′) via a quadratic-formula root "
  "(`discrim`); the node [zCDP_of_adp](#/node/zCDP_of_adp) unpacks it.",
 ],
 widgets=walk("How the proof goes (ZeroConcentrated/DP.lean, lines 651-666)", [
  {"text": "If δ ≥ 1 the conclusion holds for any mechanism, since probabilities are at most 1 (line 656).",
   "link": "ApproximateDP", "lean": "· exact ApproximateDP_gt1 m (↑ε') Hδ1"},
  {"text": "Otherwise unfold ρ = ½·ε(ε′, δ)² and split zCDP into absolute continuity H1 and the Rényi bound H2 (lines 658–661).",
   "link": "zCDP_of_adp", "lean": "rcases H with ⟨ H1, H2 ⟩"},
  {"text": "Apply the forward conversion ApproximateDP_of_zCDP (lines 574–590) with ε = ε(ε′, δ). Its proof (lines 411–558) is the real work: a tail bound from the Rényi divergence, via the auxiliary lemmas ApproximateDP_* in lines 84–410.",
   "lean": "have X := ApproximateDP_of_zCDP m (zCDP_of_adp_def.ε ε' δ) ?G1 H2 H1 δ Hδ0"},
  {"text": "Rewrite ε′ as ε²/2 + ε·√(2 ln(1/δ)) using the quadratic-root identity eqε (lines 598–639), which matches the shape of X; simp closes the goal (lines 664–666).",
   "lean": "rw [zCDP_of_adp_def.eqε ε' δ Hδ0 Hδ1]"},
 ]))


node("privNoisedHistogram_DP",
 "Headline: a noised histogram is private, in any DP system",
 "Add noise to each bin count of a histogram, with each bin given 1/numBins of the budget; the whole histogram "
 "is then ε-private. The theorem is proved once, for an abstract DP system, so it holds for pure DP with Laplace "
 "noise and for zCDP with Gaussian noise.",
 r"""## Plain English

**Theorem (`privNoisedHistogram_DP`, DifferentialPrivacy/Queries/Histogram/Properties.lean lines 76–77).** Fix a
way of sorting records into *numBins* bins ([Bins](#/node/privNoisedHistogram)), and any
[DP system](#/node/DPSystem) `dps` with a noise mechanism `dpn`. Suppose the noise parameters are chosen so that
noising a 1-sensitive integer query with parameters (ε₁, ε₂·numBins) is private at level ε/numBins (the hypothesis
`HN_bin`). Then the mechanism [privNoisedHistogram](#/node/privNoisedHistogram), which counts the records in each
bin and adds independent noise to each count, satisfies the system's privacy property at level ε.

What "private at level ε" means depends on the system:

- for [PureDPSystem](#/node/PureDPSystem) with Laplace noise it is pure ε-DP, and `HN_bin` says ε₁/(ε₂·numBins) = ε/numBins;
- for [zCDPSystem](#/node/zCDPSystem) with Gaussian noise it is ε-zCDP (ε playing the role of ρ), and `HN_bin` says ½(ε₁/(ε₂·numBins))² ≤ ε/numBins.

So the hypothesis is a **parameter-choice condition**, not a gap: for each instance it is simple arithmetic about
the inputs.

### How

Each bin count has sensitivity 1, since adding or removing one record changes exactly one count by one
(`exactBinCount_sensitivity`, lines 29–34). Noising it gives ε/numBins privacy. The histogram is built by
composing the numBins noised counts one at a time and post-processing them into a histogram, so composition gives
numBins · ε/numBins = ε.
""",
 [q("Why is the theorem stated for an abstract `DPSystem` rather than for pure DP?",
    ["So that one proof covers every instance (pure DP with Laplace noise, zCDP with Gaussian noise)",
     "Because pure DP does not compose",
     "Because the histogram is not private under pure DP",
     "It is only stated for zCDP"], 0,
    "The section variables [dps : DPSystem T] [dpn : DPNoise dps] (lines 38–39) make the theorem generic; it only uses compose_prop, postprocess_prop, const_prop and noise_prop."),
  q("What is the hypothesis HN_bin?",
    ["The noise parameters (ε₁, ε₂·numBins) give ε/numBins privacy for a 1-sensitive query",
     "An unproved lemma about histograms",
     "That the bins are equally full",
     "That the data contain no duplicates"], 0,
    "It is `dpn.noise_priv ε₁ (ε₂ * numBins) (ε / numBins)` (line 76), the noise system's own relation between parameters and privacy level."),
  q("How does the proof combine the bins?",
    ["Sequential composition, one bin at a time, then post-processing", "Parallel composition across disjoint bins",
     "A union bound", "It does not combine them; each bin is released separately"], 0,
    "privNoisedHistogramAux_DP (lines 55–71) inducts on the bin index using dps.compose_prop and dps.postprocess_prop. A separate parallel-composition histogram is in Queries/ParHistogram."),
 ],
 caveats=[NOT_BUILT,
  "The budget split is the simple sequential one (each bin gets ε/numBins). Since each record affects only one "
  "bin, parallel composition would allow more; that variant is the separate ParHistogram query (pure DP only, via `DPPar`).",
 ],
 widgets=walk("How the proof goes (Queries/Histogram/Properties.lean, lines 76-81, with lines 29-71)", [
  {"text": "Each bin count is 1-sensitive: add or remove one record and exactly one bin's count moves by 1 (exactBinCount_sensitivity, lines 29–34)."},
  {"text": "So one noised bin count is ε/numBins-private, by the noise system's guarantee (privNoisedBinCount_DP, lines 45–50).",
   "link": "DPSystem"},
  {"text": "Induction on the number of bins filled so far (privNoisedHistogramAux_DP, lines 55–71). Base case: compose bin 0 with the constant empty histogram (0-private) and post-process (lines 59–64)."},
  {"text": "Step: compose bin n+1 with the histogram so far and post-process (setCount); the levels add: (n+1)·ε/numBins + ε/numBins (lines 65–71)."},
  {"text": "Finally the full histogram uses predBins + 1 = numBins bins, so the level is numBins · (ε/numBins) = ε (lines 79–81).",
   "lean": "case HEq => simp [predBins, mul_div_left_comm]"},
 ]))


node("sv9_aboveThresh_pmf_DP",
 "Headline: AboveThreshold (sparse vector) is ε₁/ε₂ pure-DP",
 "AboveThreshold reports the first of a stream of 1-sensitive queries whose Laplace-noised value reaches a noisy "
 "threshold. However many queries it inspects, the run costs only ε = ε₁/ε₂ of pure DP. One extra hypothesis, "
 "needed for the loop to halt, is assumed.",
 r"""## Plain English

**Theorem (`sv9_aboveThresh_pmf_DP`, DifferentialPrivacy/Queries/AboveThresh/Privacy.lean lines 177–178).** Let
qs be a sequence of queries qs 0, qs 1, … (each maps a list of records to an integer), each with
[sensitivity](#/node/sensitivity) 1, and let T be an integer threshold. Assume the "lucky guess" condition
[has_lucky](#/node/sv9_aboveThresh_SPMF) qs T. Then the AboveThreshold mechanism
[sv9_aboveThresh_SPMF](#/node/sv9_aboveThresh_SPMF) is [pure ε-DP](#/node/PureDP) with ε = ε₁/ε₂.

### The algorithm

The executable version is [sv1_aboveThresh](#/node/sv1_aboveThresh) (AboveThresh/Code.lean lines 63–67):

1. draw a noisy threshold offset τ ~ Laplace(scale 2ε₂/ε₁);
2. for k = 0, 1, 2, …: draw fresh noise v_k ~ Laplace(scale 4ε₂/ε₁) and test whether qs k (l) + v_k ≥ τ + T;
3. output the first k for which the test succeeds.

This is AboveThreshold from Dwork and Roth's book (and the core of the sparse vector technique). The surprising
classical fact, now checked in Lean, is that the privacy cost does **not** grow with the number of queries
inspected.

### What "sv9" is, and why

The proof uses a version of the program that is easier to reason about. Program versions sv1 → sv2 → … → sv9 are
proved equal one step at a time (`sv1_sv2_eq` … `sv8_sv9_eq` in AboveThresh/Properties.lean). sv9 computes the
probability of each output *k* directly: presample all the noise, then check that queries 0…k−1 stay below the
threshold and query k reaches it. The privacy argument is the textbook coupling: shift the threshold noise and the
k-th query's noise by at most 1 and 2 respectively, and pay e^{ε/2} for each shift.

### The extra hypothesis

`has_lucky qs T` (DifferentialPrivacy/Queries/AboveThresh/Properties.lean lines 1802–1803) says that for every τ and every list, there is a noise value K
large enough that qs A (l) + K' ≥ τ + T for **every** query index A and every K' ≥ K. In words: the queries are
uniformly bounded below on each list, so a large enough noise draw always stops the loop. It is used only to show
the program halts with probability 1, so that its output is a true probability distribution (an `SPMF`). Queries
whose values can drift to −∞ are not covered.
""",
 [q("What does AboveThreshold output?",
    ["The index of the first query whose noisy value reaches the noisy threshold",
     "The noisy values of all queries",
     "The number of queries above the threshold",
     "The largest query value"], 0,
    "sv1_aboveThresh returns sv1_threshold sk, the length of the list of rejected noises, i.e. the first index that passed (DifferentialPrivacy/Queries/AboveThresh/Code.lean lines 63–67)."),
  q("How does the privacy cost depend on the number of queries examined?",
    ["It does not: the whole run is ε₁/ε₂-DP", "It grows linearly", "It grows like the square root", "It is unbounded"], 0,
    "The conclusion (line 178) is a single level ε = ε₁/ε₂, for every possible output k."),
  q("What is `has_lucky` needed for?",
    ["To make sure the loop stops with probability 1, so the output is a genuine probability distribution",
     "To make the queries 1-sensitive", "To make the threshold positive", "To bound ε"], 0,
    "It is the argument of sv9_aboveThresh_SPMF and sv1_hasSum_one (DifferentialPrivacy/Queries/AboveThresh/Properties.lean lines 2195–2219), which prove the probabilities sum to 1."),
  q("Which DP notion and noise does this theorem use?",
    ["Pure DP with discrete Laplace noise", "zCDP with Gaussian noise", "Any DPSystem", "Approximate DP with δ > 0"], 0,
    "sv9_aboveThresh_SPMF is built with PureDPSystem and laplace_pureDPSystem (DifferentialPrivacy/Queries/AboveThresh/Properties.lean line 2209), and the conclusion is PureDPSystem.prop."),
 ],
 caveats=[NOT_BUILT,
  "CONDITIONAL on `has_lucky qs T`, a hypothesis not in the classical statement: the queries must be uniformly "
  "bounded below on each input list so that the loop terminates almost surely.",
  "The statement is about sv9 (a rewritten, non-executable form). That it equals the executable sv1 follows from "
  "the chain sv1_sv2_eq … sv8_sv9_eq; the project chains them explicitly in `privUnboundedMax_DP` "
  "(UnboundedMax/Privacy.lean lines 70–71), but there is no general lemma \"sv1 is ε₁/ε₂-DP\".",
  "Specific to pure DP; the generic Sparse vector construction built on it takes AboveThreshold's privacy as a "
  "hypothesis ([privSparse_DP](#/node/privSparse_DP)).",
 ],
 widgets=walk("How the proof goes (Queries/AboveThresh/Privacy.lean, lines 177-470)", [
  {"text": "Pure DP for sets follows from pure DP for single outputs; reduce to showing P(sv9(l₁) = k) ≤ e^ε · P(sv9(l₂) = k) for each output k (lines 180–186).",
   "link": "PureDP", "lean": "apply singleton_to_event"},
  {"text": "Case k = 0 (lines 189–297): only the threshold noise τ and the first query noise v₀ matter. Change variables, shifting v₀ by qs 0 (l₂) − qs 0 (l₁) (lines 212–221).",
   "lean": "rw [tsum_shift cov_τ]"},
  {"text": "Compare the shifted Laplace densities pointwise; each shift by d costs a factor exp(|d|/scale) (laplace_inequality, lines 83–109; applied at line 240).",
   "lean": "· apply laplace_inequality_sub"},
  {"text": "Case k > 0 (lines 298–470), following Dwork–Roth: presample all noise, cancel the deterministic parts (line 303), and shift τ by cov_τ (the change in the running maximum G of earlier noisy queries) and the k-th noise by cov_vk (lines 345–354).",
   "lean": "let cov_vk : ℤ := cov_vk_def qs v0 vs l₁ l₂ point"},
  {"text": "After the shift the acceptance conditions for l₁ and l₂ become literally the same proposition (lines 360–376). Apply the Laplace inequalities for both shifts (lines 380–387) and cancel the remaining Laplace factors (lines 388–404)."},
  {"text": "Bound the shifts with sensitivity: |cov_τ| ≤ 1 and |cov_vk| ≤ 2 (Hsens_cov_τ, Hsens_cov_vk; lines 405–440). The total cost is exp(1/(2ε₂/ε₁)) · exp(2/(4ε₂/ε₁)) = exp(ε₁/ε₂), finished by arithmetic (lines 451–470).",
   "lean": "apply Hsens_cov_vk _ Hqs_sens"},
 ]))
