# Review: do the statements say what they claim?

Every headline here is a **problem statement**, not a result. Five of the six have `sorry` as their entire proof,
on purpose. So the question for this page is not "is the proof right?" but "does the Lean say what the competition
problem says?". A mistake there would let an agent "solve" the wrong problem. As everywhere on this site, the Lean was
**not built**.

## Putnam 2025 A2: faithful

[putnam_2025_a2](#/node/putnam_2025_a2) states both halves (largest a, smallest b) with `IsGreatest`/`IsLeast`, so
it requires optimality, not just that the constants work. The competition asks to *find* the constants; the Lean
states the known answer, which is the standard way to formalize a "find" question. **PARTIAL (sorry).**

## Putnam 2025 A3: probably not quite the competition game

[putnam_2025_a3](#/node/putnam_2025_a3) is a careful encoding: states carry the set of unvisited strings,
strategies are functions from states to states, and "Alice loses" becomes "the first illegal move happens on an even
step". Bob's moves must also be legal up to that point. We think that part is right.

The concern is the move rule ([validNext](#/node/State.validNext), putnam_2025_a3.lean line 13). A digit is a
`Fin 3`, and the move adds the integer +1 or −1 to it. By our reading of how Lean elaborates mixed arithmetic, the
sum is computed in `Fin 3`, which is arithmetic modulo 3. Then 2 + 1 = 0, and the Lean game allows a digit to jump
between 2 and 0. The competition game does not ("add or subtract 1 from one digit", digits restricted to 0, 1, 2).
The Lean game would then be played on a product of triangles rather than a product of paths.

We could not compile the file to confirm the elaboration, and we did not work out whether Bob still wins the
wrap-around variant. (For n = 1 he does: Alice 0→1, Bob 1→2, and Alice cannot go back to 0 because the start is
never unvisited.) If our reading is right, a proof of this Lean statement is a proof about a slightly different game.
**PARTIAL (sorry); possible statement mismatch.**

## Putnam 2025 A5: faithful

[putnam_2025_a5](#/node/putnam_2025_a5) characterises *all* maximisers by an iff, which is stronger than "the
alternating pattern is a maximiser" and matches the competition's "find all s". The two alternating patterns are
written as powers of −1 counted from index 0. **PARTIAL (sorry).**

## Putnam 2025 B3: faithful

[putnam_2025_b3](#/node/putnam_2025_b3) states the answer ("yes, S contains every positive integer") as a theorem.
Natural-number subtraction in 2025ⁿ − 15ⁿ is harmless because 2025ⁿ ≥ 15ⁿ. **PARTIAL (sorry).**

## Putnam 2025 B4: faithful

[putnam_2025_b4](#/node/putnam_2025_b4) models the matrix as a function on all pairs of naturals but only reads
indices 1..n, and states S ≤ (n+2)N/3 as 3S ≤ (n+2)N to stay in ℕ. **PARTIAL (sorry).**

## amc12a_2021_p7: true, but the proof may not check

[amc12a_2021_p7](#/node/amc12a_2021_p7) is a true statement (the even divisors of N sum to 14 times the odd ones,
because N has exactly 2³). Its proof is `decide`, which has the kernel enumerate divisors of 19,663,560 by trial
division. We would not be surprised if this times out or exceeds limits despite the raised options. We have not
checked either way. If it does check, it uses no extra axioms.

## The other eleven statements

We read all of them against our recollection of the problems. A1, A4, A6, B1, B5, B6 and the four sorry'd miniF2F
statements look faithful. [B2](#/node/putnam_2025_b2) asks for slightly stronger hypotheses (f strictly increasing
and continuous on all of ℝ), which is harmless. [A6](#/node/putnam_2025_a6) uses a 2-adic valuation equal to
2k + 2, which is equivalent to the competition's "divisible by 2^(2k+2) but not 2^(2k+3)".

## Surprises

- The Lake project's library target is only the placeholder Leanproblems/Basic.lean, so the bundled CI workflow
  (leanproblems/.github/workflows/lean_action_ci.yml) never compiles any of the 17 problem files.
- The repository's CLAUDE.md says the current environment is lean-4.28.0, while the bundled Lean project pins
  v4.26.0. These are different settings (Axle's remote environment versus the local project), but a reader could
  confuse them.
- The "complete file" prompt tells the agent to verify with `skills/cli/diagnostic.py`, which does not exist at the
  pinned commit (the local checker is `skills/cli/lean_check.py`).
