import os
exec(open(os.path.join(os.path.dirname(__file__), "_common.py")).read())

LEAN = "../b4-lean/#/node/"

node("Laws",
 "Headline (CHECKED-BY-BEND): the 94 laws in LAWS.bend",
 "94 equations about single instructions, faults, scheduling and memory layout, each for every machine state that fits. PROOF.bend proves all 94, mostly by computation, and the project's `make check` runs Bend's checker on them. No law is about a whole program, the float ops, or a fleet.",
 r"""## Plain English

**What a law is, in Bend's own terms.** In the Bend language this code is written for (the dependently typed
Bend at bendlang/bend; the README links the older HigherOrderCO repository), the Bend guide says "Theorems ==
laws, Proofs == defs". A `law` names a claim; `for x: T` lines quantify over variables; the body
`{lhs == rhs : T}` is an equality type. Somewhere a `def` with the law's name must inhabit it. Here that is
[PROOF.bend](#/node/Proofs), which imports LAWS.bend as `L` and defines `L.add`, `L.subtract`, … one per law.
The header comment (""" + L("LAWS.bend", 1, 2) + r""") says "Agreed B4 contracts. Proofs live separately in
PROOF.bend."

**What checks them.** The Makefile's `check` target runs `bend PROOF.bend` (""" + L("Makefile", 9, 10) + r"""),
and the project's test script `imp/test-bend` runs `make check b4i` before any tanco suite. The repository's
AGENTS.md tells contributors to run `bend imp/bend/PROOF.bend` before committing. By the Bend guide, running
`bend` on a file with no `main` only checks it. **Nothing was run for this site**, and the repository holds no
log of a run, so "CHECKED-BY-BEND" here means: complete-looking proofs, wired into the project's own check.

### The 94 laws, by kind

| Kind | Count | Where | Example |
|---|---|---|---|
| mode codes vo ru na ti = 0 1 2 3 | 4 | """ + L("LAWS.bend", 6, 13) + r""" | `state_na` |
| one opcode through `execute`, enough stack: ad sb ml an or xr eq lt nt du zp sw ov dc cd, five constants | 20 | """ + L("LAWS.bend", 15, 258) + r""" | `add` |
| nop, db, hl, `rt` with 0 on top | 4 | """ + L("LAWS.bend", 260, 302) + r""" | `top_return` |
| concrete faults (one item for ad, empty cs for cd, divisor 0, shift 32 and −32, address 65,536 or 65,533, byte BF) | 11 | """ + L("LAWS.bend", 304, 434) + r""" | `zero_division` |
| tick leaves vo, na, ti alone; a fault does not advance | 4 | """ + L("LAWS.bend", 436, 486) + r""" | `idle_na` |
| one opcode through `microcode`: dv md sh, memory, literals, jumps, register blocks | 21 | """ + L("LAWS.bend", 488, 766) + r""" | `call` |
| `accepted_instruction`: checks pass ⇒ execute = microcode | 1 | """ + L("LAWS.bend", 768, 781) + r""" | |
| `atomic_*`: a fault changes only the control record | 7 | """ + L("LAWS.bend", 783, 865) + r""" | `atomic_address` |
| advance adds 1 in vo, ru, ti | 3 | """ + L("LAWS.bend", 867, 904) + r""" | |
| `run`: zero fuel; idle modes; one more fuel = one tick first | 5 | """ + L("LAWS.bend", 906, 950) + r""", """ + L("LAWS.bend", 1117, 1120) + r""" | `run_successor` |
| `fleet_isolation` | 1 | """ + L("LAWS.bend", 952, 956) + r""" | |
| `valid_*` and `*_fault`: with a hypothesis about the operand | 10 | """ + L("LAWS.bend", 958, 998) + r""", """ + L("LAWS.bend", 1023, 1115) + r""" | `division_fault` |
| little-endian store and load | 2 | """ + L("LAWS.bend", 1000, 1021) + r""" | |
| `emit` (io command 101) | 1 | """ + L("LAWS.bend", 701, 711) + r""" | |

(Counts add to 94; """ + L("LAWS.bend", 1, 1120) + r""".)

### What the laws do say

* **`add`** (""" + L("LAWS.bend", 15, 26) + r"""): for *every* memory, stacks, pointer, control record and output,
  executing byte 128 on a data stack whose top two items are b over a gives the same machine with a + b in their
  place. Because it quantifies over the control record, it also says `execute` ignores the mode (the mode is
  checked by `tick`).
* **The fault laws** say both halves: `valid_divide` (""" + L("LAWS.bend", 958, 970) + r""") gives the quotient
  when the divisor is non-zero, and `division_fault` (""" + L("LAWS.bend", 1023, 1035) + r""") gives the
  unchanged machine in mode na when it is zero.
* **`fleet_isolation`** (""" + L("LAWS.bend", 952, 956) + r""") says ticking a pair of sub-fleets is ticking each
  half. That is just the definition of `fleet_tick` ([fleet tree](#/node/FleetTree)): true and useful for
  reading, but it does not by itself show that machines cannot interfere (they can't, because each has its own
  memory value, but no law says so).

### What they don't say

* Nothing about **more than one step**, except that `run` with n+1 fuel is `run` with n after one `tick`.
  No law is about a program: not the square-root search, not Mandelbrot, not the console.
* Nothing about the **float ops** or `io` commands other than 101.
* Nothing about the **Lean** version or any other implementation. Agreement between implementations rests on the
  shared tanco suite b4-tests.org (TESTED).
* Many laws are close restatements of the code (`microcode` case = law). That is deliberate for a contract file:
  they freeze today's behaviour so a later edit that changes it fails `make check`.

Compare the Lean side: its [step lemmas](""" + LEAN + r"""step_binop) are about a total interpreter with no
fault state and need "the stack has enough items" hypotheses; the Bend laws cover both the enough and the
not-enough cases.
""",
 [q("In Bend, what is a `law`?",
    ["A claim (a type) that must be proved by a def with the same name, here in PROOF.bend",
     "A runtime assertion checked on every step", "A comment", "A unit test with fixed inputs"], 0,
    "Bend guide ('Theorems == laws, Proofs == defs'); PROOF.bend imports LAWS.bend as L and defines L.add etc., " + L("PROOF.bend", 1, 18) + "."),
  q("Which of these is stated by a law?",
    ["dv with a zero divisor leaves the machine unchanged except for mode na and reason division-by-zero",
     "The swarm finds the square root of 10000", "fa adds two floats correctly", "Bend and Lean agree"], 0,
    "`division_fault`, " + L("LAWS.bend", 1023, 1035) + ". None of the others has a law."),
  q("Does `law add` apply when the machine's mode is ti?",
    ["Yes: it quantifies over every control record; execute does not look at the mode", "No, only in ru", "Only in na"], 0,
    L("LAWS.bend", 15, 26) + "; `execute`, " + L("vm.bend", 757, 760) + "."),
  q("How do we know Bend's checker accepts PROOF.bend at this commit?",
    ["We don't, directly: the project's Makefile and test script run it, but nothing was run for this site and no log is in the repo",
     "The site re-ran it", "There is a CI badge"], 0,
    L("Makefile", 9, 10) + "; imp/test-bend runs `make check b4i`."),
  q("What does `fleet_isolation` prove?",
    ["That ticking Both{left, right} is Both of the ticked halves, which is fleet_tick's definition",
     "That machines cannot read each other's memory", "That the fleet runs on the GPU"], 0,
    L("LAWS.bend", 952, 956) + " and " + L("vm.bend", 809, 815) + "."),
 ],
 caveats=["CHECKED-BY-BEND means: PROOF.bend gives a proof for every law and the project's `make check` (run by imp/test-bend, and required by AGENTS.md before commits) runs Bend's checker on it. Nothing was run for this site. The Makefile uses plain `bend PROOF.bend`, not the `--verdict` flag that the Bend guide says rechecks proofs with a small kernel, so the trust base is Bend's ordinary checker.",
          "The meaning of `law`, `for`, `{a == b : T}`, `{==}` and `%` is taken from the Bend guide (bendlang/bend, guide/GUIDE.md), not from this repository.",
          "The laws are about vm.bend only. b4i.bend, live.bend, swarm.bend and mandelbrot.bend are not imported by PROOF.bend, so none of their functions is covered."],
 widgets=walk("How a law gets checked (LAWS.bend, lines 1-1120; PROOF.bend, lines 1-328)", [
  {"text": "LAWS.bend states `law add`: for all mem, ds, cs, ip, control, out, a, b, execute(128, …b, a…) equals the machine with a+b on top (LAWS.bend lines 15–26)."},
  {"text": "PROOF.bend defines `L.add` with the same variables, and its body is `{==}` (PROOF.bend lines 17–18).", "link": "Proofs"},
  {"text": "`{==}` asks the checker to compute both sides. With the opcode fixed at 128 and the stack's top two cells known, `supported`, `enough`, `operands` and `commit` all reduce, leaving the microcode case for ad.", "link": "Validation"},
  {"text": "Both sides become the same term, so the equality holds for every value of the variables."},
  {"text": "`make check` runs `bend PROOF.bend` (Makefile lines 9–10), and imp/test-bend runs it before the tanco suites."},
 ]))

node("Proofs",
 "PROOF.bend: proofs by computation",
 "Almost every proof in PROOF.bend is the single token `{==}`: the checker computes both sides of the law and finds the same term. The rest add a case split (on fuel or on the mode), one rewrite with a hypothesis (`%`), or a small helper lemma. No proof needs induction.",
 r"""## Plain English

**File (""" + L("PROOF.bend", 1, 328) + r""").** 94 definitions, one per [law](#/node/Laws). By the Bend guide,
"`{==}` proves it when both sides compute to the same term", and `%e : P` rewrites the goal using an equation `e`.

| How | Laws | Example |
|---|---|---|
| `{==}` alone | 78 | `L.add`, """ + L("PROOF.bend", 17, 18) + r""" |
| case split on fuel, `{==}` in each case | `run_idle_vo`, `run_idle_na`, `run_idle_ti` | """ + L("PROOF.bend", 248, 267) + r""" |
| rewrite with the hypothesis (`%Equal.sym(…)`) | `accepted_instruction`, 3 `valid_*`, 7 `*_fault` | """ + L("PROOF.bend", 272, 274) + r""" |
| helper lemma `hop_fusion` | `hop` | """ + L("PROOF.bend", 173, 184) + r""" |
| case split on the mode, reusing `run_idle_*` | `run_successor` | """ + L("PROOF.bend", 318, 327) + r""" |

### Why computation is enough

The laws fix the opcode and the shape of the top of the stack, so every `match` in `execute` can choose a
branch: the opcode case in `supported` and `need_data`, the list cases in `enough`, the operand checks. The
remaining variables (the rest of the stack, memory, the pointer) just pass through. For the fault laws with a
hypothesis such as "`U32.is_ne(b, 0)` is False", the check cannot pick a branch until the proof rewrites that
expression to `False{}` using the hypothesis; that is the `%` step.

**`hop_fusion`** (""" + L("PROOF.bend", 173, 180) + r"""): the microcode for `hp` reads the offset through two
nested `pair` continuations ([why](#/node/MachineState)), and the law states it with one. The helper takes the
(memory, byte) pair apart and then both sides compute to the same term.

**`run_successor`** (""" + L("PROOF.bend", 318, 327) + r"""): for a running machine, run(n+1) unfolds to
run(n, tick) directly. For the three idle modes, both sides reduce to the machine itself, using `run_idle_*`.

### Status

**CHECKED-BY-BEND** in the sense on the [laws](#/node/Laws) page: the project's `make check` runs it; it was not
run here. A grep of PROOF.bend and LAWS.bend finds no `@unsafe`, which the Bend guide says would make a check
report "SOME PROOFS FAIL". (`@unsafe` appears only on the input loops of b4i.bend and live.bend, which PROOF.bend
does not import.)
""",
 [q("What does `{==}` prove?",
    ["An equality whose two sides compute to the same term", "Any equality, unchecked", "That a test passed"], 0,
    "Bend guide; used throughout " + L("PROOF.bend", 1, 328) + "."),
  q("Why do the `*_fault` proofs need a rewrite?",
    ["Their hypothesis (for example, divisor test = False) must be substituted before the check can choose the fault branch", "Because they use induction", "Because they are about floats"], 0,
    L("PROOF.bend", 290, 316) + "."),
  q("Does any proof here use induction?",
    ["No: the fuel proofs split into 0 and n+1 but never call themselves", "Yes, run_successor", "Yes, all of them"], 0,
    L("PROOF.bend", 248, 267) + ", " + L("PROOF.bend", 318, 327) + "."),
 ],
 caveats=["The counts (78 by `{==}` alone, 3, 11, 1, 1) are from reading the file, not from a tool.",
          "The reading of `%` as 'rewrite the goal with this equation' is from the Bend guide. I have not checked what Bend does at this commit's version of the language."])

node("TestsOrg",
 "tests.org and the shared suite: what is TESTED",
 "`./test bend` runs Bend's check on PROOF.bend, builds the b4i console, then runs two tanco suites through it: the shared b4-tests.org (55 tests every implementation runs) and Bend's own tests.org (40 tests of strict faults, signed arithmetic and floats).",
 r"""## Plain English

**Files.** The runner is imp/test-bend (outside imp/bend): it runs `make check b4i`, then
`tanco_run b4-tests.org` and `tanco_run imp/bend/tests.org`, both against the compiled `imp/bend/b4i`.
tanco feeds the `>` lines to the [console](#/node/B4iShell) and compares the output with the expected lines.

**tests.org** (""" + L("tests.org", 1, 329) + r"""), 40 tests:

* out-of-range `cl` and `hp` fault without moving (""" + L("tests.org", 7, 30) + r""");
* modes and `/o`, `/t` (""" + L("tests.org", 32, 38) + r""");
* every fault reason, with the stacks shown unchanged (""" + L("tests.org", 40, 90) + r""",
  """ + L("tests.org", 116, 183) + r""");
* signed division, wrap-around, signed compare, logical right shift (""" + L("tests.org", 92, 114) + r""");
* atomic `h0` and `nx`, call/return, return to 0, faults inside a call, repair and retry, offline calculator
  (""" + L("tests.org", 185, 277) + r""");
* the six float ops (""" + L("tests.org", 279, 329) + r""").

**What "TESTED" means here.** These are fixed inputs with recorded outputs, run by the project's script. The
files contain no run log, and nothing was run for this site. The demos (swarm, Mandelbrot, live, fleet test)
are **not** part of `./test bend`.
""",
 [q("Which tests does `./test bend` run?",
    ["make check (PROOF.bend), then b4-tests.org and imp/bend/tests.org through the Bend b4i", "Only PROOF.bend", "The Mandelbrot demo"], 0,
    "imp/test-bend; " + L("Makefile", 6, 10) + "."),
  q("Is the square-root swarm part of the test suite?",
    ["No; it is a demo program", "Yes, in tests.org", "Yes, in LAWS.bend"], 0,
    "Neither tests.org nor imp/test-bend mentions swarm.bend; " + L("tests.org", 1, 5) + "."),
  q("What does tests.org check that the laws do not?",
    ["The float ops, through the console", "Nothing", "The live shell"], 0,
    L("tests.org", 279, 329) + "; no law mentions opcodes A0–A5."),
 ])
