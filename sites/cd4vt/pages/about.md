# About this site

## The project

[kejace/cd4vt](https://github.com/kejace/cd4vt) is a paper together with a Lean 4 + Mathlib formalization by
**Kristoffer Josefsson** (README; `formalization.yaml` lists him as author and maintainer). The paper is "A converse
to the discrete four-vertex theorem" (source in `paper/`, website <https://kejace.github.io/cd4vt/>). In the README's
words, it answers "Tabachnikov's Problem 2
([arXiv:0710.5902](https://arxiv.org/abs/0710.5902))":

> Every cyclic sequence of positive numbers `r₁, …, rₙ` (`n ≥ 4`) with at least two local maxima and two local
> minima, with extrema counted as plateaus, is the sequence of radii of the circles through consecutive vertex
> triples of a convex polygon whose circumcenters lie inside the corresponding vertex angles.

The README and paper also credit the earlier work this builds on: S. Tabachnikov (who posed the problem),
B. Dahlberg (the discrete four-vertex theorem, which gives the reverse direction) and B. Wegner (the four-edge
theorem for side-tangent circles). The paper and the formalization were developed together, and the paper's Lean
appendix displays the formal statements.

The Lean library is called `Gluck` because it grew out of a formalization of Gluck's smooth converse four-vertex
theorem, which is also in the repository ([side result](#/node/gluck_converse)).

## What the Lean covers

The six headlines are the six theorems that the README lists, and that `Challenge.lean` restates for the
[Comparator](https://github.com/leanprover/comparator) check, with one swap: this site uses the umbrella theorem
[`tabachnikovProblem2_all`](#/node/Discrete.tabachnikovProblem2_all) as a headline in place of Theorem 8.2
(the side-tangent converse, covered in [its own node](#/node/Discrete.SideTangent.sideTangentConverse)). The site
format allows at most six headlines, and the umbrella theorem is what the radius results rest on.

| Paper | Node |
|---|---|
| Theorem 1.1 (realization) | [tabachnikov_converse_geometric](#/node/Discrete.tabachnikov_converse_geometric) |
| Corollary 1.2 (characterization) | [tabachnikov_radius_characterization](#/node/Discrete.tabachnikov_radius_characterization) |
| Problem 2 for every n ≥ 4 | [tabachnikovProblem2_all](#/node/Discrete.tabachnikovProblem2_all) |
| Theorem 7.1 (local C¹) | [localContinuousRealization_of_dfv](#/node/Discrete.localContinuousRealization_of_dfv) |
| Theorem 7.2 (no global choice) | [no_continuous_regular_hexagon_path](#/node/Discrete.GlobalContinuity.no_continuous_regular_hexagon_path) |
| Theorem 8.2 (side-tangent converse) | [sideTangentConverse](#/node/Discrete.SideTangent.sideTangentConverse) |
| Corollary 8.6 (side-tangent iff) | [realizesSideTangent_iff_admissible](#/node/Discrete.SideTangent.realizesSideTangent_iff_admissible) |

**The spine.** Radii r become curvatures κ = 1/r. A curvature word becomes a polygon-drawing recipe through
[turning angles](#/node/Discrete.turningAngle), and [realizability](#/node/Discrete.RealizesR2) means that the recipe
closes up after one turn. The existence proof puts all length on four edges
([regular anchor](#/node/Discrete.RegularFourAnchor)),
[finds such an anchor](#/node/Discrete.nonempty_regularFourAnchor_of_adjacent_unequal_dfv) after
[removing repeated readings](#/node/Discrete.ConstantRun.nonempty_regularFourAnchor_of_adjacent_unequal_producer), and
opens the other edges by the implicit function theorem. The reverse direction is
[Dahlberg's theorem](#/node/Forward.dahlberg_discrete_four_vertex_E2).

**The statement vocabulary** is in Gluck/Statements.lean, which `Challenge.lean` repeats verbatim:
[plateau extrema](#/node/Discrete.PlateauMaxRun), [two max / two min](#/node/Discrete.IsPlateauTwoMaxTwoMin),
[four-vertex windows](#/node/Discrete.DFV), [signed area and Menger curvature](#/node/Discrete.crossR2),
[coherence](#/node/Discrete.CoherentR2), [circumradius](#/node/Discrete.vertexCircumradius),
[simple](#/node/Discrete.IsSimplePolygon) and [coherent convex](#/node/Discrete.IsCoherentConvexPolygon) polygons,
[moderate arcs](#/node/Discrete.ModerateArc), the [local family](#/node/Discrete.LocalDiscreteRealizationFamily),
the [hexagon path](#/node/Discrete.GlobalContinuity.bandProfile), [Dahlberg regularity](#/node/Forward.DahlbergRegular),
and the side-tangent notions ([realization](#/node/Discrete.SideTangent.RealizesSideTangent),
[admissibility](#/node/Discrete.SideTangent.SideTangentAdmissible)).

## What this site leaves out

The library is about 83,000 lines in 188 files, and this site explains a few dozen declarations out of about 4,300.
Summarised in grouped nodes, but not explained line by line:

- the individual anchor constructions (repeated maximum, first transition, orthogonal / negative-corner cases),
  their rank computations and sign tables: most of Gluck/Discrete;
- the proof of Dahlberg's theorem, Gluck/Forward (about 27,000 lines);
- the side-tangent construction (balanced circumscribed polygons, projective balance);
- the smooth converse four-vertex theorem and its space-form generalisations (Gluck/*.lean, Gluck/Euclidean,
  Gluck/SpaceForm);
- the [general tools in ForMathlib](#/node/poincare_miranda);
- an [older conditional route](#/node/Discrete.RunsRealizes) kept in TabachnikovReduction.lean.

## Where to start

Read [Theorem 1.1](#/node/Discrete.tabachnikov_converse_geometric), then
[Corollary 1.2](#/node/Discrete.tabachnikov_radius_characterization), then the
[Problem 2 node](#/node/Discrete.tabachnikovProblem2_all) for how the proof works. The paper's "The method" section
(paper/tabachnikov/method.tex) is a two-page overview that this site follows closely.
