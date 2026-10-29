# Trust: what was and wasn't checked

## Not built

**The Lean was not built for this site.** No `lake`, `lean` or `elan` was run. When this site says something "is
proved", it only means the source contains what looks like a complete proof and a comment-aware text search finds no
`sorry`, `admit` or `axiom` in the compiled code. It does not mean Lean's kernel accepted it here.

The upstream README reports that CI runs `lake build` (0 errors, 0 sorrys, 0 warnings), `#print axioms` (only
`propext`, `Classical.choice`, `Quot.sound`), `lean4checker --fresh` on 8 modules, and the Comparator tool in a
Landlock sandbox, with results in test/verification/CI/. Those claims are the project's. They were not reproduced here.

## Gaps, axioms and escape hatches

A text search of every `.lean` file at the pinned commit, with Lean comments and strings stripped first, for `sorry`,
`admit`, `sorryAx`, `axiom` declarations, `native_decide`, `implemented_by`, `@[extern]` and `opaque`:

| What | In the library (FLT_Proofs/, 102 files) | Elsewhere in the repo |
|---|---|---|
| `sorry` in code | **0** | 15: 8 in Verification/ChallengeCrown.lean, 7 in world_model/future_work/ |
| `admit` | 0 | 0 |
| `axiom` declarations | 0 | 0 |
| `native_decide` | 0 | 0 |
| `implemented_by`, `@[extern]`, `opaque` | 0 | 0 |

### About the 17 files that mention `sorry`

A plain `grep -w sorry` hits 17 files. They fall into three groups:

1. **14 library files where `sorry` appears only in comments or docstrings.** Bridge.lean,
   Complexity/Compression.lean, Complexity/Generalization.lean, Complexity/GeneralizationResults.lean,
   Complexity/Symmetrization.lean, Complexity/IndependentVC.lean, Theorem/PAC.lean, Theorem/Separation.lean, and six
   files in Complexity/IndependentVC/ (CapacityClosures, CapacitySpectrum, Finitization, FrameworkClosures,
   ScaleFinitization, StructureClosures). Some are statements that a file is "sorry-free". Others are **stale**
   notes from earlier sessions that describe sorrys no longer present: for example, Complexity/Symmetrization.lean
   lines 1015–1028 call `exchangeability_chain_bound` "ORPHANED — contains 2 sorrys", but its body (lines 1030–1573)
   has none (and, contrary to that comment, it *is* on the fundamental theorem's path, through
   `double_sample_pattern_bound`). Likewise Theorem/Separation.lean lines 790–799 describe a "Γ₆₇: sorry" that is not in the code.
2. **Verification/ChallengeCrown.lean: 8 deliberate `sorry`s** (lines 45, 53, 62, 73, 87, 95, 106, 114). These are
   the *challenge* statements for the Comparator tool: copies of the eight "crown jewel" theorem statements (the
   fundamental theorem, compression, VC characterization, MWU approximate minimax, finite-support VC approximation,
   Dudley's bound, a capacity non-universality result and a shattering/adversary equivalence), to be matched against
   the real proofs in Verification/SolutionCrown.lean. Leaving them `sorry` is how Comparator works. The file belongs to
   the separate `Verification` library in lakefile.lean, not the default `FLT_Proofs` target. Not a gap.
3. **world_model/future_work/BridgeRealTests.lean (5) and BridgeDiagnostic.lean (2).** Experiments with a proof-search
   tactic, outside the library build (they are not in lakefile.lean's targets). Not a gap.

So the README's "0 sorry" is accurate for the library, as far as a text search can tell.

### Other things a reader should know

- **Commented-out code.** Some theorems are kept as block comments, for example `universal_trichotomy` and
  `bhmz_middle_branch` (Theorem/Extended.lean lines 25–58). The scanner correctly ignores them, and the project does
  not claim them.
- **Placeholder statements.** `gold_does_not_imply_pac : True` (Complexity/Generalization.lean lines 1013–1016) is a
  trivially true placeholder. The real content is `ex_not_implies_pac`.
- **Junk-value conventions.** Mathlib's `sInf ∅ = 0`, `ncard` of an infinite set = 0, and the Bochner integral of a
  non-integrable function = 0 all appear in definitions ([SampleComplexity](#/node/SampleComplexity),
  [GrowthFunction](#/node/GrowthFunction), [RademacherComplexity](#/node/RademacherComplexity)). The relevant node
  pages explain why each does not make a headline vacuous.
- **Outer measure.** [PACLearnable](#/node/PACLearnable) applies the product measure to sets that need not be
  measurable, which means outer measure.

## How declarations were read

Declarations were scanned from the source text by the engine's `scan_decls.py`, not extracted from a compiled
environment (`extracted: false`). Dependencies between declarations are inferred from identifiers in the text, so
they may include false positives (a name in a comment) or miss notation-level dependencies.

## Who wrote the explanations

The explanations, quizzes, roadmap and review on this site were written by an AI model (Claude) from the source at
the pinned commit and the project's README. **They have not been reviewed by the project's author or by a human
expert.** Line references were checked by the build against the pinned source. Mathematical judgments (for example
the assessment of `MeasurableConceptClass` and of the sample-complexity conjunct) are the AI's reading and could be
wrong. Please report errors.
