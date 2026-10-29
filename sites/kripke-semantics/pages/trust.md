# Trust: what was and wasn't checked

## Not built

**The Lean was not compiled for this site.** No `lake`, `lean` or `elan` was run. "Proved" here means "the file
contains a complete-looking proof", not "the kernel accepted it". The repository has no `lean-toolchain` file;
its `lakefile.toml` requires Mathlib at tag `v4.29.0` and Subverso at `main`. There is no CI configuration in
the repository.

**One line looks suspicious.** Beth/Coverage.lean line 33 (in `pullback`) appears to use a name that is not
bound anywhere. If it is an error, Beth/Coverage.lean and everything importing it (the whole Beth half,
including both Beth headlines) would fail to build at this commit. The Kripke half does not import it. This
is a reading of the text only; it may be wrong.

## Searches of the source (all `.lean` files)

| Searched for | Found |
|---|---|
| `sorry`, `admit` | **0** |
| `axiom` declarations | **0** |
| `native_decide` | **0** |
| `implemented_by`, `extern`, `opaque` | **0** |
| Classical reasoning | `open Classical` at Kripke/Completeness.lean line 7; Zorn's lemma at line 210; `Classical.choose` / `Classical.choice` in Beth/BethTrees.lean lines 111, 115 and 184–186; `by_cases` / `by_contra` on propositions in several proofs |

The classical uses are ordinary Mathlib reasoning (the standard axioms `propext`, `Classical.choice`,
`Quot.sound`), not new axioms. They matter only in that none of the completeness proofs is constructive.

## Declarations scanned from text

All 148 declarations were extracted by a text scanner (`extracted: false`), not by Lean. Their dependency
edges are approximate. Examples: the statements of the headlines mention `Pf`, `Ctxt` and `Tm` through an
opened namespace, and the scanner misses those; it also links the soundness proofs to the alias `Semantics`
(Kripke/Soundness.lean line 5) because of a namespace with the same name; and it mistook a structure field named
`covers` for the top-level `Beth.covers`, which this site corrects for the build. Line references were checked
to lie inside the files at the pinned commit.

## Explanations

All prose, summaries, walkthroughs and quizzes were **written by an AI (Claude) and have not been reviewed** by
the project's author or by a human. Every node is marked `review: draft`. The project has no licence file, so no
Lean source is reproduced here; each claim links to the exact lines on GitHub, and those lines are the ground
truth.
