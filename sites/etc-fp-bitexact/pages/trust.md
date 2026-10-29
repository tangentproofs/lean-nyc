# Trust: what was and wasn't checked

## Not built

**The Lean was not built for this site.** No `lake`, `lean` or solver was run. “Proved” on this site means the file
contains a complete-looking proof, not that the kernel was observed to accept it. Declarations were scanned from
the source text (`extracted: false`), so dependency edges in the proof graph are approximate (see the note below).

The project itself documents a re-verification protocol (TRUST.md): a clean `lake build` re-checks every stored
certificate with the SAT solver made unavailable, enforced by `scripts/gate-no-solver.sh`.

## Grep counts (pinned commit, all `.lean` files)

| keyword | count |
|---|---|
| `sorry` / `admit` | **0** |
| `axiom` (declared) | **0** |
| `native_decide` | **0** |
| `implemented_by` / `extern` / `opaque` | **0** |
| `debug.skipKernelTC` | **0** |

`#print axioms` lines appear after every proof-core theorem (for example Config1.lean line 68), and
`scripts/axiom-scan.lean` collects the four certificate-backed ones.

## The real trust base (as the project reports it)

There are no `sorry`s, but this is **not** a kernel-only, axiom-free development, and the project says so up front.
According to TRUST.md, each certificate-backed theorem (`verdict_compatible`, `verdict_domain_restricted`,
`mul_true`, `cached_xor_identity`) depends on:

- the Lean kernel;
- `propext`, `Classical.choice` and `Quot.sound` (through Lean core's verified LRAT checker);
- one **native compiler-trust axiom** `*._native.bv_decide.ax_*`, the same mechanism `native_decide` uses: the
  LRAT checker runs as compiled code and its `true` result is accepted as an axiom.

So these results also trust the Lean compiler and the soundness of the verified bit-blaster and checker. The
SAT solver (CaDiCaL) is *not* trusted, since its output is checked. The normalization-closed facts (divergence,
silence, versions, `mul_false`) carry a subset of the classical trio and no native axiom, and
`verdict_versions_incompatible` is reported as axiom-free. **These footprints were measured by the project and not
re-measured here.**

A stored certificate re-checks only on a toolchain whose `bv_decide` preprocessing produces the same SAT problem.
The pinned toolchain is `leanprover/lean4:v4.34.1`, and CHANGELOG 0.3.0 records one certificate that had to be
regenerated after a toolchain bump.

## Certificates

| file | size | used by |
|---|---|---|
| `certs/mul_true.lrat` | ~71 KB | `Arith.mul_true` |
| `certs/smoke.lrat` | ~2.7 KB | `Smoke.cached_xor_identity` |
| `certs/verdict_compatible.lrat` | 10 bytes | `Config1.verdict_compatible` |
| `certs/verdict_domain_restricted.lrat` | 10 bytes | `Config1.verdict_domain_restricted` |

The two 10-byte files contain a single LRAT step deriving the empty clause, i.e. the preprocessed problem was
almost trivially unsatisfiable.

## Dependency graph caveat

The text scanner used by this site does not follow `open` declarations, and these files rely on `open` heavily. So
many “mentions” edges (for example from the Config1 verdicts to `compatStmt` or the fixtures) are missing from the
proof graph. Node bodies link the relevant definitions by hand.

## Explanations

All explanations, quizzes and walkthroughs were written by an AI (Claude) and have **not** been reviewed by the
project's authors. Every node is marked `review: draft`.
