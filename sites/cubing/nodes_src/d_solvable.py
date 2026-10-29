NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

node("twoCornerTwist", "The algorithms the proof uses",
 "The hard direction needs only seven concrete facts about well-known algorithms (T-perm, two long cycles, A-perm, U-perm, a two-corner twist and a two-edge flip), each proved by evaluating the move tables on every piece.",
 r"""## Plain English

Cube3x3/Solvable.lean lines 22–118 prove what each tool does, by computing its effect on all twenty pieces
(the `cube_eq` tactic, or a slot-by-slot check of one permutation):

| Fact | What it shows | Lines |
|---|---|---|
| `tPerm_fst`, `tPerm_snd` | the T-perm swaps corners URF/UBR and edges UR/UL | 31–36 |
| `cycle8` | U D2 L2 moves all eight corners round one cycle | 53–54 |
| `cycle12` | U R U D L moves all twelve edges round one cycle | 65–66 |
| `aPerm` | the A-perm is a pure 3-cycle of corners, edges untouched | 77–79 |
| `uPerm` | the U-perm is a pure 3-cycle of edges, corners untouched | 90–92 |
| `twoCornerTwist` | a 26-move sequence built from sledgehammers twists UBR forward and URF back, nothing else | 103–106 |
| `twoEdgeFlip` | a 14-move sequence flips UF and UL, nothing else | 117–118 |

The first three are only about permutations (they feed [cornerSetUps_surj](#/node/cornerSetUps_surj));
the last four are the 3-cycle and two-slot-twist inputs of the [generation lemma](#/node/OPerm.SetUp.le)
for corners and for edges.

Each is an exact equation between cube states, checked by the Lean kernel through definitional
evaluation of the move tables (no `native_decide`).
""",
 [q("What does `twoCornerTwist` establish?", ["It twists every corner", "It twists exactly two corners in opposite directions and changes nothing else",
     "It swaps two corners", "It flips two edges"], 1, "Cube3x3/Solvable.lean lines 103–106: the result equals a pure pair twist on UBR and URF."),
   q("Why are `cycle8` and `cycle12` needed?", ["To count states", "Together with the T-perm swap they generate every permutation of corners (edges)",
     "To check move tables", "They are not used"], 1, "surj_of_cycle, Cube3x3/Solvable.lean lines 137–147."),
   q("How is each algorithm fact checked?", ["By evaluating the move tables on every piece inside the kernel", "By native compiled code",
     "By a physical cube", "It is assumed"], 0, "cube_eq / Equiv.ext with rfl per slot; no native_decide anywhere (CubingResults.lean is empty).")])

node("cornerSetUps_surj", "Set-ups realise every permutation",
 "Reachable states move the corners in every possible way, and likewise the edges: a full cycle plus one adjacent swap generates the whole symmetric group.",
 r"""## Plain English

**Theorems (`cornerSetUps_surj`, Cube3x3/Solvable.lean lines 164–172; `edgeSetUps_surj`, lines 175–183).**
For every permutation σ of the corner slots there is a reachable state whose corner part permutes the
corners by σ. Same for edges.

Here `cornerSetUps` (line 150) is the set of corner parts of [reachable](#/node/reachable) states.

**How.** Mathlib knows that an n-cycle together with a swap of two neighbours on it generates every
permutation. A private helper `surj_of_cycle` (lines 137–147) applies that. The cycle comes from
`cycle8` (U D2 L2 is an 8-cycle on corners), and the adjacent swap from the T-perm, whose corner swap
URF/UBR happens to be adjacent on that cycle (see [the algorithms](#/node/twoCornerTwist)). For edges,
`cycle12` and the T-perm's UR/UL swap play the same roles.

Note this does **not** say reachable states can permute corners *alone* in every way; an odd
corner permutation drags an odd edge permutation along. It only says the corner *part* can be anything,
which is all the [set-up](#/node/OPerm.SetUp) hypothesis needs.
""",
 [q("Does this theorem say a reachable state can swap two corners and nothing else?",
    ["Yes", "No, only that the corner part of some reachable state has the given permutation; edges may move too"], 1,
    "cornerSetUps is a projection of reachable (Cube3x3/Solvable.lean line 150); validity forbids a lone corner swap."),
   q("Which two permutations generate all corner permutations here?", ["The A-perm and the U-perm",
     "The 8-cycle from U D2 L2 and the T-perm's swap of two neighbours on that cycle", "U and D", "Any two"], 1,
    "Cube3x3/Solvable.lean lines 164–170.")])

node("valid_le_reachable", "Every valid state is reachable",
 "The hard direction: apply the generation lemma to corners and to edges separately, and if the parities are odd, fix that first with one quarter turn.",
 r"""## Plain English

**Theorem (`valid_le_reachable`, Cube3x3/Solvable.lean lines 271–280).** [valid](#/node/valid) is
contained in [reachable](#/node/reachable).

**Corner and edge halves.** `pureCorners` (line 194) is the set of reachable states that leave every edge
alone, viewed as corner states; `pureEdges` (line 197) likewise. Reachable set-ups conjugate these into
themselves (`setUp_corners`, `setUp_edges`, lines 200–217), and since reachable states are valid, every
pure-corner state has total twist zero (`pureCorners_le`, `pureEdges_le`, lines 220–225).

Feeding in the A-perm as the 3-cycle and `twoCornerTwist` as the pair twist, the
[generation lemma](#/node/OPerm.SetUp.le) gives `corners_le` (lines 228–237): every corner state with
zero twist and even permutation is reachable *without touching the edges*. `edges_le` (lines 240–249)
does the same for edges with the U-perm and `twoEdgeFlip`.

**Even case** (`even_mem`, lines 260–268): a valid state with even parities is its corner part times its
edge part, both reachable.

**Odd case**: multiply by one U turn. U is odd on both corners and edges, so the product is valid with even
parities, hence reachable; then undo the U turn.
""",
 [q("Why does the odd case multiply by a U turn?", ["U is the identity", "U changes both parities at once, making them even while keeping validity",
     "U fixes all twists and flips, which matters", "Any state times U is reachable"], 1,
    "Cube3x3/Solvable.lean lines 275–280."),
   q("What does `corners_le` give, in cubing terms?", ["Every corner arrangement is solvable",
     "Any corner state with zero total twist and an even permutation can be reached without disturbing the edges", "Corners can be twisted individually",
     "The corners determine the edges"], 1, "Cube3x3/Solvable.lean lines 228–237."),
   q("Which 3-cycle algorithm is used for edges?", ["T-perm", "A-perm", "U-perm", "Sune"], 2, "uPerm, Cube3x3/Solvable.lean lines 240–245.")])

node("reachable_eq_valid", "Headline: the fundamental theorem of the cube",
 "A cube state can be reached by turning faces exactly when its corner and edge permutations have the same parity, its corner twists total 0 mod 3, and its edge flips total 0 mod 2. These three invariants are the only obstructions.",
 r"""## Plain English

**Theorem (`reachable_eq_valid`, Cube3x3/Solvable.lean lines 290–291).** The subgroup of
[reachable](#/node/reachable) states equals the subgroup of [valid](#/node/valid) states.

Unpacked with `mem_valid` (Cube3x3/Invariants.lean lines 88–98): an arrangement of the 20 corner and edge
pieces (relative to fixed centres) can be produced from the solved cube by quarter turns of the six
faces **if and only if**

- the corner permutation and the edge permutation are both even or both odd,
- the corner twists sum to a multiple of 3, and
- the edge flips sum to a multiple of 2.

The source docstring calls this *the fundamental theorem of the cube*. Its proof is the two inclusions:
[reachable_le_valid](#/node/reachable_le_valid) (the invariants are preserved) and
[valid_le_reachable](#/node/valid_le_reachable) (nothing else is in the way).

**Is the statement faithful?** Yes, in the standard model: "reachable" is literally the subgroup generated
by the six quarter turns (inverses included, which costs nothing, since a turn's inverse is three turns),
and "valid" is literally the kernel of the three invariants. It is a statement about the cubie model with fixed
centres, not about stickers; [toStickers_injective](#/node/toStickers_injective) and
[colors_move_mul](#/node/colors_move_mul) are what tie that model to the coloured cube you hold.

**Status:** complete proof in the file, no `sorry`, no `native_decide`; the upstream axiom audit pins its
axioms to propext, Classical.choice and Quot.sound (CubingAudit.lean lines 13–15). Not built for this
site.
""",
 [q("Which state is NOT reachable?", ["The solved cube", "A T-perm (two corners and two edges swapped)",
     "A single corner twisted in place, everything else solved", "Two corners twisted in opposite directions"], 2,
    "A single twisted corner makes the corner twist total nonzero mod 3, so it is not valid (Cube3x3/Invariants.lean lines 88–98)."),
   q("What does the theorem say about the 'two parities'?", ["Both must be even", "They must be equal (both even or both odd)",
     "They are always odd", "Only corner parity matters"], 1, "mem_valid, Cube3x3/Invariants.lean lines 88–89."),
   q("Which direction needs the specific algorithms?", ["reachable ⊆ valid", "valid ⊆ reachable", "Both equally", "Neither"], 1,
    "valid_le_reachable (Cube3x3/Solvable.lean lines 271–280) uses the T-perm, A-perm, U-perm and orientation tools."),
   q("Does the model include slice moves or whole-cube rotations?", ["Yes", "No; centres are fixed and only the six outer faces turn"], 1,
    "Cube3x3/Moves.lean line 464 generates from the six face turns only.")],
 caveats=["Complete proof in the source; axioms pinned upstream (CubingAudit.lean lines 13–15) to the three standard ones. Not built for this site.",
          "This is the cubie-level statement (pieces in slots, with orientation conventions from Cube3x3/Moves.lean lines 8–18). The link to physical stickers is made separately in Cube3x3/Facelets.lean."],
 widgets=[{"type": "walkthrough", "title": "How the proof goes (Cube3x3/Solvable.lean, lines 290-291, with its inputs)",
   "config": {"steps": [
     {"text": "Easy inclusion: every face turn keeps all three invariants, so the subgroup they generate lies in valid (reachable_le_valid, Cube3x3/Invariants.lean lines 197–200).", "link": "reachable_le_valid"},
     {"text": "Concrete algorithms are evaluated on all pieces: T-perm, an 8-cycle and a 12-cycle, A-perm, U-perm, two-corner twist, two-edge flip (Cube3x3/Solvable.lean lines 31–118).", "link": "twoCornerTwist"},
     {"text": "The cycles plus the T-perm swaps show reachable states' corner (edge) parts realise every permutation (lines 137–183).", "link": "cornerSetUps_surj"},
     {"text": "The generic generation lemma, applied to reachable pure-corner and pure-edge states, shows every zero-twist even corner state and every zero-flip even edge state is reachable on its own (lines 200–249).", "link": "OPerm.SetUp.le"},
     {"text": "A valid state with even parities is the product of its corner and edge parts, so it is reachable (even_mem, lines 260–268)."},
     {"text": "A valid state with odd parities becomes even after one U turn, which is undone afterwards (valid_le_reachable, lines 271–280).", "link": "valid_le_reachable"},
     {"text": "The two inclusions give equality by antisymmetry (lines 290–291)."}]}}])

node("card_reachable", "Headline: 43,252,003,274,489,856,000 reachable states",
 "Exactly 43,252,003,274,489,856,000 states of the cube can be reached by turning faces, the well-known figure, now with a complete formal proof.",
 r"""## Plain English

**Theorem (`card_reachable`, Cube3x3/Solvable.lean lines 294–295).** The subgroup of
[reachable](#/node/reachable) states has exactly 43,252,003,274,489,856,000 elements (about 4.3 × 10^19).

The proof is two rewrites: by the fundamental theorem [reachable_eq_valid](#/node/reachable_eq_valid) the
reachable subgroup *is* the valid one, and [card_valid](#/node/card_valid) counts that. All the work is in
those two results.

This is the order of the Rubik's cube group in the standard model (centres fixed, six outer faces turn).
It counts positions, not the number of moves needed to reach them; nothing about "God's number" is
claimed.

**Status:** complete in the source, axioms pinned upstream (CubingAudit.lean lines 17–19). Not built for
this site.
""",
 [q("How is `card_reachable` proved?", ["By enumerating all positions", "By rewriting with reachable = valid and the count of valid states",
     "By breadth-first search", "It is an axiom"], 1, "Cube3x3/Solvable.lean lines 294–295."),
   q("Does this say anything about how many moves are needed to solve a cube?", ["Yes, at most 20", "No, it only counts positions"], 1,
    "It is a cardinality statement about a subgroup."),
   q("Would the count change if whole-cube rotations were counted as different states?", ["No, never",
     "Yes; this count fixes the centres, which is the standard convention"], 1,
    "The model fixes the centres (Cube3x3/Basic.lean lines 12–18).")],
 caveats=["Complete proof in the source; axioms pinned upstream (CubingAudit.lean lines 17–19). Not built for this site."],
 widgets=[{"type": "walkthrough", "title": "How the proof goes (Cube3x3/Solvable.lean, lines 294-295)",
   "config": {"steps": [
     {"text": "Rewrite reachable as valid, using the fundamental theorem (Cube3x3/Solvable.lean lines 290–291).", "link": "reachable_eq_valid"},
     {"text": "Apply the count of valid states, 43,252,003,274,489,856,000 (Cube3x3/Invariants.lean lines 249–253).", "link": "card_valid"}]}}])

import importlib.util as _u, os as _o
_s = _u.spec_from_file_location("_extra", _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "_extra.py"))
_m = _u.module_from_spec(_s); _s.loader.exec_module(_m); _m.apply(NODES)
