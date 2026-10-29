# Review: do the statements say what they claim?

This page compares each headline's Lean statement with what its name, docstring or the blueprint claims. Nothing
here was checked by building the Lean. Where we say a statement is false as written, that is our reading of
Mathlib's conventions, and the author should confirm it.

## expander_mixing_lemma: complete, faithful

- **Claim:** for a connected *d*-regular γ-expander on *n* vertices, |e(A,B) − (d/n)|A||B|| ≤ γ d √(|A||B|).
- **Statement:** exactly that, for Mathlib `SimpleGraph`s, arbitrary (possibly overlapping) vertex sets *A*, *B*, and
  e(A,B) counting ordered pairs ([e_AB](#/node/e_AB)). Hypotheses: *d* ≥ 1, *d*-regular, connected, γ ≥ 0.
- **The expander definition** ([expander](#/node/expander)) excludes eigenvalues by value ("≠ 1"). Together with
  connectivity and [eigval_eq_one_unique](#/node/eigval_eq_one_unique), this excludes exactly the trivial eigenvalue, so
  the hypothesis is the usual two-sided spectral expansion with λ = max over i ≥ 2 of |λᵢ|. It is not weakened.
- **Proof:** complete in the source and follows the blueprint step by step. The handling of the top eigenvector as
  "a constant *c* with *n c*² = 1" is neat and avoids square roots.

## eigval_eq_one_unique: complete, faithful

It says the eigenvalue 1 of *A*/*d* has multiplicity one on a connected regular graph, stated as "two eigenbasis
indices with eigenvalue 1 are equal". The maximum-principle proof (`eq_const_of_mulVec_eq`) is the standard one.

## chromaticNumber_le_maxDegree_add_one': complete, faithful

The statement is χ(G) ≤ Δ(G) + 1 for finite simple graphs, with Mathlib's `chromaticNumber` and `maxDegree`. The
general form with any *d* ≥ Δ is also proved. Mathlib may already have a similar bound. We didn't check, and it
doesn't affect correctness.

## zero_mem_lapSpectrum: complete, faithful (as a set statement)

It says 0 is an eigenvalue of the normalised Laplacian of a nonempty, simple, loopless graph. That matches Chung's
"λ₀ = 0" in the weak sense of membership in the spectrum. It doesn't show that 0 is the *smallest* eigenvalue or
anything about its multiplicity. The proof is neat: it covers the edgeless case by noting that ℒ would be the zero
matrix.

## connected_non_empty_edge_boundary: complete, faithful

A connected graph has a boundary edge for every nonempty proper vertex set. It assumes `hβ` (every element of the
edge type is an edge). Mathlib's `Graph` may make that unnecessary, but it is harmless.

## two_cheeger_ge_eigval_1: PARTIAL (sorry), and not true as written

- **Claim:** Chung's Lemma 2.1, λ₁ ≤ 2 h_G.
- **Proof:** `sorry`.
- **Statement problem 1, the Cheeger constant is always 0.** The definition
  `⨅ (S : Set α) (_ : 0 < min (G.vol S) (G.vol Sᶜ)), hG S` (ExpanderGraphs/chapter2.lean lines 76–77) is an infimum of
  real numbers with the condition as an extra binder. In Mathlib, an infimum of reals over an empty index (a false
  condition) is `sInf ∅ = 0`. So *S* = ∅ contributes the value 0, and since every h_G(*S*) ≥ 0, `cheeger G = 0` for every
  graph. The statement then says λ₁ ≤ 0, which is false for K₂ (λ₁ = 2). The same applies to `cheegerV` and makes
  `connected_iff_cheeger_pos` (sorry) false as written. Usual fixes: take the infimum over the subtype
  `{S // 0 < min …}`, or use `sInf` of an image set.
- **Statement problem 2, the meaning of the numerals.** Line 119 of ExpanderGraphs/chapter2.lean, and line 361 of
  ExpanderGraphs/chapter1.lean, add `[OfNat (Fin (Fintype.card α)) 0] [OfNat (Fin (Fintype.card α)) 1]` as instance
  *hypotheses*. As we understand Lean's instance resolution, `G.lapEigvals 1` then uses whatever index that assumed
  instance gives, which need not be the second one. If it picked the last index, the "λ₁" in these statements would be
  the largest eigenvalue. Using Lean's own `Fin` numerals (which need `NeZero (Fintype.card α)`) would avoid this. We
  are less sure of this point than of problem 1.
- **Connectivity:** Chung states Lemma 2.1 for connected graphs. The Lean has no such hypothesis, but on paper none is
  needed (both sides are 0 for disconnected graphs).

## Other sorry'd or surprising statements

- **lapEigvals_one_eq_inf_rayleigh** (ExpanderGraphs/chapter1.lean lines 289–294, sorry): the same ⨅-over-a-condition
  pattern, so the right-hand side is 0 for every graph (take *f* = 0, which fails "*f* ≠ 0"). As written it claims
  λ₁ = 0 for every simple loopless graph, which is false for K₂.
- **first_eigval_eq_0** (lines 441–444, sorry): it has no simple/loopless hypothesis. We believe it is false as stated
  for some multigraphs. Two vertices joined by two parallel edges give ℒ = [[1, −½], [−½, 1]], with eigenvalues ½ and 3/2,
  so neither is 0. It also uses the assumed `OfNat` instance for "0".
- **second_eigval_le_div** (lines 447–452, sorry): λ₁ ≤ n/(n−1). This is true on paper for the standard index, but it
  depends on the numeral issue above.
- **LSS** (line 249, sorry): ℒ = SSᵀ. We believe it needs `IsSimple`, because with parallel edges SSᵀ counts each one.
- **eigval_sum_eq_n_iff_no_isolation** (lines 399–408): it proves only "no isolation ⇒ the sum is *n*", despite "iff"
  in the name.
- **cheeger_lower_bound** and **two_cheegerV_ge_first_eigval** (ExpanderGraphs/chapter2.lean lines 127 and 150) are
  placeholders stated as `True := sorry`. They say nothing yet.
- **hG_le_gG** (lines 131–139): its key inequality step is `sorry` (line 138). So `cheeger_le_cheegerV`, which uses it,
  depends on a sorry as well.
- **Docstrings:** `lapEigvals` says "non-increasing order", but `eigval_order` proves the order is increasing.
  `DirichletSum` says "unordered pairs", but the sum is over ordered pairs; the 1/2 in the Rayleigh formula compensates.

## What the project does not (yet) have

Cheeger's inequality itself, the relationship between λ₁ and connectivity, the spectrum of *A*/*d* lying in [−1, 1],
and a bridge between the `SimpleGraph` mixing lemma and the `UnweightedGraph` Laplacian theory.
