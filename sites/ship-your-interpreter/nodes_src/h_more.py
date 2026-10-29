NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]

# ---------------------------------------------------------------- headlines built on the main theorem

node("Vsa.Sim.EndToEnd.endToEnd_trichotomy",
 "Headline: success, failure and divergence all line up",
 "From a loaded state, a clean exit with output out is exactly a normal big-step result out; every nonzero exit is 70 or 1; and the machine fails or diverges exactly when the program errs or diverges in the source semantics. Source error and source divergence are not told apart on the machine side.",
 r"""## Plain English

**Theorem (`endToEnd_trichotomy`, VsaIris/Interp/EndToEndTrichotomy.lean lines 61–75).** If `fillZero c` is
[Loaded](#/node/Vsa.Refine.Loaded) with `p`, then the six facts of `EndToEndTrichotomy p c` hold
(lines 14–26):

1. **clean**: the machine halts with code 0 and output `out` iff [BigStep](#/node/Vsa.While.BigStep) `p out`;
2. **fail_code**: every nonzero exit code is 70 or 1;
3. **fail_spec**: a nonzero exit means the program errs (`BigStepErr`) or diverges (`BigStepDiverges`) in the
   source semantics;
4. **div_spec**: machine divergence means the program errs or diverges;
5. **err_mach**: a source error means the machine diverges or exits 70 or 1;
6. **div_mach**: a source divergence means the same.

`EndToEndTrichotomy.fails_iff` (lines 77–90) packages 3–6: "the machine exits nonzero or diverges" iff "the
program errs or diverges".

### The source side

`BigStepErr` (Vsa/While/ErrorSem.lean lines 254–255) is a derivation that reaches a stuck point (division by
zero, failed `assert`, undefined variable, call of a non-function, depth cap and so on) or ends with a
top-level `return`, `break` or `continue`. `BigStepDiverges` (lines 442–443) says that step-indexed approximations
of every depth exist. `trichotomy_unconditional` (Vsa/While/StmtDispatchClose.lean lines 546–559) proves that
every program does one of the three, and Vsa/While/Exclusive.lean proves at most one.

### What it does not say

A source **error** may show up on the machine as divergence, and a source **divergence** may show up as exit 70
or 1. For example, a program that recurses forever hits the C call-depth check or runs out of memory.
The theorem only says that the *failure classes* match.
""",
 [q("Which exit codes can a loaded program's failing run produce?",
    ["Only 70 or 1", "Any nonzero code", "Only 1"], 0,
    "fail_code, VsaIris/Interp/EndToEndTrichotomy.lean line 18, with AbortCode at VsaIris/Interp/TopRunP.lean line 265."),
  q("If the source program divergences, must the machine diverge?",
    ["No. It may diverge or exit 70 or 1", "Yes"], 0,
    "div_mach, VsaIris/Interp/EndToEndTrichotomy.lean line 26."),
  q("What does fails_iff relate?",
    ["Machine (nonzero exit or divergence) with source (error or divergence)", "Exit 0 with BigStep"], 0,
    "VsaIris/Interp/EndToEndTrichotomy.lean lines 77–79."),
  q("Which source-level fact makes the failure side possible?",
    ["Every program has a result, an error or a divergence (trichotomy_unconditional)", "Type safety"], 0,
    "Vsa/While/StmtDispatchClose.lean lines 546–559, used at VsaIris/Interp/EndToEndTrichotomy.lean lines 53 and 55."),
 ],
 caveats=["Same trust assumptions as endToEnd_refinement: the Sail model, the ELF bytes, Loaded (with capacity and stack assumptions) and the meaning of BigStep, BigStepErr and BigStepDiverges.",
          "The theorem matches failure *classes*, not specific errors: it does not say which runtime error happened or what was printed to stderr."],
 widgets=walk("How the proof goes (VsaIris/Interp/EndToEndTrichotomy.lean, lines 28–75)", [
    {"text": "Start from the unfilled version endToEnd_trichotomy_loaded (lines 28–59), which uses the main refinement and the sharper partial simulation.", "link": "Vsa.Sim.EndToEnd.endToEnd_refinement_loaded"},
    {"text": "The clean clause is the first half of the main refinement, read backwards.", "link": "Vsa.Sim.EndToEnd.endToEnd_refinement"},
    {"text": "partialSim_iris: from a loaded state the machine diverges, or exits 0 with a big-step result, or exits 70 or 1 (VsaIris/Interp/EndToEnd.lean lines 86–110, 137–140).", "link": "VsaIris.Interp.interpRun_partial_top"},
    {"text": "A nonzero exit or divergence rules out a big-step result, by machine determinism and the refinement.", "link": "Vsa.Machine.Halts.deterministic"},
    {"text": "With no big-step result, the source trichotomy (trichotomy_unconditional) leaves error or divergence. The exclusivity lemmas give the converse directions.", "link": "Vsa.While.BigStep"},
    {"text": "Finally, transfer every clause from fillZero c to c with halts_fillZero and diverges_fillZero (lines 61–75).", "link": "Vsa.Densify.halts_fillZero"},
 ]))

node("Vsa.Sim.EndToEnd.endToEnd_checked",
 "Headline: the program assumptions, discharged by checkers",
 "endToEnd_checked restates the main theorem with the two program assumptions (capacity and stack admissibility) replaced by computations: a static allocation-cost bound B from the abstract interpreter, a stack-fit check, and a check that the heap has room for 2B plus slack.",
 r"""## Plain English

**Theorem (`endToEnd_checked`, VsaIris/Interp/EndToEndChecked.lean lines 12–16).** Suppose

- the cost analysis returns a bound: `interpCostBound p = some B` (Vsa/Sim/CheckedBoundary.lean line 12,
  the abstract interpreter's `progCost`);
- `programStackFits p` evaluates to `true` (Vsa/Sim/LayoutInstance.lean lines 111–115);
- `fillZero c` satisfies `LoadedU p`, the same as `Loaded` but **without** the capacity and stack fields
  (Vsa/Sim/CheckedBoundary.lean lines 47–64);
- the heap has room: `2·B + slack ≤ heapEnd − top` (`HeapRoom`, lines 14–16).

Then the conclusion of [endToEnd_refinement](#/node/Vsa.Sim.EndToEnd.endToEnd_refinement) holds.

The proof is one line through `loaded_of_checked` (lines 66–77). The analysis is sound (`seqcost_sound`, in
Vsa/AbsInt/CostSound.lean), so `B` bounds every terminating run's cost, which gives the capacity field.
`whileWl_interp_checks` (lines 79–82) computes, with `decide +kernel`, that the test program `while.wl` gets
bound 8,272 and passes the stack check.
""",
 [q("What replaces the capacity assumption?",
    ["A computed cost bound B and a check that the heap has room for 2B plus slack", "Nothing; it is dropped"], 0,
    "VsaIris/Interp/EndToEndChecked.lean lines 12–14 and Vsa/Sim/CheckedBoundary.lean lines 14–31."),
  q("Is the cost bound trusted?",
    ["No. The analysis is proved sound (seqcost_sound)", "Yes"], 0,
    "Vsa/Sim/CheckedBoundary.lean lines 25–26."),
  q("What can make interpCostBound return none?",
    ["The analysis cannot bound the program, for example an unbounded loop that allocates; then the theorem does not apply", "Never"], 0,
    "The hypothesis is interpCostBound p = some B (VsaIris/Interp/EndToEndChecked.lean line 12)."),
 ],
 caveats=["The rest of Loaded (the machine at interp_run with the AST laid out) is still a hypothesis, in the form LoadedU.",
          "The cost analysis may fail to give a bound for programs that do fit, so the checked theorem covers fewer programs than the main one with its hypotheses."],
 widgets=walk("How the proof goes (VsaIris/Interp/EndToEndChecked.lean, lines 12–16)", [
    {"text": "capacity_of_bound: the analysis' bound B is above every terminating run's cost (seqcost_sound), so 2B + slack ≤ free heap gives the capacity field (Vsa/Sim/CheckedBoundary.lean lines 18–31).", "link": "Vsa.Sim.DlHeap.InitialAllocatorAt"},
    {"text": "stackAdmissible_of_check: programStackFits p = true gives the stack field (lines 33–37).", "link": "Vsa.Sim.LayoutInstance.InterpRunReadyFacts"},
    {"text": "loaded_of_checked rebuilds the full Loaded from LoadedU plus these two facts (lines 66–77).", "link": "Vsa.Refine.Loaded"},
    {"text": "Apply endToEnd_refinement.", "link": "Vsa.Sim.EndToEnd.endToEnd_refinement"},
 ]))

node("Vsa.Sim.Boot.while_halts",
 "Headline: the shipped ELF prints the right answer (from a traced boot)",
 "From a concrete state built from the ELF image plus a recorded boot trace, the machine halts with code 0 and prints exactly what the semantics says while.wl prints. Loaded is kernel-checked there; that the trace is the machine's real boot is not.",
 r"""## Plain English

**Theorem (`while_halts`, Vsa/Sim/Boot/EndToEnd.lean lines 20–24).** The configuration `bootConfig (bootMem
script log) regs entrySteps` from Vsa/Sim/Boot/Gen/While.lean [halts](#/node/Vsa.Machine.Halts) with code 0 and output
"55", "2500", "36" on three lines.

### How

- **The state.** `bootMem` (Vsa/Sim/Boot/Image.lean line 64) is the ELF image: the fixed text, the
  embedded WHILE script, rodata and data. A recorded **log** of the stores made during boot (crt0, `main`,
  the parser) is written over it. `regs` are the general registers at the moment the trace reached
  `interp_run`. The `script` number is the program's source bytes packed into one integer.
- **Loaded.** The `boot_witness` command (Vsa/Sim/Boot/WitnessCmd.lean lines 3–12) runs an *untrusted*
  generator to propose the heap, AST and ownership data. It then emits kernel-checked
  (`decide +kernel`) theorems that the state satisfies [Loaded](#/node/Vsa.Refine.Loaded) for the Lean program
  `whileWl`.
- **The semantics.** `whileWl_valid` (Vsa/While/Validation.lean lines 10–11) derives
  `BigStep whileWl "55\n2500\n36\n"` with a derivation tactic.
- **Combine.** [endToEnd_refinement](#/node/Vsa.Sim.EndToEnd.endToEnd_refinement), right to left in its first clause.

The same file has five siblings (lines 14–56) for the other traced runs (`proof.elf`, arithmetic, `for`, scope, strings). Vsa/Sim/Boot/Audit.lean extends them to any
configuration whose memory matches the traced view and whose registers match, and states the error-program
cases.

### What is not checked

The README is explicit. Two links are not kernel-checked: that loading the ELF file gives the witness's image
memory, and that the traced boot is what the Sail machine does from reset. The scripts that checked them
are not in the repository. So this theorem shows that the binary interprets `while.wl` correctly **from that
traced state**. It does not show that the machine reaches that state from power-on.
""",
 [q("Where does the starting configuration come from?",
    ["The ELF image plus a recorded log of boot-time stores and registers", "From running the Sail model in Lean from reset", "From the C source"], 0,
    "Vsa/Sim/Boot/Image.lean line 64 and Vsa/Sim/Boot/Config.lean lines 55–56."),
  q("Is Loaded at that state assumed or checked?",
    ["Checked by the kernel through boot_witness's decide +kernel theorems", "Assumed"], 0,
    "Vsa/Sim/Boot/WitnessCmd.lean lines 3–12."),
  q("Which link is NOT kernel-checked, according to the README?",
    ["That the traced boot is the machine's real boot from reset (and that ELF loading gives the image)", "That BigStep holds", "That Loaded holds"], 0,
    "README, section ‘What is assumed’."),
  q("Where does the expected output come from?",
    ["The big-step derivation whileWl_valid", "From running the binary"], 0,
    "Vsa/While/Validation.lean lines 10–11 and Vsa/Sim/Boot/EndToEnd.lean line 24."),
 ],
 caveats=["The boot trace and the ELF-loading step are trusted (README, ‘What is assumed’).",
          "The Lean program whileWl is a hand-written Lean value. Its agreement with c/tests/while.wl is checked by the unverified `whilecheck --selftest`, not in Lean. The ELF embeds the script's bytes, and the witness checks that the in-memory AST encodes whileWl."],
 widgets=walk("How the proof goes (Vsa/Sim/Boot/EndToEnd.lean, lines 20–24)", [
    {"text": "Gen.While.loaded: the traced state satisfies Loaded for whileWl, produced by boot_witness and checked by the kernel.", "link": "Vsa.Refine.Loaded"},
    {"text": "whileWl_valid: the big-step semantics gives output 55, 2500, 36.", "link": "Vsa.While.BigStep"},
    {"text": "endToEnd_refinement turns the big-step result into a clean machine halt with that output.", "link": "Vsa.Sim.EndToEnd.endToEnd_refinement"},
 ]))
