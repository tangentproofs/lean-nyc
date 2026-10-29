# Review: do the Lean statements say what the names claim?

These are our own readings of the source. They are not checked by machine and not endorsed by the author.

## The headlines in Solution.lean

**`false_of_contDiff_omega_compContinuousLinearMapCLM`** (Solution.lean lines 13–21). **Faithful.** The README and
paper claim that the general analytic statement is false. The Lean takes the general statement as a hypothesis and
proves `False`, which is exactly the refutation of a universal claim. Some points to keep in mind:

- The hypothesis quantifies over fields and spaces in universe 0 (`Type`), not over every universe. Upstream lists
  this as divergence (1) in formalization.yaml. A refutation only needs one counterexample, and it lives in `Type`, so
  nothing is lost.
- `ContDiff 𝕜 ω` is Mathlib's analytic class (ω = ⊤ in `WithTop ℕ∞`). In this Mathlib, C^ω means analytic on a
  neighbourhood of each point (`not_contDiff_omega_Q` uses `analyticOnNhd`). So "not C^ω" really is "not analytic".
- It is not vacuous. The hypothesis is not trivially false for silly reasons: over fields where (#ι)! is invertible
  the statement is true (Challenge.lean docstring). The contradiction really comes from the characteristic-2
  construction, which the second headline confirms.

**`false_of_contDiff_omega_compContinuousLinearMapCLM_charTwo_banach`** (Solution.lean lines 25–33). **Faithful and
stronger.** The hypothesis is restricted to complete ultrametric fields of characteristic 2, Banach E = E′, Banach F
and ι = `Fin 2`. Refuting a weaker hypothesis is a stronger result.

The two statements are copied verbatim from Challenge.lean. Upstream CI checks the match with
`leanprover/comparator` (comparator.json); we did not run it.

## The library theorems

**`not_analyticAt_Q`** (AltCounter/Main.lean lines 348–469). **CONDITIONAL** on `TailProperty 𝕜`, an explicit
hypothesis. The condition is not smuggled in: it is a statement about bounded 4-linear forms on ℓ^∞ that never
mentions Q or analyticity, and it is proved for the constructed field (`tailProperty_of_NSC`, `exists_field`). The
result is non-analyticity at the single point 0, which is enough to refute C^ω. The paper's reduction from any base
point to 0 is not formalized.

**`core_false`** (AltCounter/Gluing.lean lines 233–399). **CONDITIONAL** on `TailProperty 𝕜`. It is an abstract
"no such family" statement whose hypotheses are exactly the properties that `not_analyticAt_Q` derives. We could not
see a way for the hypotheses to be inconsistent for a trivial reason. The diagonal formula pins down the values when
a = b, and the other conditions are structural.

**`exists_field`** (AltCounter/Final.lean lines 12–18). **Faithful.** "Not spherically complete" is stated concretely
as `HasEmptyNestedBalls`: one nested sequence of closed balls with strictly decreasing radii and empty intersection.
That is the usual definition, and Mathlib has no standard predicate for spherical completeness to compare it with.

## Differences from the original notes

The upstream formalization.yaml lists them honestly. The two that matter for a reader:

- the notes use the completed algebraic closure of 𝔽₂((t)) and cite van der Put; the Lean builds 2-power Puiseux
  series and proves the needed direction itself;
- the notes' finite identity needs an infinite residue field; the Lean replaces that step with a hypercube sum,
  which needs no such hypothesis. The Lean's field has residue field 𝔽₂.

## Surprising or noteworthy

- The obstruction is ultrametric and needs ℓ^∞. Over c₀, or over a spherically complete field like ℚ_p, the
  tail lemma that drives the argument is not available.
- Characteristic 2 shows up three times: W(x, x) = 2x ⊗ x = 0 makes W₀ alternating; determinants of symmetric
  zero-diagonal matrices become sums of squares; and Frobenius additivity lets the hypercube sum pass through those
  squares.
- Upstream reports later work, in a separate repository, that treats characteristic p ≥ 3. This site does not cover
  it.
