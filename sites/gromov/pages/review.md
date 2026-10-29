# Review: do the statements say what their names claim?

The Lean was **not built** for this site. This review compares the statements as written in the source with the
classical claims.

## gromov_forward: faithful, forward direction only

[gromov_forward](#/node/FormalConjecturesCheck.gromov_forward) (Gromov/FormalConjecturesCheck.lean lines 152–181)
assumes only that *G* has polynomial growth in the
[Formal Conjectures sense](#/node/FormalConjecturesCheck.HasPolynomialGrowth). That is: a finite generating set *S*,
real *C* > 0 and natural *d* with |ball(*n*)| ≤ *C*·*n<sup>d</sup>* for all *n* > 0. It concludes Mathlib's
`Group.IsVirtuallyNilpotent G`. This is exactly the classical hard direction of Gromov's theorem.

* The three definitions are stated to be verbatim copies of the Formal Conjectures ones (lines 7–13). This site did
  not diff them against that repository.
* **Only one direction.** Formal Conjectures states an "iff". The converse is not proved (lines 24–26), so the
  Formal Conjectures `sorry` is not fully discharged. The file says this itself.
* `gromov_forward_fg` adds the reference's redundant "finitely generated" hypothesis to match its signature exactly.

## main_gromov_theorem: faithful in its setting

[main_gromov_theorem](#/node/main_gromov_theorem) (Gromov/Gromov.lean lines 996–1024) is stated inside the
[Generates](#/node/Generates) class, which assumes the group is infinite, gives a symmetric generating set containing 1,
and includes a polynomial-growth assumption. The explicit hypothesis is growth of a specific degree,
|*S<sup>n</sup>*| ≤ *a*·*n<sup>d</sup>* with natural *a*. With 1 ∈ *S* and *S* symmetric, *S<sup>n</sup>* is the
word-metric ball, so this is the standard statement for infinite groups. Finite groups are easy, and
gromov_forward handles them. Nothing in `Generates` smuggles in nilpotency or a map onto ℤ.

A comment at lines 994–995 wonders whether "polynomial growth" should use *S* ∪ *S*⁻¹. In this setting *S* is already
symmetric, and the Formal Conjectures bridge makes the question moot.

## The spine theorems

* [exists_nontrivial_harmonic](#/node/exists_nontrivial_harmonic): "a Lipschitz harmonic function that is not
  constant". This is Kleiner's existence statement. Harmonic uses the lazy average over *S* ∋ 1, which has the same
  harmonic functions. Faithful.
* [Lipschitz_finite_dimensional](#/node/Lipschitz_finite_dimensional): the space of Lipschitz harmonic functions is
  finite-dimensional. Faithful to Kleiner's theorem. Polynomial growth is an *implicit* hypothesis through the
  `Generates` instance, which a reader of the statement alone could miss.
* [compact_lie_virtually_abelian](#/node/compact_lie_virtually_abelian): the name says "compact Lie", and the statement
  is about finitely generated polynomial-growth subgroups of **U(*n*)**. That is the case the proof needs: every compact
  linear group embeds in U(*n*) by the [unitarian trick](#/node/new_weyl_unitarian_trick), and
  [theorem_3_8_real](#/node/theorem_3_8_real) states the general compact-linear version. Not weaker than needed, but
  narrower than "compact Lie groups" in general.
* [theorem_3_1](#/node/theorem_3_1): **CONDITIONAL by design.** It takes the inductive hypothesis (Gromov's theorem in
  degree *d* − 1) as an explicit assumption. main_gromov_theorem discharges it by induction, so the final result is
  unconditional.
* [theorem_3_23](#/node/theorem_3_23) uses a "tends to 0" growth condition where the source uses "liminf < ∞"
  (comment at Gromov/QuadraticForm.lean line 106). It is an internal lemma, and its hypothesis is verified where it is
  used.

## Surprises worth knowing

* **A list of errata.** Gromov/vikman_errata.txt records places where the thesis the formalization follows is
  imprecise. Examples: a missing square in Proposition 3.18, and a bound in the proof of Theorem 3.23 that is false
  for un-normalized *u*. It compares these with Kleiner's paper and Tao's post. The Lean proofs take the corrected
  routes. This site did not check the errata's mathematics.
* The degree-0 base case never uses the contradiction with "G is infinite". It just exhibits the trivial subgroup.
* The kernel step relies on *S* containing 1, so "length exactly *n*" and "length at most *n*" agree. A comment
  (Gromov/ThreeTwoGrowth.lean lines 110–112) notes a correction to the source on this point.
