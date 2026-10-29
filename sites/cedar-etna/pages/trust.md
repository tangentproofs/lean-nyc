# Trust: what was and wasn't checked

## Not built

**The Lean was not built for this site.** No `lake`, `lean` or `elan` was run, and no ETNA property, witness or
random search was executed. When we say a theorem "is proved", we only mean the source file contains what looks like
a complete proof with no `sorry`, not that Lean's kernel accepted it. The project targets `leanprover/lean4:v4.29.1`
(lean-toolchain) and depends on Batteries and Plausible (cedar-lean/lakefile.lean).

At the pinned commit the source is the **fixed** (base) state: no ETNA patch is applied, so the upstream proofs are
in their original form. Reverse-applying a patch puts a bug back, and the README warns that this can break the proofs.
ETNA therefore builds only the `etna_cedar` executable.

## Gaps, axioms and escape hatches

A text search of all 355 `.lean` files at the pinned commit (comments excluded where possible):

| What | Count | Where |
|---|---|---|
| `sorry` | 0 | |
| `admit` | 0 | |
| `axiom` | 0 | |
| `native_decide` | 26 | 8 in Cedar/Thm/SymCC/Data/Ext.lean (lines 36–110), 2 in Cedar/Data/Int64.lean (lines 101, 106), 16 in UnitTest/ (Decimal, IPAddr) |
| `implemented_by` / `opaque` | 2 / 2 | cedar-lean/CedarFFI/Main.lean (lines 265–275), the solver FFI, outside the proofs |
| `extern` | 0 | |
| `unsafe` | 88 | CedarFFI/Main.lean, DiffTest/Main.lean, Cli/Main.lean: executables, outside the proofs |

The 10 `native_decide` uses in the library are small Int64 facts, such as `(0 : Int64).toInt = 0` and the number of
milliseconds per day. `native_decide` asks Lean's compiled code to evaluate a decision procedure. The result is trusted
through the `Lean.ofReduceBool` axiom, which trusts the compiler as well as the kernel. Cedar/Thm/SymCC/Data/Ext.lean
is imported by the SymCC proof tree (Cedar/Thm/SymCC/Data.lean and Cedar/Thm/SymCC/Compiler/Call.lean). So the SymCC
headlines ([compile_is_sound](#/node/Thm.compile_is_sound), [verifyEquivalent_is_sound](#/node/Thm.verifyEquivalent_is_sound))
very likely depend on it. We did not trace exact dependencies. Cedar/Data/Int64.lean is imported by the decimal and
datetime extensions, so the other headlines may depend on its two uses too.

## Declarations

Declarations were found by scanning source text (`extracted: false`), not from a compiled build. The scanner
**does not recognise declarations marked `public`** (Lean's module system), which most of Cedar/Spec, Cedar/Validation
and Cedar/SymCC use. So core definitions such as `isAuthorized`, `evaluate`, `validate`, `Policy` and `Request` have no
node or declaration entry. The node texts describe them and link to their exact lines instead. Some dependency links
are missing for the same reason. About 80 of the 355 files were scanned (see About for what was left out).

## The explanations

Every explanation, quiz and caveat on this site was written by an AI (Claude) from the public source, the README and
etna.toml. None has been reviewed by a human or by the project's authors. All nodes are marked `review: draft`.
