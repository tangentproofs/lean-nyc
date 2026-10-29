# Review: is the Bend code faithful, and what is surprising?

This page checks each headline against what its comments, the b4 documents (doc/opcodes.org, b4-tests.org) and
the [Lean implementation](../b4-lean/) say. Labels: **CHECKED-BY-BEND**, **TESTED**, **STATED**, **CODE**, as on
the [Roadmap](#/roadmap). Nothing was built or run for this site.

## Status table

| Headline | What is claimed | Status |
|---|---|---|
| [One step](#/node/VMStep) | the b4 instruction set with strict, atomic faults | CODE; single steps CHECKED-BY-BEND by the laws; TESTED by 55 shared + 40 Bend tanco tests |
| [The laws](#/node/Laws) | 94 equations about single instructions, faults, scheduling, memory layout | CHECKED-BY-BEND (wired into `make check`, not re-run here) |
| [Square-root search](#/node/Fleet16384) | 16,384 machines find √10000 | STATED: demo, no recorded output |
| [Mandelbrot](#/node/Mandelbrot) | 16,384 machines draw a 4,096 × 1,024 PNG | TESTED only in the sense that the PNG is committed and decodes correctly |
| [Live shell](#/node/LiveShell) | a shell over 16,384 ticking machines | STATED: demo, no test or transcript |

## Faithful to the b4 spec?

**Opcode table: yes.** The numbering and names in `microcode` and text.bend's `core_names` match
doc/opcodes.org and the Lean `runOp`. The register blocks decode the same way. `nx` follows b4-tests.org
("decrement, hop if the result is not zero, drop it when it reaches zero"), as Lean does; doc/opcodes.org's
one-line description reads slightly differently, but the tests are the shared contract.

**Strict faults: a Bend-specific choice, made explicit.** b4-tests.org mostly describes successful behaviour.
The Bend version adds a full fault model (eight reasons, checked in a fixed order, with nothing changed on
failure), and tests.org's header says so: "Out-of-range hops and calls fault and leave ip unchanged." This is
stricter than Lean, which silently does nothing on errors. Neither is wrong by the shared suite, but programs
that rely on Lean's "empty pop gives 0" behaviour would fault in Bend.

**Deliberate deviations and gaps**

* `db` does exactly what `hl` does (stop the machine). doc/opcodes.org says `db` triggers the debugger; Lean sets
  a debug flag.
* `io` supports only command 101 ('e', emit). Lean also accepts 'o', and its swarm adds channel commands.
* `rn` and `ct` (A6, A7) are not implemented and fault as unsupported opcodes. doc/opcodes.org says as much
  ("the Bend implementation the float ops").
* The stacks are unbounded lists: no overflow fault, unlike machines with fixed-size stacks.
* `jm` to a target below 256 is clamped to 256 (`jump`); `jm` to a target past the end of memory is allowed and the
  next fetch faults (tests.org *bend.fetch-oob*). The comment at vm.bend line 711 says b4-tests.org's `op.jm`
  "takes any readable target".

## Faithful to the laws' own names?

Mostly yes, with two names that promise a little more than they state:

* **`fleet_isolation`** only says that ticking `Both{left, right}` is `Both` of the ticked halves, which is the
  definition of `fleet_tick`. The isolation itself (no machine can touch another's memory) is true because of how
  the values are built, but it is not what the law states.
* **`accepted_instruction`** is a real lemma (it needs both checks to pass), but it is about `execute` versus
  `microcode`, not about a whole accepted program.

Many laws are deliberate restatements of the code. As contracts, that is their point: they freeze the current
behaviour, including validation order and atomicity, so any edit that changes it breaks `make check`.

## What is surprising

1. **Proof by computation is enough.** 78 of the 94 proofs are the single token `{==}`. The laws quantify over
   *all* memories, stacks, pointers and control records, but because they fix the opcode and the top of the
   stack, Bend's checker can evaluate `execute` symbolically down to the same term on both sides.
2. **Demo machines are smaller than the machine the checks describe.** Every bounds check assumes 65,536 bytes,
   but the swarm, Mandelbrot and live-shell machines allocate 512, 1,024 and 4,096 slots, and Bend array indexes
   wrap around. The demo programs stay in range, so their results are unaffected, but a program typed into a
   live-shell machine that writes to, say, address 5,000 would land at 904 instead of faulting.
3. **No channels.** The word "swarm" here means independent copies, not communicating machines. Parallelism
   comes from Bend evaluating a balanced tree of independent work, not from the machines cooperating.
4. **A hand-written PNG encoder.** mandelbrot.bend writes CRC-32, Adler-32, zlib and PNG framing itself, with
   uncompressed stored blocks, and the committed 4.2 MB file decodes cleanly.
5. **The live shell's `/g` is not the console's `/g`.** In b4i, `/g` runs up to a million steps at once; in the
   live shell it just sets the machine running, and it then advances one instruction per turn with the rest.
6. **The Mandelbrot picture is stretched.** The view is 3 × 2 units drawn into a 4 : 1 image, so the set appears
   about 2.7 times wider than it is. Probably harmless for a demo, but it is not a true-aspect rendering.

## What is not checked anywhere

No law or test covers: any multi-instruction program; the float ops (tests only); the fleet demos' results;
the PNG writer; the live shell; b4i's label and assembly handling beyond what the shared suite exercises; or any
agreement with the Lean implementation beyond both passing the same shared tanco suite.
