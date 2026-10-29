import os
exec(open(os.path.join(os.path.dirname(__file__), "_common.py")).read())

LEAN = "../b4-lean/#/node/"

node("FleetTree",
 "Fleets: a balanced binary tree of machines",
 "A fleet is a binary tree whose leaves are whole machines. Ticking a fleet ticks both halves with Bend's two-calls-on-one-line notation, which Bend may evaluate in parallel. Each machine owns its own memory, so there is nothing to share and nothing to lock.",
 r"""## Plain English

**Code (`Fleet`, `fleet_tick`, """ + L("vm.bend", 804, 815) + r""").** A `Fleet` is either `One{vm}` or
`Both{left, right}`. `fleet_tick` [ticks](#/node/VMStep) every leaf. The comment at """ + L("vm.bend", 804) + r"""
says "Balanced groups are schedulable in parallel without sharing VM memory."

### Why a tree, and why Bend

Bend's selling point is that independent work runs in parallel without threads or locks. The Bend guide says:
"Split the work in two, and Bend spreads the calls over every core it can find, then joins them back", and
"Parallelism requires balanced calls." Writing two calls on one line, as in `fleet_tick` at
""" + L("vm.bend", 814) + r""", is that split. A `!` after a function name (`fleet_run!` in the
[swarm](#/node/Fleet16384), `search!` in [Mandelbrot](#/node/Mandelbrot), `tick_node!` in the
[live shell](#/node/LiveShell)) marks a parallel call that the guide says runs on the GPU in native builds, and on
the CPU, still in parallel, when there is no GPU.

A machine's memory is a Bend `Array`, which has exactly one owner, so two machines cannot share memory even by
accident. There is no message passing between machines at all here: no channels, no `io` command for sending.
That is a real difference from the [Lean swarm](""" + LEAN + r"""Swarm), whose machines talk over timed channels.

The three demos each build their own copy of this tree (swarm.bend uses `Fleet`; mandelbrot.bend has an identical
`Swarm` type at """ + L("mandelbrot.bend", 56, 58) + r"""; live.bend has `Node` with an extra `Away` leaf,
""" + L("live.bend", 15, 18) + r""").

The law `fleet_isolation` (""" + L("LAWS.bend", 952, 956) + r""") restates the definition: ticking `Both` is
`Both` of the ticked halves.
""",
 [q("Do machines in a fleet exchange messages?",
    ["No: there are no channels in imp/bend; each machine runs alone", "Yes, through io", "Yes, through shared memory"], 0,
    L("vm.bend", 804, 815) + "; the only device command is emit, " + L("vm.bend", 170, 179) + "."),
  q("What makes the two halves of a fleet independent?",
    ["Each leaf is a separate VM value that owns its own memory array", "A lock", "They run one after the other"], 0,
    "Comment at " + L("vm.bend", 804) + "."),
  q("What does the `!` in `fleet_run!` or `search!` mark?",
    ["A parallel call, which the Bend guide says runs on the GPU in native builds and on CPU cores otherwise", "An unsafe call", "A call that may fail"], 0,
    L("swarm.bend", 69) + "; Bend guide."),
 ],
 caveats=["What Bend actually does with the parallel notation (cores, GPU lanes) is described from the Bend guide and the source comments. Nothing was run here, so no speed-up is claimed."])

node("FleetTest",
 "fleet-test.bend: four machines, two ticks",
 "A tiny check of the scheduler: four machines in modes vo, ru, ru and ti, two of them given a `c1` and one an `ad` with an empty stack, ticked twice. Only the running machines move, and the `ad` machine faults. No expected output is recorded and the test script does not run it.",
 r"""## Plain English

**File (""" + L("fleet-test.bend", 1, 30) + r""").** The comment calls it "A compiled parallel scheduler check,
independent of the console". `machine` (""" + L("fleet-test.bend", 5, 8) + r""") puts one opcode at 256 in a
fresh 64 KB memory. `main` (""" + L("fleet-test.bend", 26, 30) + r""") builds a fleet of four, calls
[`fleet_tick`](#/node/FleetTree) twice and prints each machine as mode:pointer:top-of-stack.

Working it through by hand (not run):

| Machine | After two ticks |
|---|---|
| vo, `c1` | untouched: 0:256:0 |
| ru, `c1` | pushes 1, then runs the 0 byte at 257 (nop): 1:258:1 |
| ru, `ad` | data underflow on the first tick, then idle: 2:256:0 |
| ti, `c1` | untouched: 3:256:0 |

**Status: STATED as a demo.** The Makefile's `clean` target mentions a `fleet-test` binary
(""" + L("Makefile", 15, 16) + r"""), but no target builds it and imp/test-bend doesn't run it, and the expected
line is not written down anywhere.
""",
 [q("Why does the ru machine with `ad` end at pointer 256?",
    ["Its first tick faults (data underflow) and a fault does not advance; afterwards tick ignores it", "It never ran", "It halted"], 0,
    L("vm.bend", 762, 790) + "."),
  q("Why does the vo machine not move?",
    ["`tick` steps only machines in mode ru", "Its opcode is invalid", "It ran out of fuel"], 0,
    L("vm.bend", 785, 790) + "."),
  q("Is this test run by `./test bend`?",
    ["No; nothing builds or runs it, and no expected output is recorded", "Yes, after tests.org", "Yes, by make check"], 0,
    L("Makefile", 1, 16) + "."),
 ])

node("Fleet16384",
 "Headline (demo): a square-root search on 16,384 machines",
 "Status: demo, STATED (no recorded output). A balanced tree of 2¹⁴ = 16,384 machines; machine k gets guess k, and all of them run du ml sb (key − guess²) under one parallel call. The machine left holding 0 had the square root of 10,000: by hand, machine 100.",
 r"""## Plain English

**File (""" + L("swarm.bend", 1, 70) + r""").**

* **The program** (`program`, """ + L("swarm.bend", 23, 28) + r"""): bytes 140, 130, 129 at addresses 256–258,
  which are `du ml sb`. In a 512-slot memory ([why small](#/node/Memory)).
* **One machine** (`machine`, """ + L("swarm.bend", 30, 32) + r"""): data stack = guess on top of the key 10,000
  (`key`, """ + L("swarm.bend", 10, 11) + r"""), pointer 256, mode ru.
* **The fleet** (`fork`, """ + L("swarm.bend", 34, 41) + r"""): a [fleet tree](#/node/FleetTree) of depth 14
  (`depth`, """ + L("swarm.bend", 13, 14) + r"""). At each level the left half keeps the guess and the right half
  adds 2^(level), so the leaves hold guesses 0 to 16,383 in order.
* **Run** (`main`, """ + L("swarm.bend", 68, 70) + r"""): `fleet_run!(3n, …)` gives every machine 3 steps of
  fuel (`fleet_run`, """ + L("swarm.bend", 43, 49) + r"""). The `!` marks the parallel call; the header comment
  says it "sends that search to the GPU (16384 lanes per wave)" (""" + L("swarm.bend", 6) + r""").
* **Report** (`hit`, `report`, """ + L("swarm.bend", 51, 66) + r"""): walk the tree again, recomputing each
  leaf's guess from its position, and print "machine k" for every machine whose top of stack is 0.

After `du ml sb` the stack holds 10,000 − guess² (the largest square, 16,383², is about 2.7 × 10⁸, so nothing
wraps). That is zero only for guess 100, so the expected output is one line, "machine 100". This is my
calculation; the repository records no output.

### What it shows, and what it doesn't

It shows the shape of b4-in-Bend parallelism: thousands of identical machines with different data, run as
independent leaves of a balanced tree. It is a brute-force search, not a clever one: every machine does the
same three steps. The machines don't communicate; compare the [Lean swarm](""" + LEAN + r"""Swarm.check), where
a √c check is a property of messages between machines.
""",
 [q("Which guess does each machine get?",
    ["Its position in the tree, 0 to 16,383", "A random number", "100 for all of them"], 0,
    "`fork`, " + L("swarm.bend", 34, 41) + "."),
  q("What does each machine compute?",
    ["key − guess², by du ml sb", "guess / key", "the full square root by Newton's method"], 0,
    L("swarm.bend", 1, 5) + " and " + L("swarm.bend", 23, 32) + "."),
  q("Is the answer 'machine 100' checked anywhere?",
    ["No: it follows from the code, but no law or test records it", "Yes, by a law", "Yes, in tests.org"], 0,
    "swarm.bend has no expected output; LAWS.bend does not import it."),
  q("How much fuel does each machine get, and why is that enough?",
    ["3 steps, one per instruction of du ml sb", "2¹⁸ steps", "Unlimited"], 0,
    L("swarm.bend", 68, 70) + "."),
 ],
 caveats=["Status: demo, STATED. The GPU claim ('16384 lanes per wave') is the source comment's; nothing was run here.",
          "The swarm's machines have 512-slot memories, not 65,536 (see Memory).",
          "The word 'swarm' here means many independent machines. Unlike the Lean swarm, there are no channels."],
 widgets=walk("The square-root search (swarm.bend, lines 1-70)", [
  {"text": "Write du ml sb at 256–258 of a 512-slot memory (lines 23–28)."},
  {"text": "Make a running machine with stack (key 10000, guess) (lines 30–32)."},
  {"text": "Grow a depth-14 tree: left keeps the guess, right adds 2^level (lines 34–41).", "link": "FleetTree"},
  {"text": "Run every leaf for 3 steps with the parallel call fleet_run! (lines 43–49, 68–69).", "link": "VMStep"},
  {"text": "Walk the tree, print each machine whose stack top is 0 (lines 51–66, 70)."},
 ]))

node("MandelbrotProgram",
 "The Mandelbrot tile program in b4 bytecode",
 "Each machine runs the same 150-byte b4 program on its own 16×16 tile: for each pixel, compute the point c from the tile coordinates with the float ops, iterate z ← z² + c at most 16 times, and store the iteration count as one byte at 768 + pixel.",
 r"""## Plain English

**Bytes (`code`, """ + L("mandelbrot.bend", 37, 38) + r"""); loading (`poke`, `machine`,
""" + L("mandelbrot.bend", 40, 54) + r""").** The program is written as a list of raw byte values and poked into
a 1,024-slot memory at 256. Each machine starts with its tile's tx on top of ty (`machine`,
""" + L("mandelbrot.bend", 50, 54) + r"""). There is no assembler here; my disassembly by hand:

1. **Set up** (bytes 256–267): store 768 in register H (output pointer), tx in I, ty in J, 0 in G (row) and F
   (column).
2. **Pixel → point** (268–313): cx = (16·tx + column) × 3/4096 − 2 and cy = (16·ty + row) × 2/1024 − 1, using
   `fi` to convert and `fm`, `fa` with float literals (0x3A400000 = 3/4096, 0xC0000000 = −2, 0x3B000000 = 2/1024,
   0xBF800000 = −1). cx goes in C, cy in D; z = (A, B) = (0, 0); count E = 0.
3. **Iterate** (314–363): stop if E = 16. Compute zr², zi², and if zr² + zi² ≥ 4 (`fl` against 4.0) stop.
   Otherwise zi ← 2·zr·zi + cy, zr ← zr² − zi² + cx, E ← E + 1, jump back.
4. **Store and loop** (364–405): write E as a byte at H and increment H; next column; after 16 columns, next row;
   after 16 rows, `hl`.

So the escape radius is 2, the iteration cap is **16**, and the view is x ∈ [−2, 1), y ∈ [−1, 1). The program
uses [registers](#/node/RegisterOps) for variables, [float ops](#/node/FloatOps) for arithmetic, and
[`h0`, `hp`, `jm`](#/node/ControlFlow) for loops.

The header comment says the custom ops "keep those bit patterns on the data stack, so a product is one
instruction" (""" + L("mandelbrot.bend", 5, 7) + r""") and that tiles inside the set run every iteration while
outside tiles halt early, so "the machines do not take the same number of steps" (""" + L("mandelbrot.bend", 8, 9) + r""").
""",
 [q("What is the iteration cap?",
    ["16", "256", "2¹⁸"], 0,
    "The loop test compares E with the literal 16 (bytes 314–319 of the program at " + L("mandelbrot.bend", 37, 38) + ")."),
  q("Where does a machine put its 256 results?",
    ["As bytes at addresses 768–1023 of its own memory", "On the data stack", "Straight into the PNG file"], 0,
    "`pixels` reads 16 rows of 16 from 768, " + L("mandelbrot.bend", 121, 123) + "."),
  q("How does a machine know which tile is its own?",
    ["tx and ty are on its data stack at start, taken from its index in the tree", "It reads a register set by the host", "All machines draw the whole picture"], 0,
    L("mandelbrot.bend", 50, 54) + "."),
 ],
 caveats=["The disassembly and the constants' meanings are my own reading of the byte list (decoded with a small script against text.bend's opcode table). They are not stated in the repository.",
          "The view's pixels are not square: 3/4096 wide but 2/1024 tall, so the picture is stretched sideways about 2.7 times. Decoding the committed mandelbrot.png shows exactly this wide shape."])

node("PngWriter",
 "Writing the PNG by hand: stored deflate blocks, CRC-32 and Adler-32",
 "mandelbrot.bend writes a valid PNG with no compression library: each 4,096-pixel scanline goes out as its own uncompressed ('stored') deflate block inside its own IDAT chunk, with the CRC-32 and the running Adler-32 checksum computed in Bend as the bytes stream past.",
 r"""## Plain English

**Code (""" + L("mandelbrot.bend", 141, 371) + r""").**

* **Fixed bytes**: the PNG signature and an IHDR chunk for 4,096 × 1,024, 8-bit greyscale, with its CRC written
  out (`header`, """ + L("mandelbrot.bend", 195, 196) + r"""); the IEND chunk (""" + L("mandelbrot.bend", 198, 199) + r""").
* **Checksums**: bitwise CRC-32 with the reflected polynomial 0xEDB88320 (`crc_bit` … `crc_list`,
  """ + L("mandelbrot.bend", 141, 166) + r"""); Adler-32 mod 65,521 (""" + L("mandelbrot.bend", 168, 189) + r""").
* **One scanline** = filter byte 0 + 4,096 grey bytes = 4,097 bytes (`scanline`, """ + L("mandelbrot.bend", 288, 289) + r""").
  It is wrapped in a stored deflate block: a not-final marker 0, then the length 4,097 and its complement
  (`block`, """ + L("mandelbrot.bend", 256, 257) + r"""). The first chunk also carries the 2-byte zlib header, so
  its length is 4,104 instead of 4,102 (`choose`, """ + L("mandelbrot.bend", 294, 299) + r""").
* **Each chunk** is length + "IDAT" + payload + CRC; `share` computes the CRC while copying the payload
  (""" + L("mandelbrot.bend", 259, 275) + r""").
* **The end**: an empty final stored block plus the big-endian Adler-32 in a last 9-byte IDAT, then IEND
  (`final_payload`, `close_file`, """ + L("mandelbrot.bend", 354, 363) + r""").
* **Colour** (`color`, """ + L("mandelbrot.bend", 77, 92) + r"""): count 16 (never escaped) is black; any other
  count n is grey 16·n.

### Getting the rows in order

The tree's index puts ty in the high bits. `write_rows` (""" + L("mandelbrot.bend", 342, 352) + r""") descends six
levels (the six bits of ty), sequentially, so each subtree it reaches holds the 256 tiles of one tile row in tx
order. `collect` gathers their pixel rows and `write_pys` (""" + L("mandelbrot.bend", 327, 332) + r""") 16 times
peels the first remaining row off every tile (`peel`, """ + L("mandelbrot.bend", 228, 247) + r""") to form one
full-width scanline.

The file size follows: 8 + 25 + 1,024 × (12 + 4,097 + 5) + 2 + 21 + 12 = 4,212,804 bytes, exactly the size git
records for mandelbrot.png. Decoding that file with a standard zlib (done for this site, in Python) succeeds,
gives 4,096 × 1,024 greyscale pixels, and shows only the grey levels 0, 16, 48, …, 240 that `color` can produce.
""",
 [q("Why is the PNG about 4.2 MB?",
    ["The deflate blocks are 'stored', i.e. uncompressed: one byte per pixel plus small headers", "It is 32-bit colour", "It includes the machines' memory"], 0,
    "`block`, " + L("mandelbrot.bend", 256, 257) + "."),
  q("Which part of the program runs in parallel?",
    ["The machines (`search!`); the file is written sequentially afterwards", "The CRC computation", "The file writes"], 0,
    "`main`, " + L("mandelbrot.bend", 365, 371) + "; `write_rows` binds IO in order, " + L("mandelbrot.bend", 350, 352) + "."),
  q("What colour is a pixel that never escaped?",
    ["Black (0)", "White (255)", "Grey 16·16 = 256"], 0,
    L("mandelbrot.bend", 77, 85) + "."),
 ],
 caveats=["The 'decoded with zlib' check was a Python read of the committed PNG for this site. It shows the file is well formed and consistent with the code. It does not show that this commit's Bend code produced it (the PNG was last changed in commit f3a8195, together with the float ops)."])

node("Mandelbrot",
 "Headline (demo): Mandelbrot on 16,384 machines, written to a PNG",
 "Status: demo; its output PNG is committed. 256 × 64 tiles of 16 × 16 pixels make 2¹⁴ machines, each running one b4 float program on its own tile, all under one parallel call. Bend then stitches the tiles into scanlines and writes a 4,096 × 1,024 greyscale PNG by hand.",
 r"""## Plain English

**File (""" + L("mandelbrot.bend", 1, 371) + r"""); header comment """ + L("mandelbrot.bend", 1, 9) + r""".**

1. **Grow** (`grow`, """ + L("mandelbrot.bend", 60, 67) + r"""): a balanced [tree](#/node/FleetTree) of depth 14
   (`depth`, """ + L("mandelbrot.bend", 13, 14) + r"""). Leaf k is a machine with the
   [tile program](#/node/MandelbrotProgram), tx = k mod 256 and ty = k ÷ 256.
2. **Search** (`search`, """ + L("mandelbrot.bend", 69, 75) + r"""): run every machine with 2¹⁸ = 262,144 steps of
   fuel. `main` calls it as `search!` (""" + L("mandelbrot.bend", 366) + r"""), the parallel call. A tile of
   256 pixels at up to 16 iterations of about 35 instructions needs roughly 145,000 steps, so the fuel is enough
   for a tile entirely inside the set.
3. **Collect** (`pixels`, `collect`, """ + L("mandelbrot.bend", 121, 139) + r"""): read each machine's 16 rows of 16
   bytes from address 768.
4. **Write** ([PNG writer](#/node/PngWriter)): stitch the tiles into 1,024 scanlines and write mandelbrot.png.

The result is committed as imp/bend/mandelbrot.png (4,096 × 1,024, about 4.2 MB). Decoded, it shows the
Mandelbrot set in black on grey bands, stretched sideways because the view is 3 × 2 units drawn into a 4 : 1
picture.

### Why it is a good b4 demo

It is a real workload for the VM, not for Bend: all the per-pixel arithmetic is b4 bytecode, interpreted by the
[step function](#/node/VMStep), with the [float ops](#/node/FloatOps) added for it. Tiles finish at different
times (the comment at """ + L("mandelbrot.bend", 8, 9) + r"""), so it also exercises `run` stopping early on `hl`.

### Compared with the Lean version

The float ops came to Lean afterwards ("floats, as in bend", see [f32op](""" + LEAN + r"""f32op)). There is no
Mandelbrot demo in the Lean implementation.
""",
 [q("How many machines are there, and how many pixels does each draw?",
    ["16,384 machines, 256 pixels (16 × 16) each", "4,096 machines, one row each", "One machine per pixel"], 0,
    L("mandelbrot.bend", 3, 4) + "."),
  q("Which arithmetic is done by b4 bytecode and which by Bend?",
    ["Pixel maths by b4 bytecode in each machine; collecting tiles, checksums and PNG bytes by Bend", "Everything by Bend", "Everything by b4"], 0,
    L("mandelbrot.bend", 37, 38) + " vs " + L("mandelbrot.bend", 141, 371) + "."),
  q("What evidence is there that the demo works?",
    ["The committed mandelbrot.png, which decodes to the expected picture; no test or law covers it", "A law in LAWS.bend", "A tanco test"], 0,
    "The PNG was added in commit 624506b and regenerated in f3a8195."),
 ],
 caveats=["Status: demo. The committed PNG is consistent with the code, but nothing records which commit's code produced it, and nothing was run for this site.",
          "The step estimate (about 145,000 for an all-black tile) is mine, from the disassembly."],
 widgets=walk("Mandelbrot from tree to file (mandelbrot.bend, lines 1-371)", [
  {"text": "Grow 2¹⁴ machines; leaf k gets the tile program, tx = k mod 256, ty = k ÷ 256 (lines 50–67).", "link": "MandelbrotProgram"},
  {"text": "`search!`: run every machine with 2¹⁸ fuel, in parallel (lines 69–75, 366).", "link": "FleetTree"},
  {"text": "Each machine leaves 16 × 16 iteration counts at 768–1023 (lines 121–123)."},
  {"text": "Write the PNG header (lines 368–369).", "link": "PngWriter"},
  {"text": "Descend six levels to one tile row; peel 16 scanlines across its 256 tiles; write each as a stored block in an IDAT chunk (lines 342–352, 327–332, 294–299)."},
  {"text": "Finish with the Adler-32 and IEND, close the file (lines 354–363, 370–371)."},
 ]))
