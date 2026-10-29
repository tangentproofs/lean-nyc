NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

node("Corner", "Corner and edge slots",
 "The twenty moving pieces are named by where they sit on a solved cube: eight corner slots and twelve edge slots, in the standard Singmaster names (URF, UFL, …, UR, UF, …).",
 r"""## Plain English

**Definitions (`Corner`, Cube3x3/Basic.lean lines 26–35; `Edge`, Cube3x3/Basic.lean lines 38–51).**
`Corner` is a type with exactly eight values, one for each corner *slot* of the cube, named by the
three faces it touches, the up or down face first: URF, UFL, ULB, UBR, DFR, DLF, DBL, DRB.
`Edge` has twelve values, one per edge slot: UR, UF, UL, UB, DR, DF, DL, DB, FR, FL, BL, BR.

A *piece* is named after the slot it occupies on the solved cube, so "the URF corner" means both a
place and the piece that belongs there. This is exactly how a blindfolded solver thinks about the
cube, as the file's own introduction points out.

The six centres are not modelled at all. They never move relative to one another under face turns,
so they serve as the fixed frame of reference. A consequence is that whole-cube rotations and
slice moves are not part of this model; see [Cube](#/node/Cube).

Both types derive decidable equality and finiteness, which later lets Lean check facts about every
slot by brute-force case analysis.
""",
 [q("What does a value of `Corner` stand for?",
    ["A slot (a place on the cube), which also names the piece that lives there when solved",
     "A colour", "A face of the cube", "A move"], 0,
    "Cube3x3/Basic.lean lines 26–35: the constructors are slot names such as URF; pieces are named by their home slot."),
   q("Why are the six centre pieces not in the model?",
    ["They are counted inside `Edge`", "They never move relative to each other under face turns, so they fix the frame",
     "Because the cube has no centres", "They are added later as a third group"], 1,
    "The file's introduction (Cube3x3/Basic.lean lines 12–18) says the centres fix the frame."),
   q("How many values does `Edge` have?", ["8", "6", "12", "24"], 2,
    "Twelve constructors, Cube3x3/Basic.lean lines 38–51.")])

node("OPerm", "Orientation-permutations (a semidirect product)",
 "One construction serves both piece types: a state of n-orientation pieces is a twist for every slot paired with a permutation of the slots, multiplied as Mathlib's semidirect product.",
 r"""## Plain English

**Definition (`OPerm`, Cube3x3/Basic.lean lines 71–72).** For a type of slots α and a number of
orientations n, `OPerm α n` is the semidirect product of

- the group of *orientation vectors*: functions from slots to the cyclic group of order n (written
  multiplicatively, via Mathlib's `Multiplicative (ZMod n)`), and
- the group of permutations of the slots (`Equiv.Perm α`),

where a permutation acts on an orientation vector by relabelling the slots (Mathlib's `mulAutArrow`).

So an element is a pair (o, σ). The docstring fixes the meaning: the piece in slot a goes to slot
σ(a), and once there it gains the twist o(σ(a)). In group-theory language this is the wreath product
of the cyclic group of order n with the symmetric group on α, a standard way to model the cube.

**Multiplication is composition, right factor first.** Two small lemmas make this explicit:
the permutation of a product is the product of the permutations
(`OPerm.mul_right`, Cube3x3/Basic.lean lines 99–100), and the twist of a product at slot a is the left
factor's twist at a times the right factor's twist carried along by the left factor's permutation
(`OPerm.mul_left_apply`, Cube3x3/Basic.lean lines 104–105). Both hold by definition (`rfl`).

Corners use n = 3 ([CornerGroup](#/node/Cube)) and edges n = 2. Results proved once for `OPerm`
(the invariants in [twistSum](#/node/OPerm.twistSum), the [generation lemma](#/node/OPerm.SetUp.le))
are then used for both.
""",
 [q("What are the two components of an `OPerm α n` element?",
    ["Two permutations", "An orientation vector (a twist per slot) and a permutation of the slots",
     "A list of moves and a colour", "A single number mod n"], 1,
    "Cube3x3/Basic.lean lines 71–72: a semidirect product of slot-to-ZMod n functions with permutations."),
   q("In the product g * h, which acts first?", ["g", "h", "Both at once", "It depends on n"], 1,
    "Cube3x3/Basic.lean lines 88–96 and the lemmas at lines 99–105: group multiplication is composition, right factor first."),
   q("Why is the construction generic in n?",
    ["So that one definition (and one set of theorems) serves corners with 3 twists and edges with 2 flips",
     "Because the cube has n faces", "To model larger cubes", "It is not generic"], 0,
    "CornerGroup is OPerm Corner 3 and EdgeGroup is OPerm Edge 2 (Cube3x3/Basic.lean lines 75–78).")])

node("Cube", "A cube state",
 "A cube state is just a corner state together with an edge state, since corners and edges never trade places; there are 3^8 · 8! · 2^12 · 12! such states before any solvability condition.",
 r"""## Plain English

**Definitions (Cube3x3/Basic.lean lines 75–86).** `CornerGroup` is [OPerm](#/node/OPerm) on the eight
[corner slots](#/node/Corner) with 3 orientations; `EdgeGroup` is `OPerm` on the twelve edge slots with
2 orientations; and `Cube` is their direct product, a pair (corner state, edge state).

A `Cube` is best read as "an arrangement of the pieces relative to the solved cube": where each piece
went and how it is twisted or flipped. The identity element 1 is the solved cube. Many elements
of `Cube` are **not** reachable by turning faces; they correspond to taking the cube apart and
reassembling it. Which ones are reachable is the subject of the headline
[reachable_eq_valid](#/node/reachable_eq_valid).

**Counting all of them** ([card_cube](#/node/card_cube)): 3^8 twists for the corners, 8! corner
arrangements, 2^12 flips for the edges, 12! edge arrangements, which is
519,024,039,293,878,272,000.

### What the model leaves out

The centres are fixed, so the model has no whole-cube rotations and no slice moves (M, E, S).
That is the standard "Rubik's cube group" setting. It also says nothing about stickers or colours
directly; those are connected later in [toStickers](#/node/toStickers) and [colors](#/node/colors).

**Composition order.** As the file stresses (Cube3x3/Basic.lean lines 88–96), g * h means "h, then g",
so cubers' left-to-right sequences are group products read right to left. [alg](#/node/alg) takes care
of the translation.
""",
 [q("What is a `Cube`?", ["A list of 54 colours", "A pair: a corner state and an edge state",
     "A subgroup", "A move sequence"], 1, "Cube3x3/Basic.lean line 86: the product CornerGroup × EdgeGroup."),
   q("Is every element of `Cube` reachable by turning faces?",
    ["Yes, by definition", "No; only one in twelve is, as the headlines show", "Only the identity", "Exactly half"], 1,
    "Reachable states are a subgroup of index 12 (index_valid, Cube3x3/Invariants.lean lines 241–246, plus reachable_eq_valid)."),
   q("Which of these does the model *not* include?", ["Corner twists", "Edge flips",
     "Moving the centres (slice moves or whole-cube rotations)", "Corner permutations"], 2,
    "The centres fix the frame (Cube3x3/Basic.lean lines 12–18), so only the 20 corner and edge pieces move.")])

node("Face", "The six faces",
 "Six faces, U D F B L R, are the generators of the cube: each names a clockwise quarter turn.",
 r"""## Plain English

**Definition (`Face`, Cube3x3/Moves.lean lines 25–32).** A type with six values: up, down, front,
back, left and right. A face is used in two ways: as the name of a quarter turn
([move](#/node/move)), and as a colour, since each sticker's colour is the face it belongs on in the
solved cube ([colors](#/node/colors)).
""",
 [q("How many values does `Face` have?", ["4", "6", "8", "54"], 1, "Cube3x3/Moves.lean lines 25–32."),
   q("Besides naming turns, what else is a `Face` used for?", ["Counting moves", "Standing for a colour",
     "Naming corners", "Nothing else"], 1, "colors returns a Face for each facelet (Cube3x3/Facelets.lean lines 207–210).")])

node("move", "The six face turns",
 "Each clockwise quarter turn is written out as four explicit tables (corner positions, corner twists, edge positions, edge flips), using the standard computer-cubing orientation convention.",
 r"""## Plain English

**Definition (`move`, Cube3x3/Moves.lean lines 417–419).** For a [Face](#/node/Face) f, `move f` is the
[Cube](#/node/Cube) state of one clockwise quarter turn of that face. It is assembled from four tables:

- `cornerPerm` (Cube3x3/Moves.lean lines 35–161): where each corner slot's piece goes, written as an
  explicit permutation with its inverse;
- `cornerTwist` (Cube3x3/Moves.lean lines 164–198): the twist, in the integers mod 3, each corner gains;
- `edgePerm` (Cube3x3/Moves.lean lines 201–375) and `edgeFlip` (Cube3x3/Moves.lean lines 378–406): the
  same for edges, with flips mod 2.

**The orientation convention** (Cube3x3/Moves.lean lines 8–18) is the one used by computer solvers
(the project's notes credit Kociemba's tables). A corner's twist is measured from its sticker facing up or
down; an edge's flip is measured from its up/down sticker, or front/back for the middle-layer edges. With
this convention U and D change no orientation, F, B, L and R twist corners, and only F and B flip edges.
A different convention would give different twist tables but the same group.

**First sanity check.** `move_pow_four` (Cube3x3/Moves.lean lines 432–433) proves that four quarter
turns of any face restore the cube, by evaluating all four tables slot by slot (the `cube_eq` tactic,
Cube3x3/Moves.lean lines 425–429). Stronger checks come later: three order facts in the Notation chapter
(see [alg](#/node/alg)) and, most convincingly, [pull_move](#/node/pull_move), which proves that every
table agrees with an actual rotation of the cube in space.
""",
 [q("Under the convention used here, which face turns flip edges?", ["All six", "Only F and B",
     "Only U and D", "Only L and R"], 1, "edgeFlip is zero for U, D, L, R (Cube3x3/Moves.lean lines 378–406)."),
   q("What does `move_pow_four` say?", ["Four quarter turns of any one face restore the cube",
     "Any four moves restore the cube", "The cube has four faces", "Moves commute"], 0,
    "Cube3x3/Moves.lean lines 432–433."),
   q("How were the move tables obtained?", ["Computed from geometry inside Lean",
     "Typed in from standard computer-cubing tables, then cross-checked by theorems", "Guessed", "Imported from Mathlib"], 1,
    "The Notation chapter says so (Cube3x3/Notation.lean lines 203–209); pull_move later checks them against geometry.")],
 caveats=["The tables are hand-entered data. Their correctness is not assumed silently: move_pow_four, the order checks in Cube3x3/Notation.lean lines 212–222, and pull_move (Cube3x3/Facelets.lean lines 339–343) all test them."])

node("reachable", "Reachable states",
 "The reachable states are defined as the subgroup generated by the six quarter turns. Inverses are included automatically, which matches physical turning, because a turn's inverse is three more turns of the same face.",
 r"""## Plain English

**Definition (`reachable`, Cube3x3/Moves.lean line 464).** The subgroup of [Cube](#/node/Cube) generated by
the six states `move f` (Mathlib's `Subgroup.closure` of the range of [move](#/node/move)).

A subgroup closure contains all products of generators **and their inverses**. On a physical cube you
only ever turn faces, but the inverse of a clockwise quarter turn is three more clockwise quarter turns
([move_pow_four](#/node/move)), so nothing extra sneaks in (Cube3x3/Moves.lean lines 458–461 make this
point in prose). Every move *sequence* lands in `reachable` (`alg_mem_reachable`,
Cube3x3/Notation.lean lines 113–118), and `move_mem_reachable` (Cube3x3/Moves.lean lines 467–468) records
that each generator is in it.

This is the left-hand side of the headline [reachable_eq_valid](#/node/reachable_eq_valid).
""",
 [q("Why does allowing inverses not change which states are reachable?",
    ["Because every move is its own inverse", "Because the inverse of a quarter turn is three more quarter turns of the same face",
     "Because inverses are excluded", "Because the group is abelian"], 1,
    "move_pow_four (Cube3x3/Moves.lean lines 432–433)."),
   q("What generates `reachable`?", ["All of Cube", "The six clockwise quarter turns", "The T-perm", "The invariants"], 1,
    "Cube3x3/Moves.lean line 464.")],
 caveats=["The Lean never separately states 'every reachable state is a product of clockwise turns only'; that follows from move_pow_four (or finiteness) but is argued only in prose (Cube3x3/Moves.lean lines 458–461)."])

node("alg", "Move sequences in Singmaster notation",
 "A cuber's move sequence, read left to right, becomes a group product read right to left; the notation is proved to compose the way cubers expect, and three known orders check the move tables.",
 r"""## Plain English

A `Move` is a face together with a `Turn` (clockwise, half or anticlockwise: 1, 2 or 3 quarter turns;
Cube3x3/Notation.lean lines 19–40). **`alg`** (Cube3x3/Notation.lean line 66) turns a list of moves into a
[Cube](#/node/Cube) state by folding from the left, multiplying each new move *on the left*, because the
product does its right factor first.

Two lemmas pin this down: a sequence starting with m is the rest of the sequence composed after m
(`alg_cons`, Cube3x3/Notation.lean lines 81–83), and doing xs then ys is `alg ys * alg xs`
(`alg_append`, Cube3x3/Notation.lean lines 86–88). A small macro lets proofs write a sequence in
standard notation, such as the T-perm, directly as a term (Cube3x3/Notation.lean lines 182–192); an
unknown token is an error, not a silent skip.

**Order checks** (Cube3x3/Notation.lean lines 203–222): the commutator R U R' U' repeated six times
restores the cube (`commutatorRU_pow_six`), R U repeated 105 times does too (`RU_pow_105`), and the T-perm
done twice does too (`tPerm_sq`). These are well-known facts; a wrong entry in the R, U or F tables
would break at least one, as the file notes. Note they say "restores", not "has order exactly": they
check that the order *divides* 6, 105 or 2.
""",
 [q("For the sequence 'R then U', which group product does `alg` produce?",
    ["move R * move U", "move U * move R", "move R + move U", "It is ambiguous"], 1,
    "The example after Cube3x3/Notation.lean lines 194–201: R U is the U turn composed after the R turn."),
   q("What does `RU_pow_105` prove?", ["R U has order exactly 105", "Repeating R U 105 times restores the cube",
     "There are 105 reachable states", "R and U commute"], 1,
    "Cube3x3/Notation.lean line 218: it is an equation (the 105th power is 1), so the order divides 105."),
   q("What is the role of these order facts in the project?", ["They are the main theorems",
     "They are sanity checks on the hand-typed move tables", "They define the moves", "They are unproved"], 1,
    "Cube3x3/Notation.lean lines 203–209.")])

import importlib.util as _u, os as _o
_s = _u.spec_from_file_location("_extra", _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "_extra.py"))
_m = _u.module_from_spec(_s); _s.loader.exec_module(_m); _m.apply(NODES)
