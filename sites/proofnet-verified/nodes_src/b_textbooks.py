import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_common.py"), encoding="utf-8").read())

# One node per source book. Each is anchored on one representative problem (node ids must be declarations),
# and summarises the rest of that book's problems. Counts come from error_taxonomy/*/per_file/*.json:
# "errors" = every verdict other than "faithful" (unfaithful, plus ambiguous or wrong informal source).

GROUP = ("This node stands for a whole group of problems. Only the representative problem is described in detail; "
         "the counts for the group were tallied by this site from the audit records, not taken from the README.")


node("Artin_exercise_11_4_6a",
 "Group: the Artin problems (28): groups, rings, polynomials",
 "28 problems from Artin's Algebra. The original ProofNet got 10 wrong and ProofNet# 3. In the representative one, the original statement was about a different polynomial over a different field.",
 r"""## Plain English

**The group.** 28 problems are taken from Michael Artin's *Algebra*: subgroups and orders of elements, rings and
ideals, irreducibility of particular polynomials, and some number theory (infinitely many primes of a given
form). By the audit records, **10** of the 28 original ProofNet statements were unfaithful, and **3** of the
ProofNet# ones. The [first headline](#/node/Artin_exercise_2_2_9) and
[the xⁿ − p problem](#/node/Artin_exercise_11_4_8) are both from this book.

**Representative (`Artin_exercise_11_4_6a`, [[L 194 13-15]]).** In any field F with exactly 2 elements, the
polynomial x² + x + 1 is irreducible. (Exercise 11.4.6(a): x² + x + 1 is irreducible over 𝔽₂.)

Saying "a field with 2 elements" (`card F = 2`) rather than naming 𝔽₂ is a common trick: every such field is
𝔽₂ up to isomorphism, and the statement doesn't need to pick one.

**What the original said.** The original ([[O 194 12-14]]) took a field with **7** elements and the polynomial
**x² + 1**. That is the next exercise in the book, which happens to be true too (−1 is not a square mod 7). But
it is a different problem. The audit ([[T 194]]) labels it *incomparable* (neither statement implies the
other) but *provable*, root cause **misunderstanding of the informal statement**. ProofNet# had already fixed it.
""",
 [q("What does the hypothesis card F = 2 accomplish?",
    ["It pins F down as the field with two elements, 𝔽₂, up to isomorphism",
     "It says the polynomial has degree 2", "It says F has characteristic 0"], 0,
    "Line 13. All fields with 2 elements are isomorphic to 𝔽₂."),
  q("Why is the original version (x² + 1 over a 7-element field) labelled 'incomparable' rather than 'false'?",
    ["It is a true statement, just not the one asked; neither statement implies the other",
     "It is false", "It is the same statement written differently"], 0,
    "The audit record says incomparable, provable. It is a correct fact about a different polynomial and field."),
  q("How many of the 28 Artin problems did the original ProofNet get wrong, by the audit?",
    ["10", "3", "28"], 0,
    "10 for ProofNet and 3 for ProofNet#, tallied from the per-problem audit records."),
 ],
 caveats=[STATUS_SORRY, GROUP])


node("Axler_exercise_5_4",
 "Group: the Axler problems (26): linear algebra",
 "26 problems from Axler's Linear Algebra Done Right, the most error-prone group: 19 of the original statements and 9 of ProofNet#'s were unfaithful. In the representative one, 'invariant under S' had become 'mapped onto itself by S', which is false.",
 r"""## Plain English

**The group.** 26 problems come from Sheldon Axler's *Linear Algebra Done Right*: linear maps, eigenvalues and
invariant subspaces, inner-product spaces, normal and self-adjoint operators. By the audit records **19** of
the original statements and **9** of ProofNet#'s were unfaithful, the highest error rate of any book. Two
headlines are from Axler: [the missing brackets](#/node/Axler_exercise_5_20) and
[the polarization identity](#/node/Axler_exercise_6_7).

**Representative (`Axler_exercise_5_4`, [[L 19 13-16]]).** If S and T are commuting linear maps on V and c is
a scalar, then S maps the null space of T − cI into itself.

In Lean: the image of ker(T − c·id) under S is **contained in** (`≤`) ker(T − c·id). That is exactly "the null
space of T − cI is invariant under S".

**What the original said.** The original ([[O 19 11-14]]) wrote `=` instead of `≤`, claiming that S maps the
null space **onto** itself. That is false: take S = 0 and c an eigenvalue of T, so the null space is non-zero but
its image is zero. Both ProofNet and ProofNet# had the `=` ([[T 19]], [[S 19]]): *stronger*, *false*, root
cause **misunderstanding of the informal statement**.
""",
 [q("What does '≤' between two submodules mean on line 15?",
    ["Containment: the first is a subspace of the second", "Comparison of dimensions", "Equality"], 0,
    "For submodules, ≤ is the subset order. Image ≤ kernel says S sends the kernel into itself."),
  q("Why was the original '=' version false?",
    ["Invariance only needs S to map the subspace into itself, not onto it; S = 0 is a counterexample",
     "Commuting maps never share null spaces", "It was true; only the notation changed"], 0,
    "With S = 0 the image is {0} while the null space of T − cI can be non-zero."),
  q("Which predecessor datasets had this problem wrong?",
    ["Both ProofNet and ProofNet#", "Only ProofNet", "Neither"], 0,
    "Both audit records say stronger, false."),
 ],
 caveats=[STATUS_SORRY, GROUP,
          "The S = 0 counterexample is this site's; the audit record argues the same point in general terms."])


node("Dummit_Foote_exercise_1_1_29",
 "Group: the Dummit–Foote problems (87): abstract algebra",
 "The biggest group: 87 problems from Dummit and Foote's Abstract Algebra. 42 originals and 12 ProofNet# statements were unfaithful. The representative one shows the same missing-brackets slip as the Axler headline, and this time it made the statement false.",
 r"""## Plain English

**The group.** 87 problems, nearly a quarter of the benchmark, come from David Dummit and Richard Foote's
*Abstract Algebra*: orders of elements, subgroups and quotients, group actions, Sylow theorems ("no group of
order 6545 is simple"), rings, ideals and irreducibility. By the audit, **42** original statements and **12**
ProofNet# statements were unfaithful. The headline [ℝ× ≇ ℂ×](#/node/Dummit_Foote_exercise_1_6_4) is from this
book.

**Representative (`Dummit_Foote_exercise_1_1_29`, [[L 217 13-16]]).** For groups A and B: the product group
A × B is abelian **if and only if** both A and B are abelian.

**What the original said.** The original ([[O 217 12-15]]) left out the brackets around the first
"for all x y in A × B". As with [Axler 5.20](#/node/Axler_exercise_5_20), the `∀` then swallows the whole ↔,
and the original says: *for every pair x, y in A × B, x and y commute iff A and B are both abelian.* That is false
whenever A × B is non-abelian, because x = y = 1 commute while the right side fails. The audit ([[T 217]])
labels it *stronger*, *false*, root cause **misunderstanding of Lean**. ProofNet# had the brackets right.
""",
 [q("How did Lean read the original line '∀ x y : A × B, x*y = y*x ↔ (A abelian) ∧ (B abelian)'?",
    ["As ∀ x y, (x*y = y*x ↔ …): the ↔ inside the ∀",
     "As (∀ x y, x*y = y*x) ↔ …, as intended", "As a type error"], 0,
    "∀ extends as far right as it can. The audit record [[T 217]] spells it out."),
  q("Why is that reading false?",
    ["Take A non-abelian: x = y = 1 commute, but the right side is false, so the ↔ fails for that pair",
     "Products of abelian groups are not abelian", "It isn't false"], 0,
    "For the identity element pair the left side is always true, so the statement would force A and B to be abelian."),
  q("Roughly what share of the whole benchmark comes from Dummit and Foote?",
    ["About a quarter (87 of 367)", "About half", "About a tenth"], 0,
    "Counted from the theorem names in proofnet-verified-latest."),
 ],
 caveats=[STATUS_SORRY, GROUP])


node("Herstein_exercise_2_3_17",
 "Group: the Herstein problems (47): groups, rings, fields",
 "47 problems from Herstein's Topics in Algebra; 27 originals and 11 ProofNet# statements were unfaithful. The representative one shows a subtle Lean trap: an extra [Mul G] made '*' mean an unrelated multiplication.",
 r"""## Plain English

**The group.** 47 problems come from I. N. Herstein's *Topics in Algebra*: groups (centralizers, Sylow
subgroups, groups of small order), rings, fields and field extensions (for example, cos 1° is algebraic over ℚ).
By the audit **27** original statements and **11** ProofNet# ones were unfaithful.

**Representative (`Herstein_exercise_2_3_17`, [[L 74 13-15]]).** In a group G, the centralizer of x⁻¹ax is
x⁻¹C(a)x, the conjugate of the centralizer of a.

**What the original said.** The original ([[O 74 12-15]]) declared G with **two** instances,
`[Mul G] [Group G]`. A `Group` already comes with a multiplication, so the extra `[Mul G]` supplies a *second*,
unrelated multiplication. The audit ([[T 74]]) explains that the `*` in the statement then resolves to that
second operation, so the claim is about an arbitrary binary operation unrelated to the group. That makes it
false. Labels: *stronger*, *false*, **misunderstanding of Lean**. ProofNet# had the same error ([[S 74]]). The
fix simply deletes `[Mul G]`.
""",
 [q("What was wrong with declaring both [Mul G] and [Group G]?",
    ["G got two unrelated multiplications, and the statement's * used the one with no group laws",
     "Nothing; it is redundant but harmless", "Lean rejects it"], 0,
    "This is the audit's explanation ([[T 74]]). It type-checks, which is why it is easy to miss."),
  q("What is centralizer {a}?",
    ["The set of elements that commute with a", "The subgroup generated by a", "The conjugacy class of a"], 0,
    "C(a) in Herstein's notation, line 14."),
  q("Did ProofNet# fix this one?",
    ["No: its audit record also says stronger, false", "Yes", "It dropped the problem"], 0,
    "See [[S 74]]."),
 ],
 caveats=[STATUS_SORRY, GROUP,
          "The claim about which multiplication * picks is the audit's; this site did not run Lean to confirm the instance resolution."])


node("Ireland_Rosen_exercise_18_4",
 "Group: the Ireland–Rosen problems (21): number theory",
 "21 number-theory problems from Ireland and Rosen; 13 originals and 8 ProofNet# statements were unfaithful. The representative, 1729 as the smallest taxicab number, was false in the original because negative cubes were allowed.",
 r"""## Plain English

**The group.** 21 problems come from Kenneth Ireland and Michael Rosen's *A Classical Introduction to Modern
Number Theory*: congruences, primitive roots, quadratic and quartic residues, sums of powers. By the audit
**13** original statements and **8** ProofNet# ones were unfaithful.

**Representative (`Ireland_Rosen_exercise_18_4`, [[L 104 12-21]]).** 1729 is the smallest positive integer
that can be written as a sum of two positive cubes in two different ways: 1729 = 1³ + 12³ = 9³ + 10³.

In Lean (lines 13–20): 1729 is the infimum (`sInf`) of the set of n > 0 for which there are positive natural
numbers x, y, z, w with x³ + y³ = n = z³ + w³, all four distinct.

**What the original said.** The original ([[O 104 12-15]]) used **integers** x, y, z, w (so negative cubes were
allowed) and only claimed "any such n is at least 1729". With negatives you get many small examples:
1³ + (−1)³ = 0 = 2³ + (−2)³, so n = 0 already satisfies the hypothesis, and 0 ≥ 1729 is false. The audit
([[T 104]]) labels it *incomparable*, *false*, root cause **misunderstanding of the informal statement**. The
corrected statement also asserts that 1729 itself qualifies, which the original never said. ProofNet# was also
wrong ([[S 104]]).
""",
 [q("Why was the original (with integer cubes) false?",
    ["Negative cubes allow tiny examples such as 0 = 1³ + (−1)³ = 2³ + (−2)³",
     "1729 is not a sum of two cubes", "There are no such numbers"], 0,
    "This counterexample is this site's; the audit record [[T 104]] makes the same point about integers."),
  q("What does the corrected statement say beyond 'every such n is at least 1729'?",
    ["That 1729 is itself such a number, since it is the infimum of the set", "That 1729 is prime",
     "Nothing more"], 0,
    "Lines 12–20 state 1729 = sInf of the set. In ℕ that requires 1729 to belong to the set and be its least element."),
  q("Which numbers are the corrected x, y, z, w?",
    ["Positive natural numbers", "Any integers", "Primes"], 0,
    "Line 14 has x y z w : ℕ and line 15 requires each to be positive."),
 ],
 caveats=[STATUS_SORRY, GROUP])


node("Munkres_exercise_28_5",
 "Group: the Munkres problems (60): point-set topology",
 "60 topology problems from Munkres; 36 originals and 19 ProofNet# statements were unfaithful. In the representative, the original nested its closed sets the wrong way round, which turned the theorem into 'every space is countably compact'.",
 r"""## Plain English

**The group.** 60 problems come from James Munkres's *Topology*: topologies, bases and subbases, continuity,
connectedness, compactness, countability and separation axioms. Several files define their own helpers
(`is_topology`, `countably_compact`, the lower-limit topology …); see [helper definitions](#/node/countably_compact).
By the audit **36** original statements and **19** ProofNet# ones were unfaithful.

**Representative (`Munkres_exercise_28_5`, [[L 125 16-20]]).** A space X is
[countably compact](#/node/countably_compact) if and only if every **decreasing** sequence C₁ ⊇ C₂ ⊇ ⋯ of
closed non-empty sets has a point in common.

**What the original said.** The original ([[O 125 17-21]]) wrote `C n ⊆ C (n + 1)`, an **increasing** sequence.
Any point of C₀ lies in every set of an increasing sequence, so the right-hand side is always true and the
original says "every space is countably compact", which is false (ℝ is not). The audit ([[T 125]]) labels it
*stronger*, *false*, **misunderstanding of the informal statement**. ProofNet# had it right.
""",
 [q("What changed between the original and the corrected statement?",
    ["The direction of nesting: C (n + 1) ⊆ C n instead of C n ⊆ C (n + 1)",
     "The definition of countably compact", "IsClosed became IsOpen"], 0,
    "Line 19 of the corrected file; the original has the inclusion the other way round."),
  q("Why did the wrong direction make the statement false?",
    ["Increasing non-empty sequences always share a point, so the theorem claimed every space is countably compact",
     "Decreasing sequences never share a point", "It made the statement vacuous but still true"], 0,
    "Any point of C₀ is in every Cₙ. The real line is not countably compact, so the claim is false."),
  q("Where does countably_compact come from?",
    ["It is defined in the problem file itself, lines 6–9", "Mathlib", "Another problem file"], 0,
    "[[L 125 6-9]]: every countable open cover has a finite subcover."),
 ],
 caveats=[STATUS_SORRY, GROUP])


node("Pugh_exercise_2_57",
 "Group: the Pugh problems (14): real analysis",
 "14 problems from Pugh's Real Mathematical Analysis, with the highest ProofNet# error rate: 9 originals and 8 ProofNet# statements were unfaithful. The representative turned 'give a counterexample' into 'every space has a counterexample'.",
 r"""## Plain English

**The group.** 14 problems come from Charles Pugh's *Real Mathematical Analysis*: sequences, metric spaces and
topology of ℝ and ℝ², connectedness, continuity. By the audit **9** original statements and **8** of ProofNet#'s
were unfaithful, so ProofNet# fixed almost none of this group.

**Representative (`Pugh_exercise_2_57`, [[L 138 12-14]]).** There is a connected subset S of the plane ℝ × ℝ
whose interior is not connected. (The informal statement: show that the interior of a connected set need not be
connected. Two closed discs touching at a point will do.)

**What the original said.** The original ([[O 138 12-14]]) quantified over **every** topological space X and
asked for such an S inside X. That is false: in a one-point space no set has a disconnected interior. Asking
for one counterexample is an existence claim about some space. The audit ([[T 138]]) labels it *stronger*,
*false*, root cause **misunderstanding of the informal statement**. ProofNet# had the same problem
([[S 138]]).
""",
 [q("How does the corrected statement express 'it is not true in general'?",
    ["It asserts that one counterexample exists, in ℝ × ℝ", "It proves a general theorem about interiors",
     "It negates connectedness of every set"], 0,
    "Line 13: ∃ S : Set (ℝ × ℝ), IsConnected S ∧ ¬ IsConnected (interior S)."),
  q("Why was the original (for an arbitrary space X) false?",
    ["Some spaces, like a one-point space, have no such set", "ℝ × ℝ has no such set",
     "Interiors are always connected"], 0,
    "The audit record [[T 138]] gives the one-point space."),
  q("Which predecessor had it right?",
    ["Neither", "ProofNet#", "ProofNet"], 0,
    "Both records say stronger, false."),
 ],
 caveats=[STATUS_SORRY, GROUP, "The touching-discs example is a standard one supplied by this site, not taken from the repository."])


node("Putnam_exercise_2010_a4",
 "Group: the Putnam problems (12): competition mathematics",
 "12 Putnam competition problems; 5 originals and 2 ProofNet# statements were unfaithful. In the representative, the original dropped 'positive', and the extra case n = 0 happened to be true, so the error was harmless to provability.",
 r"""## Plain English

**The group.** 12 problems come from the William Lowell Putnam competition (years from 1998 to 2020):
inequalities, number theory, calculus and complex numbers. By the audit **5** original statements and **2**
ProofNet# statements were unfaithful.

**Representative (`Putnam_exercise_2010_a4`, [[L 144 13-15]]).** For every positive integer n, the number
10^(10^(10^n)) + 10^(10^n) + 10^n − 1 is not prime.

**What the original said.** The original ([[O 144 10-12]]) left out `hn : n > 0`, so it also claims the case
n = 0. There the number is 10^10 + 10 + 1 − 1 = 10^10 + 10, which is even, so not prime. The original is
therefore *stronger* but still *true*. The audit ([[T 144]]) still counts it as an error (root cause **missing
premise**), because it is not the problem as stated. It shows that the audit asks whether a statement means
what the source means, not only whether it is provable.

Note that `^` in Lean groups to the right, so `10^10^10^n` is 10^(10^(10^n)), as in the problem.
""",
 [q("Why is the original version (allowing n = 0) still true?",
    ["At n = 0 the number is 10^10 + 10, which is even", "n = 0 is excluded by Nat", "It isn't true"], 0,
    "10^(10^0) = 10^1 = 10, so the sum is 10^10 + 10 + 1 − 1."),
  q("Then why does the audit count it as an error?",
    ["It claims more than the problem asks (it is 'stronger'), so it is unfaithful even though provable",
     "Because it is false", "Because of a syntax error"], 0,
    "Faithfulness and provability are separate columns of the audit ([[T 144]])."),
  q("How does Lean parse 10^10^10^n?",
    ["As 10^(10^(10^n)): ^ groups to the right", "As ((10^10)^10)^n", "It is ambiguous and rejected"], 0,
    "Exponentiation is right-associative in Lean, as in ordinary mathematics."),
 ],
 caveats=[STATUS_SORRY, GROUP])


node("Rudin_exercise_5_2",
 "Group: the Rudin problems (56): analysis",
 "56 problems from Rudin's Principles of Mathematical Analysis; 35 originals and 20 ProofNet# statements were unfaithful. In the representative, f⁻¹ meant the pointwise reciprocal 1/f, not the inverse function.",
 r"""## Plain English

**The group.** 56 problems come from Walter Rudin's *Principles of Mathematical Analysis*: the real and complex
numbers, metric spaces and compactness, sequences and series, continuity, differentiation. By the audit **35**
original statements and **20** ProofNet# ones were unfaithful, more ProofNet# errors than any other book. The
headline [inf A = −sup(−A)](#/node/Rudin_exercise_1_5) is from Rudin, and so is the one problem whose
[informal statement was itself wrong](#/node/Rudin_exercise_4_8a).

**Representative (`Rudin_exercise_5_2`, [[L 172 12-19]]).** Let f be a real function with f′(x) > 0 on (a, b),
and g a function with g(f(x)) = x there. Then f is strictly increasing on (a, b), g is differentiable on the
image f((a, b)), and g′(f(x)) = 1/f′(x).

**What the original said.** The original ([[O 172 12-18]]) wrote `g = f⁻¹`. For a function f : ℝ → ℝ, Mathlib
reads `f⁻¹` as the **pointwise reciprocal**, x ↦ 1/f(x), not the inverse function. With f(x) = x on (1, 2) the
original would claim that 1/x has derivative 1, which is false. The original also *assumed* g differentiable,
part of what the exercise asks to prove, and left out "f is strictly increasing". The audit ([[T 172]]) labels it
*incomparable*, *false*, root cause **misunderstanding of Mathlib**. ProofNet# was also wrong ([[S 172]]).
""",
 [q("What does f⁻¹ mean for a function f : ℝ → ℝ in Mathlib?",
    ["The pointwise reciprocal x ↦ 1/f(x)", "The inverse function", "The preimage map on sets"], 0,
    "This is the audit's diagnosis in [[T 172]]."),
  q("How does the corrected statement describe 'g is the inverse of f'?",
    ["By the hypothesis g (f x) = x for x in (a, b)", "By g = f⁻¹", "By g = Function.invFun f"], 0,
    "Line 15: g undoes f on the interval (a, b). That is all the exercise needs from 'inverse'."),
  q("Which part of the exercise did the original take as a hypothesis instead of proving it?",
    ["That g is differentiable", "That f′ > 0", "That a < b"], 0,
    "The original has hg_diff, an assumption that g is differentiable, which is what the exercise asks you to prove."),
 ],
 caveats=[STATUS_SORRY, GROUP])


node("Shakarchi_exercise_1_13a",
 "Group: the Shakarchi problems (16): complex analysis",
 "16 problems from Stein and Shakarchi's Complex Analysis; 9 originals and 7 ProofNet# statements were unfaithful. The representative needed a hypothesis the book leaves implicit: the open set must be connected.",
 r"""## Plain English

**The group.** 16 problems come from Elias Stein and Rami Shakarchi's *Complex Analysis*: holomorphic functions,
power series, contour integrals and residues, zeros of bounded functions. By the audit **9** original
statements and **7** ProofNet# ones were unfaithful.

**Representative (`Shakarchi_exercise_1_13a`, [[L 176 14-17]]).** Let f be holomorphic on an open, connected
set Ω (here: complex-differentiable on Ω, with Ω open and preconnected). If the real part of f is constant on Ω,
then f is constant on Ω: f(a) = f(b) for any two points a, b of Ω.

**What the original said.** The original ([[O 176 11-14]]) had no connectedness hypothesis. Without it the claim
is false: let Ω be two disjoint discs and f be 0 on one and i on the other. Re f = 0 everywhere, but f is not
constant. In the book, "open set Ω" in this chapter means a region, which is connected. The audit ([[T 176]])
labels it *stronger*, *false*, root cause **missing implicit premise**, the same kind of error as
[xⁿ − p](#/node/Artin_exercise_11_4_8). ProofNet# had the same gap ([[S 176]]).
""",
 [q("Which hypothesis did the correction add?",
    ["hconn : IsPreconnected Ω", "hΩ : IsOpen Ω", "f is bounded"], 0,
    "Line 15. IsOpen was already in the original (as h)."),
  q("Why is the claim false without connectedness?",
    ["On two disjoint discs, f can be 0 on one and i on the other: Re f is constant but f is not",
     "Holomorphic functions are never constant", "It is true anyway"], 0,
    "This is the audit's counterexample in [[T 176]]."),
  q("How does the Lean statement say 'f is constant'?",
    ["f a = f b for arbitrary points a, b of Ω", "deriv f = 0", "f = fun _ => c"], 0,
    "a and b are arbitrary points of Ω (line 14), and the conclusion is f a = f b (line 16)."),
 ],
 caveats=[STATUS_SORRY, GROUP,
          "IsPreconnected also allows Ω to be empty; for an empty Ω there are no points a, b, so nothing is lost."])
