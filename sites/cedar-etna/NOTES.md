# NOTES for the coordinator (cedar-etna)

## Time spent

About 1.5 hours of wall-clock agent time: reading the README, etna.toml and the ETNA files, picking headlines out of
about 71k lines of proofs, writing 35 nodes and 3 pages, and iterating on the build.

## Decisions made (no questions asked, per the brief)

- **Headlines (6, all upstream Cedar):** `forbid_trumps_permit`, `default_deny`, `validation_is_sound`,
  `validate_with_level_is_sound`, `compile_is_sound`, `verifyEquivalent_is_sound`. They are the properties the upstream
  README lists as "Verified properties". The ETNA layer has no theorems, so it can't supply headlines. It is
  prominent in the lead, the About page and 8 ETNA nodes.
- **Roots:** Cedar/Spec, Cedar/Data, Cedar/Validation, Cedar/SymCC, the top-level Cedar/Thm/*.lean files we headline,
  a handful of supporting Thm files, Cedar/Etna and EtnaCedar. About 80 of 355 files. Not scanned: most of Cedar/Thm
  (the per-case lemma trees), TPE, SymCCOpt, Protobuf/FFI/CLI/DiffTest/UnitTest, and the Rust crates.
- **Grouped nodes** (anchored on one real declaration each): the rest of Authorization.lean, the other 25 verification
  theorems, policy slicing + TPE, and the four ETNA property families.
- **Authors:** kept the coordinator's `authors` string. README has no author list; NOTICE says "Copyright Cedar
  Contributors". The About page names the most frequent upstream committers from git history (Craig Disselkoen,
  John Kastner, Shaobo He, Kesha Hietala) as examples, not as an exhaustive list.
- **Licence:** Apache-2.0 with NOTICE, both present; no change.

## Engine issue (worked around, not fixed)

`engine/tools/scan_decls.py`'s `DECL` regex doesn't accept the `public` modifier (Lean module system:
`public def …`, `@[expose] public def …`). Most of Cedar/Spec, Cedar/Validation and Cedar/SymCC are written that way.
So `Spec.isAuthorized`, `Spec.evaluate`, `Validation.validate`, `Policy`, `Request` and similar have **no
declaration entries** and can't be node ids. Workaround: describe them inside nodes anchored on scanned declarations
(e.g. `Thm.HasSatisfiedEffect` explains `isAuthorized`), with exact line links. Adding `public` (and `meta`?) to the
modifier list in `DECL` would fix it. Also, `@[expose] public def` is preceded by an attribute on its own line in some
files, which may need handling too. The same issue will hit any other site whose upstream uses `module`.

## Places I'm least sure of

- **`Etna.property_validator_type_preservation` / `Thm.request_and_entities_validate_implies_instance_of_wf_schema`:**
  I say that re-inserting variant 7 (dropping `validateLifted`) and variants 3 and 6 would break the upstream proofs.
  That is inferred from the etna.toml summaries and the README's general remark. I did not build, and I did not check
  which proof would fail.
- **`Etna.property_validate_rejects_undeclared_entities`, variant 5:** I argue it doesn't contradict
  `validation_is_sound`, because the short-circuited subexpression is never evaluated. The evaluator does short-circuit `||`
  (Cedar/Spec/Evaluator.lean lines 112–114). The remaining uncertainty is whether anything else in the proof relies on
  every literal being declared.
- **`Etna.property_symcc_pipeline_soundness` caveat:** I claim variants 4 and 10 report "passed" without CVC5 in
  `etna` mode. That follows from `runEtna` mapping discard→passed and from the CVC5 check, but the external ETNA CI
  (reusable workflow) may always set CVC5. I only looked at scripts/ and Main.lean.
- **native_decide reach (trust page and SymCC caveats):** I say the SymCC headlines "very likely" depend on
  Cedar/Thm/SymCC/Data/Ext.lean's `native_decide` (by import graph only), and that other headlines "may" depend on
  Cedar/Data/Int64.lean's two uses. I didn't trace the proof dependencies.
- **`Thm.type_of_is_sound`:** my gloss of "capabilities" (attribute accesses known safe after `has`) and of the
  `GuardedCapabilitiesInvariant` conclusion is simplified. I didn't read Cedar/Thm/Validation/Typechecker/Basic.lean in
  full.
- **`Thm.verifyIsAuthorized_is_sound`:** the summary of `WellBehavedIsAuthorizedQuery` (well-formed output,
  interpretable, mirrors f) is from the `where` clause names, lines 33–53, without reading every clause.

## Things the author(s) might object to

- The review page lists harness limitations: discard counted as pass, variant 2's property is weaker than the cited
  grammar, variant 5's oracle is the fix itself, and stale README/docstring text (layout, "three properties",
  "200 trials", the `#guard` mention, the smoke-test table). These are factual readings of the pinned source, but an
  author could reasonably see them as nitpicks of research-prototype code.
- The About page mentions, from the README, that construction was driven by an "etna-ify" prompt, and that ETNA
  commits are authored as "ETNA Bootstrap". It is factual, but the author may not want it emphasised.
- Cedar Contributors might object that the site's headline framing ("bugs cluster where the proofs stop") implies
  their proofs are weak. The text tries to say the opposite: the proofs are scoped to the Term level and assume the
  executable checks, and the historical bugs sit outside that scope.
