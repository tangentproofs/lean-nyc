NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]


node("SystemFMuState.type_safety",
 "Headline: well-typed programs with recursive types and state don't get stuck",
 "Take a closed program of System F with recursive types and first-order references. Run it from the empty heap: if it ever reaches a state that cannot step, that state is a value. This is genuine type safety, since programs may now loop, proved with a step-indexed, world-indexed logical relation.",
 r"""## Plain English

**Theorem (`SystemFMuState.type_safety`, TypeSystems/SystemFMuState/LogRel.lean lines 3047–3066).** Let *e* be a
closed program of the [state language](#/node/SystemFMuState.Ty) with some type *A* under the
[logical relation's typing rules](#/node/SystemFMuState.SynTyped), with no type variables and an empty context.
Suppose that, starting from the **empty heap**, *e* runs for *n* steps and reaches an expression *e′* with heap *h′*
that can make no further step ([redNsteps](#/node/SystemFMuState.redNsteps)). Then *e′* is a **value**.

Equivalently, a well-typed program never gets stuck. It can run forever, and with recursive types it really can
(TypeSystems/SystemFMu/ZCombinator.lean is about the Z combinator), but every run that stops, stops at a value.
`type_safety_safe` (lines 3072–3075) repackages the theorem through a `safe` predicate (lines 3068–3069).

### What changed from System F

Two features break the simple recursion on types used for [System F](#/node/SystemF.valRel):

- **Recursive types** μα. *A*: unfolding one gives a *bigger* type. The relation therefore carries a **step index** *k*.
  A value is related at μα. *A* with budget *k* + 1 if its unrolling is related at the unfolded type with a smaller budget.
- **Mutable references**: what a location holds can change. The relation carries a **world** *W*, a list of
  per-location invariants that the heap must satisfy, and it is monotone as the world grows.

How these fit together is explained under [semTyped](#/node/SystemFMuState.semTyped).

### Why the index trick suffices for safety

[semTyped](#/node/SystemFMuState.semTyped) holds at **every** step index. To show that a run of length *n*
ends well, the proof uses index *n* + 1. The expression relation at that index covers every complete run shorter
than *n* + 1 steps, including this one, and promises it ends in a value.
""",
 [q("What does `type_safety` say about a run that never stops?",
    ["Nothing: the hypothesis requires a run that reaches an irreducible state", "It rules such runs out", "It says the run eventually reaches a value"], 0,
    "`redNsteps` bundles *n* steps with irreducibility of the final state (TypeSystems/SystemFMuState/Execution.lean lines 26–27)."),
  q("Which step index does the proof use for a run of length *n*?",
    ["n + 1", "0", "n", "Any index"], 0,
    "Lines 3051 and 3056 instantiate at `n + 1`, and line 3065 discharges *n* < *n* + 1."),
  q("What can be stored in a reference in this type system?",
    ["Only first-order values: integers, booleans, unit, and their products and sums", "Any value, including functions", "Only integers"], 0,
    "`ref` takes a first-order type `FoTy` (TypeSystems/SystemFMuState/Types.lean lines 27–33 and 48)."),
  q("From which heap does the run start?",
    ["The empty heap", "Any heap", "Any heap well typed for the program"], 0,
    "`redNsteps n e Heap.empty e' h'` (line 3049)."),
 ],
 caveats=["The typing judgement here is the logical relation's own, in which references hold only first-order types. A separate syntactic development with unrestricted references (and a safety theorem by progress and preservation) is SystemFMuState.Syn.type_safety; the two type systems are different.",
          "Stated for runs from the empty heap only. The syntactic version allows any heap that is well typed for the program."],
 widgets=walk("How the proof goes (TypeSystems/SystemFMuState/LogRel.lean, lines 3047-3066)", [
  {"text": "Given the typing derivation and a complete run of n steps from the empty heap (lines 3048–3050).", "link": "SystemFMuState.redNsteps"},
  {"text": "The empty substitution satisfies the empty context relation at index n + 1 (lines 3051–3055)."},
  {"text": "Apply the fundamental theorem with the dummy type interpretation, the empty world [] and index n + 1 (line 3056).", "link": "SystemFMuState.sem_soundness"},
  {"text": "Drop the empty substitution and unfold the expression relation (lines 3057–3058).", "link": "SystemFMuState.semTyped"},
  {"text": "The empty world extends itself, and the empty heap satisfies the empty world (lines 3059–3063).", "link": "SystemFMuState.wsat"},
  {"text": "Feed the run (n < n + 1 steps, ending irreducible) to the expression relation: the final expression converts to a value (lines 3064–3065)."},
  {"text": "Hence it is a value (line 3066)."},
 ]))

node("SystemFMuState.Ty",
 "Types with recursion and references",
 "Types are System F's plus recursive types μ and references ref a. In this type system, a reference may only hold a first-order type: int, bool, unit, and products and sums of those.",
 r"""## Plain English

**Definitions (TypeSystems/SystemFMuState/Types.lean lines 27–49).** First-order types (`FoTy`, lines 27–33) are
`int`, `bool`, `unit` and products and sums of first-order types. They contain no type variables and no functions.

Types (`SystemFMuState.Ty`, lines 37–49) are type variables (De Bruijn indices), `int`, `bool`, `unit`, functions,
∀, ∃, products, sums, a **recursive type** μ. *A*, which binds index 0 like ∀ does, and **`ref a`** for a first-order *a*.

The doc comment on lines 19–26 explains the encoding. The restriction to first-order contents keeps the heap
invariants simple, since a stored value's meaning doesn't depend on step indices or worlds. Using a separate type
`FoTy` (instead of a predicate on `Ty`) stops type substitution from ever reaching inside a `ref`. Higher-order
state needs the Iris machinery of the later chapters ([ConcurrentLogRel](#/node/ProgramLogics.LogRel.Ty)).

The expressions (`SystemFMuState.Expr`, TypeSystems/SystemFMuState/Lang.lean lines 62–90) add `roll`/`unroll`
for μ, and `new`, `load` and `store` for references.
""",
 [q("Can a function be stored in a reference in this type system?",
    ["No; `ref` only takes first-order types", "Yes"], 0,
    "TypeSystems/SystemFMuState/Types.lean line 48."),
  q("What does μ. A bind?",
    ["Type variable index 0 in A, standing for the whole recursive type", "A term variable", "A heap location"], 0,
    "Types.lean lines 35–36: `all`, `exist` and `mu` each bind one type variable."),
  q("Why is `FoTy` a separate inductive type rather than a predicate on `Ty`?",
    ["So that type substitution never descends below a `ref`, which a lemma about the relation needs", "Lean cannot express predicates on types", "For performance"], 0,
    "Types.lean lines 22–26."),
 ])

node("SystemFMuState.SynTyped",
 "Typing rules for the state language",
 "The System F rules plus roll/unroll for recursive types and new/load/store for first-order references. The judgement carries a heap context that no rule actually inspects.",
 r"""## Plain English

**Definition (`SystemFMuState.SynTyped`, TypeSystems/SystemFMuState/Types.lean lines 437–528).** The judgement
*n*; Γ; Σ ⊢ *e* : *A* has the [System F](#/node/SystemF.SynTyped) rules plus:

- **roll / unroll** (lines 512–517): `roll e` has type μ. *A* if *e* has the unfolded type *A*[μ. *A*/0], and `unroll` goes back;
- **new** (lines 519–521): if *e* has first-order type *a*, then `new e` has type `ref a`;
- **load** (lines 522–524) and **store** (lines 525–528), as expected. Store returns `unit`.

The heap context Σ is carried along but, as the comment on lines 414–415 says, **no typing rule inspects it**. In
particular, no rule types a location literal, so a well-typed source program never mentions a raw location.
The [headline](#/node/SystemFMuState.type_safety) uses Σ = [].
""",
 [q("Which type does `store e₁ e₂` have?",
    ["unit", "The type of e₂", "ref of the type of e₂"], 0,
    "TypeSystems/SystemFMuState/Types.lean lines 525–528."),
  q("Does the heap-context argument constrain typing?",
    ["No, no rule inspects it", "Yes, it types location literals"], 0,
    "Lines 414–415."),
  q("What type must e have for `roll e : μ. A`?",
    ["A with μ. A substituted for index 0", "μ. A itself", "A unchanged"], 0,
    "`Ty.subst1 A (.mu A)` (line 513)."),
 ])

node("SystemFMuState.redNsteps",
 "Complete runs: redNsteps",
 "redNsteps n e h e′ h′ means: starting from expression e and heap h, n reduction steps reach e′ and h′, and from there no step is possible. A complete run ends either at a value or stuck.",
 r"""## Plain English

**Definition (`SystemFMuState.redNsteps`, TypeSystems/SystemFMuState/Execution.lean lines 26–27).** Two parts:

1. exactly *n* contextual reduction steps lead from (*e*, *h*) to (*e′*, *h′*) (`Nsteps`, lines 21–23);
2. (*e′*, *h′*) is **irreducible**: it can take no further step.

So "*e* reduces completely to *e′*". *e′* may be a value, or it may be stuck, e.g. loading from an integer.
Type safety says that, for well-typed programs, it is always a value.
""",
 [q("Does `redNsteps` require the final expression to be a value?",
    ["No, only irreducible; values and stuck terms both qualify", "Yes"], 0,
    "TypeSystems/SystemFMuState/Execution.lean line 27."),
  q("What does `redNsteps` say about a program that loops forever?",
    ["It never holds: there is no irreducible state to reach", "It holds for every n"], 0,
    "An infinite run never reaches an irreducible configuration."),
  q("Does the heap change along the run?",
    ["Yes; the start and end heaps h and h′ can differ", "No, the heap is fixed"], 0,
    "Steps act on expression–heap pairs (line 27)."),
 ])

node("SystemFMuState.wsat",
 "Worlds and world satisfaction",
 "A world is a list of invariants, each tying one heap location to a predicate on its contents. A heap satisfies a world when it is bounded, every invariant's location holds a value that meets its predicate, and no two invariants govern the same location.",
 r"""## Plain English

**Definitions (TypeSystems/SystemFMuState/LogRel.lean lines 41–100).**

- A **heap invariant** (`HeapInv`, lines 41–43) is a location together with a predicate on values.
- A **world** (line 46) is a list of heap invariants. *W′* **extends** *W* when *W* is a prefix of *W′*
  (`worldExt`, line 54): new invariants are only ever added at the end, never removed or changed.
- **World satisfaction** `wsat W h` (lines 97–100) means three things: the heap *h* is *bounded*, i.e. only finitely
  many locations are allocated (line 68), every invariant in *W* holds of its location's current content in *h*,
  and distinct invariants govern distinct locations.

The value relation at `ref a` (line 186) says only that the world contains the invariant "this location holds a
value of first-order type *a*". The heap itself is constrained through `wsat`. In
TypeSystems/SystemFMuState/MutBit.lean a program installs a **stronger** invariant ("the cell holds 0 or 1")
than its type alone demands.
""",
 [q("How can a world change as a program runs?",
    ["Only by appending new invariants", "Invariants can be removed when a location is overwritten", "Arbitrarily"], 0,
    "`worldExt W W'` means W' = W ++ Wn (TypeSystems/SystemFMuState/LogRel.lean line 54)."),
  q("Why does `wsat` require the heap to be bounded?",
    ["So that allocation can always find a fresh location", "To make loads terminate", "It doesn't"], 0,
    "Lines 64–68: heaps are total functions, so finiteness must be stated, and it guarantees `new` succeeds."),
  q("Is the predicate in a heap invariant restricted to type membership?",
    ["No; any predicate on values, so programs can maintain stronger invariants", "Yes, it must be foValRel of some type"], 0,
    "Lines 34–40 and MutBit.lean."),
 ])

node("SystemFMuState.semTyped",
 "The step-indexed, world-indexed logical relation",
 "Values are related at a type for k more steps in world W. Recursive types spend one step per unrolling; functions must work in all future worlds. An expression is good if every complete run of fewer than k steps, from any heap satisfying an extension of W, ends in a good value.",
 r"""## Plain English

**Definitions (TypeSystems/SystemFMuState/LogRel.lean lines 59–222).** Semantic types (lines 59–63) are predicates
on (step index, world, value) that hold only for closed values. They are **downward closed** in the index (true for
*k* means true for every smaller *k*) and **upward closed** in the world (true in *W* means true in every extension).

The value relation `valRel δ A k W v` (lines 154–187), by cases on *A*:

- base types, products, sums and type variables: as in [System F](#/node/SystemF.valRel);
- **functions**: a closed λ such that, for every smaller budget *k* − *kd*, every [extension](#/node/SystemFMuState.wsat)
  *W′* of *W*, and every argument related there, the substituted body is in the expression relation there;
- **∀ / ∃**: quantify over semantic types τ, as in System F;
- **μ. A** at budget 0: just closed. At budget *k* + 1: closed, and the unrolled value is related at
  *A*[μ. *A*/0] with every budget up to *k*. **One step of budget is spent per unrolling**;
- **ref a**: the value is a location *l*, and the world contains the invariant "*l* holds a first-order value of type *a*".

The expression relation `exprRel δ A k W e` (lines 201–205): for every run that reaches an irreducible state in
*n* < *k* steps from a heap satisfying some extension *W′* of *W*, the final expression is a value, related at
*A* with the remaining budget *k* − *n*, in some further extension *W″* that the final heap satisfies.

**Semantic typing** (`SystemFMuState.semTyped`, lines 221–222) means: for every δ, *W*, *k* and every substitution
that gives each variable a related closed value (`semCtxRel`, lines 214–217), the substituted term is in
`exprRel δ A k W`.

### Why it is well founded

The definitions recurse on the triple (step index, type size, value-or-expression) in lexicographic order
(lines 125–127, 188, 206). The μ case keeps the type size from going down, but it lowers the index.
""",
 [q("What does a related value at μ. A with budget 0 have to satisfy?",
    ["Only closedness", "Nothing at all", "Its unrolling must be related at budget 0"], 0,
    "TypeSystems/SystemFMuState/LogRel.lean line 181."),
  q("Why does the function case quantify over future worlds?",
    ["The function may be called later, after more locations have been allocated", "To make the relation decidable", "Because functions allocate"], 0,
    "Lines 170–172 quantify over every W′ extending W."),
  q("What does the expression relation promise about runs of k or more steps?",
    ["Nothing; only runs shorter than the budget k are covered", "That they end in values"], 0,
    "`n < k` (line 202). That is why semantic typing must hold at every index."),
  q("What does the relation say about a location at `ref a`?",
    ["The world has the invariant that it holds a value of first-order type a", "The location currently holds a value related at a", "Nothing"], 0,
    "Line 186. The current contents are constrained by `wsat`, not here."),
 ],
 caveats=["`valRel` and `exprRel` (lines 145–210) are a `mutual` block, which the site's text scanner doesn't list, so they are explained here.",
          "Rocq's heap invariants are arbitrary predicates on whole heaps. This port confines each invariant to one location (lines 34–40). The file says this is all that first-order references need. That claim is the port author's, and this site has not checked it."])

node("SystemFMuState.sem_soundness",
 "Fundamental theorem for the state language",
 "Every term typed by the state language's rules is semantically typed: in every world, at every step index, under every good substitution. The proof is the usual one compatibility lemma per typing rule, including roll, unroll, new, load and store.",
 r"""## Plain English

**Theorem (`SystemFMuState.sem_soundness`, TypeSystems/SystemFMuState/LogRel.lean lines 2991–3030).** If
*n*; Γ; Σ ⊢ *e* : *A* ([typing](#/node/SystemFMuState.SynTyped)), then Γ ⊨ *e* : *A*
([semantic typing](#/node/SystemFMuState.semTyped)).

The proof inducts on the typing derivation, one compatibility lemma per rule (lines 2995–3030). The doc
comment (lines 2985–2990) notes that no well-formedness condition on the context is needed.

The file is the largest in the port at about 3,000 lines. Most of it is the infrastructure needed to make the
compatibility lemmas go through: monotonicity in index and world, the bind lemma for evaluation contexts,
and moving type substitutions through the relation.
""",
 [q("Does the fundamental theorem fix a step index?",
    ["No; semantic typing holds at every index", "Yes, index 0"], 0,
    "`semTyped` quantifies over all k (TypeSystems/SystemFMuState/LogRel.lean lines 221–222)."),
  q("How many cases does the induction have?",
    ["One per typing rule, including roll, unroll, new, load and store", "One per type constructor", "Two"], 0,
    "Lines 2995–3030."),
  q("Which theorem uses this to get safety?",
    ["`type_safety`", "`Syn.type_safety`"], 0,
    "Line 3056. `Syn.type_safety` is the syntactic proof."),
 ])

node("SystemFMuState.Syn.type_safety",
 "Syntactic safety with unrestricted references",
 "The progress-and-preservation proof of safety for the state language with references to any type, from any heap well typed for the program. It is a different type system from the one the logical relation uses.",
 r"""## Plain English

**Theorem (`SystemFMuState.Syn.type_safety`, TypeSystems/SystemFMuState/TypeSafety.lean lines 2231–2245).** In the
syntactic type system of `SystemFMuState.Syn`, references may hold **any** type (TypeSafety.lean lines 11–14 and 23–36),
and the judgement uses a heap typing Θ. Suppose *e₁* is closed and well typed under a well-formed Θ, and the starting
heap is bounded and matches Θ. Then every expression *e₂* reached after *n* steps is a value or can step.

The proof is the classical one: preservation, which may extend Θ when a location is allocated, then progress.
`closed_type_safety` (lines 2248–2252) specialises it to the empty heap.

Compare [SystemFMuState.type_safety](#/node/SystemFMuState.type_safety). The semantic version covers fewer
programs, because its references are first-order, but its method extends to programs that are safe without being
well typed (MutBit.lean).
""",
 [q("Can references hold functions in `SystemFMuState.Syn`?",
    ["Yes; `ref A` takes any type there", "No"], 0,
    "TypeSystems/SystemFMuState/TypeSafety.lean lines 23–36."),
  q("What is the conclusion for each reachable state?",
    ["A value, or it can step", "A value", "It terminates"], 0,
    "Line 2235."),
  q("Is this the same typing judgement as in `SystemFMuState.type_safety`?",
    ["No; `Syn` has its own types and a heap typing", "Yes"], 0,
    "It lives in the `SystemFMuState.Syn` namespace (TypeSafety.lean lines 11–14)."),
 ])

node("SystemFMuState.Expr",
 "Expressions with recursion and state",
 "System F's expressions plus roll and unroll for recursive types, and new, load and store for references. Location literals exist as values, but no typing rule accepts them in source programs.",
 r"""## Plain English

**Definition (`SystemFMuState.Expr`, TypeSystems/SystemFMuState/Lang.lean lines 62–90).** The
[System F](#/node/SystemF.Expr) constructs (literals, variables, λ, application, operators, if, type abstraction
and application, pack and unpack, pairs and sums), plus:

- **roll** and **unroll** (lines 83–85), which fold and unfold a recursive type;
- **new**, **load** and **store** (lines 86–89): allocate a fresh cell with a given content, read a cell, and
  overwrite a cell.

A heap (line 181) maps locations to optional values. Reduction is on expression–heap pairs.
""",
 [q("Which constructs act on the heap?",
    ["new, load and store", "roll and unroll", "pack and unpack"], 0,
    "TypeSystems/SystemFMuState/Lang.lean lines 86–89."),
  q("What does unroll do?",
    ["Unfolds a value of a recursive type", "Reads a reference", "Undoes the last store"], 0,
    "Lines 83–85: roll and unroll fold and unfold isorecursive types."),
  q("Does the expression language have a built-in fixpoint operator?",
    ["No; recursion comes from recursive types, e.g. the Z combinator", "Yes, `fix`"], 0,
    "No `fix` constructor appears in lines 62–90. See TypeSystems/SystemFMu/ZCombinator.lean."),
 ])

node("SystemFMuState.Expr.isVal",
 "Being a value",
 "An expression is a value when it is a literal, a λ, a type abstraction, or a package, pair, injection or roll built from values. This is what the safety theorem promises a finished run ends in.",
 r"""## Plain English

**Definition (`SystemFMuState.Expr.isVal`, TypeSystems/SystemFMuState/Lang.lean lines 131–140).** Literals
(including location literals), λs and type abstractions are values. Packages, injections and rolls are values
when their content is, and pairs when both components are. Nothing else is a value.

The doc comment (lines 128–130) says this agrees with being the image of the value type. The predicate is spelled
out structurally so that proofs can take it apart easily.
""",
 [q("Is `roll (1 + 2)` a value?",
    ["No; roll is only a value around a value", "Yes, roll always is"], 0,
    "TypeSystems/SystemFMuState/Lang.lean line 139."),
  q("Is `load l` a value?",
    ["No; it must still step", "Yes"], 0,
    "Only the listed forms are values (line 140)."),
  q("Is a λ with an arbitrary body a value?",
    ["Yes", "Only if the body is a value"], 0,
    "λ is listed as a value with no condition on its body (line 133)."),
 ])
