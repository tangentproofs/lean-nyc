NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}


node("Slide",
 "Slide: one frame, or raw LaTeX",
 "Everything the DSL builds ends up as a Slide, which is either a Beamer frame (options, optional title, list of contents) or a raw piece of LaTeX inserted between frames.",
 r"""## Plain English

**Data type (`Slide`, LeanTeX/Slide.lean lines 34–37).** Two cases:

- a **basic slide**: a list of frame options (strings such as `fragile`), an optional title, and a list of
  [SlideContent](#/node/SlideContent) items. It prints as one Beamer `frame` ([renderSlide](#/node/renderSlide));
- a **raw slide**: a single string, copied into the document unchanged. `#latex_command` produces these
  ([elabItem](#/node/elabItem)), which is how you put `\section{…}` or other between-frame LaTeX into the deck.

A presentation is just the list of all `Slide` values tagged `@[presentation]`, in registration order
([the slide registry](#/node/LeanTeX.loadSlidesStx)).

Because a slide is an ordinary Lean value, you can compute slides with ordinary Lean functions: the DSL is a
convenience, not a requirement.
""",
 [q("How would you add \\section{Results} between two frames?",
    ["As a raw slide, e.g. with #latex_command", "As the title of a basic slide", "It isn't possible"], 0,
    "`#latex_command` (LeanTeX/SlideDSL.lean lines 415–422) registers a raw slide holding the text, and a raw slide is printed unchanged (LeanTeX/LatexGen.lean line 88)."),
  q("Is a slide title required?",
    ["No; the title is optional", "Yes, always"], 0,
    "The title field has type Option String (LeanTeX/Slide.lean line 35), and `slide do …` without a title is accepted (LeanTeX/SlideDSL.lean lines 333–340)."),
 ])


node("SlideContent",
 "SlideContent: what goes on a slide",
 "A slide's body is a tree of five kinds of content: an \\item, a LaTeX environment holding more content, raw text, an invisible grouping block, or a TikZ picture.",
 r"""## Plain English

**Data type (`SlideContent`, LeanTeX/Slide.lean lines 25–31).** The cases are:

- **item**: one `\item` with its text;
- **environment**: optional options, an environment name (`itemize`, `columns`, …) and nested contents;
- **text**: a raw string;
- **block**: a list of contents grouped together. `with steps` produces one; it prints as its contents between
  two LaTeX comment lines, so it has no visible effect;
- **tikzpicture**: a [TikZ context](#/node/TikzPictureContext) and a list of [TikZ commands](#/node/TikzCommand).

[elabItem](#/node/elabItem) builds these from the slide DSL, and [renderContent](#/node/renderContent) prints them.
Since the DSL accepts any Lean term of this type as a slide item, you can write your own functions that return
`SlideContent` and call them inside a slide; the example project does this with `SlideContent.text`.
""",
 [q("What does a block print as?",
    ["Its contents, wrapped in two LaTeX comment lines", "A Beamer block environment", "A TikZ scope"], 0,
    "LeanTeX/LatexGen.lean lines 69–71 print `%start_block`, the contents and `%end_block`. Despite the name it is not Beamer's `block` environment."),
  q("Can you use your own Lean function returning SlideContent inside a slide?",
    ["Yes: any term of that type is a valid slide item", "No: only the built-in forms are allowed"], 0,
    "LeanTeX/SlideDSL.lean line 247 makes any term a slide item, and lines 319–320 use it as is."),
 ],
 caveats=["A Beamer `block` environment is written with \\begin{block} … \\end{block}, which is an environment, not this block case."])


node("TikzCommand",
 "TikzCommand: one line of a TikZ picture",
 "A TikZ picture is a list of commands of six kinds (raw text, node, draw, path-let node, layer, and group), each carrying optional Beamer overlay ranges and style options as strings.",
 r"""## Plain English

**Data type (`TikzCommand`, LeanTeX/Slide.lean lines 16–23).**

- **text**: a raw line;
- **node**: overlay ranges ([LatexInterval](#/node/LatexInterval)), styles, optional position, optional name,
  and body text;
- **draw**: ranges, styles and the path to draw;
- **path-let node**: like a node, but preceded by TikZ's `\path let \p1 = …, \p2 = … in`, which measures
  points first; the bindings are the points to measure;
- **layer**: a named `pgfonlayer` holding more commands;
- **block**: a list of commands with no wrapper (what a `for` loop produces).

[elabTikzItem](#/node/elabTikzItem) builds them and [renderTikzCommand](#/node/renderTikzCommand) prints them.
Everything except the ranges is a plain string: LeanTeX does not model TikZ coordinates or styles, it only
assembles the text.
""",
 [q("Does LeanTeX check TikZ coordinates or style names?",
    ["No; they are plain strings passed through to TikZ", "Yes, against a list of TikZ keys"], 0,
    "Positions, styles and bodies are all `String` (LeanTeX/Slide.lean lines 18–20)."),
  q("Which case does a for loop in the TikZ DSL produce?",
    ["block", "layer", "pathLetNode"], 0,
    "LeanTeX/SlideDSL.lean lines 169–175 wrap the collected commands in `TikzCommand.block`."),
 ])


node("LatexInterval",
 "LatexInterval: a Beamer overlay range",
 "Beamer shows parts of a slide only on certain steps; a LatexInterval is one such range (exactly n, from a to b, from a on, or up to b), and it prints as n, a-b, a- or -b.",
 r"""## Plain English

**Data type (`LatexInterval`, LeanTeX/Slide.lean lines 9–14).** Four cases, all natural numbers:

| Case | Meaning | Printed |
|---|---|---|
| at *n* | only on step *n* | `n` |
| between *a* *b* | steps *a* to *b* | `a-b` |
| after *a* | step *a* onwards | `a-` |
| upto *b* | up to step *b* | `-b` |

`renderLatexInterval` (LeanTeX/LatexGen.lean lines 8–12) does the printing; a list of ranges is joined with commas
and wrapped in angle brackets, giving Beamer's `<1,3->` syntax. In the TikZ DSL you write the numbers as names
bound by `with steps` ([elabTikzItem](#/node/elabTikzItem)).
""",
 [q("How is `after 2` printed?", ["2-", "-2", "2"], 0, "LeanTeX/LatexGen.lean line 11 prints the start followed by a dash."),
  q("What does Beamer's <-3> mean?", ["Shown on steps 1 to 3", "Shown from step 3 on", "Hidden on step 3"], 0,
    "A leading dash means 'up to'; this is the `upto 3` case."),
 ])


node("TikzPictureContext",
 "TikzPictureContext: options for a whole picture",
 "The options of a tikzpicture: a map of named styles and a list of other options, printed comma-separated inside the picture's square brackets. In practice only the list is ever filled.",
 r"""## Plain English

**Structure (`TikzPictureContext`, LeanTeX/Slide.lean lines 4–7).** Two fields: a hash map from style names to
style definitions, and a list of miscellaneous option strings. `renderTikzPictureContext`
(LeanTeX/LatexGen.lean lines 3–6) prints the list entries followed by each style as `name/.style={…}`, all
separated by commas.

The DSL always builds the context with an **empty** style map and puts the `tikz [opts]` options into the list
(LeanTeX/SlideDSL.lean lines 263–278). Named styles are therefore only reachable from hand-written Lean, and the
upstream todo list still has "Setup tikzpicture with a scoped context" open.
""",
 [q("When you write tikz [thick] do …, where does `thick` go?",
    ["Into the misc list", "Into the styles map", "Nowhere"], 0,
    "LeanTeX/SlideDSL.lean lines 268–271 put the expanded options in the second (list) argument."),
 ],
 caveats=["Printing a hash map goes in the map's internal order, so if you did fill in several styles their order in the output is not the order you inserted them."])


node("renderSlide",
 "renderSlide: printing a frame",
 "A basic slide prints as \\begin{frame}[options]{title} … \\end{frame}, a raw slide prints as its text: this is the whole LaTeX back end for a slide.",
 r"""## Plain English

**Definition (`renderSlide`, LeanTeX/LatexGen.lean lines 78–88).** For a basic [Slide](#/node/Slide):

1. options, if any, are joined with commas in square brackets;
2. the title, if any, is put in braces;
3. the contents are printed by [renderContent](#/node/renderContent);
4. the result is wrapped in `\begin{frame}` … `\end{frame}`.

A raw slide is returned as is. [generateSlides](#/node/generateSlides) concatenates the rendered slides in order.

The renderer is pure string building, with no escaping: whatever text you put in a title or item reaches LaTeX
exactly as written.
""",
 [q("Where do the options of `#latex_slide [fragile] \"T\" do …` end up?",
    ["\\begin{frame}[fragile]{T}", "\\begin{document}[fragile]", "In the preamble"], 0,
    "LeanTeX/LatexGen.lean lines 81–87."),
 ])


node("renderContent",
 "renderContent: printing slide contents",
 "Slide contents are printed recursively, one LaTeX line per item, with environments as \\begin … \\end around their contents and TikZ pictures as tikzpicture environments.",
 r"""## Plain English

**Definition (`renderContent`, LeanTeX/LatexGen.lean lines 55–76).** It walks the list of
[SlideContent](#/node/SlideContent):

- an item prints as `\item` and its text;
- an environment prints its begin line, its contents (recursively) and its end line;
- text prints as itself;
- a block prints its contents between `%start_block` and `%end_block` comment lines;
- a TikZ picture prints `\begin{tikzpicture}[…]`, its commands one per line via
  [renderTikzCommand](#/node/renderTikzCommand), and `\end{tikzpicture}`.

### A suspected bug in the options form

When an environment has options, line 63 builds the begin line as `\begin`, then the options in square brackets,
then the environment name in braces. Standard LaTeX syntax puts the name first: `\begin{columns}[T]`. By this
site's reading, `latex_env! [opts] columns do …` therefore produces `\begin[T]{columns}`, which LaTeX would
reject. The plain `\begin{…}` form and `latex_env!` without options are not affected. The project was not built
or run for this site, so this is unconfirmed.
""",
 [q("For an environment with options [T] named columns, what does line 63 print, by this site's reading?",
    ["\\begin[T]{columns}", "\\begin{columns}[T]", "\\columns[T]"], 0,
    "The format string puts the options tag between \\begin and the braced name. Standard LaTeX expects \\begin{columns}[T]; see the review page."),
  q("Is the text of an \\item escaped for LaTeX?", ["No; it is printed as is", "Yes"], 0, "LeanTeX/LatexGen.lean line 58 prints the text unchanged after \\item."),
 ],
 caveats=["The options-order issue is this site's reading of the format string at LeanTeX/LatexGen.lean line 63, not a tested result."])


node("renderTikzCommand",
 "renderTikzCommand: printing TikZ",
 "Each TikZ command prints as one TikZ statement ending in a semicolon, with the overlay range in angle brackets and styles in square brackets, exactly in TikZ's own order.",
 r"""## Plain English

**Definition (`renderTikzCommand`, LeanTeX/LatexGen.lean lines 17–53).** Case by case for
[TikzCommand](#/node/TikzCommand):

- **node**: `\node`, then `<ranges>` if any, `[styles]` if any, ` (name) ` if any, ` at pos` if any, and the
  body in braces;
- **draw**: `\draw<ranges>[styles] body;`
- **path-let node**: `\path let \p1 = …, \p2 = … in node …`, numbering the bindings from 1 in order;
- **text**: the text;
- **layer**: `pgfonlayer` begin and end lines around the inner commands;
- **block**: the inner commands, one per line.

Ranges come from [LatexInterval](#/node/LatexInterval).
""",
 [q("In which order are the bindings of a path-let node numbered?",
    ["Left to right, from \\p1", "Right to left", "They aren't numbered"], 0,
    "LeanTeX/LatexGen.lean line 19 numbers them by position plus one. Compare the caveat on elabTikzItem about the binding names."),
 ])


EXTRA = {
 "Slide": [
  q("Must slides be written with the DSL?",
    ["No; a Slide is an ordinary Lean value, so any function can build one", "Yes; only the DSL can make slides"], 0,
    "`Slide` is a plain inductive type (LeanTeX/Slide.lean lines 34–37), and `#latex_slide_expr` registers any term of that type (LeanTeX/SlideDSL.lean lines 425–428)."),
 ],
 "SlideContent": [
  q("Which case does `\\item{\"Hello\"}` produce?", ["item", "text", "environment"], 0,
    "LeanTeX/SlideDSL.lean line 296 builds `SlideContent.item`."),
 ],
 "TikzCommand": [
  q("Which case prints as a pgfonlayer environment?", ["layer", "block", "draw"], 0,
    "LeanTeX/LatexGen.lean lines 48–51."),
 ],
 "LatexInterval": [
  q("What are the endpoints of a LatexInterval?", ["Natural numbers (step numbers)", "Strings", "Real numbers"], 0,
    "Every constructor takes `Nat` arguments (LeanTeX/Slide.lean lines 10–13)."),
 ],
 "TikzPictureContext": [
  q("How would a style entry `big` ↦ `scale=2` be printed?", ["big/.style={scale=2}", "big=scale=2", "\\tikzset{big}"], 0,
    "LeanTeX/LatexGen.lean line 6 formats each map entry with `/.style=`."),
  q("Can the slide DSL put anything into the styles map?", ["No; it always starts empty", "Yes, via tikz [style …]"], 0,
    "LeanTeX/SlideDSL.lean lines 270 and 277 both pass an empty map."),
 ],
 "renderSlide": [
  q("What does a raw slide render to?", ["Its string, unchanged", "A frame containing the string", "Nothing"], 0,
    "LeanTeX/LatexGen.lean line 88."),
  q("A slide with no title and no options renders as…", ["\\begin{frame} … \\end{frame} with nothing after \\begin{frame}", "An error", "A raw slide"], 0,
    "Empty options and a missing title both print as the empty string (LeanTeX/LatexGen.lean lines 81–86)."),
 ],
 "renderContent": [
  q("How is a TikZ picture's command list printed?", ["One command per line, via renderTikzCommand", "All on one line", "As a \\foreach"], 0,
    "LeanTeX/LatexGen.lean lines 72–76 join the rendered commands with newlines."),
 ],
 "renderTikzCommand": [
  q("What ends every node and draw statement?", ["A semicolon, as TikZ requires", "A newline only", "\\par"], 0,
    "LeanTeX/LatexGen.lean lines 28, 39 and 47 all end with `;`."),
  q("Where does an overlay range go in a node?", ["Right after \\node, in angle brackets", "At the end", "In the style list"], 0,
    "LeanTeX/LatexGen.lean line 39: the range string comes directly after \\node."),
 ],
}
for n in NODES: n["quiz"] += EXTRA.get(n["id"], [])
