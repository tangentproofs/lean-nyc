# NOTES for the coordinator (not published)

Slug `formal-learning-theory`, upstream Zetetic-Dhruv/formal-learning-theory-kernel at
cdc4fc3df3d4f9487c7f91872487a8eff120d188 (Apache-2.0 + a citation request in LICENSE).

## Time

Wall clock, from the system clock: started 07:24:48 UTC, last build and commit at about 07:48 UTC on 2026-10-29, so roughly
24 minutes of wall-clock time. (That is the clock reading, not an estimate.)

## What I produced

- `site.json` (renamed from `.todo`), with 6 headlines: `fundamental_theorem`, `vc_characterization`,
  `fundamental_vc_compression_with_info`, `littlestone_characterization`, `gold_theorem`, `online_pac_gold_separation`.
- 50 nodes: 6 headlines, 20 statement-set definitions, 5 spine lemmas (`vcdim_finite_imp_uc'`, `uc_imp_pac`,
  `vcdim_infinite_not_pac`, `fundamental_rademacher`, `pac_sample_complexity_sandwich`), 6 grouped nodes (measurability
  / Borel–analytic, PAC-Bayes, IndependentVC, mind changes, Extended.lean, misc PAC facts) and 13 small definitions.
- `pages/about.md` (includes the LICENSE citation request and BibTeX), `review.md`, `trust.md`, `roadmap.md`
  (33 numbered steps in dependency order with exact line links).
- Build: `engine/build.sh formal-learning-theory` ends with "built _site/formal-learning-theory". Remaining warnings
  are only minor unexplained meaning-dependencies (FinitePMF, gibbsError, SignVector, LossFunction, TrueError,
  DataStream.prefix, MeasurableHypotheses, PACLearnableWithAdviceRegular, KrappWirthSeparationMeasTarget …).

## The sorry question (asked explicitly in the task)

`grep -w sorry` hits 17 files. I stripped Lean comments and strings with a small script and re-searched:

- **FLT_Proofs/ (the library): 0 sorry in code.** 14 files mention `sorry` only in comments or docstrings. Several of
  those comments are stale and describe sorrys that are gone. Notably Complexity/Symmetrization.lean lines 1015–1028
  call `exchangeability_chain_bound` "ORPHANED — contains 2 sorrys". It has none, and it *is* on the fundamental
  theorem's path (symmetrization_uc_bound → double_sample_pattern_bound → exchangeability_chain_bound). Also
  Complexity/Generalization.lean lines 2843–2845, Theorem/PAC.lean line 375 and Theorem/Separation.lean lines 790–799, 863.
- **Verification/ChallengeCrown.lean: 8 real sorrys**, by design (Comparator challenge statements). In the separate
  `Verification` lean_lib, not the default target.
- **world_model/future_work/: 7 real sorrys** in tactic experiments, not in any lakefile target.
- No `axiom`, `admit`, `native_decide`, `implemented_by`, `extern` or `opaque` anywhere.

So the README's "0 sorry" holds for the library, as far as text search can tell. I could not verify the README's CI
claims (no build).

## Hardest parts

- Size: about 30k lines. I read the main statements, definitions and proof outlines fully and treated the rest
  (IndependentVC/, the internals of Moran–Yehudayoff, MWU, Choquet, advice elimination) at the statement level.
- Working out what `MeasurableConceptClass` really assumes, and whether the README's Borel-analytic work feeds the
  headline. (It does not, see below.)
- Tracing the symmetrization path through stale comments that contradict the code.

## Calls I made (logged as asked)

- Picked 6 headlines rather than 4–7 separate PAC conjuncts. The five conjuncts are covered by `fundamental_theorem`
  plus spine nodes.
- Grouped nodes are anchored on a real declaration each (`exists_measTarget_separation`, `pac_bayes_finite`,
  `vcDim_fundamental_theorem`, `mind_change_characterization`, `advice_elimination`, `nfl_theorem_infinite`).
- `roots` = `["FLT_Proofs"]` only. Verification/ (copies of statements) and world_model/ (experiments) are excluded
  and described on the About and Trust pages.
- `ns` left empty: the main declarations are not namespaced.
- I tried an automatic pass to add file names to bare "(lines a–b)" references inside node bodies. It mis-attributed
  files, so I reverted it. Some in-body references therefore render as plain text next to a linked one. The
  Roadmap page has every reference linked.
- Engine observation (not a bug, but worth knowing): every `.py` in nodes_src/ is loaded, including `_common.py`, so
  the helper needs `NODES = []`. I followed the numina-lean-agent pattern.

## Places I am least sure of

1. **`MeasurableConceptClass` node, and the MEAS caveat on every PAC headline.** I claim `all_measurable`
   (every c : X → Bool measurable) means every subset of X is measurable, so the theorem does not cover Borel ℝⁿ.
   I'm confident of the logic (Bool has the ⊤ σ-algebra in Mathlib), and the file's own docstring (Measurability.lean
   lines 113–140) says ℝⁿ/Borel fails. But this is the strongest critical claim on the site, so it deserves a human
   check. I did not check whether `all_measurable` is actually *needed* by the proof or could be dropped.
2. **`vcdim_finite_imp_uc'`: sample size "linear in 1/δ".** Read off line 2891,
   `(16e(v+1)/ε²)^(v+1)/δ`. That is the m₀ the proof picks, not a lower limit of the method.
3. **`RademacherComplexity` junk-value argument.** I argue that the Bochner-integral-is-0 convention cannot make
   conjunct 3 vacuous, because the converse uses a finite-support distribution. I believe this, but did not read
   `rademacher_lower_bound_on_shattered` (lines 1217–1572) in detail.
4. **`exists_measTarget_separation` group.** "No PAC theorem takes `WellBehavedVCMeasTarget` as a hypothesis" is
   based on grep at the pinned commit (its only users are the Borel bridge, interpolation and amalgamation files).
5. **`LittlestoneDim` node.** "VCDim ≤ Ldim (path-wise) is only recorded as a conditional reduction". Based on
   `hasse_open_reduction` and its docstring. I checked `ExpressivityClosures.littlestoneDim_ge_vcDim`
   (ExpressivityClosures.lean lines 528–530): it is about the *branch-wise* notion, which supports the claim. A
   differently named proof could still exist somewhere in the 30k lines.
6. **`gold_theorem` modelling notes** (extensional convergence; no pause symbol). Standard observations, but my
   own.
7. Line ranges for proof sub-steps inside long proofs (e.g. Gold.lean 26–55 / 56–112 / 113–159 / 160–187 / 188–201)
   come from the section-marker comments in the proof.

## Things the author might object to

- The prominent CONDITIONAL label and caveat on the fundamental theorem about `all_measurable`. The README says
  "for a concept class C over a measurable space X" without this qualification. The project's own docstring admits the
  Borel limitation, so I think the label is fair, but it is the most visible critical point.
- Calling the sample-complexity conjunct "weak" (an ε-free lower bound, no explicit upper bound) and noting the
  docstring/statement mismatch in `pac_lower_bound`.
- Pointing out names stronger than statements (`occam_algorithm`, `baxter_full`, `ex_strictly_stronger_finite`,
  `nfl_fixed_sample`, `pac_bayes_finite` vs McAllester, `gold_does_not_imply_pac : True`), and calling
  `mind_change_characterization` near-definitional (the README does acknowledge this).
- Noting that the README's headline metrics (21,728 lines / 53 files / 354 theorems) are out of date relative to the
  pinned tree (about 29,900 lines / 102 files).
- Pointing out stale "sorry" comments. That is meant to *support* the 0-sorry claim, but it could read as criticism.
- I did not evaluate the README's methodological claims (typed premise, AI-driven proof search, ablation numbers) and
  say so on the About page.
- Licence: Apache-2.0 LICENSE file present and matching. Short quotes only, attributed, and the citation request is
  reproduced on the About page.
