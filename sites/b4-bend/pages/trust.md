# Trust: what was and wasn't checked

## Nothing was built or run

No Bend, Lean, C or JavaScript in this project was compiled or run for this site. In particular:

* `bend PROOF.bend` (the project's `make check`) was **not** run, so "CHECKED-BY-BEND" means: PROOF.bend has a
  complete-looking proof for every one of the 94 laws, and the project's own `make check`, called by
  `imp/test-bend` and required by AGENTS.md before commits, runs Bend's checker on it. The repository has no log
  of such a run at this commit.
* The tanco suites (b4-tests.org, imp/bend/tests.org) were **not** run. "TESTED" means the project's test script
  runs them.
* The demos (swarm, Mandelbrot, live shell, fleet test) were **not** run. Expected outputs given on their pages
  are worked out by hand.
* One file was inspected with a tool: the committed mandelbrot.png was decoded with Python's zlib to confirm it is
  a well-formed 4,096 × 1,024 greyscale PNG whose grey levels match the code. That says nothing about which
  commit produced it.

## There is no Lean here

The engine behind this site scans Lean files. `imp/bend` has none, so every node is a *concept* node with a link
to a GitHub line range, and no node has a formal statement extracted by the engine. The usual counts of `sorry`,
`axiom` and `native_decide` don't apply.

## The Bend equivalents of those counts

* **Escape hatches.** `@unsafe` (which turns off Bend's termination check, and which the Bend guide says makes a
  check report SOME PROOFS FAIL for anything relying on it) appears only on the console input loop
  ([b4i.bend line 410](src/imp/bend/b4i.bend.html#L410))
  and the live-shell loop
  ([live.bend line 277](src/imp/bend/live.bend.html#L277)).
  Neither file is imported by PROOF.bend. There is none in vm.bend, LAWS.bend or PROOF.bend.
* **Unproved laws.** None: LAWS.bend has 94 `law`s and PROOF.bend has 94 matching `L.` definitions.
* **Trusted kernel.** The Makefile runs plain `bend PROOF.bend`. The Bend guide describes a `--verdict` flag that
  rechecks proofs with a small kernel; it is not used here, so the trust base is Bend's ordinary checker, and
  (per the guide) its parser and translation.
* **Host code.** poll_stdin.c and poll_stdin.js are outside any check. They are only used by the live shell.

## Sources for Bend's semantics

What `law`, `for`, `{a == b : T}`, `{==}`, `%`, `+x`, `&2`, `Array` sizes and the `!` parallel call mean was
taken from the Bend guide ([bendlang/bend, guide/GUIDE.md](https://github.com/bendlang/bend/blob/main/guide/GUIDE.md)),
read on 2026-10-29, not from this repository. The guide may describe a newer or older Bend than the one this
commit was written against.

## The explanations

Every explanation, quiz and caveat here was written by an AI (Claude) from the source at the pinned commit.
None has been reviewed by a human or by the author. All nodes are marked `review: draft`. The disassembly of the
Mandelbrot bytecode and the hand-worked demo outputs are the parts most likely to contain slips.
