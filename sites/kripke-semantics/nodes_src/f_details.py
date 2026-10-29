NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

node("Kripke.all_at_world", "A whole context holds at a world",
 "A context holds at a world when each of its formulas does; the empty context holds everywhere. Because contexts persist upward, assumptions stay available at every future world.",
 r"""## Plain English

**Definition (`all_at_world`, Kripke/Frame.lean lines 39–41).** By recursion on the list: the empty
[context](#/node/Syntax.Ctxt) holds at every world, and φ, Γ holds at w when φ is
[forced at w](#/node/Kripke.at_world) and Γ holds at w.

Two small facts follow: if Γ ≤ Δ (Δ has extra assumptions in front) and Δ holds at w, then Γ holds at w
(`all_at_of_suffix`, lines 55–58); and if Γ holds at w and w ≤ w′, then Γ holds at w′
(`mono_all`, lines 60–64).

This is what the hypotheses of [Entails](#/node/Kripke.Entails) and [SemEntails](#/node/Kripke.SemEntails) use.
""",
 [q("Where does the empty context hold?", ["Nowhere", "At every world", "Only at minimal worlds"], 1,
    "Kripke/Frame.lean line 40."),
   q("If Γ holds at w and w ≤ w′, does Γ hold at w′?", ["Yes (mono_all)", "No", "Only for variables"], 0,
    "Kripke/Frame.lean lines 60–64."),
   q("If φ, Γ holds at w, does Γ hold at w?", ["Yes", "No"], 0,
    "By definition (line 41), or by all_at_of_suffix (lines 55–58).")])

node("Semantics", "`Semantics` (an alias for Kripke frames)",
 "A top-level abbreviation that renames Kripke.Frame. Nothing on this site depends on it; the scanner links to it only because the soundness proof calls lemmas in a namespace of the same name.",
 r"""## Plain English

**Definition (`Semantics`, Kripke/Soundness.lean line 5).** `Semantics` is just another name for
[Kripke.Frame](#/node/Kripke.Frame).

**Why it shows up here.** The soundness proof calls the per-rule lemmas `Semantics.assumption`,
`Semantics.and_I`, …, which live in the *namespace* `Kripke.Semantics` (Kripke/Frame.lean lines 72–117),
not in this abbreviation. This site's text scanner cannot tell the difference, so it lists the alias as
something [soundness](#/node/Kripke.soundness) mentions. The statement of soundness does not actually use
it.
""",
 [q("What is `Semantics` (Kripke/Soundness.lean line 5)?", ["A new kind of model", "Another name for Kripke.Frame", "A theorem"], 1,
    "It is an abbrev for Kripke.Frame."),
   q("Where do the lemmas Semantics.and_I etc. live?",
    ["In the namespace Kripke.Semantics in Kripke/Frame.lean", "Inside the abbreviation", "In Mathlib"], 0,
    "Kripke/Frame.lean lines 72–117."),
   q("Does the soundness statement depend on this alias?", ["No", "Yes"], 0,
    "Its statement mentions Frame, Pf and Entails (Kripke/Soundness.lean line 11).")])

node("Beth.maximal_sieve", "The maximal sieve",
 "The maximal sieve on p is the set of all futures of p. It always covers p, and it is how Beth semantics reduces to Kripke semantics.",
 r"""## Plain English

**Definition (`maximal_sieve`, Beth/Coverage.lean lines 23–28).** All q with p ≤ q, which is a
[sieve](#/node/Beth.Sieve) because ≤ is transitive.

Every [coverage](#/node/Beth.Coverage) must count it as covering (line 38). In
[Beth forcing](#/node/Beth.at_world), using it as the witness for φ ∨ ψ amounts to "every future forces
φ or ψ"; this is what semantic ∨ introduction does (Beth/Semantics.lean lines 150–172). The coverage in
which it is the *only* covering sieve turns any Kripke frame into a Beth frame
([bethFrameOfKripke](#/node/Beth.Examples.bethFrameOfKripke)).
""",
 [q("Which points are in the maximal sieve on p?", ["Only p", "All q ≥ p", "All points"], 1, "Beth/Coverage.lean line 25."),
   q("Must the maximal sieve cover p in every coverage?", ["Yes", "No"], 0, "Beth/Coverage.lean line 38."),
   q("Does the maximal sieve on p contain p?", ["Yes, since p ≤ p", "No"], 0, "Reflexivity of the preorder.")])

node("Beth.pullback", "Pulling a sieve forward",
 "Given a sieve S on p and a later point q, the pullback is the part of S lying above q. Coverage stability says this is again a cover when S was.",
 r"""## Plain English

**Definition (`pullback`, Beth/Coverage.lean lines 31–34).** For p ≤ q and a [sieve](#/node/Beth.Sieve)
S on p, the pullback is the set of r ∈ S with q ≤ r. It is a sieve on q.

The name comes from Grothendieck topologies, where sieves are pulled back along arrows; the comment at
line 30 notes that in this preorder setting it moves forward in time.

It appears in two [coverage](#/node/Beth.Coverage) axioms (transitivity, line 40, and stability, line 41)
and in the persistence proof of [Beth forcing](#/node/Beth.at_world) for ∨ (Beth/Semantics.lean
lines 39–49).
""",
 [q("Which points are in the pullback of S to q?", ["S's members that are ≥ q", "All points ≥ q", "S's members ≤ q"], 0,
    "Beth/Coverage.lean line 32."),
   q("Which coverage axiom says pullbacks of covers are covers?", ["maximal", "stability", "transitive"], 1,
    "Beth/Coverage.lean line 41."),
   q("Is the pullback a sieve on p or on q?", ["On q", "On p"], 0, "Beth/Coverage.lean line 31.")],
 caveats=["Line 33 (the proof that members are ≥ q) appears, from the text alone, to use a name that is never bound. If so, this definition and everything Beth-related would fail to compile. Not built, so unconfirmed; see the Trust page."])

node("Beth.HasCoverage", "Points with a chosen coverage",
 "HasCoverage equips a preorder with one coverage; `covers p S` then reads 'S covers p'. It is the bridge from the coverage axioms to Beth frames.",
 r"""## Plain English

**Definitions (`HasCoverage`, Beth/Coverage.lean lines 43–44; `covers`, line 48).** A type with
`HasCoverage` is a preorder together with a [coverage](#/node/Beth.Coverage). The function `covers p`
returns that coverage's set of covering [sieves](#/node/Beth.Sieve) on p. Lines 50–58 restate the three
coverage axioms in terms of `covers`.

[Beth frames](#/node/Beth.BethFrame) extend `HasCoverage`, so in Beth semantics "S covers w" always means
`covers w S` for the frame's own coverage.
""",
 [q("What does `covers p` return?", ["A set of sieves on p", "A single sieve", "A proof"], 0, "Beth/Coverage.lean line 48."),
   q("Which class extends HasCoverage?", ["Kripke.Frame", "BethFrame", "Preorder"], 1, "Beth/Semantics.lean line 11."),
   q("How many coverages does a HasCoverage type carry?", ["Exactly one, fixed by the instance", "All of them"], 0,
    "Beth/Coverage.lean line 44.")])

node("Beth.covers", "`covers`: the covering sieves of a point",
 "`covers w S` is the statement 'S is a covering sieve on w' for the ambient coverage. It is a one-line shorthand.",
 r"""## Plain English

**Definition (`covers`, Beth/Coverage.lean line 48).** In a type with a chosen coverage
([HasCoverage](#/node/Beth.HasCoverage)), `covers p` is that coverage's set of covering
[sieves](#/node/Beth.Sieve) on p. It appears in the [Beth frame](#/node/Beth.BethFrame) axioms and in the
∨ clause of [Beth forcing](#/node/Beth.at_world).

(The structure [Coverage](#/node/Beth.Coverage) also has a *field* called `covers`; it is the same
data, accessed through the instance.)
""",
 [q("Where does `covers` appear in the forcing relation?", ["The ∨ clause", "The ⇒ clause", "Nowhere"], 0,
    "Beth/Semantics.lean lines 25–26."),
   q("Is `covers` new data or a shorthand?", ["A shorthand for the instance's coverage", "New data"], 0,
    "Beth/Coverage.lean line 48."),
   q("Which axiom of BethFrame mentions covers?", ["Both the sheaf condition and non-empty covers", "Neither"], 0,
    "Beth/Semantics.lean lines 12–13.")])

node("Beth.all_at_world", "A whole context holds at a Beth world",
 "As for Kripke frames: a context holds at a world when each of its formulas is Beth-forced there.",
 r"""## Plain English

**Definition (`all_at_world`, Beth/Semantics.lean lines 98–100).** The same recursion as the
[Kripke version](#/node/Kripke.all_at_world), using [Beth forcing](#/node/Beth.at_world). The
suffix and persistence lemmas are repeated at lines 104–123.
""",
 [q("Which forcing relation does it use?", ["Beth forcing", "Kripke forcing", "Provability"], 0, "Beth/Semantics.lean line 100."),
   q("Does a context persist to future Beth worlds?", ["Yes (mono_all)", "No"], 0, "Beth/Semantics.lean lines 119–123."),
   q("Where does the empty context hold?", ["At every world", "Nowhere"], 0, "Beth/Semantics.lean line 99.")])

node("Beth.Entails", "Semantic consequence in one Beth frame",
 "Γ entails φ in a Beth frame W when every world of W forcing all of Γ forces φ.",
 r"""## Plain English

**Definition (`Entails`, Beth/Semantics.lean lines 125–126).** The [Kripke definition](#/node/Kripke.Entails)
with [Beth forcing](#/node/Beth.at_world). [Beth soundness](#/node/Beth.soundness) concludes this for every
Beth frame; [SemEntails](#/node/Beth.SemEntails) quantifies over all of them.
""",
 [q("What does Entails W Γ φ say?", ["Every world of W forcing Γ forces φ", "Γ ⊢ φ", "φ holds somewhere in W"], 0,
    "Beth/Semantics.lean lines 125–126."),
   q("Which headline concludes Entails?", ["Beth.soundness", "Beth completeness"], 0, "Beth/Soundness.lean line 10."),
   q("Is W fixed in Entails?", ["Yes; SemEntails quantifies over all W", "No"], 0, "Beth/Semantics.lean lines 125–129.")])
