NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

NOT_BUILT = "Complete in the source (no sorry or axiom in the project). Not built for this site."


node("Discrete.RegularFourAnchor",
 "Regular four-edge anchor: the key object of the proof",
 "Put all the length on four chosen edges and collapse the rest to points. A regular anchor is a positive solution of the three closure equations in those four lengths with onto derivative. One is enough: the implicit function theorem opens every collapsed edge.",
 r"""## Plain English

**Structure (`RegularFourAnchor κ`, Gluck/Discrete/RegularFourAnchor.lean lines 19–26).** Data:
- a **frame**: four distinct edge indices e₀ < e₁ < e₂ < e₃ < n (`FourActiveSlots.Frame`,
  Gluck/Discrete/FourActiveSlotEmbedding.lean lines 25–28);
- four positive half-lengths L₀, …, L₃;
- the moderate-arc bounds: each half-length times each of the two curvatures read at the ends of its edge is < 1;
- `zero`: the **controller** vanishes at L. The controller (lines 212–217 of the same file) is the closure gap of
  the quadrilateral built from the four edges, together with (total turn − 2π). Only the eight end readings of the
  four edges enter it;
- `regular`: the derivative of the controller at L, a linear map ℝ⁴ → ℂ × ℝ ≅ ℝ³, is surjective.

**Why it suffices** (`RegularFourAnchor.realizesR2`, lines 30–32, via
`FourActiveSlots.Frame.realizesR2_of_controller_regular`, Gluck/Discrete/FourActiveSlotEmbedding.lean lines 420–439).
With every other edge at length 0, the quadrilateral already solves the closure equations of the full word. A
full-rank derivative lets the implicit function theorem (`realizesR2_of_regular_dormant_anchor_of_active_surj`,
Gluck/Discrete/RegularDormantOpening.lean lines 139–171) give the dormant edges small positive lengths while it
corrects the four active ones. The prescribed curvatures are kept exactly.

**Why it transports.** The controller depends only on the eight end readings, so an anchor can be moved to any word
with the same end readings, however many "dormant" readings sit between (`reembed`, lines 47–57). This is what makes
the constant-run reduction and the rescaling/rotation symmetries cheap.
""",
 [q("How many unknowns and equations does the anchor system have?", ["4 unknowns, 3 equations", "n unknowns, n equations", "4 unknowns, 4 equations"], 0,
    "L : Fin 4 → ℝ and a controller valued in ℂ × ℝ (Gluck/Discrete/FourActiveSlotEmbedding.lean lines 212–217)."),
  q("Which curvature readings does the controller depend on?", ["Only the two readings at the ends of each of the four active edges", "All n readings"], 0,
    "`controller_eq_of_endpoints`, Gluck/Discrete/RegularFourAnchor.lean lines 36–42."),
  q("What does 'regular' buy?", ["A surjective derivative, so the implicit function theorem applies", "Equal edge lengths", "Coherence"], 0,
    "Field `regular`, line 26."),
 ],
 caveats=[NOT_BUILT])


node("Discrete.nonempty_regularFourAnchor_of_adjacent_unequal_dfv",
 "Producing an anchor: the three-case construction",
 "Every positive window word with no two equal neighbours has a regular four-edge anchor. Either the global maximum is repeated (case R), or the highest secondary peak and a sign 'flag' choose between a first-transition frame (case F) and an orthogonal frame (case N).",
 r"""## Plain English

**Theorem (`nonempty_regularFourAnchor_of_adjacent_unequal_dfv`, Gluck/Discrete/UniversalRegularFourAnchor.lean
lines 118–136).** If n ≥ 4, all κᵢ > 0, κ has a [window](#/node/Discrete.DFV) and κᵢ ≠ κᵢ₊₁ for all i, then a
[regular anchor](#/node/Discrete.RegularFourAnchor) exists.

**The case split** (paper §2 and §6):

- **(R) Repeated maximum** (lines 127–129; `nonempty_regularFourAnchor_of_repeated_normalized_maximum`,
  Gluck/Discrete/RepeatedMaximumAnchor.lean lines 64–95). Use the edges at the two maxima; an explicit quadrilateral
  with perpendicular diagonals, deformed in two parameters, gives the anchor.
- Otherwise pick the **highest secondary peak** q, the highest strict local maximum other than the global maximum H
  (`HighestSecondaryPeak`, Gluck/Discrete/CurvatureMountainSelection.lean lines 30–33; it exists by
  `exists_highestSecondaryPeak`, lines 37–51). Rescale so κ_q = 1 and rotate indices so q = 0 (lines 74–88). Then a
  number built from four readings, the forward flag (`firstPairFlag`), decides:
  - **(F)** forward or backward flag ≥ 0: a "first transition" frame (lines 90–93);
  - **(N)** both negative: the edges at the two peaks, again an orthogonal quadrilateral (lines 94–95,
    `nonempty_regularFourAnchor_of_negative_terminals`, Gluck/Discrete/NegativeCornerAnchorSelection.lean lines 37–66).

Each construction finds a zero with the intermediate value theorem or the Poincaré–Miranda theorem, and proves
full rank by an explicit computation. These sub-proofs are most of the ~48,000 lines in Gluck/Discrete.
""",
 [q("Which case applies when the global maximum value appears twice?", ["(R), the repeated-maximum construction", "(F)", "(N)"], 0,
    "Lines 127–129."),
  q("Why may the construction assume κ_q = 1?", ["Anchors survive positive rescaling and cyclic re-indexing", "Because κ is normalized in the hypothesis"], 0,
    "`nonempty_regularFourAnchor_of_normalizedAt`, lines 26–38."),
  q("Why assume no two neighbours are equal here?", ["Equal neighbours are removed beforehand by the constant-run reduction", "The theorem is false otherwise"], 0,
    "See the constant-run reduction (Gluck/Discrete/ConstantRunAnchorReduction.lean lines 183–212)."),
 ],
 caveats=[NOT_BUILT,
  "This explainer summarises the three constructions from the paper's description; the individual Lean sub-proofs (orthogonal cores, rank computations, sign tables) were not read in detail."])


node("Discrete.ConstantRun.nonempty_regularFourAnchor_of_adjacent_unequal_producer",
 "Removing and restoring repeated readings",
 "If anchors exist for every word without equal neighbours, they exist for every window word: delete one of two equal adjacent readings, find an anchor for the shorter word by induction, and put the reading back as a dormant edge. The window survives deletion, and the anchor survives restoration.",
 r"""## Plain English

**Theorem (Gluck/Discrete/ConstantRunAnchorReduction.lean lines 183–212).** Assume a producer: every positive
window word of any length m ≥ 4 with no equal neighbours has a [regular anchor](#/node/Discrete.RegularFourAnchor).
Then every positive word with a [window](#/node/Discrete.DFV) has one.

The producer is supplied unconditionally by
[the three-case construction](#/node/Discrete.nonempty_regularFourAnchor_of_adjacent_unequal_dfv), so in the
headline this premise is discharged.

**How.** Strong induction on the length k (line 194):
- if no two neighbours are equal, use the producer (line 198);
- otherwise some wᵢ = wᵢ₊₁. Erase one of them (`eraseWord`, lines 74–75); the shorter word still has a window
  (`eraseWord_dfv`, lines 173–178) and is positive. Get its anchor by induction, then restore the erased reading
  (`restoreAnchor`, lines 160–165), which only adds a dormant edge and keeps the eight active end readings.
""",
 [q("What happens to the four-vertex window when a repeated reading is deleted?", ["It survives", "It may disappear", "It doubles"], 0,
    "`eraseWord_dfv`, Gluck/Discrete/ConstantRunAnchorReduction.lean lines 173–178."),
  q("Is the producer a remaining assumption of the main theorem?", ["No, the headline supplies it from the proved construction", "Yes"], 0,
    "Gluck/Discrete/TabachnikovFourActive.lean lines 27–29 and 43–44."),
  q("What kind of induction drives the reduction?", ["Strong induction on the word length", "Induction on the number of maxima", "No induction"], 0, "`Nat.strong_induction_on`, Gluck/Discrete/ConstantRunAnchorReduction.lean line 194."),
 ],
 caveats=[NOT_BUILT])


node("Forward.dahlberg_discrete_four_vertex_E2",
 "Dahlberg's discrete four-vertex theorem (the forward direction)",
 "A simple, Dahlberg-regular polygon with n ≥ 4 vertices that is not inscribed in a circle has signed Menger curvature with two local maxima and two local minima, alternating around the polygon in the plateau-aware sense. The project proves this from scratch (Gluck/Forward, about 27,000 lines).",
 r"""## Plain English

**Theorem (`dahlberg_discrete_four_vertex_E2`, Gluck/Forward/Euclidean.lean lines 26–34).** Let n ≥ 4 and v a
[simple](#/node/Discrete.IsSimplePolygon), [Dahlberg-regular](#/node/Forward.DahlbergRegular) polygon whose vertices
do not all lie on one circle (`Concyclic`, Gluck/Forward/Discrete/Defs.lean lines 12–13). Then the
[signed Menger curvature](#/node/Discrete.crossR2) profile satisfies `DahlbergFourVertex`
(Gluck/Forward/Kernel.lean lines 448–454): there are i₁ < i₂ < i₃ < i₄ < i₁ + n with a local max, min, max, min at
those positions, in Dahlberg's plateau-aware sense.

This is B. Dahlberg's discrete four-vertex theorem ("A discrete four vertex theorem", Geom. Dedicata). In the
project it is the "only if" half of the [characterization](#/node/Discrete.tabachnikov_radius_characterization).
The proof follows Dahlberg's paper (disk arguments: containing disks, the minimal enclosing disk, and the alternation
of their boundary contacts) and lives in Gluck/Forward/Discrete, whose biggest files are Dahlberg.lean
(~6,250 lines) and DahlbergRegions.lean (~6,000 lines). Many intermediate theorems there are named after the
lemmas of the paper ("Theorem 6", "Lemma 5", "Lemma 7", "Lemma 9").
""",
 [q("Why the 'not concyclic' hypothesis?", ["A polygon inscribed in a circle has constant curvature, with no strict extrema", "Concyclic polygons aren't simple"], 0,
    "Hypothesis `hnoncircle`, line 29."),
  q("Does the theorem need convexity?", ["No: simple and Dahlberg-regular suffice", "Yes, strict convexity"], 0,
    "Hypotheses on lines 27–29."),
  q("Which curvature is the theorem about?", ["Signed Menger curvature, 1/circumradius with sign", "Turning angle", "Edge length"], 0, "`signedMengerR2 (v (i - 1)) (v i) (v (i + 1))`, Gluck/Forward/Euclidean.lean line 31."),
 ],
 caveats=[NOT_BUILT,
  "The ~27,000 lines of the forward proof are summarised here, not explained step by step."])


node("Discrete.RunsRealizes",
 "Leftovers: an earlier, conditional route (strata hypotheses)",
 "Gluck/Discrete/TabachnikovReduction.lean keeps an older reduction of Problem 2 to three 'stratum' propositions (zigzag, runs, plateau) whose docstrings say they are not discharged. They are hypotheses of a few theorems, not axioms, and the main theorem doesn't use them.",
 r"""## Plain English

**Definitions.** `RunsRealizes n` (Gluck/Discrete/TabachnikovReduction.lean lines 83–85), `PlateauRealizes n`
(lines 98–100) and `ZigzagRealizes` (Gluck/Discrete/ZigzagWords.lean lines 456–457) are propositions saying that
certain sub-classes of window words are realizable. Some theorems in TabachnikovReduction.lean (for example
`realizesMenger_of_strata_extrema`) take them as **hypotheses**.

The docstrings say in capitals "NOT discharged anywhere in this development; open research". That was true of this
route. The general theorem [`tabachnikovProblem2_all`](#/node/Discrete.tabachnikovProblem2_all) is proved by a
different argument (four-active-edge anchors), which the file header itself says (lines 18–26). Since
TabachnikovProblem2 n covers every positive window word, it implies all three stratum propositions, though the
project doesn't state that implication.

**Why mention it.** A reader grepping for "NOT discharged" could think the main result is conditional. It isn't:
none of the six headlines depends on these propositions.
""",
 [q("Are RunsRealizes/PlateauRealizes axioms?", ["No, they are definitions of propositions, used only as hypotheses", "Yes"], 0,
    "`def RunsRealizes …: Prop`, Gluck/Discrete/TabachnikovReduction.lean line 83; grep finds no `axiom`."),
  q("Does tabachnikovProblem2_all assume them?", ["No", "Yes"], 0,
    "Gluck/Discrete/TabachnikovFourActive.lean lines 41–44."),
  q("What does the main theorem imply about these strata propositions?", ["It implies all three, since it covers every positive window word", "Nothing"], 0, "TabachnikovProblem2 n covers every positive window word (Gluck/Discrete/TabachnikovReduction.lean lines 57–58)."),
 ])


node("gluck_converse",
 "Side result: the smooth converse four-vertex theorem",
 "The project also proves the smooth converse four-vertex theorem (Gluck, Dahlberg): a continuous 2π-periodic positive function that is constant or has two value-separated maxima and minima is the curvature of a simple closed curve. It is separate from the discrete problem.",
 r"""## Plain English

**Theorem (`gluck_converse`, Gluck/Euclidean/FourVertex.lean lines 216–321).** Let κ be a
curvature function (`IsCurvatureFunction`): continuous, 2π-periodic, positive (Gluck/Curvature.lean
lines 32–33). If κ satisfies `FourVertexCondition` (lines 61–65): constant, or local maxima p₁, p₂ and minima q₁, q₂
alternating in one period with max(κ(q₁), κ(q₂)) < min(κ(p₁), κ(p₂)), then some simple closed curve γ realizes κ
as its curvature, parametrised by tangent angle.

The value separation of the extrema is Dahlberg's hypothesis (the file says so in lines 50–60). It is stronger than
just "two maxima and two minima". The proof goes through a reconstruction integral and a winding-number argument
(Gluck/Winding.lean, Gluck/Euclidean/Reduction.lean, and the topological winding number in
ForMathlib/Analysis/Complex/WindingNumber.lean).

This part (about 5,600 lines in Gluck/*.lean, Gluck/Euclidean, Gluck/SpaceForm, Gluck/Topology) is where the
library's name comes from. It is not one of the paper's six theorems, and this site doesn't explain it further.
""",
 [q("Is the smooth hypothesis 'two maxima and two minima' or something stronger?", ["Stronger: both minima must lie strictly below both maxima", "Exactly two maxima and two minima"], 0,
    "`max (κ q₁) (κ q₂) < min (κ p₁) (κ p₂)`, Gluck/Curvature.lean line 65."),
  q("Is this theorem used for the discrete headlines?", ["No, it is a separate result (though the winding-number tools are shared)", "Yes, by taking limits"], 0,
    "The discrete proof works with finite closure equations and anchors."),
  q("Which curves does gluck_converse produce?", ["Simple closed curves realizing κ", "Polygons", "Curves on the sphere"], 0, "`∃ γ : ℝ → ℂ, IsSimpleClosed γ ∧ RealizesCurvature γ κ`, Gluck/Euclidean/FourVertex.lean line 218."),
 ],
 caveats=[NOT_BUILT,
  "The 'realizes curvature' notion for a merely continuous κ is intrinsic (the curve is only C¹); see the docstring before line 216. Not examined in detail for this site.",
  "The docstring mentions a second proof `gluck_converse_flow` in Gluck/Euclidean/SpaceFormInstance.lean; that file is not in the repository at the pinned commit."])


node("poincare_miranda",
 "ForMathlib: general tools proved along the way",
 "The ForMathlib folder (about 2,400 lines, importing only Mathlib) holds general results the proof needed: the Poincaré–Miranda theorem on a rectangle, a topological winding number for continuous loops, projective balance lemmas, and parametric implicit-function corrections.",
 r"""## Plain English

**Poincaré–Miranda** (`poincare_miranda`, ForMathlib/Analysis/Complex/PoincareMiranda.lean lines 506–619). A
continuous map G = (G₁, G₂) on a rectangle [a₁, a₂] × [b₁, b₂], with G₁ ≤ 0 on the left side, G₁ ≥ 0 on the right
side, G₂ ≤ 0 on the bottom and G₂ ≥ 0 on the top, has a zero in the rectangle. It is the 2D intermediate value
theorem, used to find anchor zeros.

**Other ForMathlib files.**
- ForMathlib/Analysis/Complex/WindingNumber.lean: a winding number for merely continuous loops
  (`Complex.windingNumberAt`, lines 274–275); Mathlib only has the holomorphic one.
- ForMathlib/Analysis/Complex/ConeWinding.lean, DiamondWinding.lean, DiamondStability.lean: sign conditions on a
  square's boundary that force a zero.
- ForMathlib/Analysis/InnerProductSpace/Projective*.lean: balance lemmas for the side-tangent construction.
- ForMathlib/Analysis/Calculus/ParametricConstraintCorrection.lean, ParametricPositiveSection.lean and
  ForMathlib/Topology/Order/ParametricRoot.lean: implicit-function style corrections with parameters, used to open
  dormant edges and for the C¹ local family.

The README says these are "staged for upstreaming" to Mathlib.
""",
 [q("What is Poincaré–Miranda the 2D version of?", ["The intermediate value theorem", "The mean value theorem", "Rolle's theorem"], 0,
    "Its docstring names `intermediate_value_Icc` as the 1-dimensional analogue (ForMathlib/Analysis/Complex/PoincareMiranda.lean lines 495–505)."),
  q("May the zero lie on the boundary of the rectangle?", ["Yes, the face inequalities are weak", "No"], 0,
    "Docstring, same lines."),
  q("Does ForMathlib depend on the Gluck library?", ["No, it imports only Mathlib", "Yes"], 0, "README, Contents table: 'Mathlib-only imports, staged for upstreaming'."),
 ],
 caveats=[NOT_BUILT])
