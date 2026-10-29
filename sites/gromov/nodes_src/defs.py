NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}


node("FormalConjecturesCheck.HasPolynomialGrowth",
 "Polynomial growth (Formal Conjectures definition)",
 "G has polynomial growth if some finite generating set S has balls with at most C·nᵈ elements for every radius n ≥ 1. "
 "This is the hypothesis of the headline gromov_forward.",
 r"""## Plain English

**Definition (`HasPolynomialGrowth`, Gromov/FormalConjecturesCheck.lean lines 60–63).** A group *G* has polynomial
growth when there exist:

* a **finite** set *S* ⊆ *G* that **generates** *G* as a group;
* a real constant *C* > 0 and a natural number *d*;

such that for every *n* > 0 the [growth function](#/node/FormalConjecturesCheck.GrowthFunction) satisfies
*γ<sub>S</sub>*(*n*) ≤ *C*·*n<sup>d</sup>*.

The file says this definition is copied from Google DeepMind's *Formal Conjectures* repository (Apache-2.0)
(lines 7–13). Since it is the reference definition and not the author's own, it is a good anchor for faithfulness.

Whether growth is polynomial does not depend on the choice of finite generating set. Here only *one* such set is
required, which is the standard definition.
""",
 [q("How many generating sets must satisfy the bound?",
    ["At least one finite generating set", "Every finite generating set", "Every subset of G"], 0,
    "Lines 61–63 ask for one finite generating set with the bound."),
  q("For which n must the bound hold?",
    ["All n > 0", "All sufficiently large n only", "Only n = 1"], 0,
    "Line 63: every positive n."),
  q("Must the generating set be symmetric or contain 1?",
    ["No: the Cayley ball itself allows inverses and has radius n", "Yes, both", "It must contain 1 but need not be symmetric"], 0,
    "See CayleyBall (lines 48–49): letters may come from S or S⁻¹, and words of length ≤ n include the empty word."),
 ])


node("FormalConjecturesCheck.GrowthFunction",
 "Growth function",
 "γ_S(n) is the number of group elements within distance n of the identity, using letters from S and their inverses.",
 r"""## Plain English

**Definition (`GrowthFunction`, Gromov/FormalConjecturesCheck.lean lines 54–55).** The growth function counts the
elements of the [Cayley ball](#/node/FormalConjecturesCheck.CayleyBall) of radius *n*. For a finite generating set
this ball is finite.

For ℤ<sup>*k*</sup> with its standard generators, γ(*n*) grows like *n<sup>k</sup>*. For a free group on two
generators it grows like 3<sup>*n*</sup>. Gromov's theorem says polynomial behaviour happens only for virtually
nilpotent groups.
""",
 [q("Roughly how does the growth function of ℤ² with the standard generators behave?",
    ["Like n²", "Like 2ⁿ", "It is constant"], 0,
    "The ball of radius n is a diamond with about 2n² points."),
 ],
 caveats=["The Lean version uses Set.ncard, which returns 0 for infinite sets; with finite S the ball is always finite, "
          "so this does not matter here."])


node("FormalConjecturesCheck.CayleyBall",
 "Cayley ball",
 "The ball of radius n: all products of at most n letters, each from S or the inverse of an element of S.",
 r"""## Plain English

**Definition (`CayleyBall`, Gromov/FormalConjecturesCheck.lean lines 48–49).** An element *g* is in the ball of
radius *n* when *g* can be written as a product of a list of at most *n* letters, where each letter is in *S* or has
its inverse in *S*. The empty product (the identity) is always included.

This is the ball around 1 in the Cayley graph of (*G*, *S*).
""",
 [q("Is the identity always in the Cayley ball of radius 0?",
    ["Yes: it is the product of the empty list", "Only if 1 ∈ S", "No"], 0,
    "The empty list has length 0 ≤ n and product 1."),
 ])


node("FormalConjecturesCheck.normGen",
 "Normalized generating set S ∪ S⁻¹ ∪ {1}",
 "The bridge set: adding inverses and the identity to S turns 'balls of radius n' into plain n-fold products Sⁿ.",
 r"""## Plain English

**Definition (`normGen`, Gromov/FormalConjecturesCheck.lean lines 72–73).** Given a finite set *S*, form the finite
set *S* ∪ *S*⁻¹ ∪ {1}.

It is symmetric and contains the identity, which is what the [Generates](#/node/Generates) class requires. The
lemmas on lines 75–91 record exactly that.
""",
 [q("Why add 1 to the set?",
    ["So that the n-fold product set contains all shorter words too", "To make the group abelian",
     "Because S might not be finite"], 0,
    "With 1 available, a shorter word can be padded to length n: see coe_normGen_pow."),
 ])


node("FormalConjecturesCheck.coe_normGen_pow",
 "Bridge lemma: Sⁿ equals the Cayley ball",
 "The n-th power of S ∪ S⁻¹ ∪ {1} is exactly the Cayley ball of radius n. So the two growth notions agree.",
 r"""## Plain English

**Lemma (`coe_normGen_pow`, Gromov/FormalConjecturesCheck.lean lines 95–140).** For finite *S* and every *n*, the set
of all products of *n* elements of [normGen](#/node/FormalConjecturesCheck.normGen) *S* equals the
[Cayley ball](#/node/FormalConjecturesCheck.CayleyBall) of radius *n*.

The proof is by induction on *n*:

* if a word is shorter than *n*, pad it with the identity;
* otherwise peel off its last letter.

Then `card_normGen_pow` (lines 142–144) turns this into equality of the counts.
""",
 [q("What does this lemma let the headline do?",
    ["Translate the Formal Conjectures growth bound into a bound on |Sⁿ| for the main theorem",
     "Prove that S generates G", "Prove the converse of Gromov's theorem"], 0,
    "Used at Gromov/FormalConjecturesCheck.lean line 164 inside gromov_forward."),
 ])


node("Generates",
 "Generates: the standing assumptions",
 "The class the whole development works in: an infinite group G with a finite symmetric generating set S containing 1, "
 "of polynomial growth.",
 r"""## Plain English

**Class (`Generates`, Gromov/Defs/WordMetric.lean lines 36–48).** An instance consists of:

* a type *G* with a group structure and decidable equality;
* a nonempty finite set *S* ⊆ *G* that **generates** *G*;
* *S* contains 1, and with each element it contains its inverse;
* *G* is **infinite**;
* *S* has [polynomial growth](#/node/HasPolynomialGrowth) for some degree.

Almost every declaration in the project lives in the namespace `GeneratesNS` and assumes an ambient instance. So
"the group" and "*S*" in node descriptions mean these fields. The [word metric](#/node/WordDist) and
[harmonic functions](#/node/Harmonic) are defined relative to them.

Because the class bundles polynomial growth, results such as
[Lipschitz_finite_dimensional](#/node/Lipschitz_finite_dimensional) use growth without saying so in their
statement. The inductive step builds *new* instances for subgroups and kernels.
""",
 [q("Which groups can a Generates instance describe?",
    ["Only infinite groups of polynomial growth with a symmetric generating set containing 1",
     "Any finitely generated group", "Only finite groups"], 0,
    "Gromov/Defs/WordMetric.lean lines 36–48: fields generates, one_mem, has_inv, g_infinite, g_growth."),
  q("How does gromov_forward handle finite groups, which Generates excludes?",
    ["It treats them separately: finite groups are trivially virtually nilpotent",
     "It doesn't; finite groups are excluded from the headline", "It embeds them in ℤ"], 0,
    "Gromov/FormalConjecturesCheck.lean lines 157–158."),
 ],
 caveats=["The degree in g_growth is not carried as data (a TODO comment at line 47 says so). Theorems that need a "
          "specific degree take it as a separate hypothesis."])


node("HasPolynomialGrowthD",
 "Polynomial growth of degree d (project definition)",
 "S has growth of degree d if there is a natural number a with |Sⁿ| ≤ a·nᵈ for all n ≥ 1.",
 r"""## Plain English

**Definition (`HasPolynomialGrowthD`, Gromov/Defs/WordMetric.lean line 28).** For a finite subset *S* of a group and
a natural number *d*, there is a natural number *a* such that, for all *n* ≥ 1, the *n*-fold product set
*S<sup>n</sup>* = {*s*<sub>1</sub>⋯*s<sub>n</sub>*} has at most *a*·*n<sup>d</sup>* elements.

When *S* is symmetric and contains 1 (as in [Generates](#/node/Generates)), *S<sup>n</sup>* is the ball of radius *n*
(`closed_ball_eq_S_pow`, Gromov/Defs.lean lines 141–188), so this is the usual notion. The comment on lines 26–27
credits Yaël Dillies' LeanCamCombi and the Vikman write-up for the definition.

[HasPolynomialGrowth](#/node/HasPolynomialGrowth) (line 29) says this holds for *some* *d*.
""",
 [q("What does Sⁿ mean here?",
    ["All products of exactly n elements of S", "The n-th power of a single element", "S repeated n times as a list"], 0,
    "Pointwise power of a Finset. Because 1 ∈ S, products of exactly n elements include all shorter products."),
  q("Is the constant a real number?",
    ["No, a natural number; gromov_forward rounds the real C up", "Yes, a positive real", "There is no constant"], 0,
    "Line 28 asks for a natural-number constant; Gromov/FormalConjecturesCheck.lean line 163 rounds C up."),
 ],
 caveats=["For a set S without 1, Sⁿ would only contain words of length exactly n. The project always applies this "
          "with 1 ∈ S."])


node("HasPolynomialGrowth",
 "Polynomial growth of some degree",
 "S has polynomial growth if HasPolynomialGrowthD S d holds for some d.",
 r"""## Plain English

**Definition (`HasPolynomialGrowth`, Gromov/Defs/WordMetric.lean line 29).** There is a degree *d* with
[HasPolynomialGrowthD](#/node/HasPolynomialGrowthD) *S* *d*. It is the type of the `g_growth` field of
[Generates](#/node/Generates).

Don't confuse it with the Formal Conjectures definition of the same name,
[FormalConjecturesCheck.HasPolynomialGrowth](#/node/FormalConjecturesCheck.HasPolynomialGrowth), which is about the
group and quantifies over generating sets.
""",
 [q("What is the difference from FormalConjecturesCheck.HasPolynomialGrowth?",
    ["This one is about a fixed set S and uses Sⁿ; the other is about G and some generating set, using Cayley balls",
     "They are literally the same definition", "This one requires exponential growth"], 0,
    "Compare Gromov/Defs/WordMetric.lean line 29 with Gromov/FormalConjecturesCheck.lean lines 60–63."),
 ])


node("WordNorm",
 "Word length",
 "The length of the shortest word in S that multiplies out to g.",
 r"""## Plain English

**Definition (`WordNorm`, Gromov/Defs/WordMetric.lean line 118).** For *g* in *G*, the least *n* such that some list
of *n* elements of *S* has product *g*. Since *S* generates *G* and is symmetric, such a list always exists
(`mem_S_prod_list`, lines 98–111).
""",
 [q("What is the word length of the identity?",
    ["0, the empty word", "1", "It is undefined"], 0,
    "word_norm_one, Gromov/Defs/WordMetric.lean lines 132–133."),
 ])


node("WordDist",
 "Word metric",
 "The distance from x to y is the word length of y·x⁻¹. The project's Lipschitz functions and balls are measured with it.",
 r"""## Plain English

**Definition (`WordDist`, Gromov/Defs/WordMetric.lean line 144).** dist(*x*, *y*) = [word length](#/node/WordNorm) of
*y*·*x*⁻¹. It is symmetric (line 177) and satisfies the triangle inequality (line 182). It becomes Lean's metric on
*G* (`instMetricSpace`, lines 372–379).

The metric is invariant under multiplying both points **on the right**. That is why the group acts on functions by
right translation (*f* ↦ *f*(· *g*)) in [GRep](#/node/GRep), while harmonicity averages over left multiples *s*·*x*.
""",
 [q("Which translations preserve this metric?",
    ["Right multiplication: dist(xg, yg) = dist(x, y)", "Left multiplication only", "No translations"], 0,
    "(yg)(xg)⁻¹ = yx⁻¹. The instance isometricGMul (Gromov/Defs.lean lines 83–90) records this."),
 ])


node("Harmonic",
 "Harmonic function",
 "f is harmonic if its value at each x is the average of its values at s·x for s in S: a discrete Laplace equation.",
 r"""## Plain English

**Definition (`Harmonic`, Gromov/Defs/LipschitzH.lean line 31; "Definition 3.5" in the comments,
Gromov/Defs/Measure.lean line 308).** A function *f* : *G* → ℝ is harmonic if, for every *x*,

*f*(*x*) = (1/|*S*|) · Σ<sub>*s*∈*S*</sub> *f*(*s*·*x*).

Equivalently, *f* minus its average against the [step distribution μ](#/node/mu) is zero, so the discrete
Laplacian (`Laplace_b`, Gromov/Defs.lean line 37) vanishes.

Since *S* contains 1, the sum includes *f*(*x*) itself. That gives a "lazy" random walk, with the same harmonic
functions as averaging over *S* ∖ {1}.
""",
 [q("Which functions are always harmonic?",
    ["Constant functions", "Functions with finite support", "Indicator functions of S"], 0,
    "A constant equals its own average. ConstLipschitzH packages them."),
  q("Does including 1 ∈ S in the average change which functions are harmonic?",
    ["No", "Yes, it makes only constants harmonic", "Yes, it makes every function harmonic"], 0,
    "f(x) = (f(x) + Σ_{s≠1} f(sx))/|S| rearranges to f(x) = Σ_{s≠1} f(sx)/(|S| − 1)."),
 ])


node("LipschitzH",
 "LipschitzH: Lipschitz harmonic functions",
 "The space of functions G → ℝ that are both harmonic and Lipschitz for the word metric. Kleiner's argument studies it.",
 r"""## Plain English

**Structure (`LipschitzH`, Gromov/Defs/LipschitzH.lean lines 32–38).** An element is a function *f* : *G* → ℝ
together with proofs that

* *f* is Lipschitz for the [word metric](#/node/WordDist): for some constant *C*,
  |*f*(*x*) − *f*(*y*)| ≤ *C*·dist(*x*, *y*);
* *f* is [harmonic](#/node/Harmonic).

It is a real vector space (`lipschitzHVectorSpace`, lines 284–313). Its Lipschitz seminorm (Gromov/LipschitzNorm.lean)
becomes a norm once constants are factored out. The quotient *W* = LipschitzH / constants is the space *G* acts on in
[GRep](#/node/GRep).

Two results drive the proof:
* it contains non-constant elements ([exists_nontrivial_harmonic](#/node/exists_nontrivial_harmonic));
* under polynomial growth it is finite-dimensional
  ([Lipschitz_finite_dimensional](#/node/Lipschitz_finite_dimensional)).
""",
 [q("Which two conditions define an element of LipschitzH?",
    ["Lipschitz for the word metric and harmonic", "Bounded and harmonic", "Square-summable and harmonic"], 0,
    "Gromov/Defs/LipschitzH.lean lines 34–38."),
  q("Are bounded harmonic functions required?",
    ["No: Lipschitz functions may grow linearly", "Yes, they must be bounded", "Yes, they must have finite support"], 0,
    "Lipschitz only bounds the slope, so a non-constant harmonic function like a homomorphism to ℝ is allowed."),
 ])


node("ConstLipschitzH",
 "Constant functions as Lipschitz harmonic functions",
 "Each real number z gives the constant function z, an element of LipschitzH. 'Non-trivial' means not one of these.",
 r"""## Plain English

**Definition (`ConstLipschitzH`, Gromov/Defs/LipschitzH.lean lines 97–109).** The constant function with value *z*,
packaged as an element of [LipschitzH](#/node/LipschitzH): Lipschitz with constant 0, and harmonic. The constants form
the subspace `ConstF` (Gromov/Defs.lean lines 50–80), and *W* is the quotient by it.
""",
 [q("Why quotient by constants before building the representation?",
    ["The Lipschitz seminorm of a constant is 0, so only the quotient is a normed space",
     "Constants are not harmonic", "Constants are not Lipschitz"], 0,
    "Gromov/LipschitzNorm.lean lines 1–15 note that W is the actual normed space."),
 ])


node("mu",
 "The step distribution μ",
 "μ puts mass 1/|S| on each element of S: one step of the random walk. Harmonic means invariant under averaging by μ.",
 r"""## Plain English

**Definition (`mu`, Gromov/Defs/Convolution.lean lines 51–53).** The function *G* → ℝ equal to 1/|*S*| on *S* and 0
elsewhere. `muConv n` (lines 54–58) is its (*n*+1)-fold convolution: the distribution of the random walk after *n* + 1
steps. Averages of these are the *f<sub>n</sub>* in the [existence proof](#/node/exists_nontrivial_harmonic).
""",
 [q("What is the total mass of μ?",
    ["1", "|S|", "0"], 0,
    "|S| points of mass 1/|S| each. mu_norm_one (Gromov/Harmonic/MuConv.lean lines 335–417) proves the corresponding ℓ¹ fact for its convolution powers."),
 ])


node("SPolyData",
 "SPolyData: growth data for a subgroup",
 "For a subgroup of a matrix group: a finite symmetric generating set containing 1 with a polynomial bound on its powers. "
 "It is the growth hypothesis of the compact-group step.",
 r"""## Plain English

**Structure (`SPolyData`, Gromov/Unitary/HnEps.lean lines 27–37).** For a subgroup Γ, an instance gives:

* a finite set *S* ⊆ Γ containing 1, equal to its set of inverses, and generating Γ;
* a positive natural constant and a degree *d* with |*S<sup>r</sup>*| ≤ const·*r<sup>d</sup>* for all *r* ≥ 1.

It is the [Generates](#/node/Generates) growth notion restated for subgroups, without the infiniteness requirement.
[compact_lie_virtually_abelian](#/node/compact_lie_virtually_abelian) takes it as its growth hypothesis.
""",
 [q("Does SPolyData require the subgroup to be infinite?",
    ["No", "Yes"], 0,
    "Gromov/Unitary/HnEps.lean lines 27–37 have no infiniteness field, unlike Generates."),
 ])


node("Theorem3_1_Input",
 "Theorem3_1_Input: a finite-index subgroup mapping onto ℤ",
 "The data the inductive step needs: a finite-index subgroup G' of G and a surjective homomorphism from G' onto ℤ.",
 r"""## Plain English

**Structure (`Theorem3_1_Input`, Gromov/RhoAbelian.lean lines 623–629).** An instance gives a subgroup *G'* ⊆ *G* of
**finite index**, together with a **surjective** homomorphism φ : *G'* → ℤ. In Lean, φ goes from the additive version
of *G'* to the integers.

Producing this data is the analytic half of the proof
([exists_theorem_3_1_input](#/node/exists_theorem_3_1_input)). Consuming it is the algebraic half
([theorem_3_1](#/node/theorem_3_1.)). Tao's outline calls this "a finite-index subgroup with infinite abelianization",
reduced to a surjection onto ℤ.
""",
 [q("Why is a map onto ℤ useful?",
    ["Its kernel has smaller growth degree, which enables induction", "It makes G abelian", "It shows G is finite"], 0,
    "three_two_kernel_poly_growth: the kernel has degree d − 1."),
 ])


EXTRA = {
 "WordNorm": [
  q("Which letters may the word use?", ["Elements of S (which is symmetric, so inverses are included)", "Any group element", "Only generators of ℤ"], 0,
    "Lists of elements of S, Gromov/Defs/WordMetric.lean line 118."),
  q("Why does a word always exist?", ["S generates G and is symmetric", "G is finite", "G is abelian"], 0,
    "mem_S_prod_list, Gromov/Defs/WordMetric.lean lines 98–111."),
 ],
 "mu": [
  q("Where is μ supported?", ["On S", "On all of G", "Only at the identity"], 0, "Gromov/Defs/Convolution.lean lines 51–53."),
  q("How is harmonicity expressed with μ?", ["f equals f convolved with μ (the Laplacian f − f∗μ vanishes)", "f∗μ = 0", "μ∗μ = μ"], 0,
    "Laplace_b, Gromov/Defs.lean line 37."),
 ],
}
for n in NODES:
    n["quiz"].extend(EXTRA.get(n["id"], []))

EXTRA2 = {
 "ConstLipschitzH": [
  q("Is a constant function harmonic?", ["Yes, it equals its own average", "No"], 0, "Gromov/Defs/LipschitzH.lean lines 97–109."),
  q("What is the Lipschitz constant of a constant function?", ["0", "1", "|S|"], 0, "It never changes value."),
 ],
 "FormalConjecturesCheck.CayleyBall": [
  q("May letters be inverses of elements of S?", ["Yes", "No, only elements of S"], 0, "Line 49: each letter is in S or has its inverse in S."),
  q("Words of which lengths count for the ball of radius n?", ["All lengths ≤ n", "Exactly n", "At least n"], 0, "Line 49: the list has length at most n."),
 ],
 "FormalConjecturesCheck.GrowthFunction": [
  q("What does GrowthFunction S n count?", ["Elements of the Cayley ball of radius n", "Words of length n", "Generators"], 0,
    "Gromov/FormalConjecturesCheck.lean lines 54–55."),
  q("Roughly how does the growth function of a free group on two generators behave?", ["Exponentially, like 3ⁿ", "Like n²", "It is bounded"], 0,
    "The free group is the standard example of exponential growth."),
 ],
 "FormalConjecturesCheck.coe_normGen_pow": [
  q("How is the lemma proved?", ["Induction on n: pad short words with 1, peel the last letter off long ones", "By a cardinality bound", "By Mathlib automation alone"], 0,
    "Gromov/FormalConjecturesCheck.lean lines 96–140."),
  q("Does it hold for every n, including 0?", ["Yes", "Only n ≥ 1"], 0, "The zero case is lines 98–105."),
 ],
 "FormalConjecturesCheck.normGen": [
  q("Is normGen S symmetric?", ["Yes", "No"], 0, "inv_mem_normGen, lines 86–91."),
  q("Does normGen S still generate G when S does?", ["Yes, it contains S", "Not necessarily"], 0, "subset_normGen, lines 83–84; used at lines 159–161."),
 ],
 "Generates": [
  q("Why does the class insist that 1 ∈ S?", ["So that Sⁿ is the ball of radius n", "So that G is abelian", "So that G is finite"], 0,
    "With 1 ∈ S, shorter words can be padded; see closed_ball_eq_S_pow."),
 ],
 "Harmonic": [
  q("Which multiples of x does the average use?", ["Left multiples s·x for s ∈ S", "Right multiples x·s", "All elements of G"], 0,
    "Gromov/Defs/LipschitzH.lean line 31."),
 ],
 "HasPolynomialGrowth": [
  q("Which field of Generates has this type?", ["g_growth", "generates", "one_mem"], 0, "Gromov/Defs/WordMetric.lean line 48."),
  q("Does it fix the degree?", ["No, it only says some degree works", "Yes"], 0, "Line 29: ∃ d."),
 ],
 "HasPolynomialGrowthD": [
  q("For which n must the bound hold?", ["All n ≥ 1", "All n ≥ 0", "Large n only"], 0, "Gromov/Defs/WordMetric.lean line 28."),
 ],
 "LipschitzH": [
  q("Is LipschitzH a vector space?", ["Yes, over ℝ", "No, only a set"], 0, "lipschitzHVectorSpace, Gromov/Defs/LipschitzH.lean lines 284–313."),
 ],
 "SPolyData": [
  q("Must S be symmetric?", ["Yes: S equals S⁻¹", "No"], 0, "Field S_inv, Gromov/Unitary/HnEps.lean line 31."),
  q("Which theorem takes SPolyData as its growth hypothesis?", ["compact_lie_virtually_abelian", "main_gromov_theorem", "exists_nontrivial_harmonic"], 0,
    "Gromov/UnitaryGromov.lean lines 28–29."),
 ],
 "Theorem3_1_Input": [
  q("What must φ be?", ["A surjective homomorphism from G' onto ℤ", "An injective map into ℤ", "Any function"], 0, "Gromov/RhoAbelian.lean lines 627–629."),
  q("What must G' be?", ["A subgroup of finite index", "A normal abelian subgroup", "The whole group"], 0, "Gromov/RhoAbelian.lean lines 625–626."),
 ],
 "WordDist": [
  q("Is the word metric symmetric?", ["Yes", "No"], 0, "WordDist_comm, Gromov/Defs/WordMetric.lean lines 177–180."),
  q("What is dist(x, y)?", ["The word length of y·x⁻¹", "The word length of x·y", "|x − y|"], 0, "Gromov/Defs/WordMetric.lean line 144."),
 ],
}
for n in NODES:
    n["quiz"].extend(EXTRA2.get(n["id"], []))
