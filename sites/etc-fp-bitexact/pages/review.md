# Review: do the statements say what the names claim?

Overall the statements are small, concrete and honestly named. The project's own docs (README, TRUST.md, doc
comments) are unusually careful about what is and isn't claimed. The notes below are mostly about **scope**, where a
reader might read more into a name than the Lean says.

## Config1.verdict_compatible: faithful, and the SAT step is trivial

`compatStmt vendorA vendorB_preserve` is exactly “both admissible implementations output identical bits on all
2¹⁶ inputs”. Both operations are the identity in disguise. The stored certificate is 10 bytes (a one-step
refutation), so although the proof goes through the SAT/LRAT path, the solver does essentially no work. The
project's comment “Bit-blasts (canonOp) ⇒ full footprint + LRAT certificate” (Config1.lean lines 35–36) is
accurate about the mechanism; just don't take it as evidence of a hard SAT problem.

## Config1.verdict_divergent / verdict_silence: faithful

Both are negations of a full-domain universal, refuted on the hand-chosen witness `0x0001`. `verdict_silence`
depends on the modelling decision that an `Unspecified` commitment admits *every* flag. That is the natural audit
reading, and it is stated clearly in Core/Statement.lean lines 46–51. Neither theorem says that *every*
implementation of the silent spec misbehaves, only that the spec does not guarantee agreement.

## Config1.verdict_domain_restricted: faithful, with one naming note

`normalDomain` means “not subnormal”. It includes ±0, infinities and NaNs, not only IEEE *normal* numbers. The
theorem is still exactly what is claimed: off the subnormals the flush flag is inert. The certificate is again
10 bytes and, per CHANGELOG 0.3.0, toolchain-specific.

## Config3: flag-level only

`implStmt` treats an implementation as nothing more than its flush flag, and ignores the op tag and the inputs. So
“backward-compatible” means “every flag v1 admits, v2 admits”. `verdict_versions_compatible` is a two-value
tautology. `verdict_versions_incompatible` is an explicit existential witness (flag `true`) rather than
`¬ implStmt …`, which is equivalent and arguably stronger. The behavioural consequence on actual bits is a separate
ground theorem, `versions_behavioral_bridge`.

## Arith.mul_true: faithful; “SAT-hard” describes the family

Builtin `BitVec 4` multiplication equals the unrolled shift-and-add for all 256 input pairs. This is the one
certificate (~71 KB) where the solver did substantial work. At 4 bits the instance is small. It is a hard
*family* at larger widths, not a hard instance.

## Arith.mul_false: ground inequality

The theorem is the single inequality at `(15, 15)`. The claim that CaDiCaL discovered this witness rests on a
diagnostic quoted in the doc comment (Arith/Audit.lean lines 78–90) from a scratch run that is not in the repo.
That is plausible and clearly disclosed, but it cannot be replayed from the shipped files. The negation
`¬ mulAgree vendorA vendorB_buggy` is not stated, though it follows immediately.

## Things that might surprise a reader

- **“Canonicalize”** is not IEEE 754's canonicalize. `canonOp` is a bit-field recombination that equals the identity,
  chosen so that agreement needs bit-level reasoning.
- **Vendor A's commitment is inert.** `opOf .Canonicalize` ignores the flag, so vendor A's `Pinned Preserve` never
  affects a verdict.
- **No floating-point arithmetic** is modelled: no rounding, no NaN handling, no values. The “IEEE 754” in the
  description is the binary16 bit layout plus the subnormal test.
- A small stale comment: Report/Driver.lean says `lake build` re-checks “the two cached LRAT certificates”, but
  `certs/` holds four (the two multiplier/canary ones were presumably added later).
