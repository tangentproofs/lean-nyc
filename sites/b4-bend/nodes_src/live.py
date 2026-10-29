import os
exec(open(os.path.join(os.path.dirname(__file__), "_common.py")).read())

node("LiveShell",
 "Headline (demo): a live shell over 16,384 ticking machines",
 "Status: demo, STATED. 16,384 machines, each running a counter loop, are all ticked once per turn with a parallel call. Between turns stdin is polled without blocking; a typed line goes through the b4i console to the one attached machine, and `/m tx ty` attaches another.",
 r"""## Plain English

**File (""" + L("live.bend", 1, 297) + r"""); header comment """ + L("live.bend", 1, 5) + r""".**

* **Boot** (`main`, """ + L("live.bend", 290, 297) + r"""): `grow` (""" + L("live.bend", 160, 167) + r""") builds a
  depth-14 tree of `fresh` machines (""" + L("live.bend", 31, 44) + r"""). Each has a 4,096-slot memory and the
  program `@A c1 ad !A jm 256` ("each lap adds one to register A"), and starts in mode ru.
* **The desk** (`Desk`, """ + L("live.bend", 28, 29) + r"""): the fleet, the attached machine's index
  (`focus` = 256·ty + tx), the console's labels and assembling flag, pending output, and a quit flag.
* **One turn** (`loop`, """ + L("live.bend", 277, 288) + r"""): `tick_node!` ticks every machine once, in
  parallel (""" + L("live.bend", 143, 151) + r"""); then read whatever bytes are waiting with
  [`Poll.stdin`](#/node/PollStdin) (""" + L("live.bend", 11, 13) + r"""), print pending output, and feed the
  bytes to `pump` (""" + L("live.bend", 257, 267) + r"""), which collects characters until a newline and stops on
  the end-of-stream byte 4.
* **A line** (`route`, """ + L("live.bend", 237, 249) + r"""):
  * `/q` quits;
  * `/g` sets the attached machine running, so the turns run it (""" + L("live.bend", 225, 231) + r""");
  * `/C` replaces it with a blank stopped machine (""" + L("live.bend", 233, 235) + r""");
  * `/m tx ty` (hex) attaches to tile tx 00–ff, ty 00–3f (""" + L("live.bend", 182, 206) + r""");
  * anything else is handed to the [b4i console](#/node/B4iShell) for the attached machine
    (`delegate`, `edited`, `from_shell`, """ + L("live.bend", 208, 218) + r"""). That is how `/t`, `/s`, `?d`,
    assembly and so on work.
* **Taking one machine out of the tree and putting it back** is the [fleet zipper](#/node/FleetZipper).

The tile coordinates (256 × 64) are the same as the [Mandelbrot](#/node/Mandelbrot) grid; the shell does not
draw anything, but the addressing is shared.

### Things worth noticing

* `/g` here differs from the console's `/g`. In b4i, `/g` runs up to 1,000,000 steps at once
  (`resume`, """ + L("b4i.bend", 29, 31) + r"""). In the live shell, `/g` only sets mode ru and the machine then
  advances one instruction per turn, alongside all the others.
* Labels and the assembling flag belong to the desk, not to a machine, so a label defined while attached to one
  machine is still defined after `/m` moves to another.
* The turn rate is not limited: the loop does not block on input, so it ticks the fleet as fast as Bend can
  run a turn.
* The loop is marked `@unsafe` (""" + L("live.bend", 277) + r""") because it only ends on `/q` or end of input,
  so Bend's termination check cannot accept it.
""",
 [q("How often does each of the 16,384 machines step?",
    ["Once per turn of the loop, all of them, whether or not you typed anything", "Only when attached", "1,000,000 times per line"], 0,
    "`loop` calls `tick_node!` every turn, " + L("live.bend", 284) + "."),
  q("What does `/m 10 3` do?",
    ["Attaches to the machine with tx = 0x10, ty = 3, index 3·256 + 16", "Moves 16 bytes", "Starts machine 103"], 0,
    L("live.bend", 185, 190) + "."),
  q("Where does `?d` typed in the live shell go?",
    ["To b4i's `line` for the attached machine, which prints its data stack", "To every machine", "It is ignored"], 0,
    "`route` falls through to `delegate`, " + L("live.bend", 248, 249) + "."),
  q("What does the attached machine do while you type?",
    ["It is in the tree and keeps ticking with the rest; it is taken out only while a line is applied", "It is paused", "It is removed until /m"], 0,
    "`delegate` walks it out and `from_shell` puts it back in the same call, " + L("live.bend", 208, 218) + "."),
 ],
 caveats=["Status: demo, STATED. No test runs live.bend and no transcript is recorded. The GPU claim ('The bang runs that tick on the GPU when a device is present', lines 3–4) is the source comment's.",
          "The startup message mentions /m, /g, /t and /q but not /C, which `route` also handles."],
 widgets=walk("One turn of the live shell (live.bend, lines 257-297)", [
  {"text": "Boot: a depth-14 tree of counter machines, all running (lines 290–297, 160–167, 31–44)."},
  {"text": "Turn: `tick_node!` ticks every machine once, in parallel (lines 284, 143–151).", "link": "FleetTree"},
  {"text": "Poll stdin without blocking, print pending output (lines 285–287).", "link": "PollStdin"},
  {"text": "`pump`: collect characters; on newline apply the line; byte 4 means quit (lines 257–267)."},
  {"text": "`route`: /q, /g, /C, /m handled here; anything else goes to b4i on the attached machine (lines 237–249).", "link": "B4iShell"},
  {"text": "The attached machine is walked out, edited, and put back in the tree (lines 208–218).", "link": "FleetZipper"},
 ]))

node("FleetZipper",
 "Taking one machine out of a 16,384-machine tree",
 "To edit the attached machine, live.bend follows the 14 bits of its index from the root (left for 0, right for 1), takes the machine out and leaves an `Away` hole, then walks the same path to put the edited machine back. With Bend's single-owner values this is how you 'update one leaf'.",
 r"""## Plain English

**Code (""" + L("live.bend", 15, 151) + r""").**

* `Node` (""" + L("live.bend", 15, 18) + r""") is the [fleet tree](#/node/FleetTree) with one extra leaf,
  `Away{}`, a hole where a machine has been taken out. Ticking skips holes (""" + L("live.bend", 147, 148) + r""").
* `turns` (""" + L("live.bend", 81, 86) + r""") turns an index into a path, highest bit first: bit set = go right.
  That matches how `grow` numbered the leaves.
* `walk` (""" + L("live.bend", 101, 114) + r""") follows the path and returns the machine and the tree with a hole.
* `put` (""" + L("live.bend", 127, 141) + r""") follows the path and puts a machine in the hole (or replaces a leaf).
* If the path and the tree's shape ever disagree, `drop_walk` and `drop_put` (""" + L("live.bend", 96, 99) + r""",
  """ + L("live.bend", 122, 125) + r""") discard what is there and use a fresh machine. With a full depth-14 tree and a
  14-bit index this should not happen.
* `sink`, `discard` and `discard_path` (""" + L("live.bend", 50, 69) + r""") exist only to consume values that are
  being thrown away. Bend's values are affine, so the code takes them apart explicitly instead of just dropping
  them.
""",
 [q("Which way does `turns` go for bit 13 of the index?",
    ["First step from the root: right if the bit is set", "Last step", "It ignores it"], 0,
    "`turns(n, index)` uses bit n − 1 first, " + L("live.bend", 81, 86) + "."),
  q("What is `Away{}`?",
    ["The hole left in the tree while one machine is taken out for editing", "An offline machine", "A faulted machine"], 0,
    L("live.bend", 15, 18) + " and " + L("live.bend", 103, 104) + "."),
  q("What happens to the tree while the attached machine is out?",
    ["It has an Away hole at that leaf, which ticking skips, until `put` fills it again", "All machines pause", "The tree is rebuilt"], 0,
    L("live.bend", 143, 151) + " and " + L("live.bend", 127, 141) + "."),
  q("Why is the path read from the highest bit of the index down?",
    ["Because `grow` gives the right half the larger indexes at each level, starting at the root", "For speed", "It is arbitrary"], 0,
    L("live.bend", 160, 167) + "."),
 ],
 caveats=["The explanation of `sink` and `discard` as affine bookkeeping is my reading; the source has no comment on it."])

node("PollStdin",
 "Polling stdin without blocking (C and JavaScript)",
 "The live shell needs to read input without stopping the fleet. `Poll.stdin` is a Bend IO function with two host implementations: C uses poll() with a zero timeout, JavaScript sets O_NONBLOCK and reads. Both return an empty string for 'nothing yet' and the single byte 4 for 'closed'.",
 r"""## Plain English

**Declaration (""" + L("live.bend", 11, 13) + r"""): `Poll.stdin(max)` imports poll_stdin.c and poll_stdin.js.**

* **C** (""" + L("poll_stdin.c", 1, 43) + r"""): clamps `max` to 1…4,096 (default 256), calls `poll` on file
  descriptor 0 with timeout 0, and reads up to `max` bytes if any are ready. An error, a hang-up or a read of 0
  bytes returns the end-of-transmission byte 4. A constructor registers the function with Bend's IO table
  (""" + L("poll_stdin.c", 41, 43) + r""").
* **JavaScript** (""" + L("poll_stdin.js", 1, 17) + r"""): sets O_NONBLOCK (0x800) on stdin with `fcntl` and reads;
  a read of 0 bytes returns byte 4 and an error (no data) returns the empty string.

[`pump`](#/node/LiveShell) treats a chunk that is exactly byte 4 as quit (""" + L("live.bend", 261, 263) + r""").
""",
 [q("What does Poll.stdin return when no key has been pressed?",
    ["The empty string", "Byte 4", "It waits"], 0,
    L("poll_stdin.c", 18, 28) + "."),
  q("Why not use the ordinary blocking read that b4i uses?",
    ["A blocking read would stop the loop, so the fleet would stop ticking while waiting for input", "Bend has no read", "For speed only"], 0,
    "Compare b4i's `File.read(file, 1)`, " + L("b4i.bend", 416) + ", with live's loop, " + L("live.bend", 284, 288) + "."),
  q("What does the byte 4 mean to the live shell?",
    ["Input has closed: quit", "Ctrl-D, ignored", "Attach to machine 4"], 0,
    L("live.bend", 261, 263) + "."),
 ])

node("B4iShell",
 "b4i.bend: the interactive console the tests drive",
 "b4i is the line-based console that the shared tanco suites talk to: hex numbers push, opcode names execute (only when the machine is stopped), `:` switches to assembly, `:name` defines a label, `?d ?c ?s ?i` query, and `/s /g /t /o /C /q` step, go, stop, take offline, reset and quit.",
 r"""## Plain English

**File (""" + L("b4i.bend", 1, 439) + r"""), "Minimal b4i console for the shared VM acceptance tests".**
The syntax follows the repository's doc/b4i.org; the [text helpers](#/node/TextHelpers) parse it.

* **State** (`Shell`, """ + L("b4i.bend", 10, 11) + r"""): one machine, a label map, the assembling flag, quit,
  and pending report text. `boot` starts the [VM](#/node/MachineState) stopped at 256.
* **Tokens** (`token`, """ + L("b4i.bend", 344, 384) + r"""), one space-separated word at a time:
  * `/q /C /s /t /o /g`: quit, reboot, single step, stop (ti), offline (vo), go;
  * `?d ?c ?s ?i ?R ?addr`: show the data stack, control stack, state, pointer, a register, or 16 bytes of memory
    (`query`, """ + L("b4i.bend", 126, 147) + r""");
  * `:` alone: assembly mode for the rest of the line; `:name` defines a label (or a register, for one capital
    letter) at the current "here"; `:hex` moves "here" (""" + L("b4i.bend", 149, 182) + r""");
  * `'c`: a character literal;
  * `@R !R +R ^R` and `@label !label` and a backquote prefix: register and label access (""" + L("b4i.bend", 205, 339) + r""");
  * otherwise an opcode name, a hex number or a label (""" + L("b4i.bend", 259, 270) + r""").
* **Calculator vs assembly**: in assembly mode numbers and opcodes are written as bytes at "here" (register `_`,
  byte 124; `emit`, """ + L("b4i.bend", 16, 23) + r"""). In calculator mode numbers are pushed and an opcode is
  executed at once, **but only if the machine is stopped** (mode ti) (`calculator`, """ + L("b4i.bend", 191, 196) + r""").
  An offline or faulted machine ignores typed opcodes until `/t` (tests.org *bend.offline-calculator*,
  """ + L("tests.org", 271, 277) + r""").
* **Running code**: `/g` runs up to 1,000,000 steps (`resume`, """ + L("b4i.bend", 29, 31) + r"""). Calling a
  label or `^R` from the calculator pushes a 0 return address as a sentinel, runs, and when the machine stops
  with the control stack back at its old depth, restores the pointer (`invoke_valid`, `invoke_finish`,
  """ + L("b4i.bend", 33, 44) + r"""). The 0 is what makes [`rt` stop the machine](#/node/ControlFlow).
* **Input**: a blocking read of one byte at a time from /dev/stdin, a line at a time; output is flushed after each
  line (`loop`, `flush`, """ + L("b4i.bend", 399, 436) + r"""). The loop is the only `@unsafe` code
  (""" + L("b4i.bend", 407, 410) + r""").
""",
 [q("You type `1 2 ad` while the machine is running (mode ru). What happens to `ad`?",
    ["Nothing: calculator ops run only when the machine is stopped (ti)", "It adds", "It faults"], 0,
    "`calculator`, " + L("b4i.bend", 191, 196) + "."),
  q("What does `:A` do?",
    ["Stores the current 'here' address in register A and switches to assembly", "Jumps to A", "Prints A"], 0,
    "A single capital letter is a register, " + L("b4i.bend", 149, 158) + " and " + L("b4i.bend", 174, 182) + "."),
  q("Why does invoking a label from the console push 0 on the control stack?",
    ["So the routine's final `rt` pops 0 and stops the machine, returning control to the console", "To count calls", "It is a bug"], 0,
    L("b4i.bend", 40, 44) + "; `rt` with 0, " + L("vm.bend", 470, 474) + "."),
 ],
 caveats=["Status: CODE, TESTED through the shared b4-tests.org (55 tests) and tests.org (40), by the project's runner. Nothing was run for this site."])

node("TextHelpers",
 "text.bend: hex, the opcode table, and line clean-up",
 "Small helpers for the console: print cells as signed hex, read hex numbers with an optional minus sign, recognise register letters, strip comments, and map two-letter opcode names to bytes and back.",
 r"""## Plain English

**File (""" + L("text.bend", 1, 182) + r"""), "Hexadecimal cells and the canonical private opcode table".**

* `hex_fixed`, `hex`, `cell` (""" + L("text.bend", 5, 35) + r"""): upper-case hex; a cell with its top bit set
  prints as minus its magnitude, so −1 shows as `-1` and the float −1.0 (0xBF800000) as `-40800000`
  (tests.org """ + L("tests.org", 279, 281) + r""").
* `stack` (""" + L("text.bend", 37, 47) + r"""): prints a stack bottom first, as `ds: [1 2]`.
* `read_hex` (""" + L("text.bend", 49, 85) + r"""): hex digits in either case, optional leading `-`.
* `register` (""" + L("text.bend", 87, 92) + r"""): a single character from `@` to `_` names register 0–31.
* `normalize` (""" + L("text.bend", 94, 101) + r"""): everything after `#` is a comment; whitespace becomes spaces.
* `core_names`, `opcode` (""" + L("text.bend", 103, 134) + r"""): the 38 names `ad sb … fi` are bytes 80–A5 in
  order; `..`, `c0`, `c1`, `c2`, `n1`, `c4`, `io`, `db`, `hl` are listed separately.
* `byte` (""" + L("text.bend", 136, 182) + r"""): the reverse, for memory dumps (`?100`).
""",
 [q("How is the cell FFFFFFFF printed?",
    ["-1", "FFFFFFFF", "4294967295"], 0,
    "`cell` prints negative values as '-' + hex of the magnitude, " + L("text.bend", 27, 35) + "."),
  q("Which byte is `fi`?",
    ["A5: the 38th name in core_names, counting from 80", "FF", "C0"], 0,
    L("text.bend", 110, 111) + " and " + L("text.bend", 103, 108) + "."),
  q("What does `#` do in a console line?",
    ["Starts a comment: the rest of the line is dropped", "Pushes a number", "Defines a label"], 0,
    "`normalize`, " + L("text.bend", 94, 101) + "."),
 ])
