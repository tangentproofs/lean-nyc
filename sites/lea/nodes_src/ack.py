NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]

# ---------------------------------------------------------------- headlines

node("ack_mono_and_gt",
 "Headline: the Ackermann function grows and is strictly increasing",
 "For every m, A(m, n) > n for all n, and A(m, n+1) > A(m, n) for all n. Both facts are proved together by induction on m, and in the inductive step monotonicity comes first. This is the worked example in Lea's README.",
 r"""## Plain English

**Theorem (`ack_mono_and_gt`, examples/Ackermann.lean lines 10–32).** For every *m*:

1. A(*m*, *n*) > *n* for every *n*, and
2. A(*m*, *n* + 1) > A(*m*, *n*) for every *n*.

Here A is the [Ackermann function](#/node/ackermann). The two parts are restated separately as `ackermann_gt_n`
(lines 34–35) and `ackermann_mono` (lines 37–38).

### Where it comes from

This is the example in the prover README. The prompt asks Lea to define Ackermann "using well-founded
recursion", prove both facts, compute A(4, 1) = 65533 ([ackermann_4_1](#/node/ackermann_4_1)), and not use
Mathlib. The file has no imports, so the last request was met. The README says the file in `examples/` was
generated, but the repository doesn't record the run.

### Why prove two facts at once?

The usual reason is that each half needs the other in the induction. In this proof only the **first** half of the
hypothesis for *m* is used. Monotonicity of A(*m* + 1, ·) follows from growth of A(*m*, ·), because
A(*m* + 1, *n* + 1) = A(*m*, A(*m* + 1, *n*)) > A(*m* + 1, *n*). Then growth of A(*m* + 1, ·) follows by an inner
induction on *n* that uses that monotonicity. Bundling the two is convenient, not necessary.
""",
 [q("Which pair of facts does `ack_mono_and_gt m` give?",
    ["A(m, n) > n for all n, and A(m, n+1) > A(m, n) for all n",
     "A(m, n) > m for all n, and A(m+1, n) > A(m, n)",
     "A(m, n) = 2n + 3",
     "A is computable by primitive recursion"], 0,
    "examples/Ackermann.lean line 10. Note it is monotone in the **second** argument, for fixed m."),
  q("In the inductive step, which part of the hypothesis for m does the proof use?",
    ["Only 'A(m, x) > x'", "Only monotonicity of A(m, ·)", "Both"], 0,
    "Line 17 extracts the first half. The second half is never used."),
  q("What is the outer induction on?",
    ["m, the first argument", "n, the second argument", "The value A(m, n)"], 0,
    "Line 11. The growth part has an inner induction on n (line 24)."),
  q("Does the theorem say A is increasing in its first argument?",
    ["No. It is about the second argument with the first fixed", "Yes"], 0,
    "Both conclusions keep m fixed. Monotonicity in m is a different (true) fact the file doesn't state."),
 ],
 caveats=["Not built for this site. No sorry in the file, and the proof looks complete.",
          "Monotonicity is in the second argument only. Statements in the first argument, or the fact that A grows faster than every primitive recursive function, are not here."],
 widgets=walk("How the proof goes (examples/Ackermann.lean, lines 10-32)", [
  {"text": "Induct on m (line 11).", "link": "ackermann"},
  {"text": "m = 0: A(0, n) = n + 1, so A(0, n) > n and A(0, n+1) = n + 2 > n + 1 = A(0, n). Arithmetic closes both (lines 12–15).", "link": "ack_zero"},
  {"text": "m + 1: take the first half of the induction hypothesis, A(m, x) > x for all x (line 17)."},
  {"text": "Monotonicity first: A(m+1, n+1) unfolds to A(m, A(m+1, n)), which is bigger than A(m+1, n) by the line above (lines 18–21)."},
  {"text": "Growth by an inner induction on n. Base: A(m+1, 0) = A(m, 1) > 1 > 0 (lines 25–28)."},
  {"text": "Inner step: A(m+1, n+1) > A(m+1, n) > n by monotonicity and the inner hypothesis, so A(m+1, n+1) ≥ n + 2 > n + 1 (lines 29–31)."},
  {"text": "Package the two facts (line 32)."},
 ]))

node("ackermann_4_1",
 "Headline: A(4, 1) = 65533",
 "The file computes A(4, 1) = 65533 by a chain of rewriting steps, not by running the function. It first proves A(1, n) = n + 2 and A(2, n) = 2n + 3, then walks A(3, 0) … A(3, 13) one value at a time.",
 r"""## Plain English

**Theorem (`ackermann_4_1`, examples/Ackermann.lean lines 69–71).** The [Ackermann function](#/node/ackermann) at
(4, 1) equals 65533.

### How the number is reached

- A(1, *n*) = *n* + 2 (`ack_1`, lines 40–43) and A(2, *n*) = 2*n* + 3 ([ack_2](#/node/ack_2), lines 45–48), each by
  induction on *n*.
- A(3, 0) = A(2, 1) = 5 (line 50). Then A(3, *k* + 1) = A(2, A(3, *k*)) = 2·A(3, *k*) + 3, so the file steps
  through 13, 29, 61, …, 32765, 65533 in fourteen one-line theorems (lines 50–63). In closed form,
  A(3, *n*) = 2^(*n*+3) − 3, and 2^16 − 3 = 65533.
- A(4, 0) = A(3, 1) = 13 (lines 65–67).
- A(4, 1) = A(3, A(4, 0)) = A(3, 13) = 65533 (lines 69–71).

### Why not just compute it?

Evaluating A(4, 1) directly takes billions of recursive calls. Also, `ackermann` is defined by
well-founded recursion, and Lean's kernel doesn't unfold such definitions readily by evaluation. Rewriting with
the defining equations and the closed forms for A(1, ·) and A(2, ·) avoids both problems. (This is the usual
explanation. This site didn't try the direct computation.)
""",
 [q("What does `ackermann_4_1` state?",
    ["A(4, 1) = 65533", "A(4, 1) > 65533", "A(1, 4) = 65533", "A(4, 1) = 2^16"], 0,
    "examples/Ackermann.lean line 69. Note 65533 = 2^16 − 3."),
  q("Which closed form does the computation of the A(3, k) values rely on?",
    ["A(2, n) = 2n + 3", "A(3, n) = 2^(n+3) − 3, proved as a lemma", "A(1, n) = 2n"], 0,
    "Each step at lines 51–63 uses ack_2. The closed form for A(3, ·) is not proved in the file. The values are walked one at a time."),
  q("What is A(4, 0)?",
    ["13", "5", "1", "65533"], 0, "A(4, 0) = A(3, 1) = 13 (lines 65–67)."),
  q("How is A(4, 1) reduced to a known value?",
    ["A(4, 1) = A(3, A(4, 0)) = A(3, 13)", "A(4, 1) = A(4, 0) + 1", "By running the function to completion"], 0,
    "Line 70 rewrites with the third defining equation and A(4, 0) = 13. Line 71 finishes with A(3, 13) = 65533."),
 ],
 caveats=["Not built for this site. Every step is a short rewrite chain, and the arithmetic checks by hand: 2·k + 3 applied thirteen times starting from 5 gives 65533."],
 widgets=walk("How the proof goes (examples/Ackermann.lean, lines 40-71)", [
  {"text": "A(1, n) = n + 2 by induction on n (lines 40–43)."},
  {"text": "A(2, n) = 2n + 3 by induction on n, using A(1, ·) (lines 45–48).", "link": "ack_2"},
  {"text": "A(3, 0) = A(2, 1) = 5 (line 50)."},
  {"text": "Each A(3, k+1) = A(2, A(3, k)) = 2·A(3, k) + 3, giving 13, 29, 61, 125, 253, 509, 1021, 2045, 4093, 8189, 16381, 32765, 65533 (lines 51–63)."},
  {"text": "A(4, 0) = A(3, 1) = 13 (lines 65–67)."},
  {"text": "A(4, 1) = A(3, A(4, 0)) = A(3, 13) = 65533 (lines 69–71)."},
 ]))

# ---------------------------------------------------------------- statement set

node("ackermann",
 "The Ackermann function",
 "The two-argument Ackermann–Péter function: A(0, n) = n + 1, A(m+1, 0) = A(m, 1), A(m+1, n+1) = A(m, A(m+1, n)). It is total but grows faster than any primitive recursive function.",
 r"""## Plain English

**Definition (`ackermann`, examples/Ackermann.lean lines 1–4).** On natural numbers:

- A(0, *n*) = *n* + 1
- A(*m* + 1, 0) = A(*m*, 1)
- A(*m* + 1, *n* + 1) = A(*m*, A(*m* + 1, *n*))

This is the standard two-argument Ackermann–Péter function. Small cases: A(1, *n*) = *n* + 2, A(2, *n*) = 2*n* + 3,
A(3, *n*) = 2^(*n*+3) − 3.

### Termination

The third equation calls A inside an argument of A, so neither argument alone shrinks on every call. Lean
accepts the definition because the **pair** (*m*, *n*) decreases in lexicographic order on every recursive call.
No termination proof is written in the file, so Lean must have found that order itself. The README's prompt asked
for well-founded recursion, and this is what Lean uses here.

The three equations are restated as `ack_zero`, `ack_succ_zero` and `ack_succ_succ` (lines 6–8), and the proofs
rewrite with them.
""",
 [q("What is A(0, n)?",
    ["n + 1", "n", "1", "2n"], 0, "examples/Ackermann.lean line 2."),
  q("What is A(1, 0)?",
    ["2", "1", "0"], 0, "A(1, 0) = A(0, 1) = 2."),
  q("Why doesn't simple recursion on m alone justify termination?",
    ["The call A(m+1, n) inside the third equation has the same first argument m + 1", "Because m can be negative", "It does"], 0,
    "That inner call (line 4) shrinks n but not m. The lexicographic pair (m, n) handles both kinds of call."),
 ])

node("ack_zero",
 "Lemma: the three defining equations",
 "A(0, n) = n + 1, A(m+1, 0) = A(m, 1) and A(m+1, n+1) = A(m, A(m+1, n)), each restated as a lemma for rewriting.",
 r"""## Plain English

**Lemmas (`ack_zero`, `ack_succ_zero`, `ack_succ_succ`, examples/Ackermann.lean lines 6–8).** These restate the
three clauses of the [definition](#/node/ackermann) as equations. Each is proved by unfolding the definition once.
The later proofs rewrite with them step by step.
""",
 [q("Which lemma is used to unfold A(4, 1)?",
    ["`ack_succ_succ`", "`ack_zero`", "`ack_succ_zero`"], 0,
    "4 = 3 + 1 and 1 = 0 + 1, so the third equation applies (line 70)."),
  q("How are these lemmas proved?",
    ["By unfolding the definition once", "By induction", "They are assumed as axioms"], 0,
    "Each is a one-step rewrite with the definition (lines 6–8)."),
  q("Which lemma gives A(m+1, 0) = A(m, 1)?",
    ["`ack_succ_zero`", "`ack_zero`", "`ack_succ_succ`"], 0, "examples/Ackermann.lean line 7."),
 ])

node("ack_2",
 "Lemma: A(2, n) = 2n + 3",
 "A closed form for the second row of the Ackermann table, proved by induction on n from A(1, n) = n + 2.",
 r"""## Plain English

**Lemma (`ack_2`, examples/Ackermann.lean lines 45–48).** For every *n*, A(2, *n*) = 2*n* + 3.

**Proof idea.** Induction on *n*. A(2, 0) = A(1, 1) = 3. A(2, *n* + 1) = A(1, A(2, *n*)) = (2*n* + 3) + 2 = 2(*n* + 1) + 3.
It uses `ack_1`, A(1, *n*) = *n* + 2 (lines 40–43), proved the same way.

This lemma turns each step of the A(3, ·) chain in [ackermann_4_1](#/node/ackermann_4_1) into "double and add 3".
""",
 [q("What is A(2, 5)?",
    ["13", "10", "7"], 0, "2·5 + 3 = 13."),
  q("Which earlier closed form does the proof use?",
    ["A(1, n) = n + 2", "A(3, n) = 2^(n+3) − 3", "None"], 0, "examples/Ackermann.lean lines 47–48 rewrite with ack_1."),
  q("What is the proof by induction on?",
    ["n", "m"], 0, "examples/Ackermann.lean line 46 inducts on n."),
 ])
