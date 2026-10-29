NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]

EX = "examples/Logic.lean"

# ---------------------------------------------------------------- headline

node("soundness",
 "Headline: natural deduction for propositional logic is sound",
 "Anything derivable from assumptions with the file's natural-deduction rules is true under every interpretation that makes the assumptions true. The proof has no sorry and takes about 25 lines, one case per rule. It is one of the agent-generated sample proofs.",
 r"""## Plain English

**Theorem (`soundness`, examples/Logic.lean lines 47–72).** Take a list of assumptions Γ and a formula *p*
(both built from [PropForm](#/node/PropForm)). Suppose there is a derivation of *p* from Γ using the rules of
[Proof](#/node/Proof). Then for every way *v* of interpreting the variables as propositions, if all of Γ holds
under *v* ([evalCtx](#/node/evalCtx)), then *p* holds under *v* ([eval](#/node/eval)).

In one line: **whatever the proof system derives is true**. That is the textbook meaning of *soundness*, and the
name fits.

### Where this file comes from

This file sits in the prover's `examples/` folder. The prover README says that folder holds proofs Lea generated
(see the [About page](#/page/about)). The repository does not record the prompt that produced this particular
file, or how many attempts it took, so this site treats it as a sample of the kind of output Lea aims for.

### What the proof system can and cannot do

The rules are introduction and elimination rules for ∧, ∨, → and ¬, plus "use an assumption". There is **no**
classical rule (no excluded middle, no double-negation elimination), so this is the *intuitionistic* fragment.
Soundness only needs each rule to preserve truth, so this doesn't weaken the theorem. It does mean the system
proves fewer formulas than classical propositional logic.

### What it doesn't say

It says nothing about **completeness** (that every valid formula can be derived). That direction is much harder,
and the file doesn't attempt it.
""",
 [q("What does `soundness` conclude?",
    ["The derived formula is true under every interpretation that makes all assumptions true",
     "Every formula true under all interpretations has a derivation",
     "Derivations are unique",
     "Every formula is either derivable or its negation is"], 0,
    "examples/Logic.lean lines 47–72: from a derivation, an interpretation *v*, and the fact that the context holds under *v*, it concludes that the formula holds under *v*. The second option is completeness, which the file doesn't prove."),
  q("Does the proof system include excluded middle (p ∨ ¬p as an axiom or rule)?",
    ["No. The rules (lines 23–34) are intuitionistic: introduction and elimination rules plus using an assumption",
     "Yes, as the rule `not_elim`",
     "Yes, through Lean's `Classical.em`"], 0,
    "`not_elim` is ex falso (from *p* and ¬*p*, derive anything), not excluded middle. No rule in examples/Logic.lean lines 23–34 yields p ∨ ¬p for an arbitrary p."),
  q("How is the theorem proved?",
    ["By induction on the derivation, one case per rule",
     "By a truth-table computation",
     "By induction on the size of the formula"], 0,
    "Line 48 starts the induction on the derivation. Lines 49–72 handle the eleven rules."),
  q("What role does `in_ctx_eval` play?",
    ["It handles the 'use an assumption' rule: an assumption in a true context is true",
     "It proves completeness for atoms",
     "It evaluates the context to a Boolean"], 0,
    "The `hyp` case at line 49 calls it. It is proved separately at examples/Logic.lean lines 36–45."),
 ],
 caveats=["Not built for this site. The file contains no sorry, and the proof looks complete, but Lean's kernel was not run on it here.",
          "Formulas are interpreted as Lean propositions, not as true/false Booleans. Every Boolean assignment is a special case, so the theorem covers ordinary two-valued semantics too.",
          "Only soundness. Completeness is not stated."],
 widgets=walk("How the proof goes (examples/Logic.lean, lines 47-72)", [
  {"text": "Induct on the derivation, keeping the interpretation v and the fact that the context holds (line 48).", "link": "Proof"},
  {"text": "Assumption rule: the formula is in the context, and every member of a true context is true (line 49).", "link": "in_ctx_eval"},
  {"text": "∧ rules: pair up the two truths, or take one half of a true conjunction (lines 50–52)."},
  {"text": "∨ introduction: a true disjunct makes the disjunction true (lines 53–54)."},
  {"text": "∨ elimination: split on which disjunct is true. Add it to the context, which is still true, and use the matching sub-derivation (lines 55–58).", "link": "evalCtx"},
  {"text": "→ introduction: assume the antecedent is true, extend the context with it, and use the induction hypothesis (lines 59–61)."},
  {"text": "→ elimination (modus ponens): apply the true implication to the true antecedent (lines 62–63)."},
  {"text": "¬ introduction: if adding p to the context derives both q and ¬q, then p being true would make q both true and false, so ¬p holds (lines 64–68)."},
  {"text": "¬ elimination (ex falso): p and ¬p can't both be true, so the case is contradictory (lines 69–72)."},
 ]))

# ---------------------------------------------------------------- statement set

node("PropForm",
 "Propositional formulas",
 "Formulas are trees built from named variables with not, and, or and implies. There are no constants for true or false.",
 r"""## Plain English

**Definition (`PropForm`, examples/Logic.lean lines 1–6).** A propositional formula is one of:

- a **variable**, named by a string;
- the **negation** of a formula;
- the **conjunction**, **disjunction** or **implication** of two formulas.

That's the whole syntax. There is no built-in "true" or "false" formula. You can still say "false" indirectly, for
example as ¬(*x* → *x*).

These are syntax trees, not truth values. Their meaning comes from [eval](#/node/eval), and the derivations about
them come from [Proof](#/node/Proof).
""",
 [q("Which of these is NOT a way to build a `PropForm`?",
    ["The constant 'true'", "A named variable", "An implication between two formulas", "A negation"], 0,
    "examples/Logic.lean lines 1–6 list five constructors: variable, not, and, or, implies. There is no constant."),
  q("What names a variable?",
    ["A string", "A natural number", "A Boolean"], 0,
    "Line 2: a variable carries a string name."),
  q("Is a `PropForm` true or false by itself?",
    ["No. It is syntax. Truth depends on an interpretation, given by `eval`", "Yes. Each formula is a Boolean"], 0,
    "Truth only appears once [eval](#/node/eval) (lines 8–13) interprets the variables."),
 ])

node("eval",
 "What a formula means under an interpretation",
 "An interpretation assigns a Lean proposition to each variable name, and the connectives become Lean's own not, and, or and implies.",
 r"""## Plain English

**Definition (`eval`, examples/Logic.lean lines 8–13).** Fix an interpretation *v* that sends each variable name to
a proposition. Then the meaning of a [formula](#/node/PropForm) is computed by recursion on the formula:

- a variable means whatever *v* says about it;
- ¬*p* means "the meaning of *p* is false";
- *p* ∧ *q*, *p* ∨ *q* and *p* → *q* mean the corresponding Lean statements about the meanings of *p* and *q*.

### Why propositions and not Booleans?

The interpretation lands in Lean's `Prop` rather than in true/false Booleans. This is more general: any
Boolean assignment can be seen as a Prop assignment, so [soundness](#/node/soundness) for Prop covers the usual
truth-table semantics too. Lean's Prop is classical (excluded middle is an available axiom), but the soundness
proof doesn't need that.

(The stack-machine example has an unrelated function also called `eval`. On this site that one is
[eval'](#/node/eval').)
""",
 [q("Under the interpretation *v*, what does the formula 'variable x' mean?",
    ["The proposition *v*(x)", "True", "False", "The string \"x\""], 0,
    "examples/Logic.lean line 9."),
  q("What is the meaning of an implication *p* → *q*?",
    ["The Lean statement 'meaning of *p* implies meaning of *q*'", "The Boolean (not p) or q", "That *q* is derivable from *p*"], 0,
    "Line 13. It is semantic implication, not derivability. Derivability is [Proof](#/node/Proof)."),
  q("Why does soundness for Prop-valued interpretations also cover Boolean truth tables?",
    ["A Boolean assignment is a special case of a Prop assignment", "It doesn't", "Because Prop and Bool are the same type in Lean"], 0,
    "Send a variable to the proposition 'its Boolean value is true'. Then `eval` agrees with the truth table."),
 ])

node("evalCtx",
 "A context is true when every assumption in it is",
 "A list of assumptions holds under an interpretation exactly when each formula in the list does. The empty list always holds.",
 r"""## Plain English

**Definition (`evalCtx`, examples/Logic.lean lines 15–17).** Given an interpretation *v* and a list of
[formulas](#/node/PropForm), the list *holds* when every formula in it [evaluates](#/node/eval) to a true
proposition. It is defined by recursion on the list: the empty list holds trivially, and a list *p* followed by
the rest holds when *p* holds and the rest holds.

This is the hypothesis "all assumptions are true" in [soundness](#/node/soundness).
""",
 [q("Does the empty context hold under every interpretation?",
    ["Yes", "No", "Only if every variable is true"], 0,
    "examples/Logic.lean line 16: the empty list maps to True."),
  q("If the context is [*p*, *q*], what does it mean for it to hold under *v*?",
    ["*p* holds under *v* and *q* holds under *v*", "*p* or *q* holds", "*p* implies *q*"], 0,
    "Line 17 unfolds twice: *p* holds, and (*q* holds, and True)."),
  q("Where does `soundness` use this?",
    ["As its hypothesis that all the assumptions are true under *v*", "As its conclusion", "It doesn't"], 0,
    "examples/Logic.lean line 47."),
 ])

node("InCtx",
 "Membership of a formula in a context",
 "A hand-rolled 'is in the list' predicate: the formula equals the head of the list, or it is in the tail.",
 r"""## Plain English

**Definition (`InCtx`, examples/Logic.lean lines 19–21).** A formula *p* is *in* a list when it is equal to the
first entry or is in the rest of the list. Nothing is in the empty list.

This is the same as ordinary list membership. The file defines it by hand instead of using Lean's built-in one,
perhaps because Lea was told to keep the example self-contained (the file has no imports). It is used by the
"use an assumption" rule of [Proof](#/node/Proof).
""",
 [q("Can any formula be in the empty context?",
    ["No", "Yes, every formula", "Only variables"], 0,
    "examples/Logic.lean line 20: the empty list gives False."),
  q("Which rule of the proof system uses `InCtx`?",
    ["The assumption rule `hyp`", "The or-elimination rule", "None"], 0,
    "examples/Logic.lean line 24."),
  q("Is `InCtx` different in meaning from ordinary list membership?",
    ["No. It is the same recursion, written by hand", "Yes. It ignores duplicates", "Yes. It only looks at the first element"], 0,
    "Head or tail, recursively (lines 19–21)."),
 ])

node("Proof",
 "Derivations in natural deduction",
 "A derivation of p from a context Γ is a tree built from eleven rules: use an assumption, plus introduction and elimination rules for and, or, implies and not. No classical rule is included.",
 r"""## Plain English

**Definition (`Proof`, examples/Logic.lean lines 23–34).** `Proof` Γ *p* is the type of *derivations* of the
[formula](#/node/PropForm) *p* from the context Γ (a list of formulas). The rules are:

| Rule | Reading |
|---|---|
| `hyp` | If *p* is [in](#/node/InCtx) Γ, derive *p*. |
| `and_intro` | From *p* and *q*, derive *p* ∧ *q*. |
| `and_elim_l`, `and_elim_r` | From *p* ∧ *q*, derive *p* (or *q*). |
| `or_intro_l`, `or_intro_r` | From *p*, derive *p* ∨ *q* (or from *q*, derive *p* ∨ *q*). |
| `or_elim` | From *p* ∨ *q*, and a derivation of *r* from Γ with *p* added, and one from Γ with *q* added, derive *r*. |
| `imp_intro` | If *q* is derivable from Γ with *p* added, derive *p* → *q*. |
| `imp_elim` | From *p* → *q* and *p*, derive *q* (modus ponens). |
| `not_intro` | If Γ with *p* added derives both *q* and ¬*q*, derive ¬*p*. |
| `not_elim` | From *p* and ¬*p*, derive any *q* (ex falso). |

### Intuitionistic, not classical

None of these rules gives excluded middle or double-negation elimination, so this is intuitionistic propositional
logic. You can't derive ¬¬*x* → *x* for a variable *x* with them (this site didn't check that claim in Lean, but
it is the standard fact about the intuitionistic rules).

### A detail

A derivation lives in `Type`, not `Prop`. So derivations are data that can be inspected or counted, not just
"provability" facts. [Soundness](#/node/soundness) doesn't use this.
""",
 [q("Which rule is modus ponens?",
    ["`imp_elim`", "`imp_intro`", "`not_elim`", "`or_elim`"], 0,
    "examples/Logic.lean line 32: from *p* → *q* and *p*, derive *q*."),
  q("What does `not_elim` let you do?",
    ["From *p* and ¬*p*, derive any formula", "From ¬¬*p*, derive *p*", "Derive *p* ∨ ¬*p*"], 0,
    "Line 34: ex falso quodlibet. The other two are classical principles that are not rules here."),
  q("In `or_elim`, how do the two side derivations differ from the main context?",
    ["Each adds one disjunct to the context as a new assumption", "They use the empty context", "They are identical to it"], 0,
    "Line 30: one derives *r* with *p* added, the other with *q* added."),
  q("Is excluded middle (*p* ∨ ¬*p*) one of the rules?",
    ["No", "Yes, as `or_intro_l`", "Yes, as `hyp`"], 0,
    "The eleven rules are at examples/Logic.lean lines 24–34. None of them is excluded middle."),
 ])

node("in_ctx_eval",
 "Lemma: an assumption from a true context is true",
 "If a formula is in a context that holds under v, the formula holds under v. Proved by walking down the list.",
 r"""## Plain English

**Lemma (`in_ctx_eval`, examples/Logic.lean lines 36–45).** If *p* is [in](#/node/InCtx) the list Γ, and Γ
[holds](#/node/evalCtx) under *v*, then *p* [holds](#/node/eval) under *v*.

**Proof idea.** Induction on the list. The empty list contains nothing (line 38). For a list with head *q*:
either *p* is *q*, and the head of a true context is true (lines 41–43), or *p* is in the tail, and the tail of
a true context is true, so the induction hypothesis applies (lines 44–45).

This is the base case of [soundness](#/node/soundness): the assumption rule.
""",
 [q("What is the lemma by induction on?",
    ["The context (the list of assumptions)", "The formula *p*", "The derivation"], 0,
    "examples/Logic.lean line 37."),
  q("Why is the empty-list case immediate?",
    ["Nothing is in the empty list, so the membership hypothesis is false", "The empty context holds", "Every formula is true"], 0,
    "Line 38 closes it by `contradiction` using the definition of `InCtx` at line 20."),
  q("Which rule of the proof system does this lemma handle in the soundness proof?",
    ["The assumption rule", "Modus ponens", "Or-elimination"], 0,
    "examples/Logic.lean line 49."),
 ])
