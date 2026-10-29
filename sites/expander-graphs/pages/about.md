# About this site

## The project

[celioboulay/expander-graphs](https://github.com/celioboulay/expander-graphs) is a Lean 4 + Mathlib project by
**Celio Boulay**. The headers of the two Chung chapters (ExpanderGraphs/chapter1.lean and ExpanderGraphs/chapter2.lean)
also credit **Dylan Sparrow** and **Rafael Castro**. In the README's words, the goal is "to formalize Expander Graphs
and related Spectral Graph Theory results". The project has a LaTeX
[blueprint](https://celioboulay.github.io/expander-graphs/) that follows Fan Chung's *Spectral Graph Theory* (AMS, 1992)
for the general theory, and Swastik Kopparty's 2018 Rutgers lecture notes (scribed by Danny Scheinerman and Harsha
Tirumala) for the expander mixing lemma.

**It is a work in progress.** One file has a finished main theorem, the mixing lemma. The Chung chapters have proved
foundations, but several of the statements that matter most are still `sorry`.

## What the Lean covers

The source is about 1,340 lines in six files under ExpanderGraphs/:

1. **The expander mixing lemma** (ExpanderGraphs/EML.lean, about 390 lines, **complete**). This uses Mathlib's
   `SimpleGraph`. It defines the [normalised adjacency matrix](#/node/norm_adj_matrix), proves that the eigenvalue 1
   is [simple on connected regular graphs](#/node/eigval_eq_one_unique) by a maximum principle, defines
   [γ-expanders](#/node/expander), and proves the [mixing lemma](#/node/expander_mixing_lemma).
2. **Greedy colouring** (ExpanderGraphs/Coloring.lean, **complete**). It proves
   [χ(G) ≤ Δ(G) + 1](#/node/SimpleGraph.chromaticNumber_le_maxDegree_add_one') for finite simple graphs. It is
   independent of the rest of the project.
3. **Chung, chapter 1** (ExpanderGraphs/chapter1.lean, **partial**). This introduces a multigraph type
   [UnweightedGraph](#/node/UnweightedGraph), the [degree](#/node/UnweightedGraph.degree) and
   [volume](#/node/UnweightedGraph.vol), the [normalised Laplacian](#/node/UnweightedGraph.Laplacian) ℒ and several
   equivalent forms of it, its [symmetry](#/node/UnweightedGraph.LapHermitian), its ordered
   [eigenvalues](#/node/UnweightedGraph.lapEigvals), and the fact that
   [0 is always an eigenvalue](#/node/UnweightedGraph.zero_mem_lapSpectrum). Still open: ℒ = SSᵀ, λ₀ = 0,
   λ₁ ≤ n/(n−1), and the [Rayleigh characterisation of λ₁](#/node/UnweightedGraph.lapEigvals_one_eq_inf_rayleigh).
4. **Connectivity** (ExpanderGraphs/Connectivity.lean, **complete**). [Walks](#/node/UnweightedGraph.Walk),
   [connectedness](#/node/UnweightedGraph.Connected), the [edge boundary](#/node/UnweightedGraph.edgeBoundary), and
   [every proper vertex set of a connected graph has a boundary edge](#/node/UnweightedGraph.connected_non_empty_edge_boundary).
5. **Chung, chapter 2: isoperimetry** (ExpanderGraphs/chapter2.lean, **mostly unfinished**). The
   [Cheeger ratio](#/node/UnweightedGraph.Isoperimetry.hG) and [constant](#/node/UnweightedGraph.Isoperimetry.cheeger),
   and the statement of the [easy half of Cheeger's inequality](#/node/UnweightedGraph.Isoperimetry.two_cheeger_ge_eigval_1),
   which is sorry'd. The definition of the Cheeger constant needs a fix first; see the [review](#/review).
6. **Weighted graphs** (ExpanderGraphs/WeightedGraph.lean). A separate `WeightedGraph` type with weighted degrees and
   a weighted normalised Laplacian, proved symmetric. Nothing else uses it yet, so this site doesn't explain it node
   by node.

The two halves of the project don't connect yet. The mixing lemma is about Mathlib's `SimpleGraph` and the adjacency
matrix *A*/*d*. The Chung chapters are about the `UnweightedGraph` multigraph and ℒ. `LapOfRegGraph` (ℒ = I − A/k for
regular graphs) is where the two would meet.

## Where to start

Read the [mixing lemma](#/node/expander_mixing_lemma) and its walkthrough first, then the two definitions it rests
on, [expander](#/node/expander) and [eigval_eq_one_unique](#/node/eigval_eq_one_unique). For the spectral graph
theory side, start at the [normalised Laplacian](#/node/UnweightedGraph.Laplacian) and
[zero_mem_lapSpectrum](#/node/UnweightedGraph.zero_mem_lapSpectrum). Then read the
[Cheeger constant](#/node/UnweightedGraph.Isoperimetry.cheeger) node to see where the project is heading and what
has to change on the way.

## What this site leaves out

The site has no nodes for the weighted-graph file, the boundary matrix `S`, the operator form `LapOperator`, or the
vertex-boundary variants `gG` and `cheegerV`. They are mentioned in the nodes nearest to them. All of them are
listed in the source browser.
