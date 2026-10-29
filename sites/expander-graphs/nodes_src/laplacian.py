NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]

# Note: the engine only links file names that start with a capital letter, so references to
# ExpanderGraphs/chapter1.lean and ExpanderGraphs/chapter2.lean stay plain text (see NOTES.md).


# ---------------------------------------------------------------- the graph model

node("UnweightedGraph",
 "UnweightedGraph: a multigraph with an orientation",
 "The Fan Chung chapters use their own graph type: Mathlib's general Graph α β (vertices of type α, edges of type β, loops and parallel edges allowed) plus a chosen orientation for each edge. It is not Mathlib's SimpleGraph, which the mixing lemma uses.",
 r"""## Plain English

**Structure (`UnweightedGraph`, ExpanderGraphs/chapter1.lean lines 36–37).** An `UnweightedGraph α β` is a Mathlib
`Graph α β` together with a function `orientation : β → α`.

Mathlib's `Graph α β` is a **multigraph**: it has a set of vertices (inside the type α), a set of edges (inside the type β),
and a relation `IsLink e x y` saying that edge *e* joins *x* and *y*. Loops (*x* = *y*) and several edges between the
same two vertices are allowed. Two vertices are adjacent (`Adj x y`) when some edge links them.

The extra `orientation` picks one endpoint of each edge. It is only used for the boundary matrix `S` (lines 238–245),
whose columns carry a +1/√d at one end of the edge and −1/√d at the other. Nothing forces `orientation e` to be an
endpoint of *e*.

### Standing assumptions

The files mostly work with finite types (`Fintype α`, `Fintype β`) and declare two optional hypotheses (lines 42–43):
`hα`, "every element of α is a vertex", and `hβ`, "every element of β is an edge". A lemma uses them only when it
says so with `include`. Several results also assume [IsSimple](#/node/UnweightedGraph.IsSimple) (no parallel edges)
and "no loops", as explicit arguments.

### Why two graph types?

The [mixing lemma](#/node/expander_mixing_lemma) (ExpanderGraphs/EML.lean) and the
[colouring bound](#/node/SimpleGraph.chromaticNumber_le_maxDegree_add_one') use Mathlib's `SimpleGraph`. The Chung
chapters use this multigraph type, because Chung's book allows loops and weights. There is also a separate
`WeightedGraph` (ExpanderGraphs/WeightedGraph.lean lines 35–36) with an edge-weight function and its own Laplacian,
but nothing else in the project uses it yet.
""",
 [q("Can an UnweightedGraph have two different edges between the same pair of vertices?",
    ["Yes; it is built on Mathlib's multigraph type `Graph α β`", "No, adjacency is a simple relation"], 0,
    "`Graph α β` has an edge type β and an `IsLink` relation, so parallel edges are possible (ExpanderGraphs/chapter1.lean line 36). `IsSimple` is a separate hypothesis."),
  q("What is `orientation` used for?",
    ["Choosing the sign at each end of an edge in the boundary matrix S", "Making the graph directed for walks",
     "Nothing at all"], 0,
    "It appears only in `S` (ExpanderGraphs/chapter1.lean lines 242–245). Adjacency and walks ignore it."),
  q("Is the mixing lemma stated for UnweightedGraph?",
    ["No; it uses Mathlib's SimpleGraph", "Yes"], 0,
    "ExpanderGraphs/EML.lean line 48 has `G : SimpleGraph V`. The two parts of the project don't share a graph type yet."),
 ])


node("UnweightedGraph.degree",
 "Degree: the number of incident edges",
 "The degree of v is the number of edges that touch v, as a non-negative real. A loop counts once here, while in Chung's book it would count twice. Isolated vertices have degree 0.",
 r"""## Plain English

**Definition (`degree`, ExpanderGraphs/chapter1.lean lines 50–52).** `G.degree v` is the number of elements of
`G.incidenceSet v`, the set of edges *e* with *v* as an endpoint. It is a non-negative real number (`ℝ≥0`), which makes
the square roots and divisions in the [Laplacian](#/node/UnweightedGraph.Laplacian) easier to write.

Related definitions in the same file:

- `IsRegularOfDegree k` (lines 55–56): every vertex has degree *k*.
- [vol](#/node/UnweightedGraph.vol) *S* (lines 63–64): the sum of the degrees in *S*. `graphVolume` (lines 59–60) is
  the same for all of α.
- `IsIsolated v` (lines 67–68): degree 0. `NoIsolation` (lines 216–217): no vertex of `G.vertexSet` is isolated.
- `no_adj_iff_zero_degree` (lines 71–92, proved): degree 0 ⇔ no vertex is adjacent to *v*.

### Loops and parallel edges

Because this counts *edges*, a vertex with two parallel edges to the same neighbour has degree 2 but only one
neighbour. [IsSimple](#/node/UnweightedGraph.IsSimple) is the hypothesis that rules this out. A loop at *v* is one
incident edge, so it adds 1 to the degree. Chung's convention for loops differs, but the theorems here that matter
assume no loops anyway.
""",
 [q("A vertex has a loop and one ordinary edge. What is its degree here?", ["2", "3", "1"], 0,
    "Both edges are in the incidence set, so the count is 2 (ExpanderGraphs/chapter1.lean lines 51–52)."),
  q("Why is the degree a non-negative real rather than a natural number?",
    ["To make the √ and division in the Laplacian convenient", "Because degrees can be fractional"], 0,
    "It is the natural-number count cast to ℝ≥0 (line 52). Weighted degrees live in the separate WeightedGraph file."),
 ])


node("UnweightedGraph.IsSimple",
 "IsSimple: no parallel edges",
 "IsSimple says each vertex's degree equals its number of neighbours, so no two edges join the same pair of vertices. Several spectral results assume it, together with a separate “no loops” hypothesis.",
 r"""## Plain English

**Definition (`IsSimple`, ExpanderGraphs/chapter1.lean lines 143–144).** For every vertex *u*,
[degree](#/node/UnweightedGraph.degree) *u* = the number of vertices *v* with *u* adjacent to *v*.

If two edges joined *u* to the same neighbour, the degree would be bigger than the number of neighbours, so
`IsSimple` rules out parallel edges. Its docstring says "No multiple loops".

Loops are handled by a separate hypothesis, `∀ v, ¬ G.Adj v v`, which the theorems pass as `hLoopless`.
""",
 [q("Does IsSimple on its own forbid a loop at u?",
    ["No; that is what the separate `hLoopless` hypothesis is for",
     "Yes, it forbids loops and parallel edges"], 0,
    "A single loop at u adds 1 to the degree and makes u its own neighbour, so the counts can still match. The theorems that need it also assume `∀ v, ¬ G.Adj v v`."),
 ])


node("UnweightedGraph.Laplacian",
 "The normalised Laplacian ℒ",
 "ℒ has 1 on the diagonal (0 for isolated vertices) and −1/√(d_u·d_v) where u and v are adjacent. It equals T^(−1/2)·(D − A)·T^(−1/2). Its eigenvalues measure how well connected the graph is, and they are the subject of Chung's book.",
 r"""## Plain English

**Definition (`Laplacian`, ExpanderGraphs/chapter1.lean lines 111–115).** The matrix ℒ indexed by α × α with

- ℒ(*v*, *v*) = 1 if *d*ᵥ ≠ 0, and 0 if *v* is isolated;
- ℒ(*u*, *v*) = −1/√(*d*ᵤ *d*ᵥ) if *u* ≠ *v* and *u*, *v* are adjacent;
- ℒ(*u*, *v*) = 0 otherwise.

Here *d* is the [degree](#/node/UnweightedGraph.degree). This is Fan Chung's **normalised Laplacian**. One adjacent
pair contributes a single −1/√(*d*ᵤ *d*ᵥ) entry however many parallel edges join them, which is one reason
[IsSimple](#/node/UnweightedGraph.IsSimple) appears in the theorems.

### Proved facts about ℒ

- **ℒ = T^(−1/2) · L · T^(−1/2)** (`Lap_symmetric_normalization`, lines 126–133), where *L* (lines 104–108) is the
  combinatorial Laplacian (degrees on the diagonal, −1 for adjacent pairs) and T^(−1/2) (lines 122–123) is the
  diagonal matrix of 1/√*d*ᵥ, with 0 for isolated vertices.
- **For a loopless *k*-regular graph, ℒ = I − (1/*k*)·A** (`LapOfRegGraph`, lines 203–213). So ℒ is the identity minus
  the [normalised adjacency matrix](#/node/norm_adj_matrix) of the mixing-lemma file, and its eigenvalues are 1 − λ.
  The two files don't connect this yet: they use different graph types.
- **No isolated vertices ⇒ ℒ = I − T^(−1/2) A T^(−1/2)** (`LapOfNotIsolatedGraph`, lines 221–230).
- **ℒ as an operator** (`LapOperatorFormula`, lines 147–192): for a simple loopless graph,
  (ℒ*g*)(*u*) = (1/√*d*ᵤ) Σ over neighbours *v* of (*g*(*u*)/√*d*ᵤ − *g*(*v*)/√*d*ᵥ), which is Chung's formula on her page 3.
- **ℒ is symmetric** ([LapHermitian](#/node/UnweightedGraph.LapHermitian)), so it has real eigenvalues.

### Not yet proved

- `LSS` (lines 248–249): ℒ = *S Sᵀ* for the boundary matrix *S*, stated with `sorry`. As stated it has no simplicity
  hypothesis. With parallel edges, *S Sᵀ* would count each one, so we think the statement needs `IsSimple` to be true.
""",
 [q("What is ℒ(v, v) for an isolated vertex v?", ["0", "1", "−1"], 0,
    "The diagonal entry is `if G.degree v = 0 then 0 else 1` (ExpanderGraphs/chapter1.lean line 113)."),
  q("For a loopless 3-regular graph, what is ℒ(u, v) for adjacent u ≠ v?", ["−1/3", "−1", "1/3", "−1/9"], 0,
    "−1/√(3·3) = −1/3, matching ℒ = I − (1/3)A (`LapOfRegGraph`, lines 203–213)."),
  q("Which of these is proved in the source without sorry?",
    ["ℒ = T^(−1/2) L T^(−1/2)", "ℒ = S Sᵀ", "Both"], 0,
    "`Lap_symmetric_normalization` has a full proof (lines 126–133). `LSS` is `:= sorry` (line 249)."),
 ],
 caveats=["“ℒ = S Sᵀ needs IsSimple” is our reading of the definitions of S and ℒ, not something checked in Lean."])


node("UnweightedGraph.T_sqrt",
 "T^(1/2) and the all-ones vector τ",
 "T^(1/2) is the diagonal matrix of square roots of degrees, and τ is the all-ones vector. Their product (√d_v)ᵥ is the vector that ℒ sends to zero.",
 r"""## Plain English

**Definitions (`T_sqrt`, ExpanderGraphs/chapter1.lean lines 118–119; `τ`, lines 305–306).** T^(1/2) is the diagonal
matrix with √*d*ᵥ in position (*v*, *v*). τ is the constant function 1. So T^(1/2) τ is the vector whose *v*-entry is
√*d*ᵥ.

In Chung's book, T is the diagonal degree matrix. The [Laplacian](#/node/UnweightedGraph.Laplacian) kills
T^(1/2)·𝟙 ([zero_eigenvalue_normalized](#/node/UnweightedGraph.zero_eigenvalue_normalized)), which is why 0 is
always an eigenvalue.
""",
 [q("What is the v-entry of T^(1/2) τ?", ["√(degree v)", "degree v", "1"], 0,
    "Diagonal entries √(d_v) times the constant 1 (ExpanderGraphs/chapter1.lean lines 118–119 and 306)."),
 ])


node("UnweightedGraph.LapHermitian",
 "ℒ is symmetric",
 "The normalised Laplacian is a real symmetric (Hermitian) matrix, so the spectral theorem gives it real eigenvalues. This is the gateway to all the spectral statements.",
 r"""## Plain English

**Lemma (`LapHermitian`, ExpanderGraphs/chapter1.lean lines 258–269).** ℒ(*u*, *v*) = ℒ(*v*, *u*) for all *u*, *v*.
This needs adjacency to be symmetric (Mathlib's `Graph.adj_comm`) and *d*ᵤ *d*ᵥ = *d*ᵥ *d*ᵤ.

Mathlib then provides the eigenvalues, which [lapEigvals](#/node/UnweightedGraph.lapEigvals) puts in increasing order.
""",
 [q("Why is ℒ symmetric?",
    ["Adjacency is symmetric and the entry −1/√(d_u d_v) is symmetric in u and v", "Because the graph is regular",
     "It is only symmetric for simple graphs"], 0,
    "The proof swaps the factors of the product and uses `Graph.adj_comm` (ExpanderGraphs/chapter1.lean lines 264–269). It needs no simplicity hypothesis."),
 ])


node("UnweightedGraph.lapSpectrum",
 "The spectrum of ℒ",
 "lapSpectrum is the set of real numbers λ for which ℒ − λI is not invertible, which for a matrix is the set of its eigenvalues.",
 r"""## Plain English

**Definition (`lapSpectrum`, ExpanderGraphs/chapter1.lean lines 300–302).** Mathlib's `spectrum ℝ ℒ`: the λ such that
λ·I − ℒ has no inverse. For a matrix that is the set of eigenvalues, without multiplicities. The ordered list with
multiplicities is [lapEigvals](#/node/UnweightedGraph.lapEigvals).

[zero_mem_lapSpectrum](#/node/UnweightedGraph.zero_mem_lapSpectrum) shows that 0 is in it.
""",
 [q("Does lapSpectrum record how many times an eigenvalue occurs?",
    ["No, it is a set", "Yes, it is a list with repetitions"], 0,
    "`spectrum ℝ G.Laplacian` is a `Set ℝ` (ExpanderGraphs/chapter1.lean lines 301–302)."),
 ])


node("UnweightedGraph.zero_eigenvalue_normalized",
 "ℒ sends the vector (√d_v) to zero",
 "For a simple loopless graph, ℒ applied to the vector with entries √(degree v) gives 0. The vector is nonzero whenever the graph has an edge, so 0 is an eigenvalue.",
 r"""## Plain English

**Theorem (`zero_eigenvalue_normalized`, ExpanderGraphs/chapter1.lean lines 328–355).** If *G* is
[simple](#/node/UnweightedGraph.IsSimple) and has no loops, then ℒ · ([T^(1/2)](#/node/UnweightedGraph.T_sqrt) τ) = 0.

At a vertex *v* with *d*ᵥ ≠ 0, the entry is √*d*ᵥ minus the sum over the *d*ᵥ neighbours *u* of
√*d*ᵤ/√(*d*ᵤ *d*ᵥ) = 1/√*d*ᵥ, which is √*d*ᵥ − *d*ᵥ/√*d*ᵥ = 0. Simplicity is what makes "number of neighbours = *d*ᵥ"
true. At an isolated vertex the whole row is zero.

If the graph has no edges, T^(1/2) τ is the zero vector and the statement is trivially true. The
[next headline](#/node/UnweightedGraph.zero_mem_lapSpectrum) handles that case separately.
""",
 [q("Where is IsSimple used?",
    ["To know that v has exactly d_v neighbours, so the sum of d_v copies of 1/√d_v is √d_v",
     "To make ℒ symmetric", "To rule out isolated vertices"], 0,
    "The final step rewrites with `card_of_adj_loopless`, which is IsSimple (ExpanderGraphs/chapter1.lean lines 310–312 and 353–355)."),
  q("Does this theorem alone show that 0 is an eigenvalue for every graph?",
    ["No; when the graph has no edges, the vector is zero and is not an eigenvector", "Yes"], 0,
    "An eigenvector must be nonzero. The edgeless case needs a separate argument, which `zero_mem_lapSpectrum` supplies."),
 ])


node("UnweightedGraph.zero_mem_lapSpectrum",
 "Headline: 0 is always an eigenvalue of ℒ",
 "For any simple loopless graph with at least one vertex, 0 is in the spectrum of the normalised Laplacian. This is the first basic fact in Chung's chapter 1, and its proof in the source is complete.",
 r"""## Plain English

**Lemma (`zero_mem_lapSpectrum`, ExpanderGraphs/chapter1.lean lines 411–438).** Let *G* be an
[UnweightedGraph](#/node/UnweightedGraph) on a finite nonempty vertex type, [simple](#/node/UnweightedGraph.IsSimple)
and without loops. Then 0 ∈ [lapSpectrum](#/node/UnweightedGraph.lapSpectrum), i.e. the
[normalised Laplacian](#/node/UnweightedGraph.Laplacian) ℒ is not invertible.

In Chung's notation, λ₀ = 0. The usual eigenvector is T^(1/2)𝟙, the vector (√*d*ᵥ)ᵥ.

### The argument

The proof argues by contradiction and covers the edgeless case without a separate case split:

1. Suppose ℒ is invertible.
2. We know ℒ · (√*d*ᵥ)ᵥ = 0 ([zero_eigenvalue_normalized](#/node/UnweightedGraph.zero_eigenvalue_normalized)).
   Multiplying by the inverse gives (√*d*ᵥ)ᵥ = 0, so every degree is 0.
3. But then every entry of ℒ is 0, so ℒ is the zero matrix, which is not invertible on a nonempty index set.
   Contradiction.

### What it doesn't say

- It doesn't say how many times 0 occurs. Chung's "0 has multiplicity equal to the number of connected components" is
  not in the project.
- It is about the set `spectrum`. The ordered-list version "`lapEigvals 0 = 0`" is a separate lemma,
  `first_eigval_eq_0` (lines 441–444), which is still `sorry`.
""",
 [q("Which hypotheses does the lemma use?",
    ["A nonempty vertex type, IsSimple and no loops", "Connectivity and regularity", "No isolated vertices"], 0,
    "`[Nonempty α] (hS : G.IsSimple) (hLoopless : ∀ v, ¬ G.Adj v v)` (ExpanderGraphs/chapter1.lean line 412)."),
  q("Does the lemma hold for a graph with vertices but no edges?",
    ["Yes: then ℒ is the zero matrix, and 0 is its only eigenvalue", "No, it needs at least one edge"], 0,
    "The proof's contradiction case shows exactly this: all degrees 0 makes ℒ = 0 (lines 428–438)."),
  q("Does it show that 0 is the smallest eigenvalue?",
    ["No; it only shows 0 is an eigenvalue. That ℒ has no negative eigenvalues isn't proved here",
     "Yes, that is what “first” means"], 0,
    "The conclusion is `0 ∈ G.lapSpectrum` (line 413). `first_eigval_eq_0` (line 443), about the smallest one, is sorry'd."),
  q("Why is the edgeless case not a problem for the proof?",
    ["If ℒ were invertible, all degrees would be 0, which makes ℒ = 0, which isn't invertible",
     "The lemma assumes at least one edge", "Lean treats the zero vector as an eigenvector"], 0,
    "See ExpanderGraphs/chapter1.lean lines 428–438."),
 ],
 caveats=["Labelled “complete” because the proof text has no sorry and uses only `zero_eigenvalue_normalized` and `adj_degree_neq_zero`, which are also complete. Not built for this site."],
 widgets=walk("How the proof goes (ExpanderGraphs/chapter1.lean, lines 411-438)", [
  {"text": "Unfold the spectrum: 0 is in it unless 0·I − ℒ = −ℒ is a unit (lines 414–416)."},
  {"text": "Suppose −ℒ is a unit; then ℒ is a unit (lines 417–420)."},
  {"text": "ℒ kills T^(1/2)τ (line 421).", "link": "UnweightedGraph.zero_eigenvalue_normalized",
   "lean": "have h_ker := zero_eigenvalue_normalized hS hLoopless"},
  {"text": "Apply a left inverse B: T^(1/2)τ = 0 (lines 422–427)."},
  {"text": "Read off each entry: √(d_v) = 0, so every degree is 0 (lines 428–431).", "link": "UnweightedGraph.degree"},
  {"text": "With all degrees 0, every entry of ℒ is 0 (lines 432–436).", "link": "UnweightedGraph.Laplacian"},
  {"text": "The zero matrix is not a unit: contradiction (lines 437–438).",
   "lean": "exact not_isUnit_zero h_unit_L"},
 ]))


node("UnweightedGraph.lapEigvals",
 "The eigenvalues λ₀ ≤ λ₁ ≤ … of ℒ",
 "lapEigvals lists the n eigenvalues of ℒ, with multiplicity, in increasing order, so lapEigvals 0 is the smallest and lapEigvals 1 is Chung's λ₁. The docstring says “non-increasing”, but the proved lemma eigval_order shows the order is increasing.",
 r"""## Plain English

**Definition (`lapEigvals`, ExpanderGraphs/chapter1.lean lines 272–274).** Mathlib's `eigenvalues₀` lists the
eigenvalues of a Hermitian matrix in decreasing order. `lapEigvals i` reads that list backwards (`i.rev`), so
λ₀ ≤ λ₁ ≤ … ≤ λₙ₋₁. `eigval_order` (lines 366–371) proves exactly this.

So `lapEigvals 1` is Chung's λ₁, the second-smallest eigenvalue. It is the one that measures connectivity and is
compared to the [Cheeger constant](#/node/UnweightedGraph.Isoperimetry.cheeger).

### Proved facts

- `lapEigvals_sum_eq_trace` (lines 378–386): the eigenvalues add up to the trace of ℒ.
- `eigval_sum_le_n` (lines 389–396): that sum is at most *n*, because each diagonal entry is 0 or 1.
- `eigval_sum_eq_n_iff_no_isolation` (lines 399–408): if no vertex is isolated, the sum is exactly *n*. Despite the
  name, only this direction is proved.

### Unfinished (sorry)

- `first_eigval_eq_0` (lines 441–444): λ₀ = 0.
- `second_eigval_le_div` (lines 447–452): λ₁ ≤ *n*/(*n* − 1).
- [lapEigvals_one_eq_inf_rayleigh](#/node/UnweightedGraph.lapEigvals_one_eq_inf_rayleigh): λ₁ as a minimum of
  Rayleigh quotients.

### A quirk with "0" and "1"

From line 361 on, the file *assumes* instances `[OfNat (Fin (Fintype.card α)) 1]` and `[… 0]` as hypotheses, instead
of using Lean's usual meaning of the numerals 0 and 1 in `Fin n`. As we read it, in `first_eigval_eq_0`,
`second_eigval_le_div` and the [Cheeger bound](#/node/UnweightedGraph.Isoperimetry.two_cheeger_ge_eigval_1),
"1" then means whichever index the caller's instance supplies, which need not be the second one.
""",
 [q("Is lapEigvals 0 the largest or the smallest eigenvalue?",
    ["The smallest: the order is increasing", "The largest, as the docstring says"], 0,
    "`eigval_order` proves i ≤ j → λᵢ ≤ λⱼ (ExpanderGraphs/chapter1.lean lines 366–371). The docstring on line 272 says otherwise."),
  q("Which of these is proved without sorry?",
    ["The eigenvalues sum to at most n", "λ₀ = 0", "λ₁ ≤ n/(n−1)"], 0,
    "`eigval_sum_le_n` is complete (lines 389–396). The other two are sorry'd (lines 444 and 452)."),
  q("What does `eigval_sum_eq_n_iff_no_isolation` actually prove?",
    ["Only that no isolation implies the sum is n", "Both directions of the “iff”"], 0,
    "Its statement takes `G.NoIsolation` as a hypothesis and concludes the sum equals n (lines 401–402)."),
 ],
 caveats=["The OfNat point is our reading of the variable declarations on line 361. We haven't checked how Lean resolves the numerals; see NOTES/review."])


node("UnweightedGraph.DirichletSum",
 "The Dirichlet sum Σ (f(u) − f(v))²",
 "The Dirichlet sum adds (f(u) − f(v))² over adjacent pairs. It measures how much a function on the vertices varies across edges. It runs over ordered pairs, so each edge is counted twice, and the Rayleigh formula compensates with a factor 1/2.",
 r"""## Plain English

**Definition (`DirichletSum`, ExpanderGraphs/chapter1.lean lines 283–286).** For *f* : α → ℝ,
Σᵤ Σᵥ [*u* adjacent to *v*] (*f*(*u*) − *f*(*v*))².

The docstring says "over all unordered pairs", but the double sum runs over ordered pairs, so each adjacent pair
contributes twice. That is why [lapEigvals_one_eq_inf_rayleigh](#/node/UnweightedGraph.lapEigvals_one_eq_inf_rayleigh)
multiplies it by 1/2. A pair joined by several parallel edges still counts once in each direction.
""",
 [q("For a single edge u–v with f(u) = 1, f(v) = 0, what is the Dirichlet sum?", ["2", "1", "0"], 0,
    "Both ordered pairs (u, v) and (v, u) contribute 1 (ExpanderGraphs/chapter1.lean line 286)."),
 ])


node("UnweightedGraph.lapEigvals_one_eq_inf_rayleigh",
 "λ₁ as a minimum of Rayleigh quotients (sorry, and false as written)",
 "This is meant to be Chung's formula for λ₁ as the minimum of a Rayleigh quotient. It is stated with sorry. As written, the right-hand side is 0 for every graph, because in Lean an infimum over a false condition of real numbers is 0.",
 r"""## Plain English

**Lemma (`lapEigvals_one_eq_inf_rayleigh`, ExpanderGraphs/chapter1.lean lines 289–294), PARTIAL (sorry).** For a
nonempty, [simple](#/node/UnweightedGraph.IsSimple), loopless graph it claims

λ₁ = inf over *f* with Σ *f*(*v*)·*d*ᵥ = 0 and *f* ≠ 0 of
(½ · [DirichletSum](#/node/UnweightedGraph.DirichletSum)(*f*)) / (Σ *f*(*v*)² *d*ᵥ).

On paper this is Chung's characterisation of λ₁ (her equation (1.5)). The proof is a single `sorry` (line 294).

### Why the Lean statement doesn't say this

The infimum is written with ⨅ and the two conditions as extra binders, ⨅ *f*, ⨅ (_ : cond₁), ⨅ (_ : cond₂), …. In Mathlib,
an infimum of real numbers over an **empty** index is `sInf ∅`, which is defined to be **0**. So for every *f* that fails
a condition, the inner part contributes 0 instead of being skipped. *f* = 0 always fails "*f* ≠ 0". So 0 is among the
values, all the genuine quotients are ≥ 0, and the whole right-hand side is 0.

The statement therefore claims λ₁ = 0 for every simple loopless graph. That is false already for one edge (K₂), where
the eigenvalues are 0 and 2. The usual fix is to take the infimum over a subtype, {*f* // conditions}, or to use
`sInf` of an image set.

This trap is common in Lean formalisations. The intended mathematics is fine.
""",
 [q("Why is the right-hand side 0 for every graph?",
    ["For f = 0 the condition f ≠ 0 fails, an infimum over nothing is 0 in ℝ, and all other values are ≥ 0",
     "Because the Dirichlet sum is always 0", "Because λ₁ = 0"], 0,
    "This is how ⨅ over a Prop works for real numbers (Real.sInf_empty). See ExpanderGraphs/chapter1.lean lines 292–293."),
  q("Is the lemma proved in the project?", ["No, it is `sorry`", "Yes"], 0, "ExpanderGraphs/chapter1.lean line 294."),
  q("What would the classical statement say for K₂ (one edge)?",
    ["λ₁ = 2, attained by f = (1, −1)", "λ₁ = 0", "λ₁ = 1"], 0,
    "With f = (1, −1): ½·Dirichlet = ½·(4+4) = 4, and the denominator is 1+1 = 2, so the quotient is 2. That is the second eigenvalue of ℒ = [[1, −1], [−1, 1]]."),
 ],
 caveats=["PARTIAL (sorry).",
          "“False as written” is our analysis of Mathlib's conventions for ⨅ over a Prop in ℝ. It was not checked by Lean. We are confident about it, but the author should confirm."])


node("UnweightedGraph.vol",
 "Volume: the sum of degrees",
 "vol S adds up the degrees of the vertices in S. Chung measures the size of a vertex set by its volume, not by how many vertices it has.",
 r"""## Plain English

**Definition (`vol`, ExpanderGraphs/chapter1.lean lines 63–64).** vol *S* = Σ over *v* ∈ *S* of
[degree](#/node/UnweightedGraph.degree) *v*, as a non-negative real. The empty set has volume 0, and so does a set
of isolated vertices.

The [Cheeger ratio](#/node/UnweightedGraph.Isoperimetry.hG) divides the number of boundary edges by the smaller of
vol *S* and vol *S*ᶜ.
""",
 [q("What is vol of a set containing only isolated vertices?", ["0", "The number of vertices in it", "Undefined"], 0,
    "Each degree is 0 (ExpanderGraphs/chapter1.lean line 64)."),
 ])


# ---------------------------------------------------------------- connectivity

node("UnweightedGraph.Walk",
 "Walks in an UnweightedGraph",
 "A walk from u to v is a list of steps between adjacent vertices. The definition is copied from Mathlib's SimpleGraph.Walk and adapted to the multigraph type.",
 r"""## Plain English

**Inductive type (`Walk`, ExpanderGraphs/Connectivity.lean lines 33–38).** A walk from *u* to *w* is either

- `nil`: the empty walk from *u* to itself, or
- `cons h p`: one step from *u* to an adjacent *v* (`h : G.Adj u v`), followed by a walk *p* from *v* to *w*.

Walks record adjacency, not which edge they use. The file says these definitions are "99% inspired by mathlib
SimpleGraph" (line 31).
""",
 [q("Does a Walk remember which of several parallel edges it used?",
    ["No; each step only stores a proof that the two vertices are adjacent", "Yes"], 0,
    "The step is `h : G.Adj u v` (ExpanderGraphs/Connectivity.lean line 37)."),
 ])


node("UnweightedGraph.Connected",
 "Connected graphs",
 "A graph is connected when it has at least one vertex and any two vertices are joined by a walk. This is the multigraph analogue of Mathlib's SimpleGraph.Connected.",
 r"""## Plain English

**Structure (`Connected`, ExpanderGraphs/Connectivity.lean lines 46–50).** *G* is connected when

- it is **preconnected** (`Preconnected`, lines 43–44): every *u*, *v* are **reachable** (`Reachable`, lines 40–41),
  meaning there is a [walk](#/node/UnweightedGraph.Walk) from *u* to *v*; and
- the vertex type α is nonempty.

The walks range over the whole type α. If some element of α isn't in `G.vertexSet`, it has no edges, so a graph with
two or more elements of α can only be connected if every element is in use. The hypothesis `hα` (every element of α
is a vertex) is the natural setting.
""",
 [q("Is a graph with exactly one vertex and no edges connected?",
    ["Yes: it is nonempty, and the empty walk joins the vertex to itself", "No, it needs an edge"], 0,
    "`Walk.nil` gives reachability (ExpanderGraphs/Connectivity.lean line 36), and nonemptiness holds."),
  q("Is the empty graph (α empty) connected?", ["No; Connected requires a vertex", "Yes, vacuously"], 0,
    "The `nonempty` field is required (ExpanderGraphs/Connectivity.lean line 50)."),
 ])


node("UnweightedGraph.edgeBoundary",
 "The edge boundary ∂S",
 "∂S is the set of edges with one end in S and the other outside S. The Cheeger constant compares its size to the volume of S.",
 r"""## Plain English

**Definition (`edgeBoundary`, ExpanderGraphs/Connectivity.lean lines 53–55).** ∂*S* is the set of edges *e* in
`G.edgeSet` for which there are *a* ∈ *S* and *b* ∉ *S* with *e* linking *a* and *b*.

Facts in ExpanderGraphs/chapter2.lean: ∂*S* = ∂(*S*ᶜ) (`edgeBoundaryComplement`, lines 46–53, proved), and
∂*S* = E(*S*, *S*ᶜ) (`self_connection_eq_boundary`, lines 56–58, true by definition).

There is also a vertex boundary δ*S* (`vertexBoundary`, ExpanderGraphs/Connectivity.lean lines 58–61): the vertices
outside *S* with a neighbour in *S*.
""",
 [q("Can a loop ever be in ∂S?", ["No: both its ends are the same vertex, so it can't have one inside and one outside S", "Yes"], 0,
    "A loop links a to a, and a can't be both in S and in Sᶜ (ExpanderGraphs/Connectivity.lean line 55)."),
  q("Is ∂S the same set as ∂(Sᶜ)?", ["Yes, and the project proves it", "Only for connected graphs"], 0,
    "`edgeBoundaryComplement`, ExpanderGraphs/chapter2.lean lines 46–53."),
 ])


node("UnweightedGraph.walk_crossing",
 "A walk that leaves S crosses ∂S",
 "If a walk starts inside S and ends outside it, then some edge of the graph has one end in S and the other outside. This is the discrete intermediate value theorem.",
 r"""## Plain English

**Lemma (`walk_crossing`, ExpanderGraphs/Connectivity.lean lines 64–82).** Assume every element of β is an edge
(`hβ`). If there is a [walk](#/node/UnweightedGraph.Walk) from *u* to *v* with *u* ∈ *S* and *v* ∉ *S*, then the
[edge boundary](#/node/UnweightedGraph.edgeBoundary) ∂*S* is nonempty.

The proof is by induction on the walk. Look at its first step *u* → *y*. If *y* ∈ *S*, apply the induction hypothesis
to the rest of the walk. If *y* ∉ *S*, the edge behind that step has one end in *S* and one outside.
""",
 [q("What does the lemma conclude?",
    ["∂S contains at least one edge", "The walk uses exactly one boundary edge", "S is connected"], 0,
    "`∃ e, e ∈ G.edgeBoundary S` (ExpanderGraphs/Connectivity.lean line 68)."),
 ])


node("UnweightedGraph.connected_non_empty_edge_boundary",
 "Headline: in a connected graph, every proper vertex set has a boundary edge",
 "If the graph is connected and S is neither empty nor everything, at least one edge leaves S. This is why the Cheeger constant of a connected graph should be positive. The proof in the source is complete.",
 r"""## Plain English

**Lemma (`connected_non_empty_edge_boundary`, ExpanderGraphs/Connectivity.lean lines 85–97).** Let *G* be a
[connected](#/node/UnweightedGraph.Connected) [UnweightedGraph](#/node/UnweightedGraph) in which every element of β is
an edge (`hβ`). For any set of vertices *S* that is nonempty and is not all of α, the
[edge boundary](#/node/UnweightedGraph.edgeBoundary) ∂*S* has an element.

This is the combinatorial half of "connected ⇔ Cheeger constant > 0" (Chung, chapter 2). The project states that
equivalence as `connected_iff_cheeger_pos` (ExpanderGraphs/chapter2.lean lines 113–116), but leaves it `sorry`. Because of
how the [Cheeger constant](#/node/UnweightedGraph.Isoperimetry.cheeger) is currently written, that equivalence isn't
true as stated.

### The argument

Pick *u* ∈ *S* and *v* ∉ *S*. Connectivity gives a walk from *u* to *v*, and
[walk_crossing](#/node/UnweightedGraph.walk_crossing) finds the edge where it leaves *S*.
""",
 [q("Which sets S does the lemma cover?",
    ["Nonempty sets other than the whole vertex type", "All sets", "Only sets of at most half the vertices"], 0,
    "Hypotheses `hS_nonempty` and `hS_ne_univ` (ExpanderGraphs/Connectivity.lean line 89)."),
  q("What is the conclusion's form?",
    ["`Nonempty (G.edgeBoundary S)`: some edge lies in ∂S", "A lower bound on the size of ∂S", "∂S = ∂(Sᶜ)"], 0,
    "Line 90 of ExpanderGraphs/Connectivity.lean. It gives existence only, not a count."),
  q("Does the lemma give a lower bound on the Cheeger constant?",
    ["No. It shows ∂S ≠ ∅, which is the qualitative fact behind “connected ⇒ h > 0”", "Yes, h ≥ 1/n"], 0,
    "No volume or ratio appears in the statement (ExpanderGraphs/Connectivity.lean lines 88–90)."),
 ],
 widgets=walk("How the proof goes (ExpanderGraphs/Connectivity.lean, lines 85-97)", [
  {"text": "Pick u ∈ S (line 91)."},
  {"text": "S ≠ univ, so pick v ∉ S (line 92).", "lean": "obtain ⟨v, hv⟩ : ∃ v, v ∉ S := by grind;"},
  {"text": "Connectivity gives a walk p from u to v (lines 93–95).", "link": "UnweightedGraph.Connected"},
  {"text": "The walk starts in S and ends outside, so it crosses ∂S (lines 96–97).", "link": "UnweightedGraph.walk_crossing",
   "lean": "exact walk_crossing hβ S p hu hv"},
 ]))


# ---------------------------------------------------------------- Cheeger

node("UnweightedGraph.Isoperimetry.hG",
 "The Cheeger ratio h_G(S)",
 "h_G(S) is the number of edges leaving S divided by the smaller of vol S and vol Sᶜ. A small ratio means S is a bottleneck: a large part of the graph with few edges out.",
 r"""## Plain English

**Definition (`hG`, ExpanderGraphs/chapter2.lean lines 61–64).** h_G(*S*) = |∂*S*| / min([vol](#/node/UnweightedGraph.vol) *S*,
vol *S*ᶜ), where |∂*S*| is the number of [boundary edges](#/node/UnweightedGraph.edgeBoundary).

When the minimum volume is 0, Lean's division by zero gives h_G(*S*) = 0. That is why the
[Cheeger constant](#/node/UnweightedGraph.Isoperimetry.cheeger) is meant to range only over *S* with positive
volume on both sides.

The vertex version `gG` (lines 67–70) uses vol(δ*S*) instead of |∂*S*|. `hG_le_gG` (lines 131–139) is stated, but its
key step is `sorry` (line 138).
""",
 [q("What is h_G(∅) in Lean?", ["0, because Lean's division by zero gives 0", "Infinity", "Undefined, so it can't be written"], 0,
    "vol ∅ = 0, so the denominator is 0 (ExpanderGraphs/chapter2.lean line 64)."),
 ])


node("UnweightedGraph.Isoperimetry.cheeger",
 "The Cheeger constant h_G (as written, always 0)",
 "It is meant to be the smallest h_G(S) over sets S with positive volume on both sides. Because Lean's infimum of reals over an empty index is 0, the definition as written evaluates to 0 for every graph.",
 r"""## Plain English

**Definition (`cheeger`, ExpanderGraphs/chapter2.lean lines 73–77).** The intended meaning, as in the blueprint and Chung's
book: h_G = min over *S* with 0 < min(vol *S*, vol *S*ᶜ) of [h_G(S)](#/node/UnweightedGraph.Isoperimetry.hG). It is
small exactly when the graph has a bottleneck. Chung's chapter 2 relates it to λ₁: 2h_G ≥ λ₁ > h_G²/2.

### What the Lean actually computes

The definition is ⨅ *S*, ⨅ (_ : 0 < min (vol *S*) (vol *S*ᶜ)), h_G(*S*). The inner ⨅ is over the *proof* of the condition. For an
*S* that fails the condition, such as *S* = ∅, it is an infimum over nothing, and for real numbers Mathlib defines that
as 0 (`Real.sInf_empty`). So the outer infimum includes 0. Every h_G(*S*) is ≥ 0, so

**cheeger G = 0 for every graph.**

The same applies to `cheegerV` (lines 80–84). The usual fix is ⨅ (*S* : {*S* // 0 < min …}), h_G *S*, or a
`sInf` over an image set. A formalisation can also just work with h_G(*S*) for each *S* directly.

### Consequences for the stated results

- `cheeger_mul_volume_le_volume_frontier` (lines 87–110, proved): h_G · vol *S* ≤ |∂*S*|. It remains true, but with
  h_G = 0 it says nothing.
- `cheeger_le_cheegerV` (lines 142–147, proved apart from the `sorry` it uses in `hG_le_gG`): 0 ≤ 0.
- `connected_iff_cheeger_pos` (lines 113–116, sorry): as written, it claims connected ⇔ 0 < 0, which is false for
  every connected graph.
- The [Cheeger bound](#/node/UnweightedGraph.Isoperimetry.two_cheeger_ge_eigval_1) (sorry): as written, it claims
  λ₁ ≤ 0.
""",
 [q("What does the definition, as written, evaluate to for a connected graph like K₃?",
    ["0, like every graph", "3/4", "1"], 0,
    "S = ∅ fails the condition, so its inner infimum is sInf ∅ = 0 in ℝ, which drags the outer infimum to 0 (ExpanderGraphs/chapter2.lean lines 76–77)."),
  q("What is the intended value of h_G for the complete graph K₄?",
    ["2/3, attained by splitting the vertices 2 + 2", "0", "1"], 0,
    "For |S| = 2: 4 boundary edges, vol S = 2·3 = 6, ratio 2/3. For |S| = 1: 3/3 = 1. The minimum is 2/3."),
  q("Which proved lemma about cheeger stays true but becomes uninformative?",
    ["cheeger · vol S ≤ |∂S|", "connected ⇔ cheeger > 0"], 0,
    "`cheeger_mul_volume_le_volume_frontier` (lines 87–110) holds with cheeger = 0. The iff is sorry'd and false as written."),
 ],
 caveats=["“Always 0” is our analysis of Mathlib's ⨅ over a Prop in ℝ. It was not checked by Lean. It is the same pattern as in lapEigvals_one_eq_inf_rayleigh."])


node("UnweightedGraph.Isoperimetry.two_cheeger_ge_eigval_1",
 "Headline (unfinished): λ₁ ≤ 2·h_G, Chung's Lemma 2.1",
 "The project's stated goal is the Cheeger inequality, and this is its easy half: λ₁ is at most twice the Cheeger constant. It is stated with sorry, so it is PARTIAL. As written it isn't true yet, because the Cheeger constant is defined so that it is always 0, and the numeral 1 is an assumed instance.",
 r"""## Plain English

**Lemma (`two_cheeger_ge_eigval_1`, ExpanderGraphs/chapter2.lean lines 119–123), PARTIAL (sorry).** The intended
claim is Chung's Lemma 2.1: for a connected graph, λ₁ ≤ 2·h_G, where λ₁ is the
[second-smallest eigenvalue](#/node/UnweightedGraph.lapEigvals) of the
[normalised Laplacian](#/node/UnweightedGraph.Laplacian) and h_G is the
[Cheeger constant](#/node/UnweightedGraph.Isoperimetry.cheeger).

The Lean statement is `G.lapEigvals 1 ≤ 2 * cheeger G`, with no connectivity hypothesis (none is needed on paper:
a disconnected graph has λ₁ = 0). The proof is `:= sorry`.

### Two problems with the statement as written

1. **cheeger G is always 0.** As explained on the [cheeger](#/node/UnweightedGraph.Isoperimetry.cheeger) node, the
   real-valued infimum over a condition makes the definition 0 for every graph. So the statement claims λ₁ ≤ 0, which
   fails for K₂, where λ₁ = 2.
2. **What "1" means.** Line 119 adds `[OfNat (Fin (Fintype.card α)) 0] [OfNat (Fin (Fintype.card α)) 1]` as
   hypotheses. As we read it, the numeral `1` then refers to whatever index that instance gives, which need not be the
   second one.

Both are definition-level issues and easy to fix. The mathematics is the standard result.

### The rest of the Cheeger chapter

`cheeger_lower_bound` (line 127, the other half, λ₁ > h_G²/2) and `two_cheegerV_ge_first_eigval` (line 150) are
placeholders of the form `True := sorry`. They state nothing yet.

### How the proof would go (Chung)

Take the set *S* where h_G is attained, with vol *S* ≤ vol *S*ᶜ, and the test function *f* = 1/vol *S* on *S* and
−1/vol *S*ᶜ off *S*. Then Σ *f d* = 0, and its Rayleigh quotient is at most 2·|∂*S*|/vol *S* = 2h_G. So λ₁ ≤ 2h_G by
the [Rayleigh characterisation](#/node/UnweightedGraph.lapEigvals_one_eq_inf_rayleigh), which is itself sorry'd and has
the same infimum problem.
""",
 [q("Is this lemma proved in the project?", ["No; its proof is `sorry`", "Yes"], 0,
    "ExpanderGraphs/chapter2.lean line 123 ends with `:= sorry`."),
  q("As written, what inequality does the statement claim?",
    ["λ₁ ≤ 0, because `cheeger G` evaluates to 0", "λ₁ ≤ 2h_G with the usual h_G", "λ₁ ≥ h_G²/2"], 0,
    "The definition of cheeger (lines 76–77) is always 0. See that node."),
  q("Which part of the Cheeger inequality is this?",
    ["The easy upper bound λ₁ ≤ 2h_G", "The hard lower bound λ₁ > h_G²/2", "Both"], 0,
    "The lower bound is the placeholder `cheeger_lower_bound : True := sorry` (line 127)."),
  q("Would a correct version need a connectivity hypothesis?",
    ["No: for a disconnected graph both sides are 0 on paper", "Yes, otherwise it is false"], 0,
    "Chung states it for connected graphs, but a disconnected graph has λ₁ = 0, so the inequality still holds."),
 ],
 caveats=["PARTIAL (sorry). The proof is missing.",
          "As written, the statement is not true (cheeger is always 0). This is our analysis, not checked by Lean.",
          "The OfNat point is our reading of line 119. We haven't checked how Lean resolves the numeral."],
 widgets=walk("Status of the proof (ExpanderGraphs/chapter2.lean, lines 119-123)", [
  {"text": "Line 119 assumes OfNat instances for the indices 0 and 1 of Fin (card α)."},
  {"text": "The statement compares lapEigvals 1 with 2 · cheeger G (lines 122–123).", "link": "UnweightedGraph.lapEigvals"},
  {"text": "The proof is a single sorry (line 123): nothing is proved yet.", "lean": "G.lapEigvals 1 ≤ 2 * cheeger G := sorry"},
  {"text": "As written, cheeger G = 0, so the statement claims λ₁ ≤ 0. It needs the definition fixed first.", "link": "UnweightedGraph.Isoperimetry.cheeger"},
  {"text": "The intended proof plugs a two-valued test function into the Rayleigh quotient. That characterisation is also sorry'd.", "link": "UnweightedGraph.lapEigvals_one_eq_inf_rayleigh"},
 ]))


# ---------------------------------------------------------------- extra quiz questions (schema needs ≥ 3 per node)

EXTRA = {
 "UnweightedGraph.degree": [
  q("A vertex is joined to the same neighbour by two parallel edges and has no other edges. What are its degree and its number of neighbours?",
    ["Degree 2, one neighbour", "Degree 1, one neighbour", "Degree 2, two neighbours"], 0,
    "The degree counts incident edges (line 52). IsSimple is the hypothesis that the two numbers agree."),
 ],
 "UnweightedGraph.IsSimple": [
  q("What does IsSimple compare, for each vertex u?", ["degree u and the number of neighbours of u", "degree u and d", "The number of edges and the number of vertices"], 0,
    "ExpanderGraphs/chapter1.lean line 144."),
  q("Which headline assumes IsSimple?", ["zero_mem_lapSpectrum", "expander_mixing_lemma", "chromaticNumber_le_maxDegree_add_one'"], 0,
    "`(hS : G.IsSimple)` (ExpanderGraphs/chapter1.lean line 412). The other two use Mathlib's SimpleGraph, which is simple by construction."),
 ],
 "UnweightedGraph.T_sqrt": [
  q("What is the v-entry of T^(1/2) τ for an isolated vertex v?", ["0", "1", "Undefined"], 0, "The entry is √(d_v), and √0 = 0 (line 119)."),
  q("What does ℒ do to T^(1/2) τ in a simple loopless graph?", ["Sends it to 0", "Doubles it", "Leaves it unchanged"], 0,
    "`zero_eigenvalue_normalized`, ExpanderGraphs/chapter1.lean lines 328–330."),
 ],
 "UnweightedGraph.LapHermitian": [
  q("What does symmetry of ℒ give you?", ["Real eigenvalues and an orthonormal eigenbasis", "That 0 is an eigenvalue", "That the graph is connected"], 0,
    "Mathlib's spectral theorem for Hermitian matrices, used in `lapEigvals` (line 274)."),
  q("Does the proof of symmetry need the graph to be simple or loopless?", ["No", "Yes"], 0,
    "No hypotheses besides the standing ones (ExpanderGraphs/chapter1.lean line 260)."),
 ],
 "UnweightedGraph.lapSpectrum": [
  q("What does 0 ∈ lapSpectrum mean?", ["ℒ is not invertible", "ℒ is the zero matrix", "Every eigenvalue is 0"], 0,
    "0 is in the spectrum when 0·I − ℒ = −ℒ is not a unit (lines 414–416)."),
  q("Which lemma shows 0 ∈ lapSpectrum?", ["zero_mem_lapSpectrum", "first_eigval_eq_0", "LSS"], 0, "ExpanderGraphs/chapter1.lean lines 411–438."),
 ],
 "UnweightedGraph.zero_eigenvalue_normalized": [
  q("At an isolated vertex v, why is the v-entry of ℒ·(√d) zero?", ["Row v of ℒ is entirely 0", "Because √d_v = 1"], 0,
    "The diagonal entry is 0 when d_v = 0 and there are no neighbours (the `h_deg` case, line 336)."),
 ],
 "UnweightedGraph.DirichletSum": [
  q("Is the Dirichlet sum ever negative?", ["No; it is a sum of squares", "Yes, for oscillating f"], 0, "Each term is (f u − f v)² or 0."),
  q("What is the Dirichlet sum of a constant function?", ["0", "The number of edges", "n"], 0, "Every difference f u − f v is 0."),
 ],
 "UnweightedGraph.vol": [
  q("What is vol of the whole vertex set of a d-regular graph on n vertices?", ["n·d", "n", "d"], 0, "The sum of n degrees, each equal to d."),
  q("Is vol S the number of vertices in S?", ["No, it is the sum of their degrees", "Yes"], 0, "ExpanderGraphs/chapter1.lean line 64."),
 ],
 "UnweightedGraph.Walk": [
  q("What is the shortest walk from u to u?", ["The empty walk `nil`", "A loop at u", "There is none"], 0, "ExpanderGraphs/Connectivity.lean line 36."),
  q("What does `cons h p` add to a walk?", ["One step to an adjacent vertex at the front", "One step at the end", "A loop"], 0,
    "`cons (h : G.Adj u v) (p : Walk v w) : Walk u w` (ExpanderGraphs/Connectivity.lean line 37)."),
 ],
 "UnweightedGraph.Connected": [
  q("What does Reachable u v mean?", ["There is a walk from u to v", "u and v are adjacent", "u = v"], 0, "ExpanderGraphs/Connectivity.lean line 41."),
 ],
 "UnweightedGraph.edgeBoundary": [
  q("Which edges are in ∂S when S is all of α?", ["None: no endpoint can be outside S", "All of them"], 0, "Sᶜ is empty, so no b ∉ S exists."),
 ],
 "UnweightedGraph.walk_crossing": [
  q("How is the lemma proved?", ["By induction on the walk", "By contradiction using eigenvalues", "By counting edges"], 0,
    "`induction hW with` (ExpanderGraphs/Connectivity.lean line 69)."),
  q("In the nil case the walk starts and ends at u. Why is that case impossible?", ["u ∈ S and u ∉ S would both hold", "Because walks are nonempty"], 0,
    "ExpanderGraphs/Connectivity.lean lines 70–72."),
 ],
 "UnweightedGraph.Isoperimetry.hG": [
  q("For K₄ and S a single vertex, what is h_G(S)?", ["1", "1/3", "3"], 0, "3 boundary edges, vol S = 3, vol Sᶜ = 9, so 3/min(3, 9) = 1."),
  q("Why use the smaller of vol S and vol Sᶜ?", ["So that h_G(S) = h_G(Sᶜ) and both sides of the cut are treated alike", "To make the ratio larger"], 0,
    "∂S = ∂(Sᶜ) (`edgeBoundaryComplement`), and the min is symmetric too."),
 ],
}
for n in NODES:
    n["quiz"] += EXTRA.get(n["id"], [])
