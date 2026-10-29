# Trust: what was and wasn't checked

## Not built

**The Lean was not built for this site.** No `lake`, `lean` or `elan` was run. When we say something "is proved" or
"complete", we only mean that the source file contains what looks like a complete proof with no `sorry`, not that
Lean's kernel accepted it. The project targets Lean `v4.31.0-rc1` with Mathlib (lean-toolchain).

## Gaps, axioms and escape hatches

A text search of all the `.lean` files at the pinned commit for `sorry`, `admit`, `axiom`, `native_decide`,
`implemented_by`, `extern` and `opaque` finds:

| What | Count | Where |
|---|---|---|
| `sorry` | 9 | ExpanderGraphs/chapter1.lean lines 249 (`LSS`), 294 (`lapEigvals_one_eq_inf_rayleigh`), 444 (`first_eigval_eq_0`), 452 (`second_eigval_le_div`); ExpanderGraphs/chapter2.lean lines 116 (`connected_iff_cheeger_pos`), 123 (`two_cheeger_ge_eigval_1`), 127 (`cheeger_lower_bound`), 138 (inside `hG_le_gG`), 150 (`two_cheegerV_ge_first_eigval`) |
| `admit` | 0 | (the only match is the word "admits" in a comment, ExpanderGraphs/Coloring.lean line 19) |
| `axiom` | 0 | |
| `native_decide` | 0 | |
| `implemented_by` / `extern` / `opaque` | 0 | |

**No sorries in:** ExpanderGraphs/EML.lean (the mixing lemma), ExpanderGraphs/Coloring.lean,
ExpanderGraphs/Connectivity.lean and ExpanderGraphs/WeightedGraph.lean. The proved chapter 1 results used here
(`zero_mem_lapSpectrum`, `zero_eigenvalue_normalized`, `LapHermitian`, the eigenvalue-sum lemmas) don't depend on
any of the sorried lemmas, as far as we could see. `cheeger_le_cheegerV` does depend on the sorry in `hG_le_gG`.

**Statements that look false as written** (our analysis, not machine-checked): `two_cheeger_ge_eigval_1`,
`connected_iff_cheeger_pos` and `lapEigvals_one_eq_inf_rayleigh`, because of how the infimum is written. See the
[review](#/review).

## Declarations

All 105 declarations were found by scanning the source text (`extracted: false`), not from a compiled build. Some
dependency links are therefore missing or wrong. The scanner misses uses written with dot notation such as
`G.lapSpectrum`. It also takes the variable name `S` (a vertex set) for the boundary matrix `UnweightedGraph.S`. The
node texts give the real dependencies by hand.

The engine only turns file references into links when the file name starts with a capital letter, so references to
ExpanderGraphs/chapter1.lean and ExpanderGraphs/chapter2.lean appear as plain text. Their line numbers were checked by
hand.

## The explanations

Every explanation, quiz and caveat on this site was written by an AI (Claude) from the public source and blueprint.
None has been reviewed by a human or by the project's authors. All nodes are marked `review: draft`.
