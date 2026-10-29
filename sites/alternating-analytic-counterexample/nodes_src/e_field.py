NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}


node("AltCounter.tailProperty_of_NSC", "NSC ⇒ the tail property (a multilinear Phillips lemma)",
 "Over a complete ultrametric field with NSC, every bounded multilinear form on ℓ^∞, of any arity, is uniformly small once one argument is supported far out. The 4-linear case is the tail property.",
 r"""## Plain English

**Theorem (`tailProperty_of_NSC`, AltCounter/Phillips.lean lines 607–621).** If 𝕜 is complete, ultrametric and
satisfies [NSC](#/node/AltCounter.NSC), then [TailProperty 𝕜](#/node/AltCounter.TailProperty) holds. It is the case
d = 4 of `tail_multilinear` (lines 593–605), which handles forms of every arity d.

**The one-variable case** (`tail_functional`, AltCounter/PhillipsOne.lean lines 312–400). For a continuous linear φ
on ℓ^∞ and ε > 0, there is N with ‖φ(x)‖ ≤ ε for every x in the unit ball that vanishes below N. The proof is a
**gliding hump**. If not, pick windows further and further out on which φ is large, and build an operator sending the
k-th unit vector to the k-th window. Composing with φ gives a functional that is not small on unit vectors far out.
But NSC forces values on unit vectors to tend to 0 (`tendsto_apply_basisVec`, lines 148–238, by a shift trick).

**Induction on arity** (`tailAt_succ`, AltCounter/Phillips.lean lines 444–591). Assume the property for d-linear
forms. If a (d+1)-linear form Φ failed it, first make **all** slots supported far out (Claim 1, lines 252–369), then
inside finite windows (Claim 2, lines 371–442). Glue the witnesses into one diagonal vector x, and freeze a slot of Φ
at x to get a d-linear form that the induction hypothesis says is small, a contradiction.
""",
 [q("What is the base case of the induction?", ["d = 4", "d = 1: tails of a single functional, by a gliding hump", "d = 0 only"], 1,
    "tail_multilinear uses tailAt_zero, tailAt_one and tailAt_succ (AltCounter/Phillips.lean lines 597–605)."),
   q("Which property of the field does the gliding hump rely on?", ["Characteristic 2", "NSC (plus completeness and ultrametricity)", "Finite residue field"], 1,
    "tail_functional takes h : NSC 𝕜 (AltCounter/PhillipsOne.lean line 313).")],
 caveats=["This is the longest analytic part of the project (about 1,000 lines across Phillips.lean and PhillipsOne.lean). The outline here follows its docstrings and comments; the proof was skimmed, not traced line by line."])


node("AltCounter.nsc_of_hasEmptyNestedBalls", "Not spherically complete ⇒ NSC",
 "If an ultrametric field has a nested sequence of balls with empty intersection, then every continuous functional on ℓ^∞ that kills all unit vectors is zero. This is the direction of van der Put's theorem that the counterexample needs, proved from scratch.",
 r"""## Plain English

**Theorem (`nsc_of_hasEmptyNestedBalls`, AltCounter/NestedBalls.lean lines 29–151).** For a nontrivially normed
ultrametric field, [HasEmptyNestedBalls](#/node/AltCounter.HasEmptyNestedBalls) implies [NSC](#/node/AltCounter.NSC).

**Proof shape** (by contradiction, following the source comments). Suppose φ ≠ 0 kills every unit vector.

- φ kills every finitely supported vector, so φ(z) depends only on the *tail* of z (lines 45–53).
- Choose vectors w with φ(w) = 1 and ‖w‖ close to 1/‖φ‖ (lines 54–70).
- Use the increments c(n+1) − c(n) of the ball centres to build an approximating sequence and a single "diagonal"
  vector y from far-out pieces (lines 71–122).
- Tail estimates show φ(y) lies in every ball B(c(n), r(n)) (lines 123–151). That contradicts the empty
  intersection.

In words: a nonzero functional that ignores finite parts lets you "sum" the increments of the ball centres, and the sum
would be a common point of all the balls.
""",
 [q("Which direction of van der Put's theorem is proved?",
    ["NSC ⇒ not spherically complete", "Not spherically complete (empty nested balls) ⇒ NSC", "Both"], 1,
    "AltCounter/NestedBalls.lean lines 29–31. The upstream formalization.yaml says the other direction is not needed."),
   q("Does this theorem need completeness of the field?", ["Yes", "No; its variables are only a nontrivially normed ultrametric field"], 1,
    "AltCounter/NestedBalls.lean line 18.")],
 caveats=["The four-bullet outline is reconstructed from the section comments (AltCounter/NestedBalls.lean lines 42–136); the details of how y is built were not checked."])


node("AltCounter.IsGoodModel", "IsGoodModel: what the base field must satisfy before completion",
 "A 'good model' is a field with an absolute value that is non-archimedean, nontrivial, of characteristic 2, and has nested balls with empty intersection whose radii stay above some ρ > 0. The lower bound on the radii is what lets emptiness survive completion.",
 r"""## Plain English

**Definition (`IsGoodModel`, AltCounter/Model.lean lines 14–21).** For a field L with an absolute value v:

- `char2`: L has characteristic 2;
- `nonarch`: v(x + y) ≤ max(v(x), v(y));
- `nontriv`: some x has v(x) > 1;
- `balls`: centres c(n), radii r(n) with r strictly decreasing, all r(n) ≥ ρ for some ρ > 0, nested
  (v(c(n+1) − c(n)) ≤ r(n)), and no a in L lying in every ball.

**Why ρ?** Any point of the completion is within ρ of some point y of L. If it were in every ball, the ultrametric
inequality would put y in every ball too, because r(n) ≥ ρ. That is the argument of AltCounter/Model.lean lines 65–97.
""",
 [q("Why must the radii be bounded below by ρ > 0?",
    ["So that emptiness of the intersection survives completion", "So that L is complete", "To make v nontrivial"], 0,
    "completion_balls, AltCounter/Model.lean lines 65–97."),
   q("Is a good model required to be complete?", ["Yes", "No; completeness comes from passing to the completion"], 1,
    "IsGoodModel has no completeness field (AltCounter/Model.lean lines 16–21).")])


node("AltCounter.exists_field_of_goodModel", "Completing a good model",
 "The completion of a good model is a complete, ultrametric, nontrivially normed field of characteristic 2 that still has empty nested balls. So it satisfies every hypothesis the counterexample needs.",
 r"""## Plain English

**Theorem (`exists_field_of_goodModel`, AltCounter/Model.lean lines 101–113).** If v is a
[good model](#/node/AltCounter.IsGoodModel) on L, then the completion K of (L, v) is a nontrivially normed field with
`IsUltrametricDist`, `CompleteSpace`, `CharP K 2` and [HasEmptyNestedBalls](#/node/AltCounter.HasEmptyNestedBalls).

The pieces are private lemmas in the same file:

- ultrametricity passes to the completion by density (lines 40–53);
- characteristic 2 passes along the injective map L → K (lines 55–63);
- the same centres and radii still give empty nested balls, by the ρ argument (lines 65–97);
- nontriviality: the element with v(x) > 1 still has norm > 1 (lines 106–110).
""",
 [q("Which Mathlib construction is used for K?", ["Ultrafilters", "UniformSpace.Completion of L with the norm from v", "Algebraic closure"], 1,
    "AltCounter/Model.lean lines 106–107."),
   q("Are the centres of the balls in K new points?", ["Yes, new ones are chosen", "No, they are the images of the old centres in L"], 1,
    "AltCounter/Model.lean line 72.")])


node("AltCounter.Puiseux.isGoodModel", "The concrete field: 2-power Puiseux series over 𝔽₂",
 "L is the field of series in t^(1/2^j) over 𝔽₂ (for some j), with |f| = 2^(−order f). The partial sums c(n) = Σ_{m≤n} t^(1−2^−(m+1)) are centres of nested balls with radii ≥ 1/2, and no element of L lies in all of them, because every element has bounded denominators in its exponents.",
 r"""## Plain English

**The field (AltCounter/Puiseux.lean lines 18–224).** Inside Mathlib's Hahn series 𝔽₂⟦t^ℚ⟧ (formal series with
rational exponents and well-ordered support):

- `emb j` (lines 128–129) embeds Laurent series in t into this field, sending t to t^(1/2^j);
- `P` (lines 187–188) is the union over j of the images, a subfield: the **2-power Puiseux series**;
- `vL` (lines 216–224) is the t-adic absolute value |f| = 2^(−order f). It is non-archimedean (`vFun_isNonarch`,
  line 65).

**The balls (lines 249–352).**

- Exponents γ(m) = 1 − 2^(−(m+1)), that is 1/2, 3/4, 7/8, …, increasing to 1 (line 251).
- Centres c(n) = t^γ(0) + ⋯ + t^γ(n) (line 289). Radii rad(n) = 2^(−γ(n+1)), strictly decreasing and ≥ 1/2
  (line 310).
- **Empty intersection** (`vL_balls_empty`, lines 332–352): any a in L lies in some `emb j`, so its exponents have
  denominator dividing 2^j. But γ(j) has denominator 2^(j+1) (`γ_not_dyadic`, lines 272–273). So a has coefficient 0
  at t^γ(j), while c(j) has coefficient 1 there. Hence |a − c(j)| ≥ 2^(−γ(j)) > rad(j).

**Theorem (`isGoodModel`, lines 354–359)** packages this as a [good model](#/node/AltCounter.IsGoodModel), and
`exists_goodModel` (lines 363–364) exports it.

The "limit" Σ t^γ(m) does exist in the Hahn series field, but it needs exponents with unbounded denominators, so it is
not in L. That gap is the non-spherical completeness.
""",
 [q("Why is no element of L in every ball?",
    ["Every element of L has exponents with bounded 2-power denominators, but the centres need ever larger denominators", "Because L is finite", "Because the radii tend to 0"], 0,
    "vL_balls_empty, AltCounter/Puiseux.lean lines 332–352."),
   q("What are the first three exponents γ(0), γ(1), γ(2)?", ["1/2, 3/4, 7/8", "1, 2, 3", "1/2, 1/4, 1/8"], 0,
    "γ m = 1 − (1/2)^(m+1) (AltCounter/Puiseux.lean line 251)."),
   q("Which coefficient field is used?", ["ℚ", "𝔽₂ = ZMod 2", "ℝ"], 1, "Coeff := ZMod 2 (AltCounter/Puiseux.lean line 19)."),
   q("Is L itself complete?", ["Yes", "No; it is completed afterwards"], 1,
    "IsGoodModel does not need completeness; exists_field_of_goodModel completes it.")],
 caveats=["The residue field here is 𝔽₂, which is finite. The upstream notes explain that the original argument needed an infinite residue field and the hypercube sum removed that need."])


EXTRA = {
 "AltCounter.tailProperty_of_NSC": [q("Which arity d does tailProperty_of_NSC use?", ["1", "2", "4", "every d"], 2,
    "tail_multilinear h 4 … (AltCounter/Phillips.lean line 610).")],
 "AltCounter.nsc_of_hasEmptyNestedBalls": [q("Which simple fact starts the proof?",
    ["φ kills every finitely supported vector, so it sees only tails", "φ is bounded below", "ℓ^∞ is separable"], 0,
    "hhead and htail, AltCounter/NestedBalls.lean lines 45–53.")],
 "AltCounter.IsGoodModel": [q("Which characteristic must the model have?", ["0", "2", "Any"], 1, "char2 : CharP L 2 (AltCounter/Model.lean line 17).")],
 "AltCounter.exists_field_of_goodModel": [q("Why is the completion nontrivially normed?",
    ["The element x₀ with v(x₀) > 1 keeps norm > 1 in the completion", "Every completion is", "Because of characteristic 2"], 0,
    "AltCounter/Model.lean lines 106–110.")],
}
for n in NODES:
    n["quiz"] += EXTRA.get(n["id"], [])
