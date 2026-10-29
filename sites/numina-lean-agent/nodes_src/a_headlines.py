import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import node_maker, q, walk, ln, txt, P, M, NOT_BUILT, SORRY

NODES = []
node = node_maker(NODES)


node("putnam_2025_a2",
 "Headline: Putnam 2025 A2, squeezing sine between two parabolas",
 "On [0, π], sin x lies between a·x(π−x) and b·x(π−x). The statement says the best constants are a = 1/π and b = 4/π², and that both are sharp. The proof is left as `sorry`.",
 rf"""## What this file is

Like every Putnam file in this repository, this is a **problem statement for the agent**, not a finished theorem.
The proof slot holds a single `sorry` ({ln(P('a2'), 10)}).

## Plain English

**Statement (`putnam_2025_a2`, {ln(P('a2'), 7, 9)}).** The statement has two parts:

1. Look at all real numbers a with a·x·(π − x) ≤ sin x for every x in the closed interval [0, π]. The
   **greatest** such a is 1/π.
2. Look at all real numbers b with b·x·(π − x) ≥ sin x for every x in [0, π]. The **least** such b is 4/π².

Both parts use Mathlib's `IsGreatest` and `IsLeast`. They say two things at once: the value is in the set, *and*
it beats every other member. So it isn't enough to show that 1/π works. A proof also has to show that nothing
bigger works.

## Why these numbers

Both sides vanish at x = 0 and x = π, so look at the ratio sin x / (x(π − x)). Near the endpoints it tends to
1/π, because sin x ≈ x near 0. At the midpoint π/2 it equals 1 / (π²/4) = 4/π². The competition answer says the
ratio is smallest at the ends and largest in the middle. The best lower parabola touches sin at the endpoints, and the
best upper one touches it at the midpoint.

This matches the official Putnam 2025 A2 question, which asks for the largest a and smallest b.
""",
 [q("What does the first conjunct claim about 1/π?",
    ["It works, and no larger constant works", "It works, but a larger constant might too", "It is the average of the ratio"], 0,
    f"`IsGreatest S x` means x ∈ S and x is an upper bound of S ({txt(P('a2'), 8)})."),
  q("Over which x must the inequalities hold?", ["Only x in the closed interval [0, π]", "All real x", "Only x in (0, π)"], 0,
    f"Both sets quantify over x in the closed interval from 0 to π ({txt(P('a2'), 8, 9)}). Including the endpoints is harmless, because both sides are 0 there."),
  q("Is this theorem proved in the repository?", ["No, its proof is `sorry`", "Yes, by `decide`", "Yes, by a long tactic proof"], 0,
    f"{txt(P('a2'), 10)} is `sorry`. The file is a task for the agent."),
  q("At which point does the upper parabola 4/π²·x(π−x) touch sin x?", ["x = π/2", "x = 0", "x = π/4"], 0,
    "At π/2 both equal 1, since π/2·π/2·4/π² = 1."),
 ],
 caveats=[SORRY, NOT_BUILT,
          "Faithful to the competition problem as far as we can tell. The 'why these numbers' paragraph is the standard informal idea, not something in the repository."],
 widgets=walk(f"What a proof must supply ({txt(P('a2'), 7, 10)})", [
   {"text": f"Part 1, membership ({txt(P('a2'), 8)}): show (1/π)·x(π−x) ≤ sin x on [0, π]."},
   {"text": "Part 1, maximality: for any a > 1/π, find an x near 0 where a·x(π−x) > sin x (the ratio tends to 1/π there)."},
   {"text": f"Part 2, membership ({txt(P('a2'), 9)}): show sin x ≤ (4/π²)·x(π−x) on [0, π]."},
   {"text": "Part 2, minimality: any valid b must satisfy b·(π/2)² ≥ sin(π/2) = 1, so b ≥ 4/π²."},
   {"text": f"In this repository all of it is the single `sorry` at {txt(P('a2'), 10)}.", "hard": True},
 ]))


node("putnam_2025_a3",
 "Headline: Putnam 2025 A3, the ternary-string game (Bob wins)",
 "A two-player game on strings of n digits in {0,1,2} is encoded with states, strategies and rollouts. The theorem says the second player, Bob, has a winning strategy for every n ≥ 1. The proof is `sorry`, and the digit arithmetic in the encoding probably wraps 2+1 around to 0.",
 rf"""## What this file is

A problem statement for the agent. The proof is `sorry` ({ln(P('a3'), 32)}). This is the only Putnam file that
needs its own definitions to state the problem: [State](#/node/State), [validNext](#/node/State.validNext),
[init](#/node/State.init), [Strategy](#/node/Strategy) and [IsRollout](#/node/IsRollout) ({ln(P('a3'), 7, 24)}).

## The competition problem, roughly

Alice and Bob take turns, and Alice moves first. They play on a string of n digits, each 0, 1 or 2, which starts as all zeros.
A move changes one digit by 1 and must produce a string that has not appeared before. A player with no legal move
loses. Which player can force a win? (Answer: Bob.)

## Plain English

**Statement (`putnam_2025_a3`, {ln(P('a3'), 26, 31)}).** For every n ≥ 1 there is a Bob strategy b such that,
for every Alice strategy a and every play sequence s that is a [rollout](#/node/IsRollout) of a against b,
there is an **even** step k with two properties:

- every move before step k, by either player, was [valid](#/node/State.validNext);
- the move made at step k is **not** valid.

Even steps are Alice's turns. So "an even step whose move is invalid" encodes "Alice is the first to be unable
to move legally", and Bob wins.

How losing is modelled: a strategy is a plain function from states to states, so it always outputs *something*.
A player with no legal move is forced to output an illegal state. Making an illegal move counts as losing. That also covers
an Alice strategy that plays an illegal move on purpose.
""",
 [q("Who is claimed to have a winning strategy?", ["Bob, the second player", "Alice, the first player", "It depends on n"], 0,
    f"The statement starts with an existential over Bob's strategy b, quantified before every Alice strategy a ({txt(P('a3'), 27)})."),
  q("Why must the losing step k be even?", ["Even steps are Alice's moves, so Alice is the one who first fails", "Because n is even", "Lean requires even indices"], 0,
    f"In a rollout, even steps use Alice's strategy and odd steps use Bob's ({txt(P('a3'), 23, 24)})."),
  q("Must Bob's own moves be legal?", ["Yes: every move before step k must be valid, including Bob's", "No, only Alice's"], 0,
    f"The condition covers every i < k, odd and even alike ({txt(P('a3'), 30)})."),
  q("Is this theorem proved here?", ["No, it is `sorry`", "Yes"], 0, f"{txt(P('a3'), 32)}."),
 ],
 caveats=[SORRY, NOT_BUILT,
          "Possible encoding mismatch, which we could not check without building: digits live in `Fin 3` and a move adds the integer +1 or −1 to one digit (putnam_2025_a3.lean line 13). We expect Lean to do this arithmetic in `Fin 3`, i.e. modulo 3. Then 2 + 1 wraps to 0 and 0 − 1 wraps to 2, and each digit moves around a 3-cycle instead of the path 0–1–2 of the competition problem. If so, the Lean game has extra moves. Whether Bob still wins that variant is a separate question that we did not settle. See the Review page.",
          "The hypothesis 1 ≤ n is named `_hn` and is unused by the statement itself."],
 widgets=walk(f"How the statement is built ({txt(P('a3'), 7, 32)})", [
   {"text": f"A state is the current string together with the set of strings not yet visited ({txt(P('a3'), 7)}).", "link": "State"},
   {"text": f"A move is valid if the new string is unvisited, differs from the old one in exactly one digit by ±1, and is then removed from the unvisited set ({txt(P('a3'), 9, 14)}).", "link": "State.validNext"},
   {"text": f"Play starts at all zeros, with every other string unvisited ({txt(P('a3'), 16, 17)}).", "link": "State.init"},
   {"text": f"A strategy maps states to states; a rollout alternates Alice (even steps) and Bob (odd steps) ({txt(P('a3'), 19, 24)}).", "link": "IsRollout"},
   {"text": f"The theorem asks for a Bob strategy under which Alice is always the first to move illegally ({txt(P('a3'), 26, 31)})."},
   {"text": f"Proof: `sorry` ({txt(P('a3'), 32)}). A real proof must construct Bob's strategy explicitly and show it never runs out of moves first.", "hard": True},
 ]))


node("putnam_2025_a5",
 "Headline: Putnam 2025 A5, which sign patterns allow the most permutations",
 "For a pattern s of n signs, f counts the permutations of n+1 values whose consecutive steps go up or down as s says. The theorem says f is maximised exactly by the two alternating patterns. The proof is `sorry`.",
 rf"""## What this file is

A problem statement for the agent. The proof is `sorry` ({ln(P('a5'), 17)}). The counting function
[f](#/node/f) is defined in the same file ({ln(P('a5'), 7, 9)}).

## Plain English

Fix n ≥ 1 and a list s of n signs, each +1 or −1. [f](#/node/f) of s counts the permutations σ of {{0, …, n}}
whose consecutive differences σ(i+1) − σ(i) have the sign s(i). A + means the permutation goes up at that step,
a − means it goes down. These are permutations with a prescribed up/down pattern.

**Statement (`putnam_2025_a5`, {ln(P('a5'), 11, 16)}).** For n ≥ 1 and any sign pattern s, the following are equivalent:

- s is a **maximiser**: no pattern t has a larger count;
- s is one of the two **alternating** patterns. One goes −, +, −, +, … and the other +, −, +, −, …. In the file
  the i-th sign is (−1) raised to the power i+1 or to the power i, counting from 0.

So the theorem describes *all* maximisers, not just one. The two alternating patterns are mirror images, so they have
the same count. Permutations with an alternating pattern are the classical "zigzag" or "alternating" permutations.
""",
 [q("What does f(n, s) count?", ["Permutations of n+1 values whose up/down steps follow the signs s", "Sign patterns of length n", "Fixed points of a permutation"], 0,
    f"{txt(P('a5'), 7, 9)}: the size of the set of permutations σ with s(i)·(σ(i+1) − σ(i)) > 0 for every i."),
  q("What kind of statement is the theorem?", ["An 'if and only if' that characterises all maximisers", "Only that the alternating pattern is a maximiser", "A formula for f"], 0,
    f"The two sides of the ↔ are 'no t beats s' and 's is alternating' ({txt(P('a5'), 15, 16)})."),
  q("How many sign patterns does it say are maximisers?", ["Exactly two: the two alternating ones", "Exactly one", "All of them"], 0,
    f"The right-hand side is a disjunction of the two alternating patterns ({txt(P('a5'), 16)})."),
  q("Is it proved here?", ["No, `sorry`", "Yes"], 0, f"{txt(P('a5'), 17)}."),
 ],
 caveats=[SORRY, NOT_BUILT,
          "For n = 1 the two 'alternating' patterns are just + and −, both of which give count 1, so the statement is (correctly) trivially true there.",
          "The signs are encoded as units of the integers (ℤˣ), the elements +1 and −1, which is a faithful way to say 'a sign'."],
 widgets=walk(f"How the statement is built ({txt(P('a5'), 7, 17)})", [
   {"text": f"Define f: count permutations of Fin (n+1) whose step i has the sign s(i) ({txt(P('a5'), 7, 9)}).", "link": "f"},
   {"text": f"Left side of the ↔: s is a maximiser, i.e. f(t) ≤ f(s) for every pattern t ({txt(P('a5'), 15)})."},
   {"text": f"Right side: s is one of the two alternating patterns ({txt(P('a5'), 16)})."},
   {"text": "A proof needs both directions: alternating patterns win, and every other pattern does strictly worse than some pattern.", "hard": True},
   {"text": f"In this repository: `sorry` ({txt(P('a5'), 17)}).", "hard": True},
 ]))


node("putnam_2025_b3",
 "Headline: Putnam 2025 B3, a set closed under divisors of 2025ⁿ − 15ⁿ",
 "If a nonempty set S of positive integers contains every positive divisor of 2025ⁿ − 15ⁿ whenever it contains n, then S contains every positive integer. The proof is `sorry`.",
 rf"""## What this file is

A problem statement for the agent. The proof is `sorry` ({ln(P('b3'), 12)}). It has no extra definitions.

## Plain English

**Statement (`putnam_2025_b3`, {ln(P('b3'), 5, 11)}).** Let S be a set of natural numbers such that:

- S is nonempty;
- every element of S is positive;
- **closure:** whenever n is in S, every positive divisor d of 2025ⁿ − 15ⁿ is in S too.

Then every positive integer n is in S.

The competition question asked "must S contain all positive integers?". The Lean states the answer, yes, as a
theorem.

## Why it is plausible

2025 = 15², so 2025ⁿ − 15ⁿ = 15ⁿ(15ⁿ − 1). From one element of S you get 1 (a divisor of anything), and
from n you get every divisor of 15ⁿ(15ⁿ − 1). The work is to show that these divisor sets eventually reach every
positive integer. We don't sketch the competition argument here, and the repository doesn't contain one.
""",
 [q("Which hypothesis makes S grow?", ["Every positive divisor of 2025ⁿ − 15ⁿ joins S whenever n is in S", "S contains 1", "S is infinite"], 0,
    f"The closure hypothesis `h` ({txt(P('b3'), 8)})."),
  q("Does the statement say S is the set of all natural numbers?", ["No: only that every positive n is in S. Whether 0 is in S is ruled out by the positivity hypothesis", "Yes, including 0"], 0,
    f"The conclusion is for n > 0 ({txt(P('b3'), 9, 11)}), and the hypothesis `_h0` says S has only positive elements ({txt(P('b3'), 7)})."),
  q("In ℕ, subtraction truncates at 0. Does that matter here?", ["No, because 2025ⁿ ≥ 15ⁿ, so the difference is the true one", "Yes, it changes the problem"], 0,
    "2025ⁿ = 15²ⁿ ≥ 15ⁿ, so natural-number subtraction gives the real difference."),
  q("Is it proved here?", ["No, `sorry`", "Yes"], 0, f"{txt(P('b3'), 12)}."),
 ],
 caveats=[SORRY, NOT_BUILT,
          "Faithful to the competition problem as far as we can tell. This file, unlike the others, does not set the pretty-printing options; it only turns off the heartbeat limit (putnam_2025_b3.lean lines 1–3)."],
 widgets=walk(f"How the statement is built ({txt(P('b3'), 5, 12)})", [
   {"text": f"Hypotheses: S nonempty, S has only positive elements, and S is closed under positive divisors of 2025ⁿ − 15ⁿ ({txt(P('b3'), 6, 8)})."},
   {"text": f"Goal: an arbitrary positive n lies in S ({txt(P('b3'), 9, 11)})."},
   {"text": "A proof must show that, starting from any element, repeatedly taking divisors of 15ᵐ(15ᵐ − 1) eventually reaches n.", "hard": True},
   {"text": f"In this repository: `sorry` ({txt(P('b3'), 12)}).", "hard": True},
 ]))


node("putnam_2025_b4",
 "Headline: Putnam 2025 B4, sum versus nonzero entries of a staircase matrix",
 "For an n×n matrix of natural numbers that is zero above the anti-diagonal and grows by 0 or 1 down each column and along each row, three times the total is at most (n+2) times the number of nonzero entries. The proof is `sorry`.",
 rf"""## What this file is

A problem statement for the agent. The proof is `sorry` ({ln(P('b4'), 31)}). Five helper definitions set it up:
[MatrixProp](#/node/MatrixProp), [colSum](#/node/colSum), [colNonzeros](#/node/colNonzeros),
[totalSum](#/node/totalSum) and [nonzeroCount](#/node/nonzeroCount) ({ln(P('b4'), 7, 24)}).

## Plain English

The matrix is a function A taking row i and column j to a natural number. Only the indices 1 to n matter.

**Statement (`putnam_2025_b4`, {ln(P('b4'), 26, 30)}).** Let n ≥ 2, and suppose A satisfies
[MatrixProp](#/node/MatrixProp):

- entries with i + j ≤ n (above the anti-diagonal) are 0;
- going down a column, each entry equals the one above it or is one more;
- going right along a row, each entry equals the one to its left or is one more.

Write S for the sum of all n² entries ([totalSum](#/node/totalSum)) and N for the number of nonzero entries
([nonzeroCount](#/node/nonzeroCount)). Then 3·S ≤ (n + 2)·N.

Put another way, the average nonzero entry is at most (n + 2)/3. Multiplying through by 3 keeps everything in
natural numbers, with no division.
""",
 [q("Which entries are forced to be 0?", ["Those with i + j ≤ n", "Those on the main diagonal", "Those with i > j"], 0,
    f"The first clause of MatrixProp ({txt(P('b4'), 8)})."),
  q("What does the inequality say in words?", ["The average nonzero entry is at most (n+2)/3", "Every entry is at most (n+2)/3", "The number of nonzero entries is at most n+2"], 0,
    f"3·S ≤ (n+2)·N rearranges to S/N ≤ (n+2)/3 when N > 0 ({txt(P('b4'), 30)})."),
  q("Which indices do the sums range over?", ["Rows and columns 1 to n", "Rows and columns 0 to n−1", "All natural numbers"], 0,
    f"Each sum runs over `range n` and shifts by one, so it reads A at 1..n ({txt(P('b4'), 14, 24)})."),
  q("Is it proved here?", ["No, `sorry`", "Yes"], 0, f"{txt(P('b4'), 31)}."),
 ],
 caveats=[SORRY, NOT_BUILT,
          "A is a function on all pairs of natural numbers, but MatrixProp and the sums only look at indices 1..n, so the values elsewhere are irrelevant. This matches the n×n matrix of the problem."],
 widgets=walk(f"How the statement is built ({txt(P('b4'), 7, 31)})", [
   {"text": f"MatrixProp: zero above the anti-diagonal, and steps of 0 or +1 down columns and along rows ({txt(P('b4'), 7, 12)}).", "link": "MatrixProp"},
   {"text": f"colSum and colNonzeros: the sum and the nonzero count of one column ({txt(P('b4'), 14, 18)}).", "link": "colSum"},
   {"text": f"totalSum and nonzeroCount add those over the n columns ({txt(P('b4'), 20, 24)}).", "link": "totalSum"},
   {"text": f"Theorem: for n ≥ 2 and A satisfying MatrixProp, 3·totalSum ≤ (n+2)·nonzeroCount ({txt(P('b4'), 26, 30)})."},
   {"text": f"In this repository: `sorry` ({txt(P('b4'), 31)}).", "hard": True},
 ]))


node("amc12a_2021_p7",
 "Headline: the one statement with a proof (odd versus even divisor sums)",
 "For N = 34·34·63·270, the even divisors of N sum to exactly 14 times the odd divisors. This is the only one of the 17 problem files with a proof, and the proof is a single `decide`. It asks Lean's kernel to evaluate the divisor sums by brute force, and we did not check that this finishes.",
 rf"""## What this file is

One of five miniF2F problems in the repository. miniF2F is a standard benchmark of competition-style problems
stated in Lean. The file's comment gives the informal question ({ln(M('amc12a_2021_p7'), 5, 6)}): what is the ratio
of the sum of the odd divisors of N to the sum of the even divisors? The answer is 1 : 14.

## Plain English

**Statement (`amc12a_2021_p7`, {ln(M('amc12a_2021_p7'), 7, 9)}).** Let N = 34·34·63·270. Then 14 times
(sum of the odd divisors of N) equals (sum of the even divisors of N).

Writing the ratio as a multiplication avoids fractions. Everything stays in natural numbers.

## The by-hand argument

N = 19,663,560 = 2³ × 2,457,945, and the second factor is odd. Every divisor of N is 2ᵉ × (an odd divisor), with e = 0, 1, 2 or 3.
So the even divisors are 2, 4 or 8 times an odd divisor, and their sum is (2 + 4 + 8) = 14 times the odd sum.

## The Lean proof

The Lean proof is not this argument. It is the single tactic `decide` ({ln(M('amc12a_2021_p7'), 10)}), with the
recursion-depth and heartbeat limits raised just for this theorem ({ln(M('amc12a_2021_p7'), 3, 4)}). `decide`
asks the kernel to *compute* both sides. Mathlib defines the divisors of N by testing every number from 1 to N, so
that means about twenty million divisibility tests inside the kernel.
""",
 [q("Which equation does the Lean state?", ["14 × (odd divisor sum) = (even divisor sum)", "(odd sum) / (even sum) = 1/14 as real numbers", "The number of even divisors is 14 times the number of odd ones"], 0,
    f"Two filtered sums over `Nat.divisors`, with the odd one multiplied by 14 ({txt(M('amc12a_2021_p7'), 8, 9)})."),
  q("Why is the factor exactly 14?", ["N has exactly three factors of 2, and 2 + 4 + 8 = 14", "Because N has 14 odd divisors", "Because 270 = 14 × 19 + 4"], 0,
    "34 = 2·17 twice and 270 = 2·135 give 2³; 63 is odd."),
  q("How is it proved in the file?", ["By `decide`: brute-force evaluation", "By a hand-written argument about powers of 2", "It is `sorry`"], 0,
    f"{txt(M('amc12a_2021_p7'), 10)}."),
 ],
 caveats=[NOT_BUILT,
          "We are unsure this `decide` actually succeeds. Kernel evaluation over the roughly twenty million candidates for the divisors of 19,663,560 is the kind of computation that usually times out or exhausts the limits, even with the raised options at amc12a_2021_p7.lean lines 3–4. The agent's own prompt warns against just raising heartbeats when `decide` times out (prompts/prompt_complete_file.txt). The theorem is true either way; the question is only whether this proof checks.",
          "No `native_decide` is used, so if it checks, it checks in the kernel with no extra trust."],
 widgets=walk(f"How the proof goes ({txt(M('amc12a_2021_p7'), 3, 10)})", [
   {"text": f"Raise maxRecDepth and maxHeartbeats for this one theorem ({txt(M('amc12a_2021_p7'), 3, 4)})."},
   {"text": f"State 14·(odd divisor sum) = (even divisor sum) for N = 34·34·63·270 ({txt(M('amc12a_2021_p7'), 7, 9)})."},
   {"text": f"Call `decide` ({txt(M('amc12a_2021_p7'), 10)}): the kernel evaluates the decision procedure for this equality of natural numbers.", "hard": True},
   {"text": "That means listing the divisors of 19,663,560 by trial division, filtering by parity, summing, and comparing. The 2³ argument above is never used."},
 ]))
