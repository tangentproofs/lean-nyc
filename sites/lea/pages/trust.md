# Trust: what was and wasn't checked

## Not built

**The Lean was not built for this site.** No `lake`, `lean` or `elan` was run, and neither was SafeVerify
or its test runner. "Proved" on this site means the file contains what looks like a complete proof, not that
Lean's kernel accepted it.

## Gaps, axioms and escape hatches

A text search of all 33 `.lean` files at the pinned commit for `sorry`, `admit`, `axiom`, `native_decide`,
`implemented_by`, `extern` and `opaque` finds:

| What | Count | Where |
|---|---|---|
| `sorry` in the sample proofs (`examples/`) | 0 | |
| `sorry` in SafeVerify targets | 9, all deliberate | each `SafeVerifyTest/*/Target.lean` states the problem with `sorry`, which is how a target is meant to look (for example SafeVerifyTest/AddFalse/Target.lean line 1) |
| `sorry` in retry-test fixtures | 4, all deliberate | [helper-baseline.lean lines 10 and 17](https://github.com/VIDA-NYU/Lea/blob/a5924f6f15b980452731b6edfe00feee97791ab4/docs/reformalization-testing-guide/fixtures/helper-baseline.lean#L9-L17), [shared-baseline.lean lines 11 and 15](https://github.com/VIDA-NYU/Lea/blob/a5924f6f15b980452731b6edfe00feee97791ab4/docs/reformalization-testing-guide/fixtures/shared-baseline.lean#L9-L15) |
| `admit` | 0 | |
| `axiom` declarations | 0 | the word appears only as field and variable names in SafeVerify |
| `native_decide` | 0 | |
| `implemented_by` | 1, deliberate | the SafeVerify fixture SafeVerifyTest/ImpBy/Maybe.lean line 3, which shows a proof about a value whose compiled code returns something else |
| `extern` | 0 | |
| `opaque` | 0 as a keyword | appears in SafeVerify only as the name of a kind of constant it compares |

Three SafeVerify fixtures **deliberately** tamper with Lean's environment (SafeVerifyTest/AddFalse/Bad.lean,
SafeVerifyTest/AddFalseConstr/Bad.lean, SafeVerifyTest/ReplaceAxiom/Bad.lean). They are attacks the checker
should reject, not results.

SafeVerify's own code uses `partial def` for some helper functions (for example SafeVerify/Main.lean lines 80–105).
That is ordinary for programs, and those functions prove nothing.

## Dependencies

- Mathlib v4.29.0 for the proof workspace and for SafeVerify. Among the sample proofs, only examples/StackMachine.lean
  imports Mathlib. Ackermann.lean and Logic.lean import nothing.
- SafeVerify is vendored from upstream commit 241dfb0, according to
  [third_party/README.md](https://github.com/VIDA-NYU/Lea/blob/a5924f6f15b980452731b6edfe00feee97791ab4/apps/lea-standalone/prover/third_party/README.md). That README also says the copy
  was pinned down to Lean v4.28.0, but the copy's `lean-toolchain` and `lakefile.lean` say v4.29.0. The note
  looks out of date. One Lea commit (46b7bbc) changed the copy, adding the single-declaration option.

## Declarations

All declarations were found by scanning the source text (`extracted: false`), not from a compiled build, so some
dependency links can be missing or wrong. Two scanner artefacts on this site:

- examples/Logic.lean and examples/StackMachine.lean each define an `eval`. The scanner names the second one
  [eval'](#/node/eval'). The files never import each other, so Lean has no clash.
- The SafeVerify test fixtures repeat names across files (`falseThm`, `efsq`, …). The primed copies are the
  target versions.

## The explanations

Every explanation, quiz and caveat on this site was written by an AI (Claude) from the public source. None has
been reviewed by a human or by the project's authors. All nodes are marked `review: draft`.
