# Trust: what was and wasn't checked

## Not built

**The Lean was not built for this site.** No `lake`, `lean` or `elan` was run. When we say something "is proved",
we only mean that the source file contains what looks like a complete proof, not that Lean's kernel accepted it.
The program was not run either, so behaviour described here (such as the draw-case loop) comes from reading the
code.

## Gaps, axioms and escape hatches

A text search of all the `.lean` files at the pinned commit for `sorry`, `admit`, `axiom`, `native_decide`,
`implemented_by`, `extern` and `opaque` finds:

| What | Count | Where |
|---|---|---|
| `sorry` | 1 | TicTacToe/Lemma.lean line 16: the whole substance of [movesAreValid](#/node/movesAreValid) |
| `admit` | 0 | |
| `axiom` | 0 | |
| `native_decide` | 0 | |
| `implemented_by` / `extern` / `opaque` | 0 | |

Also: `getNumber`, `getCoord`, `getMove` and `main` are `partial` definitions (Main.lean lines 19, 34, 39, 52).
Lean accepts these without a termination proof, and you can't reason about them inside Lean. That is normal for
interactive IO loops.

The `sorry`'d file TicTacToe/Lemma.lean is not imported by the library root or by Main.lean, so it doesn't affect
the program.

## Declarations

All 33 declarations were found by scanning the source text (`extracted: false`), not from a compiled build. Some
dependency links can be missing as a result. For example, the scan doesn't see that `Board.move` uses
`Grid.modifyM`, because it is called with dot notation. The node texts state those dependencies by hand.

## The explanations

Every explanation, quiz and caveat on this site was written by an AI (Claude) from the public source. None has
been reviewed by a human or by the project's author. All nodes are marked `review: draft`.
