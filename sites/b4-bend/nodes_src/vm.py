import os
exec(open(os.path.join(os.path.dirname(__file__), "_common.py")).read())

LEAN = "../b4-lean/#/node/"

# ---------------------------------------------------------------- headline: one step

node("VMStep",
 "Headline (code): one step of the machine, and the fuelled run",
 "Status: CODE, TESTED, with CHECKED-BY-BEND laws. A step fetches the opcode, checks everything that could go wrong before touching the state, and then either runs the instruction or records a named fault and changes nothing else. `run` repeats this for a fixed amount of fuel.",
 r"""## Plain English

**Code (`execute`, `advance`, `fetch`, `step`, `tick`, `run`, """ + L("vm.bend", 740, 802) + r""").**
One step of the b4 machine, as Bend functions on the [machine state](#/node/MachineState).

1. **`step`** (""" + L("vm.bend", 779, 781) + r""") checks that the instruction pointer is a legal code address:
   at least 256 (below that are the registers and system cells) and below 65,536 (`code_ok`,
   """ + L("vm.bend", 632, 633) + r"""). If not, the machine faults with *invalid-address* at that pointer.
2. **`fetch`** (""" + L("vm.bend", 769, 777) + r""") reads the opcode byte and hands it to `execute`, then calls
   `advance`.
3. **`execute`** (""" + L("vm.bend", 757, 760) + r""") asks three questions in a fixed order
   ([validation](#/node/Validation)): is the opcode supported, does the data stack hold enough items, does the
   control stack? Then `validated` (""" + L("vm.bend", 747, 755) + r""") checks the operands (a zero divisor, an
   out-of-range shift, an address off the end of memory, a jump target outside code space).
4. **`commit`** (""" + L("vm.bend", 740, 745) + r""") either runs the opcode's [microcode](#/node/Microcode) or
   records the fault. A faulted machine has mode *na* (`Na`), the fault reason, and the address where it
   happened. Its stacks, memory and pointer are exactly as before.
5. **`advance`** (""" + L("vm.bend", 762, 767) + r""") adds 1 to the pointer, unless the machine has just
   faulted. Instructions with inline arguments (literals, jumps) have already moved the pointer to the last byte
   of the argument, so the +1 lands on the next instruction.

### Scheduling: `tick` and `run`

**`tick`** (""" + L("vm.bend", 783, 790) + r""") steps a machine only if its mode is *ru* (running). A
machine that is offline (*vo*), faulted (*na*) or stopped (*ti*) is returned unchanged. **`run`**
(""" + L("vm.bend", 792, 802) + r""") ticks a running machine up to `fuel` times and stops early as soon as the
machine is no longer running. Running out of fuel is not a fault: the comment at
""" + L("vm.bend", 792, 793) + r""" says the host may schedule the machine again, inspect it or take it offline.

Because `run` recurses on a natural number, Bend's termination check accepts it. The comment at
""" + L("b4i.bend", 407, 408) + r""" makes the point explicitly: only the console's input loop is marked
`@unsafe`; bytecode execution always has finite fuel.

### Compared with the Lean version

The [Lean interpreter](""" + LEAN + r"""runOp) has **no error state**: popping an empty stack gives 0, dividing by
zero pops both operands and pushes nothing, and a bad opcode does nothing. Here every one of those is a named
fault that leaves the machine as it was, so a host can fix the stack and retry (tests.org's
*bend.repair-and-retry*, """ + L("tests.org", 259, 269) + r"""). The Lean `step` lemmas need hypotheses that
the stack is deep enough; here the [laws](#/node/Laws) state both sides: what happens when the stack is deep
enough and what happens when it is not.
""",
 [q("A running machine executes `ad` with only one item on the data stack. What changes?",
    ["Only the control record: mode becomes na, reason data-underflow, at = the pointer. Stacks, memory and pointer are unchanged",
     "The single item is popped and 0 is used for the missing one",
     "The pointer advances and the stack is emptied",
     "Bend raises a runtime error"], 0,
    "`stack_check` reports DataUnderflow (" + L("vm.bend", 729, 738) + "), `commit` calls `fault` (" + L("vm.bend", 528, 530) + "), and `advance` does not move a faulted machine (" + L("vm.bend", 762, 765) + "). Law `add_underflow`, " + L("LAWS.bend", 304, 314) + "."),
  q("What does `tick` do to a machine whose mode is ti (stopped)?",
    ["Nothing: only ru machines are stepped", "It steps it once", "It restarts it", "It faults it"], 0,
    L("vm.bend", 785, 790) + "; laws `idle_vo`, `idle_na`, `idle_ti` at " + L("LAWS.bend", 436, 473) + "."),
  q("Why does `run` take a fuel argument?",
    ["So it always terminates, which Bend's termination check requires; running out of fuel just leaves a still-running machine",
     "Fuel is the machine's stack limit", "Fuel counts faults", "Bend has no loops"], 0,
    L("vm.bend", 792, 802) + " and the comment at " + L("b4i.bend", 407, 408) + "."),
  q("In what order are problems checked?",
    ["Unknown opcode, then data stack, then control stack, then operands",
     "Operands first, then stacks", "Only the data stack is checked", "Whatever the microcode hits first"], 0,
    "Comment at " + L("vm.bend", 684, 684) + "; `stack_check` at " + L("vm.bend", 729, 738) + " and `operands` at " + L("vm.bend", 686, 727) + "."),
 ],
 caveats=["Status: CODE. The step itself is not a claim. Its behaviour is pinned down instruction by instruction by the CHECKED-BY-BEND laws (wired into the project's `make check`, not re-run here) and exercised by the tanco suites b4-tests.org and tests.org (TESTED by the project's runner, not run here).",
          "Nothing in imp/bend states or proves anything about more than one step, apart from `run_successor` (run with n+1 fuel equals run with n fuel after one tick)."],
 widgets=walk("One step (vm.bend, lines 740-802)", [
  {"text": "`step`: is the pointer in code space, 256 to 65,535? If not, fault with invalid-address (lines 779–781, 769–772).", "link": "VMStep"},
  {"text": "`fetch`: read the opcode byte at the pointer (lines 773–777)."},
  {"text": "`execute`: supported opcode? enough data items? enough control items? (lines 757–760, 729–738)", "link": "Validation"},
  {"text": "`validated` then `operands`: divisor, shift amount, address and jump-target checks, depending on the opcode (lines 747–755, 686–727).", "link": "Validation"},
  {"text": "`commit`: run the microcode, or record the fault and change nothing else (lines 740–745).", "link": "Microcode"},
  {"text": "`advance`: pointer + 1 unless the machine just faulted (lines 762–767)."},
  {"text": "`tick` steps only ru machines; `run` repeats `tick` until fuel runs out or the machine stops (lines 785–802)."},
 ]))

# ---------------------------------------------------------------- state

node("MachineState",
 "The machine state: memory, two stacks, pointer, control record",
 "A b4 machine in Bend is one value: a byte array for memory, the data and control stacks as Bend lists (top first), the instruction pointer, a control record (mode, fault, fault address) and an output string. The four modes vo, ru, na, ti have the fixed codes 0 to 3.",
 r"""## Plain English

**Types (`Mode`, `Fault`, `Control`, `VM`, """ + L("vm.bend", 1, 26) + r""").**

* **Cells** are 32-bit unsigned numbers read as two's-complement bit patterns (""" + L("vm.bend", 1) + r""").
  Signed operations are written by hand on top of them ([arithmetic](#/node/Arithmetic)).
* **Memory** (`mem`) is a Bend `Array` of cells, one byte per slot. `boot` makes 2¹⁶ = 65,536 slots
  ([memory](#/node/Memory)).
* **Data stack** `ds` and **control stack** `cs` are Bend lists whose head is the top of the stack. Unlike the
  [Lean State](""" + LEAN + r"""State), which keeps the stacks inside memory with fixed capacities, these lists
  have no size limit, so there is no overflow fault.
* **`ip`**, the instruction pointer.
* **`control`**: a **mode** (""" + L("vm.bend", 4, 9) + r"""), a **fault reason** (""" + L("vm.bend", 11, 19) + r""")
  and the address `at` where the fault happened.
* **`output`**: characters written by the `io` [device](#/node/Device).

### The four modes ("vorunati")

| Mode | Code | Meaning |
|---|---|---|
| vo | 0 | offline |
| ru | 1 | running: `tick` will step it |
| na | 2 | faulted, with a reason and an address |
| ti | 3 | stopped (halted, or idle in the console) |

`mode_code` (""" + L("vm.bend", 517, 526) + r""") gives the codes, and the first four laws pin them
(""" + L("LAWS.bend", 6, 13) + r"""). The comment calls them "stable external state codes".

The eight fault reasons are `Clear` (no fault), data underflow, control underflow, address, zero divisor, shift
range, opcode and device. The console prints them as words such as `data-underflow` (`fault_text`,
""" + L("b4i.bend", 96, 113) + r""").

### Two Bend details

* `List<&2, U32>` is Bend's notation for a list whose elements may be copied. In the Bend guide `+List<U32>`
  is short for `List<&2, U32>`, and a `+` before a variable makes it reusable. Memory, by contrast, is an
  `Array`, which in Bend has exactly one owner at a time. That is why the code threads memory through every
  read and gets it back with each value (`pair` and `state`, """ + L("vm.bend", 29, 37) + r""").
* There is no "boot" mode: `boot` (""" + L("vm.bend", 122, 125) + r""") starts a machine in ti with the
  pointer at 256 and register `_` (the assembler's "here" pointer, at byte 124) set to 256.
""",
 [q("Where is the top of the data stack?",
    ["At the head of the Bend list `ds`", "At the last element of the list", "In memory at a fixed address"], 0,
    "Comment at " + L("LAWS.bend", 2) + "; every microcode case pushes with `x <> ds`, " + L("vm.bend", 127, 129) + "."),
  q("What is the mode code of a faulted machine?",
    ["2 (na)", "0 (vo)", "1 (ru)", "3 (ti)"], 0,
    L("vm.bend", 517, 526) + "; law `state_na`, " + L("LAWS.bend", 10, 11) + "."),
  q("Can the data stack overflow?",
    ["No: it is an unbounded Bend list and no fault reason covers overflow", "Yes, at 32 items", "Yes, at 256 items"], 0,
    "The `Fault` type has no overflow case, " + L("vm.bend", 11, 19) + "."),
 ],
 caveats=["The reading of `&2` and `+` comes from the Bend guide (bendlang/bend, guide/GUIDE.md), not from anything in this repository. It is not essential to the b4 semantics."])

node("Arithmetic",
 "Signed arithmetic on unsigned cells",
 "Cells are U32, so signed comparison, division, remainder and shifts are built by hand: flip the sign bit to compare, divide magnitudes and fix the sign, shift left for a positive count and right for a negative one.",
 r"""## Plain English

**Helpers (""" + L("vm.bend", 39, 83) + r""").**

* `negative` (""" + L("vm.bend", 42, 43) + r"""): the top bit is set. `negate` is 0 − x and `magnitude` is the
  absolute value.
* `truth` (""" + L("vm.bend", 54, 55) + r"""): true is all ones (−1), false is 0, as in every b4.
* `signed_lt` (""" + L("vm.bend", 57, 58) + r"""): XOR both numbers with 2³¹ and compare unsigned. That maps
  the signed order onto the unsigned one.
* `divide` (""" + L("vm.bend", 60, 62) + r"""): divide the magnitudes and negate if the signs differ, so the
  quotient **rounds toward zero**. `remainder` (""" + L("vm.bend", 64, 66) + r""") takes the sign of the
  dividend. tests.org checks −7 / 3 = −2, −7 mod 3 = −1, 7 / −3 = −2 and 7 mod −3 = 1
  (""" + L("tests.org", 92, 96) + r""").
* `shift` (""" + L("vm.bend", 68, 83) + r"""): a positive count shifts left, a negative count shifts **right,
  logically** (zeros come in at the top). If the magnitude of the count is 32 or more the result would be 0,
  but the [validation](#/node/Validation) step faults with *shift-out-of-range* before that can happen.
* `signed_byte` (""" + L("vm.bend", 51, 52) + r"""): sign-extends a byte, for `rs`, `ls` and hop offsets.

Edge case: the most negative number divided by −1 wraps back to itself, and the remainder is 0 (tests.org
*bend.wrap32*, """ + L("tests.org", 98, 102) + r""").
""",
 [q("How is `x lt y` (signed less-than) computed on U32 cells?",
    ["Flip the top bit of both and compare as unsigned", "Subtract and test the sign", "Convert to Int first"], 0,
    L("vm.bend", 57, 58) + "."),
  q("Which way does `dv` round −7 / 3?",
    ["Toward zero: −2", "Down: −3", "To nearest: −2 or −3"], 0,
    L("vm.bend", 60, 62) + "; tested at " + L("tests.org", 92, 96) + "."),
  q("What does a shift by −1 do to FFFFFFFF?",
    ["Logical right shift: 7FFFFFFF", "Arithmetic right shift: FFFFFFFF", "Left shift"], 0,
    L("vm.bend", 68, 80) + "; tested at " + L("tests.org", 110, 114) + "."),
 ])

node("Memory",
 "Memory: bytes, little-endian cells, and its size",
 "Memory is an array of byte slots; a 4-byte cell is read and written little-endian, one byte per slot. Every address check assumes 65,536 bytes, but the demos allocate much smaller arrays, and Bend array indexes wrap around.",
 r"""## Plain English

**Code (`read_cell`, `write_cell`, `boot`, """ + L("vm.bend", 85, 125) + r"""; bounds,
""" + L("vm.bend", 627, 633) + r""").**

* `read_cell` (""" + L("vm.bend", 91, 102) + r""") reads bytes a, a+1, a+2, a+3 and packs them low byte first.
  Each read hands the array back, because a Bend array has one owner. The two halves are packed with Bend's
  parallel call notation (the comment at """ + L("vm.bend", 85, 86) + r""").
* `write_cell` (""" + L("vm.bend", 115, 120) + r""") writes the four bytes, low byte first. The laws
  `little_endian_store` and `little_endian_load` (""" + L("LAWS.bend", 1000, 1021) + r""") restate both as
  explicit array operations.
* `address_ok` (""" + L("vm.bend", 629, 630) + r"""): a read or write of width w at address a is allowed when
  a ≤ 65,536 − w, so "no read or write may wrap around its end" (""" + L("vm.bend", 627) + r"""). A cell at
  FFFC is fine; one at FFFD faults (tests.org *bend.cell-boundary*, """ + L("tests.org", 132, 139) + r""").
* `code_ok` (""" + L("vm.bend", 632, 633) + r"""): code lives at 256 to 65,535. The first 128 bytes are the 32
  four-byte registers and the next 128 are system cells, as in every b4.

### How big is memory, really?

`boot` allocates `[0 : U32^16n]`, which by the Bend guide's rule (the number after `^` is a tree depth)
is 2¹⁶ = 65,536 slots, matching the checks. But the demos allocate less:

| Where | Depth | Slots |
|---|---|---|
| `boot` (console), """ + L("vm.bend", 123) + r""" | 16 | 65,536 |
| fleet test, """ + L("fleet-test.bend", 6) + r""" | 16 | 65,536 |
| square-root swarm, """ + L("swarm.bend", 24) + r""" | 9 | 512 |
| Mandelbrot, """ + L("mandelbrot.bend", 47, 48) + r""" | 10 | 1,024 |
| live shell, """ + L("live.bend", 32) + r""" | 12 | 4,096 |

The validation still allows any address below 65,536, and the Bend guide says array indexes wrap around. So in
a demo machine, address 1,024 + k would read the same slot as k. The demo programs stay inside their arrays, so
this does not affect their results; it does mean the demo machines are not full 64 KB b4 machines.
""",
 [q("In which order are a cell's bytes stored?",
    ["Little-endian: lowest byte at the lowest address", "Big-endian", "As one 32-bit slot"], 0,
    L("vm.bend", 115, 120) + " and law `little_endian_store`, " + L("LAWS.bend", 1000, 1011) + "."),
  q("Does `ri` at address FFFD succeed?",
    ["No: FFFD + 4 runs past 65,536, so it faults with invalid-address", "Yes, it wraps to address 0", "Yes, the missing byte reads as 0"], 0,
    "`address_ok`, " + L("vm.bend", 629, 630) + "; tested at " + L("tests.org", 132, 139) + "."),
  q("How many memory slots does each machine in the square-root swarm have?",
    ["512 (depth 9), though the bounds checks still assume 65,536", "65,536", "256"], 0,
    L("swarm.bend", 23, 28) + "."),
 ],
 caveats=["The 2^depth reading of `U32^16n` and the 'indexes wrap around' behaviour come from the Bend guide, not from this repository. The sizes are consistent with that reading (the swarm program at 256–258 fits in 512 slots, the Mandelbrot pixels at 768–1023 fit in 1,024).",
          "Whether an out-of-array access in a small demo machine wraps or does something else was not tested here; nothing was run."])

node("ControlFlow",
 "Jumps, hops, calls, returns and the nx loop",
 "Absolute jumps (`jm`, `cl`) read a 4-byte target and clamp anything below 256 up to 256. Hops (`hp`, `h0`, `nx`) add a signed byte offset to the hop's own address. `rt` with 0 on the control stack stops the machine, which is how a top-level call ends.",
 r"""## Plain English

**Helpers (""" + L("vm.bend", 140, 168) + r"""); cases jm…nx in [microcode](#/node/Microcode),
""" + L("vm.bend", 448, 480) + r""".**

* `jump(a)` (""" + L("vm.bend", 140, 141) + r"""): the new pointer is a − 1 (so that `advance` lands on a), and
  a target below 256 (compared signed) is clamped to 256.
* `hop` (""" + L("vm.bend", 143, 147) + r"""): read the signed byte after the opcode and jump to the hop's own
  address plus that offset.
* **jm** (""" + L("vm.bend", 448, 452) + r"""): jump to the 4-byte address after the opcode. A jump to 65,536 or
  more is allowed; the *next* fetch then faults (tests.org *bend.fetch-oob*, """ + L("tests.org", 147, 157) + r""").
* **hp** and **h0** (""" + L("vm.bend", 453, 464) + r"""): hop always, or pop and hop if the value was 0
  (`conditional_hop`, """ + L("vm.bend", 163, 168) + r"""). An untaken `h0` skips the offset byte.
* **cl** (""" + L("vm.bend", 465, 469) + r"""): push the address after the 4-byte target (ip + 5), then jump.
* **rt** (""" + L("vm.bend", 470, 474) + r"""): pop the control stack. If the value is 0, stay put and set mode
  ti (`return_control`, """ + L("vm.bend", 215, 220) + r"""); otherwise go there.
* **nx** (""" + L("vm.bend", 475, 480) + r"""; `next_counter`, `next_jump`, """ + L("vm.bend", 149, 161) + r"""):
  take the loop counter from the control stack; if it is positive, decrement it. If the result is non-zero, push
  it back and hop; if it is zero, drop it and continue.

### Targets are checked before anything moves

`check_target`, `check_hop` and `branch_check` (""" + L("vm.bend", 649, 682) + r""") compute where a call,
hop, taken `h0` or looping `nx` would go and fault with *invalid-address* if that is outside 256…65,535,
**before** the call pushes its return address or `h0` pops its flag. tests.org checks this "atomicity" for
`cl`, `hp`, `h0` and `nx` (""" + L("tests.org", 7, 30) + r""", """ + L("tests.org", 185, 219) + r""").
`jm` is the exception: it only checks that its 4-byte operand is readable (comment at
""" + L("vm.bend", 711, 712) + r""").
""",
 [q("A program executes `rt` while the control stack's top is 0. What happens?",
    ["The 0 is popped and the machine stops (mode ti), pointer just past the rt", "It jumps to address 0", "It faults with invalid-address"], 0,
    L("vm.bend", 470, 474) + "; law `top_return`, " + L("LAWS.bend", 293, 302) + "; tested at " + L("tests.org", 231, 238) + "."),
  q("Where does `hp 10` at address 300 go?",
    ["To 310: the offset is added to the hop's own address", "To 311", "To 10"], 0,
    "`hop` sets the pointer to 300 + 10 − 1 and `advance` adds 1, " + L("vm.bend", 140, 147) + "."),
  q("If `cl` targets an address outside code space, is the return address pushed?",
    ["No: the target is checked first and the machine faults with nothing changed", "Yes, then it faults", "It jumps anyway"], 0,
    "`check_target` in `operands`, " + L("vm.bend", 717, 718) + "; tested at " + L("tests.org", 7, 14) + "."),
 ])

node("RegisterOps",
 "Register ops: invoke, fetch, store and stream",
 "Bytes 01–7F are register ops: four blocks of 32, for invoking the address in a register, pushing its value, popping into it, and 'streaming' (push it, then add the popped amount to it). Each register is a 4-byte cell at the bottom of memory.",
 r"""## Plain English

**Code (`register_op`, `register_or_reserved`, """ + L("vm.bend", 181, 213) + r""").**
The byte's top bits pick the block (op ÷ 32) and the low five bits pick the register, whose cell is at address
(op mod 32) × 4.

| Bytes | Block | Effect |
|---|---|---|
| 01–1F | `^R` invoke | push the address of the next byte on the control stack and jump to the address held in R |
| 20–3F | `@R` fetch | push R's value |
| 40–5F | `!R` store | pop a value into R |
| 60–7F | `+R` stream | push R's value, then add the popped amount to R |

Byte 00 is the no-op, handled separately (""" + L("vm.bend", 279, 280) + r"""). Store and stream need one data
item (`need_data`, """ + L("vm.bend", 607, 608) + r"""); invoke checks that the register holds a legal code
address before it pushes anything (`register_target`, """ + L("vm.bend", 677, 682) + r""").

The [Mandelbrot program](#/node/MandelbrotProgram) uses ten registers as its variables, and the
[live shell's](#/node/LiveShell) default program is "fetch A, add 1, store A, jump back". The laws
`invoke_register`, `fetch_register`, `store_register` and `stream_register` restate each block
(""" + L("LAWS.bend", 713, 766) + r""").

This matches the decoding in the [Lean runOp](""" + LEAN + r"""runOp) and doc/opcodes.org.
""",
 [q("What does byte 0x45 do?",
    ["Pops a value into register E (block 2, register 5)", "Pushes register E", "Invokes register E"], 0,
    "0x45 = 69: 69 ÷ 32 = 2 (store), 69 mod 32 = 5 (E), " + L("vm.bend", 208, 213) + " and " + L("vm.bend", 193, 197) + "."),
  q("What does `+R` (stream) push?",
    ["R's old value; R then grows by the popped amount", "R's new value", "Nothing"], 0,
    L("vm.bend", 198, 206) + "; law `stream_register`, " + L("LAWS.bend", 754, 766) + "."),
  q("Where in memory is register C kept?",
    ["In the 4-byte cell at address 12 (3 × 4)", "In a separate register file", "At address 3"], 0,
    "The register's cell is at (op mod 32) × 4, " + L("vm.bend", 208, 211) + "."),
 ])

node("FloatOps",
 "Float ops fa fs fm fd fl fi (binary32 bit patterns in cells)",
 "Six extension ops treat a cell as the bit pattern of an IEEE single-precision float: add, subtract, multiply, divide, less-than and integer-to-float. They were added for the Mandelbrot demo and later copied into the Lean version.",
 r"""## Plain English

**Code (""" + L("vm.bend", 222, 275) + r"""; dispatch at """ + L("vm.bend", 481, 492) + r""").**
`f32_of` reinterprets a cell's 32 bits as Bend's `F32`, and `f_bits` turns a result back into bits.

| Byte | Op | Stack | Code |
|---|---|---|---|
| A0 | fa | x y → x+y | `fadd`, """ + L("vm.bend", 231, 232) + r""" |
| A1 | fs | x y → x−y | `fsub`, """ + L("vm.bend", 234, 235) + r""" |
| A2 | fm | x y → x·y | `fmul`, """ + L("vm.bend", 237, 238) + r""" |
| A3 | fd | x y → x/y | `fdiv`, """ + L("vm.bend", 240, 241) + r""" |
| A4 | fl | x y → (x<y) as −1/0 | `flt`, """ + L("vm.bend", 243, 244) + r""" |
| A5 | fi | n → float(n), n signed | `itof`, """ + L("vm.bend", 246, 257) + r""" |

`calc2` and `calc1` (""" + L("vm.bend", 263, 275) + r""") pop two (or one) cells, apply the function and push
the result. Float ops never fault apart from underflow: dividing by a float zero gives whatever `F32.div` gives.

doc/opcodes.org puts these in the "user-defined" range A0–BF and says the Bend implementation has the float ops
while Lean has all of them plus `rn` and `ct`. Here A6 (`rn`) and A7 (`ct`) are *unsupported* and fault
(`supported` accepts only bytes below A6 in this range, """ + L("vm.bend", 621, 625) + r""").
The [Lean f32op](""" + LEAN + r"""f32op) was added in a commit titled "floats, as in bend".

**Status: TESTED, not CHECKED.** tests.org has eight float tests (""" + L("tests.org", 279, 329) + r""") such as
1.0 + 2.0 = 3.0 and fi(−1) = −1.0. **No law in LAWS.bend mentions any float op.**
""",
 [q("How is a float stored on the stack?",
    ["As its IEEE binary32 bit pattern in an ordinary cell", "In a separate float stack", "As fixed point"], 0,
    "Comment at " + L("vm.bend", 222) + "."),
  q("Which of these are checked by a law in LAWS.bend?",
    ["None of the float ops", "All six", "Only fa and fm"], 0,
    "No law mentions opcodes 160–165; the float ops are covered only by tests.org, " + L("tests.org", 279, 329) + "."),
  q("What happens on byte A6 (`rn` in the Lean version)?",
    ["The machine faults with unsupported-opcode", "It pushes a random number", "Nothing"], 0,
    "`supported`, " + L("vm.bend", 621, 625) + "."),
 ])

node("Device",
 "The io device: one command, emit a character",
 "`io` pops a command. Only command 101 (the character 'e', emit) exists: it pops a character and appends it to the machine's output string. Any other command faults with unsupported-device, and the command is checked before anything is popped.",
 r"""## Plain English

**Code (`device`, """ + L("vm.bend", 170, 179) + r"""; case 253, """ + L("vm.bend", 493, 497) + r""").**

* `io` needs two data items (`need_data`, """ + L("vm.bend", 605, 606) + r""").
* `operands` (""" + L("vm.bend", 724, 725) + r""") checks that the top item is 101 *before* anything is popped,
  so a bad command leaves both items in place (tests.org *bend.bad-device*, """ + L("tests.org", 178, 183) + r""").
* Command 101 pops a character code and appends that character to `output`. The console prints the output
  after each line ([b4i](#/node/B4iShell)).

There is no input device. The [Lean version](""" + LEAN + r"""runOp) accepts both 'e' and 'o' and leaves
channel commands to its swarm layer; Bend has neither 'o' nor channels. The law `emit`
(""" + L("LAWS.bend", 701, 711) + r""") states the effect of command 101 through `execute`.
""",
 [q("What does `41 78 io` do?",
    ["Faults with unsupported-device and leaves 41 78 on the stack", "Prints 'A'", "Pops both and does nothing"], 0,
    "0x78 is not 101 (0x65), so `operands` faults first, " + L("vm.bend", 724, 725) + "; tested at " + L("tests.org", 178, 183) + "."),
  q("Can a Bend b4 machine read input through `io`?",
    ["No: the only device command is emit", "Yes, command 'r'", "Yes, command 'o'"], 0,
    L("vm.bend", 170, 179) + "."),
  q("Where does an emitted character go?",
    ["It is appended to the machine's output string, which the console prints after the line", "Straight to stdout", "Into memory at 'here'"], 0,
    L("vm.bend", 172, 176) + "; printed by `flush`, " + L("b4i.bend", 399, 405) + "."),
 ])

node("Microcode",
 "The opcode table: what each instruction does once it is allowed to run",
 "`microcode` is one big match on the opcode byte with one case per instruction: arithmetic and logic, stack shuffles, memory, literals, control flow, floats, io, halt and constants. It assumes validation has already passed, so its own pops never see an empty stack.",
 r"""## Plain English

**Code (`microcode`, """ + L("vm.bend", 277, 515) + r""").**
The opcode numbers and names match doc/opcodes.org and the [Lean runOp](""" + LEAN + r"""runOp). The names
come from `core_names` in [text.bend](#/node/TextHelpers) (""" + L("text.bend", 110, 111) + r""").

| Bytes | Ops | Lines |
|---|---|---|
| 00 | nop | """ + L("vm.bend", 279, 280) + r""" |
| 80–8C | ad sb ml dv md sh an or xr eq lt (pop b, pop a, push a∘b), nt, du | """ + L("vm.bend", 281, 367) + r""" |
| 8D–91 | sw ov zp, dc (data→control), cd (control→data) | """ + L("vm.bend", 368, 396) + r""" |
| 92–99 | rb ri wb wi (read/write byte or cell), lb li (inline literal), rs ls (signed byte) | """ + L("vm.bend", 397, 447) + r""" |
| 9A–9F | [jm hp h0 cl rt nx](#/node/ControlFlow) | """ + L("vm.bend", 448, 480) + r""" |
| A0–A5 | [fa fs fm fd fl fi](#/node/FloatOps) | """ + L("vm.bend", 481, 492) + r""" |
| FD | [io](#/node/Device) | """ + L("vm.bend", 493, 497) + r""" |
| FE, FF | db, hl: both set mode ti with no fault | """ + L("vm.bend", 498, 503) + r""" |
| C0 C1 F6 F7 F8 | constants 0, 1, 2, −1, 4 | """ + L("vm.bend", 504, 513) + r""" |
| 01–7F | [register ops](#/node/RegisterOps) | """ + L("vm.bend", 514, 515) + r""" |

Each case takes the VM apart, pops with `pop` (""" + L("vm.bend", 133, 138) + r"""), and rebuilds it. `pop`
returns 0 on an empty list, but the comment at """ + L("vm.bend", 131) + r""" notes this is an internal helper:
the public path ([validation](#/node/Validation)) has already checked the stack depth.

### Things worth noticing

* **`db` does the same as `hl`.** Both just stop the machine (mode ti). There is no debugger state.
* **Memory ops** (`rb`, `ri`, `wb`, `wi`) take the address on top and, for writes, the value under it.
  `wb` keeps only the low byte (tests.org *bend.byte-truncation*, """ + L("tests.org", 141, 145) + r""").
* **`microcode` vs `execute`.** For most ops the laws are stated through `execute`, so they also prove that
  validation passes. For divide, modulo, shift, memory, literals and control flow they are stated on
  `microcode` directly (""" + L("LAWS.bend", 488, 699) + r"""), and separate laws handle the checks.
""",
 [q("What does `ad` do with stack (… a b), b on top?",
    ["Pops b, then a, and pushes a + b", "Pushes b + a and keeps a and b", "Adds the top to memory"], 0,
    L("vm.bend", 281, 287) + "; law `add`, " + L("LAWS.bend", 15, 26) + "."),
  q("What do `db` and `hl` do in this implementation?",
    ["The same thing: set mode ti and clear the fault", "db enters a debugger, hl exits the program", "Nothing"], 0,
    L("vm.bend", 498, 503) + "; laws `debug` and `halt`, " + L("LAWS.bend", 271, 291) + "."),
  q("Why can `microcode` use a `pop` that returns 0 on an empty stack?",
    ["`execute` checks the stack depth first, so on the public path the stacks are never too short", "Because b4 defines empty pops as 0", "It can't; it is a bug"], 0,
    "Comment at " + L("vm.bend", 131) + "; depths from `need_data` and `need_control`, " + L("vm.bend", 545, 619) + "."),
 ])

node("Validation",
 "Validation: every fault is detected before any state changes",
 "Before running an instruction, `execute` decides whether it is safe: is the opcode known, do the stacks have enough items, are the operands valid? Only then does the microcode run. So a fault never leaves a half-done instruction behind, and the order of the checks is fixed.",
 r"""## Plain English

**Code (""" + L("vm.bend", 536, 760) + r""").**

1. **Known opcode?** `supported` (""" + L("vm.bend", 621, 625) + r"""): bytes 00–A5, C0, C1, F6–F8, FD–FF.
   Everything else is *unsupported-opcode* (BF in tests.org, """ + L("tests.org", 169, 176) + r""").
2. **Enough data items?** `need_data` (""" + L("vm.bend", 545, 608) + r""") lists, per opcode, how many items it
   pops; `enough` (""" + L("vm.bend", 536, 543) + r""") counts down the list.
3. **Enough control items?** `need_control` (""" + L("vm.bend", 610, 619) + r"""): 1 for `cd`, `rt` and `nx`.
4. `stack_check` (""" + L("vm.bend", 729, 738) + r""") turns those three answers into one fault, in that order.
5. **Operands** (`operands`, """ + L("vm.bend", 686, 727) + r"""), looked at without popping: divisor non-zero
   (`dv`, `md`); shift magnitude below 32 (`sh`); memory address in range (`rb ri wb wi rs`); inline argument
   inside memory (`lb li ls jm`); [jump targets](#/node/ControlFlow) inside code space (`hp h0 cl rt nx`, and
   register invokes); device command 101 (`io`).
6. `validated` and `commit` (""" + L("vm.bend", 740, 755) + r""") run the microcode only if both stages say
   `Clear`; otherwise `fault` (""" + L("vm.bend", 528, 530) + r""") sets mode na with the reason and the
   current pointer.

### Why it matters

This is what the comments and tests call **atomic** faults: tests.org's *bend.underflow.atomic*,
*bend.write-atomic*, *bend.h0-atomic* and *bend.next-atomic* (""" + L("tests.org", 40, 50) + r""",
""" + L("tests.org", 123, 130) + r""", """ + L("tests.org", 185, 210) + r""") check that the stacks and memory
are untouched. In the [laws](#/node/Laws), the seven `atomic_*` laws (""" + L("LAWS.bend", 783, 865) + r""")
say `commit` with a fault reason changes only the control record, and `accepted_instruction`
(""" + L("LAWS.bend", 768, 781) + r""") says that when both checks pass, `execute` is exactly `microcode`.
""",
 [q("A program runs `dv` with stack (123 0). What is the stack afterwards?",
    ["Still (123 0); the machine is in na with division-by-zero", "(123) with nothing pushed", "(0)"], 0,
    "`operands`, " + L("vm.bend", 688, 689) + "; tested at " + L("tests.org", 67, 73) + "."),
  q("`cd` with an empty control stack and an empty data stack: which fault?",
    ["control-underflow: cd needs nothing from the data stack", "data-underflow", "unsupported-opcode"], 0,
    "`need_data` has no entry for 145 so it needs 0; `need_control` gives 1, " + L("vm.bend", 610, 613) + "; tested at " + L("tests.org", 52, 58) + "."),
  q("What does `accepted_instruction` say?",
    ["If the stack check and the operand check both give Clear, execute equals microcode", "Every instruction is accepted", "Faults never happen"], 0,
    L("LAWS.bend", 768, 781) + "."),
 ])
