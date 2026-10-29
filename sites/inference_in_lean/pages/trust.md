# Trust: what was and wasn't checked

## Not built

**The Lean was not built for this site.** No `lake`, `lean` or `elan` was run. When we say something "is proved" or
"complete", we only mean that the source file contains what looks like a complete proof with no `sorry`, not that
Lean's kernel accepted it. The project targets Lean `v4.34.0-rc2` with Mathlib at the same tag (lean-toolchain,
lakefile.lean).

The library root InferenceInLean.lean imports only F_Resolution.lean (and through it A–E). So a default `lake build`
would compile A–F but not G_Examples.lean or the Exercises folder. We can't say whether those two compile.

## Gaps, axioms and escape hatches

A text search of all the `.lean` files at the pinned commit (including Exercises) for `sorry`, `admit`, `axiom`,
`native_decide`, `implemented_by`, `extern` and `opaque` finds:

| What | Count | Where |
|---|---|---|
| `sorry` | 1 | InferenceInLean/D_Unification.lean line 63 (forward direction of `unifiable_iff_mgu_idempot`) |
| `admit` | 0 | |
| `axiom` | 0 | |
| `native_decide` | 0 | |
| `implemented_by` / `extern` / `opaque` | 0 | |

The one `sorry` is not used by any other declaration: the resolution rules take the mgu as a hypothesis. Many proofs
end with `aesop` or `simp_all`, which are ordinary (kernel-checked) tactics, but whether they succeed can only be known
by building.

## Declarations

All declarations were found by scanning the source text (`extracted: false`), not from a compiled build. Some
dependency links are therefore missing or wrong: the scanner misses uses written with dot notation and the Lean
coercion from clauses to formulas, and the locally redefined `∘` and `≤` notations aren't linked to
`Substitution.compose` and `MoreGeneral`. The node texts give the real dependencies by hand.

## The explanations

Every explanation, quiz and caveat on this site was written by an AI (Claude) from the public source and README.
None has been reviewed by a human or by the project's authors. All nodes are marked `review: draft`.
