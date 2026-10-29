NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}


node("AltCounter.PM", "PM: perfect matchings as fixed-point-free involutions",
 "A perfect matching of a finite set is encoded as a permutation σ with σ∘σ = id and no fixed points: σ pairs each i with its partner σ(i).",
 r"""## Plain English

**Definition (`PM`, AltCounter/Pfaffian.lean lines 16–18).** The finite set of permutations σ of α with σ * σ = 1 and
σ(i) ≠ i for every i. Each such σ splits α into pairs {i, σ(i)}, which is a perfect matching. Conversely, every
perfect matching gives one such σ.

A set of size 2m has (2m − 1)!! = 1 · 3 · 5 ⋯ (2m − 1) perfect matchings, an odd number (`card_PM_odd`,
lines 219–228). See [det_eq_sum_PM_sq](#/node/AltCounter.det_eq_sum_PM_sq).
""",
 [q("Which permutation of {1,2,3,4} is in PM?", ["(1 2)(3 4)", "(1 2 3 4)", "the identity", "(1 2)"], 0,
    "It is an involution with no fixed points."),
   q("How many perfect matchings does a set of size 6 have?", ["15", "6", "8"], 0, "5 · 3 · 1 = 15."),
   q("Can a set of odd size have a perfect matching?", ["Yes", "No"], 1, "Pairs cover an even number of points.")])


node("AltCounter.pfTerm", "pfTerm: the product of a matrix along a matching",
 "pfTerm B σ multiplies the entries B_{i, σ(i)} over the edges of the matching σ, taking each edge once (from its smaller end). Summing pfTerm over matchings gives the Pfaffian, up to sign.",
 r"""## Plain English

**Definition (`pfTerm`, AltCounter/Pfaffian.lean lines 20–22).** For a matrix B and a permutation σ,

> pfTerm B σ = ∏ over i with i < σ(i) of B_{i, σ(i)}.

For a [perfect matching](#/node/AltCounter.PM), that is one factor per edge. Over a ring of characteristic 2 signs do
not matter, and Σ_σ pfTerm B σ is the Pfaffian of B. The project uses the squares:
det B = Σ_σ (pfTerm B σ)² ([det_eq_sum_PM_sq](#/node/AltCounter.det_eq_sum_PM_sq)).
""",
 [q("For σ = (1 2)(3 4), what is pfTerm B σ?", ["B₁₂ · B₃₄", "B₁₂ + B₃₄", "B₁₂ B₂₁ B₃₄ B₄₃"], 0, "One factor per edge, taken from the smaller endpoint."),
   q("Why the condition i < σ(i)?", ["So each edge is counted once", "To make B symmetric", "It selects fixed points"], 0, "AltCounter/Pfaffian.lean line 22."),
   q("What is det B in terms of pfTerm, for symmetric zero-diagonal B in characteristic 2?", ["Σ_σ (pfTerm B σ)²", "∏_σ pfTerm B σ", "pfTerm B id"], 0,
    "AltCounter/Pfaffian.lean lines 124–126.")])


node("AltCounter.bal", "bal: the balanced squarefree monomial ∏ X_i Y_i",
 "With variables X_i and Y_i (written inl i and inr i), bal S is the monomial ∏_{i∈S} X_i Y_i: every variable of S appears exactly once, in both colours. The key identity says every matching product has coefficient 1 here.",
 r"""## Plain English

**Definition (`bal`, AltCounter/Balanced.lean lines 18–20).** An exponent vector on the variables ι ⊕ ι, with
exponent 1 at X_i = `inl i` and at Y_i = `inr i` for i in S, and 0 elsewhere. For S = everything, it is the all-ones
monomial, which the [hypercube sum](#/node/AltCounter.sum_eval_cubePt) picks out.

"Balanced" because it has the same degree in the X's and in the Y's, and it is unchanged by swapping X ↔ Y.
""",
 [q("What is bal {1, 2}?", ["X₁Y₁X₂Y₂", "X₁²X₂²", "X₁Y₂"], 0, "AltCounter/Balanced.lean line 20."),
   q("Is bal S changed by the swap X ↔ Y?", ["No", "Yes"], 0, "Each X_i is paired with Y_i (mapDomain_swap_bal, AltCounter/Balanced.lean line 111)."),
   q("What is the largest exponent in bal S?", ["1", "2", "|S|"], 0, "bal_apply_le_one, AltCounter/Balanced.lean line 64.")])


node("AltCounter.cubePt", "cubePt: the 0/1 point of a subset",
 "cubePt S is the point that is 1 on the variables in S and 0 elsewhere: a vertex of the hypercube. Summing over all S visits every vertex once.",
 r"""## Plain English

**Definition (`cubePt`, AltCounter/Hypercube.lean lines 18–19).** For a finite set S of variables, cubePt S is the
function equal to 1 on S and 0 off S. The 2^k subsets of k variables give the 2^k vertices of the cube {0, 1}^k.

The [finite lemma](#/node/AltCounter.exists_block_point) finds its good point among these vertices. The entries are 0
or 1, so their norms are ≤ 1.
""",
 [q("How many points cubePt S are there with 4 variables?", ["4", "8", "16"], 2, "One per subset: 2⁴."),
   q("What is cubePt ∅?", ["The zero point", "The all-ones point"], 0, "AltCounter/Hypercube.lean line 19."),
   q("Why is ‖z_i‖ ≤ 1 automatic for z = cubePt S?", ["Entries are 0 or 1", "Because the field is complete"], 0,
    "AltCounter/FiniteLemma.lean lines 455–457.")])


node("AltCounter.blockVec", "blockVec: a finite vector placed on a block of ℓ^∞",
 "blockVec s x is the sequence that equals x_i at position s + i for i < n and 0 elsewhere. It is how a finite vector from the finite lemma becomes an element of ℓ^∞ on the block [s, s + n).",
 r"""## Plain English

**Definition (`blockVec`, AltCounter/FiniteLemma.lean lines 20–27).** For x in 𝕜ⁿ and a start s, `blockVec s x` is
the bounded sequence that is x_i at index s + i and 0 outside [s, s + n). If all ‖x_i‖ ≤ 1 then ‖blockVec s x‖ ≤ 1
(lines 53–56). Adding it to a vector that already vanishes from s on keeps the norm ≤ 1 (lines 58–67).

The unit vector e_i used in [NSC](#/node/AltCounter.NSC) is `blockVec i (1)`.
""",
 [q("Where is blockVec s x nonzero?", ["Only on [s, s + n)", "Everywhere", "Only at 0"], 0, "blockVec_apply_of_lt / _of_ge, AltCounter/FiniteLemma.lean lines 38–45."),
   q("How is the unit vector e_i expressed?", ["blockVec i (fun _ => 1)", "blockVec 0 i", "It is not"], 0, "basisVec, AltCounter/PhillipsOne.lean line 114."),
   q("Does adding blockVec s x to a vector vanishing from s on increase the norm beyond 1?", ["No, if both have norm ≤ 1", "Yes"], 0,
    "norm_add_blockVec_le, AltCounter/FiniteLemma.lean lines 58–67.")])


node("AltCounter.Stage", "Stage: one step of the gluing construction",
 "A Stage records the vectors A, B built so far, the last block on which the block determinant has norm ≥ 1, and a threshold M past which that block's forms are tiny. core_false iterates stages forever.",
 r"""## Plain English

**Structure (`Stage`, AltCounter/Gluing.lean lines 53–78).** Fields:

- `s`, `M`, `n`, `start`: A and B vanish from s on; the next block must start at or after M; the latest block is
  [start, start + n);
- `A`, `B` with ‖A‖, ‖B‖ ≤ 1 and A_k = B_k = 0 for k ≥ s;
- `hdet`: the n × n block (Λ_{start+i, start+j}(A, B, A, B)) has determinant of norm ≥ 1;
- `hsmall`: every Λ_{start+i, start+j} is ≤ 1/(8Cⁿ) on unit-ball arguments, one of which vanishes below M.

`Stage.init` (lines 80–94) is the empty stage. The step is
[exists_stage_step](#/node/AltCounter.exists_stage_step), and [core_false](#/node/AltCounter.core_false) iterates it.
""",
 [q("What does the threshold M guarantee?", ["The last block's forms are tiny when an argument vanishes below M", "A and B vanish below M", "M = s"], 0,
    "hsmall, AltCounter/Gluing.lean lines 75–78."),
   q("What is the block size of the initial stage?", ["0 (empty block)", "2", "1"], 0, "Stage.init, n := 0 (AltCounter/Gluing.lean line 84)."),
   q("Why is the empty block's determinant ≥ 1?", ["The determinant of a 0 × 0 matrix is 1", "It isn't"], 0, "Matrix.det_fin_zero, AltCounter/Gluing.lean line 93.")])
