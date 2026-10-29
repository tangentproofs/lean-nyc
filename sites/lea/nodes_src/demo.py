NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

GH = "https://github.com/VIDA-NYU/Lea/blob/a5924f6f15b980452731b6edfe00feee97791ab4/"
REF = GH + "docs/lea-overleaf-demo/reference/reference-proofs.lean"
TEX = GH + "docs/lea-overleaf-demo/overleaf/sections/02-source-review.tex"

node("LeaDemoReference.original_square_claim_is_false",
 "Demo: a false claim in a LaTeX paper, and its disproof",
 "The Overleaf demo plants a false theorem in a LaTeX document ('every real number is at most its square'). The reference Lean file disproves it at x = 1/2 and proves the corrected version for x ≥ 1. It shows the workflow Lea is built for: formalizing a paper's claims can expose a wrong one.",
 r"""## Plain English

**Theorem (`original_square_claim_is_false`, [reference-proofs.lean lines 44–47](""" + REF + r"""#L44-L47)).**
It is **not** true that *x* ≤ *x*² for every real number *x*.

**Proof idea.** Suppose it were. Take *x* = 1/2: then 1/2 ≤ 1/4, which is false. Lean's `norm_num` does the
arithmetic.

### The story around it

The Overleaf demo kit contains a short LaTeX document. One of its theorems, "Square versus the original number"
([02-source-review.tex lines 8–19](""" + TEX + r"""#L8-L19)), claims *x*² ≥ *x* for every real *x*, with a "proof"
that wrongly says both *x* and *x* − 1 are nonnegative. The kit's README says the claim is false on purpose,
and the fix is to assume *x* ≥ 1.

The corrected statement is [demo_square_bound](#/node/LeaDemoReference.demo_square_bound).

### What this file is (and isn't)

The file's header (lines 3–8) says it holds **rehearsal proofs**, checked locally by the demo's author and
"independent of Lea's generated paths". It is not a record of Lea's output. It lets a presenter know in advance
what a correct formalization looks like. The file ends with `#print axioms` for every result (lines 86–98), the
standard way to confirm that nothing rests on `sorry` or an extra axiom.

(The file name starts with a lower-case letter, so this site's automatic line links don't reach it. The links
above go straight to GitHub at the pinned commit.)
""",
 [q("What does `original_square_claim_is_false` state?",
    ["Not every real number x satisfies x ≤ x²",
     "No real number satisfies x ≤ x²",
     "x ≤ x² for x ≥ 1",
     "x² ≥ 0 for every real x"], 0,
    "It negates the universal claim. That needs only one counterexample."),
  q("Which counterexample does the proof use?",
    ["x = 1/2", "x = −1", "x = 0", "x = 2"], 0,
    "reference-proofs.lean line 46. At 1/2 the square is 1/4."),
  q("Is this file Lea's own output?",
    ["No. Its header calls it rehearsal reference proofs, independent of Lea's generated files", "Yes, it is a saved Lea run"], 0,
    "reference-proofs.lean lines 3–8."),
  q("Why does the LaTeX proof fail?",
    ["It claims x and x − 1 are both nonnegative for every real x, which is false for x < 1", "It divides by zero", "It is actually correct"], 0,
    "02-source-review.tex lines 18–19 (linked above)."),
 ],
 caveats=["Not built for this site. The proof is three lines and the arithmetic is easy to check by hand, but Lean was not run.",
          "This is demo material for a recorded presentation, not a research result."])

node("LeaDemoReference.demo_square_bound",
 "Demo: the corrected claim, x ≤ x² when x ≥ 1",
 "Once the hypothesis x ≥ 1 is added, the claim becomes true: x² − x = x(x − 1) is a product of two nonnegative numbers.",
 r"""## Plain English

**Theorem (`demo_square_bound`, [reference-proofs.lean lines 39–42](""" + REF + r"""#L39-L42)).** For a real number
*x* with 1 ≤ *x*, we have *x* ≤ *x*².

**Proof idea.** From 1 ≤ *x*, get 0 ≤ *x*. Both *x* and *x* − 1 are nonnegative, so their product *x*(*x* − 1) = *x*² − *x*
is nonnegative (lines 40–41). Lean's nonlinear-arithmetic tactic finishes (line 42).

This is the corrected form of the false LaTeX theorem, disproved in
[original_square_claim_is_false](#/node/LeaDemoReference.original_square_claim_is_false). The Lean name
`demo_square_bound` matches the `% lea: formalize label=demo_square_bound` marker in the LaTeX source. That
marker is how the Overleaf extension knows which theorem block to send to Lea.
""",
 [q("What hypothesis turns the false claim into a true one?",
    ["1 ≤ x", "0 ≤ x", "x ≠ 0", "x is an integer"], 0,
    "With only 0 ≤ x, x = 1/2 is still a counterexample. The file uses 1 ≤ x."),
  q("Which product is shown to be nonnegative?",
    ["x · (x − 1)", "x · (x + 1)", "(x − 1)²"], 0, "reference-proofs.lean line 41."),
  q("How does the LaTeX document connect to this Lean name?",
    ["A `% lea: formalize label=…` comment in the theorem block names it", "The Lean file imports the LaTeX", "By the theorem number"], 0,
    "See 02-source-review.tex line 9 (linked from the disproof node)."),
 ])
