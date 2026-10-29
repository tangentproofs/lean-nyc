# NOTES for the coordinator (lea)

## Time spent
About 10 minutes of wall-clock time by the session's timer (start/end timestamps in my scratchpad). That covers
reading all 33 `.lean` files (~1,360 lines), the README files, and the relevant Python glue (safeverify.py,
tools.py, result_selection.py), writing 33 nodes and 3 pages, and four build iterations.

## What the project is, and the calls I made
- **Lea is an agent/tooling monorepo, not a proof development.** The Lean is: 4 sample "generated" proofs in
  `prover/examples/`, a vendored SafeVerify (with test fixtures), a Lean metaprogram `LibraryInspect.lean`, an
  Overleaf-demo reference file, and two retry-test fixtures. No benchmark problem sets (the README says the evals
  live in a separate repository). This is stated on the home lead, About, Review and Trust pages.
- **Headlines (5):** `soundness` (Logic.lean), `compile_correct` (StackMachine.lean), `ack_mono_and_gt` and
  `ackermann_4_1` (Ackermann.lean, the README's worked example), and `runMain` (SafeVerify's checking pipeline,
  explained as "how the Lean side is checked"). `runMain` is a **program**, not a theorem. Its node says so, and
  its "walkthrough" is the algorithm outline.
- **Demo disproof is not a headline,** because `docs/lea-overleaf-demo/reference/reference-proofs.lean` has a
  lower-case file name, which the engine's line-link regex can't link (it needs a capital first letter). I
  linked it with hand-written GitHub URLs at the pinned SHA. Engine limitation worth noting: lower-case and
  hyphenated `.lean` file names never get line links or walkthrough-title links.
- **Roots** include the SafeVerify test fixtures (needed for the `falseThm` / `efsq` nodes). The scanner
  disambiguates repeated names with primes (`falseThm'`, `efsq'`, `eval'`). `eval'` is the StackMachine
  `eval`, and I explain it under that id and say why on the node and the Trust page.
- **Licence:** no LICENSE at the repo root and none stated in the README. **But the vendored
  `third_party/SafeVerify/` has its own Apache-2.0 LICENSE.txt** (upstream GasStationManager/SafeVerify), and
  `apps/overleaf-extension/extension/vendor/katex/` has KaTeX's licence. I kept the site-wide no-licence policy
  (no code, no verbatim statements, no `lean:` fields) for everything, including SafeVerify. The coordinator
  may decide whether SafeVerify excerpts could be shown under Apache-2.0. I didn't change `license`.
- **Authors:** kept as given. The README names no individuals. The git log is mostly darturi (Daniel Aarão Reis
  Arturi) and shaswatpatel123 (Shaswat Patel). SafeVerify is credited to GasStationManager on its nodes and the
  About page.

## Places I'm least sure of (node id + why)
- **runMain / About "three levels of checking":** I describe Lea's checks as (1) compile with no error and no
  sorry warning, (2) an axiom whitelist at result selection (result_selection.py 108–123, via
  LibraryInspect), and (3) opt-in SafeVerify. I read those functions but did not trace every call path in the
  ~large Python agent. There may be other checks (for example in the adapter or worker) that I missed. If so,
  "weaker" wording in runMain and review.md could understate Lea's checking.
- **Review page: "not designed to catch environment hacks".** This is my inference that levels 1–2 run in the
  compile-time environment (the inspector is appended to the file and compiled with it). I didn't confirm it
  by running anything.
- **compile_correct caveat:** I flag that `simp …; rfl` (lines 55–56, 58–59) only works if simp leaves exactly
  one goal. I believe it does (exec isn't in the simp set), but without a build I can't be sure the file
  compiles as written.
- **ackermann:** I say Lean finds a lexicographic well-founded termination argument automatically (no
  `termination_by` written). I'm fairly confident (structural recursion on either argument fails because of
  the nested call), but I didn't build it.
- **ackermann_4_1:** I say direct kernel evaluation is impractical (WF definitions don't reduce well, and
  ~2.9 billion calls). This is standard folklore. I didn't test it, and the node says so.
- **efsq / falseThm:** I explain *why* the replay defeats each attack (fresh environment from imports only).
  The test runner expects Bad files to fail, but I didn't run it. The exact failure point (replay vs. the
  later kernel re-check) could differ from my description.
- **equivThm / OverwrittenTypeclass:** my explanation (the extra `NeZero` instance changes the elaborated
  statement) follows the fixture's own docstring. I didn't elaborate it.
- **Proof (Logic.lean):** I state that ¬¬x → x is not derivable (the standard intuitionistic fact). The node
  says this site didn't check it in Lean.

## Things the authors might object to
- The lead and Review say plainly that, **in Lea's integration, SafeVerify's target is derived from the
  submission, so a weakened statement passes.** This is taken from the upstream docstring (safeverify.py
  lines 9–17), but foregrounding it on the home page could read as criticism.
- Calling most of the repository "not Lean" and summarizing the Lean as ~1,360 lines may undersell a project
  whose value is in the agent and UI. The About page describes those parts, but doesn't explain them.
- I note that `third_party/README.md` says SafeVerify was pinned to v4.28.0 while the files say v4.29.0
  (looks stale).
- The `examples/` proofs are described as "agent-generated samples", based on the README ("See examples/ for
  generated proofs"). No run logs are in the repository, so I can't confirm how they were produced, and I say so.

## Engine notes
- Lower-case `.lean` file names (`reference-proofs.lean`, `helper-baseline.lean`, `test_proof.lean`) can't be
  line-linked. Worked around with explicit GitHub links.
- Remaining build warnings (21) are unexplained SafeVerify helpers (CLI parsing, printing, replay helpers) and
  individual Ackermann value lemmas. All minor. The Ackermann lemmas are covered collectively in the
  `ackermann_4_1` and `ack_zero` nodes.
