# Review: do the statements say what they claim?

For each headline: what it claims by name and docstring, what the Lean statement actually says, and anything worth
flagging. Nothing below was checked by building the code; "proved" means the source contains a complete-looking proof
with no `sorry` in the files it imports.

## Schiffer_Star_Shaped and Schiffer_SimplyConnected: faithful, proved

- **Claim:** a counterexample to Schiffer's conjecture, star-shaped (respectively simply connected).
- **Statement** (Schiffer/Solution.lean lines 64–75 and 92–103): a bounded nonempty Ω ⊂ ℂ, star-shaped about 0
  (respectively path connected and simply connected), with [C² boundary](#/node/Comparator.HasC2Boundary), not a
  [disk](#/node/Comparator.IsEuclideanDisk), and *u* C² on the whole plane with −Δ*u* = *u* in Ω and *u* = 1,
  ∇*u* = 0 on the frontier of Ω.
- **Faithfulness.** This matches the standard formulation:
  - The eigenvalue is normalized to 1. That is no loss, because rescaling the domain rescales the eigenvalue.
  - Requiring the whole gradient to vanish is equivalent to the Neumann condition, since *u* is constant along the
    boundary.
  - Nonconstancy of *u* is not stated but follows: a constant *u* would be 0 in Ω and hence 0 on the boundary.
  - *u* is required to be C² on all of ℂ, which is stronger than the usual C² up to the boundary.
  - The C² boundary notion (a global defining function with 0 a regular value) is the standard one.
  - The disk notion allows nonpositive radii (empty set), which is harmless for nonempty Ω.
  - Mathlib's Laplacian on ℂ is the real Laplacian ∂²/∂*x*² + ∂²/∂*y*²; the file cites the Mathlib lemma confirming
    this (Schiffer/Solution.lean lines 45–49).
- **What it doesn't say.** Nothing about *how many* counterexamples there are (the paper title says "infinitely many";
  the Lean statement is existence of one). Nothing about analyticity of the boundary, which the informal write-up
  derives from classical free-boundary theory outside Lean.
- **Surprise level:** high. If correct, this settles a long-standing open conjecture in the negative, in the
  strongest natural class of domains. That is a reason to want the build and comparator check re-run independently,
  not a reason to doubt the statement's wording. The statement itself is clean, short and Mathlib-only.

## SchifferToPompeiu: faithful, proved

- **Claim:** the classical bridge "Schiffer data ⇒ the Pompeiu property fails".
- **Statement** (Schiffer/Solution.lean lines 311–323): for any bounded Ω with C² boundary carrying Schiffer data,
  there is a continuous nonzero *f* with ∫ over *g*(Ω) of *f* = 0 for every bijective affine isometry *g*.
- **Faithfulness.** This is the standard implication (Brown–Schreiber–Taylor; Williams). Rigid motions include
  reflections, matching the classical Pompeiu problem. The integrals are of a continuous bounded function over a
  bounded open set, so Lean's convention of returning 0 for non-integrable functions plays no role.
- **Naming note.** The docstring calls it "Pompeiu implies Schiffer" in contrapositive form. Read literally, it is
  "Schiffer data implies Pompeiu fails". Both phrasings describe the same implication; the harder converse (Williams)
  is not formalized and not needed.

## Pompeiu_Star_Shaped and Pompeiu_SimplyConnected: faithful, proved

- **Statement** (Schiffer/Solution.lean lines 329–340 and 351–363): a non-disk domain with the listed properties and
  one continuous nonzero *f* integrating to zero over every rigid copy. This is precisely the failure of the Pompeiu
  property for a bounded simply connected C² domain that is not a disk, i.e. a counterexample to the planar Pompeiu
  conjecture.

## not_hasPompeiuProperty_imp_ball: faithful refutation, proved, dimension 2 only

- **Claim:** "the hard direction of the Pompeiu conjecture is false" in the Formal Conjectures formulation.
- **Statement** (Schiffer/FormalConjecturesSolution.lean lines 446–448): it is not the case that for every *N* and
  every admissible Ω ⊂ ℝ^{*N*+1}, failing the Pompeiu property implies being a ball.
- **Faithfulness.** Refuting a "for all dimensions" claim needs one dimension; the proof uses ℝ². Nothing is said
  about dimensions 3 and higher, and the docstring doesn't suggest otherwise. The
  [admissibility conditions](#/node/FormalConjecturesComparator.IsAdmissibleDomain) are the usual ones (bounded,
  open, connected, simply connected, Lipschitz boundary).
- **Not checked here:** whether these definitions agree with the current file in google-deepmind/formal-conjectures.
  The challenge header says they follow it, keeping only one direction of the original equivalence.

## exists_schifferCounterexample: proved; the large analytic core was not reviewed

- **Statement** (Schiffer/Main.lean line 8): the structure [SchifferCounterexample](#/node/SchifferCounterexample)
  has an inhabitant.
- **Faithfulness of the structure.** [SchifferCandidate](#/node/SchifferCandidate) asks for everything a Schiffer
  solution needs on an explicit radial-graph domain, with a positive eigenvalue and a field C² on a neighbourhood of
  the closed domain. `SchifferCounterexample` adds a nonconstant profile, nonconstant field and non-disk domain. The
  structure fields are actual mathematical conditions, not certificates that could be filled in trivially. The bridge
  to the plain comparator statement is itself proved
  ([PlanarSchifferCounterexample](#/node/Analysis.SchifferCounterexample.PlanarSchifferCounterexample)), so the
  comparator statements do not depend on trusting this structure's design.
- **What this review did not do:** follow the ~100,000 lines of Bessel, cone, ODE and bifurcation estimates. Their
  correctness is exactly what a successful Lean build would certify. The upstream metadata says a full build
  succeeded with only the standard axioms (`propext`, `Quot.sound`, `Classical.choice`); this site did not
  reproduce that.

## Overall

The public statements are short, Mathlib-only and say what their names claim. No headline is conditional: none
takes extra hypotheses, and the two `sorry`s in the Schiffer challenge file are exactly the ones the solution file
fills. The trust question is entirely about whether the proofs check, which needs a build (see [Trust](#/page/trust)).
