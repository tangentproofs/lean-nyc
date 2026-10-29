# NOTES for the coordinator: sampcert

## Time spent

About 20 minutes of wall-clock time by the sandbox clock (05:47 to about 06:07 UTC, 2026-10-29), including six
builds of roughly 30 seconds each. No Lean was built.

## What was produced

- 35 nodes in four files:
  - **6 headlines:** `DiscreteGaussianSample_apply`, `privNoisedQuery_zCDP`, `privComposeAdaptive_zCDP`,
    `zCDP_ApproximateDP`, `privNoisedHistogram_DP`, `sv9_aboveThresh_pmf_DP`. Each has a walkthrough with line
    references.
  - **About 20 statement-set nodes**, grouped where natural. For example, `privComposeAdaptive` covers
    Mechanism, Query, privCompose, privPostProcess, privConst and privParCompose, and `zCDP` covers zCDPBound and
    ACNeighbour.
  - **Key lemmas:** `ofDP`, `discrete_GaussianGenSample_ZeroConcentrated`, `DiscreteLaplaceSampleMixed_apply`,
    `privUnboundedMax_DP` and `privSparse_DP`, plus one grouped node, `privNoisedBoundedMean_DP`, for the
    remaining small queries.
- Pages: about, review and trust.
- The build ends with "built _site/sampcert". There are 73 "meaning-dependency has no explainer" warnings, all for
  sub-definitions that are covered in prose inside a grouped node (e.g. `zCDPBound`, `probWhileCut`, the
  `sv2…sv8` chain) or for scanner artefacts (see below).

## Calls I made

1. **Headlines.** I picked six, following the README's three claims (Gaussian sampler, zCDP results, private
   queries) and paper_mapping.md. I left the Laplace sampler, pure-DP composition and `ofDP` as non-headline
   nodes to stay within the six-headline limit.
2. **`authors`.** The file said "the SampCert authors (Markus de Medeiros and collaborators)". The README names
   Jean-Baptiste Tristan as the *principal* developer, with Markus de Medeiros also developing it, so I changed it
   to "Jean-Baptiste Tristan (principal developer) and Markus de Medeiros, with other contributors". I did not
   change `members`. Copyright lines say Amazon.com, Inc.; I mention that on the About page.
3. **Roots.** I scan SampCert/SLang.lean, Foundations, Samplers, Util and DifferentialPrivacy. I excluded:
   - **SampCert.lean (top level).** Its example `def numBins` made the scanner treat the histogram's *variable*
     `numBins` as a dependency on that def.
   - **SampCert/Extractor** (code generation) and **Tests**.

   SampCert.lean is referenced on the Trust page by explicit pinned GitHub URLs.
4. **Walkthrough `lean:` snippets.** These must lie inside the headline's own line range, or the engine warns
   "not verbatim". So for steps describing helper lemmas (for example `privComposeAdaptive_renyi_bound` or
   `exactBinCount_sensitivity`) I kept the text and line numbers and dropped the snippet.
5. **Ambiguous file names.** `Code.lean`, `Properties.lean` and `Privacy.lean` each exist many times. The linker
   leaves an ambiguous bare name unlinked, so I qualified every such reference with its directory.

## Engine and scanner issues (not fixed; I may not edit the engine)

- **Short-name collisions.** ZeroConcentrated/DP.lean defines `B`, `C`, `t`, `β`, `A_pmf`, and
  ZeroConcentrated/Postprocessing.lean defines `δ`. Local variables with the same names elsewhere (histogram bins
  `B`, the Gaussian loop's `t`, privacy parameter `δ`, the variable `lucky_guess`) get resolved to these defs. So
  `privNoisedHistogram_DP`, `DiscreteGaussianSample_apply`, `zCDP_ApproximateDP` and others show spurious
  meaning-dependencies. This is documented on the Trust page and in the `ofDP` caveat.
- **Universe-polymorphic abbrevs are not scanned.** `abbrev SLang.{u}` and `abbrev SPMF.{u}` produce no
  declaration. The `probBind` node stands in for SLang.
- **Mathlib links for project names.** Adding `ENNReal` to `mathlibNamespaces` (needed for the gloss) did not stop
  project decls like `ENNReal.ofEReal` from resolving to the project, which is correct. But I did not audit
  whether every `ENNReal.*` identifier in the rendered source links to the right place.

## Where I am least sure

- **`zCDP` (parameter naming).** I say that `zCDP q ε` is Bun–Steinke ρ-zCDP (Rényi ≤ ε·α). Several upstream
  docstrings say "(ε²/2)-zCDP" and ZeroConcentrated/DP.lean around line 2094 notes "`zCDPBound _ ε` corresponds to
  `(1/2)ε²`-zCDP (not ε-zCDP)". I read these as a different naming convention, where the level is written ε²/2,
  not as a different definition. The definition itself (lines 46–48) is unambiguous, but a domain expert should
  confirm my wording.
- **`privNoisedQuery_zCDP` docstring.** I say the docstring "(Δε₂/ε₁)^2-zCDP" doesn't match the statement. I'm
  confident about the statement; the author may have meant something else by the comment.
- **`ofDP` proof outline.** "Two-point distributions on Bool, Jensen-type bound, reduce to the sinh inequality" is
  read off the lemma names and statements (`A_pmf`, `B`, `A_jensen`, `sinh_inequality`), not traced through
  the ~1,400 lines.
- **`sv9_aboveThresh_pmf_DP` walkthrough.** The k > 0 steps follow the proof's own comments. The descriptions of
  `cov_τ` as "the change in the running maximum G" and of the sensitivity bounds |cov_τ| ≤ 1, |cov_vk| ≤ 2 are
  from the definitions (Privacy.lean lines 19–28, 142–175). I did not check each inequality.
- **`DiscreteGaussianSample_apply` walkthrough.** The line ranges of the middle steps (267–316) are my grouping of
  a long `rw`/`conv` script. The algebra I describe (Laplace × acceptance = constant × Gaussian) is right, but which
  exact line cancels which factor is approximate.
- **`privSparse_DP` "the program always uses the Laplace-based AboveThreshold, whatever system dps".** This is
  based on `sv1_aboveThresh_PMF` being built with `PureDPSystem laplace_pureDPSystem`
  (AboveThresh/Properties.lean line 2196) while privSparse is generic in `dps`. It looks deliberate and harmless,
  but it is my inference.
- **`has_lucky` as "uniformly bounded below".** It is my paraphrase of lines 1802–1803 (∃K ∀A ∀K′ ≥ K, qs A l + K′
  ≥ τ + T, for each τ and l). I believe it's right.

## Things the authors might object to

- Labelling AboveThreshold **CONDITIONAL** because of `has_lucky`. The authors might see it as a harmless
  well-formedness condition. I kept the label but said it is mild and is discharged for the project's own queries.
- Calling `privSparse_DP` CONDITIONAL. It takes the per-round privacy as a hypothesis that is never discharged.
- Pointing out the `DirtyIOGet` "unsound" extern in SampCert.lean (I quote the authors' own comment) and stressing
  that the C++ FFI is trusted. Both are accurate, but they are prominent on the Trust page.
- Pointing out two docstring mismatches (variance vs scale; "(Δε₂/ε₁)^2-zCDP").
- The lead mentions AWS Clean Rooms deployment. That comes from the README; I made no independent claim about what
  is deployed.
