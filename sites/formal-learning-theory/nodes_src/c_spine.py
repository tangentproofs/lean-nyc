import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import node_maker, q, walk, S, NOT_BUILT, MEAS

NODES = []
node = node_maker(NODES)


node("vcdim_finite_imp_uc'",
 "Key lemma: finite VC dimension ⟹ uniform convergence",
 "Finite VC dimension (plus the measurability assumptions) gives uniform convergence. Finite domain: Hoeffding and a "
 "union bound. Infinite domain: Sauer–Shelah, then symmetrization with a ghost sample, then Hoeffding, at sample size "
 "about (16e(d+1)/ε²)^(d+1)/δ.",
 r"""## Plain English

**Theorem (`vcdim_finite_imp_uc'`, Complexity/Symmetrization.lean lines 2665–2935).** If VCDim X C < ⊤, every
concept in C is measurable, every Bool-valued function on X is measurable, and [WellBehavedVC](#/node/WellBehavedVC)
X C, then [HasUniformConvergence](#/node/HasUniformConvergence) X C.

(The prime distinguishes it from an older unprimed `vcdim_finite_imp_uc` in Complexity/Generalization.lean.)

**A stale comment to be aware of.** Lines 1015–1028 describe `exchangeability_chain_bound` (lines 1030–1573) as
"ORPHANED — contains 2 sorrys" and say the critical path avoids it. In the pinned source that lemma has no `sorry`
(it now goes through `finite_exchangeability_bound`, lines 958–1001), and it **is** on this lemma's path:
`symmetrization_uc_bound` calls `double_sample_pattern_bound` (lines 1671–1817), which calls it. So the comment is
out of date on both counts. A comment-aware search finds no `sorry` in code anywhere in FLT_Proofs/.

### Two branches

- **Finite X** (lines 2670–2867). C is then a finite set of functions. Apply one-sided Hoeffding bounds to each
  h ∈ C, then a union bound: P(some h is ε-off) ≤ |C| · 2 · exp(−2mε²). Pick m ≥ log(2|C|/δ)/(2ε²).
- **Infinite X** (lines 2868–2935), the textbook route:
  1. **Sauer–Shelah** (`vcdim_finite_imp_growth_bounded`): the [growth function](#/node/GrowthFunction) is at most
     Σ_{i ≤ v} (n choose i) for n ≥ v.
  2. **Symmetrization** (`symmetrization_uc_bound`, lines 2170–2284): with a ghost sample S′, the probability that
     some h ∈ C has |true − empirical error| ≥ ε is at most 4 · π_C(2m) · exp(−mε²/8). This is where the
     null-measurability of the double-sample bad event is used.
  3. **Arithmetic** (`growth_exp_le_delta`, lines 2321–2616): if m ≥ (16e(v+1)/ε²)^(v+1)/δ, that bound is ≤ δ.
  4. **Complement** (lines 2905–2935): the good event has probability ≥ 1 − δ.

### How good is the sample size?

The m₀ chosen at line 2891 is (16e(v+1)/ε²)^(v+1)/δ: polynomial in 1/ε (degree about 2(d+1)) and **linear in 1/δ**.
The textbook uniform convergence bound is O((d log(1/ε) + log(1/δ))/ε²). Since the PAC definition only asks for
*some* sample size, this is enough for the qualitative theorem, but it is far from the classical rate.
""",
 [q("What is the role of the 'ghost sample' in the infinite-domain branch?",
    ["It replaces the true error by the error on a second independent sample, so that only finitely many labellings (the growth function at 2m) matter",
     "It is a validation set for the learner",
     "It makes the domain finite",
     "It removes the need for Hoeffding's inequality"], 0,
    "`symmetrization_uc_bound` (Complexity/Symmetrization.lean lines 2170–2189) bounds the bad event by 4 · GrowthFunction(2m) · exp(−mε²/8)."),
  q("How does the chosen sample size depend on the confidence δ?",
    ["Linearly in 1/δ: m ≈ (16e(v+1)/ε²)^(v+1)/δ",
     "Like log(1/δ)",
     "It does not depend on δ",
     "Like 1/δ²"], 0,
    "Line 2891: `use Nat.ceil ((16 * Real.exp 1 * (↑v + 1) / ε ^ 2) ^ (v + 1) / δ)`."),
  q("Where is WellBehavedVC used?",
    ["To make the double-sample bad event null-measurable so symmetrization can integrate over it",
     "To make the learner measurable",
     "In the finite-X branch only",
     "Nowhere; it is unused"], 0,
    "Line 2902: `have hE_nullmeas := hWB D c m ε`, passed to `uc_bad_event_le_delta_proved`."),
 ],
 caveats=[NOT_BUILT,
  "The explicit hypotheses (hmeas_C, hc_meas, hWB) are the three fields of MeasurableConceptClass; in particular "
  "`hc_meas` asks every Bool-valued function on X to be measurable."],
 widgets=walk("How the proof goes (Complexity/Symmetrization.lean, lines 2665-2935)", [
   S("Split on whether X is finite.", None, "rcases finite_or_infinite X with hfin | hinf"),
   S("Finite X: C is finite; Hoeffding for each h plus a union bound, with m₀ ≈ log(2N/δ)/(2ε²).", None,
     "use max 1 (Nat.ceil ((Real.log (2 * ↑N / δ)) / (2 * ε' ^ 2)))"),
   S("Infinite X: Sauer–Shelah bounds the growth function polynomially.", "GrowthFunction",
     "obtain ⟨v₀, hv₀⟩ := vcdim_finite_imp_growth_bounded X C hC'"),
   S("Choose the sample size, polynomial in 1/ε and linear in 1/δ.", None,
     "use Nat.ceil ((16 * Real.exp 1 * (↑v + 1) / ε ^ 2) ^ (v + 1) / δ)"),
   S("Use WellBehavedVC to get null-measurability of the ghost-sample bad event.", "WellBehavedVC",
     "have hE_nullmeas := hWB D c m ε"),
   S("Symmetrization + Hoeffding + arithmetic: the bad event has probability ≤ δ.", None,
     "have h_ub := uc_bad_event_le_delta_proved D C c hmeas_C (hc_meas c) m hm_pos ε δ hε hδ hδ1"),
   S("Pass to the complement: the good event has probability ≥ 1 − δ.", "HasUniformConvergence"),
 ]))


node("uc_imp_pac",
 "Key lemma: uniform convergence ⟹ PAC (via a consistent learner)",
 "If C is nonempty and has uniform convergence, then the learner 'output some h ∈ C consistent with the sample' is a "
 "PAC learner. A consistent h has empirical error 0, so uniform convergence makes its true error < ε. No measurability "
 "is needed for this step.",
 r"""## Plain English

**Theorem (`uc_imp_pac`, Complexity/Generalization.lean lines 848–944).** If C is nonempty and
[HasUniformConvergence](#/node/HasUniformConvergence) X C, then [PACLearnable](#/node/PACLearnable) X C.

1. **The learner** (lines 855–872). Given a sample S, if some h₀ ∈ C agrees with every label of S, output one
   (chosen with `Classical.choice`). Otherwise output a fixed element of C. This is a consistent learner (an ERM
   learner in the realizable case), and it is proper: it always outputs an element of C.
2. **The sample size** (lines 876–880). mf(ε, δ) is the m₀ that uniform convergence provides for (ε, δ).
3. **The good event contains the success event** (lines 896–944). On a sample where every h ∈ C has
   |true − empirical error| < ε, look at h₀ = the learner's output. Since the target c ∈ C labels S, h₀ is
   consistent, so its empirical error is 0, and its true error is < ε.
4. Measure monotonicity (`OuterMeasure.mono`, line 898) finishes: P(success) ≥ P(UC good event) ≥ 1 − δ.

Because step 4 is monotonicity of (outer) measure, this lemma needs no measurability at all.
""",
 [q("What does the learner built in uc_imp_pac output?",
    ["A concept in C consistent with the sample, if one exists; otherwise a fixed element of C",
     "The majority label",
     "The target concept itself",
     "A random concept"], 0,
    "Complexity/Generalization.lean lines 855–858."),
  q("Why is the output's empirical error zero?",
    ["The target c ∈ C labels the sample, so a consistent concept exists and the learner picks one",
     "Because the sample is empty",
     "Because ε > 0",
     "Because the learner memorizes X"], 0,
    "Lines 907–915 use `⟨c, hcC, fun i => rfl⟩` as the witness for the existential."),
  q("Does uc_imp_pac need the MeasurableConceptClass assumptions?",
    ["No: it only uses monotonicity of the product (outer) measure",
     "Yes, all three",
     "Only WellBehavedVC",
     "Only measurability of the learner"], 0,
    "The statement (lines 848–851) has only `[MeasurableSpace X]`, `C.Nonempty` and `HasUniformConvergence`."),
 ],
 caveats=[NOT_BUILT],
 widgets=walk("How the proof goes (Complexity/Generalization.lean, lines 848-944)", [
   S("Define the consistent learner (falls back to hC.some).", "BatchLearner", "if h : ∃ h₀ ∈ C, ∀ i : Fin m, h₀ (S i).1 = (S i).2"),
   S("Use the uniform convergence m₀ as the PAC sample size.", "HasUniformConvergence",
     "if hδ : 0 < δ then (hUC ε δ hε hδ).choose"),
   S("Reduce to: UC good event ⊆ PAC success event (monotonicity).", None, "apply MeasureTheory.OuterMeasure.mono"),
   S("The output is consistent with the sample because c itself is a witness.", None,
     "((fun i => (xs i, c (xs i))) i).2 := ⟨c, hcC, fun i => rfl⟩"),
   S("Empirical error 0 and |true − empirical| < ε give true error < ε.", None, "exact le_of_lt hlt"),
 ]))


node("vcdim_infinite_not_pac",
 "Key lemma: infinite VC dimension ⟹ not PAC learnable",
 "If C shatters arbitrarily large finite sets, nothing PAC learns it. Fix ε = δ = 1/4 and the sample size m. Under "
 "the uniform distribution on a shattered set of more than 2m points, counting finds a target on which the learner "
 "fails too often.",
 r"""## Plain English

**Theorem (`vcdim_infinite_not_pac`, Complexity/Generalization.lean lines 2777–3054).** If X has measurable
singletons and VCDim X C = ⊤, then C is not [PAC learnable](#/node/PACLearnable). No measurability is assumed on C.

### The argument (a no-free-lunch argument)

1. Suppose (L, mf) is a PAC witness. Set ε = δ = 1/4 and m = mf(1/4, 1/4) (lines 2790–2797).
2. Since VCDim = ⊤, pick a shattered T with |T| > 2m (line 2793).
3. Let D be the uniform distribution on T (lines 2815–2840).
4. **Counting core** (`nfl_counting_core`, lines 1331–1462). For each labelling f of T there is a target c_f ∈ C
   realizing it. For any fixed sample xs (at most m distinct points), the learner's output is the same for all f
   that agree on the sample. Pairing f with its flip on the unseen points (more than half of T), at most one of
   each pair can have error ≤ 1/4. Averaging and pigeonholing give one f₀ for which at most half of all samples
   are "good".
5. **Measure bridge** (lines 2860–3054). Translate "at most half of the |T|ᵐ samples in Tᵐ" into
   Dᵐ(good) ≤ 1/2 < 3/4, using that the product of uniform measures on T is uniform on Tᵐ.
6. That contradicts the PAC guarantee Dᵐ(good) ≥ 1 − 1/4.

The comment at lines 2843–2845 still says "Factor into two sorry'd substeps". Both substeps are now proved (lines
2853 and following), so the comment is out of date.
""",
 [q("What distribution defeats the learner?",
    ["Uniform on a shattered set with more than 2m points",
     "A point mass",
     "The empirical distribution of the sample",
     "Any distribution, as long as it is continuous"], 0,
    "Complexity/Generalization.lean lines 2793–2840."),
  q("Why must the shattered set have more than 2m points?",
    ["So that more than half of T is unseen by any sample of size m, where the learner can only guess",
     "Because the VC dimension is 2m",
     "To make the distribution uniform",
     "It is an arbitrary choice"], 0,
    "The pairing argument in `nfl_counting_core` (lines 1331–1462) uses |unseen| ≥ |T| − m > |T|/2."),
  q("Which measurability assumption on C does this direction need?",
    ["None: only measurable singletons on X",
     "MeasurableConceptClass",
     "WellBehavedVC",
     "StandardBorelSpace"], 0,
    "The statement (lines 2777–2780) has `[MeasurableSingletonClass X]` and nothing on C."),
 ],
 caveats=[NOT_BUILT,
  "Because PACLearnable uses outer measure for possibly non-measurable success sets, refuting it is (slightly) "
  "stronger than refuting a measurable version. Here the distribution is supported on a finite set, so the "
  "issue does not arise."],
 widgets=walk("How the proof goes (Complexity/Generalization.lean, lines 2777-3054)", [
   S("Assume a PAC witness (L, mf) and fix ε = δ = 1/4.", "PACLearnable", "intro ⟨L, mf, hpac⟩"),
   S("Pick a shattered set T with more than 2m points.", "Shatters",
     "obtain ⟨T, hTshat, hTcard⟩ := hvcdim_unbounded (2 * m) (WithTop.coe_lt_top _)"),
   S("Reduce to: some probability D and c ∈ C violate the guarantee.", None,
     "exact not_le.mpr hfail (hpac14 D hDprob c hcC)"),
   S("Counting core: pair labellings, pigeonhole a bad target f₀.", None,
     "obtain ⟨f₀, c₀, hc₀C, hc₀f, hcount⟩ := nfl_counting_core hTshat hTcard_nat L"),
   S("Measure bridge: under the uniform distribution on T, good samples have probability ≤ 1/2 < 3/4.", None),
 ]))


node("fundamental_rademacher",
 "Conjunct 3: PAC ⟺ uniformly vanishing Rademacher complexity",
 "C is PAC learnable exactly when, for every ε, one sample size m₀ makes the Rademacher complexity below ε for every "
 "distribution and every m ≥ m₀. One direction uses Massart's finite-class lemma plus Sauer–Shelah; the other uses "
 "a large shattered set to force Rademacher complexity ≥ 1/2.",
 r"""## Plain English

**Theorem (`fundamental_rademacher`, Theorem/PAC.lean lines 261–290).** Under
[MeasurableConceptClass](#/node/MeasurableConceptClass):

  [PACLearnable](#/node/PACLearnable) X C ⟺ ∀ ε > 0, ∃ m₀, ∀ D probability, ∀ m ≥ m₀,
  [RademacherComplexity](#/node/RademacherComplexity) X C D m < ε.

- **⟹** PAC gives VCDim < ⊤ ([pac_imp_vcdim_finite](#/node/vc_characterization)), and
  `vcdim_finite_imp_rademacher_vanishing` (Complexity/Rademacher.lean lines 1817–1900) bounds the Rademacher
  complexity by √(2d·log(em/d)/m) for VCDim = d (`vcdim_bounds_rademacher_quantitative`, lines 930–934: Massart's
  finite-class lemma plus Sauer–Shelah), which tends to 0 uniformly in D.
- **⟸** If VCDim = ⊤, take ε = 1/2 and m = max(m₀, 1), and a shattered set T with at least 4m² + 1 points.
  `rademacher_lower_bound_on_shattered` (Complexity/Rademacher.lean lines 1217–1572) gives a distribution D with
  RademacherComplexity ≥ 1/2, a contradiction. So VCDim < ⊤, and PAC follows from the uniform convergence route.

The "vanishing" is uniform over distributions (m₀ before ∀ D). The docstring calls this "the textbook-standard form".
""",
 [q("Does m₀ in the Rademacher condition depend on D?",
    ["No: ∃ m₀ comes before ∀ D",
     "Yes",
     "Only for infinite X",
     "There is no m₀"], 0,
    "Theorem/PAC.lean lines 266–268."),
  q("How large a shattered set does the converse direction use?",
    ["At least 4m² + 1 points", "m points", "2m points", "Infinitely many"], 0,
    "Theorem/PAC.lean line 287: `h_large_shatter (4 * m ^ 2 + 1)`."),
  q("Does the ⟹ direction need the measurability assumptions?",
    ["Not for the Rademacher bound itself: vcdim_finite_imp_rademacher_vanishing has only [MeasurableSpace X]",
     "Yes, all of them",
     "Only WellBehavedVC",
     "Only MeasurableSingletonClass"], 0,
    "Complexity/Rademacher.lean lines 1817–1821."),
 ],
 caveats=[NOT_BUILT, MEAS],
 widgets=walk("How the proof goes (Theorem/PAC.lean, lines 261-290)", [
   S("⟹: PAC gives finite VC, which gives vanishing Rademacher complexity.", "RademacherComplexity",
     "⟨fun hpac => vcdim_finite_imp_rademacher_vanishing X C"),
   S("⟸: suppose VCDim = ⊤; use ε = 1/2 to get m₀.", None, "obtain ⟨m₀, hm₀⟩ := hrad (1/2) (by norm_num)"),
   S("Take a shattered set with ≥ 4m² + 1 points and a distribution with Rademacher complexity ≥ 1/2.", None,
     "obtain ⟨D, hD, hRad_ge⟩ := rademacher_lower_bound_on_shattered X C T hT_shat m (by omega) hT_card"),
   S("Contradiction with < 1/2; so VCDim < ⊤, and PAC follows via uniform convergence.", "vcdim_finite_imp_uc'",
     "exact vcdim_finite_imp_pac_via_uc' X C hvcdim hmeas_C hc_meas hWB⟩"),
 ]))


node("pac_sample_complexity_sandwich",
 "Conjunct 4: a sample-complexity sandwich (weak lower bound)",
 "If C is PAC learnable via (L, mf), then SampleComplexity ≤ mf, and when VCDim = d ≥ 1 both are at least ⌈(d−1)/2⌉ "
 "(for ε ≤ 1/4, δ ≤ 1/7). The upper half is immediate from the definitions. The lower bound is linear in d but has "
 "no 1/ε factor, unlike the textbook Ω(d/ε).",
 r"""## Plain English

**Theorem (`pac_sample_complexity_sandwich`, Theorem/PAC.lean lines 212–246).** If C is PAC learnable, there are L
and mf with

1. the PAC guarantee for (L, mf);
2. [SampleComplexity](#/node/SampleComplexity)(ε, δ) ≤ mf(ε, δ) for all ε, δ > 0;
3. if VCDim = d ≥ 1, ε ≤ 1/4, 0 < δ ≤ 1/7: ⌈(d − 1)/2⌉ ≤ SampleComplexity(ε, δ) and ⌈(d − 1)/2⌉ ≤ mf(ε, δ).

Part 1 just restates the PAC witness. Part 2 is `Nat.sInf_le` (lines 190–207). Part 3 is
`sample_complexity_lower_bound` (Complexity/GeneralizationResults.lean lines 230–257), a counting argument on a
shattered set of size d, of the same kind as [vcdim_infinite_not_pac](#/node/vcdim_infinite_not_pac).

### Faithfulness

The README calls this a "quantitative sandwich". It is a real but weak statement. The classical bounds are
Ω((d + log(1/δ))/ε) ≤ m_C(ε, δ) ≤ O((d log(1/ε) + log(1/δ))/ε). Here:

- the lower bound has no ε (it is the bound at ε = 1/4 reused for all smaller ε);
- the upper bound is "≤ whatever witness you started from", with no formula in d, ε, δ. The witness built by the
  library has sample size polynomial in 1/ε and linear in 1/δ (see [vcdim_finite_imp_uc'](#/node/vcdim_finite_imp_uc')).

The docstring of `pac_lower_bound` (Theorem/PAC.lean lines 159–172) mentions the (d − 1)/(64ε) bound and the tight
(d − 1)/(2ε) of Ehrenfeucht–Haussler–Kearns–Valiant (1989), but the proved statement is ⌈(d − 1)/2⌉.
""",
 [q("What does part 2 (SampleComplexity ≤ mf) rest on?",
    ["Just the definition of SampleComplexity as an infimum (Nat.sInf_le)",
     "A Chernoff bound",
     "Sauer–Shelah",
     "The compression theorem"], 0,
    "Theorem/PAC.lean lines 204–207."),
  q("How does the proved lower bound compare with the classical Ω(d/ε)?",
    ["It drops the 1/ε factor: ⌈(d − 1)/2⌉ for every ε ≤ 1/4",
     "It is the same",
     "It is stronger",
     "It has an extra log factor"], 0,
    "Theorem/PAC.lean lines 228–232."),
  q("Does the theorem give an explicit upper bound on the sample complexity in terms of d, ε, δ?",
    ["No: only SampleComplexity ≤ mf for the witness's own mf",
     "Yes, O(d/ε · log(1/δ))",
     "Yes, (d+1)/ε",
     "Yes, 2^d"], 0,
    "Part 2 (lines 226–227) mentions only mf."),
 ],
 caveats=[NOT_BUILT, MEAS],
 widgets=walk("How the proof goes (Theorem/PAC.lean, lines 212-246)", [
   S("Take the PAC witness (L, mf).", "PACLearnable", "rcases hPAC with ⟨L, mf, hmf⟩"),
   S("Upper bound: SampleComplexity is an infimum, so it is ≤ any working sample size.", "SampleComplexity",
     "exact sample_complexity_upper_of_pac_witness X C L mf hmf ε δ hε hδ"),
   S("Lower bound for SampleComplexity from the counting argument on a shattered set of size d.", None,
     "sample_complexity_lower_bound X C d hd ε δ hε hε1 hδ hδ1 hδ2 hd_pos hmeas_C hc_meas hWB"),
   S("Chain the two to bound mf below as well.", None, "exact ⟨hlower, le_trans hlower hupper⟩"),
 ]))
