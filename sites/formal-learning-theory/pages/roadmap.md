# Roadmap: the fundamental theorem, in dependency order

This is an outline of the proof of [fundamental_theorem](#/node/fundamental_theorem) (Theorem/PAC.lean lines
293–329), from the definitions up. Each step names the Lean declaration and its exact lines. Steps marked ★ have their
own explainer node. Nothing on this path contains `sorry` (see [Trust](#/trust)). The Lean was not built for this site.

## A. Definitions (the statement set)

1. ★ [Concept](#/node/Concept) and [ConceptClass](#/node/ConceptClass): functions X → Bool and sets of them
   (Basic.lean lines 37 and 46).
2. ★ [BatchLearner](#/node/BatchLearner): sample ↦ hypothesis (Learner/Core.lean lines 29–35).
3. ★ [PACLearnable](#/node/PACLearnable): realizable, distribution-free, i.i.d. product measure (Criterion/PAC.lean
   lines 55–68).
4. ★ [Shatters](#/node/Shatters), [VCDim](#/node/VCDim), [GrowthFunction](#/node/GrowthFunction)
   (Complexity/VCDimension.lean lines 22–41).
5. ★ [WellBehavedVC](#/node/WellBehavedVC) (Complexity/Symmetrization.lean lines 1005–1013) and
   ★ [MeasurableConceptClass](#/node/MeasurableConceptClass) (Complexity/Measurability.lean lines 60–67): the
   assumptions. **Read the second one carefully.**
6. ★ [HasUniformConvergence](#/node/HasUniformConvergence) (Complexity/Generalization.lean lines 811–822): the
   bridge notion, used in the proof but not in the statement.
7. ★ [RademacherComplexity](#/node/RademacherComplexity) (Complexity/Rademacher.lean lines 206–252),
   ★ [SampleComplexity](#/node/SampleComplexity) (Complexity/Generalization.lean lines 35–44),
   ★ [CompressionSchemeWithInfo](#/node/CompressionSchemeWithInfo) (Complexity/Structures.lean lines 215–249).

## B. Conjunct 1, hard direction: finite VC ⟹ PAC

8. **Sauer–Shelah.** `vcdim_finite_imp_growth_bounded` (Complexity/Generalization.lean lines 648–767) gives
   VCDim = d ⟹ GrowthFunction(m) ≤ Σ_{i≤d} (m choose i) for m ≥ d, by restricting C to each m-point set and applying
   Mathlib's `card_shatterer_le_sum_vcDim`. (The finite-family version `sauer_shelah_quantitative` goes through the
   bridge `growth_function_le_sauer_shelah`, Bridge.lean lines 465–483.)
9. **Hoeffding, one-sided** for a single hypothesis: `hoeffding_one_sided` (Complexity/Symmetrization.lean lines
   100–427) and `hoeffding_one_sided_upper` (Complexity/Symmetrization.lean lines 1825–1944).
10. **Exchangeability with null-measurable events.** `finite_exchangeability_bound` (Complexity/Symmetrization.lean lines 958–1001), used by
    `exchangeability_chain_bound` (Complexity/Symmetrization.lean lines 1030–1573; ignore the stale "contains 2 sorrys" comment above it).
11. **Double-sample (ghost) bound.** `double_sample_pattern_bound` (Complexity/Symmetrization.lean lines 1671–1817): bad ghost-sample events are
    controlled by the number of labellings on 2m points.
12. **Symmetrization steps.** `symmetrization_step` (Complexity/Symmetrization.lean lines 506–697) and its mirror `symmetrization_step_lower` (Complexity/Symmetrization.lean lines 1950–2121):
    P(∃ h with a true-vs-empirical gap ≥ ε) ≤ 2 · P(∃ h with a gap ≥ ε/2 between the sample and the ghost sample).
13. **The uniform convergence tail bound.** `symmetrization_uc_bound` (Complexity/Symmetrization.lean lines 2170–2284):
    P(∃ h ∈ C, |true − empirical| ≥ ε) ≤ 4 · GrowthFunction(2m) · exp(−mε²/8).
14. **Arithmetic.** `growth_exp_le_delta` (Complexity/Symmetrization.lean lines 2321–2616): with m ≥ (16e(v+1)/ε²)^(v+1)/δ the right side is ≤ δ.
    `uc_bad_event_le_delta_proved` (Complexity/Symmetrization.lean lines 2628–2659) combines 13 and 14.
15. ★ [vcdim_finite_imp_uc'](#/node/vcdim_finite_imp_uc') (Complexity/Symmetrization.lean lines 2665–2935): finite VC ⟹ uniform convergence (a
    direct union bound when X is finite; steps 8–14 when X is infinite).
16. ★ [uc_imp_pac](#/node/uc_imp_pac) (Complexity/Generalization.lean lines 848–944): uniform convergence ⟹ PAC,
    via a consistent learner.
17. `vcdim_finite_imp_pac` (Theorem/PAC.lean lines 74–88): steps 15 + 16, plus the empty-class case.

## C. Conjunct 1, easy direction: PAC ⟹ finite VC

18. **Counting core.** `nfl_counting_core` (Complexity/Generalization.lean lines 1331–1462): on a shattered set of
    size > 2m, some labelling makes any learner fail on at least half of the samples.
19. ★ [vcdim_infinite_not_pac](#/node/vcdim_infinite_not_pac) (Complexity/Generalization.lean lines 2777–3054): the counting core plus the
    uniform-measure bridge.
20. `pac_imp_vcdim_finite` (Theorem/PAC.lean lines 106–113), then ★ [vc_characterization](#/node/vc_characterization)
    (Theorem/PAC.lean lines 127–132).

## D. Conjunct 2: compression (independent of B and C)

21. `vcdim_finite_imp_proper_finite_support_learner` (Complexity/Compression.lean lines 189–305): a proper learner
    for distributions supported on the sample, from VC + Sauer–Shelah.
22. **Approximate minimax by multiplicative weights**: `mwu_approx_minimax` (PureMath/ApproxMinimax.lean lines
    597–638).
23. **Sparse approximation**: `finite_support_vc_approx` (Complexity/FiniteSupportUC.lean lines 97–426) and the
    Assouad dual bound `BinaryMatrix.assouad_transpose_vcDim` (PureMath/BinaryMatrix.lean lines 231–257).
24. **Packaging**: `finalizeIncidenceScheme` (Complexity/Compression.lean lines 748–770) and
    `moran_yehudayoff_forward_construction` (Complexity/Compression.lean lines 805–1105).
25. `vcdim_finite_imp_compression_with_info` (Complexity/Compression.lean lines 1120–1143); the converse by pigeonhole,
    `compression_with_info_imp_vcdim_finite` (Complexity/Compression.lean lines 1214–1317); together ★
    [fundamental_vc_compression_with_info](#/node/fundamental_vc_compression_with_info) (Complexity/Compression.lean lines 1321–1326).

## E. Conjunct 3: Rademacher complexity

26. **Massart's finite-class lemma**: `finite_massart_lemma` (Complexity/Rademacher.lean lines 507–676).
27. `vcdim_bounds_rademacher_quantitative` (Complexity/Rademacher.lean lines 930–1180): Rad ≤ √(2d·log(em/d)/m).
28. `vcdim_finite_imp_rademacher_vanishing` (Complexity/Rademacher.lean lines 1817–1900), and the converse witness
    `rademacher_lower_bound_on_shattered` (Complexity/Rademacher.lean lines 1217–1572).
29. ★ [fundamental_rademacher](#/node/fundamental_rademacher) (Theorem/PAC.lean lines 261–290), which reuses steps 17
    and 20.

## F. Conjunct 4: the sample-complexity sandwich

30. `pac_lower_bound_member` (Complexity/Generalization.lean lines 2274–2586) and `sample_complexity_lower_bound`
    (Complexity/GeneralizationResults.lean lines 230–257): ⌈(d − 1)/2⌉ lower bound.
31. `sample_complexity_upper_of_pac_witness` (Theorem/PAC.lean lines 190–207), then ★
    [pac_sample_complexity_sandwich](#/node/pac_sample_complexity_sandwich) (Theorem/PAC.lean lines 212–246).

## G. Conjunct 5 and assembly

32. `growth_bounded_imp_vcdim_finite` (Complexity/Generalization.lean lines 2190–2259), the converse of step 8.
33. ★ [fundamental_theorem](#/node/fundamental_theorem) (Theorem/PAC.lean lines 293–329): the five conjuncts from
    steps 20, 25, 29, 31 and 8 + 32.

## The other headlines

- ★ [littlestone_characterization](#/node/littlestone_characterization): `adversary_core` (Complexity/GameInfra.lean
  lines 95–122) → `forward_direction` (Theorem/Online.lean lines 27–49); ★ [SOA](#/node/SOA)
  (Complexity/GameInfra.lean lines 151–158) → `soa_mistakes_bounded` (Theorem/Online.lean lines 322–386) →
  `backward_direction` (Theorem/Online.lean lines 389–413).
- ★ [gold_theorem](#/node/gold_theorem) (Theorem/Gold.lean lines 19–201): self-contained.
- ★ [online_pac_gold_separation](#/node/online_pac_gold_separation) (Theorem/Separation.lean lines 1358–1363): uses
  step 15 (via `vcdim_finite_imp_pac_via_uc'`), step 19 and the Littlestone forward direction.
