# Trust: what was and wasn't checked

## Not built

**The Lean was not built for this site.** No `lake`, `lean` or `elan` was run. When this site says something "is
proved", it only means the source file contains what looks like a complete proof and that no `sorry` appears in the
project files it depends on, not that Lean's kernel accepted it.

The project's own metadata (formalization.yaml) states that "a full default `lake build` completed successfully (3177
jobs)", that the solution has no `sorry` or `admit`, and that the only axioms used are `propext`, `Quot.sound` and
`Classical.choice`. Those are the author's claims, not verified here.

## Gaps, axioms and escape hatches

A text search of all 101 `.lean` files at the pinned commit for `sorry`, `admit`, `axiom`, `native_decide`,
`implemented_by`, `extern`, `opaque`, `unsafe` and `maxHeartbeats` finds:

| What | Count | Where |
|---|---|---|
| `sorry` | 3 | [Schiffer/Challenge.lean line 68](https://github.com/jaumededios/Schiffer/blob/2938e277969c329caf154e48a3d8823f3635c7f1/Schiffer/Challenge.lean#L68) and [Schiffer/Challenge.lean line 110](https://github.com/jaumededios/Schiffer/blob/2938e277969c329caf154e48a3d8823f3635c7f1/Schiffer/Challenge.lean#L110); [Schiffer/FormalConjecturesChallenge.lean line 69](https://github.com/jaumededios/Schiffer/blob/2938e277969c329caf154e48a3d8823f3635c7f1/Schiffer/FormalConjecturesChallenge.lean#L69) |
| `admit` | 0 | |
| `axiom` (declarations) | 0 | |
| `native_decide` | 0 | |
| `implemented_by` / `extern` | 0 | |
| `opaque` (declarations) | 0 | the word appears only in comments |
| `unsafe` | 0 as a declaration modifier | it appears only as an `aesop` rule option in [Schiffer/Challenge.lean line 127](https://github.com/jaumededios/Schiffer/blob/2938e277969c329caf154e48a3d8823f3635c7f1/Schiffer/Challenge.lean#L127) and [Schiffer/Challenge.lean line 145](https://github.com/jaumededios/Schiffer/blob/2938e277969c329caf154e48a3d8823f3635c7f1/Schiffer/Challenge.lean#L145) |
| `set_option maxHeartbeats` | 0 | |

**The three `sorry`s are deliberate.** They are the placeholders of the two *challenge* files, whose purpose is to
state the theorems with Mathlib alone. Neither challenge file is imported by anything: the package root Schiffer.lean
imports `Schiffer.Main`, `Schiffer.Solution`, `Schiffer.FormalConjecturesSolution` and one analysis file. The
corresponding solution files restate the same theorems and prove them.

**The statements match.** Running `diff` on the statement blocks of Schiffer/Challenge.lean and Schiffer/Solution.lean
(definitions `IsEuclideanDisk`, `HasC2Boundary` and all five theorems) shows they differ only in a docstring. The
same holds for the definitions and final theorem of the Formal Conjectures pair. This is a text comparison, not the
comparator tool's kernel-level check.

**Bessel functions are defined, not assumed.** The Bessel function used throughout is defined from its power series
(Schiffer/Bessel/Basic.lean lines 103–108 and line 2289).

## Declarations

All declarations were found by scanning the source text (`extracted: false`), not from a compiled build, so some
dependency links may be missing or wrong. Two consequences for this site:

- The challenge files Schiffer/Challenge.lean and Schiffer/FormalConjecturesChallenge.lean are **not scanned**,
  because they repeat the solution files' names and the scanner would rename one copy. They are linked by line
  number instead.
- Schiffer/Lift/OriginSeries.lean (about 4,900 lines) is **not scanned**: the scanner wrongly took the field name
  `field` in the `SchifferCounterexample` structure to refer to a definition in that file, which pulled thousands of
  unrelated declarations into the headline statements. The file is described in prose on the
  [lift](#/node/Lift.liftLandedConeSolution) page.

## The explanations

Every explanation, quiz and caveat on this site was written by an AI (Claude) from the public source, the module
READMEs and the project's informal write-up. None has been reviewed by a human or by the project's authors. All
nodes are marked `review: draft`. The outlines of the analytic core (Bessel, cone, bifurcation, drift, density) follow
the project's own descriptions and were not traced through the proofs.
