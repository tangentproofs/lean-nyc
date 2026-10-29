# Review: do the statements say what they claim?

Nothing below was checked by building Lean. It all comes from reading the source at the pinned commit.

## endToEnd_refinement (VsaIris/Interp/EndToEnd.lean): faithful to the README, with a boundary worth stating

The Lean statement matches the README's displayed theorem and its table row. It is complete: no `sorry` anywhere
in the project's own Lean, and no extra hypotheses beyond `Loaded`.

What a reader should keep in mind:

- **"Refinement" here is a precise, two-part claim.** Part 1 is a full *iff* between normal source results and
  clean machine exits (code 0), including the output string. Part 2 is one-way: machine divergence implies no
  normal result. It does **not** say that a diverging source program makes the machine diverge. The machine
  might instead exit 70 or 1. The failure side is in
  [endToEnd_trichotomy](#/node/Vsa.Sim.EndToEnd.endToEnd_trichotomy).
- **The starting point is `interp_run`, not power-on.** The hypothesis places the machine at the first
  instruction of `interp_run` with the AST already built in memory. The C parser and boot code are outside the
  statement. The name "end to end" means *from the source semantics to the ISA*. It does not mean *from source
  text to output*. The README says this plainly in "What is assumed".
- **`Loaded` carries two program assumptions:** heap `capacity` and `stack_admissible`. They are inside the
  layout predicate, not visible in the theorem's signature.
  [endToEnd_checked](#/node/Vsa.Sim.EndToEnd.endToEnd_checked) removes them in favour of runnable checks.
- **Is the hypothesis satisfiable?** Yes. The boot witnesses prove `Loaded` (on the zero-filled state) for
  ten concrete traced states (Vsa/Sim/Boot/Gen/), so the theorem is not vacuous.

## The specification `BigStep`: the real trust question

A refinement theorem is only as meaningful as its specification. Here `BigStep` (Vsa/While/Semantics.lean) is a
detailed semantics written **to match the C interpreter**. It includes signed 64-bit wrapping arithmetic,
truncating division, string ordering, a call-depth cap of 1000 and at most 32 arguments. It also includes
display formats copied from the C code. One example: when a named function is concatenated into a string, its
rendering `<fn name>` is cut to 63 characters (`fnCatRender`, Vsa/While/Semantics.lean line 138). That
matches the C buffer (`char buf[64]` with `snprintf`,
c/src/interp.c lines 86–93). Natives display as `<native fn print>` when printed but as `<native fn>` inside
concatenation (lines 131–141), again exactly as in the C.

None of this is wrong. It is the honest specification of *this* interpreter. But the theorem cannot tell an
intended behaviour from an accidental one: if the C did something surprising and the semantics copied it, the
proof makes it "correct". A human reading of
Vsa/While/Semantics.lean (about 420 lines) is the remaining check on what "correct" means. The type-safety
and exclusivity theorems the project also proves (not covered here) are some evidence that the semantics is
sensible.

## endToEnd_trichotomy: faithful

The six clauses match the README row ("every nonzero exit is 70 … or 1 …; the binary exits nonzero or diverges
exactly when the program errs or diverges"). Note again that error and divergence are matched only as a pair.

## while_halts and siblings: faithful, with the README's stated gap

These state that a specific traced configuration halts with a specific output. `Loaded` at that state is
kernel-checked. The link from "the ELF file, loaded and booted" to "that configuration" is **not**. The README
says so. Calling these "the ELF halts" (as the README's table does: "the ELF, run from its traced `interp_run`
entry state") is accurate as long as "from its traced entry state" is kept.

## endToEnd_checked: faithful

The checked version keeps everything in `Loaded` except the two program assumptions. It requires
`interpCostBound p = some B`, so programs whose allocation the analysis cannot bound are not covered.

## Surprises

- `NewlibHoles` sounds like an assumption but is proved (`newlibHoles_proved`). The main theorem has no hidden
  hypotheses of this kind.
- The repository says it has "no comments", but several key files have module docstrings (for example
  Vsa/Lang/Basic.lean lines 3–17 and VsaIris/Lang/Route.lean lines 4–14).
