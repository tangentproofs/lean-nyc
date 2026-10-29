NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

S = "Origami/lightweight_definitions/Structures.lean"
N = "Origami/lightweight_definitions/Normalisation.lean"
R = "Origami/lightweight_definitions/Reflection.lean"


# ---------- the basic objects (Structures.lean) ----------

node("Point",
 "Point: a pair of real coordinates",
 "A point is just an (x, y) pair of real numbers. There is no paper: the whole construction lives in the infinite "
 "real plane.",
 rf"""## Plain English

**Definition (`Point`, {S} lines 4–6).** A point has two real fields, *x* and *y*. Two points are equal exactly
when both coordinates agree ({N} line 3 turns on the extensionality principle that says so).

### Things to notice

- Coordinates are **real** numbers, not rationals or constructible numbers. So the library can talk about a fold
  whose crease involves a cube root (see [huzita_6](#/node/huzita_6)) without first building a number system for it.
- There is no square of paper, no boundary and no layering of paper. Everything is analytic geometry in the plane.
  (A separate, older experiment with faces and layer order lives in `Origami/paper_folding/`; it is not imported by
  the library and is not covered on this site.)
""",
 [q("What are a point's coordinates?",
    ["Two real numbers", "Two rationals", "Two integers", "A point on the unit square"], 0,
    f"{S} lines 4–6."),
  q("Does a Point carry any information about being on the paper?",
    ["No; points range over the whole real plane", "Yes, it must lie in the unit square",
     "Yes, it records which layer it is on"], 0,
    f"The structure has only the fields x and y ({S} lines 4–6)."),
 ])


node("Line",
 "Line: ax + by + c = 0, in one canonical form",
 "A line is stored as the equation ax + by + c = 0, but normalised so that each geometric line has exactly one "
 "representation: either a = 1, or a = 0 and b = 1. That normalisation is what makes the uniqueness claims meaningful.",
 rf"""## Plain English

**Definition (`Line`, {S} lines 8–13).** A line has three real numbers *a*, *b*, *c*, standing for the equation
*a·x + b·y + c = 0*, together with two proofs:

- **nontrivial:** *a* and *b* are not both zero (otherwise the "equation" would not describe a line);
- **normalized:** either *a* = 1, or *a* = 0 and *b* = 1.

### Why the normalisation matters

The equations *x + 2y − 3 = 0* and *2x + 4y − 6 = 0* describe the same line. Without a rule, the type would contain
both, and a claim like "there is **exactly one** fold through two points" ([huzita_1](#/node/huzita_1)) would be
false for the boring reason that every line has infinitely many equations. Dividing through by *a* (or by *b* when
*a* = 0) picks one representative. The project proves that this works:
[Line.eq_of_on_line](#/node/Line.eq_of_on_line) says two `Line`s containing the same points are equal as Lean
values.

To build a line from an arbitrary equation, the project uses [mk_line](#/node/mk_line), which performs this division.
""",
 [q("Which of these is a valid `Line` value (a, b, c)?",
    ["(1, 2, −3)", "(2, 4, −6)", "(0, 0, 1)", "(0, 3, 1)"], 0,
    f"Only (1, 2, −3) satisfies the normalisation a = 1, or a = 0 and b = 1 ({S} line 13)."),
  q("Why normalise at all?",
    ["So that each geometric line has one representative and 'exactly one fold' can be stated with ordinary equality",
     "To make the coefficients rational", "To keep lines inside the paper"], 0,
    "Without it, proportional equations would be distinct values of the type; see Line.eq_of_on_line."),
  q("What does the `nontrivial` field rule out?",
    ["a = b = 0", "c = 0", "Vertical lines", "Lines through the origin"], 0,
    f"{S} line 12."),
 ])


node("Fold",
 "Fold: a crease line",
 "A fold is literally the same thing as a line: the crease. Folding means reflecting across that line.",
 rf"""## Plain English

**Definition (`Fold`, {S} line 15).** `Fold` is another name for [Line](#/node/Line). The source comment says the
second name is only there to make statements easier to read: a `Fold` argument plays the role of the crease, a
`Line` argument the role of a line being moved or hit.

What a fold *does* is given by two reflection maps: [f_places_p](#/node/f_places_p) (where a point goes) and
[f_places_l](#/node/f_places_l) (where a line goes).

### Things to notice

- A fold is the whole crease line, so "folding" here reflects the **entire plane**. There is no notion of folding
  only one flap, or of which side moves.
""",
 [q("What is a Fold in this library?",
    ["Exactly a Line (the crease)", "A pair of lines", "A reflection matrix", "A sequence of creases"], 0,
    f"{S} line 15."),
  q("When a fold is applied to a point, which points move?",
    ["Every point not on the crease is reflected across it", "Only points on one side", "Only points on the paper"], 0,
    "The reflection f_places_p is defined for every point of the plane."),
 ])


node("f_through_p",
 "f_through_p: the crease passes through a point",
 "A crease passes through a point when the point satisfies the crease's equation.",
 rf"""## Plain English

**Definition (`f_through_p`, {S} lines 19–20).** For a fold *f* with equation *a·x + b·y + c = 0* and a point *p*,
`f_through_p f p` says *a·pₓ + b·p_y + c = 0*.

It is word for word the same condition as [on_line](#/node/on_line); the project keeps both names so a statement can
say "the crease goes through *p*" in one place and "the point lies on line *l*" in another. A lemma records that the
two agree ({N} line 35).

A useful fact: a fold leaves a point where it is **exactly when** the crease passes through it
([f_places_p_eq_self_iff](#/node/f_places_p_eq_self_iff)).
""",
 [q("When does `f_through_p f p` hold?",
    ["When p satisfies the equation of the crease f", "When folding f moves p", "When p is on the paper"], 0,
    f"{S} lines 19–20."),
  q("How does it relate to `on_line`?",
    ["It is the same condition under another name", "It is the negation", "It is stronger"], 0,
    f"{N} line 35 proves they are interchangeable."),
 ])


node("on_line",
 "on_line: a point lies on a line",
 "A point lies on a line when it satisfies the line's equation.",
 rf"""## Plain English

**Definition (`on_line`, {S} lines 22–23).** `on_line l p` says *a·pₓ + b·p_y + c = 0* for the coefficients
*a*, *b*, *c* of [Line](#/node/Line) *l*. It is the same formula as [f_through_p](#/node/f_through_p).

The Huzita axioms mostly use it in the form "after folding, the image of *p* lies on *l*", i.e. *p*'s
[reflection](#/node/f_places_p) satisfies *l*'s equation.
""",
 [q("Which condition is `on_line l p`?",
    ["a·pₓ + b·p_y + c = 0", "a·pₓ + b·p_y + c > 0", "p is the foot of the perpendicular from the origin to l"], 0,
    f"{S} lines 22–23."),
 ])


node("f_places_p",
 "f_places_p: where a fold sends a point",
 "Folding along a crease sends a point to its mirror image across the crease, given by the usual reflection formula.",
 rf"""## Plain English

**Definition (`f_places_p`, {S} lines 25–28).** For a crease *a·x + b·y + c = 0* and a point *p*, let
*d* = (*a·pₓ + b·p_y + c*) / (*a*² + *b*²). Then the folded point is *p* − 2*d*·(*a*, *b*).

This is the standard formula for reflection across a line: (*a*, *b*) is the normal direction of the crease and
*d·(a, b)* is the vector from the crease to *p*, so subtracting it twice lands on the mirror image.

### Facts the project proves about it (all in {R})

- Folding twice returns the point (`f_places_p_involutive`, lines 57–59).
- It fixes a point exactly when the crease passes through it ([f_places_p_eq_self_iff](#/node/f_places_p_eq_self_iff), lines 61–77).
- It preserves squared distances between points (`f_places_p_dist2`, lines 95–101).
- Its image lies on a line *l* exactly when a single polynomial equation holds (`on_line_f_places_p`, lines 15–34);
  most Huzita proofs reduce to this equation.
""",
 [q("Applying the same fold twice to a point gives…",
    ["the original point", "the foot of the perpendicular on the crease", "a point twice as far away"], 0,
    f"f_places_p_involutive, {R} lines 57–59."),
  q("Which points does a fold leave unchanged?",
    ["Exactly the points on the crease", "Only the origin", "None"], 0,
    f"f_places_p_eq_self_iff, {R} lines 61–77."),
  q("Why is there no division-by-zero problem in the formula?",
    ["A line's a and b are never both zero, so a² + b² > 0",
     "Lean defines x/0 = 0 and the project relies on it here",
     "The formula only applies to points on the paper"], 0,
    f"The `nontrivial` field of Line ({S} line 12); {N} lines 12–16 prove a² + b² > 0."),
 ])


node("f_places_l",
 "f_places_l: where a fold sends a line",
 "Folding sends a line to its mirror image, computed by a formula on the coefficients and then renormalised to the "
 "canonical form.",
 rf"""## Plain English

**Definition (`f_places_l`, {S} lines 31–53).** Given a crease *f* and a line *l*, the definition computes new
coefficients *a′*, *b′*, *c′* from those of *l* and *f* (lines 32–35), proves that *a′* and *b′* are not both zero
(lines 36–43, via the identity *a′*² + *b′*² = (*l.a*² + *l.b*²)(*f.a*² + *f.b*²)²), and then divides through to put
the result in [canonical form](#/node/Line) (lines 44–53), exactly as [mk_line](#/node/mk_line) would.

### Why it is the right map

The definition is just a formula; the project proves it means what it should. In {R}:

- A point lies on the folded line exactly when its own reflection lies on the original line
  (`on_line_f_places_l`, lines 155–158). So the folded line really is the set of mirror images.
- Folding a line twice gives it back (`f_places_l_involutive`, lines 171–173).
- The crease is fixed (`f_places_l_self`, lines 167–169), and so is every line perpendicular to it
  (`perp_places_self`, lines 160–165).
""",
 [q("Which statement is proved about the folded line?",
    ["A point q is on it exactly when the reflection of q is on the original line",
     "It is always parallel to the original", "It always passes through the origin"], 0,
    f"on_line_f_places_l, {R} lines 155–158."),
  q("Which lines are unchanged by a fold?",
    ["The crease itself and every line perpendicular to it", "Only the crease", "Every line through the origin"], 0,
    f"f_places_l_self and perp_places_self, {R} lines 160–169."),
  q("What is the last thing the definition does?",
    ["Divides the coefficients so the result has a = 1, or a = 0 and b = 1", "Rounds to rationals",
     "Checks the line meets the paper"], 0,
    f"{S} lines 44–53."),
 ])


node("perpendicular",
 "perpendicular: normals at right angles",
 "Two lines are perpendicular when their normal vectors (a, b) have zero dot product.",
 rf"""## Plain English

**Definition (`perpendicular`, {S} line 56).** Lines *l*₁ and *l*₂ are perpendicular when
*l*₁.*a*·*l*₂.*a* + *l*₁.*b*·*l*₂.*b* = 0, i.e. their normal vectors are orthogonal. This is the usual notion. The
project proves it is symmetric (Origami/lightweight_definitions/Relations.lean lines 20–21) and that two lines
perpendicular to the same line are parallel (Relations.lean lines 37–44).
""",
 [q("Which lines are perpendicular to the x-axis (0, 1, 0)?",
    ["Exactly the vertical lines (a = 1, b = 0)", "Exactly the horizontal lines", "All lines through the origin"], 0,
    f"The condition becomes l.b = 0 ({S} line 56), and normalisation then forces a = 1."),
 ])


node("parallel",
 "parallel: proportional normals (including equal lines)",
 "Two lines are parallel when their normal vectors are proportional. A line counts as parallel to itself.",
 rf"""## Plain English

**Definition (`parallel`, {S} line 58).** Lines *l*₁, *l*₂ are parallel when
*l*₁.*a*·*l*₂.*b* − *l*₂.*a*·*l*₁.*b* = 0: the 2×2 determinant of their normals vanishes. Because lines are
normalised, this is the same as having equal *a* and *b* (`parallel_iff_normals_eq`,
Origami/lightweight_definitions/Relations.lean lines 5–18).

### Things to notice

- **Equal lines count as parallel** (`parallel_refl`, Relations.lean line 27). So the hypothesis "not parallel" in
  [huzita_6](#/node/huzita_6) and [huzita_7](#/node/huzita_7) means "the two lines cross in exactly one point".
""",
 [q("Is a line parallel to itself under this definition?",
    ["Yes", "No", "Only if it passes through the origin"], 0,
    "parallel_refl, Origami/lightweight_definitions/Relations.lean line 27."),
  q("For normalised lines, `parallel l₁ l₂` is the same as…",
    ["equal a and equal b coefficients", "equal c coefficients", "a zero dot product of normals"], 0,
    "parallel_iff_normals_eq, Origami/lightweight_definitions/Relations.lean lines 5–18."),
 ])


node("dist2",
 "dist2: squared distance between points",
 "The squared Euclidean distance between two points. Working with squares avoids square roots.",
 rf"""## Plain English

**Definition (`dist2`, {R} line 79).** dist2(*p*, *q*) = (*pₓ* − *qₓ*)² + (*p_y* − *q_y*)². The project proves it is
symmetric, zero exactly when the points coincide, and preserved by every fold ({R} lines 81–101).
""",
 [q("What is dist2((0,0), (3,4))?",
    ["25", "5", "7", "12"], 0,
    f"3² + 4² = 25; dist2 is the squared distance ({R} line 79)."),
 ])


node("dist2_line",
 "dist2_line: squared distance from a point to a line",
 "The squared distance from a point to a line, by the textbook formula (ax + by + c)² / (a² + b²).",
 rf"""## Plain English

**Definition (`dist2_line`, {R} lines 103–104).** dist2_line(*l*, *p*) = (*a·pₓ* + *b·p_y* + *c*)² / (*a*² + *b*²).
This is the square of the usual point-to-line distance. The project proves the property that justifies the name:
it is at most the squared distance from *p* to any point of *l* (`dist2_line_le_dist2`, {R} lines 119–126), and it
is zero exactly when *p* is on *l* (lines 110–117).

It appears in the exact condition for [Huzita's fifth axiom](#/node/huzita_5_iff).
""",
 [q("What does `dist2_line_le_dist2` say?",
    ["The squared point-to-line distance is at most the squared distance to any point of the line",
     "The squared point-to-line distance equals the distance to the origin",
     "dist2_line is always positive"], 0,
    f"{R} lines 119–126."),
 ])


node("mk_line",
 "mk_line: turn any equation into a canonical Line",
 "Takes any equation ax + by + c = 0 with (a, b) ≠ (0, 0) and returns the canonical Line, by dividing through by a "
 "(or by b when a = 0). All the explicit folds in the library are built with it.",
 rf"""## Plain English

**Definition (`mk_line`, {N} lines 37–45).** If *a* ≠ 0, the result has coefficients (1, *b/a*, *c/a*); otherwise
(0, 1, *c/b*). Either way the [normalisation](#/node/Line) holds.

### Key facts ({N})

- The result is a nonzero multiple of (*a*, *b*, *c*) (`exists_scale_mk_line`, lines 51–59).
- A point is on it exactly when it satisfies the original equation (`on_line_mk_line`, lines 61–71).
- `eq_mk_line` (lines 119–122): any Line whose coefficients are a nonzero multiple of (*a*, *b*, *c*) **is**
  mk_line(*a*, *b*, *c*). This is the workhorse of every uniqueness proof: show the other fold's coefficients are
  proportional, conclude equality.
""",
 [q("What does mk_line(2, 4, −6) return?",
    ["The line (1, 2, −3)", "The line (2, 4, −6)", "Nothing; it needs a = 1"], 0,
    f"It divides through by a = 2 ({N} lines 38–41)."),
  q("How is `eq_mk_line` used in the uniqueness proofs?",
    ["Showing a fold's coefficients are proportional to a given triple proves it equals the canonical fold",
     "It computes a cube root", "It shows two folds are parallel"], 0,
    f"{N} lines 119–122; e.g. Origami/lightweight_definitions/Huzita_axioms.lean line 32."),
 ])


node("Line.eq_of_on_line",
 "Lemma: lines with the same points are equal",
 "If two Lines contain exactly the same points, they are the same Lean value. This is the formal payoff of the "
 "canonical form.",
 rf"""## Plain English

**Theorem (`Line.eq_of_on_line`, {N} lines 155–170).** If, for every point *p*, *p* is on *l*₁ exactly when it is
on *l*₂, then *l*₁ = *l*₂.

### How the proof goes

1. Pick a point *q* on *l*₁ (`exists_on_line`, lines 144–147), and a second point on *l*₁ obtained by moving *q*
   along the direction (−*b*, *a*) of *l*₁ (lines 158–161).
2. Both points are on *l*₂ too. Subtracting the two equations shows *l*₂'s normal is proportional to *l*₁'s
   (line 166), so `exists_scale` gives a nonzero factor *k* (line 167).
3. Plugging *q* back in shows the *c* coefficients scale by the same *k* (line 170).
4. `Line.eq_of_scale` (lines 80–89) finishes: two normalised lines whose coefficients differ by a factor *k* must
   have *k* = 1, so they are equal.

It is used, for example, to show that folding a line twice gives it back
({R} lines 171–173).
""",
 [q("Without the normalisation in Line, would this lemma be true?",
    ["No: (1, 2, −3) and (2, 4, −6) have the same points but would be different values", "Yes, always",
     "Only for vertical lines"], 0,
    f"The proof's last step, Line.eq_of_scale ({N} lines 80–89), uses normalisation to force k = 1."),
 ])


node("f_places_p_eq_self_iff",
 "Lemma: a fold fixes exactly the points on its crease",
 "Folding leaves a point in place if and only if the crease passes through it. Several Huzita proofs use this to "
 "handle degenerate cases by folding through the given points.",
 rf"""## Plain English

**Theorem (`f_places_p_eq_self_iff`, {R} lines 61–77).** For a fold *f* and point *p*:
[f_places_p](#/node/f_places_p) *f p* = *p* exactly when [f_through_p](#/node/f_through_p) *f p*.

### How the proof goes

- If the point is fixed, comparing coordinates gives *a·d* = 0 and *b·d* = 0, where *d* is the reflection
  coefficient (lines 66–70). Combining them gives (*a*² + *b*²)·*d* = 0, hence the crease equation is zero at *p*
  (lines 71–74).
- Conversely, if *p* is on the crease then *d* = 0 and nothing moves (lines 75–77).

It is the fact behind the degenerate cases of [huzita_5](#/node/huzita_5) and [huzita_6](#/node/huzita_6), and the
comment in Origami/lightweight_definitions/Haga.lean lines 27–28 uses it to explain why
[huzita_2](#/node/huzita_2) needs *p*₁ ≠ *p*₂.
""",
 [q("A fold fixes the point p. What follows?",
    ["The crease passes through p", "p is the origin", "The crease is horizontal"], 0,
    f"{R} lines 61–74."),
 ])


# ---------- extra quiz questions (every node gets at least three) ----------
EXTRA = {
 "Point": [
  q("When are two Points equal?",
    ["When both coordinates are equal", "When they are the same distance from the origin", "Never; each is unique"], 0,
    f"Point extensionality, {N} line 3."),
 ],
 "Fold": [
  q("Why does the library have both the names Fold and Line?",
    ["Readability only: a Fold argument is a crease, a Line argument is a line being moved or hit",
     "Folds are normalised differently", "Folds carry an orientation"], 0,
    f"The comment at {S} line 16."),
 ],
 "f_through_p": [
  q("A fold f passes through p. What does folding along f do to p?",
    ["Leaves it where it is", "Moves it to the origin", "Reflects it to the other side"], 0,
    "f_places_p_eq_self_iff."),
 ],
 "on_line": [
  q("Is on_line the same formula as f_through_p?",
    ["Yes, word for word", "No, it uses a strict inequality", "No, it uses squared distance"], 0,
    f"{S} lines 19–23."),
  q("What does 'p lands on l after folding along f' mean in this library?",
    ["The reflection of p in f satisfies the equation of l", "p and l are both on the crease",
     "l passes through p"], 0,
    "That is on_line applied to f_places_p."),
 ],
 "perpendicular": [
  q("Is perpendicularity symmetric?",
    ["Yes, proved in Relations.lean", "No"], 0,
    "perpendicular_comm, Origami/lightweight_definitions/Relations.lean lines 20–21."),
  q("Two lines perpendicular to the same line are…",
    ["parallel", "perpendicular", "equal"], 0,
    "parallel_of_perpendicular, Origami/lightweight_definitions/Relations.lean lines 37–44."),
 ],
 "parallel": [
  q("Can two lines be both parallel and perpendicular?",
    ["No; the project proves this is impossible", "Yes, if they are equal", "Yes, if they pass through the origin"], 0,
    "not_parallel_and_perpendicular, Origami/lightweight_definitions/Relations.lean lines 46–52."),
 ],
 "dist2": [
  q("Does folding change the squared distance between two points?",
    ["No; every fold preserves it", "Yes, it doubles it", "Only for points on the crease"], 0,
    f"f_places_p_dist2, {R} lines 95–101."),
  q("When is dist2(p, q) = 0?",
    ["Exactly when p = q", "When p and q are on the same line", "Never"], 0,
    f"dist2_eq_zero_iff, {R} lines 86–93."),
 ],
 "dist2_line": [
  q("When is dist2_line(l, p) zero?",
    ["Exactly when p is on l", "When p is the origin", "Never"], 0,
    f"dist2_line_eq_zero_iff, {R} lines 110–117."),
  q("Is dist2_line the distance or the squared distance?",
    ["The squared distance", "The distance", "The distance times a² + b²"], 0,
    f"{R} lines 103–104: the numerator is squared."),
 ],
 "mk_line": [
  q("What does mk_line(0, 3, 6) return?",
    ["The line (0, 1, 2)", "The line (0, 3, 6)", "The line (1, 0, 2)"], 0,
    f"When a = 0 it divides by b ({N} lines 42–45)."),
 ],
 "Line.eq_of_on_line": [
  q("What does the lemma conclude?",
    ["Two Lines with the same points are equal Lean values", "Two lines with the same c are equal",
     "Every line contains the origin"], 0,
    f"{N} lines 155–156."),
  q("Which step of the proof uses the normalisation?",
    ["The final step, which forces the scale factor k to be 1", "Picking a point on l₁", "None"], 0,
    f"Line.eq_of_scale, {N} lines 80–89."),
 ],
 "f_places_p_eq_self_iff": [
  q("A point p is not on the crease. After folding, is it still at p?",
    ["No, it moves", "Yes", "Only if p is on the paper"], 0,
    "That is the contrapositive of the right-to-left direction."),
  q("Which identity does the proof use to get from the coordinate equations to the crease equation?",
    ["Combining a·d = 0 and b·d = 0 into (a² + b²)·d = 0", "The Pythagorean theorem", "The intermediate value theorem"], 0,
    f"{R} lines 69–73."),
 ],
}
for n_ in NODES:
    n_["quiz"] = n_["quiz"] + EXTRA.get(n_["id"], [])
