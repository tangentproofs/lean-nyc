# NOTES for the coordinator: b4-lean

## Time

By `date`: started 07:41 UTC, finished about 07:55 UTC on 2026-10-29. That covers reading all 13 files, writing 30
nodes and 4 pages, and the build loop.

## What was built

* 30 nodes. Headlines (6): `runOp` (the interpreter, as code), `step_binop` (step-lemma family), `runN`,
  `Swarm.settle`, `Heap.alloc_scale`, `MM.code` (the allocator, as code).
* Pages: about, review (with the PROVEN / TESTED / UNPROVEN status table), trust, roadmap.
* No Lean code blocks and no verbatim Lean statements (no-licence site). The b4a assembly is quoted only as
  isolated op names.

## Engine issues and workarounds

1. **Scanner name collisions cause a failing statement-order test.** With Main.lean in `roots`, Main's
   `structure State` (scanned as `State'`) and `B4.State` depend on each other. test_statement.mjs then fails:
   "State' should come before State". examples/Inline.lean has the same problem: its `go` is confused with
   `B4.go`, so `runOp` "mentions" Inline's `go'`, which mentions `run` → `step` → `runOp`. Workaround: `roots` are
   `imp/lean/B4`, `B4.lean`, `examples/MMTest.lean` and `examples/DSLTest.lean`. Consequences:
   * the task asked for a Main.lean node, but there is none. Main.lean is covered in prose (Roadmap section 6,
     the runOp node, About);
   * line references to Main.lean and examples/Inline.lean appear as plain text, not links, because srcrefs only
     resolves files that were scanned.
   A scanner fix would be to resolve names within the declaring file's own namespace or imports first.
2. Hypotheses named `hop` in B4.Theory are reported as meaning-dependencies on the function `hop`. Harmless,
   noted on the Trust page.

## What was hard

* Deciding what B4.Theory is *about*. It is about the real interpreter (it imports B4.Basic and unfolds `step`).
  That makes the honest summary simple: single-step facts about real code, with no multi-step results yet.
* Finding the actual extra trust: there's no `native_decide`, but `bv_decide` (B4/Theory.lean line 39) relies on
  `Lean.ofReduceBool`. Every step lemma depends on it, through the register read-back.

## Where I am least sure

* **`Swarm.settle`**: the claim that the settle rule's soundness needs monotone clocks, and that a program
  can break it with `!T` or a `wi` to byte 80. This is my own analysis, not checked by Lean and not stated by the
  author. I believe it is right, but the author may consider "programs don't rewind T" part of the intended
  discipline. I say so in the caveat. Also check my reading that a machine with its debug flag set can never
  resume inside the swarm model.
* **`getVal_setVal_self` / `step_binop` caveat**: "bv_decide relies on `Lean.ofReduceBool`". This is my
  understanding of how `bv_decide` checks its LRAT certificate in current Lean. Worth a confirmation with
  `#print axioms` when someone does build.
* **`step_binop`**: the list of instructions without lemmas (dv md sh du sw ov zp rb wb lb rs ls hp nx io db, ^R,
  +R). I compiled it by hand from the `runOp_*` / `step_*` names. An omission is possible.
* **`MM.alloc_cells`**: I wrote that 12 and 16 reduce to 4·3 and 4·4 by computation. The proof is a direct term
  application of `alloc_scale`, so it relies on definitional unfolding of numerals. Not built.
* **`runOp`**: "52 b4-tests pass" is taken from commit 344ccce and wasn't re-run. Also, the 52 tests go through
  Main.lean's own assembler, not `B4.Asm.assemble`. I'm confident in that from reading Main.lean, but it is easy to
  misstate.
* **`MM.blocks`**: the frequency "about a third frees" is approximate. The rule is `g % 3 = 0` with a non-empty
  live list.

## Things the author might object to

* Labelling `runOp` and `MM.code` as headlines although they are code, not theorems. The task asked for the
  interpreter as a possible headline, and MM.code carries the TESTED status prominently.
* The settle/clock-monotonicity remark (see above).
* The note that every `#eval` test in imp/lean has its expected output only in a comment, so none can fail the
  build. That is factual, but could read as a criticism. `#guard` would make them real tests.
* The CLI's mnemonic table has `tm` for 0xBE, which `runOp` doesn't implement (Main.lean line 58). Mentioned as a
  likely leftover.

## Licence

No LICENSE file in the repo, and the README states no licence, so the site is no-licence. `ownProject: true` was
left as given.
