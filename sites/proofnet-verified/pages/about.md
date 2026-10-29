# About ProofNet-Verified

## What it is

**ProofNet-Verified** (ProofNet-V) is a benchmark for AI systems that do mathematics in Lean. It is by One An,
Marcus J. Min, Xujie Si and Osbert Bastani, and is described in their paper *Ground False: Dissecting Errors in
Formal Mathematics Benchmarks* (AI for Math Workshop, 2026). It builds on two earlier datasets, which the README
credits:

- **ProofNet** (Azerbayev et al.): 371 exercises from undergraduate textbooks, each with an informal statement,
  an informal proof and a formal statement (originally in Lean 3);
- **ProofNet#**: a cleaned Lean 4 version of ProofNet.

The benchmark is used in two ways:

1. **Theorem proving.** A system is given a Lean statement and must replace `sorry` with a proof that Lean accepts.
2. **Autoformalization.** A system is given the informal statement and must write the Lean statement, which is
   then compared with the reference one.

Both uses rely on the reference Lean statements meaning what the textbook says. The project's main finding is
that very often they did not.

## What the project did

From the README:

- dropped 4 of ProofNet's 371 problems whose informal and formal statements didn't match, leaving **367**;
- moved the Lean environment forward (now Lean and Mathlib v4.34.0, with an archived Lean 4.28 snapshot), partly
  so that newer automation (`grind`, Canonical, Lean-SMT) can be used;
- **audited** every formal statement against its informal one and found errors in **205 of 367 (55.9%)** ProofNet
  statements and **99 of 367 (27.0%)** ProofNet# statements;
- confirmed each error, for instance by proving the negation of a false statement, or by giving a trivial proof
  of a statement that is true but says the wrong thing;
- **corrected** every error and, the authors report, **wrote a formal proof of all 367** corrected statements.
  Human reviewers and an AI agent checked that the corrections are faithful.

## What is Lean here, and what is not

**Lean:**

- `proofnet-verified-latest/`: 367 files `proofnet-1.lean` … `proofnet-367.lean`. Each has Mathlib imports, in 19
  cases a few [helper definitions](#/node/countably_compact), the informal statement as a comment, and **one
  theorem whose proof is `sorry`**. The one exception is
  [problem 35](#/node/Dummit_Foote_exercise_1_6_4), which ships a full proof. This is the folder this site scans.
- `data/archive/proofnet-verified-4.28/`: the same statements for Lean 4.28. Only four files differ, by Mathlib
  renamings such as `IsSolvable` becoming `Group.IsSolvable`.
- `data/proofnet/proofnet-4.28/`: the **original** ProofNet statements ported to Lean 4.28, kept for comparison.
  This site links to them as "original proofnet-N.lean" on GitHub.
- `data/archive/proofnet-verified_gt-4.28.zip`: the ground-truth **proofs**, zipped "to avoid data
  contamination". **This site did not open it.**

**Not Lean:**

- `error_taxonomy/`: one JSON audit record per problem, for ProofNet and for ProofNet#. Each gives a
  faithfulness verdict (faithful, weaker, stronger, incomparable, or a problem with the informal source), a
  provability verdict (true, false, independent), a root cause (eight categories, such as *missing implicit
  premise* or *misunderstanding of Mathlib*) and a written justification. The records include timing and cost
  fields, which suggests the justifications were drafted by an AI agent, in line with the README's description of
  the review.
- `data/*.jsonl`: the dataset in machine-readable form (informal statement, formal statement, informal proof).
- `scripts/`: Python. `verify_compilation.py` runs `lake env lean` on every statement file in parallel and flags
  any warning other than the expected "declaration uses sorry". `generate_jsonl.py` rebuilds the JSONL files.
- `docs/index.html`: the web viewer of all errors and corrections.

## How the Lean side is checked

For a benchmark *statement*, "checked" means it **type-checks** (Lean accepts it as a well-formed proposition
with `sorry` as its proof). That says nothing about whether it is true or faithful. The audit adds those checks,
and the ground-truth proofs (in the zip) are the evidence that each corrected statement is true. For solvers, the
README recommends Lean's `comparator` tool to check that a submitted proof really proves the given statement.

None of this was run for this site. See [the trust page](#/trust).

## What this site covers

- **Six headlines**: [a typical faithful problem](#/node/Artin_exercise_2_2_9) and five
  corrected ones, each showing a different root cause:
  [a missing implicit premise](#/node/Artin_exercise_11_4_8),
  [a misreading of Lean syntax](#/node/Axler_exercise_5_20),
  [a Mathlib convention](#/node/Axler_exercise_6_7),
  [a misused Mathlib name that compared types](#/node/Rudin_exercise_1_5), and
  [the wrong group](#/node/Dummit_Foote_exercise_1_6_4) (the problem that ships a proof).
- **Ten group nodes**, one per source book (Artin, Axler, Dummit–Foote, Herstein, Ireland–Rosen, Munkres, Pugh,
  Putnam, Rudin, Shakarchi), each with one representative problem and that book's error counts.
- [The problem with a wrong informal source](#/node/Rudin_exercise_4_8a), [helper definitions](#/node/countably_compact)
  and [one scanner artefact](#/node/I).

**Left out:** the other ~350 problems individually. Each is a short, self-contained statement; the source browser
lists them all, and the project's own viewer (marcusm117.github.io/ProofNet-Verified) shows every error next to
its correction.

## Where to start

Read [the first headline](#/node/Artin_exercise_2_2_9) for the format, then any of the error stories. The
[review page](#/review) collects this site's own observations.
