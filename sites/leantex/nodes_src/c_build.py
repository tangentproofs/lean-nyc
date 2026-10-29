NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]


node("LeanTeX.loadSlidesStx",
 "The @[presentation] attribute and the slide registry",
 "Tagging a definition @[presentation] records its name in a list that Lean saves with the compiled file; the deck is that list, in the order the files were imported and the slides declared.",
 r"""## Plain English

LeanTeX never scans your files for slides. Instead it uses Lean's **environment extensions**: small pieces of
state that Lean stores alongside each compiled module and merges when modules are imported.

- `slideRegistry` (LeanTeX/SlideRegistry.lean lines 5–10) is a list of declaration names. Imported lists are
  concatenated.
- The attribute `@[presentation]` (lines 12–17) does nothing but add the tagged declaration's name to that list.
  `#latex_slide` applies it for you ([elabItem](#/node/elabItem)).

**Definition (`LeanTeX.loadSlidesStx`, lines 24–28).** Reads the list and returns the *syntax* of a Lean list of
those names, one identifier per slide. [#leantex_config](#/node/elabLeanTexConfig) pastes that list into a
definition, so the slides are referred to by name and evaluated when the presentation program runs.

There is also `LeanTeX.loadSlides` (lines 34–37), which evaluates the slides directly inside Lean with
`evalConst`; the build path shown in this site does not use it.

### Order

Within a file, slides appear in declaration order. Across files, the order is the order Lean merges imported
modules, which follows the import graph. So to control the order of sections, control the imports.
""",
 [q("How does LeanTeX find all slides?",
    ["Each @[presentation] tag adds a name to a list stored with the compiled module",
     "It greps the .lean files for #latex_slide", "You list them by hand in a config file"], 0,
    "LeanTeX/SlideRegistry.lean lines 12–17: the attribute's handler adds the name to `slideRegistry`."),
  q("What does loadSlidesStx return?",
    ["Lean syntax for a list of the slide names", "The rendered LaTeX", "A PDF"], 0,
    "Lines 24–28 build a list literal of identifiers."),
  q("A slide is in a file that nothing imports. Is it in the deck?",
    ["No: only modules in the import graph contribute their registry", "Yes, always"], 0,
    "Registries are merged from imported modules only (line 9). The generated program imports your `lean_lib` roots ([generateSlidesLean](#/node/generateSlidesLean)), so a file must be reachable from one of them."),
 ],
 caveats=["The exact cross-file order depends on how Lean orders imported modules; this site did not test it."])


node("LeanTeX.addPackage",
 "#usepackage and the package registry",
 "#usepackage name with options [...] records a LaTeX package in a map keyed by name; declaring the same package twice with different options is a compile-time error, and the generated preamble gets one \\usepackage line per package.",
 r"""## Plain English

**Definition (`LeanTeX.addPackage`, LeanTeX/PackageRegistry.lean lines 29–37).** Called by the `#usepackage`
command (LeanTeX/SlideDSL.lean lines 343–363). It looks the package name up in `packageRegistry` (lines 18–26), a
persistent map from package names to a `UsePackageDecl` (a name and a list of options, lines 5–8):

- if the package is new, it is added;
- if it is already there with the same options, nothing happens;
- if it is there with **different** options, Lean reports an error.

`LeanTeX.getPackageStr` (lines 39–42) prints every entry as `\usepackage[opts]{name}` (or without brackets when
there are no options, lines 10–16), one per line. That text goes into the
[preamble](#/node/beamerPreamble).

Package options must be literal ([why](#/node/expandLatexOption)). A package name can be an identifier or a
string, so `#usepackage beamerthemeleantex` works, as in the example project.
""",
 [q("What happens on `#usepackage geometry with options [a4paper]` after `#usepackage geometry`?",
    ["An error: the package is redeclared with different options", "The options are merged",
     "The second line wins"], 0,
    "LeanTeX/PackageRegistry.lean lines 35–37 throw 'redeclaration of package … with different options'. No options counts as the empty list."),
  q("Are packages printed in the order you declared them?",
    ["Not necessarily: they come out in the hash map's order", "Yes, always"], 0,
    "The registry is a hash map (line 18) and `getPackageStr` prints `toList` of it (line 42). See the caveat."),
 ],
 caveats=["By this site's reading, package order in the output is the hash map's internal order, not declaration order. Some LaTeX packages (hyperref is the usual example) must be loaded last; with LeanTeX you cannot rely on #usepackage order for that. Put order-sensitive packages in a #latex_preamble instead. Untested."])


node("LeanTeX.getPreambleStr",
 "#latex_preamble and #latex_preamble_template",
 "Each #latex_preamble literal becomes a hidden definition whose name is recorded; the generated program concatenates them all into the preamble. #latex_preamble_template replaces LeanTeX's default document header altogether.",
 r"""## Plain English

**`#latex_preamble`** (LeanTeX/SlideDSL.lean lines 365–375) takes a [LaTeX literal](#/node/interpolatedLatexFn),
turns it into a `String` expression, declares it as a definition with a fresh name, and records that name with
`LeanTeX.addPreambleSnippet` (LeanTeX/PreambleRegistry.lean lines 20–21). The example project uses it for
`\title`, `\author`, `\institute` and `\date`, splicing in a Lean helper that sets the font size.

**Definition (`LeanTeX.getPreambleStr`, LeanTeX/PreambleRegistry.lean lines 28–36).** Returns the *syntax* of the
expression "snippet 1 ++ newline ++ snippet 2 ++ …", or the empty string if there are none. Because snippets are
referred to by name, Lean computes them when the presentation program runs, so they can call your own functions.

**`#latex_preamble_template`** *f* (LeanTeX/SlideDSL.lean lines 377–383) declares *f*, a function from the package
text and the preamble text to a string, as the document header. It replaces the default
[beamerPreamble](#/node/beamerPreamble), so you can use a different document class.
`LeanTeX.getPreambleTemplateCommand` (LeanTeX/PreambleRegistry.lean lines 38–43) hands it to the configuration.
Declaring a second template only produces a warning, and by this site's reading the first one stays in force.
""",
 [q("When is the text of a #latex_preamble snippet computed?",
    ["When the presentation program runs, because the config refers to the snippet by name",
     "When LeanTeX is installed", "When pdflatex runs"], 0,
    "The snippet is a `def` (SlideDSL.lean line 374), and getPreambleStr builds an expression that mentions those defs (PreambleRegistry.lean lines 34–36)."),
  q("How would you make a non-Beamer document, say an article?",
    ["Supply your own header with #latex_preamble_template", "Write #usepackage article",
     "It is impossible"], 0,
    "The template replaces `beamerPreamble`, which hard-codes the beamer document class (GenerateSlidesLib.lean lines 9–10, 53). The frames would still be Beamer frames, though."),
 ],
 caveats=["'First template wins' rests on reading the registry's merge functions (PreambleRegistry.lean lines 12–17), which rely on an implicit coercion; it was not tested."])


node("LeanTeX.setLatexCommand",
 "#latex_executable and #latex_option",
 "Two commands choose how the .tex file is compiled: #latex_executable sets the program (pdflatex by default) and #latex_option adds command-line options.",
 r"""## Plain English

**`#latex_executable "…"`** (LeanTeX/SlideDSL.lean lines 397–407) declares the string as a hidden definition and
records its name with **`LeanTeX.setLatexCommand`** (LeanTeX/LatexCommandRegistry.lean lines 19–22), which warns
if one was already set in the same file. Use it to switch to `xelatex` or `lualatex`.

**`#latex_option "…"`** (SlideDSL.lean lines 385–395) does the same for an extra command-line option, recorded by
`LeanTeX.addLatexCommandOption` (lines 24–25). Options accumulate.

Both accept Lean's usual `s!` interpolation, not the LaTeX literal. `LeanTeX.getLaTeXCommand` and
`LeanTeX.getLaTeXCommandOptions` (lines 27–42) turn the registries into Lean expressions for the
[configuration](#/node/elabLeanTexConfig). If no executable is set, [generateSlides](#/node/generateSlides) uses
`pdflatex`.
""",
 [q("What runs if you never write #latex_executable?", ["pdflatex", "xelatex", "Nothing"], 0,
    "GenerateSlidesLib.lean line 55: the command defaults to \"pdflatex\"."),
  q("Can you pass several options?", ["Yes; each #latex_option adds one", "No, only one"], 0,
    "The options registry is an array that grows with each entry (LatexCommandRegistry.lean lines 12–17)."),
 ],
 caveats=["-shell-escape is always added after your options (GenerateSlidesLib.lean line 63), whatever you configure."])


node("LeanTeXConfig",
 "LeanTeXConfig: everything needed to build the PDF",
 "A plain record collecting what the registries hold: the slides, the package lines, the preamble text, the LaTeX program and its options, and an optional replacement document header.",
 r"""## Plain English

**Structure (`LeanTeXConfig`, GenerateSlidesLib.lean lines 13–21).** Six fields:

- the list of [slides](#/node/Slide);
- the `\usepackage` lines, as one string ([packages](#/node/LeanTeX.addPackage));
- the preamble text ([preamble snippets](#/node/LeanTeX.getPreambleStr));
- the LaTeX program, if set, and its extra options ([#latex_executable](#/node/LeanTeX.setLatexCommand));
- an optional header function taking the package text and the preamble text.

[#leantex_config](#/node/elabLeanTexConfig) builds one from the registries, and
[generateSlides](#/node/generateSlides) consumes it. Because it is an ordinary structure, you could also build
or modify one by hand before calling `generateSlides`.
""",
 [q("Where does a LeanTeXConfig usually come from?",
    ["The #leantex_config command, which reads all registries", "You type it in by hand", "A JSON file"], 0,
    "GenerateSlidesLib.lean lines 26–45."),
 ])


node("elabLeanTexConfig",
 "Headline: #leantex_config, collecting the whole presentation",
 "One command, #leantex_config name, reads every LeanTeX registry in the current environment (slides, packages, preamble, LaTeX program, options, header template) and defines name as a LeanTeXConfig holding all of it. This is where compile-time bookkeeping becomes a run-time value.",
 r"""## Plain English

**Command elaborator (`elabLeanTexConfig`, GenerateSlidesLib.lean lines 26–45).** It is not a theorem; it is the
step that ties the library together.

While Lean reads your presentation files, the commands `#latex_slide`, `@[presentation]`, `#usepackage`,
`#latex_preamble`, `#latex_executable` and friends only *record names* in environment extensions. Nothing is
rendered. When a file that imports all your slides says `#leantex_config latexConfig`, this elaborator:

1. asks each registry for its contents as Lean syntax:
   [the slide list](#/node/LeanTeX.loadSlidesStx), [the package lines](#/node/LeanTeX.addPackage) (as a string
   literal), [the preamble expression](#/node/LeanTeX.getPreambleStr),
   [the LaTeX program and options](#/node/LeanTeX.setLatexCommand) and the header template;
2. emits the command "define `latexConfig` to be a [LeanTeXConfig](#/node/LeanTeXConfig) made of those six
   things" and elaborates it.

The result is an ordinary definition. The `main` function of the generated program then passes it to
[generateSlides](#/node/generateSlides).

You normally never write this command yourself: the bootstrap ([generateSlidesLean](#/node/generateSlidesLean))
writes a `GenerateSlides.lean` file containing it.
""",
 [q("When does #leantex_config read the registries?",
    ["When Lean elaborates the file containing the command, so it sees only what that file imports",
     "When the program runs", "When pdflatex runs"], 0,
    "It is a command elaborator (GenerateSlidesLib.lean lines 27–28) that queries the current environment (lines 30–35)."),
  q("What does it produce?",
    ["A definition of type LeanTeXConfig with the given name", "A .tex file", "A theorem"], 0,
    "Lines 36–44 elaborate a `def … : LeanTeXConfig := LeanTeXConfig.mk …`."),
  q("Which of these does #leantex_config NOT collect?",
    ["The contents of the static/ directory", "The slides", "The package list", "The LaTeX program"], 0,
    "Static files are copied by generateSlides at run time (lines 60–61), not recorded in the config."),
 ],
 caveats=["Declared `unsafe`, as is generateSlides; Lean then refuses to use it in proofs. This is normal for metaprograms and has no bearing on correctness claims, since there are none."],
 widgets=walk("How the command works (GenerateSlidesLib.lean, lines 26–45)", [
    {"text": "Line 26: declare the syntax #leantex_config followed by a name, and attach this elaborator to it (line 27)."},
    {"text": "Line 30: the slide registry as a list literal of slide names.", "link": "LeanTeX.loadSlidesStx"},
    {"text": "Line 31: the package registry, already rendered to \\usepackage lines, as a string literal.", "link": "LeanTeX.addPackage"},
    {"text": "Line 32: the preamble snippets as one concatenation expression.", "link": "LeanTeX.getPreambleStr"},
    {"text": "Lines 33–35: the LaTeX program, its options, and the header template, each as an expression.", "link": "LeanTeX.setLatexCommand"},
    {"text": "Lines 36–44: build and elaborate the definition of the given name as a LeanTeXConfig of those six parts.", "link": "LeanTeXConfig"},
 ]))


node("beamerPreamble",
 "The default document header",
 "Unless you supply a template, every deck starts as a 16:9 Beamer document with xcolor's named colours and TikZ loaded, followed by your packages and preamble, and ends with \\end{document}.",
 r"""## Plain English

**Definitions (`beamerPreamble` and `beamerPostamble`, GenerateSlidesLib.lean lines 9–11).** The header is:

- the `beamer` document class with a 16:9 aspect ratio and the `usenames`, `dvipsnames` and `svgnames` colour
  options;
- `\usepackage{tikz}`;
- the package lines ([#usepackage](#/node/LeanTeX.addPackage));
- the preamble text ([#latex_preamble](#/node/LeanTeX.getPreambleStr));
- `\begin{document}`.

The footer is `\end{document}` plus a few comment lines that tell Emacs's AUCTeX mode the file is a LaTeX master
file. A `#latex_preamble_template` replaces the header; the footer is always used.
""",
 [q("Which aspect ratio do LeanTeX decks use by default?", ["16:9", "4:3", "A4 portrait"], 0,
    "`aspectratio=169` in GenerateSlidesLib.lean line 10."),
  q("Do you need #usepackage tikz to use the TikZ DSL?", ["No; the default header loads TikZ", "Yes"], 0,
    "Line 10 always includes \\usepackage{tikz}. With your own template you would need to load it yourself."),
 ])


node("generateSlides",
 "Headline: generateSlides, from slides to PDF",
 "At run time, generateSlides renders every slide to LaTeX, wraps it in the header and footer, writes build/slides.tex, copies static/ into build/, and runs pdflatex (or your chosen program) once with -shell-escape. This is the entry point that `lake exec GenerateSlides` ends up calling.",
 r"""## Plain English

**Definition (`generateSlides`, GenerateSlidesLib.lean lines 51–65).** It takes a [LeanTeXConfig](#/node/LeanTeXConfig)
and, as an `IO` action:

1. renders each slide with [renderSlide](#/node/renderSlide) and concatenates them, in registry order;
2. puts the header (your template, or [beamerPreamble](#/node/beamerPreamble)) in front and `beamerPostamble`
   behind;
3. prints the whole document to the terminal;
4. creates the directory `build` if needed;
5. if a directory `static` exists, copies its contents into `build` (this is the README's "static files"
   feature, used by the example project for its Beamer theme `.sty` files);
6. writes `build/slides.tex`;
7. runs the LaTeX program (default `pdflatex`) inside `build`, with your options, then `-shell-escape`, then
   `slides.tex`, and waits for it to finish.

So the README's promise that the PDF lands in `build/slides.pdf` comes from step 7: LaTeX writes its output
next to its input.

### Things worth knowing

- LaTeX runs **once**. Documents that need a second pass (for a table of contents, or cross-references) will
  show `??` until you run it again by hand.
- The exit status of LaTeX is ignored: a failed build still looks like a successful program run, apart from
  LaTeX's own log.
- `-shell-escape` is always on. It lets the LaTeX source run shell commands (needed by packages such as
  `minted`). That is fine for your own slides, but it means compiling someone else's LeanTeX deck runs whatever
  commands their LaTeX asks for.
- Copying `static/` uses the system `cp` command, so this step assumes a Unix-like system.
""",
 [q("Where is the PDF written?", ["build/slides.pdf", "slides.pdf in the project root", "static/slides.pdf"], 0,
    "LaTeX runs with working directory `build` on `slides.tex` (GenerateSlidesLib.lean line 63)."),
  q("How many times does LaTeX run?", ["Once", "Twice, to resolve references", "Until it converges"], 0,
    "One spawn and one wait, lines 63–64."),
  q("If pdflatex fails, does generateSlides report an error?",
    ["No; the exit status is discarded", "Yes, it throws"], 0,
    "Line 64 waits for the process and ignores the result."),
  q("Which flag is always passed to LaTeX?", ["-shell-escape", "-interaction=nonstopmode", "-halt-on-error"], 0,
    "Line 63 appends -shell-escape after the configured options."),
 ],
 caveats=["This is a description of the code, not a tested run. The Lean was not built for this site.",
          "Static files are copied into build/ before slides.tex is written, so a static file named slides.tex would be overwritten."],
 widgets=walk("How it works (GenerateSlidesLib.lean, lines 51–65)", [
    {"text": "Line 52: render every slide and concatenate.", "link": "renderSlide"},
    {"text": "Lines 53–54: choose the header (template or Beamer default) and assemble the document with the footer.", "link": "beamerPreamble"},
    {"text": "Lines 55–56: choose the LaTeX program (default pdflatex) and options.", "link": "LeanTeX.setLatexCommand"},
    {"text": "Line 57: print the whole .tex to standard output."},
    {"text": "Lines 58–61: make build/, and copy static/ into it with cp -R if it exists."},
    {"text": "Line 62: write build/slides.tex."},
    {"text": "Lines 63–64: run the LaTeX program in build/ with -shell-escape and wait, ignoring the exit status."},
 ]))


node("generateSlidesLean",
 "The bootstrap: how `lake exec GenerateSlides` sets itself up",
 "On first use, LeanTeX's own program writes a GenerateSlides.lean into your project (importing every lean_lib you declared), appends a matching lean_exe to your lakefile, and reruns lake exec GenerateSlides, which now runs your project's own generator.",
 r"""## Plain English

**Definition (`generateSlidesLean`, GenerateSlides.lean lines 21–33).** Given a list of library names, it
produces the text of a Lean file that:

- imports each library and LeanTeX's `GenerateSlidesLib`;
- runs [#leantex_config](#/node/elabLeanTexConfig) to define `latexConfig`;
- has a `main` that calls [generateSlides](#/node/generateSlides) with it.

**The program (`main`, GenerateSlides.lean lines 38–56)** is LeanTeX's own executable, which a user project
inherits through `require LeanTeX`. Run from your project directory it:

1. fails if there is no `lakefile.lean` (lines 39–40);
2. finds your libraries by looking for lines starting with `lean_lib` and taking the next word
   (`extractDeps`, lines 14–19);
3. writes `GenerateSlides.lean` from `generateSlidesLean`, **only if that file does not exist yet** (lines 45–46);
4. if your lakefile has no `lean_exe GenerateSlides` line (`containsLeanExeDecl`, lines 9–12), appends one,
   marked "automatically inserted by LeanTex, DO NOT MODIFY" (lines 3–7, 48–52), and launches
   `lake exec GenerateSlides` again (lines 53–56).

On later runs your project has its own `GenerateSlides` executable, so the generated program runs directly.

### What this means for users

- Your slides must be reachable from a `lean_lib` root, since those are what the generated file imports.
- Delete `GenerateSlides.lean` if you add libraries; it is not regenerated otherwise.
- The lakefile check is textual: it needs a `lakefile.lean` (not `lakefile.toml`) and recognises `lean_lib` only as the first word
  of a line.
""",
 [q("What does the bootstrap do if GenerateSlides.lean already exists?",
    ["Leaves it alone", "Overwrites it", "Deletes it"], 0,
    "GenerateSlides.lean lines 45–46 only write the file when it is missing."),
  q("How does it decide which modules to import?",
    ["It reads the lean_lib names from your lakefile.lean as text", "It asks Lake", "It imports every .lean file"], 0,
    "`extractDeps` (lines 14–19) splits the lakefile into lines and keeps the word after `lean_lib `."),
  q("Does the bootstrap support lakefile.toml?", ["No; it looks only for lakefile.lean", "Yes"], 0,
    "Lines 35, 39–40."),
 ],
 caveats=["The second `lake exec` is spawned but not waited for (lines 53–56); in practice the parent probably exits while the child is still running. Not tested.",
          "The site's scanner lists a declaration `main` at GenerateSlides.lean line 31; that line is inside the string template, not real code. The real entry point is at line 38."])


EXTRA = {
 "LeanTeX.addPackage": [
  q("How is a package with no options printed?", ["\\usepackage{name}", "\\usepackage[]{name}", "It is skipped"], 0,
    "LeanTeX/PackageRegistry.lean lines 12–13 omit the brackets when the option list is empty."),
 ],
 "LeanTeX.getPreambleStr": [
  q("What is the preamble text if there are no #latex_preamble commands?", ["The empty string", "An error", "A default \\title"], 0,
    "LeanTeX/PreambleRegistry.lean line 32."),
 ],
 "LeanTeX.setLatexCommand": [
  q("What kind of string does #latex_executable accept?", ["An ordinary Lean string, with s!-style holes", "A latex![| |] literal", "Only an identifier"], 0,
    "LeanTeX/SlideDSL.lean line 397 uses Lean's `interpolatedStr(term)`, the same syntax as `s!`."),
 ],
 "LeanTeXConfig": [
  q("What is the type of the optional header field?", ["A function from package text and preamble text to the header text", "A file path", "A Slide"], 0,
    "GenerateSlidesLib.lean line 21."),
  q("Does LeanTeXConfig record the order of slides?", ["Yes: slides is a list, in registry order", "No"], 0,
    "GenerateSlidesLib.lean line 14; generateSlides folds over the list in order (line 52)."),
 ],
 "beamerPreamble": [
  q("What does beamerPostamble contain besides \\end{document}?", ["Emacs AUCTeX local-variable comments", "A bibliography", "Nothing"], 0,
    "GenerateSlidesLib.lean line 11."),
 ],
}
for n in NODES: n["quiz"] += EXTRA.get(n["id"], [])
