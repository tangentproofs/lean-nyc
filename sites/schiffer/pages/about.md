# About this site

## The project

[jaumededios/Schiffer](https://github.com/jaumededios/Schiffer) is a Lean 4 formalization, built on Mathlib, of a
**planar counterexample to Schiffer's conjecture**. The README describes it as joint work of **Jaume de Dios Pont**
with **Gonzalo Cao-Labora**, formalizing their upcoming paper "Infinitely many counterexamples to Schiffer's
conjecture", and says the proof "uses a uniform bifurcation theory estimate and does not rely in any numerics". The
project's metadata file (formalization.yaml) lists Jaume de Dios Pont and OpenAI Codex as authors of the
formalization and of the proof manuscript it follows, and describes the mathematical prior work it adapts
(Fall–Minlend–Weth; Enciso–Fernández–Ruiz–Sicbaldi; Cao-Labora–Fernández).

The repository also contains a machine-generated informal write-up of the Lean proof
(`informalization/modular-proof.pdf`). The README notes that the Lean proof takes a slightly different route from the
paper, because Mathlib has no elliptic regularity theory.

### The two problems

- **Schiffer's conjecture** (Yau's problem list, Problem 80): if a bounded planar domain has a nonconstant Neumann
  eigenfunction that is constant on the boundary, the domain is a disk.
- **The Pompeiu problem**: a domain has the Pompeiu property if the only continuous function with zero integral over
  every congruent copy of the domain is zero. The Pompeiu conjecture says that among bounded simply connected domains
  with reasonable boundary, only disks (balls) fail it. Classically, Schiffer data on a domain forces it to fail the
  Pompeiu property.

## What the Lean covers

### The public statements ("comparator" files)

The project is organized for Lean's *comparator* workflow: a **challenge** file states the theorems using only
Mathlib, with `sorry` as placeholders, and a **solution** file restates them word for word and proves them. A
comparator tool can then check that the solution proves exactly the challenge statements using only the standard
axioms. (This site did not run a comparator; it compared the statement text by eye and with `diff`, see
[Trust](#/page/trust).)

- **Schiffer/Challenge.lean → Schiffer/Solution.lean.** Five theorems in a chain:
  [Schiffer_Star_Shaped](#/node/Comparator.Schiffer_Star_Shaped) →
  [Schiffer_SimplyConnected](#/node/Comparator.Schiffer_SimplyConnected);
  [SchifferToPompeiu](#/node/Comparator.SchifferToPompeiu);
  [Pompeiu_Star_Shaped](#/node/Comparator.Pompeiu_Star_Shaped) and
  [Pompeiu_SimplyConnected](#/node/Comparator.Pompeiu_SimplyConnected).
- **Schiffer/FormalConjecturesChallenge.lean → Schiffer/FormalConjecturesSolution.lean.** The Pompeiu conjecture in
  the formulation of Google DeepMind's Formal Conjectures project, shown false:
  [not_hasPompeiuProperty_imp_ball](#/node/FormalConjecturesComparator.not_hasPompeiuProperty_imp_ball).

### The construction

[exists_schifferCounterexample](#/node/exists_schifferCounterexample) (Schiffer/Main.lean) produces the domain and
function. The README's map of the source:

- `Analysis/`: reusable functional analysis, weighted sequences, jet calculus, and the bridge to the comparator form;
- `Bessel/`, `Cone/`, `ODE/`: Bessel functions (defined from scratch), the cone problem in a fixed collar, and the
  spectral analysis;
- `Bifurcation/`, `Drift/`, `Density/`, `Landing/`: the nonlinear branch, the sign of its radius drift, near-integer
  Bessel crossings, and landing at an integer radius;
- `Geometry/`, `Lift/`: the planar radial-graph domain and the unfolded field.

## What this site covers, and what it leaves out

The project is about 115,000 lines. This site explains:

- all six public headline statements and every definition they mention (the comparator vocabulary, and the
  construction's endpoint structures [SchifferCandidate](#/node/SchifferCandidate) and
  [SchifferCounterexample](#/node/SchifferCounterexample) with their geometry);
- the Schiffer-to-Pompeiu bridge, including the cutoff proof of Green's identity
  ([integral_superlevel_eq_zero_of_schiffer](#/node/Analysis.integral_superlevel_eq_zero_of_schiffer));
- the top of the construction: [the bridge to the comparator form](#/node/Analysis.SchifferCounterexample.PlanarSchifferCounterexample),
  [landing](#/node/Landing.exists_landedConeSolution), [the uniform drop](#/node/Landing.uniform_quadratic_drop),
  [near-integer crossings](#/node/Density.exists_nearIntegerCrossing), [the lift](#/node/Lift.liftLandedConeSolution)
  and [nontriviality](#/node/Lift.counterexampleOfLanded).

It **leaves out**, apart from one-paragraph outlines:

- the Bessel-function theory (`Bessel/`, about 27,000 lines: asymptotics, zeros, Debye phase, Schläfli
  representation);
- the cone nonlinear map and its uniform estimates (`Cone/`, about 44,000 lines, including the 16,000-line
  `PhysicalSolution.lean`);
- the ODE mode analysis (`ODE/`), the Lyapunov–Schmidt and bifurcation machinery (`Bifurcation/`), the curvature
  asymptotics (`Drift/`), the Kronecker density argument (`Density/`);
- the Fourier–Bessel origin series (`Lift/OriginSeries.lean`), which is also left out of this site's declaration scan
  because its names confused the scanner (see [Trust](#/page/trust));
- `Reusable/` (general results kept outside the proof's dependencies) and the `informalization/` write-up.

Those parts are where most of the mathematical difficulty lives. The descriptions of them on this site come from the
project's module READMEs and informal write-up, checked against the statements that the top-level files use. They
were not traced through the proofs.

## Where to start

Read [Schiffer_SimplyConnected](#/node/Comparator.Schiffer_SimplyConnected) for what is claimed,
[SchifferToPompeiu](#/node/Comparator.SchifferToPompeiu) for the link to Pompeiu, and
[exists_schifferCounterexample](#/node/exists_schifferCounterexample) for the shape of the construction. The
[Review](#/page/review) page discusses whether the statements say what their names claim.
