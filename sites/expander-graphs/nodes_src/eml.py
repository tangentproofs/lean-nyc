NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]


# ---------------------------------------------------------------- headline: the mixing lemma

node("expander_mixing_lemma",
 "Headline: the expander mixing lemma",
 "In a connected d-regular γ-expander, the number of edges between any two vertex sets A and B is within γ·d·√(|A|·|B|) of (d/n)·|A|·|B|, which is the number you would expect from a random d-regular graph. The proof in the source is complete, with no sorry.",
 r"""## Plain English

**Theorem (`expander_mixing_lemma`, ExpanderGraphs/EML.lean lines 318–388).** Take:

- a finite simple graph *G* on a vertex type *V* (Mathlib's `SimpleGraph`), with *n* = |*V*| vertices;
- a whole number *d* ≥ 1 such that every vertex has exactly *d* neighbours (*G* is *d*-regular);
- the assumption that *G* is **connected**;
- a number γ ≥ 0 such that *G* is a [γ-expander](#/node/expander): every eigenvalue of the
  [normalised adjacency matrix](#/node/norm_adj_matrix) *M* = *A*/*d*, other than 1, has absolute value at most γ.

Then for **any** two sets of vertices *A* and *B* (they may overlap):

| [e(A, B)](#/node/e_AB) − (d/n)·|A|·|B| | ≤ γ · d · √(|A|·|B|).

Here e(*A*, *B*) counts ordered pairs (*a*, *b*) with *a* in *A*, *b* in *B* and *a*, *b* adjacent.

### Why you should care

If you choose *A* and *B* and then pick a random *d*-regular graph, each of the |*A*|·|*B*| pairs is joined with
probability about *d*/*n*, so you expect about (*d*/*n*)·|*A*|·|*B*| edges between them. The lemma says that a
good expander (small γ) behaves like that for **every** choice of *A* and *B*, not just on average. It is the
standard way of saying "expanders look random", and it is used all over pseudorandomness and complexity theory.

The file follows Swastik Kopparty's lecture notes (Rutgers, 2018; scribes Danny Scheinerman and Harsha Tirumala),
as its header says (ExpanderGraphs/EML.lean lines 33–36).

### The idea of the proof

Write the indicator vectors 𝟙_A and 𝟙_B in an orthonormal basis of [eigenvectors](#/node/eigvec) of *M*. Then

1. e(*A*, *B*) = *d* · ⟨𝟙_A, *M* 𝟙_B⟩ ([e_AB_eq_dotProduct](#/node/e_AB_eq_dotProduct)), and that inner product is
   Σᵢ λᵢ αᵢ βᵢ, where αᵢ and βᵢ are the coordinates of 𝟙_A and 𝟙_B
   ([dotProduct_mulVec_eq_sum](#/node/dotProduct_mulVec_eq_sum)).
2. Exactly one index carries the eigenvalue 1 ([eigval_eq_one_unique](#/node/eigval_eq_one_unique)), and its
   eigenvector is the constant vector with value *c*, where *n c*² = 1. That one term is exactly (*d*/*n*)·|*A*|·|*B*|.
3. Every other term has |λᵢ| ≤ γ. Cauchy–Schwarz and Parseval
   ([sum_sq_inner_eq](#/node/sum_sq_inner_eq)) bound what is left by γ·√|*A*|·√|*B*|.

A nice touch: instead of writing the top eigenvector as 𝟙/√*n*, the proof only uses "it is a constant *c* with
*n c*² = 1", so it never has to pick a square root or a sign (ExpanderGraphs/EML.lean lines 167–169).
""",
 [q("Which sets A and B does the lemma apply to?",
    ["Every pair of vertex sets, including overlapping ones", "Only disjoint sets", "Only sets of size at most n/2", "Only A = B"], 0,
    "A and B are arbitrary sets of vertices (ExpanderGraphs/EML.lean line 253); nothing requires them to be disjoint. The blueprint says “possibly overlapping”."),
  q("What does the main term (d/n)·|A|·|B| represent?",
    ["The expected number of A–B pairs joined by an edge in a random d-regular graph",
     "The number of edges inside A", "The number of edges of G", "An upper bound on e(A, B) in every graph"], 0,
    "Each of the |A|·|B| pairs is an edge with probability about d/n in a random d-regular graph. The docstring says this at ExpanderGraphs/EML.lean line 323."),
  q("Which of these is a hypothesis of the Lean theorem?",
    ["G is connected", "A and B are disjoint", "γ < 1", "G is bipartite"], 0,
    "`hconn : G.Connected` is included (ExpanderGraphs/EML.lean lines 316–318). It is needed so that the eigenvalue 1 is simple; see the expander node."),
  q("If γ ≥ 1, what does the lemma tell you?",
    ["Something true but weak: the error bound is at least d·√(|A||B|)", "Nothing, because it then assumes something false",
     "That e(A, B) = (d/n)|A||B| exactly"], 0,
    "The statement only asks γ ≥ 0 (line 324). Large γ makes the bound weak, not false."),
  q("How is e(A, B) counted?",
    ["As ordered pairs (a, b) with a ∈ A, b ∈ B and a adjacent to b, so an edge inside A ∩ B counts twice",
     "As unordered edges with one end in A and one in B, each counted once",
     "As the number of vertices of B adjacent to A"], 0,
    "See `e_AB` (ExpanderGraphs/EML.lean lines 258–259), which filters pairs `p : V × V`."),
 ],
 caveats=["Here “γ-expander” is about the normalised adjacency matrix A/d and excludes every eigenvalue equal to 1. Connectivity makes that exactly one eigenvalue. Some texts define λ as the second-largest absolute eigenvalue instead; this is the same thing for connected graphs.",
          "The statement writes n as `Fintype.card V`. The file also declares an `n` with `n = Nat.card V` and `Fact (1 ≤ n)` (line 49), but the theorem's statement does not use them.",
          "Not built for this site: “complete” means the proof text has no `sorry` and no gaps that we could see."],
 widgets=walk("How the proof goes (ExpanderGraphs/EML.lean, lines 318-388)", [
  {"text": "G is connected (Mathlib's SimpleGraph.Connected), so V is nonempty and n ≠ 0 (lines 327–328)."},
  {"text": "Pick an index i₀ whose eigenvalue is 1 (line 330), using that constants are 1-eigenvectors.", "link": "exists_eigval_eq_one",
   "lean": "obtain ⟨i₀, hi₀⟩ := exists_eigval_eq_one G d h_reg"},
  {"text": "Its eigenvector is a nonzero constant c, and normalisation gives n·c² = 1 (lines 331–332).", "link": "eigvec_const_of_eigval_eq_one"},
  {"text": "Rewrite e(A,B) as d·Σᵢ λᵢ αᵢ βᵢ (lines 334–336).", "link": "e_AB_eq_dotProduct",
   "lean": "rw [e_AB_eq_dotProduct G d h_reg, dotProduct_mulVec_eq_sum]"},
  {"text": "The i₀ term equals (d/n)|A||B|, because αᵢ₀ = c|A|, βᵢ₀ = c|B| and n c² = 1 (lines 338–342).", "link": "inner_eigvec_ind"},
  {"text": "Every other index has eigenvalue ≠ 1, by simplicity of 1, so |λᵢ| ≤ γ (lines 344–345).", "link": "eigval_eq_one_unique"},
  {"text": "Bound the remaining sum: triangle inequality, |λᵢ| ≤ γ, Cauchy–Schwarz, then Parseval for 𝟙_A and 𝟙_B (lines 347–380).", "link": "sum_sq_inner_eq",
   "lean": "mul_le_mul_of_nonneg_left (Real.sum_mul_le_sqrt_mul_sqrt _ _ _) hγ"},
  {"text": "Split off the i₀ term, cancel it against the main term and multiply the tail bound by d (lines 382–388)."},
 ]))


# ---------------------------------------------------------------- headline: simplicity of eigenvalue 1

node("eigval_eq_one_unique",
 "Headline: the eigenvalue 1 is simple",
 "On a connected d-regular graph, only one vector of the eigenbasis of M = A/d has eigenvalue 1. The reason is that every 1-eigenvector is constant, and two nonzero constant vectors can't be orthogonal.",
 r"""## Plain English

**Lemma (`eigval_eq_one_unique`, ExpanderGraphs/EML.lean lines 192–208).** Let *G* be a connected, *d*-regular
simple graph (*d* ≥ 1), and fix the orthonormal [eigenbasis](#/node/eigvec) of the
[normalised adjacency matrix](#/node/norm_adj_matrix) *M* that Mathlib's spectral theorem provides, indexed by the
vertices. If two indices *i* and *j* both have [eigenvalue](#/node/eigval) 1, then *i* = *j*.

In linear-algebra terms, the eigenvalue 1 has multiplicity one, and its eigenspace is the line of constant vectors.

### Why it matters

The [definition of a γ-expander](#/node/expander) excludes *every* index whose eigenvalue is 1. Without this
lemma, a graph could have the eigenvalue 1 several times, and the definition would quietly ignore all of them.
That happens exactly for disconnected graphs: each connected component gives its own constant-on-the-component
eigenvector. So this lemma is what makes "γ-expander" mean what it should, and the
[mixing lemma](#/node/expander_mixing_lemma) uses it to say that *all* other terms are small.

### Why it is true

- [eq_const_of_mulVec_eq](#/node/eq_const_of_mulVec_eq): on a connected regular graph every 1-eigenvector is
  constant (a maximum principle).
- [eigvec_const_of_eigval_eq_one](#/node/eigvec_const_of_eigval_eq_one): so the eigenbasis vectors at *i* and *j*
  are constants *a* and *b*, both nonzero, because they have length 1.
- Their inner product is *n*·*a*·*b*, which is not 0. But distinct vectors of an orthonormal basis have inner
  product 0. That is a contradiction, so *i* = *j*.
""",
 [q("What exactly does the lemma conclude?",
    ["Two eigenbasis indices with eigenvalue 1 must be the same index",
     "The largest eigenvalue of M is 1", "All other eigenvalues are strictly less than 1 in absolute value",
     "The eigenvalue 1 exists"], 0,
    "The conclusion is `i = j` from `eigval G d i = 1` and `eigval G d j = 1` (ExpanderGraphs/EML.lean line 195). Existence is a separate lemma, `exists_eigval_eq_one`."),
  q("Which hypothesis would you lose the lemma without?",
    ["Connectivity: a graph with two components has two independent 1-eigenvectors",
     "Finiteness of the vertex type is not needed",
     "d ≥ 1 is not needed"], 0,
    "Connectivity (`hconn`) is what makes every 1-eigenvector globally constant (ExpanderGraphs/EML.lean lines 126–132)."),
  q("Does the lemma say that −1 is not an eigenvalue?",
    ["No. A bipartite regular graph has eigenvalue −1, and the lemma says nothing about it",
     "Yes, it rules out ±1 together"], 0,
    "It only talks about the value 1. A γ-expander with γ < 1 must also avoid −1, but that comes from the `expander` hypothesis, not from this lemma."),
 ],
 caveats=["“The eigenvalue is simple” is stated about Mathlib's chosen eigenbasis, indexed by the vertex type, which is equivalent to multiplicity one."],
 widgets=walk("How the proof goes (ExpanderGraphs/EML.lean, lines 192-208)", [
  {"text": "Suppose i ≠ j (line 196)."},
  {"text": "Both eigenvectors are nonzero constants a and b (lines 197–198).", "link": "eigvec_const_of_eigval_eq_one",
   "lean": "obtain ⟨a, ha0, ha⟩ := eigvec_const_of_eigval_eq_one G d h_reg hconn hi"},
  {"text": "Orthonormality gives ⟨vᵢ, vⱼ⟩ = 0 (line 199).", "link": "eigvec",
   "lean": "have h0 : ⟪eigvec G d i, eigvec G d j⟫ = 0 := (eigvec G d).orthonormal.2 hij"},
  {"text": "Unfold the inner product of two constant vectors to n·(b·a) (lines 200–204)."},
  {"text": "n ≠ 0 because the connected graph has a vertex, so n·b·a ≠ 0: contradiction (lines 205–208)."},
 ]))


node("eq_const_of_mulVec_eq",
 "Every 1-eigenvector is constant (maximum principle)",
 "On a connected regular graph, a vector fixed by M = A/d is constant. At a vertex where it is largest, its value is the average of its neighbours' values, so they are all equally large, and that spreads along every walk.",
 r"""## Plain English

**Theorem (`eq_const_of_mulVec_eq`, ExpanderGraphs/EML.lean lines 123–132).** If *G* is connected and *d*-regular
(*d* ≥ 1) and *f* is a function on the vertices with *M f* = *f* for the
[normalised adjacency matrix](#/node/norm_adj_matrix), then *f* is constant.

This is a discrete version of the **maximum principle** for harmonic functions. *M f* = *f* says that *f*(*v*) is the
average of *f* over the *d* neighbours of *v* (`sum_neighbors_eq_of_mulVec_eq`, lines 86–95).

### The argument, in three small lemmas

1. **Mean value** (lines 86–95): Σ over neighbours *u* of *v* of *f*(*u*) = *d*·*f*(*v*).
2. **One step** (`eq_of_adj_of_isMax`, lines 97–112): if *f* ≤ *m* everywhere and *f*(*v*) = *m*, then every
   neighbour *u* also has *f*(*u*) = *m*. The differences *m* − *f*(*u*) are all ≥ 0 and add up to *d m* − *d f*(*v*) = 0,
   so each one is 0.
3. **Along walks** (`eq_of_walk_of_isMax`, lines 114–121): by induction on a walk, the maximum value spreads to the
   walk's end.

Then pick a vertex *v*₀ where *f* is largest (a finite nonempty set has a maximum), and walk from *v*₀ to any *w*:
*f*(*w*) = *f*(*v*₀).
""",
 [q("Where does connectivity enter the proof?",
    ["To get a walk from the maximising vertex to every other vertex", "To make M symmetric", "To show d ≥ 1"], 0,
    "`hconn.preconnected v₀ w` provides the walk (ExpanderGraphs/EML.lean line 131)."),
  q("Why is the neighbouring value forced to equal the maximum m?",
    ["Non-negative differences m − f(u) that sum to zero must all be zero",
     "Because f is linear", "Because M is a projection"], 0,
    "See ExpanderGraphs/EML.lean lines 105–112, using `Finset.sum_eq_zero_iff_of_nonneg`."),
  q("Does the theorem need f to be nonzero?",
    ["No: the zero function is constant too, so it is included", "Yes, otherwise the statement is false"], 0,
    "The hypothesis is just M f = f (line 127); the zero vector satisfies it and is constant."),
 ],
 widgets=walk("How the proof goes (ExpanderGraphs/EML.lean, lines 123-132)", [
  {"text": "Connected graphs have a vertex, so V is nonempty (line 128)."},
  {"text": "f attains a maximum at some v₀ (line 129).", "lean": "obtain ⟨v₀, hv₀⟩ := Finite.exists_max f"},
  {"text": "Take the constant to be f v₀ and fix an arbitrary vertex w (line 130)."},
  {"text": "Get a (Mathlib) walk from v₀ to w and push the maximum along it (lines 131–132).",
   "lean": "exact eq_of_walk_of_isMax h_reg hf hv₀ p rfl"},
 ]))


node("eigvec_const_of_eigval_eq_one",
 "The eigenvector for eigenvalue 1 is a nonzero constant",
 "At any eigenbasis index whose eigenvalue is 1, the eigenvector is a constant c with c ≠ 0. In fact n·c² = 1, because the vector has length 1.",
 r"""## Plain English

**Lemma (`eigvec_const_of_eigval_eq_one`, ExpanderGraphs/EML.lean lines 180–190).** On a connected *d*-regular graph,
if [eigval](#/node/eigval) *i* = 1 then the [eigenbasis](#/node/eigvec) vector at *i* is a constant *c* with *c* ≠ 0.

- Constancy is [eq_const_of_mulVec_eq](#/node/eq_const_of_mulVec_eq) applied to that eigenvector.
- `card_mul_sq_eq_one` (lines 167–178) says a constant unit vector with value *c* has *n*·*c*² = 1, so *c* = 0 is
  impossible.

The mixing lemma uses *n*·*c*² = 1 to turn the top term into exactly (*d*/*n*)·|*A*|·|*B*|.
""",
 [q("Why can't the constant c be 0?",
    ["The eigenbasis vector has length 1, and n·c² = 1", "Because eigenvalue 1 is positive", "Because d ≥ 1"], 0,
    "ExpanderGraphs/EML.lean lines 186–190 plug c = 0 into `card_mul_sq_eq_one` and get 0 = 1."),
  q("Does this lemma say which index i has eigenvalue 1?",
    ["No; it assumes one is given. `exists_eigval_eq_one` shows one exists", "Yes, it is always the first vertex"], 0,
    "The index is a hypothesis `hi` (line 182). Mathlib's eigenvalue order is not used here."),
 ])


# ---------------------------------------------------------------- definitions

node("norm_adj_matrix",
 "The normalised adjacency matrix M = A/d",
 "M is the adjacency matrix divided by d. For a d-regular graph it is the transition matrix of the random walk: applying M to a function replaces each value by the average over the neighbours.",
 r"""## Plain English

**Definition (`norm_adj_matrix`, ExpanderGraphs/EML.lean lines 54–56).** For a simple graph *G* and a number *d*,
*M* = (1/*d*)·*A*, where *A* is Mathlib's adjacency matrix (`SimpleGraph.adjMatrix`): *A*(*u*, *v*) = 1 if *u* and *v* are
adjacent, and 0 otherwise.

The definition itself works for any *d*, but it is only meaningful when *G* is *d*-regular and *d* ≥ 1. The file
assumes this everywhere through `h_reg` and `Fact (1 ≤ d)` (line 50).

### Facts proved about it

- **Symmetric** (`norm_adj_matrix_isHermitian`, lines 58–62), so the spectral theorem gives real
  [eigenvalues](#/node/eigval) and an orthonormal [eigenbasis](#/node/eigvec).
- **Constants are fixed** (`norm_adj_matrix_mulVec_const`, lines 64–74): each vertex has *d* neighbours, so
  averaging a constant gives the same constant. Hence 1 is an eigenvalue (`exists_eigval_eq_one`, lines 151–163).

For a *d*-regular graph all eigenvalues of *M* lie in [−1, 1]. The docstring mentions this (line 55), but the file
does not prove it, and the mixing lemma doesn't need it.
""",
 [q("What is M(u, v) when u and v are adjacent in a 4-regular graph (with d = 4)?",
    ["1/4", "1", "−1/4", "4"], 0, "M = d⁻¹ • A (ExpanderGraphs/EML.lean line 56) and A(u, v) = 1."),
  q("Which property of M does the file prove?",
    ["It is symmetric (Hermitian)", "All its eigenvalues lie in [−1, 1]", "It is invertible"], 0,
    "Symmetry is `norm_adj_matrix_isHermitian` (lines 58–62). The [−1, 1] claim is only in a comment."),
 ])


node("eigval",
 "The eigenvalues of M",
 "eigval G d i is the i-th eigenvalue of M, in Mathlib's spectral theorem's indexing by vertices. No order is assumed: “the top eigenvalue” is found by its value 1, not by its position.",
 r"""## Plain English

**Definition (`eigval`, ExpanderGraphs/EML.lean lines 140–141).** Because [M](#/node/norm_adj_matrix) is symmetric,
Mathlib's spectral theorem (`Matrix.IsHermitian.eigenvalues`) gives one real eigenvalue for each element of the index
type, here the vertex type *V*, counted with multiplicity. `eigval G d i` is the one at index *i*.

The matching eigenvectors are [eigvec](#/node/eigvec), and `mulVec_eigvec` (lines 147–149) records
*M* vᵢ = λᵢ vᵢ.

The indexing has no meaning in the graph: index *i* is a vertex only because Mathlib uses the matrix's row
type for the eigenbasis. The project never assumes the eigenvalues are sorted. It refers to "the eigenvalue 1" by
value and uses [eigval_eq_one_unique](#/node/eigval_eq_one_unique) to know it appears once.
""",
 [q("Is eigval G d i related to the vertex i in any graph-theoretic way?",
    ["No; the vertex type is just used as an index set for the n eigenvalues", "Yes, it is the degree of i divided by d",
     "Yes, it is the largest eigenvalue of the neighbourhood of i"], 0,
    "The index set of Mathlib's eigenbasis is the matrix's row type (ExpanderGraphs/EML.lean lines 140–145)."),
 ])


node("eigvec",
 "An orthonormal eigenbasis of M",
 "eigvec G d is the orthonormal basis of eigenvectors that Mathlib's spectral theorem gives for the symmetric matrix M. Writing indicator vectors in this basis is how the mixing lemma is proved.",
 r"""## Plain English

**Definition (`eigvec`, ExpanderGraphs/EML.lean lines 143–145).** A fixed orthonormal basis v₁, …, vₙ of ℝⁿ
(Mathlib's `EuclideanSpace ℝ V`) consisting of eigenvectors of [M](#/node/norm_adj_matrix), with
*M* vᵢ = [eigval](#/node/eigval)ᵢ · vᵢ (lines 147–149).

Two identities about it drive the mixing lemma:

- [dotProduct_mulVec_eq_sum](#/node/dotProduct_mulVec_eq_sum): ⟨*x*, *M y*⟩ = Σᵢ λᵢ ⟨vᵢ, *x*⟩ ⟨vᵢ, *y*⟩;
- [sum_sq_inner_eq](#/node/sum_sq_inner_eq) (Parseval): Σᵢ ⟨vᵢ, *x*⟩² = ⟨*x*, *x*⟩.
""",
 [q("What does “orthonormal” give the proof of eigval_eq_one_unique?",
    ["Distinct basis vectors have inner product 0, and each has length 1", "That all eigenvalues are distinct",
     "That the vectors are constant"], 0,
    "Both facts are used, at ExpanderGraphs/EML.lean line 199 and lines 172–174."),
 ])


node("expander",
 "What “γ-expander” means here",
 "G is a γ-expander when every eigenvalue of M = A/d that is not equal to 1 has absolute value at most γ. On a connected regular graph this leaves out exactly one eigenvalue, the trivial one.",
 r"""## Plain English

**Definition (`expander`, ExpanderGraphs/EML.lean lines 210–215).** For a real number γ, `expander G d γ` means: for
every eigenbasis index *i*, if [eigval](#/node/eigval) *i* ≠ 1 then |eigval *i*| ≤ γ.

So the condition looks at **all** eigenvalues of the [normalised adjacency matrix](#/node/norm_adj_matrix) except
those equal to 1, and asks that they lie in [−γ, γ]. Small γ means a good expander: random walks mix fast and edges
are spread evenly, which is what the [mixing lemma](#/node/expander_mixing_lemma) makes precise.

### A subtlety handled correctly

The definition excludes eigenvalues *by value*. If the eigenvalue 1 occurred twice, both copies would be excluded,
and the condition would be too weak. The project deals with this by assuming connectivity wherever the definition is
used and proving that the eigenvalue 1 then occurs exactly once
([eigval_eq_one_unique](#/node/eigval_eq_one_unique)). The docstring says so (lines 213–214).

### Things to notice

- The **negative** end counts too: a bipartite *d*-regular graph has eigenvalue −1, so it is a γ-expander only for
  γ ≥ 1. This is the "two-sided" notion of expansion.
- The definition doesn't require γ < 1 and doesn't mention connectivity. Those assumptions sit in the theorems that
  use it.
""",
 [q("Does `expander G d γ` constrain eigenvalues equal to 1?",
    ["No, they are explicitly excluded", "Yes, they must be at most γ"], 0,
    "The condition is `eigval G d i ≠ 1 → |eigval G d i| ≤ γ` (ExpanderGraphs/EML.lean line 215)."),
  q("A connected 3-regular bipartite graph: what is the smallest γ for which it is a γ-expander?",
    ["At least 1, because −1 is an eigenvalue", "Possibly much less than 1",
     "0, since bipartite graphs have only eigenvalues 0 and 1"], 0,
    "Bipartite regular graphs have eigenvalue −1 for M. The definition takes absolute values (line 215)."),
  q("Why does the project need connectivity alongside this definition?",
    ["So that the excluded value 1 occurs only once and no nontrivial eigenvalue is ignored",
     "Because the definition is false for disconnected graphs", "To make M symmetric"], 0,
    "See the docstring at ExpanderGraphs/EML.lean lines 210–214 and the lemma `eigval_eq_one_unique`."),
 ])


node("e_AB",
 "e(A, B): edges between two vertex sets",
 "e(A, B) counts ordered pairs (a, b) with a in A, b in B and a adjacent to b. When A and B overlap, an edge with both ends in A ∩ B is counted twice, once in each direction.",
 r"""## Plain English

**Definition (`e_AB`, ExpanderGraphs/EML.lean lines 258–259).** The number of pairs (*a*, *b*) in *V* × *V* with
*a* ∈ *A*, *b* ∈ *B* and *a* adjacent to *b*.

This is the standard count for the mixing lemma, and the one that makes the formula clean:
e(*A*, *B*) = Σᵢⱼ 𝟙_A(*i*)·𝟙_B(*j*)·*A*ᵢⱼ (`e_AB_eq_sum_indicators`, lines 261–272) = 𝟙_Aᵀ *A* 𝟙_B.

Examples:

- *A* and *B* disjoint: e(*A*, *B*) is the number of edges between them.
- *A* = *B* = *S*: e(*S*, *S*) is twice the number of edges inside *S*.
- *A* = *B* = all vertices of a *d*-regular graph: e = *n d*.

The blueprint's wording, "edges (a, b) ∈ E(G)", is consistent with this ordered-pair count.
""",
 [q("In a triangle (3 vertices, 3 edges), what is e(V, V)?", ["6", "3", "9"], 0,
    "Each edge gives two ordered pairs, so 6 (ExpanderGraphs/EML.lean line 259)."),
  q("What is e(A, B) if A and B are disjoint and no edge joins them?", ["0", "|A|·|B|", "It is undefined"], 0,
    "No pair (a, b) passes the adjacency filter."),
 ])


# ---------------------------------------------------------------- key proof lemmas

node("e_AB_eq_dotProduct",
 "e(A, B) = d · ⟨𝟙_A, M 𝟙_B⟩",
 "Counting edges between A and B is the same as d times the inner product of 1_A with M applied to 1_B. This turns a combinatorial count into linear algebra.",
 r"""## Plain English

**Lemma (`e_AB_eq_dotProduct`, ExpanderGraphs/EML.lean lines 289–302).** For a *d*-regular graph (*d* ≥ 1),
[e(A, B)](#/node/e_AB) = *d* · (𝟙_A · (*M* 𝟙_B)), where 𝟙_S is the 0/1 indicator vector of *S* (`indicator` and
`ind`, lines 255–256 and 274–276).

The proof writes e(*A*, *B*) as a double sum of indicator products against the adjacency matrix (lines 261–272),
then cancels *d* against the 1/*d* inside [M](#/node/norm_adj_matrix).
""",
 [q("Does this identity use regularity in an essential way?",
    ["No; the proof only needs d ≠ 0 to cancel d against 1/d", "Yes, it is false for non-regular graphs whatever d is"], 0,
    "`h_reg` is included, but the proof only uses `d ≠ 0`, which comes from `Fact (1 ≤ d)` (ExpanderGraphs/EML.lean line 293). The identity e = 𝟙_Aᵀ A 𝟙_B holds for any graph."),
 ])


node("dotProduct_mulVec_eq_sum",
 "⟨x, M y⟩ = Σ λᵢ αᵢ βᵢ in the eigenbasis",
 "In the eigenbasis of M, the quadratic form ⟨x, M y⟩ becomes the sum over i of λᵢ times the i-th coordinates of x and y. That separates the top eigenvalue's term from the rest.",
 r"""## Plain English

**Lemma (`dotProduct_mulVec_eq_sum`, ExpanderGraphs/EML.lean lines 231–241).** For vectors *x*, *y*,
*x* · (*M y*) = Σᵢ λᵢ · ⟨vᵢ, *x*⟩ · ⟨vᵢ, *y*⟩, where vᵢ is the [eigenbasis](#/node/eigvec) and λᵢ the
[eigenvalues](#/node/eigval).

It comes from `mulVec_eq_sum_eigvec` (lines 222–229): write *y* = Σ ⟨vᵢ, *y*⟩ vᵢ, apply *M* term by term, and take
the inner product with *x*.

With *x* = 𝟙_A and *y* = 𝟙_B, this is step 1 of the [mixing lemma](#/node/expander_mixing_lemma).
""",
 [q("Does this lemma need G to be regular or connected?",
    ["No; it is just the spectral theorem for the symmetric matrix M", "Yes, both"], 0,
    "No `include h_reg` or `hconn` precedes it (ExpanderGraphs/EML.lean lines 231–234)."),
 ])


node("sum_sq_inner_eq",
 "Parseval: the coordinates keep the length",
 "The squares of a vector's coordinates in an orthonormal basis add up to its squared length. For an indicator vector 1_A that is |A|.",
 r"""## Plain English

**Lemma (`sum_sq_inner_eq`, ExpanderGraphs/EML.lean lines 243–249).** For any *x*, Σᵢ ⟨vᵢ, *x*⟩² = *x* · *x*, where
vᵢ is the [eigenbasis](#/node/eigvec). It is a restatement of Mathlib's
`OrthonormalBasis.sum_sq_norm_inner_right`.

Specialised to an indicator (`sum_sq_inner_ind`, lines 312–314, with `dotProduct_ind_self`, lines 283–287):
Σᵢ ⟨vᵢ, 𝟙_A⟩² = |*A*|, because 𝟙_A · 𝟙_A counts the elements of *A*.

In the [mixing lemma](#/node/expander_mixing_lemma), dropping the top term from this sum can only make it smaller,
which gives the bounds hA' and hB' (lines 350–361).
""",
 [q("Why is 𝟙_A · 𝟙_A = |A|?", ["Each entry is 0 or 1, and 1·1 = 1", "Because A is nonempty", "By Cauchy–Schwarz"], 0,
    "See `dotProduct_ind_self`, ExpanderGraphs/EML.lean lines 283–287."),
 ])


node("exists_eigval_eq_one",
 "1 is an eigenvalue of M",
 "For a d-regular graph with at least one vertex, 1 is one of the eigenvalues of M, with the all-ones vector as an eigenvector.",
 r"""## Plain English

**Lemma (`exists_eigval_eq_one`, ExpanderGraphs/EML.lean lines 151–163).** If *G* is *d*-regular and *V* is nonempty,
some index *i* has [eigval](#/node/eigval) *i* = 1.

The proof shows that 1 is in the spectrum of [M](#/node/norm_adj_matrix), because the all-ones function is a nonzero
fixed vector (lines 154–161). Then it uses Mathlib's fact that the spectrum of a Hermitian matrix is the set of its
eigenvalues (line 162).
""",
 [q("Which vector witnesses the eigenvalue 1?", ["The all-ones vector", "The indicator of one vertex", "The zero vector"], 0,
    "`Function.const V 1` (ExpanderGraphs/EML.lean line 157)."),
 ])


node("inner_eigvec_ind",
 "The top coordinate of 1_A is c·|A|",
 "If an eigenvector is the constant c, then the coordinate of the indicator 1_A along it is c times the size of A.",
 r"""## Plain English

**Lemma (`inner_eigvec_ind`, ExpanderGraphs/EML.lean lines 304–310).** If [eigvec](#/node/eigvec) *i* is the constant
function *c*, then ⟨vᵢ, 𝟙_A⟩ = *c*·|*A*|. Summing *c*·𝟙_A(*v*) over all *v* gives *c* times the number of elements of *A*.

This is the informal proof's α₁ = |*A*|/√*n*, without the square root.
""",
 [q("What would this coordinate be if c = 1/√n?", ["|A|/√n", "|A|", "√|A|"], 0,
    "c·|A| with c = 1/√n. The file avoids the square root by keeping c abstract with n c² = 1 (ExpanderGraphs/EML.lean lines 167–178)."),
 ])


node("ind",
 "Indicator vectors 𝟙_S",
 "𝟙_S is the vector that is 1 on the vertices of S and 0 elsewhere, viewed in Euclidean space so that it can be expanded in the eigenbasis.",
 r"""## Plain English

**Definitions (`indicator`, ExpanderGraphs/EML.lean lines 255–256; `ind`, lines 274–276).** `indicator S` is the
function *v* ↦ 1 if *v* ∈ *S*, else 0. `ind S` is the same function, packaged as an element of `EuclideanSpace ℝ V`, so
that inner products with the [eigenbasis](#/node/eigvec) make sense. `ofLp_ind` (line 278) says unpacking gives back
`indicator S`.

Facts used in the [mixing lemma](#/node/expander_mixing_lemma):

- Σᵥ 𝟙_S(*v*) = |*S*| (`sum_indicator`, lines 280–281);
- 𝟙_S · 𝟙_S = |*S*| (`dotProduct_ind_self`, lines 283–287).
""",
 [q("What is 𝟙_S · 𝟙_S?", ["|S|", "|S|²", "1"], 0, "Each entry is 0 or 1 and squares to itself (ExpanderGraphs/EML.lean lines 283–287)."),
  q("Why have two versions, indicator and ind?", ["`ind` lives in EuclideanSpace, which carries the inner product the eigenbasis needs", "They are different functions"], 0,
    "Mathlib's `OrthonormalBasis` works in `EuclideanSpace ℝ V` (ExpanderGraphs/EML.lean lines 274–276)."),
  q("What is Σᵥ 𝟙_S(v)?", ["The number of elements of S", "The number of edges in S", "vol S"], 0, "`sum_indicator`, ExpanderGraphs/EML.lean lines 280–281."),
 ])


# ---------------------------------------------------------------- extra quiz questions (schema needs ≥ 3 per node)

EXTRA = {
 "eigvec_const_of_eigval_eq_one": [
  q("Which hypothesis makes the eigenvector constant?",
    ["Connectivity, through the maximum principle eq_const_of_mulVec_eq", "That the eigenbasis is orthonormal", "That d ≥ 1 alone"], 0,
    "Line 185 applies `eq_const_of_mulVec_eq h_reg hconn`."),
 ],
 "norm_adj_matrix": [
  q("For a d-regular graph, what does M do to a function f on the vertices?",
    ["(M f)(v) is the average of f over the d neighbours of v", "(M f)(v) is the sum of f over all vertices",
     "(M f)(v) = d · f(v)"], 0,
    "(A f)(v) is the sum over neighbours, and dividing by d gives the average (ExpanderGraphs/EML.lean lines 54–55)."),
 ],
 "eigval": [
  q("How many eigenvalues does eigval list?", ["n = |V|, counted with multiplicity", "Only the distinct ones", "d of them"], 0,
    "One per index i : V (ExpanderGraphs/EML.lean line 141)."),
  q("Are the eigenvalues of M real?", ["Yes, because M is symmetric", "Not necessarily"], 0,
    "`eigval` is ℝ-valued and comes from `norm_adj_matrix_isHermitian` (lines 58–62 and 141)."),
 ],
 "eigvec": [
  q("What equation does each eigvec i satisfy?", ["M vᵢ = eigval i · vᵢ", "M vᵢ = vᵢ", "vᵢ is constant"], 0,
    "`mulVec_eigvec`, ExpanderGraphs/EML.lean lines 147–149."),
  q("Is the eigenbasis unique?", ["No; Mathlib picks one fixed basis, and the proofs work for that choice", "Yes, eigenvectors are unique"], 0,
    "The docstring says “A fixed orthonormal basis” (ExpanderGraphs/EML.lean line 143). Only its properties are used."),
 ],
 "e_AB": [
  q("For a d-regular graph, what is e(V, V)?", ["n·d", "n·d/2", "d"], 0,
    "Each of the n vertices has d neighbours, giving n·d ordered pairs."),
 ],
 "e_AB_eq_dotProduct": [
  q("What is 𝟙_A?", ["The vector that is 1 on A and 0 elsewhere", "The all-ones vector", "The adjacency matrix restricted to A"], 0,
    "`indicator`, ExpanderGraphs/EML.lean lines 255–256."),
  q("Where is this identity used?", ["In the first step of the mixing lemma (the `key` step)", "To prove eigenvalue 1 is simple"], 0,
    "ExpanderGraphs/EML.lean lines 334–336."),
 ],
 "dotProduct_mulVec_eq_sum": [
  q("In the mixing lemma, which single term of this sum gives the main term (d/n)|A||B|?",
    ["The term for the eigenvalue-1 index i₀", "The term with the largest |λᵢ|", "All terms equally"], 0,
    "`hmain`, ExpanderGraphs/EML.lean lines 338–342."),
  q("What are ⟨vᵢ, x⟩?", ["The coordinates of x in the eigenbasis", "The eigenvalues", "The entries of x"], 0,
    "`mulVec_eq_sum_eigvec` expands y with these coefficients (ExpanderGraphs/EML.lean lines 222–229)."),
 ],
 "sum_sq_inner_eq": [
  q("Why can the mixing lemma drop the top term and still use Parseval?",
    ["Every term is a square ≥ 0, so a partial sum is at most the full sum", "Because the top term is 0"], 0,
    "`Finset.sum_le_sum_of_subset_of_nonneg` (ExpanderGraphs/EML.lean lines 354–355)."),
  q("Does Parseval need the basis to be orthonormal?", ["Yes", "No, any basis works"], 0,
    "It is a property of orthonormal bases (`OrthonormalBasis.sum_sq_norm_inner_right`, line 246)."),
 ],
 "exists_eigval_eq_one": [
  q("Does this lemma need connectivity?", ["No, only d-regularity and a nonempty vertex set", "Yes"], 0,
    "Only `include h_reg` and `[Nonempty V]` (ExpanderGraphs/EML.lean lines 151–153)."),
  q("Does it say the eigenvalue 1 occurs only once?", ["No; that is eigval_eq_one_unique", "Yes"], 0,
    "This lemma is existence only (line 153)."),
 ],
 "inner_eigvec_ind": [
  q("Which hypothesis does this lemma need about the eigenvector?", ["That it is a constant function c", "That its eigenvalue is 1", "Nothing"], 0,
    "`hc : ⇑(eigvec G d i) = Function.const V c` (ExpanderGraphs/EML.lean line 306)."),
  q("In the mixing lemma, the product of the top coordinates of 1_A and 1_B is…", ["c²·|A|·|B| = |A|·|B|/n", "|A|·|B|", "0"], 0,
    "Using n c² = 1 (ExpanderGraphs/EML.lean lines 338–342)."),
 ],
}
for n in NODES:
    n["quiz"] += EXTRA.get(n["id"], [])
