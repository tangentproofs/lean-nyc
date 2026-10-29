NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}


node("AltCounter.Linf", "ℓ^∞: bounded sequences",
 "The space E of the counterexample is ℓ^∞(ℕ, 𝕜), the bounded sequences with the sup norm. It is huge and has no nice basis, which is exactly what lets analyticity fail.",
 r"""## Plain English

**Definition (`Linf`, AltCounter/Defs.lean lines 13–14).** `Linf 𝕜` is the space of bounded sequences
(x₀, x₁, x₂, …) of elements of 𝕜, with norm ‖x‖ = sup_i ‖x_i‖. In Lean it is Mathlib's space of bounded continuous
functions ℕ →ᵇ 𝕜 (every function on the discrete space ℕ is continuous, so this is just "bounded sequences").

It is a Banach space whenever 𝕜 is complete. Both E and E′ in the headline are this space, and the matrices that make
up the target [F](#/node/AltCounter.F) are bounded functions on ℕ × ℕ, a two-index version of it.

**Why ℓ^∞?** Every continuous linear functional on the smaller space c₀ (sequences tending to 0) is determined by its
values on the unit vectors. On ℓ^∞ that can fail. Over the special field of this project it doesn't fail:
[NSC](#/node/AltCounter.NSC) says a functional on ℓ^∞ that kills every unit vector is zero. That rigidity is the
source of the [tail property](#/node/AltCounter.TailProperty).

**Ultrametric norm.** Mathlib has no `IsUltrametricDist` instance for this space, so AltCounter/NestedBalls.lean
lines 24–28 prove ‖f + g‖ ≤ max(‖f‖, ‖g‖) coordinatewise.
""",
 [q("What is an element of Linf 𝕜?",
    ["A sequence tending to 0", "A bounded sequence of elements of 𝕜", "A finite sequence", "A continuous function on ℝ"], 1,
    "AltCounter/Defs.lean line 14: bounded continuous functions on ℕ, which are just bounded sequences."),
   q("What is the norm?", ["The sum of absolute values", "The supremum of ‖x_i‖", "The limit of ‖x_i‖"], 1,
    "The norm of bounded continuous functions is the sup norm.")])


node("AltCounter.Wfun", "The symmetric matrix x ⊗ y + y ⊗ x",
 "W(x, y) is the infinite matrix with (p, q) entry x_p y_q + y_p x_q. In characteristic 2 it is symmetric with zero diagonal, and it is alternating in (x, y): W(x, x) = 2 x ⊗ x = 0.",
 r"""## Plain English

**Definition (`Wfun`, AltCounter/Main.lean lines 20–31).** For x, y in [ℓ^∞](#/node/AltCounter.Linf), `Wfun 𝕜 x y`
is the bounded function on ℕ × ℕ

> W(x, y)_{pq} = x_p · y_q + y_p · x_q,

with the bound 2‖x‖‖y‖ (lines 23–31).

**In characteristic 2** (AltCounter/Main.lean lines 103–109):

- it is symmetric, W_{pq} = W_{qp};
- its diagonal is W_{pp} = 2 x_p y_p = 0;
- W(x, x) = 2 x ⊗ x = 0, so (x, y) ↦ W(x, y) is **alternating**.

This is the model of an alternating 2-form: think of W(x, y) as x ∧ y, written as a symmetric zero-diagonal matrix.
The closed span of all W(x, y) is the target space [F](#/node/AltCounter.F), and the 2-form
[W₀](#/node/AltCounter.W₀) is (x, y) ↦ W(x, y).

Each W(x, y) has **rank at most 2**: it is the sum of the two rank-1 matrices x ⊗ y and y ⊗ x
(AltCounter/Main.lean lines 189–196). This low rank is what the end of [core_false](#/node/AltCounter.core_false)
exploits.
""",
 [q("What is W(x, y)_{pq}?", ["x_p y_p", "x_p y_q + y_p x_q", "x_p y_q − y_p x_q", "x_q y_q"], 1,
    "AltCounter/Main.lean line 23."),
   q("Why is W(x, x) = 0 in characteristic 2?", ["Because x ⊗ x = 0", "Because W(x, x) = 2 x ⊗ x and 2 = 0", "It is not zero"], 1,
    "AltCounter/Main.lean lines 286–287 use CharTwo.add_self_eq_zero."),
   q("What is the rank of W(x, y) as a matrix?", ["At most 2", "Infinite", "Exactly 1"], 0,
    "It is x ⊗ y + y ⊗ x (AltCounter/Main.lean lines 191–196).")])


node("AltCounter.FSub", "FSub: the closed span of the W(x, y)",
 "FSub is the closure, inside the bounded functions on ℕ × ℕ, of the linear span of all matrices W(x, y). Everything in it is symmetric with zero diagonal (in characteristic 2) and is a uniform limit of finite-rank matrices.",
 r"""## Plain English

**Definition (`FSub`, AltCounter/Main.lean lines 33–35).** The submodule of ℓ^∞(ℕ × ℕ, 𝕜) obtained by taking the
linear span of all matrices [W(x, y)](#/node/AltCounter.Wfun) and then its topological closure.

**Two properties inherited from the generators**, because both are preserved by sums, scalar multiples and limits:

- **Symmetric with zero diagonal** in characteristic 2 (`FSub_le_symSub`, AltCounter/Main.lean lines 111–115;
  the submodule of such matrices is defined on lines 73–84 and shown closed on lines 90–101).
- **Uniformly approximable by finite-rank matrices** (`FSub_approx`, AltCounter/Main.lean line 204): for every η > 0
  there are finitely many sequences u_k, v_k with |g_{pq} − Σ_k u_k(p) v_k(q)| ≤ η for all p, q. The predicate is
  `Approx` (lines 125–128); its closure under limits is lines 170–187.

These two facts become hypotheses (iii) and (iv) of [core_false](#/node/AltCounter.core_false).
""",
 [q("Why is every element of FSub symmetric with zero diagonal?",
    ["Because the generators are, and those properties survive linear combinations and limits",
     "Because FSub is finite-dimensional", "By definition of FSub"], 0,
    "AltCounter/Main.lean lines 111–115 use topologicalClosure_minimal with the closed submodule symSub."),
   q("What does the finite-rank approximation property say?",
    ["Every element has finite rank",
     "Every element is within η of a finite sum of rank-1 matrices, for every η > 0",
     "Every element is zero far from the diagonal"], 1,
    "Approx, AltCounter/Main.lean lines 125–128.")],
 caveats=["Symmetry and zero diagonal use characteristic 2; the finite-rank approximation does not."])


node("AltCounter.F", "F: the target space of the 2-forms",
 "F is FSub viewed as a normed space in its own right. The counterexample studies alternating 2-forms ℓ^∞ × ℓ^∞ → F.",
 r"""## Plain English

**Definition (`F`, AltCounter/Main.lean lines 37–42).** `F 𝕜` is the subspace [FSub](#/node/AltCounter.FSub) (the
closed span of the matrices x ⊗ y + y ⊗ x) made into its own type, with the norm and 𝕜-module structure copied over.
`F.incl` (line 45) is the inclusion back into ℓ^∞(ℕ × ℕ, 𝕜), and it preserves norms (line 64).

**Why a separate type?** The ARCHITECTURE.md file explains that using the submodule directly confused Lean's instance
search for the operator-norm structure on maps between alternating-map spaces. A type synonym with copied instances
avoids that. Mathematically F is just FSub.

**Completeness.** F is closed in a Banach space, so it is complete when 𝕜 is (AltCounter/Final.lean lines 20–22). The
[Banach headline](#/node/AlternatingAnalyticChallenge.false_of_contDiff_omega_compContinuousLinearMapCLM_charTwo_banach)
needs this.

**Why this target?** It is the smallest closed space that contains all values of the 2-form
[W₀](#/node/AltCounter.W₀). Every value of a 2-form with values in F is then a symmetric, zero-diagonal,
nearly-finite-rank matrix. Those are the constraints that [core_false](#/node/AltCounter.core_false) turns into a
contradiction.
""",
 [q("Is F a different space from FSub mathematically?", ["Yes", "No, it is the same subspace as its own type"], 1,
    "AltCounter/Main.lean lines 37–42: a type synonym with the inherited instances."),
   q("When is F complete?", ["Never", "When 𝕜 is complete, since F is closed in a Banach space", "Only if finite-dimensional"], 1,
    "AltCounter/Final.lean lines 20–22.")],
 caveats=["The scanner links some declarations to `AltCounter.F` merely because a bound variable is also called F (e.g. in the hypothesis of the general headline). Those links are artefacts of text scanning."])


node("AltCounter.Q", "Q: the precomposition map",
 "Q sends an operator f on ℓ^∞ to the map m ↦ m ∘ (f, f) on continuous alternating 2-forms ℓ^∞ × ℓ^∞ → F. It is homogeneous of degree 2: Q(c f) = c² Q(f). The project proves that Q is not analytic at 0.",
 r"""## Plain English

**Definition (`Q`, AltCounter/Main.lean lines 47–50).** For a continuous linear map f : ℓ^∞ → ℓ^∞,

> Q(f) : Alt²(ℓ^∞, F) → Alt²(ℓ^∞, F),  Q(f)(m)(x, y) = m(f x, f y).

It is literally Mathlib's `ContinuousAlternatingMap.compContinuousLinearMapCLM f` at E = E′ = [ℓ^∞](#/node/AltCounter.Linf),
target [F](#/node/AltCounter.F) and ι = `Fin 2`. That is why the headline's hypothesis, instantiated at these
spaces, says exactly "Q is C^ω".

**Homogeneous of degree 2** (`Q_homogeneous`, AltCounter/Main.lean lines 336–342): Q(c · f) = c² · Q(f), because
m(c f x, c f y) = c² m(f x, f y). So Q is a "quadratic" map, the diagonal of a bilinear-looking expression. Over ℝ or
ℂ, such a map is always the diagonal of a bounded bilinear map: polarise, (Q(f + g) − Q(f) − Q(g)) / 2. In
characteristic 2 you cannot divide by 2, and the whole counterexample lives in that gap.

**Main result about Q:** [not_analyticAt_Q](#/node/AltCounter.not_analyticAt_Q).
""",
 [q("What is Q(f)(m)(x, y)?", ["m(x, y) · f", "m(f x, f y)", "f(m(x, y))", "m(x, f y)"], 1,
    "Q f is compContinuousLinearMapCLM f (AltCounter/Main.lean line 50), which precomposes m with f in each slot."),
   q("What is Q(c · f)?", ["c · Q(f)", "c² · Q(f)", "Q(f)", "2c · Q(f)"], 1,
    "Q_homogeneous, AltCounter/Main.lean lines 336–342."),
   q("Why does characteristic 2 matter for a degree-2 map?",
    ["Polarisation divides by 2, which is impossible there", "Degree-2 maps are zero there", "It doesn't matter"], 0,
    "Over fields where 2 is invertible a quadratic map is the diagonal of the bilinear map obtained by polarisation.")])


node("AltCounter.W₀", "W₀: the test 2-form (x, y) ↦ x ⊗ y + y ⊗ x",
 "W₀ is the continuous alternating 2-form ℓ^∞ × ℓ^∞ → F sending (x, y) to W(x, y). The proof applies Q(f) to this single form and reads off matrix entries.",
 r"""## Plain English

**Definition (`W₀`, AltCounter/Main.lean lines 305–310).** In characteristic 2, (x, y) ↦ [W(x, y)](#/node/AltCounter.Wfun)
is bilinear and alternating (W(x, x) = 0), and bounded by 2‖x‖‖y‖. So it is a continuous alternating 2-form with values
in [F](#/node/AltCounter.F), and its norm is at most 2 (line 314). Lines 256–287 build it in stages: multilinear map,
then alternating map, then continuous.

**How it is used.** For a [multiplication operator](#/node/AltCounter.mulL) f = m_a (pointwise multiplication by a
sequence a),

> Q(m_a)(W₀)(x, y) = W(a x, a y),  with (p, q) entry a_p x_p a_q y_q + a_p y_p a_q x_q.

That is hypothesis (ii) of [core_false](#/node/AltCounter.core_false), and it is checked on AltCounter/Main.lean
lines 451–460.
""",
 [q("Why is W₀ alternating?", ["Because W(x, x) = 2 x ⊗ x = 0 in characteristic 2", "Because W is antisymmetric over every field", "It is not alternating"], 0,
    "AltCounter/Main.lean lines 275–287."),
   q("What is Q(m_a)(W₀)(x, y)?", ["W(x, y)", "W(a x, a y)", "a · W(x, y)", "0"], 1,
    "AltCounter/Main.lean lines 455–460.")])


node("AltCounter.mulL", "Multiplication operators on ℓ^∞",
 "m_a is the operator 'multiply pointwise by the bounded sequence a'. The proof only ever feeds Q operators of this form, and they already break analyticity.",
 r"""## Plain English

**Definition (`mulL`, AltCounter/Main.lean lines 319–321).** For a in [ℓ^∞](#/node/AltCounter.Linf), m_a x is the
sequence (a_p x_p)_p. It is linear in a (lines 325–329) and ‖m_a‖ ≤ ‖a‖ (lines 331–332).

**Role in the proof.** If Q had a bounded bilinear lift P, then

> M(a, b) := P(m_a, m_b)(W₀)

would be a bounded bilinear function of the two sequences a, b, with values in alternating 2-forms. Taking matrix
entries gives the 4-linear forms Λ_{pq}(a, b, x, y) that [core_false](#/node/AltCounter.core_false) rules out. See
[not_analyticAt_Q](#/node/AltCounter.not_analyticAt_Q), AltCounter/Main.lean lines 354–355.
""",
 [q("What is (m_a x)_p?", ["a_p + x_p", "a_p · x_p", "Σ a_i x_i", "a_0 x_p"], 1, "mulL_apply, AltCounter/Main.lean line 323."),
   q("Which operators does the proof plug into the bilinear lift?", ["All operators on ℓ^∞", "Only multiplication operators m_a", "Only the identity"], 1,
    "AltCounter/Main.lean line 355.")])


node("AltCounter.IsBdd4", "IsBdd4: a bounded 4-linear form on ℓ^∞",
 "IsBdd4 Λ C says Λ(a, b, x, y) is additive and homogeneous in each of its four ℓ^∞ arguments and bounded by C‖a‖‖b‖‖x‖‖y‖. It is a hands-on spelling of 'bounded 4-linear form'.",
 r"""## Plain English

**Definition (`IsBdd4`, AltCounter/Defs.lean lines 18–29).** For Λ : ℓ^∞ × ℓ^∞ × ℓ^∞ × ℓ^∞ → 𝕜 and a real C,
`IsBdd4 𝕜 Λ C` bundles nine facts:

- additivity in each slot (four fields `add₁`…`add₄`);
- homogeneity in each slot, Λ(c a, b, x, y) = c Λ(a, b, x, y) and so on (`smul₁`…`smul₄`);
- the bound ‖Λ(a, b, x, y)‖ ≤ C ‖a‖ ‖b‖ ‖x‖ ‖y‖.

Together these say Λ is a continuous 4-linear form with norm at most C, without going through Mathlib's
`ContinuousMultilinearMap`. Phillips.lean has the d-argument version `IsBddML` (lines 14–15) and converts between
them (lines 60–74).

It appears in [TailProperty](#/node/AltCounter.TailProperty) and as hypothesis `hlin` of
[core_false](#/node/AltCounter.core_false).
""",
 [q("How many arguments does Λ take?", ["Two", "Four, each in ℓ^∞", "Infinitely many"], 1, "AltCounter/Defs.lean line 20."),
   q("What does the bound field say?", ["‖Λ(a,b,x,y)‖ ≤ C", "‖Λ(a,b,x,y)‖ ≤ C‖a‖‖b‖‖x‖‖y‖", "Λ is bounded below"], 1,
    "AltCounter/Defs.lean line 29.")])


node("AltCounter.TailProperty", "TailProperty: the multilinear Phillips property",
 "TailProperty 𝕜 says: a bounded 4-linear form on ℓ^∞ is uniformly tiny on unit vectors as soon as one argument vanishes on a long enough initial segment. Over the special field this holds; over spherically complete fields it fails.",
 r"""## Plain English

**Definition (`TailProperty`, AltCounter/Defs.lean lines 31–38).** For every bounded 4-linear form Λ
([IsBdd4](#/node/AltCounter.IsBdd4) with constant C) and every ε > 0, there is an N such that

> ‖Λ(a, b, x, y)‖ ≤ ε  whenever ‖a‖, ‖b‖, ‖x‖, ‖y‖ ≤ 1 and **at least one** of a, b, x, y is zero in positions 0, …, N − 1.

In words: Λ "only sees the start" of its arguments. Anything supported far out contributes almost nothing,
uniformly.

**Why the name.** For linear functionals on ℓ^∞ this is a Phillips-type lemma. It is true when every functional on
ℓ^∞ is determined by its values on unit vectors ([NSC](#/node/AltCounter.NSC)). Over a spherically complete field
(ℝ is not ultrametric, but think ℚ_p) there are functionals that vanish on c₀ and are nonzero on the constant sequence
1, and the property fails.

**Status.** This is a **hypothesis** of [not_analyticAt_Q](#/node/AltCounter.not_analyticAt_Q) and
[core_false](#/node/AltCounter.core_false). It is proved from NSC in
[tailProperty_of_NSC](#/node/AltCounter.tailProperty_of_NSC), and NSC is proved for the constructed field. So the
headlines are unconditional.
""",
 [q("When does the property force ‖Λ(a,b,x,y)‖ ≤ ε?",
    ["When all four arguments vanish below N", "When at least one argument vanishes below N (and all have norm ≤ 1)",
     "When a = b", "Always"], 1,
    "The disjunction on AltCounter/Defs.lean line 37."),
   q("Is TailProperty assumed or proved for the counterexample field?",
    ["Assumed as an axiom", "Proved, via NSC and nested balls", "Neither: it is not needed"], 1,
    "tailProperty_of_NSC (AltCounter/Phillips.lean lines 607–621) and nsc_of_hasEmptyNestedBalls (AltCounter/NestedBalls.lean lines 29–151)."),
   q("Does N depend on Λ and ε?", ["Yes", "No, one N works for everything"], 0,
    "The ∃ N comes after ∀ Λ C, ∀ ε (AltCounter/Defs.lean lines 35–36).")],
 caveats=["The upstream docstring says the property fails for spherically complete fields; that claim is commentary, not proved in Lean."])


node("AltCounter.NSC", "NSC: (ℓ^∞ / c₀)′ = 0",
 "NSC 𝕜 says: a continuous linear functional on ℓ^∞ that vanishes on every unit vector e_i is zero. For complete non-archimedean fields it is the classical characterisation of not being spherically complete.",
 r"""## Plain English

**Definition (`NSC`, AltCounter/PhillipsOne.lean lines 116–118).** For every continuous linear φ : ℓ^∞ → 𝕜, if
φ(e_i) = 0 for every unit vector e_i (`basisVec`, line 114), then φ = 0.

Over ℝ this is false: a Banach limit kills every e_i but sends the constant sequence 1 to 1. Over a complete
non-archimedean field, van der Put (1969, Thm 3.2) showed that NSC holds **exactly** when the field is not spherically
complete. The project needs only one direction, and proves it itself:
[nsc_of_hasEmptyNestedBalls](#/node/AltCounter.nsc_of_hasEmptyNestedBalls).

The name abbreviates "not spherically complete". AltCounter/Bridge.lean lines 15–54 also show that the literal form
"a functional vanishing on c₀ is zero" implies NSC; it is not used by the main theorems.

From NSC, [tailProperty_of_NSC](#/node/AltCounter.tailProperty_of_NSC) derives the
[tail property](#/node/AltCounter.TailProperty).
""",
 [q("What does NSC say?",
    ["Every functional on ℓ^∞ is zero", "A functional on ℓ^∞ vanishing on all unit vectors is zero",
     "ℓ^∞ has a Schauder basis", "Every bounded sequence converges"], 1,
    "AltCounter/PhillipsOne.lean line 118."),
   q("Does NSC hold over ℝ?", ["Yes", "No: Banach limits are counterexamples"], 1,
    "A Banach limit vanishes on c₀ but not on the constant sequence 1.")],
 caveats=["The equivalence with non-spherical completeness is van der Put's theorem, cited, not formalized; only the direction 'empty nested balls ⇒ NSC' is proved."])


node("AltCounter.HasEmptyNestedBalls", "HasEmptyNestedBalls: not spherically complete",
 "A field has empty nested balls when some sequence of closed balls, each inside the previous one with strictly shrinking radii, has nothing in common. Complete fields can still do this when the radii stay bounded away from 0.",
 r"""## Plain English

**Definition (`HasEmptyNestedBalls`, AltCounter/NestedBalls.lean lines 12–16).** There are centres c(n) and radii r(n)
such that

- r is strictly decreasing;
- ‖c(n+1) − c(n)‖ ≤ r(n), which in an ultrametric field means the ball B(c(n+1), r(n+1)) sits inside B(c(n), r(n));
- for every a there is an n with r(n) < ‖a − c(n)‖: no point lies in every ball.

A field is *spherically complete* when every nested sequence of closed balls has a common point. So this says the field
is **not** spherically complete. In a complete field the radii of such a sequence cannot tend to 0 (the centres would
converge to a common point), so the radii must stay bounded below.

Used by [nsc_of_hasEmptyNestedBalls](#/node/AltCounter.nsc_of_hasEmptyNestedBalls) and
[exists_field](#/node/AltCounter.exists_field).
""",
 [q("What does the last clause say?", ["Some point lies in every ball", "No point lies in every ball", "The radii tend to 0"], 1,
    "∀ a, ∃ n, r n < ‖a − c n‖ (AltCounter/NestedBalls.lean line 16)."),
   q("Is 'spherically complete' the same as 'complete'?",
    ["Yes", "No: spherically complete is stronger; a complete field can still have empty nested balls"], 1,
    "The constructed field is complete and has empty nested balls (AltCounter/Final.lean lines 14–16).")])


EXTRA = {
 "AltCounter.Linf": [q("Is Linf 𝕜 complete when 𝕜 is complete?", ["Yes, it is a Banach space", "No", "Only if 𝕜 is finite"], 0,
    "Bounded functions into a complete space form a complete space; the Banach headline uses this for E = Linf K.")],
 "AltCounter.FSub": [q("FSub is obtained from the matrices W(x, y) by which two operations?",
    ["Taking the linear span, then the topological closure", "Taking products, then inverses", "Only the span (no closure)"], 0,
    "Submodule.span … then topologicalClosure (AltCounter/Main.lean line 35).")],
 "AltCounter.W₀": [q("What bound does the source give for ‖W₀‖?", ["≤ 1", "≤ 2", "Unbounded"], 1,
    "norm_W₀_le, AltCounter/Main.lean line 314.")],
 "AltCounter.mulL": [q("What bound holds for the operator norm of m_a?", ["‖m_a‖ ≤ ‖a‖", "‖m_a‖ ≥ ‖a‖²", "‖m_a‖ = 1"], 0,
    "norm_mulL_le, AltCounter/Main.lean lines 331–332.")],
 "AltCounter.IsBdd4": [q("Does IsBdd4 require Λ to be alternating?", ["Yes", "No; alternation is a separate hypothesis of core_false"], 1,
    "IsBdd4 has only additivity, homogeneity and the bound (AltCounter/Defs.lean lines 20–29); alternation is halt in core_false.")],
 "AltCounter.NSC": [q("Which vectors does NSC test the functional on?", ["All of ℓ^∞", "The unit vectors e_i", "The constant sequence 1"], 1,
    "∀ i, φ (basisVec 𝕜 i) = 0 (AltCounter/PhillipsOne.lean line 118).")],
 "AltCounter.HasEmptyNestedBalls": [q("Must the radii be strictly decreasing?", ["Yes, StrictAnti r", "No"], 0,
    "AltCounter/NestedBalls.lean line 15.")],
}
for n in NODES:
    n["quiz"] += EXTRA.get(n["id"], [])

for n in NODES:
    if n["id"] == "AltCounter.F":
        n["quiz"].append(q("Which 2-forms does the counterexample study?",
            ["Alternating 2-forms ℓ^∞ × ℓ^∞ → F", "Symmetric forms ℓ^∞ × ℓ^∞ → 𝕜", "Linear maps F → ℓ^∞"], 0,
            "Q acts on (Linf 𝕜) [⋀^Fin 2]→L[𝕜] (F 𝕜) (AltCounter/Main.lean line 49)."))
