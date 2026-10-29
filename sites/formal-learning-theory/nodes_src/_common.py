NOT_BUILT = ("Not built for this site: \"proved\" means the source contains a complete-looking proof, and a text "
             "search finds no `sorry`, `admit` or `axiom` in the compiled library (FLT_Proofs/). Lean's kernel was not "
             "run here. The upstream README reports CI runs of `lake build`, `#print axioms`, lean4checker and "
             "Comparator; those were not repeated for this site.")

MEAS = ("CONDITIONAL on `[MeasurableConceptClass X C]`. Its field `all_measurable` asks that **every** Bool-valued "
        "function on X be measurable, i.e. every subset of X is an event (Complexity/Measurability.lean lines 60–67). "
        "That holds for countable X with the discrete σ-algebra (or any X with the σ-algebra of all subsets), but "
        "**not** for ℝ or ℝⁿ with the Borel σ-algebra, so the textbook examples of thresholds and half-spaces on ℝⁿ "
        "under Borel distributions are not covered as stated. The field `wellBehaved` (the WellBehavedVC null-"
        "measurability condition) is a further real assumption. The file's own docstring says this (Complexity/Measurability.lean lines 113–140).")

NODES = []  # this helper file defines no nodes (the engine loads every .py here)


def node_maker(nodes):
    def node(id, title, summary, body, quiz, caveats=(), widgets=None):
        nodes.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz,
                          caveats=list(caveats), widgets=widgets))
    return node


def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}


def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]


def S(text, link=None, lean=None):
    d = {"text": text}
    if link: d["link"] = link
    if lean: d["lean"] = lean
    return d
