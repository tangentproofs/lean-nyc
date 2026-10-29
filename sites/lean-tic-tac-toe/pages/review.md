# Review: do the statements say what they claim?

This project makes only one formal claim, the lemma [movesAreValid](#/node/movesAreValid). Its other "results"
are definitions and a program, so this review asks whether each one does what its name and the README suggest.
Nothing below was checked by running or building the code.

## movesAreValid: PARTIAL (sorry)

- **Claim (by name):** moves produced by `Board.move` are valid.
- **Statement:** if a move succeeds, the new board differs from the old one by exactly one square, which was
  empty and now holds the mover's mark ([BoardTransition](#/node/BoardTransition)). That is a faithful
  formalisation of "valid move", restricted to the board. It doesn't cover turn order or whether the game was
  already over.
- **Proof:** it gives the witnesses (*x*, *y*) and then `sorry` (TicTacToe/Lemma.lean line 16). **Not proved.**
- **Oddity:** the success hypothesis is an implicit argument in curly braces (TicTacToe/Lemma.lean line 14), so
  Lean can't fill it in automatically. This makes the lemma awkward to use, but doesn't change its meaning.
- **Plausibility:** we believe the statement is true. A proof would need facts about reading an array right
  after setting one entry.

## Board.move

Faithful to "place a mark on an empty square, or fail". It does not check whose turn it is. That is left to
`main`. Off-board coordinates are excluded by the types (`Fin n`), not by a runtime check.

## gameDone

Faithful to the usual tic-tac-toe win on *n*×*n* boards: some full row, column or long diagonal for one player.
Two things are worth knowing:

- **There is no draw outcome.** A full board with no line looks the same as an unfinished game.
- On a board larger than 3×3, a win needs a full line of *n*, not three in a row.

## main and the "failure-free" claim

The README claims the program "will never error" and makes no claim that it terminates. That matches the code:

- every cell lookup carries an in-range proof ([Vector.get](#/node/Vector.get));
- bad input of every kind gets a "try again" prompt;
- the input loops are `partial`, so Lean doesn't require them to terminate.

**Surprising:** a drawn game doesn't end. Once the board is full with no winner, `gameDone` says "no winner",
so the loop asks for another move, and every move is rejected because all squares are taken. The program keeps
prompting until it is interrupted. That is consistent with the README's no-termination caveat, but a reader
might not expect it.

**Also worth knowing:** the first coordinate the player types (the prompt calls it *x*) chooses the printed
**row**, and the second chooses the position along it. That is the matrix convention, not the x-across,
y-down screen convention.

## Tests

The `#eval` lines in TicTacToe/Test.lean compare results with `=` and print the answer. A wrong answer would
print `false` without failing anything, so they are spot checks for whoever reads the build output, not
verification.
