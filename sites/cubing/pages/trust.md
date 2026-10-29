# Trust: what was and wasn't checked

## Not built

**The Lean was not compiled for this site.** No `lake`, `lean` or `elan` was run. "Proved" here means "the file
contains a complete-looking proof", not "the kernel accepted it". The upstream project says its CI builds with
`--wfail` and treats the theorems as its tests, but this site did not verify that. The toolchain is pinned to a
release candidate (`leanprover/lean4:v4.29.0-rc4`, using the experimental module system) with Mathlib resolved
to a fixed `master` commit in `lake-manifest.json`.

## Searches of the source (library `Cubing/` plus the root files)

| Searched for | Found |
|---|---|
| `sorry`, `admit` | **0** |
| `axiom` declarations | **0**. The word appears only in CubingAudit.lean and CubingResults.lean comments and `#print axioms` checks. |
| `native_decide` | **0** uses. CubingResults.lean (lines 1–8) is reserved for it and is empty. |
| `implemented_by`, `extern`, `opaque` | **0** |
| `decide +kernel` | 5 uses: Cube3x3/Invariants.lean lines 163 and 168, Cube3x3/Facelets.lean lines 276, 281 and 343. These are kernel-checked brute-force evaluations over finite types. |
| raised `maxRecDepth` | Cube3x3/Notation.lean lines 212, 216 and 220; Cube3x3/Solvable.lean line 102. These are for evaluating long move sequences by `rfl`, which is sound. |

The upstream **axiom audit** (CubingAudit.lean lines 13–43) pins `reachable_eq_valid`, `card_reachable`,
`card_valid`, `toStickers_injective`, `colors_corner`, `colors_edge`, `Facelet.cubie_normal_injective` and
`colors_move_mul` to exactly `propext`, `Classical.choice` and `Quot.sound`. That is a strong signal if the
upstream build passes, but again it was not run here.

## Declarations scanned from text

All 134 declarations on this site were extracted by a text scanner (`extracted: false`), not by Lean. Their
dependency edges are approximate. For example, `open` namespaces can hide some dependencies, such as those of
`invariants` on `OPerm.parity` and `OPerm.twistSum`. Line references were checked to lie inside the files at
the pinned commit.

## Explanations

All prose, summaries, walkthroughs and quizzes were **written by an AI (Claude) and have not been reviewed** by
the project's author or by a human. Every node is marked `review: draft`. The project has no licence file,
so no Lean source is reproduced here; each claim links to the exact lines on GitHub, and those lines are the
ground truth.
