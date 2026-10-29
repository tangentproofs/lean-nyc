# About this site

## The project

[leanprover/SampCert](https://github.com/leanprover/SampCert) is, in its README's words, "a verified implementation
using Lean and Mathlib of randomized algorithms including the discrete Gaussian sampler for differential privacy,
key results in zero concentrated differential privacy, and some verified (unbounded) private queries". The README
says SampCert is **deployed in the AWS Clean Rooms Differential Privacy service**.

The README names **Jean-Baptiste Tristan** as the principal developer, with **Markus de Medeiros** also developing
it. It thanks Leo de Moura, Anjali Joshi, Joseph Tassarotti, Stefan Zetzsche, Aws Albharghouti, Muhammad Naveed,
Tristan Ravitch, Fabian Zaiser and Tomas Skrivan for important ideas or deployment tools. The source files carry
"Copyright (c) 2024 Amazon.com, Inc. or its affiliates" and the Apache 2.0 licence. The project's citation is
*SampCert: Verified Differential Privacy* (Zenodo, doi 10.5281/zenodo.11204806). The repository's paper_mapping.md
maps an accompanying paper's definitions and listings to the code.

The README cites three papers: Canonne, Kamath and Steinke on the discrete Gaussian (arXiv:2004.00010), Bun and
Steinke on zero-concentrated DP (arXiv:1605.02065), and arXiv:1909.01917 for the unbounded queries.

## What the Lean covers

SampCert has two halves. They meet in the noise mechanisms.

### 1. Samplers, verified exactly

Randomized programs are written in **SLang**, a probability monad in which a program *is* its probability mass
function ([probBind](#/node/probBind)). Loops have a limit semantics ([probWhile](#/node/probWhile),
[probUntil](#/node/probUntil)). Starting from one primitive, a uniform random byte, the library builds and verifies
uniform and Bernoulli samplers ([probUniformByte](#/node/probUniformByte)), an exp(−γ) coin
([BernoulliExpNegSample](#/node/BernoulliExpNegSample)), two discrete Laplace samplers
([DiscreteLaplaceSample](#/node/DiscreteLaplaceSample)) and the discrete Gaussian sampler
([DiscreteGaussianSample](#/node/DiscreteGaussianSample)). For each one, the output distribution is proved to be
**exactly** the intended formula. The headline is
[DiscreteGaussianSample_apply](#/node/DiscreteGaussianSample_apply).

### 2. A differential privacy framework

- Datasets are lists, neighbours differ by one inserted or deleted record ([Neighbour](#/node/Neighbour)), and
  mechanisms are maps from lists to distributions ([Mechanism and combinators](#/node/privComposeAdaptive)).
- Three privacy notions: [pure ε-DP](#/node/PureDP), [(ε, δ)-DP](#/node/ApproximateDP) and
  [ρ-zCDP](#/node/zCDP) via [Rényi divergence](#/node/RenyiDivergence).
- An abstract interface [DPSystem](#/node/DPSystem), with instances [PureDPSystem](#/node/PureDPSystem) (Laplace
  noise) and [zCDPSystem](#/node/zCDPSystem) (Gaussian noise). Each comes with proofs of adaptive composition,
  post-processing, constants, and conversion to (ε, δ)-DP.
- Headlines on the zCDP side: the [Gaussian mechanism](#/node/privNoisedQuery_zCDP),
  [adaptive composition](#/node/privComposeAdaptive_zCDP) and the
  [zCDP → (ε, δ)-DP conversion](#/node/zCDP_ApproximateDP). The key lemma [ofDP](#/node/ofDP) shows that pure ε-DP
  implies ½ε²-zCDP.
- Queries: the [noised histogram](#/node/privNoisedHistogram_DP) (generic over the DP system),
  [AboveThreshold](#/node/sv9_aboveThresh_pmf_DP) (pure DP), the [unbounded max](#/node/privUnboundedMax_DP), the
  [sparse vector technique](#/node/privSparse_DP) (conditional), and
  [count, bounded sum and mean, histogram mean, parallel histogram](#/node/privNoisedBoundedMean_DP).

## What this site leaves out

- **Execution and extraction.** SLang's primitives are `@[extern]` and run as C++ in ffi.cpp. SampCert/Extractor/
  (about 800 lines) translates samplers to Dafny and then Python, and Tests/ has Kolmogorov–Smirnov tests and
  benchmarks. None of this is verified and none of it is explained here, except where it affects trust
  ([Trust](#/page/trust)).
- **The top-level file SampCert.lean.** It restates the bounded-mean privacy for both systems
  (`combineConcentrated`, `combinePure`), defines an example histogram mean, and exports
  `DiscreteGaussianSampleGet` for use from other languages. It is not scanned (its example definition `numBins`
  clashed with a variable name and confused the scanner) and is described in prose.
- **Most proof-internal lemmas.** About 760 declarations were scanned. This site explains 35 of them: the six
  headlines, their statement set (grouped where natural) and a few key lemmas. The Rényi-divergence library, the
  Gaussian/Poisson-summation analysis, the 2,200-line AboveThreshold program-equivalence chain and the 1,400-line
  proof of [ofDP](#/node/ofDP) are outlined, not explained step by step.

## Where to start

Read [what an SLang program is](#/node/probBind), then the
[sampler headline](#/node/DiscreteGaussianSample_apply). For privacy, start at [zCDP](#/node/zCDP) and the
[Gaussian mechanism](#/node/privNoisedQuery_zCDP), then the [DPSystem](#/node/DPSystem) interface and the
[histogram](#/node/privNoisedHistogram_DP).
