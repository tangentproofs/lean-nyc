NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]


node("Syntax.Signature",
 "Signature: the vocabulary of a first-order language",
 "A signature is just two types: the function symbols and the predicate symbols. Unlike the textbook definition, it records no arities, so the same symbol may be applied to any number of arguments.",
 r"""## Plain English

**Definition (`Signature`, InferenceInLean/A_Syntax.lean lines 16–20).** A signature has a type `funs` of function
symbols and a type `preds` of predicate symbols. Variables are a separate type `X` (`Variables` is just `Type`,
line 22), passed alongside the signature everywhere.

In the lecture notes a signature also gives each symbol an arity (how many arguments it takes). Here there is no
arity: a [Term](#/node/Syntax.Term) `f(t₁, …, tₙ)` may use any list of arguments, and an
[Interpretation](#/node/Semantics.Interpretation) gives each symbol a function on *lists* of values. This makes the
semantics a little more permissive than the textbook one, but nothing in the soundness proofs depends on arities.

The Peano example in InferenceInLean/G_Examples.lean lines 16–27 builds a signature with function symbols zero,
succ, add, mul and predicates <, ≈.
""",
 [q("What does a Signature in this project record?",
    ["Two types: function symbols and predicate symbols", "Symbols together with their arities", "A list of axioms"], 0,
    "InferenceInLean/A_Syntax.lean lines 16–20 have only `funs` and `preds`."),
  q("Can the same function symbol be used with two arguments in one term and three in another?",
    ["Yes, there are no arities", "No, Lean rejects it"], 0,
    "`Term.func` takes an arbitrary `List` of arguments (InferenceInLean/A_Syntax.lean line 30)."),
  q("Where do variables come from?", ["A separate type X passed alongside the signature", "They are a field of Signature"], 0,
    "`Variables := Type` (InferenceInLean/A_Syntax.lean line 22)."),
 ],
 caveats=["No arities: this is more general than the notes' signatures. It is harmless for soundness."])


node("Syntax.Term",
 "Term: variables and function applications",
 "A term is either a variable x or a function symbol applied to a list of terms. Constants are function symbols applied to the empty list.",
 r"""## Plain English

**Definition (`Term`, InferenceInLean/A_Syntax.lean lines 28–30).** A term over signature `sig` and variables `X` is
- `var x` for a variable `x`, or
- `func f args` for a function symbol `f` and a list `args` of terms.

A constant `c` is `func c []`. A **ground term** is a term with no variables; the project gets these for free by
taking the variable type to be `Empty` (`GroundTerm`, line 32).

Because the arguments sit inside a `List`, `Term` is a *nested* inductive type, and Lean's automatic induction
principle is awkward to use. The authors prove their own principle `Term.induction` (lines 36–51): to prove `P t` for
all terms, prove it for variables and show that `P` for every argument gives `P (func f args)`.

The free variables of a term (`Term.freeVars`, lines 73–76) are all the variables that occur in it.
""",
 [q("How is a constant c represented?", ["func c []", "var c", "A separate constructor"], 0,
    "The comment at InferenceInLean/A_Syntax.lean lines 26–27 says constants are functions of arity zero."),
  q("What is a ground term here?", ["A term whose variable type is Empty", "A term of depth 1", "A term with no function symbols"], 0,
    "`GroundTerm sig := Term sig Empty` (InferenceInLean/A_Syntax.lean line 32)."),
  q("Why do the authors write their own induction principle?",
    ["Term is nested (arguments in a List), so the built-in one is awkward", "Lean has no induction for inductive types"], 0,
    "InferenceInLean/A_Syntax.lean lines 34–35."),
 ])


node("Syntax.Atom",
 "Atoms and literals",
 "An atom is a predicate symbol applied to a list of terms, P(t₁, …, tₙ). A literal is an atom or its negation.",
 r"""## Plain English

**Definitions.**
- `Atom` (InferenceInLean/A_Syntax.lean lines 94–95): `pred p args`, i.e. P(t₁, …, tₙ).
- `Literal` (lines 102–106): `pos a` (the atom a) or `neg a` (¬a).
- `Literal.comp` (lines 109–111) swaps `pos` and `neg`.

Atoms are where the predicates are evaluated in [Formula.eval](#/node/Semantics.Formula.eval). Literals are the
building blocks of [clauses](#/node/Syntax.Clause). In [unification](#/node/Unification.Unifier) the
equations are between atoms, not terms.
""",
 [q("Is ¬¬P(x) a literal?", ["No, a literal has at most one negation", "Yes"], 0,
    "`Literal` has just `pos a` and `neg a` (InferenceInLean/A_Syntax.lean lines 102–106)."),
  q("What does `Literal.comp (neg a)` give?", ["pos a", "neg a", "neg (neg a)"], 0,
    "InferenceInLean/A_Syntax.lean line 111."),
 ])


node("Syntax.Formula",
 "Formula: full first-order formulas",
 "Formulas are built from ⊥, ⊤ and atoms with ¬, ∧, ∨, →, ↔ and the quantifiers ∀x and ∃x, exactly as in the lecture notes.",
 r"""## Plain English

**Definition (`Formula`, InferenceInLean/A_Syntax.lean lines 126–136).** The constructors are `falsum` (⊥), `verum`
(⊤), `atom a`, `neg`, `and`, `or`, `imp`, `iff`, `all x F` (∀x F) and `ex x F` (∃x F). The comment on line 125 notes
that ¬, ∧ and ∀ would suffice, but the authors follow the notes.

**Free variables** (`Formula.freeVars`, lines 144–154): the free variables of the atoms, with `x` removed under
`∀x` and `∃x`. A formula is **closed** (`Formula.closed`, lines 170–171) if it has no free variables.

**Big quantifier** (`Formula.bigForall`, lines 177–181): `bigForall [x₁, …, xₙ] F` is ∀x₁ … ∀xₙ F. If every free
variable of F is in the list, the result is closed (`bigForall_subset_freeVars`, lines 214–225).

The meaning of a formula is given by [Formula.eval](#/node/Semantics.Formula.eval).
""",
 [q("What are the free variables of ∀x P(x, y)?", ["{y}", "{x, y}", "∅"], 0,
    "`all x f` gives `freeVars f \\ {x}` (InferenceInLean/A_Syntax.lean line 153)."),
  q("Is ⊥ closed?", ["Yes, it has no free variables", "No"], 0, "InferenceInLean/A_Syntax.lean line 145."),
  q("What is `bigForall [] F`?", ["F itself", "⊤", "∀ F"], 0, "InferenceInLean/A_Syntax.lean line 180."),
 ])


node("Syntax.Clause",
 "Clause: a list of literals, read as their disjunction",
 "A clause is a list of literals L₁, …, Lₙ and stands for L₁ ∨ … ∨ Lₙ. The empty clause stands for ⊥. Free variables in a clause are read as universally quantified.",
 r"""## Plain English

**Definition (`Clause`, InferenceInLean/A_Syntax.lean line 114).** A clause is a `List` of [literals](#/node/Syntax.Atom).

**As a formula** (`Clause.toFormula`, lines 158–161): `[L₁, …, Lₙ]` becomes L₁ ∨ (L₂ ∨ … ∨ (Lₙ ∨ ⊥)). In particular the
empty clause is ⊥. Lean inserts this conversion automatically (the coercion on lines 163–164), so a clause can be used
wherever a formula is expected.

**As a closed formula** (`Clause.toClosedFormula`, lines 496–497): put ∀ in front for each free variable of the
clause (collected without duplicates by `Clause.freeVarsList`, lines 406–409). `closedClause_closed` (lines 525–531)
proves the result is indeed closed.

Two readings of "a clause is true in I" therefore appear in the project:
- the open clause is true for **every** assignment ([ValidIn](#/node/Models.ValidIn)), and
- its universal closure is true. These agree, by [validclosed_iff_valid](#/node/Resolution.validclosed_iff_valid).

Because a clause is a list, the order of the literals matters syntactically, though not semantically. The resolution
rules are written with the resolved literal at the **front** of the list (see
[GeneralResolutionRule](#/node/Resolution.GeneralResolutionRule)).
""",
 [q("What formula does the empty clause stand for?", ["⊥ (falsum)", "⊤ (verum)", "It has no formula"], 0,
    "InferenceInLean/A_Syntax.lean line 159."),
  q("How is the clause [P(x), ¬Q(x)] read as a closed formula?", ["∀x (P(x) ∨ (¬Q(x) ∨ ⊥))", "∃x (P(x) ∧ ¬Q(x))", "P(x) ∨ ¬Q(x) with x free"], 0,
    "`toClosedFormula` wraps `toFormula` in `bigForall` over the free variables (InferenceInLean/A_Syntax.lean lines 496–497)."),
  q("Are [P, Q] and [Q, P] the same clause in Lean?", ["No, they are different lists, but they mean the same", "Yes"], 0,
    "`Clause` is a `List` (InferenceInLean/A_Syntax.lean line 114); `toFormula` gives two disjunctions with the same truth value."),
 ])


node("Syntax.Substitution",
 "Substitutions and how they act",
 "A substitution σ sends every variable to a term. Applying it to a term, atom, literal or clause replaces each variable x by σ(x), simultaneously.",
 r"""## Plain English

**Definition (`Substitution`, InferenceInLean/A_Syntax.lean line 539).** A substitution is any function from variables
to terms. The notes require only finitely many variables to change; the comment on lines 535–537 says the authors drop
that requirement because it doesn't change the proofs.

**Applying it** (lines 552–571): `Term.substitute σ` replaces `var x` by `σ x` and works through function
arguments; `Atom.substitute`, `Literal.substitute` and `Clause.substitute` push it through atoms, literals and every
literal of a clause. We write tσ, Cσ.

**Composition** (`Substitution.compose`, lines 574–577), written `σ ∘ τ`, means "first τ, then σ": (σ ∘ τ)(x) = τ(x)σ.

**Domain and codomain** (lines 580–585): the domain is the set of variables that σ actually moves (σ(x) ≠ x). The
codomain is the set of variables that occur in σ(x) for some x in the domain.

**More general** (`MoreGeneral`, lines 588–590), written `σ ≤ τ`: there is ρ with ρ ∘ σ = τ, i.e. τ is σ followed by
some further substitution. A worked example is on lines 592–603.

**Idempotent** (`Idempotent`, lines 606–607): σ ∘ σ = σ. See the headline
[idempotent_iff_inter_empty](#/node/Syntax.idempotent_iff_inter_empty).
""",
 [q("If σ(z) = f(y) and σ leaves everything else alone, what is P(z, y)σ?", ["P(f(y), y)", "P(f(f(y)), y)", "P(z, y)"], 0,
    "Substitution is simultaneous and applied once (InferenceInLean/A_Syntax.lean line 554)."),
  q("In this project, what does σ ∘ τ do to a variable x?", ["Applies τ first, then σ: τ(x)σ", "Applies σ first, then τ"], 0,
    "`(τ x).substitute σ` (InferenceInLean/A_Syntax.lean line 576)."),
  q("What does σ ≤ τ mean?", ["τ = ρ ∘ σ for some ρ (σ is more general)", "σ moves fewer variables than τ", "σ(x) is shorter than τ(x)"], 0,
    "InferenceInLean/A_Syntax.lean lines 588–589."),
  q("Must a substitution move only finitely many variables?", ["No, the project drops that condition", "Yes"], 0,
    "InferenceInLean/A_Syntax.lean lines 535–537."),
 ],
 caveats=["The infix notations `∘` and `≤` are redefined locally for substitutions (InferenceInLean/A_Syntax.lean lines 577 and 590)."])


node("Syntax.idempotent_iff_inter_empty",
 "Headline: σ is idempotent exactly when its domain and codomain are disjoint",
 "Applying σ twice gives the same as applying it once exactly when no variable that σ moves appears in what σ produces. Both directions are proved in the source.",
 r"""## Plain English

**Theorem (`idempotent_iff_inter_empty`, InferenceInLean/A_Syntax.lean lines 682–712).** For every
[substitution](#/node/Syntax.Substitution) σ:

σ ∘ σ = σ **if and only if** dom(σ) ∩ codom(σ) = ∅.

Example: σ = {x ↦ f(y)} is idempotent (y is not moved). σ = {x ↦ f(y), y ↦ z} is not: applying it twice sends x to
f(z), not f(y), and indeed y is in both the domain and the codomain.

This is a standard fact used in unification: the "nice" most general unifiers are idempotent ones, see
[unifiable_iff_mgu_idempot](#/node/Unification.unifiable_iff_mgu_idempot).

### The two directions

- **(⇒)** Suppose x is in the domain and occurs in t = σ(y). Idempotence says tσ = t. But
  `ne_subst_of_mem_dom_free` (lines 648–679) shows that if a term contains a variable that σ moves, then applying σ
  changes the term. Contradiction.
- **(⇐)** For each x, either σ(x) = x, and then (σ ∘ σ)(x) = σ(x) directly; or x is in the domain, so every variable
  of σ(x) is in the codomain, hence not in the domain, so σ leaves σ(x) unchanged
  (`id_of_free_not_in_domain`, lines 638–645).
""",
 [q("Is σ = {x ↦ g(x)} idempotent?", ["No: x is in both domain and codomain", "Yes"], 0,
    "Applying it twice gives g(g(x)). The theorem's right side fails (InferenceInLean/A_Syntax.lean line 683)."),
  q("Does the theorem need σ to move only finitely many variables?", ["No", "Yes"], 0,
    "No finiteness hypothesis appears (InferenceInLean/A_Syntax.lean lines 682–683)."),
  q("Which key fact drives the (⇒) direction?",
    ["A term containing a moved variable is changed by σ", "Every substitution is idempotent", "The domain is always finite"], 0,
    "`Substitution.ne_subst_of_mem_dom_free` (InferenceInLean/A_Syntax.lean lines 648–650)."),
 ],
 caveats=["Proof complete in the source, with no sorry; not machine-checked for this site."],
 widgets=walk("How the proof goes (InferenceInLean/A_Syntax.lean, lines 682-712)", [
  {"text": "(⇒) Take x in dom(σ) ∩ codom(σ): x occurs in t = σ(y) for some y in the domain (lines 686–690)."},
  {"text": "Idempotence at y says tσ = t (line 691). But a term containing a moved variable changes under σ: contradiction (lines 692–694).",
   "lean": "exact Substitution.ne_subst_of_mem_dom_free σ t hexists <| symm hidemy", "link": "Syntax.Substitution"},
  {"text": "(⇐) If σ(x) = x, both sides are σ(x) (lines 699–700)."},
  {"text": "Otherwise x is in the domain, every variable of σ(x) is in the codomain, so none is in the domain (lines 701–710)."},
  {"text": "So σ leaves σ(x) unchanged, which is exactly (σ ∘ σ)(x) = σ(x) (lines 711–712).",
   "lean": "exact Substitution.id_of_free_not_in_domain σ (σ x) free_not_in_dom"},
 ]))


import importlib.util as _u, os as _o
_s = _u.spec_from_file_location("_zx", _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "z_extra.py"))
_m = _u.module_from_spec(_s); _s.loader.exec_module(_m)
for _n in NODES:
    _n["quiz"] += _m.EXTRA.get(_n["id"], [])
