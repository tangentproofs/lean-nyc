NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

ETNA_NOT_PROOF = ("ETNA code is executable test code, not theorems: it proves nothing, and it was not run for this site.")


node("Etna.PropertyResult",
 "What ETNA adds: properties that pass, fail or discard",
 "The fork's own contribution is a testing harness, not proofs. Each ETNA property is an ordinary Lean function that runs Cedar code on an input and returns pass, fail (with a message) or discard (input not applicable).",
 r"""## Plain English

**ETNA** is a benchmark framework for property-based testing (PBT) tools: a *workload* is a program plus a set of
historical bugs, each re-introducible by a patch, plus properties that should catch them. This repository,
alpaylan/cedar-etna by Alperen Keleş, turns Cedar's Lean specification into such a workload.

What it adds on top of upstream Cedar (all under cedar-lean/Cedar/Etna/, cedar-lean/EtnaCedar/ and the repository
root):
- **patches/** (12 files): each patch goes *buggy → fixed*. Reverse-applying it (`git apply -R`) re-inserts one
  historical cedar-spec bug.
- **etna.toml**: the manifest listing, per variant, the source PR, the invariant, how it is triggered, the property
  and the witness.
- **Properties.lean**: the `property_*` functions;
  **Witnesses.lean**: fixed inputs that trigger each bug;
  **Generators.lean** and **TypeDirectedGen.lean**: random input generators for the Plausible PBT library;
  **EtnaCedar/Main.lean**: the command-line runner.

**Definition (`PropertyResult`, Cedar/Etna/Property.lean lines 15–19).** Three outcomes: `pass`, `fail msg` and
`discard` (the input doesn't meet the property's preconditions). `toBool` (lines 21–23) counts both pass and
discard as success. `emitJson` (lines 57–60) prints the one-line JSON record the ETNA tooling reads.

A property is meant to be "pure, total, owned-input" (lines 4–6) and written *black-box*, as a tester would without
knowing which patch is applied (Cedar/Etna/Properties.lean lines 1–16).
""",
 [q("What does `discard` mean?", ["The input doesn't meet the property's preconditions", "The property failed"], 0,
    "`toBool` treats discard like pass (Cedar/Etna/Property.lean lines 21–23)."),
  q("Do ETNA properties prove anything about Cedar?", ["No, they are runtime tests", "Yes, they are theorems"], 0,
    "They return `PropertyResult`, not `Prop` (Cedar/Etna/Property.lean lines 15–19)."),
  q("In which direction do the patches go?", ["buggy → fixed; reverse-applying re-inserts the bug", "fixed → buggy"], 0,
    "README 'Adding a new variant', step 4."),
 ],
 caveats=[ETNA_NOT_PROOF])


node("Etna.property_validator_type_preservation",
 "Testing typechecker soundness at runtime",
 "An executable spot-check of the type-soundness theorem: if the schema is well-formed, the request validates, the expression typechecks and evaluation succeeds, the value must have the promised type. It catches the 'singleton boolean attribute' bug (PR #689).",
 r"""## Plain English

**Property (Cedar/Etna/Properties.lean lines 370–388).** For a random (expression, schema, request, entities):
discard unless `Schema.validateWellFormed` passes, `validateRequest` passes, the schema has an environment for the
request's (principal type, resource type, action), the expression typechecks in it, and evaluation returns `.ok v`.
Then pass iff `instanceOfType v (its type) env`.

This is the `.ok v` case of [type_of_is_sound](#/node/Thm.type_of_is_sound), checked on one input. Note it
deliberately does **not** require `validateEntities` (docstring lines 363–368), so it tests the typechecker against
entity data that may not conform. That is a different statement from the theorem, which assumes conforming entities.

**The bug it targets (variant 7, cedar-spec PR #689).** The patch for this variant
(patches/schema_well_formed_no_singleton_bools_e785e2e_1.patch) removes one line from
`StandardSchemaEntry.validateWellFormed`: the `validateLifted` check. Cedar's type system has *singleton* boolean types
(`true`, `false`) used internally. Without the check, a schema may declare `User.flag : true`; the typechecker then
promises `principal.flag : true`, while the entity data says `false`. The witness
(`witness_schema_well_formed_no_singleton_bools_case_attr_bool_tt`, Cedar/Etna/Witnesses.lean lines 199–204) is
exactly that.

**Why the proofs care.** With the line removed, the upstream proof of
[schema conformance](#/node/Thm.request_and_entities_validate_implies_instance_of_wf_schema) and so of
[validation soundness](#/node/Thm.validation_is_sound) should no longer go through. The README says ETNA builds only
the `etna_cedar` executable and not the proofs (`lake build etna_cedar`, not `lake build Cedar`) for exactly this
reason.
""",
 [q("When does this property discard?", ["When any precondition fails, including evaluation erroring", "Never"], 0,
    "Cedar/Etna/Properties.lean lines 372–386."),
  q("Does it require the entities to validate against the schema?", ["No, on purpose", "Yes"], 0,
    "Docstring, Cedar/Etna/Properties.lean lines 363–368."),
  q("What does the variant-7 patch remove?", ["The `validateLifted` check on entity attribute types", "The whole typechecker"], 0,
    "One deleted line in Cedar/Validation/EnvironmentValidator.lean (see the patch file)."),
 ],
 caveats=[ETNA_NOT_PROOF,
          "Our claim that removing `validateLifted` breaks the upstream proofs comes from the etna.toml summary and the README, not from building."])


node("Etna.property_symcc_pipeline_soundness",
 "Testing the unverified SymCC tail: encoder → CVC5 → decoder",
 "This property runs the part of Cedar's verifier that the proofs don't cover: encode the query as SMT-LIB, run CVC5, decode the model. A malformed script or an undecodable model is a failure. It needs a CVC5 binary; without one it discards.",
 r"""## Plain English

**Property (Cedar/Etna/Properties.lean lines 431–472).** Given a type environment and a policy body, build
`permit when { body }` (lines 422–429) and:
1. compute `verifyAlwaysMatches` asserts (line 442) (see [verification queries](#/node/SymCC.verifyEquivalent));
2. encode them to SMT-LIB and send them to CVC5 (lines 446–449);
3. if CVC5 answers `sat`, fetch the model and run `Decoder.decode` on it (lines 450–451, 466–469).

It **fails** if CVC5 rejects the script (the encoder produced malformed SMT-LIB) or the decoder rejects CVC5's model.
It **discards** if the `CVC5` environment variable is unset (lines 432–433) or the query can't be built.

This targets the gap left by [compile_is_sound](#/node/Thm.compile_is_sound) and
[verifyEquivalent_is_sound](#/node/Thm.verifyEquivalent_is_sound): those are about Lean terms, while the real tool also
needs the text encoder and decoder. Three historical bugs live there:
- **variant 4 (PR #640)**: string literals containing `"` were not escaped as `""`;
- **variant 10 (PR #752)**: an empty record was emitted as the illegal `(R0 )`;
- **variant 11 (PR #721)**: the decoder rejected the bare symbol `R0` for an empty record.

Random inputs come from `TypeDirected.genJointInputs` (Cedar/Etna/TypeDirectedGen.lean lines 381–384), which generates
well-typed expressions by target type rather than at random, to avoid discarding almost everything.

The two fixed witnesses (Cedar/Etna/Witnesses.lean lines 275–291) are `principal.name == "x\"y"` and `context == {}`.
""",
 [q("Without a CVC5 binary this property returns…", ["discard", "fail", "pass after skipping the solver"], 0,
    "Cedar/Etna/Properties.lean lines 432–433."),
  q("Which query does it encode?", ["verifyAlwaysMatches", "verifyEquivalent", "verifyNeverErrors"], 0,
    "Line 442; the comment at lines 436–441 explains why: never-errors asserts can constant-fold away the literals."),
  q("Why does this layer need testing even though SymCC is proved sound?", ["The proofs stop at Lean terms; the SMT-LIB text encoder and decoder are unverified", "The proofs have sorry"], 0,
    "Compare Cedar/Thm/SymbolicCompilation.lean lines 71–78 with Cedar/SymCC/Encoder.lean."),
 ],
 caveats=[ETNA_NOT_PROOF,
          "The `etna` runner maps `discard` to 'passed' (EtnaCedar/Main.lean lines 237–238). Variants 4 and 10 are wired to this CVC5-backed witness (lines 198–214), so without CVC5 they report 'passed' even with the bug inserted. The repository's scripts don't set CVC5, as far as we can see; the external ETNA CI may."])


node("Etna.property_evaluator_extension_consistency",
 "Parser bugs: decimal and duration literals (variants 1, 2, 12)",
 "Three historical bugs are in Cedar's extension-value parsers: `decimal(\"-0.5\")` lost its sign, `decimal(\"1_2.34\")` was accepted, and the smallest 64-bit duration failed to parse. The properties check that evaluating the parser call returns the expected value.",
 r"""## Plain English

The Lean spec has no policy-text parser. These bugs are in the parsers that run when a policy calls `decimal("…")` or
`duration("…")`.

**`property_evaluator_extension_consistency e s`** (Cedar/Etna/Properties.lean lines 86–95): evaluate the expression
"call the extension constructor for e's type on the string s" and require `.ok (.ext e)`.

- **Variant 1 (PR #799)**: `property_decimal_parse_negative_sign_preserved` (lines 99–104) renders a random 64-bit
  decimal with `toString` and parses it back. The bug took the sign from the integer part, and "-0" parses to 0, so
  `-0.0001` came back positive. Witness: n = −1 (Cedar/Etna/Witnesses.lean lines 58–59).
- **Variant 12 (PR #577)**: `property_duration_parse_min_value` (lines 109–114) does the same for durations `"{n}ms"`.
  The bug parsed the magnitude first, and 9223372036854775808 doesn't fit in Int64. Witness: n = −2⁶³
  (Witnesses.lean lines 246–247).
- **Variant 2 (PR #877)**: `property_decimal_parse_no_underscore` (lines 122–133): if `decimal(s)` succeeds, s
  contains only `-`, `.` and digits. Lean's `String.toInt?` accepts `_` as a digit separator, which leaked into
  Cedar. Witness: `"1_2.34"` (Witnesses.lean lines 64–65).

Variant 2's property is weaker than the grammar it cites (`[-]?[0-9]+\.[0-9]+`, line 118): it only checks the
character set, so it would not catch, say, `"1.2.3"` being accepted.
""",
 [q("Does the Lean spec contain a parser for Cedar policy text?", ["No; these are extension-function parsers", "Yes"], 0,
    "Cedar/Etna/Properties.lean lines 42–45."),
  q("Why did \"-0.5\" lose its sign in the buggy version?", ["The sign was taken from the parsed integer part, and -0 = 0", "Underscores"], 0,
    "etna.toml, variant 1 summary; witness at Cedar/Etna/Witnesses.lean lines 54–59."),
  q("Would the underscore property catch an accepted \"1.2.3\"?", ["No, it only checks the character set", "Yes"], 0,
    "Cedar/Etna/Properties.lean lines 127–132."),
 ],
 caveats=[ETNA_NOT_PROOF])


node("Etna.property_validate_rejects_undeclared_entities",
 "Validator bugs: properties for variants 3, 5 and 6",
 "Three properties of the form 'if the validator accepts, then a spec rule holds': action entities carry no attributes, every entity literal in a policy is declared, and the request principal's type is declared.",
 r"""## Plain English

All three say "if validation returned `.ok`, a spec invariant holds", and pass when validation errors.

- **`property_validate_action_entity_no_attrs`** (Cedar/Etna/Properties.lean lines 292–303), **variant 3, PR #648**:
  if `validateEntities` accepts, every action entity has empty attributes. This is part of
  [schema conformance](#/node/Thm.InstanceOfWellFormedEnvironment) (Cedar/Thm/Validation/Typechecker/Types.lean
  lines 114–117). Witness: an action entity with `attrs = {x: 1}` (Cedar/Etna/Witnesses.lean lines 45–68).
- **`property_validate_rejects_undeclared_entities`** (lines 313–323), **variant 5, PR #779**: if `validate`
  accepts, `checkEntities` (Cedar/Validation/Validator.lean line 117) also accepts every policy. The bug: the
  typechecker short-circuits `true || …` and never looks at the right side, so `principal == Foo::"x"` with undeclared
  `Foo` slipped through. The fix added `checkEntities` to `typecheckPolicyWithEnvironments`. The property uses that
  same function as its oracle, so this is closer to a regression test than an independent check.
- **`property_validate_request_principal_exists`** (lines 333–338), **variant 6, PR #658**: if `validateRequest`
  accepts, the principal's type is declared in the schema. Witness: `User::"ghost"` against a schema with no `User`
  (Witnesses.lean lines 118–132).

How these relate to [validation_is_sound](#/node/Thm.validation_is_sound): variants 3 and 6 are holes in the executable
checks that the theorem's hypotheses rely on. Variant 5 is subtler. A short-circuited undeclared literal never gets
evaluated (the evaluator short-circuits `||` too, Cedar/Spec/Evaluator.lean lines 112–114), so it doesn't contradict "evaluates to a boolean". The etna.toml summary describes it as a disagreement with
the Rust validator.
""",
 [q("What does variant 5's property use as its oracle?", ["checkEntities, the function the fix introduced", "An SMT solver"], 0,
    "Cedar/Etna/Properties.lean lines 317–320."),
  q("Why did the typechecker miss `Foo` in `true || principal == Foo::\"x\"`?", ["It short-circuits after typing `true` as the singleton type", "Foo was declared"], 0,
    "etna.toml variant 5 summary; Cedar/Etna/Witnesses.lean around lines 78–104."),
  q("When validation fails, these properties…", ["pass", "fail", "discard"], 0,
    "e.g. `| .error _ => .pass` (Cedar/Etna/Properties.lean line 294)."),
 ],
 caveats=[ETNA_NOT_PROOF,
          "Our reading of how each bug relates to the upstream soundness theorem is our own inference, not a statement from the authors."])


node("Etna.property_define_entity_rejects_non_member",
 "SymCC encoder/decoder bugs: properties for variants 4, 8, 10, 11",
 "Narrow properties for the text-level SMT code: balanced quotes in the SMT-LIB output, no illegal empty application `(R0 )`, decoding a bare empty-record symbol, and rejecting enum entities that aren't declared members.",
 r"""## Plain English

These properties run Cedar's SMT-LIB encoder or decoder directly. Unlike the
[CVC5 pipeline property](#/node/Etna.property_symcc_pipeline_soundness), they need no solver.

- **`property_smt_encode_string_balanced_quotes`** (Cedar/Etna/Properties.lean lines 165–169), **variant 4,
  PR #640**: compile and encode an expression into a buffer (`runFullEncode`, lines 144–156) and require an even number
  of `"` characters. SMT-LIB escapes `"` inside strings as `""`.
- **`property_encoder_empty_record_well_formed`** (lines 182–186), **variant 10, PR #752**: the encoded text must not
  contain a line ending in ` ))`. This is a text heuristic that the docstring justifies (lines 171–181).
- **`property_encoder_empty_record_decode_roundtrip`** (lines 275–281), **variant 11, PR #721**: the decoder must
  accept a hand-written model line using a bare record symbol as the value.
- **`property_define_entity_rejects_non_member`** (lines 234–246), **variant 8, PR #855**: with a hand-built
  symbolic environment declaring an enum entity type with given members (lines 214–225), encoding a non-member entity
  must error. The bug used `List.idxOf`, which returns the list length for a missing element, and emitted an
  identifier for a nonexistent member.

Variant 8 is defense in depth: the docstring (lines 188–205) notes the validator already rejects non-member literals,
so it can't be reached through the normal path.

**Wiring.** In the deterministic `etna` mode, variants 4 and 10 now use the CVC5 pipeline witnesses instead of these
narrow ones (EtnaCedar/Main.lean lines 198–214); see [the runner](#/node/EtnaCedar.witnessFor).
""",
 [q("What does the balanced-quotes property count?", ["The number of '\"' characters in the encoded SMT text", "The number of string literals"], 0,
    "Cedar/Etna/Properties.lean lines 166–169."),
  q("Why did the buggy encoder produce a bogus enum identifier?", ["`List.idxOf` returns the list length for a missing element", "Integer overflow"], 0,
    "etna.toml variant 8 summary."),
  q("Do these properties need CVC5?", ["No", "Yes"], 0,
    "They write to a buffer or /dev/null (Cedar/Etna/Properties.lean lines 144–156, 207–210)."),
 ],
 caveats=[ETNA_NOT_PROOF])


node("Etna.property_validate_with_level_accepts",
 "A completeness bug: the level checker was too strict (variant 9)",
 "The one ETNA bug where Cedar rejected something valid: the level checker refused `Action::\"a\" in Action::\"a\"`. No soundness theorem can catch this kind of bug, so it needs a test.",
 r"""## Plain English

**Property (Cedar/Etna/Properties.lean lines 398–403).** Run `validateWithLevel policies schema level`. Fail only if
it returns a `.levelError`; any other result passes.

**The bug (PR #573).** `checkEntityAccessLevel` (Cedar/Validation/Levels.lean line 57 onward) had no case for an
entity *literal* in an entity-access position, so `Action::"a" in Action::"a"` was rejected at level 1. The witness
(Cedar/Etna/Witnesses.lean lines 219–234) is exactly that policy.

**Why it's interesting.** [validate_with_level_is_sound](#/node/Thm.validate_with_level_is_sound) says: *if* the level
checker accepts, slicing is safe. A checker that rejects too much satisfies that trivially. Proving the checker
accepts everything it should would need a completeness theorem, which this repository doesn't have.

The docstring is candid (lines 391–396): this is a unit-test-style property, and random search "has no leverage here"
because a random policy set that fails with a level error is usually genuinely too deep.
""",
 [q("Is this a soundness or a completeness bug?", ["Completeness: valid policies were rejected", "Soundness"], 0,
    "etna.toml variant 9 summary."),
  q("Would it contradict validate_with_level_is_sound?", ["No", "Yes"], 0,
    "Rejecting more only makes the theorem's hypothesis harder to satisfy (Cedar/Thm/Validation.lean line 91)."),
  q("Does the property fail on a type error?", ["No, only on `.levelError`", "Yes"], 0, "Cedar/Etna/Properties.lean lines 399–403."),
 ],
 caveats=[ETNA_NOT_PROOF])


node("EtnaCedar.witnessFor",
 "The ETNA runner: witnesses, random search and JSON output",
 "`lake exe etna_cedar <tool> <Property>` either replays the fixed witness for a property (`etna`) or runs random search with Plausible generators (`plausible`). It always prints one JSON line.",
 r"""## Plain English

**`witnessFor`** (EtnaCedar/Main.lean lines 190–223) maps each of the 12 property names in etna.toml (plus two extra
pipeline names) to its witness from Cedar/Etna/Witnesses.lean. **`runEtna`** (lines 225–242) runs it and reports
`passed` for pass *or discard*, `failed` with the message, or `aborted` on an IO exception.

**`runPlausible`** (lines 248–294) runs random search: up to 1,000,000 trials or about 595 seconds (lines 46–47),
sizes up to 100, using the `Arbitrary` instances in Cedar/Etna/Generators.lean or the type-directed generator for the
SymCC pipeline. It stops at the first failure.

**The contract** (Cedar/Etna/Witnesses.lean lines 5–11): on the base tree every witness passes; with a patch
reverse-applied, its witness fails. scripts/validate_lean_workload.sh checks this by reverse-applying each patch,
building `etna_cedar` and running the witness.

**What this site did not do.** We ran none of this. The README's smoke-test table (12 variants × 10 trials) reports 9
of 12 found by Plausible and 3 needing "co-generation". It predates the most recent commits, which rewrote generators
and rewired witnesses, so it may not describe the pinned commit.

**Small inconsistencies at the pinned commit** (reported, not judged):
- The README still says Plausible mode is wired for only three properties; `runPlausible` wires all twelve.
- Cedar/Etna/Witnesses.lean lines 9–11 mention `#guard` checks "below"; there are none in the file.
- The README's layout section describes a `workloads/Lean/Cedar/.cedar-spec/` checkout, but the repository is the
  cedar-spec fork itself (cedar-lean/ is at the root).
""",
 [q("In `etna` mode, a witness that returns `discard` is reported as…", ["passed", "failed", "aborted"], 0,
    "EtnaCedar/Main.lean lines 237–238."),
  q("What does the validate script expect after reverse-applying a patch?", ["The witness fails", "The proofs still build"], 0,
    "Cedar/Etna/Witnesses.lean lines 5–7; README 'Validate end-to-end'."),
  q("What is the default random-search budget?", ["1,000,000 trials or about 595 s", "200 trials"], 0,
    "EtnaCedar/Main.lean lines 46–47 (the README's '200 trials' is out of date)."),
 ],
 caveats=[ETNA_NOT_PROOF])
