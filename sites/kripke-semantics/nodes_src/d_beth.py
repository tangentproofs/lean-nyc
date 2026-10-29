NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

node("Beth.Sieve", "Sieves (upward-closed sets of futures)",
 "A sieve on a world p is a set of futures of p that is closed upward: once a state is in it, every later state is too. Sieves play the role of 'bars' in Beth semantics.",
 r"""## Plain English

**Definition (`Sieve`, Beth/Coverage.lean lines 8–11).** In a preorder, a sieve on p is a set S of
points such that every member q satisfies p ≤ q ("bounded": S only contains futures of p), and if
r ∈ S and r ≤ q then q ∈ S ("upward closed").

Think of S as "the set of future states by which some event has happened". Once it has happened, it
stays happened.

**Constructions.**

- The **maximal sieve** on p (lines 23–28) is the set of all futures of p.
- The **pullback** of a sieve S on p to a later point q ≥ p (lines 31–34) keeps the members of S that
  are also ≥ q. The comment at line 30 notes that the category-theory name "pullback" is used even
  though, in this order, it moves forward.
- **Gluing** (`glue_sieves`, lines 74–78): given a sieve U on p and, for each q ∈ U, a sieve on q,
  take the union of all those sieves. This is a sieve on p.

The vocabulary (sieve, coverage, sheaf) comes from Grothendieck topologies; here it is specialised to a
preorder, where everything reduces to sets of points.
""",
 [q("Which of these must hold for a sieve S on p?",
    ["S contains p", "Every member of S is ≥ p, and S is closed upward", "S is finite", "S is a chain"], 1,
    "Beth/Coverage.lean lines 8–11. A sieve need not contain p."),
   q("What is the maximal sieve on p?", ["{p}", "All q with p ≤ q", "The empty set", "All points"], 1,
    "Beth/Coverage.lean lines 23–28."),
   q("What does pulling back a sieve S on p along p ≤ q give?",
    ["Members of S that are also ≥ q", "All points ≤ q", "S unchanged"], 0,
    "Beth/Coverage.lean line 32.")],
 caveats=["Possible build problem: in `pullback`, the 'bounded' field (Beth/Coverage.lean line 33) appears, from reading the text, to refer to a name that is not bound anywhere. The intended proof is clear (members are ≥ q by construction), but if this is a genuine typo the file would not compile, and everything Beth-related depends on it. The Lean was not built for this site, so this is unconfirmed; see the Trust page."])

node("Beth.Coverage", "Coverages (which sieves count as 'covering')",
 "A coverage picks out, for each world, which sieves 'cover' it: sets of futures that are guaranteed to be reached. The axioms say the whole future covers, covers can be composed, and covers survive moving forward.",
 r"""## Plain English

**Definition (`Coverage`, Beth/Coverage.lean lines 36–41).** For each point p, a set of
[sieves](#/node/Beth.Sieve) on p called the *covering* sieves, such that:

- **maximal** (line 38): the maximal sieve (all futures) covers p;
- **transitive** (lines 39–40): if U covers p, and for every q ∈ U the pullback of V to q covers q,
  then V covers p ("a cover of covers is a cover");
- **stability** (line 41): if U covers p and p ≤ q, then the pullback of U to q covers q.

`HasCoverage` (lines 43–44) bundles a preorder with a coverage, and lines 48–58 give short names for the
axioms. Two derived facts: a bigger sieve than a covering one also covers (`covers_mono`, lines 60–72),
and gluing covering sieves over a cover gives a cover (`covers_glue`, lines 80–90).

**Intuition.** In Beth's original setting the points are nodes of a tree and "U covers p" means "every
infinite path through p eventually enters U": U is a *bar*. See
[BethTreeCoverage](#/node/Beth.BethTrees.BethTreeCoverage). The simplest coverage, where only the
maximal sieve covers, is `maximalSieveCoverage` (lines 111–134); with it, Beth semantics collapses to
Kripke semantics (see [bethFrameOfKripke](#/node/Beth.Examples.bethFrameOfKripke)).
""",
 [q("Which is NOT a coverage axiom here?",
    ["The maximal sieve covers", "Covers are stable under moving forward", "Every covering sieve contains p itself", "Covers of covers are covers"], 2,
    "Beth/Coverage.lean lines 36–41; a covering sieve need not contain p."),
   q("In a tree with the bar coverage, when does U cover a node p?",
    ["When U contains p", "When every infinite path through p eventually enters U", "When U is finite"], 1,
    "IsBar, Beth/BethTrees.lean lines 82–86."),
   q("If U covers p and U ⊆ V, does V cover p?", ["Yes (covers_mono)", "No", "Only if V is maximal"], 0,
    "Beth/Coverage.lean lines 60–72.")])

node("Beth.BethFrame", "Beth frames",
 "A Beth frame is a Kripke frame with a coverage, where a variable that holds on a covering sieve already holds at the world (the 'sheaf condition'), and no covering sieve is empty.",
 r"""## Plain English

**Definition (`BethFrame`, Beth/Semantics.lean lines 11–13).** A type W with

- a [Kripke frame](#/node/Kripke.Frame) structure (preorder, valuation, persistence);
- a [coverage](#/node/Beth.Coverage) on the same preorder;
- the **sheaf condition** (line 12): if S covers w and variable i holds at every member of S, then i
  holds at w. Read: "if i is bound to become true, it is already true";
- **non-empty covers** (line 13): every covering sieve has at least one member. Without this, the
  empty sieve could cover and *false* would be forced (see the ff case of
  [sheaf_term](#/node/Beth.sheaf_term)).

This is a generalisation of Beth's tree models (1956) in the style of sheaf/topos semantics: Beth trees
with bars ([BethTreeFrame](#/node/Beth.BethTrees.BethTreeFrame)) and Kripke frames with the trivial coverage
([bethFrameOfKripke](#/node/Beth.Examples.bethFrameOfKripke)) are both instances.
""",
 [q("What does the sheaf condition say?",
    ["Every variable holds somewhere", "If a variable holds throughout a covering sieve on w, it holds at w",
     "Covers are finite", "The order is a tree"], 1,
    "Beth/Semantics.lean line 12."),
   q("Why require covering sieves to be non-empty?",
    ["For decidability", "Otherwise the empty sieve could cover w and false would be forced at w", "To make the order total"], 1,
    "Beth/Semantics.lean line 13, used in the ff case at lines 93–96."),
   q("Is every Kripke frame a Beth frame?", ["Yes, with the coverage where only the maximal sieve covers", "No"], 0,
    "Beth/Examples.lean lines 21–32.")])

node("Beth.at_world", "Beth forcing",
 "Beth forcing is Kripke forcing with one change: φ ∨ ψ holds at w when some covering sieve of futures each forces φ or forces ψ. You need not know which disjunct holds now, only that one will be settled on a cover.",
 r"""## Plain English

**Definition (`at_world`, Beth/Semantics.lean lines 21–29).** In a [Beth frame](#/node/Beth.BethFrame):

- variables, ∧, ⇒, true and false are exactly as in [Kripke forcing](#/node/Kripke.at_world)
  (⇒ quantifies over all futures);
- **φ ∨ ψ holds at w when there is a sieve S covering w such that every world in S forces φ or forces
  ψ** (lines 25–26).

So a disjunction can be forced at a world where neither disjunct is: the
[binary-tree example](#/node/Beth.Examples.BinaryBitsTree.binaryBranchVal) has P ∨ Q forced at the root,
since every path takes a first step left (P) or right (Q), while neither P nor Q holds at the root.

**Two key properties.**

- **Persistence** (`mono_at`, lines 34–52): the ∨ case pulls the covering sieve forward using
  stability.
- **Local character** (`sheaf_term`, lines 55–96): see [sheaf_term](#/node/Beth.sheaf_term).

Validity and semantic consequence (`Entails`, lines 125–126; `SemEntails`, lines 128–129) are defined
exactly as for Kripke frames, quantifying over Beth frames instead.
""",
 [q("When does φ ∨ ψ hold at w in Beth semantics?",
    ["When φ or ψ holds at w", "When some covering sieve on w consists of worlds each forcing φ or forcing ψ",
     "When φ ∨ ψ holds at every world", "Never"], 1,
    "Beth/Semantics.lean lines 25–26."),
   q("Which clauses differ from Kripke forcing?", ["Only ∨", "∨ and ⇒", "All of them"], 0,
    "Compare Beth/Semantics.lean lines 21–29 with Kripke/Frame.lean lines 16–23."),
   q("Can P ∨ Q hold at a world where neither P nor Q holds?",
    ["Never", "Yes, in Beth semantics, if a cover of futures each settle one of them"], 1,
    "The binary-tree example, Beth/Examples.lean lines 129–156.")])

node("Beth.sheaf_term", "Every formula satisfies the sheaf condition",
 "If a formula holds at every world of a covering sieve on w, it holds at w. The frame only demands this for variables; this lemma lifts it to all formulas, and it is the engine of Beth soundness for ∨ elimination.",
 r"""## Plain English

**Lemma (`sheaf_term`, Beth/Semantics.lean lines 55–96).** In a [Beth frame](#/node/Beth.BethFrame),
if S covers w and φ is [forced](#/node/Beth.at_world) at every member of S, then φ is forced at w.

**By induction on φ.**

- variables: the frame's sheaf condition (line 57);
- ∧: componentwise (lines 58–66);
- **∨** (lines 67–79): each member of S has its own covering sieve deciding φ or ψ; pick one for each
  (using choice), glue them over S, and the glued sieve covers w (`covers_glue`);
- ⇒ (lines 80–89): pull S forward to the future world and use the induction hypothesis there;
- false (lines 93–96): a covering sieve has a member, and false holds nowhere, so the hypothesis is
  impossible. This is exactly where non-empty covers are used.

In Kripke semantics this is trivial (only the maximal sieve covers, and it contains w). In Beth
semantics it is what lets ∨ elimination be sound: to derive C from φ ∨ ψ, prove C on each member of a
cover deciding the disjunction, then pull C back down.
""",
 [q("Where does the proof use non-empty covers?", ["The ∨ case", "The false case", "The variable case"], 1,
    "Beth/Semantics.lean lines 93–96."),
   q("How is the ∨ case handled?",
    ["By excluded middle", "By choosing a deciding sieve at each member and gluing them into one cover", "It is trivial"], 1,
    "Beth/Semantics.lean lines 67–79."),
   q("Which soundness case needs this lemma?", ["⇒ intro", "∨ elim", "∧ intro", "true intro"], 1,
    "Semantic ∨ elim, Beth/Semantics.lean lines 174–190.")])

node("Beth.SemEntails", "Semantic consequence over Beth frames",
 "Γ ⊨ φ (Beth) means: in every Beth frame, every world that forces all of Γ forces φ.",
 r"""## Plain English

**Definitions (`Entails`, Beth/Semantics.lean lines 125–126; `SemEntails`, lines 128–129).** These
mirror the [Kripke versions](#/node/Kripke.SemEntails) word for word, with [Beth frames](#/node/Beth.BethFrame)
and [Beth forcing](#/node/Beth.at_world) in place of Kripke frames and Kripke forcing. As there, the
completeness theorem uses frames whose worlds are in universe 0.

Lines 131–208 then prove a semantic version of each proof rule. The ∨ introduction rules use the
maximal sieve (lines 150–172), and ∨ elimination uses [sheaf_term](#/node/Beth.sheaf_term) (lines 174–190).
""",
 [q("How does Beth SemEntails differ from Kripke SemEntails?",
    ["It quantifies over Beth frames and uses Beth forcing", "It uses proofs", "It is identical"], 0,
    "Beth/Semantics.lean lines 128–129 versus Kripke/Frame.lean lines 69–70."),
   q("Which sieve witnesses φ ∨ ψ in semantic ∨ introduction?", ["The empty sieve", "The maximal sieve", "A bar of depth 1"], 1,
    "Beth/Semantics.lean lines 150–160.")])

node("Beth.soundness", "Headline: soundness for Beth frames",
 "Anything provable in intuitionistic natural deduction is true in every Beth frame. The only rule that needs real work is ∨ elimination, handled by the sheaf property of all formulas.",
 r"""## Plain English

**Theorem (`soundness`, Beth/Soundness.lean lines 10–48).** For every [Beth frame](#/node/Beth.BethFrame)
W: if [Γ ⊢ φ](#/node/Syntax.Pf) then [Γ entails φ in W](#/node/Beth.SemEntails).

The structure is identical to [Kripke soundness](#/node/Kripke.soundness): one case per proof rule,
each discharged by the matching semantic lemma in Beth/Semantics.lean lines 131–208.

**Status.** Complete as written, no `sorry`. Stated as a `def` with a propositional type. Not built for
this site. Since every Kripke frame is a Beth frame ([bethFrameOfKripke](#/node/Beth.Examples.bethFrameOfKripke)),
one might expect Kripke soundness to follow, but that would need a lemma saying Beth forcing in that
frame agrees with Kripke forcing; that lemma is not in the project, and Kripke soundness is proved separately.
""",
 [q("Which proof rule makes Beth soundness harder than Kripke soundness?",
    ["⇒ intro", "∨ elim", "∧ elim", "weakening"], 1,
    "Semantic ∨ elim needs sheaf_term (Beth/Semantics.lean lines 174–190)."),
   q("Does the project derive Kripke soundness from Beth soundness?",
    ["Yes", "No, the two are proved independently"], 1,
    "Kripke/Soundness.lean lines 11–46 is a separate proof; no lemma compares the two forcing relations."),
   q("For which frames does Beth soundness hold?",
    ["Every Beth frame", "Only Beth trees", "Only the canonical model"], 0,
    "The frame W is arbitrary (Beth/Soundness.lean line 10).")],
 caveats=["Everything Beth-related depends on `pullback` (Beth/Coverage.lean lines 31–34), whose line 33 looks, from the text, like it may not compile. Unconfirmed, since nothing was built.",
          "The ∨ case of sheaf_term uses choice to pick a sieve per world (Beth/Semantics.lean line 71)."],
 widgets=[{"type": "walkthrough", "title": "How the proof goes (Beth/Soundness.lean, lines 10-48)",
   "config": {"steps": [
     {"text": "Recurse on the derivation, one case per rule of Pf.", "link": "Syntax.Pf"},
     {"text": "Assumption, weakening and the ∧ rules (lines 11–26) are as in the Kripke case, using persistence of contexts.", "link": "Beth.SemEntails"},
     {"text": "∨ intro (lines 27–32): witness the disjunction with the maximal sieve, on which the chosen disjunct holds by persistence (Beth/Semantics.lean lines 150–172).", "link": "Beth.Sieve"},
     {"text": "∨ elim (lines 33–37): take the covering sieve deciding φ ∨ ψ, derive C at each of its members from the two branches, then pull C down with sheaf_term (Beth/Semantics.lean lines 174–190).", "link": "Beth.sheaf_term"},
     {"text": "⇒ intro, ⇒ elim, true, false (lines 38–48): as in the Kripke case.", "link": "Beth.at_world"}]}}])

node("Beth.Completeness.World", "The Beth canonical model: consistent contexts",
 "The Beth canonical model's worlds are just the finite contexts that do not prove false, ordered by 'adding assumptions'. A variable holds at Γ when Γ proves it. No infinite theories, no Zorn.",
 r"""## Plain English

**Definition (`World`, Beth/Completeness.lean lines 14–16; order at lines 18–21).** A world is a
[context](#/node/Syntax.Ctxt) Γ (a finite list of formulas) with Γ ⊬ ff. The order is the suffix order
of contexts: Δ is above Γ when Δ is Γ with more assumptions on the front.

**Valuation (line 180).** Variable i holds at Γ when Γ ⊢ variable i. Persistence is the weakening rule.

Compare the [Kripke canonical model](#/node/Kripke.Canonical.World), whose worlds are infinite prime
theories built by Zorn's lemma. Here the worlds are finite and concrete, and the job primeness did
there (deciding disjunctions) is taken over by the [coverage](#/node/Beth.Completeness.ContextCovers).
""",
 [q("What is a world of the Beth canonical model?",
    ["A prime theory", "A finite context that does not prove false", "A path in a tree", "A Boolean valuation"], 1,
    "Beth/Completeness.lean lines 14–16."),
   q("When does variable i hold at world Γ?", ["When it is the first formula of Γ", "When Γ ⊢ variable i", "Never"], 1,
    "Beth/Completeness.lean line 180.")])

node("Beth.Completeness.ContextCovers", "The canonical coverage: provable disjunctions",
 "In the Beth canonical model, a sieve covers Γ when Γ proves a disjunction A₁ ∨ … ∨ Aₙ and the sieve contains every extension of Γ proving some Aᵢ, plus whatever the coverage axioms then force.",
 r"""## Plain English

**Supporting definitions (Beth/Completeness.lean lines 23–80).**

- `context_sieve Γ L` (lines 23–33): the [canonical worlds](#/node/Beth.Completeness.World) above Γ that
  prove at least one formula from the list L.
- `mk_disjunction L` (lines 35–37): A₁ ∨ (A₂ ∨ (… ∨ ff)), the disjunction of a list, with the empty
  disjunction being *false*. Lemmas at lines 39–80 give its introduction and elimination rules.

**Definition (`ContextCovers`, lines 82–92).** The covering sieves are generated by three rules:

1. **basic**: if Γ ⊢ the disjunction of L, any sieve containing `context_sieve Γ L` covers Γ;
2. **maximal**: the maximal sieve covers;
3. **trans**: covers of covers are covers.

Stability under moving forward is then proved by induction (lines 94–142), so this is a
[coverage](#/node/Beth.Coverage) (`contextCoverage`, lines 144–152).

**The key lemma (`pf_sheaf`, lines 154–176).** If S covers Γ and every world in S proves r, then Γ
proves r. In the basic case, use disjunction elimination on A₁ ∨ … ∨ Aₙ; for each Aᵢ, either
Aᵢ, Γ is inconsistent (then it proves r by false elimination) or it is a world in S (then it proves r by
hypothesis). This lemma gives the frame its sheaf condition and non-empty covers (lines 178–192).
""",
 [q("Which sieve does a proof of A ∨ B from Γ make covering?",
    ["Only the maximal sieve", "Any sieve containing all extensions of Γ that prove A or prove B", "The empty sieve"], 1,
    "ContextCovers.basic with L = [A, B], Beth/Completeness.lean lines 83–86."),
   q("What is the disjunction of the empty list?", ["true", "false", "undefined"], 1,
    "Beth/Completeness.lean line 36."),
   q("What does pf_sheaf say?",
    ["Provability is local: if r is provable at every world of a cover of Γ, it is provable from Γ", "Every sieve covers", "Γ is consistent"], 0,
    "Beth/Completeness.lean lines 154–157."),
   q("Why are covering sieves non-empty in this model?",
    ["By definition", "An empty cover would make Γ prove false via pf_sheaf, but worlds are consistent", "Because L is non-empty"], 1,
    "Beth/Completeness.lean lines 185–192.")],
 caveats=["pf_sheaf case-splits on whether a context proves false (line 163). In Lean this uses classical logic, since provability is not shown to be decidable."])

node("Beth.Completeness.truth_lemma", "Truth lemma (Beth)",
 "In the Beth canonical model, a formula is forced at a context exactly when the context proves it. The disjunction case is the whole point: Γ ⊢ φ ∨ ψ gives a cover deciding it, by definition of the coverage.",
 r"""## Plain English

**Theorem (`truth_lemma`, Beth/Completeness.lean lines 195–265).** For every
[canonical world](#/node/Beth.Completeness.World) Γ and formula φ: φ is
[Beth-forced](#/node/Beth.at_world) at Γ iff Γ ⊢ φ.

**By induction on φ.**

- variables (lines 196–197): by definition;
- ∧ (lines 198–207): ∧ intro and elims;
- **∨, forced to provable** (lines 209–221): on the covering sieve each world proves φ or ψ, hence
  φ ∨ ψ; [pf_sheaf](#/node/Beth.Completeness.ContextCovers) pulls this down to Γ;
- **∨, provable to forced** (lines 222–239): the sieve of extensions proving φ or proving ψ covers Γ,
  by the basic covering rule;
- **⇒, forced to provable** (lines 241–249): if φ, Γ is inconsistent, φ ⇒ ψ follows from false.
  Otherwise φ, Γ is a world above Γ forcing φ, so it forces ψ, so φ, Γ ⊢ ψ and ⇒ intro finishes;
- ⇒, provable to forced (lines 250–253): weakening and modus ponens;
- true, false (lines 254–265): false is unprovable in a world by consistency.

Contrast the [Kripke truth lemma](#/node/Kripke.Canonical.truth_lemma): there the ⇒ case had to build a new
prime theory by Zorn's lemma; here the needed world is simply "add φ to the context".
""",
 [q("In the ⇒ case, which world is used as the witness future?",
    ["A prime extension from Zorn", "The context with φ added at the front", "The empty context"], 1,
    "Beth/Completeness.lean lines 245–249."),
   q("What does the truth lemma equate?",
    ["Beth forcing at Γ with provability from Γ", "Kripke and Beth forcing", "Truth and membership in a prime theory"], 0,
    "Beth/Completeness.lean line 195.")])

node("Beth.Completeness.completeness", "Headline: completeness for Beth frames",
 "If φ is forced wherever Γ is, in every Beth frame, then Γ ⊢ φ. The proof uses one canonical model whose worlds are finite consistent contexts, and needs no Zorn's lemma.",
 r"""## Plain English

**Theorem (`completeness`, Beth/Completeness.lean lines 289–297).** For any finite
[context](#/node/Syntax.Ctxt) Γ and formula φ: if [Γ ⊨ φ in Beth semantics](#/node/Beth.SemEntails)
(over all Beth frames whose worlds form an ordinary type, universe 0), then [Γ ⊢ φ](#/node/Syntax.Pf).

With [Beth soundness](#/node/Beth.soundness), this says intuitionistic natural deduction proves exactly
the Beth-valid sequents.

**The proof is short.** If Γ is inconsistent, Γ ⊢ φ trivially. Otherwise Γ itself is a world of the
[canonical model](#/node/Beth.Completeness.World), all of Γ is forced there (`all_at_world_self`, lines
268–287), so φ is forced there, and the [truth lemma](#/node/Beth.Completeness.truth_lemma) turns that
into Γ ⊢ φ.

**What is and isn't claimed.**

- Finite-premise completeness, frames in universe 0, as for the [Kripke theorem](#/node/Kripke.completeness).
- No Zorn's lemma or maximal theories. The meta-proof still uses classical case splits on provability
  (lines 163, 243, 291) and choice inside [sheaf_term](#/node/Beth.sheaf_term). So it is *simpler*, not
  fully constructive.
- Beth completeness does not imply Kripke completeness here: the project proves the two separately.
""",
 [q("What is the countermodel world when Γ is consistent?",
    ["A prime theory from Zorn's lemma", "Γ itself", "The root of a binary tree"], 1,
    "Beth/Completeness.lean lines 293–297."),
   q("Does this proof use Zorn's lemma?", ["Yes", "No"], 1,
    "Nothing in Beth/Completeness.lean invokes Zorn; worlds are finite contexts."),
   q("Is the proof entirely free of classical logic?",
    ["Yes", "No: it case-splits on whether a context proves false, which in Lean is classical"], 1,
    "Beth/Completeness.lean line 291 (and lines 163, 243)."),
   q("What if Γ proves false?", ["The theorem fails", "Then Γ ⊢ φ by false elimination", "Γ is not a context"], 1,
    "Beth/Completeness.lean lines 291–292.")],
 caveats=["Weak (finite-premise) completeness only, over Beth frames in universe 0.",
          "Uses classical case splits (by_cases on provability) and choice; not a constructive completeness proof.",
          "Depends on `pullback` in Beth/Coverage.lean, whose line 33 may not compile (unconfirmed; not built)."],
 widgets=[{"type": "walkthrough", "title": "How the proof goes (Beth/Completeness.lean, lines 14-297)",
   "config": {"steps": [
     {"text": "Worlds: finite contexts that do not prove false, ordered by suffix; a variable holds when it is provable (lines 14–21, 180).", "link": "Beth.Completeness.World"},
     {"text": "Coverage: generated by 'Γ proves A₁ ∨ … ∨ Aₙ, so the extensions proving some Aᵢ cover Γ', plus maximality and transitivity; stability by induction (lines 23–152).", "link": "Beth.Completeness.ContextCovers"},
     {"text": "Provability is local (pf_sheaf, lines 154–176), which gives the sheaf condition and non-empty covers, making this a Beth frame (lines 178–192).", "link": "Beth.Completeness.ContextCovers"},
     {"text": "Truth lemma: Beth forcing at Γ equals provability from Γ, by induction on the formula (lines 195–265).", "link": "Beth.Completeness.truth_lemma"},
     {"text": "Each consistent Γ forces all of its own formulas (lines 268–287).", "link": "Beth.Completeness.truth_lemma"},
     {"text": "Main proof: inconsistent Γ is trivial; otherwise apply the semantic hypothesis at the world Γ and read off Γ ⊢ φ by the truth lemma (lines 289–297)."}]}}])

import importlib.util as _u, os as _o
_s = _u.spec_from_file_location("_extra", _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "_extra.py"))
_m = _u.module_from_spec(_s); _s.loader.exec_module(_m); _m.apply(NODES)
