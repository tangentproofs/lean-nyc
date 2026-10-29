NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]


node("AlternatingAnalyticChallenge.false_of_contDiff_omega_compContinuousLinearMapCLM",
 "Headline: the general C^ω statement for precomposition is false",
 "If you assume that precomposition f ↦ m ∘ (f, …, f) on continuous alternating maps is analytic (C^ω) for every normed field, every normed space and every finite index type, you can derive False. The smooth (C^n) version is true; the analytic version fails, and the failure lives in characteristic 2.",
 r"""## Plain English

**Theorem (`false_of_contDiff_omega_compContinuousLinearMapCLM`, Solution.lean lines 13–21).** Suppose that for
**every** nontrivially normed field 𝕜, **all** normed spaces E, E′, F over 𝕜 and **every** finite index type ι, the map

> f ↦ (m ↦ m ∘ (f, …, f)),  from continuous linear maps E → E′ to continuous linear maps
> Alt^ι(E′, F) → Alt^ι(E, F),

is `ContDiff 𝕜 ω`, that is, smooth of analytic class. Then `False`.

Here Alt^ι(E, F) is the space of continuous alternating ι-linear maps E × ⋯ × E → F, and the map in question is
Mathlib's `ContinuousAlternatingMap.compContinuousLinearMapCLM`: it pulls an alternating form back along f by feeding
f(x₁), …, f(xₖ) into it.

**Why anyone would want the statement.** The map is a homogeneous polynomial of degree #ι in f, and the Challenge.lean
docstring notes that it is C^n for every finite n in every characteristic, and C^ω when (#ι)! is invertible in 𝕜. The
fully general C^ω version is what one would need to give bundles of alternating maps an analytic vector-bundle
structure. This theorem says that general version cannot be proved, because it is inconsistent.

**What "derive False" means here.** The theorem takes the universal statement as a hypothesis `h` and returns
`False`, so it is a proof of the *negation* of that universal statement. To refute a "for all", one counterexample
is enough, and the project builds one: a specific field `K`, E = E′ = [ℓ^∞](#/node/AltCounter.Linf), the target
space [F](#/node/AltCounter.F) and ι = `Fin 2`.

**Where the work is.** The proof is one line: it calls
`AltCounter.false_of_general_contDiff_omega` (AltCounter/Final.lean lines 25–36), which

1. takes the field from [exists_field](#/node/AltCounter.exists_field);
2. turns that field's "nested balls with empty intersection" into [NSC](#/node/AltCounter.NSC) using
   [nsc_of_hasEmptyNestedBalls](#/node/AltCounter.nsc_of_hasEmptyNestedBalls);
3. applies `h` at that field, E = E′ = ℓ^∞(K), F = `F K` and ι = `Fin 2`;
4. contradicts it with [not_contDiff_omega_Q_of_NSC](#/node/AltCounter.not_contDiff_omega_Q_of_NSC).

Solution.lean repeats the statement of Challenge.lean word for word (Challenge.lean lines 29–37 have it with
`sorry`); the upstream CI uses `leanprover/comparator` to check that the two match.
""",
 [q("What does this theorem prove?",
    ["That precomposition is analytic in characteristic 2",
     "That the universal statement 'precomposition is C^ω for all fields, spaces and ι' is false",
     "That precomposition is not C^1", "That ℓ^∞ is not a Banach space"], 1,
    "The universal statement is the hypothesis h (Solution.lean lines 14–20) and the conclusion is False (line 20)."),
   q("Does the theorem contradict the fact that precomposition is C^n for every finite n?",
    ["Yes", "No: only the analytic exponent ω is refuted"], 1,
    "The hypothesis uses ω (Solution.lean line 17). The Challenge.lean docstring states the C^n result for n : ℕ∞, which this theorem leaves alone."),
   q("Which index type ι does the counterexample use?",
    ["ℕ", "Fin 2 (alternating 2-forms)", "Fin 3", "Every finite type at once"], 1,
    "AltCounter/Final.lean line 36 instantiates h with ι = Fin 2."),
   q("Why is a single field enough?",
    ["Because the hypothesis is a 'for all' over fields, so one counterexample refutes it",
     "Because all fields of characteristic 2 are isomorphic", "Because ℓ^∞ does not depend on the field"], 0,
    "h quantifies over every nontrivially normed field 𝕜 (Solution.lean line 14).")],
 caveats=["The hypothesis quantifies over types in universe 0 (`Type`), as the upstream formalization.yaml notes. That is harmless: the counterexample field is in `Type`.",
          "'ContDiff 𝕜 ω' is Mathlib's analytic smoothness class (ω is written ⊤ in WithTop ℕ∞). In this Mathlib it implies being analytic near every point, which is what the proof uses.",
          "Lean was not built for this site: 'proved' means the file has a complete-looking proof with no sorry."],
 widgets=walk("How the proof goes (Solution.lean lines 13–21 and AltCounter/Final.lean lines 25–36)", [
    {"text": "Solution.lean just forwards the hypothesis to the library theorem.", "lean": "AltCounter.false_of_general_contDiff_omega h"},
    {"text": "Get a complete ultrametric field K of characteristic 2 with nested balls having empty intersection (Final.lean line 33).", "link": "AltCounter.exists_field"},
    {"text": "Turn the nested balls into NSC, and NSC into ¬ C^ω for the concrete map Q (Final.lean line 35).", "link": "AltCounter.not_contDiff_omega_Q_of_NSC"},
    {"text": "Feed it the hypothesis at 𝕜 = K, E = E′ = ℓ^∞(K), F = F K and ι = Fin 2 (Final.lean line 36). This is literally Q, so the two contradict each other.", "link": "AltCounter.Q"}]))


node("AlternatingAnalyticChallenge.false_of_contDiff_omega_compContinuousLinearMapCLM_charTwo_banach",
 "Headline: it already fails for Banach spaces in characteristic 2",
 "A sharper refutation: even if you only claim analyticity over complete ultrametric fields of characteristic 2, for Banach spaces E = E′ and alternating 2-forms, the claim is still inconsistent. The same counterexample works, because it already satisfies all these extra conditions.",
 r"""## Plain English

**Theorem (`false_of_contDiff_omega_compContinuousLinearMapCLM_charTwo_banach`, Solution.lean lines 25–33).** Suppose
that for every nontrivially normed field 𝕜 that is **ultrametric**, **complete** and of **characteristic 2**, and all
**complete** normed spaces (Banach spaces) E and F over it, the precomposition map

> f ↦ (m ↦ m ∘ (f, f)),  from continuous linear maps E → E to continuous linear maps Alt²(E, F) → Alt²(E, F),

is `ContDiff 𝕜 ω`. Then `False`.

Compared with the [general headline](#/node/AlternatingAnalyticChallenge.false_of_contDiff_omega_compContinuousLinearMapCLM),
the hypothesis is **weaker**: it promises less (fewer fields, only Banach spaces, E′ = E, only ι = `Fin 2`). Refuting
a weaker hypothesis is a stronger result. It says that the obstruction really is about characteristic 2 and 2-forms,
not about some pathology like incomplete spaces.

**Why the extra conditions cost nothing.** The counterexample from the first headline already has every property
asked for here:

- the field from [exists_field](#/node/AltCounter.exists_field) is ultrametric, complete and of characteristic 2;
- [ℓ^∞](#/node/AltCounter.Linf) is complete (Mathlib);
- [F](#/node/AltCounter.F) is a closed subspace of a Banach space, hence complete. AltCounter/Final.lean lines 20–22
  record this as an instance.

The proof (AltCounter/Final.lean lines 40–51) is the same as before, with `h K (Linf K) (F K)`.

**A consistency check.** For ι = `Fin 2`, the known sufficient condition for C^ω is that 2! = 2 be invertible in 𝕜.
In characteristic 2, 2 = 0, so that condition fails. The counterexample lives exactly where the known positive result
does not apply.
""",
 [q("Compared with the general headline, is the hypothesis here stronger or weaker?",
    ["Stronger (it promises more)", "Weaker (it promises less), so refuting it is a stronger result", "Identical"], 1,
    "It only claims C^ω over complete ultrametric fields of characteristic 2, for Banach spaces and ι = Fin 2 (Solution.lean lines 26–32)."),
   q("Why does the result not contradict the known C^ω theorem when (#ι)! is invertible?",
    ["Because 2! = 2 = 0 in characteristic 2, so that theorem does not apply",
     "Because ℓ^∞ is not a normed space", "It does contradict it"], 0,
    "With ι = Fin 2 the factorial is 2, which is zero in a field of characteristic 2."),
   q("Why is the target space F complete?",
    ["It is finite-dimensional", "It is a closed subspace of the Banach space ℓ^∞(ℕ × ℕ)", "It is not complete"], 1,
    "F is a topological closure (AltCounter/Main.lean lines 33–35); the instance is in AltCounter/Final.lean lines 20–22.")],
 caveats=["Same status as the general headline: complete-looking proof, no sorry, Lean not built for this site.",
          "Only E′ = E and ι = Fin 2 are treated. The upstream notes sketch, on paper, how larger ι reduce to this case in characteristic 2; that reduction is not formalized."],
 widgets=walk("How the proof goes (Solution.lean lines 25–33 and AltCounter/Final.lean lines 40–51)", [
    {"text": "Solution.lean forwards to the library theorem.", "lean": "AltCounter.false_of_charTwo_banach_contDiff_omega h"},
    {"text": "Get the field K (Final.lean line 48).", "link": "AltCounter.exists_field"},
    {"text": "The hypothesis needs CompleteSpace (F K); the instance on Final.lean lines 20–22 supplies it.", "link": "AltCounter.F"},
    {"text": "Contradict h at K, E = ℓ^∞(K), F = F K (Final.lean lines 50–51).", "link": "AltCounter.not_contDiff_omega_Q_of_NSC"}]))


node("AltCounter.exists_field",
 "Headline: a field where the counterexample runs",
 "There really is a complete, non-archimedean field of characteristic 2 that is not spherically complete: the completion of the 2-power Puiseux series over 𝔽₂, built by hand. Without it the main theorem would be conditional on a field that might not exist.",
 r"""## Plain English

**Theorem (`exists_field`, AltCounter/Final.lean lines 12–18).** There is a type K with a nontrivially normed field
structure such that

- K is **ultrametric**: ‖x + y‖ ≤ max(‖x‖, ‖y‖) (`IsUltrametricDist`);
- K is **complete** (`CompleteSpace`);
- K has **characteristic 2** (`CharP K 2`): 1 + 1 = 0;
- K is **not spherically complete**, in the concrete form [HasEmptyNestedBalls](#/node/AltCounter.HasEmptyNestedBalls):
  there is a decreasing sequence of closed balls with strictly decreasing radii and nothing in all of them.

**Why each property is needed.** Ultrametricity drives every estimate (sums are no bigger than their largest term).
Characteristic 2 makes the determinant identity of the [finite lemma](#/node/AltCounter.exists_block_point) work.
Non-spherical completeness gives the [tail property](#/node/AltCounter.TailProperty), via
[NSC](#/node/AltCounter.NSC). Completeness is needed for the tail lemma's proof and for the Banach headline.

**How it is built.**

1. [Puiseux.isGoodModel](#/node/AltCounter.Puiseux.isGoodModel): the field L of 2-power Puiseux series over 𝔽₂ (series
   in t^{1/2^j} for some j), with |f| = 2^(−order f), has a nested sequence of balls with radii ≥ 1/2 and empty
   intersection. It is not complete.
2. [exists_field_of_goodModel](#/node/AltCounter.exists_field_of_goodModel): pass to the completion. All the
   properties survive, and the lower bound 1/2 on the radii is what keeps the intersection empty in the completion.

The original notes (paper/COUNTEREXAMPLE.md) use the completed algebraic closure of 𝔽₂((t)) and cite van der Put's
theorem instead; the Lean takes this more explicit route and proves the needed direction itself.
""",
 [q("Which property of K is NOT claimed by exists_field?",
    ["Complete", "Characteristic 2", "Spherically complete", "Ultrametric"], 2,
    "It claims the opposite: HasEmptyNestedBalls K, i.e. K is not spherically complete (AltCounter/Final.lean lines 15–16)."),
   q("What is the field built from?",
    ["The real numbers", "The 2-adic numbers ℚ₂", "2-power Puiseux series over 𝔽₂, then completed", "An ultrapower"], 2,
    "exists_goodModel (AltCounter/Puiseux.lean lines 363–364) and exists_field_of_goodModel (AltCounter/Model.lean lines 103–113)."),
   q("Why does it matter that this theorem is proved rather than assumed?",
    ["It doesn't matter", "Without it the main theorem would only say 'if such a field exists, then …'",
     "It makes the proof faster"], 1,
    "not_analyticAt_Q assumes the tail property; exists_field is what discharges that assumption for a real field.")],
 caveats=["'Not spherically complete' is stated in a concrete form (one nested sequence of balls with empty intersection), not as the negation of a Mathlib predicate. That is the usual meaning, and it is all the proof needs."],
 widgets=walk("How the proof goes (AltCounter/Final.lean lines 14–18)", [
    {"text": "Get a non-complete 'good model' field L with absolute value v: the 2-power Puiseux series.", "link": "AltCounter.Puiseux.isGoodModel",
     "lean": "obtain ⟨L, _, v, hv⟩ := exists_goodModel"},
    {"text": "Complete it; the completion keeps every property, including the empty nested balls.", "link": "AltCounter.exists_field_of_goodModel",
     "lean": "exact exists_field_of_goodModel v hv"}]))
