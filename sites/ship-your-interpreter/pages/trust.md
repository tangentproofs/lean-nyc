# Trust: what was and wasn't checked

## Not built

**The Lean was not built for this site.** No `lake`, `lean` or `elan` was run. The README says a full build is
long. On this site, "proved" means the file contains what looks like a complete proof, not that Lean's kernel
accepted it. The repository has 62 `#print axioms` commands. The README states that every listed theorem
depends only on `propext`, `Classical.choice` and `Quot.sound`. That claim was **not** re-checked here.

## Gaps, axioms and escape hatches

A text search of the project's own Lean (`Vsa/`, `VsaIris/` and the root files, 822 files) at the pinned commit:

| What | Count | Notes |
|---|---|---|
| `sorry` | 0 | |
| `admit` | 0 | |
| `axiom` declarations | 0 | |
| `native_decide` | 0 | Computation is checked with `decide +kernel` (109 uses), which the kernel itself evaluates. |
| `implemented_by`, `extern` | 0 | |
| `opaque` | 0 as a keyword | The word appears once in a comment (Vsa/Compiler/R6Row.lean line 13). |
| `unsafe` | 11 | All in metaprograms that run during elaboration to *propose* data or proof terms, for example `boot_witness` (Vsa/Sim/Boot/WitnessCmd.lean lines 23–25) and the symbolic front end (VsaIris/Interp/SymFront.lean line 283). The kernel checks the results, so they are not trusted. |
| `partial def` | 57 | Program code: the unverified WHILE parser (Vsa/While/Parse.lean) and tooling. Nothing on the main theorem's path. |

In the vendored `riscv-lean/` (about 246,000 lines):

- `sorry` once, inside commented-out code in the emulator
  (riscv-lean/lean_emulator/LeanRiscv.lean line 40). It has no effect.
- `axiom` 75 times, all in riscv-lean/Lean_RV64D/LeanRV64D/RiscvExtras.lean. That file belongs to the
  **non-executable** model copy `Lean_RV64D`. The project imports the executable copy
  `Lean_RV64D_executable` through `lean_emulator` (riscv-lean/lean_emulator/lakefile.toml lines 16–18), and
  that copy declares no axioms. This site checked the imports by reading only. A build plus `#print axioms`
  would confirm it.

## What the main theorem trusts

1. **The Sail RISC-V model** in `riscv-lean/`, as the meaning of the machine. It is generated from the official
   Sail specification, and its fidelity to hardware is outside the proof.
2. **The ELF bytes.** The proofs are about the committed `c/while-riscv-htif.elf`. Nothing proves that it was
   compiled from `c/src/`. The C source is documentation of intent. The README warns that a rebuild "can
   produce different bytes".
3. **The hypothesis `Loaded`.** The theorem starts at the entry of `interp_run` with the AST in memory. Reset,
   `crt0`, `main` and the **C parser** are not covered. `Loaded` also contains two program assumptions:
   heap `capacity` and `stack_admissible`. They are discharged by checkers in
   [endToEnd_checked](#/node/Vsa.Sim.EndToEnd.endToEnd_checked).
4. **Boot traces** (for the concrete `*_halts` theorems only). According to the README, two links are not
   kernel-checked: that loading the ELF gives the witness's initial memory, and that the traced boot is the
   machine's own. The scripts that checked them and the witness generator are not in the repository.
5. **The specification `BigStep`.** The theorem shows the binary agrees with this semantics. Whether the
   semantics is the intended WHILE is a human judgement. The author has said in a talk that the semantics was
   written with an LLM. See [Review](#/review).
6. **iris-lean** (pinned at rev 740e2c4) for adequacy and the proof mode, plus Lean's kernel and its standard
   library.

What it does **not** trust: the C compiler, the C semantics, newlib's source, the witness generator or the
symbolic executor's code. Their outputs enter only through kernel-checked proofs.

## Not proved

- Anything about the C **parser**: the theorem takes the AST as given.
- Behaviour from **power-on** to `interp_run`: only traced, not proved.
- Programs that exceed the **heap or stack** budget. They are outside `Loaded`.
- The `repl_mode` path of `interp_run`. `Loaded` fixes `repl_mode = 0` (Vsa/Sim/LayoutInstance.lean line 52).
- The parsers and ELF writer of the `whilec` and `whilecheck` executables. The README says these are not
  verified.

## Declarations

All 13,141 declarations were found by scanning the source text of `Vsa/` and `VsaIris/` (`extracted: false`),
not from a compiled build, so some dependency links may be missing or wrong. Names created by commands, such as
`boot_witness`'s `loaded` theorems in Vsa/Sim/Boot/Gen/, are invisible to the scanner. Because the repository has
no licence, the site does not publish its source. Every line reference links to GitHub at the pinned commit.

## The explanations

Every explanation, quiz and caveat on this site was written by an AI (Claude) from the public source. None has
been reviewed by a human or by the project's author. All nodes are marked `review: draft`.
