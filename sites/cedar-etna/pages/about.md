# About this site

## The project

[alpaylan/cedar-etna](https://github.com/alpaylan/cedar-etna) is maintained by **Alperen Keleş**. It is a fork of
[cedar-policy/cedar-spec](https://github.com/cedar-policy/cedar-spec), the formal specification of
[Cedar](https://www.cedarpolicy.com/), Amazon's open-source language for writing authorization policies. The fork
adds an **ETNA workload**. ETNA is a framework for benchmarking property-based testing (PBT) tools: a workload bundles
a program, a set of real bugs that can be switched back on, and properties that should detect them.

The README describes it as an "ETNA workload built from the cedar-policy/cedar-spec Lean 4 formalization", where "each
variant reintroduces one historical bug fix from cedar-spec history by reverse-applying a hand-crafted patch against a
pinned base commit, paired with a property and a deterministic witness."

So the repository has two layers with different authors:

1. **Cedar's Lean specification and proofs**, by the Cedar Contributors (NOTICE: "Copyright Cedar Contributors";
   the most frequent committers in the history include Craig Disselkoen, John Kastner, Shaobo He and Kesha Hietala).
   This is about 96,000 of the roughly 98,800 lines and contains every theorem on this site.
2. **The ETNA layer**, added by Alperen Keleş: cedar-lean/Cedar/Etna/ (five files), cedar-lean/EtnaCedar/Main.lean,
   twelve patches in patches/, the manifest etna.toml, scripts, BUGS.md/TASKS.md and a CI workflow. About 2,000
   lines of Lean. The README says the workload's construction was driven by an "etna-ify" prompt and skill set, and
   the ETNA commits are authored as "ETNA Bootstrap".

## What the Lean covers (upstream Cedar)

Cedar's README lists its verified properties. This site headlines six of them, with their dependency spines:

- **Authorization** (Cedar/Thm/Authorization.lean): [forbid trumps permit](#/node/Thm.forbid_trumps_permit) and
  [default deny](#/node/Thm.default_deny), built on [satisfied policies](#/node/Thm.HasSatisfiedEffect). Further
  facts (order independence, monotonicity) are [grouped](#/node/Thm.allowed_iff_explicitly_permitted_and_not_denied).
- **Validation** (Cedar/Thm/Validation.lean): [validation is sound](#/node/Thm.validation_is_sound). Validated policies
  evaluate to a boolean or one of [three allowed runtime errors](#/node/Thm.EvaluatesTo). The spine goes through
  [schema conformance](#/node/Thm.InstanceOfWellFormedEnvironment) and
  [typechecker soundness](#/node/Thm.type_of_is_sound).
- **Level-based entity slicing**: [validate_with_level_is_sound](#/node/Thm.validate_with_level_is_sound). Loading only
  nearby entities gives the same answer.
- **Symbolic compilation** (Cedar/Thm/SymbolicCompilation.lean): [compile_is_sound](#/node/Thm.compile_is_sound) and
  [complete](#/node/Thm.compile_is_complete), for [the compiler to SMT terms](#/node/SymCC.compile).
- **Verification queries** (Cedar/Thm/Verification.lean): [the equivalence check is sound](#/node/Thm.verifyEquivalent_is_sound);
  [25 sibling theorems](#/node/Thm.verifyNeverErrors_is_sound) are grouped.

## What the ETNA layer adds

Read [what ETNA adds](#/node/Etna.PropertyResult) first. The twelve bugs, all from cedar-spec's history, fall into:

- **Validator and type-environment soundness holes** (variants 3, 5, 6, 7): [type preservation](#/node/Etna.property_validator_type_preservation),
  [validator invariants](#/node/Etna.property_validate_rejects_undeclared_entities);
- **SymCC SMT-LIB encoder and decoder** (variants 4, 8, 10, 11): [the CVC5 pipeline](#/node/Etna.property_symcc_pipeline_soundness),
  [narrow encoder/decoder checks](#/node/Etna.property_define_entity_rejects_non_member);
- **Extension-value parsers** (variants 1, 2, 12): [decimal and duration parsing](#/node/Etna.property_evaluator_extension_consistency);
- **A completeness bug** in the level checker (variant 9): [too strict](#/node/Etna.property_validate_with_level_accepts).

The [runner](#/node/EtnaCedar.witnessFor) replays a witness or runs Plausible random search.

One thread runs through the site: **the ETNA bugs cluster where the proofs stop.** Validation soundness assumes the
executable request, entity and schema checks are right, and variants 3, 6 and 7 broke exactly those checks. SymCC's
soundness theorems are about Lean terms, while the SMT-LIB text encoder, the solver and the decoder are outside them,
and variants 4, 8, 10 and 11 are there. With a bug re-inserted the proofs would generally no longer compile, which is
why ETNA builds only the runner executable.

## What this site leaves out

The repository has about 71,000 lines of proofs. We cover the top-level statements and their first layers only. Left
out: the per-expression-form typechecker lemmas (Cedar/Thm/Validation/Typechecker/), the SymCC term, factory and
enforcer theory (most of Cedar/Thm/SymCC/), the SymCC optimiser (Cedar/SymCCOpt), batched evaluation, TPE internals,
the protobuf/FFI/CLI/differential-testing code, and the Rust crates (cedar-drt, cedar-policy-generators) that also
live in the fork. Policy slicing and TPE get one [grouped node](#/node/Thm.isAuthorized_eq_for_sound_policy_slice).

## Where to start

Start with [forbid trumps permit](#/node/Thm.forbid_trumps_permit), then [validation is sound](#/node/Thm.validation_is_sound),
then [what ETNA adds](#/node/Etna.PropertyResult) and [the CVC5 pipeline property](#/node/Etna.property_symcc_pipeline_soundness).
