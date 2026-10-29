NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

node("Kripke.Canonical.Theory", "Theory (a set of formulas)",
 "A theory is just a set of formulas, possibly infinite. It is the type of the canonical Kripke model's worlds before the closed/consistent/prime conditions are added.",
 r"""## Plain English

**Definition (`Theory`, Kripke/Completeness.lean line 13).** An abbreviation for "set of
[formulas](#/node/Syntax.Tm)". See [theories and what they prove](#/node/Kripke.Canonical.ProvableFrom)
for the notions built on it.
""",
 [q("Can a theory be infinite?", ["Yes, it is an arbitrary set", "No, it is a list"], 0, "Kripke/Completeness.lean line 13."),
  q("How does a theory differ from a context?", ["A context is a finite ordered list; a theory is any set", "They are the same"], 0,
    "Compare Logic/Syntax.lean line 21."),
  q("Where are theories used?", ["In the Kripke completeness proof", "In the Beth completeness proof"], 0,
    "The Beth canonical model uses finite contexts instead (Beth/Completeness.lean lines 14–16).")])

node("Kripke.Canonical.Closed", "Closed theories",
 "A theory is closed when it already contains everything it proves.",
 r"""## Plain English

**Definition (`Closed`, Kripke/Completeness.lean lines 18–19).** T is closed when every φ that
[T proves](#/node/Kripke.Canonical.ProvableFrom) is a member of T. The closure of any theory is closed
(lines 94–97), and a union of a chain of closed theories is closed (lines 143–151).
""",
 [q("When is T closed?", ["When it contains everything it proves", "When it is finite", "When it is prime"], 0,
    "Kripke/Completeness.lean lines 18–19."),
  q("Is the union of a chain of closed theories closed?", ["Yes (sUnion_closed)", "Not in general"], 0,
    "Kripke/Completeness.lean lines 143–151; proofs use finitely many premises."),
  q("Is the closure of a theory closed?", ["Yes", "No"], 0, "closure_closed, Kripke/Completeness.lean lines 94–97.")])

node("Kripke.Canonical.Consistent", "Consistent theories",
 "A theory is consistent when it does not contain 'false'.",
 r"""## Plain English

**Definition (`Consistent`, Kripke/Completeness.lean lines 21–22).** *false* ∉ T. For a
[closed](#/node/Kripke.Canonical.Closed) theory this is equivalent to T not proving false. See
[theories](#/node/Kripke.Canonical.ProvableFrom).
""",
 [q("What does Consistent T say?", ["false is not a member of T", "T proves every formula", "T is prime"], 0,
    "Kripke/Completeness.lean lines 21–22."),
  q("Why do canonical worlds need consistency?", ["So that false is not forced anywhere, matching the semantics", "For finiteness"], 0,
    "The ff case of the truth lemma, Kripke/Completeness.lean lines 445–451."),
  q("Is consistency alone the same as 'does not prove false'?", ["Only for closed theories", "Always"], 0,
    "A non-closed T could prove false without containing it.")])

node("Kripke.Canonical.Prime", "Prime theories",
 "A theory is prime when, whenever it contains a disjunction, it contains one of the disjuncts: the intuitionistic analogue of a complete theory.",
 r"""## Plain English

**Definition (`Prime`, Kripke/Completeness.lean lines 24–25).** φ ∨ ψ ∈ T implies φ ∈ T or ψ ∈ T.
Primeness is what makes ∨ behave in the [truth lemma](#/node/Kripke.Canonical.truth_lemma). It is
obtained by the [prime extension lemma](#/node/Kripke.Canonical.prime_extension_avoiding).
""",
 [q("What does Prime T require?", ["If φ ∨ ψ ∈ T then φ ∈ T or ψ ∈ T", "φ ∈ T or ¬φ ∈ T for every φ", "T is finite"], 0,
    "Kripke/Completeness.lean lines 24–25."),
  q("Which lemma builds prime theories?", ["prime_extension_avoiding", "multicut", "soundness"], 0,
    "Kripke/Completeness.lean lines 201–292."),
  q("Does a prime theory decide every formula?", ["No", "Yes"], 0,
    "Only disjunctions it contains; otherwise excluded middle would hold in the canonical model.")])

node("Beth.BethTrees.IsBar", "Bars in a Beth tree",
 "A set of nodes is a bar at node l when every infinite path through l eventually enters it.",
 r"""## Plain English

**Definition (`IsBar`, Beth/BethTrees.lean lines 82–86).** For every infinite sequence f such that l
followed by any initial segment of f is a node of the [tree](#/node/Beth.BethTrees.BethTree), there is
some n such that l followed by the first n values of f is in the set. Bars are the covering sieves of the
[tree coverage](#/node/Beth.BethTrees.BethTreeCoverage). In a pruned tree a bar is never empty
(`IsBar.nonempty`, lines 179–199).
""",
 [q("What must every path through l do?", ["Eventually enter the bar", "Avoid the bar", "Stay finite"], 0,
    "Beth/BethTrees.lean lines 82–86."),
  q("Is a bar at l allowed to contain l itself?", ["Yes (then it is hit at depth 0)", "No"], 0, "Take n = 0."),
  q("Why is a bar in a pruned tree non-empty?", ["Some infinite path exists and must hit it", "By definition"], 0,
    "Beth/BethTrees.lean lines 179–199 build a path by repeated choice.")])
