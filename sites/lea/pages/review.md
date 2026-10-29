# Review: do the statements say what they claim?

Nothing below was checked by building Lean. It all comes from reading the source at the pinned commit.

Lea is an agent, not a theorem library, so "faithful" here mostly means: does each sample file prove what its
name, and the README's description of the task, say?

## soundness (examples/Logic.lean): faithful

Soundness of a natural-deduction system for propositional logic, with formulas interpreted as Lean propositions.
The name matches the textbook notion. Two notes. The rules are **intuitionistic** (no excluded middle), and
**completeness** is not attempted. Neither is a defect.

## compile_correct (examples/StackMachine.lean): faithful

The standard correctness theorem for compiling +/× expressions to a stack machine, for every starting stack.
The language is deliberately tiny. The only thing this site is unsure about without running Lean is a
proof-script detail (a `rfl` after `simp`), not the statement.

## ack_mono_and_gt and ackermann_4_1 (examples/Ackermann.lean): faithful

The README's prompt asks Lea to: define Ackermann "using well-founded recursion"; prove A(*m*, *n*) > *n*; prove
A(*m*, *n* + 1) > A(*m*, *n*); prove A(4, 1) = 65533; and not use Mathlib. The file states exactly those three
facts (the first two also bundled as `ack_mono_and_gt`) and has no imports. The definition is ordinary
pattern matching, and Lean must find the lexicographic termination argument by itself, since none is written.
That *is* well-founded recursion, so the request is met in substance. The value 65533 checks by hand
(A(3, *n*) = 2^(*n*+3) − 3, and A(4, 1) = A(3, 13)).

Monotonicity is in the **second** argument only, which is what the prompt asked for.

## runMain / SafeVerify: a program, not a theorem

SafeVerify makes no mathematical claim. It is a checker, and nothing proves it correct. Two points matter for
anyone reading Lea's results:

- **In Lea, the target is derived from the submission** (Python, [safeverify.py lines 9–17](https://github.com/VIDA-NYU/Lea/blob/a5924f6f15b980452731b6edfe00feee97791ab4/apps/lea-standalone/prover/lea/safeverify.py#L9-L17)).
  A "SafeVerify OK" result therefore means the proofs are genuine kernel-checked proofs of *the statements in the
  file*. It does not mean those statements match the natural-language request. The upstream code says this
  itself.
- SafeVerify is **opt-in** and may be **unavailable** (the leanest install skips it). Without it, Lea relies on
  "compiles with no error and no sorry warning", plus an axiom check when a result is selected (see
  [About](#/page/about)). Those catch `sorry` and extra axioms. They run inside the environment the file built
  while compiling, so they are not designed to catch environment hacks like [falseThm](#/node/falseThm) or
  [efsq](#/node/efsq). (Remember that efsq even reports only an allowed axiom.)

## Demo: original_square_claim_is_false and demo_square_bound: faithful

The disproof refutes exactly the universal claim *x* ≤ *x*² over the reals, and the corrected theorem adds 1 ≤ *x*.
The file says it holds rehearsal proofs for a presentation, not Lea output, and this site labels it that way.

## Deliberately unfinished files

`docs/reformalization-testing-guide/fixtures/*.lean` contain four `sorry`s on purpose. They are baselines for
testing that a retry leaves unrelated, unfinished work alone. Their comments say so ("unrelated work must
remain unfinished"). This site found no other file that refers to them.
