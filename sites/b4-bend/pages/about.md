# About b4 in Bend

**b4** is a small Forth-like virtual machine by Michal Wallace. The repository
([tangentstorm/b4](https://github.com/tangentstorm/b4)) holds implementations in many languages (Pascal, J, lil,
JavaScript, C, Rust, Bend, Lean, GDScript) that all answer to one shared acceptance suite, `b4-tests.org`. Its
AGENTS.md says "Current focus is implementing the machine in bend."

This site covers only **`imp/bend/`**, the implementation in [Bend](https://github.com/bendlang/bend), a
functional language whose main idea is that independent work runs in parallel without threads or locks. The
dialect used here is the newer, dependently typed Bend: it has `law` declarations, equality proofs, affine
(single-owner) arrays, a termination check, and a `!` marker for parallel (GPU-capable) calls. The repository's
README still links the older HigherOrderCO/bend repository.

## What is in imp/bend

* **An interpreter** ([vm.bend](#/node/VMStep)): the whole b4 instruction set as pure functions on a machine
  value, with a strict fault model. Every failure (underflow, bad address, zero divisor, bad opcode, …) is a
  named fault detected before any state changes.
* **Contracts and proofs** ([LAWS.bend and PROOF.bend](#/node/Laws)): 94 laws about single instructions, the
  fault path, scheduling and memory layout, each with a proof that Bend checks, mostly by plain computation.
* **A console** ([b4i.bend](#/node/B4iShell), [text.bend](#/node/TextHelpers)) that the shared tanco test suites
  drive, plus Bend's own extra tests ([tests.org](#/node/TestsOrg)).
* **Three demos on 16,384 machines**: a [square-root search](#/node/Fleet16384), a
  [Mandelbrot picture written to PNG](#/node/Mandelbrot), and a [live shell](#/node/LiveShell) that ticks every
  machine each turn while you type into one of them.

## Where to start

The [Roadmap](#/roadmap) gives a file-by-file reading order with line ranges. For the ideas, read
[one step of the machine](#/node/VMStep), then [the laws](#/node/Laws), then the three demos.

## How it relates to the Lean implementation

The sister site [b4-lean](../b4-lean/) explains `imp/lean`. Both implement the same opcode table, but they make
different choices:

* **Errors.** Lean's interpreter has no error state (an empty pop gives 0). Bend's faults and leaves the machine
  untouched.
* **Stacks.** Lean keeps the stacks inside machine memory with fixed sizes; Bend uses unbounded lists.
* **Proofs.** Lean proves step lemmas with hypotheses about stack depth; Bend states laws for both the
  successful and the failing case, and proves them by computation.
* **Many machines.** Lean's swarm has message channels and a √c check about them; Bend's fleets are independent
  machines in a balanced tree, built for parallel evaluation, with no communication.
* **Floats.** The float ops were written for Bend's Mandelbrot demo first and then copied into Lean.

## What this site leaves out

The rest of the b4 repository (the b4a assembler and BIOS, the Forth layer, the other implementations, the
shared test documents themselves) is out of scope, except where `imp/bend` uses it. The repository has no
LICENSE file, so this site quotes no source: it describes the code in prose and links to exact lines.
