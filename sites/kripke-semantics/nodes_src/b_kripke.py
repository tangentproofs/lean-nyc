NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

node("Kripke.Frame", "Kripke frames (models)",
 "A Kripke model is a preorder of 'states of knowledge' together with a record of which variables are known at each state, with the one rule that knowledge is never lost as you move up.",
 r"""## Plain English

**Definition (`Frame`, Kripke/Frame.lean lines 8–10).** A type W is a Kripke frame when it carries:

- a **preorder** ≤ (reflexive, transitive); think of w ≤ w′ as "w′ is a possible future of w", a state
  where at least as much has been established;
- a **valuation** `val`: for each world w and variable number i, a proposition "variable i is
  established at w";
- **persistence** (`le_val`): if w ≤ w′ and variable i is established at w, it is still established at w′.

Strictly speaking, logicians call the preorder alone a *frame* and frame-plus-valuation a *model*. Here
the name `Frame` covers both.

The worlds can be any type at all: three named points ([EMFrame](#/node/Kripke.ExcludedMiddle.em_not_provable)),
sets of formulas ([the canonical model](#/node/Kripke.Canonical.World)), or open sets of a topological
space ([opensFrame](#/node/Kripke.opensFrame)).
""",
 [q("What does the persistence condition say?",
    ["Every variable is true somewhere", "If a variable holds at w and w ≤ w′, it holds at w′",
     "Worlds are linearly ordered", "The valuation is decidable"], 1,
    "Kripke/Frame.lean line 10."),
   q("Must the order on worlds be antisymmetric (a partial order)?",
    ["Yes", "No, a preorder is enough"], 1,
    "The class extends Mathlib's Preorder (Kripke/Frame.lean line 8)."),
   q("What kind of thing is `val w i`?",
    ["A Boolean", "A proposition (Prop)", "A number", "A formula"], 1,
    "Kripke/Frame.lean line 9: a predicate on worlds and variable numbers.")])

node("Kripke.at_world", "Forcing: when a formula holds at a world",
 "A formula holds at a world by the usual rules, except implication: φ ⇒ ψ holds at w only if, at every future world where φ holds, ψ holds too. That one clause is what breaks excluded middle.",
 r"""## Plain English

**Definition (`at_world`, Kripke/Frame.lean lines 16–23).** For a world w of a
[Kripke frame](#/node/Kripke.Frame), "w forces φ" is defined by recursion on the
[formula](#/node/Syntax.Tm):

- a variable holds at w when the valuation says so;
- φ ∧ ψ holds when both hold at w; φ ∨ ψ when at least one holds at w;
- **φ ⇒ ψ holds at w when, for every w′ ≥ w at which φ holds, ψ also holds at w′** (line 21);
- *true* always holds and *false* never holds.

So ¬φ (that is, φ ⇒ ff) holds at w exactly when φ holds at *no* future world of w. A world can
therefore fail to force both φ and ¬φ: φ is not yet established, but it might be later. That gap is
how [excluded middle fails](#/node/Kripke.ExcludedMiddle.em_not_provable).

**Persistence for all formulas (`mono_at`, Kripke/Frame.lean lines 27–37).** If w ≤ w′ and φ holds at
w, then φ holds at w′. The variable case is the frame's persistence axiom; the implication case is
transitivity of ≤. Every truth established stays established.

`all_at_world` (lines 39–41) says every formula of a [context](#/node/Syntax.Ctxt) holds at w, and
`mono_all` (lines 60–64) lifts persistence to contexts.
""",
 [q("When does φ ⇒ ψ hold at w?",
    ["When φ fails at w or ψ holds at w", "When at every w′ ≥ w where φ holds, ψ holds too",
     "When ψ holds at every world", "When φ and ψ hold at w"], 1,
    "Kripke/Frame.lean line 21. The first option is the classical truth table, which is NOT used."),
   q("When does ¬φ (φ ⇒ ff) hold at w?",
    ["When φ fails at w", "When φ holds at no world w′ ≥ w", "Never", "Always"], 1,
    "Unfold the implication clause with ψ = ff, which never holds (line 23)."),
   q("Why does persistence hold for implications?",
    ["Because ≤ is transitive: futures of a future are futures", "Because of the valuation axiom",
     "It does not hold for implications"], 0,
    "mono_at, Kripke/Frame.lean line 35.")])

node("Kripke.Entails", "Semantic consequence in one model",
 "Γ entails φ in a model W when every world of W that forces all of Γ also forces φ.",
 r"""## Plain English

**Definition (`Entails`, Kripke/Frame.lean lines 66–67).** For a fixed
[Kripke frame](#/node/Kripke.Frame) W, a [context](#/node/Syntax.Ctxt) Γ entails φ when, at every
world w, if [all of Γ holds at w](#/node/Kripke.at_world) then φ holds at w.

**The proof rules are valid, one by one (Kripke/Frame.lean lines 72–117).** The section `ProofRules`
proves a semantic counterpart of each [Pf](#/node/Syntax.Pf) rule for `Entails W`. Two are worth
reading:

- **⇒ intro** (lines 101–103): to show φ ⇒ ψ at w, take a future w′ where φ holds; the context
  persists to w′ (`mono_all`), so the hypothesis gives ψ at w′.
- **⇒ elim** (lines 105–107): use the implication at w itself, which is a legal "future" because ≤ is
  reflexive.

These fifteen-or-so small lemmas are exactly what [soundness](#/node/Kripke.soundness) stitches together.
""",
 [q("What does Entails W Γ φ require?",
    ["φ holds at some world of W", "Every world of W that forces all of Γ forces φ",
     "Γ ⊢ φ", "φ holds at every world of every frame"], 1,
    "Kripke/Frame.lean lines 66–67."),
   q("Which property of ≤ makes the semantic ⇒ elim rule work?",
    ["Antisymmetry", "Reflexivity (w ≤ w)", "Totality", "Well-foundedness"], 1,
    "Kripke/Frame.lean lines 105–107 use le_refl."),
   q("Why does the semantic ⇒ intro rule need persistence of the context?",
    ["It doesn't", "Because it must use the assumptions Γ at a future world w′, not at w", "Because of false elim"], 1,
    "Kripke/Frame.lean lines 101–103 apply mono_all.")])

node("Kripke.SemEntails", "Semantic consequence over all models",
 "Γ ⊨ φ means: in every Kripke frame, at every world, if all of Γ holds then φ holds. Completeness is stated for frames whose worlds live in the lowest universe.",
 r"""## Plain English

**Definition (`SemEntails`, Kripke/Frame.lean lines 69–70).** Γ semantically entails φ (Γ ⊨ φ)
when, for every type W with a [Kripke frame](#/node/Kripke.Frame) structure, and every world w of W,
if all of Γ [holds at w](#/node/Kripke.at_world), then φ holds at w. It is
[Entails](#/node/Kripke.Entails) for all W at once.

**A universe detail.** The definition quantifies over all types W in a fixed universe level. The
[completeness theorem](#/node/Kripke.completeness) uses level 0, the level of ordinary types.
That is the natural reading ("all models"), and it is in fact the *weaker* hypothesis to need in
completeness, since the canonical model lives at level 0.
""",
 [q("How does SemEntails differ from Entails?",
    ["It is the same", "It quantifies over every frame W, not one fixed frame", "It uses proofs instead of worlds"], 1,
    "Kripke/Frame.lean lines 66–70."),
   q("At which universe level is SemEntails used in Kripke.completeness?",
    ["0 (ordinary types)", "1", "Every level simultaneously"], 0,
    "Kripke/Completeness.lean line 458 and line 501 instantiate it at level 0.")])

node("Kripke.soundness", "Headline: soundness for Kripke models",
 "Anything provable in intuitionistic natural deduction is true in every Kripke model: if Γ ⊢ φ then, in any frame W, every world that forces Γ forces φ.",
 r"""## Plain English

**Theorem (`soundness`, Kripke/Soundness.lean lines 11–46).** For every
[Kripke frame](#/node/Kripke.Frame) W, every [context](#/node/Syntax.Ctxt) Γ and
[formula](#/node/Syntax.Tm) φ: if [Γ ⊢ φ](#/node/Syntax.Pf) then
[Γ entails φ in W](#/node/Kripke.Entails).

This is the easy half of "Kripke semantics is exactly right for intuitionistic logic". Its main use is
*negative*: to show something is **not** provable, exhibit one Kripke world where it fails. The
project does this twice:

- the [one-point model](#/node/Kripke.Consistency.consistency) shows *false* is not provable;
- the [three-point model](#/node/Kripke.ExcludedMiddle.em_not_provable) shows excluded middle is not provable.

**Status.** The proof is complete as written (no `sorry`). It is stated as a `def` rather than a
`theorem`, which makes no difference to what it proves, since its type is a proposition. The Lean was
not built for this site.
""",
 [q("What does soundness let you conclude from Γ ⊢ φ?",
    ["φ is provable without Γ", "In every Kripke frame, each world forcing all of Γ forces φ",
     "Γ is consistent", "φ is classically true but not intuitionistically"], 1,
    "Kripke/Soundness.lean line 11."),
   q("How is soundness typically used in this project?",
    ["To prove formulas", "To show a formula is NOT provable, by a countermodel", "To build the canonical model"], 1,
    "Kripke/Soundness.lean lines 74–78 and 123–137 both apply it to a countermodel."),
   q("Does soundness hold for frames of any size and any universe?",
    ["Yes, W is an arbitrary type", "Only for finite frames", "Only for universe 0"], 0,
    "The frame W is arbitrary (Kripke/Soundness.lean line 11, universe u).")],
 caveats=["Not built: 'proved' means the file contains a complete-looking proof by structural recursion."],
 widgets=[{"type": "walkthrough", "title": "How the proof goes (Kripke/Soundness.lean, lines 11-46)",
   "config": {"steps": [
     {"text": "Recurse on the derivation of Γ ⊢ φ, one case per rule of Pf (Logic/Syntax.lean lines 30–43).", "link": "Syntax.Pf"},
     {"text": "Each case applies the matching semantic rule from the ProofRules section, e.g. assumption (Kripke/Soundness.lean lines 12–13 using Kripke/Frame.lean line 76), weakening (lines 14–15) and the ∧ rules (lines 16–25).", "link": "Kripke.Entails"},
     {"text": "The ∨ rules (lines 26–36) use the semantic ∨ intro and ∨ elim; ∨ elim splits on which disjunct holds at the world.", "link": "Kripke.at_world"},
     {"text": "⇒ intro (lines 37–39) is the one place persistence of the context is needed (Kripke/Frame.lean lines 101–103); ⇒ elim (lines 40–43) uses reflexivity.", "link": "Kripke.at_world"},
     {"text": "true intro is trivial (line 44) and false elim (lines 45–46) uses that false holds nowhere."}]}}])

node("Kripke.Consistency.consistency", "Consistency: false is not provable",
 "Nothing proves 'false' from no assumptions. Proof: a one-world model where false fails, plus soundness.",
 r"""## Plain English

**Theorem (`consistency`, Kripke/Soundness.lean lines 74–78).** There is no derivation of *false*
from the empty context.

**The model (lines 54–70).** `Triv` has a single world w0, related to itself, where no variable holds.
If ⊢ ff, [soundness](#/node/Kripke.soundness) would make *false* hold at w0, but
[*false* holds nowhere](#/node/Kripke.at_world).

Any one-point model would do; this is the smallest countermodel argument there is.
""",
 [q("Which model refutes ⊢ ff?",
    ["The canonical model", "A one-world model with no true variables", "The three-world excluded-middle model", "No model is needed"], 1,
    "Kripke/Soundness.lean lines 54–70."),
   q("Which theorem turns a derivation into truth at w0?", ["completeness", "soundness", "multicut"], 1,
    "Kripke/Soundness.lean line 77.")])

node("Kripke.ExcludedMiddle.em_not_provable", "Headline: excluded middle is not provable",
 "The law of excluded middle, 'P or not P', has no intuitionistic proof. A three-world Kripke model, where P becomes true along one future and is ruled out along another, is the witness.",
 r"""## Plain English

**Theorem (`em_not_provable`, Kripke/Soundness.lean lines 123–137).** For the variable P = variable 0,
there is no derivation, from no assumptions, of P ∨ (P ⇒ ff), i.e. of P ∨ ¬P.

**The model (`EMFrame`, lines 96–118).** Three worlds, drawn in the docstring at lines 86–95:

- w0 at the bottom, below both w1 and w2 (w1 and w2 are incomparable);
- P holds at w1 only.

At w0, P does not hold (it is not yet settled). ¬P does not hold either, because w1 is a future of w0
where P holds. So [P ∨ ¬P fails at w0](#/node/Kripke.at_world), and by
[soundness](#/node/Kripke.soundness) it cannot be provable.

(World w2, where ¬P holds, is not needed for the argument. The two-world model w0 ≤ w1 would already
work; w2 makes the picture symmetric: one future decides P, the other decides ¬P.)

This is the formal content of the slogan "intuitionistic logic does not prove excluded middle", and
shows the [proof system](#/node/Syntax.Pf) is strictly weaker than classical logic.
""",
 [q("Why does ¬P fail at w0?",
    ["Because P holds at w0", "Because w1 ≥ w0 and P holds at w1", "Because w2 is above w0", "It does not fail"], 1,
    "Kripke/Soundness.lean lines 135–137."),
   q("Which formula exactly is shown unprovable?",
    ["P ⇒ P", "¬¬P ⇒ P for every P", "variable 0 ∨ (variable 0 ⇒ false), from no assumptions", "false"], 2,
    "Kripke/Soundness.lean line 123. It is one instance, which is enough to show the law is not derivable as a schema."),
   q("Is world w2 essential to the argument?",
    ["Yes", "No: w0 ≤ w1 with P at w1 alone already refutes it"], 1,
    "The proof (lines 128–137) only uses w0 and w1."),
   q("Does this theorem say excluded middle is false?",
    ["Yes", "No: only that it is not provable in this system; its negation is not provable either"], 1,
    "¬(P ∨ ¬P) is also unprovable; the statement here is about derivability only.")],
 caveats=["The statement is about a single instance (variable 0). That suffices to show the schema is not derivable, which is what the name claims.",
          "Not built: 'proved' means the file contains a complete-looking proof."],
 widgets=[{"type": "walkthrough", "title": "How the proof goes (Kripke/Soundness.lean, lines 96-137)",
   "config": {"steps": [
     {"text": "Build the three-world frame: the order (lines 99–104) puts w0 below everything and w1, w2 only below themselves; preorder laws by case analysis (lines 106–109).", "link": "Kripke.Frame"},
     {"text": "Valuation: variable 0 holds at w1 only; persistence checked by cases (lines 111–118).", "link": "Kripke.Frame"},
     {"text": "Suppose a derivation exists. Soundness at w0 (with the empty context, trivially satisfied) gives P ∨ ¬P at w0 (line 126).", "link": "Kripke.soundness"},
     {"text": "Case P at w0: the valuation says no (lines 129–131)."},
     {"text": "Case ¬P at w0: apply it to the future w1, where P holds, to get false (lines 132–137).", "link": "Kripke.at_world"}]}}])

node("Kripke.opensFrame", "Example: open sets as a Kripke frame",
 "The open sets of any topological space, ordered by reverse inclusion, form a Kripke frame where a variable holds on an open set U when U lies inside that variable's region. Only the construction is given; no theorem uses it.",
 r"""## Plain English

**Definitions (`frameOfPreorder`, Kripke/Examples.lean lines 7–11; `opensFrame`, lines 30–34).**
`frameOfPreorder` packages any preorder plus a persistent valuation as a
[Kripke frame](#/node/Kripke.Frame).

`opensFrame` applies it to a topological space X and an assignment of an open set p(i) to each
variable i. Worlds are open sets, with U ≤ V when V ⊆ U (smaller open set = more information), and
variable i holds on U when U ⊆ p(i). Persistence is immediate: shrinking U keeps it inside p(i).

This hints at the link between intuitionistic logic and topology (open sets form a Heyting algebra),
which the [Beth](#/node/Beth.BethFrame) half of the project develops further with coverages. The
file proves nothing about this frame beyond its being one.
""",
 [q("In opensFrame, when is U ≤ V?", ["U ⊆ V", "V ⊆ U", "U and V are disjoint"], 1,
    "Reverse inclusion, Kripke/Examples.lean lines 13–24 (docstring) and line 33."),
   q("When does variable i hold on the open set U?", ["U ⊆ p(i)", "p(i) ⊆ U", "U meets p(i)"], 0,
    "Kripke/Examples.lean line 33.")])

import importlib.util as _u, os as _o
_s = _u.spec_from_file_location("_extra", _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "_extra.py"))
_m = _u.module_from_spec(_s); _s.loader.exec_module(_m); _m.apply(NODES)
