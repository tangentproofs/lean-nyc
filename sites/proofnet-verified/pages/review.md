# Review: do the statements say what they claim?

ProofNet-Verified is itself a faithfulness review, so this page has two jobs: check this site's headlines
against their textbook exercises, and note what this site noticed about the benchmark as a whole. Everything here
comes from reading the source at the pinned commit. Nothing was built or run.

## The headlines

| Headline | Faithful to the exercise? | Status |
|---|---|---|
| [Artin 2.2.9](#/node/Artin_exercise_2_2_9): commuting generators give an abelian subgroup | Yes. "Abelian" is spelled out as "any two elements commute". | statement only (`sorry`) |
| [Artin 11.4.8](#/node/Artin_exercise_11_4_8): xⁿ − p irreducible over ℚ | Yes, with the implicit n ≥ 1 made explicit. | statement only (`sorry`) |
| [Axler 5.20](#/node/Axler_exercise_5_20): same eigenvectors ⇒ commute | Yes. "Same eigenvectors" is read as "eigenvector or zero", which is harmless. | statement only (`sorry`) |
| [Axler 6.7](#/node/Axler_exercise_6_7): polarization identity | Yes, **after translating conventions**. The symbols differ from the book because Mathlib's inner product is linear in the other argument. This site re-derived the sign. | statement only (`sorry`) |
| [Rudin 1.5](#/node/Rudin_exercise_1_5): inf A = −sup(−A) | Yes. The hypotheses rule out Mathlib's junk value for `sInf`/`sSup`. | statement only (`sorry`) |
| [Dummit–Foote 1.6.4](#/node/Dummit_Foote_exercise_1_6_4): ℝ× ≇ ℂ× | Yes (`ℝˣ`, `ℂˣ` are the non-zero numbers under multiplication). | **complete-looking proof in the file**, not built here |

None of the five "error stories" is this site's discovery. Each is documented in the project's audit records,
which every node links to. For each one this site read both versions and the record and agrees with the verdict.
In several cases this site supplied its own small counterexample (marked in the node's caveats).

## Observations about the benchmark

1. **One problem ships its answer.** The README says each statement ends in `sorry`, and the JSONL describes
   `formal_stmt` the same way. Problem 35 (`Dummit_Foote_exercise_1_6_4`) instead contains a full 47-line proof
   ([proofnet-35.lean lines 15–61](src/proofnet-verified-latest/proofnet-35.lean.html#L15-L61)), in both the latest
   and the archived 4.28 statement folders and in the `formal_stmt` field of `data/proofnet-verified-latest.jsonl`.
   A prover evaluated on these files is given that problem's solution. This is probably an oversight, but it
   affects scoring by one problem in 367.
2. **Two problems are now the same theorem.** Correcting problem 168 (whose informal text was impossible) turned
   it into Rudin 4.8(a), which problem 351 already was. Both are now named `Rudin_exercise_4_8a` and state the same
   fact in slightly different form ([the node](#/node/Rudin_exercise_4_8a)). Rudin's exercise has a part (b)
   (boundedness of E can't be dropped), which may have been the intent. Either way, the benchmark has 366 distinct
   theorems under 367 indices.
3. **The headline numbers check out.** Tallying the per-problem records in `error_taxonomy/` gives 205 non-faithful
   ProofNet entries and 99 non-faithful ProofNet# entries, matching the README. The faithfulness × provability
   breakdown also matches `error_taxonomy/proofnet/summary.md` (for example 75 *stronger*, 54 *weaker*).
4. **"Unfaithful" is not the same as "false".** Of the 205 ProofNet errors, 106 are provably false, 98 are
   provable but say something other than the exercise (as in [Axler 5.20](#/node/Axler_exercise_5_20) or
   [Putnam 2010 A4](#/node/Putnam_exercise_2010_a4)), and 1 is labelled independent
   ([Rudin 1.5](#/node/Rudin_exercise_1_5)). A prover that "solves" an unfaithful-but-true statement has proved a
   real theorem, just not the textbook's.
5. **The "independent" label is an argument, not a theorem.** The record for problem 150 says so itself. Nothing in
   the repository proves that the original Rudin 1.5 statement is independent.
6. **The audit justifications look AI-drafted.** Each record carries `duration_ms` and `cost_usd` fields. The README
   says humans and an AI agent reviewed the corrections until they agreed. This site did not try to check that
   process. It spot-checked about 20 records against the two Lean versions and found nothing it disagreed with.
7. **The proofs were not inspected.** The authors keep the ground-truth proofs in a zip to avoid data contamination.
   This site respected that, so it cannot confirm that every corrected statement has a proof. The README says so,
   and the zip lists 367 files.

## What would make the statements stronger or weaker

Not applicable in the usual sense: these are fixed benchmark targets, and the question is whether each matches
its exercise. The project's answer, which this site has no reason to doubt from what it read, is that after
correction all 367 do. Problem 168 is the exception noted above: it matches Rudin 4.8(a) rather than what
ProofNet's text originally asked for.
