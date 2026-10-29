import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import node_maker, q, ln, txt, P, M, NOT_BUILT, SORRY

NODES = []
node = node_maker(NODES)

MSORRY = ("PARTIAL (sorry): a miniF2F benchmark statement whose proof is deliberately left as `sorry` for the agent "
          "to fill in.")


def stmt_q(path, line):
    return q("Is this proved in the repository?", ["No, its proof is `sorry`", "Yes"], 0, f"{txt(path, line)} is `sorry`.")


# ---- the other Putnam 2025 problems ---------------------------------------------------------------------------

node("putnam_2025_a1",
 "Putnam 2025 A1: fractions (2m+1)/(2n+1) become reduced",
 "Start with distinct positive integers m₀ ≠ n₀ and repeatedly replace (m, n) by the reduced numerator and denominator of (2m+1)/(2n+1). Then 2m+1 and 2n+1 fail to be coprime only finitely often. The proof is `sorry`.",
 rf"""## Plain English

**Statement (`putnam_2025_a1`, {ln(P('a1'), 7, 11)}).** Let m and n be sequences of natural numbers with
m₀, n₀ > 0 and m₀ ≠ n₀. At each step, m and n become the numerator and denominator of the rational number
(2mₖ + 1)/(2nₖ + 1) in lowest terms. Then the set of k for which 2mₖ + 1 and 2nₖ + 1 are **not** coprime
is finite.

That is the competition's "coprime for all but finitely many k". The recursion uses Mathlib's `Rat.num` and
`Rat.den`, which return a fraction in lowest terms. The equations compare m and n, cast to integers, with that
numerator and denominator. The fractions stay positive, so nothing is lost.
""",
 [q("What does the conclusion say?", ["Non-coprime steps happen only finitely often", "2mₖ+1 and 2nₖ+1 are always coprime", "The sequence is eventually constant"], 0,
    f"A set of indices is declared finite ({txt(P('a1'), 11)})."),
  q("Why must m₀ ≠ n₀?", ["If they were equal, the fraction would be 1 forever and the claim would fail", "To keep the numbers positive", "It is not needed"], 0,
    "With m = n, (2m+1)/(2n+1) = 1/1, and from then on 3 and 3 are not coprime at every step."),
  stmt_q(P('a1'), 12)],
 caveats=[SORRY, NOT_BUILT])


node("putnam_2025_a4",
 "Putnam 2025 A4: 2025 matrices that commute exactly with their cyclic neighbours",
 "The smallest k for which 2025 real k×k matrices can be chosen so that two of them commute exactly when their indices are equal or adjacent around a cycle is k = 3. The proof is `sorry`.",
 rf"""## Plain English

**Statement (`putnam_2025_a4`, {ln(P('a4'), 7, 8)}).** Among positive integers k for which there exist k×k real
matrices A₀, …, A₂₀₂₄ such that

Aᵢ and Aⱼ commute **if and only if** |i − j| is 0, 1 or 2024,

the least is 3. The difference 2024 links A₀ and A₂₀₂₄, so "adjacent" is around a 2025-cycle. The "only if"
direction matters too: non-neighbours must **fail** to commute.
""",
 [q("Which pairs must commute?", ["Equal or cyclically adjacent indices", "All pairs", "Only equal indices"], 0, f"{txt(P('a4'), 8)}."),
  q("Must non-adjacent matrices fail to commute?", ["Yes, it's an 'if and only if'", "No"], 0, f"The ↔ in {txt(P('a4'), 8)}."),
  stmt_q(P('a4'), 9)],
 caveats=[SORRY, NOT_BUILT])


node("putnam_2025_a6",
 "Putnam 2025 A6: the exact power of 2 in a difference of recursion values",
 "For bₙ₊₁ = 2bₙ² + bₙ + 1 with b₀ = 0, and k ≥ 1, the 2-adic valuation of b at 2^(k+1) minus twice b at 2^k is exactly 2k + 2. The proof is `sorry`.",
 rf"""## Plain English

**Statement (`putnam_2025_a6`, {ln(P('a6'), 7, 12)}).** Define integers b by b₀ = 0 and bₙ₊₁ = 2bₙ² + bₙ + 1.
For every k ≥ 1, the exponent of 2 in b(2^(k+1)) − 2·b(2^k) is exactly 2k + 2.

The competition says "divisible by 2^(2k+2) but not by 2^(2k+3)". Mathlib's `padicValInt` gives 0 for the number 0,
and 2k+2 is never 0, so the Lean version also implies that the difference is nonzero. The two forms say the same
thing.
""",
 [q("What is padicValInt 2 x?", ["The exponent of 2 in x", "x mod 2", "log₂ x rounded"], 0, "The 2-adic valuation."),
  q("Does the statement imply the difference is nonzero?", ["Yes, since the valuation of 0 is defined as 0 ≠ 2k+2", "No"], 0, f"{txt(P('a6'), 12)}."),
  stmt_q(P('a6'), 13)],
 caveats=[SORRY, NOT_BUILT])


node("putnam_2025_b1",
 "Putnam 2025 B1: a two-colouring closed under circumcentres is constant",
 "If every point of the plane is coloured one of two colours, and every non-degenerate triangle with all three vertices the same colour has its circumcentre that colour too, then the whole plane is one colour. The proof is `sorry`.",
 rf"""## Plain English

**Statement (`putnam_2025_b1`, {ln(P('b1'), 7, 10)}).** Colour the Euclidean plane with a Boolean (two colours).
Suppose that for every triangle (Mathlib's `Triangle`, three affinely independent points, so never degenerate)
whose vertices all share a colour, its circumcentre has that colour too. Then some single colour c₀ is the colour
of every point.
""",
 [q("Can the triangle be degenerate (collinear)?", ["No, Mathlib triangles are affinely independent", "Yes"], 0,
    "Collinear points have no circumcentre, and Mathlib's Triangle excludes them."),
  q("How many colours are allowed?", ["Two (a Bool)", "Three", "Any number"], 0, f"{txt(P('b1'), 7)}."),
  stmt_q(P('b1'), 11)],
 caveats=[SORRY, NOT_BUILT])


node("putnam_2025_b2",
 "Putnam 2025 B2: centroid of a region versus its solid of revolution",
 "For a continuous, strictly increasing, nonnegative f on [0,1], the region under its graph has a centroid whose x-coordinate is strictly less than the centroid of the solid swept out by rotating the region about the x-axis. The proof is `sorry`.",
 rf"""## Plain English

**Statement (`putnam_2025_b2`, {ln(P('b2'), 7, 15)}).** Let f be continuous and strictly increasing on ℝ, and
nonnegative on [0, 1]. Let R be the region 0 ≤ x ≤ 1, 0 ≤ y ≤ f(x), and x₁ the average of the x-coordinate over
R (its centroid's x-coordinate). Let R′ be the solid obtained by rotating R about the x-axis, and x₂ the average
x-coordinate over R′. Then x₁ < x₂.

The averages use Mathlib's set average ⨍ with respect to area and volume.
""",
 [q("What is x₁?", ["The x-coordinate of the centroid of the planar region", "The area of R", "The maximum of f"], 0, f"An average over R ({txt(P('b2'), 12)})."),
  q("Is f required to be increasing only on [0,1]?", ["No, the file asks for strictly increasing on all of ℝ, which loses nothing since only [0,1] matters", "Yes"], 0,
    f"`StrictMono f` ({txt(P('b2'), 9)})."),
  stmt_q(P('b2'), 16)],
 caveats=[SORRY, NOT_BUILT,
          "Slightly stronger hypotheses than the competition (f defined, continuous and strictly increasing on all of ℝ). Any f on [0,1] with the competition's properties extends to such a function, so this is a harmless reformulation."])


node("putnam_2025_b5",
 "Putnam 2025 B5: how often the inverse mod p goes down",
 "For a prime p > 3, more than p/4 − 1 of the residues k = 1, …, p−2 have the inverse of k+1 smaller than the inverse of k (inverses taken mod p and read as numbers in 0..p−1). The proof is `sorry`.",
 rf"""## Plain English

**Statement (`putnam_2025_b5`, {ln(P('b5'), 7, 10)}).** Let p > 3 be prime. Count the k in ZMod p with k ≠ 0,
k ≠ −1, such that the inverse of k+1, read as a number from 0 to p−1, is smaller than the inverse of k. This count,
as a real number, is greater than p/4 − 1.

k ≠ 0 and k ≠ −1 pick out exactly k = 1, …, p−2, the range in the competition problem.
""",
 [q("Which k are counted from?", ["1 to p−2", "1 to p−1", "0 to p−1"], 0, f"k ≠ 0 and k ≠ −1 ({txt(P('b5'), 10)})."),
  q("How are the inverses compared?", ["As natural numbers 0..p−1 via `.val`", "In ZMod p directly", "As real numbers"], 0, f"{txt(P('b5'), 10)}."),
  stmt_q(P('b5'), 11)],
 caveats=[SORRY, NOT_BUILT])


node("putnam_2025_b6",
 "Putnam 2025 B6: the best exponent r with g(n+1) − g(n) ≥ g(g(n))^r",
 "The largest real r for which some function g from positive integers to positive integers satisfies g(n+1) − g(n) ≥ g(g(n))^r for all n is r = 1/4. The proof is `sorry`.",
 rf"""## Plain English

**Statement (`putnam_2025_b6`, {ln(P('b6'), 7, 8)}).** Among real r for which there is a function g from positive
integers to positive integers with g(n+1) − g(n) ≥ g(g(n))^r for every positive n, the greatest is 1/4.

As in [A2](#/node/putnam_2025_a2), `IsGreatest` asks for two things: r = 1/4 is achievable, and no larger r is.
""",
 [q("What does IsGreatest require?", ["1/4 works, and nothing larger works", "Only that 1/4 works"], 0, f"{txt(P('b6'), 8)}."),
  q("Where is the difference g(n+1) − g(n) computed?", ["In the reals, so it can be negative", "In ℕ, truncated at 0"], 0, "Both values are cast to ℝ first."),
  stmt_q(P('b6'), 9)],
 caveats=[SORRY, NOT_BUILT])


# ---- the other miniF2F problems -------------------------------------------------------------------------------

node("imo_1964_p1_a",
 "miniF2F: IMO 1964 P1(a), when 7 divides 2ⁿ − 1",
 "For positive n, 7 divides 2ⁿ − 1 exactly when 3 divides n. The proof is `sorry`.",
 rf"""## Plain English

**Statement (`imo_1964_p1_a`, {ln(M('imo_1964_p1'), 5)}).** For n > 0: 7 ∣ 2ⁿ − 1 if and only if 3 ∣ n.
The informal problem is in the comment at {ln(M('imo_1964_p1'), 3, 4)}.

Powers of 2 mod 7 cycle 2, 4, 1, so 2ⁿ ≡ 1 exactly when n is a multiple of 3. Part (b) is
[imo_1964_p1_b](#/node/imo_1964_p1_b).
""",
 [q("Does natural-number subtraction cause trouble here?", ["No, 2ⁿ ≥ 1 so 2ⁿ − 1 is the true value", "Yes"], 0, "2ⁿ is at least 1."),
  q("Why does 3 appear?", ["2³ = 8 ≡ 1 mod 7, so powers of 2 repeat every 3 steps", "Because n must be odd"], 0, "The order of 2 mod 7 is 3."),
  stmt_q(M('imo_1964_p1'), 6)],
 caveats=[MSORRY, NOT_BUILT, "The original asks to 'find all n'; the Lean states the answer (multiples of 3) as an iff."])


node("imo_1964_p1_b",
 "miniF2F: IMO 1964 P1(b), 7 never divides 2ⁿ + 1",
 "For positive n, 7 does not divide 2ⁿ + 1. The proof is `sorry`.",
 rf"""## Plain English

**Statement (`imo_1964_p1_b`, {ln(M('imo_1964_p1'), 8)}).** For n > 0, 7 ∤ 2ⁿ + 1. Powers of 2 mod 7 are 1, 2 or
4, so 2ⁿ + 1 is 2, 3 or 5 mod 7, never 0.
""",
 [q("What are the possible values of 2ⁿ mod 7?", ["1, 2, 4", "1 to 6", "0 and 1"], 0, "The cycle 2, 4, 1."),
  q("Is n > 0 needed?", ["Not really: for n = 0, 2⁰ + 1 = 2 is not divisible by 7 either", "Yes, essential"], 0, "The hypothesis is harmless."),
  stmt_q(M('imo_1964_p1'), 9)],
 caveats=[MSORRY, NOT_BUILT])


node("algebra_sqineq_2atp2bpge2ab",
 "miniF2F: a² + b² ≥ 2ab",
 "For all real a and b, a² + b² ≥ 2ab. This is the easiest problem in the set, and its proof is still `sorry`, as a warm-up for the agent.",
 rf"""## Plain English

**Statement (`algebra_sqineq_2atp2bpge2ab`, {ln(M('algebra_sqineq_2atp2bpge2ab'), 4)}).** For real a, b:
a² + b² ≥ 2ab. It follows from (a − b)² ≥ 0.
""",
 [q("Which fact gives it immediately?", ["(a − b)² ≥ 0", "The triangle inequality", "AM-GM for three numbers"], 0, "Expand (a − b)²."),
  q("Does it need a, b ≥ 0?", ["No, it holds for all reals", "Yes"], 0, f"No hypotheses ({txt(M('algebra_sqineq_2atp2bpge2ab'), 4)})."),
  stmt_q(M('algebra_sqineq_2atp2bpge2ab'), 5)],
 caveats=[MSORRY, NOT_BUILT])


node("mathd_algebra_478",
 "miniF2F: (2009² − 2009)/2009 = 2008",
 "If x = (2009² − 2009)/2009 as real numbers, then x = 2008. The proof is `sorry`.",
 rf"""## Plain English

**Statement (`mathd_algebra_478`, {ln(M('mathd_algebra_478'), 4)}).** A real x equal to (2009² − 2009)/2009 is 2008,
since the numerator is 2009 · 2008.
""",
 [q("Why is the answer 2008?", ["2009² − 2009 = 2009·2008", "Rounding", "Because division truncates"], 0, "Factor out 2009."),
  q("Which number system is used?", ["Real numbers, so division is exact", "Natural numbers with truncating division"], 0, f"x : ℝ ({txt(M('mathd_algebra_478'), 4)})."),
  stmt_q(M('mathd_algebra_478'), 5)],
 caveats=[MSORRY, NOT_BUILT])


node("mathd_numbertheory_284",
 "miniF2F: gcd(2¹⁰⁰¹ − 1, 2¹⁰¹² − 1) = 2¹¹ − 1",
 "The greatest common divisor of 2¹⁰⁰¹ − 1 and 2¹⁰¹² − 1 is 2¹¹ − 1, an instance of gcd(2ᵃ − 1, 2ᵇ − 1) = 2^gcd(a,b) − 1 with gcd(1001, 1012) = 11. The proof is `sorry`.",
 rf"""## Plain English

**Statement (`mathd_numbertheory_284`, {ln(M('mathd_numbertheory_284'), 4)}).** Nat.gcd of 2¹⁰⁰¹ − 1 and 2¹⁰¹² − 1
is 2¹¹ − 1. Since 1012 − 1001 = 11 and 1001 = 7 · 11 · 13, gcd(1001, 1012) = 11.

Lean can evaluate this directly too: the numbers have about 300 digits, which is easy for arbitrary-precision
arithmetic.
""",
 [q("Which identity is behind it?", ["gcd(2ᵃ − 1, 2ᵇ − 1) = 2^gcd(a,b) − 1", "gcd(a, b) = ab / lcm(a, b) only"], 0, "A standard fact about Mersenne-type numbers."),
  q("What is gcd(1001, 1012)?", ["11", "1", "13"], 0, "1012 − 1001 = 11 and 11 divides 1001."),
  stmt_q(M('mathd_numbertheory_284'), 5)],
 caveats=[MSORRY, NOT_BUILT])
