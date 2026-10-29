NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}


node("Vector",
 "Vector: an array that knows its length",
 "A `Vector α n` is an ordinary array together with a proof that its length is exactly `n`. That stored proof is what lets every later lookup be safe without a runtime bounds check.",
 r"""## Plain English

**Structure (`Vector`, TicTacToe/Vector.lean lines 3–6).** A `Vector α n` has two fields:

- `array`: an ordinary Lean `Array` of elements of type α;
- `sz`: a proof that *n* equals the array's size.

So the length is part of the *type*. A `Vector CellState 3` is a list of exactly three cells, and Lean will not
let you build one from a two-element array, because you could not supply the proof.

The README calls this the "Fibonacci" of dependent types, meaning the standard first example. Its point is that
two vectors of the same type are guaranteed to have the same length, which is what you need to build a *square*
grid ([Grid](#/node/Grid)).

The structure also derives equality testing and printing. Equality testing is what lets the tests compare whole
boards with `=`.

This `Vector` is defined by the project itself, at the top level. It is not the `Vector` from Lean core or Batteries.
""",
 [q("What does the `sz` field of a `Vector α n` contain?",
    ["A proof that the array has exactly `n` elements", "The number `n` as data", "The index of the last element"], 0,
    "TicTacToe/Vector.lean line 5: `sz` is an equation between `n` and the array's size."),
  q("Can a `Vector Nat 3` be built from a 2-element array?",
    ["No: the size proof can't be supplied", "Yes, it is padded with zeros", "Yes, but lookups at index 2 will fail"], 0,
    "Building one requires a proof that 3 equals the array size (TicTacToe/Vector.lean lines 3–5)."),
  q("Why does the project want vectors rather than plain arrays for the board?",
    ["So that rows of a grid are guaranteed to have equal length and indices can be checked by type",
     "Because arrays are slower", "Because arrays can't hold enumerated values"], 0,
    "See the README's explanation, and Grid in TicTacToe/Grid.lean lines 5–7."),
 ])


node("Vector.get",
 "Vector.get: lookup with no failure case",
 "Looking up position `i` of a `Vector α n` needs `i` to be a `Fin n`, a number already proved to be below `n`. The lookup turns that proof into a proof that `i` is below the array's size, so it can never fail.",
 r"""## Plain English

**Definition (`Vector.get`, TicTacToe/Vector.lean lines 8–15).** Given a vector of length *n* and an index *i* of
type `Fin n`, return the element at position *i*.

Lean's array indexing normally needs a proof that the index is in range, unless you use a version that checks at
run time and can panic. Here the proof is built from two facts:

1. *i* is below *n*, which comes with every `Fin n`;
2. *n* equals the array's size, which is the vector's [sz](#/node/Vector) field.

Rewriting (1) with (2) gives "i is below the array size", so the indexing goes through with no runtime check and
no failure case. Every cell lookup in the game ([Grid.get](#/node/Grid.get), [completeSeries](#/node/completeSeries),
the diagonals) goes through this function. That is the concrete basis for the README's "failure-free" claim.
""",
 [q("Where does the in-range proof used by `Vector.get` come from?",
    ["The index's `Fin n` bound combined with the vector's size proof", "A runtime comparison", "It is assumed with `sorry`"], 0,
    "TicTacToe/Vector.lean lines 13–15 rewrite with `sz` and then use the index's bound."),
  q("What type must the index of `Vector.get` have for a `Vector α 5`?",
    ["`Fin 5`", "`Nat`", "`Option Nat`"], 0,
    "TicTacToe/Vector.lean line 11."),
  q("Can `Vector.get` return a 'missing' result?",
    ["No. It always returns an element of type α", "Yes, it returns `none` for bad indices"], 0,
    "The result type is plain α (TicTacToe/Vector.lean line 12), with no Option."),
 ])


node("Vector.ofFn",
 "Vector.ofFn: a vector from a formula",
 "Builds a length-`n` vector whose entry `i` is `f i`, for any function `f` on `Fin n`. It is used to build the transposed grid and both diagonals.",
 r"""## Plain English

**Definition (`Vector.ofFn`, TicTacToe/Vector.lean lines 45–49).** Given a function *f* that assigns a value to
every index below *n*, produce the vector [*f*(0), *f*(1), …, *f*(*n*−1)]. The size proof comes from the library
fact that an array built from a function on `Fin n` has size *n*.

It is how [diagonalOne](#/node/diagonalOne), [diagonalTwo](#/node/diagonalTwo) and
[Grid.transpose](#/node/Grid.transpose) describe a new line as "entry *i* is such-and-such cell".
""",
 [q("What is entry 2 of the vector `Vector.ofFn f`?",
    ["`f 2`", "`f 0`", "It depends on the array's capacity"], 0,
    "The array is built with Array.ofFn from f (TicTacToe/Vector.lean lines 45–48)."),
  q("How long is the vector built from `f : Fin 7 → α`?",
    ["7", "8", "Any length"], 0,
    "The length index comes from the domain `Fin n` (TicTacToe/Vector.lean line 45)."),
  q("Which part of the game uses `Vector.ofFn`?",
    ["The diagonals and the transpose used for win detection", "Reading input", "Printing the board"], 0,
    "See TicTacToe.lean lines 42–54 and TicTacToe/Grid.lean lines 53–62."),
 ])


node("Vector.functor",
 "Vector.functor: applying a function to every entry",
 "Mapping a function over a vector keeps its length, with a proof, so `Vector α n` becomes `Vector β n`. The transpose uses this.",
 r"""## Plain English

**Instance (`Vector.functor`, TicTacToe/Vector.lean lines 17–23).** This makes "vectors of a fixed length *n*" a
`Functor`. Mapping *f* over a vector applies *f* to every entry of the underlying array. The new size proof says
that mapping doesn't change an array's size, so the length is still *n*.

[Grid.transpose](#/node/Grid.transpose) uses it to pull entry *y* out of every row. The grid's own
`Functor` instance (TicTacToe/Grid.lean lines 16–19) maps twice, through rows and then cells, but the game never
uses it.
""",
 [q("If `v : Vector Nat 4`, what is the length of the result of mapping a function over `v`?",
    ["4", "It depends on the function", "5"], 0,
    "The size proof in TicTacToe/Vector.lean lines 20–22 shows the length is kept."),
  q("What does mapping do to the entries?",
    ["Applies the function to each one", "Applies the function only to the first one", "Reverses them"], 0,
    "It is Array.map on the underlying array (TicTacToe/Vector.lean line 19)."),
  q("Which game function relies on this instance?",
    ["Grid.transpose", "Board.move", "getNumber"], 0,
    "TicTacToe/Grid.lean lines 58–61."),
 ])


node("Vector.modifyM",
 "Vector.modifyM: change one entry, possibly failing",
 "Replaces entry `i` of a vector by the result of an effectful function, for example one that can fail. The result has the same length, with a proof. It is the low-level step behind every move.",
 r"""## Plain English

**Definition (`Vector.modifyM`, TicTacToe/Vector.lean lines 51–68).** Given a vector, an index *i* below its length,
and a function *f* that takes the old entry and returns a new one *inside some monad m*, it:

1. reads the old entry with [Vector.get](#/node/Vector.get);
2. runs *f* on it in *m*. In the game *m* is `Option`, so this step may fail;
3. converts *i* into an index for the underlying array, using the size proof;
4. writes the new entry with `Array.set` and proves that the array's size is unchanged.

If step 2 fails, the whole call fails and nothing is written. Otherwise the result is a vector of the same length
with one entry replaced.

"M" is the usual Lean/Haskell suffix for "the monadic version". With `Option`, it means "modify, or fail".
""",
 [q("In the game, what is the monad `m` when `Vector.modifyM` is used?",
    ["`Option`, so the modification can fail", "`IO`", "There is no monad"], 0,
    "Board.move works in Option (TicTacToe.lean lines 24–31), and that choice flows down through Grid.modifyM."),
  q("Does `Vector.modifyM` change the vector's length?",
    ["No. The result has the same length, with a proof", "It can grow by one", "Only if f fails"], 0,
    "The size proof at TicTacToe/Vector.lean lines 65–67 uses the fact that Array.set keeps the size."),
  q("If the function `f` fails on the old entry, what happens?",
    ["The whole modify fails, and no new vector is produced", "The old entry is kept and the call succeeds", "The entry is cleared"], 0,
    "f runs in the monad before the write (TicTacToe/Vector.lean lines 60–64), so a failure there stops everything."),
 ])


node("Grid",
 "Grid: a square n×n array",
 "A `Grid t n` is a vector of `n` vectors, each of length `n`. Being square is part of the type, so no row can be shorter or longer than the others.",
 r"""## Plain English

**Structure (`Grid`, TicTacToe/Grid.lean lines 5–7).** A grid has one field, `inner`, a
[Vector](#/node/Vector) of length *n* whose entries are themselves vectors of length *n*. So a `Grid t n` is an
*n*×*n* table of values of type *t*.

A plain array of arrays could be ragged. Here every inner vector has the same length *n* by its type, which is
what the README means by "arrays of arrays where all the interior arrays must be the same length".

**Convention.** The outer vector's entries are what [printBoard](#/node/printBoard) prints as lines, so the
first index selects a printed row and the second selects a position in it.
""",
 [q("Can a `Grid t 3` have a row of length 2?",
    ["No. Every inner vector has type `Vector t 3`", "Yes, rows can be ragged", "Only the last row"], 0,
    "TicTacToe/Grid.lean line 6: the inner vectors all have length n."),
  q("How many cells does a `Grid t 5` have?",
    ["25", "5", "10"], 0,
    "Five rows of five (TicTacToe/Grid.lean line 6)."),
  q("Which index picks the printed row?",
    ["The first one (the outer vector)", "The second one", "Neither, rows are printed as columns"], 0,
    "printBoard prints each outer entry as a line (Main.lean lines 15–17)."),
 ])


node("Grid.get",
 "Grid.get: read one cell",
 "Reads the cell in outer position `x`, inner position `y` of a grid by two safe vector lookups. Both coordinates are `Fin n`, so it can't go out of bounds.",
 r"""## Plain English

**Definition (`Grid.get`, TicTacToe/Grid.lean lines 9–14).** Take inner vector number *x* of the
[grid](#/node/Grid), then entry *y* of that vector, using [Vector.get](#/node/Vector.get) twice. Both coordinates
are `Fin n`, so both lookups are in range.

[BoardTransition](#/node/BoardTransition), the property in the sorry'd lemma, is stated in terms of
`Grid.get`, and so are the diagonals.
""",
 [q("For `Grid.get g x y`, which coordinate selects the outer vector?",
    ["`x`", "`y`", "Whichever is smaller"], 0,
    "TicTacToe/Grid.lean line 14 looks up x in the outer vector first."),
  q("Can `Grid.get` fail?",
    ["No. Both indices are `Fin n` and both lookups are proof-checked", "Yes, it returns `none` off the board"], 0,
    "The result type is plain t (TicTacToe/Grid.lean line 13)."),
  q("Which project statement is phrased in terms of `Grid.get`?",
    ["BoardTransition, the conclusion of the sorry'd lemma", "getNumber", "Grid.mkGrid"], 0,
    "TicTacToe/Lemma.lean lines 3–8 compare cells of two boards with Grid.get."),
 ])


node("Grid.modifyM",
 "Grid.modifyM: change one cell, possibly failing",
 "Changes one cell of a grid by running a possibly-failing function on it. It does this by modifying row `x`, and inside it entry `y`, using `Vector.modifyM` twice.",
 r"""## Plain English

**Definition (`Grid.modifyM`, TicTacToe/Grid.lean lines 36–51).** Given a [grid](#/node/Grid), coordinates *x*,
*y* below *n*, and a cell function *f* in some monad, it:

1. uses [Vector.modifyM](#/node/Vector.modifyM) on the outer vector at position *x*;
2. the "modification" applied to that row is *itself* a `Vector.modifyM` at position *y* with *f*;
3. wraps the resulting outer vector back up as a grid.

If *f* fails, the inner modify fails, so the outer one fails too, and no grid comes out.
[Board.move](#/node/Board.move) uses this with `Option` and a cell function that rejects occupied cells.

The definition also asks for the monad to be *lawful* (`LawfulMonad`), but the body never uses that. It would
matter only for proofs, such as the unfinished one in [movesAreValid](#/node/movesAreValid).
""",
 [q("How does `Grid.modifyM` reach cell (x, y)?",
    ["It modifies row x, and within that row modifies entry y", "It rebuilds the whole grid from scratch", "It flattens the grid to one array"], 0,
    "TicTacToe/Grid.lean lines 47–48 nest two Vector.modifyM calls."),
  q("If the cell function fails, what does `Grid.modifyM` return?",
    ["The failure (in Option: `none`)", "The original grid", "A grid with that cell emptied"], 0,
    "A failure in the inner call propagates through both monadic binds (TicTacToe/Grid.lean lines 46–51)."),
  q("Is the `LawfulMonad` requirement used by the code?",
    ["No. The body only uses ordinary monad operations", "Yes, it is needed to compile the nested calls"], 0,
    "TicTacToe/Grid.lean line 40 asks for it, and lines 46–51 never use it."),
 ])


node("Grid.mkGrid",
 "Grid.mkGrid: a grid filled with one value",
 "Builds an n×n grid in which every cell holds the same given value. The game uses it to make the empty board.",
 r"""## Plain English

**Definition (`Grid.mkGrid`, TicTacToe/Grid.lean lines 32–34).** Make a vector of length *n* in which every entry
is a vector of length *n* in which every entry is the given value. It uses the helper `Vector.mkVector`
(TicTacToe/Vector.lean lines 40–43) twice. That helper's size proof is the library fact that an array of *n* copies
has size *n*.

[Board.init](#/node/Board.init) calls it with "empty".
""",
 [q("What is in every cell of `Grid.mkGrid v`?",
    ["`v`", "Nothing, it is uninitialised", "The cell's index"], 0,
    "TicTacToe/Grid.lean lines 32–34."),
  q("What size is the grid?",
    ["Whatever `n` the type asks for", "Always 3×3", "1×1"], 0,
    "n is an implicit argument chosen by the expected type (TicTacToe/Grid.lean line 32)."),
  q("Where does the game use it?",
    ["To make the empty starting board", "To check for a win", "To print the board"], 0,
    "Board.init in TicTacToe.lean lines 20–22."),
 ])


node("Grid.transpose",
 "Grid.transpose: columns become rows",
 "Swaps the roles of the two coordinates: row `y` of the transposed grid is column `y` of the original. Win detection uses it to check columns with the same code that checks rows.",
 r"""## Plain English

**Definition (`Grid.transpose`, TicTacToe/Grid.lean lines 53–62).** Build a new grid with
[Vector.ofFn](#/node/Vector.ofFn): its line number *y* is obtained by taking entry *y* of every original line,
which is a [map](#/node/Vector.functor) of [Vector.get](#/node/Vector.get) over the outer vector. So the new
cell (*y*, *x*) is the old cell (*x*, *y*).

[gameDone](#/node/gameDone) uses this so that "is some column all one player?" becomes "is some row of the
transpose all one player?".

The project doesn't prove that transposing twice gives back the original, or anything else about it.
""",
 [q("In the transposed grid, which old cell is at (y, x)?",
    ["(x, y)", "(y, x)", "(n − x, n − y)"], 0,
    "TicTacToe/Grid.lean lines 58–61: line y gathers entry y of each old line."),
  q("Why does `gameDone` transpose the grid?",
    ["To check columns using the same row search", "To check diagonals", "To rotate the board for the other player"], 0,
    "TicTacToe.lean line 59."),
  q("Is it proved that transposing twice is the identity?",
    ["No, nothing about transpose is proved", "Yes, in TicTacToe/Lemma.lean"], 0,
    "TicTacToe/Lemma.lean contains only BoardTransition and movesAreValid."),
 ])
