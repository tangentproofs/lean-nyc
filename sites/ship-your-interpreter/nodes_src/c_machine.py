NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

# ---------------------------------------------------------------- B. the machine

node("Vsa.stepOnce",
 "One machine step (the Sail model plus the exit device)",
 "stepOnce is the single point where the proof touches the vendored Sail RISC-V model. It checks the HTIF ‘done’ flag, runs one Sail try_step, and reports either the next counters or an exit code. Everything the theorem says about ‘the machine’ is relative to this function.",
 r"""## Plain English

**Definition (`stepOnce`, Vsa/Elf.lean lines 22–36).** A computation in Sail's state monad, with two
counters (the position within the current timer tick, and the number of instructions so far):

1. If the HTIF device has already signalled *done*, report the exit code it holds.
2. Otherwise run one `try_step` of the Sail RV64 model. That is the official ISA semantics, translated to
   Lean and vendored in `riscv-lean/Lean_RV64D_executable`.
3. If that step made the program write its exit to HTIF, report the exit code. Otherwise advance the
   counters, ticking the clock every `plat_insns_per_tick` instructions, and continue.

[Step, Halts and Diverges](#/node/Vsa.Machine.Halts) are defined from this function, so the machine in the
main theorem is *this* function iterated.

### Trusted

The Sail model is the trusted base for "what RISC-V does". It is about 246,000 lines of generated Lean
in `riscv-lean/`. This site does not explain or audit it. The *executable* copy that the project imports
declares no axioms. A text search finds `axiom` only in the non-executable copy
(riscv-lean/Lean_RV64D/LeanRV64D/RiscvExtras.lean), which this project does not import.
""",
 [q("What does stepOnce return when the program has written its exit?",
    ["The exit code (and step count) instead of next counters", "An error", "Nothing; it loops"], 0,
    "Vsa/Elf.lean lines 24–31."),
  q("What does stepOnce run to execute an instruction?",
    ["The Sail model's try_step", "A hand-written RISC-V interpreter", "Real hardware"], 0,
    "Vsa/Elf.lean line 27."),
  q("Is the Sail model proved correct in this repository?",
    ["No. It is the trusted definition of the ISA", "Yes"], 0,
    "It is vendored from the Sail project (riscv-lean/). The proofs treat it as the specification of the hardware."),
 ],
 caveats=["The Sail model is trusted, not verified here. Its fidelity to real RV64 silicon is outside the theorem."])

node("Vsa.Machine.Halts",
 "Halts: the machine exits with a code and output",
 "Halts c out e says some finite run from configuration c reaches a step that exits with code e, and the console output at that moment is out. Because the Sail step is a function, a configuration halts in at most one way.",
 r"""## Plain English

**Definitions (Vsa/Machine.lean lines 9–39).**

- A **configuration** is the Sail machine state plus the two step counters (lines 9–14). Its **output**
  is everything the Sail model's console has collected (line 16).
- **`Step c c'`** (lines 18–21): `stepOnce` run from `c` succeeds without exiting and gives `c'`.
  **`Halted c e σ`** (lines 23–26): `stepOnce` run from `c` exits with code `e` in final state `σ`.
- **`Halts c out e`** (lines 36–37): some sequence of steps from `c` reaches a configuration that is
  `Halted` with code `e`, and the final output is `out`.
- **[`Diverges c`](#/node/Vsa.Machine.Diverges)** (line 39): for every `n` there is an `n`-step run.

A Sail *error* (the monad's exception case) is neither a step nor a halt. A configuration that raises one
is stuck, so it neither halts nor diverges.

[Halts.deterministic](#/node/Vsa.Machine.Halts.deterministic) and
[Diverges.not_halts](#/node/Vsa.Machine.Diverges.not_halts) are the two facts the refinement argument
needs.
""",
 [q("What does Halts c out e require?",
    ["A finite run from c to an exit with code e and console output out", "That c is the final state", "That the program printed nothing"], 0,
    "Vsa/Machine.lean lines 36–37."),
  q("If the Sail model throws an error, does the configuration halt?",
    ["No. It is stuck: neither Step nor Halted holds", "Yes, with code 0"], 0,
    "Step and Halted (Vsa/Machine.lean lines 18–26) both require the .ok result."),
  q("Where is ‘output’ read from?",
    ["The Sail model's console output buffer", "A WHILE state"], 0,
    "Vsa/Machine.lean line 16."),
 ])

node("Vsa.Machine.Diverges",
 "Diverges: the machine runs forever",
 "Diverges c says runs of every finite length exist from c. Since steps are deterministic, that is the same as the unique run never stopping.",
 r"""## Plain English

**Definition (`Diverges`, Vsa/Machine.lean line 39).** For every natural number `n` there is a
configuration reachable from `c` in exactly `n` [steps](#/node/Vsa.Machine.Halts).

This is the "runs forever" side of the main theorem's second clause: if the machine diverges, the program
has no normal big-step result. [Diverges.not_halts](#/node/Vsa.Machine.Diverges.not_halts) shows that a
diverging configuration cannot also halt.
""",
 [q("What does Diverges c say?",
    ["For every n there is an n-step run from c", "c is stuck", "c halts with a nonzero code"], 0,
    "Vsa/Machine.lean line 39."),
  q("Can a configuration both diverge and halt?",
    ["No (Diverges.not_halts)", "Yes"], 0,
    "Vsa/Machine.lean lines 115–120."),
  q("Is a stuck configuration (Sail error) diverging?",
    ["No. It has no run longer than the steps before the error", "Yes"], 0,
    "A stuck configuration has no Step, so long enough StepsN runs do not exist."),
 ])

node("Vsa.Machine.Halts.deterministic",
 "The machine halts in at most one way",
 "If a configuration halts with (out, e) and with (out', e'), then out = out' and e = e'. This determinism is what turns a one-way simulation into the two-way ‘iff’ of the main theorem.",
 r"""## Plain English

**Theorem (`Halts.deterministic`, Vsa/Machine.lean lines 83–90).** Two halting runs from the same
configuration end at the same place, so they have the same output and exit code.

It is built from three small facts: a step has a unique successor (`Step.deterministic`, lines 41–47),
an exit has a unique code and state (`Halted.deterministic`, lines 49–55), and a configuration cannot both
step and exit (`Step.not_halted`, lines 57–62). All three hold because `stepOnce` is a *function* of the
state.

It is used in [Sim.refinement](#/node/Vsa.Lang.Lang.Sim.refinement): once the simulation says a normal result
`out` makes the machine halt with (0, `out`), any other observed halt must be the same one.
""",
 [q("Why is the machine deterministic?",
    ["Because stepOnce is a function of the state", "Because of an axiom", "It is assumed in Loaded"], 0,
    "Vsa/Machine.lean lines 41–62 prove it by rewriting with the step's result."),
  q("What does determinism buy the main proof?",
    ["The ‘if’ direction: a clean machine halt with output out implies BigStep p out", "Termination"], 0,
    "Vsa/Lang/Basic.lean lines 51–61 use it."),
  q("Does this rely on the WHILE semantics being deterministic?",
    ["No, only the machine", "Yes"], 0,
    "The proof only uses Vsa/Machine.lean. Source determinism is in fact derived from it (Vsa/Lang/Basic.lean lines 74–77)."),
 ])

node("Vsa.Machine.Diverges.not_halts",
 "Divergence excludes halting",
 "A diverging configuration cannot also halt. The proof takes the halting run's length n and asks divergence for an (n+1)-step run, which determinism rules out.",
 r"""## Plain English

**Theorem (`Diverges.not_halts`, Vsa/Machine.lean lines 115–120).** If `c` [diverges](#/node/Vsa.Machine.Diverges)
then `c` does not [halt](#/node/Vsa.Machine.Halts) with any output or code.

A halting run reaches an exiting configuration after some `n` steps. Divergence gives a run of `n + 1`
steps. By determinism, its first `n` steps follow the halting run, so its last step would start from an
exiting configuration, which is impossible (`StepsN.halted_no_extension`, lines 92–106).

The refinement argument uses it twice. A diverging machine has no normal result
(`Sim.no_spec_of_diverges`, Vsa/Lang/Basic.lean lines 63–65). And a stuck-case divergence contradicts an
observed halt (lines 51–61).
""",
 [q("What does the proof compare?",
    ["The halting run of length n with an (n+1)-step run given by divergence", "Two divergent runs"], 0,
    "Vsa/Machine.lean lines 115–120."),
  q("Which property of the machine makes this work?",
    ["Determinism of steps", "Finiteness of memory"], 0,
    "StepsN.halted_no_extension (Vsa/Machine.lean lines 92–106) uses Step.deterministic."),
  q("Where is it used?",
    ["In the generic refinement theorem (Vsa/Lang/Basic.lean)", "In the Sail model"], 0,
    "Vsa/Lang/Basic.lean lines 59 and 65."),
 ])

node("Vsa.Densify.fillZero",
 "fillZero: read missing RAM as zero",
 "fillZero c is c with every RAM byte that the memory map leaves out set to 0. The Sail model already reads a missing byte as 0, so the change is invisible to the machine. It lets traced, sparse configurations satisfy the dense memory facts in Loaded.",
 r"""## Plain English

**Definition (`fillZero`, Vsa/Densify/Transport.lean lines 141–142).** Machine memory is a finite hash
map from addresses to bytes. `fillZeroMem` (lines 121–122) is a map that agrees with the original outside
RAM and, inside RAM, holds the stored byte or 0 if there was none (lines 117–119). `fillZero` puts this
memory into the configuration and keeps everything else.

Why bother? [Loaded](#/node/Vsa.Refine.Loaded) asks, for example, that every stack byte be present.
A configuration built from a trace lists only bytes that were written. Zero-filling makes those
facts true without changing behaviour. [halts_fillZero](#/node/Vsa.Densify.halts_fillZero) proves that it
changes nothing.

The map is chosen with `Classical.choose` from an existence proof (lines 115–122), so `fillZero` is
noncomputable. That is fine for a specification.
""",
 [q("Which bytes does fillZero change?",
    ["Only RAM addresses that were missing, which become 0", "Every byte", "Only stack bytes"], 0,
    "Vsa/Densify/Transport.lean lines 117–119."),
  q("Does fillZero change halting or divergence?",
    ["No (halts_fillZero, diverges_fillZero)", "Yes"], 0,
    "Vsa/Densify.lean lines 10–15."),
  q("Why does the main theorem use it?",
    ["So that Loaded can be satisfied by configurations with sparse memory, such as boot traces", "To make the proof shorter"], 0,
    "Vsa/Lang/Densify.lean lines 4–8."),
 ])

node("Vsa.Densify.halts_fillZero",
 "Zero-filling does not change the run",
 "A configuration halts with (out, e) iff its zero-filled version does, and diverges iff it does. The proof needs a generated lemma for every Sail function involved: each one gives equivalent results on memories that agree up to ‘missing reads as zero’.",
 r"""## Plain English

**Theorems (`halts_fillZero` and `diverges_fillZero`, Vsa/Densify.lean lines 10–15).** For every
configuration `c`, `c` [halts](#/node/Vsa.Machine.Halts) with output `out` and code `e` iff
[fillZero](#/node/Vsa.Densify.fillZero) `c` does. Likewise for [divergence](#/node/Vsa.Machine.Diverges).

### How

- Two machine states are **equivalent** (`SEqv`, Vsa/Densify/Resp.lean lines 22–27) if they have the same
  registers and output and their memories agree when a missing byte is read as 0.
- A Sail computation **respects** the equivalence (`Resp`, lines 38–39) if equivalent starting states
  give equal results and equivalent final states.
- [Gen.stepOnce_resp](#/node/Vsa.Densify.Gen.stepOnce_resp) shows that one machine step respects it.
- Then a step-by-step simulation in both directions (Vsa/Densify/Transport.lean lines 17–92) moves
  halting and divergence across.
""",
 [q("What is the key property of a Sail function needed here?",
    ["It gives equivalent results on states whose memories agree up to missing-is-zero", "It terminates", "It is total"], 0,
    "Resp, Vsa/Densify/Resp.lean lines 38–39."),
  q("Does halts_fillZero hold for all configurations, loaded or not?",
    ["Yes, for every configuration", "Only for loaded ones"], 0,
    "Vsa/Densify.lean lines 10–12 have no hypothesis."),
  q("Where is it used on the path to the main theorem?",
    ["In OutSim.refinement_fillZero, the last step", "In the interpreter loop"], 0,
    "Vsa/Lang/Densify.lean lines 31–38."),
 ])

node("Vsa.Densify.Gen.stepOnce_resp",
 "Every Sail function respects zero-filled memory (generated)",
 "A generated proof of about 1,400 lines unfolds every Sail function reachable from one machine step and shows each one respects the ‘missing reads as zero’ equivalence. It is the only place the proof looks inside the Sail model as a whole.",
 r"""## Plain English

**Theorem (`Gen.stepOnce_resp`, Vsa/Densify/GenC.lean lines 108–111).** For all counters, `stepOnce`
[respects](#/node/Vsa.Densify.halts_fillZero) memory equivalence.

It is the last of a long generated chain. Vsa/Densify/GenA.lean, GenB.lean and GenC.lean (about 1,370
lines in total) contain one lemma per Sail function, for example `should_inc_minstret`, `try_step` and
the instruction `execute`. Each one unfolds the function and calls the `resp_auto` tactic
(Vsa/Densify/Tactic.lean) with the lemmas for the functions it calls. Hand-written base cases cover reading
and writing registers and memory (Vsa/Densify/Resp.lean).

The README says the repository holds generated files "as they were produced", without the generator.
Here the kernel checks the output, so the missing generator is not part of the trusted base.
""",
 [q("How was this proof produced?",
    ["Generated: one lemma per Sail function, each closed by a tactic", "Hand-written for each instruction"], 0,
    "Vsa/Densify/GenA.lean, GenB.lean, GenC.lean."),
  q("Does trusting this result require trusting the generator?",
    ["No. The generated proofs are checked by Lean's kernel", "Yes"], 0,
    "The generated files are ordinary Lean proofs. They would fail to compile if wrong (the site did not build them)."),
  q("What is the ‘equivalence’ being respected?",
    ["Same registers and output; memories equal when missing bytes read as 0", "Bitwise-identical states"], 0,
    "SEqv and MemEqv, Vsa/Densify/Resp.lean lines 9–27."),
 ])
