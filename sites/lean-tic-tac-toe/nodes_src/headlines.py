NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]


node("Board.move",
 "Headline: making a move",
 "A move names a square with two in-range coordinates and either returns the new board or fails with `none` if the square is already taken. Off-board coordinates can't even be passed in, so the only way a move can fail is an occupied square.",
 r"""## Plain English

**Definition (`Board.move`, TicTacToe.lean lines 24–31).** Given a [Board](#/node/Board) of size *n*, the
[Player](#/node/Player) whose turn it is, and two coordinates *x* and *y*, each a number below *n* (a `Fin n`),
`Board.move` returns an *optional* board:

- if the square at (*x*, *y*) is [empty](#/node/CellState), you get `some` of the new board, which is the old one
  with that square now filled by the player;
- if the square is already filled, by either player, you get `none`.

That is the whole rule. "Is it really this player's turn?" is not checked here. The game loop in
[main](#/node/main) takes care of turns by alternating X and O.

### Why there is no "out of bounds" case

The coordinates have type `Fin n`, so each one carries a proof that it is below the board size. A caller who has
only an ordinary number must first turn it into a `Fin n`, which means proving it is in range. The terminal
frontend does exactly that in [getCoord](#/node/getCoord). So `Board.move` never needs a "coordinate too big"
branch, and none of the lookups it does can fail.

### How it is built

The work is done by [Grid.modifyM](#/node/Grid.modifyM), a "modify one cell, possibly failing" operation on grids.
`Board.move` passes it a small function on cells: an empty cell becomes "filled by this player", and anything else
gives `none`. Since this runs in the `Option` monad, a `none` from that function makes the whole move `none`. A
success is rewrapped as a board.

### Which coordinate is which?

[Grid.get](#/node/Grid.get) treats the first coordinate as the index into the *outer* vector, and the outer
entries are what [printBoard](#/node/printBoard) prints as lines. So the first number the player types (the
prompt calls it *x*) picks the **printed row**, and the second picks the position within that row. The tests
confirm it: an O at (0, 1) on a 3×3 board lands in the first row, middle column (TicTacToe/Test.lean lines 24–45).
Counting starts at 0.
""",
 [q("On a 3×3 board, what does `Board.move` return if the chosen square already holds an X and it is O's turn?",
    ["`none`", "The board unchanged, wrapped in `some`", "A board with the X replaced by an O", "A runtime error"], 0,
    "Any non-empty cell makes the cell function give `none`, and the Option monad passes that failure straight through (TicTacToe.lean lines 27–30)."),
  q("Why does `Board.move` have no case for coordinates outside the board?",
    ["Its coordinates have type `Fin n`, so they are below `n` by construction",
     "It silently wraps coordinates around modulo `n`",
     "It returns `none` for them, the same as for occupied squares",
     "It panics, and the README hides this"], 0,
    "The coordinates are `Fin n` (TicTacToe.lean line 25), so an out-of-range value can't be built in the first place."),
  q("Does `Board.move` check that it is the given player's turn?",
    ["No. It fills the square for whichever player it is given; `main` handles alternation",
     "Yes, it returns `none` if the same player moves twice",
     "Yes, by counting the X's and O's on the board"], 0,
    "Nothing in TicTacToe.lean lines 24–31 looks at whose turn it is. Turns alternate in `main` (Main.lean lines 75–77)."),
  q("A player types `0` then `2` on a 3×3 board. Where does the mark go, as printed?",
    ["First printed row, third position", "Third printed row, first position", "Centre square"], 0,
    "The first coordinate picks the outer vector, which `printBoard` prints as a line (TicTacToe/Grid.lean lines 9–14, Main.lean lines 15–17)."),
 ],
 caveats=["\"New board = old board with that square filled\" is the intended reading, and it is what the sorry'd lemma `movesAreValid` would establish. Nothing in the project proves it."],
 widgets=walk("How the definition works (TicTacToe.lean, lines 24-31)", [
  {"text": "Run the board's grid through Grid.modifyM at row x, column y, in the Option monad.", "link": "Grid.modifyM"},
  {"text": "The cell function: an empty cell becomes 'filled by the current player' (line 29)."},
  {"text": "Any other cell, filled by either player, gives none, which aborts the whole move (line 30)."},
  {"text": "On success, wrap the new grid back up as a Board and return it in some (line 31).", "link": "Board"},
 ]))


node("gameDone",
 "Headline: detecting a win",
 "A game is won when some row, column or one of the two long diagonals is completely filled by one player. `gameDone` checks rows, then columns, then the two diagonals, and reports the first winner it finds. It never reports a draw.",
 r"""## Plain English

**Definition (`gameDone`, TicTacToe.lean lines 56–63).** For a board whose size is at least 1 (written as a
successor, `Nat.succ n`), `gameDone` returns `some p` if player *p* has a complete line and `none` otherwise.
"Complete line" means one of:

1. a **row**: some inner vector of the grid is entirely *p*;
2. a **column**: some row of the [transposed](#/node/Grid.transpose) grid is entirely *p*;
3. the **main diagonal** ([diagonalOne](#/node/diagonalOne)): cells (0,0), (1,1), …;
4. the **other diagonal** ([diagonalTwo](#/node/diagonalTwo)): cells (0, n−1), (1, n−2), ….

Each line is checked by [completeSeries](#/node/completeSeries): look at its first cell, and if that cell is
filled by *p*, check that every cell is filled by *p*.

### The order, and laziness

The four checks are stored as *delayed* computations, each taking a dummy unit argument. They are then combined
from left to right with `Option.orElse`: keep the first `some`, and only run the next check while everything so
far gave `none`. So rows are checked first, then columns, then the diagonals, and once a winner is found the
remaining checks do not run. Within rows and columns, the first winning line (by index) wins.

### What it does *not* do

- **No draws.** A full board with no line gives `none`, just like a game in progress. See [main](#/node/main) for
  what that means for the program.
- **Any size.** Nothing is special about 3: on an *n*×*n* board a win is a full line of *n*, not "three in a row".
- **No consistency check.** If a made-up board had lines for both players, the one found first would be
  reported. That can't happen in real play.

### Why the size must be at least 1

[completeSeries](#/node/completeSeries) starts by reading cell 0 of the line, which only exists if the line is
non-empty. The type `Board (Nat.succ n)` makes that true. This is why [main](#/node/main) refuses a board size
of 0.
""",
 [q("On a 4×4 board, X has three in a row and the fourth square of that row is empty. What does `gameDone` say?",
    ["`none`: a win needs a whole line of 4", "`some X`: three in a row always wins", "It is undefined for 4×4 boards"], 0,
    "`completeSeries` requires *every* cell of the line to be the same player (TicTacToe.lean lines 33–40). The line length is the board size."),
  q("The board is full and nobody has a line. What does `gameDone` return?",
    ["`none`, the same as an unfinished game", "A special draw value", "`some` of whoever moved last"], 0,
    "The return type is `Option Player` (TicTacToe.lean line 56). There is no value for a draw."),
  q("Why is `gameDone` stated only for boards of size `Nat.succ n`?",
    ["Its line check reads the first cell of each line, which must exist",
     "Tic-tac-toe needs at least 3 squares per side",
     "Transposing an empty grid is impossible"], 0,
    "`completeSeries` reads cell 0 of a vector of length `Nat.succ n` (TicTacToe.lean lines 33–34)."),
  q("Which lines does `gameDone` look at?",
    ["All rows, all columns, and the two long diagonals",
     "Only rows and columns",
     "Every diagonal of every length",
     "Only the row and column of the last move"], 0,
    "The four checks are listed in TicTacToe.lean lines 58–61."),
 ],
 caveats=["Nothing is proved about `gameDone`. The tests in TicTacToe/Test.lean lines 47–168 run it on five 3×3 boards (no winner, row, column, both diagonals). They are `#eval` lines that print true or false. They are not proofs, and a false result would not stop the build."],
 widgets=walk("How the definition works (TicTacToe.lean, lines 56-63)", [
  {"text": "Check 1, rows: search the grid's rows for the first one where completeSeries finds a winner (line 58).", "link": "completeSeries"},
  {"text": "Check 2, columns: do the same search on the transposed grid (line 59).", "link": "Grid.transpose"},
  {"text": "Checks 3 and 4: run completeSeries on the two diagonals (lines 60–61).", "link": "diagonalTwo"},
  {"text": "Combine the four delayed checks left to right with Option.orElse, starting from none. The first some wins, and later checks are not run (line 63)."},
 ]))


node("main",
 "Headline: the playable game",
 "`main` is the terminal game. It asks for a board size of at least 1, then alternates X and O, re-prompting on bad input until a legal move is entered, and stops only when someone wins. A drawn game never ends: the program keeps asking for a move that can't be made.",
 r"""## Plain English

**Program (`main`, Main.lean lines 52–82).** This is the executable named in the lakefile. It runs as follows:

1. Print a banner, "Tic-Tac-Toe without bounds checks*", with the footnote "*In theory".
2. Ask for the board size using [getNumber](#/node/getNumber). An answer of 0 is rejected and asked again. An
   answer *k* ≥ 1 is kept as *k* − 1, so the board type is `Board (Nat.succ (k−1))`, a size known to be at
   least 1, which [gameDone](#/node/gameDone) needs.
3. Start from the empty board ([Board.init](#/node/Board.init)) and print it ([printBoard](#/node/printBoard)).
4. Loop: ask the current player for a move ([getMove](#/node/getMove)), print the new board, and ask
   [gameDone](#/node/gameDone) whether someone has won. If yes, print "Congrats" and that player's letter and
   stop. If not, switch players (X → O → X …) and repeat. X moves first.

### "Failure-free", in the README's sense

The README says the program is not guaranteed to terminate but "will never error". That is what the code shows.
Every input step is a retry loop (marked `partial`, so Lean does not require a termination proof). Bad numbers,
coordinates that are too large, and occupied squares all lead to "please try again". No step ever indexes an array
without a proof that the index is in range.

### The draw case

[gameDone](#/node/gameDone) has no "draw" answer. So when the board fills up with no winner, the loop calls
[getMove](#/node/getMove) again. Every square is taken, so every move is rejected, and the program asks forever
until the user interrupts it. This is a case of the non-termination the README admits to. It is not a crash.
""",
 [q("What happens if the user enters 0 as the board size?",
    ["They are told the size must be at least 1 and asked again", "The program crashes", "A 0×0 board is created and X wins immediately"], 0,
    "The size check sends 0 back as an error message, and getNumber prompts again (Main.lean lines 60–62)."),
  q("A game on a 3×3 board ends with all nine squares filled and no line. What does the program do?",
    ["It keeps asking for a move, and rejects every one", "It prints \"Draw\" and stops", "It prints \"Congrats X!\""], 0,
    "`gameDone` returns `none`, so the loop continues (Main.lean lines 73–77), and `getMove` rejects every occupied square (Main.lean lines 45–49)."),
  q("Which player moves first?",
    ["X", "O", "The user chooses"], 0,
    "The loop starts with player X (Main.lean line 82)."),
  q("What does the README's 'failure-free' claim amount to here?",
    ["Every bad input is caught and asked again, and no array lookup can be out of range; the program may still loop forever",
     "A Lean proof that every game terminates",
     "A Lean proof that the game logic is correct"], 0,
    "No theorem about `main` exists. The guarantee comes from the types (`Fin n` coordinates, size-indexed vectors) together with the retry loops."),
 ],
 caveats=["`main`, `getMove`, `getNumber` and `getCoord` are `partial`. Lean accepts them without a termination proof, and nothing is proved about their behaviour. The \"never errors\" reading is from inspecting the source, not from a theorem.",
          "The draw-case behaviour comes from reading the code. The program was not run for this site."],
 widgets=walk("How the program goes (Main.lean, lines 52-82)", [
  {"text": "Print the banner (lines 53–56)."},
  {"text": "Read the board size and reject 0. Keep the size minus one, so the board type is a successor (lines 58–62).", "link": "getNumber"},
  {"text": "Create the empty board of that size and print it (lines 64–66).", "link": "Board.init"},
  {"text": "Loop: get a legal move from the current player, and print the board (lines 68–71).", "link": "getMove"},
  {"text": "Ask gameDone. If there is no winner, swap players and loop. If there is a winner, congratulate them and stop (lines 73–80).", "link": "gameDone"},
  {"text": "Start the loop with an empty board and player X (line 82)."},
 ]))


node("movesAreValid",
 "Headline: a successful move is a valid transition — PARTIAL (sorry)",
 "The project's only theorem says that whenever a move succeeds, exactly one previously empty square became the mover's and nothing else changed. Its proof is unfinished: it names the square and then stops at `sorry`. **PARTIAL (sorry).**",
 r"""## Plain English

**Theorem (`movesAreValid`, TicTacToe/Lemma.lean lines 10–16), PARTIAL (sorry).** Take any board `prev`, any
player, and any coordinates *x*, *y*. Suppose [Board.move](#/node/Board.move) returns `some next`. Then going from
`prev` to `next` is a [BoardTransition](#/node/BoardTransition) for that player. In other words, there is a square
that

- was empty in `prev`,
- is filled by the mover in `next`,

and every *other* square has the same contents in both boards.

This is the correctness property you would want from `Board.move`: a successful move does exactly one thing,
to exactly one empty square.

### Status: unfinished

The proof supplies *x* and *y* as the square (the obvious choice) and leaves everything else to `sorry`. Upstream
commit history calls the last change "Slightly fill in lemma". So **none of the three facts is proved**: not
"was empty", not "is now filled", not "everything else unchanged". The README says it too: "Nothing interesting
is prooved". The statement looks true to us, but it would take lemmas about how `Array.set` interacts with
lookups, and the project doesn't supply them.

### Two details of the statement

- The hypothesis "the move returned `some next`" is written as an **implicit** argument, in curly braces.
  Implicit arguments are normally filled in automatically by Lean. A proof of an equation can't be found that
  way, so anyone using this theorem would have to pass that hypothesis explicitly by name. It doesn't change what
  the theorem claims. It only makes it awkward to use.
- [BoardTransition](#/node/BoardTransition) only says *some* square changed. It doesn't say the square is (*x*,
  *y*). The proof does pick (*x*, *y*), though, so the full proof would show that too.

### Does the game depend on it?

No. The file is not imported by the library root (TicTacToe.lean lines 3–4) or by `Main.lean`, so the `sorry`
has no effect on the game. It is a stated goal, not a foundation.
""",
 [q("What has actually been proved about `Board.move` in this repository?",
    ["Nothing: the one theorem about it ends in `sorry`",
     "That it changes exactly one empty square",
     "That it never returns `none`"], 0,
    "The proof term in TicTacToe/Lemma.lean line 16 supplies the coordinates and then `sorry`."),
  q("Suppose `Board.move prev X 1 2 = some next`. What would the finished theorem tell you?",
    ["Some square that was empty in `prev` holds X in `next`, and all other squares match",
     "`next` has a winning line for X",
     "It is O's turn in `next`",
     "`prev` was the empty board"], 0,
    "That is the definition of `BoardTransition` (TicTacToe/Lemma.lean lines 3–8), which is the conclusion."),
  q("Does `BoardTransition` say anything about whose turn it is?",
    ["No. It only relates two boards and the player who filled the square", "Yes, it says the players alternate"], 0,
    "The player is a parameter, and only the filled square mentions it (TicTacToe/Lemma.lean lines 3–8)."),
  q("Does the `sorry` in this theorem affect the playable game?",
    ["No. The game doesn't import TicTacToe/Lemma.lean", "Yes. The game can't be compiled while a `sorry` is present"], 0,
    "Main.lean imports only TicTacToe and TicTacToe.Test (Main.lean lines 1–2), and the library root imports only Vector and Grid (TicTacToe.lean lines 3–4)."),
 ],
 caveats=["**PARTIAL (sorry).** Everything after the choice of witnesses is `sorry` (TicTacToe/Lemma.lean line 16).",
          "The success hypothesis is an implicit binder, which is unusual for a hypothesis. The meaning is unchanged.",
          "We think the statement is true, but nobody, including this site, has proved it, and the Lean was not built here."],
 widgets=walk("How the proof goes (TicTacToe/Lemma.lean, lines 10-16)", [
  {"text": "Goal: there are coordinates with three properties: empty before, filled after, and every other square unchanged.", "link": "BoardTransition"},
  {"text": "Supply x as the first coordinate and y as the second (line 16)."},
  {"text": "The three properties together: sorry. Not proved (line 16)."},
  {"text": "Proving them would mean unfolding Board.move, Grid.modifyM and Vector.modifyM, and using the success hypothesis to rule out the 'occupied' branch.", "link": "Board.move"},
 ]))
