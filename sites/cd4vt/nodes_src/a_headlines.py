NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]

NOT_BUILT = ("Complete in the source: the project has no sorry and no axiom, and the README says `#print axioms` "
             "shows only propext, Classical.choice and Quot.sound. The Lean was not built for this site, so this "
             "is not our own kernel check.")


node("Discrete.tabachnikov_converse_geometric",
 "Headline: two-max, two-min radii come from a coherent convex polygon (Thm 1.1)",
 "Take n ≥ 4 positive numbers in a cycle with two local maxima and two local minima (a flat run counts once). Some strictly convex n-gon has them as the radii of the circles through its consecutive vertex triples, each centre inside its vertex angle. This answers Tabachnikov's Problem 2.",
 r"""## Plain English

**Theorem (`tabachnikov_converse_geometric`, Gluck/Discrete/TabachnikovConverse.lean lines 254–258; Theorem 1.1 of
the paper).** Let n ≥ 4 and let r₀, …, r_{n−1} be positive numbers read cyclically (indices in `ZMod n`). Suppose r
[has two distinct plateau maxima and two distinct plateau minima](#/node/Discrete.IsPlateauTwoMaxTwoMin). Then there
is a polygon v₀, …, v_{n−1} in the plane (points of ℂ) such that

- v is a [coherent convex polygon](#/node/Discrete.IsCoherentConvexPolygon): simple, strictly convex,
  counterclockwise, and for each i the centre of the circle through v_{i−1}, v_i, v_{i+1} lies strictly inside the
  angle at v_i;
- for every i, the [radius of that circle](#/node/Discrete.vertexCircumradius) is exactly r_i.

### Where it comes from

Tabachnikov ("Converse Sturm–Hurwitz–Kellogg theorem and related results", arXiv:0710.5902) asked this as Problem 2.
It is a discrete cousin of the *converse four-vertex theorem* for smooth curves (Gluck, Dahlberg): any positive
function with two maxima and two minima is the curvature of a simple closed convex curve. Here the "curvature" at a
vertex is 1/r_i, the curvature of the circle through that vertex and its two neighbours.

The forward direction (every such polygon's radii have four extrema) is Dahlberg's discrete four-vertex theorem;
see the [characterization](#/node/Discrete.tabachnikov_radius_characterization).

### How it is proved, in one paragraph

Turn radii into curvatures κ_i = 1/r_i. Two maxima of r are two minima of κ and vice versa, so κ is in the
hypothesis class of [Tabachnikov's Problem 2 in curvature form](#/node/Discrete.TabachnikovProblem2), which is
[proved for every n ≥ 4](#/node/Discrete.tabachnikovProblem2_all). That gives edge lengths ℓ whose
[development](#/node/Discrete.RealizesR2) closes up into a simple polygon. A separate lemma shows such a polygon is
automatically coherent and strictly convex, and its circumradii are 1/κ_i = r_i. The packaging is done in the
stronger [collated theorem](#/node/Discrete.tabachnikov_converse); this headline just drops two extra conclusions.
""",
 [q("Which sequence satisfies the hypothesis (n = 6, cyclic)?", ["1, 3, 1, 3, 1, 3", "1, 2, 3, 4, 5, 6", "2, 2, 2, 2, 2, 2"], 0,
    "1,3,1,3,1,3 has three plateau maxima and three minima. 1..6 has only one of each cyclically; the constant has none (Gluck/Statements.lean lines 206–247)."),
  q("What does 'coherent' add beyond convexity?", ["Each vertex's circumcentre lies inside that vertex's angle", "All vertices lie on one circle", "All edges have equal length"], 0,
    "`CoherentR2`, Gluck/Statements.lean lines 197–199."),
  q("Is the polygon unique?", ["No; the theorem only says one exists", "Yes, up to rotation", "Yes, up to similarity"], 0,
    "The conclusion is ∃ v (line 256). The paper's Figure on the method shows two different realizations of one word."),
  q("Is n = 3 covered?", ["No, the theorem needs 4 ≤ n", "Yes"], 0,
    "Hypothesis `hn : 4 ≤ n`, line 254. A cyclic sequence of length 3 can't have two maxima and two minima anyway."),
  q("What is a constant sequence's status here?", ["Not covered: a constant sequence has no strict plateau extrema", "Covered: it gives the regular n-gon"], 0,
    "PlateauMaxRun needs strict drops on both sides (Gluck/Statements.lean lines 206–209). The regular n-gon is handled elsewhere (`realizesR2_of_const`, Gluck/Discrete/Converse.lean lines 64–68)."),
 ],
 caveats=[NOT_BUILT,
  "Faithfulness: 'local maximum' is read plateau-aware (a maximal flat run with strictly lower neighbours on both ends counts once). This is Dahlberg's convention, and the paper calls it the sharp form. A reader who counts each point of a plateau separately would get a different (false) statement.",
  "Polygons are labelled tuples `ZMod n → ℂ`; 'convex' is encoded as: every vertex lies strictly to the left of every edge not incident to it (Gluck/Statements.lean line 275)."],
 widgets=walk("How the proof goes (Gluck/Discrete/TabachnikovConverse.lean, lines 254-258)", [
  {"text": "Apply the collated theorem tabachnikov_converse to the same data (line 258).", "link": "Discrete.tabachnikov_converse"},
  {"text": "It returns a polygon with four properties: coherent-convex, prescribed circumradii, prescribed signed Menger curvature 1/rᵢ, and a non-degeneracy clause. Keep the first two (line 258).",
   "lean": "(tabachnikov_converse hn hr hext).imp fun _ h ↦ ⟨h.1, h.2.1⟩"},
 ]))


node("Discrete.tabachnikov_converse",
 "The collated converse: radii, Menger curvature and non-degeneracy",
 "The working form of Theorem 1.1. Besides the coherent convex polygon with circumradii rᵢ, it records that the signed Menger curvature at each vertex is 1/rᵢ, and that when no two neighbouring radii are equal, no four consecutive vertices lie on one circle.",
 r"""## Plain English

**Theorem (`tabachnikov_converse`, Gluck/Discrete/TabachnikovConverse.lean lines 224–250).** Same hypotheses as the
[headline](#/node/Discrete.tabachnikov_converse_geometric). There is a polygon v that

1. is a [coherent convex polygon](#/node/Discrete.IsCoherentConvexPolygon);
2. has [circumradius](#/node/Discrete.vertexCircumradius) r_i at every vertex;
3. has [signed Menger curvature](#/node/Discrete.crossR2) exactly 1/r_i at every vertex (positive, since the polygon
   turns left);
4. if r_i ≠ r_{i+1} for all i, then no four consecutive vertices v_{i−1}, v_i, v_{i+1}, v_{i+2} are concyclic
   (`Concyclic4`, lines 137–138). Tabachnikov states this non-degeneracy as part of his setting.

### The idea

Everything happens in curvature language. With κ_i = 1/r_i the reciprocal sequence is in the extremum-form
hypothesis class (`discreteFourVertexExtrema_inv`, lines 156–162), so the general
[Problem 2 theorem](#/node/Discrete.tabachnikovProblem2_all) produces edge lengths ℓ that make the
[development](#/node/Discrete.RealizesR2) close up. Then three geometric lemmas about closed developments do the
rest: coherence (`coherent_development_moderate`, Gluck/Discrete/LocalRegularity.lean lines 558–627), the Menger
curvature identity (`signedMengerR2_polygonR2`, line 110 onward), and strict convexity
(`crossR2_polygonR2_edge_vertex_pos`, Gluck/Discrete/Convexity.lean line 341 onward).

The non-degeneracy clause is short: if four consecutive vertices were on one circle, the two triples inside them
would have the same circumcircle, so r_i = r_{i+1} (`vertexCircumradius_eq_of_concyclic`, lines 200–215).
""",
 [q("Which way does the polygon turn?", ["Counterclockwise (left), so the signed Menger curvature is +1/rᵢ", "Clockwise", "Either"], 0,
    "Conclusion 3, line 228, and the positive cross-product condition in IsCoherentConvexPolygon."),
  q("When does the theorem promise no four consecutive concyclic vertices?", ["Only when all neighbouring radii differ", "Always", "Never"], 0,
    "The implication on lines 229–230."),
  q("What is the polygon, concretely?", ["The development polygonR2 κ ℓ built from the curvatures κ = 1/r and the lengths ℓ", "A regular n-gon", "A polygon inscribed in a circle"], 0,
    "`refine ⟨polygonR2 κ ℓ, …` on line 244."),
 ],
 caveats=[NOT_BUILT],
 widgets=walk("How the proof goes (Gluck/Discrete/TabachnikovConverse.lean, lines 224-250)", [
  {"text": "Set κᵢ = 1/rᵢ, which is positive (lines 231–232)."},
  {"text": "κ has two plateau maxima and two plateau minima (they swap roles under 1/x), so Problem 2 in its extremum form gives RealizesR2 κ (lines 233–235).", "link": "Discrete.tabachnikovProblem2_all",
   "lean": "tabachnikovProblem2_iff_extrema_form.mp (tabachnikovProblem2_all hn) κ"},
  {"text": "Unpack: lengths ℓ, moderate arcs, closure gap 0, total turn 2π, simple polygon (line 236).", "link": "Discrete.RealizesR2"},
  {"text": "Closed moderate-arc developments are coherent, and their signed Menger curvatures are κ (lines 238–239).", "link": "Discrete.CoherentR2"},
  {"text": "Circumradius = 1/|Menger curvature| = 1/κᵢ = rᵢ (lines 240–243).", "link": "Discrete.vertexCircumradius"},
  {"text": "Assemble: simple, strictly convex (positive cross products), coherent (lines 244–246)."},
  {"text": "Non-degeneracy: four concyclic consecutive vertices would force rᵢ = rᵢ₊₁ (lines 247–250)."},
 ]))


node("Discrete.tabachnikov_radius_characterization",
 "Headline: the exact characterization of circumradius sequences (Corollary 1.2)",
 "For nonconstant positive data with n ≥ 4: the numbers are the vertex circumradii of some coherent convex polygon if and only if they have two distinct plateau maxima and two distinct plateau minima. The 'only if' half is Dahlberg's discrete four-vertex theorem, which the project also proves.",
 r"""## Plain English

**Theorem (`tabachnikov_radius_characterization`, Gluck/Discrete/TabachnikovCharacterization.lean lines 88–109;
Corollary 1.2).** Let n ≥ 4 and let r be a positive cyclic sequence that is **not constant**. Then

> some [coherent convex polygon](#/node/Discrete.IsCoherentConvexPolygon) has
> [circumradii](#/node/Discrete.vertexCircumradius) r
> **if and only if**
> r [has two distinct plateau maxima and two distinct plateau minima](#/node/Discrete.IsPlateauTwoMaxTwoMin).

- **⇐** is the [converse theorem](#/node/Discrete.tabachnikov_converse_geometric) (line 109).
- **⇒** is [Dahlberg's discrete four-vertex theorem](#/node/Forward.dahlberg_discrete_four_vertex_E2), translated
  from curvatures to radii (lines 93–108).

### Why "nonconstant" is needed

A constant sequence is realized (by the regular n-gon), but it has no strict maxima or minima, so the right-hand side
is false. Without the hypothesis the equivalence would fail. With it, this is a clean "exactly these sequences"
statement.
""",
 [q("Why does the theorem assume r is not constant?", ["A constant r is realized (regular n-gon) but has no plateau extrema, so the iff would fail", "Constant sequences can't be realized", "Dahlberg's theorem fails for squares"], 0,
    "Hypothesis `hnc`, line 89; constant case in Gluck/Discrete/Converse.lean lines 64–68."),
  q("Which direction uses Dahlberg's theorem?", ["Polygon ⇒ two max, two min", "Two max, two min ⇒ polygon"], 0,
    "`dahlberg_discrete_four_vertex_E2` on line 101, inside the forward (rintro) branch."),
  q("In the ⇒ direction, why is the polygon not concyclic?", ["All vertices on one circle would make every circumradius equal, contradicting nonconstancy", "Because n ≥ 4", "Because the polygon is simple"], 0,
    "Lines 94–100."),
  q("Is the forward direction assumed from the literature?", ["No, Dahlberg's theorem is proved in the project (Gluck/Forward)", "Yes, as an axiom"], 0,
    "The project has no `axiom`; Gluck/Forward/Euclidean.lean lines 26–34 is a theorem."),
 ],
 caveats=[NOT_BUILT,
  "The circle here is the circle through three consecutive vertices, not a circle tangent to sides; the tangent-circle analogue is a separate headline (realizesSideTangent_iff_admissible)."],
 widgets=walk("How the proof goes (Gluck/Discrete/TabachnikovCharacterization.lean, lines 88-109)", [
  {"text": "⇒: take a coherent convex polygon v with circumradii r (line 93)."},
  {"text": "v is not concyclic: a circle through all vertices would make the Menger curvature constant, so r would be constant (lines 94–100)."},
  {"text": "Coherence (open cone) implies Dahlberg regularity (closed cone). Apply Dahlberg's theorem to get four alternating plateau extrema of the curvature (line 101).", "link": "Forward.dahlberg_discrete_four_vertex_E2",
   "lean": "have hfv := dahlberg_discrete_four_vertex_E2 hn v hv.1 hv.2.2.dahlbergRegular hnoncircle"},
  {"text": "The curvature is positive, so its reciprocal r again has four alternating extrema (lines 102–104)."},
  {"text": "r equals that reciprocal, so it has two plateau maxima and two plateau minima (lines 105–108)."},
  {"text": "⇐: the converse theorem (line 109).", "link": "Discrete.tabachnikov_converse_geometric"},
 ]))


node("Discrete.tabachnikovProblem2_all",
 "Headline: Tabachnikov's Problem 2 in curvature form, for every n ≥ 4",
 "Every positive cyclic curvature word (n ≥ 4) that is constant or has a strict four-vertex window is realized by a closed simple polygon. The proof puts all length on four chosen edges, solves three equations there, and opens the other edges by the implicit function theorem.",
 r"""## Plain English

**Theorem (`tabachnikovProblem2_all`, Gluck/Discrete/TabachnikovFourActive.lean lines 41–44).** For every n ≥ 4,
[`TabachnikovProblem2 n`](#/node/Discrete.TabachnikovProblem2) holds: every positive κ : ZMod n → ℝ that is constant
or has a [four-vertex window](#/node/Discrete.DFV) at some positive level c is
[realizable](#/node/Discrete.RealizesR2): there are edge lengths ℓ such that, walking the edges and turning by the
[turning angle](#/node/Discrete.turningAngle) at each vertex, you come back to the start after exactly one full turn,
and the resulting polygon is simple.

This is the engine behind all the radius headlines. The README calls it the "umbrella theorem" stating Problem 2
for every n ≥ 4.

### The method (paper §2)

The paper explains it like this. Write 2h_i for the length of edge i. A chord of length 2h in a circle of curvature
κ makes angle arcsin(κh) with the tangent, so for the circle through three consecutive vertices to have curvature
κ_i, the polygon must turn by arcsin(κ_i h_{i−1}) + arcsin(κ_i h_i) at vertex i. Closing up is three real
equations (two coordinates of the closure gap, and total turn 2π) in n unknowns.

1. **Constant runs.** Repeated adjacent values are deleted one at a time and later restored exactly
   ([constant-run reduction](#/node/Discrete.ConstantRun.nonempty_regularFourAnchor_of_adjacent_unequal_producer)).
2. **Four active edges.** Give length only to four edges; the others have length 0 and the vertices between collapse
   to points. The equations then involve only the eight curvature readings at the ends of those four edges. A
   positive solution where the derivative has full rank is a [regular four-edge anchor](#/node/Discrete.RegularFourAnchor).
3. **Choosing the edges.** A case split on where the maximum is
   ([anchor production](#/node/Discrete.nonempty_regularFourAnchor_of_adjacent_unequal_dfv)) always finds an anchor.
4. **Opening.** The implicit function theorem gives every zero-length edge a small positive length while keeping
   all curvatures. The result is a genuine realization.
""",
 [q("What does RealizesR2 κ ask for?", ["Edge lengths making the turning-angle development close up after one full turn, as a simple polygon", "A polygon inscribed in a circle", "A smooth closed curve"], 0,
    "Gluck/Discrete/Defs.lean lines 222–224."),
  q("Which words does TabachnikovProblem2 n cover?", ["Positive words that are constant or have a strict four-vertex window at a positive level", "All positive words", "Only words with distinct values"], 0,
    "`DiscreteFourVertexPos`, Gluck/Discrete/Converse.lean lines 42–43."),
  q("What is a regular four-edge anchor, informally?", ["A closed quadrilateral solution using only four edges, at which the closure equations have full rank", "A regular polygon", "A choice of four vertices on a circle"], 0,
    "Gluck/Discrete/RegularFourAnchor.lean lines 19–26."),
  q("Is this theorem conditional on any unproved 'stratum' hypothesis?", ["No. The older strata route in TabachnikovReduction.lean is not used", "Yes, on ZigzagRealizes"], 0,
    "Line 43 uses `tabachnikovProblem2_of_adjacent_unequal_regular_anchors` with the proved producer on line 44."),
 ],
 caveats=[NOT_BUILT,
  "The statement is in curvature/turning-angle language, not radii. Its connection to circumradii (circle through three consecutive vertices) is proved separately in TabachnikovConverse.lean.",
  "TabachnikovReduction.lean also contains an older, conditional route: theorems that assume three unproved 'stratum' hypotheses (`ZigzagRealizes`, `RunsRealizes`, `PlateauRealizes`). The file says so in capitals. Those are hypotheses, not axioms, and the headline does not use them."],
 widgets=walk("How the proof goes (Gluck/Discrete/TabachnikovFourActive.lean, lines 41-44, and what it calls)", [
  {"text": "Apply the reduction tabachnikovProblem2_of_adjacent_unequal_regular_anchors, which needs a regular-anchor producer for adjacent-unequal words (lines 43–44).",
   "lean": "tabachnikovProblem2_of_adjacent_unequal_regular_anchors"},
  {"text": "Constant words: the regular n-gon (Gluck/Discrete/RegularFourAnchorConverse.lean lines 29–30)."},
  {"text": "Window words: delete repeated adjacent readings by strong induction on n, find an anchor for the shorter word, and restore it (Gluck/Discrete/RegularFourAnchorConverse.lean lines 31–33).", "link": "Discrete.ConstantRun.nonempty_regularFourAnchor_of_adjacent_unequal_producer"},
  {"text": "The producer: global maximum repeated, or highest secondary peak plus flag case split (Gluck/Discrete/UniversalRegularFourAnchor.lean lines 118–136).", "link": "Discrete.nonempty_regularFourAnchor_of_adjacent_unequal_dfv"},
  {"text": "Open the anchor into a full realization by the implicit function theorem (Gluck/Discrete/RegularFourAnchorConverse.lean line 34).", "link": "Discrete.RegularFourAnchor",
   "lean": "exact A.realizesR2 hpositive"},
 ]))


node("Discrete.localContinuousRealization_of_dfv",
 "Headline: near any admissible word, the polygon can be chosen C¹ (Thm 7.1)",
 "Around every positive curvature word with a four-vertex window there is an open set of words and a C¹ rule assigning each word in it edge lengths, and hence a realizing simple polygon whose vertices also move C¹. So realizations can be chosen smoothly, but only locally.",
 r"""## Plain English

**Theorem (`localContinuousRealization_of_dfv`, Gluck/Discrete/LocalContinuity.lean lines 147–151; Theorem 7.1).**
Let κ₀ be positive with a [four-vertex window](#/node/Discrete.DFV). Then there is a
[local realization family](#/node/Discrete.LocalDiscreteRealizationFamily) around κ₀: an open set U of curvature
words containing κ₀, and a map κ ↦ ℓ(κ) that is C¹ on U, such that for every κ in U, κ is positive, the lengths are
moderate, the development closes with total turn 2π, the polygon is simple, and the vertex positions depend C¹ on κ.

In words: if you wiggle the prescribed curvatures a little, you can wiggle the polygon a little to match.

### How

The same [regular anchor](#/node/Discrete.RegularFourAnchor) that proves existence has a full-rank derivative.
Running the implicit-function argument with the curvatures as extra parameters (the project's
`ParametricPositiveSection` in ForMathlib) gives the C¹ family. The proof does not need the anchor *choice* to vary
continuously; one anchor at κ₀ suffices (`RegularFourAnchor.nonempty_localDiscreteRealizationFamily`, lines 129–143).

The [hexagon obstruction](#/node/Discrete.GlobalContinuity.no_continuous_regular_hexagon_path) shows this can't be
made global.
""",
 [q("Does this theorem cover constant words?", ["No: a strict window needs values on both sides of c", "Yes"], 0,
    "DFV needs κ values strictly above and below c (Gluck/Statements.lean lines 131–134); the file docstring says constant profiles are not covered."),
  q("What is chosen C¹ in κ?", ["The edge lengths, and with them the vertex positions", "Only the total turn", "The anchor's four edges"], 0,
    "`contDiffOn_lengths` and `contDiffOn_vertices`, Gluck/Statements.lean lines 326 and 332."),
  q("Does the family pass through a polygon you choose in advance?", ["Not claimed: it is the existence of some local choice", "Yes, any given realization"], 0,
    "The file docstring of LocalContinuity.lean says it 'does not assert passage through an arbitrary given polygon'."),
  q("Is n ≥ 4 an explicit hypothesis?", ["No, a four-vertex window already forces n ≥ 4", "Yes"], 0,
    "Only `hκ₀` and `hdfv` (lines 148–149); `DFV.four_le_period` is used elsewhere."),
 ],
 caveats=[NOT_BUILT,
  "The structure's conclusions are moderate arcs, closure, full turn and simplicity, i.e. RealizesR2 for each κ. Coherence and convexity follow from those by separate lemmas but are not fields of the structure.",
  "The output is phrased in curvatures, not radii; with r = 1/κ the same statement holds for radii since 1/x is smooth on positives, but the radius form is not stated separately."],
 widgets=walk("How the proof goes (Gluck/Discrete/LocalContinuity.lean, lines 147-151)", [
  {"text": "Get a regular four-edge anchor for κ₀ (line 150).", "link": "Discrete.RegularFourAnchor",
   "lean": "obtain ⟨A⟩ := nonempty_regularFourAnchor_of_dfv hκ₀ hdfv"},
  {"text": "Feed the anchor's surjective derivative to the parametric positive-section theorem: it opens dormant edges and corrects closure while κ varies (lines 129–143, line 151).",
   "lean": "exact A.nonempty_localDiscreteRealizationFamily hκ₀"},
  {"text": "Simplicity of each member comes from positive turning (line 121); C¹ vertices from smoothness of the development map (lines 123–125)."},
 ]))


node("Discrete.GlobalContinuity.no_continuous_regular_hexagon_path",
 "Headline: no continuous choice along a path of hexagon data (Thm 7.2)",
 "Each curvature word (14, 11, 10+3s, 5, 7−3s, 3), s ∈ [0,1], is realizable, but no continuous path of simple Dahlberg-regular hexagons realizes them all: 1/(smallest enclosing radius) would have to move continuously from ≤ 7 to ≥ 11 without ever equalling 9.",
 r"""## Plain English

**Theorem (`no_continuous_regular_hexagon_path`, Gluck/Discrete/GlobalContinuity/EnclosingCircleObstruction.lean
lines 253–261; Theorem 7.2).** There is **no** map s ↦ p(s) from [0, 1] to hexagons (ZMod 6 → ℂ), continuous on
[0, 1], such that for every s the hexagon p(s) is [simple](#/node/Discrete.IsSimplePolygon),
[Dahlberg-regular](#/node/Forward.DahlbergRegular), and has signed Menger curvature profile exactly
[`bandProfile s`](#/node/Discrete.GlobalContinuity.bandProfile) = (14, 11, 10 + 3s, 5, 7 − 3s, 3).

Each single word κ^s is admissible (its four-vertex window levels are the bands (5, 7−3s) ∪ (11, 10+3s), `bandProfile_dfv_iff`, Gluck/Discrete/GlobalContinuity/LevelBands.lean lines 42–67), so it *is* realized by some coherent hexagon (`bandProfile_pointwise_realizable`, lines 312–314). The problem is choosing
them continuously.

### The invariant: the smallest enclosing circle

Let R(p) be the radius of the smallest disk containing all six vertices. R is 1-Lipschitz in the vertices
(`enclosingRadius_lipschitz`, lines 52–60), so along a continuous path 1/R moves continuously. Then:

- at s = 0, 1/R ≤ 7 (lines 133–188);
- at s = 1, 1/R ≥ 11 (lines 190–226);
- for every s, 1/R ≠ 9 (lines 106–131).

The intermediate value theorem gives an s with 1/R = 9, a contradiction. Each bound comes from looking at which
vertices touch the enclosing circle: a contact vertex has curvature at least 1/R, and contacts confined to three
consecutive vertices force further inequalities that the specific numbers violate.
""",
 [q("Is each individual κ^s realizable?", ["Yes, each is admissible, so the converse applies; only a continuous choice fails", "No, that is the point", "Only at s = 0 and s = 1"], 0,
    "`bandProfile_pointwise_realizable`, Gluck/Discrete/GlobalContinuity/EnclosingCircleObstruction.lean lines 312–314."),
  q("Which quantity is used as the continuous invariant?", ["1 / (radius of the smallest enclosing disk)", "The perimeter", "The area"], 0,
    "`c s = 1 / enclosingRadius (p s)`, line 236."),
  q("Why is the value 9 special?", ["It lies between 7 and 11, and the hexagon data forbid 1/R = 9 for every s", "It is the average curvature", "It is 14 − 5"], 0,
    "`band_enclosing_level_ne_nine`, lines 106–131."),
  q("Is DahlbergRegular weaker or stronger than coherence?", ["Weaker (closed cone, collinear triples allowed), so ruling out regular paths is the stronger result", "Stronger"], 0,
    "Gluck/Statements.lean lines 366–372 vs. lines 190–199; coherence implies regularity (Gluck/Discrete/TabachnikovCharacterization.lean lines 25–41)."),
  q("Does the theorem forbid a discontinuous choice?", ["No, it only rules out a choice continuous on [0,1]", "Yes, any choice"], 0,
    "`ContinuousOn p (Set.Icc 0 1)`, line 254."),
 ],
 caveats=[NOT_BUILT,
  "The data are curvatures (signed Menger curvature = 1/circumradius), not radii. The equivalent radius path is (1/14, 1/11, …).",
  "Continuity is of the labelled vertex tuple in ℂ⁶ (sup distance). Positive orientation is derived from the positive profile rather than assumed (lines 259–261).",
  "The docstring of LevelBands.lean still says the level-band argument 'does not claim to refute global polygon selection'; that refers to the separate level-selection lemma in that file, not to this theorem."],
 widgets=walk("How the proof goes (Gluck/Discrete/GlobalContinuity/EnclosingCircleObstruction.lean, lines 230-261)", [
  {"text": "Reduce to the version that also assumes positive orientation; a positive Menger profile gives that orientation for free (lines 258–261)."},
  {"text": "Suppose p is such a path; set c(s) = 1 / enclosingRadius(p(s)) (lines 235–236).", "lean": "let c : ℝ → ℝ := fun s => 1 / enclosingRadius (p s)"},
  {"text": "c is continuous on [0,1]: the enclosing radius is 1-Lipschitz and positive for simple polygons (lines 237–241)."},
  {"text": "c(0) ≤ 7 and c(1) ≥ 11 (lines 244–245)."},
  {"text": "Intermediate value theorem: c(s) = 9 for some s (lines 246–247).", "lean": "obtain ⟨s, hs, heq⟩ := intermediate_value_Icc (by norm_num : (0 : ℝ) ≤ 1) hc"},
  {"text": "But 1/R = 9 is impossible for every band hexagon (lines 248–249)."},
 ]))


node("Discrete.SideTangent.realizesSideTangent_iff_admissible",
 "Headline: the side-tangent circle characterization (Corollary 8.6)",
 "For n ≥ 4, positive ρᵢ are the radii of the inward circles tangent to three consecutive side lines of a simple strictly convex polygon exactly when ρ is constant or its differences ρᵢ₋₁ − ρᵢ change sign four times. One half is Wegner's four-edge theorem; the other is new.",
 r"""## Plain English

**Theorem (`realizesSideTangent_iff_admissible`, Gluck/Discrete/SideTangentForward.lean lines 51–56;
Corollary 8.6).** For n ≥ 4 and any ρ : ZMod n → ℝ:

> ρ [is realized by side-tangent circles](#/node/Discrete.SideTangent.RealizesSideTangent)
> **if and only if** ρ is [side-tangent admissible](#/node/Discrete.SideTangent.SideTangentAdmissible): all ρᵢ > 0,
> and ρ is constant or the differences cᵢ = ρᵢ₋₁ − ρᵢ have four cyclic sign changes.

This is a second discrete curvature of a convex polygon. Instead of the circle through three consecutive
*vertices*, take, for each edge i, the circle on the inner side that is tangent to the lines of edges i−1, i and
i+1, touching edge i itself inside the edge.

- **⇒** (lines 54–55) is Wegner's four-edge theorem (`sideTangentForward`, lines 39–46), proved in the project.
- **⇐** (line 56) is the [side-tangent converse](#/node/Discrete.SideTangent.sideTangentConverse), Theorem 8.2.

Unlike the vertex-circle [characterization](#/node/Discrete.tabachnikov_radius_characterization), constants are
included on both sides here, so no "nonconstant" hypothesis is needed.
""",
 [q("Which circle does this theorem talk about?", ["The inward circle tangent to the lines of three consecutive edges", "The circle through three consecutive vertices", "The inscribed circle of the whole polygon"], 0,
    "`ThreeLineCircle`, Gluck/Statements.lean lines 410–412."),
  q("Why is no 'nonconstant' hypothesis needed here?", ["Constants are included in SideTangentAdmissible, and they are realized", "Constants can't be realized"], 0,
    "`(∃ r, ∀ i, ρ i = r) ∨ …`, Gluck/Statements.lean line 433."),
  q("What does 'four sign changes' mean for ρ = (1, 2, 1, 2)?", ["Differences are −1, +1, −1, +1 cyclically: four sign changes, so admissible", "Not admissible"], 0,
    "`DFV (radiusDifference ρ) 0`, Gluck/Statements.lean lines 393 and 433."),
  q("Which direction is Wegner's theorem?", ["Realized ⇒ admissible", "Admissible ⇒ realized"], 0,
    "`sideTangentForward`, Gluck/Discrete/SideTangentForward.lean lines 39–46."),
 ],
 caveats=[NOT_BUILT,
  "The neighbouring tangency points may lie on extensions of the neighbouring edges; only the central contact must be inside its edge (paper Definition 8.1). The circle need not lie inside the polygon."],
 widgets=walk("How the proof goes (Gluck/Discrete/SideTangentForward.lean, lines 51-56)", [
  {"text": "⇒: from a realization (P, N, C) build a strictly convex polygon circumscribed about the unit circle whose vertices, weighted by the differences cᵢ, balance to zero (line 42)."},
  {"text": "A balanced combination of the vertices of such a polygon either has all coefficients zero (ρ constant) or the coefficients change sign four times (lines 44–46)."},
  {"text": "⇐: the side-tangent converse (line 56).", "link": "Discrete.SideTangent.sideTangentConverse",
   "lean": "· exact sideTangentConverse hn ρ"},
 ]))


node("Discrete.SideTangent.sideTangentConverse",
 "The side-tangent converse (Theorem 8.2)",
 "Every admissible positive ρ (constant, or four sign changes in its differences) is realized exactly by a simple strictly convex polygon's inward three-line circles. The construction rescales the edges of a polygon circumscribed about the unit circle, unrelated to the four-edge method.",
 r"""## Plain English

**Theorem (`sideTangentConverse`, Gluck/Discrete/SideTangentConverse.lean lines 126–131; Theorem 8.2).** For n ≥ 4,
if ρ is [admissible](#/node/Discrete.SideTangent.SideTangentAdmissible) then it
[is realized by side-tangent circles](#/node/Discrete.SideTangent.RealizesSideTangent).

### The construction (paper §8)

Start from a strictly convex polygon Y circumscribed about the unit circle, chosen so that the vertices weighted by
cᵢ = ρᵢ₋₁ − ρᵢ sum to zero. Four sign changes are exactly what make such a balanced polygon exist
(`exists_sideTangent_scaledPolygon`, Gluck/Discrete/SideTangentScaledPolygon.lean lines 301–328, which uses the
project's projective-balance and winding-number lemmas in ForMathlib). Scaling the edges by ρ then closes up and
gives the required polygon P, and the three-line circle equations hold with radius ρᵢ, uniquely.

For constant ρ the balance is automatic, and a regular tangential polygon works (lines 112–122).
""",
 [q("What does the construction start from?", ["A polygon circumscribed about the unit circle, balanced by the differences", "A regular four-edge anchor", "A circle packing"], 0,
    "`exists_sideTangent_scaledPolygon` (Gluck/Discrete/SideTangentScaledPolygon.lean lines 301–328)."),
  q("Is the circle at each edge uniquely determined?", ["Yes, the realization includes a uniqueness field", "No"], 0,
    "`unique_circle`, Gluck/Statements.lean line 424."),
  q("How are constant ρ handled?", ["By a regular strict tangential fan; the balance condition holds trivially", "They are excluded"], 0,
    "`sideTangentConverse_of_const`, lines 112–122."),
 ],
 caveats=[NOT_BUILT],
 widgets=walk("How the proof goes (Gluck/Discrete/SideTangentConverse.lean, lines 126-131)", [
  {"text": "Split the admissibility hypothesis into positivity and constant-or-sign-changes (line 128)."},
  {"text": "Constant: regular tangential polygon, trivially balanced, then scale (lines 129–130, using lines 112–122)."},
  {"text": "Four sign changes: balanced circumscribed polygon, then scale (line 131, using lines 106–109).",
   "lean": "· exact sideTangentConverse_of_dfv ρ hρ hdfv"},
 ]))
