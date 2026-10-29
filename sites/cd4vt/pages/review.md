# Review: do the statements say what they claim?

This page compares each headline's Lean statement with the README and the paper. Nothing here was checked by
building the Lean. All six are **complete** in the source: the project has no `sorry` and no `axiom`. None is
conditional on an unproved hypothesis.

## tabachnikov_converse_geometric (Theorem 1.1): faithful, with the plateau reading made explicit

- **Claim:** every positive cyclic sequence with at least two local maxima and two local minima (n ≥ 4) is the
  circumradius sequence of a coherent convex polygon.
- **Statement:** exactly this. "Local maximum" is read *plateau-aware*: a flat run with strictly lower neighbours
  counts once, and two maxima must be disjoint runs. The README says "with extrema counted as plateaus". This is
  Dahlberg's convention and the natural sharp form. Tabachnikov's original phrasing doesn't fix a convention for
  repeated values.
- **"Convex"** is strict convexity with counterclockwise orientation (every vertex strictly left of every
  non-incident edge), plus simplicity. **"Coherent"** uses the *open* vertex cone, which is the strongest reasonable
  reading.
- **Radii** are measured as the distance from the closed-form circumcentre to the middle vertex. That is the true
  circumradius because coherence excludes collinear triples.
- The stronger [collated form](#/node/Discrete.tabachnikov_converse) also gives Tabachnikov's non-degeneracy (no four
  consecutive concyclic vertices) when neighbouring radii differ.

## tabachnikov_radius_characterization (Corollary 1.2): faithful

An iff for **nonconstant** positive data. The nonconstant hypothesis is necessary: constants are realized by the
regular polygon but have no strict extrema. The forward direction uses the project's own proof of Dahlberg's
theorem, which needs only simplicity, Dahlberg regularity (implied by coherence) and non-concyclicity.

## tabachnikovProblem2_all: faithful, in curvature language

- `TabachnikovProblem2 n` is stated with curvatures and turning angles, not radii: positive words that are constant
  or have a strict four-vertex window at a positive level are realizable as closed simple developments.
- The project proves the hypothesis class equals "constant or two plateau maxima and two plateau minima"
  (`discreteFourVertexPos_iff_extrema`), so it is not a weaker proxy.
- **Possible confusion.** The same file keeps an older reduction to three "stratum" hypotheses whose docstrings say
  "NOT discharged … open research". They are not used by this theorem (see
  [the leftovers node](#/node/Discrete.RunsRealizes)). Those docstrings now read as stale, because the main theorem
  implies all three strata.

## localContinuousRealization_of_dfv (Theorem 7.1): faithful, phrased in curvatures

- Gives an open neighbourhood and a C¹ choice of edge lengths with C¹ vertices, for every positive word with a
  four-vertex window. Constant words are not covered, as the paper says ("near every nonconstant admissible
  sequence").
- The family's fields are closure, full turn, moderate arcs and simplicity. Coherence and convexity of each member
  follow from separate lemmas but are not packaged in the structure.
- The paper states the radius version. The Lean is in curvature coordinates; since r ↦ 1/r is smooth on positive
  numbers, the two are equivalent, but the radius version isn't written out.

## no_continuous_regular_hexagon_path (Theorem 7.2): faithful, and slightly stronger than the paper's wording

- The paper's Theorem 7.2 forbids a continuous path of *coherent convex* hexagons realizing κ^s. The Lean forbids
  continuous paths of *simple, Dahlberg-regular* hexagons with signed Menger profile κ^s. Dahlberg regularity (closed
  cone, collinear triples allowed) is weaker than coherence, and convexity isn't assumed, so the Lean statement
  excludes more paths.
- Pointwise realizability of every κ^s is proved separately (`bandProfile_pointwise_realizable`), so the
  obstruction is really to continuous selection.
- Continuity is of labelled vertex tuples. A path that relabels vertices continuously isn't a separate case, since
  labels are part of the data.

## realizesSideTangent_iff_admissible (Corollary 8.6): faithful

- "Admissible" = positive and constant, or four cyclic sign changes of the differences ρᵢ₋₁ − ρᵢ, with zeros
  allowed. Constants are on both sides, so no nonconstant hypothesis is needed.
- The realization notion is demanding: unit outward normals, supporting lines, a *unique* three-line circle at
  each edge, and the central contact in the open edge. The neighbouring contacts may lie on edge extensions, as in
  the paper's definition.
- The forward half is Wegner's theorem, proved in the project (`sideTangentForward`).

## Anything surprising?

- **Comparator.** The README describes a [Comparator](https://github.com/leanprover/comparator) setup
  (`Challenge.lean`, `Solution.lean`, `comparator.json`). It checks that the library proves exactly the six
  statements of `Challenge.lean`, with the definitions copied verbatim from Gluck/Statements.lean, using only the
  three standard axioms, under three kernels. That is a strong statement-faithfulness guarantee *if run*. It was not
  run for this site.
- A few docstrings refer to files or names that don't exist at this commit (for example `gluck_converse_flow` in
  `Gluck/Euclidean/SpaceFormInstance.lean`). They don't affect any headline.
