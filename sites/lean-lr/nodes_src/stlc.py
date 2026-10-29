NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]


# ---------------------------------------------------------------- headline

node("STLC.type_safety",
 "Headline: every closed well-typed STLC term terminates",
 "Despite the name, this theorem is a termination result: any closed term the simply typed λ-calculus accepts evaluates to a value. The proof is the textbook logical-relations argument, and it fits in nine lines because all the work is in the fundamental theorem.",
 r"""## Plain English

**Theorem (`STLC.type_safety`, TypeSystems/Stlc/LogRel.lean lines 340–348).** Take an expression *e* of the
[simply typed λ-calculus](#/node/STLC.Expr). Suppose it has some type *A* in the **empty** context, by the
[typing rules](#/node/STLC.SynTyped). Then *e* [terminates](#/node/STLC.terminates): there is a value *v* with
*e* ⇓ *v* in the [big-step semantics](#/node/STLC.BigStep).

### Why the name is misleading

In most textbooks "type safety" means *a well-typed program never gets stuck*. It may run forever, but it never
reaches a non-value that cannot step. This theorem says something different and stronger for this language:
the program **finishes**. In a big-step semantics, "evaluates to a value" excludes getting stuck *and* running
forever at once. The course calls this the semantic route to safety, and the file keeps the course's name. The
usual "never gets stuck" theorem, proved by progress and preservation, is
[STLC.typed_safety](#/node/STLC.typed_safety) in a different file.

### What makes it work

A typing derivation is a syntactic object. You cannot run it. The proof goes through a *logical relation*: for
each type *A*, a set of "good" values of type *A* and "good" expressions of type *A*
([semTyped](#/node/STLC.semTyped) explains the details). An expression is good at *A* when it evaluates to a
good value. The [fundamental theorem](#/node/STLC.fundamental) says that every well-typed term is good, and a
good term evaluates to a value by definition. So all that is left is to apply the fundamental theorem with the
empty substitution, which is what lines 342–348 do.

### The scope

The language is tiny: integers, addition, variables, λ and application. Products, sums and other operators are
in `StlcExtended`, which proves its own termination theorem (TypeSystems/StlcExtended/LogRel.lean lines 302–307).
There is also a call-by-name variant (TypeSystems/Stlc/CbnLogRel.lean lines 303–309).
""",
 [q("What does `STLC.type_safety` conclude about a closed well-typed term *e*?",
    ["*e* evaluates (big-step) to some value",
     "*e* never reaches a stuck non-value, but may loop forever",
     "*e* has a unique type",
     "*e* is already a value"], 0,
    "The conclusion is `terminates e`, which is defined as the existence of a value *v* with *e* ⇓ *v* (TypeSystems/Stlc/Operational.lean lines 52–53)."),
  q("Which theorem in the STLC folder is the classical 'well-typed programs don't get stuck' statement?",
    ["`STLC.typed_safety`, by progress and preservation", "`STLC.type_safety`", "`STLC.fundamental`", "There is none"], 0,
    "`typed_safety` (TypeSystems/Stlc/TypeSafety.lean lines 277–282) says every term reachable by small steps is a value or can step. `type_safety` is the termination result."),
  q("Why must the context be empty?",
    ["A term with free variables cannot be evaluated: there is no value to substitute for them",
     "The fundamental theorem only holds for the empty context",
     "Lean cannot represent non-empty contexts"], 0,
    "The fundamental theorem holds in any context. To get an evaluation you need to close the term. With the empty context the empty substitution does it, and lines 344–345 apply it and rewrite it away."),
  q("Is the theorem's proof long?",
    ["No. About seven lines that apply `fundamental` and unfold the expression relation",
     "Yes. Hundreds of lines of case analysis in the theorem itself"], 0,
    "TypeSystems/Stlc/LogRel.lean lines 342–348. The work sits in the compatibility lemmas behind `fundamental`."),
 ],
 caveats=["The name says 'type safety', but the statement is termination (normalisation) for closed terms. Termination implies safety for this big-step semantics, but the converse fails, so the theorem is stronger than its name.",
          "The typing rules have no rule for λ with an anonymous binder (TypeSystems/Stlc/Types.lean lines 54–74), so such terms are simply untypable. This makes the theorem cover slightly fewer programs than you might expect. It doesn't make it wrong."],
 widgets=walk("How the proof goes (TypeSystems/Stlc/LogRel.lean, lines 340-348)", [
  {"text": "Assume e has type A in the empty context (line 341).", "link": "STLC.SynTyped"},
  {"text": "Apply the fundamental theorem to get that e is semantically typed: closed, and good for every good substitution (line 343).", "link": "STLC.fundamental"},
  {"text": "Instantiate with the empty substitution, which the context relation accepts for the empty context (line 344).", "link": "STLC.semTyped"},
  {"text": "The empty substitution leaves e unchanged (line 345)."},
  {"text": "Unfold the expression relation: there is a value v with e ⇓ v (and v is good, which is no longer needed) (lines 346–347)."},
  {"text": "That value witnesses `terminates e` (line 348).", "link": "STLC.terminates"},
 ]))


# ---------------------------------------------------------------- statement set

node("STLC.Expr",
 "STLC expressions",
 "The simply typed λ-calculus here has just five kinds of expression: variables, λ-abstractions, applications, integer literals and addition. Values are integers and λs.",
 r"""## Plain English

**Definition (`STLC.Expr`, TypeSystems/Stlc/Lang.lean lines 21–27).** An expression is one of:

- a **variable**, named by a string;
- a **λ-abstraction** with a *binder* and a body. A binder is either a name or "anonymous", meaning
  the argument is ignored (lines 8–11);
- an **application** of one expression to another;
- an **integer literal**;
- a **sum** of two expressions.

The **values** (`STLC.Val`, lines 30–33) are the integer literals and the λ-abstractions. A conversion back
to expressions is defined on lines 36–38.

Variables are names, not De Bruijn indices, and substitution (TypeSystems/Stlc/Operational.lean lines 5–16) does
not avoid capture. That is safe because the semantics only ever substitutes **closed** values. The logical
relation tracks closedness explicitly for this reason (see [semTyped](#/node/STLC.semTyped)).
""",
 [q("Which of these is a value in STLC?",
    ["A λ-abstraction, whatever its body", "An application", "A sum of two literals", "A variable"], 0,
    "Values are integer literals and λs (TypeSystems/Stlc/Lang.lean lines 30–33). A sum of literals still has to take a step."),
  q("Does substitution avoid variable capture?",
    ["No, but only closed values are ever substituted, so capture can't happen", "Yes, it renames bound variables", "There is no substitution: the language uses environments"], 0,
    "TypeSystems/Stlc/Operational.lean lines 5–16 only stops at shadowing binders. Closedness is tracked separately."),
  q("What does an anonymous binder mean?",
    ["The λ ignores its argument", "The λ is recursive", "The variable is bound by an outer λ"], 0,
    "Substituting under an anonymous binder does nothing (TypeSystems/Stlc/Operational.lean lines 18–21)."),
 ])

node("STLC.SynTyped",
 "STLC typing rules",
 "The usual five typing rules: look up a variable, type a λ by typing its body under one more assumption, apply functions to arguments, and give literals and sums the integer type. Types are just `int` and function types.",
 r"""## Plain English

**Definition (`STLC.SynTyped`, TypeSystems/Stlc/Types.lean lines 54–74).** Types (`STLC.Ty`, lines 18–21)
are `int` and function types *A* ⇒ *B*. A typing context is a finite map from variable names to types
(lines 27–30). The judgement Γ ⊢ *e* : *A* is generated by:

- **var:** if Γ maps *x* to *A*, then *x* : *A*;
- **lam:** if *e* : *B* under Γ extended with *x* : *A*, then λ*x*. *e* : *A* ⇒ *B*. Only **named**
  binders have a rule;
- **app:** if *e₁* : *A* ⇒ *B* and *e₂* : *A*, then *e₁ e₂* : *B*;
- **literal:** every integer literal has type `int`;
- **plus:** if both summands have type `int`, so does their sum.

This is the judgement in the hypothesis of [type_safety](#/node/STLC.type_safety) and
[fundamental](#/node/STLC.fundamental).
""",
 [q("Can λ_. 5 (an anonymous binder) be typed?",
    ["No. There is no typing rule for anonymous λs in this file", "Yes, at any type A ⇒ int", "Only at int ⇒ int"], 0,
    "Only the named-binder rule exists (TypeSystems/Stlc/Types.lean lines 59–61). The System F development does add an anonymous rule."),
  q("What type does 1 + 2 have?",
    ["int", "int ⇒ int", "None, because + needs variables"], 0,
    "By the plus rule and the literal rule (TypeSystems/Stlc/Types.lean lines 68–74)."),
  q("Is there a rule that types an ill-formed application such as 3 4?",
    ["No. The function position must have a function type, and literals only have type int", "Yes, at type int"], 0,
    "The app rule requires *e₁* : *A* ⇒ *B* (line 64), and 3 only has type int."),
 ])

node("STLC.BigStep",
 "STLC big-step evaluation",
 "e ⇓ v says that e evaluates to the value v under call-by-value: evaluate the function, then the argument, then the body with the argument substituted. Getting stuck and running forever both mean there is no v.",
 r"""## Plain English

**Definition (`STLC.BigStep`, TypeSystems/Stlc/Operational.lean lines 26–42).** The relation *e* ⇓ *v*:

- a literal and a λ evaluate to themselves;
- for an application *e₁ e₂*: if *e₁* ⇓ λ*x*. *e*, *e₂* ⇓ *v₂*, and *e* with *v₂* substituted for *x* evaluates to *v*,
  then *e₁ e₂* ⇓ *v*. This is **call-by-value**: the argument is evaluated before substitution;
- for a sum: if both sides evaluate to integers, the sum evaluates to their total.

It is an inductive relation, so a derivation is a finite tree. A looping program has no derivation, and neither
has a stuck one such as 3 4. The evaluation is deterministic (lines 55–74).

The file also has a small-step semantics with evaluation contexts (the rest of Operational.lean). That is the
semantics used by [typed_safety](#/node/STLC.typed_safety).
""",
 [q("Why can't a non-terminating term have a big-step derivation?",
    ["Derivations are finite trees, and an infinite evaluation would need an infinite one", "Lean adds a step limit", "Because the relation is defined only for values"], 0,
    "BigStep is an inductive relation (TypeSystems/Stlc/Operational.lean lines 26–42), so every derivation is finite."),
  q("In which order does application evaluate?",
    ["Function, then argument, then the substituted body: call-by-value", "Body first, then the argument only if needed: call-by-name"], 0,
    "The app rule has the three premises in that order and substitutes the *value* of the argument (lines 33–37). Call-by-name is the separate CbnLogRel.lean."),
  q("Does 1 + (λx. x) evaluate?",
    ["No. The plus rule requires both sides to evaluate to integers", "Yes, to 1", "Yes, to λx. x"], 0,
    "Lines 39–42."),
 ])

node("STLC.terminates",
 "terminates",
 "A term terminates when it evaluates to some value. This is the conclusion of the misleadingly named STLC.type_safety.",
 r"""## Plain English

**Definition (`STLC.terminates`, TypeSystems/Stlc/Operational.lean lines 52–53).** *e* terminates if there is a
value *v* with *e* ⇓ *v* ([BigStep](#/node/STLC.BigStep)).

Because big-step evaluation has no derivation for stuck terms, "terminates" here means "runs to completion and
produces a value". It rules out both crashing and looping.
""",
 [q("Does `terminates (3 4)` hold?",
    ["No. 3 4 is stuck, so it has no big-step derivation", "Yes, since it stops immediately"], 0,
    "No BigStep rule applies to an application whose function part evaluates to an integer (TypeSystems/Stlc/Operational.lean lines 33–37)."),
  q("Does `terminates` say which value is produced?",
    ["No, only that some value exists (which is unique by determinism)", "Yes, it fixes the value to be an integer"], 0,
    "It is an existential (line 53). Determinism is a separate lemma (lines 55–74)."),
  q("Does `terminates e` imply that *e* is well typed?",
    ["No. The ill-typed (λx. x) (λy. y y) evaluates to λy. y y", "Yes, only typed terms evaluate"], 0,
    "`terminates` is about evaluation only. Self-application is ill-typed, but this application still evaluates to a value in one β-step."),
 ])

node("STLC.semTyped",
 "The STLC logical relation (semantic typing)",
 "A value is good at int when it is an integer, and good at A ⇒ B when it is a closed λ that turns every good A-value into a good B-expression. A good expression evaluates to a good value. An open term is semantically typed when all good substitutions make it good.",
 r"""## Plain English

**Definitions (TypeSystems/Stlc/LogRel.lean lines 18–47).** The two relations at the heart of the file are
defined together by recursion on the type (lines 18–30). The site's source scanner misses definitions inside a
`mutual` block, so these two have no node of their own:

- **value relation 𝒱⟦A⟧:** at `int`, the integer literals. At *A* ⇒ *B*, a λ*x*. *e* whose body has no free
  variables except *x*, such that for **every** value *v′* in 𝒱⟦A⟧, the body with *v′* substituted is in ℰ⟦B⟧;
- **expression relation ℰ⟦A⟧:** *e* evaluates ([BigStep](#/node/STLC.BigStep)) to some value in 𝒱⟦A⟧.

The **context relation** 𝒢⟦Γ⟧ (lines 35–41) relates Γ to substitutions σ that map each variable *x* : *A* in Γ to
a value in 𝒱⟦A⟧.

**Semantic typing** Γ ⊨ *e* : *A* (`STLC.semTyped`, lines 45–47) means: *e*'s free variables are among Γ's, and
for every σ in 𝒢⟦Γ⟧, applying σ to *e* gives an expression in ℰ⟦A⟧.

### Why this shape

The function case says what it means to *behave like* a function of type *A* ⇒ *B*: send good inputs to good
outputs. It refers to ℰ at the smaller type *B* and 𝒱 at the smaller type *A*, so the recursion is on the type
and terminates. In the richer languages that follow, this simple measure stops working (recursive types), and a
step index is added ([SystemFMuState](#/node/SystemFMuState.semTyped)).
""",
 [q("When is λx. x + 1 in 𝒱⟦int ⇒ int⟧?",
    ["Yes: for every integer n, n + 1 evaluates to an integer", "No: the body has a free variable", "Only after it is applied"], 0,
    "The body's only free variable is *x* (allowed), and for any integer value the substituted body evaluates to an integer (TypeSystems/Stlc/LogRel.lean lines 23–25)."),
  q("What does ℰ⟦A⟧ e require?",
    ["*e* evaluates to a value in 𝒱⟦A⟧", "*e* is syntactically typed at *A*", "*e* is a value"], 0,
    "Lines 28–29."),
  q("Why do the relations recurse on the type rather than on the expression?",
    ["The function case talks about all inputs, not subterms; types get smaller (A ⇒ B to A and B), so recursion on types terminates",
     "Lean forbids recursion on expressions"], 0,
    "The function case quantifies over all values *v′* (line 25), which need not be subterms."),
  q("Is semantic typing defined using the typing rules?",
    ["No. It only mentions evaluation and closedness, which is what makes the fundamental theorem non-trivial", "Yes, it includes Γ ⊢ e : A as a conjunct"], 0,
    "Lines 45–47 mention closedness, substitutions and ℰ, not `SynTyped`."),
 ],
 caveats=["`valRel` and `exprRel` (lines 18–30) are inside a `mutual` block and the site's text scanner doesn't list them, so they are explained here."])

node("STLC.fundamental",
 "STLC fundamental theorem",
 "Every syntactically well-typed term is semantically well-typed. The proof is one compatibility lemma per typing rule, put together by induction on the derivation.",
 r"""## Plain English

**Theorem (`STLC.fundamental`, TypeSystems/Stlc/LogRel.lean lines 330–338).** If Γ ⊢ *e* : *A*
([typing](#/node/STLC.SynTyped)), then Γ ⊨ *e* : *A* ([semantic typing](#/node/STLC.semTyped)).

The proof is an induction on the typing derivation. Each case is a **compatibility lemma**, which says that the
semantic relation is closed under the corresponding typing rule. For example, `compatLamNamed` (lines 283–305)
shows that if the body is semantically typed under Γ, *x* : *A*, then the λ is semantically typed at *A* ⇒ *B*,
and `compatPlus` (lines 307–328) does the same for addition. The variable and application cases are earlier in
the file.

This is the pattern of every chapter of the port: define semantic types, prove a compatibility lemma per rule,
and read off a consequence. See [SystemF.sem_soundness](#/node/SystemF.sem_soundness),
[SystemFMuState.sem_soundness](#/node/SystemFMuState.sem_soundness) and
[ConcurrentLogRel.fundamental](#/node/ProgramLogics.ConcurrentLogRel.fundamental).
""",
 [q("What kind of induction proves the fundamental theorem?",
    ["Induction on the typing derivation", "Induction on the number of evaluation steps", "Induction on the size of the type"], 0,
    "TypeSystems/Stlc/LogRel.lean line 333 inducts on the `SynTyped` derivation."),
  q("What is a compatibility lemma?",
    ["A proof that semantic typing is preserved by one typing rule", "A proof that two languages are compatible", "A lemma that types are decidable"], 0,
    "One per rule, e.g. `compatPlus` at lines 307–328."),
  q("Does the fundamental theorem need the context to be empty?",
    ["No. It holds for every Γ", "Yes"], 0,
    "Line 330 is stated for any Γ. Emptiness is only needed when the result is used in `type_safety`."),
 ],
 widgets=walk("How the proof goes (TypeSystems/Stlc/LogRel.lean, lines 330-338)", [
  {"text": "Induct on the typing derivation (line 333).", "link": "STLC.SynTyped"},
  {"text": "Variable: compat_var (line 334)."},
  {"text": "Named λ: compatLamNamed, using the induction hypothesis for the body (line 335)."},
  {"text": "Application: compatApp (line 336)."},
  {"text": "Integer literal and plus: compat_int and compatPlus (lines 337–338)."},
 ]))

node("STLC.typed_safety",
 "STLC syntactic type safety (progress and preservation)",
 "The classical safety theorem, proved the classical way: every term reachable from a closed well-typed term by small steps is a value or can take another step. Compare it with the semantic STLC.type_safety, which proves termination.",
 r"""## Plain English

**Theorem (`STLC.typed_safety`, TypeSystems/Stlc/TypeSafety.lean lines 277–282).** If *e₁* is closed and well
typed, and *e₁* reduces to *e₂* in any number of small (contextual) steps, then *e₂* is a value or can take
another step.

The proof is the standard induction on the reduction sequence. **Progress** says a closed well-typed term is a
value or can step. **Preservation** (lines 270–274) says a step keeps the type.

This file is included for contrast. It is the *syntactic* route of the course's Chapter 1, and
[STLC.type_safety](#/node/STLC.type_safety) is the *semantic* route. The semantic route proves more here
(termination), and it extends to things the syntactic route cannot handle, such as code that is safe without
being well typed.
""",
 [q("What does `typed_safety` conclude about every reachable *e₂*?",
    ["It is a value or can step", "It is a value", "It terminates"], 0,
    "TypeSystems/Stlc/TypeSafety.lean line 279."),
  q("Does `typed_safety` show that well-typed STLC programs terminate?",
    ["No. It is compatible with infinite reduction; termination is `type_safety`", "Yes"], 0,
    "Progress and preservation alone say nothing about termination."),
  q("Which semantics does it use?",
    ["The small-step contextual semantics", "The big-step semantics"], 0,
    "It quantifies over `ContextualSteps` (line 278)."),
 ])
