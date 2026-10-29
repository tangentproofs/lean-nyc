# Review: do the statements say what they claim?

For each headline: is the Lean statement faithful to its name, its docstring and the README or paper mapping? This
review was done by reading the source. Nothing was compiled.

## DiscreteGaussianSample_apply: faithful, and strong

The statement is an exact equality, at every integer, between the program's probability and the discrete Gaussian
formula exp(−x²/2σ²)/Σ exp(−z²/2σ²). It matches the README's claim of a verified discrete Gaussian sampler. Two
remarks:

- **σ is the scale, not the variance.** Docstrings in Samplers/Gaussian/Code.lean say "variance (num/den)^2". The
  discrete Gaussian's variance is slightly below σ². The theorem itself is unambiguous.
- **It is a statement about the Lean meaning of the program.** The program that runs replaces the four SLang
  primitives with C++ (`@[extern]`). See [Trust](#/page/trust).

## privNoisedQuery_zCDP: faithful; one docstring is off

The statement gives ρ = ½(ε₁/ε₂)² for discrete Gaussian noise of scale Δε₂/ε₁ on a Δ-sensitive query. That is the
standard Gaussian-mechanism bound Δ²/(2σ²), stated for the **actual sampler**. The docstrings on lines 23 and 130
call it "(Δε₂/ε₁)^2-zCDP", which is not what the statement says (it looks like the noise scale squared). The statement
is right; the comment is misleading.

## zCDP: the definition matches Bun–Steinke

`zCDP q ρ` is: absolute continuity on neighbours, plus Rényi divergence D_α ≤ ρα for all α > 1. This is Bun and
Steinke's ρ-zCDP. The absolute-continuity conjunct is not in their definition, but it follows from a finite Rényi
bound, so nothing is lost. The code calls the parameter ε and some docstrings write "(ε²/2)-zCDP", which can
mislead a reader into thinking the parameter is ε. Pure ε-DP gives `zCDP q (ε²/2)` ([ofDP](#/node/ofDP)), exactly as
in Bun–Steinke Proposition 1.4.

## privComposeAdaptive_zCDP: faithful

Adaptive composition with ρ₁ + ρ₂, the second mechanism required to be ρ₂-zCDP for every value of the first output.
That is the standard theorem. It requires discrete (countable) output types, which is the library's setting
throughout.

## zCDP_ApproximateDP: faithful, stated in reverse

The usual statement is "ρ-zCDP ⇒ (ρ + 2√(ρ ln 1/δ), δ)-DP". The Lean statement fixes the target (ε′, δ) and computes
the ρ that suffices, as the root of a quadratic. The forward form is `ApproximateDP_of_zCDP` (same file, lines
574–576). The two agree (`zCDP_of_adp_def.eqε`). The δ ≥ 1 case is handled trivially, which is correct.

## privNoisedHistogram_DP: faithful; parameterised

The hypothesis `HN_bin` is the noise system's parameter condition for one bin at level ε/numBins, not a missing
proof. For the two instances it is simple arithmetic. The budget split is sequential. Parallel composition would
allow a full ε per bin, and the separate ParHistogram query does that for pure DP.

## sv9_aboveThresh_pmf_DP: CONDITIONAL, and about a rewritten program

- **Extra hypothesis.** `has_lucky qs T` requires the queries to be uniformly bounded below on each list, so the loop
  halts almost surely. Classical AboveThreshold has no such assumption; it allows non-termination (or an explicit
  ⊥ output). This restriction is real but mild for typical counting queries. The project discharges it for the
  queries it uses (`lucky_guess`).
- **About sv9, not sv1.** The privacy theorem is stated for `sv9_aboveThresh_SPMF`, a non-executable rearrangement.
  It is *proved equal* to the executable sv1 through eight equalities, so nothing is lost mathematically. But the
  repository has no standalone lemma "sv1_aboveThresh_PMF is ε₁/ε₂-DP". The equality chain is applied explicitly
  only inside [privUnboundedMax_DP](#/node/privUnboundedMax_DP).
- **Pure DP only.** AboveThreshold is proved for the Laplace/pure-DP instance, not for zCDP.

## Other things worth knowing

- **Sparse vector is conditional.** [privSparse_DP](#/node/privSparse_DP) assumes the per-round AboveThreshold
  privacy (`HDP`) for an arbitrary DP system, and that assumption is never discharged. Moreover the rounds always use
  the Laplace-based AboveThreshold program, whatever system `dps` the result is stated for.
- **Neighbouring is add/remove.** All results are for "unbounded" DP (insert or delete one record). Replace-one
  neighbours cost twice as much.
- **Exact, not floating point.** All sampler arithmetic is on naturals and integers, and all distributions are
  exact. This is a genuine strength over floating-point implementations.
