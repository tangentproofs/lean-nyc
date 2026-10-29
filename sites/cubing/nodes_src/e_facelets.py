NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

node("Sticker", "The 48 moving stickers",
 "A moving sticker is a piece's slot together with one of its orientations: 8 corners × 3 plus 12 edges × 2 = 48 stickers.",
 r"""## Plain English

**Definition (`Sticker`, Cube3x3/Facelets.lean line 78).** Either a pair (corner slot, orientation mod 3)
or a pair (edge slot, orientation mod 2). That is 24 + 24 = 48 stickers; with the 6 fixed centres this
gives the 54 squares of a real cube.

**How states move stickers** (Cube3x3/Facelets.lean lines 36–50). A state of [OPerm](#/node/OPerm) acts
on (slot, orientation) pairs: the sticker goes to the slot where its piece goes, and its orientation is
shifted by the twist that piece gains (`OPerm.smul_def`, lines 53–54). The file proves this is a genuine
group action, compatible with the product order of [Cube](#/node/Cube), and that it is **faithful**: a
state is determined by where it sends stickers (lines 63–71).
""",
 [q("How many moving stickers are there?", ["20", "48", "54", "60"], 1, "8×3 + 12×2 (Cube3x3/Facelets.lean line 78)."),
   q("What does 'faithful' mean here?", ["Every state is reachable", "Two states that move every sticker the same way are equal",
     "Stickers never move", "The action is commutative"], 1, "Cube3x3/Facelets.lean lines 63–71.")])

node("toStickers", "A cube state as a permutation of stickers",
 "Every cube state gives a permutation of the 48 moving stickers, and this assignment is a group homomorphism.",
 r"""## Plain English

**Definition (`toStickers`, Cube3x3/Facelets.lean lines 81–84).** A homomorphism from [Cube](#/node/Cube)
to the permutations of [Sticker](#/node/Sticker). It lets the corner part act on corner stickers and the
edge part on edge stickers (via Mathlib's `MulAction.toPermHom`), and glues the two with Mathlib's
`Perm.sumCongrHom` (a permutation of each half gives a permutation of the disjoint union).

This is the "cube in the hand" view: 48 coloured squares being shuffled.
""",
 [q("What is the target of `toStickers`?", ["The 54 facelets", "Permutations of the 48 moving stickers", "Colours", "Integers"], 1,
    "Cube3x3/Facelets.lean lines 81–84."),
   q("Is `toStickers` a homomorphism?", ["Yes; doing two states and then converting equals converting each and composing", "No"], 0,
    "It is built as a MonoidHom (Cube3x3/Facelets.lean line 81).")])

node("toStickers_injective", "Headline: the cubie model loses nothing",
 "Different cube states always move the stickers differently, so describing the cube by pieces, slots and twists is exactly as informative as describing it by stickers.",
 r"""## Plain English

**Theorem (`toStickers_injective`, Cube3x3/Facelets.lean lines 87–89).** The map
[toStickers](#/node/toStickers) from cube states to sticker permutations is injective.

So the abstract group [Cube](#/node/Cube) embeds into the permutations of the 48 moving stickers: two
states that act identically on stickers are the same state. This justifies working with pieces and twists
instead of stickers; the headline [reachable_eq_valid](#/node/reachable_eq_valid) loses no information by
doing so.

**What it does not say:** it does not say which sticker permutations come from cube states (most don't;
a single sticker can't move alone), nor anything about colours. Colours are handled by
[colors](#/node/colors).

**Status:** complete in the source, axioms pinned upstream (CubingAudit.lean lines 25–27). Not built for
this site.
""",
 [q("What does injectivity of `toStickers` mean concretely?", ["Every sticker permutation is a cube state",
     "Two different cube states never move all the stickers in the same way", "Stickers determine colours", "Each sticker moves"], 1,
    "Cube3x3/Facelets.lean lines 86–89."),
   q("Does this theorem say every sticker permutation is achievable?", ["Yes", "No, it says nothing of the kind"], 1,
    "Injective, not surjective."),
   q("Why is this a sanity check on the model?", ["It shows the piece-and-twist description loses nothing compared with tracking stickers",
     "It proves the move tables correct", "It counts states"], 0, "Docstring at Cube3x3/Facelets.lean line 86.")],
 caveats=["Complete proof in the source; axioms pinned upstream (CubingAudit.lean lines 25–27). Not built for this site."],
 widgets=[{"type": "walkthrough", "title": "How the proof goes (Cube3x3/Facelets.lean, lines 36-89)",
   "config": {"steps": [
     {"text": "Define how a state moves a (slot, orientation) sticker and check the group-action laws (lines 36–50).", "link": "Sticker"},
     {"text": "Faithfulness: if two states move all stickers alike, looking at orientation-0 stickers recovers the permutation, and then the orientation shifts recover the twists (lines 63–71)."},
     {"text": "So each half (corners, edges) maps injectively into sticker permutations (Mathlib's MulAction.toPerm_injective), the pair of halves does too, and gluing the two halves of a disjoint union is injective (Perm.sumCongrHom_injective). Composing gives the theorem (lines 87–89).", "link": "toStickers"}]}}])

node("Facelet", "The 54 facelets of the net",
 "A facelet is a position on the cube's surface: a centre, or a sticker position of a corner or edge slot; 6 + 24 + 24 = 54.",
 r"""## Plain English

**Definition (`Facelet`, Cube3x3/Facelets.lean lines 101–105).** Three kinds: the centre of a
[Face](#/node/Face), the sticker of corner slot c at orientation k, or the sticker of edge slot e at
orientation k.

Hand-written tables then fix the conventions: each corner's three faces in orientation order
(`cornerStickers`, lines 109–117), each edge's two (`edgeStickers`, lines 120–132), and where each facelet
sits on the familiar unfolded net (`netFacelet`, lines 136–190, following the numbering used by computer
solvers). `cornerFace` and `edgeFace` (lines 193–199) read off the home face of a sticker.

For the 3D view each facelet gets a position (`Facelet.cubie`: the centre of its little cube, a vector in
{−1,0,1}³ obtained by adding the outward normals of the faces it touches; lines 263–266) and a direction
(`Facelet.normal`, lines 269–272). Lean checks, by evaluating all cases, that no two facelets share both
(`Facelet.cubie_normal_injective`, lines 279–281) and that every facelet drawn on a face of the net points
out of that face (`normal_netFacelet`, lines 275–276).
""",
 [q("How many facelets are there?", ["48", "54", "26", "20"], 1, "6 centres + 8×3 + 12×2."),
   q("What does `Facelet.cubie_normal_injective` guarantee?", ["Colours are distinct", "No two facelets have the same position and the same direction",
     "Every facelet moves", "The net is connected"], 1, "Cube3x3/Facelets.lean lines 279–281.")])

node("colors", "Colouring the cube",
 "The colour shown at each facelet is the home face of whichever sticker the state has carried there, and this is proved to agree with the sticker permutation.",
 r"""## Plain English

**Definition (`colors`, Cube3x3/Facelets.lean lines 207–210).** For a [Cube](#/node/Cube) state g and a
[Facelet](#/node/Facelet), the colour (a [Face](#/node/Face)) seen there. A centre shows its own face.
At a corner position (c, k) we look back: which piece came into slot c (apply the inverse permutation), and
which of its stickers is at orientation k after the twist it gained (subtract the twist). The colour is that
sticker's home face. Edges work the same way.

**It is not a separate model.** `colors_corner` and `colors_edge` (lines 225–232) prove the colour at each
position equals the home face of the sticker that [toStickers](#/node/toStickers) carries there. And
`colors_one_net` (lines 235–236) checks that on the solved cube every face of the net is a single colour.

Every cube picture in the upstream book is computed with this function.
""",
 [q("On the solved cube, what does `colors` show on the up face of the net?", ["All six colours", "Only the up colour, at all nine positions",
     "Random colours", "Nothing"], 1, "colors_one_net, Cube3x3/Facelets.lean lines 235–236."),
   q("To find the colour at a corner position, `colors` uses:", ["The forward permutation", "The inverse permutation and the twist, to find which sticker arrived there",
     "Only the twist", "A lookup table of pictures"], 1, "Cube3x3/Facelets.lean lines 207–210.")])

node("Face.turnVec", "Turning a layer in space",
 "Geometry for the 3D picture: a face's layer is the set of facelets one step out along its normal, and a clockwise quarter turn is an explicit rotation of integer vectors.",
 r"""## Plain English

Space is integer 3-vectors (`Vec`, Cube3x3/Facelets.lean line 247) with the usual dot and cross product
(lines 250–254). Each face has an outward unit normal (`Face.normal`, lines 257–260: right is +x, up is +y,
front is +z).

**`Face.layer`** (line 284): a facelet lies on face f's turning layer when the dot product of f's normal
with the facelet's cubie position is 1, i.e. the facelet's little cube is in the outer slab on that side.

**`Face.turnVec`** (line 292): the clockwise quarter turn about f as seen from outside, given by an explicit
formula: take the component along the normal and subtract the cross product of the normal with the vector.
Two small facts: it preserves the distance along the axis, so it maps the layer to itself (`Face.dot_turnVec`,
lines 295–297), and it is injective (`Face.turnVec_injective`, lines 300–302).

For example, for the up face the formula sends the front direction to the left direction, as a clockwise turn
seen from above should.
""",
 [q("When is a facelet on face f's layer?", ["When its colour is f", "When its cubie position has dot product 1 with f's normal",
     "When it is a centre", "Always"], 1, "Cube3x3/Facelets.lean line 284."),
   q("What does `Face.dot_turnVec` show?", ["Turning keeps the coordinate along the axis, so the layer maps to itself",
     "Turning is the identity", "The cube is round"], 0, "Cube3x3/Facelets.lean lines 295–297.")])

node("pull_move", "The move tables agree with geometry",
 "The strongest check on the hand-typed move tables: for every face and every facelet, Lean verifies that the table for a quarter turn moves facelets exactly as the geometric rotation of that layer does.",
 r"""## Plain English

**Theorem (`pull_move`, Cube3x3/Facelets.lean lines 339–343).** For every [Face](#/node/Face) f and every
[Facelet](#/node/Facelet) p:

- if p is on f's layer, then the facelet whose sticker [move](#/node/move) f carries to p (computed from the
  tables by `Facelet.pull`, lines 310–313), once rotated by [Face.turnVec](#/node/Face.turnVec), has p's
  position and p's direction;
- if p is off the layer, the turn brings p's own sticker back to p (nothing moves there).

Proved by brute-force kernel evaluation over all 6 × 54 cases (`decide +kernel`).

**Why it matters.** The permutation and twist tables in Cube3x3/Moves.lean were typed in by hand. This
theorem compares every entry against an independent geometric description (vectors and cross products).
The comparison does lean on the other hand-written tables (`cornerStickers`, `edgeStickers`), so it
checks that the conventions are mutually consistent rather than checking against the physical world
directly; still, a typo in a move table would almost certainly break it.
""",
 [q("How many cases does `pull_move` check?", ["6", "54", "6 faces × 54 facelets", "One general argument"], 2,
    "It reverts f and p and decides, Cube3x3/Facelets.lean lines 339–343."),
   q("What is it a check of?", ["The move tables against the geometric rotation of each layer", "The count of states",
     "That colours are distinct", "Mathlib"], 0, "Docstring, Cube3x3/Facelets.lean lines 337–338.")])

node("colors_move_mul", "Headline: face turns are the rotations they look like",
 "Turning face f after any state g moves the colours on f's layer exactly by the geometric quarter-turn rotation, and leaves every other facelet's colour unchanged. The abstract move tables really are the physical turns.",
 r"""## Plain English

**Theorem (`colors_move_mul`, Cube3x3/Facelets.lean lines 349–359).** For every face f and every state g
(remember `move f * g` means g first, then the turn f):

1. for facelets p and q, if p is on f's layer and the rotation [Face.turnVec](#/node/Face.turnVec) carries
   p's position and direction to q's, then after the turn the colour at q is the colour that was at p;
2. if p is not on f's layer, its colour is unchanged by the turn.

In plain terms: the turn picks up the colours of one layer and rotates them a quarter turn in space,
and nothing else changes. This is the bridge between the abstract group of the headline
[reachable_eq_valid](#/node/reachable_eq_valid) and a real cube's colours. The upstream book's 3D viewer
rotates layers by exactly this rotation.

**Status:** complete in the source, axioms pinned upstream (CubingAudit.lean lines 41–43). Not built
for this site.
""",
 [q("Which facelets change colour when face f is turned?", ["All of them", "Only facelets on f's layer", "Only centres", "None"], 1,
    "Part 2 of the statement, Cube3x3/Facelets.lean line 352."),
   q("In `move f * g`, what happens first?", ["The turn f", "The state g", "They commute"], 1,
    "Products do the right factor first (Cube3x3/Basic.lean lines 88–96)."),
   q("What role does this theorem play?", ["It counts states", "It ties the abstract move tables to actual geometric rotations of coloured stickers",
     "It proves solvability", "It defines the moves"], 1, "Docstring, Cube3x3/Facelets.lean lines 345–348.")],
 caveats=["Complete proof in the source; axioms pinned upstream (CubingAudit.lean lines 41–43). Not built for this site.",
          "The geometry (positions, normals, the turn formula) and the sticker-order tables are themselves definitions written by the author; the theorem shows they and the move tables agree, which is strong evidence but not a proof about physical cubes."],
 widgets=[{"type": "walkthrough", "title": "How the proof goes (Cube3x3/Facelets.lean, lines 349-359)",
   "config": {"steps": [
     {"text": "Colours compose: after g then h, each position shows the colour g left on the facelet that h pulls there (colors_mul, lines 317–325).", "link": "colors"},
     {"text": "Off the layer: pull_move says the turn pulls p from itself, so the colour is unchanged (line 353).", "link": "pull_move"},
     {"text": "On the layer: q is on the layer too, since the rotation preserves the axis coordinate (Face.dot_turnVec; lines 354–356).", "link": "Face.turnVec"},
     {"text": "pull_move says rotating the facelet pulled to q gives q's position and direction; so does rotating p. The rotation is injective (lines 300–302), so the pulled facelet and p have the same position and direction (lines 357–359)."},
     {"text": "Facelets are determined by position and direction (Facelet.cubie_normal_injective, lines 279–281), so the pulled facelet is p, and the colour at q is g's colour at p (lines 358–359).", "link": "Facelet"}]}}])

import importlib.util as _u, os as _o
_s = _u.spec_from_file_location("_extra", _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "_extra.py"))
_m = _u.module_from_spec(_s); _s.loader.exec_module(_m); _m.apply(NODES)
