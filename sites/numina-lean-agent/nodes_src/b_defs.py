import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import node_maker, q, ln, txt, P

NODES = []
node = node_maker(NODES)

A3 = P("a3")
B4 = P("b4")


# ---- Putnam 2025 A3: the game -------------------------------------------------------------------------------

node("State",
 "A3 game state: current string plus unvisited strings",
 "A game state is a pair: the current string of n digits (each in Fin 3, i.e. 0, 1 or 2), and the finite set of strings that have not appeared yet.",
 rf"""## Plain English

**Definition (`State n`, {ln(A3, 7)}).** A state of the [A3 game](#/node/putnam_2025_a3) on strings of length n
is a pair:

1. the **current string**, a function from the n positions to `Fin 3`, the three values 0, 1 and 2;
2. the **unvisited set**, a finite set of such strings.

Storing what has *not* been visited, rather than the history, makes "the new string must not have appeared before"
a simple membership test (see [validNext](#/node/State.validNext)).

The file declares it with `abbrev`, so Lean unfolds it freely. It is just a pair type with a name.
""",
 [q("What does the second component of a state record?", ["The strings that have not appeared yet", "The strings already played", "Whose turn it is"], 0,
    f"It is the set that the move rule removes strings from ({txt(A3, 14)})."),
  q("How many values can each digit take?", ["Three: 0, 1, 2", "Two", "n"], 0, f"`Fin 3` ({txt(A3, 7)})."),
  q("Does the state record whose turn it is?", ["No, turns are tracked by the step index in a rollout", "Yes"], 0,
    f"Turns come from even/odd step numbers in IsRollout ({txt(A3, 23, 24)})."),
 ])


node("State.validNext",
 "A3: the legal moves from a state",
 "From a state, a legal next state has an unvisited string that differs from the current one in exactly one digit, by +1 or −1. That string is then removed from the unvisited set. In `Fin 3` the ±1 probably wraps around.",
 rf"""## Plain English

**Definition (`State.validNext s`, {ln(A3, 9, 14)}).** The finite set of states s′ such that:

1. s′'s current string was **unvisited** in s ({ln(A3, 11)});
2. there is one position i and a step δ, either +1 or −1, such that s′'s string equals s's string with δ added at
   position i, and agrees with it everywhere else ({ln(A3, 12, 13)});
3. s′'s unvisited set is s's unvisited set with the new string removed ({ln(A3, 14)}).

The [theorem](#/node/putnam_2025_a3) uses this set to judge every move. A move from s to s′ is legal exactly
when s′ is in `validNext s`.

## The wrap-around question

The digit is in `Fin 3`, but δ is an integer. We read Lean's elaboration rules as doing this addition in `Fin 3`,
that is modulo 3, because the left-hand side of the equation has type `Fin 3`. Under that reading 2 + 1 = 0 and
0 − 1 = 2, so a digit can jump from 2 to 0. The competition problem doesn't allow that. We did not compile the file,
so this is our reading, not a checked fact.
""",
 [q("Can a legal move return to the starting string of all zeros?", ["No, the start is never in the unvisited set", "Yes, if it's two moves later"], 0,
    f"State.init removes the all-zero string from the unvisited set ({txt(A3, 17)}), and a move needs an unvisited target ({txt(A3, 11)})."),
  q("How many digits change in a legal move?", ["Exactly one", "At least one", "Any number"], 0,
    f"One position i changes by δ and every other position j stays the same ({txt(A3, 12, 13)})."),
  q("Under the likely modulo-3 reading, is 2 → 0 a legal change of one digit?", ["Yes, because 2 + 1 = 0 in Fin 3", "No"], 0,
    f"That is the encoding concern ({txt(A3, 13)}). In the competition problem it would not be legal."),
 ],
 caveats=["The modulo-3 reading is an inference from Lean's arithmetic elaboration rules, not from a build. If Lean instead did the arithmetic in ℤ after casting the digits, there would be no wrap-around and the encoding would match the competition."])


node("State.init",
 "A3: the starting state",
 "The game starts at the all-zero string, and every other string is unvisited.",
 rf"""## Plain English

**Definition (`State.init n`, {ln(A3, 16, 17)}).** The current string is all zeros. The unvisited set is every
string of length n except the all-zero one.

Removing the start means no move can ever return to it, matching "a string that has not appeared before" in the
competition problem. A [rollout](#/node/IsRollout) must begin here.
""",
 [q("Which string is missing from the starting unvisited set?", ["The all-zero string", "The all-two string", "None"], 0, f"{txt(A3, 17)}."),
  q("How many strings are unvisited at the start?", ["3ⁿ − 1", "3ⁿ", "2ⁿ"], 0, "All 3ⁿ strings minus the starting one."),
  q("Who moves first from this state?", ["Alice (step 0 is even)", "Bob"], 0, f"Even steps use Alice's strategy ({txt(A3, 23)})."),
 ])


node("Strategy",
 "A3: a strategy is a function from states to states",
 "A strategy simply says, for each state, which state to move to. Because the state includes the unvisited set, this loses nothing compared with strategies that look at the whole history.",
 rf"""## Plain English

**Definition (`Strategy n`, {ln(A3, 19)}).** A function from [State](#/node/State) n to State n.

Nothing forces the output to be legal. Legality is checked separately, by [validNext](#/node/State.validNext), in
the [theorem](#/node/putnam_2025_a3). That is how "a player with no legal move" is modelled: the function still
outputs a state, it just isn't a valid one.

Since a state records the current string and the set of strings already used up, it carries everything that matters
about the history. A deterministic strategy that sees only the state is therefore enough for a winning strategy.
""",
 [q("Must a Strategy's output be a legal move?", ["No, legality is checked by the theorem using validNext", "Yes, by its type"], 0,
    f"The type is just State n → State n ({txt(A3, 19)})."),
  q("Does a Strategy see the full history?", ["Only through the state: current string and unvisited set", "Yes, it gets the list of past moves"], 0,
    f"Its input is a single State ({txt(A3, 19)})."),
  q("Is a Strategy allowed to be random?", ["No, it is a deterministic function", "Yes"], 0, "It is an ordinary Lean function."),
 ])


node("IsRollout",
 "A3: a play sequence produced by two strategies",
 "A rollout is an infinite sequence of states. It starts at the initial state, applies Alice's strategy on even steps and Bob's on odd steps.",
 rf"""## Plain English

**Definition (`IsRollout a b s`, {ln(A3, 21, 24)}).** The sequence s : ℕ → [State](#/node/State) n is a rollout of
Alice's strategy a against Bob's strategy b when:

- s 0 is the [initial state](#/node/State.init) ({ln(A3, 22)});
- for every even i, s (i+1) is a applied to s i ({ln(A3, 23)});
- for every odd i, s (i+1) is b applied to s i ({ln(A3, 24)}).

The sequence continues forever, even after someone has made an illegal move. The [theorem](#/node/putnam_2025_a3)
only looks at the prefix up to the first illegal move.

Given a and b there is exactly one rollout, so quantifying over "every s with IsRollout a b s" just means "the
game a and b play".
""",
 [q("Who moves at step 0?", ["Alice: 0 is even", "Bob"], 0, f"{txt(A3, 23)}."),
  q("How many rollouts are there for fixed strategies a and b?", ["Exactly one", "Infinitely many", "None, unless the game ends"], 0,
    "The start and every step are determined, so the sequence is unique."),
  q("Does a rollout stop at an illegal move?", ["No, it continues; the theorem only inspects the prefix", "Yes"], 0,
    f"It's a function on all of ℕ ({txt(A3, 21)})."),
 ])


# ---- Putnam 2025 A5: the counting function ------------------------------------------------------------------

node("f",
 "A5: f counts permutations with a prescribed up/down pattern",
 "f n s is the number of permutations σ of {0,…,n} such that, for each i, σ(i+1) − σ(i) has the sign s(i).",
 rf"""## Plain English

**Definition (`f n s`, {ln(P('a5'), 7, 9)}).** Given n and a sign pattern s (n entries, each +1 or −1, as units of
the integers), f n s is the number of permutations σ of `Fin (n+1)` with

s(i) · (σ(i+1) − σ(i)) > 0 for every i from 0 to n − 1.

The differences are taken in the integers, so the condition says "step i goes up if s(i) = +1 and down if
s(i) = −1". For example, with n = 2 and pattern (+, −), the permutations of {{0, 1, 2}} that go up then down are
0 2 1 and 1 2 0. So f = 2.

Used by [putnam_2025_a5](#/node/putnam_2025_a5).
""",
 [q("For n = 2 and pattern (+, +), what is f?", ["1: only 0 1 2 goes up twice", "2", "6"], 0,
    "A permutation that rises at every step must be the identity."),
  q("Why are the differences taken as integers?", ["So 'down' means a negative difference, not natural-number truncation to 0", "For speed", "Lean requires it"], 0,
    f"σ values are cast to ℤ before subtracting ({txt(P('a5'), 9)})."),
  q("How many values does σ permute?", ["n + 1", "n", "2n"], 0, f"`Fin (n + 1)` ({txt(P('a5'), 8)})."),
 ],
 caveats=["The scanner also lists `f` as a dependency of putnam_2025_b2. That is a false positive: in B2, `f` is a local variable (a function on the reals), unrelated to this definition."])


# ---- Putnam 2025 B4: the matrix -----------------------------------------------------------------------------

node("MatrixProp",
 "B4: the staircase conditions on the matrix",
 "MatrixProp n A says three things about the entries at rows and columns 1..n: zero above the anti-diagonal, and steps of 0 or +1 going down columns and going right along rows.",
 rf"""## Plain English

**Definition (`MatrixProp n A`, {ln(B4, 7, 12)}).** For a function A : ℕ → ℕ → ℕ read as a matrix with rows and
columns 1..n, all three of:

1. **zero corner:** A i j = 0 whenever i + j ≤ n ({ln(B4, 8)});
2. **columns climb slowly:** for rows 1 to n−1, the entry below is equal to A i j or one more ({ln(B4, 9, 10)});
3. **rows climb slowly:** for columns 1 to n−1, the entry to the right is equal to A i j or one more
   ({ln(B4, 11, 12)}).

Together these make A a staircase. It is zero in the top-left triangle and then rises by at most 1 per step to
the right or down. The largest entry possible is at the bottom-right corner.

Used by [putnam_2025_b4](#/node/putnam_2025_b4).
""",
 [q("For n = 3, is entry (1, 2) forced to be 0?", ["Yes, since 1 + 2 ≤ 3", "No"], 0, f"{txt(B4, 8)}."),
  q("Can an entry jump by 2 from its left neighbour?", ["No, only 0 or +1", "Yes"], 0, f"{txt(B4, 11, 12)}."),
  q("Are entries allowed to decrease going right?", ["No", "Yes, by at most 1"], 0, "The two options are equal or one more."),
 ])


node("colSum",
 "B4: sum of one column",
 "colSum n A j adds up rows 1..n of column j.",
 rf"""## Plain English

**Definition (`colSum n A j`, {ln(B4, 14, 15)}).** The sum of A(i+1, j) over i from 0 to n−1, i.e. rows 1..n of
column j. [totalSum](#/node/totalSum) adds these up over the columns.
""",
 [q("Which rows does colSum read?", ["Rows 1 to n", "Rows 0 to n−1", "Rows 0 to n"], 0, f"`range n` shifted by one ({txt(B4, 15)})."),
  q("Does colSum depend on MatrixProp?", ["No, it is defined for any A", "Yes"], 0, "It's a plain sum."),
  q("What is colSum for a column of all zeros?", ["0", "n", "1"], 0, "A sum of zeros."),
 ])


node("colNonzeros",
 "B4: nonzero entries in one column",
 "colNonzeros n A j counts how many of rows 1..n in column j are nonzero.",
 rf"""## Plain English

**Definition (`colNonzeros n A j`, {ln(B4, 17, 18)}).** The number of i from 0 to n−1 with A(i+1, j) ≠ 0.
[nonzeroCount](#/node/nonzeroCount) adds these up over the columns.
""",
 [q("What does colNonzeros count?", ["Nonzero entries in a column", "The sum of a column", "Zero entries"], 0, f"{txt(B4, 18)}."),
  q("What's the largest value it can take?", ["n", "n²", "1"], 0, "One count per row."),
  q("If a column has entries 0, 1, 2, what is colNonzeros?", ["2", "3", "1"], 0, "Two entries are nonzero."),
 ])


node("totalSum",
 "B4: sum of all entries (S)",
 "totalSum n A is the sum of all n² entries, over rows and columns 1..n. It is S in the problem.",
 rf"""## Plain English

**Definition (`totalSum n A`, {ln(B4, 20, 21)}).** The sum of [colSum](#/node/colSum) over columns 1..n. This is
the S of the [B4 statement](#/node/putnam_2025_b4).
""",
 [q("Over which columns does totalSum add?", ["1 to n", "0 to n−1"], 0, f"{txt(B4, 21)}."),
  q("Which quantity of the competition problem is this?", ["S, the sum of entries", "N, the number of nonzero entries"], 0, "The left side of 3·S ≤ (n+2)·N."),
  q("Is it a sum of n² entries?", ["Yes: n columns, each with n rows", "No, n entries"], 0, f"{txt(B4, 14, 21)}."),
 ])


node("nonzeroCount",
 "B4: number of nonzero entries (N)",
 "nonzeroCount n A counts the nonzero entries over rows and columns 1..n. It is N in the problem.",
 rf"""## Plain English

**Definition (`nonzeroCount n A`, {ln(B4, 23, 24)}).** The sum of [colNonzeros](#/node/colNonzeros) over columns
1..n. This is the N of the [B4 statement](#/node/putnam_2025_b4).
""",
 [q("Which quantity of the competition problem is this?", ["N, the number of nonzero entries", "S, the sum of entries"], 0, "The right side of 3·S ≤ (n+2)·N."),
  q("Can it exceed n²?", ["No", "Yes"], 0, "There are only n² entries."),
  q("Under MatrixProp, can it be n²?", ["No: entries with i + j ≤ n are zero", "Yes"], 0, f"{txt(B4, 8)}."),
 ])
