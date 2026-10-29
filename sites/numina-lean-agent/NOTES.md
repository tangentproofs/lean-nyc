# NOTES for the coordinator (numina-lean-agent)

## Time

About 10 minutes of wall-clock time by the system clock (2026-10-29, 06:05 to 06:14 UTC), one Claude session.

## Licence: needs a decision

`site.json` says `spdx: null` (no LICENSE file), and I left it that way as AUTHORING.md says. **But the upstream
README's last section says "MIT License".** There is no LICENSE file at the pinned commit. If you decide the README
line is enough, switching to MIT would allow walkthrough `lean:` snippets. I followed the no-licence rules
throughout: no Lean code blocks, no verbatim statements, no `lean:` fields.

## Calls I made

- **Scope.** The repository is mostly Python, prompts and skills; the Lean is 17 sorry'd benchmark problem files
  (12 Putnam 2025, 5 miniF2F) plus a hello-world placeholder. I scanned only `leanproblems/Putnam2025` and
  `leanproblems/Minif2f` and wrote a node for every declaration (29 nodes: 18 theorems, 11 definitions). About
  explains the non-Lean parts in outline only.
- **Headlines.** A2, A3, A5, B3, B4 and amc12a_2021_p7, chosen for variety. amc12a_2021_p7 is the only one with a
  proof. Five of the six are PARTIAL (sorry), as benchmark statements.
- **Walkthroughs for sorry'd headlines.** There is no proof to outline, so each walkthrough explains how the
  statement is built and what a proof must supply, and ends with a step pointing at the `sorry` line. I gave a short
  informal idea only where I was confident (A2, amc12a). I deliberately did not sketch solutions for A3/A5/B3/B4.
- **Authors.** Expanded `authors` to "Project Numina" plus the 13 paper authors from the README citation, and set
  `authorUrl` to the GitHub org.

## Engine issue (worked around, not fixed)

`engine/tools/srcrefs.mjs` only auto-links `.lean` file names whose basename starts with a capital letter. Every
problem file here is lower-case (`putnam_2025_a1.lean`), so no line reference would link. Workaround: helper
`nodes_src/_common.py` writes explicit GitHub links at the pinned commit (`ln()`), and checks each range against the
submodule source so a bad range still fails the build. Quiz explanations and walkthrough steps use plain-text
references (`txt()`, also range-checked); walkthrough text is HTML-escaped, so links are impossible there anyway.
Also, `write_nodes.py` loads every `.py` in nodes_src including `_`-prefixed helpers and reads their `NODES`. So the
helper keeps an empty `NODES`, and each node file builds its own list via `node_maker`. This contradicts the brief's
"files starting with `_` are helpers", which suggests they are skipped.

## Where I'm least sure

1. **`State.validNext` / `putnam_2025_a3`: the modulo-3 wrap-around.** I claim the move rule's arithmetic
   (a `Fin 3` digit plus an integer ±1, putnam_2025_a3.lean line 13) elaborates in `Fin 3`, so 2+1 = 0. That rests on
   my reading of Lean's `binop%`/`binrel%` elaboration: the "max type" starts at the first leaf (`Fin 3`), and ℤ
   coerces into `Fin 3` via `IntCast`. Not verified by a build. If instead it elaborates in ℤ with the digits cast, the
   encoding is faithful and the Review section on A3 is wrong. The site hedges ("probably", "our reading"), but this
   is the headline claim most likely to be wrong, and the one the authors would most want to see.
2. **`amc12a_2021_p7`: whether `decide` finishes.** I say it probably times out (kernel trial division up to about
   2×10⁷). I'm fairly but not fully confident. Kernel Nat operations are GMP-accelerated, but the `Finset.filter` over
   `range` still needs millions of reduction steps, and `decide` must first evaluate the `Decidable` instance. If the
   authors ran it and it checked, that caveat is wrong. Separately, I vaguely recall that miniF2F's
   `amc12a_2021_p7` is a different problem (a minimum of (xy−1)² + (x+y)²). I did **not** put this on the site,
   because I'm not sure.
3. **Faithfulness of the other statements to the official Putnam 2025 texts.** I compared them with my recollection
   of the problems, not with an official source (no web access used). The A5 answer (both alternating patterns) and
   the B5 index range are the spots where my memory is weakest.
4. **The checking pipeline description (About).** This is from reading `scripts/runner.py`, `lean_checker.py`,
   `statement_tracker.py` and `safe_verify.py`, and none of it was run. "Text match on compiler output" is accurate
   for `lean_checker.py` lines 82–90. Exactly what SafeVerify checks comes from its docstring, not from the
   SafeVerify source.

## Things the authors might object to

- The A3 encoding concern (above). It's phrased as a possible mismatch, but it's still a critique of their
  benchmark statement.
- Saying the `decide` proof may not check.
- Pointing out that the CI only builds the placeholder library, that the "complete file" prompt references a
  non-existent `skills/cli/diagnostic.py`, and that the same prompt suggests `native_decide` while the medium-mode
  prompt forbids it. All are factual at the pinned commit, but they read as nitpicks.
- Saying the Putnam proofs and the Brascamp–Lieb formalization are "not in this repository". That's true, and
  the README links the Putnam repo, but a reader of the README's first paragraph might expect otherwise.
