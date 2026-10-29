NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]


# ---------------------------------------------------------------- headline: the LaTeX literal

node("interpolatedLatexFn",
 "Headline: the latex![| … |] literal, raw LaTeX with Lean holes",
 "LeanTeX adds a new kind of string to Lean: text between [| and |] is copied to the output exactly as typed, backslashes and all, and you open a hole back into Lean with a nested [| … |] or with @{ … }. This hand-written parser is what lets you paste ordinary LaTeX into a Lean file.",
 r"""## Plain English

This is not a theorem. LeanTeX is a tool for writing **Beamer slide decks in Lean**, and this function is the
piece that makes the rest pleasant to use.

**Parser (`interpolatedLatexFn`, LeanTeX/LatexLiteral.lean lines 33–107).** It reads a *LaTeX literal* from
the source file:

- it must start with the two characters `[|`;
- everything after that is **raw text**: no escape sequences, so a backslash is just a backslash, and you can
  write `\begin{itemize}` exactly as you would in a `.tex` file (in an ordinary Lean string you would have to
  double every backslash);
- a nested `[|` opens a **Lean term**, which runs until the matching `|]`. The term's value is turned into text
  and spliced in. That is how the README's example puts the result of a Lean function such as `fontsize` inside
  a LaTeX `\author{…}`;
- `@{` also opens a Lean term, closed by `}`. This short form suits places where `[| |]` would clash with the
  LaTeX, such as a Beamer overlay specification `<@{step1}->`;
- an unnested `|]` ends the literal.

You never call this function yourself. It is wrapped as a Lean parser
(`interpolatedLatexParser`, lines 110–112) and plugged into the grammar after the keyword `latex!` inside slides
([elabItem](#/node/elabItem)), and after the commands `#latex_preamble` and `#latex_command`
([preamble snippets](#/node/LeanTeX.getPreambleStr)).

### How it reuses Lean's own string interpolation

The parser builds exactly the same syntax tree that Lean's built-in `s!"…{x}…"` strings produce
(an *interpolated string*): alternating text chunks and terms. Lean's syntax for those is reused, only the
reading of the characters is new. Turning that tree into a Lean expression is the job of
[expandInterpolatedLatex](#/node/expandInterpolatedLatex).

### How a user meets it

In a slide you write the keyword `latex!` followed by a literal containing, say, a whole `tikzpicture`. In the
preamble you write `#latex_preamble` followed by a literal containing `\title{…}` and `\author{…}`. The
README's "escape hatch" feature is this literal.
""",
 [q("Inside a latex![| … |] literal, how do you write the LaTeX command \\item?",
    ["Exactly as in LaTeX, with one backslash: the text is copied raw",
     "With a doubled backslash, as in any Lean string",
     "You can't: backslashes are forbidden"], 0,
    "The parser copies characters as they are (LeanTeX/LatexLiteral.lean lines 98–99 just move on), and the chunk becomes a string literal with the same contents (lines 141–143). No escape processing happens."),
  q("Which of these opens a hole for a Lean term inside the literal?",
    ["Either a nested [| … |] or @{ … }", "Only {x}, as in s!\"…\"", "Only $x"], 0,
    "Lines 58–79 handle a nested `[|`, which runs Lean's term parser and expects `|]` after it. Lines 80–97 handle `@{`, which expects `}`."),
  q("Is interpolatedLatexFn a theorem about LaTeX?",
    ["No. It is a parser: code that runs when Lean reads your file",
     "Yes. It proves the generated LaTeX compiles"], 0,
    "It has type `ParserFn`. LeanTeX contains no theorems at all; it is a metaprogramming library."),
  q("What can't you write literally inside a LaTeX literal?",
    ["The two-character sequences [| and |], and @ followed by {",
     "Curly braces", "Percent signs"], 0,
    "`[|` always opens a hole (line 61), `|]` always ends the literal (line 53), and `@{` always opens a hole (line 83). There is no escape for them. Braces and `%` on their own are fine."),
 ],
 caveats=["This is a parser, not a proved result. Nothing about it is verified: 'correct' here means only that the code reads as described.",
          "The step counter in the inner loop (line 39) is only used by commented-out debugging code (lines 41–43)."],
 widgets=walk("How the parser works (LeanTeX/LatexLiteral.lean, lines 33–107)", [
    {"text": "Lines 100–107: remember where the literal starts, insist on the opening [| (the helper leanTexStart, lines 18–28), then start the scanning loop."},
    {"text": "Lines 44–46: running off the end of the file is an 'unterminated latex literal' error."},
    {"text": "Lines 50–57: on |], close the current text chunk and finish the whole literal as an interpolated-string node. A | followed by anything else is ordinary text."},
    {"text": "Lines 58–79: on a nested [|, close the current text chunk, run Lean's ordinary term parser, then demand |]. Scanning resumes with a fresh chunk."},
    {"text": "Lines 80–97: on @{, the same, but the text chunk is cut just before the @ and the term must be followed by }."},
    {"text": "Lines 98–99: any other character is plain text; keep scanning."},
    {"text": "Lines 110–119: wrap the function as a Lean parser that produces the same node kind as s!\"…\" strings, with empty pretty-printer hooks.", "link": "expandInterpolatedLatex"},
 ]))


node("expandInterpolatedLatex",
 "Turning a LaTeX literal into a String",
 "After parsing, a LaTeX literal is a list of raw text chunks and Lean terms; this macro helper glues them into one Lean expression of type String, converting every piece with toString and joining with ++.",
 r"""## Plain English

**Definition (`expandInterpolatedLatex`, LeanTeX/LatexLiteral.lean lines 151–154).** Given the syntax produced by
[the literal parser](#/node/interpolatedLatexFn), a target type and a conversion function, it produces a Lean
term. LeanTeX always calls it with target type `String` and conversion `toString`.

The work happens in `expandInterpolatedLatexChunks` (lines 137–149):

1. Walk over the chunks in order.
2. A raw text chunk still carries its delimiters (`[|`, `|]`), because the parser recorded the source text
   verbatim. `decodeInterpLatexLit` (lines 121–130) strips one leading and one trailing delimiter, and the result
   becomes an ordinary string literal.
3. A Lean term is left alone.
4. Each piece is wrapped in the conversion function, and the pieces are joined left to right with `++`.

The result is ascribed the target type (line 154). So a literal such as "text, then the term *x*, then more
text" becomes, in effect, the string `toString "text" ++ toString x ++ toString "more"`.

Because the holes go through `toString`, you can splice in anything that has a `ToString` instance: numbers
(which is how [named animation steps](#/node/elabItem) become overlay numbers), strings returned by your own
helper functions, and so on.
""",
 [q("What type does a latex!-literal have after expansion, everywhere LeanTeX uses it?",
    ["String", "Slide", "Syntax", "TikzCommand"], 0,
    "Every call site passes the type `String` and the function `toString` (for example LeanTeX/SlideDSL.lean line 294 and line 371)."),
  q("Why can you splice a natural number into a literal?",
    ["Every hole is passed through toString, and Nat has a ToString instance",
     "Lean coerces every type to String automatically", "You can't; holes must be strings"], 0,
    "Line 142 wraps every term in the conversion function, which is `toString` at every call site."),
  q("What does decodeInterpLatexLit do?",
    ["Strips the [| / |] delimiters left on a raw text chunk", "Escapes LaTeX special characters",
     "Checks that the LaTeX is well formed"], 0,
    "LeanTeX/LatexLiteral.lean lines 121–130: it tries to drop a `[|` or `|]` prefix and suffix. No LaTeX checking happens anywhere in LeanTeX."),
 ],
 caveats=["decodeInterpLatexLit is marked partial although it does not recurse; that has no effect on behaviour.",
          "Text is never escaped for LaTeX: a spliced string containing % or { goes into the .tex file as is. That is the intended 'escape hatch' behaviour, but it means LeanTeX gives no protection against malformed LaTeX."])


# ---------------------------------------------------------------- headline: the slide DSL

node("elabItem",
 "Headline: the slide DSL (slide … do, #latex_slide, \\begin…\\end, with steps)",
 "A LeanTeX slide is written as a do-block whose lines look like LaTeX (\\begin{itemize}, \\item{…}) but are Lean syntax; elabItem translates each line into a SlideContent value, and you can drop to a raw latex! literal or any Lean expression at any point.",
 r"""## Plain English

This is the heart of the user-facing DSL. It is code, not a theorem.

**Elaborator (`elabItem`, LeanTeX/SlideDSL.lean lines 262–321).** LeanTeX declares a new syntax category of
*slide items* (line 10) and gives it these forms (lines 19–26, 243–247):

| You write | It becomes ([SlideContent](#/node/SlideContent)) | Lines |
|---|---|---|
| `\begin{env}` … items … `\end{env}` | an environment named `env` holding the inner items; the two names must match | 297–302 |
| `latex_env!` *env* `do` … items | the same, written as an indented block | 304–310 |
| `latex_env! [opts]` *env* `do` … | an environment with [options](#/node/expandLatexOption) | 311–318 |
| `\item{` *term* `}` | an `\item`; the braces hold a Lean string | 296 |
| `latex!` + a [LaTeX literal](#/node/interpolatedLatexFn) | raw text | 293–295 |
| `tikz do` … | a TikZ picture built from the [TikZ DSL](#/node/elabTikzItem) | 263–278 |
| `with steps [a, b, c] do` … | the inner items, with `a`, `b`, `c` bound to 1, 2, 3 | 279–292 |
| any Lean term | that term, which must itself be a `SlideContent` | 319–320 |

Note what `\begin{itemize}` is here: Lean keywords `\begin` and `\end` (line 20), not text. LeanTeX can therefore
check at compile time that the begin and end names match (line 298–299), which LaTeX itself would only report
when you run it.

### Named animation steps

Beamer reveals things in numbered steps (`<2->` means "from step 2 on"). `with steps [first, second] do …`
simply puts `let first := 1` and `let second := 2` around the block (lines 285–292), so you can write
`<@{second}->` inside a literal and reorder steps by reordering the list. A term-level version does the same for a
single expression (lines 249–260).

### Where items go: slides

Items are used in two places:

- the **term** `slide "Title" do …` (lines 17, 323–340) builds a value of type [Slide](#/node/Slide); you put it in a
  `def` and tag it `@[presentation]` to include it in the deck ([slide registry](#/node/LeanTeX.loadSlidesStx));
- the **command** `#latex_slide [opts] "Title" do …` (lines 411, 424–471) does both at once: it builds the slide,
  invents a fresh name for it, and declares it with `@[presentation]`. The options become frame options such as
  `fragile`; the title is optional.

There are also `#latex_slide_expr` (register any `Slide` value, lines 425–428) and `#latex_command` (register a
raw LaTeX literal as a "slide", for things like `\section{…}` between frames, lines 415–422).
""",
 [q("In a LeanTeX slide, what is \\begin{itemize}?",
    ["Lean syntax that LeanTeX turns into an environment value", "Raw text copied into the .tex file",
     "A comment"], 0,
    "`\\begin` and `\\end` are keywords of the slide_item grammar (LeanTeX/SlideDSL.lean lines 19–21), handled at lines 297–302. Raw text needs `latex!`."),
  q("What does `with steps [s1, s2] do …` bind s1 and s2 to?",
    ["The numbers 1 and 2", "The strings \"s1\" and \"s2\"", "Two fresh slides"], 0,
    "Lines 285–292: each name is bound with `let` to its position plus one."),
  q("What does #latex_slide do that the slide … term does not?",
    ["It also declares the slide under a fresh name tagged @[presentation], so it is included automatically",
     "It checks that the slide fits on the page", "It compiles the slide to PDF immediately"], 0,
    "Lines 429–471 elaborate the body like `slide` and then emit a `@[presentation] def` with a fresh name. With the `slide` term you write the def and the attribute yourself, as the example project does."),
  q("What happens if you write \\begin{itemize} … \\end{enumerate}?",
    ["Lean reports a 'mismatched tags' error when it reads the file", "pdflatex reports it later",
     "Nothing; LaTeX accepts it"], 0,
    "Lines 298–299 compare the two names and throw an error at elaboration time."),
  q("Does LeanTeX prove anything about the slides it builds?",
    ["No. It has no theorems; it is a code generator", "Yes, that every slide renders"], 0,
    "A text search finds no `theorem` or `lemma` in the repository. Everything is definitions, syntax and elaborators."),
 ],
 caveats=["No theorems are involved; this is a description of what the elaborator does, read from the source without running it.",
          "The table lists the forms as the grammar declares them. The DSL was not tried out for this site, so whitespace and indentation subtleties (the `colGt`/`colEq` position checks) are not described.",
          "With options, `latex_env!` renders as \\begin[opts]{env} (LeanTeX/LatexGen.lean lines 60–63). Standard LaTeX expects \\begin{env}[opts], so by this site's reading the options form may produce invalid LaTeX; see the review page."],
 widgets=walk("How the elaborator works (LeanTeX/SlideDSL.lean, lines 262–340)", [
    {"text": "Lines 263–278: a tikz block. Each TikZ line is translated by elabTikzItem; the options, if any, go into the picture's context.", "link": "elabTikzItem"},
    {"text": "Lines 279–292: with steps. Translate the inner items recursively, wrap them in one block, then bind each step name to its number.", "link": "SlideContent"},
    {"text": "Lines 293–295: latex! text. Expand the literal to a String and wrap it as text content.", "link": "expandInterpolatedLatex"},
    {"text": "Line 296: \\item{t} becomes an item holding t."},
    {"text": "Lines 297–318: environments, in the \\begin/\\end form (with the name check) and the latex_env! form (optionally with options).", "link": "expandLatexOption"},
    {"text": "Lines 319–320: anything else is taken to be a Lean term of type SlideContent and used as is."},
    {"text": "Lines 323–340: the slide term elaborates every item and builds a basic slide, with or without a title.", "link": "Slide"},
    {"text": "Lines 414–471: the #latex_slide commands do the same and then declare the result with @[presentation] under a fresh name.", "link": "LeanTeX.loadSlidesStx"},
 ]))


node("expandLatexOption",
 "Options in square brackets",
 "Wherever LeanTeX accepts [options] (frames, environments, TikZ pictures and commands) you can write a bare name, name = value, a string, a latex! or s! literal, or {any Lean term}; each one becomes a String at run time.",
 r"""## Plain English

**Definition (`expandLatexOption`, LeanTeX/SlideDSL.lean lines 46–61).** The option grammar (lines 28–33) has six
forms, each turned into a Lean `String` expression:

- a bare identifier such as `fragile` becomes the text `fragile`;
- `name = term` becomes the name, an equals sign, and the term (which must itself be a string);
- a `latex!` literal ([see here](#/node/expandInterpolatedLatex)) or an `s!"…"` string is expanded;
- a plain string literal is used as is;
- `{ term }` converts any Lean value with `toString`.

The options are joined with commas when the LaTeX is printed ([renderSlide](#/node/renderSlide)).

### The compile-time variant

`#usepackage` options are handled by a stricter sibling, `expandLatexOptionStr` (lines 35–43), which accepts only
the literal forms (a name, `name = "string"`, or a string). Packages are recorded while Lean reads your file
([the package registry](#/node/LeanTeX.addPackage)), so their options have to be known at that moment, not
computed later.
""",
 [q("What does the option `fragile` (a bare name) become?",
    ["The text fragile", "The value of a Lean variable called fragile", "An error"], 0,
    "Line 47–50: an identifier is turned into a string literal of its own name. To use a Lean variable, write `{fragile}`."),
  q("Why does #usepackage accept fewer option forms than a slide?",
    ["Package options are recorded while the file is being read, so they must be literal",
     "LaTeX packages take no options", "It is an oversight with no reason"], 0,
    "`expandLatexOptionStr` (lines 35–43) returns a plain String during elaboration and rejects other forms with an error, because `LeanTeX.addPackage` stores the options in the environment immediately."),
  q("How do you pass a computed value as an option?",
    ["Wrap the Lean expression in braces: {e}", "Write it bare", "It isn't possible"], 0,
    "Line 60: `{ t }` becomes `ToString.toString t`."),
 ])


node("elabTikzItem",
 "Headline: the TikZ mini-language (node, draw, with coordinates, on layer, for)",
 "Inside a tikz do block, LeanTeX offers a small structured language for TikZ pictures, with Beamer overlay ranges written as named steps and real Lean for-loops that generate repeated nodes; elabTikzItem turns each line into a TikzCommand value.",
 r"""## Plain English

**Elaborator (`elabTikzItem`, LeanTeX/SlideDSL.lean lines 145–240).** A `tikz do` block in a slide
([elabItem](#/node/elabItem)) contains lines of these forms (grammar at lines 105–110):

| You write | It becomes ([TikzCommand](#/node/TikzCommand)) | Rendered as |
|---|---|---|
| `node` ⟨range⟩ [opts] name `at` pos body | a node | `\node<…>[…] (name) at pos {body};` |
| `draw` ⟨range⟩ [opts] body | a draw command | `\draw<…>[…] body;` |
| `with coordinates (x, y) := "a", … in node …` | a `\path let` node | `\path let \p1 = a, … in node …` |
| `on layer` L `do` … | a layer block | `pgfonlayer` environment |
| `for` *i* `in` *list* `do` … | a block of commands built by a Lean loop | the commands, one per line |

Every part in angle brackets or square brackets is optional.

### Ranges are named steps

The ⟨range⟩ is a Beamer overlay specification written with identifiers, not numbers: `<a>`, `<a-b>`, `<a->`,
`<-b>`, or a comma-separated list (lines 63–68, 70–75, 113–121). The identifiers are ordinary Lean variables,
normally bound by `with steps` ([elabItem](#/node/elabItem)), so the steps are numbered for you. They become
[LatexInterval](#/node/LatexInterval) values.

### Positions and bodies

`at (e1, e2)` prints the pair, `at (e)` or `at x` prints a Lean value, and `at "…"` uses the string as is
(lines 77–87). A body is a `latex!` literal or any Lean term, converted with `toString` (lines 90–99).

### Coordinates

`with coordinates (x, y) := "(n1)" in node …` uses TikZ's `\path let` to measure a point. In Lean, `x` and `y`
are bound to the TikZ macro names `\x1` and `\y1` (`\x2`, `\y2` for the second binding, and so on), so you can use
them inside the node's position or body (lines 123–142, 188–216).

### Loops

`for i in list do …` (lines 154–175) generates Lean code that runs the loop, collects one command per iteration
and wraps them in a block. This is Lean's own `for`, so the loop runs when the presentation program runs, not
inside TeX.
""",
 [q("In `draw <a-> body`, what is `a`?",
    ["A Lean variable holding a step number, usually bound by with steps", "The letter a, printed literally",
     "A TikZ coordinate"], 0,
    "`expandInterval` (LeanTeX/SlideDSL.lean lines 70–75) passes the identifier to a LatexInterval constructor that takes a Nat, so it must name a number."),
  q("Where does a `for` loop inside a tikz block run?",
    ["In Lean, when the slide-generating program runs; it produces one command per iteration",
     "In TeX, as a \\foreach loop", "At parse time, unrolled by the macro"], 0,
    "Lines 154–175 build an `Id.run do` block with a real Lean `for` that collects commands into a list."),
  q("With `with coordinates (x, y) := \"(a)\" in node …`, what does x stand for in Lean?",
    ["The string \\x1, TikZ's name for the x-component of the first measured point",
     "The numeric x-coordinate of (a)", "Nothing; x is unused"], 0,
    "`elabTikzCoordinateBindingFold` (lines 131–142) binds the pair to the strings `\\x{n}` and `\\y{n}`. TikZ does the measuring."),
 ],
 caveats=["By this site's reading, the coordinate numbering differs between the two `with coordinates` forms: with options the bindings are numbered left to right (foldlM, line 201), without options right to left (foldrM, line 215), while the printed \\p1, \\p2 … always go left to right (LeanTeX/LatexGen.lean line 19). With two or more bindings and no options, x and y could therefore refer to the wrong point. This was not tested.",
          "There is no way to write a plain TikZ text command from this grammar; the TikzCommand.text constructor is reachable only from Lean code.",
          "The `styles` map of a TikZ picture is always created empty (lines 270, 277); only the option list is used. The todo file lists 'tikzpicture with a scoped context' as unfinished."],
 widgets=walk("How the TikZ elaborator works (LeanTeX/SlideDSL.lean, lines 145–240)", [
    {"text": "Lines 146–153: on layer L — translate the inner lines recursively, wrap them as a layer named L.", "link": "TikzCommand"},
    {"text": "Lines 154–175: for — translate the body lines, then generate an Id.run do block that loops, prepends each result to a fresh list variable, and finally reverses it into a block."},
    {"text": "Lines 177–186: draw, with and without options. Range via expandIntervalSpec, options via expandLatexOption, body via expandTikzBody.", "link": "LatexInterval"},
    {"text": "Lines 188–216: with coordinates … in node. Build the path-let node, then wrap it in one let per binding that names x and y as \\x{n} and \\y{n}."},
    {"text": "Lines 217–239: node, with and without options; optional name and position become Option values.", "link": "renderTikzCommand"},
    {"text": "Line 240: anything else is an 'Illegal Tikz Item form' error."},
 ]))
