# NOTES for the coordinator (lean-tic-tac-toe)

## Time spent
About 45 minutes, including reading the whole repo (about 470 lines), writing 27 nodes and 3 pages, and build iterations.

## Calls I made
- **Headlines:** `Board.move`, `gameDone`, `main`, `movesAreValid`. The repo has one theorem, and it is sorry'd.
  The README says the point is the program and its "failure-free" typing, so three of the headlines are
  definitions. Their walkthroughs are titled "How the definition works / How the program goes" and outline the
  code rather than a proof.
- **Roots:** `TicTacToe.lean`, `TicTacToe/` (which includes Test.lean, but it has no declarations) and `Main.lean`.
  I left out the lakefile.
- **No licence:** no Lean code blocks, no verbatim statements, and no `lean:` walkthrough fields. Everything is
  paraphrased. The README states no licence either, so there was nothing to escalate.
- **No nodes** for the unused `Vector.zipWith`, `Grid.zipWith` and the grid `Functor` instance (`instance_16`), or
  for the tiny `printRow`, `playerToChar` and `Vector.mkVector`. These are mentioned in the text and on the About page.
  The remaining build warnings are about those three tiny helpers.
- **Authors:** "John Ericson", as in site.json. The git history agrees, and the README names no one else.

## What was hard
- Saying honestly that there is "nothing proved" while still giving every headline a walkthrough.
- Working out the coordinate convention: the first coordinate is the printed row. I confirmed it from the
  Test.lean expected boards (lines 24–45).

## Least sure about (concrete)
- **movesAreValid / trust.md:** I claim TicTacToe/Lemma.lean is *not built* by `lake build`, so the sorry doesn't
  touch the executable. This relies on Lake's default `lean_lib` globs being just the root module, and on
  Lemma.lean not being imported by TicTacToe.lean or Main.lean. The imports are certain. The Lake default is from
  memory.
- **main / getMove, the draw-case infinite loop:** this comes from reading the code. I didn't run the program. I'm
  fairly confident, since `gameDone` has no draw value and `getMove` loops until a move succeeds.
- **movesAreValid, the "implicit hypothesis is awkward to use" remark:** this is right about elaboration in general.
  A named argument `(eval := h)` works. I described this as "awkward", not "unusable".
- **gameDone, laziness via `Option.orElse`:** I said later checks aren't run once a winner is found. That holds
  if `Option.orElse` in Lean 4.10 takes its fallback as a thunk, which the code relies on (the tests are
  `Unit → Option Player`). The *result* is first-some-wins either way.
- **Vector:** I said this project-local `Vector` is not core's or Batteries'. At Lean 4.10 / Batteries v4.10,
  Batteries' vector was namespaced, I believe. If the coordinator ever builds the project on newer Lean, the
  top-level name would clash with core `Vector`. That doesn't matter at the pinned toolchain.

## Things the author might object to
- The headline **"A drawn game never ends"** (summary of `main`, and review.md) reads as a criticism. It's
  phrased as consistent with the README's own non-termination caveat.
- Labelling the coordinate convention "the matrix convention, not the screen convention" in review.md.
- Calling the tests "spot checks, not verification".

## Engine notes
No engine bugs hit. The source scan misses `Board.move` → `Grid.modifyM`, because it is called with dot notation
on a field (`b.grid.modifyM`). The node text links it by hand, and trust.md mentions it.
