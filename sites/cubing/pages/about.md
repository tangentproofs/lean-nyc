# About this project

**[rdavison/cubing](https://github.com/rdavison/cubing)** by Richard Davison is, in its README's words, "an
interactive cubing reference and trainer, formalised in Lean 4". The Lean library doubles as the chapters of a
[Verso](https://github.com/leanprover/verso) book: every definition is Lean, every claim is a theorem, and every
cube diagram in the book is computed from the formal model when the site is built.

## What the Lean covers (at the pinned commit)

The first part, which is everything in the library so far, builds the 3x3x3 cube group and proves its
fundamental theorem. Seven files under `Cubing/Cube3x3/`, in reading order:

1. **Basic.lean.** Corner and edge slots, and the generic orientation-permutation group (a semidirect
   product from Mathlib). A cube state is a corner state paired with an edge state. Start at [Cube](#/node/Cube).
2. **Moves.lean.** The six face turns as explicit tables, and the [reachable](#/node/reachable) subgroup they
   generate.
3. **Notation.lean.** Singmaster notation (R, U', F2, …) as [move sequences](#/node/alg), plus order
   checks on the tables.
4. **Invariants.lean.** Twist, flip and parity; the [valid](#/node/valid) subgroup; the easy direction
   [reachable ⊆ valid](#/node/reachable_le_valid); and the count [card_valid](#/node/card_valid).
5. **Generate.lean.** The abstract [generation lemma](#/node/OPerm.SetUp.le): set-up moves, one 3-cycle and
   one pair twist generate everything with zero twist and even permutation.
6. **Solvable.lean.** Concrete [algorithms](#/node/twoCornerTwist) (T-perm, A-perm, U-perm, …) feed the lemma,
   giving the headline [reachable_eq_valid](#/node/reachable_eq_valid) and
   [card_reachable](#/node/card_reachable) = 43,252,003,274,489,856,000.
7. **Facelets.lean.** The link to real stickers and colours: the piece model is
   [faithful](#/node/toStickers_injective), and the turns are
   [the geometric rotations they look like](#/node/colors_move_mul).

## What this site leaves out

- The **book** (`book/`, about 590 lines of Verso and widget code that renders the chapters and draws cubes).
  It contains no mathematics of its own.
- `CubingImpl` (a stub with one placeholder function), `CubingResults` (empty; reserved for any future
  `native_decide` results), `CubingDoc` (validates cube diagrams in the docs) and `Main.lean` (prints a net).
- Smaller lemmas, notation plumbing (`parseAlg?`, `renderAlg`, token readers) and the vector helpers. They are
  linked from the nodes that use them.

The README describes the longer-term plan: treat solving methods (especially blindfolded methods) as
programs, prove them correct, and compare them by number of algorithms, moves and memorisation. **None of that is
in the repository at this commit**; only the cube group and its fundamental theorem are.

## Where to start

Read [Cube](#/node/Cube) → [move](#/node/move) → [valid](#/node/valid) → [reachable_eq_valid](#/node/reachable_eq_valid).
If you know some group theory, the [generation lemma](#/node/OPerm.SetUp.le) is the mathematical heart. The
upstream repository's book is the authoritative, author-written explanation, with interactive cube pictures.
