NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]

NOT_BUILT = ("The Lean was not built for this site. \"Proved\" here means the file contains a complete-looking proof and "
             "a text search finds no live sorry in the project, not that Lean's kernel accepted it.")


node("FormalConjecturesCheck.gromov_forward",
 "Headline: Gromov's theorem (Formal Conjectures wording)",
 "A finitely generated group whose balls grow at most polynomially has a nilpotent subgroup of finite index. This is "
 "the hard direction of the Formal Conjectures statement, proved by reduction to main_gromov_theorem. The converse "
 "is not proved.",
 r"""## Plain English

**Theorem (`gromov_forward`, Gromov/FormalConjecturesCheck.lean lines 152–181).** Let *G* be any group. Suppose
*G* [has polynomial growth](#/node/FormalConjecturesCheck.HasPolynomialGrowth): there are a finite generating set
*S*, a constant *C* > 0 and an exponent *d* such that, for every *n* ≥ 1, the
[ball of radius n](#/node/FormalConjecturesCheck.CayleyBall) has at most *C*·*n*<sup>*d*</sup> elements. Then *G* is
**virtually nilpotent**: it has a nilpotent subgroup of finite index (Mathlib's `Group.IsVirtuallyNilpotent`).

This is the direction of Gromov's 1981 theorem that needs real work. Google DeepMind's *Formal Conjectures* project
states the theorem as an "if and only if", with a `sorry` as the proof. This file copies its three definitions word
for word (lines 1–30 explain that the toolchains differ, so the file could not be imported) and proves the forward
implication.

A twin, `gromov_forward_fg` (lines 187–189), has the reference statement's exact signature, including an extra
"finitely generated" assumption. That assumption is redundant, because polynomial growth already supplies a finite
generating set.

### What is *not* here

The **converse**, that a virtually nilpotent group has polynomial growth (Wolf, Bass, Guivarc'h), is not proved.
The file says so in lines 24–26. So the Formal Conjectures `sorry` is not discharged as an "iff". Only the hard half is.

### How it connects

The project's own main theorem, [main_gromov_theorem](#/node/main_gromov_theorem), uses a different packaging. It
works inside a class [Generates](#/node/Generates) that bundles an **infinite** group with a symmetric generating
set containing 1, and it measures growth by the product sets *S<sup>n</sup>*. This file bridges the gap:

* finite groups are handled separately: they are trivially virtually nilpotent;
* the generating set is replaced by *S* ∪ *S*⁻¹ ∪ {1} ([normGen](#/node/FormalConjecturesCheck.normGen)), whose
  *n*-th power is exactly the Cayley ball
  ([coe_normGen_pow](#/node/FormalConjecturesCheck.coe_normGen_pow));
* the real constant *C* is rounded up to a natural number.
""",
 [q("What does gromov_forward assume about G?",
    ["Only that it has polynomial growth for some finite generating set",
     "That it is finitely generated, infinite and nilpotent",
     "That it is a subgroup of a matrix group"], 0,
    "Gromov/FormalConjecturesCheck.lean line 152: the only hypothesis is HasPolynomialGrowth G. Finiteness of G is "
    "handled inside the proof."),
  q("Does this project prove the full 'if and only if' from Formal Conjectures?",
    ["No: only polynomial growth ⇒ virtually nilpotent", "Yes, both directions",
     "No: only virtually nilpotent ⇒ polynomial growth"], 0,
    "Gromov/FormalConjecturesCheck.lean lines 24–26 say the converse (Bass–Guivarc'h) is not proved."),
  q("What does 'virtually nilpotent' mean here?",
    ["Some finite-index subgroup is nilpotent", "The group is nilpotent", "The group is finite",
     "Some finite-index subgroup is abelian"], 0,
    "It is Mathlib's Group.IsVirtuallyNilpotent: a nilpotent subgroup of finite index."),
  q("Why does the proof replace S by S ∪ S⁻¹ ∪ {1}?",
    ["Because the main theorem's class wants a symmetric set containing 1, and then S-powers equal Cayley balls",
     "To make the group abelian", "To make the growth exponent smaller"], 0,
    "Lines 159–180 build the Generates instance from normGen; coe_normGen_pow (lines 95–140) matches the two ball "
    "notions."),
 ],
 caveats=[NOT_BUILT,
          "Faithful to the classical forward statement: the hypothesis is exactly 'some finite generating set has "
          "polynomially bounded balls' and the conclusion is Mathlib's virtually nilpotent. No extra hypotheses.",
          "Only the forward direction. The Formal Conjectures statement is an iff, and its converse is not proved here."],
 widgets=walk("How the proof goes (Gromov/FormalConjecturesCheck.lean, lines 152–181)", [
   {"text": "Unpack the hypothesis: a finite generating set S, a constant C > 0, an exponent d and the ball bound (line 156)."},
   {"text": "Split on whether G is finite (line 157). A finite group is virtually nilpotent with the trivial subgroup, "
            "which is nilpotent and of finite index (line 158; finite_virtually_nilpotent)."},
   {"text": "Infinite case: the normalized set S ∪ S⁻¹ ∪ {1} still generates G (lines 159–161).",
    "link": "FormalConjecturesCheck.normGen"},
   {"text": "Turn the ball bound into the project's growth notion: the n-th power of the normalized set has exactly as "
            "many elements as the Cayley ball, and C is rounded up to ⌈C⌉ (lines 162–169).",
    "link": "FormalConjecturesCheck.coe_normGen_pow"},
   {"text": "Package G, the normalized set, the proof that G is infinite, and the growth bound as an instance of the "
            "Generates class (lines 170–180).", "link": "Generates"},
   {"text": "Apply the project's main theorem (line 181).", "link": "main_gromov_theorem"},
 ]))


node("main_gromov_theorem",
 "Headline: the main theorem, by induction on the growth degree",
 "For an infinite group with a symmetric generating set S containing 1, if |Sⁿ| ≤ a·nᵈ for all n ≥ 1, the group is "
 "virtually nilpotent. The proof is an induction on d, and each step is the inductive step theorem_3_1.",
 r"""## Plain English

**Theorem (`main_gromov_theorem`, Gromov/Gromov.lean lines 996–1024).** Work inside the class
[Generates](#/node/Generates): an infinite group *G* with a finite generating set *S* that is symmetric and contains 1.
If, for some natural number *n*, the product sets satisfy |*S<sup>k</sup>*| ≤ *a*·*k<sup>n</sup>* for all *k* ≥ 1
([HasPolynomialGrowthD](#/node/HasPolynomialGrowthD)), then *G* is virtually nilpotent.

Because *S* contains 1 and is symmetric, *S<sup>k</sup>* is the ball of radius *k* in the word metric, so this is the
usual statement of Gromov's theorem for infinite groups. The user-facing form is
[gromov_forward](#/node/FormalConjecturesCheck.gromov_forward).

### The induction

The proof inducts on the degree *n* (Tao's strategy):

* **Degree 0.** Bounded balls force *G* to be finite ([finite_of_growth_zero](#/node/finite_of_growth_zero)). That
  contradicts `Generates`' infiniteness assumption, but the proof doesn't need the contradiction: it just exhibits the
  trivial subgroup as a nilpotent subgroup of finite index.
* **Degree *k* + 1.** First find a finite-index subgroup *G'* that maps onto ℤ
  ([exists_theorem_3_1_input](#/node/exists_theorem_3_1_input)). This is where harmonic functions come in. Then apply
  the [inductive step](#/node/theorem_3_1.). It needs, as an input, Gromov's theorem for every group of growth degree
  *k*, and the induction hypothesis supplies that. Finite groups are again handled directly.

The induction is over all `Generates` instances at once (`generalizing hGS`, line 997). That matters because the
inductive hypothesis is applied to a *different* group: the kernel of the map to ℤ.

### Status

At the pinned commit the file ends with `#print sorries` and `#print axioms` for this theorem (lines 1026–1027). A
text search of the whole project finds `sorry` only in comments. The Lean was not built for this site, so the output
of those commands was not seen.
""",
 [q("What is the induction variable in main_gromov_theorem?",
    ["The polynomial growth degree", "The number of generators", "The nilpotency class", "The size of the group"], 0,
    "Gromov/Gromov.lean line 997: induction on n, the degree in HasPolynomialGrowthD S n."),
  q("Why is the induction stated for all Generates instances, not just the current group?",
    ["Because the inductive hypothesis is used on a different group, the kernel of a map onto ℤ",
     "Because Lean requires it for every induction", "To allow non-symmetric generating sets"], 0,
    "Line 997 generalizes over hGS; line 1023 applies the hypothesis to Q_generates, built from the kernel."),
  q("Which groups does main_gromov_theorem cover directly?",
    ["Infinite groups packaged with a symmetric generating set containing 1",
     "All groups with any finite generating set", "Only finite groups"], 0,
    "The Generates class (Gromov/Defs/WordMetric.lean lines 36–48) requires an infinite group and a symmetric S ∋ 1. "
    "gromov_forward removes these restrictions."),
 ],
 caveats=[NOT_BUILT,
          "The ambient class Generates already contains a growth assumption (its g_growth field), and the theorem "
          "takes a second, explicit degree n. These fit together: the explicit one gives the degree used by the induction.",
          "The degree-0 case does not use the contradiction with infiniteness; it proves the conclusion directly."],
 widgets=walk("How the proof goes (Gromov/Gromov.lean, lines 996–1024)", [
   {"text": "Induct on the degree n, generalizing over the Generates instance (line 997)."},
   {"text": "n = 0: polynomial growth of degree 0 means bounded balls, so G is finite (line 1000). The trivial subgroup "
            "is then nilpotent and of finite index (lines 1001–1005).", "link": "finite_of_growth_zero"},
   {"text": "n = k + 1: obtain a finite-index subgroup G' with a surjection onto ℤ (line 1008).",
    "link": "exists_theorem_3_1_input"},
   {"text": "Apply the inductive step theorem_3_1 (line 1011). It reduces the goal to Gromov's theorem for groups of "
            "growth degree n − 1.", "link": "theorem_3_1."},
   {"text": "For such a group Q: if Q is finite, it is virtually nilpotent with the trivial subgroup (lines 1014–1020). "
            "Otherwise use the induction hypothesis (line 1023)."},
 ]))


node("exists_nontrivial_harmonic",
 "Headline: a non-constant Lipschitz harmonic function exists",
 "On an infinite finitely generated group there is a harmonic function that is Lipschitz for the word metric and is "
 "not constant. This is the first of Kleiner's two facts about harmonic functions.",
 r"""## Plain English

**Theorem (`exists_nontrivial_harmonic`, Gromov/Harmonic.lean lines 439–447; "Theorem 3.6" in the comments).** On
the group of a [Generates](#/node/Generates) instance (infinite, with a symmetric generating set *S* containing 1)
there is an element *F* of [LipschitzH](#/node/LipschitzH), a Lipschitz [harmonic](#/node/Harmonic) function
*G* → ℝ, that differs from every constant function.

"Harmonic" means that the value at *x* is the average of the values at the points *s*·*x*, *s* ∈ *S*. On a finite
group such a function must be constant (maximum principle). On an infinite group, Kleiner's insight is that
**non-constant ones with bounded slope always exist**. They are the raw material for the representation in
[GRep](#/node/GRep).

This statement does not use polynomial growth. Only infiniteness enters, through the Laplacian on ℓ²(*G*) (see the
proof outline). The project follows the write-up its comments call "Vikman". The comments' numbering, from
Definition 3.5 to Theorem 3.23, follows that source, which in turn follows Kleiner and Tao.

### How the proof goes, at a high level

Let *f<sub>n</sub>* be the average of the first *n* + 1 steps of the random walk distribution (*μ* convolved with
itself), where *μ* is the [uniform measure on S](#/node/mu). Split on whether *f<sub>n</sub>* becomes almost invariant
under each generator in ℓ¹:

* **Case 2: not almost invariant** (`nontrivial_harmonic_case_two`, Gromov/Harmonic.lean lines 36–433). Use the
  sign pattern of *f<sub>n</sub>* − *f<sub>n</sub>*·*δ<sub>s</sub>* as a bounded test function. Convolving it with
  *f<sub>n</sub>* gives functions that are uniformly Lipschitz and closer and closer to harmonic. Then extract a limit.
* **Case 1: almost invariant for every generator** (`nontrivial_harmonic_case_one`,
  Gromov/Harmonic/CaseOne.lean lines 35–713). Use the spectral theory of the Laplacian on ℓ²(*G*). It is
  self-adjoint and positive, and 0 is in its spectrum (Gromov/Harmonic/SelfAdjoint.lean lines 752–890) but is not an
  eigenvalue. That gives ℓ² functions with tiny Laplacian, which are normalized via the
  [energy identity](#/node/proposition_3_18) and turned into a limit.

Both cases build their limit with the shared construction `nontrivial_harmonic_common`
(Gromov/Harmonic/LaplaceLinear.lean lines 33–261). It takes a pointwise limit of uniformly Lipschitz functions along a
subsequence and checks that the limit is harmonic.
""",
 [q("Does this theorem assume polynomial growth?",
    ["No, it needs only an infinite finitely generated group (as packaged by Generates)",
     "Yes, it needs growth of degree d",
     "Yes, it needs the group to be nilpotent"], 0,
    "The statement (Gromov/Harmonic.lean line 439) has no growth hypothesis. The two cases depend only on the random "
    "walk and the Laplacian."),
  q("What does 'non-trivial' mean in this statement?",
    ["F is not equal to any constant function", "F is not identically zero", "F is unbounded"], 0,
    "Line 439: F differs from the constant function z for every real number z."),
  q("What is the case split in the proof?",
    ["Whether the averaged random-walk distributions become almost invariant under each generator in ℓ¹",
     "Whether G is abelian", "Whether the growth degree is 0"], 0,
    "Gromov/Harmonic.lean lines 440–446 split on whether the ℓ¹ norm of f_n − f_n * δ_s tends to 0."),
 ],
 caveats=[NOT_BUILT,
          "Harmonic is defined with the average over S including the identity (a 'lazy' walk). Since S contains 1, this "
          "gives the same harmonic functions as averaging over S without 1, so nothing is lost.",
          "The outline of the two cases was taken from the declarations and comments, not from a line-by-line reading of "
          "the 700-line case proofs."],
 widgets=walk("How the proof goes (Gromov/Harmonic.lean, lines 439–447)", [
   {"text": "Case split: is there a generator s for which f_n − f_n * δ_s does not tend to 0 in ℓ¹? (line 440)"},
   {"text": "If yes, nontrivial_harmonic_case_two builds the function from bounded sign-pattern test functions convolved "
            "with f_n (line 441; Gromov/Harmonic.lean lines 36–433)."},
   {"text": "If no, nontrivial_harmonic_case_one uses ℓ² spectral theory of the Laplacian (lines 443–446; "
            "Gromov/Harmonic/CaseOne.lean lines 35–713).", "link": "proposition_3_18"},
   {"text": "Either way the result is an element of LipschitzH that is not constant.", "link": "LipschitzH"},
 ]))


node("Lipschitz_finite_dimensional",
 "Headline: Lipschitz harmonic functions form a finite-dimensional space",
 "For a group of polynomial growth, the vector space of Lipschitz harmonic functions is finite-dimensional. This is "
 "Kleiner's theorem (and Colding–Minicozzi's in geometry). It is what makes the group act by finite matrices.",
 r"""## Plain English

**Theorem (`Lipschitz_finite_dimensional`, Gromov/Theorem323.lean lines 294–465; "Theorem 3.19" in the comments).**
For the group of a [Generates](#/node/Generates) instance, the real vector space [LipschitzH](#/node/LipschitzH) of
Lipschitz harmonic functions is finite-dimensional.

Polynomial growth enters here. It is not written in the statement because it is part of the `Generates` class (the
field `g_growth`). In Lean this result is an `instance`, so Mathlib's linear algebra uses it automatically from then
on.

### Route

The classical proofs are Colding–Minicozzi (for manifolds) and Kleiner (for groups, with a Poincaré inequality). The
project follows Kleiner's argument, which Tao and Shalom–Tao streamlined, through the write-up its comments call
"Vikman":

1. **Theorem 3.23** ([theorem_3_23](#/node/theorem_3_23), Gromov/Theorem323.lean lines 34–286). For each degree *d*
   there is a bound *C*. Any finite-dimensional subspace *V* of Lipschitz harmonic functions with a "growth bound" has
   dimension less than *C*. The growth bound says that |*S<sup>R</sup>*| times a normalized determinant of the Gram
   matrix of *V* on the ball of radius *R*, divided by *R<sup>d</sup>*, tends to 0. The proof combines the
   [Poincaré inequality](#/node/poincare_inequality), a reverse Poincaré ("*R*²") inequality for harmonic functions
   (Gromov/HarmonicR2.lean lines 31–368), a ball-packing argument at a well-chosen scale (Gromov/Packing.lean) and a
   determinant estimate (Gromov/Lemma326.lean lines 66–281).
2. **This theorem.** If the space were infinite-dimensional, take 2 + 2*C* linearly independent functions, span them,
   and check that the span satisfies the growth bound (which uses the polynomial growth of *G*). Theorem 3.23 then says
   its dimension is less than *C*, which is a contradiction.
""",
 [q("Where does the polynomial growth assumption enter this statement?",
    ["Through the ambient Generates class, whose g_growth field it uses", "It is an explicit hypothesis",
     "It does not enter at all"], 0,
    "Gromov/Theorem323.lean line 307 takes the degree d from the g_growth field of the Generates instance."),
  q("What does the theorem say about the space of Lipschitz harmonic functions?",
    ["It is finite-dimensional", "It is zero-dimensional (only constants)", "It is one-dimensional",
     "It is infinite-dimensional"], 0,
    "It is a finite-dimensionality instance for LipschitzH over ℝ. Constants are in the space, and exists_nontrivial_harmonic "
    "shows the dimension is at least 2."),
  q("How is the proof structured?",
    ["By contradiction: a large independent family would violate the dimension bound of Theorem 3.23",
     "By computing an explicit basis", "By induction on the growth degree"], 0,
    "Lines 296–465: assume not finite-dimensional, pick 2 + 2C basis vectors (line 310), apply theorem_3_23."),
 ],
 caveats=[NOT_BUILT,
          "The 'growth bound' in Theorem 3.23 is a 'tends to 0' condition. The comment at Gromov/QuadraticForm.lean "
          "line 106 notes that the source states a liminf < ∞ condition, and that the stronger form is provable here "
          "and easier to work with.",
          "The packing and determinant files (several thousand lines) were not read line by line for this site."],
 widgets=walk("How the proof goes (Gromov/Theorem323.lean, lines 294–465)", [
   {"text": "Suppose LipschitzH is not finite-dimensional. Then a basis of it is infinite (lines 296–307)."},
   {"text": "Take the growth degree d of G from the Generates instance. Apply Theorem 3.23 with degree 2(d + 3) to get "
            "a dimension bound C (lines 307–308).", "link": "theorem_3_23"},
   {"text": "Choose 2 + 2C basis vectors and let V be their span: even dimension, nontrivial, finite-dimensional "
            "(from line 310)."},
   {"text": "Show that V satisfies the growth bound, using the polynomial growth of G and the fact that Lipschitz "
            "functions grow at most linearly. Then Theorem 3.23 gives dim V < C, contradicting dim V = 2 + 2C "
            "(rest of the proof, to line 465)."},
 ]))


node("compact_lie_virtually_abelian",
 "Headline: polynomial-growth subgroups of U(n) are virtually abelian",
 "A finitely generated subgroup of the unitary group U(n) that has polynomial growth has an abelian subgroup of "
 "finite index. This is the 'compact Lie group' case of Tao's outline, proved here directly for matrices.",
 r"""## Plain English

**Theorem (`compact_lie_virtually_abelian`, Gromov/UnitaryGromov.lean lines 28–438).** Let *n* ≥ 1 and let Γ be a
finitely generated subgroup of the unitary group U(*n*) (complex *n*×*n* matrices with *U*\**U* = 1). Suppose Γ
comes with [growth data](#/node/SPolyData): a finite symmetric generating set containing 1 whose balls grow at most
polynomially. Then Γ has an abelian subgroup of finite index.

This is the compact Lie group step of the proof. In Tao's outline it is proved with a Jordan–Zassenhaus-style
argument. Elements close to the identity have commutators even closer to the identity. Polynomial growth limits how
many such elements there can be.

### How it is used

The group *G* acts on the finite-dimensional space of Lipschitz harmonic functions modulo constants, and the action
preserves a norm ([GRep](#/node/GRep)). So the image of *G* lies in a compact group of linear maps. The unitarian
trick ([new_weyl_unitarian_trick](#/node/new_weyl_unitarian_trick)) conjugates it into U(*n*), and
[theorem_3_8_real](#/node/theorem_3_8_real) then applies this theorem to the image.

### Structure of the proof

The proof is a well-founded induction (lines 433–437 close lexicographic-order goals):

* *n* = 1: U(1) is abelian (from line 37).
* If some element of the relevant finite-index subgroup is central but **not a scalar**, split ℂ<sup>*n*</sup> into
  its eigenspaces. These are smaller, so the induction applies to each block (the `nontrivial_centrer_implies_virtual`
  step from line 73).
* If every central element is a scalar, the core argument `central_trivial_virtually_abelian`
  (Gromov/Unitary/CentralTrivial.lean lines 208–960) applies. It looks at the elements within ε of the identity
  (Gromov/Unitary/HnEps.lean). Counting distinct words built from them (Gromov/Unitary/Words.lean) against
  polynomial growth, together with a volume-packing bound in U(*n*) (Gromov/Unitary/Packing.lean), forces the
  conclusion.
""",
 [q("What is the conclusion of compact_lie_virtually_abelian?",
    ["The subgroup has an abelian subgroup of finite index", "The subgroup is finite", "The subgroup is nilpotent",
     "The subgroup is trivial"], 0,
    "Gromov/UnitaryGromov.lean line 29: some subgroup is commutative and has finite index."),
  q("Which assumptions does it need besides being a subgroup of U(n)?",
    ["Finitely generated, with a polynomial-growth generating set (SPolyData)",
     "Only that it is closed", "That it is abelian already"], 0,
    "Line 28 assumes the subgroup is finitely generated and takes SPolyData for it."),
  q("Why does a subgroup of U(n) appear in a theorem about abstract groups?",
    ["G acts on finitely many dimensions of harmonic functions by norm-preserving maps, and these can be made unitary",
     "Every group is a subgroup of U(n)", "Because G is assumed to be a matrix group"], 0,
    "See GRep, rho_g_contains_abelian and new_weyl_unitarian_trick."),
 ],
 caveats=[NOT_BUILT,
          "The classical statement is about compact Lie groups in general; this theorem is about subgroups of U(n). That "
          "is enough because every compact linear group is conjugate into U(n) (new_weyl_unitarian_trick).",
          "The proof outline is reconstructed from the case structure and the auxiliary file names. The 750-line "
          "centrally trivial case was not read line by line."],
 widgets=walk("How the proof goes (Gromov/UnitaryGromov.lean, lines 28–438)", [
   {"text": "Record the growth degree for the auxiliary H_n(ε) machinery (lines 33–35).", "link": "SPolyData"},
   {"text": "n = 1: matrices in U(1) commute, so the whole group is abelian (lines 37–72)."},
   {"text": "n ≥ 2, case 1: a central element that is not a scalar splits ℂⁿ into smaller eigenspaces. Induct on "
            "the blocks (from line 73)."},
   {"text": "n ≥ 2, case 2: every central element of the finite-index subgroup built from elements near the identity "
            "is a scalar. Apply central_trivial_virtually_abelian (line 415; Gromov/Unitary/CentralTrivial.lean "
            "lines 208–960)."},
   {"text": "Discharge the well-founded induction's ordering goals (lines 433–437)."},
 ]))


node("theorem_3_1.",
 "Headline: the inductive step (theorem_3_1)",
 "If G has growth degree d ≥ 1, contains a finite-index subgroup G' mapping onto ℤ, and Gromov's theorem holds in "
 "degree d − 1, then G is virtually nilpotent. The kernel is virtually nilpotent by induction, and the extra ℤ "
 "direction acts unipotently after taking a power.",
 r"""## Plain English

**Theorem (`theorem_3_1`, Gromov/Gromov.lean lines 44–989; Theorem 3.1 in the comments' numbering).** Inside a
[Generates](#/node/Generates) instance, assume:

* polynomial growth of degree *d* ≥ 1;
* a [Theorem3_1_Input](#/node/Theorem3_1_Input): a finite-index subgroup *G'* and a surjective homomorphism φ from
  *G'* onto ℤ;
* the **inductive hypothesis**: every `Generates` group of growth degree *d* − 1 is virtually nilpotent.

Then *G* is virtually nilpotent.

This is the algebraic half of Gromov's theorem, and it is the longest single proof in the project (about 950
lines). The scanned id has a trailing dot (`theorem_3_1.`) because the declaration carries an explicit universe
annotation that the site's text scanner does not strip.

### Why this works (Tao's §3 / Milnor–Wolf argument)

1. *G'* has finite index, so it is finitely generated and has the same growth degree *d* (lines 49–85, via
   `poly_growth_equiv`).
2. Pick γ with φ(γ) = 1. The kernel *K* of φ is generated by the conjugates γ<sup>m</sup>*e*γ<sup>−m</sup> for
   |*m*| ≤ *n* of finitely many elements *e*. Polynomial growth makes a bounded range of *m* enough
   ([three_two_ker_fg](#/node/three_two_ker_fg)). With those generators, *K* has growth degree *d* − 1
   ([three_two_kernel_poly_growth](#/node/three_two_kernel_poly_growth)). Lines 127–130.
3. By the inductive hypothesis *K* is virtually nilpotent (lines 148–211).
4. Inside *K* take a nilpotent, finite-index, finitely generated subgroup *N'* that is **characteristic**, so
   conjugation by γ maps it to itself. It is generated by the *k*-th powers in a normal nilpotent finite-index
   subgroup, where *k* is that subgroup's index (lines 212–323).
5. Conjugation by γ is an automorphism of *N'* (lines 328–355). The subset products of its orbits grow only
   polynomially (lines 427–567). By [exists_gamma_n_unipotent_N'](#/node/exists_gamma_n_unipotent_N') some power
   γ<sup>α</sup> acts **unipotently**: commuting with γ<sup>α</sup> enough times kills every element of *N'*
   (lines 568–598). Underneath is the fact that an integer matrix with polynomially growing orbits has all its
   eigenvalues on the unit circle ([int_matrix_poly_growth_eigenvalue](#/node/int_matrix_poly_growth_eigenvalue)).
6. Then the subgroup generated by *N'* and γ<sup>α</sup> is nilpotent
   ([unipotent_commutator_trivial](#/node/unipotent_commutator_trivial), line 612). It has finite index in *G'*,
   hence in *G* (lines 677–989).
""",
 [q("What does theorem_3_1 take as an input that main_gromov_theorem supplies by induction?",
    ["Gromov's theorem for all groups of growth degree d − 1", "Gromov's theorem for G itself",
     "A nilpotent subgroup of G"], 0,
    "Gromov/Gromov.lean line 45: the hypothesis inductive_gromov quantifies over all Generates instances of degree d − 1."),
  q("Why is the growth degree of the kernel d − 1 rather than d?",
    ["The ℤ quotient direction accounts for one degree of growth",
     "Kernels always have degree 0", "Because the kernel is abelian"], 0,
    "three_two_kernel_poly_growth (Gromov/GrowthZero.lean lines 159–416) proves the d − 1 bound."),
  q("What role does 'unipotent' play in the proof?",
    ["Some power of γ acts on N' so that iterated commutators with it vanish, which keeps ⟨N', γ^α⟩ nilpotent",
     "It means γ has finite order", "It means N' is abelian"], 0,
    "Lines 568–612: exists_gamma_n_unipotent_N' then unipotent_commutator_trivial."),
  q("Where does the finite-index subgroup with a map onto ℤ come from?",
    ["From the representation on harmonic functions (exists_theorem_3_1_input)", "It is assumed in the main theorem",
     "From the lower central series of G"], 0,
    "main_gromov_theorem line 1008 obtains it from exists_theorem_3_1_input."),
 ],
 caveats=[NOT_BUILT,
          "CONDITIONAL by design: the inductive hypothesis is an explicit assumption. main_gromov_theorem discharges it "
          "by induction, so the final theorem is unconditional.",
          "Step numbers and line ranges were read from the have/obtain structure of the proof. Some intermediate steps "
          "(especially lines 677–989) were only skimmed."],
 widgets=walk("How the proof goes (Gromov/Gromov.lean, lines 44–989)", [
   {"text": "G' has finite index, so it is finitely generated. Build a symmetric generating set S_G' and show that G' "
            "has growth degree d (lines 49–85)."},
   {"text": "Package G' as a new Generates instance, proving that it is infinite (lines 91–126).", "link": "Generates"},
   {"text": "Choose γ with φ(γ) = 1. The kernel of φ is finitely generated with growth degree d − 1 (lines 127–130).",
    "link": "three_two_kernel_poly_growth"},
   {"text": "By the inductive hypothesis the kernel is virtually nilpotent (lines 148–211)."},
   {"text": "Pass to a characteristic, nilpotent, finitely generated, finite-index subgroup N' of the kernel "
            "(lines 212–323)."},
   {"text": "Conjugation by γ is an automorphism of N' whose orbit subset-products grow polynomially (lines 328–567)."},
   {"text": "Some power γ^α acts unipotently on N' (lines 568–598).", "link": "exists_gamma_n_unipotent_N'"},
   {"text": "The subgroup generated by N' and γ^α is nilpotent (line 612).", "link": "unipotent_commutator_trivial"},
   {"text": "It has finite index in G, so G is virtually nilpotent (lines 677–989)."},
 ]))
