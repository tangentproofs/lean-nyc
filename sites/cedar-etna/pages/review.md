# Review: do the statements say what the names claim?

All six headlines are upstream Cedar theorems. None has a `sorry`; none is conditional beyond the hypotheses listed
in its statement. As everywhere on this site, the Lean was **not built**.

## forbid_trumps_permit and default_deny

**Faithful.** Both hold for *all* requests, entity stores and policy lists, with no side conditions
(Cedar/Thm/Authorization.lean lines 64–103). One subtlety the names don't show: an erroring policy is simply not
satisfied (Cedar/Spec/Authorizer.lean lines 29–30). So a `forbid` that throws at runtime doesn't forbid. That is
Cedar's documented skip-on-error design, and the theorems describe it correctly.

## validation_is_sound

**Faithful, soundness only.** The four hypotheses are all executable checks, which makes the theorem usable. The
conclusion still allows three runtime errors (missing entity, extension error, overflow), as its docstring says
(Cedar/Thm/Validation.lean lines 42–48). Nothing claims the validator is *complete*. ETNA variant 9 is a historical
completeness bug in the level checker, which no soundness theorem could catch.

The theorem's strength depends on the executable checks being right. Three ETNA variants are holes in those checks:
action entities with attributes (PR #648), undeclared request principals (PR #658), and singleton-bool attribute
types (PR #689). We expect the upstream proof to fail to compile with any of those bugs re-inserted. We infer that
from the etna.toml summaries and the README's remark that "some variants intentionally break those proofs"; we did
not build to check.

## validate_with_level_is_sound

**Faithful.** It is an equality of full responses with full vs sliced entities (Cedar/Thm/Validation.lean lines 87–93).
The README phrase "for any set of entities, the result of evaluating the expression with entities sliced at level n is
the same" is the per-expression lemma (Cedar/Thm/Validation/Levels.lean lines 45–109); the headline lifts it to
`isAuthorized`.

## compile_is_sound

**Faithful, at the Term level.** The README's "overapproximates (soundness) and underapproximates (completeness)"
matches `compile_is_sound`/`compile_is_complete`. Two scoping notes:

- Outcomes record only "value or error", not *which* error (docstring, Cedar/Thm/SymbolicCompilation.lean lines 64–69).
- The theorem is about `compile`'s Lean `Term`. The SMT-LIB text the encoder writes, the solver's answer and the
  decoder that reads the model back are not covered. ETNA variants 4, 8, 10 and 11 were bugs in that unverified tail.

## verifyEquivalent_is_sound

**Faithful, with the same trust boundary.** "Equivalent" means **same decision** (`bothAllowOrBothDeny`), not same
response, on inputs that are *strongly* well-formed (acyclic entity hierarchy, no dangling references). `εnv ⊭ asserts`
is a statement about Lean interpretations. Using the theorem in practice means trusting the encoder, CVC5 and the
decoder to establish it.

## The ETNA layer

ETNA properties are tests, not theorems. A few observations from reading the source at the pinned commit:

- **Discard counts as pass.** `runEtna` reports `passed` for `.discard` (EtnaCedar/Main.lean lines 237–238).
  Variants 4 and 10 are wired to the CVC5-backed pipeline witness (lines 198–214), which discards when the `CVC5`
  environment variable is unset (Cedar/Etna/Properties.lean lines 432–433). Without CVC5, those two variants would
  report `passed` with the bug in place. We found no CVC5 setup in scripts/; the external ETNA CI may provide it.
- **Variant 2's property is weaker than the grammar it cites**: it checks only the character set
  (Cedar/Etna/Properties.lean lines 127–132), not the shape `[-]?[0-9]+\.[0-9]+`.
- **Variant 5's oracle is the fix itself**: `property_validate_rejects_undeclared_entities` checks the result against
  `checkEntities`, the very function PR #779 added (Cedar/Etna/Properties.lean lines 317–320). That makes it a
  regression test more than an independent property.
- **The type-preservation property** checks a different statement from the theorem: it drops the entity-validation
  hypothesis on purpose (Cedar/Etna/Properties.lean lines 363–368).
- **Stale documentation**: the README's layout, Plausible coverage ("three properties", "200 trials") and smoke-test
  table predate the latest commits. Cedar/Etna/Witnesses.lean lines 9–11 refer to `#guard` checks that are not in the
  file. The upstream README points to `Cedar/Thm/Slicing.lean`, which is now Cedar/Thm/PolicySlice.lean.

None of these are errors in the proofs. They describe what the ETNA harness actually checks.
