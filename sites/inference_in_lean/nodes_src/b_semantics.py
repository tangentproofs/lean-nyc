NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]


node("Semantics.Interpretation",
 "Interpretation: what the symbols mean",
 "An interpretation picks a universe of values and gives every function symbol a function on lists of values and every predicate symbol a property of lists of values.",
 r"""## Plain English

**Definition (`Interpretation`, InferenceInLean/B_Semantics.lean lines 19–21).** Fix a type `univ` (the universe,
`Universes` is just `Type`, line 15). An interpretation of a [signature](#/node/Syntax.Signature) gives
- for each function symbol f, a function `List univ → univ`, and
- for each predicate symbol P, a predicate `List univ → Prop`.

Because there are no arities, these functions must accept argument lists of any length. The Peano example
(InferenceInLean/G_Examples.lean lines 41–49) simply reads off the first one or two list entries.

Two differences from the notes are worth knowing:
- The universe is a Lean type, and nothing requires it to be non-empty.
- The universe is a **parameter**, not part of the interpretation. So [Valid](#/node/Models.ValidIn) and
  [Entails](#/node/Models.Entails) quantify over interpretations on one fixed universe type. The soundness theorems
  hold for every universe, so this doesn't weaken them.

A **Herbrand interpretation** (`HerbrandInterpretation`, lines 24–25) takes the ground terms as the universe and
interprets each function symbol as "build that term".

An **assignment** (`Assignment`, line 33) gives a value to every variable, and `β.modify x a` (lines 38–40), written
β[x ↦ a], changes the value of one variable.
""",
 [q("What is the type of the meaning of a function symbol?", ["List univ → univ", "univ × univ → univ", "Term → Term"], 0,
    "InferenceInLean/B_Semantics.lean line 20."),
  q("Must the universe be non-empty?", ["No, nothing in the definition requires it", "Yes"], 0,
    "`univ : Universes` is any `Type` (InferenceInLean/B_Semantics.lean lines 15–21)."),
  q("What does β[x ↦ a] do to a variable y ≠ x?", ["Returns β(y)", "Returns a", "Is undefined"], 0,
    "InferenceInLean/B_Semantics.lean line 40."),
 ],
 caveats=["Universes are not required to be non-empty, unlike the usual textbook definition."])


node("Semantics.Formula.eval",
 "Evaluating terms and formulas",
 "Given an interpretation I and an assignment β, a term evaluates to a value and a formula to a Lean proposition, by the usual Tarski clauses.",
 r"""## Plain English

**Definitions (InferenceInLean/B_Semantics.lean lines 63–85).**
- `Term.eval I β` (lines 63–66): a variable x gives β(x); f(t₁, …, tₙ) gives I(f) applied to the values of the tᵢ.
- `Atom.eval I β` (lines 69–71): P(t₁, …, tₙ) gives I(P) applied to the values of the tᵢ.
- `Formula.eval I β` (lines 74–85): ⊥ is `False`, ⊤ is `True`, the connectives are Lean's ¬ ∧ ∨ → ↔, and
  - ∀x F holds if F holds under β[x ↦ a] for **every** a in the universe,
  - ∃x F holds if F holds under β[x ↦ a] for **some** a.

The result is a Lean `Prop`, not a Boolean. So the semantics is classical mathematics, not a decision procedure.

The basic facts about evaluation are:
- [eval_of_closed](#/node/Semantics.Formula.eval_of_closed): a closed formula's value doesn't depend on β;
- [substitution_lemma](#/node/Models.substitution_lemma): evaluating tσ under β is the same as evaluating t under
  "β after σ".
""",
 [q("Under what condition does ∃x F hold at I, β?", ["F holds at β[x ↦ a] for some a", "F holds at β", "F holds for every a"], 0,
    "InferenceInLean/B_Semantics.lean line 85."),
  q("What does a formula evaluate to?", ["A Lean proposition (Prop)", "A Bool", "A term"], 0,
    "`Formula.eval … : Formula sig X -> Prop` (InferenceInLean/B_Semantics.lean line 75)."),
  q("How is a variable evaluated?", ["By the assignment: β(x)", "By the interpretation of x", "It cannot be"], 0,
    "InferenceInLean/B_Semantics.lean line 65."),
 ])


node("Semantics.Formula.eval_of_closed",
 "Headline: a closed formula's truth doesn't depend on the assignment",
 "If a formula has no free variables, it is either true under every assignment or false under every assignment. The proof first shows a stronger statement for formulas whose free variables are all re-assigned.",
 r"""## Plain English

**Theorem (`Formula.eval_of_closed`, InferenceInLean/B_Semantics.lean lines 600–609).** For every interpretation I
and every [closed](#/node/Syntax.Formula) formula F, and any two assignments β and γ:

I, β ⊨ F has the same truth value as I, γ ⊨ F.

This is what lets the project talk about a closed formula, such as the universal closure of a
[clause](#/node/Syntax.Clause), being simply "true in I". It is used as `validIn_of_entails_closed`
(InferenceInLean/C_Models.lean lines 164–171): if a closed formula holds under one assignment, it holds under all.

### The stronger statement

`Formula.eval_of_many_free` (lines 545–598): if every free variable of F is among x₁, …, xₙ, then F has the same
value under β[x₁ ↦ a₁, …, xₙ ↦ aₙ] and γ[x₁ ↦ a₁, …, xₙ ↦ aₙ], for any β and γ. (The multi-variable update
β[x₁ ↦ a₁, …] is `Assignment.bigModify`, lines 96–101.) The closed case is n = 0.

The stronger form is needed because the induction passes under quantifiers: inside ∀y G, the variable y is free in G
and gets re-assigned, so the list of re-assigned variables must grow.
""",
 [q("Does the theorem say that every closed formula is true?", ["No, only that its value is the same for all assignments", "Yes"], 0,
    "The statement is an equality between two evaluations (InferenceInLean/B_Semantics.lean line 603)."),
  q("Does it compare different interpretations?", ["No, the interpretation I is fixed", "Yes"], 0,
    "One `I` appears on both sides (InferenceInLean/B_Semantics.lean lines 601–603)."),
  q("Why is the stronger statement eval_of_many_free needed?",
    ["Under a quantifier the bound variable becomes free and is re-assigned, so the induction needs a list of re-assigned variables",
     "Because Lean has no induction on formulas", "To handle function symbols"], 0,
    "See the comment at InferenceInLean/B_Semantics.lean lines 371–378."),
 ],
 caveats=["Proof complete in the source, with no sorry; not machine-checked for this site."],
 widgets=walk("How the proof goes (InferenceInLean/B_Semantics.lean, lines 545-609)", [
  {"text": "Generalise: if the free variables of F are among x₁, …, xₙ, then β and γ, both updated at those variables with the same values, give F the same value (lines 545–549)."},
  {"text": "Induction on F, generalising β, γ and the lists (lines 551–552). ⊥, ⊤ are trivial (lines 553–554)."},
  {"text": "Atoms: reduce to the same fact for terms, by induction on terms (lines 555–558; the term and atom versions are lines 423–495)."},
  {"text": "Connectives: apply the induction hypotheses to both parts (lines 559–567)."},
  {"text": "∀y G and ∃y G: split on whether y is already in the list and whether y is free in G, and extend or reorder the list of updates (lines 568–598, using the helper on lines 500–543)."},
  {"text": "The closed case is the empty list: β[] = β and γ[] = γ (lines 604–609).",
   "lean": "have s := Formula.eval_of_many_free I F [] [] rfl (by aesop) β γ"},
 ]))


node("Models.ValidIn",
 "Truth in an interpretation, validity and satisfiability",
 "F is true in I when it holds under every assignment. It is valid when it is true in every interpretation, and satisfiable when it holds for some interpretation and assignment. All of these are relative to one fixed universe type.",
 r"""## Plain English

**Definitions (InferenceInLean/C_Models.lean).**
- `EntailsInterpret I β F` (lines 22–24), written I, β ⊨ F: just [Formula.eval](#/node/Semantics.Formula.eval).
- `ValidIn F I` (lines 33–34), I ⊨ F: F holds for **every** assignment β.
- `Valid F` (lines 38–39), ⊨ F: every interpretation and every assignment.
- `Satisfiable F` (lines 74–75): some interpretation and some assignment. `Unsatisfiable` is its negation (lines 78–79).

The usual dualities are proved, as in Proposition 3.3.3 of the notes: F is valid iff ¬F is unsatisfiable
(`valid_iff_not_unsat`, lines 81–82), and F ⊨ G iff F ∧ ¬G is unsatisfiable (`entails_iff_and_not_unsat`,
lines 84–85).

**The universe is fixed.** Each of these takes the universe type as an (implicit) parameter. So `Valid F` really says
"valid over interpretations with values in this one type", not over all universes at once. Every theorem quantifies
over the universe, so the results still hold for all universes.

For a [clause](#/node/Syntax.Clause), "true in I" (`ValidIn`) means: true for every value of its variables. That is how
clauses are read throughout the soundness proofs.
""",
 [q("When is a clause C true in I in the sense of ValidIn?", ["When it holds for every assignment of its variables", "When it holds for some assignment", "When it is closed"], 0,
    "`ValidIn F I := ∀ β, EntailsInterpret I β F` (InferenceInLean/C_Models.lean lines 33–34)."),
  q("Which is proved?", ["F valid ⟺ ¬F unsatisfiable", "F valid ⟺ F satisfiable", "F satisfiable ⟺ ¬F valid"], 0,
    "`valid_iff_not_unsat` (InferenceInLean/C_Models.lean lines 81–82)."),
  q("Over which universes does `Valid F` quantify?", ["Only interpretations on one fixed universe type", "All types at once"], 0,
    "`univ` is a section variable, not quantified inside `Valid` (InferenceInLean/C_Models.lean lines 16 and 38–39)."),
 ])


node("Models.Entails",
 "Entailment F ⊨ G",
 "F entails G when every interpretation and assignment that make F true also make G true.",
 r"""## Plain English

**Definition (`Entails`, InferenceInLean/C_Models.lean lines 45–48).** F ⊨ G means: for all I and β, if I, β ⊨ F then
I, β ⊨ G.

Note the assignment is shared: this is entailment "pointwise" in β. For closed formulas that makes no difference, by
[eval_of_closed](#/node/Semantics.Formula.eval_of_closed). The project uses `Entails` between **closed** formulas
in [generalResolutionRuleSound](#/node/Resolution.generalResolutionRuleSound).

Related facts: F ⊨ G iff ⊨ F → G (`entails_iff_imp_valid`, lines 51–53), and the set version `SetEntails`
(lines 57–60) with N ⊨ G iff N ∪ {¬G} is unsatisfiable (`setEntails_iff_union_not_unsat`, lines 151–160).

For sets of **clauses** the project uses a different notion, [ClauseSetEntails](#/node/Models.ClauseSetEntails),
which reads clauses as universally quantified.
""",
 [q("Does `Entails` use the same assignment on both sides?", ["Yes", "No, each side has its own"], 0,
    "InferenceInLean/C_Models.lean lines 46–47."),
  q("F ⊨ G is proved equivalent to…", ["⊨ (F → G)", "⊨ F and ⊨ G", "F ∧ G satisfiable"], 0,
    "`entails_iff_imp_valid` (InferenceInLean/C_Models.lean lines 51–53)."),
 ])


node("Models.ClauseSetEntails",
 "Clause-set entailment N ⊨ C",
 "A set of clauses N entails a clause C when every interpretation in which all clauses of N are true (for all values of their variables) also makes C true for all values of its variables. This is the notion soundness is about.",
 r"""## Plain English

**Definition (`ClauseSetEntails`, InferenceInLean/C_Models.lean lines 63–66).** For a set N of clauses and a clause C:

for every interpretation I, if every D ∈ N is [true in I](#/node/Models.ValidIn) (under all assignments), then C is
true in I (under all assignments).

This reads every clause as implicitly universally quantified, **each clause separately**. That is the standard reading
in resolution: the clauses ∀x P(x) and ∀x ¬P(x) ∨ Q(x) don't share their x.

Contrast with [Entails](#/node/Models.Entails), where one assignment β is used throughout. The difference matters:
P(x) does **not** pointwise-entail P(y), but as clauses {P(x)} ⊨ P(y) does hold, because P(x) true for every x makes
P(y) true for every y.

[Soundness](#/node/Inferences.Soundness) of an inference system is stated with `ClauseSetEntails`.
""",
 [q("Does {P(x)} ⊨ P(y) hold in the sense of ClauseSetEntails?", ["Yes", "No"], 0,
    "If P(x) holds for all assignments, so does P(y) (InferenceInLean/C_Models.lean lines 63–66)."),
  q("How are clauses read in ClauseSetEntails?", ["Each universally quantified on its own", "All sharing one assignment", "Existentially quantified"], 0,
    "Each clause uses `ValidIn`, which quantifies over all β (InferenceInLean/C_Models.lean line 66)."),
  q("Is the interpretation's universe also quantified inside ClauseSetEntails?", ["No, it is a fixed parameter", "Yes"], 0,
    "`univ` comes from the section variables (InferenceInLean/C_Models.lean line 16)."),
 ])


node("Models.substitution_lemma",
 "The substitution lemma: I(β)(tσ) = I(β ∘ σ)(t)",
 "Evaluating a substituted term is the same as evaluating the original term under the assignment that sends each x to the value of σ(x). The same holds for clauses (Lemma 3.3.5 of the notes, here only for clauses).",
 r"""## Plain English

**Theorem (`substitution_lemma`, InferenceInLean/C_Models.lean lines 200–214).** For any interpretation I, assignment
β, [substitution](#/node/Syntax.Substitution) σ and term t:

value of tσ under β = value of t under β ∘ σ,

where β ∘ σ (`Assignment.compose`, lines 179–181) is the assignment x ↦ value of σ(x) under β.

**For clauses** (`three_three_five`, lines 217–243): the same equation with a [clause](#/node/Syntax.Clause) C in
place of t: Cσ is true under β iff C is true under β ∘ σ. `three_three_six` (lines 246–250) restates it with ⊨.

The notes state Lemma 3.3.5 for arbitrary formulas. The Lean version is only for clauses, which have no quantifiers
and so avoid variable capture. That is all the resolution proofs need.

**Consequence** (`valid_sub_of_valid`, lines 294–302): if a clause C is true in I for every assignment, so is Cσ.
Take any β and apply the lemma: Cσ under β is C under β ∘ σ, which is true.
""",
 [q("If σ(x) = f(y), what is β ∘ σ applied to x?", ["The value of f(y) under β", "β(x)", "f(β(y)) as a term"], 0,
    "`fun x ↦ Term.eval I β (σ x)` (InferenceInLean/C_Models.lean line 181)."),
  q("For what kind of formula is the Lean `three_three_five` stated?", ["Clauses only", "All formulas", "Closed formulas only"], 0,
    "Its argument is `C : Clause _ _` (InferenceInLean/C_Models.lean line 218)."),
  q("Why is the clause case enough to avoid trouble with quantifiers?",
    ["Clauses contain no quantifiers, so no variable capture can occur", "Lean forbids quantifiers"], 0,
    "`Clause.toFormula` only uses ∨, ¬, atoms and ⊥ (InferenceInLean/A_Syntax.lean lines 158–161)."),
 ])


node("Models.three_three_seven",
 "∀-closure doesn't change truth in I (Lemmas 3.3.7 and 3.3.8)",
 "A formula is true in I for all assignments exactly when its universal closure ∀x₁…xₙ F is. Combined with the substitution lemma, if ∀x C is true in I then so is any universal closure of Cσ.",
 r"""## Plain English

**Lemma (`three_three_seven`, InferenceInLean/C_Models.lean lines 255–291).** For a list of distinct variables
x₁, …, xₙ:

I ⊨ ∀x₁ … ∀xₙ F **iff** I ⊨ F.

The comment (lines 252–254) notes that the notes assume F closed; the Lean version doesn't, so it is slightly stronger.

**Lemma (`three_three_eight`, lines 305–314).** For a clause C, a substitution σ and any two lists of distinct
variables xs and ys: if I ⊨ ∀xs C then I ⊨ ∀ys (Cσ). Proof: strip ∀xs with 3.3.7, use
[valid_sub_of_valid](#/node/Models.substitution_lemma), and put ∀ys back with 3.3.7.

**Used as** `validclosed_iff_valid` (InferenceInLean/F_Resolution.lean lines 92–101): a clause is true in I iff its
universal closure (`toClosedFormula`) is. This is how the resolution proofs move between closed formulas and open
clauses.
""",
 [q("Must the variable list in three_three_seven have no repeats?", ["Yes, it assumes xs.Nodup", "No"], 0,
    "`huniq : xs.Nodup` (InferenceInLean/C_Models.lean line 256)."),
  q("In three_three_eight, must ys be the free variables of Cσ?", ["No, any list of distinct variables works", "Yes"], 0,
    "ys is arbitrary with `hyuniq : ys.Nodup` (InferenceInLean/C_Models.lean lines 306–308)."),
  q("Is three_three_seven about truth under one assignment or under all?", ["All (ValidIn on both sides)", "One"], 0,
    "Both sides are `ValidIn … I` (InferenceInLean/C_Models.lean line 257)."),
 ])


import importlib.util as _u, os as _o
_s = _u.spec_from_file_location("_zx", _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "z_extra.py"))
_m = _u.module_from_spec(_s); _s.loader.exec_module(_m)
for _n in NODES:
    _n["quiz"] += _m.EXTRA.get(_n["id"], [])
