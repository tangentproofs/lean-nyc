# Trust: what was and wasn't checked

## Not built

**The Lean was not built for this site.** No `lake`, `lean` or `elan` was run. When we say something "is proved" or
"complete", we only mean that the source contains what looks like a complete proof with no `sorry`. It does not mean
we saw Lean's kernel accept it. The project targets Lean `v4.35.0-rc3` with Mathlib `v4.35.0-rc3` (lean-toolchain,
README).

The README states two checks you can run yourself:
- `lake env lean scripts/axioms.lean` prints the axioms of the six paper theorems and of `tabachnikovProblem2_all`.
  The README says each depends only on `propext`, `Classical.choice` and `Quot.sound`.
- `scripts/verify-comparator.sh` runs [Comparator](https://github.com/leanprover/comparator): it checks that the
  library proves exactly the statements in `Challenge.lean` (whose definitions are copied verbatim from
  Gluck/Statements.lean), with only those three axioms, under three kernels.

We ran neither. We have only the README's report of their results.

## Gaps, axioms and escape hatches

A whole-word text search of every `.lean` file at the pinned commit for `sorry`, `admit`, `axiom`, `native_decide`,
`implemented_by`, `extern` and `opaque` finds:

| What | In the library (Gluck/, ForMathlib/) | Elsewhere |
|---|---|---|
| `sorry` | 0 | 6 in Challenge.lean, deliberately: it states the six theorems with `sorry` for Comparator to compare against |
| `admit` | 0 as a tactic (one occurrence of the English word in a docstring) | 0 |
| `axiom` | 0 declarations (the word appears once in prose, Gluck/Euclidean/Reduction.lean line 35) | 0 |
| `native_decide` | 0 | 0 |
| `implemented_by` / `extern` / `opaque` | 0 | 0 |

The library root Gluck.lean imports Gluck.Discrete, and every Gluck/ and ForMathlib/ file is reachable from the
default build targets (`Gluck`, `ForMathlib`, `Challenge`, `Solution` in lakefile.toml).

**Hypotheses that look like gaps but aren't used.** Gluck/Discrete/TabachnikovReduction.lean defines three
propositions (`RunsRealizes`, `PlateauRealizes`, and `ZigzagRealizes` in ZigzagWords.lean) whose docstrings say
"NOT discharged". A few theorems in that file take them as hypotheses. None of the headlines uses them
([details](#/node/Discrete.RunsRealizes)).

## Declarations

All 4,349 declarations were found by scanning the source text (`extracted: false`), not from a compiled build. So
some dependency links are missing or wrong. For example, the field name `radius_pos` of `IsSideTangentRealization`
is linked to the unrelated top-level lemma `Gluck.radius_pos`, and dot-notation uses (`A.realizesR2`,
`hv.2.2.dahlbergRegular`) aren't linked. The node texts give the real dependencies by hand.

## The explanations

Every explanation, quiz and caveat on this site was written by an AI (Claude) from the public source, README and
paper. None has been reviewed by a human or by the project's author. All nodes are marked `review: draft`. The
anchor constructions and the forward (Dahlberg) proof are summarised from the paper's description, not checked line
by line against the Lean.
