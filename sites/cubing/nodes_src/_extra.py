# Extra quiz questions, appended by each node file (files starting with _ are not node files).
NODES = []  # write_nodes.py loads every .py, including _-prefixed ones
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
EXTRA = {
 "Face": q("Which face turns change no orientation under the convention used here?", ["U and D", "F and B", "L and R", "None"], 0,
   "cornerTwist and edgeFlip are zero for U and D (Cube3x3/Moves.lean lines 164–166 and 378–380)."),
 "reachable": q("Is `reachable` a subgroup or merely a set?", ["Just a set of move sequences", "A subgroup of Cube", "A number", "A list"], 1,
   "Subgroup.closure (Cube3x3/Moves.lean line 464)."),
 "OPerm.twistSum": q("Does `twistSum` look at the permutation part of a state?", ["Yes, it multiplies by the sign", "No, only the orientation vector",
   "Only for edges"], 1, "twistSum_apply, Cube3x3/Invariants.lean lines 61–62."),
 "OPerm.parity": q("Into which group does `OPerm.parity` map?", ["ZMod 3", "The units of the integers, {+1, −1}", "The natural numbers", "Permutations"], 1,
   "Cube3x3/Invariants.lean line 65."),
 "invariants": q("What is the parity-product component of `invariants` on the T-perm (two corners and two edges swapped)?",
   ["+1, since both parities are −1", "−1", "0"], 0,
   "Each swap is odd; −1 × −1 = +1 (Cube3x3/Invariants.lean lines 79–81)."),
 "valid": q("Which result turns the kernel definition into three readable conditions?", ["card_valid", "mem_valid", "move_pow_four", "alg_cons"], 1,
   "Cube3x3/Invariants.lean lines 88–98."),
 "reachable_le_valid": q("Which cubing fact is an instance of this theorem?", ["Any position can be solved",
   "You cannot twist a single corner in place by turning faces", "God's number is 20", "R U has order 105"], 1,
   "A lone twisted corner has nonzero corner twist total, so it is not valid, hence not reachable."),
 "card_cube": q("What is 3^8 · 8! · 2^12 · 12!?", ["43,252,003,274,489,856,000", "519,024,039,293,878,272,000", "12", "2^64"], 1,
   "Twelve times the reachable count."),
 "OPerm.SetUp": q("Which cubing technique does `SetUp` formalise?", ["Memorising algorithms", "Set-up moves / conjugation: move pieces into place, apply a tool, undo",
   "Fingertricks", "Speed"], 1, "Cube3x3/Generate.lean lines 28–33."),
 "OPerm.pairTwist": q("What is `pairTwist i i`?", ["A full turn", "The zero (trivial) orientation vector", "Undefined", "A 3-cycle"], 1,
   "+1 and −1 at the same slot cancel; see the case split in Cube3x3/Generate.lean lines 104–105."),
 "cornerSetUps_surj": q("Why must the swap be between *neighbours* on the 8-cycle?", ["For the Mathlib generation lemma to apply (a full cycle plus an adjacent swap generate all permutations)",
   "Any swap works equally", "Because corners are adjacent on the cube"], 0, "Perm.closure_cycle_adjacent_swap, used in Cube3x3/Solvable.lean lines 137–147."),
 "Sticker": q("What happens to a sticker's orientation component when a state moves it?", ["Nothing", "It is shifted by the twist its piece gains",
   "It is reset to 0", "It becomes the face colour"], 1, "smul_def, Cube3x3/Facelets.lean lines 53–54."),
 "toStickers": q("Which Mathlib construction glues the corner and edge halves together?", ["Perm.sumCongrHom", "Subgroup.closure", "ZMod", "Nat.card"], 0,
   "Cube3x3/Facelets.lean lines 81–84."),
 "Facelet": q("How is a corner facelet's cubie position computed?", ["Looked up in a picture", "By adding the outward normals of the three faces the corner touches",
   "Randomly", "From colours"], 1, "Facelet.cubie, Cube3x3/Facelets.lean lines 263–266."),
 "colors": q("What colour does a centre facelet show?", ["Depends on the state", "Always its own face", "White"], 1,
   "Centres never move: Cube3x3/Facelets.lean line 208."),
 "Face.turnVec": q("Can two different vectors be sent to the same vector by `Face.turnVec`?", ["No, it is proved injective", "Yes, it collapses the axis", "Only for the up face"], 0,
   "Face.turnVec_injective, Cube3x3/Facelets.lean lines 300–302."),
 "pull_move": q("Does `pull_move` rely only on the move tables?", ["Yes", "No, also on the hand-written sticker-order tables and the geometry definitions"], 1,
   "Facelet.cubie and Facelet.normal use cornerStickers / edgeStickers (Cube3x3/Facelets.lean lines 263–272)."),
}
def apply(nodes):
    for n in nodes:
        if n["id"] in EXTRA: n["quiz"].append(EXTRA[n["id"]])
