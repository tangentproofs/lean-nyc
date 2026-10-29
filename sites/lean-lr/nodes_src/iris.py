NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]

IRIS = "https://github.com/leanprover-community/iris-lean/blob/728a17140939e49af9236f7cb0d037da9ec52435/Iris/Iris"


# ---------------------------------------------------------------- headline: concurrency

node("ProgramLogics.ConcurrentLogRel.syn_soundness_not_stuck",
 "Headline: in a well-typed concurrent program, no thread ever gets stuck",
 "Run a closed, well-typed program of a concurrent language with polymorphism, recursive types, higher-order references, fork and compare-and-swap, from any initial state. Under any interleaving, every thread in every reachable pool is a value or can step. No side conditions.",
 r"""## Plain English

**Theorem (`ProgramLogics.ConcurrentLogRel.syn_soundness_not_stuck`, ProgramLogics/ConcurrentLogRel/Adequacy.lean
lines 45–48).** Let *e* be a closed expression of iris-lean's HeapLang with type *A*, under the
[concurrent typing rules](#/node/ProgramLogics.ConcurrentLogRel.SynTyped), with no type variables and an empty
context. Start a thread pool containing just *e* in any state σ, and let it take any number of steps, each step
executed by any thread, including threads created by `fork` along the way. Then every thread *e′* in the
resulting pool is **not stuck**: it is a value, or it can take a step in the current state.

### What the types cover

The type language ([LogRel.Ty](#/node/ProgramLogics.LogRel.Ty)) is the full Chapter 7 language: polymorphism (∀, ∃),
recursive types μ, products, sums, and **references to any type**, including functions and other references.
Chapter 10 adds two rules: **fork** and **compare-and-swap** (CmpXchg) at "comparable" types.

### How it is proved

This is where the course leaves pure type theory. Types are interpreted in the **Iris** separation logic
([semTyped](#/node/ProgramLogics.ConcurrentLogRel.semTyped)). An expression is good at *A* when Iris's weakest
precondition guarantees it runs safely and returns a value satisfying *A*'s interpretation. A reference is good
when an Iris **invariant** says that its location always holds a good value. The
[fundamental theorem](#/node/ProgramLogics.ConcurrentLogRel.fundamental) shows that typed terms are good. Then
iris-lean's own adequacy theorem for HeapLang turns "the weakest precondition holds" into the operational
statement "no reachable thread is stuck" (lines 26–35).

### Compared with the sequential chapter

The Chapter 7 version, [LogRel.syn_soundness_not_stuck](#/node/ProgramLogics.LogRel.syn_soundness_not_stuck), is
built on the course's sequential weakest precondition and takes an extra **no-fork** hypothesis. This concurrent
version uses the concurrent weakest precondition and needs no such condition (lines 6–8).
""",
 [q("Which initial states does the theorem allow?",
    ["Any state σ", "Only the empty heap", "Only heaps well typed for the program"], 0,
    "σ is arbitrary (ProgramLogics/ConcurrentLogRel/Adequacy.lean line 45). A typed program can't mention a location literal, so the initial heap is irrelevant to it."),
  q("What does 'not stuck' mean for a thread?",
    ["It is a value or it can take a step", "It terminates", "It holds no locks"], 0,
    "iris-lean's `NotStuck`: the expression converts to a value, or is reducible in the current state."),
  q("Does the theorem need a hypothesis that the program never forks?",
    ["No. The concurrent weakest precondition handles forked threads", "Yes, like the Chapter 7 version"], 0,
    "Lines 45–47 have only typing, a run and membership in the pool. Compare ProgramLogics/LogRel/Adequacy.lean lines 48–52."),
  q("Can references in this language hold functions?",
    ["Yes; `ref A` takes any type", "No, only first-order values"], 0,
    "ProgramLogics/LogRel/Syntactic.lean line 36. This is unlike the first-order references of SystemFMuState."),
 ],
 caveats=["The last step of the proof is iris-lean's `heap_adequacy`, which is outside this repository. A text search of iris-lean at the pinned revision (728a171) finds no active `sorry` and no `axiom`, but its proofs were not checked either.",
          "Nothing is said about termination or about the values the threads produce; 'not stuck' is the whole conclusion."],
 widgets=walk("How the proof goes (ProgramLogics/ConcurrentLogRel/Adequacy.lean, lines 26-48)", [
  {"text": "Fundamental theorem: the syntactically typed e is semantically typed, for every Iris instance (lines 38–42).", "link": "ProgramLogics.ConcurrentLogRel.fundamental"},
  {"text": "soundness: start iris-lean's heap_adequacy, whose premise is a weakest precondition for e (line 29)."},
  {"text": "Instantiate semantic typing with the empty context, the empty value map and an environment sending every type variable to the empty type (lines 21–23, 31–33).", "link": "ProgramLogics.ConcurrentLogRel.semTyped"},
  {"text": "The expression interpretation is exactly a weakest precondition. Weaken its postcondition to True (lines 34–35)."},
  {"text": "heap_adequacy yields the 'adequate, not stuck' record; read off its not-stuck field for the given run and thread (line 48)."},
 ]))


# ---------------------------------------------------------------- headline: ReLoC

node("ProgramLogics.Reloc.refines_sound",
 "Headline: ReLoC refinement soundness (CONDITIONAL, condition unsatisfiable)",
 "Meant: if e refines e′ in the ReLoC relational logic, then e contextually refines e′. As written, the theorem also assumes no execution of any context around e ever forks, and some context does fork, so the statement is vacuous. CONDITIONAL, on a condition that cannot hold.",
 r"""## Plain English

**Theorem (`ProgramLogics.Reloc.refines_sound`, ProgramLogics/Reloc/ContextualRefinement.lean lines 434–449).**
It has two hypotheses about closed HeapLang programs *e* (the implementation) and *e′* (the specification) at a
closed type *A*:

1. **Refinement in ReLoC:** for every interpretation of type variables, *e* [refines](#/node/ProgramLogics.Reloc.refines)
   *e′* at *A*. This is an Iris proof that, step by step, *e* can be matched by *e′*, ending in values related at *A*;
2. **No forking:** for **every** program context *K*, every initial state, and every reachable thread pool from
   *K*[*e*], the pool has exactly one thread (lines 436–437).

The conclusion is **contextual refinement** ([ctxRefines](#/node/ProgramLogics.Reloc.ctxRefines)): in every *typed*
context, if *K*[*e*] runs to a value, then *K*[*e′*] also runs to a value.

### CONDITIONAL, and the condition cannot hold

Hypothesis 2 quantifies over **all** contexts *K* of the [context syntax](#/node/ProgramLogics.Reloc.TypedCtx), not
only the typed ones. Contexts may contain arbitrary HeapLang expressions, and HeapLang has a `fork` instruction.
Take the one-frame context "a pair whose first component is the hole and whose second component is `fork` applied
to the unit value". HeapLang evaluates the components of a pair **right to left**
([iris-lean Semantics.lean, the pair evaluation contexts](""" + IRIS + r"""/HeapLang/Semantics.lean#L30-L31)), so the first
step from any state runs the fork, which adds a thread
([the fork rule](""" + IRIS + r"""/HeapLang/Semantics.lean#L436-L437)). The pool then has two threads. This
happens whatever *e* is.

So no *e* satisfies hypothesis 2, and the theorem is true for the trivial reason that its assumptions are never
met. The same applies to `refines_sound_open` (lines 423–432), which has the same hypothesis. The fix is probably
small: restrict hypothesis 2 to **typed** contexts. The Chapter 7 type system has no fork rule, so a typed context
plausibly never forks, though the repository doesn't prove this.

### What *is* usable

The underlying machinery is not affected:

- [refines_sound_open's](#/node/ProgramLogics.Reloc.refines_sound_open) other ingredient,
  `log_related_under_typed_ctx` (lines 284–322), is the real precongruence argument;
- `logrel_adequate` (lines 387–404) and `F_mu_ref_typesafety` (lines 483–487) take a no-fork hypothesis about **one**
  program only. That hypothesis can hold, though the repository never discharges it for any program.

This site's analysis has **not** been checked by building or running Lean. See the review page.
""",
 [q("What does contextual refinement, the conclusion, promise?",
    ["In every typed context, if the implementation terminates with a value, so does the specification", "The two programs return equal values in every context", "The implementation never forks"], 0,
    "`ctxRefines` (ProgramLogics/Reloc/ContextualRefinement.lean lines 253–259)."),
  q("Over which contexts does the no-fork hypothesis quantify?",
    ["All syntactic contexts, typed or not", "Only typed contexts", "Only the empty context"], 0,
    "Lines 436–437 quantify over every `K : Ctx` with no typing condition."),
  q("Why can no program satisfy that hypothesis?",
    ["A context can contain a fork that runs before the hole is even evaluated", "Because ReLoC requires forking", "Because the empty context forks"], 0,
    "Pairing the hole with `fork` of unit forks on the first step, since HeapLang evaluates pairs right to left."),
  q("What would most likely repair the statement?",
    ["Requiring no-fork only for typed contexts, which cannot contain fork in the Chapter 7 type system", "Removing the refinement hypothesis", "Allowing more threads"], 0,
    "The conclusion only quantifies over typed contexts (line 256), so the hypothesis only needs to cover those."),
 ],
 caveats=["CONDITIONAL, on a condition that is never met: the theorem assumes that no execution of any context around e ever forks (lines 436–437). The argument above shows that this assumption is never satisfied, which makes the statement vacuously true. This is the site's own analysis, made by reading the source. It was not checked in Lean.",
          "The upstream Rocq course has no such hypothesis. According to comments in the port (ProgramLogics/SeqAdequacy.lean lines 18–21), the no-fork condition comes from building the sequential adequacy theorem on iris-lean's concurrent machinery. The port refers to a CORRESPONDENCE.md §5.12 for details, but that file is not in the repository at the pinned commit."],
 widgets=walk("How the proof goes (ProgramLogics/Reloc/ContextualRefinement.lean, lines 423-449)", [
  {"text": "refines_sound reduces to refines_sound_open by turning the closed refinement into semantic typing in the empty context (lines 439–449).", "link": "ProgramLogics.Reloc.refines_sound_open"},
  {"text": "In the empty context, the context interpretation forces the value map to be empty (line 443), so the substitutions vanish (lines 445–447)."},
  {"text": "The refinement hypothesis then closes the goal (lines 448–449).", "link": "ProgramLogics.Reloc.refines"},
  {"text": "refines_sound_open: given a typed context K and a terminating run of K[e] (line 428)…", "link": "ProgramLogics.Reloc.ctxRefines"},
  {"text": "…the relation is closed under typed contexts, so K[e] and K[e′] are related at the context's result type (log_related_under_typed_ctx, line 431).", "link": "ProgramLogics.Reloc.TypedCtx"},
  {"text": "logrel_simul, using adequacy and the no-fork hypothesis for this K, gives a run of K[e′] to a value (lines 429–432)."},
 ]))


# ---------------------------------------------------------------- statement set: concurrent

node("ProgramLogics.LogRel.Ty",
 "Types of the Iris-based chapters",
 "The type language shared by Chapters 7, 8 and 10: type variables, int, bool, unit, ∀, ∃, functions, recursive types μ, references to any type, products and sums.",
 r"""## Plain English

**Definition (`ProgramLogics.LogRel.Ty`, ProgramLogics/LogRel/Syntactic.lean lines 27–39).** The same types as
[SystemFMuState](#/node/SystemFMuState.Ty), with one big difference: **`ref A` takes any type *A*.** References to
functions or to other references are allowed. Interpreting such types needs the impredicative invariants of Iris,
which is why these chapters work in Iris rather than in plain Lean predicates.

The programs are not a custom language. They are **iris-lean's HeapLang**, with polymorphism encoded by
helper definitions (`tApp`, `tLam`, `pack`, `unpack`, `roll`, `unroll`; see ProgramLogics/LogRel/Notation.lean).
The ReLoC chapter ([Reloc](#/node/ProgramLogics.Reloc.refines_sound)) and the concurrent chapter
([ConcurrentLogRel](#/node/ProgramLogics.ConcurrentLogRel.SynTyped)) reuse these types.
""",
 [q("Can `ref (fn int int)` be written in this type language?",
    ["Yes; references may hold any type", "No"], 0,
    "ProgramLogics/LogRel/Syntactic.lean line 36."),
  q("What language are programs written in?",
    ["iris-lean's HeapLang, with polymorphism encoded by helpers", "A custom System F syntax", "Rocq"], 0,
    "The chapter files work over HeapLang expressions; see ProgramLogics/LogRel/Notation.lean."),
  q("Is μ present?",
    ["Yes", "No"], 0,
    "`mu` is a constructor (ProgramLogics/LogRel/Syntactic.lean line 35)."),
 ])

node("ProgramLogics.ConcurrentLogRel.SynTyped",
 "Typing rules for the concurrent language",
 "Chapter 7's typing rules for HeapLang, plus fork (any well-typed expression can be forked, giving unit) and compare-and-swap at comparable types. It is the hypothesis of the concurrent safety headline.",
 r"""## Plain English

**Definition (`ProgramLogics.ConcurrentLogRel.SynTyped`, ProgramLogics/ConcurrentLogRel/Syntactic.lean lines 105–206).**
The judgement *n*; Γ ⊢ *e* : *A* over HeapLang expressions has the Chapter 7 rules: variables, λ (via HeapLang's
recursive functions), application, type abstraction and application, pack/unpack, literals, operators, if,
pairs, sums, roll/unroll, and allocation, load and store at any type. The two new rules are:

- **fork** (lines 198–200): if *e* has some type, then `fork e` has type `unit`;
- **compare-and-swap** (lines 201–206): on a `ref A` with expected and new values of type *A*, it returns a pair of
  the old value and a success flag. *A* must be **comparable** (lines 97–99): unit, int, bool or a reference, or a
  sum of two of those. HeapLang can only compare such values atomically (lines 88–89).
""",
 [q("What type does `fork e` have?",
    ["unit, provided e is well typed", "The type of e", "ref of the type of e"], 0,
    "ProgramLogics/ConcurrentLogRel/Syntactic.lean lines 198–200."),
  q("Can compare-and-swap be used on a reference to a function?",
    ["No; function types are not comparable", "Yes"], 0,
    "`ComparableLit` and `Comparable` (lines 91–99) only allows unit, int, bool, references and sums of those."),
  q("What does compare-and-swap return?",
    ["A pair of the old value and a boolean success flag", "unit", "The new value"], 0,
    "Its type is `.prod A .bool` (line 206)."),
 ])

node("ProgramLogics.ConcurrentLogRel.semTyped",
 "Semantic typing in Iris (concurrent)",
 "An open term is semantically typed when, in Iris, for every interpretation of type variables and every map of variables to values satisfying the context, the substituted term's weakest precondition guarantees a result satisfying the type's interpretation.",
 r"""## Plain English

**Definition (`ProgramLogics.ConcurrentLogRel.semTyped`, ProgramLogics/ConcurrentLogRel/LogRel.lean lines 428–431).**
Γ ⊨ *e* : *A* is the Iris entailment "⊢ for all δ and γ, if γ satisfies Γ under δ, then **WP** γ(*e*) {*A* under δ}".

The pieces:

- a **semantic type** (line 34) is a *persistent* Iris predicate on values: once true, it stays true and can be
  shared between threads;
- the **expression interpretation** (line 58) is Iris's concurrent weakest precondition: *e* is safe to run (it
  never gets stuck, in any thread it forks) and if it returns, the value satisfies the type;
- the **type interpretation** (`typeInterp`, from line 72): a function value must, for every good argument, have a
  good application. ∀ quantifies over semantic types. μ is a guarded fixpoint, with an Iris "later" ▷ in
  place of an explicit step index. **A reference to *A* is a location governed by an Iris invariant** saying it
  always holds a good *A* value (lines 95–97);
- the **context interpretation** (lines 377–378) requires each variable's value to satisfy its type.
""",
 [q("Which construct makes the expression interpretation a safety guarantee?",
    ["Iris's weakest precondition", "Big-step evaluation", "A step-indexed Lean predicate"], 0,
    "`exprInterp` is a WP (ProgramLogics/ConcurrentLogRel/LogRel.lean line 58)."),
  q("How is a reference to A interpreted?",
    ["A location with an Iris invariant that it always holds a value good at A", "A location currently holding a good value, with no invariant", "Any location"], 0,
    "`refInterp` (lines 95–97)."),
  q("Why must semantic types be persistent?",
    ["So that facts about values can be duplicated and shared, e.g. between threads", "For decidability", "They need not be"], 0,
    "A semantic type is a `PersistentPred` (line 34)."),
 ])

node("ProgramLogics.ConcurrentLogRel.fundamental",
 "Fundamental theorem for the concurrent language",
 "Every term typed by the concurrent rules is semantically typed in Iris. This includes the two new cases: fork, using the concurrent weakest precondition's fork rule, and compare-and-swap, using the reference invariant around one atomic step.",
 r"""## Plain English

**Theorem (`ProgramLogics.ConcurrentLogRel.fundamental`, ProgramLogics/ConcurrentLogRel/LogRel.lean lines 1043–1073).**
If *n*; Γ ⊢ *e* : *A* by the [concurrent rules](#/node/ProgramLogics.ConcurrentLogRel.SynTyped), then
Γ ⊨ *e* : *A* ([semantic typing](#/node/ProgramLogics.ConcurrentLogRel.semTyped)).

Induction on the typing derivation, one compatibility lemma per rule (lines 1046–1073). Compared with the
sequential Chapter 7 proof, the reference invariant is opened around **a single atomic step** (a load, a store or
a compare-and-swap), not around a whole sequential block (lines 11–14). That is what makes the proof sound for
interleaved threads. The file also proves three ADTs semantically typed (ProgramLogics/ConcurrentLogRel/Adts.lean):
a counter, a channel and a symbol generator.
""",
 [q("How long may a thread keep the reference invariant open in this proof?",
    ["Only around one atomic step", "For an entire sequential block", "Forever"], 0,
    "ProgramLogics/ConcurrentLogRel/LogRel.lean lines 11–14."),
  q("What is the proof technique?",
    ["Induction on the typing derivation with one compatibility lemma per rule", "Model checking all interleavings"], 0,
    "Lines 1045–1073."),
  q("Which two cases are new relative to Chapter 7?",
    ["fork and compare-and-swap", "load and store", "pack and unpack"], 0,
    "Lines 1071–1073."),
 ])

node("ProgramLogics.LogRel.syn_soundness_not_stuck",
 "Chapter 7 safety, CONDITIONAL on fork-freedom",
 "Chapter 7's version of the safety theorem: a closed well-typed program never has a stuck thread. It assumes that the run never forks. Typed Chapter 7 programs cannot contain fork, but the port doesn't prove that they satisfy this assumption.",
 r"""## Plain English

**Theorem (`ProgramLogics.LogRel.syn_soundness_not_stuck`, ProgramLogics/LogRel/Adequacy.lean lines 48–52).** If *e*
is closed and typed by the Chapter 7 rules (no fork, no compare-and-swap), **and every reachable thread pool from
([e], σ) has exactly one thread**, then no thread in any reachable pool is stuck.

**CONDITIONAL.** The second hypothesis is the "no fork" side condition the doc comment mentions (lines 10–11).
It comes from the port's sequential weakest precondition, whose adequacy theorem `heap_swp_adequacy`
(ProgramLogics/SeqAdequacy.lean lines 320–350) needs it. Unlike the [ReLoC](#/node/ProgramLogics.Reloc.refines_sound)
version, this hypothesis concerns one program and can be satisfied. A typed Chapter 7 program contains no `fork`,
so it should hold for every typed program, but the repository doesn't prove that. The
[concurrent version](#/node/ProgramLogics.ConcurrentLogRel.syn_soundness_not_stuck) removes the condition altogether.
""",
 [q("What extra hypothesis does the Chapter 7 version have?",
    ["Every reachable thread pool has exactly one thread", "The heap starts empty", "The program terminates"], 0,
    "ProgramLogics/LogRel/Adequacy.lean line 50."),
  q("Is that hypothesis proved for well-typed programs anywhere in the repo?",
    ["No, it is left to the user", "Yes, by a lemma in Syntactic.lean"], 0,
    "No lemma discharges it. The concurrent chapter avoids it instead."),
  q("Is the hypothesis satisfiable?",
    ["Yes, e.g. by programs that never execute fork", "No, never"], 0,
    "It mentions only the one program e, unlike ReLoC's hypothesis over all contexts."),
 ],
 caveats=["CONDITIONAL on fork-freedom of the run (line 50)."])


# ---------------------------------------------------------------- statement set: ReLoC

node("ProgramLogics.Reloc.refines",
 "ReLoC's refinement judgement",
 "e refines e′ at Ψ: for every evaluation context K around the source e′, running e safely (sequential weakest precondition) can be matched by running K[e′] to K[v′], with the final values related by Ψ. The source program is tracked as Iris ghost state.",
 r"""## Plain English

**Definition (`ProgramLogics.Reloc.refines`, ProgramLogics/Reloc/LogRel.lean lines 57–59).** For every evaluation
context *K*: if the ghost state records that the *source* (specification) thread is currently *K*[*e′*], then the
sequential weakest precondition of the *target* *e* holds, with the postcondition "the source has reached
*K*[*v′*] for some *v′* with Ψ(*v*, *v′*)".

The source program is not run by the machine. It is simulated in the logic: the proof steps it forward by
updating ghost state, using the rules of ProgramLogics/Reloc/SrcRules.lean. A refinement proof is therefore a
proof that every behaviour of *e* can be **simulated** by *e′*.

Semantic typing for pairs of open terms (`Reloc.semTyped`, ProgramLogics/Reloc/Fundamental.lean lines 312–317)
lifts this to contexts, and the ReLoC fundamental theorem (lines 882–909) shows every typed term refines itself.
""",
 [q("Which program actually runs in the weakest precondition?",
    ["The target e", "The source e′", "Both, in parallel"], 0,
    "`swp … e …` (ProgramLogics/Reloc/LogRel.lean line 59). The source is tracked in ghost state."),
  q("What does the postcondition require?",
    ["The source has stepped to a value related to the target's value by Ψ", "The two values are equal", "Nothing"], 0,
    "The postcondition of the WP (ProgramLogics/Reloc/LogRel.lean line 59)."),
  q("Why quantify over evaluation contexts K around the source?",
    ["So that refinement composes when the source is part of a larger computation", "To allow forking", "It's a technicality with no purpose"], 0,
    "This is the standard ReLoC formulation; it is what makes the bind rules (lines 75–88) work."),
 ])

node("ProgramLogics.Reloc.ctxRefines",
 "Contextual refinement",
 "e contextually refines e′ at A if, for every typed program context K producing a closed program, whenever K[e] runs (as a single thread) to a value from a state, K[e′] also runs to some value from that same state.",
 r"""## Plain English

**Definition (`ProgramLogics.Reloc.ctxRefines`, ProgramLogics/Reloc/ContextualRefinement.lean lines 253–259).**
For every context *K* that is [typed](#/node/ProgramLogics.Reloc.TypedCtx) from holes (*n*, Γ, *A*) to a closed
program of some type *B*, every initial state σ₀ (of the standard shape), and every value *v₁*: if *K*[*e*] reduces
to *v₁*, then *K*[*e′*] reduces to **some** value *v₂*.

Two details:

- the steps are single-thread steps (`ThreadStep`), and termination is the only observation;
- the result values are not compared. For first-order result types they would have to be equal by
  `ObsType_soundness` (lines 341–374), but the definition doesn't ask for this.

The relation is reflexive and transitive (lines 261–266).
""",
 [q("What does contextual refinement observe?",
    ["Whether the program terminates with a value", "The exact value returned", "The final heap"], 0,
    "ProgramLogics/Reloc/ContextualRefinement.lean lines 257–259."),
  q("Are the contexts typed?",
    ["Yes; `TypedCtx K n Γ A 0 ∅ B` is required", "No"], 0,
    "The `TypedCtx` premise (ProgramLogics/Reloc/ContextualRefinement.lean line 256)."),
  q("Is it symmetric?",
    ["No. If K[e] terminates then K[e′] must; not the converse", "Yes"], 0,
    "It is a refinement (a preorder), not an equivalence."),
 ])

node("ProgramLogics.Reloc.TypedCtx",
 "Program contexts and their typing (ReLoC)",
 "A program context is a list of frames, each one HeapLang constructor with a hole in one position. Frames may carry arbitrary HeapLang subexpressions, including fork. TypedCtx types a context frame by frame, using the Chapter 7 rules for the subexpressions.",
 r"""## Plain English

**Definitions (ProgramLogics/Reloc/ContextualRefinement.lean lines 24–197).** `CtxItem` (lines 24–53) lists the
frames: λ, application (hole on either side), operators, if (three positions), pairs (two positions),
projections, injections, case, allocation, load, store, roll/unroll, type abstraction, application and
pack/unpack. Frames carry **arbitrary** HeapLang expressions as the other subterms. `fillCtx` (line 90) plugs an
expression into a list of frames.

`TypedCtx K n Γ A n′ Γ′ B` (lines 191–197) types the context frame by frame (`TypedCtxItem`, from line 102). The
other subterms must be typed by the Chapter 7 judgement, which has **no** rule for fork. So a typed context cannot
contain `fork`, but an untyped `Ctx` can. This distinction is what goes wrong in the
[refines_sound headline](#/node/ProgramLogics.Reloc.refines_sound).
""",
 [q("Can an untyped `Ctx` contain a fork?",
    ["Yes; frames carry arbitrary HeapLang expressions", "No"], 0,
    "e.g. the `pairL` frame carries any expression as the second component (ProgramLogics/Reloc/ContextualRefinement.lean line 34)."),
  q("Can a *typed* context contain a fork?",
    ["Not via the Chapter 7 typing rules, which have no fork rule", "Yes"], 0,
    "`TypedCtxItem` uses `LogRel.SynTyped` for subterms (from line 102)."),
  q("How does `fillCtx` combine frames?",
    ["By folding them around the expression, innermost frame last in the list", "By sequencing them"], 0,
    "`K.foldr fillCtxItem e` (line 90)."),
 ])

node("ProgramLogics.Reloc.refines_sound_open",
 "Refinement soundness for open terms (same unsatisfiable hypothesis)",
 "If e and e′ are related by ReLoC's semantic typing under Γ, then e contextually refines e′, again assuming that no context around e can fork. The proof is genuine, but the assumption is unsatisfiable, as for the headline.",
 r"""## Plain English

**Theorem (`ProgramLogics.Reloc.refines_sound_open`, ProgramLogics/Reloc/ContextualRefinement.lean lines 423–432).**
Assume (1) Γ ⊨ *e* ≤ *e′* : *A* in ReLoC for every Iris instance, and (2) for every context *K* and every initial
state, every run of *K*[*e*] keeps a single thread. Then *e* [contextually refines](#/node/ProgramLogics.Reloc.ctxRefines) *e′*.

The proof is the real content of the chapter:

1. `log_related_under_typed_ctx` (lines 284–322): the logical relation is preserved by every typed context, a
   precongruence proved frame by frame;
2. `logrel_simul` (lines 414–421): adequacy for the binary relation. If the target runs to a value, so does the
   source. It rests on `refines_adequate` (ProgramLogics/Reloc/Adequacy.lean lines 38–97).

Hypothesis (2) is only used for the particular *K* at hand (line 431). As explained under the
[headline](#/node/ProgramLogics.Reloc.refines_sound), it cannot hold for all *K*. If it were restricted to typed
contexts, the proof above would apparently go through unchanged, since it only ever uses the hypothesis at the
typed *K* it is given.
""",
 [q("At which contexts does the proof actually use the no-fork hypothesis?",
    ["Only at the typed context K given to it", "At every context", "Never"], 0,
    "`Hnf K σ₀` on line 431."),
  q("What does `log_related_under_typed_ctx` show?",
    ["Related terms stay related when placed in the same typed context", "Typed contexts never fork", "Refinement is symmetric"], 0,
    "ProgramLogics/Reloc/ContextualRefinement.lean lines 284–287."),
  q("Is this theorem usable as stated?",
    ["No: its no-fork hypothesis over all contexts cannot be met", "Yes, for any fork-free e"], 0,
    "A context that forks before evaluating the hole refutes the hypothesis for every e."),
 ],
 caveats=["CONDITIONAL, on the same unsatisfiable no-fork hypothesis as refines_sound (lines 425–426)."])
