# Trust: what was and wasn't checked

## Not built

**The Lean was not built for this site.** No `lake`, `lean` or `elan` was run. When we say something "is proved",
we only mean that the source file contains what looks like a complete proof, not that Lean's kernel accepted it.
The repository has a CI workflow (.github/workflows/lean_action_ci.yml), but this site did not look at its results.

## Gaps, axioms and escape hatches

A text search of all 106 `.lean` files at the pinned commit for `sorry`, `admit`, `axiom`, `native_decide`,
`implemented_by`, `extern` and `opaque` finds:

| What | Count | Where |
|---|---|---|
| `sorry` | 0 | |
| `admit` | 0 | |
| `axiom` | 0 | one occurrence of the word in a doc comment (ProgramLogics/HoareLib.lean line 22), which explains that the course's Rocq axiom became an instance argument |
| `native_decide` | 0 | |
| `implemented_by` / `extern` | 0 | |
| `opaque` | 0 | the word appears only in comments (ProgramLogics/LaterLoeb.lean line 386, TypeSystems/SystemFMuState/Execution.lean line 284) |

Some files raise Lean's resource limits (`maxHeartbeats`, `maxRecDepth`), for example
TypeSystems/SystemFMuState/MutBit.lean line 18. This doesn't affect soundness.

## Dependencies

The program-logic chapters depend on **iris-lean**, pinned by lake-manifest.json to revision 728a171, and on
Lean core and Batteries. The concurrent headline's last step is iris-lean's `heap_adequacy`. A text search of
iris-lean at that revision finds no active `sorry` (four occurrences, all inside comments) and no `axiom`.
iris-lean was not built or reviewed either.

## Hypotheses that matter

- [Reloc.refines_sound](#/node/ProgramLogics.Reloc.refines_sound) and `refines_sound_open`: a no-fork hypothesis over
  all contexts. By this site's reading it is unsatisfiable, so the theorems are vacuous (see the review page).
- [LogRel.syn_soundness_not_stuck](#/node/ProgramLogics.LogRel.syn_soundness_not_stuck) and the other sequential
  adequacy results: a no-fork hypothesis for one program, which is satisfiable but never discharged.

## Declarations

All declarations were found by scanning the source text (`extracted: false`), not from a compiled build, so some
dependency links can be missing or wrong. Two known scanner limitations affected this site:

- definitions inside a `mutual` block (the STLC and state-language `valRel` / `exprRel`) are not listed, so they
  are explained inside the `semTyped` nodes;
- a constructor name inside `SystemF.TypeWf` was mistaken for a theorem of the same short name in
  TypeSystems/SystemF/ChurchEncodings.lean, which created a dependency cycle. That file is excluded from the scan.

## The explanations

Every explanation, quiz and caveat on this site was written by an AI (Claude) from the public source. None has
been reviewed by a human or by the project's author. All nodes are marked `review: draft`.
