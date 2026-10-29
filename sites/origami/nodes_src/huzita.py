NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]

H = "Origami/lightweight_definitions/Huzita_axioms.lean"
SH = "Origami/lightweight_definitions/Sharpness.lean"
CR = "Origami/lightweight_definitions/CubicRoot.lean"
NB = "Not built for this site: \"proved\" means the file contains a complete-looking proof with no sorry, not that Lean checked it."
PLANE = ("The plane is the whole real plane, not a square of paper: a fold here is a reflection of the entire plane, "
         "so the axioms say nothing about whether the crease meets a finite sheet.")


node("huzita_1",
 "Axiom 1: exactly one crease through two points",
 "Through two different points there is exactly one crease. In this library the 'axiom' is a theorem, proved from "
 "the coordinate model.",
 rf"""## Plain English

**Theorem (`huzita_1`, {H} lines 23–32).** If *p*₁ ≠ *p*₂, there is exactly one [Fold](#/node/Fold) whose crease
[passes through](#/node/f_through_p) both points.

This is the first Huzita–Hatori axiom. Classically these seven "axioms" describe the single-fold operations an
origamist may use; here every one is a **theorem** about lines and reflections in the real plane.

### How the proof goes

- **Existence:** the explicit crease `fold_through` (lines 12–13) is the line through the two points, built with
  [mk_line](#/node/mk_line) from the familiar two-point formula. Plugging in either point gives zero
  (lines 15–21).
- **Uniqueness:** if another fold *g* passes through both points, subtracting its two equations shows *g*'s normal
  is proportional to the explicit one (line 30); `exists_scale` gives the factor and
  [eq_mk_line](#/node/mk_line) concludes *g* is the same Line (lines 31–32).

### Sharpness

Without *p*₁ ≠ *p*₂ the claim is false: `huzita_1_not_unique_of_eq` ({SH} lines 104–112) shows both coordinate axes
pass through the origin, so "exactly one" fails when the two points coincide.
""",
 [q("What does the theorem need about the two points?",
    ["They are different", "They lie on the paper", "They have rational coordinates", "Nothing"], 0,
    f"The hypothesis p₁ ≠ p₂ ({H} line 23); {SH} lines 104–112 show it is needed."),
  q("What does 'exactly one' mean here, given that a line has many equations?",
    ["Exactly one canonical Line value, i.e. exactly one geometric line",
     "Exactly one equation up to sign", "Exactly one pair (a, b)"], 0,
    "Lines are stored in canonical form, so equality of Line values is equality of geometric lines."),
  q("Is Huzita's first axiom assumed in this library?",
    ["No, it is proved as a theorem about the coordinate model", "Yes, as a Lean axiom",
     "It is left as sorry"], 0,
    f"{H} lines 23–32 contain a full proof."),
 ],
 caveats=[NB])


node("huzita_2",
 "Headline: Axiom 2, exactly one fold placing one point onto another",
 "For two different points there is exactly one fold that sends the first onto the second: the perpendicular "
 "bisector of the segment between them.",
 rf"""## Plain English

**Theorem (`huzita_2`, {H} lines 52–72).** If *p*₁ ≠ *p*₂, there is exactly one [Fold](#/node/Fold) whose
[reflection](#/node/f_places_p) sends *p*₁ to *p*₂.

This is the second Huzita–Hatori axiom, and the one the Haga construction uses
([haga_first_theorem](#/node/haga_first_theorem)).

The fold is the **perpendicular bisector** of the segment *p*₁*p*₂, built explicitly as `fold_bisector`
(lines 34–36): its normal is *p*₂ − *p*₁, and it passes through the midpoint. A companion lemma confirms the
textbook description: a point is on this crease exactly when it is equally far from *p*₁ and *p*₂
(`fold_bisector_through`, lines 44–50).

### Things to notice

- The hypothesis *p*₁ ≠ *p*₂ is needed for uniqueness: if the points are equal, every crease through the point
  "sends it onto itself". `huzita_2_not_unique_of_eq` ({SH} lines 32–39) proves this with the two coordinate axes.
- The statement is about the crease only. It does not say which side of the paper moves.
""",
 [q("Which line is the unique fold sending p₁ onto p₂?",
    ["The perpendicular bisector of the segment p₁p₂", "The line through p₁ and p₂",
     "Any line through the midpoint"], 0,
    f"fold_bisector, {H} lines 34–36; fold_bisector_through, lines 44–50."),
  q("What goes wrong if p₁ = p₂?",
    ["Every crease through the point works, so the fold is not unique", "No fold exists", "Nothing"], 0,
    f"{SH} lines 32–39."),
  q("What exactly does the theorem assert?",
    ["Existence and uniqueness of the fold", "Only existence", "Only uniqueness"], 0,
    f"It is an exists-unique statement ({H} line 53)."),
 ],
 caveats=[NB, PLANE],
 widgets=walk(f"How the proof goes ({H}, lines 52-72)", [
  {"text": "Witness: the explicit perpendicular bisector fold_bisector (lines 34–36, used at line 55).", "link": "mk_line"},
  {"text": "It does send p₁ to p₂: fold_bisector_places (lines 38–42) expands the reflection formula and clears denominators."},
  {"text": "Uniqueness: take any fold g sending p₁ to p₂ and compare coordinates (lines 56–61).", "link": "f_places_p"},
  {"text": "The displacement p₂ − p₁ is a multiple of g's normal, so g's normal is proportional to p₂ − p₁ (lines 62–68)."},
  {"text": "The midpoint of p₁p₂ lies on g (lines 69–70)."},
  {"text": "So g's coefficients are a nonzero multiple of fold_bisector's, and eq_mk_line gives equality (lines 71–72).", "link": "mk_line"},
 ]))


node("huzita_3",
 "Axiom 3: a fold placing one line onto another",
 "For any two lines there is a fold placing the first onto the second (an angle bisector). Only existence is "
 "claimed, and the project proves uniqueness fails.",
 rf"""## Plain English

**Theorem (`huzita_3`, {H} lines 168–169).** For any lines *l*₁ and *l*₂ there is a fold whose
[line reflection](#/node/f_places_l) sends *l*₁ to *l*₂.

The witness `fold_bisect_lines` (lines 154–160) is an **angle bisector**: its coefficients are the two lines'
coefficients, each weighted by the length of the *other* line's normal (using square roots). The lemma
`bisector_places_line` (lines 74–106) checks by direct algebra that it does the job, and `inner_add_norms_pos`
(lines 134–152) shows the bisector's equation is never degenerate, even for parallel lines (where it gives the
midline) or equal lines.

### Sharpness ({SH})

- Uniqueness fails in general: `huzita_3_not_unique` (lines 41–47) shows both axes send the x-axis to itself.
- Even for crossing lines there are two folds: `huzita_3_two_bisectors` (lines 55–65) exhibits the two diagonals
  *y* = *x* and *y* = −*x*, each sending the x-axis onto the y-axis.
""",
 [q("Does huzita_3 claim the fold is unique?",
    ["No, only that one exists; the project proves uniqueness fails", "Yes", "Only for parallel lines"], 0,
    f"{H} line 168 is a plain existence statement; {SH} lines 41–65 show non-uniqueness."),
  q("Does the theorem need the two lines to cross?",
    ["No, it holds for any two lines", "Yes", "Only if they are perpendicular"], 0,
    f"There are no hypotheses ({H} line 168); parallel lines get the midline."),
 ],
 caveats=[NB])


node("huzita_4",
 "Axiom 4: exactly one fold through a point, perpendicular to a line",
 "Through any point there is exactly one crease perpendicular to a given line. No hypotheses needed.",
 rf"""## Plain English

**Theorem (`huzita_4`, {H} lines 183–193).** For any point *p* and line *l*, there is exactly one fold that is
[perpendicular](#/node/perpendicular) to *l* and [passes through](#/node/f_through_p) *p*.

The witness `fold_perp` (lines 171–172) has normal (−*b*, *a*), i.e. it runs along *l*'s normal direction, shifted to
pass through *p*. Uniqueness: perpendicularity forces any other such fold's normal to be proportional to (−*b*, *a*)
(lines 191–192), and passing through *p* pins the constant term (line 193).
""",
 [q("Does Axiom 4 need any hypothesis on p and l?",
    ["No: it holds even when p is on l", "p must not be on l", "l must not pass through the origin"], 0,
    f"{H} lines 183–184 have no hypotheses."),
 ],
 caveats=[NB])


node("huzita_5",
 "Axiom 5: a fold through one point placing another onto a line",
 "If a line is close enough to a point p₂ (no farther than p₁ is), some crease through p₂ folds p₁ onto the line.",
 rf"""## Plain English

**Theorem (`huzita_5`, {H} lines 214–233).** Given points *p*₁, *p*₂ and a line *l*₁, suppose the
[squared distance from p₂ to l₁](#/node/dist2_line) is at most the [squared distance](#/node/dist2) from *p*₁ to
*p*₂. Then there is a fold that passes through *p*₂ and sends *p*₁ onto *l*₁.

Picture it: folding along a crease through *p*₂ swings *p*₁ around a circle centred at *p*₂. That circle meets
*l*₁ exactly when *l*₁ is close enough to *p*₂, which is the hypothesis. The converse is proved separately in
[huzita_5_iff](#/node/huzita_5_iff).

### How the proof goes

1. Find a point *q* on *l*₁ at the right distance from *p*₂ (`exists_on_line_dist2`, lines 195–212). It is given by
   an explicit formula using a square root; the hypothesis guarantees the square root is of a nonnegative number.
2. If *p*₁ ≠ *q*, fold along the perpendicular bisector of *p*₁*q*: it sends *p*₁ to *q* (on *l*₁) and passes through
   *p*₂ because *p*₂ is equally far from both (lines 229–233).
3. If *p*₁ = *q*, then *p*₁ is already on *l*₁, and any crease through *p*₁ and *p*₂ works, because folding fixes points
   on the crease (lines 217–228, using [f_places_p_eq_self_iff](#/node/f_places_p_eq_self_iff)).
""",
 [q("Folding along creases through p₂ moves p₁ along…",
    ["the circle centred at p₂ through p₁", "the line through p₁ and p₂", "the line l₁"], 0,
    "Reflections in lines through p₂ preserve the distance to p₂."),
  q("What is the role of the distance hypothesis?",
    ["It ensures that circle meets l₁", "It ensures p₁ is on l₁", "It ensures the fold is unique"], 0,
    f"It makes the square root in exists_on_line_dist2 well-defined ({H} lines 195–201)."),
  q("Does huzita_5 claim the fold is unique?",
    ["No, existence only (there can be two)", "Yes"], 0,
    f"{H} line 215 is an existence statement."),
 ],
 caveats=[NB, PLANE])


node("huzita_5_iff",
 "Headline: Axiom 5, with its exact condition",
 "A crease through p₂ can fold p₁ onto line l₁ if and only if l₁ is no farther from p₂ than p₁ is. The condition is "
 "both sufficient and necessary.",
 rf"""## Plain English

**Theorem (`huzita_5_iff`, {SH} lines 5–16).** For points *p*₁, *p*₂ and a line *l*₁, the following are equivalent:

- there is a fold that [passes through](#/node/f_through_p) *p*₂ and [sends](#/node/f_places_p) *p*₁ onto
  [l₁](#/node/on_line);
- the [squared distance from p₂ to l₁](#/node/dist2_line) is at most the [squared distance](#/node/dist2) between *p*₁
  and *p*₂.

The right-to-left direction is [huzita_5](#/node/huzita_5). The new content is the left-to-right direction: the
distance condition is exactly right, not merely sufficient. This is the "sharpness" theme of the file: for axioms 5
and 7 the project pins down precisely when the fold exists.

Using squared distances avoids square roots: the condition is the same as "distance from *p*₂ to *l*₁ ≤ |*p*₁*p*₂|".
""",
 [q("What does the left-to-right direction say?",
    ["If such a fold exists, then l₁ is within distance |p₁p₂| of p₂",
     "If l₁ is close to p₂, the fold exists", "The fold is unique"], 0,
    f"{SH} lines 9–16."),
  q("If l₁ is farther from p₂ than p₁ is, what does the theorem tell us?",
    ["No crease through p₂ folds p₁ onto l₁", "Exactly one such crease exists", "Nothing"], 0,
    "That is the contrapositive of the left-to-right direction."),
  q("Why is the condition stated with squared distances?",
    ["To avoid square roots; it is equivalent to comparing ordinary distances",
     "Because the Lean statement is weaker than the classical one",
     "Because distances are rational"], 0,
    "dist2 and dist2_line are squares of the usual distances, and both sides are nonnegative."),
 ],
 caveats=[NB, PLANE],
 widgets=walk(f"How the proof goes ({SH}, lines 5-16)", [
  {"text": "Right to left: this is huzita_5 (line 8).", "link": "huzita_5"},
  {"text": "Left to right: take the fold f; it passes through p₂, so it fixes p₂ (line 10).", "link": "f_places_p_eq_self_iff"},
  {"text": "Folds preserve distances, so the image of p₁ is as far from p₂ as p₁ is (lines 11–13).", "link": "dist2"},
  {"text": "The image of p₁ is on l₁, and the distance from p₂ to l₁ is at most the distance to any point of l₁ (line 14).", "link": "dist2_line"},
  {"text": "Chain the two facts and swap the order of p₁, p₂ (lines 15–16)."},
 ]))


node("exists_hom_cubic_root",
 "Lemma: every real cubic has a root (the origami-beyond-compass step)",
 "Every homogeneous cubic in two real variables has a nonzero solution. This is where Huzita's sixth axiom gets its "
 "extra power: the crease direction is a root of a cubic.",
 rf"""## Plain English

**Theorem (`exists_hom_cubic_root`, {CR} lines 43–48).** For any real *A*, *B*, *C*, *E* there are *a*, *b*, not both
zero, with *A·a*³ + *B·a*²*b* + *C·ab*² + *E·b*³ = 0.

### How the proof goes

- If *A* = 0, take (*a*, *b*) = (1, 0) (line 46).
- Otherwise set *b* = 1 and solve the one-variable cubic *A·t*³ + *B·t*² + *C·t* + *E* = 0 (lines 47–48), using
  `exists_cubic_root` (lines 36–41).
- `exists_cubic_root` reduces to a positive leading coefficient and then applies the **intermediate value
  theorem** (lines 5–34): for a large enough *M*, built from the coefficients (line 7), the cubic is positive at *M*
  and negative at −*M*, so it vanishes in between.

### Why it matters

A compass-and-straightedge construction only ever solves equations of degree 2. The sixth Huzita axiom can solve
cubics (that is how origami trisects angles and doubles cubes). In this library, that power shows up exactly here:
[huzita_6_aux](#/node/huzita_6_aux) finds the crease direction as a root of a cubic. The proof is purely existential:
it does not give a formula for the root.
""",
 [q("Which Mathlib result does the cubic-root proof rest on?",
    ["The intermediate value theorem", "The fundamental theorem of algebra", "Cardano's formula"], 0,
    f"intermediate_value_Icc, {CR} line 33."),
  q("Is the root given by an explicit formula?",
    ["No, its existence is proved by a sign change", "Yes, by Cardano's formula", "Yes, by Newton's method"], 0,
    f"{CR} lines 20–34."),
 ],
 caveats=[NB])


node("huzita_6_aux",
 "Lemma: Axiom 6 when p₁ is not already on l₁",
 "The main case of Axiom 6: when p₁ is off l₁, the crease's normal direction is a root of a homogeneous cubic, and "
 "its offset is then forced by the requirement that p₁ land on l₁.",
 rf"""## Plain English

**Theorem (`huzita_6_aux`, {H} lines 246–282).** If *l*₁ and *l*₂ are not [parallel](#/node/parallel) and *p*₁ is not
on *l*₁, there is a fold sending *p*₁ onto *l*₁ and *p*₂ onto *l*₂.

### How the proof goes

1. Write the unknown crease as *a·x* + *b·y* + *c* = 0. The two conditions are two equations in *a*, *b*, *c*
   (via `on_line_f_places_p`). Eliminating *c* leaves one equation in (*a*, *b*) that is homogeneous of degree 3.
2. `exists_fold_normal` (lines 235–244) solves that cubic with [exists_hom_cubic_root](#/node/exists_hom_cubic_root),
   giving a direction (*a*, *b*) (lines 250–252).
3. Check that the crease direction is not perpendicular-degenerate, i.e. *l*₁.*a·a* + *l*₁.*b·b* ≠ 0
   (lines 254–265). If it were zero, the cubic would force the same for *l*₂, and then *l*₁ and *l*₂ would be parallel,
   contradicting the hypothesis. This step is where "*p*₁ not on *l*₁" is used.
4. Choose *c* so that *p*₁ lands on *l*₁; this is a linear equation in *c*, solvable by step 3 (lines 266–277).
5. The cubic equation then says exactly that *p*₂ lands on *l*₂ (lines 278–281).
""",
 [q("Where does the cubic come from?",
    ["Eliminating the crease's offset c from the two landing conditions", "From the paper's corners",
     "From Cardano's formula"], 0,
    f"{H} lines 235–252."),
  q("What is the hypothesis 'p₁ not on l₁' used for?",
    ["To rule out a degenerate direction so that c can be solved for", "To make the fold unique",
     "To make the lines parallel"], 0,
    f"{H} lines 254–265."),
 ],
 caveats=[NB])


node("huzita_6",
 "Headline: Axiom 6, a fold placing two points onto two lines (solves cubics)",
 "If two lines cross, there is always a fold that simultaneously places p₁ onto the first and p₂ onto the second. "
 "Finding it amounts to solving a cubic, which is why origami can do more than compass and straightedge.",
 rf"""## Plain English

**Theorem (`huzita_6`, {H} lines 284–305).** For any points *p*₁, *p*₂ and lines *l*₁, *l*₂ that are not
[parallel](#/node/parallel) (i.e. they cross in one point), there is a [fold](#/node/Fold) whose
[reflection](#/node/f_places_p) sends *p*₁ [onto](#/node/on_line) *l*₁ and *p*₂ onto *l*₂.

This is the famous sixth Huzita–Hatori axiom (also called the Beloch fold). Its crease is tangent to two parabolas
at once and is found by solving a cubic equation; that is how paper folding trisects angles and doubles the cube.

### Faithfulness

- **Existence only.** There can be up to three such folds; the theorem claims at least one.
- **Sufficient, not necessary.** "Not parallel" is a convenient sufficient condition. For parallel lines the fold can
  still exist (for example, when *p*₁ is already on *l*₁ and *p*₂ on *l*₂, a crease through both points works), and
  those cases are not covered. `huzita_6_needs_not_parallel` ({SH} lines 133–140) shows only that *some* restriction is needed: for
  the points (0, 1), (0, 2) and the parallel lines *y* = 0, *y* = −2, no fold works.
- {PLANE}
""",
 [q("What does the theorem need about l₁ and l₂?",
    ["They are not parallel (they cross)", "They are perpendicular", "Nothing"], 0,
    f"{H} line 284."),
  q("Does the theorem say the fold is unique?",
    ["No, it is an existence statement; there can be several such folds", "Yes"], 0,
    f"{H} line 285."),
  q("Does the project prove that parallel lines never allow such a fold?",
    ["No; it gives one parallel example where no fold exists, which shows a hypothesis is needed",
     "Yes, it proves an if-and-only-if", "It says nothing about parallel lines"], 0,
    f"{SH} lines 133–140 is a single counterexample."),
  q("Which extra mathematical ingredient makes this axiom stronger than compass and straightedge?",
    ["Solving a cubic equation", "Using rational coordinates", "Using perpendicular bisectors"], 0,
    "See exists_hom_cubic_root and huzita_6_aux."),
 ],
 caveats=[NB, "The condition 'not parallel' is sufficient but not necessary; the parallel-but-possible cases are not "
          "covered by this theorem."],
 widgets=walk(f"How the proof goes ({H}, lines 284-305)", [
  {"text": "Case p₁ is not on l₁: use the main lemma huzita_6_aux (lines 286–287).", "link": "huzita_6_aux"},
  {"text": "Case p₁ is on l₁ but p₂ is not on l₂: apply the same lemma with the roles of the two pairs swapped, and swap the results back (lines 288–291).", "link": "huzita_6_aux"},
  {"text": "Case both points already lie on their lines: any crease through both points fixes them (lines 292–305).", "link": "f_places_p_eq_self_iff"},
  {"text": "Sub-case p₁ = p₂: use the crease through p₁ perpendicular to l₁ (lines 293–298).", "link": "huzita_4"},
  {"text": "Sub-case p₁ ≠ p₂: use the crease through both points (lines 299–305).", "link": "huzita_1"},
 ]))


node("huzita_6_needs_not_parallel",
 "Sharpness: Axiom 6 can fail for parallel lines",
 "A concrete example shows the hypothesis of Axiom 6 cannot simply be dropped: points (0,1), (0,2) and the parallel "
 "lines y = 0 and y = −2 admit no such fold.",
 rf"""## Plain English

**Theorem (`huzita_6_needs_not_parallel`, {SH} lines 133–140).** It is not true that for all points *p*₁, *p*₂ and all
lines *l*₁, *l*₂ there is a fold placing *p*₁ onto *l*₁ and *p*₂ onto *l*₂.

The counterexample takes *p*₁ = (0, 1), *p*₂ = (0, 2), *l*₁ the x-axis and *l*₂ the line *y* = −2 (line 137). The two
landing conditions turn into polynomial equations in the crease coefficients that `nlinarith` shows are
incompatible (lines 138–140). The intuition: a fold preserves distances, the two points are 1 apart, but any point of
*y* = 0 is at least 2 away from any point of *y* = −2.

This shows a hypothesis is needed, not that "not parallel" is the right one; see [huzita_6](#/node/huzita_6).
""",
 [q("What does this theorem show?",
    ["That Axiom 6 can fail without some hypothesis", "That parallel lines never allow an Axiom-6 fold",
     "That Axiom 6 folds are unique"], 0,
    f"It refutes the unrestricted statement with one example ({SH} lines 133–140)."),
 ],
 caveats=[NB])


node("huzita_7",
 "Axiom 7: exactly one fold placing a point onto a line, perpendicular to another",
 "If two lines cross, exactly one crease perpendicular to the second line folds a given point onto the first.",
 rf"""## Plain English

**Theorem (`huzita_7`, {H} lines 336–360).** If *l*₁ and *l*₂ are not [parallel](#/node/parallel), then for any point
*p* there is exactly one fold that sends *p* [onto](#/node/on_line) *l*₁ and is
[perpendicular](#/node/perpendicular) to *l*₂.

The witness `fold_perp_place` (lines 318–324) is an explicit formula. Being perpendicular to *l*₂ fixes the crease's
direction; requiring *p* to land on *l*₁ fixes its offset, and this is solvable because *l*₁ crosses *l*₂. Uniqueness
follows the usual pattern: show any other such fold has proportional coefficients and apply
[eq_mk_line](#/node/mk_line) (lines 343–360).

The exact condition, an if-and-only-if, is the headline [huzita_7_iff](#/node/huzita_7_iff).
""",
 [q("Which part of the fold does 'perpendicular to l₂' determine?",
    ["Its direction", "Its offset", "Nothing"], 0,
    "Perpendicular folds all have normal proportional to (−l₂.b, l₂.a)."),
 ],
 caveats=[NB])


node("huzita_7_iff",
 "Headline: Axiom 7, with its exact condition",
 "There is exactly one crease perpendicular to l₂ that folds p onto l₁ if and only if l₁ and l₂ are not parallel. "
 "For parallel lines there is either no such fold or infinitely many.",
 rf"""## Plain English

**Theorem (`huzita_7_iff`, {SH} lines 97–102).** For any point *p* and lines *l*₁, *l*₂: there is **exactly one** fold
that sends *p* onto *l*₁ and is perpendicular to *l*₂ if and only if *l*₁ and *l*₂ are not
[parallel](#/node/parallel).

The right-to-left direction is [huzita_7](#/node/huzita_7). The left-to-right direction analyses parallel lines:

- if *p* is not on *l*₁, **no** fold works (`huzita_7_parallel_none`, lines 67–75): a crease perpendicular to *l*₂ is
  also perpendicular to *l*₁, and reflecting in it maps *l*₁ to itself and points off *l*₁ to points off *l*₁;
- if *p* is on *l*₁, **every** crease perpendicular to *l*₂ works, so there are infinitely many
  (`huzita_7_parallel_on_not_unique`, lines 77–95).

Either way "exactly one" fails. Remember that a line counts as parallel to itself, so *l*₁ = *l*₂ falls in this case.
""",
 [q("For parallel l₁, l₂ and p not on l₁, how many such folds are there?",
    ["None", "Exactly one", "Two", "Infinitely many"], 0,
    f"huzita_7_parallel_none, {SH} lines 67–75."),
  q("For parallel l₁, l₂ and p on l₁, how many such folds are there?",
    ["Infinitely many", "None", "Exactly one"], 0,
    f"huzita_7_parallel_on_not_unique, {SH} lines 77–95."),
  q("What exactly is characterised by 'not parallel'?",
    ["The existence of exactly one such fold", "The existence of at least one such fold",
     "The existence of two such folds"], 0,
    f"The left side of the iff is an exists-unique statement ({SH} line 98)."),
 ],
 caveats=[NB],
 widgets=walk(f"How the proof goes ({SH}, lines 97-102)", [
  {"text": "Right to left: not parallel gives exactly one fold by huzita_7 (line 99).", "link": "huzita_7"},
  {"text": "Left to right: assume exactly one fold and that the lines are parallel; derive a contradiction (line 99)."},
  {"text": "If p is on l₁, there are infinitely many folds (one for each offset c), contradicting uniqueness (lines 100–101, using lines 77–95).", "link": "mk_line"},
  {"text": "If p is not on l₁, there is no fold at all, contradicting existence (line 102, using lines 67–75).", "link": "perpendicular"},
 ]))


# ---------- extra quiz questions (every node gets at least three) ----------
EXTRA = {
 "huzita_3": [
  q("Which two folds send the x-axis onto the y-axis?",
    ["The diagonals y = x and y = −x", "The two axes", "Only y = x"], 0,
    f"huzita_3_two_bisectors, {SH} lines 49–65."),
 ],
 "huzita_4": [
  q("What direction does the Axiom 4 crease have?",
    ["It crosses l at a right angle (its normal is (−b, a))", "Parallel to l", "Always horizontal"], 0,
    f"fold_perp, {H} lines 171–172."),
  q("Is the Axiom 4 fold unique?",
    ["Yes, exactly one", "No, there are two", "Only if p is on l"], 0,
    f"It is an exists-unique statement ({H} line 184)."),
 ],
 "exists_hom_cubic_root": [
  q("In the case A = 0, which solution does the proof use?",
    ["(a, b) = (1, 0)", "(a, b) = (0, 1)", "(a, b) = (0, 0)"], 0,
    f"{CR} line 46; (0, 0) is excluded by the 'not both zero' requirement."),
 ],
 "huzita_6_aux": [
  q("Which lemma supplies the crease direction?",
    ["exists_fold_normal, via exists_hom_cubic_root", "huzita_2", "fold_through"], 0,
    f"{H} lines 239–244 and 250–252."),
 ],
 "huzita_6_needs_not_parallel": [
  q("Why can't any fold work in the example?",
    ["Folds preserve distance: the points are 1 apart, but the lines are 2 apart", "The points are on the lines",
     "The lines cross"], 0,
    f"The concrete data are at {SH} line 137."),
  q("Does this prove that not-parallel is necessary for Axiom 6?",
    ["No, only that some hypothesis is needed", "Yes"], 0,
    "It refutes only the fully universal statement."),
 ],
 "huzita_7": [
  q("Does huzita_7 need the lines to be non-parallel?",
    ["Yes", "No"], 0,
    f"{H} line 336."),
  q("Is the Axiom 7 fold unique?",
    ["Yes, when the lines are not parallel", "No, there are always two", "Only when p is on l₁"], 0,
    f"It is an exists-unique statement ({H} line 337)."),
 ],
}
for n_ in NODES:
    n_["quiz"] = n_["quiz"] + EXTRA.get(n_["id"], [])
