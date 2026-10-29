NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

node("OPerm.twistSum", "Total twist (as a homomorphism)",
 "Adding up all the twists of a state is a group homomorphism, because a permutation only moves twists between slots and never changes their sum.",
 r"""## Plain English

**`OPerm.total`** (Cube3x3/Invariants.lean lines 40–43) takes an orientation vector and multiplies all
its entries; since the group is written multiplicatively, this is the *sum* of the twists mod n.
Relabelling slots does not change that sum (`OPerm.total_mulAutArrow`, Cube3x3/Invariants.lean lines 46–49).

**`OPerm.twistSum`** (Cube3x3/Invariants.lean lines 55–58) extends this to whole states of
[OPerm](#/node/OPerm), ignoring the permutation, and packages it as a homomorphism using Mathlib's
`SemidirectProduct.lift`. The point of the construction is the compatibility condition: lift requires
that the permutation action does not change the total, which is exactly the relabelling lemma above.
`OPerm.twistSum_apply` (Cube3x3/Invariants.lean lines 61–62) confirms that the value on a state is simply
the product (sum) of its orientation vector.

For corners this is the total corner twist mod 3; for edges, the total edge flip mod 2. A value of
1 in the multiplicative notation means a total of 0.
""",
 [q("Why is total twist a homomorphism (total of a product = product of totals)?",
    ["Because twists are always zero", "Because permuting slots only moves twists around, so it cannot change their sum",
     "Because the group is commutative", "It is assumed as an axiom"], 1,
    "SemidirectProduct.lift needs exactly total_mulAutArrow (Cube3x3/Invariants.lean lines 46–58)."),
   q("In this code, `twistSum g = 1` means:", ["The twists total one", "The twists total zero (mod n)",
     "Only one piece is twisted", "g is the identity"], 1,
    "The orientation group is Multiplicative (ZMod n), so its identity 1 is the additive 0.")])

node("OPerm.parity", "Parity of a state",
 "The parity of a corner or edge state is the sign (+1 even, −1 odd) of its permutation of slots, ignoring twists.",
 r"""## Plain English

**Definition (`OPerm.parity`, Cube3x3/Invariants.lean line 65).** Mathlib's permutation sign composed
with the projection that forgets twists. It is a homomorphism into the units of the integers, the
two-element group {+1, −1}: +1 for an even permutation, −1 for an odd one.

Every face turn moves four corners in a 4-cycle and four edges in a 4-cycle. A 4-cycle is a product
of three swaps, so it is odd: `parity_move_fst` and `parity_move_snd` (Cube3x3/Invariants.lean lines
147–158) give −1 for both, after `cornerPerm_eq` and `edgePerm_eq` (lines 113–144) exhibit each face turn
explicitly as three swaps.
""",
 [q("What is the parity of the corner permutation of a single face turn?", ["+1 (even)", "−1 (odd)",
     "0", "It depends on the face"], 1, "parity_move_fst, Cube3x3/Invariants.lean lines 147–151: a 4-cycle is three swaps."),
   q("Does `OPerm.parity` depend on twists?", ["Yes", "No, only on the permutation of slots"], 1,
    "It is the sign of the right (permutation) component, Cube3x3/Invariants.lean line 65.")])

node("invariants", "The three invariants",
 "The three classical cube invariants are packaged as one homomorphism: the product of the corner and edge parities, the total corner twist mod 3, and the total edge flip mod 2.",
 r"""## Plain English

**Definition (`invariants`, Cube3x3/Invariants.lean lines 79–81).** A group homomorphism from
[Cube](#/node/Cube) to the product of {±1}, the cyclic group of order 3 and the cyclic group of order 2,
sending a state to

1. corner [parity](#/node/OPerm.parity) times edge parity: +1 exactly when the two parities agree;
2. the corner [total twist](#/node/OPerm.twistSum);
3. the edge total flip.

The parities are multiplied rather than recorded separately because, as the file says (lines 71–75),
only their *agreement* is preserved by face turns; each one alone changes with every quarter turn.

These are the three facts a cuber learns from reassembling a cube wrongly (Cube3x3/Invariants.lean
lines 16–27): twists sum to a multiple of 3, flips to a multiple of 2, and the two permutations are both
even or both odd.

The target group has 2 · 3 · 2 = 12 elements, and every one of them is hit
(`invariants_surjective`, Cube3x3/Invariants.lean lines 231–238). That is where the factor 12 in
[card_valid](#/node/card_valid) comes from.
""",
 [q("Why are the corner and edge parities multiplied instead of kept separately?",
    ["To save space", "Because each parity changes with every quarter turn, but their agreement never does",
     "Because edges have no parity", "Because Mathlib requires it"], 1, "Cube3x3/Invariants.lean lines 71–81."),
   q("How many possible values does `invariants` take?", ["3", "6", "12", "24"], 2,
    "2 × 3 × 2, and all occur (invariants_surjective, Cube3x3/Invariants.lean lines 231–238).")])

node("valid", "Valid states",
 "A state is valid when all three invariants are trivial: parities agree, corner twists total 0 mod 3, edge flips total 0 mod 2. Defining it as a kernel makes it a subgroup for free.",
 r"""## Plain English

**Definition (`valid`, Cube3x3/Invariants.lean line 84).** The kernel of [invariants](#/node/invariants).
Because it is a kernel, it is automatically a (normal) subgroup of [Cube](#/node/Cube).

**The readable form** is `mem_valid` (Cube3x3/Invariants.lean lines 88–98): a state is valid exactly when
the corner parity equals the edge parity, the corner twists total zero, and the edge flips total zero.
The only work in the proof is converting "the product of two signs is +1" into "the two signs are equal".

This is the right-hand side of the headline [reachable_eq_valid](#/node/reachable_eq_valid).
""",
 [q("Which of these states is valid?",
    ["One corner twisted in place, everything else solved", "Two edges swapped, everything else solved",
     "Two corners swapped and two edges swapped, everything else solved", "One edge flipped in place"], 2,
    "Two swaps give odd corner parity and odd edge parity, which agree; twists and flips are untouched (mem_valid, Cube3x3/Invariants.lean lines 88–98)."),
   q("Why is `valid` automatically a subgroup?", ["It is defined as the kernel of a homomorphism",
     "Because it is finite", "It is proved by case analysis", "It is not a subgroup"], 0,
    "Cube3x3/Invariants.lean line 84.")])

node("reachable_le_valid", "Every reachable state is valid",
 "The easy direction: each of the six generators keeps all three invariants, so everything they generate does too.",
 r"""## Plain English

**Theorem (`reachable_le_valid`, Cube3x3/Invariants.lean lines 197–200).** [reachable](#/node/reachable)
is contained in [valid](#/node/valid).

Since `valid` is a subgroup, it suffices to show each generator `move f` is valid (`move_mem_valid`,
Cube3x3/Invariants.lean lines 171–173):

- **parities:** both are −1 for every face turn (`parity_move_fst`, `parity_move_snd`, lines 147–158), so they agree;
- **twists and flips:** for each of the six faces the totals are zero, checked by kernel evaluation
  (`twistSum_move_fst`, `twistSum_move_snd`, lines 161–168).

This is half of the headline [reachable_eq_valid](#/node/reachable_eq_valid), and the half every cuber
already knows: you can't twist a single corner by turning faces.
""",
 [q("Why does checking the six generators suffice?", ["Because valid is a subgroup, and a subgroup containing the generators contains everything they generate",
     "Because there are only six reachable states", "Because the cube is abelian", "It does not suffice"], 0,
    "Subgroup.closure_le, Cube3x3/Invariants.lean lines 197–200."),
   q("How are the twist totals of the face turns checked?", ["By hand in comments", "By kernel evaluation over all slots",
     "By native code", "They are assumed"], 1, "decide +kernel, Cube3x3/Invariants.lean lines 161–168.")],
 widgets=[{"type": "walkthrough", "title": "How the proof goes (Cube3x3/Invariants.lean, lines 107-200)",
   "config": {"steps": [
     {"text": "A product of three swaps of distinct neighbouring elements has sign −1 (sign_cycle4, lines 107–110)."},
     {"text": "Each face's corner and edge permutation is written out as three such swaps and checked slot by slot (cornerPerm_eq, edgePerm_eq, lines 113–144).", "link": "move"},
     {"text": "So both parities of every face turn are −1 (lines 147–158), and they agree.", "link": "OPerm.parity"},
     {"text": "The twist and flip totals of each face turn are zero, by kernel evaluation (lines 161–168).", "link": "OPerm.twistSum"},
     {"text": "Hence every face turn is valid (lines 171–173), and the subgroup they generate lies inside the subgroup valid (lines 197–200).", "link": "valid"}]}}])

node("card_cube", "Counting all states",
 "Without any solvability condition there are 3^8 · 8! · 2^12 · 12! cube states, computed from Mathlib's cardinality lemmas for semidirect products, function spaces and permutations.",
 r"""## Plain English

**Theorem (`card_cube`, Cube3x3/Invariants.lean lines 212–219).** The number of elements of
[Cube](#/node/Cube) is 3^8 · 8! · 2^12 · 12! (= 519,024,039,293,878,272,000).

The proof rewrites with Mathlib facts: the size of a product, of a semidirect product (product of the
two factors' sizes), of a function space, and of a permutation group; then uses that there are 8 corners
and 12 edges.
""",
 [q("Which factor counts the ways to flip the edges?", ["3^8", "8!", "2^12", "12!"], 2,
    "Twelve edges, two flips each (Cube3x3/Invariants.lean lines 202–213)."),
   q("Does this count only reachable states?", ["Yes", "No, it counts all states of the model, reachable or not"], 1,
    "card_cube is about the whole group Cube; the reachable count is twelve times smaller.")])

node("card_valid", "Headline: there are 43,252,003,274,489,856,000 valid states",
 "Exactly one twelfth of all arrangements is valid: 43,252,003,274,489,856,000 states. The count comes from group theory (the invariants hit all 12 values), not from enumeration.",
 r"""## Plain English

**Theorem (`card_valid`, Cube3x3/Invariants.lean lines 249–253).** The subgroup [valid](#/node/valid)
has exactly 43,252,003,274,489,856,000 elements.

**How it is counted.**

- [card_cube](#/node/card_cube): all states number 3^8 · 8! · 2^12 · 12!.
- `invariants_surjective` (Cube3x3/Invariants.lean lines 231–238): every one of the 12 combinations of
  invariant values occurs. Witnesses: twist one corner (URF) by any amount, flip one edge (UR) by any amount,
  and optionally swap two corners to make the parities disagree.
- `index_valid` (Cube3x3/Invariants.lean lines 241–246): so the kernel `valid` has index 12, by the
  first isomorphism theorem (index of a kernel = size of the image).
- Size × index = size of the whole group; dividing gives the number. The final arithmetic is done by
  `norm_num` and `omega`.

On its own this is a statement about the subgroup defined by the invariants. Combined with
[reachable_eq_valid](#/node/reachable_eq_valid) it becomes the famous count of reachable positions,
[card_reachable](#/node/card_reachable).

**Status:** complete proof in the file, no `sorry`; its axioms are pinned in CubingAudit.lean
lines 21–23 to the three standard ones. The Lean was not built for this site.
""",
 [q("Where does the factor 1/12 come from?",
    ["From enumerating states by computer", "From the invariants taking all 2·3·2 = 12 values, so their kernel has index 12",
     "From the 12 edges", "From 12 face turns"], 1,
    "invariants_surjective and index_valid, Cube3x3/Invariants.lean lines 231–246."),
   q("Does `card_valid` by itself say anything about reachability?",
    ["Yes, it counts reachable states directly", "No; it counts the states with trivial invariants. Reachability comes from reachable_eq_valid",
     "It shows half of all states are reachable"], 1, "card_reachable (Cube3x3/Solvable.lean lines 294–295) combines the two."),
   q("Is the number computed by listing all states?", ["Yes, with native_decide", "No; it is derived from cardinality lemmas and the index",
     "Yes, by kernel evaluation"], 1, "Cube3x3/Invariants.lean lines 249–253 use valid.card_mul_index and arithmetic.")],
 caveats=["Proof complete in the source (no sorry, no native_decide); the upstream axiom audit (CubingAudit.lean lines 21–23) pins it to propext, Classical.choice and Quot.sound. Not built for this site."],
 widgets=[{"type": "walkthrough", "title": "How the proof goes (Cube3x3/Invariants.lean, lines 212-253)",
   "config": {"steps": [
     {"text": "Count all states: 3^8 · 8! · 2^12 · 12! (card_cube, lines 212–219).", "link": "card_cube"},
     {"text": "Show the invariants take all 12 values, with explicit one-corner-twist / one-edge-flip / two-corner-swap witnesses (invariants_surjective, lines 231–238).", "link": "invariants"},
     {"text": "Index of the kernel = size of the image = 12 (index_valid, lines 241–246).", "link": "valid"},
     {"text": "Use |valid| · 12 = |Cube| and finish the arithmetic with norm_num and omega (lines 249–253)."}]}}])

import importlib.util as _u, os as _o
_s = _u.spec_from_file_location("_extra", _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "_extra.py"))
_m = _u.module_from_spec(_s); _s.loader.exec_module(_m); _m.apply(NODES)
