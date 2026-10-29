NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

node("OPerm.SetUp", "Set-up moves",
 "A 'set-up' hypothesis says two things about a subgroup K of states: conjugating by a family L of set-up moves keeps you in K, and L can realise every permutation of the slots.",
 r"""## Plain English

**Definition (`OPerm.SetUp`, Cube3x3/Generate.lean lines 83–88).** For two subgroups K and L of
[OPerm](#/node/OPerm) states, `SetUp K L` holds when

1. for every l in L and k in K, the conjugate l · k · l⁻¹ is again in K ("do a set-up, do the tool, undo
   the set-up"), and
2. every permutation of the slots is the permutation part of some element of L.

This is the formal version of the cuber's commutator-and-conjugate technique: once you can move any
pieces into position, a single tool that affects only a few pieces can be aimed anywhere.

In the cube proof, K is the set of reachable states that touch only corners (or only edges), and L is the
corner part (or edge part) of all reachable states; see `setUp_corners` (Cube3x3/Solvable.lean
lines 200–207) and [cornerSetUps_surj](#/node/cornerSetUps_surj).

Two consequences in Cube3x3/Generate.lean: with full set-ups, the pure twists in K are closed under
relabelling (`OPerm.SetUp.relabel`, lines 93–99, using that conjugating a pure twist just relabels it,
`OPerm.conj_inl`, lines 47–51), and K's permutations include every even permutation once they include one
3-cycle (`OPerm.SetUp.alternating_le`, lines 145–152).
""",
 [q("What does the first condition of `SetUp K L` say?", ["K is finite", "Conjugating anything in K by anything in L stays in K",
     "L is contained in K", "K is abelian"], 1, "Cube3x3/Generate.lean lines 84–85."),
   q("What does the second condition demand of L?", ["That L is the whole group",
     "That every permutation of the slots is the permutation part of some element of L", "That L contains a 3-cycle",
     "That L has no twists"], 1, "Cube3x3/Generate.lean lines 86–87.")])

node("OPerm.pairTwist", "Two-slot twists",
 "The basic orientation tool: twist one slot forward by one and another back by one, leaving the total unchanged.",
 r"""## Plain English

**Definition (`OPerm.pairTwist`, Cube3x3/Generate.lean lines 76–77).** For slots i and j, the
orientation vector that adds +1 at i and −1 at j (and 0 elsewhere). If i = j it is the zero vector.

`OPerm.twists K` (Cube3x3/Generate.lean line 80) is the set of orientation vectors whose *pure twist*
(that twist with the identity permutation) lies in K.

**Key lemma (`OPerm.SetUp.mem_twists`, Cube3x3/Generate.lean lines 111–133).** With full set-up moves
and one two-slot twist in K, every orientation vector with total zero is in `twists K`. First, relabelling
turns one pair twist into every pair twist (`OPerm.SetUp.pairTwist_mem`, lines 102–109, using
`OPerm.exists_perm_pair`, lines 55–65: any two distinct slots can be sent to any other two). Then any
zero-total vector is a product of pair twists: twist each slot a against a fixed slot j₀ the right number
of times; slot j₀ ends up carrying the total, which is zero.

On the cube the corner tool is the sledgehammer-based `twoCornerTwist` and the edge tool `twoEdgeFlip`
(see [twoCornerTwist](#/node/twoCornerTwist)).
""",
 [q("What is the total twist of a pair twist?", ["+1", "−1", "0", "2"], 2, "+1 at one slot and −1 at another (Cube3x3/Generate.lean lines 76–77)."),
   q("In the decomposition of a zero-total vector, why does the fixed slot j₀ come out right?",
    ["It is set by hand", "It absorbs minus the sum of all other twists, and the total is zero", "It is never twisted",
     "Because n = 3"], 1, "Comment in Cube3x3/Generate.lean lines 117–118 and the proof through line 133.")])

node("OPerm.SetUp.le", "The generation lemma",
 "The engine of the hard direction, proved once for any slot type and any number of orientations: with full set-up moves, one 3-cycle and one two-slot twist, a zero-total subgroup contains every state with zero total twist and an even permutation.",
 r"""## Plain English

**Theorem (`OPerm.SetUp.le`, Cube3x3/Generate.lean lines 168–188).** Let K be a subgroup of
[OPerm](#/node/OPerm) states. Suppose

- `SetUp K L` for some L ([set-up moves](#/node/OPerm.SetUp));
- every element of K has total twist zero;
- K contains some state whose permutation is a 3-cycle;
- K contains the pure [two-slot twist](#/node/OPerm.pairTwist) for some pair of distinct slots.

Then every state whose total twist is zero and whose permutation is even lies in K.

In the source docstring (lines 162–167) this is called **the generation lemma**. It is the textbook
argument for solvability, stated abstractly so it can be used twice: once for corners (n = 3) and once for
edges (n = 2).

**Why the zero-total hypothesis on K?** It is used to show that the leftover pure twist has total zero;
for the cube it holds because every reachable state is [valid](#/node/valid).
""",
 [q("Which permutations does the conclusion cover?", ["All permutations", "Even permutations only", "Only 3-cycles", "Only the identity"], 1,
    "The conclusion intersects with the alternating group (Cube3x3/Generate.lean lines 168–171)."),
   q("Why does one 3-cycle give all even permutations?", ["All 3-cycles are conjugate, set-ups realise every conjugator, and 3-cycles generate the even permutations",
     "Because 3 divides 12", "Because the group is abelian", "By computer search"], 0,
    "OPerm.SetUp.alternating_le, Cube3x3/Generate.lean lines 145–152."),
   q("Is this lemma specific to the 3x3x3 cube?", ["Yes, it mentions corners", "No, it holds for any finite slot type and any n with n ≠ 0",
     "It only works for n = 2"], 1, "It is stated in namespace OPerm over a general α and n (Cube3x3/Generate.lean lines 24–26).")],
 widgets=[{"type": "walkthrough", "title": "How the proof goes (Cube3x3/Generate.lean, lines 168-188)",
   "config": {"steps": [
     {"text": "Take x with zero total twist and an even permutation (line 172)."},
     {"text": "All 3-cycles share a cycle type, so they are conjugate; set-ups realise every conjugator, and 3-cycles generate the alternating group. So some k' in K has the same permutation as x (OPerm.SetUp.alternating_le, lines 145–152; used at line 173).", "link": "OPerm.SetUp"},
     {"text": "Then x · k'⁻¹ permutes nothing: it is a pure twist (lines 176–179)."},
     {"text": "Its total is zero, because x has total zero and k' (being in K) does too (lines 180–184)."},
     {"text": "A zero-total pure twist is in K by the pair-twist decomposition (OPerm.SetUp.mem_twists, lines 111–133; used at lines 185–187).", "link": "OPerm.pairTwist"},
     {"text": "So x = (x · k'⁻¹) · k' is in K (line 188)."}]}}])

import importlib.util as _u, os as _o
_s = _u.spec_from_file_location("_extra", _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "_extra.py"))
_m = _u.module_from_spec(_s); _s.loader.exec_module(_m); _m.apply(NODES)
