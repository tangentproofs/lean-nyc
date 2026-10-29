# About this site

## The project

[Aaron1011/gromov](https://github.com/Aaron1011/gromov) is a Lean 4 formalization, built on Mathlib, of
**Gromov's theorem on groups of polynomial growth**, by **Aaron Hill**. The repository's README is just the title.
The commit history (about 1,500 commits, May 2025 to August 2026) has a single author. Aaron presented the work at
Lean NYC on 30 August 2026 in the talk
[Formalizing Gromov's theorem on groups of polynomial growth in Lean](https://lean.nyc/blog/formalizing-gromovs-theorem).

### The theorem

Fix a finite generating set *S* of a group *G*. Let *γ*(*n*) be the number of elements you can write as products of
at most *n* letters from *S* ∪ *S*⁻¹. *G* has **polynomial growth** if *γ*(*n*) ≤ *C*·*n<sup>d</sup>* for some
constants. Gromov (1981) proved:

> A finitely generated group of polynomial growth is **virtually nilpotent**: it has a nilpotent subgroup of finite
> index.

The converse, that virtually nilpotent groups have polynomial growth, is older and easier (Wolf, Bass, Guivarc'h).
It is **not** part of this project.

## What the Lean covers

* **The headline** [gromov_forward](#/node/FormalConjecturesCheck.gromov_forward) states the theorem with
  definitions copied from Google DeepMind's
  [Formal Conjectures](https://github.com/google-deepmind/formal-conjectures) repository, where the full "iff" is an
  open `sorry`. It proves the forward direction.
* **The project's own main theorem** [main_gromov_theorem](#/node/main_gromov_theorem) proves the same thing inside
  the project's [Generates](#/node/Generates) setting, by induction on the growth degree.
* **The proof spine**, as described on the [Roadmap](#/roadmap): non-constant Lipschitz harmonic functions exist; there
  are only finitely many dimensions of them; *G* therefore acts on a finite-dimensional space by isometries; compact
  linear groups of polynomial growth are virtually abelian; this yields a finite-index subgroup mapping onto ℤ; and
  the kernel has smaller growth degree, which closes the induction.

A text search finds no live `sorry` anywhere (see [Trust](#/trust)).

### Which route the proof takes

There are three classical routes to Gromov's theorem:

1. Gromov's original proof, via asymptotic cones and the Montgomery–Zippin solution of Hilbert's fifth problem.
2. Kleiner's 2007 proof, via **Lipschitz harmonic functions** and a Colding–Minicozzi-style finite-dimensionality
   theorem, together with Shalom–Tao's quantitative refinement.
3. Ultrafilter/approximate-group proofs (Hrushovski, Breuillard–Green–Tao).

This project takes **route 2**, in the form of **Tao's 2010 blog post** "A proof of Gromov's theorem". The Lean NYC
talk page says so. Code comments cite Tao's post (Gromov/ThreeTwoGrowth.lean line 110) and number their results after
a thesis they call "Vikman" (Theorem 3.1, 3.6, 3.8, 3.23, …), which writes up Kleiner's and Tao's argument. The
repository also keeps a list of corrections to that thesis (Gromov/vikman_errata.txt). There is no Hilbert fifth
problem, no asymptotic cone and no Tits alternative. The compact-group step is proved by hand for subgroups of U(*n*),
and the step "polynomial growth ⇒ eigenvalues on the unit circle" is proved directly for integer matrices.

## Where to start

Read [gromov_forward](#/node/FormalConjecturesCheck.gromov_forward), then the [Roadmap](#/roadmap). The
[Review](#/review) page discusses how faithful each headline statement is.

## What this site leaves out

The project is large, so this site explains the statements and the dependency spine and only outlines the heavy
estimates. Not explained node by node:

* the packing and scale-selection machinery behind Theorem 3.23 (Gromov/Packing.lean, Gromov/VWrapper.lean,
  Gromov/BoundedDoubling.lean, Gromov/QuadraticForm.lean, Gromov/Lemma326.lean, Gromov/CutoffInequality.lean);
* the ℓ² spectral theory of the Laplacian (Gromov/Harmonic/SelfAdjoint.lean and neighbours);
* the word counting in U(*n*) (Gromov/Unitary/);
* the commutator calculus in Gromov/Unipotent/;
* the `poly_tendsto` tactic (Gromov/TendstoTactic.lean);
* the `ToMathlib/` helper lemmas;
* the vendored Carleson-project convolution inequalities (Gromov/Vendor/).

Gromov/VWrapper.lean is deliberately left out of the declaration scan. See [Trust](#/trust) for why.
