NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]

# ---------------------------------------------------------------- headline

node("compile_correct",
 "Headline: the arithmetic-to-stack-machine compiler is correct",
 "Running the compiled code of an arithmetic expression pushes exactly the expression's value onto the stack, whatever was on the stack before. The proof is a short induction on the expression, and the file contains no sorry.",
 r"""## Plain English

**Theorem (`compile_correct`, examples/StackMachine.lean lines 50–59).** Take any arithmetic
[expression](#/node/Expr) *e* and any starting stack *s* of natural numbers. [Compile](#/node/compile) *e* to a list
of stack-machine instructions and [run them](#/node/execList) starting from *s*. The final stack is *s* with the
[value](#/node/eval') of *e* pushed on top.

This is the classic first compiler-correctness theorem, as in textbook treatments of compiling expressions to a
stack machine.

### Why "any starting stack" matters

The statement is about **every** starting stack, not just the empty one. This is what makes the induction go
through: to compile *e*₁ + *e*₂, the code for *e*₂ runs first and leaves its value on the stack, and then the
code for *e*₁ runs on that **non-empty** stack. The inductive hypothesis has to cover that case.

### What it shows about stack underflow

The machine handles "add with fewer than two numbers on the stack" by doing nothing
([exec](#/node/exec), lines 23 and 25). The theorem shows that compiled code never reaches that case, because each
operator always finds its two operands in place.
""",
 [q("What does `compile_correct` say about running `compile e` from stack *s*?",
    ["The result is the value of *e* pushed onto *s*",
     "The result is the value of *e* alone, and *s* is discarded",
     "The result is *s* unchanged",
     "It only holds for the empty stack"], 0,
    "examples/StackMachine.lean lines 50–51. The old stack *s* is preserved underneath."),
  q("Why does the theorem quantify over every starting stack?",
    ["The code for a sub-expression runs on a stack that already holds other values, so the induction needs that case",
     "Lean requires it for well-formedness",
     "To handle stack underflow"], 0,
    "The proof generalizes the stack before the induction (line 52) for this reason."),
  q("Does the theorem allow subtraction or division?",
    ["No. Expressions are constants, sums and products only", "Yes, both", "Only subtraction"], 0,
    "[Expr](#/node/Expr) has three constructors (examples/StackMachine.lean lines 3–6)."),
  q("What would happen if compiled code ever ran `add` with fewer than two numbers on the stack?",
    ["`exec` would leave the stack unchanged, but the theorem shows this never happens for compiled code",
     "Lean would crash", "It would push 0"], 0,
    "examples/StackMachine.lean lines 23 and 25 are the fall-through cases."),
 ],
 caveats=["Not built for this site. The file has no sorry and the proof looks complete. One spot this site is unsure of without running Lean: in the add and mul cases (lines 55–56 and 58–59), `simp` is followed by `rfl`. That only works if simp leaves exactly one goal of the right shape. If a future simp closes the goal by itself, the `rfl` would raise a 'no goals' error.",
          "The file imports a Mathlib list module (line 1) that it doesn't seem to need. Harmless."],
 widgets=walk("How the proof goes (examples/StackMachine.lean, lines 50-59)", [
  {"text": "Induct on the expression, with the starting stack left general so the hypotheses apply to any stack (line 52).", "link": "Expr"},
  {"text": "Constant n: the code is a single push of n, so the result is n on top of the stack by definition (line 53).", "link": "compile"},
  {"text": "Sum e1 + e2: the code is code(e2), then code(e1), then add. Running a concatenation is running the parts in order (the append lemma). By the hypotheses, the stack becomes val(e1) on top of val(e2) on top of s (line 55).", "link": "execList_append"},
  {"text": "The final add pops those two and pushes val(e1) + val(e2), which is the value of the sum. The closing rfl checks this by unfolding exec (line 56).", "link": "exec"},
  {"text": "Product: the same argument with mul (lines 57–59)."},
 ]))

# ---------------------------------------------------------------- statement set

node("Expr",
 "Arithmetic expressions",
 "Expressions are natural-number constants combined with + and ×. Nothing else: no variables, no subtraction.",
 r"""## Plain English

**Definition (`Expr`, examples/StackMachine.lean lines 3–7).** An expression is a natural-number constant, the sum of
two expressions, or the product of two expressions. Its value is [eval'](#/node/eval').
""",
 [q("Which is an `Expr`?",
    ["(2 + 3) × 4", "x + 1", "5 − 2", "7 / 3"], 0,
    "Only constants, sums and products (examples/StackMachine.lean lines 4–6). There are no variables."),
  q("What kind of numbers are the constants?",
    ["Natural numbers", "Integers", "Reals"], 0, "examples/StackMachine.lean line 4."),
  q("Can an `Expr` contain a variable?",
    ["No", "Yes"], 0, "There is no variable constructor (lines 3–6)."),
 ])

node("eval'",
 "The value of an expression",
 "Evaluate an expression by recursion: a constant is itself, and sums and products are computed from the parts.",
 r"""## Plain English

**Definition (`eval`, examples/StackMachine.lean lines 9–12).** The value of a constant is the constant. The value of
a sum (product) is the sum (product) of the values. This is the "meaning" that the [compiler](#/node/compile) must
respect.

(On this site the id has a prime because examples/Logic.lean also defines an unrelated `eval`, explained as
[eval](#/node/eval). The two files never meet, so there is no clash in Lean.)
""",
 [q("What is the value of add (const 2) (mul (const 3) (const 4))?",
    ["14", "20", "9"], 0, "2 + 3 × 4 = 14 (examples/StackMachine.lean lines 10–12)."),
  q("Is `eval` here related to the `eval` in Logic.lean?",
    ["No. They are separate files with unrelated functions that happen to share a name", "Yes, it is the same function"], 0,
    "Logic.lean evaluates formulas to propositions. This one evaluates arithmetic to numbers."),
  q("What kind of value does it return?",
    ["A natural number", "A stack", "A proposition"], 0, "examples/StackMachine.lean line 9."),
 ])

node("Inst",
 "Stack-machine instructions",
 "Three instructions: push a number, add the top two, multiply the top two.",
 r"""## Plain English

**Definition (`Inst`, examples/StackMachine.lean lines 14–18).** An instruction is *push n*, *add* or *mul*. What
they do is [exec](#/node/exec).
""",
 [q("How many kinds of instruction are there?",
    ["Three", "Two", "Five"], 0, "examples/StackMachine.lean lines 15–17."),
  q("Does any instruction take an argument?",
    ["Only push, which takes the number to push", "All three", "None"], 0, "examples/StackMachine.lean line 15."),
  q("Is there a pop or swap instruction?",
    ["No", "Yes"], 0, "Only push, add and mul (lines 15–17)."),
 ])

node("exec",
 "Running one instruction",
 "Push puts a number on top. Add and mul replace the top two numbers by their sum or product. With fewer than two numbers, add and mul do nothing.",
 r"""## Plain English

**Definition (`exec`, examples/StackMachine.lean lines 20–25).** The stack is a list of natural numbers with the
top first.

- *push n* puts *n* on top.
- *add*: if the stack starts with *x* then *y*, replace them by *x* + *y*. Otherwise leave the stack alone.
- *mul*: the same with *x* × *y*.

The "otherwise leave it alone" cases (lines 23 and 25) make `exec` a total function. They never fire on compiled
code, which is part of what [compile_correct](#/node/compile_correct) shows.
""",
 [q("Starting from stack [3, 4, 9] (top first), what does *add* produce?",
    ["[7, 9]", "[3, 4, 9]", "[12, 9]", "[16]"], 0, "examples/StackMachine.lean line 22: 3 + 4 = 7 replaces the top two."),
  q("What does *mul* do on a stack holding only [5]?",
    ["Leaves it as [5]", "Produces [0]", "Produces [5, 5]"], 0, "Line 25: the fall-through case."),
  q("Is the top of the stack the first or last list element?",
    ["The first", "The last"], 0, "Push adds at the front (line 21)."),
 ])

node("execList",
 "Running a program",
 "Run a list of instructions one after another, left to right.",
 r"""## Plain English

**Definition (`execList`, examples/StackMachine.lean lines 27–29).** Running the empty program leaves the stack
unchanged. Running *i* followed by the rest means: [run](#/node/exec) *i*, then run the rest on the new stack.

The file also states the two defining equations as simplification lemmas (lines 31–36) and proves that running
a concatenation runs the parts in order ([execList_append](#/node/execList_append)).
""",
 [q("In what order are instructions run?",
    ["Left to right, from the head of the list", "Right to left", "All at once"], 0, "examples/StackMachine.lean line 29."),
  q("What does running the empty program do?",
    ["Nothing: the stack is unchanged", "Clears the stack"], 0, "examples/StackMachine.lean line 28."),
  q("Why are the defining equations restated as lemmas at lines 31–36?",
    ["So that `simp` can use them automatically", "Because the definition is incomplete", "To make the function faster"], 0,
    "They are tagged for `simp`, which the compiler proof relies on."),
 ])

node("execList_append",
 "Lemma: running two programs back to back",
 "Running program A followed by program B is the same as running A and then running B on the resulting stack.",
 r"""## Plain English

**Lemma (`execList_append`, examples/StackMachine.lean lines 38–43).** For any programs *A*, *B* and any starting
stack, running the concatenation *A* ++ *B* gives the same result as [running](#/node/execList) *A* first and then
*B*.

**Proof idea.** Induction on *A*, with the stack left general. An empty *A* is trivial. A non-empty *A* peels off
its first instruction and uses the induction hypothesis (lines 41–43).

This is the key fact behind [compile_correct](#/node/compile_correct), because the compiler builds code by
concatenation.
""",
 [q("What is the lemma by induction on?",
    ["The first program", "The second program", "The stack"], 0, "examples/StackMachine.lean line 41."),
  q("Why is the lemma needed in the compiler proof?",
    ["Compiled code is built by concatenating the code of sub-expressions", "To handle underflow", "It isn't"], 0,
    "[compile](#/node/compile) uses ++ in lines 47–48."),
  q("Is it tagged for simp?",
    ["Yes", "No"], 0, "examples/StackMachine.lean line 38."),
 ])

node("compile",
 "The compiler",
 "A constant becomes a single push. A sum or product becomes the code for the right operand, then the code for the left operand, then the operator.",
 r"""## Plain English

**Definition (`compile`, examples/StackMachine.lean lines 45–48).**

- constant *n* ↦ [*push n*]
- *e*₁ + *e*₂ ↦ code(*e*₂) ++ code(*e*₁) ++ [*add*]
- *e*₁ × *e*₂ ↦ code(*e*₂) ++ code(*e*₁) ++ [*mul*]

The **right** operand is compiled first, so when the operator runs, the left operand's value is on top and the
right one is just below. For + and × the order doesn't change the result. It would for a non-commutative
operator, which this language doesn't have.
""",
 [q("What does compile produce for 2 + 3?",
    ["[push 3, push 2, add]", "[push 2, push 3, add]", "[add, push 2, push 3]"], 0,
    "examples/StackMachine.lean line 47: right operand first, then left, then the operator."),
  q("When `add` runs on compiled code for *e*₁ + *e*₂, which value is on top?",
    ["The value of *e*₁", "The value of *e*₂"], 0,
    "*e*₁'s code runs last, so its value ends up on top."),
  q("How many instructions does compile produce for a constant?",
    ["One", "Two", "Zero"], 0, "examples/Ackermann.lean line 46 inducts on n."),
 ])
