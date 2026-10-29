# NOTES for the coordinator (leantex)

## Time spent
About 1 hour: reading all ~1,040 lines of library Lean plus the example project, writing 22 nodes and 3 pages,
and a few build iterations (the first failed only on schema limits: ≥ 3 quiz questions per node, summary ≤ 300
characters).

## Calls I made
- **No theorems, so the headlines are machinery.** Five headlines: `interpolatedLatexFn` (the `latex![| |]`
  literal parser), `elabItem` (the slide DSL), `elabTikzItem` (the TikZ DSL), `elabLeanTexConfig`
  (`#leantex_config`, which gathers the registries) and `generateSlides` (the run-time PDF build). The lead, About,
  Review and Trust pages all say plainly that there are no theorems.
- **Commands without declarations.** `syntax`/`elab_rules`/`initialize` are invisible to the scanner, so
  `#latex_slide`, `#usepackage`, `#latex_preamble`, `#latex_executable`, `#latex_option`, `#latex_command` and the
  `@[presentation]` attribute are explained on the node of the function each one calls (`LeanTeX.addPackage`,
  `LeanTeX.getPreambleStr`, `LeanTeX.setLatexCommand`, `LeanTeX.loadSlidesStx`). Node titles name the commands.
- **The bootstrap `main`** is explained on `generateSlidesLean`, not on `main'` (the scanner's name for it), to
  avoid an apostrophe in a node URL.
- **Roots:** LeanTeX.lean, LeanTeX/, GenerateSlides.lean, GenerateSlidesLib.lean. `example/` is not scanned, so
  references to example/… files on the review page are plain text, not links.
- **No licence:** no code blocks, no verbatim statements, no `lean:` walkthrough fields. Inline identifiers and
  the DSL's keywords (`\begin`, `with steps`, `#usepackage`) are named, as in the README; I didn't reproduce
  any multi-token code. The README states no licence either, so there was nothing to escalate.
- **Authors:** Kiran Gopinathan, as in site.json (all commits are theirs apart from one merged outside PR that
  updated to Lean 4.26; I mention the outside contribution without naming the contributor).

## Places I'm least sure of
- **renderContent / review item 1** (`\begin[opts]{env}`): I read LeanTeX/LatexGen.lean line 63 as putting the
  options before the braced name. I'm confident in the reading of the format string; I'm not 100% sure that LaTeX
  rejects it outright in every setting (it should: `\begin` reads one argument, which would be `[`).
- **elabTikzItem caveat / review item 2** (foldlM vs foldrM coordinate numbering, LeanTeX/SlideDSL.lean
  lines 201 and 215): fairly confident there is an asymmetry. Whether it bites depends on `foldrM` processing order,
  which I believe is right-to-left. Untested.
- **LeanTeX.addPackage caveat** (hash-map order): `PersistentHashMap.toList` order is not insertion order, I'm
  fairly sure, but I didn't check the Lean core implementation.
- **LeanTeX.getPreambleStr / setLatexCommand** ("first declaration wins"): rests on the merge functions
  `(·.or ·)` and `(·.getD ·)` coercing `Name` to `Option Name`. Plausible but untested; I hedged in the caveat.
- **LeanTeX.loadSlidesStx** (cross-file slide order follows import order): reasonable reading of how
  `SimplePersistentEnvExtension` merges imported entries; untested.
- **generateSlidesLean**: that a user project's own `GenerateSlides` exe takes precedence over the dependency's
  one with the same name on later `lake exec` runs. That's how the design must work, but I didn't confirm Lake's
  resolution rule.
- **Review item 6** (example project out of date): example/GenerateSlides.lean calls `#declared_slides` etc.,
  which don't exist in the library at this commit. I'm confident about that. "Intro/Motivation/Conclusion slides
  not registered" assumes nothing else imports those modules; the example's lakefile only declares `lean_lib Example`.

## Engine notes
- The scanner lists a declaration `main` at GenerateSlides.lean line 31, which is inside a multi-line string
  literal (the template of the generated file); the real `main` gets the deduplicated id `main'`. Worked around by
  not using either id; the Trust page notes it.
- Remaining "meaning-dependency has no explainer" warnings are all small helpers (`beamerPostamble`,
  `expandTikzAtSpec`, `expandIntervalSpec`, registry getters, …), each described inside its parent node.

## What the author might object to
- The review page lists seven "suspected bugs and surprises" found by reading only. Items 1, 2 and 6 are the ones
  most likely to be wrong-footed by something I missed; all are worded "by this site's reading" and "untested".
- Calling out `-shell-escape` as always on could read as a security criticism. I framed it as a design choice
  worth knowing about.
