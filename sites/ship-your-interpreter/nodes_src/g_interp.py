NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

# ---------------------------------------------------------------- F. the interpreter proof

node("VsaIris.Interp.Boot",
 "Boot: the data behind a loaded configuration",
 "Boot c p is the unpacked form of Loaded: the statement array, the interpreter object, the native function addresses, the arena and address maps, the initial ownership data, the heap chunks and bins, and the facts about them. The interpreter proof works from this record.",
 r"""## Plain English

**Structure (`Boot`, VsaIris/Interp/World.lean lines 251–273).** Fields:

- where the AST is (`stmts`, `count`) and its [representation](#/node/Vsa.MemRepr.ProgramRepr) proof;
- the interpreter object `inp`, the native function addresses `N` (`print`, `println`, `assert`), the
  value arena `A`, and the maps from WHILE frame and closure numbers to C addresses;
- the [readiness facts](#/node/Vsa.Sim.LayoutInstance.InterpRunReadyFacts);
- initial ownership (`owned`), the allocator state with [capacity](#/node/Vsa.Sim.DlHeap.InitialAllocatorAt)
  (`alloc`), the global frame's layout, and extra heap facts.

[boot_of_loaded](#/node/VsaIris.Interp.boot_of_loaded) produces one from `Loaded`.
""",
 [q("Where does a Boot record come from?",
    ["From Loaded, by boot_of_loaded", "From running the ELF"], 0,
    "VsaIris/Interp/World.lean lines 276–281."),
  q("Does Boot contain the heap-capacity fact?",
    ["Yes, inside alloc", "No"], 0,
    "VsaIris/Interp/World.lean lines 268–269."),
  q("Is Boot a Prop?",
    ["No. It is a data structure, and boot_of_loaded gives Nonempty (Boot c p)", "Yes"], 0,
    "VsaIris/Interp/World.lean lines 251 and 276–277."),
 ])

node("VsaIris.Interp.boot_of_loaded",
 "Unpacking Loaded",
 "boot_of_loaded turns the existential hypothesis Loaded into a Boot record by destructuring it. It is bookkeeping, but it marks the point where the generic Loaded meets the interpreter's own data.",
 r"""## Plain English

**Theorem (`boot_of_loaded`, VsaIris/Interp/World.lean lines 276–281).** If `c` is
[Loaded](#/node/Vsa.Refine.Loaded) with `p` at `interpRunLayout`, there is a [Boot](#/node/VsaIris.Interp.Boot)
record for `c` and `p`.

The proof takes apart the nested existentials of `Loaded`, `InterpRunReady` and the heap's `boot` field,
and puts the pieces back together as a `Boot`. No reasoning is involved.

It is used at the start of both halves of the simulation: [interpSim_iris](#/node/VsaIris.Interp.interpSim_iris)
and `partial_sim_of` (VsaIris/Interp/EndToEnd.lean line 91).
""",
 [q("Is any reasoning done in boot_of_loaded?",
    ["No. It reorganises the hypothesis", "Yes, it simulates the boot code"], 0,
    "VsaIris/Interp/World.lean lines 278–281."),
  q("Why is the result Nonempty rather than a Prop?",
    ["Boot is a data structure, and Loaded only says one exists", "It is an accident"], 0,
    "VsaIris/Interp/World.lean line 277."),
  q("Does it involve the ELF boot code (crt0, main)?",
    ["No. It starts from the interp_run entry state", "Yes"], 0,
    "Loaded already places the machine at interp_run."),
 ])

node("VsaIris.Interp.Boot.regime_of_bigStep",
 "A normal result fits the heap",
 "For a normal result of the loaded program, regime_of_bigStep finds a cost-annotated derivation with cost n and shows, by the capacity assumption, that the heap's counted regime with budget n is OK. This is the only place the capacity assumption is used.",
 r"""## Plain English

**Theorem (`Boot.regime_of_bigStep`, VsaIris/Interp/World.lean lines 740–746).** Given a
[Boot](#/node/VsaIris.Interp.Boot) record and `BigStep p out`, there are a final state `st'` and a cost `n` such that

- `p` has a [cost-annotated](#/node/Vsa.While.ExecSeqCost) normal run to `st'` with cost `n`,
- `st'` printed `out`, and
- `RegimeOK top (counted n)`: twice `n` plus the slack fits between the heap top and the heap end
  (lines 736–738).

Proof: [BigStep.cost](#/node/Vsa.While.BigStep.cost) gives the cost, and the `capacity` field gives the
bound.

The *partial* half of the proof runs in the **uncounted** regime, where `RegimeOK` is trivially true
(line 747). There an allocation may fail, and the interpreter then exits with code 1 (out of memory),
which the stuck half allows.
""",
 [q("What does RegimeOK top (counted n) say?",
    ["2·n + slack ≤ heapEnd − top", "n = 0", "The stack is large enough"], 0,
    "VsaIris/Interp/World.lean lines 736–738."),
  q("Is the capacity assumption needed in the partial (stuck) case?",
    ["No. That case uses the uncounted regime, and running out of memory exits 1", "Yes"], 0,
    "VsaIris/Interp/World.lean line 747 and VsaIris/Interp/EndToEnd.lean line 74."),
  q("Which lemma supplies the cost n?",
    ["BigStep.cost", "boot_of_loaded"], 0,
    "VsaIris/Interp/World.lean line 744."),
 ])

node("VsaIris.Interp.world_of_boundary",
 "From raw bytes to the interpreter's world",
 "At the boundary, the proof owns a flat map of memory bytes and the console. world_of_boundary allocates the interpreter's ghost state and carves those bytes into structured Iris resources: heap, store representation, console and stdio state, code, AST, stack and caller frame.",
 r"""## Plain English

**Theorem (`world_of_boundary`, VsaIris/Interp/World.lean lines 953–960).** From ownership of every boot
byte (`b.bytes`) and of the console holding the initial output, after an Iris update, there are ghost
names for frames and closures under which `bootRes b ρ` holds.

**`bootRes`** (lines 856–860) is the interpreter's starting world:

- `worldPre`: the dlmalloc heap in regime `ρ`, the WHILE store represented in C memory, console
  ownership, the stdio state and the interpreter context (call depth 0);
- the global frame, and the AST as read-only memory (`astSs`);
- the code and shared read-only data, the free stack block, and the caller's frame.

The real work is in `boot_of_bytes` (lines 873–951). It splits the byte map along disjoint address
classes (read-only, store, heap, stack, statics, stdio) and rebuilds each component's invariant from the
boot facts.
""",
 [q("What does the proof start with?",
    ["Ownership of a flat map of boot bytes and of the console", "A Sail trace"], 0,
    "VsaIris/Interp/World.lean lines 953–955."),
  q("What does bootRes include about the AST?",
    ["Read-only ownership of its C structs (astSs)", "Nothing"], 0,
    "VsaIris/Interp/World.lean line 858."),
  q("Which regime does the total proof use?",
    ["The counted regime with the cost from regime_of_bigStep", "The uncounted one"], 0,
    "VsaIris/Interp/EndToEnd.lean lines 57 and 63."),
 ])

node("VsaIris.Interp.supplies_of",
 "Every C helper, specified and proved",
 "Proves the machine-code specifications the interpreter loop needs (value helpers, environments, string routines, snprintf, malloc/realloc/free, the natives, the exit path), once for the total WP and once for the partial WP.",
 r"""## Plain English

**Theorem (`supplies_of`, VsaIris/Interp/Supply.lean lines 376–382).** The structure `Supplies`
(lines 370–374) asks, for any Iris instance and any native addresses that point at the right code, for:

- a **`TermSupply`** (VsaIris/Interp/TermSim.lean lines 46–77): specifications under the *total* WP of
  `value_int`, `value_bool`, `value_null`, `value_str`, `value_truthy`, `value_equal`, `strcmp`,
  `env_get`/`set`/`new`/`define`, the three natives, the allocator, stringify, `strlen`, `memcpy`, `strcpy`;
- a **`StuckSupply`** (VsaIris/Interp/StuckSim.lean lines 43–74): the same under the *partial* WP, plus the
  error environment that describes `longjmp` to the runtime-error handler.

Each specification is about the **machine code** of the committed ELF. The proofs step through the
function's instructions from its entry to its return. They use the step rules and the symbolic executor
([symRun_swp](#/node/VsaIris.SymExec.symRun_swp)), together with the allocator, printf and newlib proofs
under `VsaIris/Vsa/`.

This is where most of the roughly 109,000 lines of `VsaIris/` go.
""",
 [q("What are the specifications about?",
    ["The machine code of the committed ELF", "The C source"], 0,
    "They are stated with machine WPs over vsaModel (e.g. VsaIris/Interp/TermSim.lean lines 48–77)."),
  q("Why two records?",
    ["One for the total WP (terminating runs), one for the partial WP (stuck case)", "One per CPU"], 0,
    "VsaIris/Interp/Supply.lean lines 370–374."),
  q("Are any of these specifications assumed rather than proved?",
    ["No. supplies_of proves both records", "Yes, malloc is assumed"], 0,
    "VsaIris/Interp/Supply.lean lines 376–382 build them from proved parts. A text search found no sorry."),
 ])

node("VsaIris.SymExec.symRun_swp",
 "Symbolic execution, proved sound once",
 "Instead of a separate lemma per instruction address, the project runs a reflective symbolic executor over the binary's code and proves it sound once. A run of straight-line and branching code becomes one closed computation, and what is left is a small list of obligations.",
 r"""## Plain English

**Theorem (`symRun_swp`, VsaIris/Vsa/SymExec.lean, from line 2087).** The module comment (lines 7–24)
explains the design:

- the code bytes in a range are pinned to the ELF image (`CodeAt`, lines 37–39);
- one generic rule for each kind of instruction (any ordinary line, a conditional branch, a direct
  jump), proved against the Sail model;
- an executor `symRun` that runs a whole stretch of code over a symbolic state, with registers and memory
  as expressions over the entry values, collecting side obligations;
- **`symRun_swp`**: whatever `symRun` computes is a valid weakest-precondition step at the entry state;
- a reflective checker that discharges most obligations about intervals and separation automatically.

The README's "Proof structure" table lists this with the other layers that replaced per-address lemmas:
decoding normal forms (`decodeW`), text pieces, step rules, and region and heap reasoning. The
`abstractions/ROUND-*.md` notes record how each layer was chosen and measured.
""",
 [q("What problem does the symbolic executor solve?",
    ["It replaces many per-address step lemmas with one soundness proof", "It compiles WHILE"], 0,
    "VsaIris/Vsa/SymExec.lean lines 7–24."),
  q("Does trusting it require trusting the executor's code?",
    ["No. symRun_swp proves it sound in Lean", "Yes"], 0,
    "Reflection: the executor's result is used only through symRun_swp."),
  q("What are the ‘residual obligations’?",
    ["Side conditions the executor could not decide, left as goals", "Unproved axioms"], 0,
    "VsaIris/Vsa/SymExec.lean lines 21–23."),
 ])

node("VsaIris.Interp.interpSeqT_all",
 "The terminating case: the loop follows each rule",
 "interpSeqT_all proves, by induction over a cost-annotated derivation, that the interpreter's machine code for a statement sequence ends in the state the rule describes. It needs the total-WP specifications from TermSupply. This is the core of term_sim.",
 r"""## Plain English

**Theorem (`interpSeqT_all`, VsaIris/Interp/TermSim.lean lines 372–377).** Given a `TermSupply` and a
[cost-annotated](#/node/Vsa.While.ExecSeqCost) derivation of a statement list from `st` to `st'` with status
`status` and cost `n`, the property `interpSeqT_body` holds of it.

That property (VsaIris/Interp/SeqLoopInterp.lean lines 121–141) says, roughly: if the machine is at the
interpreter's statement loop with the C representation of `st`, the AST of the remaining statements, enough
stack, and a heap budget of at least `n`, then the total WP holds for any continuation that expects the
representation of `st'` and the C encoding of `status`.

The proof (the `term_rec` tactic, VsaIris/Interp/TermSim.lean lines 214–370) is one case per rule of the cost semantics: literals, variables,
operators, calls into closures and natives, blocks, `if`, `while`, `for`, `return`, `break`, `continue`, and
sequencing. Each case uses the specification of the C code that implements it.
""",
 [q("What is the induction over?",
    ["A cost-annotated big-step derivation", "The machine steps", "The program text"], 0,
    "VsaIris/Interp/TermSim.lean lines 373–376."),
  q("Which WP is involved?",
    ["The total WP (twpW)", "The partial WP"], 0,
    "TermSupply's fields use twpW (VsaIris/Interp/TermSim.lean lines 46–77)."),
  q("Why is the cost needed?",
    ["The heap budget must cover every allocation the run makes", "To count steps"], 0,
    "world … (.counted (k + n)) in interpSeqT_body (VsaIris/Interp/SeqLoopInterp.lean line 135)."),
 ])

node("VsaIris.Interp.specsP_all",
 "The partial case: Löb induction over all code",
 "specsP_all proves partial specifications for every expression and statement at once, using Löb induction (assume the specs ‘later’, prove them now). Each spec says the machine produces the semantics' result if one exists, or else jumps to the runtime-error path. This is the core of stuck_sim.",
 r"""## Plain English

**Theorem (`specsP_all`, VsaIris/Interp/StuckSim.lean lines 194–209).** Given a `StuckSupply` and the
error context (the `setjmp` buffer and runtime-error code), the persistent proposition `specsPI` holds: for
every state, depth, environment and expression or statement, `eval_expr`/`exec_stmt` satisfy their partial
specifications.

**Löb induction** (`loeb_wand`, line 198) lets the proof assume `specsPI` under Iris's `▷` and use it for
recursive calls. Every recursive call happens after at least one machine step, so the `▷` can be removed.
No derivation is needed, so the proof also covers programs whose source run gets stuck or never ends.

The individual cases are `evalP_cases` (lines 98–164) and `execP_cases` (lines 166–192).
""",
 [q("What proof principle makes the partial specs possible without a derivation?",
    ["Löb induction in Iris", "Induction on the program size", "Induction on BigStep"], 0,
    "VsaIris/Interp/StuckSim.lean line 198."),
  q("What may a partial spec end in, besides the semantics' result?",
    ["The runtime-error path (exit 70) or out of memory (exit 1)", "Any state"], 0,
    "VsaIris/Interp/TopRunP.lean line 265 defines AbortCode as 70 or 1."),
  q("Which WP is involved?",
    ["The partial WP (wpW)", "The total WP"], 0,
    "StuckSupply's fields use wpW (VsaIris/Interp/StuckSim.lean lines 43–74)."),
 ])

node("VsaIris.Interp.interpRun_total_top",
 "interp_run from entry to exit (terminating case)",
 "For a normal, cost-annotated run within budget, the total WP holds at the entry of interp_run with postcondition ‘exit code 0 and output = the program's output’. This covers the prologue, the statement loop, the return into main, and the HTIF exit.",
 r"""## Plain English

**Theorem (`interpRun_total_top`, VsaIris/Interp/TopEntryBoot.lean lines 121–129).** Given proved newlib
facts, a [Boot](#/node/VsaIris.Interp.Boot) record, a cost-annotated normal run with cost `n`, and its
[loop proof](#/node/VsaIris.Interp.interpSeqT_all): from the boot world in the counted regime with budget
`n`, plus ownership of the entry registers, the total WP holds with postcondition "the result is (0, the
final output)".

Chain inside:

- `topEntry_of_regs` (lines 110–119) splits the registers and makes the code image persistent;
- `interpRun_total_boot` (VsaIris/Interp/TopRun.lean lines 707–716) moves to the top-level precondition;
- `interpRun_total` (VsaIris/Interp/TopRun.lean lines 612–) runs the prologue of `interp_run`
  (`setjmp`, then the loop over `count` statements), returns into `main`, and follows the exit path to
  the HTIF device with code 0.
""",
 [q("What is the postcondition?",
    ["The machine exits with code 0 and the program's output", "The machine diverges"], 0,
    "VsaIris/Interp/TopEntryBoot.lean line 127."),
  q("Does this cover code after interp_run returns?",
    ["Yes, through main's exit path to HTIF", "No"], 0,
    "The postcondition is about the machine's exit, which happens after interp_run returns (ra points into main)."),
  q("Which regime is the heap in?",
    ["Counted, with the run's cost n", "Uncounted"], 0,
    "VsaIris/Interp/TopEntryBoot.lean line 126."),
 ])

node("VsaIris.Interp.interpRun_partial_top",
 "interp_run from entry to exit (partial case)",
 "With no assumption about the source run, the partial WP holds at interp_run's entry for any postcondition that accepts (0, out) for every normal result out and accepts any (70 or 1, out). In words: the machine diverges, exits 0 with a genuine result, or aborts with 70 or 1.",
 r"""## Plain English

**Theorem (`interpRun_partial_top`, VsaIris/Interp/TopEntryBoot.lean lines 131–143).** Given the
[partial statement specs](#/node/VsaIris.Interp.specsP_all) and a postcondition `Φ` such that

- `Φ (0, st'.out)` holds whenever `p` runs normally to `st'`, and
- `Φ (e, o)` holds whenever `e` is an abort code (70 or 1, VsaIris/Interp/TopRunP.lean line 265),

the partial WP with postcondition `Φ` holds from the boot world in the uncounted regime.

The abort codes match `c/src/main.c`: `run_source` returns 70 when `interp_run` reports a runtime error.
Exit code 1 is the out-of-memory path. The proof also covers a top-level `return`, `break` or
`continue`, which `interp_run` reports as a runtime error (c/src/interp.c, the end of `interp_run`).
""",
 [q("What exit codes can a non-normal run produce, according to this theorem?",
    ["70 or 1", "Any nonzero code", "Only 70"], 0,
    "AbortCode, VsaIris/Interp/TopRunP.lean line 265."),
  q("Does this theorem assume the program has a big-step result?",
    ["No", "Yes"], 0,
    "VsaIris/Interp/TopEntryBoot.lean lines 131–138 have no derivation hypothesis."),
  q("Which regime is the heap in?",
    ["Uncounted", "Counted"], 0,
    "VsaIris/Interp/TopEntryBoot.lean line 139."),
 ])
