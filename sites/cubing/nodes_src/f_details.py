NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

node("Edge", "Edge slots",
 "Twelve edge slots, named by the two faces each touches; each edge piece can sit in its slot two ways (flipped or not).",
 r"""## Plain English

**Definition (`Edge`, Cube3x3/Basic.lean lines 38–51).** Twelve values: four on the up layer (UR, UF, UL,
UB), four on the down layer (DR, DF, DL, DB) and four in the middle layer (FR, FL, BL, BR). See
[Corner](#/node/Corner) for how slots and pieces are named. Edge states use two orientations
(`EdgeGroup`, Cube3x3/Basic.lean line 78; see [Cube](#/node/Cube)).
""",
 [q("How many edges are in the middle layer?", ["2", "4", "8", "12"], 1, "FR, FL, BL, BR (Cube3x3/Basic.lean lines 47–50)."),
  q("How many orientations does an edge have in the model?", ["1", "2", "3", "4"], 1, "EdgeGroup is OPerm Edge 2 (Cube3x3/Basic.lean line 78)."),
  q("Do edges and corners ever trade places?", ["Yes", "No, so a state is a separate corner state and edge state"], 1,
    "Cube3x3/Basic.lean lines 80–86.")])

node("cornerTwist", "Twist and flip tables",
 "The orientation half of each face turn: the twist (mod 3) each corner gains and the flip (mod 2) each edge gains, under the standard computer-solver convention.",
 r"""## Plain English

**Definitions (`cornerTwist`, Cube3x3/Moves.lean lines 164–198; `edgeFlip`, lines 378–406).** For each
[Face](#/node/Face) and each slot, an element of the integers mod 3 (corners) or mod 2 (edges): the twist the
piece gains on arriving in its new slot. The permutation halves are `cornerPerm` (lines 35–161) and `edgePerm`
(lines 201–375). Together they make [move](#/node/move).

Pattern: U and D give all zeros. F, B, L, R give each of their four corners a twist of 1 or 2 (the four
twists on one face total 6, which is 0 mod 3). Only F and B flip edges, all four of their edges.

These numbers depend on the chosen convention (Cube3x3/Moves.lean lines 13–17); the group they generate does not.
""",
 [q("What is the total corner twist added by an R turn?", ["1", "0 mod 3", "4", "2"], 1,
    "2 + 1 + 1 + 2 = 6 ≡ 0 (Cube3x3/Moves.lean lines 191–198); this is twistSum_move_fst."),
  q("How many edges does an F turn flip?", ["0", "2", "4", "12"], 2, "Cube3x3/Moves.lean lines 381–392."),
  q("Would a different orientation convention change which states are reachable?", ["Yes", "No, only the numbers in the tables"], 1,
    "The convention is a choice of bookkeeping (Cube3x3/Moves.lean lines 13–17).")])

node("Facelet.cubie", "Where a facelet sits in space",
 "Each facelet's little cube is placed at the sum of the outward normals of the faces it touches, a point in {−1,0,1}³.",
 r"""## Plain English

**Definition (`Facelet.cubie`, Cube3x3/Facelets.lean lines 263–266).** A centre sits at its face's normal; a
corner sticker at the sum of the three normals of its corner's faces (from `cornerStickers`); an edge sticker
at the sum of two. All stickers of one piece share a position; they differ in direction
([Facelet.normal](#/node/Facelet.normal)). Used by [Face.layer](#/node/Face.layer) and by the headline
[colors_move_mul](#/node/colors_move_mul).
""",
 [q("Where is the URF corner's cubie?", ["(1, 1, 1)", "(0, 0, 0)", "(−1, 1, 1)", "(1, 0, 0)"], 0,
    "Right (+x) + up (+y) + front (+z); Face.normal at Cube3x3/Facelets.lean lines 257–260."),
  q("Do the three stickers of one corner have the same cubie position?", ["Yes", "No"], 0, "The position ignores the orientation index (line 265)."),
  q("What distinguishes them, then?", ["Their direction (Facelet.normal)", "Their colour only", "Nothing"], 0,
    "Facelet.cubie_normal_injective, Cube3x3/Facelets.lean lines 279–281.")])

node("Facelet.normal", "Which way a facelet faces",
 "A facelet faces outward along the normal of its home face (for a moving sticker, the face it belongs to when solved).",
 r"""## Plain English

**Definition (`Facelet.normal`, Cube3x3/Facelets.lean lines 269–272).** For a centre, its face's normal; for
a corner or edge sticker position, the normal of the face that sticker position lies on (via `cornerFace` /
`edgeFace`, lines 193–199). Together with [Facelet.cubie](#/node/Facelet.cubie) it pins a facelet down
uniquely (`Facelet.cubie_normal_injective`, lines 279–281).
""",
 [q("For a facelet position, what does `Facelet.normal` give?", ["A colour", "An outward unit vector", "A number mod 3"], 1,
    "Cube3x3/Facelets.lean lines 269–272."),
  q("Do position and direction together identify a facelet?", ["Yes, proved by checking all pairs", "No"], 0,
    "Cube3x3/Facelets.lean lines 279–281."),
  q("Does `Facelet.normal` depend on the cube state?", ["Yes", "No, it describes fixed positions on the surface"], 1,
    "It takes only a facelet, no state (line 269).")])

node("Face.layer", "A face's turning layer",
 "A facelet is on face f's layer when its little cube lies in the outer slab on f's side: dot product of f's normal with its position equals 1.",
 r"""## Plain English

**Definition (`Face.layer`, Cube3x3/Facelets.lean line 284).** See [Face.turnVec](#/node/Face.turnVec) for
the geometry. Each layer has 21 facelets: 9 on the face itself and 3 on each of the four neighbouring faces'
edge rows. It is decidable (line 286), which lets [pull_move](#/node/pull_move) check every case.
""",
 [q("Is the centre of face f on f's layer?", ["Yes", "No"], 0, "Its position is f's normal, whose dot product with itself is 1."),
  q("Is the centre of the opposite face on f's layer?", ["Yes", "No, its dot product is −1"], 1, "Cube3x3/Facelets.lean line 284."),
  q("How many facelets does one turning layer carry?", ["9", "12", "21", "54"], 2,
    "9 on the face plus a row of 3 on each of the four adjacent faces.")])
