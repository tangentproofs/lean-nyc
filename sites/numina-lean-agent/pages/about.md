# About this site

## The project

[project-numina/numina-lean-agent](https://github.com/project-numina/numina-lean-agent) is by **Project Numina**.
The README cites the paper *Numina-Lean-Agent: An Open and General Agentic Reasoning System for Formal Mathematics*
([arXiv:2601.14027](https://arxiv.org/abs/2601.14027)) by Junqi Liu, Zihao Zhou, Zekai Zhu, Marco Dos Santos,
Weikun He, Jiawei Liu, Ran Wang, Yunzhou Xie, Junqiao Zhao, Qiufeng Wang, Lihong Zhi, Jia Li and Wenda Li.

The README calls it "an agent built on Claude Code for formal theorem proving tasks". It reports that the team used
the system to prove all 12 Putnam 2025 problems and to formalize a paper on effective Brascamp–Lieb inequalities.
**Neither of those proof developments is in this repository.** The Putnam proofs are published separately in
[project-numina/Numina-Putnam2025](https://github.com/project-numina/Numina-Putnam2025), which this site did not
examine.

## What is in the repository, and what is not Lean

Most of the repository is not Lean. By file count it is about 47 Markdown files, 21 Python files (about 4,200
lines) and 19 Lean files.

- **The harness (Python, `scripts/`).** `run_claude` launches Claude Code on a `.lean` file or folder and keeps it
  going for several rounds. It checks the result after each round and records logs and statistics. Commands
  `run`, `batch` and `from-folder` are documented in tutorial/usage.md.
- **Prompts (Markdown/text, `prompts/`).** Instructions for the agent in several modes: complete a file, "medium" and
  "hard" modes, an "autosearch" coordinator with sub-agent prompts, and a blueprint template.
- **Skills (`skills/`).** Claude Code skills, backed by small Python command-line tools: Mathlib search (Leandex,
  LeanSearch, Loogle, LeanFinder, state search, premise selection), verification (local compile check, plus
  the external Axle service's verify-proof and disprove), code transforms (repair, simplify, sorry-to-lemma),
  and LLM helpers that call Gemini or GPT as an "informal prover" or "discussion partner".
- **Configs (`config/`).** Batch configurations for miniF2F and for a benchmark called LiveProveBench. The
  LiveProveBench problems themselves are not in the repository; the list in config/lists.txt points to paths on the
  authors' machine.
- **The Lean (`leanproblems/`).** A small Lake project, pinned to Lean v4.26.0 and Mathlib v4.26.0, holding
  **17 problem statements**. This site is about these.

## What the Lean covers

The Lean is **input for the agent**: competition problems written as Lean theorems with the proof replaced by
`sorry`. The agent's job is to replace the `sorry` with a proof the harness accepts.

- **Putnam 2025, all twelve problems** (leanproblems/Putnam2025/). Each file states one problem. Three need their own
  definitions: [A3](#/node/putnam_2025_a3) encodes a two-player game, [A5](#/node/putnam_2025_a5) defines a
  permutation count, and [B4](#/node/putnam_2025_b4) defines a staircase matrix and its sums. All twelve proofs are
  `sorry`.
- **Five miniF2F problems** (leanproblems/Minif2f/), from the standard competition-math benchmark, with the
  informal problem in a comment. Four are `sorry`. The fifth, [amc12a_2021_p7](#/node/amc12a_2021_p7), is
  "proved" by a single `decide`, which may well not finish (see its node).
- A placeholder library file whose only content is a hello-world definition (leanproblems/Leanproblems/Basic.lean).
  It is the only thing the Lake project's default build target, and so its CI, actually compiles.

The six headlines were chosen to show the range: an analysis problem ([A2](#/node/putnam_2025_a2)), a game with
custom definitions ([A3](#/node/putnam_2025_a3)), a combinatorial characterisation ([A5](#/node/putnam_2025_a5)),
a number-theory closure property ([B3](#/node/putnam_2025_b3)), a matrix inequality ([B4](#/node/putnam_2025_b4)),
and the one statement with a proof ([amc12a_2021_p7](#/node/amc12a_2021_p7)). The other eleven statements each
have a short node too.

## How the Lean side is checked by the harness

None of this was run for this site. This is what the Python source says it does.

1. **Compile and grep.** After the agent reports it is done, `scripts/lean_checker.py` runs `lake env lean` on each
   target file, with a 60-second timeout. It marks a file as failed if the output mentions "error", or mentions
   "sorry" (unless the task allows sorry). This is a text match on compiler output, not an axiom audit.
2. **Statement tracking.** `scripts/statement_tracker.py` snapshots every theorem/lemma statement before the run. If
   the agent edits a statement, for example weakening the goal to make it easier, the harness detects the change
   and either stops ("STATEMENT_CHANGED") or restores the original statement before the next round.
3. **SafeVerify (optional).** If configured, `scripts/safe_verify.py` compiles the original sorry'd file and the
   agent's file and runs the external [SafeVerify](https://github.com/GasStationManager/SafeVerify) tool, which
   replays the submission in the kernel against the original target.
4. **Prompts.** The prompts forbid new axioms. The "medium" mode forbids `native_decide`; the "complete file" prompt
   instead *suggests* `native_decide` for computational goals. The plain compile check in step 1 would not flag
   `native_decide` or extra axioms; only SafeVerify or Axle's verify-proof would.

## Where to start

Read [A2](#/node/putnam_2025_a2) to see what a benchmark statement looks like. Then read [A3](#/node/putnam_2025_a3)
to see how much design goes into stating a game faithfully, along with the encoding question we raise there. The
[Review](#/page/review) page goes through each headline's faithfulness.

## What this site leaves out

The Python harness, prompts and skills are described only in outline. We did not evaluate the agent, its prompts,
or its benchmark results, and we did not look at the separate Putnam proof repository.
