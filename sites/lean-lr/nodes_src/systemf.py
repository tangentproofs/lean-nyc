NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]


# ---------------------------------------------------------------- headlines

node("SystemF.all_identity",
 "Headline: free theorem — every closed ∀α. α → α is the identity",
 "If a closed System F program has type ∀α. α → α, then instantiating it and applying it to any closed value v₀ evaluates to v₀ itself. Nobody inspects the program's code: parametricity alone forces it.",
 r"""## Plain English

**Theorem (`SystemF.all_identity`, TypeSystems/SystemF/FreeTheorems.lean lines 27–44).** Let *e* be a
[System F](#/node/SystemF.Expr) expression with type ∀α. α → α in the empty context with no type variables in
scope ([typing](#/node/SystemF.SynTyped)). Let *v₀* be **any** value whose expression has no free variables.
Then the program "instantiate *e* at a type, then apply it to *v₀*" evaluates ([big-step](#/node/SystemF.BigStep))
to *v₀*.

### Why this is surprising

The theorem never looks at *e*. It could be Λα. λ*x*. *x*, or something convoluted that computes a lot before
returning. The type alone guarantees the behaviour. The intuition is Reynolds' parametricity: a function that
works uniformly *for every* type α has no way to inspect or produce an α. All it can do is hand back the α it
was given.

### How the logical relation captures this

The [value relation](#/node/SystemF.valRel) interprets ∀α. *A* by quantifying over **all semantic types** τ:
arbitrary sets of closed values, not just the sets that syntactic types denote. The proof picks the
singleton τ = {*v₀*}. Read with α := {*v₀*}, the relation for α → α says that the function maps members of {*v₀*}
to results in {*v₀*}. The result must therefore be *v₀*.

### A detail worth noticing

*v₀* is not required to be well typed, only closed. The singleton semantic type can hold any closed value, so the
theorem also covers inputs the type system could never give a type to.

The companion theorem [not_every_type_inhabited](#/node/SystemF.not_every_type_inhabited) uses the *empty*
semantic type to show that no closed term has type ∀α. α.
""",
 [q("What does `all_identity` assume about the argument *v₀*?",
    ["Only that it is a closed value", "That it has some closed type", "That it is an integer", "That it has type α"], 0,
    "The hypotheses are a value *v₀* and closedness of its expression (TypeSystems/SystemF/FreeTheorems.lean line 30). No typing is required."),
  q("Which semantic type does the proof instantiate α with?",
    ["The singleton {v₀}", "The empty set", "All closed values", "The integers"], 0,
    "Line 38 builds the semantic type whose only member is *v₀*."),
  q("Does the theorem say that *e* is syntactically equal to Λα. λx. x?",
    ["No. It says how *e* behaves when instantiated and applied", "Yes", "Only up to renaming"], 0,
    "The conclusion is a big-step evaluation to *v₀* (line 31), a statement about behaviour."),
  q("Why can't this proof go through with a value relation where ∀ ranges only over syntactic types?",
    ["{v₀} is generally not the meaning of any syntactic type; the proof needs the freedom to pick it", "It can; the choice doesn't matter"], 0,
    "The ∀ case quantifies over every `SemType` (TypeSystems/SystemF/LogRel.lean lines 77–79), and the proof relies on that."),
 ],
 caveats=["'Is the identity' means: after one type application, applying the result to a closed value evaluates to that value. It says nothing about open arguments, or about what happens without the type application."],
 widgets=walk("How the proof goes (TypeSystems/SystemF/FreeTheorems.lean, lines 27-44)", [
  {"text": "By the fundamental theorem, e is semantically typed at ∀α. α → α (line 32).", "link": "SystemF.sem_soundness"},
  {"text": "Instantiate with the empty substitution and a dummy interpretation of type variables: e evaluates to a value v in the relation (lines 33–34).", "link": "SystemF.valRel"},
  {"text": "Unfold the ∀ case: v is a type abstraction Λ. e′ with e′ closed, and for every semantic type τ, e′ evaluates to a value related at α → α under α := τ (lines 35–36)."},
  {"text": "Choose τ to be the singleton {v₀}. This is allowed because v₀ is closed (line 38)."},
  {"text": "So e′ evaluates to a λ that maps members of {v₀} to results in {v₀} (lines 39–40)."},
  {"text": "Apply it to v₀, which is in the singleton: the body evaluates to some u in {v₀}, so u = v₀ (lines 41–43)."},
  {"text": "Assemble the big-step derivation: type application, then application to v₀, which yields v₀ (line 44).", "link": "SystemF.BigStep"},
 ]))

node("SystemF.Binary.soundness_wrt_ctx_equiv",
 "Headline: logically related System F programs are contextually equivalent",
 "If two System F expressions are related by the binary logical relation, then no well-typed program context can tell them apart: plugged into any closed integer-valued context, they produce the same integer.",
 r"""## Plain English

**Theorem (`SystemF.Binary.soundness_wrt_ctx_equiv`, TypeSystems/SystemF/BinaryLogRel.lean lines 1244–1247).**
Let *e₁* and *e₂* both have type *A* under Δ type variables and the context Γ. Suppose they are related by the
binary logical relation at *A* ([Binary.semTyped](#/node/SystemF.Binary.semTyped)). Then they are
**contextually equivalent** ([ctx_equiv](#/node/SystemF.Binary.ctx_equiv)). For every
[typed program context](#/node/SystemF.Binary.PctxTyped) *K* that turns a hole of type *A* into a closed program
of type `int`, the programs *K*[*e₁*] and *K*[*e₂*] evaluate to the **same** integer.

### Why this matters

Contextual equivalence is the gold-standard notion of "these two programs are interchangeable". It is also very
hard to prove directly, because it quantifies over every possible surrounding program. The binary logical
relation gives a *compositional* way to establish it. Prove the two expressions related, type by type, and
contextual equivalence follows. For example, this is how two implementations of an abstract data type hidden
behind an existential can be shown interchangeable.

### What the theorem does *not* do

- It does **not** produce the relatedness. That is the hypothesis, and you must prove it for your particular
  pair, e.g. with the compatibility lemmas and some reasoning about evaluation. ChurchEncodingsFaithful.lean
  uses the binary relation this way.
- The two typing hypotheses are not used in the proof (TypeSystems/SystemF/BinaryLogRel.lean line 1245: they are
  named with a leading underscore). The real work is in `sem_typing_ctx_equiv` (lines 1235–1242). They are
  kept to match the course's statement.
- The observation is "same integer". Because System F terminates
  ([termination](#/node/SystemF.termination)), "both terminate" is not an interesting observation here, and
  integers are enough to distinguish anything a context can see.
""",
 [q("What does contextual equivalence observe?",
    ["The integer that a closed int-typed context produces around each expression", "Whether the two expressions are syntactically equal", "Only whether both terminate"], 0,
    "`ctx_equiv` requires both *K*[*e₁*] and *K*[*e₂*] to evaluate to the same integer *z* (TypeSystems/SystemF/BinaryLogRel.lean lines 1229–1232)."),
  q("Are the typing hypotheses of `soundness_wrt_ctx_equiv` needed in its proof?",
    ["No. They are unused; the semantic relatedness alone suffices", "Yes, both are essential", "Only the first one"], 0,
    "They are named `_h₁` and `_h₂` and the proof just calls `sem_typing_ctx_equiv` (lines 1245–1247)."),
  q("Which contexts are quantified over?",
    ["Typed program contexts with a hole anywhere, including under λ, that produce a closed int program", "Only evaluation contexts", "Untyped contexts as well"], 0,
    "`Pctx` places the hole in any position (lines 895–919), and `PctxTyped` types it (lines 949–1057)."),
  q("Does the theorem prove any particular pair of programs equivalent?",
    ["No. It reduces contextual equivalence to proving them logically related", "Yes, all well-typed programs of the same type"], 0,
    "Relatedness is a hypothesis (line 1245)."),
 ],
 caveats=["Contextual equivalence here is only with respect to integer-valued closed contexts and big-step evaluation, the standard choice for a terminating language."],
 widgets=walk("How the proof goes (TypeSystems/SystemF/BinaryLogRel.lean, lines 1235-1247)", [
  {"text": "The headline passes straight through to sem_typing_ctx_equiv, discarding the typing hypotheses (lines 1244–1247)."},
  {"text": "Take a typed context K with a hole of type A that produces a closed int program (line 1237).", "link": "SystemF.Binary.PctxTyped"},
  {"text": "Congruence: the relation is preserved by every context, so K[e₁] and K[e₂] are related at int in the empty context (line 1238).", "link": "SystemF.Binary.sem_typed_congruence"},
  {"text": "Instantiate with the empty substitutions and the dummy interpretation of type variables (lines 1239–1241)."},
  {"text": "Adequacy at int: related int expressions evaluate to the same integer z (line 1242, using lines 1222–1227)."},
 ]))


# ---------------------------------------------------------------- statement set: unary

node("SystemF.Expr",
 "System F expressions and values",
 "System F adds type abstraction and application, existential packages, pairs, sums, booleans, unit and operators to the λ-calculus. Types are erased from the terms: a type application in the program carries no type.",
 r"""## Plain English

**Definition (`SystemF.Expr`, TypeSystems/SystemF/Lang.lean lines 45–66).** Expressions are literals (integers,
booleans, unit), variables, λ, application, unary and binary operators, if-then-else, **type abstraction**
`tLam` and **type application** `tApp`, existential **pack** and **unpack**, pairs with projections, and
sums with injections and `case`.

The doc comment on lines 42–43 states the key design choice: type abstraction, application and packing carry
**no type annotation**. A type application is just "run the body of the type abstraction". This is why
the [free theorem](#/node/SystemF.all_identity) can talk about "instantiate and apply" without naming a type.

Values (`SystemF.Val`, lines 68–75) are literals, λs, type abstractions, packages of values, pairs of values and
injections of values.
""",
 [q("What does a type application `tApp e` carry?",
    ["Nothing but the expression e: types are erased", "The type being applied", "A De Bruijn index"], 0,
    "TypeSystems/SystemF/Lang.lean lines 42–43 and 54."),
  q("Is a type abstraction `tLam e` a value?",
    ["Yes, whatever e is", "Only if e is a value"], 0,
    "`tLamV` is a value constructor (Lang.lean line 71). Its body runs only at a type application."),
  q("Which is NOT in this System F?",
    ["Recursive types (μ)", "Existential packages", "Sum types", "Booleans"], 0,
    "μ arrives in SystemFMu. This language has no general recursion, which is why it terminates."),
 ])

node("SystemF.Ty",
 "System F types",
 "Types are type variables (as De Bruijn indices), int, bool, unit, functions, ∀, ∃, products and sums. ∀ and ∃ bind index 0 in their body.",
 r"""## Plain English

**Definition (`SystemF.Ty`, TypeSystems/SystemF/Types.lean lines 21–31).** A type is a type variable *n* (a
**De Bruijn index**: 0 means the nearest enclosing binder), `int`, `bool`, `unit`, a function type, a universal
type ∀. *A*, an existential type ∃. *A*, a product or a sum.

So ∀α. α → α is written "all of (function from variable 0 to variable 0)". `TypeWf n A` (lines 35–44) says that
every free index in *A* is below *n*: *A* makes sense with *n* type variables in scope.
""",
 [q("How is ∀α. ∀β. α → β written with De Bruijn indices?",
    ["all (all (fn (tVar 1) (tVar 0)))", "all (all (fn (tVar 0) (tVar 1)))"], 0,
    "Index 0 refers to the innermost binder (β), so α is index 1."),
  q("What does `TypeWf 0 A` say?",
    ["A has no free type variables", "A is the type int", "A has exactly one type variable"], 0,
    "Free indices must be below 0, i.e. there are none (Types.lean lines 35–44)."),
  q("Does this type language have recursive types?",
    ["No; μ is added in SystemFMu", "Yes"], 0,
    "Lines 21–31 list the constructors, and there is no μ."),
 ])

node("SystemF.SynTyped",
 "System F typing rules",
 "The judgement n; Γ ⊢ e : A, with n type variables in scope. Under a type abstraction, n grows and the term context's types are shifted. Type application substitutes a well-formed type for the bound variable.",
 r"""## Plain English

**Definition (`SystemF.SynTyped`, TypeSystems/SystemF/Types.lean lines 336–414).** The usual rules for
literals, variables, λ (named and anonymous), application, products, sums, operators and if. The polymorphic
rules are:

- **type abstraction:** if *e* has type *A* with *n* + 1 type variables and the context shifted to match, then
  `tLam e` has type ∀. *A* (lines 358–361);
- **type application:** if *e* : ∀. *A* and *B* is well formed with *n* variables, then `tApp e` has type
  *A*[*B*/0] (lines 362–365);
- **pack / unpack** for existentials (lines 366–377).

`case` takes its two branches as **functions** (lines 396–400): `case e e₁ e₂` applies *e₁* or *e₂* to the
payload. Both headlines about System F use this judgement with *n* = 0 and the empty context, i.e. closed programs.
""",
 [q("What does the first argument *n* of SynTyped count?",
    ["The type variables in scope", "The term variables in scope", "Evaluation steps"], 0,
    "It is the bound for `TypeWf` (e.g. lines 347–348) and grows by one under `tLam` (line 360)."),
  q("In this file, how are the branches of `case` typed?",
    ["As functions from the payload types to the result type", "As bodies with a bound variable"], 0,
    "TypeSystems/SystemF/Types.lean lines 396–400."),
  q("What does type application produce?",
    ["The body type with the applied type substituted for index 0", "The body type unchanged", "A fresh type variable"], 0,
    "`A.subst1 B` (line 365)."),
 ])

node("SystemF.BigStep",
 "System F big-step evaluation",
 "Call-by-value big-step evaluation for System F. Type application runs the body of a type abstraction, unpack substitutes the package contents, and case applies the chosen branch function.",
 r"""## Plain English

**Definition (`SystemF.BigStep`, TypeSystems/SystemF/BigStep.lean lines 18–49).** The relation *e* ⇓ *v* with one
rule per construct. The rules the System F headlines rely on are:

- **application** (lines 26–28): evaluate the function to λ*x*. *e*, the argument to *v₂*, then the body with *v₂*
  substituted;
- **type application** (lines 29–30): evaluate *e₁* to a type abstraction, then evaluate its body;
- **type abstraction** (line 31): it is already a value.

Like the STLC version, this is an inductive relation, so evaluating means *finishing*. A program that loops or
gets stuck has no derivation.
""",
 [q("How does `tApp e` evaluate?",
    ["Evaluate e to a type abstraction tLamV e′, then evaluate e′", "It is already a value", "It substitutes a type into e"], 0,
    "TypeSystems/SystemF/BigStep.lean lines 29–30. Types are erased, so nothing is substituted."),
  q("Does BigStep relate a looping program to anything?",
    ["No; derivations are finite", "Yes, to a special 'divergence' value"], 0,
    "It is an inductive relation."),
  q("How is `case` evaluated?",
    ["Evaluate the scrutinee to an injection, then apply the matching branch to the payload", "Evaluate both branches, then choose"], 0,
    "Lines 46–49."),
 ])

node("SystemF.valRel",
 "System F unary logical relation",
 "The value relation is defined by recursion on the type, relative to an interpretation δ of the type variables as semantic types. Its ∀ case quantifies over every semantic type, any set of closed values at all. That is impredicative, and it is what makes free theorems possible.",
 r"""## Plain English

**Definitions (TypeSystems/SystemF/LogRel.lean lines 27–86).**

A **semantic type** (`SystemF.SemType`, lines 27–29) is a predicate on values that holds only of closed values.
An **interpretation** δ (line 31) gives a semantic type for each type variable.

The **value relation** `valRel δ A v` (lines 64–82):

- `int`, `bool`, `unit`: *v* is a literal of that kind;
- type variable α: *v* is in the semantic type δ(α);
- product, sum: componentwise, as you would expect;
- *A* → *B*: *v* is a closed λ*x*. *e*, and for every *v′* in the relation at *A*, the body with *v′* substituted
  evaluates to a value in the relation at *B*;
- ∀. *A*: *v* is a closed type abstraction Λ. *e*, and **for every semantic type τ**, *e* evaluates to a value in
  the relation at *A* with index 0 interpreted by τ;
- ∃. *A*: *v* is a package of *v′*, and **some** semantic type τ makes *v′* related at *A*.

The **expression relation** `exprRel δ A e` (lines 85–86) means *e* evaluates to a value in `valRel δ A`.

### Why it is well founded

The ∀ case refers to *A* under a bigger interpretation, but *A* is smaller than ∀. *A*. The recursion is on the
size of the type (lines 44–53, 81–82), and the interpretation is just a parameter. There is no step index:
System F has no recursive types (lines 15–17).
""",
 [q("Over what does the ∀ case of the value relation quantify?",
    ["Every semantic type, i.e. any predicate on closed values", "Every syntactic closed type", "Only int, bool and unit"], 0,
    "`∀ τ : SemType` (TypeSystems/SystemF/LogRel.lean line 79)."),
  q("What is δ for?",
    ["Interpreting the free type variables of the type as semantic types", "Substituting values for term variables", "Counting steps"], 0,
    "`TyVarInterp := Nat → SemType` (line 31); the type-variable case looks up δ (line 68)."),
  q("Why does this relation need no step index?",
    ["Recursion is on the type's size, which suffices without recursive types", "Because the language is untyped", "Because the relation is binary"], 0,
    "TypeSystems/SystemF/LogRel.lean lines 15–17 and 81–82."),
  q("What does the ∃ case require?",
    ["Some semantic type τ under which the packed value is related", "Every semantic type τ"], 0,
    "The ∃ case (TypeSystems/SystemF/LogRel.lean line 80)."),
 ])

node("SystemF.sem_soundness",
 "System F fundamental theorem",
 "Every well-typed System F term is semantically typed, under every good substitution and every interpretation of its type variables. All three System F consequences (termination, both free theorems) start here.",
 r"""## Plain English

**Theorem (`SystemF.sem_soundness`, TypeSystems/SystemF/LogRel.lean lines 823–849).** If *n*; Γ ⊢ *e* : *A*, then
*e* is semantically typed. *Semantically typed* (`semTyped`, lines 245–247) means: *e*'s free term variables are
among Γ's, and for every substitution θ and every interpretation δ such that θ maps each *x* : *B* in Γ to a value
in the relation at *B* under δ, the expression θ(*e*) is in the [expression relation](#/node/SystemF.valRel) at *A*
under δ.

The proof is one compatibility lemma per typing rule (lines 826–849). The polymorphic cases are the
interesting ones. For type abstraction, the body is semantically typed under every extension of δ, since the
induction hypothesis holds for all δ. For type application at *B*, the lemmas that "move the interpretation
around" (from line 249 on) show that relating at *A*[*B*/0] under δ is the same as relating at *A* under
δ extended with the meaning of *B*.

### Consequences in the repo

- [termination](#/node/SystemF.termination): every closed well-typed program evaluates;
- [not_every_type_inhabited](#/node/SystemF.not_every_type_inhabited): ∀α. α is empty;
- [all_identity](#/node/SystemF.all_identity): ∀α. α → α contains only the identity.
""",
 [q("Does `semTyped` quantify over interpretations δ of type variables?",
    ["Yes, over all of them", "No, δ is fixed to the dummy interpretation"], 0,
    "TypeSystems/SystemF/LogRel.lean lines 245–247."),
  q("How is the fundamental theorem proved?",
    ["Induction on the typing derivation, one compatibility lemma per rule", "By the free theorems", "By termination"], 0,
    "Lines 825–849."),
  q("Why does the type-application case need extra lemmas?",
    ["To trade substituting B into the type for extending δ with B's meaning", "Because type application can loop", "It doesn't"], 0,
    "The 'moving the interpretation around' section, from line 249 on."),
 ])

node("SystemF.termination",
 "System F termination",
 "Every closed well-typed System F program evaluates to a value. This is strong normalisation for call-by-value System F, obtained from the fundamental theorem in five lines.",
 r"""## Plain English

**Theorem (`SystemF.termination`, TypeSystems/SystemF/LogRel.lean lines 859–865).** If *e* has some type *A* with no
type variables in scope and an empty context, then there is a value *v* with *e* ⇓ *v*.

This is the System F analogue of [STLC.type_safety](#/node/STLC.type_safety), and it is a substantial
classical result: Girard's normalisation of System F, here for a call-by-value big-step semantics. The
logical relation with its impredicative ∀ case is precisely Girard's method of "reducibility candidates", in a
simple form.

The proof applies [sem_soundness](#/node/SystemF.sem_soundness) with the empty substitution and the dummy
interpretation `δ_any`, which sends every type variable to "all closed values" (lines 852–856). The dummy
choice is harmless because a closed type has no free type variables to interpret.
""",
 [q("What kind of result is `SystemF.termination`?",
    ["Normalisation: closed well-typed programs always finish", "Progress: they can always take a step", "Decidability of type checking"], 0,
    "The conclusion is the existence of a big-step value (line 861)."),
  q("Which interpretation of type variables does the proof use?",
    ["δ_any: every type variable means all closed values", "The empty interpretation", "It doesn't need one"], 0,
    "Lines 851–856 and 863."),
  q("Could a closed well-typed System F program in this language loop forever?",
    ["No, by this theorem", "Yes, using a fixed-point combinator"], 0,
    "No fixed-point combinator is typable in System F. With recursive types (SystemFMu) the Z combinator becomes typable (ZCombinator.lean)."),
 ],
 widgets=walk("How the proof goes (TypeSystems/SystemF/LogRel.lean, lines 859-865)", [
  {"text": "Apply the fundamental theorem to the typing derivation (line 862).", "link": "SystemF.sem_soundness"},
  {"text": "Instantiate with the empty substitution and δ_any; the empty context relation holds trivially (line 863)."},
  {"text": "Drop the empty substitution and keep the value it evaluates to (lines 864–865)."},
 ]))

node("SystemF.not_every_type_inhabited",
 "Free theorem: ∀α. α has no closed inhabitants",
 "No closed System F term has type ∀α. α. The proof instantiates the type variable with the empty semantic type, under which nothing can be related.",
 r"""## Plain English

**Theorem (`SystemF.not_every_type_inhabited`, TypeSystems/SystemF/FreeTheorems.lean lines 15–25).** There is no
expression *e* with type ∀α. α in the empty context.

From the [fundamental theorem](#/node/SystemF.sem_soundness), *e* would evaluate to a type abstraction whose body,
for **every** semantic type τ, evaluates to a value in τ. Take τ to be the empty predicate (line 23). No value is
in it, which is a contradiction.

This is the logical reading too: ∀α. α is "false" under propositions-as-types, and System F is consistent.
""",
 [q("Which semantic type does the proof choose?",
    ["The empty one, which no value satisfies", "The singleton of some value", "All closed values"], 0,
    "TypeSystems/SystemF/FreeTheorems.lean line 23."),
  q("Would the proof work with the dummy interpretation `δ_any` alone?",
    ["No. Under 'all closed values' the body's result *is* related; the empty τ is what gives the contradiction", "Yes"], 0,
    "`δ_any` is only used for the (empty) outer context; the contradiction comes from the τ chosen at line 23."),
  q("What does the theorem say in logical terms?",
    ["The proposition ∀α. α (falsity) has no proof: consistency", "Every type is inhabited"], 0,
    "Under propositions-as-types, ∀α. α is falsity."),
 ])


# ---------------------------------------------------------------- statement set: binary

node("SystemF.Binary.valRel",
 "System F binary logical relation",
 "The binary relation says when two values are indistinguishable at a type. Integers must be equal, functions must map related inputs to related outputs, and at ∀ the two bodies must be related under every relational interpretation of the type variable.",
 r"""## Plain English

**Definitions (TypeSystems/SystemF/BinaryLogRel.lean lines 25–78).** A binary **semantic type** (lines 25–27)
is a relation between closed values. The value relation `valRel δ A v w` (lines 49–74) is defined case by case:

- `int`, `bool`, `unit`: *v* and *w* are the **same** literal;
- type variable α: *v* and *w* are related by δ(α);
- products, sums: componentwise, with the same injection on both sides;
- *A* → *B*: both are closed λs, and related inputs make the two bodies evaluate to related outputs;
- ∀. *A*: both are closed type abstractions, and **for every relation τ** their bodies evaluate to values related at *A*
  with α := τ;
- ∃. *A*: both are packages, and **some** relation τ relates their contents at *A*.

The expression relation (lines 77–78) says that both expressions evaluate, to related values.

The ∃ case is what lets two different implementations of an abstract type count as equivalent. You choose τ to
connect the two internal representations.
""",
 [q("When are two integers related at `int`?",
    ["When they are equal", "Always", "When both are positive"], 0,
    "TypeSystems/SystemF/BinaryLogRel.lean line 50."),
  q("What does the ∃ case let you choose?",
    ["A relation τ connecting the two hidden representations", "A single representation type", "Nothing"], 0,
    "Lines 70–72."),
  q("What must related function values do?",
    ["Map related arguments to bodies that evaluate to related results", "Be syntactically identical", "Return the same integer for every input"], 0,
    "Lines 60–65."),
 ])

node("SystemF.Binary.semTyped",
 "Binary semantic typing (logical relatedness of open terms)",
 "Two open expressions are logically related at A under Γ when both are closed over Γ and, for every interpretation δ and every pair of substitutions with related values for Γ's variables, the substituted expressions are in the expression relation.",
 r"""## Plain English

**Definition (`SystemF.Binary.semTyped`, TypeSystems/SystemF/BinaryLogRel.lean lines 251–254).** Γ ⊨ *e₁* ≈ *e₂* : *A*
holds when:

- both *e₁* and *e₂* have no free term variables outside Γ;
- for every interpretation δ of type variables as relations, and every two substitutions θ₁ and θ₂ that map
  each *x* : *B* of Γ to **related** values at *B* (`SemCtxRel`, lines 142–150), θ₁(*e₁*) and θ₂(*e₂*) are
  [related](#/node/SystemF.Binary.valRel) at *A*: both evaluate, to related values.

This is the hypothesis of the [headline](#/node/SystemF.Binary.soundness_wrt_ctx_equiv). The binary fundamental
theorem `SystemF.Binary.sem_soundness` (lines 854–882) shows that every well-typed term is related to **itself**.
Relating two *different* terms takes work specific to them.
""",
 [q("Which substitutions does binary semantic typing quantify over?",
    ["Pairs of substitutions that give related values to every variable", "A single substitution used on both sides", "Only the empty substitution"], 0,
    "TypeSystems/SystemF/BinaryLogRel.lean lines 252–254 with `SemCtxRel` at lines 142–150."),
  q("What does the binary fundamental theorem give?",
    ["Every well-typed term is related to itself", "Every two terms of the same type are related", "Contextual equivalence directly"], 0,
    "`sem_soundness` (lines 854–882) has a single typed term on both sides."),
  q("Does `semTyped` include the typing judgement?",
    ["No; only closedness and the relational condition", "Yes"], 0,
    "Lines 251–254."),
 ])

node("SystemF.Binary.PctxTyped",
 "Typed program contexts",
 "A program context is an expression with one hole, anywhere, even under a λ or a type abstraction. PctxTyped says that filling a hole typed n; Γ ⊢ _ : A gives a term typed n′; Γ′ ⊢ _ : B.",
 r"""## Plain English

**Definitions (TypeSystems/SystemF/BinaryLogRel.lean lines 895–1057).** A program context (`Pctx`, lines 895–919)
is the syntax of expressions with a single hole in any position. `pfill K e` (lines 921–945) plugs *e* into the hole.

`PctxTyped Δ Γ A K Δ′ Γ′ B` (lines 949–1057) says *K* is well typed as a function from terms of type *A* (under Δ
type variables and context Γ) to terms of type *B* (under Δ′ and Γ′). There is one rule per position of the hole.
The other subterms of each frame must be well typed in the ordinary sense, and binders crossed on the way to the
hole extend the context, so that the hole may mention variables bound by the context. `pfill_typed`
(lines 1059–1091) checks this reading: filling a typed context with a typed term yields a typed term.
""",
 [q("Can the hole of a program context sit under a λ?",
    ["Yes; that's what distinguishes program contexts from evaluation contexts", "No, only in evaluation position"], 0,
    "`lamPCtx` and `tLamPCtx` (TypeSystems/SystemF/BinaryLogRel.lean lines 918–919)."),
  q("What does `pfill_typed` show?",
    ["Filling a typed context with a well-typed term gives a well-typed term", "Every context is typed", "Contexts preserve evaluation"], 0,
    "Lines 1059–1061."),
  q("Why may a term in the hole refer to variables not free in the whole program?",
    ["Because binders on the path to the hole bind them", "It may not"], 0,
    "e.g. the λ rule types the inner context under Γ′ extended with *x* : *B* (lines 1050–1053)."),
 ])

node("SystemF.Binary.ctx_equiv",
 "Contextual equivalence",
 "e₁ and e₂ are contextually equivalent at A if every typed program context that closes them into an int-typed program makes both evaluate to the same integer.",
 r"""## Plain English

**Definition (`SystemF.Binary.ctx_equiv`, TypeSystems/SystemF/BinaryLogRel.lean lines 1229–1232).** For every
context *K* that is [typed](#/node/SystemF.Binary.PctxTyped) from holes of type *A* (under Δ and Γ) to closed
programs of type `int` (no type variables, empty context), there is an integer *z* such that both *K*[*e₁*] and
*K*[*e₂*] evaluate to *z*.

The definition asks for **both** to evaluate. In System F that is free, by [termination](#/node/SystemF.termination).
It is the conclusion of the [headline](#/node/SystemF.Binary.soundness_wrt_ctx_equiv).
""",
 [q("What is the result type of the contexts in `ctx_equiv`?",
    ["int", "A", "Any type"], 0,
    "`PctxTyped Δ Γ A K 0 ∅ .int` (line 1230)."),
  q("Does `ctx_equiv` require the two programs to be syntactically related in any way?",
    ["No; it only compares the integers produced", "Yes, they must have the same free variables"], 0,
    "Lines 1229–1232."),
  q("Would a context that distinguishes e₁ and e₂ by looping on one of them be relevant here?",
    ["No such typed context exists in this terminating language; the definition compares integers", "Yes, divergence is the observation"], 0,
    "System F terminates, so integer results are the natural observation."),
 ])

node("SystemF.Binary.sem_typed_congruence",
 "The binary relation is a congruence",
 "Plugging two related expressions into the same typed program context yields related programs. This key lemma is proved by induction on the context, reusing the binary compatibility lemmas.",
 r"""## Plain English

**Theorem (`SystemF.Binary.sem_typed_congruence`, TypeSystems/SystemF/BinaryLogRel.lean lines 1171–1219).** If
Γ ⊨ *e₁* ≈ *e₂* : *A* and *K* is a [typed context](#/node/SystemF.Binary.PctxTyped) from (Δ, Γ, *A*) to (Δ′, Γ′, *B*),
then Γ′ ⊨ *K*[*e₁*] ≈ *K*[*e₂*] : *B*.

The proof inducts on the typing of *K*. At each frame, the hole side is related by the induction hypothesis,
and the other subterms are related **to themselves** by the binary fundamental theorem. A compatibility lemma
combines them. This is why the compatibility lemmas are stated for two possibly different terms, not just for one.
""",
 [q("How are the frame's other subterms handled?",
    ["They are related to themselves by the binary fundamental theorem", "They are ignored", "They must be values"], 0,
    "e.g. `sem_soundness h₂` at TypeSystems/SystemF/BinaryLogRel.lean line 1177."),
  q("What is the induction on?",
    ["The typing derivation of the context", "The size of e₁", "Evaluation steps"], 0,
    "Line 1174."),
  q("Which theorem uses this lemma?",
    ["`sem_typing_ctx_equiv`, and through it the contextual-equivalence headline", "`all_identity`"], 0,
    "Line 1238."),
 ])
