NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]

# ---------------------------------------------------------------- the main theorem

node("Vsa.Sim.EndToEnd.endToEnd_refinement",
 "Headline: the binary interpreter refines the WHILE semantics",
 "Put a WHILE program's AST in memory and the RISC-V machine at the compiled C function interp_run. Then the machine exits 0 with output out exactly when the big-step semantics gives out, and if it diverges the program has no result. It is about a real ELF on the Sail model.",
 r"""## Plain English

**Theorem (`endToEnd_refinement`, VsaIris/Interp/EndToEnd.lean lines 159–163).** For every WHILE program
`p` and every machine configuration `c`:

*if* `c`, with every missing RAM byte read as zero, is [Loaded](#/node/Vsa.Refine.Loaded) with `p` at the
[interpRunLayout](#/node/Vsa.Sim.LayoutInstance.interpRunLayout), *then*

1. for every string `out`, [BigStep](#/node/Vsa.While.BigStep) `p out` holds **if and only if** the machine,
   started from `c`, [halts](#/node/Vsa.Machine.Halts) with exit code 0 and console output `out`;
2. if the machine [diverges](#/node/Vsa.Machine.Diverges) from `c`, then no `out` has `BigStep p out`.

### What the pieces mean

- **The program side** is an inductive big-step semantics of a small dynamically typed language (WHILE),
  with closures, strings, 64-bit wrapping integers and a call-depth cap of 1000. "`p` has a normal result
  `out`" means the derivation finishes with status *normal* and `out` is everything `print`/`println` wrote.
- **The machine side** is the Sail-generated RV64 model in `riscv-lean/`, stepped one instruction at a time
  with the HTIF exit device. "Halts with code 0" means the program wrote exit code 0 to `tohost`.
- **The bridge** is the hypothesis `Loaded`. It says the AST of `p` is in memory as the C structs of
  `c/src/ast.h`, and that the machine sits at the first instruction of `interp_run` (address 0x800043ec in
  the committed ELF) with the ELF's code, data, C runtime and allocator in their initial state. It also
  says the heap and stack are big enough for `p` (see [InterpRunReadyFacts](#/node/Vsa.Sim.LayoutInstance.InterpRunReadyFacts)).
- **`fillZero`** only changes how memory is represented. The Sail model reads a missing byte as 0
  anyway, and [halts_fillZero](#/node/Vsa.Densify.halts_fillZero) shows that the change is harmless.

### Why it is remarkable

The theorem is about the **compiled binary**, `c/while-riscv-htif.elf`, as an ISA specification sees it. No
C semantics is involved, and no C compiler has to be trusted. The C code shows what the binary was meant
to do. The proof works on the instructions themselves, including `malloc`, `snprintf` and the parts of
newlib that the interpreter reaches.

### What it does not say

- It starts at `interp_run`, after the C parser has built the AST. The parser, `main` and the boot code are
  not in this statement. For ten concrete programs, [while_halts](#/node/Vsa.Sim.Boot.while_halts) and its
  siblings connect it to boot states traced from the ELF.
- It says nothing about *which* nonzero code a failing program exits with. That is
  [endToEnd_trichotomy](#/node/Vsa.Sim.EndToEnd.endToEnd_trichotomy).
- It is only as meaningful as `BigStep`. See [Review](#/review).

The full chain of lemmas is on the [Roadmap](#/roadmap).
""",
 [q("What is the only hypothesis of endToEnd_refinement?",
    ["That the (zero-filled) configuration is Loaded with p at interpRunLayout",
     "That p type-checks",
     "That p terminates",
     "That the C compiler is correct"], 0,
    "VsaIris/Interp/EndToEnd.lean lines 159–160. The heap and stack conditions are inside Loaded, not separate hypotheses."),
  q("Which way does the first conclusion go?",
    ["Both ways: BigStep p out holds iff the machine halts with code 0 and output out",
     "Only from the semantics to the machine",
     "Only from the machine to the semantics"], 0,
    "VsaIris/Interp/EndToEnd.lean line 161. The ‘iff’ comes from forward simulation plus machine determinism (Vsa/Lang/Basic.lean lines 51–71)."),
  q("If the machine diverges, what does the theorem conclude?",
    ["That the program has no normal big-step result",
     "That the program diverges in the source semantics",
     "Nothing"], 0,
    "VsaIris/Interp/EndToEnd.lean line 162. That the source *diverges* (rather than errs) is not claimed here. That needs endToEnd_trichotomy."),
  q("What is the ‘machine’ in this theorem?",
    ["The Sail-generated RV64 model in riscv-lean, run on the committed ELF's bytes",
     "A C abstract machine",
     "Real hardware"], 0,
    "Vsa/Machine.lean lines 18–39 define Step, Halts and Diverges through Vsa.stepOnce (Vsa/Elf.lean lines 22–36), which runs the Sail model."),
  q("Does the theorem cover the C parser that turns source text into the AST?",
    ["No. It starts at interp_run with the AST already in memory",
     "Yes, it starts from the reset vector",
     "Yes, the parser is verified in Lean"], 0,
    "Loaded (Vsa/Refinement.lean lines 12–13) assumes the AST is laid out and the PC is at interp_run. c/src/main.c calls parse_program before interp_run."),
 ],
 caveats=["Not built for this site. The repository's own `#print axioms` lines were not run, so ‘proved’ means the file contains a complete-looking proof. A text search found no `sorry` outside `riscv-lean/`.",
          "The theorem is about the ISA model and the ELF bytes. Agreement with real hardware, and with the C source, is trusted, not proved.",
          "`BigStep` is the specification. If it encodes a behaviour of the C code that nobody intended, the theorem calls that behaviour correct.",
          "The heap-capacity and stack assumptions sit inside `Loaded`, so a reader skimming the statement can miss them."],
 widgets=walk("How the proof goes (VsaIris/Interp/EndToEnd.lean, lines 128–163)", [
    {"text": "The WHILE semantics BigStep is the specification: a normal-status run from the initial state, with its printed output.", "link": "Vsa.While.BigStep"},
    {"text": "Loaded says the AST is in memory as C structs and the machine is ready at interp_run, including the heap-capacity and stack assumptions.", "link": "Vsa.Refine.Loaded"},
    {"text": "From Loaded, extract the Boot record: addresses, arena, initial heap chunks, and the capacity fact for each terminating run.", "link": "VsaIris.Interp.boot_of_loaded"},
    {"text": "Split the initial memory bytes into Iris ownership of the interpreter's world: heap, store, console, code, AST, stack.", "link": "VsaIris.Interp.world_of_boundary"},
    {"text": "Collect the machine-code specifications of every C helper and libc routine the interpreter calls (supplies_of, newlibHoles_proved).", "link": "VsaIris.Interp.supplies_of"},
    {"text": "Terminating case: induction on the cost-annotated derivation shows the interpreter loop follows each rule.", "link": "VsaIris.Interp.interpSeqT_all"},
    {"text": "Non-terminating or failing case: Löb induction gives partial specifications for every statement and expression.", "link": "VsaIris.Interp.specsP_all"},
    {"text": "Run interp_run from its entry to the HTIF exit: a total WP ending at (0, out), and a partial WP ending at 0 with a result or at code 70 or 1.", "link": "VsaIris.Interp.interpRun_total_top"},
    {"text": "routeAt_of_boot packages the initial resources and both WPs as the Iris obligations at one loaded configuration.", "link": "VsaIris.Interp.routeAt_of_boot"},
    {"text": "Iris adequacy turns the WPs into machine facts, and IrisRoute.sim makes them a forward simulation.", "link": "VsaIris.Lang.IrisRoute.sim"},
    {"text": "interpSim_iris: OutSim for BigStep at Loaded interpRunLayout.", "link": "VsaIris.Interp.interpSim_iris"},
    {"text": "Determinism turns forward simulation into the two-way refinement (OutSim.refinement).", "link": "Vsa.Lang.OutSim.refinement"},
    {"text": "Halting and divergence do not change under fillZero, so the hypothesis can be stated on the zero-filled configuration.", "link": "Vsa.Lang.OutSim.refinement_fillZero"},
 ]))

node("Vsa.Sim.EndToEnd.endToEnd_refinement_loaded",
 "The refinement, before zero-filling",
 "The same theorem, with Loaded stated directly on the configuration c rather than on fillZero c. It is one line: the generic refinement theorem applied to the interpreter's simulation proof.",
 r"""## Plain English

**Theorem (`endToEnd_refinement_loaded`, VsaIris/Interp/EndToEnd.lean lines 153–157).** If `c` is
[Loaded](#/node/Vsa.Refine.Loaded) with `p`, then `BigStep p out` holds iff the machine halts from `c` with
code 0 and output `out`, and divergence rules out a normal result.

The proof is [Vsa.Refine.refinement](#/node/Vsa.Refine.refinement) applied to
[interpSim_iris](#/node/VsaIris.Interp.interpSim_iris). All the work is in the simulation. This step only
uses machine determinism.

The headline [endToEnd_refinement](#/node/Vsa.Sim.EndToEnd.endToEnd_refinement) states the hypothesis on
`fillZero c` instead. A configuration traced from a real run lists only the bytes that were actually
written, but `Loaded` speaks about every byte of the stack, for example. Filling in the zeros the Sail
model would read anyway makes the hypothesis true of such traces.
""",
 [q("What does this version assume about c?",
    ["Loaded interpRunLayout p c, with no zero-filling", "Loaded on fillZero c", "Nothing"], 0,
    "VsaIris/Interp/EndToEnd.lean line 154."),
  q("Where is the real work of this proof?",
    ["In interpSim_iris, the simulation proof; this step is a one-line application of the generic refinement theorem",
     "In this theorem's own long tactic proof"], 0,
    "VsaIris/Interp/EndToEnd.lean line 157."),
  q("Why does the headline use fillZero c instead?",
    ["So that configurations whose memory lists only some bytes can still satisfy Loaded; missing RAM reads as 0 in Sail anyway",
     "Because the theorem is false without it",
     "To weaken the conclusion"], 0,
    "Vsa/Lang/Densify.lean lines 4–8 explain this, and Vsa/Densify.lean lines 10–15 show that halting and divergence do not change."),
 ])

node("VsaIris.Interp.interpSim_iris",
 "The interpreter simulates BigStep (the core result)",
 "The core result: the binary forward-simulates BigStep at the interp_run loading relation. Normal results become clean halts; with no normal result, the machine diverges or exits nonzero. It comes through the Iris route.",
 r"""## Plain English

**Theorem (`interpSim_iris`, VsaIris/Interp/EndToEnd.lean lines 132–134).** [OutSim](#/node/Vsa.Lang.OutSim)
holds for `BigStep` at `Loaded interpRunLayout`. That means two things:

- **term_sim:** if `p` is loaded in `c` and `BigStep p out`, the machine halts from `c` with code 0 and
  output `out`;
- **stuck_sim:** if `p` is loaded in `c` and has no normal result, the machine diverges or halts with a
  nonzero code.

### How

For each loaded configuration, [boot_of_loaded](#/node/VsaIris.Interp.boot_of_loaded) produces a `Boot`
record. [routeAt_of_boot](#/node/VsaIris.Interp.routeAt_of_boot) then builds the Iris obligations from it,
using the proved helper specifications ([supplies_of](#/node/VsaIris.Interp.supplies_of)) and the proved
newlib facts ([newlibHoles_proved](#/node/VsaIris.Interp.newlibHoles_proved)).
[IrisRoute.sim](#/node/VsaIris.Lang.IrisRoute.sim) turns those into the generic simulation, and
`OutSim.of_sim` (Vsa/Lang/Basic.lean lines 144–146) specialises it to an output-only language.

Almost all of the roughly 109,000 lines in `VsaIris/` exist to make `routeAt_of_boot` possible.
""",
 [q("What are the two halves of OutSim?",
    ["term_sim (results become clean halts) and stuck_sim (no result means divergence or nonzero exit)",
     "Soundness and completeness of the parser",
     "Type safety and progress"], 0,
    "Vsa/Lang/Basic.lean lines 133–136."),
  q("Does stuck_sim say which nonzero code the machine exits with?",
    ["No; partial_sim_of (VsaIris/Interp/EndToEnd.lean lines 86–110) pins it to 70 or 1",
     "Yes, always 70"], 0,
    "OutSim only asks for e ≠ 0. The sharper fact is used by endToEnd_trichotomy."),
  q("Which framework turns the per-configuration proofs into a simulation?",
    ["Iris weakest preconditions plus adequacy (IrisRoute.sim)", "A hand-rolled bisimulation", "Model checking"], 0,
    "VsaIris/Lang/Route.lean lines 48–58."),
 ])

node("VsaIris.Interp.routeAt_of_boot",
 "Obligations at one loaded configuration",
 "routeAt_of_boot is where the interpreter proof meets the generic route. From a Boot record it supplies the initial resources, a total WP that ends at (0, out) for every normal result, and a partial WP that ends at a nonzero code when there is none.",
 r"""## Plain English

**Definition (`routeAt_of_boot`, VsaIris/Interp/EndToEnd.lean lines 47–80).** Given proved helper
specifications, proved newlib facts and a [Boot](#/node/VsaIris.Interp.Boot) record for `p` at `c`, it builds a
[RouteAt](#/node/VsaIris.Lang.RouteAt) value:

- **resources**: the register map read from `c`, and the boot bytes of memory with their agreement proofs;
- **term** (lines 55–67): for a normal result, [Boot.regime_of_bigStep](#/node/VsaIris.Interp.Boot.regime_of_bigStep)
  turns it into a cost-annotated derivation that fits the heap. The boundary is then opened
  ([world_of_boundary](#/node/VsaIris.Interp.world_of_boundary)), and the total run
  [interpRun_total_top](#/node/VsaIris.Interp.interpRun_total_top) is applied, with the per-rule loop proof
  [interpSeqT_all](#/node/VsaIris.Interp.interpSeqT_all);
- **stuck** (lines 68–80): with no normal result, the partial run
  [interpRun_partial_top](#/node/VsaIris.Interp.interpRun_partial_top), fed by
  [specsP_all](#/node/VsaIris.Interp.specsP_all), ends at 0 only with a big-step result (impossible here)
  or at an abort code, which is nonzero.

`boundary_bind` (lines 35–44) allocates the two ghost names the interpreter's invariants use.
""",
 [q("Which kind of WP does the term branch produce?",
    ["A total WP (twpW), so the machine must terminate", "A partial WP"], 0,
    "VsaIris/Interp/EndToEnd.lean line 59."),
  q("Why can the stuck branch rule out exit code 0?",
    ["Exit 0 would need a big-step result, which by assumption does not exist", "Exit 0 is impossible on RISC-V"], 0,
    "VsaIris/Interp/EndToEnd.lean line 78."),
  q("Where does the heap-capacity assumption enter?",
    ["Through Boot.regime_of_bigStep in the term branch", "In the stuck branch", "Nowhere"], 0,
    "VsaIris/Interp/EndToEnd.lean line 57 and VsaIris/Interp/World.lean lines 740–746."),
 ])

node("VsaIris.Interp.newlibHoles_proved",
 "All newlib calls are proved",
 "Despite the name, NewlibHoles is not an assumption here. newlibHoles_proved builds it from proved specifications of the newlib code the interpreter reaches (stdio, fprintf, snprintf, exit handlers).",
 r"""## Plain English

**Theorem (`newlibHoles_proved`, VsaIris/Interp/EndToEnd.lean lines 128–130).** The proposition
`NewlibHoles` (VsaIris/Vsa/Newlib.lean lines 226–226) bundles specifications of the C library routines that
the interpreter's machine code jumps into. Examples are `fprintf` to stderr on a runtime error, the stdout
path of `print`, and the exit handlers. This theorem proves that bundle from three proved parts: the core
newlib facts, `fprintf_ok` and `snprintf_ok`.

The word "holes" is a name left over from development. The main theorem's proof passes this *proved*
value, not a hypothesis. A reader worried that `NewlibHoles` is an unproved assumption can check that
`interpSim_iris` (lines 132–134) uses this theorem.
""",
 [q("Is NewlibHoles a hypothesis of endToEnd_refinement?",
    ["No. It is proved by newlibHoles_proved and passed in", "Yes, it is an extra assumption"], 0,
    "VsaIris/Interp/EndToEnd.lean lines 128–134."),
  q("What does it cover?",
    ["Specifications of the newlib routines the interpreter's code reaches", "The Sail model", "The C parser"], 0,
    "VsaIris/Vsa/Newlib.lean lines 215–226."),
  q("Are these specifications about C source or machine code?",
    ["Machine code of the committed ELF, run on the Sail model", "C source"], 0,
    "Each is stated with machine WPs over vsaModel (for example VsaIris/Vsa/Newlib.lean lines 217–222)."),
 ])
