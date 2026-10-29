NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

# ---------------------------------------------------------------- E. machine program logic

node("VsaIris.MachineModel",
 "A machine as an Iris language",
 "The interface for a machine Iris can reason about: states, a step function (next, halt with code and output, or stuck), and readers for registers, memory and output. It is embedded in iris-lean as a one-expression language that keeps stepping.",
 r"""## Plain English

**Structure (`MachineModel`, VsaIris/Machine.lean lines 15–24).** A machine model has

- a type of states;
- a **step** function whose result is *next state*, *halt with exit code and output*, or *stuck* (lines 5–8);
- functions reading a 64-bit register and an 8-bit memory byte from a state;
- the output so far, and a well-formedness predicate `ok`.

The file then makes it an Iris *language* with a single expression, `Loop`, whose primitive step runs the
machine's step (line 111 onwards). An Iris weakest precondition for `Loop` is a statement about running
the machine. Separate ghost state gives ownership of registers (`r ↦ᵣ v`), memory bytes (`a ↦ₘ b`) and the
console (VsaIris/Ptsto.lean lines 44–93).

The RISC-V instance is [vsaModel](#/node/VsaIris.Inst.vsaModel).
""",
 [q("What can the step function return?",
    ["Next state, halt with code and output, or stuck", "Only next state"], 0,
    "VsaIris/Machine.lean lines 5–8."),
  q("How is the machine embedded in Iris?",
    ["As a language whose only expression, Loop, steps the machine", "As a C program"], 0,
    "VsaIris/Machine.lean line 111 onwards."),
  q("Is this interface specific to RISC-V?",
    ["No. vsaModel is one instance", "Yes"], 0,
    "VsaIris/Vsa/Instance.lean lines 33–39 instantiate it."),
 ])

node("VsaIris.Inst.vsaModel",
 "The RISC-V machine as a MachineModel",
 "vsaModel plugs the Sail-based stepOnce into the Iris machine interface. Its step agrees exactly with the Step and Halted relations used in the main theorem, so facts proved in Iris transfer to Halts and Diverges with no gap.",
 r"""## Plain English

**Definitions (VsaIris/Vsa/Instance.lean lines 15–39).**

- `vsaStep` (lines 15–19) runs [stepOnce](#/node/Vsa.stepOnce): an `.ok` non-exit becomes *next*, an exit with
  code `e` becomes *halt e* with the current console output, and anything else (a Sail error) is *stuck*.
- `vsaReg` reads the PC or a general register; memory reads a missing byte as 0.
- `VsaOk` (lines 26–31) is the well-formedness invariant: a good Sail state, the tick counter below 2,
  all general registers defined, every "live" code byte present, and HTIF idle.
- `vsaModel live` (lines 33–39) packages these.

The bridge lemmas right after (lines 41–78) show that `vsaStep` returning *next* is exactly
[Step](#/node/Vsa.Machine.Halts) and *halt* is exactly `Halted`. So an Iris adequacy statement about
`vsaModel` becomes a statement about `Halts` and `Diverges`.
""",
 [q("What does vsaStep do on a Sail error?",
    ["Reports stuck", "Halts with code 0", "Retries"], 0,
    "VsaIris/Vsa/Instance.lean line 19."),
  q("Why do the bridge lemmas matter?",
    ["They make Iris results about vsaModel into facts about Vsa.Machine.Halts and Diverges", "They speed up the proof"], 0,
    "VsaIris/Vsa/Instance.lean lines 41–78."),
  q("What does the parameter `live` control?",
    ["Which memory addresses must be present (code bytes) in VsaOk", "Which registers exist"], 0,
    "VsaIris/Vsa/Instance.lean line 30."),
 ])

node("VsaIris.MachWP",
 "Two weakest preconditions: total and partial",
 "The proof uses two WPs over the machine. twpW is total: it can only be proved if the code terminates. wpW is partial: it allows running forever, and its recursion is guarded by Iris's ‘later’. The interpreter proof is written once against the common interface MachWP and run twice.",
 r"""## Plain English

**Structure (`MachWP`, VsaIris/MachWP.lean lines 11–29).** An abstract weakest precondition `W Φ` with:

- `lagRun`: if a stretch of machine code with a known footprint runs from a state satisfying `Pre` to one
  satisfying `Post`, it can be stepped over;
- `halt`: if the machine is about to exit, `Φ` must hold of (code, output);
- `fupd`: Iris updates can be absorbed;
- a "later" modality `lat` used when stepping. For the total WP it is the identity. For the partial one
  it is Iris's `▷`.

**Instances.**

- **`twpW`** (lines 33–50) uses Iris's *total* WP (`mTWP`). Adequacy for it proves **termination**
  (VsaIris/Adequacy.lean lines 83–100 use iris-lean's `twp_total`).
- **`wpW`** (lines 52–71) uses the ordinary *partial* WP (`mWP`), where `▷` allows recursion through Löb
  induction, which is what you need for loops that may not terminate.

Many specifications in `VsaIris/Interp/` are stated for an arbitrary `MachWP`, so one proof serves both
the [terminating case](#/node/VsaIris.Interp.interpSeqT_all) and the
[partial case](#/node/VsaIris.Interp.specsP_all).
""",
 [q("Which WP proves that the machine terminates?",
    ["twpW, the total WP", "wpW, the partial WP"], 0,
    "VsaIris/MachWP.lean lines 33–50 and VsaIris/Adequacy.lean lines 83–100."),
  q("Why is a partial WP needed at all?",
    ["Programs with no normal result may run forever, and the stuck case must still say something", "For speed"], 0,
    "stuck_sim allows divergence (Vsa/Lang/Basic.lean lines 135–136)."),
  q("How do proofs avoid being written twice?",
    ["Specifications are stated for an abstract MachWP and instantiated with both", "They are written twice"], 0,
    "VsaIris/MachWP.lean lines 11–29."),
 ])

node("VsaIris.mach_adequacy",
 "Adequacy: a closed total WP proof means the machine halts",
 "If, from ownership of the initial registers, memory bytes and console, one can prove the total WP with a pure postcondition φ, then the machine really halts and φ holds of its exit code and output. This is where Iris proofs become plain facts.",
 r"""## Plain English

**Theorem (`mach_adequacy`, VsaIris/Adequacy.lean lines 150–155).** Take a state `σ`, a register map and a
memory map that agree with `σ`, and suppose `σ` is well-formed. Suppose that from the corresponding Iris
resources one can prove the total WP with postcondition `φ` (this hypothesis is `AdequacyHyp`, lines 48–53).
Then the machine halts from `σ` with some code `e` and output `out`, and `φ (e, out)` holds.

It combines two iris-lean results:

- *strong normalisation* from the total WP (`mach_sn`, lines 83–100, via iris-lean's `twp_total`), and
- *adequacy* (`mach_adequate`, lines 102–117, via `wp_adequacy_gen`). The run is not stuck, and any
  result satisfies the postcondition.

`halts_of_sn_adequate` (lines 119–148) turns those into a halting run.

For the RISC-V model, [vsa_adequacy_exit](#/node/VsaIris.Inst.vsa_adequacy_exit) restates it with
`Vsa.Machine.Halts`.
""",
 [q("What does the hypothesis AdequacyHyp say?",
    ["From the initial register, memory and console resources, the total WP with postcondition φ holds", "The machine halts"], 0,
    "VsaIris/Adequacy.lean lines 48–53."),
  q("What does the conclusion give?",
    ["A real halting run whose (code, output) satisfies φ", "Another Iris proposition"], 0,
    "VsaIris/Adequacy.lean line 153."),
  q("Which external library provides the core adequacy theorems?",
    ["iris-lean", "Mathlib", "Sail"], 0,
    "VsaIris/Adequacy.lean lines 1–3 import Iris.ProgramLogic.TotalAdequacy and Adequacy."),
 ],
 caveats=["The soundness of iris-lean's adequacy and total-adequacy theorems is a dependency, pinned at rev 740e2c4 in lakefile.toml. This site did not inspect that library."])

node("VsaIris.mach_adequacyP",
 "Adequacy for the partial WP: diverge or halt well",
 "From a closed partial-WP proof with pure postcondition φ: either runs of every length exist (the machine diverges) or the machine halts with a result satisfying φ. Being stuck is ruled out.",
 r"""## Plain English

**Theorem (`mach_adequacyP`, VsaIris/Adequacy.lean lines 222–226).** As [mach_adequacy](#/node/VsaIris.mach_adequacy),
but with the partial WP (hypothesis `AdequacyHypP`, lines 157–162). The conclusion is weaker: for every
`n` there is an `n`-step run, **or** the machine halts with (`e`, `out`) satisfying `φ`.

The proof uses iris-lean's adequacy in "not stuck" mode (`mach_adequateP`, lines 164–178). Every reachable
state can step or halt, and `diverges_or_halts_of_adequate` (lines 201–220) splits on whether a halt is
ever reached.

[vsa_adequacyP](#/node/VsaIris.Inst.vsa_adequacyP) restates it with `Vsa.Machine.Diverges` and `Halts`. It
provides the stuck half of the simulation.
""",
 [q("What does the partial adequacy theorem rule out?",
    ["Getting stuck, and halting with a result that violates φ", "Divergence"], 0,
    "VsaIris/Adequacy.lean lines 222–226."),
  q("Which half of OutSim does it serve?",
    ["stuck_sim", "term_sim"], 0,
    "VsaIris/Lang/Route.lean lines 56–58."),
  q("Does it prove termination?",
    ["No. Divergence is one allowed outcome", "Yes"], 0,
    "VsaIris/Adequacy.lean line 225."),
 ])

node("VsaIris.Inst.vsa_adequacy_exit",
 "Adequacy for the RISC-V machine",
 "vsa_adequacy_exit and vsa_adequacyP are the two adequacy theorems restated for vsaModel, with conclusions in terms of Vsa.Machine.Halts and Diverges, the same predicates as in the main theorem.",
 r"""## Plain English

**Theorems (VsaIris/Vsa/Instance.lean lines 80–101).**

- `vsa_adequacy_exit` (lines 80–89): from initial resources agreeing with configuration `c`, `VsaOk c`, and
  a total WP with postcondition `φ`, there are `e` and `out` with `Halts c out e` and `φ (e, out)`.
- [vsa_adequacyP](#/node/VsaIris.Inst.vsa_adequacyP) (lines 91–101): with the partial WP, `c` diverges or halts
  with a result satisfying `φ`.

Each one applies the generic theorem ([mach_adequacy](#/node/VsaIris.mach_adequacy) or
[mach_adequacyP](#/node/VsaIris.mach_adequacyP)) and translates runs with the bridge lemmas of
[vsaModel](#/node/VsaIris.Inst.vsaModel).
""",
 [q("Which configuration predicate must hold initially?",
    ["VsaOk", "Loaded", "Nothing"], 0,
    "VsaIris/Vsa/Instance.lean line 83."),
  q("Are the conclusions about the same Halts as the main theorem?",
    ["Yes, Vsa.Machine.Halts", "No, an Iris-internal notion"], 0,
    "VsaIris/Vsa/Instance.lean line 85."),
  q("Where are they used?",
    ["In IrisRoute.sim", "In the Sail model"], 0,
    "VsaIris/Lang/Route.lean lines 53 and 58."),
 ])

node("VsaIris.Inst.vsa_adequacyP",
 "Partial adequacy for the RISC-V machine",
 "If the partial WP with postcondition φ holds from resources matching c, then c diverges or halts with a result satisfying φ. This is the stuck half of the interpreter's simulation.",
 r"""## Plain English

**Theorem (`vsa_adequacyP`, VsaIris/Vsa/Instance.lean lines 91–101).** It is
[mach_adequacyP](#/node/VsaIris.mach_adequacyP) for [vsaModel](#/node/VsaIris.Inst.vsaModel). The "runs of every
length" disjunct becomes [Diverges](#/node/Vsa.Machine.Diverges), and the halt becomes [Halts](#/node/Vsa.Machine.Halts).

The interpreter uses it with the postcondition "exit code is not observable", that is, nonzero
([IrisRoute.sim](#/node/VsaIris.Lang.IrisRoute.sim)). The sharper postcondition "code 0 with a big-step
result, or code 70 or 1" is used in `partial_sim_of` (VsaIris/Interp/EndToEnd.lean lines 86–110).
""",
 [q("What are the two possible outcomes?",
    ["Divergence, or a halt satisfying φ", "Only a halt"], 0,
    "VsaIris/Vsa/Instance.lean line 96."),
  q("Which WP does it need?",
    ["The partial wpW / mWP", "The total twpW"], 0,
    "AdequacyHypP, VsaIris/Adequacy.lean lines 157–162."),
  q("Which postcondition does partial_sim_of use?",
    ["Code 0 with a big-step result, or an abort code (70 or 1)", "Always code 0"], 0,
    "VsaIris/Interp/EndToEnd.lean lines 92–93."),
 ])

node("VsaIris.Lang.RouteAt",
 "RouteAt: the Iris obligations at one configuration",
 "RouteAt bundles what an interpreter proof must provide at a loaded configuration: initial register and memory resources agreeing with it, well-formedness, a total WP ending at each specified (code, output), and a partial WP ending at an unobservable code when nothing is specified.",
 r"""## Plain English

**Structure (`RouteAt`, VsaIris/Lang/Route.lean lines 29–41).** For a language, a program `p` and a
configuration `c`:

- `mr`, `mm`: a register map and a byte map;
- `hr`, `hm`, `ok`: they agree with `c`, and `c` satisfies `VsaOk`;
- **`term`**: for every specified (`e`, `out`), the total-WP adequacy hypothesis with postcondition "the result
  is exactly (`e`, `out`)";
- **`stuck`**: if nothing is specified, the partial-WP hypothesis with postcondition "the code is not
  observable".

`IrisRoute` (lines 44–46) asks for a `RouteAt` at every loaded configuration. The module comment
(lines 4–14) describes the design. For the WHILE interpreter, `RouteAt` values come from
[routeAt_of_boot](#/node/VsaIris.Interp.routeAt_of_boot).
""",
 [q("Which WP must the term field provide?",
    ["The total one (AdequacyHyp)", "The partial one"], 0,
    "VsaIris/Lang/Route.lean lines 37–38."),
  q("What postcondition does the stuck field use?",
    ["The exit code is not observable", "The exit code is 0"], 0,
    "VsaIris/Lang/Route.lean lines 40–41."),
  q("Is RouteAt specific to WHILE?",
    ["No. It is stated for any Lang", "Yes"], 0,
    "VsaIris/Lang/Route.lean line 29."),
 ])

node("VsaIris.Lang.IrisRoute.sim",
 "From Iris obligations to simulation",
 "IrisRoute.sim: if every loaded configuration has its RouteAt, then forward simulation (Lang.Sim) holds. Each field goes through the matching adequacy theorem. This is the hinge between the program logic and the refinement argument.",
 r"""## Plain English

**Theorem (`IrisRoute.sim`, VsaIris/Lang/Route.lean lines 48–58).**

- **term**: get the `RouteAt` and apply [vsa_adequacy_exit](#/node/VsaIris.Inst.vsa_adequacy_exit) to its total
  WP. The machine halts with a result equal to (`e`, `out`).
- **stuck**: apply [vsa_adequacyP](#/node/VsaIris.Inst.vsa_adequacyP) to its partial WP. The machine diverges or
  halts with an unobservable code.

The result is `Lang.Sim` (Vsa/Lang/Basic.lean lines 39–42), which
[interpSim_iris](#/node/VsaIris.Interp.interpSim_iris) turns into [OutSim](#/node/Vsa.Lang.OutSim).
""",
 [q("What does IrisRoute.sim conclude?",
    ["Lang.Sim (forward simulation) at the loading relation", "The main theorem directly"], 0,
    "VsaIris/Lang/Route.lean line 49."),
  q("How long is the proof?",
    ["About ten lines, applying the two adequacy theorems", "Thousands of lines"], 0,
    "VsaIris/Lang/Route.lean lines 48–58."),
  q("What must the user of IrisRoute.sim supply?",
    ["A RouteAt for every loaded configuration", "A Sail proof"], 0,
    "VsaIris/Lang/Route.lean lines 44–46."),
 ])
