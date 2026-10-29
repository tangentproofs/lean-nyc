NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]

NATIVE = ("The SymCC proof tree imports Cedar/Thm/SymCC/Data/Ext.lean, which uses `native_decide` 8 times for small "
          "Int64 arithmetic facts (lines 36–110), and Cedar/Data/Int64.lean uses it twice (lines 101 and 106). "
          "`native_decide` trusts Lean's compiler as well as its kernel. We did not trace whether this particular "
          "theorem's proof reaches those lemmas.")


node("SymCC.compile",
 "SymCC: compiling a Cedar expression to an SMT term",
 "Cedar's symbolic compiler turns a policy expression into a single SMT term over unknowns that stand for the request and entity data. One term then represents the expression's result for every possible input at once.",
 r"""## Plain English

**SymCC** ("symbolic compiler", Cedar/SymCC/) lets Cedar answer questions such as "do these two policy sets ever
disagree?" with an SMT solver (CVC5) instead of by testing.

- A **symbolic environment** `εnv : SymEnv` describes requests and entity stores with *unknowns* (term variables
  and uninterpreted functions) in place of concrete data.
- **`compile x εnv`** (Cedar/SymCC/Compiler.lean lines 255–286) walks the expression and builds a `Term` of type
  "option of τ": `none` means "evaluation errors", `some v` the value. Each expression form has a helper
  (`compileIf`, `compileAnd`, `compileGetAttr`, …).
- An **interpretation** `I` assigns concrete values to the unknowns. `env ∈ᵢ εnv`
  (Cedar/Thm/SymCC/Data/Basic.lean lines 784–787) says some well-formed interpretation turns `εnv` into the concrete
  environment `env`. `o ∈ₒ t` (lines 779–782) says some interpretation turns term `t` into the concrete outcome `o`.
- The **encoder** (Cedar/SymCC/Encoder.lean) prints terms as SMT-LIB text for the solver; the **decoder**
  (Cedar/SymCC/Decoder.lean) parses the solver's model back. These two are *not* covered by the soundness proofs
  (they are string-processing code), and five of the twelve ETNA bugs live there; see
  [the encoder/decoder properties](#/node/Etna.property_define_entity_rejects_non_member).

The docstring (Cedar/SymCC/Compiler.lean lines 250–254) states the intended contract, proved as
`compile_well_typed` (Cedar/Thm/SymbolicCompilation.lean lines 208–221): on a well-typed expression in a well-formed
environment, compilation succeeds and yields a well-formed term of the matching type.
""",
 [q("What does a `none` in the compiled option-typed term stand for?", ["An evaluation error", "A false policy", "An unknown attribute"], 0,
    "The compiler produces an `.option τ` term; errors map to none (Cedar/SymCC/Compiler.lean lines 250–254)."),
  q("Are the SMT-LIB encoder and decoder covered by the soundness theorems?", ["No, the theorems stop at Terms", "Yes"], 0,
    "`compile_is_sound` is about `compile`, a Term-level function; the encoder is separate text-producing code."),
  q("What does `env ∈ᵢ εnv` mean?", ["Some well-formed interpretation of εnv's unknowns gives env", "env is a subset of εnv"], 0,
    "Cedar/Thm/SymCC/Data/Basic.lean lines 784–787."),
 ])


node("Thm.compile_is_sound",
 "Headline: symbolic compilation is sound",
 "Whatever concrete input you pick from the set a symbolic environment describes, the real evaluator's result is one of the outcomes the compiled SMT term allows. The compiler never misses a behaviour.",
 r"""## Plain English

**Theorem (`compile_is_sound`, Cedar/Thm/SymbolicCompilation.lean lines 71–85).** Let `x` be an expression, `env` a
concrete environment (request + entities) and `εnv` a symbolic one. Assume
1. `εnv` is well-formed for `x` (no dangling entity types or references, valid types);
2. `env` is well-formed for `x` (no dangling entity references);
3. `env ∈ᵢ εnv`, i.e. `env` is one of the environments `εnv` represents;
4. `compile x εnv = .ok t`.

Then there is an outcome `o` with `o ∈ₒ t` (the term can produce it) and
`evaluate x env.request env.entities ∼ o` (the real evaluator's result matches it).

The outcome only records "value v" or "some error": per the docstring (lines 64–69), the symbolic compiler doesn't
distinguish error kinds.

The converse is [compile_is_complete](#/node/Thm.compile_is_complete): every outcome the term allows is produced by
some well-formed concrete input. Together they say the term is an **exact** description. The README calls them
"sound and complete symbolic compilation", which matches.

**Status.** Complete proof in the source (it rests on `compile_bisimulation`, Cedar/Thm/SymCC/Compiler.lean
lines 161–172, and about 39,000 lines under Cedar/Thm/SymCC/). Upstream Cedar result. Not built.
""",
 [q("Does soundness say which kind of error the evaluator raises?", ["No, only whether it errors", "Yes"], 0,
    "Outcomes are `Except Unit α` (Cedar/Thm/SymCC/Data/Basic.lean line 217); see the docstring at Cedar/Thm/SymbolicCompilation.lean lines 64–69."),
  q("Which direction is 'soundness' here?", ["Every real behaviour is allowed by the term", "Every behaviour the term allows is real"], 0,
    "The second is `compile_is_complete` (Cedar/Thm/SymbolicCompilation.lean lines 99–106)."),
  q("Is the SMT-LIB text sent to CVC5 covered?", ["No, the theorem is about the Term, before encoding", "Yes"], 0,
    "The conclusion mentions `t`, the compiled Term (Cedar/Thm/SymbolicCompilation.lean lines 75–78)."),
  q("What must hold of the concrete environment?", ["It is well-formed for x and represented by εnv", "Nothing"], 0,
    "Hypotheses at Cedar/Thm/SymbolicCompilation.lean lines 73–74."),
 ],
 caveats=["Upstream Cedar result. Not built for this site.", NATIVE,
          "Stops at the Term level: the SMT-LIB encoder, the solver (CVC5) and the model decoder are trusted, not verified. ETNA's SymCC variants are bugs in exactly that unverified layer."],
 widgets=walk("How the proof goes (Cedar/Thm/SymbolicCompilation.lean, lines 71-85)", [
  {"text": "Introduce the four hypotheses.", "lean": "intros h₁ h₂ h₃ h₄"},
  {"text": "Unpack `env ∈ᵢ εnv` into a well-formed interpretation I with env ∼ εnv.interpret I.",
   "lean": "replace ⟨I, h₃, h₅⟩ := h₃"},
  {"text": "The bisimulation lemma: evaluating x on env matches interpreting the compiled term under I. Convert that to an outcome o.",
   "lean": "have ⟨o, h₆, h₇⟩ := same_results_implies_exists_outcome (compile_bisimulation h₁ h₂ h₃ h₅ h₄)",
   "link": "SymCC.compile"},
  {"text": "Offer o as the witness; the evaluator part is immediate…", "lean": "exists o"},
  {"text": "…and `o ∈ₒ t` is witnessed by the same interpretation I.", "lean": "exists I"},
 ]))


node("Thm.compile_is_complete",
 "Symbolic compilation is complete",
 "Every outcome the compiled term allows is the real result for some well-formed concrete input. So an SMT counterexample is never spurious.",
 r"""## Plain English

**Theorem (Cedar/Thm/SymbolicCompilation.lean lines 99–118).** If `εnv` is well-formed for `x`, `compile x εnv = .ok t`
and `o ∈ₒ t`, then there is a concrete environment `env` that is well-formed for `x`, satisfies `env ∈ᵢ εnv`, and on
which evaluation gives `o`.

**Proof idea.** From the interpretation I that produces o, build a concrete environment with `exists_wf_env`
(line 110), then use the same bisimulation as [soundness](#/node/Thm.compile_is_sound) and the fact that equal
"sameness" outcomes are equal (lines 115–118).

`isAuthorized_is_sound` and `isAuthorized_is_complete` (lines 155–200) lift both directions from one expression to
the authorization decision of a whole policy set; see [isAuthorized_is_sound](#/node/Thm.isAuthorized_is_sound).
""",
 [q("What does completeness rule out?", ["Spurious counterexamples from the solver", "Missed counterexamples"], 0,
    "Every symbolic outcome is realised by a real input (Cedar/Thm/SymbolicCompilation.lean lines 103–106)."),
  q("Does completeness need a concrete environment as a hypothesis?", ["No, it constructs one", "Yes"], 0,
    "The conclusion is `∃ env, …` (Cedar/Thm/SymbolicCompilation.lean line 103)."),
  q("Which lemma constructs the concrete environment?", ["exists_wf_env", "compile_bisimulation"], 0, "Cedar/Thm/SymbolicCompilation.lean line 110."),
 ])


node("Thm.isAuthorized_is_sound",
 "Symbolic authorization is sound (and complete)",
 "Compiling a whole policy set gives a boolean term whose possible values are exactly the decisions the concrete authorizer makes on the represented inputs.",
 r"""## Plain English

**Theorem (Cedar/Thm/SymbolicCompilation.lean lines 155–169).** With well-formedness hypotheses for the policies,
`env ∈ᵢ εnv` and `SymCC.isAuthorized ps εnv = .ok t`: the concrete decision `Spec.isAuthorized env.request env.entities ps`
is among the decisions `t` allows. `isAuthorized_is_complete` (lines 183–200) is the converse.

Only the **decision** (allow/deny) is modelled, not the determining or erroring policy sets (docstring
lines 148–153).

Both rest on `isAuthorized_bisimulation` (Cedar/Thm/SymCC/Authorizer.lean). They are the building blocks of the
verification queries, e.g. [verifyEquivalent_is_sound](#/node/Thm.verifyEquivalent_is_sound).
""",
 [q("Does the symbolic authorizer model the list of determining policies?", ["No, only the decision", "Yes"], 0,
    "Cedar/Thm/SymbolicCompilation.lean lines 148–153."),
  q("isAuthorized_is_complete says every decision the term allows is…", ["made by the concrete authorizer on some well-formed input", "allow"], 0,
    "Cedar/Thm/SymbolicCompilation.lean lines 183–190."),
  q("Which theorem is the per-expression analogue?", ["compile_is_sound", "validation_is_sound"], 0, "See [compile_is_sound](#/node/Thm.compile_is_sound)."),
 ],
 caveats=[NATIVE])


node("SymCC.verifyEquivalent",
 "Verification queries: asking the solver about policies",
 "A verification query compiles the policies and asserts the negation of the property you want. If the solver says 'unsatisfiable', no counterexample exists and the property holds.",
 r"""## Plain English

Cedar/SymCC/Verifier.lean defines the analyses Cedar users can run, all built from the same pattern:

- `verifyIsAuthorized φ ps₁ ps₂ εnv` (lines 67–71): compile both policy sets to boolean terms t₁ and t₂ with the
  symbolic authorizer, add the well-formedness constraints `enforce …`, and add `not (φ t₁ t₂)`.
- **`verifyEquivalent ps₁ ps₂ εnv`** (lines 181–182) is `verifyIsAuthorized eq`: "is there an input where the two
  policy sets decide differently?"
- Others: `verifyImplies`, `verifyDisjoint`, `verifyAlwaysAllows`, `verifyAlwaysDenies` (policy sets), and
  `verifyNeverErrors`, `verifyAlwaysMatches`, `verifyNeverMatches`, `verifyMatchesEquivalent/Implies/Disjoint` (single
  policies, via `verifyEvaluate` lines 43–46 and `verifyEvaluatePair` lines 54–59).

The result is a list of terms, `Asserts` (line 36). `εnv ⊭ asserts` (Cedar/Thm/SymCC/Data/Basic.lean lines 760–767)
means no well-formed interpretation makes all of them true.

In practice the asserts are encoded to SMT-LIB and sent to CVC5. ETNA's
[pipeline property](#/node/Etna.property_symcc_pipeline_soundness) runs exactly that path with `verifyAlwaysMatches`.
""",
 [q("What does an 'unsatisfiable' answer mean for verifyEquivalent?", ["The two policy sets agree on every represented input", "They disagree somewhere"], 0,
    "The asserts include `not (eq t₁ t₂)` (Cedar/SymCC/Verifier.lean lines 67–71, 181–182)."),
  q("What is `Asserts`?", ["A list of SMT terms", "A Lean proposition"], 0, "Cedar/SymCC/Verifier.lean line 36."),
  q("Is 'unsatisfiable' here about SMT-LIB text?", ["No, about Lean terms under Lean interpretations", "Yes"], 0,
    "`Asserts.Unsatisfiable` quantifies over `Interpretation`s (Cedar/Thm/SymCC/Data/Basic.lean lines 760–764)."),
 ])


node("Thm.verifyEquivalent_is_sound",
 "Headline: the equivalence check is sound",
 "If the equivalence query is unsatisfiable, two policy sets give the same allow/deny decision on every strongly well-formed input the symbolic environment describes.",
 r"""## Plain English

**Theorem (`verifyEquivalent_is_sound`, Cedar/Thm/Verification.lean lines 448–461).** Assume `εnv` is *strongly*
well-formed for both policy sets, `verifyEquivalent ps₁ ps₂ εnv = .ok asserts`, and `εnv ⊭ asserts`. Then for every
concrete `env ∈ᵢ εnv` that is strongly well-formed for both sets, `bothAllowOrBothDeny` holds: the two
`Spec.isAuthorized` responses have the same decision (Cedar/Thm/SymCC/Verifier/VerifyIsAuthorizedQueries.lean
lines 27–28).

"**Strongly** well-formed" (docstring, Cedar/Thm/Verification.lean lines 29–32) adds that the entity hierarchy is the
transitive closure of a DAG, which real entity stores are expected to be.

`verifyEquivalent_is_complete` (lines 471–486) is the converse: if the asserts are satisfiable, there is a concrete
strongly well-formed input where the decisions differ. So a counterexample from a correct solver is real.

This is the theorem behind Cedar's "policy change analysis": refactor a policy set and prove nothing changed.

**What is trusted.** `⊭` is a mathematical statement about Lean terms. In practice it is established by encoding to
SMT-LIB, running CVC5 and believing its "unsat". The encoder and the solver are outside the proof. A bug there (like the
string-quoting bug of ETNA variant 4, PR #640) could make the tool give a wrong answer without contradicting this
theorem.

**Status.** Complete proof in the source; upstream Cedar result. Not built.
""",
 [q("What does the theorem conclude?", ["Same decision on every strongly well-formed represented input", "Same response including diagnostics", "The solver is correct"], 0,
    "`bothAllowOrBothDeny` compares `.decision` only (Cedar/Thm/SymCC/Verifier/VerifyIsAuthorizedQueries.lean lines 27–28)."),
  q("Does the theorem cover the SMT-LIB encoder and CVC5?", ["No, `⊭` is a Lean-level statement", "Yes"], 0,
    "`Asserts.Unsatisfiable` is defined over Lean interpretations (Cedar/Thm/SymCC/Data/Basic.lean lines 760–764)."),
  q("What extra condition does 'strongly' well-formed add?", ["The ancestor relation is the transitive closure of a DAG", "All attributes are present"], 0,
    "Cedar/Thm/Verification.lean lines 29–32."),
  q("Which theorem says counterexamples are real?", ["verifyEquivalent_is_complete", "compile_is_sound"], 0,
    "Cedar/Thm/Verification.lean lines 471–486."),
 ],
 caveats=["Upstream Cedar result. Not built for this site.", NATIVE,
          "The bridge from `εnv ⊭ asserts` to an actual solver run (encoder, CVC5, decoder) is not verified."],
 widgets=walk("How the proof goes (Cedar/Thm/Verification.lean, lines 448-461)", [
  {"text": "Take the hypotheses: strong well-formedness of εnv for both policy sets, the query result, and its unsatisfiability.",
   "lean": "verifyEquivalent ps₁ ps₂ εnv = .ok asserts →"},
  {"text": "The proof is one line: the generic soundness theorem for `verifyIsAuthorized` queries, applied with the fact that `eq` on terms matches `bothAllowOrBothDeny` on responses (a 'well-behaved' query).",
   "lean": "exact verifyIsAuthorized_is_sound verifyEquivalent_wbaq", "link": "Thm.verifyIsAuthorized_is_sound"},
  {"text": "All the work is in the generic theorem: see its own walkthrough (Cedar/Thm/SymCC/Verifier/VerifyIsAuthorized.lean lines 99–132).",
   "link": "Thm.verifyIsAuthorized_is_sound"},
 ]))


node("Thm.bothAllowOrBothDeny",
 "Same decision",
 "Two authorization responses agree when their decisions are equal. The determining and erroring policy sets are ignored.",
 r"""## Plain English

**Definition (Cedar/Thm/SymCC/Verifier/VerifyIsAuthorizedQueries.lean lines 27–28).** `bothAllowOrBothDeny r₁ r₂` is
the Boolean test `r₁.decision = r₂.decision`.

It is the conclusion of [verifyEquivalent_is_sound](#/node/Thm.verifyEquivalent_is_sound). Two policy sets proved
"equivalent" this way may still report different determining policies for the same request.
""",
 [q("Does `bothAllowOrBothDeny` compare determining policies?", ["No, only decisions", "Yes"], 0,
    "Cedar/Thm/SymCC/Verifier/VerifyIsAuthorizedQueries.lean lines 27–28."),
  q("Two responses, both deny, with different forbid policies as reasons. Are they 'both deny'?", ["Yes", "No"], 0,
    "Only `.decision` is compared."),
  q("Is it a Prop or a Bool?", ["A Bool", "A Prop"], 0, "Its type is `Bool` (line 27)."),
 ])


node("Thm.verifyIsAuthorized_is_sound",
 "Key lemma: generic soundness of policy-set queries",
 "For any query formula that faithfully mirrors a Boolean comparison of responses, unsatisfiability of the query means the comparison holds on every strongly well-formed represented input. All five policy-set verification theorems are instances.",
 r"""## Plain English

**Theorem (Cedar/Thm/SymCC/Verifier/VerifyIsAuthorized.lean lines 99–132).** Given a *well-behaved* pair (φ, f)
(`WellBehavedIsAuthorizedQuery`, lines 33–53: φ maps well-formed boolean terms to a well-formed boolean term,
commutes with interpretation, and mirrors f on concrete responses), if `verifyIsAuthorized φ ps₁ ps₂ εnv` is
unsatisfiable then `f (isAuthorized … ps₁) (isAuthorized … ps₂) = true` on every strongly well-formed `env ∈ᵢ εnv`.

`verifyEquivalent_wbaq` (Cedar/Thm/SymCC/Verifier/VerifyIsAuthorizedQueries.lean lines 30 onward) shows that
(`eq`, [bothAllowOrBothDeny](#/node/Thm.bothAllowOrBothDeny)) is well-behaved, which gives
[verifyEquivalent_is_sound](#/node/Thm.verifyEquivalent_is_sound).
""",
 [q("What must a query be for this theorem to apply?", ["Well-behaved: its term formula mirrors a Boolean comparison of responses", "Any formula"], 0,
    "Hypothesis `WellBehavedIsAuthorizedQuery φ f` (Cedar/Thm/SymCC/Verifier/VerifyIsAuthorized.lean line 100)."),
  q("Which assert must be the false one, in the proof?", ["The final `not (φ t₁ t₂)`", "One of the well-formedness constraints"], 0,
    "The `enforce` constraints hold for a strongly well-formed env (lines 116–119)."),
  q("Which bisimulation does it use?", ["isAuthorized_bisimulation", "compile_bisimulation directly"], 0, "Lines 124 and 127."),
 ],
 widgets=walk("How the proof goes (Cedar/Thm/SymCC/Verifier/VerifyIsAuthorized.lean, lines 99-132)", [
  {"text": "Unsatisfiability, applied to the interpretation I that produces env, gives an assert that is not true under I.",
   "lean": "replace ⟨t, hsat⟩ := hsat I hwI"},
  {"text": "The well-formedness constraints (`enforce …`) are all true under I for a strongly well-formed env, so the false assert must be the last one, `not (φ t₁ t₂)`.",
   "lean": "replace ha := asserts_last_not_true ha hsat.left hsat.right"},
  {"text": "Symbolic authorization of each policy set matches concrete authorization (bisimulation).",
   "lean": "have hrb₁ := isAuthorized_bisimulation hwε₁ hwe₁ hwI heq hok₁", "link": "Thm.isAuthorized_is_sound"},
  {"text": "So `φ t₁ t₂` being true under I means the concrete responses satisfy f.",
   "lean": "exact same_bool_not_not_true_implies_true hrb hsat"},
 ]))


node("Thm.verifyNeverErrors_is_sound",
 "The other verification theorems (grouped)",
 "Each of Cedar's 11 verification queries has a soundness theorem (unsat means the property holds) and a completeness theorem (sat means a real counterexample exists): 26 theorems in Cedar/Thm/Verification.lean, counting two primed variants each for AlwaysMatches and NeverMatches.",
 r"""## Plain English

Cedar/Thm/Verification.lean has 26 theorems, a sound/complete pair for each query (some with a primed variant). They
all follow the [verifyEquivalent](#/node/Thm.verifyEquivalent_is_sound) pattern: each is a one-line application of a
generic theorem (`verifyEvaluate_is_sound`, `verifyEvaluatePair_is_sound`, `verifyIsAuthorized_is_sound` and their
completeness twins) to a proof that the query's formula is "well-behaved".

- **`verifyNeverErrors_is_sound`** (lines 46–55): if unsat, the policy never errors on any strongly well-formed input.
  This is what can close the gap left by [validation soundness](#/node/Thm.validation_is_sound), which still allows
  three error kinds.
- `verifyAlwaysMatches`, `verifyNeverMatches` (lines 84–268): a single policy is always/never satisfied.
- `verifyMatchesEquivalent/Implies/Disjoint` (lines 277–439): relations between two policies' match sets.
- `verifyEquivalent/Disjoint/Implies` (lines 448–579) and `verifyAlwaysDenies/Allows` (lines 588–676): policy sets.

All are upstream Cedar results with complete proofs in the source. The same trust caveat applies: the SMT-LIB encoder,
the solver and the decoder are outside the proofs.
""",
 [q("How many theorems are in Cedar/Thm/Verification.lean?", ["26", "6", "100+"], 0, "Counted at the pinned commit."),
  q("Which query closes the 'three allowed errors' gap for a given policy?", ["verifyNeverErrors", "verifyAlwaysMatches"], 0,
    "Cedar/Thm/Verification.lean lines 46–55."),
  q("How are most of these theorems proved?", ["One-line applications of a generic theorem", "Each by a long induction"], 0,
    "e.g. `exact verifyEvaluate_is_sound verifyNeverErrors_wbeq` (Cedar/Thm/Verification.lean line 55)."),
 ],
 caveats=[NATIVE])


node("Thm.isAuthorized_eq_for_sound_policy_slice",
 "Also in the repository: policy slicing and partial evaluation (grouped)",
 "Two more families of upstream Cedar theorems: dropping irrelevant policies (a sound slice) doesn't change the response, and type-aware partial evaluation (TPE) agrees with full authorization once the missing data arrives.",
 r"""## Plain English

Not headlined on this site, but proved in the same repository (all upstream Cedar):

**Policy slicing** (Cedar/Thm/PolicySlice.lean).
- `isAuthorized_eq_for_sound_policy_slice` (lines 47–55): if `slice` is a *sound slice* of `policies` for this
  request (it keeps every policy that could be satisfied or error), authorizing with the slice gives the same response.
- `sound_bound_analysis_produces_sound_slices` (lines 60–85) and `isAuthorized_eq_for_scope_based_policy_slice`
  (lines 139–145): slicing by the principal/resource bounds in policy scopes is sound.

The upstream README points to `Cedar/Thm/Slicing.lean`; at the pinned commit the file is Cedar/Thm/PolicySlice.lean.

**Type-aware partial evaluation, TPE** (Cedar/Thm/TPE.lean). Authorize with a partial request and partial entities,
get residual policies, then finish later.
- `reauthorize_is_sound` (lines 51–74): re-authorizing the partial response with the full data equals authorizing
  from scratch.
- `partial_authorize_decision_is_sound` (lines 79–98): if partial authorization already returns a decision, full
  authorization reaches the same one. Further theorems (lines 102–281) cover the determining and erroring policies.
- These need `isValidAndConsistent` (the concrete data extends the partial data and validates).

About 5,600 lines of TPE proofs sit under Cedar/Thm/TPE/.
""",
 [q("A sound policy slice gives…", ["the same full response", "the same decision but maybe different diagnostics"], 0,
    "Equality of `isAuthorized` results (Cedar/Thm/PolicySlice.lean lines 47–49)."),
  q("If partial evaluation already decides 'deny', full authorization…", ["also decides deny (given consistent, valid data)", "may decide allow"], 0,
    "`partial_authorize_decision_is_sound` (Cedar/Thm/TPE.lean lines 79–91)."),
  q("What file does the README call Slicing.lean?", ["Cedar/Thm/PolicySlice.lean", "Cedar/Spec/Slice.lean"], 0,
    "README section 'Sound policy slicing'; the file at the pinned commit is PolicySlice.lean."),
 ])
