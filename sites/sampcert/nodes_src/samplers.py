NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]

NOT_BUILT = ("Not built for this site: \"proved\" means the source contains a complete-looking proof, and a text "
             "search of the project finds no `sorry`, `admit` or `axiom`. Lean's kernel was not run here.")


node("probBind",
 "SLang: programs are (sub)probability mass functions",
 "In SampCert a randomized program of type SLang α is literally a function α → [0, ∞]: the probability of each "
 "outcome. Sequencing two programs (bind) multiplies and sums, so every program can be read as an infinite sum.",
 r"""## Plain English

`SLang α` is defined as α → ℝ≥0∞ (SLang.lean line 29): a program *is* its probability mass function. There is no
separate operational semantics in the proofs. The building blocks (SLang.lean lines 56–153) are:

- `probZero`: the zero function (a program that never returns; used to start loop unrollings);
- `probPure a`: probability 1 at *a* (line 66);
- **`probBind p f`** (lines 72–73): run *p*, feed its result *a* to *f*. The probability of *b* is
  Σ_a p(a)·f(a)(b). This makes SLang a monad, so programs are written with Lean's `do` notation;
- `probUniformByte`: each of the 256 byte values with probability 1/256 (line 84). This is the **only source of
  randomness**; everything else is built from it ([uniform samplers](#/node/probUniformByte));
- [probWhile](#/node/probWhile) and [probUntil](#/node/probUntil) for unbounded loops.

Nothing in the type forces the probabilities to sum to 1. A program can lose mass (for example a loop that never
exits), so SLang values are *sub*-probability distributions. Each sampler gets a separate "normalizes" theorem
(Σ = 1), and the subtype `SPMF α` (line 159) packages a program with that proof. Mechanisms in the DP library
return SPMFs or Mathlib `PMF`s.

### Executing SLang

You cannot compute with a function into the extended reals. SampCert runs these programs by marking
`probPure`, `probBind`, `probUniformByte` and `probWhile` as `@[extern]` (lines 65, 71, 83, 143). Compiled code
replaces them with C++ functions in ffi.cpp that really sample, reading bytes from /dev/urandom. The proofs are
about the Lean definitions. That the C++ behaves like them is a trusted assumption.
""",
 [q("What is a value of type SLang ℤ?",
    ["A function from ℤ to [0, ∞] giving each integer's probability", "A random number generator state",
     "A list of samples", "An IO action"], 0,
    "SLang.lean line 29: `abbrev SLang.{u} (α : Type u) : Type u := α → ℝ≥0∞`."),
  q("Must an SLang program's probabilities sum to 1?",
    ["No; that is proved separately for each sampler (or packaged in SPMF)", "Yes, by its type",
     "Only for finite types", "Only for while loops"], 0,
    "The SLang docstring (lines 11–21) says normalization is proven separately; SPMF (line 159) is the subtype with HasSum f 1."),
  q("What is the probability of b under probBind p f?",
    ["Σ over a of p(a)·f(a)(b)", "p(b)·f(b)(b)", "max over a of p(a)·f(a)(b)", "p(b) + f(b)"], 0,
    "SLang.lean lines 72–73."),
 ],
 caveats=["`SLang` and `SPMF` are declared with explicit universe parameters (`abbrev SLang.{u}`), which this site's "
          "source scanner does not pick up, so they have no page of their own; this node stands in for them.",
          "The link between the Lean definitions and the C++ implementations in ffi.cpp is not verified."])


node("probWhile",
 "probWhile: an unbounded loop, defined as a limit of unrollings",
 "A while loop in SLang is the supremum over n of the loop unrolled n times, where runs that have not finished "
 "after n steps get probability 0. So the probability of an outcome is the limit of the probability of reaching it "
 "within n iterations.",
 r"""## Plain English

`probWhile cond body init` (SLang.lean lines 144–145) runs *body* repeatedly, starting from *init*, while *cond*
holds, and returns the final state. Its meaning is built in two steps:

- `probWhileFunctional cond body wh` (lines 115–121) is one step: if *cond a*, run *body* and continue with *wh*;
  otherwise return *a*.
- `probWhileCut cond body n` (lines 126–131) applies that step *n* times, starting from `probZero`. So it is the
  loop truncated at n iterations, where unfinished runs count for nothing.

Then probWhile at outcome x is the supremum over n of probWhileCut at x. The truncations only increase, so this is
the limit of the probability of finishing at x within n steps.

This is a standard least-fixed-point semantics. The loop may lose probability mass if it can run forever. Whether
it does is a separate question, answered for each sampler by its "normalizes" theorem.
""",
 [q("What does probWhileCut cond body 0 a denote?",
    ["The zero (sub)distribution", "The point mass at a", "One iteration of the body", "The full loop"], 0,
    "SLang.lean line 129: the zero case is probZero."),
  q("How is the probability of x under probWhile defined?",
    ["As the supremum over n of the probability under the n-step truncation", "As the n-step truncation for n = 1000",
     "As the probability that the body returns x", "It is axiomatised"], 0,
    "SLang.lean line 145: ⨆ i, probWhileCut cond body i init x."),
 ])


node("probUntil",
 "probUntil: rejection sampling",
 "probUntil body cond draws from body, and redraws until the result satisfies cond. When body is a proper "
 "distribution, the result has the conditional distribution: P(x) = body(x)·[cond x] / P(cond).",
 r"""## Plain English

`probUntil body cond` (SLang.lean lines 151–153) samples once from *body* and then uses
[probWhile](#/node/probWhile) to keep resampling while the condition fails.

The key fact used by every rejection sampler in SampCert is `probUntil_apply_norm` (Foundations/Until.lean lines
252–254). If *body* sums to 1, then

  P(probUntil body cond = x) = (body(x) if cond x, else 0) / Σ_y (body(y) if cond y, else 0).

In words, the output is *body* conditioned on *cond*. The proof (Foundations/Until.lean) sums the geometric series
of failed attempts.

It is used in [UniformSample](#/node/probUniformByte) (reject values ≥ n), the
[discrete Laplace](#/node/DiscreteLaplaceSample) sampler and the
[discrete Gaussian](#/node/DiscreteGaussianSample) sampler.
""",
 [q("If body is a proper distribution, what is the output distribution of probUntil body cond?",
    ["body conditioned on cond", "body itself", "the uniform distribution on {x | cond x}", "a point mass"], 0,
    "probUntil_apply_norm, Foundations/Until.lean lines 252–254."),
  q("What happens if no outcome of body satisfies cond?",
    ["The loop never exits; the output has total probability 0", "It returns the last sample",
     "It returns a default value", "Lean rejects the program"], 0,
    "probWhile's least-fixed-point meaning (SLang.lean lines 144–145) gives 0 to runs that never finish. (The normalized formula then divides by 0, so it is only used when acceptance has positive probability.)"),
 ])


node("probUniformByte",
 "Uniform samplers, from random bytes up",
 "All randomness in SampCert comes from one primitive, a uniformly random byte. From it, a uniform sample on "
 "[0, 2^i) is built from whole bytes plus a few top bits, and a uniform sample on [0, n) by rejecting values ≥ n.",
 r"""## Plain English

- `probUniformByte` (SLang.lean line 84): each `UInt8` value with probability 1/256. At run time this is a byte from
  /dev/urandom (ffi.cpp).
- `probUniformByteUpperBits i` (lines 89–91): the top *i* bits of a byte, uniform on [0, 2^i) for i ≤ 8.
- `probUniformP2 i` (lines 96–102): uniform on [0, 2^i). For i ≥ 8 it draws a whole byte and recurses on i − 8.
- `UniformPowerOfTwoSample n` (lines 108–109): uniform on [0, 2^⌊log₂ n⌋).
- `UniformSample n` (Samplers/Uniform/Code.lean lines 21–23): uniform on [0, n). It draws from
  UniformPowerOfTwoSample (2n) and [rejects](#/node/probUntil) values ≥ n.
- `BernoulliSample num den` (Samplers/Bernoulli/Code.lean lines 23–25): true with probability num/den, by
  testing whether a uniform sample on [0, den) is below num.

Each has "apply" and "normalizes" theorems in the matching Samplers/Uniform/Properties.lean (for example
Samplers/Uniform/Properties.lean). Counting bytes this way lets the project measure exactly how much randomness a
sampler uses (REPRODUCING.md mentions a byte-consumption profile).
""",
 [q("What is the only primitive source of randomness?",
    ["A uniformly random byte", "A uniform real in [0,1]", "A fair coin", "A Gaussian sample"], 0,
    "probUniformByte, SLang.lean line 84; everything else is built from it with bind, while and until."),
  q("How does UniformSample n get an exactly uniform value on [0, n)?",
    ["Rejection: sample uniformly from a power-of-two range and retry when the value is ≥ n",
     "Take a random byte modulo n", "Scale a random real", "Round a Gaussian"], 0,
    "Samplers/Uniform/Code.lean lines 21–23 use probUntil with condition x < n."),
 ])


node("BernoulliExpNegSample",
 "BernoulliExpNegSample: a coin that lands heads with probability exp(−num/den)",
 "Using only uniform integers, this sampler flips a coin with probability exactly e^(−γ) for a rational γ = num/den. "
 "It is the acceptance test inside both the Laplace and the Gaussian samplers.",
 r"""## Plain English

`BernoulliExpNegSample num den` (Samplers/BernoulliNegativeExponential/Code.lean lines 115–126) returns true with
probability exp(−num/den). This is proved as `BernoulliExpNegSample_apply_true`
(Samplers/BernoulliNegativeExponential/Properties.lean lines 1189–1215).

How it works (Samplers/BernoulliNegativeExponential/Code.lean docstrings, lines 37–113):

- **γ ≤ 1** (`BernoulliExpNegSampleUnit`, lines 76–78). Von Neumann's trick: draw independent Bernoulli(γ/1),
  Bernoulli(γ/2), Bernoulli(γ/3), … until one fails. Let K be the step at which it fails. Then
  P(K = n) = γ^{n−2}/(n−2)! − γ^{n−1}/(n−1)!, so P(K even) = Σ (−γ)^i/i! = e^{−γ}. Return whether K is even.
  The loop is a [probWhile](#/node/probWhile) (`BernoulliExpNegSampleUnitAux`, lines 60–62).
- **γ > 1** (lines 119–126): split γ = ⌊γ⌋ + (fractional part). Flip ⌊γ⌋ independent e^{−1} coins
  (`BernoulliExpNegSampleGenLoop`, lines 89–95), then one e^{−frac} coin, and return true only if all succeed:
  e^{−⌊γ⌋}·e^{−frac} = e^{−γ}.

The proof in Samplers/BernoulliNegativeExponential/Properties.lean (about 1,200 lines) computes the loop's distribution exactly and sums the
alternating exponential series.
""",
 [q("With what probability does BernoulliExpNegSample num den return true?",
    ["exp(−num/den)", "num/den", "1 − exp(−num/den)", "exp(num/den)/2"], 0,
    "BernoulliExpNegSample_apply_true, Samplers/BernoulliNegativeExponential/Properties.lean lines 1189–1190."),
  q("How does the γ ≤ 1 case turn a loop into e^{−γ}?",
    ["The probability that the stopping step is even is the alternating series Σ(−γ)^i/i!", "By rejection sampling a Gaussian",
     "By computing e^{−γ} in floating point", "By a Taylor polynomial truncated at 10 terms"], 0,
    "Samplers/BernoulliNegativeExponential/Code.lean lines 64–78 (docstring of BernoulliExpNegSampleUnit)."),
 ])


node("DiscreteLaplaceSample",
 "The discrete Laplace samplers",
 "SampCert has two discrete Laplace samplers, a plain one and an optimised one, plus a switch that picks between "
 "them. All three are proved to output P(x) ∝ exp(−|x|/s) with s = num/den, and to be equal as distributions.",
 r"""## Plain English

The discrete Laplace distribution with scale s puts probability (e^{1/s} − 1)/(e^{1/s} + 1) · e^{−|x|/s} on each
integer x. It is the noise for [pure DP](#/node/PureDPSystem), and the Gaussian sampler uses it to
[propose candidates](#/node/DiscreteGaussianSample).

- `DiscreteLaplaceSample num den` (Samplers/Laplace/Code.lean lines 66–69): draw a geometric magnitude by
  repeatedly flipping e^{−den/num} coins (`DiscreteLaplaceSampleLoop`, lines 56–60, via
  [BernoulliExpNegSample](#/node/BernoulliExpNegSample)) and a random sign. Reject "negative zero" so 0 is not
  counted twice.
- `DiscreteLaplaceSampleOptimized` (lines 75–78): the variant from Canonne–Kamath–Steinke that first draws a
  uniform remainder and a geometric quotient (`DiscreteLaplaceSampleLoop'`, lines 47–54), then divides. It is
  faster when s is large.
- `DiscreteLaplaceSampleMixed num den mix` (lines 84–87): uses the plain sampler when num ≤ den·mix and the
  optimised one otherwise.

Their closed form is `DiscreteLaplaceSample_apply` (Samplers/Laplace/Properties.lean lines 345–414). The fact that
the two algorithms give the *same* distribution is `DiscreteLaplaceSample_equiv` (lines 1056–1058; the main work
is `DiscreteLaplaceSampleLoop_equiv`, lines 782–1051). See also
[DiscreteLaplaceSampleMixed_apply](#/node/DiscreteLaplaceSampleMixed_apply).

`DiscreteLaplaceGenSample num den μ` (Samplers/LaplaceGen/Code.lean lines 12–14) adds μ to shift the centre;
`DiscreteLaplaceGenSamplePMF` packages it as a PMF.
""",
 [q("What is the scale s of DiscreteLaplaceSample num den?",
    ["num/den", "den/num", "num·den", "1"], 0,
    "DiscreteLaplaceSample_apply (Samplers/Laplace/Properties.lean line 346) has exp(−|x|/(num/den))."),
  q("Why does the plain sampler reject the outcome (sign = negative, magnitude = 0)?",
    ["Otherwise 0 would be produced by both signs and get twice its share", "To make the output positive",
     "To speed it up", "Because 0 is not an integer"], 0,
    "Samplers/Laplace/Code.lean line 67: probUntil with condition ¬(x.1 ∧ x.2 = 0)."),
 ])


node("DiscreteLaplaceSampleMixed_apply",
 "Key lemma: both Laplace samplers give the same exact distribution",
 "Whichever branch the mixed sampler takes, its probability at x is (e^{1/s} − 1)/(e^{1/s} + 1) · e^{−|x|/s} with "
 "s = num/den. So the speed switch can never change the privacy analysis.",
 r"""## Plain English

**Lemma (`DiscreteLaplaceSampleMixed_apply`, Samplers/Laplace/Properties.lean lines 1093–1094).** For all positive
num, den, every *mix*, and every integer x,

  P(DiscreteLaplaceSampleMixed num den mix = x) = (e^{1/s} − 1)/(e^{1/s} + 1) · e^{−|x|/s},  where s = num/den.

The proof (lines 1095–1098) just splits on the branch and uses the closed forms of the two samplers,
`DiscreteLaplaceSample_apply` (lines 345–414) and `DiscreteLaplaceSampleOptimized_apply` (lines 1073–1076). The
companion `DiscreteLaplaceSampleMixed_equiv` (lines 1103–1109) states the two as programs are equal. The
[Gaussian sampler](#/node/DiscreteGaussianSample)'s proof uses it to remove the dependence on *mix*.

The constant (e^{1/s} − 1)/(e^{1/s} + 1) is the normaliser: summing e^{−|x|/s} over all integers gives
(e^{1/s} + 1)/(e^{1/s} − 1).
""",
 [q("Does the lemma's right-hand side depend on mix?",
    ["No", "Yes, linearly", "Only when mix = 0", "Only through the normalising constant"], 0,
    "Line 1094: the formula mentions only num, den and x."),
  q("What is Σ over integers x of e^{−|x|/s}?",
    ["(e^{1/s} + 1)/(e^{1/s} − 1)", "s", "2s", "1"], 0,
    "That is why the normaliser in the lemma is its reciprocal."),
 ],
 caveats=[NOT_BUILT])


node("DiscreteGaussianSample",
 "DiscreteGaussianSample: the Canonne–Kamath–Steinke rejection sampler",
 "Propose an integer from a discrete Laplace distribution of scale t = ⌊σ⌋ + 1, accept it with probability "
 "exp(−(|y| − σ²/t)²/(2σ²)), and repeat until accepted. The accepted value is exactly discrete-Gaussian with scale σ.",
 r"""## Plain English

`DiscreteGaussianSample num den mix` (Samplers/Gaussian/Code.lean lines 36–42), with σ = num/den:

1. set t = ⌊num/den⌋ + 1 (lines 37–38), and square num and den (lines 39–40), since the algorithm works with σ²;
2. **loop body** `DiscreteGaussianSampleLoop` (lines 25–31): draw Y from the
   [discrete Laplace sampler](#/node/DiscreteLaplaceSample) with scale t, and flip a
   [coin with probability e^{−n/d}](#/node/BernoulliExpNegSample), where n/d = (|Y|·t − σ²)² / (2σ²t²), i.e. the
   coin succeeds with probability exp(−(|Y| − σ²/t)²/(2σ²));
3. [repeat until](#/node/probUntil) the coin succeeds (line 41), and return Y (line 42).

All the arithmetic is on natural numbers and positive integers, so it is exact. The whole construction rests on
the uniform byte primitive.

Its output distribution is the headline [DiscreteGaussianSample_apply](#/node/DiscreteGaussianSample_apply).
`DiscreteGaussianSample_normalizes` (Samplers/Gaussian/Properties.lean lines 361–376) then shows the probabilities
sum to 1, and `DiscreteGaussianPMF` (lines 383–384) packages it as a Mathlib PMF. That PMF is the function the
deployed library exports (SampCert.lean, `DiscreteGaussianSampleGet`).

`DiscreteGaussianGenSample num den μ` (Samplers/GaussianGen/Code.lean lines 22–24) shifts the output by μ. Note it
hard-codes mix = 7. Its PMF version `DiscreteGaussianGenPMF` is the noise used by the
[Gaussian mechanism](#/node/privNoisedQuery).
""",
 [q("What distribution are the candidates drawn from?",
    ["Discrete Laplace with scale ⌊σ⌋ + 1", "Uniform on [−σ, σ]", "Discrete Gaussian with scale 2σ", "Geometric"], 0,
    "Samplers/Gaussian/Code.lean line 26 calls DiscreteLaplaceSampleMixed t 1 mix with t = (num/den).succPNat."),
  q("Why can the sampler be exact?",
    ["It uses only integer arithmetic and exact Bernoulli(e^{−q}) coins for rational q", "It uses 128-bit floats",
     "It truncates the tails at 10σ", "It precomputes a table"], 0,
    "All quantities in lines 25–42 are natural numbers or positive integers; the only probabilities are rational Bernoulli and exp(−rational) coins."),
 ])


node("discrete_gaussian",
 "discrete_gaussian: the target formula",
 "discrete_gaussian σ μ x is exp(−(x − μ)²/(2σ²)) divided by the sum of the same expression over all integers. It is "
 "an ordinary real-valued formula, and the sampler is proved to match it.",
 r"""## Plain English

- `gauss_term_ℝ σ μ x` (Util/Gaussian/DiscreteGaussian.lean lines 29–30) is exp(−(x − μ)²/(2σ²)), the Gaussian
  bell curve without a normalising constant.
- `discrete_gaussian σ μ x` (lines 68–69) divides it by Σ over all integers z of gauss_term_ℝ σ μ z.

So discrete_gaussian σ μ restricted to the integers is a probability distribution (`discrete_gaussian_normalizes`,
lines 332–337, needs σ ≠ 0), centred at μ with scale σ.

For the privacy proofs, the project uses Mathlib's **Poisson summation formula** (`poisson_gauss_term`, lines
210–217) to show that shifting the centre by a real amount never increases the normalising sum
(`sum_gauss_term_bound`, Util/Gaussian/GaussBound.lean lines 39–40). This is one of the "deep properties" the
README mentions. For integer shifts the sum is unchanged (Util/Gaussian/GaussPeriodicity.lean).
""",
 [q("What is the denominator of discrete_gaussian σ μ x?",
    ["Σ over all integers z of exp(−(z − μ)²/(2σ²))", "σ√(2π)", "The number of integers within 3σ", "1"], 0,
    "Util/Gaussian/DiscreteGaussian.lean lines 68–69."),
  q("Where is Poisson summation used?",
    ["To compare the normalising sums of shifted and centred Gaussians", "To build the sampler",
     "To prove the Laplace sampler correct", "Nowhere"], 0,
    "poisson_gauss_term (lines 210–217) feeds sum_gauss_term_bound (GaussBound.lean lines 39–153), used in the Rényi bound."),
 ])


node("discrete_GaussianGenSample_ZeroConcentrated",
 "Key lemma: the Rényi divergence between two shifted discrete Gaussians",
 "For discrete Gaussians of the same scale σ centred at integers μ and ν, the Rényi divergence of order α is at "
 "most α·(μ − ν)²/(2σ²). This is the whole privacy content of the Gaussian mechanism.",
 r"""## Plain English

**Lemma (`discrete_GaussianGenSample_ZeroConcentrated`, DifferentialPrivacy/ZeroConcentrated/ConcentratedBound.lean
lines 615–617).** For α > 1, positive num, den and integers μ, ν,

  [RenyiDivergence](#/node/RenyiDivergence)(DiscreteGaussianGenPMF num den μ, DiscreteGaussianGenPMF num den ν, α)
  ≤ α · (μ − ν)² / (2·(num/den)²).

It is stated directly about the **sampler's** PMF. The proof (lines 618–678) first replaces it by the formula
[discrete_gaussian](#/node/discrete_gaussian), using the sampler-correctness theorem. It then applies
`Renyi_divergence_bound` (lines 95–98), which computes the Rényi sum for Gaussians: after completing the square it
is a ratio of two normalising sums. The comparison of those sums uses the Poisson-summation bound
`sum_gauss_term_bound` (line 205).

The [Gaussian mechanism](#/node/privNoisedQuery_zCDP) applies it with |μ − ν| ≤ Δ.
""",
 [q("What does the bound depend on?",
    ["α, the shift μ − ν and the scale σ", "Only σ", "The data list", "Only α"], 0,
    "ConcentratedBound.lean line 617."),
  q("Is the lemma about an idealised Gaussian or about the sampler?",
    ["The sampler's PMF (DiscreteGaussianGenPMF)", "An idealised continuous Gaussian", "A floating-point approximation", "Neither"], 0,
    "Line 616 names DiscreteGaussianGenPMF; lines 624–630 bridge it to the formula via DiscreteGaussianGenSample_apply."),
 ],
 caveats=[NOT_BUILT])


EXTRA = {
 "probWhile": [q("Can a probWhile loop lose probability mass?",
    ["Yes, if it can run forever; termination is proved separately", "No, never", "Only if cond is constant", "Only for infinite types"], 0,
    "The meaning is a supremum of truncations (SLang.lean lines 144–145); mass on never-ending runs is simply absent.")],
 "probUntil": [q("Which samplers use probUntil?",
    ["The uniform, discrete Laplace and discrete Gaussian samplers", "None", "Only the Bernoulli sampler", "Only AboveThreshold"], 0,
    "Samplers/Uniform/Code.lean line 22, Samplers/Laplace/Code.lean line 67, Samplers/Gaussian/Code.lean line 41.")],
 "probUniformByte": [q("How does BernoulliSample num den decide true?",
    ["A uniform sample on [0, den) is below num", "A byte is below num", "A Gaussian is positive", "num > den"], 0,
    "Samplers/Bernoulli/Code.lean lines 23–25.")],
 "BernoulliExpNegSample": [q("How is γ > 1 handled?",
    ["Split γ into integer and fractional parts and multiply independent coins", "It is not allowed", "By rescaling γ to 1", "By using floating point"], 0,
    "Samplers/BernoulliNegativeExponential/Code.lean lines 119–126.")],
 "DiscreteLaplaceSample": [q("Which sampler does DiscreteLaplaceSampleMixed choose when num ≤ den·mix?",
    ["The plain DiscreteLaplaceSample", "The optimised one", "Both, averaged", "A Gaussian"], 0,
    "Samplers/Laplace/Code.lean lines 84–87.")],
 "DiscreteLaplaceSampleMixed_apply": [q("Why does it matter for privacy that the two branches agree?",
    ["The privacy proofs use only the closed form, so the speed choice cannot weaken privacy", "It does not matter", "Because the optimised one is less private", "Because mix is secret"], 0,
    "Both branches have the same closed form (lines 1093–1098), and the mechanisms' proofs use that closed form.")],
 "DiscreteGaussianSample": [q("What is returned once the coin succeeds?",
    ["The Laplace candidate Y itself", "Y shifted by t", "|Y|", "The number of attempts"], 0,
    "Samplers/Gaussian/Code.lean line 42 returns r.1, the candidate.")],
 "discrete_gaussian": [q("Is discrete_gaussian a program or a formula?",
    ["A real-valued formula", "An SLang program", "An axiom", "A PMF built by sampling"], 0,
    "It is a plain `def` returning ℝ (Util/Gaussian/DiscreteGaussian.lean lines 68–69).")],
 "discrete_GaussianGenSample_ZeroConcentrated": [q("For α = 2, σ = 3 and centres 0 and 1, what is the bound?",
    ["2·1/(2·9) = 1/9", "1/3", "2/3", "1"], 0,
    "α·(μ−ν)²/(2σ²) = 2·1/18.")],
}
for n in NODES:
    n["quiz"] += EXTRA.get(n["id"], [])
