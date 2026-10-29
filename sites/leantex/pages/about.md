# About this site

## The project

[kiranandcode/LeanTeX](https://github.com/kiranandcode/LeanTeX) is **Kiran Gopinathan**'s Lean 4 library for
making LaTeX Beamer presentations. The README sums it up as "LaTeX presentations in Lean 4", for people who want
"macros and extensibility without having to learn TeX". The commits run from April to December 2025 and the
library targets Lean 4.26 (the update to 4.26 was an outside contribution, merged in December 2025).

You write a Lean project that requires LeanTeX, write your slides as Lean definitions, and run
`lake exec GenerateSlides`. LeanTeX generates `build/slides.tex` and runs `pdflatex` on it.

## What the Lean is

**LeanTeX is a tool, not a proof development. It contains no theorems, lemmas or proofs.** Its Lean is
metaprogramming: a hand-written parser, new syntax categories, macros and elaborators that run while Lean reads
your files, environment extensions that remember what you declared, and an ordinary program that writes a file and
calls LaTeX. So the "headlines" on this site are its main pieces of machinery, and the walkthroughs outline how the
code works rather than how a proof goes.

The pieces, in the order a user meets them:

1. **The LaTeX literal** `latex![| … |]` ([interpolatedLatexFn](#/node/interpolatedLatexFn)): raw LaTeX inside Lean,
   with holes back into Lean.
2. **The slide DSL** ([elabItem](#/node/elabItem)): `slide "Title" do …` and `#latex_slide`, with LaTeX-looking
   `\begin{…}`, `\item{…}` lines and named animation steps.
3. **The TikZ DSL** ([elabTikzItem](#/node/elabTikzItem)): structured `node`, `draw`, layers and Lean `for`
   loops inside `tikz do`.
4. **The registries**: `@[presentation]`, `#usepackage`, `#latex_preamble`, `#latex_executable` and
   `#latex_option` only *record* things, and [#leantex_config](#/node/elabLeanTexConfig) gathers them into one
   [LeanTeXConfig](#/node/LeanTeXConfig).
5. **The build** ([generateSlides](#/node/generateSlides)) renders everything and runs LaTeX, and
   [the bootstrap](#/node/generateSlidesLean) sets up `lake exec GenerateSlides` in your project the first time.

About 1,040 lines of Lean in 11 files, most of it in LeanTeX/SlideDSL.lean. The repository also has an `example/`
project (a short demo deck with a custom Beamer theme), which this site describes but did not scan.

## Where to start

Read the three DSL headlines first, then [generateSlides](#/node/generateSlides). The [review page](#/review)
lists a few places where the code, read closely, seems not to do what a user would expect. None of them were
tested, since nothing was built or run for this site.

## What this site leaves out

Small helper functions (the option and interval expanders, `leanTexStart`, the registry getters) are explained
inside the nodes that use them rather than on their own pages. The alternative `LeanTeX.loadSlides`, which
evaluates slides inside Lean, is mentioned only in passing.
