NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]


node("Resolution.GroundResolution",
 "Ground resolution and ground factorisation",
 "Ground resolution cuts A out of A ∨ C and ¬A ∨ D to give C ∨ D. Ground factorisation merges a repeated A ∨ A ∨ C into A ∨ C. Ground means no variables at all.",
 r"""## Plain English

Everything here uses the variable type `Empty`, so clauses have no variables.

**Resolution** (`GroundResolutionRule A C D`, InferenceInLean/F_Resolution.lean lines 23–24):

premises A ∨ C and ¬A ∨ D, conclusion C ∨ D, no side condition.

**Factorisation** (`GroundFactorizationRule A C`, lines 27–28):

premise A ∨ A ∨ C, conclusion A ∨ C, no side condition.

**The system** (`GroundResolution sig A C D`, lines 32–34) is the two-element list of these two
[inferences](#/node/Inferences.Inference), for one fixed choice of the atom A and the clauses C, D.

In the clause lists the literal A (or ¬A) is the **first** element; C and D are the rest of the clause, and C ∨ D is
list concatenation `C ++ D`.
""",
 [q("From the ground clauses P(a) ∨ Q(b) and ¬P(a), what does ground resolution give?", ["Q(b)", "P(a)", "The empty clause"], 0,
    "Take A = P(a), C = [Q(b)], D = [] in InferenceInLean/F_Resolution.lean lines 23–24."),
  q("Does ground factorisation have a side condition?", ["No (it is True)", "Yes, an mgu"], 0,
    "InferenceInLean/F_Resolution.lean line 28."),
  q("Where must A sit in the premise clause?", ["At the front of the list", "Anywhere", "At the end"], 0,
    "`.pos A :: C` (InferenceInLean/F_Resolution.lean line 24)."),
 ])


node("Resolution.groundResolution_soundness",
 "Headline: ground resolution is sound",
 "For every ground atom A and ground clauses C, D, the resolution step from A ∨ C and ¬A ∨ D to C ∨ D, and the factorisation step from A ∨ A ∨ C to A ∨ C, never lead from true clauses to a false one.",
 r"""## Plain English

**Theorem (`groundResolution_soundness`, InferenceInLean/F_Resolution.lean lines 68–88).** For every atom A and
clauses C, D without variables, the two-inference system [GroundResolution](#/node/Resolution.GroundResolution) A C D
is [sound](#/node/Inferences.Soundness):
- {A ∨ C, ¬A ∨ D} ⊨ C ∨ D, and
- {A ∨ A ∨ C} ⊨ A ∨ C.

### Why it is true

In any interpretation, A is either true or false. If A is true, ¬A ∨ D forces D, so C ∨ D holds. If A is false, A ∨ C
forces C, so C ∨ D holds. Factorisation is just A ∨ A ∨ C ⟺ A ∨ C.

The Lean proof needs one bookkeeping lemma, `eval_append_iff_eval_or` (lines 36–55): the clause `C ++ D` is true iff
the disjunction C ∨ D is. After that, `aesop` finishes both cases.

Since A, C and D are arbitrary, this is soundness of the two ground **rules**, one instance at a time.
""",
 [q("Why is C ∨ D true whenever A ∨ C and ¬A ∨ D are?", ["Case split on A: one of the premises then forces C or D", "Because C and D are always true", "By unification"], 0,
    "The resolution case, InferenceInLean/F_Resolution.lean lines 77–85."),
  q("Does this theorem allow variables in C and D?", ["No, the variable type is Empty", "Yes"], 0,
    "`Clause sig Empty` (InferenceInLean/F_Resolution.lean line 68)."),
  q("Which lemma converts list concatenation into disjunction?", ["eval_append_iff_eval_or", "substitution_lemma", "three_three_seven"], 0,
    "InferenceInLean/F_Resolution.lean lines 36–39."),
 ],
 caveats=["Proof complete in the source, with no sorry; the final steps are closed by `aesop`. Not machine-checked for this site."],
 widgets=walk("How the proof goes (InferenceInLean/F_Resolution.lean, lines 68-88)", [
  {"text": "Take a rule of the system, its (trivial) condition, an interpretation I and the truth of its premises (line 70)."},
  {"text": "The rule is one of the two list elements (lines 74–75).", "link": "Resolution.GroundResolution"},
  {"text": "Resolution: get A ∨ C and ¬A ∨ D under β (lines 77–83)."},
  {"text": "Rewrite the conclusion C ++ D as the disjunction C ∨ D, and let aesop do the case split on A (lines 84–85).",
   "lean": "rw [eval_append_iff_eval_or]"},
  {"text": "Factorisation: aesop directly (lines 87–88)."},
 ]))


node("Resolution.GeneralResolutionRule",
 "General resolution: D ∨ B and C ∨ ¬A give (D ∨ C)σ",
 "First-order resolution: if σ is a most general unifier of the atoms A and B, then from B ∨ D and ¬A ∨ C you may derive (D ∨ C)σ. This is the rule of Proposition 3.10.14 in the notes.",
 r"""## Plain English

**Definition (`GeneralResolutionRule A B C D σ`, InferenceInLean/F_Resolution.lean lines 215–218).** The
[inference](#/node/Inferences.Inference) with
- premises: B ∨ D and ¬A ∨ C,
- conclusion: (D ∨ C)σ,
- condition: σ is a [most general unifier](#/node/Unification.Unifier) of A ≐ B.

As in the ground case, the resolved literal is the first element of each clause list.

**Example.** From P(x) ∨ Q(x) and ¬P(f(y)) ∨ R(y), with B = P(x), A = P(f(y)) and σ = {x ↦ f(y)}, derive
Q(f(y)) ∨ R(y).

The notes rename the two premises apart (no shared variables) before resolving. The Lean rule doesn't require that.
For **soundness** it is not needed, since each premise is read as separately universally quantified
([ClauseSetEntails](#/node/Models.ClauseSetEntails)), but a complete prover would need renaming.
""",
 [q("What is the side condition of the rule?", ["σ is an mgu of A ≐ B", "C and D are ground", "None"], 0,
    "InferenceInLean/F_Resolution.lean line 218."),
  q("Is σ applied to the premises or the conclusion?", ["Only to the conclusion D ++ C", "Only to the premises"], 0,
    "`(D ++ C).substitute σ` (InferenceInLean/F_Resolution.lean line 218)."),
  q("Must the two premises have disjoint variables?", ["No, the Lean rule doesn't require it", "Yes"], 0,
    "No such condition appears in InferenceInLean/F_Resolution.lean lines 215–218."),
 ])


node("Resolution.GeneralFactorizationRule",
 "General factorisation: B ∨ A ∨ C gives (A ∨ C)σ",
 "First-order (positive) factorisation: if σ is a most general unifier of A and B, then from B ∨ A ∨ C you may derive (A ∨ C)σ.",
 r"""## Plain English

**Definition (`GeneralFactorizationRule A B C σ`, InferenceInLean/F_Resolution.lean lines 221–224).**
- premise: B ∨ A ∨ C,
- conclusion: (A ∨ C)σ,
- condition: σ is a [most general unifier](#/node/Unification.Unifier) of A ≐ B.

Example: from P(x) ∨ P(a) ∨ Q(x) with σ = {x ↦ a}, derive P(a) ∨ Q(a).

Only positive literals are factored, as in the notes.
""",
 [q("From P(x) ∨ P(a) with σ = {x ↦ a}, what does factorisation give?", ["P(a)", "P(x)", "P(x) ∨ P(a)"], 0,
    "Take B = P(x), A = P(a), C = [] in InferenceInLean/F_Resolution.lean line 224."),
  q("Are negative literals factored by this rule?", ["No, both literals are `.pos`", "Yes"], 0,
    "InferenceInLean/F_Resolution.lean line 224."),
 ])


node("Resolution.generalResolutionRuleSound",
 "Resolution step is sound (Proposition 3.10.14)",
 "If σ unifies A and B, then the universal closures of B ∨ D and ¬A ∨ C together entail the universal closure of (D ∨ C)σ.",
 r"""## Plain English

**Theorem (`generalResolutionRuleSound`, InferenceInLean/F_Resolution.lean lines 104–196).** Let σ be a most general
unifier of A ≐ B. Then

∀(B ∨ D) ∧ ∀(¬A ∨ C) ⊨ ∀((D ∨ C)σ),

where ∀ means [universal closure](#/node/Syntax.Clause) over all free variables. The comment on line 103 calls it a
direct formalisation of Proposition 3.10.14 of the notes.

### Proof idea

1. The premises are closed, so true under one assignment means true under all
   ([eval_of_closed](#/node/Semantics.Formula.eval_of_closed)).
2. Apply σ: (B ∨ D)σ and (¬A ∨ C)σ are true in I for every assignment ([Lemma 3.3.8](#/node/Models.three_three_seven)).
3. Since σ is a unifier, Aσ = Bσ, so they have the same truth value under any β.
4. Fix β. If Bσ is true, then Aσ is true, so (¬A ∨ C)σ gives Cσ. If Bσ is false, (B ∨ D)σ gives Dσ. Either way
   (D ∨ C)σ is true.
5. Close it up again with ∀ ([validclosed_iff_valid](#/node/Models.three_three_seven)).

Only "σ is a unifier" is used; most-generality isn't needed (see the Faithfulness notes).
""",
 [q("Which property of σ does the proof actually use?", ["Aσ = Bσ", "That σ is idempotent", "That σ is most general"], 0,
    "`hBσeqAσ` (InferenceInLean/F_Resolution.lean lines 174–175) is the only use of `hmgu`."),
  q("Why can the proof switch from one assignment β to all assignments?", ["The premises are closed formulas", "Because σ is a unifier", "Because the universe is finite"], 0,
    "`validIn_of_entails_closed` (InferenceInLean/F_Resolution.lean lines 124–125)."),
  q("In step 4, what is the case split on?", ["Whether Bσ is true under β", "Whether C is empty", "Whether σ is the identity"], 0,
    "InferenceInLean/F_Resolution.lean line 178."),
 ],
 caveats=["Stronger than needed: the hypothesis says 'most general unifier', but only the unifier part is used, so the statement would hold for any unifier."],
 widgets=walk("How the proof goes (InferenceInLean/F_Resolution.lean, lines 104-196)", [
  {"text": "Both premises are closed, and true under β, so they are true in I for every assignment (lines 115–125).",
   "lean": "have hleftvalid : ValidIn left I := validIn_of_entails_closed I _ hleftclosed (by use β)", "link": "Semantics.Formula.eval_of_closed"},
  {"text": "Apply Lemma 3.3.8 to get (B ∨ D)σ and (¬A ∨ C)σ, then strip the quantifiers with 3.3.7 (lines 126–153).", "link": "Models.three_three_seven"},
  {"text": "Read off: if Bσ is false then Dσ; if Aσ is true then Cσ (lines 154–173)."},
  {"text": "Because σ unifies A and B, Aσ and Bσ have the same value everywhere (lines 174–175).",
   "lean": "have hBσeqAσ: ∀ (β : Assignment X univ), Atom.eval I β (A.substitute σ)", "link": "Unification.Unifier"},
  {"text": "Case split on Bσ to get (D ++ C)σ under every assignment (lines 176–195).",
   "lean": "by_cases hBσ : Atom.eval I β' (B.substitute σ)"},
  {"text": "Turn this back into the closed formula at β (line 196).",
   "lean": "exact validclosed_iff_valid.mp hCDσ β"},
 ]))


node("Resolution.generalFactorizationRuleSound",
 "Factorisation step is sound",
 "If σ unifies A and B, the universal closure of B ∨ A ∨ C entails the universal closure of (A ∨ C)σ.",
 r"""## Plain English

**Theorem (`generalFactorizationRuleSound`, InferenceInLean/F_Resolution.lean lines 198–212).** Let σ be a most
general unifier of A ≐ B. Then ∀(B ∨ A ∨ C) ⊨ ∀((A ∨ C)σ).

Proof: the premise is closed, so it is true for all assignments. By [Lemma 3.3.8](#/node/Models.three_three_seven)
(B ∨ A ∨ C)σ = Bσ ∨ Aσ ∨ Cσ is true for every assignment. Since Bσ = Aσ, this is Aσ ∨ Cσ. The final step is `aesop`
(line 212).
""",
 [q("Why does Bσ ∨ Aσ ∨ Cσ reduce to Aσ ∨ Cσ?", ["Because σ unifies A and B, so Bσ = Aσ", "Because B is false", "Because C is empty"], 0,
    "The `hmgu` hypothesis, used by `aesop` at InferenceInLean/F_Resolution.lean line 212."),
 ])


node("Resolution.generalResolution_soundness",
 "Headline: general (first-order) resolution is sound",
 "For all atoms A, B, clauses C, D and substitutions σ, the system made of the general resolution step and the general factorisation step is sound: whenever σ is an mgu of A and B, the premises entail the conclusion, reading clauses as universally quantified.",
 r"""## Plain English

**Theorem (`generalResolution_soundness`, InferenceInLean/F_Resolution.lean lines 226–253).** For all atoms A, B,
clauses C, D and substitutions σ, the two-inference system

[ [GeneralResolutionRule](#/node/Resolution.GeneralResolutionRule) A B C D σ,
[GeneralFactorizationRule](#/node/Resolution.GeneralFactorizationRule) A B C σ ]

is [sound](#/node/Inferences.Soundness). Spelled out: if σ is a most general unifier of A ≐ B, then in every
interpretation I,
- if B ∨ D and ¬A ∨ C are true in I (for all values of their variables), so is (D ∨ C)σ;
- if B ∨ A ∨ C is true in I, so is (A ∨ C)σ.

This is the main result of the project. With
[generalSoundness_of_soundness](#/node/Inferences.generalSoundness_of_soundness) it gives the familiar consequence:
anything derived from N by these rules is true in every model of N. In particular, if the empty clause (⊥) is derived,
N has no model, which is how resolution provers refute.

### How it is proved

It translates between open clauses and their universal closures with `validclosed_iff_valid` (lines 92–101), and
then applies the two step lemmas [generalResolutionRuleSound](#/node/Resolution.generalResolutionRuleSound) and
[generalFactorizationRuleSound](#/node/Resolution.generalFactorizationRuleSound).

### What it covers

- **Soundness only.** Completeness of resolution (every unsatisfiable clause set refutes to ⊥) is not attempted.
- **Each instance separately.** The theorem is about the two concrete inferences for one choice of A, B, C, D, σ.
  Because all of these are universally quantified, this is the same as soundness of the two rules.
- **No sorry is used.** The mgu is a hypothesis, so the sorry in
  [unifiable_iff_mgu_idempot](#/node/Unification.unifiable_iff_mgu_idempot) is not involved.
""",
 [q("What does the theorem guarantee?", ["Every instance of the two rules with an mgu leads from true clauses to a true clause",
     "Every unsatisfiable clause set can be refuted", "An mgu always exists"], 0,
    "`Soundness` of the two-element list (InferenceInLean/F_Resolution.lean lines 226–228)."),
  q("Does it prove completeness of resolution?", ["No", "Yes"], 0, "Only `Soundness` is concluded (InferenceInLean/F_Resolution.lean line 228)."),
  q("How is a clause with variables read?", ["As true for all values of its variables", "As true for some values", "As a ground clause"], 0,
    "Through `ClauseSetEntails` and `ValidIn` (InferenceInLean/C_Models.lean lines 63–66)."),
  q("Does it depend on the sorry in the unification file?", ["No", "Yes"], 0,
    "The mgu is assumed as the inference's condition (InferenceInLean/F_Resolution.lean line 218)."),
 ],
 caveats=["Proof complete in the source, with no sorry (several steps closed by `simp_all`/`aesop`); not machine-checked for this site.",
          "Soundness for each rule instance; the combination with generalSoundness_of_soundness for multi-step proofs is not stated as one theorem.",
          "The resolved literal must be first in each premise list; resolving on a literal in the middle needs a reordered clause."],
 widgets=walk("How the proof goes (InferenceInLean/F_Resolution.lean, lines 226-253)", [
  {"text": "Take a rule of the list, its condition (σ is an mgu), an interpretation I and the truth of its premises in I (line 229)."},
  {"text": "The rule is either the resolution step or the factorisation step (lines 231–232)."},
  {"text": "Resolution: switch the premises to their universal closures (lines 237–242).", "link": "Models.three_three_seven"},
  {"text": "Apply the step lemma, Proposition 3.10.14 (line 243).",
   "lean": "have conclosed := @generalResolutionRuleSound sig X univ _ A B C D σ hcond I", "link": "Resolution.generalResolutionRuleSound"},
  {"text": "Switch the conclusion back from its closure and finish with simp_all (lines 244–245).",
   "lean": "apply validclosed_iff_valid.mpr"},
  {"text": "Factorisation: the same pattern with the factorisation step lemma (lines 247–253).",
   "lean": "have conclosed := @generalFactorizationRuleSound sig X univ _ A B C σ hcond I", "link": "Resolution.generalFactorizationRuleSound"},
 ]))


node("Resolution.validclosed_iff_valid",
 "A clause is true in I iff its universal closure is",
 "For any clause C and interpretation I, C holds under every assignment exactly when ∀x₁…xₙ C holds (under every assignment), where x₁…xₙ are C's free variables.",
 r"""## Plain English

**Lemma (`validclosed_iff_valid`, InferenceInLean/F_Resolution.lean lines 92–101).** I ⊨ C iff I ⊨ C's universal
closure. It is the special case of [Lemma 3.3.7](#/node/Models.three_three_seven) with the duplicate-free list of
C's free variables (`nodup_clauseFreeVarsList`, InferenceInLean/A_Syntax.lean lines 488–492).

It is the bridge between the step lemmas, stated with closed formulas and [Entails](#/node/Models.Entails), and
[Soundness](#/node/Inferences.Soundness), stated with open clauses and
[ClauseSetEntails](#/node/Models.ClauseSetEntails).
""",
 [q("Which lemma does it specialise?", ["three_three_seven", "substitution_lemma", "eval_append_iff_eval_or"], 0,
    "InferenceInLean/F_Resolution.lean line 100."),
 ])


import importlib.util as _u, os as _o
_s = _u.spec_from_file_location("_zx", _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "z_extra.py"))
_m = _u.module_from_spec(_s); _s.loader.exec_module(_m)
for _n in NODES:
    _n["quiz"] += _m.EXTRA.get(_n["id"], [])
