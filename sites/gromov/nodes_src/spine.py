NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

SKIM = "Outlined from the statement, the case structure and the comments; the proof body was not read line by line for this site."


# ---------------------------------------------------------------- the representation

node("GRep",
 "GRep: G acts on Lipschitz harmonic functions",
 "G acts on Lipschitz harmonic functions by right translation, f ↦ f(· g). The action preserves the Lipschitz "
 "seminorm, so on W = LipschitzH / constants it is an action by isometries of a finite-dimensional normed space.",
 r"""## Plain English

**Definition (`GRep`, Gromov/Representation.lean lines 127–152).** For *g* ∈ *G*, the map
*f* ↦ (*x* ↦ *f*(*x*·*g*)) (`gAct`, Gromov/Defs.lean lines 94–115) sends [Lipschitz harmonic](#/node/LipschitzH)
functions to Lipschitz harmonic functions. Harmonicity averages over *left* multiples, and the
[word metric](#/node/WordDist) is right-invariant. Together these maps form a linear representation of *G* on
LipschitzH.

The construction then continues:

* constants are fixed, so the action passes to the quotient *W* (`GRepW_non_invertible`, lines 153–168);
* it becomes a homomorphism into the invertible linear maps of *W* (`GRepW_base`, lines 169–172);
* right translation preserves the Lipschitz seminorm (`GRep_preserves_norm`, lines 173–231), so each *g* acts on *W*
  with operator norm at most 1 (`GRepW_norm_le`, lines 310–313).

The image of *G* is the group [rho_g](#/node/rho_g). By
[Lipschitz_finite_dimensional](#/node/Lipschitz_finite_dimensional), *W* is finite-dimensional, so this is a
finite-dimensional representation by isometries. In Tao's outline it is "the representation of *G* on harmonic
functions modulo constants".
""",
 [q("How does g act on a function f?",
    ["By right translation: x ↦ f(x·g)", "By left translation: x ↦ f(g·x)", "By multiplying f by g"], 0,
    "gAct, Gromov/Defs.lean lines 94–98."),
  q("Why does the action preserve harmonicity?",
    ["Harmonicity averages over left multiples s·x, which commute with right translation",
     "Because every function is harmonic", "Because G is abelian"], 0,
    "The proof in Gromov/Defs.lean lines 106–115 just reassociates (s·x)·g = s·(x·g)."),
  q("What does the norm-preservation give?",
    ["The image of G lies in a bounded, hence relatively compact, group of linear maps of W",
     "The image of G is finite", "The representation is irreducible"], 0,
    "This is what lets rho_g_contains_abelian use a compact group."),
 ])


node("rho_g",
 "rho_g: the image of G in GL(W)",
 "rho_g is the image of G inside the invertible linear maps of W. The case split 'finite or infinite image' is how "
 "the proof finds a map onto ℤ.",
 r"""## Plain English

**Definition (`rho_g`, Gromov/Representation.lean lines 320–323).** The range of the homomorphism `GRepW_base` from
*G* to the invertible linear maps of *W* (see [GRep](#/node/GRep)). It is finitely generated (`rho_g_FG`,
Gromov/Theorem38.lean lines 202–207), being the image of a finitely generated group.

[exists_theorem_3_1_input](#/node/exists_theorem_3_1_input) splits on whether rho_g is finite.
""",
 [q("Why is rho_g finitely generated?",
    ["It is a homomorphic image of the finitely generated group G", "Because W is finite-dimensional",
     "It is finite"], 0,
    "Gromov/Theorem38.lean lines 202–207."),
 ])


node("exists_theorem_3_1_input",
 "A finite-index subgroup mapping onto ℤ exists",
 "Every infinite group of polynomial growth has a finite-index subgroup with a surjection onto ℤ. If the image of G "
 "in GL(W) is infinite, it comes from the compact-group step. If the image is finite, it comes directly from harmonic functions.",
 r"""## Plain English

**Theorem (`exists_theorem_3_1_input`, Gromov/Theorem31Input.lean lines 342–345).** Under
[Generates](#/node/Generates), if *S* has growth degree *d*, there is a
[Theorem3_1_Input](#/node/Theorem3_1_Input): a finite-index subgroup with a surjective homomorphism onto ℤ.

This is "Case 1 / Case 2 of Section 3.3" in the comments. It is the bridge from analysis to algebra.

* **Infinite image** (`rho_g_case_infinite`, Gromov/RhoAbelian.lean lines 775–803). By
  [rho_g_contains_abelian](#/node/rho_g_contains_abelian), [rho_g](#/node/rho_g) has an abelian subgroup *H* of finite
  index. *H* is infinite and finitely generated, and an infinite finitely generated abelian group maps onto ℤ. Pull
  back along *G* → rho_g (`g_hom_abelian`, lines 635–771).
* **Finite image** (`rho_g_case_finite`, Gromov/Theorem31Input.lean lines 63–341). The kernel *G'* of
  *G* → GL(*W*) has finite index and acts trivially on *W*. So for each Lipschitz harmonic *f*, the difference
  *f*(*x*·*g*) − *f*(*x*) is a constant λ<sub>*g*</sub>(*f*) for *g* ∈ *G'* (lines 88–125). The map
  *g* ↦ λ<sub>*g*</sub> is a homomorphism from *G'* to an abelian group of linear functionals (lines 131 onward). It
  is non-zero because a [non-constant harmonic function exists](#/node/exists_nontrivial_harmonic). Its image is a
  non-trivial, finitely generated, torsion-free abelian group, which maps onto ℤ.
""",
 [q("Where does the non-constant harmonic function enter?",
    ["In the finite-image case, to show the homomorphism g ↦ λ_g is non-zero",
     "Only in the infinite-image case", "It is not used"], 0,
    "rho_g_case_finite uses exists_nontrivial_harmonic. In the infinite case it is the dimension of W that matters."),
  q("What does the infinite-image case rely on?",
    ["The image has a finite-index abelian subgroup (the compact-group step)",
     "The image is cyclic", "The image is nilpotent by induction"], 0,
    "rho_g_case_infinite calls rho_g_contains_abelian (Gromov/RhoAbelian.lean line 776)."),
 ],
 caveats=["The description of the finite-image case is from the proof's let/have structure (lines 66–131) and "
          "comments, plus the classical argument. " + SKIM])


node("rho_g_contains_abelian",
 "The image of G is virtually abelian",
 "Because G acts on finite-dimensional W by isometries, its image sits inside a compact linear group. The compact-group "
 "step then gives the image an abelian subgroup of finite index.",
 r"""## Plain English

**Theorem (`rho_g_contains_abelian`, Gromov/RhoAbelian.lean lines 40–621).** If *S* has growth degree *d*, then
[rho_g](#/node/rho_g) has an abelian subgroup of finite index.

The proof is mostly plumbing:

* give the finite-dimensional space *W* an inner product, by transporting the Euclidean one (lines 43–75);
* the image of *G* preserves the Lipschitz norm on *W* ([GRep](#/node/GRep)), so its closure in the invertible maps is
  **compact** (lines 288–433);
* growth data passes to the image (lines 451–453);
* apply [theorem_3_8_real](#/node/theorem_3_8_real) to the image inside that compact group (line 456);
* pull the abelian subgroup back to rho_g (lines 459–621).
""",
 [q("Why is the closure of the image compact?",
    ["Its elements have operator norm ≤ 1 on a finite-dimensional space, so the closure is closed and bounded",
     "Because G is finite", "Because W is one-dimensional"], 0,
    "See GRepW_norm_le and Gromov/RhoAbelian.lean lines 288–433."),
 ],
 caveats=[SKIM])


# ---------------------------------------------------------------- compact groups

node("theorem_3_8_real",
 "Theorem 3.8: compact linear groups (real version)",
 "A finitely generated subgroup of polynomial growth inside a compact group of invertible linear maps of a real "
 "inner product space is virtually abelian. It is reduced to the complex unitary case.",
 r"""## Plain English

**Theorem (`theorem_3_8_real`, Gromov/Theorem38.lean lines 277–303).** Let *V* be a finite-dimensional real inner
product space and *H* a compact group of invertible continuous linear maps of *V*. If Γ ⊆ *H* is finitely
generated with [growth data](#/node/SPolyData), then Γ has an abelian subgroup of finite index.

The proof complexifies *V* (Gromov/Complexification.lean) and applies the complex version `theorem_3_8`
(Gromov/Theorem38.lean lines 38–201). That version uses the [unitarian trick](#/node/new_weyl_unitarian_trick) to
identify *H* with a subgroup of U(*n*), and then applies
[compact_lie_virtually_abelian](#/node/compact_lie_virtually_abelian).
""",
 [q("What does complexification buy?",
    ["It lets the real representation use the complex unitary-group machinery",
     "It makes the group abelian", "It reduces the dimension"], 0,
    "Gromov/Complexification.lean lines 1–20 explain the purpose."),
 ])


node("new_weyl_unitarian_trick",
 "The unitarian trick",
 "A compact group of invertible complex linear maps is isomorphic to a subgroup of U(n), by averaging an inner product "
 "over the group.",
 r"""## Plain English

**Theorem (`new_weyl_unitarian_trick`, Gromov/Unitary/WeylTrick.lean lines 28–354).** If *H* is a compact (and
locally compact) group of invertible linear maps of a finite-dimensional complex inner product space *V*, then *H* is
isomorphic, as a group, to a subgroup of the unitary group U(*n*), *n* = dim *V*.

This is Weyl's classical trick. Average the inner product ⟨*hv*, *hw*⟩ over *h* ∈ *H* using Haar measure (lines
29–31 set up the integrand). Every element of *H* preserves the averaged inner product, so in an orthonormal basis for
it, *H* becomes a group of unitary matrices.
""",
 [q("Why must H be compact?",
    ["So that its Haar measure is finite and the average exists", "So that H is finite", "So that H is abelian"], 0,
    "A finite Haar measure is what makes the averaged inner product well defined."),
 ],
 caveats=["The statement only gives an abstract group isomorphism with a subgroup of U(n). Classically it is conjugation "
          "by a fixed matrix, which is stronger, but the isomorphism is all the next step needs."])


# ---------------------------------------------------------------- finite dimensionality

node("theorem_3_23",
 "Theorem 3.23: dimension bound for slowly growing subspaces",
 "There is a constant C (depending on the degree d) such that every finite-dimensional space of Lipschitz harmonic "
 "functions whose Gram determinants on balls grow slowly enough has dimension below C.",
 r"""## Plain English

**Theorem (`theorem_3_23`, Gromov/Theorem323.lean lines 34–286).** For each *d* > 0 there is a natural number *C*.
Let *V* be any finite-dimensional, non-trivial, even-dimensional subspace of [LipschitzH](#/node/LipschitzH) (the
`V_Wrapper` class, Gromov/VWrapper.lean lines 43–48). If *V* satisfies the "growth bound" of degree *d*, then
dim *V* < *C*.

Write *Q<sub>R</sub>*(*u*, *v*) for Σ *u*(*g*)*v*(*g*) over the ball of radius *R* (Gromov/QuadraticForm.lean
line 30). The growth bound (line 107) says that

|*S<sup>R</sup>*| · det(*Q<sub>R</sub>* on a basis of *V*)<sup>1/dim *V*</sup> / *R<sup>d</sup>* → 0.

The proof is Kleiner's scale-selection argument:

* pick a scale where the growth is almost multiplicative (Gromov/VWrapper.lean, `lemma_3_24`, lines 307 onward);
* cover a ball by small balls ([packing](#/node/poincare_inequality), Gromov/Packing.lean);
* on each small ball, control *u* by its average plus its gradient
  ([Poincaré inequality](#/node/poincare_inequality));
* control the gradient of a harmonic function by its size on a larger ball (Gromov/HarmonicR2.lean lines 31–368);
* combine these into the determinant estimate `lemma_3_26_a` (Gromov/Lemma326.lean lines 66–281). If dim *V* is too
  large, this contradicts the growth bound.
""",
 [q("What does the constant C depend on?",
    ["Only on d (and the group's fixed data), not on the subspace V", "On the subspace V",
     "On the radius R"], 0,
    "Gromov/Theorem323.lean line 34: C is chosen first, then the bound holds for every subspace V."),
  q("Which inequality controls a function on a ball by its gradient?",
    ["The Poincaré inequality", "The Cauchy–Schwarz inequality only", "Young's inequality"], 0,
    "poincare_inequality, Gromov/Poincare.lean lines 244–580."),
 ],
 caveats=["The growth bound here (tends to 0) is stronger than the source's liminf < ∞ condition (comment at "
          "Gromov/QuadraticForm.lean line 106). It is a hypothesis of an internal lemma, so this is a design choice, "
          "not a weakening of the final theorem.", SKIM])


node("poincare_inequality",
 "Poincaré inequality on balls",
 "On a ball of radius about R, a function's squared deviation from its average is bounded by R² times a volume "
 "ratio times its squared gradient on a ball three times larger.",
 r"""## Plain English

**Theorem (`poincare_inequality`, Gromov/Poincare.lean lines 244–580; "Theorem 3.20" in the comments).** For every
radius *R* and every *f* : *G* → ℝ, the sum over the ball of radius *R* − 1 of |*f* − average|² is at most

16·*R*²·|*S*| · (|ball(2*R* − 2)| / |ball(*R* − 1)|) · Σ over the ball of radius 3*R* of the squared gradient of *f*.

The squared gradient sums (*f*(*sx*) − *f*(*x*))² over *s* ∈ *S*. The volume ratio is where polynomial growth helps
later: at a well-chosen scale it is bounded. This is the discrete Poincaré inequality Kleiner's proof relies on. The
packing-averaged version is `lemma_3_25_poincare` (lines 620–735).
""",
 [q("Does this inequality assume f is harmonic?",
    ["No, it holds for every function", "Yes", "Only for Lipschitz f"], 0,
    "Gromov/Poincare.lean line 244: f is an arbitrary function G → ℝ."),
 ],
 caveats=[SKIM])


node("proposition_3_18",
 "Energy identity for the Laplacian",
 "For square-summable f, the pairing of f with its Laplacian equals (1/2|S|) Σ_s ‖f − f·δ_s‖². The Laplacian is "
 "a positive operator, and small Laplacian means f is almost invariant.",
 r"""## Plain English

**Theorem (`proposition_3_18`, Gromov/Harmonic/Proposition318.lean lines 386–597).** For every *f* in ℓ²(*G*),

Σ<sub>*g*</sub> *f*(*g*)·(Δ*f*)(*g*) = (1/(2|*S*|)) · Σ<sub>*s*∈*S*</sub> ‖*f* − *f*∗*δ<sub>s</sub>*‖².

Here Δ*f* = *f* − *f*∗*μ* is the Laplacian (see [mu](#/node/mu)). The comment at lines 383–384 notes that the source
misstates this: the right-hand side needs a *squared* norm. This identity powers Case 1 of
[exists_nontrivial_harmonic](#/node/exists_nontrivial_harmonic).
""",
 [q("What does the identity show about the Laplacian?",
    ["⟨f, Δf⟩ ≥ 0, so Δ is positive", "Δ is invertible", "Δ is zero"], 0,
    "The right-hand side is a sum of squares; see laplace_positive_semidefinite (Gromov/Harmonic/SelfAdjoint.lean lines 562–686)."),
 ])


# ---------------------------------------------------------------- the algebraic induction

node("three_two_ker_fg",
 "The kernel of φ is finitely generated",
 "If G has polynomial growth and φ maps G onto ℤ, the kernel of φ is finitely generated. It is generated by the "
 "conjugates γᵐeγ⁻ᵐ with |m| ≤ n, for one bounded n.",
 r"""## Plain English

**Theorem (`three_two_ker_fg`, Gromov/ThreeTwoGenerates.lean lines 918–932).** Under [Generates](#/node/Generates),
with growth degree *d* ≥ 1, the kernel of every surjective homomorphism φ : *G* → ℤ is finitely generated.

Pick γ with φ(γ) = 1. Every generator *s* can be corrected to *e<sub>s</sub>* = *s*·γ<sup>−φ(s)</sup> in the kernel.
The conjugates γ<sup>*m*</sup>*e<sub>s</sub>*γ<sup>−*m*</sup> for all *m* generate the kernel
(`three_two_gamma_m_generates`, lines 260–820). The key point is that a bounded range |*m*| ≤ *n* already suffices
(`three_two_S_n_generates`, lines 849–916). Otherwise the words in these conjugates would give exponentially many
distinct elements (`new_three_two_poly_growth`, Gromov/ThreeTwoGrowth.lean lines 127–602), contradicting polynomial
growth. This is Milnor's lemma as presented by Tao. A comment at Gromov/ThreeTwoGrowth.lean lines 110–112 notes a
correction to the source ("length at most *n*").
""",
 [q("Why does polynomial growth bound the range of m?",
    ["Otherwise there would be exponentially many distinct products, contradicting the growth bound",
     "Because γ has finite order", "Because the kernel is abelian"], 0,
    "new_three_two_poly_growth, Gromov/ThreeTwoGrowth.lean lines 127–602."),
 ],
 caveats=[SKIM])


node("three_two_kernel_poly_growth",
 "The kernel has growth degree d − 1",
 "With the bounded generating set of conjugates, the kernel of φ : G → ℤ has polynomial growth of degree one less "
 "than G. This drives the induction.",
 r"""## Plain English

**Theorem (`three_two_kernel_poly_growth`, Gromov/GrowthZero.lean lines 159–416).** With *d* ≥ 1, φ(γ) = 1 and the
generating set *S<sub>n</sub>* of [conjugates](#/node/three_two_ker_fg), made symmetric, the kernel of φ has
[growth of degree](#/node/HasPolynomialGrowthD) *d* − 1.

Intuition: a ball of radius *R* in *G* contains, for each of about *R* values of *k*, a translate γ<sup>*k*</sup> of a
ball of radius about *R* in the kernel, and these translates are disjoint. So |kernel ball| · *R* ≲ |*G* ball| ≲
*R<sup>d</sup>*.

The kernel is then repackaged as a new [Generates](#/node/Generates) instance (`ker_generates`, lines 69–157), so the induction hypothesis of [main_gromov_theorem](#/node/main_gromov_theorem)
can be applied to it.
""",
 [q("Why must d be at least 1?",
    ["Degree d − 1 must make sense; degree 0 is the finite base case", "Because ℤ has degree 2",
     "It need not be"], 0,
    "Gromov/GrowthZero.lean line 159 assumes d is at least 1."),
 ],
 caveats=["The intuition given is the classical argument; the Lean proof's details were not traced. " + SKIM])


node("exists_gamma_n_unipotent_N'",
 "Some power of γ acts unipotently on N'",
 "If an automorphism of a finitely generated nilpotent group has polynomially growing subset products, then some "
 "power of it acts unipotently: repeatedly applying x ↦ x·γ(x)⁻¹ kills everything.",
 r"""## Plain English

**Theorem (`exists_gamma_n_unipotent_N'`, Gromov/Unipotent/GammaN.lean lines 645–842).** Let *N'* be a finitely
generated nilpotent normal subgroup and γ an automorphism of *N'* whose orbit subset-products grow at most
polynomially (`gamma_conj_bound`, lines 112–114). Then for each *p* > 0 there are *a* ≠ 0 and *n* such that
applying *x* ↦ *x*·γ<sup>*ap*</sup>(*x*⁻¹) *n* times sends every element of *N'* to 1.

The proof climbs the lower central series. On each abelian layer, a finitely generated abelian group, γ acts by an
integer matrix *A*:

* polynomial growth forces every eigenvalue of *A* to have absolute value 1
  ([int_matrix_poly_growth_eigenvalue](#/node/int_matrix_poly_growth_eigenvalue));
* by Kronecker's theorem, a power of *A* is unipotent ([int_matrix_unipotent](#/node/int_matrix_unipotent));
* the centre case is `exists_gamma_n_unipotent_center_N'` (lines 117–639).

The commented-out block at lines 799–842, the only place the word `sorry` appears in proof text, is inert.
""",
 [q("What does 'unipotent' mean for the action here?",
    ["Iterating x ↦ x·γ(x)⁻¹ enough times gives 1 for every x", "γ has order 1", "γ commutes with N'"], 0,
    "Gromov/Unipotent/GammaN.lean line 646."),
  q("Are the sorry lines in this file live?",
    ["No, they are inside a commented-out block", "Yes, the theorem is partial"], 0,
    "Gromov/Unipotent/GammaN.lean lines 799–842: every line starts with --."),
 ],
 caveats=[SKIM])


node("int_matrix_poly_growth_eigenvalue",
 "Slow orbit growth puts integer-matrix eigenvalues on the unit circle",
 "If the subset sums of Aᵏv grow slowly for an invertible integer matrix A, then every complex eigenvalue of A "
 "has absolute value exactly 1.",
 r"""## Plain English

**Theorem (`int_matrix_poly_growth_eigenvalue`, Gromov/MatrixSubsum.lean lines 26–145).** Let *A* be an invertible
*d*×*d* integer matrix. Assume a technical counting bound: for every candidate eigenvalue size |*k*| > 1, the subset
sums of the vectors *A<sup>jm</sup>v*, for suitable *m* and ranges of *j*, take fewer distinct values than an
exponential lower bound would require. Then every complex eigenvalue of *A* has absolute value 1.

The reason: an eigenvalue of size ≥ 3 makes distinct subsets give distinct sums (`subsums_unique`,
Gromov/MatrixSubsum/Subsums.lean). That gives exponentially many group elements, contradicting polynomial growth.
Eigenvalues inside the unit circle are excluded by applying the same argument to *A*⁻¹, since det *A* = ±1.
""",
 [q("Why can't an eigenvalue be smaller than 1 in absolute value?",
    ["A is invertible over ℤ, so the inverse matrix would have an eigenvalue larger than 1",
     "Eigenvalues of integer matrices are integers", "It can be"], 0,
    "The product of the eigenvalues is det A = ±1."),
 ],
 caveats=["The hypothesis is a long explicit counting inequality (lines 26–28), not literally 'polynomial growth'. It is "
          "supplied from the growth bound inside Gromov/Unipotent/GammaN.lean (around line 374).", SKIM])


node("int_matrix_unipotent",
 "Kronecker step: a power of the matrix is unipotent",
 "If all eigenvalues of an invertible integer matrix have absolute value 1, they are roots of unity, so a power of the "
 "matrix minus the identity is nilpotent.",
 r"""## Plain English

**Theorem (`int_matrix_unipotent`, Gromov/MatrixSubsum.lean lines 269–518).** Let *A* be an invertible integer
matrix all of whose complex eigenvalues have absolute value 1. Then for a suitable exponent *K* (`KroneckerPow`,
lines 256–257) and every *n* > 0, (*A*<sup>*nK*</sup> − 1)<sup>*m*</sup> = 0 for some *m*.

This is **Kronecker's theorem**. An algebraic integer whose conjugates all lie on the unit circle is a root of
unity. The project gets it from Mathlib's `Polynomial.pow_eq_one_of_mahlerMeasure_eq_one` (line 199), applied to the
characteristic polynomial.
""",
 [q("What is the eigenvalue fact behind this lemma?",
    ["Kronecker: algebraic integers with all conjugates on the unit circle are roots of unity",
     "The spectral theorem", "Cayley–Hamilton only"], 0,
    "Gromov/MatrixSubsum.lean line 199 uses Mathlib's Mahler-measure form of Kronecker's theorem."),
 ])


node("unipotent_commutator_trivial",
 "A nilpotent group plus a unipotent element generate a nilpotent group",
 "If γ normalizes a finitely generated nilpotent N' and iterated commutators with γ eventually kill N', then the "
 "group generated by N' and γ is nilpotent.",
 r"""## Plain English

**Theorem (`unipotent_commutator_trivial`, Gromov/UnipotentGromov.lean lines 224–594).** Let *H* be a normal subgroup
of *G* and *N'* a characteristic, nilpotent subgroup of *H*, generated by a finite set. Let γ ∈ *G* lie outside *N'*,
and suppose the *m*-fold iterated commutator of every element of *N'* with γ is 1. Then the subgroup generated by *N'*
and γ is nilpotent.

Since *N'* is characteristic in the normal subgroup *H*, conjugation by γ maps *N'* to itself. The hypothesis says γ
acts unipotently. The proof shows that the lower central series of ⟨*N'*, γ⟩ reaches 1, by counting how often γ appears
in long commutators (`count_mem_group_implies_lowercentral`, lines 165–214). This is the last step of
[theorem_3_1](#/node/theorem_3_1.).
""",
 [q("Why does N' need to be characteristic in H?",
    ["So that conjugation by γ (which preserves the normal subgroup H) also preserves N'",
     "So that N' is abelian", "So that γ ∈ N'"], 0,
    "Gromov/UnipotentGromov.lean line 224 assumes N' is characteristic in H and H is normal in G."),
 ],
 caveats=[SKIM])


node("finite_of_growth_zero",
 "Degree-0 growth means a finite group",
 "If |Sⁿ| is bounded by a constant, the group is finite. This is the base case of the induction.",
 r"""## Plain English

**Theorem (`finite_of_growth_zero`, Gromov/GrowthZero.lean lines 432–579).** If *S* has [growth of
degree](#/node/HasPolynomialGrowthD) 0, that is |*S<sup>n</sup>*| ≤ *a* for all *n*, then *G* is finite.

Since 1 ∈ *S*, the sets *S<sup>n</sup>* increase with *n*. Bounded size means they stabilize, so some *S<sup>y</sup>*
is closed under multiplication by *S*, and it is the whole group. The docstring at lines 428–431 says this.
""",
 [q("Why do the sets Sⁿ increase with n?",
    ["Because 1 ∈ S, so Sⁿ ⊆ Sⁿ⁺¹", "Because S is symmetric", "They don't"], 0,
    "Multiplying by 1 keeps every element of Sⁿ in Sⁿ⁺¹."),
 ])


# ---------------------------------------------------------------- extra quiz questions (three per node)
EXTRA = {
 "rho_g": [
  q("What is rho_g a subgroup of?", ["The invertible linear maps of W = LipschitzH / constants", "G itself", "The unitary group U(n)"], 0,
    "Gromov/Representation.lean lines 320–323: the range of GRepW_base."),
  q("Is rho_g assumed to be finite or infinite?", ["Neither; the proof treats both cases", "It is always finite", "It is always infinite"], 0,
    "exists_theorem_3_1_input (Gromov/Theorem31Input.lean lines 342–345) splits on it."),
 ],
 "exists_theorem_3_1_input": [
  q("What does the theorem produce?", ["A finite-index subgroup with a surjective homomorphism onto ℤ", "A nilpotent subgroup", "A harmonic function"], 0,
    "Its conclusion is that a Theorem3_1_Input for G exists."),
 ],
 "rho_g_contains_abelian": [
  q("Which theorem does the proof finally apply?", ["theorem_3_8_real, the compact linear group case", "main_gromov_theorem", "poincare_inequality"], 0,
    "Gromov/RhoAbelian.lean line 456."),
  q("What is the conclusion?", ["rho_g has an abelian subgroup of finite index", "rho_g is finite", "rho_g is abelian"], 0,
    "Gromov/RhoAbelian.lean line 40."),
 ],
 "theorem_3_8_real": [
  q("What is the conclusion?", ["The subgroup has an abelian subgroup of finite index", "The subgroup is finite", "The subgroup is unitary"], 0,
    "Gromov/Theorem38.lean line 280."),
  q("Which hypothesis carries polynomial growth?", ["The SPolyData argument", "CompactSpace H", "Finite-dimensionality of V"], 0,
    "The SPolyData argument, Gromov/Theorem38.lean line 279."),
 ],
 "new_weyl_unitarian_trick": [
  q("What does the theorem produce?", ["A subgroup of U(n) isomorphic to H", "A homomorphism onto ℤ", "An abelian subgroup"], 0,
    "Gromov/Unitary/WeylTrick.lean line 28."),
  q("Which n is used for U(n)?", ["The complex dimension of V", "The number of generators", "Always 2"], 0,
    "The complex dimension of V, line 28."),
 ],
 "theorem_3_23": [
  q("How is the bound used later?", ["Lipschitz_finite_dimensional applies it to a large span of basis vectors to get a contradiction",
    "It is the final theorem", "It is not used"], 0, "Gromov/Theorem323.lean line 308."),
 ],
 "poincare_inequality": [
  q("What measures the 'gradient' of f?", ["The sum over s ∈ S of (f(sx) − f(x))²", "The Lipschitz constant", "The ℓ² norm of f"], 0,
    "deriv_sq_R in Gromov/Poincare.lean."),
  q("Why does the bound involve a ratio of ball sizes?", ["It comes from averaging over translates; polynomial growth later keeps it bounded at good scales",
    "It is a constant 1", "Because G is abelian"], 0, "See the statement, Gromov/Poincare.lean lines 244–245."),
 ],
 "proposition_3_18": [
  q("Which functions does the identity apply to?", ["Square-summable functions on G (ℓ²)", "All functions", "Only harmonic functions"], 0,
    "Gromov/Harmonic/Proposition318.lean line 386: f is in the Lebesgue space L² for counting measure, i.e. ℓ²(G)."),
  q("What does the repo say about the source's version?", ["It is missing a square on the norm", "It is correct", "It has the wrong sign"], 0,
    "Gromov/Harmonic/Proposition318.lean lines 383–384 and Gromov/vikman_errata.txt."),
 ],
 "three_two_ker_fg": [
  q("Which elements generate the kernel?", ["Conjugates γᵐ e γ⁻ᵐ of corrected generators, for |m| ≤ n", "S itself", "Powers of γ"], 0,
    "three_two_S_n, Gromov/ThreeTwoGrowth.lean lines 108–115."),
  q("Which hypothesis is needed besides polynomial growth?", ["φ is surjective onto ℤ", "G is abelian", "G is finite"], 0,
    "Gromov/ThreeTwoGenerates.lean line 918."),
 ],
 "three_two_kernel_poly_growth": [
  q("What is the conclusion?", ["The kernel's symmetric generating set has growth degree d − 1", "The kernel is finite", "The kernel is abelian"], 0,
    "Gromov/GrowthZero.lean lines 159–160."),
  q("Where is this used?", ["In the inductive step theorem_3_1", "In exists_nontrivial_harmonic", "In the unitarian trick"], 0,
    "Gromov/Gromov.lean line 129."),
 ],
 "exists_gamma_n_unipotent_N'": [
  q("Which structure on N' does the proof climb?", ["Its lower central series", "Its derived series of matrices", "Its Sylow subgroups"], 0,
    "Each layer is finitely generated abelian, on which γ acts by an integer matrix."),
 ],
 "int_matrix_poly_growth_eigenvalue": [
  q("What is the conclusion?", ["Every complex eigenvalue has absolute value 1", "A is the identity", "A has finite order"], 0,
    "Gromov/MatrixSubsum.lean line 28."),
  q("Is the hypothesis literally 'polynomial growth'?", ["No, an explicit counting inequality derived from it", "Yes, word for word"], 0,
    "Gromov/MatrixSubsum.lean lines 26–27."),
 ],
 "int_matrix_unipotent": [
  q("What does the conclusion say?", ["A power of A, minus the identity, is nilpotent", "A is diagonal", "A equals the identity"], 0,
    "Gromov/MatrixSubsum.lean line 269."),
  q("What is assumed about A?", ["Invertible over ℤ with all eigenvalues of absolute value 1", "Symmetric", "Upper triangular"], 0,
    "Gromov/MatrixSubsum.lean line 269."),
 ],
 "unipotent_commutator_trivial": [
  q("What is the conclusion?", ["The subgroup generated by N' and γ is nilpotent", "γ is the identity", "N' is abelian"], 0,
    "Gromov/UnipotentGromov.lean line 227."),
  q("What does the hypothesis on γ say?", ["The m-fold iterated commutator of each element of N' with γ is 1", "γ has finite order", "γ commutes with everything"], 0,
    "Gromov/UnipotentGromov.lean line 225."),
 ],
 "finite_of_growth_zero": [
  q("Where is this used?", ["In the base case of main_gromov_theorem", "In the harmonic-function construction", "In the unitarian trick"], 0,
    "Gromov/Gromov.lean line 1000."),
  q("Does it contradict the Generates class?", ["Yes, Generates assumes G infinite, but the proof uses it only to conclude directly", "No"], 0,
    "Gromov/Gromov.lean lines 998–1005."),
 ],
}
for n in NODES:
    n["quiz"].extend(EXTRA.get(n["id"], []))
