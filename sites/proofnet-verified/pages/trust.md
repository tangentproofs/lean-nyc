# Trust: what was and wasn't checked

## Not built

**The Lean was not built or run for this site.** No `lake`, `lean` or `elan` was run, and the project's
`scripts/verify_compilation.py` was not run either. That the 367 statements type-check under Lean/Mathlib v4.34.0
is the authors' claim. Where this site says a proof is "complete", it means the file contains a complete-looking
proof, not that Lean was seen to accept it.

## Gaps and escape hatches

A text search of the scanned folder `proofnet-verified-latest/` (367 files, about 6,150 lines) at the pinned
commit finds:

| What | Count | Where |
|---|---|---|
| `sorry` | 366, one per file | every problem file except proofnet-35.lean, always as the whole proof of the file's single theorem, **by design**: these are benchmark problems |
| complete proofs | 1 | [proofnet-35.lean lines 15–61](src/proofnet-verified-latest/proofnet-35.lean.html#L15-L61) (see [review](#/review)) |
| `admit` | 0 | |
| `axiom` | 0 | |
| `native_decide` | 0 | |
| `implemented_by` / `extern` / `opaque` | 0 | |

So **every theorem on this site except one is PARTIAL (sorry) by design.** That is the intended state of a
benchmark, not a defect. The folders that were not scanned look the same: `data/archive/proofnet-verified-4.28/`
(367 files, 366 `sorry`, the same exception), `data/proofnet/proofnet-4.28/` (the 367 originals, all `sorry`) and
`data/proofnet/proofnet_lean4-6deae98/formal/` (11 files, an older Lean 4 port), with no axioms or `native_decide`
anywhere.

The ground-truth proofs are in `data/archive/proofnet-verified_gt-4.28.zip`, which this site **deliberately did
not open**: the authors zipped them to keep them out of AI training data, and quoting them here would undo that.
Whether each corrected statement is true therefore rests on the authors' report.

## Declarations

All declarations were found by scanning the source text (`extracted: false`), not from a compiled build. Known
scanner artefacts on this site:

- **Repeated names.** Each problem file is standalone, so several files define the same helper (`is_topology` ×5,
  `I` ×5, `countably_compact` ×2, `lower_limit_topology` ×2) and two files share the theorem name
  `Rudin_exercise_4_8a`. The scanner adds primes to keep ids unique: `is_topology'`, `I''`,
  `Rudin_exercise_4_8a'` (problem 351) and so on. In the benchmark there is no clash.
- **False dependencies.** The scanner matches names without knowing which namespace or local variable is meant. The
  `I` in [the polarization identity](#/node/Axler_exercise_6_7) is the complex number i, but it is linked to the
  unit-interval helper [I](#/node/I). Bound variables named `f` or `g` in several statements (for example
  Herstein 2.3.17, Shakarchi 1.13a, Rudin 4.8a) are linked to the unrelated helper sequences `f` and `g` of
  Rudin 3.3 and 3.6. Ignore those links.
- **Original statements are not scanned.** Links labelled "original proofnet-N.lean" go to GitHub at the pinned
  commit, not to this site's source browser.

## The audit data

Faithfulness and provability verdicts, root causes and per-book error counts come from the project's JSON records
in `error_taxonomy/`. Per-book counts were tallied by this site from those records. The records were read, not
re-derived, apart from about 20 that this site compared with the two Lean versions by hand.

## The explanations

Every explanation, quiz and caveat on this site was written by an AI (Claude) from the public repository. None has
been reviewed by a human or by the project's authors. All nodes are marked `review: draft`.
