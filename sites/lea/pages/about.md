# About this site

## The project

[VIDA-NYU/Lea](https://github.com/VIDA-NYU/Lea) ("LeaEcosystem") is a monorepo from NYU's VIDA group. Its git
history is mostly by **Daniel Aarão Reis Arturi** and **Shaswat Patel**, with a few other contributors. The README
names no individual authors, so this site credits "VIDA-NYU (Shaswat Patel, Daniel Aarão Reis Arturi and
contributors)".

At its core is **Lea**, "a minimal Lean 4 theorem proving agent", in its own README's words. You give it a
math statement in natural language. It writes a `.lean` file, compiles it, reads the errors, edits, searches
Mathlib, and repeats until the file compiles with no errors and no `sorry`
([prover README](https://github.com/VIDA-NYU/Lea/blob/a5924f6f15b980452731b6edfe00feee97791ab4/apps/lea-standalone/prover/README.md)). Lea calls a large language model of your choice
(OpenAI, Anthropic, Gemini, self-hosted models and others). Around the agent, the repository adds:

- a **standalone web UI** (React and Vite) with a FastAPI adapter, a SQLite store for proof timelines, and a
  background worker that owns the Lean workspace;
- an **Overleaf extension** (a Chrome extension plus a local Node companion). It formalizes theorem blocks in
  a LaTeX document that are marked with `% lea: formalize label=…` comments;
- a shared model catalog, Docker images, install scripts and extensive design documents.

The README says the evaluation harnesses (miniF2F, Putnam, FormalQualBench) and their results live in a
**separate** repository. This repository has no benchmark problem sets.

## What is (and isn't) Lean here

**Almost all of the repository is not Lean.** It is Python (the agent and the adapter), TypeScript and JavaScript
(the UI, the extension, the companion), SQL, shell scripts and LaTeX. That code is not explained here, beyond what
is needed to say how the Lean is checked.

The Lean is about 1,360 lines in 33 files, in four groups:

| Group | Where | What this site says |
|---|---|---|
| Sample proofs | `apps/lea-standalone/prover/examples/` | Four small files that the prover README describes as generated proofs. Three of them are the headline results here: [propositional soundness](#/node/soundness), [the stack-machine compiler](#/node/compile_correct), and Ackermann ([growth and monotonicity](#/node/ack_mono_and_gt), [A(4, 1) = 65533](#/node/ackermann_4_1)). The fourth, `test_proof.lean`, proves *n* + 0 = *n*. |
| Proof checking | `prover/third_party/SafeVerify/` | A vendored copy of [SafeVerify](https://github.com/GasStationManager/SafeVerify) by GasStationManager (Apache-2.0), the Lean program Lea can use to audit a finished proof. See [runMain](#/node/runMain), with its test fixtures [falseThm](#/node/falseThm) and [efsq](#/node/efsq). |
| Tooling | `prover/lea/LibraryInspect.lean` | A metaprogram that makes Lean report each declaration's type, axioms and dependencies as JSON ([inspect](#/node/LeaLibraryInspector.inspect)). |
| Demo and test fixtures | `docs/lea-overleaf-demo/reference/`, `docs/reformalization-testing-guide/fixtures/` | Rehearsal proofs for an Overleaf demo, including [a disproof of a deliberately false claim](#/node/LeaDemoReference.original_square_claim_is_false), and two small files with deliberate `sorry`s for testing how Lea retries a proof without touching unrelated work. |

There is also a `lakefile.lean` for the workspace in which Lea writes proofs, pinned to Mathlib v4.29.0.

## How the Lean side is checked

There are three levels, from weakest to strongest:

1. **The agent's own loop:** Lea counts a proof as done when Lean compiles the file with no errors and no
   "declaration uses sorry" warning.
2. **Result selection:** when a specific result is recorded, Lea compiles the file with its
   [inspector](#/node/LeaLibraryInspector.inspect) appended and rejects the result if it depends on any axiom
   other than \`propext\`, \`Quot.sound\` and \`Classical.choice\`
   ([result_selection.py lines 13 and 108–123](https://github.com/VIDA-NYU/Lea/blob/a5924f6f15b980452731b6edfe00feee97791ab4/apps/lea-standalone/prover/lea/result_selection.py#L108-L123)). This catches \`sorry\` and
   extra axioms, but it trusts the environment the file built while compiling.
3. **An optional audit:** [SafeVerify](#/node/runMain) re-runs Lean's kernel on the compiled file in a clean
   environment, requires every statement to match a target exactly, and applies the same axiom list. In Lea,
   the target is the submission with its proofs replaced by \`sorry\`. So the audit guards the *proofs*. Whether
   the *statement* says what was meant is left to the human, and the code says so.

## Where to start

Read [compile_correct](#/node/compile_correct) or [soundness](#/node/soundness) for a feel of the sample
output, then [runMain](#/node/runMain) for the checker.

## What this site leaves out

All the non-Lean code. Most declarations inside SafeVerify (printing, JSON, command-line parsing). The Ackermann
value lemmas one by one. The second copy of the Overleaf demo definitions (namespace `LeaDemoImplicitBinders`,
which only changes how arguments are passed, for a repair exercise). And the SafeVerify fixtures marked "Maybe",
whose expected outcome the test runner leaves undefined.
