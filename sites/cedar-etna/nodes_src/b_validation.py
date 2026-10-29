NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]


node("Thm.EvaluatesTo",
 "EvaluatesTo: a value, or one of three allowed errors",
 "Validation can't rule out every runtime error. `EvaluatesTo e req es v` says evaluation returns v, or fails with one of exactly three errors: missing entity, extension error, or arithmetic overflow.",
 r"""## Plain English

**Definition (`EvaluatesTo`, Cedar/Thm/Validation/Typechecker/Basic.lean lines 55–59).** Evaluating expression `e`
against the request and entities gives one of:

1. `.error .entityDoesNotExist`, a referenced entity is missing from the store;
2. `.error .extensionError`, e.g. a bad `decimal("…")` string;
3. `.error .arithBoundsError`, 64-bit overflow;
4. `.ok v`.

The docstring (lines 31–54) explains why these three can't be prevented statically: they depend on the entity data
supplied at request time and on arithmetic. The remaining error kinds, *missing attribute* and *type error*, are the
ones the validator promises to rule out.

**`EvaluatesToBool` and `AllEvaluateToBool`** (Cedar/Thm/Validation/Validator.lean lines 33–38) specialise this:
there is some boolean b with `EvaluatesTo expr … b`, and that holds for every policy in a list. See
[AllEvaluateToBool](#/node/Thm.AllEvaluateToBool).
""",
 [q("Which error is NOT allowed by `EvaluatesTo`?", ["A type error", "entityDoesNotExist", "arithBoundsError", "extensionError"], 0,
    "Only the three listed errors are allowed (Cedar/Thm/Validation/Typechecker/Basic.lean lines 55–59)."),
  q("Why can't the validator rule out entityDoesNotExist?", ["It depends on the entity store supplied at request time", "Because of a missing proof"], 0,
    "Docstring, Cedar/Thm/Validation/Typechecker/Basic.lean lines 38–41."),
  q("Is `EvaluatesTo e r es v` a statement about a specific value v?", ["Yes, but it is also true if evaluation returns one of the three errors", "No"], 0,
    "It is a four-way disjunction; in the error cases v is irrelevant."),
 ])


node("Thm.AllEvaluateToBool",
 "AllEvaluateToBool: every policy yields a boolean (or an allowed error)",
 "The conclusion of validator soundness: each policy, as an expression, evaluates to a boolean, or fails only with one of the three runtime errors validation can't prevent.",
 r"""## Plain English

**Definitions (Cedar/Thm/Validation/Validator.lean lines 33–38).**
- `EvaluatesToBool expr req es`: there is a boolean b such that [EvaluatesTo](#/node/Thm.EvaluatesTo) `expr req es b`.
- `AllEvaluateToBool policies req es`: every policy in the list satisfies `EvaluatesToBool` for its expression
  `policy.toExpr`.

So a validated policy set can never produce a "type error" or "attribute does not exist" error at authorization time,
and never returns a non-boolean.

Note what it does **not** promise: that a policy never errors. Missing entities and arithmetic overflow are still
possible. Cedar's SymCC [never-errors check](#/node/Thm.verifyNeverErrors_is_sound) is the tool for proving those
absent for a given policy.
""",
 [q("Can a policy in a validated set still raise arithBoundsError?", ["Yes", "No"], 0,
    "It is one of the allowed errors in `EvaluatesTo` (Cedar/Thm/Validation/Typechecker/Basic.lean line 58)."),
  q("Can a validated policy evaluate to the string \"yes\"?", ["No, a successful result is a boolean", "Yes"], 0,
    "`EvaluatesToBool` asks for `EvaluatesTo … b` with b a Bool (Cedar/Thm/Validation/Validator.lean lines 33–34)."),
  q("`AllEvaluateToBool` quantifies over…", ["every policy in the list", "every request", "every schema"], 0,
    "Cedar/Thm/Validation/Validator.lean lines 37–38. Requests and entities are fixed parameters."),
 ])


node("Thm.InstanceOfWellFormedEnvironment",
 "When a request and entity store conform to a schema",
 "The soundness theorems only promise anything for requests and entities that fit the schema: right entity types, right attribute types, action entities with no attributes, and all declared actions present.",
 r"""## Plain English

A Cedar **schema** declares entity types (with attribute and tag types), actions, and which principal/resource types
each action applies to. The validator splits it into one **type environment** (`TypeEnv`) per
(principal type, action, resource type) combination (`Schema.environments`, Cedar/Validation/Validator.lean line 45).

**Definition (`InstanceOfWellFormedEnvironment`, Cedar/Thm/Validation/Typechecker/Types.lean lines 139–144).**
For an environment `env`:
1. `env` is well-formed;
2. the request is an instance of the environment's request type (lines 79–83): principal and resource have the right
   entity types, the action is the environment's action, and the context record has the declared type;
3. the entity store is an instance of the schema (lines 133–137): every entity has a declared type, its attributes,
   tags and ancestors match the declarations, **action entities have no attributes or tags** (lines 114–120), and every
   declared action is present (lines 126–128).

`InstanceOfWellFormedSchema` (Cedar/Thm/Validation/Validator.lean lines 40–42) says this holds for *some*
environment of the schema.

The concrete, executable checks `validateRequest` and `validateEntities` (Cedar/Validation/RequestEntityValidator.lean
lines 151–166) are proved to establish this; see
[request_and_entities_validate…](#/node/Thm.request_and_entities_validate_implies_instance_of_wf_schema).

**ETNA connection.** Point 3's "action entities have no attributes" is exactly the invariant ETNA's
[validator properties](#/node/Etna.property_validate_rejects_undeclared_entities) test at runtime
(variant `validator_action_entity_no_attrs`, cedar-spec PR #648).
""",
 [q("May an action entity carry attributes in a conforming entity store?", ["No", "Yes, if declared"], 0,
    "`InstanceOfActionSchemaEntry` requires `data.attrs = .empty` (Cedar/Thm/Validation/Typechecker/Types.lean lines 114–117)."),
  q("How many type environments does a schema give?", ["One per (principal type, action, resource type) combination", "Exactly one"], 0,
    "`Schema.environments`, Cedar/Validation/Validator.lean line 45."),
  q("Must the request's action equal the environment's action?", ["Yes", "No, any declared action works"], 0,
    "Cedar/Thm/Validation/Typechecker/Types.lean line 81."),
 ])


node("Thm.request_and_entities_validate_implies_instance_of_wf_schema",
 "The runtime checks establish schema conformance",
 "If the schema is well-formed and the executable `validateRequest` and `validateEntities` checks pass, the request and entities really do conform to one of the schema's environments.",
 r"""## Plain English

**Theorem (Cedar/Thm/Validation/RequestEntityValidation.lean lines 270–289).** If
`schema.validateWellFormed = .ok ()`, `validateRequest schema request = .ok ()` and
`validateEntities schema entities = .ok ()`, then `InstanceOfWellFormedSchema schema request entities`
(see [schema conformance](#/node/Thm.InstanceOfWellFormedEnvironment)).

This links the Boolean checking functions an implementation runs to the logical predicates the soundness proofs use.
It is the first step of both [validation_is_sound](#/node/Thm.validation_is_sound) and
[validate_with_level_is_sound](#/node/Thm.validate_with_level_is_sound).

**Proof idea.** `validateRequest` finds some environment the request matches (lines 278–283); the
`instance_of_well_formed_env` lemma (lines 253–268) then turns the per-environment Boolean checks into the predicates.

**ETNA connection.** Three of the twelve ETNA bugs are in exactly these checks: request principal existence (PR #658),
action entities with attributes (PR #648), and singleton-bool attribute types in `validateWellFormed` (PR #689).
Reintroducing any of them would break this theorem's proof, which is why ETNA builds only the runner and not the proofs
(see [the runner](#/node/EtnaCedar.witnessFor)).
""",
 [q("Which three checks are hypotheses?", ["validateWellFormed, validateRequest, validateEntities", "validate, typecheck, evaluate"], 0,
    "Cedar/Thm/Validation/RequestEntityValidation.lean lines 271–273."),
  q("The conclusion holds for…", ["some environment of the schema", "every environment of the schema"], 0,
    "`InstanceOfWellFormedSchema` is an existential (Cedar/Thm/Validation/Validator.lean lines 40–42)."),
  q("Would this theorem still hold if validateEntities accepted action entities with attributes?", ["No, conformance requires action attrs to be empty", "Yes"], 0,
    "Cedar/Thm/Validation/Typechecker/Types.lean lines 114–117; this is ETNA variant 3."),
 ])


node("Thm.type_of_is_sound",
 "Key lemma: the typechecker is sound for expressions",
 "If the typechecker assigns an expression a type, evaluation returns a value of that type, or one of the three allowed runtime errors. The proof is by induction on the expression, one case per expression form.",
 r"""## Plain English

**Theorem (`type_of_is_sound`, Cedar/Thm/Validation/Typechecker.lean lines 50–104).** Suppose
- the "capabilities" (the set of attribute accesses already known to be safe, e.g. after a `has` test) are valid for
  this request and entities,
- the request and entities [conform](#/node/Thm.InstanceOfWellFormedEnvironment) to the environment, and
- `typeOf e c₁ env = .ok (ty, c₂)`.

Then the output capabilities are valid whenever `e` evaluates to true, and there is a value v with
[EvaluatesTo](#/node/Thm.EvaluatesTo) `e … v` and v an instance of the type `ty.typeOf`.

This is the classic "well-typed programs don't go wrong" theorem, for Cedar's type system (which includes singleton
boolean types `true`/`false`, record types with optional attributes, and capability tracking for `has`).

**Proof shape.** Structural recursion on `e` (lines 58–104): each expression form (literal, variable, if, and, or,
unary/binary operator, has, get-attribute, set, record, extension call) is discharged by its own lemma in the
Cedar/Thm/Validation/Typechecker/ directory (about 6,700 lines). This site doesn't go into those.

**ETNA connection.** [property_validator_type_preservation](#/node/Etna.property_validator_type_preservation) is an
executable spot-check of a weaker form of this statement: it only checks the `.ok v` case.
""",
 [q("What does 'v is an instance of ty' rule out?", ["e.g. a string where the type said bool", "Any evaluation error"], 0,
    "`InstanceOfType` (Cedar/Thm/Validation/Typechecker/Types.lean lines 52–77) relates values to types."),
  q("How is the proof organised?", ["Recursion on the expression, one lemma per expression form", "One big simp call"], 0,
    "Cedar/Thm/Validation/Typechecker.lean lines 58–104."),
  q("Does it say evaluation always succeeds?", ["No, three error kinds remain possible", "Yes"], 0,
    "The conclusion uses `EvaluatesTo` (Cedar/Thm/Validation/Typechecker.lean line 55)."),
 ])


node("Thm.typecheck_policy_with_environments_is_sound",
 "From one expression to one policy across all environments",
 "If a policy typechecks in every environment of the schema, and the request conforms to one of them, the policy evaluates to a boolean or an allowed error.",
 r"""## Plain English

Three layers sit between [type_of_is_sound](#/node/Thm.type_of_is_sound) and the headline:

1. **`typecheck_policy_is_sound`** (Cedar/Thm/Validation/Validator.lean lines 66–83). `typecheckPolicy`
   (Cedar/Validation/Validator.lean lines 196–203) first replaces the variable `action` with the environment's
   concrete action, then typechecks and demands a boolean type. The proof applies `type_of_is_sound`, shows a value of
   boolean type is a boolean (line 79), and undoes the action substitution (line 82).
2. **`typecheck_policy_with_environments_is_sound`** (lines 85–102). `typecheckPolicyWithEnvironments`
   (Cedar/Validation/Validator.lean lines 216–219) runs `checkEntities` (every entity literal is declared), then
   typechecks the policy in **every** environment, and rejects a policy that is `false` in all of them. The proof
   picks the environment the request conforms to and uses layer 1 there.
3. **`typecheck_is_sound`** (Cedar/Thm/Typechecking.lean lines 43–60) is an older single-environment statement
   with the same conclusion, without the action substitution.

The "impossible policy" check (`allFalse`) and `checkEntities` are *extra* rejections. They make validation stricter,
not more permissive, so soundness doesn't depend on them. ETNA variant 5 (PR #779) is about `checkEntities` being
needed: in `true || principal == Foo::"x"`, the typechecker short-circuits and never sees the undeclared type `Foo`.
""",
 [q("Does the soundness proof rely on `checkEntities`?", ["No, it only makes validation stricter", "Yes, essentially"], 0,
    "The proof just steps past it (Cedar/Thm/Validation/Validator.lean line 92)."),
  q("In how many environments must the policy typecheck?", ["All of the schema's environments", "At least one"], 0,
    "`schema.environments.mapM (tc policy)` (Cedar/Validation/Validator.lean line 218)."),
  q("What does typecheckPolicy do before typechecking?", ["Substitutes the environment's action for the `action` variable", "Removes all `unless` clauses"], 0,
    "Cedar/Validation/Validator.lean lines 196–197."),
 ])


node("Thm.validation_is_sound",
 "Headline: validation is sound",
 "If the schema is well-formed, the policies validate, and the request and entities pass their validation checks, then every policy evaluates to a boolean, or fails only with a missing-entity, extension or overflow error.",
 r"""## Plain English

**Theorem (`validation_is_sound`, Cedar/Thm/Validation.lean lines 50–79).** Assume
1. `schema.validateWellFormed = .ok ()`;
2. `validate policies schema = .ok ()`;
3. `validateRequest schema request = .ok ()`;
4. `validateEntities schema entities = .ok ()`.

Then [AllEvaluateToBool](#/node/Thm.AllEvaluateToBool) `policies request entities`: every policy evaluates to a boolean
or to one of the three [allowed errors](#/node/Thm.EvaluatesTo).

This is the guarantee the Cedar validator gives users: validated policies never hit a type error or a missing
attribute at authorization time. All four hypotheses are **executable checks**, so a user can actually establish
them.

**Faithfulness.** The name and the README ("Sound type checking") match the statement. It is a *soundness*
(no-false-accept) result only: nothing says the validator accepts every safe policy. ETNA variant 9 (PR #573) is a
historical *completeness* bug in the level checker, which no soundness theorem can catch; see
[property_validate_with_level_accepts](#/node/Etna.property_validate_with_level_accepts).

**Status.** Complete proof in the source; upstream Cedar result. Not built for this site.
""",
 [q("Which of these can still happen for a validated policy?", ["entityDoesNotExist error", "A type error", "Evaluating to a string"], 0,
    "See `EvaluatesTo` (Cedar/Thm/Validation/Typechecker/Basic.lean lines 55–59)."),
  q("Does the theorem require the entities to be validated against the schema?", ["Yes, hypothesis 4", "No"], 0,
    "Cedar/Thm/Validation.lean line 54."),
  q("Does it show the validator accepts all safe policies?", ["No, it is soundness only", "Yes"], 0,
    "The conclusion is about validated policies only (Cedar/Thm/Validation.lean lines 50–55)."),
  q("Is the empty policy list a special case in the proof?", ["Yes, it's handled separately and trivially", "No"], 0,
    "Cedar/Thm/Validation.lean line 62."),
 ],
 caveats=["Upstream Cedar result (cedar-policy/cedar-spec). Not built for this site.",
          "Soundness only: it does not say the validator is complete (accepts every safe policy)."],
 widgets=walk("How the proof goes (Cedar/Thm/Validation.lean, lines 50-79)", [
  {"text": "Turn the three executable checks into 'the request and entities conform to some environment'.",
   "lean": "have h₁ := request_and_entities_validate_implies_instance_of_wf_schema schema request entities hwf h₁ h₂",
   "link": "Thm.request_and_entities_validate_implies_instance_of_wf_schema"},
  {"text": "Case on the policy list. The empty list is trivial.",
   "lean": "| nil => simp only [List.not_mem_nil, false_implies, implies_true]"},
  {"text": "For a non-empty list, take any policy in it and apply per-policy soundness.",
   "lean": "apply typecheck_policy_with_environments_is_sound policy schema request entities h₁",
   "link": "Thm.typecheck_policy_with_environments_is_sound"},
  {"text": "What remains is that this policy passed `typecheckPolicyWithEnvironments`. `validate` is a `forM` over the list, so the head passed (lines 69–76)…"},
  {"text": "…and every tail policy passed too, by the forM-all-ok lemma.",
   "lean": "apply List.forM_ok_implies_all_ok t' (typecheckPolicyWithEnvironments _ · schema)"},
 ]))


node("Thm.validate_with_level_is_sound",
 "Headline: level-based entity slicing is sound",
 "If policies validate at level n, an authorizer can load only the entities reachable from the request within n attribute dereferences and still get exactly the same response.",
 r"""## Plain English

Real deployments can't send the whole entity database to the authorizer. Cedar's **level** validation
(`validateWithLevel`, Cedar/Validation/Validator.lean lines 232–233) additionally checks that each policy dereferences
entities at most n levels deep (`TypedExpr.checkLevel`, Cedar/Validation/Levels.lean lines 97–132). For example,
`principal.manager.manager.name` is level 2.

`Entities.sliceAtLevel` (Cedar/Spec/Slice.lean lines 46–56) keeps the entities reachable from the principal, action,
resource and context in at most n hops through attribute and tag values.

**Theorem (`validate_with_level_is_sound`, Cedar/Thm/Validation.lean lines 87–93).** If the schema is well-formed,
the request and entities validate, and `validateWithLevel ps schema n = .ok ()`, then

`isAuthorized request entities ps = isAuthorized request (entities.sliceAtLevel request n) ps`.

It is an equality of whole responses: decision, determining policies and erroring policies.

**Status.** Complete proof in the source; upstream Cedar result. Not built.

**ETNA connection.** Historical bug PR #573 made the level checker *reject* `Action::"a" in Action::"a"` at level 1.
That is a completeness bug (too strict), and it doesn't contradict this theorem.
""",
 [q("What does the theorem compare?", ["The full responses with full vs sliced entities", "Only the decisions"], 0,
    "Equality of `isAuthorized …` results (Cedar/Thm/Validation.lean line 92)."),
  q("What is n?", ["The maximum depth of entity dereferences the policies may make", "The number of policies"], 0,
    "See `checkLevel` (Cedar/Validation/Levels.lean lines 97–132)."),
  q("Does `validateWithLevel` also do ordinary validation?", ["Yes, it typechecks then checks the level", "No"], 0,
    "`typecheckPolicyWithLevel` calls `typecheckPolicy` first (Cedar/Validation/Validator.lean lines 205–210)."),
  q("Would the bug 'level checker rejects a valid policy' break this theorem?", ["No, rejecting more only makes the hypothesis harder to meet", "Yes"], 0,
    "This is ETNA variant 9, a completeness bug."),
 ],
 caveats=["Upstream Cedar result. Not built for this site."],
 widgets=walk("How the proof goes (Cedar/Thm/Validation.lean, lines 87-93)", [
  {"text": "Turn the executable request/entity checks into schema conformance.",
   "lean": "(request_and_entities_validate_implies_instance_of_wf_schema _ _ _ hwf hr he)",
   "link": "Thm.request_and_entities_validate_implies_instance_of_wf_schema"},
  {"text": "Hand it to the well-formed version, which does the real work.",
   "lean": ":= validate_with_level_is_sound_wf (request_and_entities_validate_implies_instance_of_wf_schema _ _ _ hwf hr he) htl",
   "link": "Thm.validate_with_level_is_sound_wf"},
 ]))


node("Thm.validate_with_level_is_sound_wf",
 "Level slicing: the per-policy argument",
 "Each level-checked policy evaluates identically on the full and the sliced entity store. Since the authorizer only looks at policy evaluation results, the responses agree too.",
 r"""## Plain English

**Theorem (Cedar/Thm/Validation/Levels.lean lines 149–158).** Same as
[the headline](#/node/Thm.validate_with_level_is_sound), with schema conformance as a hypothesis instead of the
executable checks.

**Proof chain.**
1. `level_based_slicing_is_sound_expr` (lines 45–109): for a well-typed expression within level n,
   `evaluate e request entities = evaluate e request (entities.sliceAtLevel request n)`. Structural recursion on the
   expression, with one lemma per form in Cedar/Thm/Validation/Levels/.
2. `typecheck_policy_with_level_is_sound` (lines 111–128): the same for a whole policy, undoing the action
   substitution.
3. `typecheck_policy_at_level_with_environments_is_sound` (lines 130–147): pick the conforming environment.
4. Lines 154–158: every policy evaluates the same, and `is_authorized_congr_evaluate`
   (Cedar/Thm/Authorization/Authorizer.lean lines 94–103) says that if every policy evaluates the same under two
   inputs, `isAuthorized` gives the same response.
""",
 [q("Which fact about the authorizer is used at the end?", ["It depends only on each policy's evaluation result", "It is order-independent"], 0,
    "`is_authorized_congr_evaluate` (Cedar/Thm/Authorization/Authorizer.lean lines 94–97)."),
  q("The expression-level lemma is proved by…", ["recursion on the expression", "SMT solving"], 0,
    "Cedar/Thm/Validation/Levels.lean lines 52–109."),
  q("Does the expression lemma need the expression to be well-typed?", ["Yes", "No"], 0,
    "Hypothesis `ht : typeOf e c env = .ok (tx, c₁)` (Cedar/Thm/Validation/Levels.lean line 48)."),
 ])


node("Thm.InstanceOfWellFormedSchema",
 "Conforming to some environment of the schema",
 "A request and entity store conform to a schema when they conform to at least one of its type environments.",
 r"""## Plain English

**Definition (Cedar/Thm/Validation/Validator.lean lines 40–42).** There is an environment `env` in
`schema.environments` with [InstanceOfWellFormedEnvironment](#/node/Thm.InstanceOfWellFormedEnvironment)
`request entities env`.

It is what the executable checks establish
([request_and_entities_validate…](#/node/Thm.request_and_entities_validate_implies_instance_of_wf_schema)) and what
[level-slicing soundness](#/node/Thm.validate_with_level_is_sound_wf) assumes.
""",
 [q("Is it 'some environment' or 'every environment'?", ["Some", "Every"], 0, "An existential (Cedar/Thm/Validation/Validator.lean line 41)."),
  q("Which environment will a real request conform to?", ["The one for its own (principal type, action, resource type)", "All of them"], 0,
    "The action must match the environment's action (Cedar/Thm/Validation/Typechecker/Types.lean line 81)."),
  q("Is this a runnable check?", ["No, it is a Prop", "Yes"], 0, "It is defined with `∃` (Cedar/Thm/Validation/Validator.lean lines 40–42)."),
 ])
