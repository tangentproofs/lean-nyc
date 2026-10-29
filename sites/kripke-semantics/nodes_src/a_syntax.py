NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

node("Syntax.Tm", "Formulas of propositional logic",
 "Formulas are built from numbered variables with and, or, implies, true and false. There is no separate negation: 'not φ' is written as 'φ implies false'.",
 r"""## Plain English

**Definition (`Tm`, Logic/Syntax.lean lines 7–13).** A formula is one of:

- a propositional variable, identified by a natural number (variable 0, variable 1, …);
- a conjunction φ ∧ ψ, a disjunction φ ∨ ψ, or an implication φ ⇒ ψ of two smaller formulas;
- the constant *true* (`tt`) or the constant *false* (`ff`).

Lines 17–19 give the usual infix notation for the three connectives, with implication binding loosest
and associating to the right.

**Negation is not primitive.** Throughout the project, "not φ" is the formula φ ⇒ ff. This is the
standard choice in intuitionistic logic, where ¬φ *means* "φ leads to a contradiction". You can see it
in [the excluded-middle result](#/node/Kripke.ExcludedMiddle.em_not_provable), whose formula is
"variable 0, or (variable 0 implies false)".

The formulas are the ones of full **intuitionistic propositional logic** (IPL). The proof rules
([Pf](#/node/Syntax.Pf)) decide that the logic is intuitionistic rather than classical.

**A leftover second syntax.** Kripke/Syntax.lean has an older, smaller copy of this type (only
variables, ∧, ⇒ and true; lines 6–10) with its own proof rules. Nothing imports that file. All results on
this site use the full syntax in Logic/Syntax.lean.
""",
 [q("How is 'not φ' expressed in this syntax?",
    ["By a dedicated negation constructor", "As φ ⇒ ff (φ implies false)", "As φ ∨ ff", "It cannot be expressed"], 1,
    "There is no negation constructor in Logic/Syntax.lean lines 7–13; the excluded-middle result in Kripke/Soundness.lean line 123 uses 'variable 0 implies false'."),
   q("What identifies a propositional variable?",
    ["A string name", "A natural number", "A world", "A truth value"], 1,
    "The variable constructor takes a natural number (Logic/Syntax.lean line 8)."),
   q("Which file's syntax do the soundness and completeness theorems use?",
    ["Kripke/Syntax.lean (∧, ⇒, true only)", "Logic/Syntax.lean (∧, ∨, ⇒, true, false)", "Both, separately", "Neither"], 1,
    "Kripke/Frame.lean and Beth/Semantics.lean import Logic.Syntax; Kripke/Syntax.lean is not imported anywhere.")],
 caveats=["The connectives' notation is scoped and overloads the usual ∧ and ∨ symbols; on this site ∧, ∨, ⇒ always mean the object-language connectives, not Lean's own."])

node("Syntax.Ctxt", "Contexts (lists of assumptions)",
 "A context is a finite list of formulas, newest assumption first. One context is 'below' another when it is a suffix of it, so moving up means adding assumptions at the front.",
 r"""## Plain English

**Definition (`Ctxt`, Logic/Syntax.lean line 21).** A context Γ is simply a list of
[formulas](#/node/Syntax.Tm): the assumptions currently in force. New assumptions are added at the
front of the list.

**The order (Logic/Syntax.lean lines 23–28).** Γ ≤ Δ means Γ is a *suffix* of Δ: Δ is Γ with some
extra formulas stuck on the front. This is a preorder (reflexive and transitive), borrowed from Mathlib's
list-suffix relation.

Why a suffix and not "every formula of Γ occurs in Δ"? Because a suffix is exactly what you get by
repeatedly assuming new things, which is how contexts grow in a natural-deduction proof. The more
flexible "subset" version is proved later as a lemma ([monotone_mem](#/node/Syntax.Pf.multicut)).

The same order is reused in two places:

- the weakening rule of [Pf](#/node/Syntax.Pf);
- the **worlds** of the [Beth canonical model](#/node/Beth.Completeness.World), which are contexts
  ordered by this very suffix relation.
""",
 [q("When is Γ ≤ Δ for contexts?",
    ["When Γ and Δ have the same length", "When Γ is a suffix of Δ (Δ adds formulas at the front)",
     "When every formula of Δ is in Γ", "When Γ proves everything Δ proves"], 1,
    "Logic/Syntax.lean lines 23–28 use Mathlib's list-suffix relation."),
   q("Is [A, B, C] ≥ [B, C]?", ["Yes", "No", "Only if A = B"], 0,
    "[B, C] is a suffix of [A, B, C]."),
   q("Is [B, C] ≤ [B, A, C] in this order?", ["Yes", "No"], 1,
    "[B, C] is not a suffix of [B, A, C] (the last two entries are A, C). Lemmas like monotone_mem (Logic/Syntax.lean lines 150–153) handle such reorderings.")])

node("Syntax.Pf", "Natural-deduction proofs",
 "Γ ⊢ φ ('φ is provable from the assumptions Γ') is defined by the standard introduction and elimination rules of intuitionistic natural deduction, plus a weakening rule. There is no excluded middle and no double-negation rule.",
 r"""## Plain English

**Definition (`Pf`, Logic/Syntax.lean lines 30–43).** `Pf Γ φ` is a proposition: "there is a
natural-deduction derivation of φ from the assumptions in [context](#/node/Syntax.Ctxt) Γ".
Written Γ ⊢ φ below. It is the smallest relation closed under these rules:

| Rule | In words |
|---|---|
| assume | the newest assumption is provable: φ, Γ ⊢ φ |
| wk (weakening) | if Γ ⊢ φ and Γ ≤ Δ, then Δ ⊢ φ |
| ∧ intro / two ∧ elims | from φ and ψ get φ ∧ ψ; from φ ∧ ψ get either one |
| ∨ intro (two) | from φ get φ ∨ ψ; from ψ get φ ∨ ψ |
| ∨ elim | if Γ ⊢ φ ∨ ψ, and C follows both from φ, Γ and from ψ, Γ, then Γ ⊢ C |
| ⇒ intro | if φ, Γ ⊢ ψ then Γ ⊢ φ ⇒ ψ |
| ⇒ elim (modus ponens) | from φ ⇒ ψ and φ get ψ |
| false elim | from ff, anything |
| true intro | tt is always provable |

This is the textbook system **NJ** for intuitionistic propositional logic. What is *missing* is the
point: there is no rule giving φ ∨ ¬φ, and none turning ¬¬φ into φ. The two
[completeness theorems](#/node/Kripke.completeness) say this rule set proves exactly what is true in
every Kripke (or Beth) model, and [em_not_provable](#/node/Kripke.ExcludedMiddle.em_not_provable)
shows excluded middle is genuinely missing.

A small worked example sits at Logic/Syntax.lean lines 45–51 (a derivation of "(A ⇒ B) ∧ A, then B"
with ⇒ intro). Line 54–59 derive the **cut** rule from ⇒ intro and ⇒ elim.

**Helper lemmas.** `of_mem` (lines 63–71): any formula *anywhere* in Γ is provable from Γ.
`quodlibet` (lines 73–79): from ¬φ you can prove φ ⇒ t for any t. `or_cases_to` (lines 81–92):
from φ ∨ ψ, φ ⇒ A and ψ ⇒ A you get A. These feed the completeness proofs.
""",
 [q("Which of these is NOT a rule of `Pf`?",
    ["From φ ⇒ ψ and φ, conclude ψ", "From φ ∧ ψ conclude φ", "Conclude φ ∨ (φ ⇒ ff) outright", "From ff conclude anything"], 2,
    "Logic/Syntax.lean lines 30–43 list no excluded-middle rule; that absence is what makes the logic intuitionistic."),
   q("The assume rule only gives the *first* formula of the context. How do you use one further back?",
    ["You cannot", "By the derived lemma of_mem, which uses weakening (Logic/Syntax.lean lines 63–71)",
     "By reordering the list", "By false elim"], 1,
    "of_mem proves Γ ⊢ φ whenever φ ∈ Γ, by induction on Γ with weakening."),
   q("Is `Pf Γ φ` data (a proof tree you can inspect) or a proposition?",
    ["A proposition: it only records *that* a derivation exists", "Data", "A Boolean"], 0,
    "It is declared as an inductive Prop (Logic/Syntax.lean line 30).")])

node("Syntax.Pf.multicut", "Multicut (substituting proofs for assumptions)",
 "If every assumption of Δ is provable from Γ, then anything provable from Δ is provable from Γ. This 'cut many assumptions at once' lemma is what lets the completeness proofs move freely between contexts.",
 r"""## Plain English

**Theorem (`Pf.multicut`, Logic/Syntax.lean lines 94–148).** Suppose Δ ⊢ P, and suppose every
formula Q in Δ satisfies Γ ⊢ Q. Then Γ ⊢ P.

In words: you may replace each assumption by a proof of it. It is the admissibility of a
simultaneous cut, proved here without any cut-elimination machinery, simply by induction on the
derivation of Δ ⊢ P.

**How the induction goes.** Each rule is rebuilt over Γ. The only interesting cases are the rules that
*extend* the context (∨ elim at lines 120–132 and ⇒ intro at lines 133–139): there the new hypothesis
φ is put in front of Γ too, and every old assumption is weakened past it.

**Consequence: `monotone_mem` (lines 150–153).** If every formula of Γ also occurs in Δ (in any order,
with any repetitions), then Γ ⊢ P implies Δ ⊢ P. This frees later proofs from the strict suffix
order of [Ctxt](#/node/Syntax.Ctxt).
""",
 [q("What does multicut let you do?",
    ["Remove all assumptions", "Replace every assumption of Δ by a proof of it from Γ",
     "Prove excluded middle", "Turn proofs into worlds"], 1,
    "Logic/Syntax.lean lines 94–95."),
   q("Which rule cases need the most care in the induction?",
    ["∧ intro", "The rules that add a hypothesis to the context: ∨ elim and ⇒ intro", "true intro", "false elim"], 1,
    "Lines 120–139 extend Γ with the new hypothesis and weaken the old ones."),
   q("What does monotone_mem relax compared with the weakening rule?",
    ["Nothing", "Γ need only be contained in Δ as a set of formulas, not be a suffix of it", "It allows removing assumptions"], 1,
    "Logic/Syntax.lean lines 150–153.")])

import importlib.util as _u, os as _o
_s = _u.spec_from_file_location("_extra", _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "_extra.py"))
_m = _u.module_from_spec(_s); _s.loader.exec_module(_m); _m.apply(NODES)
