NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]


node("Unification.Unifier",
 "Unifiers and most general unifiers",
 "A unifier of a list of equations between atoms is a substitution that makes both sides of every equation identical. A most general unifier (mgu) is a unifier from which every other unifier can be obtained by substituting further.",
 r"""## Plain English

**Definitions (InferenceInLean/D_Unification.lean).**
- An `Equality` (lines 17–18) is a pair of [atoms](#/node/Syntax.Atom); an `EqualityProblem` (lines 21–22) is a
  list of them, E = {A₁ ≐ B₁, …, Aₙ ≐ Bₙ}.
- `Unifier E σ` (lines 34–36): Aᵢσ = Bᵢσ, syntactically, for every equation.
- `MostGeneralUnifier E σ` (lines 48–50): σ is a unifier, and σ ≤ τ for every unifier τ, i.e. every unifier is
  τ = ρ ∘ σ for some ρ ([more general](#/node/Syntax.Substitution)).
- `Unifiable E` (lines 56–57): some unifier exists.

The example on lines 38–45: σ = {y ↦ f(x)} unifies P(f(x)) ≐ P(y).

In the resolution rules the problem is the single equation A ≐ B between the two atoms being resolved. The
soundness proofs only use that σ is a **unifier**, that is, Aσ = Bσ. Most-generality isn't needed for soundness. It
matters for completeness, which this project doesn't cover.
""",
 [q("Which σ unifies P(f(x)) ≐ P(y)?", ["{y ↦ f(x)}", "{x ↦ y}", "None exists"], 0,
    "`example_unification` (InferenceInLean/D_Unification.lean lines 38–45)."),
  q("What does 'most general' add to 'unifier'?", ["Every other unifier is σ followed by some ρ", "σ moves the fewest variables", "σ is idempotent"], 0,
    "InferenceInLean/D_Unification.lean line 50."),
  q("Do the soundness proofs need σ to be *most general*?", ["No, Aσ = Bσ is all they use", "Yes, essentially"], 0,
    "Only the unifier part is used: `hBσeqAσ` (InferenceInLean/F_Resolution.lean lines 174–175)."),
  q("Are the two sides of an Equality terms or atoms?", ["Atoms", "Terms"], 0,
    "`Atom sig X × Atom sig X` (InferenceInLean/D_Unification.lean line 18)."),
 ])


node("Unification.unifiable_iff_mgu_idempot",
 "Headline (PARTIAL, sorry): the main unification theorem",
 "The claim: a unification problem has some unifier exactly when it has an idempotent most general unifier that mentions only the problem's own variables. Only the easy direction is proved; the hard direction (existence of an mgu) is sorry.",
 r"""## Plain English

**Theorem (`unifiable_iff_mgu_idempot`, alias `main_unification_theorem`, InferenceInLean/D_Unification.lean
lines 59–71).** For an equality problem E:

E is [unifiable](#/node/Unification.Unifier) **iff** there is a σ that is a most general unifier of E, is
[idempotent](#/node/Syntax.idempotent_iff_inter_empty), and has dom(σ) ∪ codom(σ) ⊆ the variables of E.

**Status: PARTIAL (sorry).**
- (⇐) is proved (lines 68–70): an mgu is in particular a unifier.
- (⇒) is `sorry` (line 63). The authors' comment (lines 64–67) says this direction needs the standard unification
  algorithm, which they tried but judged outside the scope of the project.

The (⇒) direction is the real content: it is the theorem that the unification algorithm (Robinson's, or the
Martelli–Montanari rule system in the notes) always finds an mgu when one exists.

**Nothing else uses it.** The resolution rules take the mgu σ as a given hypothesis, so the soundness theorems don't
depend on this sorry.
""",
 [q("Which direction is proved?", ["Only ⇐ (an mgu is a unifier)", "Only ⇒", "Both", "Neither"], 0,
    "The ⇒ branch is `sorry` (InferenceInLean/D_Unification.lean line 63)."),
  q("Do the resolution soundness theorems depend on this sorry?", ["No, they take σ as a hypothesis", "Yes"], 0,
    "`hmgu : MostGeneralUnifier [(A, B)] σ` is an argument of `generalResolutionRuleSound` (InferenceInLean/F_Resolution.lean line 105)."),
  q("What would proving ⇒ amount to?", ["Showing a unification algorithm always finds an idempotent mgu", "Showing every substitution is idempotent", "A one-line fact"], 0,
    "The authors' comment, InferenceInLean/D_Unification.lean lines 64–67."),
 ],
 caveats=["PARTIAL (sorry): the forward direction is sorry (InferenceInLean/D_Unification.lean line 63). Only the trivial backward direction is proved."],
 widgets=walk("How the proof goes (InferenceInLean/D_Unification.lean, lines 59-71)", [
  {"text": "Split into the two directions (line 62)."},
  {"text": "(⇒) unifiable implies an idempotent mgu exists: not proved (line 63).", "lean": "· sorry"},
  {"text": "(⇐) take the mgu σ; its first component is a unifier, so E is unifiable (lines 68–70).", "link": "Unification.Unifier",
   "lean": "obtain ⟨σ, ⟨⟨⟩⟩⟩ := h"},
 ]))


node("Inferences.Inference",
 "Inferences and inference systems",
 "An inference is a set of premise clauses, a conclusion clause and a side condition. An inference system is a finite list of such inferences.",
 r"""## Plain English

**Definition (`Inference`, InferenceInLean/E_Inference.lean lines 23–26).** An inference has
- `premises`: a **set** of clauses,
- `conclusion`: a clause,
- `condition`: a proposition that must hold for the inference to be used (for resolution: "σ is an mgu of A ≐ B").

The comment on line 22 says inferences are limited to clauses.

**Definition (`InferenceSystem`, line 28).** A `List` of inferences.

**Note: a list of instances, not a schema.** In the notes, an inference *rule* such as resolution stands for
infinitely many inferences, one for every choice of clauses and atoms. Here an `Inference` is one concrete
instance, and an inference system is a finite list of instances. The resolution "systems" in this project are
two-element lists for one fixed choice of A, B, C, D, σ (see
[generalResolution_soundness](#/node/Resolution.generalResolution_soundness)). Since the soundness theorems hold for
every such choice, they still give soundness of the rules.
""",
 [q("What is an inference system here?", ["A finite list of concrete inferences", "A set of rule schemas", "A proof"], 0,
    "`abbrev InferenceSystem := List (Inference sig X)` (InferenceInLean/E_Inference.lean line 28)."),
  q("Are the premises a list or a set?", ["A set", "A list"], 0,
    "`premises : Set (Clause sig X)` (InferenceInLean/E_Inference.lean line 24)."),
  q("What is the `condition` of a general resolution inference?", ["That σ is an mgu of A ≐ B", "True", "That C and D share no variables"], 0,
    "InferenceInLean/F_Resolution.lean line 218."),
 ])


node("Inferences.Proof",
 "Proofs and provability N ⊢ C",
 "A proof from assumptions N is a non-empty list of clauses ending with the conclusion, in which every clause is either an assumption or the conclusion of an inference of the system whose condition holds and whose premises all appear earlier.",
 r"""## Plain English

**Definition (`Proof Γ`, InferenceInLean/E_Inference.lean lines 37–46).** A proof in an
[inference system](#/node/Inferences.Inference) Γ consists of
- a set of `assumptions` and a `conclusion`,
- a list `clauses` = C₀, C₁, …, Cₖ that is non-empty (line 41) and ends with the conclusion (lines 42–43),
- and the validity condition (lines 44–46): for every i, either Cᵢ is an assumption, or there is an inference in Γ
  whose conclusion is Cᵢ, whose condition holds, and each of whose premises equals some Cⱼ with j < i.

The comment on lines 35–36 says this is one of several possible translations of the notes' definition, chosen for
convenience.

**Definition (`Provability Γ N C`, lines 50–51), N ⊢ C:** there is a proof with assumptions N and conclusion C.
""",
 [q("Can a clause in a proof use a premise that appears later in the list?", ["No, premises must have index j < i", "Yes"], 0,
    "InferenceInLean/E_Inference.lean line 46."),
  q("Can a proof be the empty list?", ["No", "Yes"], 0, "`clauses_not_empty` (InferenceInLean/E_Inference.lean line 41)."),
  q("What must be true of an inference's condition for it to be used?", ["It must hold", "Nothing"], 0,
    "`inference.condition` appears in the validity clause (InferenceInLean/E_Inference.lean line 45)."),
 ])


node("Inferences.Soundness",
 "Soundness: two definitions",
 "An inference system is sound if every inference whose condition holds has premises that entail its conclusion. The general version says every provable clause is entailed by the assumptions.",
 r"""## Plain English

**Definition (`Soundness Γ`, InferenceInLean/E_Inference.lean lines 55–57).** For every inference in Γ whose condition
holds, premises ⊨ conclusion, in the sense of [ClauseSetEntails](#/node/Models.ClauseSetEntails). This is the
definition in the notes: "each single step is sound".

**Definition (`GeneralSoundness Γ`, lines 62–63).** For all N and C: if N ⊢ C ([Provability](#/node/Inferences.Proof))
then N ⊨ C. This is what "sound" usually means: everything you can prove is true.

The project shows the first implies the second:
[generalSoundness_of_soundness](#/node/Inferences.generalSoundness_of_soundness).

Both definitions carry the universe type as a parameter: "sound" means "sound for interpretations on this universe".
The theorems prove it for every universe.
""",
 [q("Which definition is about single inferences?", ["Soundness", "GeneralSoundness"], 0,
    "InferenceInLean/E_Inference.lean lines 55–57."),
  q("What does GeneralSoundness say?", ["N ⊢ C implies N ⊨ C", "N ⊨ C implies N ⊢ C", "Every clause is provable"], 0,
    "InferenceInLean/E_Inference.lean line 63. The converse would be completeness."),
  q("Does Soundness require anything of inferences whose condition fails?", ["No", "Yes, they must still be sound"], 0,
    "`inference.condition →` (InferenceInLean/E_Inference.lean line 56)."),
 ])


node("Inferences.generalSoundness_of_soundness",
 "Headline: sound steps give sound proofs",
 "If every single inference of a system is sound, then everything provable in the system from N is entailed by N. The proof is a strong induction along the proof list.",
 r"""## Plain English

**Theorem (`generalSoundness_of_soundness`, InferenceInLean/E_Inference.lean lines 68–111).** For any inference
system Γ: if Γ is [sound](#/node/Inferences.Soundness) step by step, then N ⊢ C implies N ⊨ C for all N and C.

In words: fix an interpretation I in which every clause of N is true. Show by strong induction on i that every clause
Cᵢ of the [proof](#/node/Inferences.Proof) is true in I:
- if Cᵢ is an assumption, it is in N, so it is true;
- if Cᵢ is the conclusion of an inference, its premises are earlier clauses, which are true by the induction hypothesis,
  so the inference's soundness makes Cᵢ true.

The last clause is the conclusion C, so C is true in I.

### Scope

Γ is a finite list of concrete inferences ([see here](#/node/Inferences.Inference)). To apply this to a resolution
proof, you would take Γ to be the list of resolution and factorisation instances that the proof uses; each of them is
sound by [generalResolution_soundness](#/node/Resolution.generalResolution_soundness). The project doesn't spell out
that combination as a theorem, but it is a short step.
""",
 [q("What is the induction on?", ["The position i of a clause in the proof list (strong induction)", "The size of the clauses", "The number of variables"], 0,
    "`Nat.case_strong_induction_on` (InferenceInLean/E_Inference.lean line 77)."),
  q("Does the theorem prove completeness (N ⊨ C implies N ⊢ C)?", ["No, only soundness", "Yes"], 0,
    "The conclusion is `GeneralSoundness` (InferenceInLean/E_Inference.lean lines 62–63, 69)."),
  q("Does the theorem talk directly about resolution?", ["No, it holds for any inference system", "Yes, only resolution"], 0,
    "Γ is arbitrary (InferenceInLean/E_Inference.lean line 69)."),
 ],
 caveats=["Proof complete in the source, with no sorry; not machine-checked for this site.",
          "The project doesn't state the combined theorem 'resolution proofs are sound'; it gives the two pieces."],
 widgets=walk("How the proof goes (InferenceInLean/E_Inference.lean, lines 68-111)", [
  {"text": "Fix N, C, a proof of C from N, an interpretation I in which all of N is true, and an assignment β (line 70)."},
  {"text": "Claim: every clause in the proof list is true (line 73). Prove it for index i by strong induction (lines 74–77).",
   "lean": "induction' i using Nat.case_strong_induction_on with i ih generalizing β"},
  {"text": "Index 0: it must be an assumption, or an inference with no earlier premises (lines 78–79)."},
  {"text": "Index i + 1: if it is an assumption, it is true because it is in N (lines 80–82)."},
  {"text": "Otherwise it is the conclusion of a sound inference whose premises are earlier, hence true by induction (lines 83–94).",
   "lean": "have hinfsound := hsound inference hin", "link": "Inferences.Soundness"},
  {"text": "Apply the claim to the last clause, which is the conclusion C (lines 99–111).",
   "lean": "have hfconclusion := proof.is_valid (proof.clauses.length - 1) hlen"},
 ]))
