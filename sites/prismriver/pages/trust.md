# Trust: what was and wasn't checked

## Not built

The Lean was **not compiled** for this site (no `lake`, no `lean`). Declarations were scanned from the source
text at the pinned commit (every declaration has `extracted: false`). "Proved" here means "the file contains a
complete-looking proof with no `sorry`", not "the kernel accepted it". The upstream repository runs CI
(`.woodpecker.yml`), but this site did not check its results.

## Grep results (whole repository, pinned commit)

| Pattern | Count | Where |
|---|---|---|
| `sorry` / `admit` | 0 | none |
| `axiom` | 0 | none |
| `native_decide` | 2 | Prismriver/Composition/Counterpoint.lean lines 126–127, inside an `example`; no headline depends on it |
| `implemented_by` / `extern` / `opaque` | 0 | none |
| `unsafe` | 1 | Prismriver/IO/Alda.lean line 22 (playback IO, not a proof) |
| `partial def` | 7 | Prismriver/IO/Xml.lean (XML printer and parser, lines 33–515), not proofs |

The proofs use `simp`, `omega` and `grind` heavily; these produce ordinary kernel-checked terms.

## The explanations

Every node on this site was written by an AI (Claude) from the source and is **unreviewed** by the project's
authors (`review: draft`). Line references point to the pinned commit. Where an explanation goes beyond what a
statement literally says (for example the minor-triad label convention), the node says so in its caveats.
