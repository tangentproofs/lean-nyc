NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]

SKIMMED = ("The large analytic files behind this step were not read line by line for this site. The description follows "
           "the module README and the informal write-up, checked against the statement and the top-level proof.")


node("Comparator.Pompeiu_Star_Shaped",
 "Pompeiu, star-shaped version",
 "The star-shaped counterexample domain also fails the Pompeiu property: one nonzero continuous function integrates to "
 "zero over every rigid copy of it.",
 r"""## Plain English

**Theorem (`Pompeiu_Star_Shaped`, Schiffer/Solution.lean lines 329–347).** There is a bounded, nonempty set Ω,
star-shaped about the origin, with [C² boundary](#/node/Comparator.HasC2Boundary), not a
[disk](#/node/Comparator.IsEuclideanDisk), and a continuous nonzero *f* whose integral over every rigid image of Ω is
zero.

The proof takes the [star-shaped Schiffer counterexample](#/node/Comparator.Schiffer_Star_Shaped) and applies the
[Schiffer-to-Pompeiu bridge](#/node/Comparator.SchifferToPompeiu) to it. It is the star-shaped twin of
[Pompeiu_SimplyConnected](#/node/Comparator.Pompeiu_SimplyConnected).
""",
 [q("Which two results does this theorem combine?",
    ["The star-shaped Schiffer counterexample and the Schiffer-to-Pompeiu bridge",
     "The Formal Conjectures statement and the cone construction",
     "Two numerical computations"], 0,
    "Schiffer/Solution.lean lines 341–347.")])


node("Analysis.SchifferCounterexample.PlanarSchifferCounterexample",
 "Bridge: from the constructed witness to the plain statement",
 "Turns the constructed SchifferCounterexample (eigenvalue λ, field C² only near the domain, normal-derivative "
 "condition) into the plain form the comparator wants (eigenvalue 1, field C² on the whole plane, full gradient zero "
 "on the boundary), by rescaling and a smooth cutoff.",
 r"""## Plain English

**Theorem (`PlanarSchifferCounterexample`, Schiffer/Analysis/SchifferCounterexample.lean lines 956–969).** The same
statement as the [star-shaped headline](#/node/Comparator.Schiffer_Star_Shaped), but with "star-shaped", "C²
boundary" and "disk" written out by hand in this file (lines 41–56) instead of using Mathlib's names.

This file is the bridge between the construction's internal format,
[SchifferCounterexample](#/node/SchifferCounterexample), and a statement that mentions nothing but Mathlib. The
differences it has to remove:

| Construction gives | Comparator wants | How it is bridged |
|---|---|---|
| −Δ*u* = λ*u* for some λ > 0 | −Δ*u* = *u* | shrink the domain by the factor √λ and compose *u* with the inverse scaling (lines 597–633, 743–816) |
| *u* is C² near the closed domain | *u* is C² on the whole plane | multiply by a smooth cutoff equal to 1 near the closed domain (lines 876–912) |
| boundary given as *r* = *N* − *h*(*N*φ) | a global C² defining function *F* | build *F* from the polar radius and a bump (lines 152–505) |
| zero normal derivative | full gradient zero | the tangential derivative vanishes because *u* is constant along the boundary (lines 506–596) |
| radial-graph domain is not a disk | rescaled domain is not a disk | scaling maps disks to disks (lines 713–742) |
""",
 [q("Why does the bridge rescale the domain?",
    ["To change the eigenvalue λ to 1", "To make the domain star-shaped", "To make the boundary C²"], 0,
    "Scaling by √λ turns −Δu = λu into −Δu = u (Schiffer/Analysis/SchifferCounterexample.lean lines 597–633)."),
  q("How does the bridge get a field that is C² on the whole plane?",
    ["It multiplies the field by a smooth function equal to 1 near the closed domain and 0 far away",
     "It solves the PDE on the whole plane", "It assumes it"], 0,
    "Schiffer/Analysis/SchifferCounterexample.lean lines 876–912, using Mathlib's smooth bump functions."),
 ],
 caveats=["Not built for this site."],
 widgets=walk("How the proof goes (Schiffer/Analysis/SchifferCounterexample.lean, lines 914-969)", [
  {"text": "Get a SchifferCounterexample c from the construction (line 967).", "link": "exists_schifferCounterexample"},
  {"text": "Extend c's field to a C² function on the whole plane that agrees with it near the closed domain (line 931, using lines 876–912)."},
  {"text": "Let Ω be the domain scaled by √λ and u the extended field composed with the inverse scaling (lines 932–933)."},
  {"text": "Check bounded, nonempty and star-shaped, which survive scaling (lines 935–937)."},
  {"text": "Supply the defining function for the C² boundary (lines 938–941).", "link": "Comparator.HasC2Boundary"},
  {"text": "Not a disk, because scaling preserves disks (line 942)."},
  {"text": "u is C²; −Δu = u in Ω; u = 1 and ∇u = 0 on the frontier (lines 943–950)."},
 ]))


node("Analysis.integral_superlevel_eq_zero_of_schiffer",
 "Key lemma: Green's identity by cutoffs",
 "If w vanishes to second order on the boundary of a bounded C² domain and Δw + w = 1 inside, then every solution of "
 "Δv + v = 0 has integral zero over the domain. The proof avoids boundary integrals by smoothing w off near the "
 "boundary and letting the smoothing width go to zero.",
 r"""## Plain English

**Theorem (`integral_superlevel_eq_zero_of_schiffer`, Schiffer/Analysis/SchifferCutoff.lean lines 296–496).** Let
Ω = {*F* > 0} be bounded, where *F* is C² and its derivative is nonzero wherever *F* = 0, and assume the zero set of
*F* is nonempty. Let *g* and *v* be C² functions on the plane with

- Δ*g* + *g* = 1 in Ω,
- Δ*v* + *v* = 0 in Ω,
- *g* = 0 and the derivative of *g* is zero wherever *F* = 0.

Then the integral of *v* over Ω is zero.

In [SchifferToPompeiu](#/node/Comparator.SchifferToPompeiu), *g* = 1 − *u* and *v* is a rotated plane wave.

### Why this is true

Formally: ∫_Ω *v* = ∫_Ω *v*(Δ*g* + *g*) = ∫_Ω *g*(Δ*v* + *v*) = 0, where the middle step is Green's second identity
and the boundary terms vanish because *g* and ∇*g* vanish on the boundary.

### Why the proof is long

Mathlib does not have Green's identity on a C² domain. The proof uses instead the cutoffs
*w*_ε = *g* · η(*F*/ε), where η is Mathlib's smooth transition from 0 to 1. Each *w*_ε is C² with compact support
inside Ω, so whole-plane integration by parts (no boundary) gives ∫ *v*(Δ*w*_ε + *w*_ε) = ∫ *w*_ε(Δ*v* + *v*) = 0.
Then:

- far inside Ω, *w*_ε = *g*, so the residual Δ*w*_ε + *w*_ε equals 1;
- outside Ω it is 0;
- in the thin layer 0 < *F* ≤ ε it is bounded by a constant independent of ε, because *g* vanishes quadratically at
  the boundary (this is where both *g* = 0 and ∇*g* = 0 are used).

So the residual tends to the indicator of Ω with a uniform bound, and dominated convergence turns the zeros into
∫_Ω *v* = 0.
""",
 [q("Why are both g = 0 and ∇g = 0 on the boundary needed?",
    ["So that g vanishes quadratically there, which keeps the cutoff residual bounded as ε → 0",
     "Only g = 0 is needed; the other is decoration",
     "To make Ω star-shaped"], 0,
    "The quadratic control lemma is used at Schiffer/Analysis/SchifferCutoff.lean lines 316–317; without it the cutoff's derivatives would blow up like 1/ε."),
  q("What replaces the boundary integrals of the classical Green identity?",
    ["Compactly supported cutoffs and a limit by dominated convergence", "Numerical quadrature", "An axiom"], 0,
    "Schiffer/Analysis/SchifferCutoff.lean lines 296–496."),
 ],
 caveats=["Not built for this site. The summary of lines 330–496 (the limiting argument) was read at the level of its main steps, not every estimate."],
 widgets=walk("How the proof goes (Schiffer/Analysis/SchifferCutoff.lean, lines 296-496)", [
  {"text": "The closure K of Ω is compact and meets the zero set of F (lines 308–315)."},
  {"text": "Near the boundary, |g| is at most C times F², from g = 0 and Dg = 0 there (lines 316–317)."},
  {"text": "Uniform bounds for the smooth step η, for F's first two derivatives on K, for g's second derivative and for v (lines 318–343)."},
  {"text": "Define cutoffs w_n = g · η(F/ε_n) with ε_n → 0 and their residuals Δw_n + w_n (lines 344–365)."},
  {"text": "The residual is bounded by one constant H everywhere, is 0 outside K, and converges pointwise to the indicator of Ω (lines 366–425)."},
  {"text": "Integrate by parts on the whole plane for each n, then pass to the limit by dominated convergence to get the integral of v over Ω equals 0 (lines 426–496)."},
 ]))


node("Landing.LandedConeSolution",
 "A cone solution landed at an integer radius",
 "The data handed from the cone construction to the planar lift: a uniform branch of cone solutions through a Bessel "
 "crossing, an integer N, and a nonzero amplitude at which the branch's cone radius is exactly N.",
 r"""## Plain English

**Structure (`LandedConeSolution`, Schiffer/Landing/IntegerRadius.lean lines 13–34).** It bundles:

- `uniform`: fixed collar data (a collar width *L* and a threshold *R*₀ beyond which all estimates are uniform);
- `N`: an integer with *N* ≥ 2 and *N* ≥ 2*L*;
- `crossing`: a **crossing** (*R*, ρ): ρ > 0 is simultaneously a zero of the Bessel function *J*₁ and a zero of *J*_*R*
  (Schiffer/Cone/CollarParameters.lean lines 14–22), with *R* ≥ *R*₀ and ρ²/*R*² between 2 and 3;
- `branch`: a uniform C³ branch of solutions of the cone equation through that crossing, parametrized by an amplitude
  *a*, with cone radius `radius a` and state `state a` (Schiffer/Bifurcation/UniformBranch.lean lines 14–56);
- `amplitude`: a **nonzero** amplitude inside the branch's interval with **`radius` equal to *N***;
- side conditions used by the lift: ρ²/*N*² is in [2, 3], certain Bessel values *J*_{*kN*}(ρ(1 − *L*/*N*)) are nonzero,
  and the boundary profile is smaller than 1/2 in absolute value.

On the cone with reciprocal aperture *R*, the radial solution *J*₀(ρ(1 − *x*/*R*))/*J*₀(ρ) exists whenever *J*₁(ρ) = 0;
a crossing is where the first angular mode also becomes resonant, so a nonradial branch can bifurcate. "Landed" means
the branch has reached a cone that is exactly the plane divided by an *N*-fold rotation.

The Bessel function *J* is defined in the project from its power series (Schiffer/Bessel/Basic.lean lines 103–108
and 2289), not assumed.
""",
 [q("What does it mean that the branch has 'landed'?",
    ["At some nonzero amplitude, the cone radius on the branch is exactly the integer N",
     "The amplitude is zero",
     "The crossing radius R is an integer"], 0,
    "Field radius_integer (Schiffer/Landing/IntegerRadius.lean line 27). The crossing radius R itself is just above N, not equal to it."),
  q("Why must the amplitude be nonzero?",
    ["At amplitude 0 the solution is the radial one, which would unfold to a disk",
     "Because Lean forbids zero", "To keep the radius positive"], 0,
    "The state at amplitude 0 is 0 (state_zero in UniformConeBranch), i.e. the unperturbed radial solution."),
 ],
 caveats=[SKIMMED])


node("Landing.exists_landedConeSolution",
 "Landing: some branch reaches an integer radius",
 "There is a cone branch that lands at an integer radius. Its crossing starts just above an integer N, the branch "
 "radius falls by a fixed amount, and the intermediate value theorem finds an amplitude where it equals N exactly.",
 r"""## Plain English

**Theorem (`exists_landedConeSolution`, Schiffer/Landing/IntegerRadius.lean lines 36–157).** A
[LandedConeSolution](#/node/Landing.LandedConeSolution) exists.

### The argument

It combines two results:

1. **[Uniform drop](#/node/Landing.uniform_quadratic_drop).** There are positive numbers σ and η, and a threshold,
   such that for *every* crossing (*R*, ρ) beyond that threshold with ρ²/*R*² in [2, 3], the branch through it has
   radius *R* at amplitude 0 and at most *R* − η at amplitude σ.
2. **[Near-integer crossing](#/node/Density.exists_nearIntegerCrossing).** For any δ > 0 and any lower bound, there is
   a crossing with *N* < *R* < *N* + δ for some large integer *N*.

Choose δ ≤ η. Then the branch radius starts at *R* > *N* and ends at most *R* − η < *N*. It is continuous, so by the
intermediate value theorem it equals *N* at some amplitude *a* between 0 and σ. And *a* ≠ 0, because at 0 the radius is
*R* ≠ *N*.

The key point is that η does not depend on the crossing. That is why the project works so hard on *uniform* estimates:
the density argument can only promise crossings close to an integer, not how close relative to a crossing-dependent
drop.
""",
 [q("Why must the drop η be independent of the crossing?",
    ["Because δ must be chosen below η before the near-integer crossing is picked",
     "Because η must be an integer", "It doesn't have to be"], 0,
    "The proof picks δ = min(η, 1) from the uniform drop first, then calls the density theorem with δ (Schiffer/Landing/IntegerRadius.lean lines 37–50)."),
  q("Which classical theorem finds the landing amplitude?",
    ["The intermediate value theorem", "The implicit function theorem", "The Banach fixed point theorem"], 0,
    "Schiffer/Landing/IntegerRadius.lean lines 113–114."),
  q("Why is the landing amplitude nonzero?",
    ["At amplitude 0 the radius is R, which is strictly larger than N", "Because σ > 0", "By assumption"], 0,
    "Schiffer/Landing/IntegerRadius.lean lines 117–123."),
 ],
 caveats=["Not built for this site. The top-level proof was read in full; the two results it combines were not."],
 widgets=walk("How the proof goes (Schiffer/Landing/IntegerRadius.lean, lines 36-157)", [
  {"text": "Get uniform collar data, a threshold, an amplitude σ > 0 and a drop η > 0 that work for all large crossings (lines 37–38).", "link": "Landing.uniform_quadratic_drop"},
  {"text": "Set δ = min(η, 1) and a minimum integer Nmin above the threshold and above 2L (lines 39–47)."},
  {"text": "Get an integer N ≥ Nmin and a crossing (R, ρ) with N < R < N + δ and ρ²/R² in (2, 3) (lines 48–50, packaged as a Crossing at 73–85).", "link": "Density.exists_nearIntegerCrossing"},
  {"text": "Take the uniform branch b through that crossing: radius R at amplitude 0, at most R − η < N at amplitude σ (lines 92–112)."},
  {"text": "Intermediate value theorem: some a in [0, σ] has radius exactly N (lines 113–116)."},
  {"text": "a ≠ 0 since the radius at 0 is R ≠ N (lines 117–123)."},
  {"text": "Check the side conditions (Bessel tail values nonzero, profile smaller than 1/2) and package everything (lines 124–157).", "link": "Landing.LandedConeSolution"},
 ]))


node("Landing.uniform_quadratic_drop",
 "Uniform drop of the cone radius along the branch",
 "Along every sufficiently late branch, the cone radius goes down by at least a fixed amount η by the time the "
 "amplitude reaches a fixed σ. This comes from a uniformly negative second derivative of the radius in the amplitude.",
 r"""## Plain English

**Theorem (`uniform_quadratic_drop`, Schiffer/Landing/UniformDrop.lean lines 103–173).** There are collar data, a
threshold *R*₀, and numbers σ > 0, η > 0, such that for every crossing (*R*, ρ) with *R* ≥ *R*₀ and ρ²/*R*² in
[2, 3], there is a uniform cone branch through it with

- amplitude interval longer than σ,
- radius at amplitude σ at most *R* − η,
- radius at amplitude 0 equal to *R*.

### Where it comes from

- The **branch** with uniform C³ bounds comes from a quantitative Lyapunov–Schmidt reduction (Schiffer/Bifurcation).
- The radius is even in the amplitude (a half-turn symmetry), so its first derivative at 0 vanishes.
- The **drift** modules compute its second derivative at 0 and show it converges, uniformly over the spectral window,
  to a strictly negative limit as *R* → ∞ (Schiffer/Drift).
- A Taylor expansion with the common third-derivative bound then gives radius(σ) ≤ *R* − κσ²/4 for suitable κ, σ.
""",
 [q("Why is the first derivative of the radius at amplitude 0 equal to zero?",
    ["The radius is an even function of the amplitude, by a half-turn symmetry",
     "Because the branch is constant", "Because R is an integer"], 0,
    "Field radius_even in UniformConeBranch (Schiffer/Bifurcation/UniformBranch.lean lines 38–40)."),
  q("Which sign of the second derivative makes landing possible from above?",
    ["Negative: the radius bends downward from R toward N", "Positive", "Zero"], 0,
    "The crossing starts just above N, so the radius must decrease."),
 ],
 caveats=[SKIMMED])


node("Density.exists_nearIntegerCrossing",
 "Crossings just above an integer",
 "For any tolerance δ > 0 there are arbitrarily large integers N and Bessel crossings (R, ρ) with N < R < N + δ: ρ is "
 "a zero of both J₁ and J_R. The proof uses a Kronecker-type density theorem on the two-torus.",
 r"""## Plain English

**Theorem (`exists_nearIntegerCrossing`, Schiffer/Density/NearInteger.lean lines 324–677).** For every δ > 0 and every
lower bound *N*min, there are an integer *N* ≥ *N*min and reals *R*, ρ such that

- ρ is a (selected) positive zero of *J*₁,
- ρ is the *m*-th positive zero of *J*_*R* for some *m*,
- *N* < *R* < *N* + δ,
- 2 < ρ²/*R*² < 3, and ρ²/*N*² is in [9/4, 11/4].

### The idea

Zeros of Bessel functions are asymptotically equally spaced with phases governed by the Debye phase function. Matching
a zero of *J*₁ with a zero of *J*_*R*, with *R* just above an integer, becomes a question of hitting a small target on
a two-dimensional torus with an orbit *n* ↦ (*n*·*a*, *n*·*b*) mod 1. The project proves that if 1, *a*, *b* are
rationally independent such orbits are dense (a Kronecker theorem, proved from scratch), and that a ratio *c* in
(3/2, 8/5) avoiding all resonances exists (countably many bad values). Then the intermediate value theorem in *R*
produces an exact crossing.
""",
 [q("Does this theorem give a crossing with R exactly an integer?",
    ["No: R is strictly between N and N + δ; exact integer radius comes later, from the branch",
     "Yes", "Only when δ = 0"], 0,
    "Schiffer/Density/NearInteger.lean line 330. Siegel's theorem rules out exact integer crossings for distinct integer orders, which is why landing is needed."),
  q("What tool gives density of the relevant phases?",
    ["A Kronecker-type theorem on the two-torus for rationally independent ratios", "The prime number theorem", "Numerical search"], 0,
    "Schiffer/Density/Kronecker.lean, per the module README."),
 ],
 caveats=[SKIMMED])


node("Lift.liftLandedConeSolution",
 "Unfolding the landed cone solution to the plane",
 "Given a landed cone solution, build the planar Schiffer candidate: the boundary profile from the cone, the domain "
 "r < N − h(Nφ), and a C² field that solves −Δu = (ρ²/N²)u, glued from the collar solution and a Fourier–Bessel series "
 "near the origin.",
 r"""## Plain English

**Definition (`liftLandedConeSolution`, Schiffer/Lift/Solution.lean lines 1206–1209).** Turns a
[LandedConeSolution](#/node/Landing.LandedConeSolution) into a [SchifferCandidate](#/node/SchifferCandidate).

- **Graph.** The cone boundary profile, as a Fourier series in θ (Schiffer/Lift/Solution.lean lines 14–23), becomes the
  [PeriodicGraph](#/node/PeriodicGraph) *h*.
- **Domain.** The [radial-graph domain](#/node/radialGraphDomain) with radius *N* − *h*(*N*φ).
- **Eigenvalue.** λ = ρ²/*N*² (lines 1197–1204).
- **Field.** Near the boundary, the cone solution pulled back along (*r*, φ) ↦ (*N* − *r*, *N*φ), which is a local
  isometry because the cone is the plane divided by the *N*-fold rotation. Near the origin, where the cone has its tip,
  the project uses a series of Bessel modes *J*_{*kN*}(ρ*r*/*N*) cos(*kN*φ), proves it converges with two derivatives,
  and shows it matches the collar solution to second order across an interface circle
  (Schiffer/Lift/OriginSeries.lean, about 4,900 lines).

According to the project's informal write-up, this direct construction of the field near the origin replaces an
elliptic-regularity argument, because Mathlib lacks elliptic regularity.
""",
 [q("Why can a solution on the integer cone be pulled back to the plane?",
    ["The map (r, φ) ↦ (N − r, Nφ) is a local isometry from the punctured plane to the cone",
     "Because every cone is flat", "Because N is large"], 0,
    "This is the covering described in the write-up; the Lean identities are in Schiffer/Lift/IntegerCone.lean."),
  q("What eigenvalue does the planar field have?",
    ["ρ²/N²", "1", "ρ²"], 0,
    "Schiffer/Lift/Solution.lean lines 1197–1204. The bridge rescales it to 1 later."),
 ],
 caveats=[SKIMMED, "Schiffer/Lift/OriginSeries.lean is excluded from this site's declaration scan (see the About page), so its declarations do not have pages here."])


node("Lift.counterexampleOfLanded",
 "Packaging the counterexample",
 "From a landed cone solution, build the planar candidate and prove the boundary profile is nonconstant; the field's "
 "nonconstancy and the 'not a disk' property follow. The profile is nonconstant because its first Fourier coefficient "
 "is a nonzero multiple of the nonzero landing amplitude.",
 r"""## Plain English

**Definition (`counterexampleOfLanded`, Schiffer/Lift/Nontriviality.lean lines 136–139).** Produces a
[SchifferCounterexample](#/node/SchifferCounterexample) from a [LandedConeSolution](#/node/Landing.LandedConeSolution):

1. the candidate is [liftLandedConeSolution](#/node/Lift.liftLandedConeSolution);
2. **the profile is nonconstant** (lines 66–107): along the branch, twice the first Fourier coefficient of the profile
   equals a nonzero factor times the amplitude (the `physical_amplitude` field of the branch). The landing amplitude is
   nonzero, so the first coefficient is nonzero, so the profile is not constant;
3. **the field is nonconstant**, automatically for every candidate (lines 12–60, see
   [NonconstantOn](#/node/NonconstantOn));
4. **the domain is not a disk**, from the nonconstant profile (lines 109–120, using
   Schiffer/Geometry/RadialGraph.lean lines 479–559).
""",
 [q("Why is the boundary profile nonconstant?",
    ["Its first Fourier coefficient is a nonzero multiple of the nonzero landing amplitude",
     "Because N ≥ 2", "Because the field is nonconstant"], 0,
    "Schiffer/Lift/Nontriviality.lean lines 66–99."),
 ],
 caveats=["Not built for this site."],
 widgets=None)


# ---------- extra quiz questions (the schema asks for at least three per node) ----------

EXTRA = {
 "Comparator.Pompeiu_Star_Shaped": [
  q("Is the star-shaped domain here the same one as in the Schiffer star-shaped theorem?", ["Yes, the proof reuses it", "No, it is a new domain"], 0,
    "Schiffer/Solution.lean lines 341–347."),
  q("Does Pompeiu_Star_Shaped have a sorry in the solution file?", ["No", "Yes"], 0,
    "Only the challenge file has sorries, and this theorem is derived there too (Schiffer/Challenge.lean lines 113–127)."),
 ],
 "Analysis.SchifferCounterexample.PlanarSchifferCounterexample": [
  q("Why upgrade 'zero normal derivative' to 'zero gradient'?",
    ["The comparator statement asks for the full gradient; it follows because u is constant along the boundary", "Because they are unrelated", "To make the domain convex"], 0,
    "Schiffer/Analysis/SchifferCounterexample.lean lines 506–596."),
 ],
 "Analysis.integral_superlevel_eq_zero_of_schiffer": [
  q("In the Pompeiu bridge, what plays the role of g?", ["1 − u, where u is the Schiffer function", "u itself", "the plane wave"], 0,
    "Schiffer/Solution.lean line 238."),
 ],
 "Landing.LandedConeSolution": [
  q("What is a crossing (R, ρ)?", ["ρ is a common positive zero of J₁ and J_R", "R and ρ are both integers", "ρ = R"], 0,
    "Schiffer/Cone/CollarParameters.lean lines 14–22."),
 ],
 "Landing.uniform_quadratic_drop": [
  q("Do σ and η depend on the crossing?", ["No: they are chosen before the crossing", "Yes"], 0,
    "In the statement, σ and η are quantified before 'for every crossing' (Schiffer/Landing/UniformDrop.lean lines 105–111)."),
 ],
 "Density.exists_nearIntegerCrossing": [
  q("Can N be taken as large as we like?", ["Yes: N ≥ Nmin for any given Nmin", "No, N is fixed"], 0,
    "Schiffer/Density/NearInteger.lean line 327."),
 ],
 "Lift.liftLandedConeSolution": [
  q("Why is a separate series needed near the origin?",
    ["The cone has a tip there, where the collar solution is not defined", "To change the eigenvalue", "To make h periodic"], 0,
    "The collar only covers a fixed band near the boundary; the origin corresponds to the cone tip."),
 ],
 "Lift.counterexampleOfLanded": [
  q("Which field of the uniform branch links the profile to the amplitude?", ["physical_amplitude", "radius_even", "state_zero"], 0,
    "Schiffer/Bifurcation/UniformBranch.lean lines 51–56."),
  q("Where is the 'not a disk' property ultimately proved?", ["Schiffer/Geometry/RadialGraph.lean lines 479–559", "In Main.lean", "It is assumed"], 0,
    "Schiffer/Lift/Nontriviality.lean line 113 calls it."),
 ],
}
for n in NODES:
    n["quiz"] += EXTRA.get(n["id"], [])


node("Cone.Crossing",
 "A Bessel crossing",
 "A crossing is a pair (R, ρ) with ρ > 0 a zero of both J₁ and J_R. On the cone with reciprocal aperture R, that is "
 "where a nonradial mode joins the radial Schiffer solution, so a new branch can start.",
 r"""## Plain English

**Structure (`Crossing`, Schiffer/Cone/CollarParameters.lean lines 14–22).** Positive reals *R* and ρ, a positive integer
*m*, and proofs that

- *J*₁(ρ) = 0,
- *J*_*R*(ρ) = 0, and ρ is the *m*-th positive zero of *J*_*R*.

Here *J*_ν is the Bessel function of real order ν (defined in Schiffer/Bessel/Basic.lean).

### Why these two zeros

On the cone of reciprocal aperture *R*, the radial function *J*₀(ρ(1 − *x*/*R*))/*J*₀(ρ) has value 1 and zero normal
derivative on the boundary exactly when *J*₁(ρ) = 0 (since *J*₀′ = −*J*₁). The first angular mode on that cone is
built from *J*_*R*, and it is resonant in the linearized boundary problem when *J*_*R*(ρ) = 0. Both together give a
one-dimensional kernel, from which a branch bifurcates.

For integer *R* ≥ 2 this cannot happen (distinct integer-order Bessel functions share no positive zeros), which is why
the construction needs non-integer *R* and then [lands](#/node/Landing.exists_landedConeSolution) at an integer.

`crossingLambda` (line 26) is ρ²/*R*², the eigenvalue on the cone; the construction keeps it in [2, 3].
""",
 [q("What two equations define a crossing?", ["J₁(ρ) = 0 and J_R(ρ) = 0", "J₀(ρ) = 0 and J₁(ρ) = 0", "R = ρ and J_R(ρ) = 1"], 0,
    "Schiffer/Cone/CollarParameters.lean lines 20–21."),
  q("Why can R not simply be an integer at a crossing?", ["Bessel functions of distinct integer orders share no positive zeros (Siegel)", "Because R must be irrational by definition", "It can"], 0,
    "Bourget's hypothesis, proved by Siegel, as explained in the project's write-up."),
  q("Is R required to be an integer in this structure?", ["No, R is any positive real", "Yes"], 0,
    "Field R : ℝ with R_pos (Schiffer/Cone/CollarParameters.lean lines 15–18)."),
 ],
 caveats=["The explanation of why these two zeros give a crossing follows the project's informal write-up (informalization/parts/01_main_theorem.tex), not the Lean proofs in Schiffer/Cone and Schiffer/ODE."])
