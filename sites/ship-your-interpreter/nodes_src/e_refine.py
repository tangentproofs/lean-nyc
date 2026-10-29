NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

# ---------------------------------------------------------------- D. abstract refinement

node("Vsa.Lang.OutSim",
 "OutSim: what the interpreter proof must deliver",
 "OutSim asks for just two one-way facts about a loaded program: a normal result becomes a clean machine halt with the same output, and no normal result means the machine diverges or exits nonzero. Machine determinism does the rest.",
 r"""## Plain English

**Structure (`OutSim`, Vsa/Lang/Basic.lean lines 133–136).** For a source semantics `S` (a program and its
output) and a loading relation, `OutSim` has two fields:

- **term_sim**: if `p` is loaded in `c` and `S p out`, then `c` [halts](#/node/Vsa.Machine.Halts) with
  output `out` and code 0;
- **stuck_sim**: if `p` is loaded in `c` and has no `out` with `S p out`, then `c`
  [diverges](#/node/Vsa.Machine.Diverges) or halts with some code `e ≠ 0`.

It is a special case of the general `Lang.Sim` (lines 39–42) for languages observed only through clean
exits (`ofOutput`, lines 121–126). `OutSim.sim` and `OutSim.of_sim` (lines 140–146) convert between the two.

Note what is *not* asked: no claim about intermediate states, no backward simulation. The two-way
statement of the main theorem comes from [determinism](#/node/Vsa.Machine.Halts.deterministic).
""",
 [q("What does term_sim require?",
    ["A normal result out makes the loaded machine halt with code 0 and output out", "The machine never halts", "The program type-checks"], 0,
    "Vsa/Lang/Basic.lean line 134."),
  q("What does stuck_sim allow when the program has no normal result?",
    ["Divergence, or a halt with a nonzero code", "Only divergence", "Only exit code 70"], 0,
    "Vsa/Lang/Basic.lean lines 135–136."),
  q("Is a backward simulation (machine to source) required?",
    ["No. Determinism derives the backward direction", "Yes"], 0,
    "Vsa/Lang/Basic.lean lines 51–61."),
 ])

node("Vsa.Lang.Lang.Sim.refinement",
 "Determinism turns simulation into refinement",
 "From forward simulation plus machine determinism: for observable exit codes, the source says (e, out) iff the machine halts with (e, out), and a diverging machine means no source result. This 20-line argument is the whole ‘why an iff’.",
 r"""## Plain English

**Theorem (`Sim.refinement`, Vsa/Lang/Basic.lean lines 68–71)**, with its two helpers:

- **`Sim.spec_of_halts`** (lines 51–61). Suppose the machine halts with an observable code `e` and output
  `out`. If the source has *some* result (`e'`, `out'`), simulation makes the machine halt with it, and
  [determinism](#/node/Vsa.Machine.Halts.deterministic) says it is the same halt, so the source has (`e`, `out`).
  If the source has *no* result, the stuck case says the machine diverges, which contradicts halting
  ([Diverges.not_halts](#/node/Vsa.Machine.Diverges.not_halts)), or halts unobservably, which contradicts `e`
  being observable.
- **`Sim.no_spec_of_diverges`** (lines 63–65). A source result would make the machine halt, contradicting
  divergence.

The conclusion `Refines` (lines 45–47) bundles the "iff" for observable codes with the divergence clause.
The module comment at lines 1–17 describes the design.

This step is language-independent. The same argument would serve another interpreter on this machine
(docs/PORTING.md).
""",
 [q("Which machine property is essential for the ‘if’ direction?",
    ["Determinism of halting", "Termination", "Memory safety"], 0,
    "Vsa/Lang/Basic.lean line 56 uses Halts.deterministic."),
  q("How long is the argument?",
    ["About 20 lines; all the hard work is in the simulation", "Thousands of lines"], 0,
    "Vsa/Lang/Basic.lean lines 51–71."),
  q("Is it specific to WHILE?",
    ["No. It is stated for any Lang", "Yes"], 0,
    "Vsa/Lang/Basic.lean lines 23–31 define the general Lang."),
 ])

node("Vsa.Lang.OutSim.refinement",
 "Refinement for an output-only language",
 "OutSim.refinement specialises the generic theorem to clean-exit languages: S p out iff the machine halts with code 0 and output out, and divergence means no result. With S = BigStep this is exactly the shape of the main theorem.",
 r"""## Plain English

**Theorem (`OutSim.refinement`, Vsa/Lang/Basic.lean lines 149–155).** If [OutSim](#/node/Vsa.Lang.OutSim)
holds for `S` at a loading relation, then for every loaded `p` and `c`:

1. for all `out`, `S p out` iff `c` halts with output `out` and code 0;
2. if `c` diverges, `S p` has no output.

It converts the `OutSim` to `Lang.Sim`, applies [Sim.refinement](#/node/Vsa.Lang.Lang.Sim.refinement), and
reads off the code-0 instance.

`Vsa.Refine.refinement` (Vsa/Refinement.lean lines 21–25) is this theorem at `S = BigStep`. The main
theorem uses the zero-filled variant [OutSim.refinement_fillZero](#/node/Vsa.Lang.OutSim.refinement_fillZero).
""",
 [q("What is S in the main theorem?",
    ["BigStep", "ExecSeqCost", "Halts"], 0,
    "Vsa/Refinement.lean lines 16–19."),
  q("Which exit code does this theorem talk about?",
    ["Only 0", "Every code"], 0,
    "ofOutput observes only e = 0 (Vsa/Lang/Basic.lean lines 121–126)."),
  q("What does it add on top of Sim.refinement?",
    ["Only the specialisation to clean exits", "A new simulation proof"], 0,
    "Vsa/Lang/Basic.lean lines 149–155."),
 ])

node("Vsa.Lang.OutSim.refinement_fillZero",
 "The refinement, stated on zero-filled memory",
 "The last step of the main proof: refinement where loading is stated on fillZero c but halting and divergence are about c itself. It holds because zero-filling never changes a run.",
 r"""## Plain English

**Theorem (`OutSim.refinement_fillZero`, Vsa/Lang/Densify.lean lines 31–38).** If `OutSim` holds and
`fillZero c` is loaded with `p`, then `S p out` iff `c` (not the zero-filled one) halts with (0, `out`), and if `c`
diverges, `p` has no result.

Proof: apply [OutSim.refinement](#/node/Vsa.Lang.OutSim.refinement) to `fillZero c`, then move halting and
divergence back to `c` with [halts_fillZero](#/node/Vsa.Densify.halts_fillZero) and `diverges_fillZero`.

With the interpreter's simulation [interpSim_iris](#/node/VsaIris.Interp.interpSim_iris), this is
[endToEnd_refinement](#/node/Vsa.Sim.EndToEnd.endToEnd_refinement).
""",
 [q("In the conclusion, is halting about c or fillZero c?",
    ["About c", "About fillZero c"], 0,
    "Vsa/Lang/Densify.lean line 34."),
  q("Which lemmas move the conclusion from fillZero c to c?",
    ["halts_fillZero and diverges_fillZero", "boot_of_loaded"], 0,
    "Vsa/Lang/Densify.lean lines 37–38."),
  q("Is this step specific to the WHILE interpreter?",
    ["No. It works for any OutSim", "Yes"], 0,
    "It is stated for an arbitrary S and loading relation (Vsa/Lang/Densify.lean lines 31–33)."),
 ])

node("Vsa.Refine.refinement",
 "Refinement for WHILE at any layout",
 "Vsa.Refine.refinement is OutSim.refinement for BigStep at a layout's Loaded relation. It is the form used by endToEnd_refinement_loaded.",
 r"""## Plain English

**Theorem (`refinement`, Vsa/Refinement.lean lines 21–25).** For any layout `L`, if the interpreter
simulates `BigStep` at `Loaded L` (`InterpSim L`, line 19), then for every loaded `p`, `c`: `BigStep p out` iff
`c` halts with (0, `out`), and divergence rules out a result.

It is one line, [OutSim.refinement](#/node/Vsa.Lang.OutSim.refinement). It is stated separately so that
the WHILE-specific names (`whileLang`, `InterpSim`) have a home.
""",
 [q("What is InterpSim L?",
    ["OutSim for BigStep at Loaded L", "A Sail property"], 0,
    "Vsa/Refinement.lean line 19."),
  q("Is this theorem tied to the committed ELF?",
    ["No. It holds for any layout", "Yes"], 0,
    "The layout L is a parameter (Vsa/Refinement.lean line 21)."),
  q("Which headline uses it directly?",
    ["endToEnd_refinement_loaded", "endToEnd_checked"], 0,
    "VsaIris/Interp/EndToEnd.lean line 157."),
 ])
