NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]


node("SimpleGraph.chromaticNumber_le_maxDegree_add_one'",
 "Headline: greedy colouring, χ(G) ≤ Δ(G) + 1",
 "Every finite simple graph can be properly coloured with one more colour than its maximum degree. Colour the vertices one at a time; each vertex has at most Δ already-coloured neighbours, so a free colour is always left. The proof in the source is complete.",
 r"""## Plain English

**Theorem (`chromaticNumber_le_maxDegree_add_one'`, ExpanderGraphs/Coloring.lean lines 90–93).** For a finite
simple graph *G* (Mathlib's `SimpleGraph` on a `Fintype`), the chromatic number is at most the maximum degree plus one:
χ(*G*) ≤ Δ(*G*) + 1.

It is the special case *d* = Δ(*G*) of `chromaticNumber_le_maxDegree_add_one` (lines 83–87): **any** *d* ≥ Δ(*G*)
gives χ(*G*) ≤ *d* + 1.

The chromatic number is the fewest colours that give adjacent vertices different colours. Mathlib's `chromaticNumber`
takes values in ℕ∞ (natural numbers with ∞), and the right-hand side is cast into it.

### The greedy argument

1. [exists_color_not_used](#/node/SimpleGraph.exists_color_not_used): a vertex has at most *d* neighbours, so among
   *d* + 1 colours one is unused by its neighbours.
2. [exists_coloring_on](#/node/SimpleGraph.exists_coloring_on): by induction on a finite set of vertices, add one
   vertex at a time and give it a free colour.
3. Apply step 2 to the set of all vertices and turn the colouring into Mathlib's `Coloring`.

### How this fits the project

This file is separate from the spectral material. It uses Mathlib's `SimpleGraph`, isn't imported by the other files,
and isn't in the blueprint. The bound is tight for complete graphs and odd cycles. Brooks' theorem says those are the
only connected cases where it is.
""",
 [q("For a cycle on 5 vertices (max degree 2), what does the theorem guarantee?",
    ["χ ≤ 3", "χ ≤ 2", "χ = 3"], 0,
    "Δ + 1 = 3. The theorem gives an upper bound only (ExpanderGraphs/Coloring.lean line 92). (C₅ does need 3.)"),
  q("Does the theorem say χ(G) = Δ(G) + 1?", ["No, only ≤", "Yes"], 0,
    "A star with Δ = 10 has χ = 2. The statement is an inequality (line 92)."),
  q("Which graphs does it apply to?",
    ["Finite simple graphs (Mathlib SimpleGraph on a Fintype)", "Multigraphs of the UnweightedGraph type", "Infinite graphs too"], 0,
    "`V : Type u` with `[Fintype V]` and `G : SimpleGraph V` (ExpanderGraphs/Coloring.lean line 31)."),
 ],
 widgets=walk("How the proof goes (ExpanderGraphs/Coloring.lean, lines 61-93)", [
  {"text": "Empty set: any colouring works (line 65).", "link": "SimpleGraph.exists_coloring_on"},
  {"text": "Add a vertex a to an already-coloured set s and find a colour x unused by a's neighbours in s (lines 66–69).", "link": "SimpleGraph.exists_color_not_used",
   "lean": "obtain ⟨x, hx⟩ := exists_color_not_used G hd a s c"},
  {"text": "Recolour a with x and check the four cases of an edge u–v inside s ∪ {a} (lines 70–81)."},
  {"text": "Apply this to all vertices and build a Mathlib Coloring, giving χ ≤ d + 1 (lines 84–88).",
   "lean": "obtain ⟨c, hc⟩ := exists_coloring_on G hd Finset.univ"},
  {"text": "Take d = Δ(G) (lines 91–93).", "lean": "chromaticNumber_le_maxDegree_add_one G le_rfl"},
 ]))


node("SimpleGraph.exists_coloring_on",
 "Greedy colouring of any finite vertex set",
 "Any finite set of vertices can be coloured with d + 1 colours so that adjacent vertices in the set get different colours, provided every degree is at most d.",
 r"""## Plain English

**Lemma (`exists_coloring_on`, ExpanderGraphs/Coloring.lean lines 59–81).** If Δ(*G*) ≤ *d* and *s* is a finite set of
vertices, there is a function *c* from vertices to {0, …, *d*} such that *c*(*u*) ≠ *c*(*v*) whenever *u*, *v* ∈ *s* are
adjacent.

The proof is induction on *s* (Mathlib's `Finset.induction_on`). The insert step recolours only the new vertex *a*, with a
colour from [exists_color_not_used](#/node/SimpleGraph.exists_color_not_used). Because *a* ∉ *s*, the colours of the old
vertices don't change (line 72). The case *u* = *v* = *a* can't happen, because a simple graph has no loops (line 75).
""",
 [q("Why does colouring the new vertex a not spoil the old colouring?",
    ["`Function.update` changes only a's colour, and a is not in s", "Because a has no neighbours"], 0,
    "See `hne` and the `update_of_ne` rewrites (ExpanderGraphs/Coloring.lean lines 70–81)."),
 ])


node("SimpleGraph.exists_color_not_used",
 "A free colour always exists",
 "A vertex of degree at most d has at most d coloured neighbours, so they use at most d of the d + 1 colours, and at least one is free.",
 r"""## Plain English

**Lemma (`exists_color_not_used`, ExpanderGraphs/Coloring.lean lines 33–57).** If Δ(*G*) ≤ *d*, then for any vertex *a*,
set *s* and colouring *c* with *d* + 1 colours, there is a colour *x* that no neighbour of *a* in *s* uses.

It is a pigeonhole count: the set of colours used by *a*'s neighbours in *s* has at most deg(*a*) ≤ *d* < *d* + 1
elements (lines 39–47), so it isn't all of the *d* + 1 colours (lines 49–53).
""",
 [q("Does the free colour depend on the colours of non-neighbours?", ["No; only neighbours of a in s matter", "Yes"], 0,
    "The used-colour set T is the image of the neighbours in s (ExpanderGraphs/Coloring.lean line 39)."),
 ])


EXTRA = {
 "SimpleGraph.exists_coloring_on": [
  q("What is the base case of the induction?", ["The empty set, coloured by the constant colour 0", "A single vertex", "The whole graph"], 0,
    "ExpanderGraphs/Coloring.lean line 65."),
  q("What does the lemma require of the colouring outside s?", ["Nothing", "That it is also proper"], 0,
    "Only pairs u, v ∈ s are constrained (ExpanderGraphs/Coloring.lean line 62)."),
 ],
 "SimpleGraph.exists_color_not_used": [
  q("Why are d + 1 colours enough?", ["At most d colours are used by neighbours, which is fewer than d + 1", "Because the graph is bipartite"], 0,
    "The `hcard` calculation (ExpanderGraphs/Coloring.lean lines 40–47)."),
  q("Which Mathlib quantity bounds the number of neighbours?", ["maxDegree", "chromaticNumber", "card V"], 0,
    "`G.degree_le_maxDegree a` (ExpanderGraphs/Coloring.lean line 44)."),
 ],
}
for n in NODES:
    n["quiz"] += EXTRA.get(n["id"], [])
