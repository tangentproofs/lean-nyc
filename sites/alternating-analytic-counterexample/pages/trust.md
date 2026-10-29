# Trust: what was and wasn't checked

## Not built

**The Lean was not built for this site.** No `lake`, `lean` or `elan` was run. When this site says something "is
proved", it only means that the source file has what looks like a complete proof with no `sorry`. It does not mean
that Lean's kernel accepted it. The upstream README and formalization.yaml say that CI builds the project against a
pinned Mathlib, checks the axioms with `#guard_msgs` (AltCounter/Check.lean lines 1–49), and runs
`leanprover/comparator` on Challenge.lean and Solution.lean. We did not rerun any of that.

## Gaps, axioms and escape hatches

A text search of every `.lean` file at the pinned commit for `sorry`, `admit`, `axiom`, `native_decide`,
`implemented_by`, `extern` and `opaque` finds:

| What | Count | Where |
|---|---|---|
| `sorry` | 2 | Challenge.lean lines 37 and 49, the statement-only copies of the two headlines. The comparator format requires them. The proved copies are in Solution.lean. |
| `admit` | 0 | |
| `axiom` | 0 | only `#print axioms` checks in AltCounter/Check.lean, not declarations |
| `native_decide` | 0 | (`decide` is used a few times, e.g. AltCounter/Pfaffian.lean line 228; that is checked by the kernel) |
| `implemented_by` / `extern` / `opaque` | 0 | |

**No `sorry` in AltCounter/ or Solution.lean.** AltCounter/Check.lean expects every main theorem to depend only on
`propext`, `Classical.choice` and `Quot.sound`. We did not run that check.

Some proofs raise `maxHeartbeats` (e.g. AltCounter/Main.lean lines 346–347). That is a performance setting, not a
soundness concern.

## Declarations

All declarations were found by scanning the source text (`extracted: false`), not from a compiled build, so some
dependency links are missing or wrong. In particular:

- bound variables named `F` (in the headline hypotheses) are mistaken for the space `AltCounter.F`;
- uses written with dot notation, or through `choose`/`obtain`, are often missed.

The node texts give the real dependencies by hand. Challenge.lean is left out of the scan on purpose. It declares
the same two names as Solution.lean, and including it would have attached the `sorry` versions to the headline pages.

## Explanations

Every explanation on this site was written by an AI (Claude) from the source text, the README, the paper and the
upstream notes, and **nobody has reviewed them**. Line references were checked against the pinned commit. The longest
analytic proofs (the gliding hump and induction on arity in Phillips.lean and PhillipsOne.lean, and the
nested-balls argument in NestedBalls.lean) are summarised from their docstrings and comments, not traced line by
line. Those nodes say so in their caveats.
