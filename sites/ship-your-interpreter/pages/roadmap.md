# Roadmap: how `endToEnd_refinement` is proved

This page walks the proof of the main theorem,
[endToEnd_refinement](#/node/Vsa.Sim.EndToEnd.endToEnd_refinement), from the bottom up. Each step comes
before the steps that use it. Each one gets a sentence or two, a link to its node on this site, and a link
to the exact lines on GitHub at the pinned commit.

**The theorem in one sentence.** Load a WHILE program `p`, as C structs, into the memory of the compiled
interpreter, and stop the RISC-V machine at the entry of the C function `interp_run`. Then the machine halts
with exit code 0 and output `out` **exactly when** the WHILE semantics says `p` finishes normally with output
`out`, and if the machine runs forever, `p` has no normal result.

The proof has five layers. The **source** (WHILE and its big-step semantics) and the **machine** (the
Sail RISC-V model) are specifications. The **loading relation** says how the two meet in memory. An
**abstract refinement argument** turns two simulation facts into the theorem. A large **Iris program-logic
proof about the binary** supplies those two facts.

Nothing on this page was built or run. See [Trust](#/trust).

---

## A. The source language

1. **The WHILE syntax.** A program is a list of statements. Expressions include integers, strings, booleans,
   `null`, variables, assignment, arithmetic, comparison, `and`/`or`, calls and anonymous functions.
   Statements include blocks, `if`, `while`, `for`, `return`, `break` and `continue`.
   [Program](#/node/Vsa.While.Program), Vsa/While/Ast.lean lines 17–48.

2. **The big-step semantics.** Mutually inductive relations say what an expression evaluates to, what a
   statement does to the store and output, and what a function call returns. Integers wrap at 64 bits,
   division by zero has no rule, and calls deeper than 1000 have no rule.
   [ExecSeq and friends](#/node/Vsa.While.ExecS), Vsa/While/Semantics.lean lines 192–406.

3. **`BigStep p out`.** The program, started in the initial state (three built-in natives: `print`,
   `println`, `assert`), finishes with status *normal* and has printed `out`. This is the
   specification side of the theorem. [BigStep](#/node/Vsa.While.BigStep), Vsa/While/Semantics.lean lines 410–418.

4. **A cost-counting copy of the semantics.** The same rules again, with a natural number counting heap
   allocation. Every `BigStep` derivation has a cost-annotated twin. The proof needs this to know that the
   C heap does not run out. [ExecSeqCost](#/node/Vsa.While.ExecSeqCost), Vsa/While/Cost.lean lines 273–285;
   [BigStep.cost](#/node/Vsa.While.BigStep.cost), Vsa/While/CostExists.lean lines 39–43.

## B. The machine

5. **The Sail RISC-V model (trusted).** `riscv-lean/` vendors a Lean translation of the official Sail
   RV64 specification. It is about 246,000 lines of generated Lean. This site does not explain it. The
   project treats it as the definition of what the hardware does. [stepOnce](#/node/Vsa.stepOnce) wraps one
   Sail step together with the HTIF "tohost" exit device, Vsa/Elf.lean lines 22–36.

6. **Machine runs: `Step`, `Halts`, `Diverges`.** A configuration steps when `stepOnce` succeeds and does not
   exit. `Halts c out e` means some run reaches an exit with code `e` and console output `out`.
   `Diverges c` means that runs of every length exist. Determinism follows because the Sail model is a
   function. [Halts](#/node/Vsa.Machine.Halts), [Diverges](#/node/Vsa.Machine.Diverges),
   [Halts.deterministic](#/node/Vsa.Machine.Halts.deterministic),
   [Diverges.not_halts](#/node/Vsa.Machine.Diverges.not_halts), Vsa/Machine.lean lines 18–120.

7. **Unset memory reads as zero (`fillZero`).** The Sail model reads a missing RAM byte as 0, so filling every
   missing RAM byte with 0 changes no run. This is proved by checking that *every* Sail function respects
   "equal up to missing-equals-zero" memory, a generated proof about 1,400 lines long.
   [fillZero](#/node/Vsa.Densify.fillZero), Vsa/Densify/Transport.lean lines 141–142;
   [halts_fillZero](#/node/Vsa.Densify.halts_fillZero), Vsa/Densify.lean lines 10–15;
   [Gen.stepOnce_resp](#/node/Vsa.Densify.Gen.stepOnce_resp), Vsa/Densify/GenC.lean lines 108–110.

## C. Where source meets machine: loading

8. **The AST in memory.** `ProgramRepr` says that memory holds the C structs of `c/src/ast.h` for exactly
   the program `p`: an array of statement pointers, each pointing to tagged structs, with strings as
   NUL-terminated ASCII. [ProgramRepr](#/node/Vsa.MemRepr.ProgramRepr), Vsa/MemRepr.lean lines 46–205.

9. **The machine is at `interp_run`.** `InterpRunReady` is a long list of facts about one configuration:
   the PC is at `interp_run` (0x800043ec), the argument registers point at the interpreter object and the
   statement array, the ELF's code and data bytes are in memory, the C runtime, console and allocator are
   in their initial state, and so on. It also contains the two **program assumptions**: `capacity` (the heap
   has room for every terminating run) and `stack_admissible` (the program's static stack need fits).
   [InterpRunReadyFacts](#/node/Vsa.Sim.LayoutInstance.InterpRunReadyFacts),
   Vsa/Sim/LayoutInstance.lean lines 41–205; [InitialAllocatorAt](#/node/Vsa.Sim.DlHeap.InitialAllocatorAt),
   Vsa/Sim/DlHeap.lean lines 105–110.

10. **`Loaded`.** Loaded means some address and count exist such that the AST is laid out there (8) and
    the machine is ready at those arguments (9). This is the **only hypothesis** of the main theorem.
    [Loaded](#/node/Vsa.Refine.Loaded), Vsa/Refinement.lean lines 9–13;
    [interpRunLayout](#/node/Vsa.Sim.LayoutInstance.interpRunLayout), Vsa/Sim/LayoutInstance.lean lines 204–205.

## D. The abstract refinement argument (small, language-independent)

11. **Forward simulation is enough.** The project's `OutSim` asks for two things. (i) **term_sim:** if `p`
    has a normal result with output `out`, the loaded machine halts with code 0 and output `out`.
    (ii) **stuck_sim:** if `p` has no normal result, the machine diverges or halts with a *nonzero*
    code. [OutSim](#/node/Vsa.Lang.OutSim), Vsa/Lang/Basic.lean lines 133–136.

12. **Determinism turns simulation into an "iff".** Suppose the machine halts with code 0 and output `out`.
    If `p` had some result, (i) and determinism force it to be this one. If `p` had none, (ii) contradicts
    the clean halt. If the machine diverges, `p` can have no result, because (i) would make it halt.
    [Sim.refinement](#/node/Vsa.Lang.Lang.Sim.refinement), Vsa/Lang/Basic.lean lines 51–71;
    [OutSim.refinement](#/node/Vsa.Lang.OutSim.refinement), Vsa/Lang/Basic.lean lines 149–155;
    for WHILE, [Vsa.Refine.refinement](#/node/Vsa.Refine.refinement), Vsa/Refinement.lean lines 21–25.

13. **Moving to the `fillZero` view.** The same conclusion with loading stated on `fillZero c`, using (7).
    [OutSim.refinement_fillZero](#/node/Vsa.Lang.OutSim.refinement_fillZero), Vsa/Lang/Densify.lean lines 31–38.

## E. The machine program logic (Iris)

14. **The machine as an Iris language.** The Sail step is wrapped as a `MachineModel`: a step function
    that returns *next state*, *halt with code and output*, or *stuck*. Iris resources are introduced for
    registers (`r ↦ᵣ v`), memory bytes (`a ↦ₘ b`) and the console.
    [vsaModel](#/node/VsaIris.Inst.vsaModel), VsaIris/Vsa/Instance.lean lines 15–39;
    [MachineModel](#/node/VsaIris.MachineModel), VsaIris/Machine.lean lines 15–24.

15. **Two weakest preconditions.** `twpW` is a *total* WP: it proves the code terminates. `wpW` is a
    *partial* WP that allows running forever. The interpreter proof uses the total one for terminating
    programs and the partial one for the rest. [twpW / wpW](#/node/VsaIris.MachWP),
    VsaIris/MachWP.lean lines 11–60.

16. **Adequacy.** A closed proof of a WP from the initial register, memory and console resources gives a
    real fact about the machine. From the total WP, the machine halts and its result satisfies the
    postcondition. From the partial WP, it diverges or halts with a result that satisfies it. This rests on
    iris-lean's adequacy theorems. [mach_adequacy](#/node/VsaIris.mach_adequacy),
    [mach_adequacyP](#/node/VsaIris.mach_adequacyP), VsaIris/Adequacy.lean lines 150–226;
    [vsa_adequacy_exit](#/node/VsaIris.Inst.vsa_adequacy_exit) and [vsa_adequacyP](#/node/VsaIris.Inst.vsa_adequacyP),
    VsaIris/Vsa/Instance.lean lines 80–101.

17. **The Iris route.** Simulation follows if, at each loaded configuration, you can provide initial
    resources matching the configuration, a total WP that ends at (0, `out`) for every result, and a
    partial WP that ends at a nonzero code when there is no result.
    [RouteAt](#/node/VsaIris.Lang.RouteAt), [IrisRoute.sim](#/node/VsaIris.Lang.IrisRoute.sim),
    VsaIris/Lang/Route.lean lines 29–58.

## F. The interpreter proof

18. **From `Loaded` to boot data.** Unpacking `Loaded` gives a `Boot` record: the AST address, the
    interpreter object, the arena, the initial heap chunks and so on. The `capacity` assumption, applied
    to the cost of a terminating run, gives the heap "regime" that the total proof needs.
    [boot_of_loaded](#/node/VsaIris.Interp.boot_of_loaded), VsaIris/Interp/World.lean lines 251–281;
    [Boot.regime_of_bigStep](#/node/VsaIris.Interp.Boot.regime_of_bigStep), VsaIris/Interp/World.lean lines 740–746.

19. **From raw bytes to structured ownership.** The initial bytes are split, as Iris resources, into the
    interpreter's world: heap, store representation, console, stdio state, code (read-only), AST (read-only)
    and stack. [world_of_boundary](#/node/VsaIris.Interp.world_of_boundary), VsaIris/Interp/World.lean lines 856–960.

20. **Specifications for every C function the interpreter calls.** Value helpers, environment
    lookup/define/set, `strcmp`, `strlen`, `memcpy`, `strcpy`, `snprintf`, `malloc`/`realloc`/`free`, the
    `print`/`println`/`assert` natives, the exit path, and the newlib internals they reach are each proved
    against the binary's actual instructions, with help from a symbolic executor that is proved sound once
    ([symRun_swp](#/node/VsaIris.SymExec.symRun_swp), VsaIris/Vsa/SymExec.lean lines 2087–2100). They are collected into two records, one for each kind of
    WP. [Supplies / supplies_of](#/node/VsaIris.Interp.supplies_of), VsaIris/Interp/Supply.lean lines 370–382;
    [newlibHoles_proved](#/node/VsaIris.Interp.newlibHoles_proved), VsaIris/Interp/EndToEnd.lean lines 128–130.

21. **The interpreter loop, by induction on the derivation.** For terminating runs, an induction over the
    cost-annotated derivation shows that the machine code of `eval_expr`/`exec_stmt` follows each rule.
    [interpSeqT_all](#/node/VsaIris.Interp.interpSeqT_all), VsaIris/Interp/TermSim.lean lines 372–377.
    For the partial case, Löb induction gives specifications for every statement and expression at once:
    the machine either produces the semantics' result or aborts through the runtime-error path.
    [specsP_all](#/node/VsaIris.Interp.specsP_all), VsaIris/Interp/StuckSim.lean lines 194–209.

22. **`interp_run` from its entry.** The previous pieces are put together for the top-level function:
    the prologue, the statement loop, the epilogue back into `main`, and the HTIF exit. The total version
    ends at exit code 0 with the program's output. The partial version ends at 0 with a big-step result,
    or at code 70 or 1. [interpRun_total_top](#/node/VsaIris.Interp.interpRun_total_top),
    [interpRun_partial_top](#/node/VsaIris.Interp.interpRun_partial_top),
    VsaIris/Interp/TopEntryBoot.lean lines 121–143.

23. **The obligations at one loaded configuration.** `routeAt_of_boot` fills in (17) for this interpreter:
    the resources from (19), the total WP from (21)+(22), and the partial WP from (21)+(22).
    [routeAt_of_boot](#/node/VsaIris.Interp.routeAt_of_boot), VsaIris/Interp/EndToEnd.lean lines 47–80.

24. **The simulation.** (23) for every loaded configuration, put through (17), gives `OutSim` for `BigStep`
    at `Loaded interpRunLayout`. [interpSim_iris](#/node/VsaIris.Interp.interpSim_iris),
    VsaIris/Interp/EndToEnd.lean lines 132–134.

## G. The theorem

25. **`endToEnd_refinement_loaded`** is (12) applied to (24).
    [node](#/node/Vsa.Sim.EndToEnd.endToEnd_refinement_loaded), VsaIris/Interp/EndToEnd.lean lines 153–157.

26. **`endToEnd_refinement`** is (13) applied to (24), so the loading hypothesis is stated on the
    zero-filled configuration. [node](#/node/Vsa.Sim.EndToEnd.endToEnd_refinement),
    VsaIris/Interp/EndToEnd.lean lines 159–163.

## H. What builds on it

- [endToEnd_trichotomy](#/node/Vsa.Sim.EndToEnd.endToEnd_trichotomy) adds the failure side: every nonzero
  exit is 70 or 1, and the machine fails or diverges exactly when the program errs or diverges.
- [endToEnd_checked](#/node/Vsa.Sim.EndToEnd.endToEnd_checked) replaces the two program assumptions with
  checkers you can run: a static allocation-cost bound and a stack check.
- [while_halts](#/node/Vsa.Sim.Boot.while_halts) and its siblings apply the theorem to concrete boot states
  traced from the ELF. Those states are `Loaded`, as the kernel checks with the boot witnesses.

## What is trusted, and what is not proved

- **The Sail RISC-V model** (`riscv-lean/`) is the meaning of "the machine". If it differs from real
  hardware, the theorem is about the model.
- **The ELF.** The proofs are about the committed bytes of `c/while-riscv-htif.elf`, not about the C
  source. The C compiler is not verified and does not need to be. But nothing proves that this ELF came
  from this C.
- **Loading.** The theorem starts *at the entry of `interp_run`*, with the AST already in memory.
  Reset, `crt0`, `main`, reading the script and the C **parser** are not covered by
  `endToEnd_refinement`. For ten test programs, the boot witnesses check `Loaded` at states traced from
  real runs. The README says that two links are *not* kernel-checked: that loading the ELF gives the
  witness memory, and that the traced boot is the machine's own. The scripts that checked them are not
  in the repository.
- **The specification itself.** `BigStep` is the spec. The theorem says the binary matches *it*, not
  that it matches anyone's informal idea of WHILE. The author has said in a talk that the semantics was
  written with an LLM. A rule that copied a quirk of the C code would make the theorem true and the
  quirk "correct". A human must review Vsa/While/Semantics.lean to trust the meaning.
- **Program assumptions.** `capacity` and `stack_admissible` are hypotheses. A program that needs more
  heap or stack than the image provides is outside the theorem. `endToEnd_checked` discharges them by
  computation.
- **Libraries.** iris-lean (adequacy, the proof mode) and Lean's kernel. The README says every theorem
  uses only the three standard axioms. This site did not re-check that.
