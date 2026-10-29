# Roadmap: the proof in dependency order

The route is Kleiner's harmonic-function proof as presented by Tao, with Theorem numbers from the "Vikman" thesis
that the code comments follow. Each item links to its explainer node and to the exact lines at the pinned commit.

## 0. The statement and the setting

1. **The target.** [gromov_forward](#/node/FormalConjecturesCheck.gromov_forward) states the theorem: polynomial
   growth ⇒ virtually nilpotent (Gromov/FormalConjecturesCheck.lean lines 152–181). The definitions are
   [HasPolynomialGrowth](#/node/FormalConjecturesCheck.HasPolynomialGrowth),
   [GrowthFunction](#/node/FormalConjecturesCheck.GrowthFunction) and
   [CayleyBall](#/node/FormalConjecturesCheck.CayleyBall).
2. **The bridge.** Finite groups are handled directly. Otherwise use *S* ∪ *S*⁻¹ ∪ {1}
   ([normGen](#/node/FormalConjecturesCheck.normGen)), whose powers are the Cayley balls
   ([coe_normGen_pow](#/node/FormalConjecturesCheck.coe_normGen_pow), Gromov/FormalConjecturesCheck.lean
   lines 95–140).
3. **The setting.** [Generates](#/node/Generates) (Gromov/Defs/WordMetric.lean lines 36–48): an infinite group, a
   symmetric generating set *S* ∋ 1, and polynomial growth
   ([HasPolynomialGrowthD](#/node/HasPolynomialGrowthD), line 28). The [word metric](#/node/WordDist) is defined at
   line 144.
4. **The induction.** [main_gromov_theorem](#/node/main_gromov_theorem) inducts on the growth degree
   (Gromov/Gromov.lean lines 996–1024). Degree 0 means finite ([finite_of_growth_zero](#/node/finite_of_growth_zero),
   Gromov/GrowthZero.lean lines 432–579). Degree *d* ≥ 1 needs steps A–C below.

## A. Harmonic functions (analysis)

5. **Definitions.** [Harmonic](#/node/Harmonic) (Gromov/Defs/LipschitzH.lean line 31),
   [LipschitzH](#/node/LipschitzH) (lines 32–38), [constants](#/node/ConstLipschitzH) (lines 97–109), and the step
   distribution [μ](#/node/mu) (Gromov/Defs/Convolution.lean lines 51–53).
6. **Existence (Theorem 3.6).** [exists_nontrivial_harmonic](#/node/exists_nontrivial_harmonic)
   (Gromov/Harmonic.lean lines 439–447). There is a non-constant Lipschitz harmonic function. Case 1 uses the
   ℓ² Laplacian and the [energy identity](#/node/proposition_3_18) (Gromov/Harmonic/Proposition318.lean
   lines 386–597; Gromov/Harmonic/CaseOne.lean lines 35–713). Case 2 is Gromov/Harmonic.lean lines 36–433.
7. **Poincaré inequality (Theorem 3.20).** [poincare_inequality](#/node/poincare_inequality) (Gromov/Poincare.lean
   lines 244–580). There is also a reverse "*R*²" inequality for harmonic functions (Gromov/HarmonicR2.lean
   lines 31–368).
8. **Dimension bound (Theorem 3.23).** [theorem_3_23](#/node/theorem_3_23) (Gromov/Theorem323.lean lines 34–286), via
   scale selection, packing (Gromov/Packing.lean) and the determinant estimate `lemma_3_26_a`
   (Gromov/Lemma326.lean lines 66–281).
9. **Finite dimensionality (Theorem 3.19).** [Lipschitz_finite_dimensional](#/node/Lipschitz_finite_dimensional)
   (Gromov/Theorem323.lean lines 294–465).

## B. The representation and compact groups

10. **The action.** [GRep](#/node/GRep) (Gromov/Representation.lean lines 127–152). *G* acts on *W* =
    LipschitzH / constants by right translation, and preserves the norm (lines 173–231, 310–313). Its image is
    [rho_g](#/node/rho_g) (lines 320–323).
11. **Unitarian trick.** [new_weyl_unitarian_trick](#/node/new_weyl_unitarian_trick)
    (Gromov/Unitary/WeylTrick.lean lines 28–354): a compact linear group embeds in U(*n*).
12. **Compact groups of polynomial growth.** [compact_lie_virtually_abelian](#/node/compact_lie_virtually_abelian)
    (Gromov/UnitaryGromov.lean lines 28–438), using [SPolyData](#/node/SPolyData) and the centrally trivial case
    (Gromov/Unitary/CentralTrivial.lean lines 208–960). The real form via complexification is
    [theorem_3_8_real](#/node/theorem_3_8_real) (Gromov/Theorem38.lean lines 277–303).
13. **The image is virtually abelian.** [rho_g_contains_abelian](#/node/rho_g_contains_abelian)
    (Gromov/RhoAbelian.lean lines 40–621).
14. **A map onto ℤ.** [exists_theorem_3_1_input](#/node/exists_theorem_3_1_input) (Gromov/Theorem31Input.lean
    lines 342–345) produces a [Theorem3_1_Input](#/node/Theorem3_1_Input). If the image is infinite, use step 13
    (Gromov/RhoAbelian.lean lines 775–803). If it is finite, the kernel acts by adding constants, which gives a
    homomorphism to ℝ (Gromov/Theorem31Input.lean lines 63–341).

## C. The inductive step (algebra)

15. **Kernel is finitely generated** (Milnor's lemma). [three_two_ker_fg](#/node/three_two_ker_fg)
    (Gromov/ThreeTwoGenerates.lean lines 918–932).
16. **Kernel has degree *d* − 1.** [three_two_kernel_poly_growth](#/node/three_two_kernel_poly_growth)
    (Gromov/GrowthZero.lean lines 159–416), so the induction hypothesis applies to it.
17. **Eigenvalues on the unit circle.**
    [int_matrix_poly_growth_eigenvalue](#/node/int_matrix_poly_growth_eigenvalue) (Gromov/MatrixSubsum.lean
    lines 26–145), then Kronecker: [int_matrix_unipotent](#/node/int_matrix_unipotent) (lines 269–518).
18. **A power of γ acts unipotently.** [exists_gamma_n_unipotent_N'](#/node/exists_gamma_n_unipotent_N')
    (Gromov/Unipotent/GammaN.lean lines 645–842).
19. **Nilpotent extension.** [unipotent_commutator_trivial](#/node/unipotent_commutator_trivial)
    (Gromov/UnipotentGromov.lean lines 224–594).
20. **Assemble.** [theorem_3_1](#/node/theorem_3_1.) (Gromov/Gromov.lean lines 44–989). The kernel is virtually
    nilpotent by induction. A characteristic nilpotent finite-index subgroup *N'* together with γ<sup>α</sup>
    generates a nilpotent finite-index subgroup of *G*.
