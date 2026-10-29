# About this site

## The project

[BasisResearch/ship-your-interpreter](https://github.com/BasisResearch/ship-your-interpreter) is by **Kiran
Gopinathan** at **Basis Research**. Its README begins: "This Lean 4 project verifies `c/while-riscv-htif.elf`,
a WHILE-language interpreter written in C and compiled to bare-metal RV64."

The idea in the title: you write an interpreter in an ordinary language (here about 1,800 lines of C), compile
it with an ordinary toolchain, and then prove in Lean that **the shipped binary** implements a formal semantics
of the language it interprets. The proof never mentions C. It works on the bytes of the ELF, run on the
Sail-generated RISC-V ISA model.

The repository contains:

- `c/`: the interpreter's C source (lexer, parser, tree-walking evaluator, environments, values, HTIF
  console), its Makefile and linker script, test programs `c/tests/*.wl`, and the committed ELF;
- `Vsa/`: the WHILE AST, its big-step, error and cost semantics, a type system with checker and inference, an
  abstract interpreter, the machine model, the memory-layout relation, boot witnesses, and verified compilers
  from WHILE to RV64;
- `VsaIris/`: an Iris-style program logic for the machine (using
  [iris-lean](https://github.com/leanprover-community/iris-lean)) and the proof about the interpreter's binary;
- `riscv-lean/`: vendored Sail-generated RV64 models, a Lean emulator and `lean-sail`;
- `abstractions/`: notes, one per "round", on how each proof layer was chosen and measured. They describe
  proof work done by AI agents (for example abstractions/ROUND-1.md, abstractions/ROUND-4-iris.md).

## Size

About 175,700 lines of Lean in 822 files belong to the project itself: `Vsa/` about 66,000 and `VsaIris/` about
109,400. The vendored `riscv-lean/` adds about 246,000 lines in 291 files, almost all of it generated. That makes
roughly 420,000 lines in total.

## What this site covers

The site follows **one thread**: how the main theorem
[endToEnd_refinement](#/node/Vsa.Sim.EndToEnd.endToEnd_refinement) is proved. Start with the
[Roadmap](#/roadmap). It lists every major lemma on the path in dependency order, with a node for each.

Headlines:

1. [endToEnd_refinement](#/node/Vsa.Sim.EndToEnd.endToEnd_refinement): the binary halts cleanly with output
   `out` exactly when the program's big-step result is `out`, and divergence rules out a result.
2. [endToEnd_trichotomy](#/node/Vsa.Sim.EndToEnd.endToEnd_trichotomy): failures line up too (exit 70 or 1,
   or divergence, exactly for source errors or divergence).
3. [while_halts](#/node/Vsa.Sim.Boot.while_halts): the theorem applied to a concrete traced boot state, giving
   the output of a real test program.
4. [endToEnd_checked](#/node/Vsa.Sim.EndToEnd.endToEnd_checked): the program assumptions replaced by checkers.

## What this site leaves out

The repository proves much more than this thread. The site does not explain:

- the **type system** (`Vsa/While/Type*.lean`): type preservation and soundness, a decidable checker and
  complete inference, and type safety stated for the binary (`VsaIris/Interp/TypeSafety.lean`);
- the **abstract interpreter** (`Vsa/AbsInt/`): soundness of the analysis and of the allocation-cost bound,
  except as used by `endToEnd_checked`;
- the **source-level program logic** (`VsaIris/WhileLogic/`): a WP calculus for WHILE with adequacy down to the
  machine;
- the **verified compilers** (`Vsa/Compiler/`): three WHILE-to-RV64 compilers with the same refinement property;
- the thousands of **per-routine proofs** (allocator paths, `snprintf`, newlib, environment helpers) under
  `VsaIris/Vsa/` and `VsaIris/Interp/`, beyond how they are collected;
- the **Sail model** itself.

The README's "What is proved" table lists these results with their files.

The engine scanned `Vsa/` and `VsaIris/` (about 13,100 declarations) to build the proof graph and source
index. It did not scan `riscv-lean/`.
