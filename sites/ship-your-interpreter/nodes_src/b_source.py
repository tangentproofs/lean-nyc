NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

# ---------------------------------------------------------------- A. the source language

node("Vsa.While.Program",
 "WHILE programs (the AST)",
 "A WHILE program is a list of statements over a small, dynamically typed, Lox-like language with first-class functions. The Lean AST mirrors the C structs in c/src/ast.h one to one, which is what makes the memory layout relation possible.",
 r"""## Plain English

**Definitions (Vsa/While/Ast.lean lines 1–50).** Two mutually recursive types:

- **expressions**: integer, string and boolean literals, `null`, a variable, an assignment `x = e`,
  a binary operator (`+ - * / %`, the six comparisons), `and`/`or`, unary `-` and `!`, a call `f(args)`,
  and an anonymous or named function literal with parameter names and a body;
- **statements**: an expression statement, `var x` with an optional initialiser, a block, `if` with an
  optional `else`, `while`, a C-style `for` with optional parts, `return` with an optional value, `break`
  and `continue`.

A **program** is a list of statements (line 48).

The tests in `c/tests/*.wl` are written in this language, and Vsa/While/Programs.lean gives several of them
as Lean values (for example `whileWl`, from line 15). The executable `whilecheck --selftest` compares the
Lean parser's output with these values. That parser is not verified.
""",
 [q("What is a Program?",
    ["A list of statements", "A single expression", "A string of source text"], 0,
    "Vsa/While/Ast.lean line 48."),
  q("Are functions first-class values in WHILE?",
    ["Yes. A function literal is an expression and evaluates to a closure", "No, only top-level declarations"], 0,
    "The fn constructor of Expr (Vsa/While/Ast.lean line 30) and the fn rule of EvalE (Vsa/While/Semantics.lean lines 248–251)."),
  q("Does the main theorem start from source text?",
    ["No, from this AST already laid out in memory", "Yes"], 0,
    "Loaded relates the machine memory to a Program value, not to text (Vsa/Refinement.lean lines 12–13)."),
 ])

node("Vsa.While.ExecS",
 "The big-step rules",
 "Mutually inductive big-step relations for expressions, calls, statements, loops and sequences. A missing rule means no result: division by zero, failed assert, calling a non-function, wrong arity and call depth beyond 1000 all get stuck.",
 r"""## Plain English

**Definitions (Vsa/While/Semantics.lean lines 192–406).** A state `St` has a **store** (an array of
environment frames, each with a parent pointer and a list of bindings, plus an array of closures) and the
**output** printed so far (lines 20–40). The judgements carry a call depth `d` and the current
environment frame:

- `EvalE`: an expression evaluates to a value and a new state (lines 194–251). Variables are looked up
  along the parent chain. `and`/`or` short-circuit. Binary operators go through `binOpSem`
  (lines 166–186): integer arithmetic **wraps to 64 bits** (`wrap64`), `+` on a string concatenates with a
  display form of the other side, and `/` and `%` by zero have **no** result.
- `Call`: calling a closure needs a matching argument count, `d < 1000` (`maxCallDepth`, line 188), and a
  fresh frame for the parameters. The body ends normally (result `null`) or by `return v`. The natives
  `print`, `println` and `assert` append to the output or check truthiness (lines 261–282).
- `ExecS`: statements produce a **status**: normal, break, continue or return-with-value (lines 42–43,
  284–352). `while` and `for` have their own loop relations.
- `ExecSeq`: a list runs left to right and stops at the first abrupt status (lines 393–406).

There are no rules for errors. A run that divides by zero is simply not derivable. The separate
error semantics (Vsa/While/ErrorSem.lean) describes failing runs, and Vsa/While/Exclusive.lean proves the
three outcomes exclusive.
""",
 [q("What happens in the semantics on division by zero?",
    ["No rule applies, so that run has no big-step result", "It returns 0", "It returns null"], 0,
    "binOpSem returns none for a zero divisor (Vsa/While/Semantics.lean lines 174–175), and the binary rule needs some value."),
  q("What is the maximum call depth?",
    ["1000; a call at depth ≥ 1000 has no rule", "Unbounded", "64"], 0,
    "maxCallDepth (Vsa/While/Semantics.lean line 188) and the d < maxCallDepth premise of Call.closure."),
  q("How do integers behave on overflow?",
    ["They wrap to signed 64-bit, like the C code", "They are unbounded mathematical integers", "Overflow is an error"], 0,
    "wrap64 (Vsa/While/Semantics.lean line 150) is applied in each arithmetic case."),
  q("What does a statement produce besides a new state?",
    ["A status: normal, break, continue or return v", "A type", "An exit code"], 0,
    "Status (Vsa/While/Semantics.lean lines 42–43)."),
 ],
 caveats=["These rules are the specification. They were written to match the C interpreter, including details such as 64-bit wrapping, string concatenation display and the depth cap. Whether they match anyone's intended WHILE is a question for a human reader.",
          "Only the relations' shapes are summarised here. There are about 40 rules (Vsa/While/Semantics.lean lines 192–406)."])

node("Vsa.While.BigStep",
 "BigStep: a program's normal result",
 "BigStep p out says the program, started from the initial state with the three natives bound, runs to the end with status normal and has printed exactly out. A top-level return, break or continue is not a normal result.",
 r"""## Plain English

**Definition (`BigStep`, Vsa/While/Semantics.lean lines 417–418).** `BigStep p out` holds when there is a
final state `st'` such that the statement list `p`, run by [ExecSeq](#/node/Vsa.While.ExecS) from the initial
state at depth 0 in frame 0, ends with status **normal** in `st'`, and the output of `st'` is `out`.

The **initial state** `initSt` (lines 410–415) has one global frame binding `print`, `println` and
`assert` to the natives. It has no closures and empty output.

So `BigStep` relates a program to its output on success. Because the semantics is deterministic in
practice (the theorem derives this from machine determinism, Vsa/Lang/Basic.lean lines 74–77), there is
at most one such `out`. Programs that fail or run forever have none. Those are described by
`BigStepErr` and `BigStepDiverges` (Vsa/While/ErrorSem.lean lines 254–255 and 442–443).
""",
 [q("Does a program that ends with a top-level `return` have a BigStep result?",
    ["No. BigStep needs final status normal", "Yes, with the returned value as output"], 0,
    "Vsa/While/Semantics.lean line 418. A top-level abrupt status counts as an error (TopAbrupt, Vsa/While/ErrorSem.lean lines 251–252)."),
  q("What is `out` in BigStep p out?",
    ["Everything print and println wrote, as one string", "The value of the last expression", "The exit code"], 0,
    "Vsa/While/Semantics.lean line 418: st'.out = out."),
  q("Which names are bound at the start?",
    ["print, println and assert", "None", "All C library functions"], 0,
    "initSt, Vsa/While/Semantics.lean lines 410–415."),
 ])

node("Vsa.While.ExecSeqCost",
 "The cost-counting semantics",
 "A second copy of the big-step rules that also counts heap allocation. Every BigStep derivation has a cost-annotated twin (BigStep.cost). The machine proof uses the cost to show the C heap never runs out on a terminating run.",
 r"""## Plain English

**Definitions (Vsa/While/Cost.lean, `ExecSeqCost` at lines 273–285).** Each relation of the
[big-step semantics](#/node/Vsa.While.ExecS) has a twin with one extra natural number: an upper estimate of
the bytes the C interpreter allocates while performing that step. The estimate covers environment frames,
closures, string concatenation and stringified values. Sequencing adds costs.

The total machine proof runs in a **counted regime**. The heap invariant carries a budget, and each
allocation spends from it. The `capacity` assumption inside `Loaded`
([InitialAllocatorAt](#/node/Vsa.Sim.DlHeap.InitialAllocatorAt)) says that for every cost-annotated
terminating run of the loaded program with cost `n`, twice `n` plus a fixed slack fits between the heap top
and the heap end.

[BigStep.cost](#/node/Vsa.While.BigStep.cost) shows that the extra index is no restriction: every
ordinary derivation has a cost.
""",
 [q("Why does the machine proof need a cost semantics?",
    ["To show malloc never fails on a terminating run, using the capacity assumption", "To measure running time", "To prove termination"], 0,
    "VsaIris/Interp/World.lean lines 736–746 (RegimeOK and Boot.regime_of_bigStep)."),
  q("Does every BigStep derivation have a cost?",
    ["Yes, by BigStep.cost", "Only for loop-free programs"], 0,
    "Vsa/While/CostExists.lean lines 39–43."),
  q("Where does a concrete cost bound come from for a given program?",
    ["From the static analysis progCost, used by endToEnd_checked", "It is guessed"], 0,
    "Vsa/Sim/CheckedBoundary.lean lines 12 and 18–31."),
 ])

node("Vsa.While.BigStep.cost",
 "Every result has a cost",
 "Any BigStep derivation can be re-read as a cost-annotated derivation with the same final state, so the counted machine proof applies to every normal result.",
 r"""## Plain English

**Theorem (`BigStep.cost`, Vsa/While/CostExists.lean lines 39–43).** If `BigStep p out`, there are a final
state `st'` and a number `n` with a [cost-annotated](#/node/Vsa.While.ExecSeqCost) derivation of `p` from the
initial state to `st'` with status normal and cost `n`, and `st'.out = out`.

The proof is a mutual induction over all the semantic relations (the motives are set up in
Vsa/While/Cost.lean lines 288–301, and `costExists` is proved at Vsa/While/CostExists.lean line 20):
each rule has a cost-annotated counterpart.

It is used in [Boot.regime_of_bigStep](#/node/VsaIris.Interp.Boot.regime_of_bigStep), the step that
turns a normal result into a heap budget.
""",
 [q("Does BigStep.cost change the final state or output?",
    ["No, the same st' and out", "Yes, it may differ"], 0,
    "Vsa/While/CostExists.lean line 40."),
  q("How is it proved?",
    ["By mutual induction over the semantic relations", "By computation"], 0,
    "Vsa/While/Cost.lean lines 288–301 and Vsa/While/CostExists.lean lines 20–37."),
  q("Where is it used on the path to the main theorem?",
    ["In Boot.regime_of_bigStep", "In the Sail model"], 0,
    "VsaIris/Interp/World.lean line 744."),
 ])
