# About this site

## What the project is

[etc-fp-bitexact](https://github.com/evolvingtech/etc-fp-bitexact) is by **Evolving Technologies Corporation**, with
Loren Abdulezer named as author in every source header and in `CITATION.cff`. In the README's own words it is
“an open, independently re-checkable, bit-exact IEEE 754 verification component … designed to integrate with the
ETC Verify™ framework” (ETC Verify is a trademark of Evolving Technologies Corporation, application pending).

It is **not a theorem library** in the usual sense. It is a small, Mathlib-free *demonstration substrate* for one
workflow:

1. capture two (invented) interface specs as data ([MockICD](#/node/Core.ICD.MockICD));
2. build the proposition “every pair of implementations these specs allow produces identical bits”
   ([compatStmtOn](#/node/Core.Statement.compatStmtOn));
3. settle it with Lean's `bv_decide` bit-blaster, either proving agreement or producing a concrete counterexample input;
4. store the SAT solver's LRAT proof under `certs/` so that anyone can later re-check it with `bv_check`
   and no solver installed;
5. present each scenario through a report layer (`Report/`).

The README is explicit that the fixtures are invented, that “it formalizes no real interface”, and that it is “not a
theorem prover, a model checker, or a verification product for any particular industry”.

## What the Lean covers

- **Configuration 1, two vendors** (Config1.lean): [compatible](#/node/Config1.verdict_compatible),
  [divergent](#/node/Config1.verdict_divergent), [silence](#/node/Config1.verdict_silence) and
  [domain-restricted](#/node/Config1.verdict_domain_restricted).
- **Configuration 3, two versions of one spec** (Config3.lean): [relaxing is backward-compatible](#/node/Config3.verdict_versions_compatible),
  and [tightening is not](#/node/Config3.verdict_versions_incompatible).
- **Arithmetic SAT stress** (Arith/): [4-bit multiplier equivalence](#/node/Arith.mul_true) with a substantial certificate, and a
  [defective multiplier](#/node/Arith.mul_false) caught on a solver-found witness.
- **Plumbing**: a [divergence-witness bundle](#/node/DivergenceWitness) and a [certificate canary](#/node/Smoke.cached_xor_identity).

The only floating-point notion actually modelled is the binary16 bit layout and the
[subnormal test](#/node/Core.Format.isSubnormal). The operations are rounding-free passthroughs that differ only in
whether they flush subnormals to zero. There is no IEEE 754 arithmetic, rounding or NaN semantics.

## What this site leaves out

- The **report shell** (`ETCFPBitexact/Report/`, about 380 lines): report types, a text renderer, a JSON serializer
  and an `#eval` driver. It is IO and presentation, not part of what the theorems depend on, and the project keeps it
  out of the proof cone deliberately. It is still browsable on the Source page via GitHub.
- `LiveSolveCanary.lean` (the live-solver twin of the canary) and the maintainer scripts under `scripts/` are
  mentioned but not given nodes.

## Where to start

Read [compatStmtOn](#/node/Core.Statement.compatStmtOn), then the four Configuration-1 verdicts in order.
The [Review](#/review) page discusses what each headline does and doesn't claim, and [Trust](#/trust) covers what
was checked.
