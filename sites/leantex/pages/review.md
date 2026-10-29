# Review: does the code do what it says?

LeanTeX has **no theorems**, so there are no statements to check for faithfulness. Instead, this page compares
each headline with what the README promises, and lists places where a close reading suggests a bug or a
surprise. **Nothing was built or run for this site**, so every "bug" below is a reading of the source, not a
reproduced failure.

## The headlines against the README

- **Escape hatch** ([interpolatedLatexFn](#/node/interpolatedLatexFn)). As described: `[| |]` breaks back into
  Lean, and `@{}` is also allowed (LeanTeX/LatexLiteral.lean lines 58–97). Not mentioned in the README: there is
  no way to write a literal `[|`, `|]` or `@{` in the LaTeX text.
- **DSL for slides** ([elabItem](#/node/elabItem)). As described. The README shows `slide "…" do`; the
  `#latex_slide` command, `latex_env!` and `#latex_command` are undocumented but present.
- **Animations** ([elabItem](#/node/elabItem)). `with steps [a, b, …]` binds the names to 1, 2, …
  (LeanTeX/SlideDSL.lean lines 279–292), as the README describes.
- **TikZ DSL** ([elabTikzItem](#/node/elabTikzItem)). Not in the README at all; it is the largest single piece of
  the code.
- **Static files** ([generateSlides](#/node/generateSlides)). As described: `static/` is copied into `build/`
  (GenerateSlidesLib.lean lines 60–61).
- **The PDF lands in build/slides.pdf.** Consistent with LaTeX running in `build/` on `slides.tex` (line 63).

## Suspected bugs and surprises (by reading only)

1. **Environment options in the wrong place.** For `latex_env! [opts] env do …`, LeanTeX/LatexGen.lean line 63
   prints `\begin[opts]{env}`. LaTeX's syntax is `\begin{env}[opts]`, so this form would likely fail to compile.
   The forms without options are fine. ([renderContent](#/node/renderContent))
2. **Coordinate numbering in `with coordinates` without options.** The version with options numbers the
   bindings left to right (LeanTeX/SlideDSL.lean line 201); the version without options numbers them right to
   left (line 215). The printed `\p1, \p2, …` are always left to right (LeanTeX/LatexGen.lean line 19). With two or
   more bindings and no options, the names would refer to the wrong points. ([elabTikzItem](#/node/elabTikzItem))
3. **Package order is not declaration order.** Packages are kept in a hash map (LeanTeX/PackageRegistry.lean
   line 18) and printed in its order (line 42). Order-sensitive packages may be loaded in the wrong order.
   ([#usepackage](#/node/LeanTeX.addPackage))
4. **LaTeX failures are silent and LaTeX runs once.** The exit status is ignored (GenerateSlidesLib.lean
   lines 63–64), and there is no second pass for references.
5. **`-shell-escape` is always on** (line 63). Building a deck from an untrusted source lets its LaTeX run shell
   commands. This is a design choice, but worth knowing.
6. **The example project looks out of date.** example/GenerateSlides.lean uses commands named
   `#declared_slides`, `#declared_packages` and `#declared_preamble` and a three-argument `generateSlides`
   (example/GenerateSlides.lean lines 4–10). None of these exist in the library at the pinned commit, which uses
   `#leantex_config` and a one-argument `generateSlides` (GenerateSlidesLib.lean lines 26, 51). Because the
   bootstrap never overwrites an existing GenerateSlides.lean, the example would probably not build as checked in.
   In addition, example/Example.lean does not import the Intro, Motivation and Conclusion modules, so their
   `@[presentation]` slides would not be registered in the deck unless something else imports them.
7. **The bootstrap does not wait** for the second `lake exec` it starts (GenerateSlides.lean lines 53–56).

## Honesty labels

There is nothing to label PARTIAL or CONDITIONAL: there are no proofs, and no `sorry`. The word "unsafe" on
several definitions is Lean's marker for code that evaluates declarations at run time; it is normal for
metaprograms and has nothing to do with proof gaps (see [Trust](#/trust)).
