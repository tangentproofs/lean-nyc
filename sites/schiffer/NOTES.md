# NOTES for the coordinator: schiffer

## Time spent

About 35 minutes of wall-clock time (05:05 to 05:40 UTC, 2026-10-29), including four full builds of about two
minutes each (scanning 115k lines is slow).

## What was produced

- 38 nodes: 6 headlines (`Comparator.Schiffer_SimplyConnected`, `Comparator.Schiffer_Star_Shaped`,
  `Comparator.SchifferToPompeiu`, `Comparator.Pompeiu_SimplyConnected`,
  `FormalConjecturesComparator.not_hasPompeiuProperty_imp_ball`, `exists_schifferCounterexample`), the full statement
  set (22 definitions), and 10 key lemmas or structures from the construction chain.
- about / review / trust pages. No Lean code blocks, no verbatim statements, no walkthrough `lean:` fields (repo has no
  licence).
- The remaining build warnings are unexplained meaning-dependencies of the *construction* nodes (e.g.
  `Cone.UniformCollarData`, `Bifurcation.UniformConeBranch`, private `Lift.*` helpers). The headline statement set is
  fully explained.

## Calls I made (logged as asked)

1. **Authors.** `site.json` had "Jaume de Dios Pont". The README says "Joint work with Gonzalo Cao-Labora", so I set
   `authors` to "Jaume de Dios Pont and Gonzalo Cao-Labora". formalization.yaml lists "Jaume de Dios Pont" and
   "OpenAI Codex" as project authors; I mention that on the About page but did not put Codex in `authors`. Please
   check this is what you want. `members` unchanged.
2. **Licence.** No LICENSE file. formalization.yaml says `license: "UNLICENSED"`, which agrees with `spdx: null`. Left as is.
3. **Headline ids point to the solution files.** Challenge.lean / FormalConjecturesChallenge.lean declare the same
   names as Solution.lean / FormalConjecturesSolution.lean. If both are scanned, the scanner gives the *challenge*
   (sorry'd) copies the clean ids and the solution copies a `'` suffix, regardless of root order. So I **excluded both
   challenge files from `roots`**. Their line references are written as explicit pinned GitHub links in bodies and
   pages (the engine only auto-links files it scanned); in quiz explanations they are plain text.
4. **Lift/OriginSeries.lean excluded from `roots`.** With it scanned, `SchifferCounterexample`'s mention of the
   structure field `field` resolved to the unrelated def `Lift.IntegerTailSeriesData.field`, pulling ~5,000 decls
   into the headline statement set, and `tools/test_statement.mjs` then failed ("Bessel.localZeroCurveIndex.rho should
   come before Bessel.localZeroCurveIndex.ZeroChart", a meaning-dep cycle in the bloated set). Engine issues worth
   fixing: (a) structure-field projections like `x.field` resolved by suffix to an unrelated decl; (b) the
   real-data ordering test can't cope with meaning-dependency cycles, though the synthetic test says cycles are allowed;
   (c) duplicate decl names across files get `'` suffixes by file order with no way to choose.
5. **Scope.** Large analytic directories (Bessel, Cone, ODE, Bifurcation, Drift, Density, about 95k lines) are outlined
   from the module READMEs and `informalization/parts/01_main_theorem.tex`, not traced. The About page says so.

## Where I am least sure

- **`exists_schifferCounterexample` and `Lift.liftLandedConeSolution`:** the six-step story (cones, uniform branch,
  drift, density, landing, unfolding plus origin series) comes from the informal write-up and READMEs. The specific
  Lean claim that the origin series "matches the collar solution to second order across an interface circle" is my
  paraphrase of the Lift README and the names in Lift/Solution.lean; I didn't read OriginSeries.lean.
- **`Cone.Crossing`:** the explanation of why J₁(ρ) = 0 and J_R(ρ) = 0 give a bifurcation point comes from the
  write-up's introduction, not the Lean. Also: the `J1_zero` condition makes the radial solution satisfy the Neumann
  condition because J₀′ = −J₁; that's standard but I didn't find where the Lean proves it.
- **`Landing.uniform_quadratic_drop`:** "radius(σ) ≤ R − κσ²/4" is my reading of Schiffer/Landing/UniformDrop.lean lines 119–121 (κ = γmin/2,
  η = κσ²/4); the Taylor step itself wasn't traced.
- **`Density.exists_nearIntegerCrossing`:** the Kronecker/torus summary is from the Density README. `oneZero n` is
  "a selected positive zero of J₁", not necessarily the n-th; I worded it that way.
- **`Analysis.integral_superlevel_eq_zero_of_schiffer`:** the walkthrough's line ranges for the limit argument
  (366–425, 426–496) are grouped by reading the `have` names, not every step.
- **`radialGraphDomain` non-disk argument:** the first half (the 2π/N rotation fixes the ball's centre, so it is 0)
  is read from the Lean; "a nonconstant radius is not a circle" is my summary of lines ~530–559.
- **`SchifferToPompeiu` naming note:** I say the docstring's "Pompeiu implies Schiffer, in contrapositive" and the
  literal statement describe the same implication. That's right as logic, but the classical attribution
  (Brown–Schreiber–Taylor for this direction, Williams for the converse) is from the write-up's citations and my own
  background, not checked further.
- **Formal Conjectures fidelity:** I didn't compare the definitions with the actual
  google-deepmind/formal-conjectures file (no network fetch). The review page says so.

## Things the author might object to

- **Framing.** The lead and review call this a counterexample to Schiffer's conjecture and say "if correct, this
  settles a long-standing conjecture". That's accurate to the README and statement, but the authors might prefer more
  (or less) caution while the paper is unpublished. Every headline carries the "not built" caveat.
- **Authors line.** Including Cao-Labora in `authors`, and mentioning "OpenAI Codex" from formalization.yaml on the
  About page.
- **"Machine-generated" informalization.** I repeat the README's own words for the PDF; nothing stronger.
- **The excluded files** (challenge files, OriginSeries.lean) don't appear in the source index. That's a tooling
  workaround, not a judgement on those files. The trust page explains it.
- The comparator check was **not** run; I only did a textual `diff` of the challenge and solution statements
  (identical apart from one docstring).
