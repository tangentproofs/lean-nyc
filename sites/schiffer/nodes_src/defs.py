NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}


# ---------- the comparator vocabulary (Schiffer/Solution.lean) ----------

node("Comparator.HasC2Boundary",
 "C² boundary, as a regular level set",
 "A set has C² boundary here if it is exactly the region where some C² function F is positive, and F's gradient never "
 "vanishes where F is zero. This is the standard 'defining function' way to say the boundary is a C² curve.",
 r"""## Plain English

**Definition (`HasC2Boundary`, Schiffer/Solution.lean lines 57–61).** A set Ω in the plane has C² boundary if there
is a function *F* from the plane to the reals such that

- *F* is twice continuously differentiable on the whole plane,
- Ω is exactly the set of points where *F* > 0, and
- at every point where *F* = 0, the gradient of *F* is not zero.

The last condition says 0 is a **regular value** of *F*. By the implicit function theorem, the zero set {*F* = 0} is
then locally a C² curve, and Ω lies on one side of it. Because *F* is continuous, Ω is automatically open.

The challenge file contains the identical definition ([Schiffer/Challenge.lean lines 49–53](https://github.com/jaumededios/Schiffer/blob/2938e277969c329caf154e48a3d8823f3635c7f1/Schiffer/Challenge.lean#L49-L53)), which is what lets the
comparator match the two files.

### Things to notice

- It does not say directly that the boundary of Ω is {*F* = 0}. That is a consequence, proved in the project for
  regular level sets (it is used in Schiffer/Solution.lean lines 233–234).
- For a bounded Ω, this is the usual notion of a bounded C² domain (possibly with several boundary curves). For the
  constructed domain, *F* is built from the polar radius function (Schiffer/Analysis/SchifferCounterexample.lean
  lines 495–505).
""",
 [q("Which set is Ω for the defining function F?",
    ["{x : F(x) > 0}", "{x : F(x) = 0}", "{x : F(x) ≥ 0}", "{x : ∇F(x) ≠ 0}"], 0,
    "Schiffer/Solution.lean line 60."),
  q("Where must the gradient of F be nonzero?",
    ["At every point where F = 0", "Everywhere", "Only inside Ω", "Nowhere; it is not required"], 0,
    "Schiffer/Solution.lean line 61: 0 must be a regular value."),
  q("Is a set with C² boundary in this sense automatically open?",
    ["Yes, because it is {F > 0} for a continuous F", "No, it may contain its boundary", "Only if it is bounded"], 0,
    "Strict superlevel sets of continuous functions are open; the docstring at line 55–56 says so."),
 ])


node("Comparator.IsEuclideanDisk",
 "Being an ordinary disk",
 "Ω is a Euclidean disk if it equals the open ball of some centre c and some radius r. 'Not a disk' therefore rules out "
 "every disk at once, whatever its centre and size.",
 r"""## Plain English

**Definition (`IsEuclideanDisk`, Schiffer/Solution.lean lines 52–53).** Ω is a Euclidean disk if there are a centre
*c* in the plane and a real number *r* with Ω equal to the open ball of radius *r* about *c* (all points at distance
less than *r* from *c*).

The headline theorems use the negation: Ω is **not** equal to any such ball.

### A detail

The radius *r* is not required to be positive. A ball of radius *r* ≤ 0 is empty, so allowing it only adds the empty
set to the list of "disks". Since the headline domains are nonempty, this makes no difference, and if anything makes
"not a disk" harder to satisfy, not easier. The geometry module has its own version with 0 < *r*
([IsEuclideanDisk](#/node/IsEuclideanDisk)).
""",
 [q("Which sets count as Euclidean disks under this definition?",
    ["Open balls with any centre and any real radius (radius ≤ 0 gives the empty set)",
     "Only the unit disk about the origin",
     "Closed disks only",
     "Any region bounded by a circle-like curve"], 0,
    "Schiffer/Solution.lean lines 52–53."),
  q("Would allowing r ≤ 0 make 'not a disk' a weaker claim?",
    ["No: it adds only the empty set, which is excluded anyway because Ω is nonempty",
     "Yes: it makes every set a disk",
     "Yes: negative radii give large balls"], 0,
    "A ball with nonpositive radius is empty."),
 ])


# ---------- Formal Conjectures vocabulary ----------

node("FormalConjecturesComparator.RigidMotion",
 "Rigid motions of Euclidean space",
 "A rigid motion of (N+1)-dimensional Euclidean space is a bijective affine map that preserves distances: any "
 "combination of translations, rotations and reflections.",
 r"""## Plain English

**Definition (`RigidMotion`, Schiffer/FormalConjecturesSolution.lean lines 30–32).** For a natural number *N*, a rigid
motion of *N* + 1 dimensional Euclidean space is an element of Mathlib's `AffineIsometryEquiv` from
`EuclideanSpace ℝ (Fin (N + 1))` to itself: a bijection of the form *x* ↦ *A x* + *b* where *A* is an orthogonal
linear map.

Orientation is not required, so reflections are included. This matches the classical Pompeiu problem, where one
integrates over all congruent copies of the domain. (Including reflections only makes "the integral vanishes over every
rigid copy" a stronger demand on *f*.)

The dimension is written *N* + 1 so it is always at least 1. The planar case is *N* = 1.
""",
 [q("Are reflections rigid motions in this definition?",
    ["Yes: any bijective affine isometry counts", "No: only orientation-preserving maps", "Only reflections through the origin"], 0,
    "AffineIsometryEquiv requires distance preservation, not orientation (Schiffer/FormalConjecturesSolution.lean lines 30–32)."),
  q("What dimension does RigidMotion 1 act on?",
    ["2", "1", "3"], 0, "The space is EuclideanSpace ℝ (Fin (N + 1)), so N = 1 gives the plane."),
 ])


node("FormalConjecturesComparator.HasPompeiuProperty",
 "The Pompeiu property",
 "A domain has the Pompeiu property if the only continuous function whose integral over every rigid copy of the domain "
 "is zero is the zero function. Disks do not have it; the conjecture is that, among nice domains, only balls fail it.",
 r"""## Plain English

**Definition (`HasPompeiuProperty`, Schiffer/FormalConjecturesSolution.lean lines 36–38).** A set Ω in (*N* + 1)-dimensional
Euclidean space has the Pompeiu property if: for every continuous real function *f* on the space, **if** the integral
of *f* over σ(Ω) is zero for every [rigid motion](#/node/FormalConjecturesComparator.RigidMotion) σ, **then** *f* is
zero at every point.

Failing the property means exhibiting a continuous *f*, not identically zero, whose integral vanishes over every
rigid image of Ω. That is exactly what [SchifferToPompeiu](#/node/Comparator.SchifferToPompeiu) produces.

### About Lean's integrals

Lean's integral of a non-integrable function is defined to be 0, so in general "the integral is 0" can be vacuous.
That cannot help a counterexample here: the witness is cos(Re *x*), which is continuous and bounded, and the domain is
bounded, so the integrals are genuine.
""",
 [q("To show Ω fails the Pompeiu property, what must be produced?",
    ["A continuous f, not identically zero, with zero integral over every rigid image of Ω",
     "A rigid motion that maps Ω to itself",
     "A continuous f with zero integral over Ω itself only"], 0,
    "Negating the definition at Schiffer/FormalConjecturesSolution.lean lines 36–38."),
  q("Does a disk have the Pompeiu property?",
    ["No: there are nonzero Bessel-type functions with zero integral over every disk of a fixed radius", "Yes", "Only the unit disk does"], 0,
    "That is classical and is why the conjecture singles out balls."),
 ])


node("FormalConjecturesComparator.IsBall",
 "Being a ball (Formal Conjectures version)",
 "Ω is a ball if it equals the open ball of some centre and some positive radius in (N+1)-dimensional Euclidean space.",
 r"""## Plain English

**Definition (`IsBall`, Schiffer/FormalConjecturesSolution.lean lines 41–43).** Ω is a ball if there are a centre *c*
and a radius *r* > 0 with Ω equal to the open ball of radius *r* about *c*.

Unlike the planar [IsEuclideanDisk](#/node/Comparator.IsEuclideanDisk), this one requires *r* > 0. The proof only
needs one direction: if the transported planar domain were a ball here, it would be a disk in the planar sense
(Schiffer/FormalConjecturesSolution.lean lines 437–443), which the construction rules out.
""",
 [q("What does the proof need to know about IsBall?",
    ["That a ball in EuclideanSpace ℝ (Fin 2) pulls back to a disk in ℂ", "That every ball has the Pompeiu property", "Nothing"], 0,
    "Schiffer/FormalConjecturesSolution.lean lines 437–443."),
 ])


node("FormalConjecturesComparator.HasLipschitzBoundary",
 "Lipschitz boundary",
 "Near every boundary point, after a suitable rigid motion, the domain is exactly the region strictly below the graph "
 "of a Lipschitz function. This is the usual minimal-regularity notion of a 'nice' boundary.",
 r"""## Plain English

**Definition (`HasLipschitzBoundary`, Schiffer/FormalConjecturesSolution.lean lines 47–54).** For every point *p* on
the boundary of Ω there are

- a neighbourhood *U* of *p*,
- a [rigid motion](#/node/FormalConjecturesComparator.RigidMotion) σ,
- a Lipschitz function *g* from *N*-dimensional space to the reals,

such that, for points *x* in *U*, *x* lies in Ω exactly when the last coordinate of σ(*x*) is less than *g* applied
to the first *N* coordinates of σ(*x*).

In words: zoom in near any boundary point, rotate so that the boundary runs roughly horizontally, and Ω is the region
below a graph with bounded slope.

The planar counterexample has a C² regular-level-set boundary, which is much smoother. Turning that into this local
graph form is a real (if routine) piece of work: the project does it with Mathlib's implicit function theorem in
Schiffer/FormalConjecturesSolution.lean lines 256–344, then transfers it from ℂ to `EuclideanSpace ℝ (Fin 2)` in
lines 348–386.
""",
 [q("Near a boundary point, what does Ω look like under this definition?",
    ["After a rigid motion, the region strictly below the graph of a Lipschitz function",
     "A disk", "A half-plane exactly", "The region above a C² graph"], 0,
    "Schiffer/FormalConjecturesSolution.lean lines 53–55."),
  q("Is a C² regular-level-set boundary also Lipschitz in this sense?",
    ["Yes; the project proves it via the implicit function theorem", "No; Lipschitz is a stronger condition", "Only for convex domains"], 0,
    "Schiffer/FormalConjecturesSolution.lean lines 256–344."),
 ])


node("FormalConjecturesComparator.IsAdmissibleDomain",
 "Admissible domains for the Pompeiu conjecture",
 "The hypotheses the Formal Conjectures statement places on a domain: bounded, open, connected, simply connected and "
 "with Lipschitz boundary.",
 r"""## Plain English

**Definition (`IsAdmissibleDomain`, Schiffer/FormalConjecturesSolution.lean lines 57–62).** A set Ω in
(*N* + 1)-dimensional Euclidean space is admissible if it is

1. bounded,
2. open,
3. connected,
4. simply connected (as a topological space in its own right), and
5. has [Lipschitz boundary](#/node/FormalConjecturesComparator.HasLipschitzBoundary).

These are the conditions under which the Pompeiu conjecture is usually stated. Simple connectivity matters: without
it there are easy counterexamples (annuli fail the Pompeiu property too), which is why the conjecture restricts to
simply connected domains.

The planar counterexample satisfies all five after transport to `EuclideanSpace ℝ (Fin 2)`
(Schiffer/FormalConjecturesSolution.lean lines 459–465).
""",
 [q("Which of these is NOT one of the admissibility conditions?",
    ["Convex", "Bounded", "Simply connected", "Lipschitz boundary"], 0,
    "The five fields are at Schiffer/FormalConjecturesSolution.lean lines 58–62; convexity is not among them."),
  q("Why is simple connectivity part of the hypotheses?",
    ["Without it, domains with holes such as annuli would be easy counterexamples", "It is needed to define the integral", "It is implied by boundedness"], 0,
    "The classical conjecture is restricted to simply connected domains for this reason."),
 ])


# ---------- the construction's endpoint (Schiffer/Statement.lean, Geometry) ----------

node("PlanarPoint",
 "Points of the plane",
 "In the construction, a point of the plane is a complex number, used only as a two-dimensional real vector space.",
 r"""## Plain English

**Definition (`PlanarPoint`, Schiffer/Geometry/RadialGraph.lean line 15).** `PlanarPoint` is another name for ℂ.
The project uses complex numbers only for convenience (polar coordinates via the exponential, rotation by
multiplication); all calculus is real calculus on ℝ².
""",
 [q("What is a PlanarPoint?", ["A complex number, viewed as a point of ℝ²", "A pair of natural numbers", "A point on the cone"], 0,
    "Schiffer/Geometry/RadialGraph.lean line 15.")])


node("PeriodicGraph",
 "Periodic boundary profiles",
 "A PeriodicGraph is a real function of an angle that is 2π-periodic and twice continuously differentiable. It "
 "describes how far the boundary is pushed in or out at each angle.",
 r"""## Plain English

**Definition (`PeriodicGraph`, Schiffer/Geometry/RadialGraph.lean lines 17–20).** A structure with

- a function *h* from ℝ to ℝ,
- a proof that *h* is 2π-periodic, and
- a proof that *h* is C².

In the construction, *h* is the boundary profile found on the cone; the planar boundary is then
*r* = *N* − *h*(*N*φ) ([planarRadius](#/node/planarRadius)). Because *h* is evaluated at *N*φ, the planar boundary
repeats *N* times around the circle.
""",
 [q("What regularity does a PeriodicGraph have?", ["C²", "Only continuous", "Real-analytic"], 0,
    "The field contDiff_two (Schiffer/Geometry/RadialGraph.lean line 20).")])


node("planarRadius",
 "The boundary radius at angle φ",
 "At polar angle φ, the boundary of the constructed domain lies at distance N − h(Nφ) from the origin: a circle of "
 "radius N, wobbled by the profile h repeated N times.",
 r"""## Plain English

**Definition (`planarRadius`, Schiffer/Geometry/RadialGraph.lean lines 31–32).** Given an integer *N* and a
[PeriodicGraph](#/node/PeriodicGraph) *h*, the radius at angle φ is *N* − *h*(*N*φ).

This is the lift of the cone boundary *x* = *h*(θ) along the covering map (*r*, φ) ↦ (*N* − *r*, *N*φ) described
in the project's write-up. In the construction |*h*| < 1/2 and *N* ≥ 2, so the radius stays between *N* − 1/2 and
*N* + 1/2 and is positive.
""",
 [q("How many times does the boundary pattern repeat around the origin?", ["N times", "Once", "2π times"], 0,
    "h is 2π-periodic and evaluated at Nφ (Schiffer/Geometry/RadialGraph.lean line 32).")])


node("boundaryPoint",
 "Boundary points",
 "The boundary point at angle φ is the point at distance planarRadius(φ) from the origin in direction φ.",
 r"""## Plain English

**Definition (`boundaryPoint`, Schiffer/Geometry/RadialGraph.lean lines 34–35).** The point
*r*(φ)·*e*^{*i*φ}, where *r* is [planarRadius](#/node/planarRadius). As φ runs over [0, 2π), these points trace the
boundary curve of the [radial-graph domain](#/node/radialGraphDomain); the project proves the frontier is exactly
the set of these points (Schiffer/Geometry/RadialGraph.lean lines 399–425).
""",
 [q("What is boundaryPoint N h φ?", ["The point at polar angle φ and radius N − h(Nφ)", "The point h(φ) on the real axis", "The centre of the domain"], 0,
    "Schiffer/Geometry/RadialGraph.lean lines 31–35.")])


node("boundaryNormal",
 "The (unnormalized) outward normal",
 "At the boundary point with angle φ, this vector is perpendicular to the boundary curve and points outward. It is not "
 "scaled to length 1, which does not matter for saying a derivative in its direction is zero.",
 r"""## Plain English

**Definition (`boundaryNormal`, Schiffer/Geometry/RadialGraph.lean lines 37–40).** In the rotated frame at angle φ
(radial direction, then tangential direction), the vector has radial component *r*(φ) and tangential component
*N h*′(*N*φ), where *r* is [planarRadius](#/node/planarRadius).

Why that is a normal: the boundary curve is *r*(φ)*e*^{*i*φ}, whose tangent vector has radial component *r*′(φ) =
−*N h*′(*N*φ) and tangential component *r*(φ). Rotating the tangent a quarter turn clockwise gives radial component
*r*(φ) and tangential component *N h*′(*N*φ), which is this vector. Its radial component is positive, so it points
outward.

It is used in [HasZeroNormalDerivative](#/node/HasZeroNormalDerivative). The project proves it is never zero
(Schiffer/Geometry/RadialGraph.lean lines 359–370).
""",
 [q("Why is it fine that this normal is not a unit vector?",
    ["The condition using it says a directional derivative is zero, which is unaffected by scaling the direction",
     "Because it always has length 1 anyway", "Because the boundary is a circle"], 0,
    "A derivative along v is zero iff the derivative along any nonzero multiple of v is zero."),
 ])


node("radialGraphDomain",
 "The radial-graph domain",
 "The constructed domain is everything strictly inside the closed curve r = N − h(Nφ): all points t·boundaryPoint(φ) "
 "with 0 ≤ t < 1. It is star-shaped about the origin by construction.",
 r"""## Plain English

**Definition (`radialGraphDomain`, Schiffer/Geometry/RadialGraph.lean lines 42–44).** The set of points
*t*·[boundaryPoint](#/node/boundaryPoint)(φ) with 0 ≤ *t* < 1 and φ any angle.

So the domain is the union of the half-open segments from the origin to each boundary point. Star-shapedness about
0 is immediate from the definition. Openness, boundedness, simple connectivity and the description of the frontier
need the boundary radius to be positive, which holds when |*h*| < 1/2 and *N* ≥ 2; the project proves those facts in
Schiffer/Geometry/RadialGraph.lean lines 359–478.

If *h* is nonconstant, the domain is not a disk (Schiffer/Geometry/RadialGraph.lean lines 479–559). The argument uses
the symmetry: the domain is unchanged by rotation through 2π/*N* about the origin, so if it were a ball, that rotation
would fix the ball's centre, which forces the centre to be the origin (since *N* ≥ 2, the rotation is not the
identity). A ball centred at the origin has the same boundary radius in every direction, but the radius
*N* − *h*(*N*φ) varies because *h* is nonconstant.
""",
 [q("Is the origin in the radial-graph domain?", ["Yes: take t = 0", "No", "Only if h(0) = 0"], 0,
    "t = 0 is allowed (Schiffer/Geometry/RadialGraph.lean lines 43–44)."),
  q("Is the boundary curve itself part of the domain?", ["No: t < 1 strictly", "Yes: t ≤ 1", "Only at φ = 0"], 0,
    "The parameter t satisfies t < 1, and the frontier is the set of boundary points (lines 399–425)."),
 ],
 caveats=["The summary of why a nonconstant radius is not a disk follows the first half of the Lean argument (rotation fixes the centre); the second half, at Schiffer/Geometry/RadialGraph.lean lines 530–559, was skimmed rather than traced step by step."])


node("IsEuclideanDisk",
 "Being a disk (construction version)",
 "In the construction, a disk is an open ball with a positive radius and any centre.",
 r"""## Plain English

**Definition (`IsEuclideanDisk`, Schiffer/Geometry/RadialGraph.lean lines 46–47).** There are a centre *c* and a
radius *r* > 0 with Ω equal to the open ball of radius *r* about *c*.

This is the construction's own notion, used in [SchifferCounterexample](#/node/SchifferCounterexample). The
comparator file has a separate [IsEuclideanDisk](#/node/Comparator.IsEuclideanDisk) that allows any radius. The
bridge between them (Schiffer/Analysis/SchifferCounterexample.lean lines 713–742) also has to undo the rescaling of the
domain.
""",
 [q("How does this differ from the comparator's IsEuclideanDisk?",
    ["It requires a positive radius", "It requires the centre to be 0", "There is no difference"], 0,
    "Compare Schiffer/Geometry/RadialGraph.lean line 47 with Schiffer/Solution.lean line 53.")])


node("planeLaplacian",
 "The Laplacian in the plane",
 "The ordinary Laplacian Δu = ∂²u/∂x² + ∂²u/∂y², written as the sum of second derivatives in the directions 1 and i.",
 r"""## Plain English

**Definition (`planeLaplacian`, Schiffer/Analysis/PolarLaplacian.lean lines 15–17).** For a real function *u* on the
plane and a point *z*, add the second derivative of *u* at *z* in the direction 1 (the *x*-direction) twice, and the
second derivative in the direction *i* (the *y*-direction) twice.

That is ∂²*u*/∂*x*² + ∂²*u*/∂*y*². The comparator statements use Mathlib's own Laplacian instead, which on ℂ is the
same thing (Mathlib's `laplacian_eq_iteratedFDeriv_complexPlane`, cited in Schiffer/Solution.lean lines 45–49). The
same file proves the polar-coordinate formula used to lift cone solutions (Schiffer/Analysis/PolarLaplacian.lean
lines 132 onward).
""",
 [q("Which directions does planeLaplacian differentiate in?", ["1 and i, the two coordinate axes", "Radial and angular", "Along the boundary normal"], 0,
    "Schiffer/Analysis/PolarLaplacian.lean lines 16–17.")])


node("SatisfiesHelmholtz",
 "The Helmholtz equation in a domain",
 "u satisfies the Helmholtz equation with parameter λ in Ω if −Δu = λu at every point of Ω.",
 r"""## Plain English

**Definition (`SatisfiesHelmholtz`, Schiffer/Statement.lean lines 13–15).** For every point *z* of Ω,
minus the [plane Laplacian](#/node/planeLaplacian) of *u* at *z* equals λ times *u*(*z*).

With λ > 0 this says *u* is an eigenfunction of −Δ with eigenvalue λ inside Ω. Nothing is said outside Ω.
""",
 [q("Where must the equation hold?", ["At every point of Ω", "On the whole plane", "Only on the boundary"], 0,
    "Schiffer/Statement.lean line 15.")])


node("HasBoundaryValueOne",
 "Boundary value one",
 "u equals 1 at every boundary point of the radial-graph domain.",
 r"""## Plain English

**Definition (`HasBoundaryValueOne`, Schiffer/Statement.lean lines 17–19).** For every angle φ,
*u*([boundaryPoint](#/node/boundaryPoint)(φ)) = 1.

This is the "constant boundary trace" half of the Schiffer condition, normalized to the constant 1.
""",
 [q("Why the constant 1 rather than an arbitrary constant c?", ["Multiplying u by 1/c normalizes it, as long as c ≠ 0", "Because Schiffer's conjecture is only about the value 1", "It is a typo"], 0,
    "The equations are linear in u. (If the constant were 0, the Neumann-and-Dirichlet data would force u = 0 by unique continuation, so c ≠ 0 is the interesting case.)")])


node("HasZeroNormalDerivative",
 "Zero normal derivative",
 "At every boundary point, the derivative of u in the direction of the outward normal is zero: the Neumann condition.",
 r"""## Plain English

**Definition (`HasZeroNormalDerivative`, Schiffer/Statement.lean lines 21–24).** For every angle φ, the derivative of
*u* at [boundaryPoint](#/node/boundaryPoint)(φ), applied to the vector [boundaryNormal](#/node/boundaryNormal)(φ),
is zero.

Together with [boundary value one](#/node/HasBoundaryValueOne) this is Schiffer's overdetermined boundary condition.
The comparator version instead asks for the whole gradient to vanish on the boundary; the bridge proves that from
this one, because the tangential derivative of *u* is zero along a curve where *u* is constant
(Schiffer/Analysis/SchifferCounterexample.lean lines 554–596).
""",
 [q("Which derivative is required to vanish?", ["The derivative along the boundary normal", "The full gradient", "The second derivative"], 0,
    "Schiffer/Statement.lean line 24. The full-gradient version is derived later.")])


node("Nonconstant",
 "Nonconstant functions",
 "A function is nonconstant if it takes two different values somewhere.",
 r"""## Plain English

**Definition (`Nonconstant`, Schiffer/Geometry/RadialGraph.lean lines 25–26).** There are inputs *x* and *y* with
*f*(*x*) ≠ *f*(*y*). The variant [NonconstantOn](#/node/NonconstantOn) restricts *x* and *y* to a set.
""",
 [q("Is the zero function nonconstant?", ["No", "Yes"], 0, "All its values agree.")])


node("NonconstantOn",
 "Nonconstant on a set",
 "A function is nonconstant on a set if it takes two different values at points of that set.",
 r"""## Plain English

**Definition (`NonconstantOn`, Schiffer/Geometry/RadialGraph.lean lines 28–29).** There are points *x* and *y* in the
set *s* with *f*(*x*) ≠ *f*(*y*). It is used to say the Schiffer field is not constant on the domain. For any
[SchifferCandidate](#/node/SchifferCandidate) this is automatic (Schiffer/Lift/Nontriviality.lean lines 12–60):
a constant field would have zero Laplacian at the origin, but the Helmholtz equation and the boundary value would make
it 1 there, which is a contradiction since λ > 0.
""",
 [q("Why is the field of every Schiffer candidate nonconstant on its domain?",
    ["A constant field equal to 1 would give 0 = λ·1 at the origin, impossible for λ > 0",
     "Because the domain is not a disk", "It is assumed as an axiom"], 0,
    "Schiffer/Lift/Nontriviality.lean lines 12–60.")])


node("SchifferCandidate",
 "A Schiffer candidate",
 "The bundle of everything a planar Schiffer solution needs: an integer N ≥ 2, a small periodic profile h, the "
 "radial-graph domain it defines with its basic topology, a positive eigenvalue λ, and a C² field u solving −Δu = λu "
 "with u = 1 and zero normal derivative on the boundary.",
 r"""## Plain English

**Structure (`SchifferCandidate`, Schiffer/Statement.lean lines 26–47).** A Schiffer candidate consists of:

- **Shape:** an integer *N* ≥ 2 and a [PeriodicGraph](#/node/PeriodicGraph) *h* with |*h*(θ)| < 1/2 for all θ.
- **Eigenvalue:** a real λ > 0.
- **Domain:** a set equal to the [radial-graph domain](#/node/radialGraphDomain) of *N* and *h*, together with proofs
  that it is open, bounded, star-convex about 0 and simply connected, and that its frontier is exactly the set of
  [boundary points](#/node/boundaryPoint).
- **Field:** an open set (the "ambient" set) containing the closure of the domain, and a function *u* that is C² on
  it, with
  - [−Δ*u* = λ*u*](#/node/SatisfiesHelmholtz) in the domain,
  - [*u* = 1](#/node/HasBoundaryValueOne) at the boundary points,
  - [zero normal derivative](#/node/HasZeroNormalDerivative) at the boundary points.

Some fields are redundant (openness, boundedness and so on follow from the shape), but storing them makes the endpoint
easy to use. A disk of radius *N* with *h* = 0 and the radial Bessel solution would be a candidate; a
[SchifferCounterexample](#/node/SchifferCounterexample) adds the requirement that it is not a disk.

### Why the field is only C² on a neighbourhood

A neighbourhood of the closed domain is the natural place for a PDE solution to live. The comparator form wants a C²
function on the whole plane; that is obtained with a smooth cutoff
(Schiffer/Analysis/SchifferCounterexample.lean lines 876–912).
""",
 [q("Could a disk with its radial Bessel solution be a SchifferCandidate?",
    ["Yes: nothing in SchifferCandidate rules out h = 0", "No: the structure requires h to be nonconstant", "No: N must be 1 for a disk"], 0,
    "Nonconstancy and 'not a disk' are added in SchifferCounterexample (Schiffer/Statement.lean lines 49–53)."),
  q("Where is the field required to be C²?",
    ["On an open set containing the closure of the domain", "Only inside the domain", "On the whole plane"], 0,
    "Fields ambient, ambient_open, closure_domain_subset_ambient and field_C2 (Schiffer/Statement.lean lines 40–44)."),
  q("What bound is imposed on the profile h?", ["|h(θ)| < 1/2 everywhere", "h is zero", "|h| < 1/N"], 0,
    "Field graph_small (Schiffer/Statement.lean line 30)."),
 ])


node("SchifferCounterexample",
 "A Schiffer counterexample",
 "A Schiffer candidate whose profile h is nonconstant, whose field is nonconstant on the domain, and whose domain is "
 "not a disk. This is the object the whole construction produces.",
 r"""## Plain English

**Structure (`SchifferCounterexample`, Schiffer/Statement.lean lines 49–53).** A [SchifferCandidate](#/node/SchifferCandidate)
together with three extra facts:

1. the profile *h* is [nonconstant](#/node/Nonconstant);
2. the field is [nonconstant on the domain](#/node/NonconstantOn);
3. the domain is not a [disk](#/node/IsEuclideanDisk).

Fact 2 holds for every candidate, and fact 3 follows from fact 1 for these radial-graph domains (see
Schiffer/Lift/Nontriviality.lean lines 109–124). So the real content beyond a candidate is: **the boundary profile is
not flat**.

[exists_schifferCounterexample](#/node/exists_schifferCounterexample) says one exists. The bridge
[PlanarSchifferCounterexample](#/node/Analysis.SchifferCounterexample.PlanarSchifferCounterexample) turns it into the
plain comparator statement.
""",
 [q("Which extra fact carries the real mathematical content beyond SchifferCandidate?",
    ["The boundary profile h is nonconstant", "The field is nonconstant", "The eigenvalue is positive"], 0,
    "Field nonconstancy is automatic and non-disk follows from a nonconstant h (Schiffer/Lift/Nontriviality.lean lines 12–60 and 109–124)."),
 ])


# ---------- extra quiz questions (the schema asks for at least three per node) ----------

EXTRA = {
 "Comparator.IsEuclideanDisk": [
  q("The headline says Ω is not a disk. Does that exclude disks centred away from the origin?",
    ["Yes: the centre c is existentially quantified, so every centre is excluded", "No: only disks centred at 0 are excluded"], 0,
    "Schiffer/Solution.lean line 53 quantifies over all centres c and radii r."),
 ],
 "FormalConjecturesComparator.RigidMotion": [
  q("Is a scaling x ↦ 2x a rigid motion?", ["No: it doubles distances", "Yes", "Only in dimension 1"], 0,
    "Rigid motions preserve distances (AffineIsometryEquiv)."),
 ],
 "FormalConjecturesComparator.HasPompeiuProperty": [
  q("Which quantifier order does the definition use?",
    ["For every continuous f: if its integral vanishes over every rigid image, then f is zero everywhere",
     "There is a rigid motion such that every f integrates to zero",
     "For every rigid motion there is an f"], 0,
    "Schiffer/FormalConjecturesSolution.lean lines 37–38."),
 ],
 "FormalConjecturesComparator.IsBall": [
  q("Is the empty set a ball under this definition?", ["No: the radius must be positive, so the ball is nonempty", "Yes"], 0,
    "Schiffer/FormalConjecturesSolution.lean line 43 requires 0 < r."),
  q("In which space are the balls taken?", ["EuclideanSpace ℝ (Fin (N + 1))", "ℂ", "The cone"], 0,
    "Schiffer/FormalConjecturesSolution.lean lines 41–43."),
 ],
 "FormalConjecturesComparator.HasLipschitzBoundary": [
  q("Is the Lipschitz function g allowed to depend on the boundary point?",
    ["Yes: U, σ, K and g are chosen separately for each boundary point", "No: one g works for the whole boundary"], 0,
    "All are existentially quantified inside 'for every p in the frontier' (Schiffer/FormalConjecturesSolution.lean lines 49–51)."),
 ],
 "FormalConjecturesComparator.IsAdmissibleDomain": [
  q("Does the planar counterexample's domain satisfy these conditions after moving to EuclideanSpace ℝ (Fin 2)?",
    ["Yes, all five are proved", "Only boundedness", "No; the theorem only needs four of them"], 0,
    "Schiffer/FormalConjecturesSolution.lean lines 459–465."),
 ],
 "PlanarPoint": [
  q("Does the project use complex multiplication in its analysis?",
    ["Only for convenience, e.g. rotations and polar form; derivatives are real derivatives", "No, never", "Yes, all functions are holomorphic"], 0,
    "The fields are real-valued functions on ℂ differentiated over ℝ (e.g. ContDiff ℝ 2)."),
  q("What does PlanarPoint unfold to?", ["ℂ", "ℝ", "ℝ × ℝ × ℝ"], 0, "Schiffer/Geometry/RadialGraph.lean line 15."),
 ],
 "PeriodicGraph": [
  q("What period does a PeriodicGraph have?", ["2π", "2π/N", "1"], 0, "Schiffer/Geometry/RadialGraph.lean line 19."),
  q("Where does the PeriodicGraph of the counterexample come from?",
    ["The boundary profile of the landed cone solution, as a Fourier series", "A numerical fit", "It is the zero function"], 0,
    "Schiffer/Lift/Solution.lean lines 14–23."),
 ],
 "planarRadius": [
  q("With |h| < 1/2 and N ≥ 2, what range does the radius lie in?", ["Between N − 1/2 and N + 1/2", "Between 0 and 1", "Exactly N"], 0,
    "N − h(Nφ) with |h| < 1/2."),
  q("If h is the zero function, what is the domain's boundary?", ["The circle of radius N", "A point", "Empty"], 0,
    "The radius is then N at every angle."),
 ],
 "boundaryPoint": [
  q("Is the boundary curve periodic in φ with period 2π?", ["Yes", "No, period 2π/N only", "It is not periodic"], 0,
    "Both the radius and e^{iφ} are 2π-periodic (the radius even has period 2π/N)."),
  q("Which boundary condition definitions use boundaryPoint?",
    ["HasBoundaryValueOne and HasZeroNormalDerivative", "Only IsEuclideanDisk", "None"], 0,
    "Schiffer/Statement.lean lines 17–24."),
 ],
 "boundaryNormal": [
  q("Which way does boundaryNormal point?", ["Outward: its radial component r(φ) is positive", "Inward", "Along the boundary"], 0,
    "Schiffer/Geometry/RadialGraph.lean lines 37–40."),
  q("If h is the zero function, what is boundaryNormal(φ)?", ["N·e^{iφ}, the radial direction scaled by N", "Zero", "i·e^{iφ}"], 0,
    "With h = 0 the tangential component vanishes and r = N."),
 ],
 "radialGraphDomain": [
  q("Why is the radial-graph domain star-shaped about 0 almost by definition?",
    ["Each point is t times a boundary point with 0 ≤ t < 1, so shrinking t keeps it inside", "Because it is convex", "Because h is periodic"], 0,
    "Schiffer/Geometry/RadialGraph.lean lines 42–44, proved at lines 427–444."),
 ],
 "IsEuclideanDisk": [
  q("Is the empty set a disk in this sense?", ["No: the radius must be positive", "Yes"], 0,
    "Schiffer/Geometry/RadialGraph.lean line 47."),
  q("How does the project show the radial-graph domain is not a disk?",
    ["Rotation symmetry forces the centre to be 0, and a nonconstant radius is not a circle", "By computing its area", "It assumes it"], 0,
    "Schiffer/Geometry/RadialGraph.lean lines 479–559."),
 ],
 "planeLaplacian": [
  q("Is planeLaplacian the same as Mathlib's Laplacian on ℂ?", ["Yes, both are ∂²/∂x² + ∂²/∂y²", "No, it has the opposite sign", "No, it is the polar Laplacian"], 0,
    "Mathlib's laplacian_eq_iteratedFDeriv_complexPlane, cited in Schiffer/Solution.lean lines 45–49."),
  q("What is the planeLaplacian of x² + y²?", ["4", "2", "0"], 0, "∂²/∂x² of x² is 2 and ∂²/∂y² of y² is 2, so the sum is 4."),
 ],
 "SatisfiesHelmholtz": [
  q("With λ = 1, what equation is this?", ["−Δu = u", "Δu = 0", "Δu = u"], 0, "Schiffer/Statement.lean line 15."),
  q("Does SatisfiesHelmholtz say anything about u outside Ω?", ["No", "Yes, the equation holds everywhere"], 0,
    "The quantifier is over z ∈ Ω only."),
 ],
 "HasBoundaryValueOne": [
  q("Where must u equal 1?", ["At every boundary point of the radial-graph domain", "Everywhere in the domain", "Only at the origin"], 0,
    "Schiffer/Statement.lean line 19."),
  q("Together with which condition does it form Schiffer's overdetermined boundary data?",
    ["Zero normal derivative", "u = 0 at the origin", "Nonconstancy of h"], 0, "See HasZeroNormalDerivative."),
 ],
 "HasZeroNormalDerivative": [
  q("Does the normal vector need to have length one?", ["No; only the direction matters for a zero derivative", "Yes"], 0,
    "boundaryNormal is not normalized (Schiffer/Geometry/RadialGraph.lean lines 37–40)."),
  q("Why does this imply the full gradient vanishes on the boundary, given u = 1 there?",
    ["The tangential derivative is zero because u is constant along the boundary", "It doesn't", "Because Δu = 0"], 0,
    "Schiffer/Analysis/SchifferCounterexample.lean lines 554–596."),
 ],
 "Nonconstant": [
  q("What must be exhibited to show f is nonconstant?", ["Two inputs where f takes different values", "One input where f is nonzero", "A derivative"], 0,
    "Schiffer/Geometry/RadialGraph.lean line 26."),
  q("Which object is required to be Nonconstant in a SchifferCounterexample?", ["The boundary profile h", "The eigenvalue", "N"], 0,
    "Schiffer/Statement.lean line 50."),
 ],
 "NonconstantOn": [
  q("How does NonconstantOn differ from Nonconstant?", ["Both points must lie in the given set", "It requires three points", "No difference"], 0,
    "Schiffer/Geometry/RadialGraph.lean lines 28–29."),
  q("Could a function be nonconstant on the plane but constant on Ω?", ["Yes, so NonconstantOn is the right notion for the field", "No"], 0,
    "The field lives on the plane but only matters on the domain."),
 ],
 "SchifferCounterexample": [
  q("Which fact is automatic for every SchifferCandidate?", ["The field is nonconstant on the domain", "The domain is not a disk", "h is nonconstant"], 0,
    "Schiffer/Lift/Nontriviality.lean lines 12–60."),
  q("Which theorem says a SchifferCounterexample exists?", ["exists_schifferCounterexample", "SchifferToPompeiu", "IsEuclideanDisk"], 0,
    "Schiffer/Main.lean lines 8–10."),
 ],
}
for n in NODES:
    n["quiz"] += EXTRA.get(n["id"], [])
