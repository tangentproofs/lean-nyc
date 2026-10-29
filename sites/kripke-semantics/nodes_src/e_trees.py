NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

node("Beth.BethTrees.BethTree", "Beth trees",
 "A Beth tree is a set of finite sequences that contains the empty sequence, is closed under taking prefixes, and has no dead ends: every node has a child. Its infinite paths are the 'possible futures'.",
 r"""## Plain English

**Definitions (Beth/BethTrees.lean lines 11–77).** Nodes are finite sequences of labels, built by
adding at the end (`SnocList`, lines 11–13), ordered by "is a prefix of" (lines 39–63).

A **Beth tree** over labels α (`BethTree`, lines 73–77) is a predicate picking out which sequences are
nodes, such that:

- the empty sequence (the root) is a node;
- prefixes of nodes are nodes;
- **pruned**: every node has at least one child, so every node lies on an infinite path.

`initial f n` (lines 65–67) is the first n labels of an infinite sequence f. An infinite path through
node l is a sequence f such that l followed by the first n values of f is a node for every n.
Since the tree is pruned, such paths always exist (`IsBar.nonempty`, lines 179–199, builds one by
dependent choice).

These trees, with the [bar coverage](#/node/Beth.BethTrees.BethTreeCoverage), are Beth's original
models.
""",
 [q("What does 'pruned' mean for a Beth tree?",
    ["It is finite", "Every node has at least one child", "Every node has exactly two children", "It has no root"], 1,
    "Beth/BethTrees.lean line 77."),
   q("How is the order on nodes defined?", ["By length", "By 'is a prefix of'", "Alphabetically"], 1,
    "Beth/BethTrees.lean lines 39–63.")])

node("Beth.BethTrees.BethTreeCoverage", "Bars: the coverage on a Beth tree",
 "On a Beth tree, a set of nodes covers node l when it is a bar: every infinite path through l eventually passes through it. The three coverage axioms are proved for bars.",
 r"""## Plain English

**Definition (`IsBar`, Beth/BethTrees.lean lines 82–86).** A set S of sequences is a *bar* at node l
when, for every infinite sequence f whose extensions of l are all nodes, some finite extension of l
along f lies in S.

**Theorem-like definition (`BethTreeCoverage`, lines 211–286).** Taking "the sieve's nodes form a bar"
as the covering relation gives a [coverage](#/node/Beth.Coverage) on the tree's nodes:

- **maximal** (lines 214–218): all futures form a bar; take n = 0;
- **stability** (lines 219–264): a bar at p restricts to a bar at any later q. Proof: given a path from
  q, prefix it with the route from p to q (`le_init`, lines 106–126), find where the bar is hit, and
  split on whether that is before or after q;
- **transitivity** (lines 265–286): follow the path until it hits the first bar U, then continue until
  it hits the bar V there; add the two depths.

This is a substantial piece of bookkeeping with finite sequences (most of BethTrees.lean), and it is
what certifies that classical Beth trees fit the general [Beth frame](#/node/Beth.BethFrame) definition.
""",
 [q("When is S a bar at node l?",
    ["S contains l", "Every infinite path through l eventually meets S", "S is finite", "S contains all children of l"], 1,
    "Beth/BethTrees.lean lines 82–86."),
   q("How is transitivity of bars proved?",
    ["By Zorn's lemma", "Follow the path to the first bar, then on to the second, adding depths", "It is assumed"], 1,
    "Beth/BethTrees.lean lines 265–286.")])

node("Beth.BethTrees.BethTreeFrame", "Every Beth tree with a bar-respecting valuation is a Beth frame",
 "A Beth tree, plus a valuation that is persistent along the tree and holds at a node whenever it holds on a bar there, is an instance of the general Beth frame.",
 r"""## Plain English

**Definitions (`BethVal`, Beth/BethTrees.lean lines 201–204; `BethTreeFrame`, lines 289–305).**
A valuation on a [Beth tree](#/node/Beth.BethTrees.BethTree) says which variables hold at each
sequence, subject to

- persistence: from l to any node extending it;
- the bar condition: if the nodes where variable i holds form a [bar](#/node/Beth.BethTrees.BethTreeCoverage)
  at node l, then i holds at l.

Then the nodes of the tree, with the bar coverage and this valuation, form a [Beth frame](#/node/Beth.BethFrame).
Non-empty covers come from the tree being pruned: a bar at l is hit by some path, so it has a member
(lines 302–305).

So the general theory (and in particular [Beth soundness](#/node/Beth.soundness)) applies to Beth's
original tree models. Completeness for tree models specifically is not stated; the
[completeness theorem](#/node/Beth.Completeness.completeness) uses a different canonical frame.
""",
 [q("Which property of the tree gives non-empty covers?", ["Prefix-closure", "Being pruned (every node has a child)", "Having a root"], 1,
    "Beth/BethTrees.lean lines 302–305 use IsBar.nonempty, which needs pruning."),
   q("Is Beth completeness proved for tree models specifically?", ["Yes", "No, it is proved for the general Beth frames via a canonical frame of contexts"], 1,
    "Beth/Completeness.lean uses a frame of contexts, not a tree.")])

node("Beth.Examples.BinaryBitsTree.binaryBranchVal", "Example: P ∨ Q at the root of the binary tree",
 "On the full binary tree, let P hold at every node below the first left step and Q below the first right step. Then P ∨ Q is Beth-forced at the root, though neither P nor Q holds there.",
 r"""## Plain English

**The model (Beth/Examples.lean lines 52–127).** The full binary tree (`fullBinaryTree`, lines 52–56)
has every finite sequence of Booleans as a node. The valuation (`binaryBranchVal`, lines 90–122):

- variable 0 (P) holds at a node if its first step was *false* ("left");
- variable 1 (Q) holds if its first step was *true* ("right");
- no other variable holds anywhere.

The bar condition (lines 101–122) is checked by following the constant path in the other direction:
a node not below the first left step can be extended forever without ever getting there.

**The example (lines 129–156).** Using the sieve "all nodes below the first left or first right step"
as a cover of the root (it is a bar at depth 1, since every path takes some first step),
P ∨ Q is [Beth-forced](#/node/Beth.at_world) at the root.

At the root itself, neither P nor Q holds. In Kripke semantics (on the same tree as a Kripke frame) the
root would not force P ∨ Q. The docstring says so (Beth/Examples.lean lines 46–49), but the
project does not state or prove that Kripke-side claim.

The example is an anonymous Lean `example`, so it has no name and no node of its own on this site.
""",
 [q("Why is P ∨ Q forced at the root?",
    ["Because P holds at the root", "Because the nodes after one step form a bar, and each of them forces P or forces Q", "By excluded middle"], 1,
    "Beth/Examples.lean lines 129–156."),
   q("Does P hold at the root?", ["Yes", "No: the root has no first step yet"], 1,
    "Beth/Examples.lean line 92: P needs a first step to the left."),
   q("Is the claim that P ∨ Q fails at the root in Kripke semantics proved in Lean?",
    ["Yes", "No, it is only stated in a comment"], 1,
    "Beth/Examples.lean lines 38–50 (docstring); no Kripke-side lemma follows.")])

node("Beth.Examples.bethFrameOfKripke", "Every Kripke frame is a Beth frame",
 "Give a Kripke frame the coverage in which only the maximal sieve covers, and it becomes a Beth frame. This is the 'discrete topology' embedding of Kripke models into Beth models.",
 r"""## Plain English

**Definition (`bethFrameOfKripke`, Beth/Examples.lean lines 21–32).** For any
[Kripke frame](#/node/Kripke.Frame) W, use `maximalSieveCoverage` (Beth/Coverage.lean lines 111–134),
where a sieve covers w only if it is all futures of w. The sheaf condition and non-empty covers hold
because w itself is in that sieve.

In this frame, [Beth forcing](#/node/Beth.at_world) of φ ∨ ψ amounts to "every future forces φ or
ψ", which (by persistence, applied at w itself) is the same as Kripke forcing. So Beth semantics
generalises Kripke semantics.

**Not proved:** a lemma that the two forcing relations agree in this frame is not in the project. Only
the frame instance is given.
""",
 [q("Which sieves cover in the Beth frame of a Kripke frame?",
    ["All sieves", "Only the maximal sieve (all futures)", "Only finite sieves"], 1,
    "Beth/Coverage.lean line 112."),
   q("Does the project prove that Beth and Kripke forcing agree there?", ["Yes", "No, only the instance is constructed"], 1,
    "Beth/Examples.lean lines 21–32 contain only the instance.")])

import importlib.util as _u, os as _o
_s = _u.spec_from_file_location("_extra", _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "_extra.py"))
_m = _u.module_from_spec(_s); _s.loader.exec_module(_m); _m.apply(NODES)
