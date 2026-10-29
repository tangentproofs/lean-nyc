NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]

NOT_BUILT = ("Not built for this site: \"proved\" means Schiffer/Solution.lean contains a complete-looking proof with no "
             "`sorry` anywhere in the files it imports. The project's own metadata says a full build succeeded, but that "
             "was not re-checked here.")


node("Comparator.Schiffer_SimplyConnected",
 "Headline: a simply connected planar domain that breaks Schiffer's conjecture",
 "There is a bounded, simply connected region of the plane that is not a disk, and a function on the plane that solves "
 "−Δu = u inside it with u = 1 and ∇u = 0 on its boundary. Schiffer's conjecture says only a disk can carry such a "
 "function, so this statement, if the proof holds, refutes it.",
 r"""## Plain English

**Theorem (`Schiffer_SimplyConnected`, Schiffer/Solution.lean lines 92–109).** There exist a set Ω in the plane
(the plane is modelled as the complex numbers ℂ) and a real function *u* on the whole plane such that:

1. Ω is **bounded** and **nonempty**;
2. Ω is **path connected** and **simply connected** (no holes);
3. Ω has a **C² boundary**, in the precise sense of [HasC2Boundary](#/node/Comparator.HasC2Boundary):
   Ω is the region where some twice-differentiable function *F* is positive, and the gradient of *F* never vanishes
   where *F* = 0;
4. Ω is **not a disk** ([IsEuclideanDisk](#/node/Comparator.IsEuclideanDisk));
5. *u* is twice continuously differentiable on the whole plane;
6. inside Ω, *u* solves the **Helmholtz equation** −Δ*u* = *u* (Δ is the ordinary Laplacian ∂²/∂x² + ∂²/∂y²);
7. on the boundary of Ω, *u* = 1; and
8. on the boundary of Ω, the full gradient ∇*u* is zero.

### Why this is "Schiffer's conjecture is false"

Schiffer's conjecture (Yau's problem list, Problem 80) says: if a bounded planar domain has a Neumann eigenfunction
(−Δ*u* = μ*u*, normal derivative zero on the boundary) that is also *constant* on the boundary, and is not itself
constant, then the domain is a disk. The disk does have such functions (built from the Bessel function J₀ at a zero
of J₁).

The theorem gives exactly the forbidden object in a non-disk:

- Conditions 6–8 are the overdetermined problem with the eigenvalue scaled to 1. Since *u* is constant on the
  boundary, its tangential derivative there is zero automatically, so "∇*u* = 0" is the same as "normal derivative
  zero".
- *u* is automatically **not constant** on Ω. If it were constant, Δ*u* = 0 would force *u* = 0 inside, and by
  continuity *u* = 0 on the boundary, contradicting *u* = 1. (The theorem does not state this separately; it follows
  from the listed conditions because Ω is bounded and nonempty, so it has boundary points.)

So the statement is the existence of a counterexample to Schiffer's conjecture in the most restrictive natural
class: bounded, simply connected, C² boundary.

### How it relates to the other headlines

This is "Schiffer 2" of a five-step chain that the challenge file [Schiffer/Challenge.lean lines 1–147](https://github.com/jaumededios/Schiffer/blob/2938e277969c329caf154e48a3d8823f3635c7f1/Schiffer/Challenge.lean#L1-L147) states with
two deliberate `sorry` holes, and that Schiffer/Solution.lean fills in. It is derived from the stronger
[star-shaped version](#/node/Comparator.Schiffer_Star_Shaped) in a few lines.
""",
 [q("Which of these does the theorem assert about the domain Ω?",
    ["It is bounded, simply connected, has C² boundary and is not a disk",
     "It is convex and has real-analytic boundary",
     "It is an annulus",
     "It is a disk with a small bump"], 0,
    "Those are conditions 1–4 (Schiffer/Solution.lean lines 92–99). Convexity and analyticity are not claimed; the paper's analyticity remark is not formalized."),
  q("Why does the theorem not need to say separately that u is nonconstant?",
    ["If u were constant on Ω, −Δu = u would force u = 0 there, contradicting u = 1 on the boundary",
     "Because Lean assumes all functions are nonconstant",
     "It does say it, in the gradient condition",
     "Nonconstancy is not needed for Schiffer's conjecture"], 0,
    "A constant u has Δu = 0, so −Δu = u gives u = 0 in Ω, and continuity carries that to the (nonempty) boundary, where u must be 1."),
  q("The eigenvalue in the statement is 1. Does that lose generality?",
    ["No: scaling the domain by a factor rescales the eigenvalue, so any positive eigenvalue can be normalized to 1",
     "Yes: the classical conjecture is about eigenvalue 0",
     "Yes: the statement only covers the unit disk"], 0,
    "The construction produces a positive eigenvalue λ and then shrinks the domain by √λ (Schiffer/Analysis/SchifferCounterexample.lean lines 597–633)."),
  q("What does the condition 'gradient of u is zero on the boundary' amount to, given u = 1 there?",
    ["The normal derivative is zero (the Neumann condition)",
     "u is constant on the whole plane",
     "The boundary is a circle"], 0,
    "Along the boundary u is constant, so the tangential derivative vanishes; the remaining component of the gradient is the normal derivative."),
 ],
 caveats=[NOT_BUILT,
          "This node calls the statement a counterexample to Schiffer's conjecture because its hypotheses match the usual formulation (bounded, simply connected, C² boundary, Neumann eigenfunction constant on the boundary). The upstream README says the accompanying paper is still upcoming, and nothing here has been peer reviewed.",
          "Regularity is C² only. The informal write-up says the domain can be taken real-analytic, but that upgrade is not part of the Lean statement."],
 widgets=walk("How the proof goes (Schiffer/Solution.lean, lines 92-109)", [
  {"text": "Take the domain Ω and function u from the star-shaped theorem, with all its properties (lines 104–105).", "link": "Comparator.Schiffer_Star_Shaped"},
  {"text": "A nonempty set that is star-shaped about a point is contractible: slide every point along its segment to the centre. Mathlib supplies this as an instance (lines 106–107)."},
  {"text": "Contractible implies path connected, and contractible implies simply connected (Mathlib's SimplyConnectedSpace.ofContractible), line 108–109."},
  {"text": "Every other property (bounded, C² boundary, not a disk, the PDE and boundary conditions) is passed through unchanged (line 109)."},
 ]))


node("Comparator.Schiffer_Star_Shaped",
 "Headline: the star-shaped counterexample",
 "The core existence statement: a bounded, nonempty domain that is star-shaped about the origin, has a C² boundary and "
 "is not a disk, together with a C² function u with −Δu = u inside and u = 1, ∇u = 0 on the boundary. Everything else "
 "in the comparator chain is derived from this.",
 r"""## Plain English

**Theorem (`Schiffer_Star_Shaped`, Schiffer/Solution.lean lines 64–88).** The same statement as
[the simply connected version](#/node/Comparator.Schiffer_SimplyConnected), except that conditions about topology
are replaced by one stronger geometric condition:

- Ω is **star-shaped about the origin**: for every point *x* of Ω, the whole segment from 0 to *x* lies in Ω.

The other conditions are identical: Ω is bounded and nonempty, has a [C² boundary](#/node/Comparator.HasC2Boundary),
is not a [disk](#/node/Comparator.IsEuclideanDisk), and *u* is C² on the plane with −Δ*u* = *u* in Ω and *u* = 1,
∇*u* = 0 on the boundary of Ω.

In the challenge file ([Schiffer/Challenge.lean lines 56–68](https://github.com/jaumededios/Schiffer/blob/2938e277969c329caf154e48a3d8823f3635c7f1/Schiffer/Challenge.lean#L56-L68)) this is the first of two deliberate `sorry` holes. In
Schiffer/Solution.lean it is proved.

### Where the witness comes from

The proof is short because all the work happens elsewhere. It takes the witness from
[PlanarSchifferCounterexample](#/node/Analysis.SchifferCounterexample.PlanarSchifferCounterexample), an internal
version of this statement in which "star-shaped" and "disk" are spelled out by hand rather than with Mathlib's
names. That theorem in turn unpacks the
[constructed counterexample](#/node/exists_schifferCounterexample) from the 115,000-line construction.

### What the domain looks like

From the construction ([radialGraphDomain](#/node/radialGraphDomain)): before rescaling, Ω is a slightly wobbly
disk of radius *N* (a large integer), whose boundary in polar coordinates is *r* = *N* − *h*(*N*φ) with *h* a small
2π-periodic function. So the boundary has *N*-fold rotational symmetry. This statement doesn't say any of that, it
only asserts that some such Ω exists.
""",
 [q("What does 'star-shaped about the origin' mean here?",
    ["Every segment from 0 to a point of Ω lies in Ω",
     "Ω is shaped like a star with N points",
     "Ω is symmetric under rotation about 0",
     "The boundary of Ω passes through 0"], 0,
    "Mathlib's StarConvex ℝ 0 Ω, explained in the comment at Schiffer/Solution.lean line 68."),
  q("Is 'star-shaped' stronger or weaker than 'simply connected' for a nonempty set?",
    ["Stronger: star-shaped implies contractible, hence simply connected",
     "Weaker: there are star-shaped sets with holes",
     "They are unrelated"], 0,
    "That implication is exactly how Schiffer_SimplyConnected is derived (Schiffer/Solution.lean lines 104–109)."),
  q("In the challenge file Schiffer/Challenge.lean, what is the proof of this theorem?",
    ["A deliberate `sorry`: the challenge states it, and the solution file proves it",
     "The same proof as in Solution.lean",
     "It is assumed as an axiom"], 0,
    "Schiffer/Challenge.lean line 68. The comparator workflow checks that Solution.lean proves the same statement."),
 ],
 caveats=[NOT_BUILT,
          "The internal theorem it uses defines its own `IsEuclideanDisk` with the set written as {x : ‖x − c‖ < r}; the proof converts this to Mathlib's `Metric.ball` (Schiffer/Solution.lean lines 83–88). This is a routine rewrite."],
 widgets=walk("How the proof goes (Schiffer/Solution.lean, lines 64-88)", [
  {"text": "Obtain Ω, u and all nine properties from the internal theorem PlanarSchifferCounterexample (lines 76–78).", "link": "Analysis.SchifferCounterexample.PlanarSchifferCounterexample"},
  {"text": "The hand-written star-shaped condition (segments from 0 stay inside) is converted to Mathlib's StarConvex ℝ 0 by a library lemma (line 79)."},
  {"text": "The C² boundary condition is the same definition under two names; unfolding both closes it (lines 81–82).", "link": "Comparator.HasC2Boundary"},
  {"text": "'Not a disk': if Ω were Metric.ball c r, it would also be {x : ‖x − c‖ < r}, contradicting the internal non-disk property (lines 83–88).", "link": "Comparator.IsEuclideanDisk"},
 ]))


node("Comparator.SchifferToPompeiu",
 "Headline: Schiffer data forces the Pompeiu property to fail",
 "If a bounded C² domain carries a Schiffer function (−Δu = u inside, u = 1 and ∇u = 0 on the boundary), the plane "
 "wave cos(Re x) integrates to zero over every rigid copy of the domain. The classical bridge, proved by Green's "
 "identity with cutoffs.",
 r"""## Plain English

**Theorem (`SchifferToPompeiu`, Schiffer/Solution.lean lines 311–325).** Let Ω be a bounded set in the plane with
[C² boundary](#/node/Comparator.HasC2Boundary), and let *u* be a C² function on the plane with

- −Δ*u* = *u* in Ω,
- *u* = 1 on the boundary of Ω,
- ∇*u* = 0 on the boundary of Ω.

Then there is a **continuous, not identically zero** function *f* on the plane whose integral over **every rigid
copy** of Ω is zero. A rigid copy is the image of Ω under a bijective distance-preserving affine map of the plane
(Mathlib's `AffineIsometryEquiv`): any combination of translation, rotation and reflection.

This says Ω **fails the Pompeiu property**: the property that the only continuous function with zero integral over
every congruent copy of Ω is the zero function. In the challenge file this is the second deliberate `sorry`
([Schiffer/Challenge.lean lines 97–110](https://github.com/jaumededios/Schiffer/blob/2938e277969c329caf154e48a3d8823f3635c7f1/Schiffer/Challenge.lean#L97-L110)).

### The witness and why it works

The function is the plane wave *f*(*x*) = cos(Re *x*), that is, cos of the first coordinate. It is continuous and
equals 1 at the origin, so it is not zero.

For a rigid motion *g*, change variables: the integral of *f* over *g*(Ω) equals the integral of *v* = *f* ∘ *g* over
Ω, because rigid motions preserve area. And *v* is again a plane wave of frequency 1, so it also solves −Δ*v* = *v*.
Now put *w* = 1 − *u*. Then Δ*w* + *w* = 1 in Ω, and *w* and its gradient vanish on the boundary. Green's second
identity gives

∫_Ω *v* = ∫_Ω *v*(Δ*w* + *w*) = ∫_Ω *w*(Δ*v* + *v*) + (boundary terms) = 0,

because Δ*v* + *v* = 0 and every boundary term contains *w* or ∇*w*.

### How the Lean proof avoids boundary integrals

Mathlib has no divergence theorem on a C² domain. So the Lean proof replaces *w* by the cut-off functions
*w*·η(*F*/ε), where *F* is the boundary's defining function and η a smooth step. These are compactly supported and C²
on the whole plane, so whole-plane integration by parts applies with no boundary at all. As ε → 0 the cut-off
residual tends to the indicator of Ω, with a uniform bound, and dominated convergence gives the identity. That is
[integral_superlevel_eq_zero_of_schiffer](#/node/Analysis.integral_superlevel_eq_zero_of_schiffer).
""",
 [q("Which function does the proof use as the nonzero function with vanishing integrals?",
    ["The plane wave cos(Re x)", "The Schiffer function u itself", "The indicator function of Ω", "A Bessel function J₀(|x|)"], 0,
    "Schiffer/Solution.lean line 295."),
  q("What counts as a 'rigid copy' of Ω in this statement?",
    ["The image of Ω under any bijective affine isometry: translations, rotations and reflections",
     "Only translations of Ω",
     "Only rotations about the origin",
     "Any scaled copy of Ω"], 0,
    "The quantifier ranges over all bijective affine isometries of the plane (Schiffer/Solution.lean line 322), which includes reflections. Scalings are not isometries."),
  q("Does the theorem assume Ω is simply connected or not a disk?",
    ["No: it holds for any bounded Ω with C² boundary carrying Schiffer data, disks included",
     "Yes, it assumes Ω is not a disk",
     "Yes, it assumes Ω is star-shaped"], 0,
    "The hypotheses are lines 313–318: boundedness, C² boundary and the Schiffer conditions only. Disks carry Schiffer data too, and indeed fail the Pompeiu property."),
  q("Why can the integral of cos(Re x) over Ω not be 'zero by Lean convention'?",
    ["It is continuous and bounded on a bounded open set, so it is genuinely integrable",
     "Lean never uses conventions for integrals",
     "Because Ω is a disk"], 0,
    "Lean's integral returns 0 for non-integrable functions, but a continuous function on a bounded set of finite area is integrable, so the zero is a real computation."),
 ],
 caveats=[NOT_BUILT,
          "The name follows the challenge file's docstring, which calls this the classical implication 'Pompeiu implies Schiffer' written in the contrapositive. Classically the converse (failure of Pompeiu implies Schiffer data, for simply connected Lipschitz domains) is Williams' harder theorem; that converse is not formalized and not needed."],
 widgets=walk("How the proof goes (Schiffer/Solution.lean, lines 282-304 and 205-276)", [
  {"text": "Choose f(x) = cos(Re x). It is continuous (line 296) and nonzero because f(0) = 1 (lines 297–299)."},
  {"text": "For a rigid motion g, rewrite the integral over g(Ω) as the integral over Ω of f ∘ g, using that rigid motions preserve Lebesgue measure (lines 112–132, 301)."},
  {"text": "Show f ∘ g is a unit-frequency plane wave: it is cos of a unit linear functional plus a constant, and its Laplacian is minus itself (lines 135–201)."},
  {"text": "Set w = 1 − u. Then Δw + w = 1 in Ω, and w and its derivative vanish on the boundary {F = 0} (lines 238–269)."},
  {"text": "Apply the cutoff Green identity to w and v = f ∘ g to conclude the integral over Ω is zero (lines 270–274).", "link": "Analysis.integral_superlevel_eq_zero_of_schiffer"},
  {"text": "The empty-domain case is trivial (lines 275–276)."},
 ]))


node("Comparator.Pompeiu_SimplyConnected",
 "Headline: a simply connected planar domain without the Pompeiu property",
 "There is a bounded, simply connected domain with C² boundary, not a disk, and a continuous nonzero function whose "
 "integral over every rigid copy of the domain vanishes. The Pompeiu conjecture says only disks can fail this way.",
 r"""## Plain English

**Theorem (`Pompeiu_SimplyConnected`, Schiffer/Solution.lean lines 351–370).** There is a set Ω in the plane that is

- bounded and nonempty,
- path connected and simply connected,
- has a [C² boundary](#/node/Comparator.HasC2Boundary),
- is not a [disk](#/node/Comparator.IsEuclideanDisk),

and a function *f* on the plane that is continuous, not identically zero, and integrates to zero over every image of
Ω under a translation, rotation or reflection.

### Why this matters

The **Pompeiu problem** (1929) asks which domains Ω have the *Pompeiu property*: the only continuous *f* with zero
integral over every congruent copy of Ω is *f* = 0. Squares, ellipses and polygons have it; disks do not (there are
nonzero functions, built from Bessel functions, with zero integral over every disk of a given radius). The
**Pompeiu conjecture** says that among bounded simply connected domains with reasonable boundary, the disk is the
only one that fails. This theorem gives a non-disk that fails.

The companion statement `Pompeiu_Star_Shaped` (Schiffer/Solution.lean lines 329–347) is the same with "star-shaped
about the origin" in place of the two topological conditions. The statement in the
[Formal Conjectures form](#/node/FormalConjecturesComparator.not_hasPompeiuProperty_imp_ball) repackages this one.
""",
 [q("Which domains are classically known to fail the Pompeiu property?",
    ["Disks", "Squares", "Ellipses", "All polygons"], 0,
    "Disks fail it; the conjecture is that they are the only bounded simply connected examples. The theorem gives a non-disk example."),
  q("How is this theorem proved from the others?",
    ["Take the simply connected Schiffer counterexample and feed its data to the Schiffer-to-Pompeiu bridge",
     "By a separate 100,000-line construction",
     "By computing the integral numerically"], 0,
    "Schiffer/Solution.lean lines 364–370."),
  q("Does the theorem say the function f is the same for every rigid copy of Ω?",
    ["Yes: one f is chosen first, then its integral vanishes over every rigid copy",
     "No: a different f may be chosen for each copy"], 0,
    "The existential over f comes before the universal over rigid motions (Schiffer/Solution.lean lines 359–363), which is what the Pompeiu property needs."),
 ],
 caveats=[NOT_BUILT],
 widgets=walk("How the proof goes (Schiffer/Solution.lean, lines 351-370)", [
  {"text": "Take Ω and u from the simply connected Schiffer theorem (lines 364–366).", "link": "Comparator.Schiffer_SimplyConnected"},
  {"text": "Apply the Schiffer-to-Pompeiu bridge to Ω and u, which needs only boundedness, the C² boundary and the Schiffer conditions; it returns f (lines 367–368).", "link": "Comparator.SchifferToPompeiu"},
  {"text": "Package Ω's geometric properties with f (lines 369–370)."},
 ]))


node("FormalConjecturesComparator.not_hasPompeiuProperty_imp_ball",
 "Headline: the Formal Conjectures form of the Pompeiu conjecture is false",
 "The Formal Conjectures statement 'in every dimension, an admissible domain failing the Pompeiu property is a ball' "
 "is false. The proof moves the planar counterexample into Mathlib's ℝ² (dimension 2, N = 1).",
 r"""## Plain English

**Theorem (`not_hasPompeiuProperty_imp_ball`, Schiffer/FormalConjecturesSolution.lean lines 446–469).** It is
**not** true that for every dimension *N* + 1 and every set Ω in (*N* + 1)-dimensional Euclidean space:

> if Ω is an [admissible domain](#/node/FormalConjecturesComparator.IsAdmissibleDomain) (bounded, open, connected,
> simply connected, Lipschitz boundary), and Ω does **not** have the
> [Pompeiu property](#/node/FormalConjecturesComparator.HasPompeiuProperty), then Ω is a
> [ball](#/node/FormalConjecturesComparator.IsBall).

The challenge version ([Schiffer/FormalConjecturesChallenge.lean lines 66–69](https://github.com/jaumededios/Schiffer/blob/2938e277969c329caf154e48a3d8823f3635c7f1/Schiffer/FormalConjecturesChallenge.lean#L66-L69)) has the same statement with a deliberate
`sorry`. According to its header, the definitions follow the formulation in Google DeepMind's `formal-conjectures`
repository, keeping only the "hard direction" of an if-and-only-if.

### What it takes to refute it

One counterexample suffices: a dimension (here 2, written *N* = 1) and a set that is admissible, fails Pompeiu, and
is not a ball. The planar domain from [Pompeiu_SimplyConnected](#/node/Comparator.Pompeiu_SimplyConnected) is that
set, after being transported from ℂ to `EuclideanSpace ℝ (Fin 2)` by the standard isometry *z* ↦ (Re *z*, Im *z*).

The only real work is the boundary condition: the planar theorem gives a C² boundary in the "regular level set"
form, while Formal Conjectures asks for a **Lipschitz** boundary in the "locally a subgraph after a rigid motion"
form. A C² regular level set is locally a C¹ graph (implicit function theorem), and C¹ functions are locally
Lipschitz; the file proves this conversion in about 90 lines (Schiffer/FormalConjecturesSolution.lean lines 256–344).
""",
 [q("What does this theorem refute?",
    ["The claim that, in every dimension, admissible domains failing the Pompeiu property are balls",
     "The claim that balls fail the Pompeiu property",
     "The Pompeiu property for all polygons",
     "Schiffer's conjecture in dimension 3"], 0,
    "The statement is the negation of a universal claim over N and Ω (Schiffer/FormalConjecturesSolution.lean lines 446–448)."),
  q("In which dimension is the counterexample given?",
    ["Dimension 2 (N = 1)", "Every dimension", "Dimension 3", "Dimension 1"], 0,
    "The proof applies the hypothetical universal claim at N = 1 (line 469). Higher dimensions are not addressed."),
  q("Why is a boundary-conversion lemma needed?",
    ["The planar result has a C² level-set boundary, but the Formal Conjectures definition asks for local Lipschitz subgraphs",
     "Because Lipschitz boundaries are stronger than C² ones in general",
     "To prove the domain is bounded"], 0,
    "Schiffer/FormalConjecturesSolution.lean lines 256–386 turn the regular C² superlevel set into local Lipschitz subgraphs."),
 ],
 caveats=[NOT_BUILT,
          "This site did not compare the definitions with the actual file in google-deepmind/formal-conjectures. The challenge header says it follows that formulation and keeps only the 'hard direction'; refuting one direction of an equivalence refutes the equivalence."],
 widgets=walk("How the proof goes (Schiffer/FormalConjecturesSolution.lean, lines 446-469)", [
  {"text": "Assume the universal claim, and take Ω, f from the planar Pompeiu counterexample (lines 449–452).", "link": "Comparator.Pompeiu_SimplyConnected"},
  {"text": "Ω is open because it is {F > 0} for a continuous F (lines 453–456).", "link": "Comparator.HasC2Boundary"},
  {"text": "The image of Ω in EuclideanSpace ℝ (Fin 2) has Lipschitz boundary, by the implicit-function conversion of the C² level set (lines 457–458, using lines 256–386).", "link": "FormalConjecturesComparator.HasLipschitzBoundary"},
  {"text": "Bounded, open, connected and simply connected all transfer along the isometry, giving admissibility (lines 459–465).", "link": "FormalConjecturesComparator.IsAdmissibleDomain"},
  {"text": "The transported Ω fails the Pompeiu property: pull rigid motions of ℝ² back to ℂ and change variables (lines 466–467, using lines 389–434).", "link": "FormalConjecturesComparator.HasPompeiuProperty"},
  {"text": "The universal claim at N = 1 would make it a ball, so Ω would be a disk; contradiction (lines 468–469, using lines 437–443).", "link": "FormalConjecturesComparator.IsBall"},
 ]))


node("exists_schifferCounterexample",
 "Headline: the construction produces a Schiffer counterexample",
 "A `SchifferCounterexample` exists: an N-fold symmetric perturbation of a disk of integer radius N carrying "
 "Schiffer data. It is built by landing a bifurcating branch on a flat cone at an integer radius and unfolding the "
 "cone to the plane.",
 r"""## Plain English

**Theorem (`exists_schifferCounterexample`, Schiffer/Main.lean lines 8–10).** The type
[SchifferCounterexample](#/node/SchifferCounterexample) is nonempty: there is at least one bundle of data consisting of

- an integer *N* ≥ 2 and a small 2π-periodic C² function *h* (the [graph](#/node/PeriodicGraph));
- the domain whose boundary in polar coordinates is *r* = *N* − *h*(*N*φ) ([radialGraphDomain](#/node/radialGraphDomain));
- a positive number λ and a C² function *u* with −Δ*u* = λ*u* in the domain, *u* = 1 on the boundary and zero normal
  derivative on the boundary;
- proofs that *h* and *u* are nonconstant and the domain is not a disk.

Everything the [headline comparator theorems](#/node/Comparator.Schiffer_Star_Shaped) need is extracted from this.

### The idea of the construction (from the project's informal write-up)

Bifurcation from disks doesn't work directly: a disk's Schiffer function needs a common zero of two Bessel functions
of different integer orders, and those don't exist (Bourget's hypothesis, proved by Siegel). So the construction
leaves the plane:

1. **Cones.** An *N*-fold symmetric planar picture, divided by rotation through 2π/*N*, is a flat cone. Flat cones
   exist for every real "reciprocal aperture" *R*, not just integers, which gives a continuous parameter. On these
   cones there are genuine crossings where a nonradial mode bifurcates from the radial solution.
2. **Uniform branch.** For crossings with *R* large, a nonlinear branch of solutions is built by a quantitative
   Lyapunov–Schmidt reduction, with estimates that do not depend on *R*.
3. **Drift.** Along the branch, *R* decreases quadratically with the amplitude, by a definite amount
   ([uniform_quadratic_drop](#/node/Landing.uniform_quadratic_drop)).
4. **Density.** Using Kronecker-type density of Bessel zeros, there are crossings with *R* just above an integer *N*,
   closer than that definite drop ([exists_nearIntegerCrossing](#/node/Density.exists_nearIntegerCrossing)).
5. **Landing.** By the intermediate value theorem, some nonzero amplitude has *R* exactly *N*
   ([exists_landedConeSolution](#/node/Landing.exists_landedConeSolution)).
6. **Unfolding.** An integer cone is the plane divided by an *N*-fold rotation, so the landed solution unfolds to an
   *N*-fold symmetric planar solution, completed near the origin by a Fourier–Bessel series
   ([liftLandedConeSolution](#/node/Lift.liftLandedConeSolution), [counterexampleOfLanded](#/node/Lift.counterexampleOfLanded)).
""",
 [q("What kind of statement is `exists_schifferCounterexample`?",
    ["An existence statement: the structure SchifferCounterexample has an inhabitant",
     "A uniqueness statement about Schiffer domains",
     "A definition of a specific numerical domain with N = 28"], 0,
    "Schiffer/Main.lean line 8. The N = 28 picture in the write-up is illustrative and not part of the proof."),
  q("Why does the construction pass through cones instead of perturbing disks directly?",
    ["Disks have no transverse spectral crossings to bifurcate from; cones give a continuous parameter R",
     "Because the Laplacian is not defined on disks in Mathlib",
     "Because cones are star-shaped and disks are not"], 0,
    "Distinct-order Bessel functions have no common positive zeros, so disks have no nonradial kernel to bifurcate along; this is the motivation in the informal write-up."),
  q("What is special about the landed radius?",
    ["It is an integer N, so the cone is exactly the plane divided by an N-fold rotation and can be unfolded",
     "It equals 1",
     "It is irrational, which avoids resonances"], 0,
    "`radius_integer` in LandedConeSolution (Schiffer/Landing/IntegerRadius.lean line 27)."),
 ],
 caveats=[NOT_BUILT,
          "The six-step outline is a summary of the project's informal write-up (informalization/parts/01_main_theorem.tex) and module READMEs, checked against the top-level Lean files only. The tens of thousands of lines of Bessel, cone and bifurcation estimates behind steps 1–4 were not read for this site."],
 widgets=walk("How the proof goes (Schiffer/Main.lean, lines 8-10)", [
  {"text": "Obtain a landed cone solution: a uniform cone branch at a crossing just above an integer N, with an amplitude where its radius is exactly N (line 9).", "link": "Landing.exists_landedConeSolution"},
  {"text": "Unfold it to the plane and package the result, with its nontriviality proofs, as a SchifferCounterexample (line 10).", "link": "Lift.counterexampleOfLanded"},
 ]))
