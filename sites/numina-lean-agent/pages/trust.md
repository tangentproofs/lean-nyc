# Trust: what was and wasn't checked

## Not built

**The Lean was not built for this site.** No `lake`, `lean` or `elan` was run. The Python harness, the agent and the
external tools were not run either. The project pins `leanprover/lean4:v4.26.0` with Mathlib v4.26.0
(leanproblems/lean-toolchain, leanproblems/lakefile.toml). The project's own CI builds only the placeholder library,
not the problem files (see [Review](#/page/review)).

## Gaps, axioms and escape hatches

A text search of all 19 `.lean` files at the pinned commit:

| What | Count | Where |
|---|---|---|
| `sorry` | 17 | every Putnam file (12) and four of the five miniF2F files (5 theorems; imo_1964_p1.lean has two) |
| `admit` | 0 | |
| `axiom` | 0 | |
| `native_decide` | 0 | |
| `decide` | 1 | the only completed proof, amc12a_2021_p7.lean line 10 |
| `implemented_by` / `extern` / `opaque` | 0 | |

The `sorry`s are **deliberate**. These files are tasks for the agent, and each `sorry` marks the hole it should
fill. Each node links to its own `sorry` line. So 17 of the 18 theorems are PARTIAL (sorry). The 18th
([amc12a_2021_p7](#/node/amc12a_2021_p7)) has a complete-looking proof that we suspect may not finish checking.

All twelve Putnam files set `maxHeartbeats 0`, which turns off Lean's time limit for elaboration. That doesn't
affect soundness.

## Declarations

The 29 declarations (18 theorems, 11 definitions) were found by scanning source text (`extracted: false`), not from
a compiled build. The scanner lists `f` (A5's counting function) as a dependency of B2; that is a false positive, because B2's
`f` is a local variable.

The problem files have lower-case names (putnam_2025_a1.lean), and the site engine only auto-links capitalised
`.lean` file names. So node bodies link to GitHub explicitly, and quiz explanations and walkthrough steps give the
lines as plain text.

## The explanations

Every explanation, quiz and caveat on this site was written by an AI (Claude) from the public source and README.
None has been reviewed by a human or by the project's authors. All nodes are marked `review: draft`. The
faithfulness judgements on the Review page compare the Lean with our own recollection of the Putnam 2025 problems,
not with an official text.
