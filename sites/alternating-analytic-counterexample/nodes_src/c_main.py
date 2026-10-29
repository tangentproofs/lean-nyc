NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]


node("AltCounter.not_analyticAt_Q",
 "Headline: Q is not analytic at 0 (given the tail property)",
 "Over an ultrametric field of characteristic 2 with the tail property, Q is not analytic at 0. Otherwise its degree-2 coefficient would be a bounded bilinear lift, and evaluating it on multiplication operators and W₀ would give a family of 4-linear forms that cannot exist.",
 r"""## Plain English

**Theorem (`not_analyticAt_Q`, AltCounter/Main.lean lines 348–469).** Let 𝕜 be a nontrivially normed field that is
ultrametric and of characteristic 2, and assume the [tail property](#/node/AltCounter.TailProperty). Then
[Q](#/node/AltCounter.Q) is **not** analytic at 0.

`not_contDiff_omega_Q` (lines 471–474) adds the one-line consequence: Q is not `ContDiff 𝕜 ω`, because C^ω would
make Q analytic at every point, including 0.

This is **CONDITIONAL** on `TailProperty 𝕜`. The condition is then discharged for a real field:
[not_contDiff_omega_Q_of_NSC](#/node/AltCounter.not_contDiff_omega_Q_of_NSC) replaces it by NSC, and
[exists_field](#/node/AltCounter.exists_field) gives a field with NSC.

**The idea in three moves.**

1. **Analytic ⇒ bilinear lift.** Q is homogeneous of degree 2, so if it is analytic at 0 its power series is just its
   degree-2 term. That term is a bounded bilinear P with P(f, f) = Q(f)
   ([exists_bilinear_of_analyticAt_of_homogeneous](#/node/AltCounter.exists_bilinear_of_analyticAt_of_homogeneous)).
   This step works in any characteristic.
2. **Bilinear lift ⇒ 4-linear family.** Put M(a, b) = P(m_a, m_b)(W₀), using
   [multiplication operators](#/node/AltCounter.mulL) and the 2-form [W₀](#/node/AltCounter.W₀). Then M(a, b) is an
   alternating 2-form with values in [F](#/node/AltCounter.F). Its matrix entries
   Λ_{pq}(a, b, x, y) = M(a, b)(x, y)_{pq} are bounded 4-linear forms.
3. **That family cannot exist.** The family has exactly the five properties that
   [core_false](#/node/AltCounter.core_false) forbids:
   - (i) alternating in (x, y), because M(a, b) is an alternating form;
   - (ii) on the diagonal a = b it is Q(m_a)(W₀), so Λ_{pq}(a, a, x, y) = W(a x, a y)_{pq};
   - (iii) symmetric with zero diagonal in (p, q), and (iv) nearly finite rank, because every value lies in F.
""",
 [q("Which hypothesis makes this theorem conditional?",
    ["CharP 𝕜 2", "TailProperty 𝕜", "CompleteSpace 𝕜", "None"], 1,
    "TailProperty 𝕜 is an explicit argument (AltCounter/Main.lean line 350). Ultrametricity and characteristic 2 are properties of the field, also assumed, but the field built later has them."),
   q("What is the first step from 'Q analytic at 0'?",
    ["Q is constant", "Q has a bounded bilinear lift P with P(f, f) = Q(f)", "Q is linear", "Q is injective"], 1,
    "AltCounter/Main.lean lines 352–353 call exists_bilinear_of_analyticAt_of_homogeneous."),
   q("Which operators f are plugged into the bilinear lift?",
    ["Arbitrary operators", "Multiplication operators m_a", "Shifts", "Projections"], 1,
    "M a b = P ![mulL a, mulL b] W₀ (AltCounter/Main.lean lines 354–355)."),
   q("Why is the 4-linear family symmetric with zero diagonal in (p, q)?",
    ["Because every value lies in F, whose elements are symmetric with zero diagonal in characteristic 2",
     "Because P is symmetric", "Because Λ is alternating in (a, b)"], 0,
    "AltCounter/Main.lean lines 461–466 use FSub_symm and FSub_diag.")],
 caveats=["CONDITIONAL on TailProperty 𝕜. The headlines in Solution.lean are unconditional because the condition is proved for the constructed field.",
          "Non-analyticity is proved at the base point 0 only. The upstream notes reduce other base points to 0 on paper; that reduction is not formalized. Failure at 0 already refutes C^ω.",
          "The bilinear lift P need not be symmetric. Only bilinearity and P(f, f) = Q(f) are used."],
 widgets=walk("How the proof goes (AltCounter/Main.lean lines 348–469)", [
    {"text": "Assume Q is analytic at 0 and get a bounded bilinear P with P(f, f) = Q(f) (lines 351–353).", "link": "AltCounter.exists_bilinear_of_analyticAt_of_homogeneous",
     "lean": "exists_bilinear_of_analyticAt_of_homogeneous (Q 𝕜) (fun c f => Q_homogeneous 𝕜 c f) hQ"},
    {"text": "Define M(a, b) = P(m_a, m_b)(W₀) (lines 354–355).", "link": "AltCounter.mulL",
     "lean": "∀ a b, M a b = (P ![mulL 𝕜 a, mulL 𝕜 b]) (W₀ 𝕜) := ⟨_, fun _ _ => rfl⟩"},
    {"text": "M is additive and homogeneous in a and in b, since P is multilinear (lines 357–376), and ‖M(a, b)‖ ≤ ‖P‖‖W₀‖‖a‖‖b‖ (lines 378–390)."},
    {"text": "Apply core_false to Λ_{pq}(a, b, x, y) = M(a, b)(x, y)_{pq}, with constant max(1, ‖P‖‖W₀‖) (lines 392–394).", "link": "AltCounter.core_false",
     "lean": "refine core_false htail"},
    {"text": "Bounded 4-linearity (lines 395–444): each of the nine IsBdd4 fields, from multilinearity of P and of M(a, b).", "link": "AltCounter.IsBdd4"},
    {"text": "Alternating in (x, y) because M(a, b) is an alternating map (lines 445–450)."},
    {"text": "Diagonal values: M(a, a) = Q(m_a)(W₀), whose entries are W(a x, a y)_{pq} (lines 451–460).", "link": "AltCounter.W₀",
     "lean": "have h : M a a = (Q 𝕜 (mulL 𝕜 a)) (W₀ 𝕜) := by rw [hM, hconst, hP]"},
    {"text": "Symmetry, zero diagonal and finite-rank approximation all come from membership in F (lines 461–469).", "link": "AltCounter.FSub"}]))


node("AltCounter.not_contDiff_omega_Q_of_NSC", "Q is not C^ω, assuming only NSC",
 "Replacing the tail property by NSC: over a complete ultrametric field of characteristic 2 in which functionals on ℓ^∞ that kill all unit vectors are zero, Q is neither analytic at 0 nor C^ω.",
 r"""## Plain English

**Theorems (AltCounter/MainNSC.lean lines 13–22).** Let 𝕜 be complete, ultrametric and of characteristic 2, and
assume [NSC](#/node/AltCounter.NSC). Then

- `not_analyticAt_Q_of_NSC` (lines 15–17): Q is not analytic at 0;
- `not_contDiff_omega_Q_of_NSC` (lines 20–22): Q is not `ContDiff 𝕜 ω`.

Each is a one-liner: [tailProperty_of_NSC](#/node/AltCounter.tailProperty_of_NSC) turns NSC into the tail property,
and [not_analyticAt_Q](#/node/AltCounter.not_analyticAt_Q) does the rest.

This form is closest to the paper's Theorem: NSC is the classical condition (ℓ^∞ / c₀)′ = 0, which for complete
non-archimedean fields is equivalent to not being spherically complete (van der Put). The
[headlines](#/node/AlternatingAnalyticChallenge.false_of_contDiff_omega_compContinuousLinearMapCLM) use the C^ω version.
""",
 [q("What extra hypothesis does this version need compared with not_analyticAt_Q?",
    ["None", "Completeness of 𝕜, which the tail-property proof uses; NSC replaces TailProperty", "Finite dimension"], 1,
    "The section variables include CompleteSpace 𝕜 (AltCounter/MainNSC.lean line 10); NSC replaces TailProperty."),
   q("Is this still conditional?", ["Yes, on NSC 𝕜, which exists_field + nsc_of_hasEmptyNestedBalls discharge for one field", "No"], 0,
    "hnsc : NSC 𝕜 is an argument (AltCounter/MainNSC.lean line 20).")],
 caveats=["CONDITIONAL on NSC 𝕜, discharged for the constructed field in AltCounter/Final.lean."])


node("AltCounter.exists_bilinear_of_analyticAt_of_homogeneous", "Analytic + degree-2 homogeneous ⇒ bilinear lift",
 "If a map Q between normed spaces satisfies Q(c f) = c² Q(f) and is analytic at 0, then Q(f) = P(f, f) for a bounded bilinear P, namely the degree-2 term of its power series. No division by 2 is involved, so this works in every characteristic.",
 r"""## Plain English

**Theorem (`exists_bilinear_of_analyticAt_of_homogeneous`, AltCounter/Criterion.lean lines 43–63).** Let Q : X → Z
satisfy Q(c · f) = c² · Q(f) for all scalars c, and be analytic at 0. Then there is a continuous bilinear map P
(a `ContinuousMultilinearMap` on two copies of X) with P(f, f) = Q(f) for every f.

**Proof idea.** Take the power series p of Q at 0 and let P = p₂, its degree-2 term. Fix y and restrict Q to the line
t ↦ t y. On one hand this restriction has the power series p composed with t ↦ t y. On the other hand it equals
t ↦ t² Q(y), whose power series is 0 except for t² Q(y) in degree 2. Power-series coefficients in one variable are
unique (Mathlib's `HasFPowerSeriesAt.eq_formalMultilinearSeries`, whose proof uses no factorials). So
p₂(y, y) = Q(y).

**Why this matters in characteristic 2.** Analyticity hands you a bilinear lift for free. In characteristic 2 a
degree-2 map need not have a bounded bilinear lift, and the counterexample shows that Q has none. So Q cannot be
analytic.
""",
 [q("What is P in the proof?", ["Polarisation (Q(f+g) − Q(f) − Q(g)) / 2", "The degree-2 term p 2 of Q's power series at 0", "The derivative of Q"], 1,
    "refine ⟨p 2, …⟩ (AltCounter/Criterion.lean line 47)."),
   q("Does the argument divide by 2?", ["Yes", "No: it uses uniqueness of one-variable power series coefficients"], 1,
    "AltCounter/Criterion.lean line 58.")],
 widgets=walk("How the proof goes (AltCounter/Criterion.lean lines 43–63)", [
    {"text": "Get a power series p for Q at 0 and propose P = p 2.", "lean": "refine ⟨p 2, fun y => ?_⟩"},
    {"text": "Restrict to the line t ↦ t • y with a continuous linear map u.", "lean": "have h1 : HasFPowerSeriesAt (Q ∘ u) (p.compContinuousLinearMap u) 0 :="},
    {"text": "On that line Q is t ↦ t² Q(y), by homogeneity.", "lean": "have h2 : (Q ∘ u) = fun t : 𝕜 => t ^ 2 • Q y := by"},
    {"text": "Compare coefficients with the explicit series of t² Q(y) (sqSeries, lines 18–41).", "lean": "have heq := h1.eq_formalMultilinearSeries (hasFPowerSeriesAt_sqSeries (Q y))"},
    {"text": "Evaluate the degree-2 coefficients at (1, 1): p₂(y, y) = Q(y) (lines 59–63)."}]))


node("AltCounter.core_false",
 "Headline: the core contradiction",
 "No bounded family of 4-linear forms Λ_{pq} on ℓ^∞ can be alternating, equal W(a x, a y)_{pq} when a = b, be symmetric with zero diagonal, and have nearly-finite-rank values. Gluing larger and larger blocks gives determinants ≥ 1; finite rank forces them to be small.",
 r"""## Plain English

**Theorem (`core_false`, AltCounter/Gluing.lean lines 233–399).** Let 𝕜 be ultrametric, of characteristic 2, with the
[tail property](#/node/AltCounter.TailProperty). Let Λ_{pq} (for p, q in ℕ) be 4-linear forms on ℓ^∞, all bounded by
the same C ≥ 1 ([IsBdd4](#/node/AltCounter.IsBdd4)), such that

1. **alternating:** Λ_{pq}(a, b, x, x) = 0;
2. **diagonal values:** Λ_{pq}(a, a, x, y) = a_p x_p a_q y_q + a_p y_p a_q x_q, i.e. W(a x, a y)_{pq};
3. **symmetric:** Λ_{pq} = Λ_{qp}; **zero diagonal:** Λ_{pp} = 0;
4. **finite-rank approximable:** for fixed a, b, x, y and η > 0, the matrix (Λ_{pq}(a, b, x, y))_{p,q} is within η,
   entrywise, of a finite sum of rank-1 matrices.

Then `False`.

**The strategy.**

- **Large blocks.** On any block of 2k consecutive indices, the [finite lemma](#/node/AltCounter.exists_block_point)
  finds 0/1-valued vectors x, y on that block such that the 2k × 2k block of the matrix
  (Λ_{pq}(A, B, A, B)) has determinant of norm ≥ 1, where A, B are the old vectors plus x, y.
- **Gluing.** Do this for blocks of size 2, 4, 6, …, each placed far enough out that, by the tail property, it does
  not disturb the earlier blocks ([exists_stage_step](#/node/AltCounter.exists_stage_step)). The limit vectors A, B
  still give every block determinant of norm ≥ 1
  ([one_le_norm_det_block](#/node/AltCounter.one_le_norm_det_block)).
- **Contradiction.** Hypothesis 4 for (A, B, A, B) with η = 1/(2C) gives a rank r. A matrix with entries bounded by C
  that is η-close to rank r has determinant at most C^r η^{N−r}
  ([norm_det_le_of_close_to_lowrank](#/node/AltCounter.norm_det_le_of_close_to_lowrank)). For the block of size
  N = 2(r + 1) that is C^r / (2C)^{r+2} < 1. But that block's determinant has norm ≥ 1.
""",
 [q("Which hypothesis forces block determinants to be small?",
    ["Alternation", "Finite-rank approximation (hypothesis 4)", "Symmetry", "The diagonal formula"], 1,
    "AltCounter/Gluing.lean lines 370–399 use happrox with η = 1/(2C)."),
   q("Which hypothesis forces some block determinant to be large?",
    ["Only the tail property",
     "Alternation, the diagonal formula and symmetry/zero diagonal, via the finite lemma in characteristic 2",
     "Finite-rank approximation"], 1,
    "exists_block_point uses halt, hdiag, hsymm, hzero (AltCounter/Gluing.lean line 126)."),
   q("What role does the tail property play?",
    ["It makes the blocks independent: later blocks, placed far out, barely change earlier block determinants",
     "It gives the finite-rank approximation", "None"], 0,
    "exists_stage_step chooses the next threshold M′ from htail (AltCounter/Gluing.lean lines 132–134)."),
   q("Which block size gives the contradiction when the approximating rank is r?",
    ["r", "2(r + 1)", "r + 1", "Any size"], 1,
    "seq (r + 1) has n = 2(r + 1) (AltCounter/Gluing.lean line 376), and n − r = r + 2 (line 388).")],
 caveats=["CONDITIONAL on TailProperty 𝕜 (discharged for the constructed field).",
          "The theorem is about an abstract family Λ. Its link to analyticity is made in not_analyticAt_Q."],
 widgets=walk("How the proof goes (AltCounter/Gluing.lean lines 239–399)", [
    {"text": "Pick a step function from exists_stage_step and iterate it from the empty stage (lines 249–254).", "link": "AltCounter.exists_stage_step",
     "lean": "choose f hf using exists_stage_step Λ C htail hC hlin halt hdiag hsymm hzero"},
    {"text": "Stage t + 1 adds a block of size 2(t + 1) beyond the previous threshold; the supports grow and the stage vectors agree on earlier coordinates (lines 255–304)."},
    {"text": "Define the limit vectors A, B coordinatewise; they have norm ≤ 1, agree with each stage below its threshold, and differ from it by norm ≤ 1 (lines 305–359)."},
    {"text": "Each block of the limit still has determinant of norm ≥ 1 (lines 360–369).", "link": "AltCounter.one_le_norm_det_block",
     "lean": "refine one_le_norm_det_block Λ C hC hlin (seq (t + 1)).n (seq (t + 1)).start (seq (t + 1)).M"},
    {"text": "Finite-rank approximation of (Λ_{pq}(A, B, A, B)) with η = 1/(2C) gives rank r (lines 370–375).",
     "lean": "obtain ⟨r, u, v, huv⟩ := happrox A B A B (1 / (2 * C)) hηpos"},
    {"text": "On block r + 1 (size 2(r + 1)) the determinant is ≤ C^r (1/(2C))^{r+2} (lines 376–389).", "link": "AltCounter.norm_det_le_of_close_to_lowrank"},
    {"text": "That number is < 1, contradicting the lower bound (lines 390–399)."}]))


node("AltCounter.exists_stage_step", "The gluing step: add one more block",
 "From a stage (vectors A, B and a threshold M beyond which the last block's forms are tiny), produce the next stage: put the finite lemma's 0/1 vectors on a new block of size 2(t + 1) starting at M, then use the tail property to choose a new threshold.",
 r"""## Plain English

**Structure (`Stage`, AltCounter/Gluing.lean lines 53–78).** A stage records:

- vectors A, B of norm ≤ 1, zero from position s on;
- the latest block, of size n starting at `start`, on which det(Λ_{start+i, start+j}(A, B, A, B))_{i,j} has norm ≥ 1;
- a threshold M ≥ s such that every form Λ_{start+i, start+j} of that block is ≤ 1/(8Cⁿ) on unit-ball arguments
  when one argument vanishes below M.

**Theorem (`exists_stage_step`, AltCounter/Gluing.lean lines 108–173).** Given a stage and t, there is a new stage
whose block has size 2(t + 1), starts at or after the old M, and whose vectors agree with the old ones before the new
block.

**How.**

1. Place the block at start = M. The old A, B vanish there.
2. [exists_block_point](#/node/AltCounter.exists_block_point) gives x, y with entries of norm ≤ 1 on the block such
   that, with A′ = A + x and B′ = B + y, the block determinant has norm ≥ 1.
3. A′, B′ still have norm ≤ 1, by the ultrametric inequality and disjoint supports.
4. For each of the finitely many pairs (i, j) in the block, the [tail property](#/node/AltCounter.TailProperty) gives
   a threshold N(i, j). Take M′ = max(start + n, max N(i, j)).

The bound 1/(8Cⁿ) is chosen so that, later, [one_le_norm_det_add](#/node/AltCounter.one_le_norm_det_add) keeps the
determinant ≥ 1 when the far-out tail changes.
""",
 [q("Where does the new block start?", ["At 0", "At the old threshold M", "Anywhere"], 1,
    "start := st.M (AltCounter/Gluing.lean line 122)."),
   q("Why are only finitely many thresholds needed per step?",
    ["Because the block is finite: one threshold per pair (i, j)", "Because the tail property gives a uniform N for all forms", "Because C is fixed"], 0,
    "choose N hN over Fin n × Fin n, then M′ = max(…) (AltCounter/Gluing.lean lines 132–134).")])


node("AltCounter.one_le_norm_det_block", "Changing far-out coordinates keeps the block determinant large",
 "If A, B agree with the stage vectors A₀, B₀ below the threshold M, then the block determinant for (A, B) still has norm ≥ 1. Each entry moves by at most 1/(8Cⁿ), and in an ultrametric field that is too little to change a determinant of norm ≥ 1.",
 r"""## Plain English

**Theorem (`one_le_norm_det_block`, AltCounter/Gluing.lean lines 179–230).** Suppose the n × n block with entries
Λ_{start+i, start+j}(A₀, B₀, A₀, B₀) has determinant of norm ≥ 1, the differences A − A₀ and B − B₀ vanish below M, and
the block's forms are ≤ 1/(8Cⁿ) whenever an argument vanishes below M. Then the block for (A, B, A, B) also has
determinant of norm ≥ 1.

**Why.** `IsBdd4.decomp` (lines 33–45) writes Λ(A, B, A, B) − Λ(A₀, B₀, A₀, B₀) as four terms, each with one argument
equal to A − A₀ or B − B₀. By the threshold, each is ≤ 1/(8Cⁿ), and by the ultrametric inequality so is the sum.
[one_le_norm_det_add](#/node/AltCounter.one_le_norm_det_add) then says a determinant of norm ≥ 1 survives such a
small perturbation.
""",
 [q("How large can each entry change be?", ["Up to C", "At most 1/(8Cⁿ)", "Unbounded"], 1,
    "hentry, AltCounter/Gluing.lean lines 203–213.")])


node("AltCounter.one_le_norm_det_add", "Ultrametric determinant stability",
 "Over an ultrametric field: if det G has norm ≥ 1, G's entries are ≤ C (C ≥ 1) and E's entries are ≤ ε with ε C^(N−1) < 1, then det(G + E) still has norm ≥ 1.",
 r"""## Plain English

**Theorem (`one_le_norm_det_add`, AltCounter/DetBounds.lean lines 100–144).** For N × N matrices G and E over an
ultrametric field, with ‖G_{ij}‖ ≤ C, C ≥ 1, ‖E_{ij}‖ ≤ ε ≤ 1, ε C^(N−1) < 1 and ‖det G‖ ≥ 1, we get
‖det(G + E)‖ ≥ 1.

**Why.** Expand det(G + E) column by column (`det_add_eq_sum_mixCols`, lines 44–72): it is det G plus terms in which
at least one column comes from E. Each such term has norm ≤ C^(N−1) ε < 1 (lines 74–99). In an ultrametric field, a
number of norm ≥ 1 plus things of norm < 1 still has norm ≥ 1.

Over ℝ this argument would need a factor 2^N for the number of terms. The ultrametric inequality removes it.
""",
 [q("Why is the ultrametric inequality essential?",
    ["It means a sum is no bigger than its largest term, so the number of terms doesn't matter", "It isn't", "It makes determinants multiplicative"], 0,
    "AltCounter/DetBounds.lean lines 103–144.")])


node("AltCounter.norm_det_le_of_close_to_lowrank", "Nearly low rank ⇒ small determinant",
 "Over an ultrametric field: if an N × N matrix with entries ≤ C is within η ≤ 1 of a matrix of rank ≤ r, then its determinant has norm at most C^r η^(N−r). Big blocks of a nearly-finite-rank matrix have tiny determinants.",
 r"""## Plain English

**Theorem (`norm_det_le_of_close_to_lowrank`, AltCounter/DetBounds.lean lines 146–207).** If ‖A_{ij}‖ ≤ C (C ≥ 1),
r ≤ N, and ‖A_{ij} − Σ_{k<r} u_k(i) v_k(j)‖ ≤ η ≤ 1 for all i, j, then ‖det A‖ ≤ C^r · η^(N−r).

**Why.** Write A = R + E with R the rank-≤-r part and ‖E_{ij}‖ ≤ η. Expanding the determinant column by column, any
term that takes more than r columns from R vanishes, because those columns are linearly dependent. So every surviving
term has at least N − r columns from E, and its norm is ≤ C^r η^(N−r). The ultrametric inequality bounds the sum by
the largest term.

This is the "upper bound" half of the squeeze in [core_false](#/node/AltCounter.core_false).
""",
 [q("For N = 2(r + 1) and η = 1/(2C), what is the bound?", ["C^r / (2C)^(r+2), which is < 1", "1", "C^N"], 0,
    "AltCounter/Gluing.lean lines 376–399."),
   q("Why do terms with more than r columns from R vanish?", ["Those columns lie in an r-dimensional space, so they are dependent", "Because R is zero", "Because η ≤ 1"], 0,
    "R is Σ_{k<r} u_k ⊗ v_k.")],
 caveats=["The vanishing argument is paraphrased from the statement and the comments; the proof body (lines 152–207) was not traced step by step for this page."])


EXTRA = {
 "AltCounter.not_contDiff_omega_Q_of_NSC": [q("What does the proof of not_contDiff_omega_Q_of_NSC consist of?",
    ["A long new argument", "One line: tailProperty_of_NSC, then not_contDiff_omega_Q", "An appeal to an axiom"], 1,
    "AltCounter/MainNSC.lean line 22.")],
 "AltCounter.exists_bilinear_of_analyticAt_of_homogeneous": [q("Is the lift P claimed to be symmetric?", ["Yes", "No, only bilinear with P(f, f) = Q(f)"], 1,
    "The conclusion is ∀ f, P (fun _ => f) = Q f (AltCounter/Criterion.lean line 45).")],
 "AltCounter.exists_stage_step": [q("How big is the block added at step t?", ["t", "2(t + 1)", "2^t"], 1,
    "st'.n = 2 * (t + 1) (AltCounter/Gluing.lean line 118 in the statement; set on line 121).")],
 "AltCounter.one_le_norm_det_block": [q("Which inequality combines the four small terms?", ["The triangle inequality with a factor 4", "The ultrametric inequality", "Cauchy–Schwarz"], 1,
    "IsUltrametricDist.norm_add_le_max, AltCounter/Gluing.lean lines 207–209."),
   q("What must A − A₀ and B − B₀ satisfy?", ["Vanish below M (and have norm ≤ 1)", "Be zero", "Be supported below M"], 0,
    "hvanA, hvanB and hdA, hdB in the statement (AltCounter/Gluing.lean lines 183–186).")],
 "AltCounter.one_le_norm_det_add": [q("What is required of ε?", ["ε C^(N−1) < 1 and ε ≤ 1", "ε = 0", "ε > C"], 0,
    "hε1 and hsmall in the statement (AltCounter/DetBounds.lean lines 103–105)."),
   q("Would the same argument work verbatim over ℝ?", ["Yes", "No: the triangle inequality would add up 2^N terms"], 1,
    "The proof bounds the sum by its largest term, which needs the ultrametric inequality.")],
 "AltCounter.norm_det_le_of_close_to_lowrank": [q("What is required of η?", ["0 ≤ η ≤ 1", "η > 1", "η = 0"], 0,
    "hη0 and hη1 (AltCounter/DetBounds.lean line 149).")],
}
for n in NODES:
    n["quiz"] += EXTRA.get(n["id"], [])
