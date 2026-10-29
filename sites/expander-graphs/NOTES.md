# NOTES for the coordinator: expander-graphs

Not published. Written by Claude, working autonomously.

## Time spent

About 1.5 hours of session time: reading all 6 Lean files and the blueprint, writing 39 nodes and 3 pages, and
iterating on the build.

## What I did / decisions I made

- **Authors.** `site.json` had "Celio Boulay". The file headers of ExpanderGraphs/chapter1.lean and chapter2.lean say
  "Authors: Celio Boulay, Dylan Sparrow, Rafael Castro", and git history has one commit by Dylan Sparrow. I set
  `authors` to "Celio Boulay, with Dylan Sparrow and Rafael Castro" and left `members` alone. The README names no one.
  Revert if you prefer the hub to list only the member.
- **Licence.** There is a LICENSE file (Apache-2.0), consistent with the file headers. Unchanged.
- **Headlines (6):** `expander_mixing_lemma`, `eigval_eq_one_unique`, `SimpleGraph.chromaticNumber_le_maxDegree_add_one'`,
  `UnweightedGraph.zero_mem_lapSpectrum`, `UnweightedGraph.connected_non_empty_edge_boundary` (all complete) and
  `UnweightedGraph.Isoperimetry.two_cheeger_ge_eigval_1` (PARTIAL, sorry). I included the sorry'd Cheeger bound
  because it is the project's stated direction, and it is where the most important review finding sits.
- **Left out** of node coverage: WeightedGraph.lean (unused by anything else), `S`/`LSS`, `LapOperator`, `gG`/`cheegerV`,
  `vertexBoundary`. They are mentioned in neighbouring nodes and on the About page.
- **ns** left empty, because ids from three namespaces would collide (`degree`, `vol`, `lapEigvals` exist in both
  `UnweightedGraph` and `WeightedGraph`).

## Hardest parts

- Deciding how to present the Chung chapters honestly. They are a mix of proved basics, sorry'd key lemmas, and (I
  believe) statements that are false as written. I wanted that to be clear without sounding dismissive of a work in
  progress.
- Working out the iInf-over-Prop issue (below) and making sure it really makes the definitions degenerate.

## Places I am least sure of (please check these)

1. **`UnweightedGraph.Isoperimetry.cheeger` "is always 0"** (also stated in the `lead`, the review, the
   `two_cheeger_ge_eigval_1` node and `lapEigvals_one_eq_inf_rayleigh`). Reasoning: `⨅ S, ⨅ (_ : p S), f S` in ℝ. For
   S = ∅, `p` is false, the inner iInf is over an empty type, and `Real.sInf_empty`/`Real.iInf_of_isEmpty` give 0. Every
   other value is ≥ 0, so the outer iInf is 0. I am fairly confident (this is a well-known trap), but it wasn't checked
   by Lean. If I'm wrong, the lead, the cheeger node, the Cheeger headline, the Rayleigh node, the review and the trust
   page all need edits.
2. **The `[OfNat (Fin (Fintype.card α)) 1]` instance hypotheses** (ExpanderGraphs/chapter1.lean line 361,
   chapter2.lean line 119). I claim that `lapEigvals 1` then uses the assumed instance, which can be any index. I am less
   sure here: it depends on Lean preferring local instances, which I believe it does. I've hedged it everywhere
   ("as we read it").
3. **`first_eigval_eq_0` false for a double edge** (review page). ℒ for two vertices joined by two parallel edges: degrees
   2, off-diagonal −1/√4 = −1/2, eigenvalues 1/2 and 3/2. I believe that is right given the definitions (one adjacency
   entry regardless of multiplicity), but I didn't check it mechanically.
4. **`LSS` needs `IsSimple`**: my reading of the definitions of `S` and ℒ. It is hedged in the node.
5. **`connected_non_empty_edge_boundary` and `hβ`**: I hinted that Mathlib's `Graph` might make `hβ` unnecessary
   (`IsLink` should imply the edge is in `edgeSet`). This is only in the review page, and hedged.
6. In `lapEigvals_one_eq_inf_rayleigh`, `G.lapEigvals 1` appears *before* the OfNat variables (line 290). I assumed the
   global `Fin` numeral instance via `NeZero (Fintype.card α)` from `[Nonempty α]`. I didn't verify which instance
   Mathlib provides.

## Things the author might object to

- The headline "Cheeger constant, as currently defined, is 0 for every graph" in the `lead` is prominent for a WIP
  project. I kept it because it is the most useful thing a reader or the author can learn here, and I phrased it as
  "by our reading" with an easy fix. You may want to soften it or move it off the home page.
- Calling `two_cheeger_ge_eigval_1`, `connected_iff_cheeger_pos` and `lapEigvals_one_eq_inf_rayleigh` "false as written".
- Pointing out docstring mismatches (`lapEigvals` "non-increasing", `DirichletSum` "unordered pairs",
  `eigval_sum_eq_n_iff_no_isolation` only one direction).
- Listing Dylan Sparrow and Rafael Castro as co-authors on the hub, if the member prefers otherwise.

## Engine issues (not fixed; I did not touch engine/)

- **Lower-case file names aren't linked.** `srcrefs.mjs` requires the final path segment to start with a capital
  letter, so `ExpanderGraphs/chapter1.lean lines …` and `ExpanderGraphs/chapter2.lean …` are not linked and their
  ranges are **not range-checked** by the build. I checked those line numbers by hand against the pinned commit.
- **Scanner false dependency:** the variable name `S` (a `Set α`) is resolved to the def `UnweightedGraph.S`, causing
  "meaning-dependency 'UnweightedGraph.S' has no explainer" warnings on several nodes. Dot-notation uses
  (`G.lapSpectrum`, `G.edgeBoundary`) are missed.
- **Page routes:** the router knows `#/review`, `#/trust` and `#/about`, not `#/page/<name>`. I first wrote `#/page/review` and fixed it. The authoring brief could mention this.
