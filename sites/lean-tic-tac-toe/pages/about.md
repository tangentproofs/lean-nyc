# About this site

## The project

[Ericson2314/lean-tic-tac-toe](https://github.com/Ericson2314/lean-tic-tac-toe) is a small Lean 4 program by
**John Ericson** that plays tic-tac-toe in the terminal. All the commits are from early September 2024, on Lean
4.10 with Batteries. In the README's words, tic-tac-toe is "a game of a square matrix over 3 states", and the
project's interest is in the fixed-length array, which the README calls the "Fibonacci" of dependent types: an
array whose length is part of its type. Squares are then arrays of arrays whose inner arrays all have the same
length.

**This is a program, not a theorem library.** The README is explicit: "Nothing interesting is prooved, but the
code is failure-free". The program may not terminate, for example if you keep typing invalid numbers, but it
never errors and has no implicit failures.

## What the Lean covers

The code is layered the way the README describes:

1. **Vectors** (TicTacToe/Vector.lean): [Vector](#/node/Vector), an array carrying a proof of its length, with
   safe [lookup](#/node/Vector.get), [map](#/node/Vector.functor), [construction from a function](#/node/Vector.ofFn)
   and [one-entry update](#/node/Vector.modifyM).
2. **Grids** (TicTacToe/Grid.lean): [Grid](#/node/Grid), a vector of vectors of the same length, with
   [lookup](#/node/Grid.get), [update](#/node/Grid.modifyM), [constant grids](#/node/Grid.mkGrid) and
   [transpose](#/node/Grid.transpose).
3. **The game** (TicTacToe.lean): [players](#/node/Player), [cells](#/node/CellState), the
   [board](#/node/Board), [moves](#/node/Board.move) and [win detection](#/node/gameDone), on boards of any size
   *n*×*n*.
4. **The terminal frontend** (Main.lean): [main](#/node/main) and its input loops.
5. **One lemma** (TicTacToe/Lemma.lean): [movesAreValid](#/node/movesAreValid), which says a successful move fills
   exactly one empty square. It is **unfinished (sorry)**.
6. **Tests** (TicTacToe/Test.lean): eight `#eval` lines. One prints the empty 2×2 board, and seven compare a move or a win check with an expected answer. They print
   true or false when the file is compiled. They are not proofs.

## Where to start

Read [Vector](#/node/Vector) and [Vector.get](#/node/Vector.get) to see where the "no failure" comes from. Then
read [Board.move](#/node/Board.move), [gameDone](#/node/gameDone) and [main](#/node/main). Finish with
[movesAreValid](#/node/movesAreValid) to see what the project set out to prove and where it stopped.

## What this site leaves out

The `zipWith` helpers for vectors and grids (TicTacToe/Vector.lean lines 25–38, TicTacToe/Grid.lean lines 22–30)
and the grid's `Functor` instance (TicTacToe/Grid.lean lines 16–19) are defined but not used by the game, so they
get no nodes. The small printing helpers `printRow` and `playerToChar` are covered under
[printBoard](#/node/printBoard), and `Vector.mkVector` under [Grid.mkGrid](#/node/Grid.mkGrid).

The repository has **no licence file**, so this site quotes none of its code. Everything here is a paraphrase,
with links to the exact lines on GitHub.
