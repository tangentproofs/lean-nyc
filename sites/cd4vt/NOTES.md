# NOTES for the coordinator (cd4vt)

## Time

About 1.5–2 hours of agent time: reading the README, the paper's method/continuity/side-tangent sections, the
statement file and the headline proofs; writing 32 nodes and 3 pages; build iterations (schema fixes for title and
summary lengths and the 3-question quiz minimum).

## Decisions I made (and why)

- **Headlines (6).** The README lists six paper theorems and also names the umbrella theorem
  `tabachnikovProblem2_all`. The task allowed 4–7 headlines, but AUTHORING.md caps them at 6. So I headlined
  Thm 1.1, Cor 1.2, `tabachnikovProblem2_all`, Thm 7.1, Thm 7.2 and Cor 8.6. Thm 8.2 (`sideTangentConverse`) is a
  full node with its own walkthrough, but not a headline. Cor 8.6 already contains it as one direction. This swap is
  stated on the About page.
- **Roots** = `Gluck`, `ForMathlib` (everything reachable from the default targets). `Challenge.lean` /
  `Solution.lean` are left out of the scan: Challenge is a verbatim copy of the statements with `sorry`, and would
  have produced duplicate ids.
- **ns** = `Gluck.`, so ids look like `Discrete.tabachnikov_converse_geometric`, and the smooth theorem is just
  `gluck_converse`.
- **Grouped nodes.** About 48k lines of anchor constructions are one node
  (`Discrete.nonempty_regularFourAnchor_of_adjacent_unequal_dfv`). The Dahlberg forward proof (~27k lines) is one
  node, ForMathlib is one node (`poincare_miranda`), the smooth converse is one node (`gluck_converse`), and the old
  strata route is one node (`Discrete.RunsRealizes`). Small definitions are folded into the node of their main
  user: `circumcenterR2`/`vertexCone` into CoherentR2, `heading`/`vertexR2`/`closureGap`/`turningSum`/`polygonR2`
  into turningAngle, `sK`/`cK`/`tK` into ModerateArc and turningAngle, `signedMengerR2`/`SignedMengerProfile` into
  crossR2, the side-tangent sub-structures into their parents. That leaves 34 "no explainer" warnings, all of them
  for these folded names.
- **Authors/licence:** unchanged. The README, LICENSE (Apache-2.0) and formalization.yaml all name Kristoffer
  Josefsson. Source headers say "Authors: kejace" (his GitHub handle).

## What was hard

- Size: 83k lines and 4,349 declarations. I relied on the README's table, `Challenge.lean`, Gluck/Statements.lean and
  the paper's own "method" section to find the spine, and read the headline proofs and their direct callers. I did
  not read the anchor constructions or the Dahlberg proof in Lean.
- Two languages: the paper states things with radii, while most of the Lean works with curvatures and turning
  angles. I had to keep track of which headline is in which language.

## Where I'm least sure (concrete)

1. **`Discrete.nonempty_regularFourAnchor_of_adjacent_unequal_dfv`.** The descriptions of cases R / F / N (which
   frame, "first transition", "orthogonal quadrilateral", IVT vs Poincaré–Miranda) are paraphrased from
   paper/tabachnikov/method.tex. I checked only the top-level case split in UniversalRegularFourAnchor.lean
   lines 118–136 and lines 68–95, not the sub-constructions.
2. **`Discrete.RegularFourAnchor`.** "Controller = closure gap of the quadrilateral plus (total turn − 2π)" comes from
   reading `Frame.controller` (FourActiveSlotEmbedding.lean lines 212–217) and its docstrings. The exact role of
   the `start`/`finish` readings, and the claim that "only the eight end readings enter", rest on
   `controller_eq_of_endpoints` and the paper.
3. **`Discrete.SideTangent.realizesSideTangent_iff_admissible` walkthrough, ⇒ direction.** "Balanced circumscribed
   polygon ⇒ zero or four sign changes" is my reading of the names `exists_strict_balanced_polygon_of_realization` /
   `zero_or_dfv_of_strict_affine_balance` plus the paper. I didn't read those proofs.
4. **`Discrete.GlobalContinuity.no_continuous_regular_hexagon_path`.** The informal "contact vertex has curvature
   ≥ 1/R" gloss summarises lemma names (`signedMengerProfile_inv_radius_le_of_minimal_boundary_of_cross_pos`,
   `curvature_le_level_of_contacts_in_triple`). The direction of the inequality is as the proof uses it, but I
   didn't read those lemmas.
5. **`Forward.dahlberg_discrete_four_vertex_E2`.** The "disk arguments" description of the forward proof is
   high-level, based on file and theorem names (Lemma 5 containing disks, Lemma 7, Lemma 9 bridge).
6. **`gluck_converse`.** I didn't check what `RealizesCurvature` means exactly (the docstring says it is intrinsic,
   for a C¹ curve).
7. **Review claim** that Lean's Theorem 7.2 is *stronger* than the paper's wording (Dahlberg-regular + simple vs.
   coherent convex). I'm confident regular is weaker than coherent (there is a lemma) and that convexity isn't
   assumed. Whether the author would call it "stronger" or just "the formal form" is a matter of taste.

## Things the author might object to

- Calling the strata docstrings in TabachnikovReduction.lean ("NOT discharged … open research") **stale**. They are
  accurate about that route but could mislead, and I say so on the Trust/Review pages and in the RunsRealizes node.
- Pointing out docstrings that refer to things missing at this commit: `gluck_converse_flow` /
  `Gluck/Euclidean/SpaceFormInstance.lean` (FourVertex.lean docstring); the LevelBands.lean header "does not claim
  to refute global polygon selection" (now refuted, in the separate file).
- Not headlining Theorem 8.2.
- Summarising ~75k lines of construction and forward proof in a few grouped nodes.

## Engine notes

- AUTHORING.md says files in `nodes_src/` starting with `_` are helpers, but `engine/tools/write_nodes.py` loads
  every `.py` (including `_*.py`) and reads `m.NODES` from it, and doesn't put `nodes_src` on `sys.path`. So a helper
  module can't be imported, and a `_helper.py` without `NODES` would crash the build. I worked around this by
  defining `node`/`q`/`walk` in each node file.
- The scanner links the structure field `radius_pos` (in `IsSideTangentRealization`) to the unrelated top-level
  lemma `Gluck.radius_pos` (Curvature.lean), so `gluck_converse`-side names show up as meaning-dependencies of the
  side-tangent nodes. I mention this on the Trust page.
