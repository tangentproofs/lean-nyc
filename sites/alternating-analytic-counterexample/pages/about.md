# About this project

**alternating-analytic-counterexample** is a Lean 4 + Mathlib formalization by **Jack McCarthy**
([Deicyde on GitHub](https://github.com/Deicyde/alternating-analytic-counterexample)). It comes with a paper,
*Precomposition on continuous alternating maps is not analytic in characteristic 2* (paper/counterexample.pdf,
October 2026), and the original working notes (paper/COUNTEREXAMPLE.md). This site is an **unofficial** explainer
and is not affiliated with the author.

The upstream repository is open about how the work was made. The paper's first footnote says AI was used to help
find the result and draft the paper: the counterexample, its proof and the Lean formalization "were developed with
Claude, ChatGPT and the AutoformBot plugin". The upstream `formalization.yaml` adds that the Lean code was written by
AI agents in Claude Code at the author's direction and not edited by hand. It also says that, so far, the informal
proof has been reviewed by AI referee agents and not by a human expert in non-archimedean functional analysis.

## The question

Mathlib has continuous alternating maps Alt^ι(E, F) and the precomposition map

> f ↦ (m ↦ m ∘ (f, …, f)),  `ContinuousAlternatingMap.compContinuousLinearMapCLM`.

It is a homogeneous polynomial in f, so it is C^n for every finite n, and it is C^ω (analytic) when (#ι)! is
invertible in the field. Analytic vector bundles of alternating maps would need the C^ω version **without** that
condition. The paper asks whether it holds, and the answer is no.

## What the Lean proves

- **The headline** (Solution.lean): assuming "precomposition is C^ω for every nontrivially normed field, all normed
  spaces and every finite ι" leads to `False`. A sharper version restricts the assumption to complete ultrametric
  fields of characteristic 2, Banach spaces and 2-forms, and still refutes it.
- **The counterexample:** E = ℓ^∞(ℕ, K), F = the closed span of the matrices x ⊗ y + y ⊗ x, ι = `Fin 2`, over an
  explicit field K. That field is the completion of the 2-power Puiseux series over 𝔽₂. It is complete,
  non-archimedean, of characteristic 2 and not spherically complete.
- **Not formalized** (as upstream says itself): non-analyticity at base points other than 0, index types with more
  than two elements, and the vector-bundle consequence.

## How the proof is organised

| Part | Files | Node to start from |
|---|---|---|
| Analytic ⇒ bounded bilinear lift | AltCounter/Criterion.lean | [exists_bilinear_of_analyticAt_of_homogeneous](#/node/AltCounter.exists_bilinear_of_analyticAt_of_homogeneous) |
| The main reduction | AltCounter/Main.lean | [not_analyticAt_Q](#/node/AltCounter.not_analyticAt_Q) |
| Gluing blocks into a contradiction | AltCounter/Gluing.lean, AltCounter/DetBounds.lean | [core_false](#/node/AltCounter.core_false) |
| Characteristic-2 algebra (Pfaffians, hypercube sums) | AltCounter/Pfaffian.lean, AltCounter/Balanced.lean, AltCounter/Hypercube.lean, AltCounter/FiniteLemma.lean | [exists_block_point](#/node/AltCounter.exists_block_point) |
| Tails of multilinear forms on ℓ^∞ | AltCounter/PhillipsOne.lean, AltCounter/Phillips.lean | [tailProperty_of_NSC](#/node/AltCounter.tailProperty_of_NSC) |
| The field | AltCounter/NestedBalls.lean, AltCounter/Model.lean, AltCounter/Puiseux.lean, AltCounter/Final.lean | [exists_field](#/node/AltCounter.exists_field) |

## What this site leaves out

It explains the statement set and the main line of the proof. Many helper lemmas get no page of their own: the
truncation operators `headOf` and `tailOf`, the internals of the gliding-hump and induction-on-arity arguments in
Phillips.lean, and the Hahn-series bookkeeping in Puiseux.lean. Challenge.lean, the comparator's statement-only copy of
the headlines with `sorry`, is not scanned, so that the declaration pages use the proved versions in Solution.lean.
AltCounter/Bridge.lean (an alternative form of NSC, not used by the main theorems) and AltCounter/Check.lean
(axiom checks) are mentioned only in passing.
