# Extra quiz questions for nodes defined in the other files, plus short nodes for the rest of the statement set.
NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

EXTRA = {
 "Models.Entails": [
  q("Is P(x) ⊨ P(y) true in the sense of Entails (one shared assignment)?", ["No: take β with P(β x) true and P(β y) false", "Yes"], 0,
    "`Entails` uses the same β on both sides (InferenceInLean/C_Models.lean lines 45–47)."),
 ],
 "Syntax.Atom": [
  q("What are the free variables of P(x, f(y))?", ["{x, y}", "{x}", "∅"], 0,
    "`Atom.freeVars` unions the free variables of the arguments (InferenceInLean/A_Syntax.lean lines 98–100)."),
 ],
 "Resolution.GeneralFactorizationRule": [
  q("Is the substitution applied to the premise?", ["No, only to the conclusion A ∨ C", "Yes"], 0,
    "`Clause.substitute σ (.pos A :: C)` is the conclusion (InferenceInLean/F_Resolution.lean line 224)."),
 ],
 "Resolution.generalFactorizationRuleSound": [
  q("How is the premise read?", ["As its universal closure", "With its variables free"], 0,
    "`Clause.toClosedFormula` (InferenceInLean/F_Resolution.lean line 201)."),
  q("Which lemma moves from ∀(B ∨ A ∨ C) to (B ∨ A ∨ C)σ?", ["three_three_eight", "eval_append_iff_eval_or", "idempotent_iff_inter_empty"], 0,
    "InferenceInLean/F_Resolution.lean line 211."),
 ],
 "Resolution.validclosed_iff_valid": [
  q("Does it hold for a clause with no variables?", ["Yes, then the closure is the clause itself", "No"], 0,
    "`bigForall []` is the identity (InferenceInLean/A_Syntax.lean line 180)."),
  q("Is the interpretation fixed?", ["Yes, both sides are about the same I", "No"], 0,
    "InferenceInLean/F_Resolution.lean line 93."),
 ],
}

node("Syntax.Literal",
 "Literal: an atom or a negated atom",
 "A literal is `pos a` (the atom a) or `neg a` (¬a). Clauses are lists of literals.",
 r"""## Plain English

**Definition (`Literal`, InferenceInLean/A_Syntax.lean lines 102–106).** See [atoms and literals](#/node/Syntax.Atom).
When a [clause](#/node/Syntax.Clause) is turned into a formula, `pos a` becomes the atom a and `neg a` becomes ¬a
(lines 160–161).
""",
 [q("How many constructors does Literal have?", ["Two", "Three", "One"], 0, "InferenceInLean/A_Syntax.lean lines 104 and 106."),
  q("What formula does `neg a` become inside a clause?", ["¬a", "a", "⊥"], 0, "InferenceInLean/A_Syntax.lean line 161."),
  q("Can a literal contain ∀?", ["No, it is an atom or a negated atom", "Yes"], 0, "InferenceInLean/A_Syntax.lean lines 102–106."),
 ])

node("Syntax.Formula.closed",
 "Closed formulas",
 "A formula is closed when its set of free variables is empty.",
 r"""## Plain English

**Definition (`Formula.closed`, InferenceInLean/A_Syntax.lean lines 170–171).** F is closed iff `F.freeVars = ∅`, with
free variables as defined in [Formula](#/node/Syntax.Formula). Closed formulas have a truth value that doesn't depend
on the assignment ([eval_of_closed](#/node/Semantics.Formula.eval_of_closed)).
""",
 [q("Is ∀x P(x, y) closed?", ["No, y is free", "Yes"], 0, "InferenceInLean/A_Syntax.lean line 153."),
  q("Is ∀x ∃y P(x, y) closed?", ["Yes", "No"], 0, "Both variables are removed by quantifiers (InferenceInLean/A_Syntax.lean lines 153–154)."),
  q("Is the universal closure of a clause closed?", ["Yes, by closedClause_closed", "Not always"], 0, "InferenceInLean/A_Syntax.lean lines 525–531."),
 ])

node("Syntax.Clause.toClosedFormula",
 "Universal closure of a clause",
 "The closed formula ∀x₁ … ∀xₙ (L₁ ∨ … ∨ Lₘ ∨ ⊥), quantifying over each free variable of the clause once.",
 r"""## Plain English

**Definition (`Clause.toClosedFormula`, InferenceInLean/A_Syntax.lean lines 496–497).** Apply `bigForall` to the
duplicate-free list of the clause's free variables (`Clause.freeVarsList`, lines 406–409, duplicate-free by
lines 488–492). It is closed (`closedClause_closed`, lines 525–531). See [Clause](#/node/Syntax.Clause).
""",
 [q("Is each free variable quantified once?", ["Yes, the variable list has no duplicates", "No, once per occurrence"], 0,
    "`nodup_clauseFreeVarsList` (InferenceInLean/A_Syntax.lean lines 488–492)."),
  q("What is the closure of a ground clause?", ["The clause's formula itself", "⊤"], 0, "No variables, so `bigForall []` (InferenceInLean/A_Syntax.lean line 180)."),
  q("Which lemma says a clause and its closure are true in the same interpretations?", ["validclosed_iff_valid", "substitution_lemma"], 0,
    "InferenceInLean/F_Resolution.lean lines 92–93."),
 ])

node("Syntax.Substitution.domain",
 "Domain of a substitution",
 "The domain of σ is the set of variables it actually moves: those x with σ(x) ≠ x.",
 r"""## Plain English

**Definition (`Substitution.domain`, InferenceInLean/A_Syntax.lean lines 580–581).** {x | σ(x) ≠ x}. It may be
infinite, since the project allows any function from variables to terms. See
[Substitution](#/node/Syntax.Substitution).
""",
 [q("What is the domain of the identity substitution?", ["∅", "All variables"], 0, "InferenceInLean/A_Syntax.lean line 581."),
  q("For σ = {x ↦ f(y)}, is y in the domain?", ["No", "Yes"], 0, "σ(y) = y (InferenceInLean/A_Syntax.lean line 581)."),
  q("If the domain is empty, what does σ do to a term?", ["Nothing", "Replaces it by a constant"], 0,
    "`Substitution.id_of_domain_empty` (InferenceInLean/A_Syntax.lean lines 610–612)."),
 ])

node("Syntax.Substitution.codomain",
 "Codomain of a substitution",
 "The codomain of σ is the set of variables occurring in the terms σ(x) for x in the domain.",
 r"""## Plain English

**Definition (`Substitution.codomain`, InferenceInLean/A_Syntax.lean lines 584–585).** {x | x occurs in σ(y) for some
y in the [domain](#/node/Syntax.Substitution.domain)}. It is the set of variables σ can introduce. (Some texts call this
the variable range.)
""",
 [q("For σ = {x ↦ f(y, z)}, what is the codomain?", ["{y, z}", "{x}", "{x, y, z}"], 0, "InferenceInLean/A_Syntax.lean line 585."),
  q("For σ = {x ↦ a} with a constant a, what is the codomain?", ["∅", "{a}", "{x}"], 0, "Constants have no variables."),
  q("Does the codomain look at σ(y) for y outside the domain?", ["No", "Yes"], 0, "`∃ y ∈ σ.domain` (InferenceInLean/A_Syntax.lean line 585)."),
 ])

node("Syntax.Idempotent",
 "Idempotent substitutions",
 "σ is idempotent when σ ∘ σ = σ: applying it a second time changes nothing.",
 r"""## Plain English

**Definition (`Idempotent`, InferenceInLean/A_Syntax.lean lines 606–607).** σ ∘ σ = σ, as functions on variables, with
the project's [composition](#/node/Syntax.Substitution). Characterised by
[idempotent_iff_inter_empty](#/node/Syntax.idempotent_iff_inter_empty).
""",
 [q("Is {x ↦ f(y)} idempotent?", ["Yes", "No"], 0, "y isn't moved, so a second application changes nothing."),
  q("Is {x ↦ y, y ↦ x} idempotent?", ["No", "Yes"], 0, "Applying it twice gives the identity, not σ."),
  q("Is the identity substitution idempotent?", ["Yes", "No"], 0, "Its domain is empty."),
 ])

node("Semantics.Assignment",
 "Assignments",
 "An assignment β gives a value in the universe to every variable. β[x ↦ a] changes the value of x only.",
 r"""## Plain English

**Definition (`Assignment`, InferenceInLean/B_Semantics.lean line 33).** A function from variables to the universe.
`Assignment.modify` (lines 38–40) is β[x ↦ a]; `Assignment.bigModify` (lines 96–101) updates a list of variables in
order. See [Interpretation](#/node/Semantics.Interpretation).
""",
 [q("What is β[x ↦ β(x)]?", ["β itself", "A different assignment"], 0, "`modify_rfl` (InferenceInLean/B_Semantics.lean lines 44–45)."),
  q("Do β[x ↦ a][y ↦ b] and β[y ↦ b][x ↦ a] agree when x ≠ y?", ["Yes", "No"], 0, "`modify_comm` (InferenceInLean/B_Semantics.lean lines 54–56)."),
  q("Is an assignment part of an interpretation?", ["No, it is separate", "Yes"], 0, "InferenceInLean/B_Semantics.lean lines 19–21 and 33."),
 ])

node("Unification.EqualityProblem",
 "Equality problems",
 "An equality problem is a list of equations A ≐ B between atoms, to be solved by one substitution.",
 r"""## Plain English

**Definition (`EqualityProblem`, InferenceInLean/D_Unification.lean lines 21–22).** A list of pairs of atoms.
`EqualityProblem.freeVars` (lines 28–31) is the set of all variables occurring in it. See
[unifiers](#/node/Unification.Unifier).
""",
 [q("What are the two sides of each equation?", ["Atoms", "Terms", "Clauses"], 0, "InferenceInLean/D_Unification.lean line 18."),
  q("Which problem appears in the resolution rule?", ["The single equation A ≐ B", "All atoms of both clauses"], 0, "`[(A, B)]` (InferenceInLean/F_Resolution.lean line 218)."),
  q("What are the variables of P(x) ≐ P(f(y))?", ["{x, y}", "{x}", "∅"], 0, "InferenceInLean/D_Unification.lean line 31."),
 ])

node("Unification.MostGeneralUnifier",
 "Most general unifier",
 "σ is a most general unifier of E if it unifies E and every unifier of E is σ followed by some further substitution.",
 r"""## Plain English

**Definition (`MostGeneralUnifier`, InferenceInLean/D_Unification.lean lines 48–50).** See
[unifiers and mgus](#/node/Unification.Unifier).
""",
 [q("Is {x ↦ a, y ↦ a} an mgu of P(x) ≐ P(y)?", ["No, {x ↦ y} is more general", "Yes"], 0,
    "{x ↦ a, y ↦ a} = {y ↦ a} ∘ {x ↦ y}, but not the other way round."),
  q("Is every mgu a unifier?", ["Yes", "No"], 0, "`mgu_imp_unifier` (InferenceInLean/D_Unification.lean lines 52–53)."),
  q("Is the mgu of a problem unique?", ["Only up to renaming; the definition doesn't pick one", "Yes, exactly"], 0, "The definition is a property of σ (InferenceInLean/D_Unification.lean lines 48–50)."),
 ])

node("Unification.Unifiable",
 "Unifiable problems",
 "A problem is unifiable when some substitution unifies it.",
 r"""## Plain English

**Definition (`Unifiable`, InferenceInLean/D_Unification.lean lines 56–57).** ∃σ, σ is a [unifier](#/node/Unification.Unifier).
""",
 [q("Is P(x) ≐ Q(x) unifiable?", ["No, different predicate symbols never match", "Yes"], 0, "Substitution doesn't change the predicate symbol (InferenceInLean/A_Syntax.lean line 560)."),
  q("Is P(x) ≐ P(f(x)) unifiable?", ["No (occurs check)", "Yes"], 0, "x would have to equal a term strictly containing it."),
  q("Does unifiable require a most general unifier?", ["No, just some unifier", "Yes"], 0, "InferenceInLean/D_Unification.lean line 57."),
 ])

node("Inferences.InferenceSystem",
 "Inference system",
 "A finite list of concrete inferences.",
 r"""## Plain English

**Definition (`InferenceSystem`, InferenceInLean/E_Inference.lean line 28).** See [Inference](#/node/Inferences.Inference).
""",
 [q("Is an InferenceSystem a list or a set?", ["A list", "A set"], 0, "InferenceInLean/E_Inference.lean line 28."),
  q("Can it contain infinitely many inferences?", ["No, lists are finite", "Yes"], 0, "InferenceInLean/E_Inference.lean line 28."),
  q("How many inferences are in the general resolution system of the headline?", ["Two", "One", "Infinitely many"], 0, "InferenceInLean/F_Resolution.lean line 228."),
 ])

node("Inferences.GeneralSoundness",
 "General soundness: N ⊢ C implies N ⊨ C",
 "Everything provable in the system from N is entailed by N.",
 r"""## Plain English

**Definition (`GeneralSoundness`, InferenceInLean/E_Inference.lean lines 62–63).** See [Soundness](#/node/Inferences.Soundness).
""",
 [q("What is the converse property called?", ["Completeness", "Consistency", "Compactness"], 0, "N ⊨ C ⟹ N ⊢ C is completeness."),
  q("Which entailment is used?", ["ClauseSetEntails", "Entails"], 0, "InferenceInLean/E_Inference.lean line 63."),
  q("Which theorem derives it from step-by-step soundness?", ["generalSoundness_of_soundness", "groundResolution_soundness"], 0, "InferenceInLean/E_Inference.lean lines 68–69."),
 ])

node("Resolution.GroundResolutionRule",
 "The ground resolution inference",
 "Premises A ∨ C and ¬A ∨ D, conclusion C ∨ D, no condition.",
 r"""## Plain English

**Definition (`GroundResolutionRule`, InferenceInLean/F_Resolution.lean lines 23–24).** See
[ground resolution](#/node/Resolution.GroundResolution).
""",
 [q("What is the conclusion?", ["C ++ D", "A :: C ++ D", "The empty clause"], 0, "InferenceInLean/F_Resolution.lean line 24."),
  q("What is the condition?", ["True", "An mgu exists"], 0, "InferenceInLean/F_Resolution.lean line 24."),
  q("How many premises?", ["Two", "One"], 0, "InferenceInLean/F_Resolution.lean line 24."),
 ])

node("Resolution.GroundFactorizationRule",
 "The ground factorisation inference",
 "Premise A ∨ A ∨ C, conclusion A ∨ C, no condition.",
 r"""## Plain English

**Definition (`GroundFactorizationRule`, InferenceInLean/F_Resolution.lean lines 27–28).** See
[ground resolution](#/node/Resolution.GroundResolution).
""",
 [q("What is removed?", ["One copy of the repeated A", "The literal A entirely"], 0, "InferenceInLean/F_Resolution.lean line 28."),
  q("Does it factor negative literals?", ["No", "Yes"], 0, "Both copies are `.pos A` (InferenceInLean/F_Resolution.lean line 28)."),
  q("How many premises?", ["One", "Two"], 0, "InferenceInLean/F_Resolution.lean line 28."),
 ])

node("Inferences.Provability",
 "Provability N ⊢ C",
 "C is provable from N in Γ when some proof in Γ has assumptions N and conclusion C.",
 r"""## Plain English

**Definition (`Provability`, InferenceInLean/E_Inference.lean lines 50–51).** ∃ a [proof](#/node/Inferences.Proof)
with `assumptions = N` and `conclusion = C`.
""",
 [q("Is every clause of N provable from N?", ["Yes, by the one-clause proof [C]", "No"], 0, "Assumptions are allowed at any index (InferenceInLean/E_Inference.lean line 44)."),
  q("Does provability depend on the inference system Γ?", ["Yes", "No"], 0, "InferenceInLean/E_Inference.lean line 50."),
  q("Is provability a semantic notion?", ["No, it is syntactic", "Yes"], 0, "It only asks for a list of clauses with the right shape."),
 ])

node("Syntax.Clause.substitute",
 "Applying a substitution to a clause",
 "Cσ applies σ to every literal of C, keeping the order.",
 r"""## Plain English

**Definition (`Clause.substitute`, InferenceInLean/A_Syntax.lean lines 569–571).** Map `Literal.substitute σ` over the
list. See [Substitution](#/node/Syntax.Substitution).
""",
 [q("Does Cσ have the same number of literals as C?", ["Yes, even if two literals become equal", "No, duplicates are merged"], 0,
    "`C.map` keeps the length (InferenceInLean/A_Syntax.lean line 571). Merging is the job of factorisation."),
  q("Does substitution change a literal's sign?", ["No", "Yes"], 0, "InferenceInLean/A_Syntax.lean lines 565–566."),
  q("What is (P(x) ∨ ¬Q(y)){x ↦ a}?", ["P(a) ∨ ¬Q(y)", "P(a) ∨ ¬Q(a)", "P(x) ∨ ¬Q(y)"], 0, "Only x is replaced."),
 ])
