NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]


node("AltCounter.exists_block_point", "The finite lemma: a 0/1 point with block determinant of norm ≥ 1",
 "On any block of even size there are 0/1 vectors x, y making the block of Λ_{pq}(a′ + x, b′ + y, a′ + x, b′ + y) have determinant of norm ≥ 1, whatever a′, b′ are. The reason is characteristic-2 algebra: summed over all 0/1 points, the determinant is 1.",
 r"""## Plain English

**Theorem (`exists_block_point`, AltCounter/FiniteLemma.lean lines 462–542).** Let 𝕜 be ultrametric of characteristic
2, and Λ_{pq} bounded 4-linear forms that are alternating in the last two slots, symmetric with zero diagonal in
(p, q), and satisfy the diagonal formula Λ_{pq}(a, a, x, y) = W(a x, a y)_{pq}. Fix an even n, a start s, and any
a′, b′ in ℓ^∞. Then there are x, y in 𝕜ⁿ with all ‖x_i‖, ‖y_i‖ ≤ 1 such that

> ‖det( Λ_{s+p, s+q}(a′ + x, b′ + y, a′ + x, b′ + y) )_{p,q<n}‖ ≥ 1,

where x and y are placed on the block [s, s + n) (`blockVec`, lines 20–27).

**The polynomial.** Make x and y formal variables X₀…X_{n−1}, Y₀…Y_{n−1}. Each entry is then a polynomial G_{pq} of
total degree ≤ 4 in 2n variables (`Gpoly`, lines 196–201). Write G = g + c, with g the degree-4 part (only the block
vectors) and c of degree ≤ 3 (it involves a′ or b′).

**The chain of facts.**

1. The matrix G is symmetric with zero diagonal, so in characteristic 2,
   det G = Σ over perfect matchings σ of (∏_{edges} G_e)² ([det_eq_sum_PM_sq](#/node/AltCounter.det_eq_sum_PM_sq)).
2. The degree-4 part g satisfies a **swap identity**, g_{pq}(Y, X) = g_{pq}(X, Y) + X_p²Y_q² + X_q²Y_p², and the
   **diagonal identity** g_{pq}(X, X) = 0 (lines 328–373). They follow from alternation and the diagonal formula by
   polarisation in characteristic 2 (`char2_key`, `alt_symm`, lines 302–324).
3. Those identities force every matching product ∏ g_e to have coefficient **1** at the balanced monomial
   ∏_i X_i Y_i ([coeff_bal_prod_matching](#/node/AltCounter.coeff_bal_prod_matching)). The lower-degree part c does
   not change that coefficient (`coeff_bal_pfTerm_perturb`, AltCounter/Balanced.lean lines 358–432).
4. [exists_cubePt_norm_det_ge_one](#/node/AltCounter.exists_cubePt_norm_det_ge_one) turns this into a 0/1 point with
   ‖det G‖ ≥ 1.

The point x, y does depend on a′ and b′. This is why the gluing builds blocks one at a time.
""",
 [q("What kind of vectors x, y does the lemma produce?",
    ["Arbitrary vectors", "Vectors with entries of norm ≤ 1; the proof actually finds 0/1 entries", "Unit vectors e_i"], 1,
    "The statement promises ‖x_i‖, ‖y_i‖ ≤ 1 (AltCounter/FiniteLemma.lean line 475); the witness is a hypercube point cubePt S."),
   q("Why must the block size n be even?",
    ["A set of odd size has no perfect matchings, so det G would be 0 in characteristic 2", "To make C ≥ 1", "It doesn't need to be"], 0,
    "hn : Even n (line 474); card_PM_odd needs even cardinality."),
   q("Why does the lower-degree part c not matter?",
    ["It is zero", "The balanced monomial has the top degree 2n, and c only lowers degrees", "Because a′ = b′ = 0"], 1,
    "coeff_bal_pfTerm_perturb, AltCounter/Balanced.lean lines 358–432."),
   q("Which hypotheses of core_false does the lemma use?",
    ["Only finite-rank approximation", "Alternation, the diagonal formula, symmetry and zero diagonal", "Only the tail property"], 1,
    "halt, hdiag, hsymm, hzero (AltCounter/FiniteLemma.lean lines 469–473).")],
 caveats=["The upstream original notes prove a different, 'border' form of this identity with an extra residue-field hypothesis. The Lean uses the simplified even-block form plus the hypercube sum, which needs no residue-field hypothesis. The upstream formalization.yaml records this divergence."],
 widgets=walk("How the proof goes (AltCounter/FiniteLemma.lean lines 467–542)", [
    {"text": "Symmetry and zero diagonal of the polynomial matrix, from hsymm and hzero (lines 480–489)."},
    {"text": "Split each entry into its degree-4 part g (c = 0) and a remainder of degree ≤ 3 (lines 490–494)."},
    {"text": "The swap and diagonal identities for g (lines 495–501).", "link": "AltCounter.coeff_bal_prod_matching"},
    {"text": "Every matching product of the full matrix has balanced coefficient 1: first strip the remainder, then apply the key identity (lines 505–515).",
     "lean": "exact coeff_bal_prod_matching (blockFam Λ s a' b' 0 n) hgswap hgdiagz σ hσ"},
    {"text": "Each entry has total degree ≤ 4 (lines 516–523)."},
    {"text": "The hypercube sum gives a point z with ‖det‖ ≥ 1 (lines 524–528).", "link": "AltCounter.exists_cubePt_norm_det_ge_one",
     "lean": "exists_cubePt_norm_det_ge_one (blockFam Λ s a' b' 1 n) hGsymm hGdiag hgdeg hperturb"},
    {"text": "Split z into x and y and evaluate the polynomial determinant back to the actual block determinant (lines 529–542)."}]))


node("AltCounter.exists_cubePt_norm_det_ge_one", "From coefficients to a point: the hypercube trick",
 "If G is a symmetric zero-diagonal matrix of degree-≤4 polynomials in 2n variables (n even) and every matching product has balanced coefficient 1, then det G, summed over all 0/1 points, is 1. By the ultrametric inequality, some 0/1 point has ‖det G‖ ≥ 1.",
 r"""## Plain English

**Theorem (`exists_cubePt_norm_det_ge_one`, AltCounter/FiniteLemma.lean lines 406–460).** Over an ultrametric field
of characteristic 2, let G be a symmetric, zero-diagonal matrix indexed by a finite ι of even size, whose entries are
polynomials of total degree ≤ 4 in the variables X_i, Y_i (i in ι). Suppose every matching product has coefficient 1
at ∏_i X_i Y_i. Then some point z with every ‖z_i‖ ≤ 1 has ‖det G(z)‖ ≥ 1.

**Proof, in five lines.**

1. det G = Σ_σ (∏_{e∈σ} G_e)², a sum over perfect matchings σ ([det_eq_sum_PM_sq](#/node/AltCounter.det_eq_sum_PM_sq)).
2. A matching of |ι| points has |ι|/2 edges. So ∏_{e∈σ} G_e has degree ≤ 4 · |ι|/2 = 2|ι|, the number of variables
   (`totalDegree_pfTerm_le`, lines 388–404).
3. The [hypercube sum](#/node/AltCounter.sum_eval_cubePt): summing such a polynomial over all 0/1 points gives its
   coefficient at the all-ones monomial, here 1.
4. Squaring is additive in characteristic 2 (Frobenius), so Σ_z det G(z) = Σ_σ (Σ_z ∏ G_e(z))² = Σ_σ 1 = the number
   of perfect matchings. That number, (|ι| − 1)!!, is odd (`card_PM_odd`), so the sum is 1.
5. In an ultrametric field, a finite sum of norm 1 has a term of norm ≥ 1. That term is the point.

The point found is a 0/1 vector (the indicator of a subset), so ‖z_i‖ ≤ 1 holds automatically.
""",
 [q("Why is the degree bound 'at most the number of variables' needed?",
    ["The hypercube sum identity only holds under that bound", "To keep norms ≤ 1", "It is not needed"], 0,
    "sum_eval_cubePt has hypothesis hf : totalDegree ≤ card σ (AltCounter/Hypercube.lean line 80)."),
   q("Where is Frobenius additivity used?",
    ["To move the hypercube sum inside the squares: Σ (f(z))² = (Σ f(z))²", "To show G is symmetric", "Nowhere"], 0,
    "sum_pow_char at AltCounter/FiniteLemma.lean line 444."),
   q("Why does an odd count give sum 1?", ["In characteristic 2, an odd number equals 1", "Because det = 1", "It doesn't"], 0,
    "card_PM_odd, then CharTwo.two_eq_zero (AltCounter/FiniteLemma.lean lines 447–450)."),
   q("How is the single good point chosen?",
    ["Explicitly as x = y = 1", "By the ultrametric inequality: some summand has norm ≥ the norm of the sum", "Randomly"], 1,
    "IsUltrametricDist.exists_norm_finsetSum_le_of_nonempty (AltCounter/FiniteLemma.lean lines 451–453).")])


node("AltCounter.sum_eval_cubePt", "Hypercube sums in characteristic 2",
 "In characteristic 2, if a polynomial has total degree at most the number of variables, then the sum of its values over all 0/1 points equals its coefficient at the monomial x₁x₂⋯x_k. Every other monomial is 1 at an even number of points.",
 r"""## Plain English

**Theorem (`sum_eval_cubePt`, AltCounter/Hypercube.lean lines 76–125).** Over a commutative ring of characteristic 2,
let f be a polynomial in finitely many variables with total degree ≤ the number of variables, and m the monomial with
every exponent 1. Then

> Σ over all subsets S of the variables of f(1_S) = coefficient of m in f,

where 1_S (`cubePt`, lines 18–19) is 1 on S and 0 elsewhere.

**Why.** A monomial ∏_{i∈T} x_i^{e_i} with all e_i ≥ 1 is 1 at the point 1_S exactly when T ⊆ S. There are 2^(k−|T|)
such S, which is even unless T is all k variables. If T is everything and the degree is ≤ k, all e_i are 1, so the
monomial is m (`eq_of_support_eq_univ`, lines 59–74). So in characteristic 2 everything cancels except the
coefficient of m.

This replaced, in the upstream development, an older Gauss-norm argument that needed an infinite residue field (see
paper/COUNTEREXAMPLE.md).
""",
 [q("At how many 0/1 points is x₁x₂ equal to 1, with 4 variables?", ["1", "4", "2", "16"], 1,
    "Points with x₁ = x₂ = 1: 2^(4−2) = 4, an even number, so it contributes 0 in characteristic 2."),
   q("Which monomial survives the sum?", ["The constant 1", "x₁x₂⋯x_k (all exponents 1)", "All of them"], 1,
    "AltCounter/Hypercube.lean lines 79–81."),
   q("Why the degree hypothesis?", ["Otherwise e.g. x₁²x₂ ⋯ x_k would also touch every variable and survive", "To make f symmetric", "It isn't needed"], 0,
    "With degree ≤ k, a monomial touching all k variables has all exponents 1.")])


node("AltCounter.det_eq_sum_PM_sq", "Characteristic 2: a symmetric zero-diagonal determinant is a sum of squares",
 "In characteristic 2, the determinant of a symmetric matrix with zero diagonal equals Σ over perfect matchings of (product of entries along the matching)². It is the square of the Pfaffian, with no signs.",
 r"""## Plain English

**Theorem (`det_eq_sum_PM_sq`, AltCounter/Pfaffian.lean lines 124–144).** Over a commutative ring of characteristic
2, if B is symmetric with zero diagonal then

> det B = Σ_{σ ∈ PM} (pfTerm B σ)²,

where `PM` (lines 16–18) is the set of perfect matchings, encoded as fixed-point-free involutions, and
`pfTerm B σ` (lines 20–22) is the product of B_{i, σ(i)} over the edges {i, σ(i)} with i < σ(i).

**Why.** In characteristic 2 signs disappear. Pairing each permutation with its inverse cancels every permutation that
is not an involution: the two terms are equal by symmetry, so they sum to 0. Involutions with a fixed point vanish
because the diagonal is 0. A fixed-point-free involution σ contributes ∏_i B_{σ(i), i} = (∏_{edges} B_e)².

**Companion: `card_PM_odd`** (lines 219–228). A set of even size has an odd number of perfect matchings. The proof
is slick: the all-ones-off-the-diagonal matrix J over 𝔽₂ squares to the identity when the size is even, so det J = 1,
and by the formula above det J is the number of matchings mod 2.
""",
 [q("What is a perfect matching in this encoding?", ["Any permutation", "A permutation σ with σ∘σ = id and no fixed points", "A subset of edges"], 1,
    "PM, AltCounter/Pfaffian.lean lines 16–18."),
   q("Why do non-involutions cancel?", ["σ and σ⁻¹ give equal terms (B symmetric), and x + x = 0", "Their signs are −1", "They don't"], 0,
    "sum_perm_eq_sum_involutions, AltCounter/Pfaffian.lean line 70."),
   q("How many perfect matchings does a 4-element set have, and is it odd?", ["3, odd", "2, even", "6, even"], 0,
    "(4 − 1)!! = 3, consistent with card_PM_odd.")])


node("AltCounter.coeff_bal_prod_matching", "The key identity: every matching product has balanced coefficient 1",
 "If polynomials g_{pq} satisfy the swap identity g(Y, X) = g(X, Y) + X_p²Y_q² + X_q²Y_p² and vanish when Y = X, then for every perfect matching, the product of the g along its edges has coefficient exactly 1 at ∏_i X_i Y_i. This is where the specific form of the diagonal values W(a x, a y) enters.",
 r"""## Plain English

**Theorem (`coeff_bal_prod_matching`, AltCounter/Balanced.lean lines 306–356).** Over a ring of characteristic 2, let
g_{pq} be polynomials in variables X_i, Y_i with, for p ≠ q,

- **swap identity:** swapping X ↔ Y in g_{pq} gives g_{pq} + (X_pY_q)² + (X_qY_p)²;
- **diagonal identity:** substituting Y_i := X_i in g_{pq} gives 0.

Then for every perfect matching σ, the product of g_{i,σ(i)} over its edges has coefficient 1 at the "balanced"
monomial `bal univ` = ∏_i X_i Y_i (lines 18–20).

**Proof sketch** (the comments (i)–(iv) in the source):

- Put g′_e = g_e + (X_iY_{σ(i)})² on each edge e = {i, σ(i)}. Adding a square never changes the balanced coefficient,
  because the balanced monomial has every exponent 1 (`coeff_bal_prod_add`).
- The product of the g′ is **swap-invariant**: the extra squares exactly absorb the swap identity's error terms, in
  characteristic 2 (lines 329–341).
- For a swap-invariant polynomial in characteristic 2, the balanced coefficient equals the coefficient of ∏_i X_i²
  after setting Y = X (`coeff_bal_of_swap_invariant`, lines 197–276). Monomials other than the balanced one come in
  swapped pairs and cancel.
- After Y = X, each g′_e becomes (X_i X_{σ(i)})², and the product over a perfect matching is exactly ∏_i X_i², with
  coefficient 1 (lines 342–356).
""",
 [q("What is the balanced monomial?", ["∏ X_i²", "∏ X_i Y_i", "∏ Y_i²", "X_1 Y_2"], 1,
    "bal, AltCounter/Balanced.lean lines 18–20."),
   q("Why add (X_iY_{σ(i)})² to each factor?", ["To make the product swap-invariant without changing the balanced coefficient", "To raise the degree", "To make it symmetric in p, q"], 0,
    "key1 and hsw, AltCounter/Balanced.lean lines 318–341."),
   q("Where do the swap and diagonal identities come from in the application?",
    ["From alternation and the diagonal formula W(a x, a y) of Λ", "From the tail property", "From finite rank"], 0,
    "swapXY_Gpoly_zero and diagXY_Gpoly_zero, AltCounter/FiniteLemma.lean lines 328–373.")],
 caveats=["The middle step (swap-invariant ⇒ read the coefficient after Y = X) is explained from the docstring and comments; its 80-line proof was skimmed, not traced."])
