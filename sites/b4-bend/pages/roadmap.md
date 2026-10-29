# Roadmap: reading imp/bend in order

A reading order through `imp/bend` at the pinned commit, from the interpreter out to the demos. Every range links
to GitHub. Status labels: **CHECKED-BY-BEND** (a law with a proof that the project's `make check` runs; not re-run
here), **TESTED** (tanco tests run by the project's `./test bend`, or a committed demo output), **STATED**
(a comment or a demo with no recorded result), **CODE** (a program, with no claim attached).

## 1. The interpreter: vm.bend (816 lines, CODE)

Everything else imports it.

* [lines 1–26](src/imp/bend/vm.bend.html#L1-L26):
  modes, faults, the control record and the [VM type](#/node/MachineState);
* [lines 29–37](src/imp/bend/vm.bend.html#L29-L37):
  `pair` and `state`, continuations for threading the single-owner memory array;
* [lines 39–83](src/imp/bend/vm.bend.html#L39-L83):
  [signed arithmetic](#/node/Arithmetic) on U32 cells;
* [lines 85–125](src/imp/bend/vm.bend.html#L85-L125):
  [memory](#/node/Memory): little-endian cells, `boot`;
* [lines 127–168](src/imp/bend/vm.bend.html#L127-L168):
  push, pop, and the [jump and hop helpers](#/node/ControlFlow);
* [lines 170–179](src/imp/bend/vm.bend.html#L170-L179):
  the [io device](#/node/Device);
* [lines 181–220](src/imp/bend/vm.bend.html#L181-L220):
  [register ops](#/node/RegisterOps) and `return_control`;
* [lines 222–275](src/imp/bend/vm.bend.html#L222-L275):
  [float ops](#/node/FloatOps) (TESTED only);
* [lines 277–515](src/imp/bend/vm.bend.html#L277-L515):
  [`microcode`](#/node/Microcode), one case per opcode;
* [lines 517–534](src/imp/bend/vm.bend.html#L517-L534):
  mode codes, `fault`, `set_mode`;
* [lines 536–760](src/imp/bend/vm.bend.html#L536-L760):
  [validation](#/node/Validation): stack depths, supported opcodes, operand checks, `commit`, `execute`;
* [lines 762–802](src/imp/bend/vm.bend.html#L762-L802):
  [`advance`, `fetch`, `step`, `tick`, `run`](#/node/VMStep);
* [lines 804–815](src/imp/bend/vm.bend.html#L804-L815):
  the [fleet tree](#/node/FleetTree) and `fleet_tick`.

## 2. The contracts: LAWS.bend (1,121 lines) and PROOF.bend (328 lines), CHECKED-BY-BEND

* [LAWS.bend lines 1–1120](src/imp/bend/LAWS.bend.html#L1-L1120):
  [94 laws](#/node/Laws), grouped by kind on the Laws node;
* [PROOF.bend lines 1–328](src/imp/bend/PROOF.bend.html#L1-L328):
  [one proof per law](#/node/Proofs), 78 of them just `{==}`;
* [Makefile lines 9–10](src/imp/bend/Makefile.html#L9-L10):
  `make check` runs `bend PROOF.bend`.

## 3. The console: text.bend (182 lines) and b4i.bend (440 lines), TESTED

* [text.bend lines 1–182](src/imp/bend/text.bend.html#L1-L182):
  [hex and the opcode table](#/node/TextHelpers);
* [b4i.bend lines 1–439](src/imp/bend/b4i.bend.html#L1-L439):
  the [b4i console](#/node/B4iShell) that the tanco suites drive;
* [Makefile lines 6–7](src/imp/bend/Makefile.html#L6-L7):
  `bend b4i.bend -o b4i` builds it.

## 4. The extra tests: tests.org (329 lines), TESTED

* [tests.org lines 1–329](src/imp/bend/tests.org.html#L1-L329):
  [40 tests](#/node/TestsOrg) of strict faults, signed arithmetic and floats, run after the shared b4-tests.org.

## 5. Fleets: fleet-test.bend (30 lines) and swarm.bend (70 lines), STATED

* [fleet-test.bend lines 1–30](src/imp/bend/fleet-test.bend.html#L1-L30):
  [four machines, two ticks](#/node/FleetTest);
* [swarm.bend lines 1–70](src/imp/bend/swarm.bend.html#L1-L70):
  the [square-root search on 16,384 machines](#/node/Fleet16384).

## 6. Mandelbrot: mandelbrot.bend (371 lines) and mandelbrot.png, TESTED (committed output)

* [lines 1–139](src/imp/bend/mandelbrot.bend.html#L1-L139):
  [growing, running and collecting the tiles](#/node/Mandelbrot), with the
  [tile program](#/node/MandelbrotProgram) at lines 37–38;
* [lines 141–371](src/imp/bend/mandelbrot.bend.html#L141-L371):
  the [hand-written PNG encoder](#/node/PngWriter).

## 7. The live shell: live.bend (297 lines), poll_stdin.c (43), poll_stdin.js (17), STATED

* [live.bend lines 1–297](src/imp/bend/live.bend.html#L1-L297):
  the [live shell](#/node/LiveShell); [lines 15–151](src/imp/bend/live.bend.html#L15-L151)
  are the [fleet zipper](#/node/FleetZipper);
* [poll_stdin.c lines 1–43](src/imp/bend/poll_stdin.c.html#L1-L43)
  and [poll_stdin.js lines 1–17](src/imp/bend/poll_stdin.js.html#L1-L17):
  [non-blocking stdin](#/node/PollStdin).

## History

`git log -- imp/bend` at this commit: the interpreter, laws, proofs, console and tests arrived together on
2026-09-24 (a9c624a, "imp: gather implementations and language tests"); then the square-root swarm (c2cd7c1,
09-24), Mandelbrot (c27bb1c and 2df3319, 09-25; the PNG in 624506b), the float ops with Mandelbrot redone on
them (f3a8195, 09-26) and the live shell (56abc47, 09-26), merged on 09-27.
