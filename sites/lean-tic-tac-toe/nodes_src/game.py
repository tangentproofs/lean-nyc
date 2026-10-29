NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}


node("Player",
 "Player: X or O",
 "There are exactly two players, X and O, with nothing else attached to them.",
 r"""## Plain English

**Type (`Player`, TicTacToe.lean lines 6–9).** A player is either `x` or `o`. The type derives printing and
equality testing. The terminal frontend shows them as the letters X and O (Main.lean lines 4–6).
""",
 [q("How many values does `Player` have?", ["2", "3, counting 'nobody'", "Any number"], 0,
    "TicTacToe.lean lines 6–9 list x and o. 'Nobody' is represented by CellState.empty instead."),
  q("Where is 'no player here' represented?", ["In CellState, as empty", "As a third Player value", "As Option Player inside Player"], 0,
    "TicTacToe.lean lines 11–14."),
  q("Who moves first in the game?", ["X", "O"], 0, "Main.lean line 82."),
 ])


node("CellState",
 "CellState: empty or taken by a player",
 "A square is either empty or filled by one specific player. This is the README's \"three states\": empty, X, O.",
 r"""## Plain English

**Type (`CellState`, TicTacToe.lean lines 11–14).** A cell is `empty`, or `filled p` for a
[Player](#/node/Player) *p*. With two players that makes the three states the README mentions ("a square matrix
over 3 states"). Equality testing is derived, and [completeSeries](#/node/completeSeries) uses it to compare cells.
On screen, an empty cell is shown as a box character (Main.lean lines 10–12).
""",
 [q("How many different cell states are there?", ["3", "2", "4"], 0,
    "empty, filled x, filled o (TicTacToe.lean lines 11–14)."),
  q("What does `filled o` mean?", ["The square holds an O", "The square is about to be filled by O", "O has won"], 0,
    "TicTacToe.lean line 13."),
  q("Which cell state can a move overwrite?", ["Only empty", "Any", "Only the other player's"], 0,
    "Board.move rejects any non-empty cell (TicTacToe.lean lines 28–30)."),
 ])


node("Board",
 "Board: an n×n grid of cells",
 "A `Board n` is just a square `n`×`n` grid of cell states. The size is part of the type, so a 3×3 board and a 4×4 board are different types.",
 r"""## Plain English

**Structure (`Board`, TicTacToe.lean lines 16–18).** A board of size *n* wraps one
[Grid](#/node/Grid) of [CellState](#/node/CellState)s of side *n*. It adds nothing else: no record of whose turn
it is and no move history. Equality and printing are derived.

Because the size is in the type, the board size the player types at run time becomes part of the board's type
in [main](#/node/main). That is why main has to turn the number into a type-level size, at least 1.
""",
 [q("Does a `Board` record whose turn it is?", ["No, only the cells", "Yes, in a turn field"], 0,
    "The only field is grid (TicTacToe.lean lines 16–18)."),
  q("Is the game limited to 3×3?", ["No. Any n works, and main asks for the size", "Yes, n is fixed to 3"], 0,
    "Board is parametrised by n (TicTacToe.lean line 16), and main reads n from the user (Main.lean lines 58–64)."),
  q("What is a `Board 2`?", ["A 2×2 grid of cell states", "A board for 2 players", "A board after 2 moves"], 0,
    "TicTacToe.lean lines 16–18. Test.lean also builds 2×2 boards."),
 ])


node("Board.init",
 "Board.init: the empty board",
 "The starting board, with every square empty, at whatever size is wanted.",
 r"""## Plain English

**Definition (`Board.init`, TicTacToe.lean lines 20–22).** A [board](#/node/Board) whose grid is
[Grid.mkGrid](#/node/Grid.mkGrid) filled with [empty](#/node/CellState). The size comes from the expected type.
[main](#/node/main) uses it at the size the player chose.
""",
 [q("What is in the cells of `Board.init`?", ["All empty", "An X in the centre", "Alternating X and O"], 0,
    "TicTacToe.lean line 21."),
  q("How is its size chosen?", ["By the type it is used at", "It is always 3", "It is passed as a string"], 0,
    "n is implicit (TicTacToe.lean line 20). See Main.lean line 64."),
  q("Which function builds the cells?", ["Grid.mkGrid", "Grid.transpose", "Board.move"], 0, "TicTacToe.lean line 21."),
 ])


node("completeSeries",
 "completeSeries: is this line all one player?",
 "Given a non-empty line of cells, returns the player who fills every cell of it, or `none` if any cell is empty or the line is mixed. It decides one row, column or diagonal.",
 r"""## Plain English

**Definition (`completeSeries`, TicTacToe.lean lines 33–40).** The line is a [Vector](#/node/Vector) of length
`Nat.succ n`, so it has at least one cell. Look at cell 0:

- if it is empty, the line is not a win: `none`;
- if it is filled by *p*, check that **every** cell of the line equals "filled by *p*". If so, `some p`;
  otherwise `none`.

The "every cell" check is over the whole underlying array, cell 0 included, which is harmless. Requiring the line
to be non-empty is what lets the first lookup happen without a failure case, and it is why
[gameDone](#/node/gameDone) needs boards of size at least 1.
""",
 [q("For the line (X, X, empty), what is the result?", ["`none`", "`some X`", "`some empty`"], 0,
    "Not every cell equals X (TicTacToe.lean lines 38–40)."),
  q("For (O, O, O)?", ["`some O`", "`none`"], 0, "TicTacToe.lean lines 37–39."),
  q("Why is the input's length written `Nat.succ n`?", ["So that cell 0 exists", "To exclude 1×1 boards", "For performance"], 0,
    "Cell 0 is read in TicTacToe.lean line 34."),
 ])


node("diagonalOne",
 "diagonalOne: the main diagonal",
 "The line of cells (0,0), (1,1), …, (n−1,n−1), from top-left to bottom-right as printed.",
 r"""## Plain English

**Definition (`diagonalOne`, TicTacToe.lean lines 42–43).** Using [Vector.ofFn](#/node/Vector.ofFn), entry *i* is
cell (*i*, *i*) of the board (read with [Grid.get](#/node/Grid.get)). With the first coordinate as the printed row,
this runs from the top-left to the bottom-right.
""",
 [q("Which cells are on `diagonalOne` of a 3×3 board?", ["(0,0), (1,1), (2,2)", "(0,2), (1,1), (2,0)", "(0,0), (0,1), (0,2)"], 0,
    "TicTacToe.lean line 43."),
  q("How long is it on an n×n board?", ["n", "2n", "n − 1"], 0, "It is a Vector CellState n (TicTacToe.lean line 42)."),
  q("Which function decides whether it is a win?", ["completeSeries", "Board.move", "invertFin"], 0, "TicTacToe.lean line 60."),
 ])


node("invertFin",
 "invertFin: counting from the other end",
 "Sends index `i` below `n` to `n − 1 − i`, with a proof that the result is still below `n`. It is used to walk the second diagonal.",
 r"""## Plain English

**Definition (`invertFin`, TicTacToe.lean lines 45–51).** Split on the size *n*:

- *n* = 0: there are no indices below 0, so this case can't happen (`Fin.elim0`);
- *n* = *m* + 1: send *i* to *m* − *i*, which is *n* − 1 − *i*. The proof that this is below *m* + 1 is a library
  fact about subtraction.

So 0 ↦ *n*−1, 1 ↦ *n*−2, …, *n*−1 ↦ 0. (Lean's subtraction on naturals stops at 0, but *i* ≤ *m* here, so no
truncation happens.)
""",
 [q("On a size-5 board, where does `invertFin` send 1?", ["3", "4", "1"], 0, "m = 4, and 4 − 1 = 3 (TicTacToe.lean line 49)."),
  q("Why is there a case for n = 0?", ["Lean needs every case handled; there are no indices then", "To return a default value"], 0,
    "TicTacToe.lean line 47 uses Fin.elim0."),
  q("What is it used for?", ["The anti-diagonal", "Transposing", "Reading input"], 0, "diagonalTwo, TicTacToe.lean line 54."),
 ])


node("diagonalTwo",
 "diagonalTwo: the other diagonal",
 "The line of cells (0, n−1), (1, n−2), …, (n−1, 0), from top-right to bottom-left as printed.",
 r"""## Plain English

**Definition (`diagonalTwo`, TicTacToe.lean lines 53–54).** Entry *i* is the cell at (*i*, [invertFin](#/node/invertFin) *i*),
which is (*i*, *n*−1−*i*). With rows as printed lines, this is the diagonal from top-right to bottom-left. The
last test in TicTacToe/Test.lean lines 145–168 checks it on one 3×3 board.
""",
 [q("Which cells are on `diagonalTwo` of a 3×3 board?", ["(0,2), (1,1), (2,0)", "(0,0), (1,1), (2,2)", "(2,0), (2,1), (2,2)"], 0,
    "TicTacToe.lean line 54 with invertFin."),
  q("On a 1×1 board, how do the two diagonals compare?", ["They are the same single cell", "diagonalTwo is empty", "They are disjoint"], 0,
    "invertFin sends 0 to 0 when n = 1 (TicTacToe.lean line 49)."),
  q("What does the other coordinate of entry i come from?", ["invertFin i", "i + 1", "The transpose"], 0, "TicTacToe.lean line 54."),
 ])


node("BoardTransition",
 "BoardTransition: what a legal move looks like",
 "Says that `next` arises from `prev` by one player filling one empty square: that square was empty, is now theirs, and every other square is unchanged. It is a specification, used only in the sorry'd lemma.",
 r"""## Plain English

**Definition (`BoardTransition`, TicTacToe/Lemma.lean lines 3–8).** For a player and two boards `prev` and
`next` of the same size, `BoardTransition` holds when there are coordinates (*x*, *y*) such that

1. cell (*x*, *y*) of `prev` is [empty](#/node/CellState);
2. cell (*x*, *y*) of `next` is filled by the player;
3. for every cell (*i*, *j*) other than (*x*, *y*), meaning *i* ≠ *x* or *j* ≠ *y*, the two boards agree.

This is a *statement* (a `Prop`), not a computation. It is how the project specifies a valid move, independent of
how [Board.move](#/node/Board.move) is coded. The connecting theorem, [movesAreValid](#/node/movesAreValid), is
unfinished.

It doesn't say anything about whose turn it is, about the game being unfinished, or about which coordinates were
asked for.
""",
 [q("Which of these is a BoardTransition for X?",
    ["An empty board → the same board with one X added",
     "An empty board → a board with two X's",
     "A board with an O at (0,0) → X at (0,0) instead"], 0,
    "Exactly one cell changes, from empty to X (TicTacToe/Lemma.lean lines 4–8)."),
  q("Is 'X moves twice in a row' ruled out by `BoardTransition`?",
    ["No. It relates single moves and doesn't track turns", "Yes"], 0,
    "No turn information appears in TicTacToe/Lemma.lean lines 3–8."),
  q("What does condition 3 say?",
    ["Every square other than the chosen one is the same in both boards",
     "Every square is the same in both boards",
     "The chosen square is the same in both boards"], 0,
    "TicTacToe/Lemma.lean lines 7–8."),
 ])


node("printBoard",
 "printBoard: drawing the board",
 "Prints the board one outer vector per line, with X, O, or a box character for an empty square.",
 r"""## Plain English

**Definition (`printBoard`, Main.lean lines 15–17).** For each inner vector of the grid, print it as one line
(`printRow`, Main.lean lines 8–13), showing X or O for filled cells (`playerToChar`, Main.lean lines 4–6) and a
box character for empty ones. This is why the first coordinate counts as the "row" in this explainer.
""",
 [q("What does one printed line show?", ["One inner vector of the grid", "One column", "One diagonal"], 0, "Main.lean lines 16–17."),
  q("How is an empty cell shown?", ["As a box character", "As a dot", "As a space"], 0, "Main.lean line 11."),
  q("Does printing number the rows and columns?", ["No", "Yes, from 0", "Yes, from 1"], 0, "Main.lean lines 8–17 print only cells."),
 ])


node("getNumber",
 "getNumber: read a number, retrying until acceptable",
 "Reads a line, parses it as a natural number, and checks it with a given test. If either step fails, it prints a message and asks again, forever if necessary.",
 r"""## Plain English

**Definition (`getNumber`, Main.lean lines 19–32).** It takes a *test* that, for each natural number, gives
either an error message or an accepted result. Then it loops:

1. read a line from standard input and trim it;
2. if it isn't a natural number, print "Invalid natural number…" and loop;
3. otherwise apply the test. On an error message, print it and loop. On a result, return it.

It is `partial`: Lean doesn't ask for a proof that the loop ends, because it might not. This is the
"not guaranteed to terminate" from the README.
""",
 [q("What happens if the user types `abc`?", ["An error message, then another prompt", "The program crashes", "It is read as 0"], 0,
    "Main.lean lines 23–26."),
  q("Why is `getNumber` marked `partial`?", ["The loop may never end, so there is no termination proof", "It only handles some numbers", "It uses sorry"], 0,
    "Main.lean line 19. See the README on termination."),
  q("Who decides which numbers are acceptable?", ["The test passed in by the caller", "getNumber itself", "The board"], 0,
    "decPred, Main.lean lines 19 and 27–31."),
 ])


node("getCoord",
 "getCoord: read a coordinate that is provably on the board",
 "Reads a number and accepts it only if it is below the board size, returning it together with that proof as a `Fin n`. This is where an ordinary typed number becomes a safe index.",
 r"""## Plain English

**Definition (`getCoord`, Main.lean lines 34–37).** Uses [getNumber](#/node/getNumber) with the test "is it below
*n*?". The test is a *decision* that gives evidence either way: if it is below, the evidence is the proof that the
number is less than *n*, which is packaged with the number as a `Fin n`. If not, the message is "coordinate too
large, please try again".

This is the only place where untrusted input becomes an index, and the check happens once, here. Everything
downstream ([Board.move](#/node/Board.move), [Grid.get](#/node/Grid.get), …) relies on the type.
""",
 [q("On a 3×3 board the user types 3. What happens?", ["\"coordinate too large\", then another prompt", "It is read as 0", "The move goes to the last square"], 0,
    "Main.lean line 37."),
  q("What does `getCoord` return?", ["A number together with a proof that it is below n", "A plain natural number", "An Option Nat"], 0,
    "The result type is Fin n (Main.lean lines 34–36)."),
  q("Are negative coordinates possible?", ["No. Input is parsed as a natural number", "Yes, they wrap around"], 0,
    "getNumber parses with toNat? (Main.lean line 23)."),
 ])


node("getMove",
 "getMove: ask until a legal move is entered",
 "Prompts the current player for two coordinates and tries the move. If the square is taken, it says so and asks again, until some move succeeds.",
 r"""## Plain English

**Definition (`getMove`, Main.lean lines 39–50).** Print "Player X please enter x then y coordinates" (or O). Read
two coordinates with [getCoord](#/node/getCoord) and try [Board.move](#/node/Board.move). On success, return the
new board. On `none` (occupied square), print "Invalid move, please try again" and start over.

On a full board every move fails, so this loops forever. That is the draw case discussed under [main](#/node/main).
""",
 [q("What happens if the player picks an occupied square?", ["\"Invalid move\", then both coordinates are asked again", "Only y is asked again", "The other player's turn begins"], 0,
    "Main.lean lines 47–49 restart the whole loop."),
  q("Can `getMove` return without a successful move?", ["No", "Yes, after three tries"], 0, "It returns only in the some branch (Main.lean line 46)."),
  q("What happens on a full board?", ["It asks forever", "It returns the board unchanged", "It declares a draw"], 0,
    "Board.move fails on every square, so the loop never exits (Main.lean lines 45–49)."),
 ])
