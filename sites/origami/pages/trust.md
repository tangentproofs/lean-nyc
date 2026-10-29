# Trust: what was and wasn't checked

## Not built

**The Lean was not built for this site.** No `lake`, `lean` or `elan` was run. When this site says something "is
proved", it only means the source file contains what looks like a complete proof and that no `sorry` appears in the
project, not that Lean's kernel accepted it. The project pins Lean v4.32.1 and Mathlib v4.32.1 (lean-toolchain,
lakefile.toml).

## Gaps, axioms and escape hatches

A text search of all `.lean` files at the pinned commit for `sorry`, `admit`, `axiom`, `native_decide`,
`implemented_by`, `extern` and `opaque` finds:

| What | Count | Where |
|---|---|---|
| `sorry` | 0 | |
| `admit` | 0 | |
| `axiom` (declarations) | 7 + 2 | Origami/lightweight_definitions/Haga.lean lines 10–15 and 20 (generated: points `p1`–`p5`, line `l1`, hypothesis `hyp1`); Haga.lean lines 50–51 (hand-added: `p1_coords`, `p2_coords`) |
| `native_decide` | 0 | |
| `implemented_by` / `extern` | 0 | |
| `opaque` (declarations) | 0 | the word appears only in comments (Haga.lean lines 18 and 44) |

**What the axioms affect.** Only declarations in Haga.lean that mention the postulated points use them:
[haga_construction](#/node/haga_construction), [haga_fold_exists](#/node/haga_fold_exists) and
[haga_result](#/node/haga_result). The Huzita theorems, the sharpness results, and the two Haga headlines
[haga_first_theorem](#/node/haga_first_theorem) and [haga_gen_equation](#/node/haga_gen_equation) do not mention them.
The axioms are jointly satisfiable (take the points at their commented coordinates), so they cannot introduce a
contradiction.

**Automation used.** Proofs rely on standard Mathlib tactics (`linear_combination`, `nlinarith`, `field_simp`,
`positivity`, `grind`). The Haga proofs use `grind` and `simp` for the coordinate computations; whether these succeed
can only be confirmed by building.

## Declarations

All declarations were found by scanning the source text (`extracted: false`), not from a compiled build, so some
dependency links may be missing or wrong. Known effects:

- Lean `axiom` declarations are not picked up by the scanner, so `p1`, `p2`, `hyp1`, `p1_coords`, `p2_coords` have no
  pages and are linked by line number.
- The Haga theorems begin their statements with local `let` definitions; the scanner cuts their statements short, so
  their "mentions" lists are incomplete.
- Only `Origami.lean` and `Origami/lightweight_definitions/` were scanned. `Origami/paper_folding/` was left out (see
  the About page).

## The explanations

The explanations on this site were written by an AI assistant from the source text and have not been reviewed by the
project's authors. The repository has no licence file, so this site quotes no Lean source: statements are paraphrased
and every reference links to the exact lines on GitHub at the pinned commit.
