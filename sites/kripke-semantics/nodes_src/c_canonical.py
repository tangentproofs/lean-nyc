NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

node("Kripke.Canonical.ProvableFrom", "Theories and what they prove",
 "A theory is an arbitrary (possibly infinite) set of formulas; it proves φ when some finite list of its members proves φ. From this come closed, consistent and prime theories, the raw material of the canonical model.",
 r"""## Plain English

**Definitions (Kripke/Completeness.lean lines 13–27).**

- A **theory** is any set of [formulas](#/node/Syntax.Tm) (line 13).
- T **proves** φ (`ProvableFrom`, lines 15–16) when there is a finite [context](#/node/Syntax.Ctxt)
  Γ, all of whose formulas lie in T, with [Γ ⊢ φ](#/node/Syntax.Pf). Proofs only ever use finitely
  many assumptions.
- T is **closed** (`Closed`, lines 18–19) when everything T proves is already in T.
- T is **consistent** (`Consistent`, lines 21–22) when *false* is not in T. (For a closed theory this
  is the same as "T does not prove false".)
- T is **prime** (`Prime`, lines 24–25) when whenever φ ∨ ψ is in T, φ is in T or ψ is in T.
  This is the intuitionistic stand-in for the classical notion of a *complete* (maximal) theory: an
  intuitionistic world need not decide every formula, but it must decide every disjunction it believes.
- The **closure** of T (line 27) is the set of everything T proves.

**Basic facts.** T is inside its closure (lines 35–42); the closure is closed (lines 94–97, via
[multicut](#/node/Syntax.Pf.multicut)); and for a finite context Γ, φ lies in the closure of Γ's
formulas exactly when Γ ⊢ φ (`mem_theoryOf`, lines 103–113).
""",
 [q("What does it mean for a theory T to prove φ here?",
    ["T is finite and T ⊢ φ", "Some finite list of members of T proves φ", "φ ∈ T", "Every member of T implies φ"], 1,
    "Kripke/Completeness.lean lines 15–16."),
   q("What does 'prime' require?",
    ["T contains every formula or its negation", "If φ ∨ ψ ∈ T then φ ∈ T or ψ ∈ T", "T is finite", "T is maximal consistent"], 1,
    "Kripke/Completeness.lean lines 24–25. Note it does NOT demand φ or ¬φ for every φ."),
   q("Why is 'prime' used rather than 'maximal consistent'?",
    ["Maximal consistent theories would decide every φ, making the model classical", "It is shorter", "There is no reason"], 0,
    "A world that decides every formula forces excluded middle; prime theories only decide disjunctions they contain.")])

node("Kripke.Canonical.Admissible", "Admissible extensions",
 "Given a base theory S and a formula A to avoid, an admissible theory contains S, is closed and consistent, and does not contain A. Zorn's lemma will pick a maximal one.",
 r"""## Plain English

**Definition (`Admissible S A T`, Kripke/Completeness.lean lines 29–33).** T is admissible for S and A when

1. S ⊆ T,
2. T is [closed](#/node/Kripke.Canonical.ProvableFrom),
3. T is consistent, and
4. A ∉ T.

The candidates of the [prime extension lemma](#/node/Kripke.Canonical.prime_extension_avoiding) are
exactly the admissible theories.

**Two lemmas about adding one formula (lines 153–198).**

- `closure_insert_imp` (lines 153–171): if T is closed and the closure of T ∪ {φ} contains t, then
  φ ⇒ t is already in T. This is the **deduction theorem** at the level of theories: the proof of t
  uses φ plus finitely many members of T, so ⇒ intro discharges φ.
- `imp_target_of_failure` (lines 188–198): if adding φ to T breaks admissibility (the closure
  contains A or false), then φ ⇒ A ∈ T. In the "false" case one gets ¬φ ∈ T, and from ¬φ any
  implication φ ⇒ A follows (`quodlibet`, Logic/Syntax.lean lines 73–79).
""",
 [q("Which is NOT a condition of Admissible S A T?",
    ["S ⊆ T", "T is closed", "T is prime", "A ∉ T"], 2,
    "Kripke/Completeness.lean lines 29–33; primeness is what the extension lemma adds."),
   q("closure_insert_imp is a version of which classical fact?",
    ["The deduction theorem", "Compactness", "Zorn's lemma", "Excluded middle"], 0,
    "Kripke/Completeness.lean lines 153–171 discharge φ with ⇒ intro.")])

node("Kripke.Canonical.prime_extension_avoiding", "Prime extension lemma (via Zorn)",
 "Every closed, consistent theory that does not contain A can be enlarged to a closed, consistent, prime theory that still does not contain A. This is the intuitionistic Lindenbaum lemma, and it is where Zorn's lemma (hence the axiom of choice) enters.",
 r"""## Plain English

**Theorem (`prime_extension_avoiding`, Kripke/Completeness.lean lines 201–292).** Let S be
[closed and consistent](#/node/Kripke.Canonical.ProvableFrom) with A ∉ S. Then there is a theory T that
is [admissible](#/node/Kripke.Canonical.Admissible) for S and A (contains S, closed, consistent,
avoids A) and is also prime.

**Proof idea.**

1. **Zorn (lines 207–235).** Admissible theories, ordered by ⊆, have upper bounds for nonempty
   chains: the union. The union is closed because any proof uses finitely many formulas, and a finite
   set from a chain lies in one member (`chain_member_for_ctxt`, lines 121–141; `sUnion_closed`, lines
   143–151). It contains S, and avoids false and A because no member contains them. Mathlib's
   `zorn_subset_nonempty` gives a maximal admissible M ⊇ S.
2. **M is prime (lines 239–292).** Suppose φ ∨ ψ ∈ M but neither φ nor ψ is. Adding φ to M and
   closing gives a strictly bigger theory, so by maximality it is not admissible; thus
   φ ⇒ A ∈ M (via `imp_target_of_failure`). Likewise ψ ⇒ A ∈ M. From φ ∨ ψ, φ ⇒ A and ψ ⇒ A one
   proves A (`or_cases_to`, Logic/Syntax.lean lines 81–92), so A ∈ M by closedness, contradicting
   admissibility.

The trick of avoiding a specific A (rather than just staying consistent) is what makes primeness
come out: maximality "against A" forces every disjunction to be split.
""",
 [q("What does Zorn's lemma supply here?",
    ["A finite theory", "A maximal admissible theory containing S", "A proof of A", "A Beth frame"], 1,
    "Kripke/Completeness.lean lines 207–210."),
   q("Why is the union of a chain of closed theories closed?",
    ["Because proofs use only finitely many assumptions, which all lie in one member of the chain",
     "Because unions are always closed", "By excluded middle"], 0,
    "chain_member_for_ctxt and sUnion_closed, Kripke/Completeness.lean lines 121–151."),
   q("In the primeness argument, what contradiction is reached?",
    ["false ∈ M", "A ∈ M, though M avoids A", "φ ∈ M", "M is not closed"], 1,
    "Kripke/Completeness.lean lines 281–292."),
   q("Is this proof constructive?",
    ["Yes", "No: it uses Zorn's lemma and classical reasoning"], 1,
    "Line 7 opens Classical; line 210 uses zorn_subset_nonempty.")],
 caveats=["Classical: uses Zorn's lemma and the axiom of choice. This is the standard textbook route, but it means the Kripke completeness proof is not constructive."])

node("Kripke.Canonical.World", "The canonical Kripke model",
 "The canonical model's worlds are the closed, consistent, prime theories, ordered by inclusion; a variable holds at a world when it is in the theory.",
 r"""## Plain English

**Definition (`World`, Kripke/Completeness.lean lines 294–298, with its frame structure at lines
300–310).** A world is a theory that is [closed, consistent and prime](#/node/Kripke.Canonical.ProvableFrom).
The order is inclusion of theories (w ≤ v when everything in w is in v), and variable i holds at w
when "variable i" is a member of w. Persistence is then just "subsets of v are in v".

So every possible "complete-enough state of knowledge" is a world, and moving up means learning more.
The [truth lemma](#/node/Kripke.Canonical.truth_lemma) shows that *every* formula, not just the
variables, is forced at w exactly when it belongs to w.
""",
 [q("When is w ≤ v in the canonical model?", ["When w's theory is a subset of v's", "When v ⊆ w", "When they share a variable"], 0,
    "Kripke/Completeness.lean lines 300–301."),
   q("Which three properties must a canonical world's theory have?",
    ["Finite, decidable, consistent", "Closed, consistent, prime", "Maximal, consistent, complete"], 1,
    "Kripke/Completeness.lean lines 294–298.")])

node("Kripke.Canonical.truth_lemma", "Truth lemma (Kripke)",
 "In the canonical model, a formula is forced at a world exactly when it belongs to that world's theory. Primeness handles 'or'; the prime extension lemma handles 'implies'.",
 r"""## Plain English

**Theorem (`truth_lemma`, Kripke/Completeness.lean lines 313–451).** For every canonical
[world](#/node/Kripke.Canonical.World) w and every formula φ: φ is
[forced at w](#/node/Kripke.at_world) if and only if φ ∈ w.

**By induction on φ.**

- **Variables** (line 314): by definition of the valuation.
- **∧** (lines 315–349): use closedness with ∧ intro and the ∧ elims.
- **∨** (lines 350–381): forced ⇒ member uses ∨ intro and closedness; member ⇒ forced is **exactly
  where primeness is needed** (line 373).
- **⇒, member to forced** (lines 421–439): if φ ⇒ ψ ∈ w and v ⊇ w has φ, modus ponens in v gives ψ.
- **⇒, forced to member** (lines 384–420), the hard case. Suppose φ ⇒ ψ ∉ w. Add φ to w and close:
  this cannot contain ψ (else φ ⇒ ψ ∈ w by the deduction theorem) and cannot contain false (else
  ¬φ ∈ w, which gives φ ⇒ ψ). The [prime extension lemma](#/node/Kripke.Canonical.prime_extension_avoiding)
  stretches it to a world v ⊇ w with φ ∈ v and ψ ∉ v. So φ ⇒ ψ is not forced at w.
- **true / false** (lines 440–451): closedness gives true; consistency excludes false.
""",
 [q("Which case of the truth lemma uses primeness?",
    ["∧", "∨, from membership to forcing", "⇒", "Variables"], 1,
    "Kripke/Completeness.lean line 373 calls w.prime."),
   q("Which case needs the prime extension lemma?",
    ["⇒, from forcing to membership", "∨", "true", "∧"], 0,
    "Kripke/Completeness.lean lines 406–407."),
   q("What does the truth lemma say about the canonical model?",
    ["Every formula is forced everywhere", "Forcing at w coincides with membership in w", "Only variables are forced"], 1,
    "Kripke/Completeness.lean line 313.")])

node("Kripke.countermodel", "Countermodel: every unprovable sequent fails somewhere",
 "If Γ does not prove φ, there is a world of the canonical model where all of Γ holds but φ does not. This is completeness in contrapositive form.",
 r"""## Plain English

**Theorem (`countermodel`, Kripke/Completeness.lean lines 457–499).** If Γ ⊬ φ, then Γ does
**not** [semantically entail](#/node/Kripke.SemEntails) φ (over frames in the lowest universe).

**Proof.** Let S be the set of consequences of Γ. Then φ ∉ S (else Γ ⊢ φ, lines 459–463) and S is
consistent (else Γ ⊢ ff ⊢ φ, lines 464–469). The
[prime extension lemma](#/node/Kripke.Canonical.prime_extension_avoiding) gives a prime T ⊇ S avoiding φ
(lines 470–471), which is a [canonical world](#/node/Kripke.Canonical.World) w (line 472). By the
[truth lemma](#/node/Kripke.Canonical.truth_lemma), all of Γ is forced at w (lines 473–490) and φ is
not (lines 491–495). So the canonical frame is a countermodel.
""",
 [q("Which world refutes Γ ⊨ φ when Γ ⊬ φ?",
    ["A three-point frame", "A prime theory containing Γ's consequences and avoiding φ", "The empty theory"], 1,
    "Kripke/Completeness.lean lines 470–472."),
   q("Why is the theory of Γ's consequences consistent when Γ ⊬ φ?",
    ["Because Γ is finite", "If it contained false then Γ ⊢ false and so Γ ⊢ φ", "By Zorn's lemma"], 1,
    "Kripke/Completeness.lean lines 464–469.")])

node("Kripke.completeness", "Headline: completeness for Kripke models",
 "If φ holds at every world forcing Γ in every Kripke model, then Γ ⊢ φ. Together with soundness: intuitionistic natural deduction proves exactly the Kripke-valid sequents.",
 r"""## Plain English

**Theorem (`completeness`, Kripke/Completeness.lean lines 501–503).** For any finite
[context](#/node/Syntax.Ctxt) Γ and formula φ: if [Γ ⊨ φ](#/node/Kripke.SemEntails) (over all Kripke frames
whose worlds form an ordinary type, universe 0), then [Γ ⊢ φ](#/node/Syntax.Pf).

With [soundness](#/node/Kripke.soundness), this is the classic theorem (Kripke, 1965) that
intuitionistic propositional logic is sound and complete for Kripke semantics.

**What is and isn't claimed.**

- The context Γ is a **finite list**. This is ordinary ("weak", or finite-premise) completeness.
  Infinite theories appear inside the proof, but the statement does not cover them.
- The completeness proof is **classical**: it uses Zorn's lemma, through the canonical model
  of prime theories. That is the standard textbook proof. It does not give an algorithm and it is not
  the constructive proof one might hope for in a project about intuitionistic logic. The
  [Beth completeness theorem](#/node/Beth.Completeness.completeness) on this site avoids Zorn.
- The countermodel is infinite. The **finite model property** (enough to check finite frames) is
  not proved.
""",
 [q("What does completeness conclude?",
    ["Γ ⊨ φ from Γ ⊢ φ", "Γ ⊢ φ from Γ ⊨ φ", "Excluded middle", "Every formula is decidable"], 1,
    "Kripke/Completeness.lean line 501."),
   q("Does the theorem cover infinite sets of premises?",
    ["Yes", "No: Γ is a finite list of formulas"], 1,
    "The context type is a list (Logic/Syntax.lean line 21)."),
   q("Which non-constructive principle does its proof use?",
    ["None", "Zorn's lemma (via the prime extension lemma)", "Only excluded middle on numbers"], 1,
    "Kripke/Completeness.lean line 210."),
   q("Does it prove the finite model property?",
    ["Yes", "No: the canonical countermodel is infinite and no finite-model statement is proved"], 1,
    "Nothing in Kripke/Completeness.lean restricts to finite frames.")],
 caveats=["Weak (finite-premise) completeness only, over frames in universe 0.",
          "Classical proof (Zorn's lemma, Classical namespace opened at Kripke/Completeness.lean line 7).",
          "Not built: 'proved' means the file contains a complete-looking proof with no sorry."],
 widgets=[{"type": "walkthrough", "title": "How the proof goes (Kripke/Completeness.lean, lines 13-503)",
   "config": {"steps": [
     {"text": "Contrapose: it suffices to show that if Γ ⊬ φ then Γ ⊭ φ (lines 501–503).", "link": "Kripke.countermodel"},
     {"text": "Set up theories: closed, consistent, prime, and the closure operation (lines 13–27); the deduction theorem for theories (closure_insert_imp, lines 153–171).", "link": "Kripke.Canonical.ProvableFrom"},
     {"text": "Prime extension: Zorn's lemma gives a maximal closed consistent theory avoiding a target formula, and maximality forces primeness (lines 201–292).", "link": "Kripke.Canonical.prime_extension_avoiding"},
     {"text": "The canonical frame: prime theories ordered by inclusion, variables true when they are members (lines 294–310).", "link": "Kripke.Canonical.World"},
     {"text": "Truth lemma: forcing equals membership, by induction on the formula; the implication case uses prime extension again (lines 313–451).", "link": "Kripke.Canonical.truth_lemma"},
     {"text": "Extend the consequences of Γ to a prime theory avoiding φ; that world forces Γ but not φ (lines 457–499).", "link": "Kripke.countermodel"}]}}])

import importlib.util as _u, os as _o
_s = _u.spec_from_file_location("_extra", _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "_extra.py"))
_m = _u.module_from_spec(_s); _s.loader.exec_module(_m); _m.apply(NODES)
