# NOTES for the coordinator (etc-fp-bitexact)

## Time spent
About 40 minutes: reading roughly 1,300 lines of Lean and the docs, then writing, then a few build iterations.

## What was hard
- **Choosing what to call a "result".** This is a demonstration substrate, not a theorem library. The theorems are
  deliberately small (several are one-liners or two-value tautologies). The interesting content is the workflow
  and the trust model, so I put a lot of weight on the Trust page and on honest scale notes (10-byte certificates
  versus the 71 KB one).
- **Engine limitation (not fixed, as instructed).** `engine/tools/scan_decls.py` never fills in `"opens"`, so
  identifiers reached through `open X Y` are not resolved. Every Config1/Config3 verdict therefore shows
  **no meaning-dependencies** in decls.json, and `vendorOp` shows none on `isSubnormal`. The proof graph is sparse
  as a result. Workaround: node bodies link the definitions by hand, and the Trust page explains the gap.
  Suggested fix: record `open` lines per file and try each opened namespace in `resolve()`.
- The remaining "no explainer yet" warnings are for `Arith.opOf`, `Arith.MulICD`, `Arith.vendorA` /
  `vendorB_*`, `Arith.w9x` / `w9y`, `expMask` / `mantMask`, and `Core.ICD.OpTag` / `Commitment`. All of them are covered
  in prose inside `Arith.mulAgree`, `Core.Format.isSubnormal` and `Core.ICD.MockICD` rather than as separate nodes.

## Decisions I made
- Headlines (6): `Config1.verdict_compatible`, `Config1.verdict_silence`, `Config1.verdict_domain_restricted`
  (which the project calls its "signature result"), `Config3.verdict_versions_incompatible`, `Arith.mul_true`,
  `Arith.mul_false`. `verdict_divergent` is a normal node, because `verdict_silence` is the same proof plus the
  more interesting point.
- Roots exclude `ETCFPBitexact/Report/` (the IO/presentation shell, which the project keeps out of the proof cone),
  `LiveSolveCanary.lean` and `scripts/`. The About page says so.
- `authors` left as given ("Evolving Technologies Corporation (Loren Abdulezer)"), which matches the README, the
  source headers and CITATION.cff. The licence matches (an Apache-2.0 LICENSE plus NOTICE exist).
- Nothing is labelled PARTIAL: there are 0 sorry/admit/axiom/native_decide in the source. Nothing is labelled
  CONDITIONAL. I did flag the **native compiler-trust axiom** that `bv_decide`/`bv_check` introduce, as reported by
  the project's own TRUST.md, which I did not re-measure.

## Where I am least sure
- **`Config1.verdict_compatible` / `verdict_domain_restricted`, the reading of the 10-byte certs.** Both files
  contain `3 0 1 2 0`. I read this as one LRAT addition step deriving the empty clause from unit clauses 1 and 2,
  i.e. preprocessing left an almost trivially UNSAT problem. I am fairly but not fully sure of that LRAT reading,
  and of the claim that the "solver did essentially no work".
- **Axiom footprints** (Trust page, several caveats). Copied from TRUST.md, CHANGELOG 0.3.0 and the Report strings,
  not measured. The sources slightly disagree in detail: `trustEvaluated` says "propext, Quot.sound", the versions
  scenario string says the full trio, and `mul_false` is "propext only". I attributed these to the project rather
  than asserting them.
- **`Arith.mul_true`, "a small instance of a hard family".** This is my characterisation. The project calls it
  "genuinely SAT-hard".
- **`Core.Ops.canonOp`, the comparison with IEEE 754 `canonicalize`.** I state that the IEEE operation can alter
  non-canonical encodings. That is true in general, but binary16 interchange encodings are mostly canonical, so the
  contrast may be overstated.
- **`Config3.verdict_versions_incompatible`, the "Ariane-flavored" gloss.** I paraphrased it as "a spec change
  silently invalidating an old component". The project does not expand on it.

## What the author might object to
- Repeatedly pointing out that the two Config-1 certificates are trivial (10 bytes), and that 4-bit multiplier
  equivalence is a small instance. Both are true, but they could read as downplaying the demo.
- Noting that "Canonicalize" is not IEEE canonicalize, that vendor A's commitment is inert, and that
  `normalDomain` includes NaN, ±0 and infinities.
- Noting that the "solver-discovered" witness for `mul_false` cannot be replayed from the repo (the scratch run is
  only quoted in a comment).
- The Review page points out a stale comment in Report/Driver.lean ("the two cached LRAT certificates", but there
  are four).
- Trademark: I reproduced the README's "ETC Verify™ … trademark … application pending" wording once on the About
  page, attributed to the README.
