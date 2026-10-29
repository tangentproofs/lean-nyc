# Trust: what was and wasn't checked

## Not built

**The Lean was not built or run for this site.** No `lake`, `lean` or `elan` was run, and no slides were
generated. Every description of behaviour, including the suspected bugs on the [review page](#/review), comes
from reading the source at the pinned commit.

## Theorems, gaps and escape hatches

LeanTeX has **no theorems**, so "proved" never applies here. A text search of all `.lean` files at the pinned
commit (library and example) finds:

| What | Count | Where |
|---|---|---|
| `theorem` / `lemma` | 0 | |
| `sorry` / `admit` | 0 | |
| `axiom` | 0 | |
| `native_decide` | 0 | |
| `implemented_by` / `extern` / `opaque` | 0 | |
| `unsafe` | 6 | LeanTeX/SlideRegistry.lean lines 30 and 34, GenerateSlidesLib.lean lines 28 and 51, GenerateSlides.lean line 31 (inside a string template), example/GenerateSlides.lean line 9 |
| `partial` | 5 | LeanTeX/LatexLiteral.lean lines 34, 121 and 132; LeanTeX/SlideDSL.lean lines 145 and 262 |

`unsafe` is needed because the code evaluates declarations by name (`evalConst`) or is called from such code.
`partial` marks functions Lean does not check for termination. Neither matters for a tool with no proofs.

## Running external programs

At run time the generated program runs `cp` (to copy `static/`) and the LaTeX program with `-shell-escape`, and
the bootstrap edits your `lakefile.lean` and runs `lake`. See [generateSlides](#/node/generateSlides) and
[the bootstrap](#/node/generateSlidesLean).

## Declarations

All declarations were found by scanning the source text (`extracted: false`), not from a compiled build. Known
scanner artefacts on this site:

- a declaration `main` is listed at GenerateSlides.lean line 31, but that line is inside a string (the template
  of the generated file); the real `main` (line 38) is listed as `main'`;
- syntax declarations, `elab_rules` and `initialize` blocks are not declarations to the scanner, so the commands
  `#latex_slide`, `#usepackage` and so on, and the `@[presentation]` attribute, are explained inside the nodes of
  the functions they call.

## The explanations

Every explanation, quiz and caveat on this site was written by an AI (Claude) from the public source. None has
been reviewed by a human or by the project's author. All nodes are marked `review: draft`.
