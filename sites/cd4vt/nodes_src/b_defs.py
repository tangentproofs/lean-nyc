NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}


# ---------- extrema and windows ----------

node("Discrete.PlateauMaxRun",
 "Plateau maxima and minima",
 "A plateau maximum is a run of equal consecutive values whose two outside neighbours are both strictly lower; a plateau minimum is the same with both neighbours strictly higher. A flat top counts once, however long it is.",
 r"""## Plain English

**Definition (`PlateauMaxRun f a k`, Gluck/Statements.lean lines 206–209).** Starting at index a, the k + 1 values
f(a), f(a+1), …, f(a+k) (indices mod n) are all equal, and both outside neighbours are strictly smaller:
f(a−1) < f(a) and f(a+k+1) < f(a).

**Definition (`PlateauMinRun f a k`, lines 213–216).** The same with both inequalities reversed.

This is Dahlberg's convention for counting extrema when values repeat. For example, in the cyclic sequence
(1, 3, 3, 1, 2, 2) the run 3, 3 is one plateau maximum (a = 1, k = 1), the run 2, 2 is another, and each 1 is a
plateau minimum.

A run is described by its start a (a natural number, cast into `ZMod n`) and its extra length k. The definition
does not say the run is maximal, but strict drops at both ends force it to be.
""",
 [q("In the cyclic sequence (2, 5, 5, 5, 2, 4), how many plateau maxima are there?", ["2 (the run 5,5,5 and the single 4)", "4", "1"], 0,
    "The 5-run has strictly lower neighbours 2 and 2; the 4 has neighbours 2 and 2 (cyclically). Gluck/Statements.lean lines 206–209."),
  q("Is a point in the middle of a flat plateau a plateau maximum on its own (k = 0)?", ["No, its neighbours are equal, not strictly lower", "Yes"], 0,
    "Both end inequalities are strict (lines 208–209)."),
  q("Does a constant sequence have any plateau maximum?", ["No", "Yes, the whole cycle"], 0,
    "There is no strictly lower neighbour anywhere."),
 ])


node("Discrete.IsPlateauTwoMaxTwoMin",
 "At least two maxima and two minima, counted as plateaus",
 "Tabachnikov's hypothesis, made precise: two plateau-maximum runs that share no index and two plateau-minimum runs that share no index. Each run has fewer than n entries.",
 r"""## Plain English

**Definition (`IsPlateauTwoMaxTwoMin r`, Gluck/Statements.lean lines 267–268)** is the conjunction of

- `HasTwoPlateauMaxRuns r` (lines 234–238): there are two [plateau-maximum runs](#/node/Discrete.PlateauMaxRun)
  (a₁, k₁) and (a₂, k₂), each shorter than the whole cycle (kⱼ < n), whose index sets are disjoint;
- `HasTwoPlateauMinRuns r` (lines 243–247): the same for plateau minima.

The project also shows that the minima half follows from the maxima half
(`hasTwoPlateauMaxRuns_iff_hasTwoPlateauMinRuns`, mentioned in the header of
Gluck/Discrete/TabachnikovReduction.lean), and that this class equals the
[four-vertex-window](#/node/Discrete.DFV) class for positive words (`discreteFourVertexPos_iff_extrema`,
Gluck/Discrete/TabachnikovReduction.lean lines 362–371).
""",
 [q("Does (1, 2, 3, 2) satisfy the hypothesis?", ["No: one maximum (3) and one minimum (1)", "Yes"], 0,
    "Cyclically it rises once and falls once."),
  q("Does (1, 2, 1, 2) satisfy it?", ["Yes: maxima at both 2s, minima at both 1s", "No"], 0,
    "Each 2 has strictly lower neighbours; each 1 has strictly higher ones."),
  q("Why must the two maximum runs be disjoint?", ["Otherwise one plateau could be counted twice", "To make n even"], 0,
    "The last conjunct on lines 237–238."),
 ])


node("Discrete.DFV",
 "Four-vertex window at a level c",
 "κ has a four-vertex window at level c if, going once around the cycle, you can find four positions in order whose values are above c, below c, above c, below c. That is the convenient algebraic form of 'two maxima and two minima'.",
 r"""## Plain English

**Definition (`DFV κ c`, Gluck/Statements.lean lines 131–134).** There are natural numbers i₁ < i₂ < i₃ < i₄ < i₁ + n
(so four positions in cyclic order within one lap) with

κ(i₁) > c, κ(i₂) < c, κ(i₃) > c, κ(i₄) < c.

All inequalities are strict. A word with such a window can't be constant, and needs n ≥ 4
(`DFV.four_le_period`, Gluck/Discrete/ConstantRunDFV.lean line 59).

**Where it is used.**
- In [Problem 2](#/node/Discrete.TabachnikovProblem2) the window level must be positive.
- In the [side-tangent admissibility](#/node/Discrete.SideTangent.SideTangentAdmissible) it is applied to the
  differences ρᵢ₋₁ − ρᵢ at level 0, which says "four sign changes".
- For the hexagon path, the window levels of (14, 11, 10+3s, 5, 7−3s, 3) are exactly the two bands
  (5, 7−3s) ∪ (11, 10+3s) (`bandProfile_dfv_iff`, Gluck/Discrete/GlobalContinuity/LevelBands.lean lines 42–67).
""",
 [q("Does (1, 3, 1, 3) have a window at c = 2?", ["Yes: positions 1, 2, 3, 4 read 3 > 2, 1 < 2, 3 > 2, 1 < 2", "No"], 0,
    "Take i₁ = 1, …, i₄ = 4 < 1 + 4 (Gluck/Statements.lean lines 132–134)."),
  q("Does (1, 3, 1, 3) have a window at c = 3?", ["No: nothing is strictly above 3", "Yes"], 0,
    "The inequalities are strict."),
  q("Is DFV the same as 'two plateau maxima and two plateau minima'?", ["For some level c, yes; the project proves the two classes agree", "No, it is weaker"], 0,
    "`discreteFourVertexPos_iff_extrema`, Gluck/Discrete/TabachnikovReduction.lean lines 362–371."),
 ])


# ---------- triangles, circles, polygons ----------

node("Discrete.crossR2",
 "Signed area and signed Menger curvature of three points",
 "crossR2 A B C is twice the signed area of triangle ABC (positive when A, B, C turn left). The signed Menger curvature is 2·crossR2 / (product of the three side lengths), which is ±1/(circumradius).",
 r"""## Plain English

**Definition (`crossR2 A B C`, Gluck/Statements.lean lines 153–154).** With points as complex numbers,
crossR2 A B C = (B − A)ₓ(C − A)ᵧ − (B − A)ᵧ(C − A)ₓ, the 2D cross product. It is positive when the turn A → B → C is
to the left, negative to the right, zero when the points are collinear.

**Definition (`signedMengerR2 A B C`, lines 159–160).** 2 · crossR2 A B C / (|AB| · |BC| · |CA|). For a
non-degenerate triangle its absolute value is 1/R, where R is the circumradius (the classical identity
2|Δ|R = abc, proved as `dist_circumcenterR2_mul`, Gluck/Discrete/TabachnikovConverse.lean lines 48–85). The sign
records orientation.

The **signed Menger profile** of a polygon (`SignedMengerProfile v`, lines 375–376) is i ↦ signedMengerR2(v_{i−1},
v_i, v_{i+1}), the discrete curvature at each vertex used in Dahlberg's theorem and in the
[hexagon headline](#/node/Discrete.GlobalContinuity.no_continuous_regular_hexagon_path).
""",
 [q("What is the signed Menger curvature of three points on a circle of radius 2, taken counterclockwise?", ["1/2", "−1/2", "2"], 0,
    "|value| = 1/R and the left turn gives +."),
  q("What is crossR2 of three collinear points?", ["0", "1", "Undefined"], 0,
    "The cross product of parallel vectors vanishes (lines 153–154)."),
  q("What does |signedMengerR2 A B C| equal for a non-degenerate triangle?", ["1 / circumradius", "The area", "The perimeter"], 0, "From 2|Δ|R = abc (`dist_circumcenterR2_mul`, Gluck/Discrete/TabachnikovConverse.lean lines 48–85)."),
 ])


node("Discrete.CoherentR2",
 "Coherent polygon: each circumcentre lies inside its vertex angle",
 "A polygon is coherent when, at every vertex, the three points v_{i−1}, v_i, v_{i+1} are not collinear and the centre of the circle through them lies strictly inside the angle formed at v_i by its two edges. This is Tabachnikov's condition.",
 r"""## Plain English

**Definition (`CoherentR2 v`, Gluck/Statements.lean lines 197–199).** For every i:
1. crossR2(v_i, v_{i−1}, v_{i+1}) ≠ 0: the triple is not collinear;
2. the circumcentre `circumcenterR2 (v i) (v (i-1)) (v (i+1))` lies in the **open vertex cone** at v_i.

**Circumcentre** (`circumcenterR2 p q r`, lines 183–185). The closed-form centre of the circle through p, q, r. It is
a total function (it divides by zero on collinear triples), which is why coherence first asks for non-collinearity.

**Open vertex cone** (`vertexCone v i`, lines 190–192). All points v_i + s(v_{i−1} − v_i) + t(v_{i+1} − v_i) with
s, t > 0: the open angular region at v_i spanned by the two edges.

Geometrically, coherence fails when a vertex angle is so flat (and the neighbours so lopsided) that the circle's
centre falls outside the angle. Dahlberg's weaker [regularity](#/node/Forward.DahlbergRegular) uses the closed cone
and allows collinear triples.
""",
 [q("Is the regular hexagon coherent?", ["Yes: each circumcentre is the hexagon's centre, inside every vertex angle", "No"], 0,
    "All vertices are on one circle centred inside the polygon."),
  q("Why does coherence demand a non-zero cross product first?", ["The closed-form circumcentre divides by it; collinear triples have no circumcircle", "To make the polygon convex"], 0,
    "Gluck/Statements.lean lines 183–185 and 198."),
  q("Is the cone open or closed?", ["Open (s, t > 0)", "Closed (s, t ≥ 0)"], 0,
    "Line 191. The closed version is Dahlberg's InVertexCone (lines 352–354)."),
 ])


node("Discrete.vertexCircumradius",
 "Vertex circumradius",
 "The radius of the circle through v_{i−1}, v_i, v_{i+1}, computed as the distance from its circumcentre to v_i. These are the 'radii' that Tabachnikov's problem prescribes.",
 r"""## Plain English

**Definition (`vertexCircumradius v i`, Gluck/Statements.lean lines 280–281).** dist(circumcenterR2(v_i, v_{i−1},
v_{i+1}), v_i).

On a non-collinear triple this is the circumradius R, equal to 1/|signed Menger curvature|
(`dist_circumcenterR2_eq_inv_abs_signedMenger`, used in Gluck/Discrete/TabachnikovConverse.lean line 242). On a
collinear triple the formula returns a junk value, but every theorem using it also assumes coherence, which rules
collinear triples out.
""",
 [q("For a counterclockwise coherent convex polygon, how does vertexCircumradius relate to the signed Menger curvature?", ["It is its reciprocal", "It is its square", "They are equal"], 0,
    "`IsCoherentConvexPolygon.vertexCircumradius_eq_inv`, Gluck/Discrete/TabachnikovCharacterization.lean lines 58–63."),
  q("Which triple's circle is used at vertex i?", ["v_{i−1}, v_i, v_{i+1}", "v_i, v_{i+1}, v_{i+2}"], 0,
    "Gluck/Statements.lean line 281."),
  q("What does vertexCircumradius return on a collinear triple?", ["A junk value of the total circumcentre formula; theorems exclude this case", "Infinity", "Zero always"], 0, "`circumcenterR2` divides by crossR2 = 0 (Gluck/Statements.lean lines 183–185)."),
 ])


node("Discrete.IsSimplePolygon",
 "Simple polygon",
 "A cyclic list of points is a simple polygon when no edge has length zero, consecutive edges meet only at their shared vertex, and non-adjacent edges don't meet at all.",
 r"""## Plain English

**Definition (`IsSimplePolygon v`, Gluck/Statements.lean lines 106–112).** For v : ZMod n → ℂ, with edges the
closed segments [v_i, v_{i+1}]:
1. v_i ≠ v_{i+1} for every i;
2. edge i and edge i+1 intersect in exactly {v_{i+1}};
3. edges i and j are disjoint whenever they are different and not adjacent.

That is the usual "the boundary doesn't cross itself" condition, stated with Mathlib's `segment`.
""",
 [q("Is a figure-eight quadrilateral (bow-tie) simple?", ["No: two non-adjacent edges cross", "Yes"], 0,
    "Condition 3, lines 111–112."),
  q("May two consecutive edges overlap along a segment?", ["No, their intersection must be exactly the shared vertex", "Yes"], 0,
    "Condition 2, lines 108–110."),
  q("Is a polygon with a repeated vertex v_i = v_{i+1} simple?", ["No, condition 1 forbids zero-length edges", "Yes"], 0, "Gluck/Statements.lean line 107."),
 ])


node("Discrete.IsCoherentConvexPolygon",
 "Coherent convex polygon",
 "Simple, strictly convex and counterclockwise (every vertex is strictly left of every edge not touching it), and coherent. This is the class of polygons in Tabachnikov's Problem 2.",
 r"""## Plain English

**Definition (`IsCoherentConvexPolygon v`, Gluck/Statements.lean lines 273–276).** Three conditions:
1. v is a [simple polygon](#/node/Discrete.IsSimplePolygon);
2. for every edge (v_a, v_{a+1}) and every vertex v_c with c ≠ a, a + 1: [crossR2](#/node/Discrete.crossR2)(v_a,
   v_{a+1}, v_c) > 0, i.e. v_c is strictly to the left of the edge. This is strict convexity with counterclockwise
   orientation; the same condition appears as `StrictConvexEdgeSupport` (lines 300–302);
3. v is [coherent](#/node/Discrete.CoherentR2).
""",
 [q("Is a clockwise square a coherent convex polygon in this sense?", ["No: the definition fixes counterclockwise orientation", "Yes"], 0,
    "Condition 2 asks for positive cross products (line 275). Reversing the labels fixes it."),
  q("Can three consecutive vertices be collinear?", ["No: strict convexity and coherence both forbid it", "Yes"], 0,
    "The middle vertex would lie on the line, not strictly to its left."),
  q("Which three ingredients make up IsCoherentConvexPolygon?", ["Simple, strictly convex counterclockwise, coherent", "Simple, inscribed in a circle, equilateral", "Convex and coherent only"], 0, "Gluck/Statements.lean lines 273–276."),
 ])


# ---------- the development ----------

node("Discrete.turningAngle",
 "Turning angles and the development",
 "Given curvatures κᵢ and edge lengths ℓᵢ, turn at vertex i by arcsin(κᵢℓᵢ₋₁/2) + arcsin(κᵢℓᵢ/2) and walk the edges. That is exactly the turn that makes the circle through three consecutive vertices have curvature κᵢ, so curvature data become a polygon-drawing recipe.",
 r"""## Plain English

**Turning angle** (`turningAngle K κ ℓ i`, Gluck/Statements.lean lines 72–73). arcsin(κ_i · tK(ℓ_{i−1}/2)) +
arcsin(κ_i · tK(ℓ_i/2)). The headlines all use K = 0 (the Euclidean plane), where `tK` is the identity, so the
turn is arcsin(κ_i ℓ_{i−1}/2) + arcsin(κ_i ℓ_i/2). The reason: a chord of length 2h in a circle of curvature κ meets
the tangent at angle arcsin(κh).

**Heading** (`heading κ ℓ j`, lines 78–79). The direction of edge j: the sum of the turns at vertices 0, …, j.

**Vertices** (`vertexR2 κ ℓ k`, lines 83–85). Start at 0 and add ℓ_j · e^{i·heading j} for j < k.

**Closure gap** (`closureGap`, lines 89–90). vertexR2 at k = n: where you end up after all n edges. The polygon
closes iff it is 0.

**Total turning** (`turningSum`, lines 94–95). The sum of all n turning angles.

**The polygon** (`polygonR2 κ ℓ`, lines 99–100). i ↦ vertexR2 κ ℓ i.

The general K ∈ {1, −1} versions (sphere, hyperbolic plane; `sK`, `cK`, `tK`, lines 43–54) are part of the
definitions but no headline uses them.
""",
 [q("With κ = 1 and all edges of length ℓ, what is the turning angle at each vertex?", ["2 arcsin(ℓ/2)", "ℓ", "arcsin(ℓ)"], 0,
    "K = 0 makes tK the identity (Gluck/Statements.lean lines 53–54, 72–73)."),
  q("When does the development close up?", ["When the closure gap vertexR2 κ ℓ n is 0", "When the total turning is 0", "Always"], 0,
    "Lines 89–90."),
  q("Why arcsin and not another formula?", ["It is analytic through κ = 0 and is the exact chord–tangent angle", "It is a small-angle approximation"], 0,
    "Docstring on lines 68–71."),
 ])


node("Discrete.ModerateArc",
 "Moderate arcs: the admissible edge lengths",
 "The edge lengths must be positive and short enough that each arcsin is defined with room to spare: |κᵢ|·ℓ/2 < 1 for both edges at vertex i. That strict wall keeps every turning angle below π.",
 r"""## Plain English

**Definition (`ModerateArc K κ ℓ`, Gluck/Statements.lean lines 64–66).** For every i: ℓ_i > 0, the branch conditions
sK(ℓ_i/2) > 0 and cK(ℓ_i/2) > 0 (automatic at K = 0), and

|κ_i| · tK(ℓ_{i−1}/2) < 1 and |κ_i| · tK(ℓ_i/2) < 1.

At K = 0 this is |κ_i| ℓ_{i−1}/2 < 1 and |κ_i| ℓ_i/2 < 1: each edge is shorter than the diameter 2/|κ_i| of the
circle it must be a chord of.

The paper writes the same as κ_i h_{i−1} < 1, κ_i h_i < 1 with half-lengths h.
""",
 [q("For κᵢ = 2, what bound does moderate-arc put on the adjacent edge lengths?", ["Each is < 1 (the diameter of a radius-1/2 circle)", "Each is < 2", "None"], 0,
    "|2| · ℓ/2 < 1 ⇔ ℓ < 1 (Gluck/Statements.lean line 66)."),
  q("Are zero-length edges allowed?", ["No, ℓᵢ > 0", "Yes"], 0,
    "First conjunct, line 65. (Anchors use zero-length edges internally, but the final realization has none.)"),
  q("What does moderate-arc guarantee about each turning angle?", ["It is strictly less than π", "It is exactly 2π/n", "It is negative"], 0, "Docstring of ModerateArc, Gluck/Statements.lean lines 58–63 (`abs_turningAngle_lt_pi`)."),
 ])


node("Discrete.RealizesR2",
 "Realizing a curvature word",
 "κ is realizable when some moderate edge lengths make the development close up (gap 0) after exactly one full turn (total 2π) and the resulting polygon is simple.",
 r"""## Plain English

**Definition (`RealizesR2 κ`, Gluck/Discrete/Defs.lean lines 222–224).** There exist edge lengths ℓ with
1. [ModerateArc](#/node/Discrete.ModerateArc) 0 κ ℓ;
2. [closureGap](#/node/Discrete.turningAngle) κ ℓ = 0;
3. turningSum κ ℓ = 2π;
4. polygonR2 κ ℓ is [simple](#/node/Discrete.IsSimplePolygon).

For positive κ, the project proves that such a polygon is automatically coherent and strictly convex, and its
signed Menger curvatures are exactly κ (used in [the collated converse](#/node/Discrete.tabachnikov_converse)). So
"κ is realizable" really means "some coherent convex polygon has curvatures κ".

It is the conclusion of [TabachnikovProblem2](#/node/Discrete.TabachnikovProblem2).
""",
 [q("Why require total turning exactly 2π?", ["So the polygon winds once around: a closed walk turning 4π would wrap twice", "To make the edges equal"], 0,
    "Condition 3 (Gluck/Discrete/Defs.lean line 224)."),
  q("Does RealizesR2 mention circumradii directly?", ["No, it is phrased with turning angles; the circle facts are lemmas", "Yes"], 0,
    "Lines 222–224."),
  q("Is simplicity part of RealizesR2 or a consequence?", ["Part of the definition (fourth conjunct)", "Not mentioned"], 0, "`IsSimplePolygon (polygonR2 κ ℓ)`, Gluck/Discrete/Defs.lean line 224."),
 ])


node("Discrete.TabachnikovProblem2",
 "Tabachnikov's Problem 2 as one proposition",
 "TabachnikovProblem2 n says: every positive curvature word of length n that is constant or has a strict four-vertex window at a positive level is realizable.",
 r"""## Plain English

**Definition (`TabachnikovProblem2 n`, Gluck/Discrete/TabachnikovReduction.lean lines 57–58).** For every
κ : ZMod n → ℝ, if `DiscreteFourVertexPos κ` then [`RealizesR2 κ`](#/node/Discrete.RealizesR2).

**The hypothesis class** (`DiscreteFourVertexPos κ`, Gluck/Discrete/Converse.lean lines 42–43). All κᵢ > 0, and
either κ is constant or it has a [four-vertex window](#/node/Discrete.DFV) at some level c > 0.

The same file proves this class equals "constant, or two plateau maxima and two plateau minima"
(`discreteFourVertexPos_iff_extrema`, lines 362–371; `tabachnikovProblem2_iff_extrema_form`, lines 382–387), so the
proposition is the literature's problem, not a weaker stand-in.

It is proved for n = 4 in this file (`tabachnikovProblem2_four`, lines 63–64) and for every n ≥ 4 in
[`tabachnikovProblem2_all`](#/node/Discrete.tabachnikovProblem2_all).
""",
 [q("Is the constant word included?", ["Yes", "No"], 0,
    "`(∃ c, ∀ i, κ i = c)` in Gluck/Discrete/Converse.lean line 43."),
  q("Why can the window level be required positive without loss?", ["For a positive word, any window level is automatically positive", "It can't; this is an extra assumption"], 0,
    "`DFV.pos_of_pos`, Gluck/Discrete/TabachnikovReduction.lean (the window supplies a positive value below c)."),
  q("For which n is TabachnikovProblem2 n proved?", ["Every n ≥ 4", "Only n = 4", "Only even n"], 0, "`tabachnikovProblem2_all`, Gluck/Discrete/TabachnikovFourActive.lean lines 41–44."),
 ])


node("Discrete.LocalDiscreteRealizationFamily",
 "A local C¹ family of realizations",
 "A structure bundling an open neighbourhood of curvature words, a C¹ length map on it, and proofs that every word in the neighbourhood is realized by its lengths, with vertex positions also C¹.",
 r"""## Plain English

**Structure (`LocalDiscreteRealizationFamily κ₀`, Gluck/Statements.lean lines 321–332).** Fields:
- `neighborhood`: an open set of words containing κ₀;
- `lengths`: a map from words to edge-length vectors, C¹ on the neighbourhood;
- for each κ in the neighbourhood: κ is positive, the lengths are [moderate](#/node/Discrete.ModerateArc), the
  closure gap is 0, the total turn is 2π, the polygon is [simple](#/node/Discrete.IsSimplePolygon);
- the vertex map κ ↦ polygonR2 κ (lengths κ) is C¹ on the neighbourhood.

So each member [realizes](#/node/Discrete.RealizesR2) its own word (`LocalDiscreteRealizationFamily.realizesR2`,
Gluck/Discrete/LocalContinuity.lean lines 37–39). "C¹" is Mathlib's `ContDiffOn ℝ 1` on finite-dimensional vectors.
""",
 [q("Which topology is used on curvature words?", ["The usual one on ℝⁿ (functions ZMod n → ℝ)", "A discrete topology"], 0,
    "File docstring of Gluck/Discrete/LocalContinuity.lean."),
  q("Must every word in the neighbourhood be positive?", ["Yes, that is a field", "No"], 0,
    "`positive`, Gluck/Statements.lean line 327."),
  q("Does the family's length map have to be C¹?", ["Yes, `contDiffOn_lengths` on the neighbourhood", "Only continuous"], 0, "Gluck/Statements.lean line 326."),
 ])


node("Discrete.GlobalContinuity.bandProfile",
 "The hexagon band path κ^s",
 "bandProfile s = (14, 11, 10+3s, 5, 7−3s, 3) for s ∈ [0,1]. Each word is positive and admissible, but the window levels jump from the lower band (5, 7−3s) to the upper band (11, 10+3s) as s goes from 0 to 1.",
 r"""## Plain English

**Definition (`bandProfile s`, Gluck/Statements.lean lines 445–446).** The six-entry word
(14, 11, 10 + 3s, 5, 7 − 3s, 3).

For s ∈ [0, 1] (Gluck/Discrete/GlobalContinuity/LevelBands.lean):
- it is positive (lines 29–32) and never constant (lines 34–40);
- its [four-vertex window](#/node/Discrete.DFV) levels are exactly (5, 7 − 3s) ∪ (11, 10 + 3s) (lines 42–67);
- the lower band is non-empty for s < 2/3 (window at indices 0, 3, 4, 5), the upper for s > 1/3 (indices 0, 1, 2, 5),
  so every word is admissible (lines 69 onward).

The levels must jump from one band to the other. The polygon-level version of this jump is the
[hexagon obstruction](#/node/Discrete.GlobalContinuity.no_continuous_regular_hexagon_path).
""",
 [q("At s = 0, which band of window levels is available?", ["Only the lower band (5, 7)", "Only the upper band", "Both"], 0,
    "Upper band (11, 10) is empty at s = 0."),
  q("At s = 1/2, which bands are non-empty?", ["Both: (5, 5.5) and (11, 11.5)", "Neither", "Only the lower"], 0,
    "7 − 1.5 = 5.5 and 10 + 1.5 = 11.5."),
  q("Is bandProfile s ever constant?", ["No, never (for any real s)", "Yes, at s = 1/2"], 0, "`bandProfile_nonconstant`, Gluck/Discrete/GlobalContinuity/LevelBands.lean lines 34–40: entries 14 and 3 always differ."),
 ])


node("Forward.DahlbergRegular",
 "Dahlberg regularity",
 "A polygon is Dahlberg-regular when at each vertex either the vertex lies on the straight segment between its neighbours, or the circle through the three has its centre in the closed angle at the vertex. It is a weaker relative of coherence, used in Dahlberg's theorem and in the hexagon obstruction.",
 r"""## Plain English

**Definition (`DahlbergRegularAt A B C`, Gluck/Statements.lean lines 366–368).** Either A, B, C are collinear with
B on the segment [A, C], or there is a circle through A, B, C (centre O, radius R > 0, `CircumcircleR2`,
lines 347–348) with O in the **closed** cone at B spanned by A − B and C − B (`InVertexCone`, lines 352–354).

**Definition (`DahlbergRegular v`, lines 371–372).** Every vertex is regular.

**Signed Menger profile** (`SignedMengerProfile v`, lines 375–376): see [crossR2](#/node/Discrete.crossR2).

[Coherence](#/node/Discrete.CoherentR2) implies regularity (`CoherentR2.dahlbergRegular`,
Gluck/Discrete/TabachnikovCharacterization.lean lines 25–41).
""",
 [q("Is a straight vertex (B the midpoint of AC) regular?", ["Yes, by the first alternative", "No"], 0,
    "Gluck/Statements.lean line 367."),
  q("Is a straight vertex coherent?", ["No, coherence forbids collinear triples", "Yes"], 0,
    "CoherentR2 requires crossR2 ≠ 0 (line 198)."),
  q("Does coherence imply Dahlberg regularity?", ["Yes", "No"], 0, "`CoherentR2.dahlbergRegular`, Gluck/Discrete/TabachnikovCharacterization.lean lines 25–41."),
 ])


# ---------- side-tangent ----------

node("Discrete.SideTangent.RealizesSideTangent",
 "Side-tangent realization",
 "ρ is side-tangent realized when a simple strictly convex polygon has, at every edge i, a unique inward circle of radius ρᵢ tangent to the lines of edges i−1, i, i+1, touching edge i inside the edge.",
 r"""## Plain English

**Three-line circle** (`ThreeLineCircle P N i C r`, Gluck/Statements.lean lines 410–412). With N the outward unit
normals of the edges, the point C is at signed distance r inward from the lines of edges i − 1, i and i + 1.

**Realization** (`IsSideTangentRealization ρ P N C`, lines 415–425) bundles:
- all ρᵢ > 0; P is [simple](#/node/Discrete.IsSimplePolygon) and strictly convex (`StrictConvexEdgeSupport`);
- each Nᵢ is a unit vector and edge i points along i·Nᵢ (so Nᵢ is the outward normal, counterclockwise);
- each edge line supports the polygon;
- at each i, C_i and ρ_i satisfy the three-line equations, and they are the **only** solution;
- the central contact C_i + ρ_i N_i lies in the open edge (P_i, P_{i+1}).

**`RealizesSideTangent ρ`** (lines 428–429): some P, N, C form such a realization.
""",
 [q("Must the contacts on the neighbouring lines lie on the edges themselves?", ["No, only the central contact must be inside its edge", "Yes, all three"], 0,
    "`central_contact`, line 425; paper Definition 8.1."),
  q("Is the circle at edge i uniquely determined by the polygon?", ["Yes, the `unique_circle` field says so", "No"], 0,
    "`unique_circle`, Gluck/Statements.lean line 424."),
  q("Which way do the normals N point?", ["Outward: edge i points along i·Nᵢ, a counterclockwise quarter-turn of Nᵢ", "Inward"], 0, "`oriented_edge`, Gluck/Statements.lean line 421, and the SideTangentConverse.lean header."),
 ])


node("Discrete.SideTangent.SideTangentAdmissible",
 "Side-tangent admissibility: four sign changes of the differences",
 "ρ is admissible when all ρᵢ > 0 and either ρ is constant or the differences ρᵢ₋₁ − ρᵢ have a four-vertex window at level 0: positive, negative, positive, negative in cyclic order. Zero differences are allowed and simply don't count.",
 r"""## Plain English

**Definition (`radiusDifference ρ i`, Gluck/Statements.lean line 393).** ρ_{i−1} − ρ_i.

**Definition (`SideTangentAdmissible ρ`, lines 432–433).** All ρᵢ > 0 and either ρ is constant, or
[`DFV`](#/node/Discrete.DFV) (radiusDifference ρ) 0: there are four cyclically ordered positions where the
difference is > 0, < 0, > 0, < 0.

Repeated adjacent radii give zero differences. They are kept, but they don't count as a sign. This is the hypothesis
of Wegner's four-edge theorem.
""",
 [q("Is ρ = (1, 1, 2, 2) admissible?", ["No: the differences (1, 0, −1, 0) change sign only twice", "Yes"], 0,
    "Cyclic differences ρ₃−ρ₀ = 1, 0, −1, 0. Only one + and one −."),
  q("Is ρ = (1, 2, 1, 2, 1, 2) admissible?", ["Yes", "No"], 0,
    "The cyclic differences alternate +1, −1, +1, … (ρ₅ − ρ₀ = 1, ρ₀ − ρ₁ = −1, …)."),
  q("Does a zero difference count as a sign change?", ["No, zero differences are kept but not counted", "Yes"], 0, "DFV uses strict inequalities against 0 (Gluck/Statements.lean lines 133–134)."),
 ])
