# Review: do the statements say what they claim?

For each headline: what it claims by name, what the Lean statement says, and anything worth flagging. Nothing below
was checked by building the code. "Proved" means the source contains a complete-looking proof and no `sorry` appears
anywhere in the project.

## General remarks on the model

- **Real plane, no paper.** Points are pairs of reals and a fold reflects the whole plane. The classical Huzita–Hatori
  axioms are about folding a sheet; here they become statements about lines and reflections. That is the standard
  mathematical reading, but it means nothing is said about a crease actually crossing a finite square, or about
  which flap moves.
- **Canonical lines.** Lines are normalised (*a* = 1, or *a* = 0 and *b* = 1), and the project proves that two lines with
  the same points are equal ([Line.eq_of_on_line](#/node/Line.eq_of_on_line)). So the uniqueness ("exactly one")
  statements mean what they should.
- **Definitions are formulas.** The reflection maps are given by formulas. The project proves the properties that
  justify them (involutive, distance-preserving, fixes exactly the crease, maps lines to the set of reflected points),
  so they are not merely asserted to be reflections.

## huzita_2: faithful, proved

- **Claim:** Huzita's second axiom: a unique fold places one point onto another.
- **Statement** (Origami/lightweight_definitions/Huzita_axioms.lean lines 52–53): for distinct points, there is exactly
  one fold whose reflection sends the first to the second.
- **Faithful.** The hypothesis that the points differ is necessary, as the project shows
  (Origami/lightweight_definitions/Sharpness.lean lines 32–39).

## huzita_5_iff: faithful and sharper than the classical axiom, proved

- **Claim:** Huzita's fifth axiom together with its exact condition.
- **Statement** (Sharpness.lean lines 5–7): a fold through *p*₂ placing *p*₁ onto *l*₁ exists if and only if the squared
  distance from *p*₂ to *l*₁ is at most the squared distance between *p*₁ and *p*₂.
- **Faithful.** Squared distances are used to avoid square roots; the comparison is equivalent to the one with ordinary
  distances. The existence direction alone is `huzita_5`. The number of solutions (up to two) is not addressed.

## huzita_6: faithful as an existence statement under a sufficient hypothesis, proved

- **Claim:** Huzita's sixth axiom (the Beloch fold).
- **Statement** (Huzita_axioms.lean lines 284–285): for crossing (non-parallel) lines *l*₁, *l*₂ and any points *p*₁,
  *p*₂, some fold places *p*₁ onto *l*₁ and *p*₂ onto *l*₂.
- **Notes.**
  - "Not parallel" is a **sufficient** condition, not a characterisation. Some parallel configurations also admit
    such a fold (for instance when each point already lies on its line), and they are not covered.
    `huzita_6_needs_not_parallel` (Sharpness.lean lines 133–140) only shows that the unrestricted statement is false.
  - Only existence is claimed (there can be up to three such folds).
  - The cubic is solved by the intermediate value theorem, so the proof is non-constructive. Nothing in the project
    connects this to angle trisection or cube duplication; that remark on this site is background.

## huzita_7_iff: faithful, proved

- **Claim:** Huzita's seventh axiom with its exact condition.
- **Statement** (Sharpness.lean lines 97–98): there is **exactly one** fold placing *p* onto *l*₁ and perpendicular to
  *l*₂ if and only if *l*₁ and *l*₂ are not parallel.
- **Faithful.** Note that it characterises *unique* existence: for parallel lines there are either none or infinitely
  many such folds, and both cases are proved.

## haga_first_theorem: faithful (to the line version), proved, no axioms

- **Claim:** Haga's first theorem.
- **Statement** (Origami/lightweight_definitions/Haga.lean lines 60–67): for any fold sending (1, 0) to (1/2, 1), the
  reflection of the line *y* = 0 passes through (0, 1/3).
- **Notes.** This is the geometric content of Haga's theorem (the folded bottom edge meets the left edge a third of
  the way up). The statement is about the infinite reflected line, and the square is never modelled, so the fact that
  this intersection lies on the actual folded edge is not part of the statement. A point (0, 0) is named in the
  statement but unused.

## haga_gen_equation: faithful, proved, no axioms

- **Claim:** a one-parameter generalisation of Haga's theorem.
- **Statement** (Haga.lean lines 118–124): for rational 0 < *n* < 1 and any fold sending (1, 0) to (*n*, 1), the
  reflection of *y* = 0 passes through (0, *n*/(2 − *n*)).
- **Notes.** At *n* = 1/2 it gives 1/3. A spot check of the formula with floating point at *n* = 0.3, 0.5, 0.8 agreed.
  The parameter is rational rather than real, which is a mild restriction.

## Non-headline but worth knowing: haga_result is CONDITIONAL

[haga_result](#/node/haga_result) (Haga.lean lines 103–116) says the fold produced by the generated construction has
the Haga property. It depends on five Lean `axiom`s: the generated points `p1`, `p2`, the generated hypothesis `hyp1`,
and two hand-added axioms `p1_coords`, `p2_coords` fixing the points' coordinates (Haga.lean lines 10–11, 20, 50–51).
These are jointly satisfiable, so they do not make the system inconsistent, but the result is conditional on them.
The generated construction itself ([haga_construction](#/node/haga_construction)) has the statement `True`; its point
is that the generated proof script type-checks.
