# Trust: what was and wasn't checked

## Not built

**The Lean was not built for this site.** No `lake`, `lean` or `elan` was run. When this site says something "is
proved", it only means the source contains what looks like a complete proof and that no `sorry`, `admit` or `axiom`
appears in the project, not that Lean's kernel accepted it. The repository's REPRODUCING.md describes a Docker build
of the artifact; that was not run either.

## Gaps, axioms and escape hatches

A text search of all 108 `.lean` files at the pinned commit for `sorry`, `admit`, `axiom`, `native_decide`,
`implemented_by`, `extern`, `opaque`, `unsafe` and `maxHeartbeats` finds:

| What | Count | Where |
|---|---|---|
| `sorry` | 0 | |
| `admit` | 0 | |
| `axiom` (declarations) | 0 | |
| `native_decide` | 0 | |
| `implemented_by` | 0 | |
| `set_option maxHeartbeats` | 0 | |
| `@[extern]` | 5 active (+1 commented out) | SLang.lean line 65 (probPure), line 71 (probBind), line 83 (probUniformByte), line 143 (probWhile), line 225 (PMF.run); line 150 (probUntil) is commented out; plus one in SampCert.lean, see below |
| `opaque` | 2 | SLang.lean line 226 (`PMF.run`); [SampCert.lean line 64](https://github.com/leanprover/SampCert/blob/a2c53bb5ff790e729e252958060699b7eff898b9/SampCert.lean#L64) (`DirtyIOGet`) |

### What the `@[extern]` attributes mean

`@[extern]` does not add an axiom and does not affect any theorem. It tells the **compiler** to call a C++ function
instead of the Lean definition. SampCert uses it to make SLang programs executable. The definitions of probPure,
probBind, probUniformByte and probWhile are functions into [0, ∞] and cannot be run. ffi.cpp (69 lines) provides
sampling implementations: a byte from /dev/urandom, a sequential bind, a real loop. `PMF.run` (SLang.lean lines
225–226) is an opaque bridge that runs an SPMF in `IO`.

So every theorem on this site is about the **mathematical meaning** of the samplers. That the C++ implements that
meaning (and that /dev/urandom is uniform) is a trusted assumption, not a proved fact. The same goes for the
Dafny/Python extraction in SampCert/Extractor/.

### The "unsound" helper in SampCert.lean

[SampCert.lean lines 61–64](https://github.com/leanprover/SampCert/blob/a2c53bb5ff790e729e252958060699b7eff898b9/SampCert.lean#L61-L64)
declare `DirtyIOGet : IO ℤ → UInt32` as an `@[extern]` opaque function. The code comment says it "is unsound and
should NOT be part of the code" and is used "until the Python FFI is richer". It is used only by the exported
`DiscreteGaussianSampleGet`. It is not used by any theorem, so it does not affect the results here, but it is part of
the deployed entry point.

## Declarations

All declarations were found by scanning the source text (`extracted: false`), not from a compiled build, so some
dependency links may be missing or wrong. Known problems on this site:

- **Spurious dependencies from short names.** ZeroConcentrated/DP.lean defines helpers named `B`, `C`, `t`, `β`
  and `A_pmf`, and ZeroConcentrated/Postprocessing.lean defines `δ`. The scanner sometimes takes local variables with the same names
  elsewhere (the histogram's bins `B`, the Gaussian loop's `t`, privacy parameters `δ`) for these definitions. So
  some "depends on" lists show links to them that are not real.
- **`SLang` and `SPMF` are not scanned**, because they are declared with explicit universe parameters. The
  [probBind](#/node/probBind) page explains them.
- **SampCert.lean (the top-level file) and SampCert/Extractor/ are not scanned.** SampCert.lean defines an
  example `numBins` that collided with the histogram's variable of the same name. Extractor is code generation, not
  verified mathematics.

## The explanations

Every explanation, quiz and caveat on this site was written by an AI (Claude) from the public source, the README,
paper_mapping.md and the cited papers' standard statements. None has been reviewed by a human or by the project's
authors. All nodes are marked `review: draft`. The walkthroughs follow the proof scripts' structure and comments.
Long proofs (the AboveThreshold coupling, ofDP, the Rényi composition bound) are outlined, not traced line by line.
