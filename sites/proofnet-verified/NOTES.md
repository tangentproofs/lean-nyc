# NOTES for the coordinator (proofnet-verified)

## Time spent
About 15 minutes of wall-clock time by the session's own timer, from the first command to the commit: reading the
README and structure, sampling about 20 problems in both versions plus their audit records, writing 19 nodes and
3 pages, and about 6 build iterations. The failures were schema limits (title ≤ 80 characters, quiz explanation
≥ 10 characters).

## What the project is, and the calls I made
- **It is a benchmark, not a proof development.** 367 single-theorem files, all `sorry` by design except one.
  The lead, About, Review and Trust pages say so plainly, and every sorry'd node carries a "PARTIAL (sorry) by design"
  caveat.
- **Headlines (6):** one typical faithful problem (`Artin_exercise_2_2_9`, the README's own example) plus five
  corrected problems, chosen so that each shows a different root cause: missing implicit premise
  (`Artin_exercise_11_4_8`), Lean precedence (`Axler_exercise_5_20`), Mathlib convention (`Axler_exercise_6_7`),
  misused Mathlib name giving the audit's only "independent" verdict (`Rudin_exercise_1_5`), and wrong group
  (`Dummit_Foote_exercise_1_6_4`, the one file that ships a proof).
- **Grouped nodes:** node ids must be declarations, so each of the 10 source books has one node anchored on a
  representative problem. The title says "Group: the X problems (n)" and the body gives the book's error counts,
  which I tallied from `error_taxonomy/*/per_file/*.json`. One node each covers the problem with a wrong informal
  source (`Rudin_exercise_4_8a`), the helper definitions (anchored on `countably_compact`), and `I` (needed because
  the scanner falsely links the polarization headline's `I` to it).
- **Roots:** only `proofnet-verified-latest/`. Scanning the archive and the originals too would triple every
  theorem name. Original statements are linked on GitHub instead.
- **Line references:** the engine's auto-linker only recognises file names that start with a capital letter
  (`srcrefs.mjs` regex), and every file here is `proofnet-N.lean`. **Engine limitation, worked around:** I wrote
  `nodes_src/_common.py` with an `R()` helper that expands `[[L n a-b]]` / `[[O n a-b]]` / `[[T n]]` / `[[S n]]`
  into explicit Markdown links (rendered source, original on GitHub, audit records). It **checks every range
  against the file length** and fails the build if one is out of range, the same guarantee the engine gives.
  Walkthrough `lean:` fields are located by the engine as usual. Links in the three pages are written by hand
  (only two, both checked).
- **Ground-truth proofs zip: deliberately not opened.** The authors zip the proofs "to avoid data contamination".
  Quoting them on a public page would undo that, so walkthroughs for sorry'd headlines show the Lean statement
  lines plus the dataset's *informal* proof (which is public in the JSONL), clearly labelled as such. I only
  listed the zip's file count (367).
- **Authors:** site.json now credits One An, Marcus J. Min, Xujie Si and Osbert Bastani (the authors of the
  *Ground False* paper cited in the README), building on ProofNet (Azerbayev et al.) and ProofNet# (Poiroux et
  al.). All commits in the repo are by marcusm117. Please check that you're happy with the authors string. It is
  longer than most.
- **Licence:** Apache-2.0 with a LICENSE file, which matches site.json. Short `lean:` quotes are used in walkthroughs.

## Places I'm least sure of
- **`Rudin_exercise_4_8a` (problem 168):** I say ProofNet's wrong text "looks like a garbled version of" Rudin
  4.8(b), and that the correction made it a duplicate of problem 351. The duplicate is a fact (same name, same
  content). The 4.8(b) intent is my guess, flagged as such in a caveat.
- **`Herstein_exercise_2_3_17`:** the claim that `[Mul G] [Group G]` makes `*` resolve to the unrelated `Mul` is
  the audit's. I didn't run Lean to confirm instance resolution, and I hedged in a caveat.
- **`Rudin_exercise_1_5`:** the explanation of `Min A` as "the type of binary min operations on A" follows the
  audit record and my understanding of Mathlib's `Min` class. I'm confident, but haven't verified it against
  Mathlib v4.34.
- **`Axler_exercise_6_7`:** I re-derived the sign by hand (Re/Im of ⟨u, ±iv⟩ under second-slot linearity). It
  matches the audit and the corrected statement.
- **`Ireland_Rosen_exercise_18_4`, `Axler_exercise_5_4`, `Pugh_exercise_2_57`:** the small counterexamples (0 = 1³ +
  (−1)³ = 2³ + (−2)³; S = 0; touching discs) are mine and are marked as such.
- **The book titles** (Herstein *Topics in Algebra*, Ireland–Rosen *A Classical Introduction to Modern Number
  Theory*, Pugh *Real Mathematical Analysis*, Stein–Shakarchi *Complex Analysis*) come from my knowledge of
  ProofNet's sources. The repository only gives short names such as "Herstein".
- **"The audit justifications look AI-drafted"** (review page, item 6): an inference from the `duration_ms` /
  `cost_usd` fields together with the README's mention of an AI agent. Worded as "look" and "suggests".

## Anything the authors might object to
- **Review item 1: problem 35 ships its proof**, contrary to the README's "ends with `sorry`". It is stated
  neutrally ("probably an oversight"), but it is a public note that the benchmark leaks one answer.
- **Review item 2: the 168/351 duplicate**, i.e. 366 distinct theorems under 367 indices.
- **The "independent" verdict** for problem 150 is described as the audit's own metatheoretic judgment, quoting the
  record's own caveat. I think that is fair, but it draws attention to a soft spot.
- **Per-book error counts** are my tallies, not numbers the authors published. I checked that they sum to the
  README's 205 / 99.

## Engine notes (not fixed, as instructed)
- `srcrefs.mjs` can't link lower-case or hyphenated Lean file names (`proofnet-1.lean`); see above.
- `write_nodes.py` also imports `_`-prefixed files in `nodes_src/` (harmless here because `_common.py` defines an
  empty `NODES`). AUTHORING.md implies they are skipped.
- The scanner resolves bound variables (`f`, `g`) and opened names (`Complex.I` as `I`) to unrelated helper
  definitions in other files. That causes the remaining "needs explainer" warnings for `f`/`g`, which I left
  unexplained on purpose (documented on the Trust page).
