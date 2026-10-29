import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_common.py"), encoding="utf-8").read())


node("Rudin_exercise_4_8a",
 "The one problem whose textbook source was wrong (and is now a duplicate)",
 "ProofNet's informal text for this Rudin problem asked for something impossible: a uniformly continuous function that is unbounded on a bounded set. The correction rewrote both the text and the Lean to Rudin's actual claim, so problem 168 now states the same theorem as problem 351.",
 r"""## Plain English

**Theorem (`Rudin_exercise_4_8a`, [[L 168 14-17]]).** Let E be a bounded set of real numbers. Then every
function f : ℝ → ℝ that is uniformly continuous on E is bounded on E (its image f(E) is a bounded set).

### What went wrong in the original

This is the only problem the audit labels **NL source incorrect**: the *informal* statement itself was wrong. The
original ProofNet text ([[O 168 7-10]]) read: let E be a bounded set; prove there is a uniformly continuous
function that is not bounded on E. That can't be done. Uniform continuity on a bounded subset of ℝ forces a
bounded image, which is the theorem above. The original Lean ([[O 168 12-15]]) followed that text (and even
dropped the boundedness of E). The audit ([[T 168]]) records it as false: with E empty, no function is
unbounded on E. ProofNet# had the same text ([[S 168]]).

Rudin's exercise 4.8 has two parts: (a) prove the theorem above; (b) show that the conclusion fails if E is not
bounded. ProofNet's text looks like a garbled version of (b). The correction replaced both the comment (line 10)
and the theorem with part (a), and renamed it from `…_4_8b` to `…_4_8a`.

### A duplicate

Problem 351 ([[L 351 13-16]]) was already Rudin 4.8(a), faithful in the original. So after the correction the
benchmark contains **two problems with the same name and the same mathematical content**, written slightly
differently (one quantifies over f after the hypotheses, the other takes f as an argument). This site's
scanner lists the second one as `Rudin_exercise_4_8a'`. Anyone counting "367 distinct problems" may want to know
this. See the [review page](#/review).
""",
 [q("Why could the original informal statement never be proved?",
    ["On a bounded subset of ℝ, a uniformly continuous function is always bounded",
     "Uniformly continuous functions don't exist on bounded sets", "The statement was about complex numbers"], 0,
    "That is exactly the corrected theorem ([[L 168 14-17]])."),
  q("What does the corrected statement say?",
    ["If E is bounded, every function uniformly continuous on E has a bounded image f(E)",
     "There is an unbounded uniformly continuous function on every unbounded E",
     "Every continuous function on a bounded set is bounded"], 0,
    "Lines 15–16. Note 'uniformly': a merely continuous function such as 1/x on (0, 1) can be unbounded on a bounded set."),
  q("How does problem 168 relate to problem 351 after the correction?",
    ["They state the same theorem under the same name, Rudin_exercise_4_8a",
     "351 is the negation of 168", "They are unrelated"], 0,
    "Compare [[L 168 14-17]] with [[L 351 13-16]]."),
 ],
 caveats=[STATUS_SORRY,
          "That ProofNet's text was meant to be part (b) of Rudin's exercise is this site's guess from the wording; the repository only says the informal source was wrong.",
          "The duplicate is an observation by this site, not something the README mentions."])


node("countably_compact",
 "Helper definitions inside problem files",
 "A few problems need a notion Mathlib lacks or names differently, so the file defines it just above the theorem. These are part of the statement: a solver must reason about them exactly as defined. Here: countably compact means every countable open cover has a finite subcover.",
 r"""## Plain English

Most problem files contain only the theorem. **19 files** also define helpers in the area between the
imports and the informal-statement comment, which the dataset calls the `helper` field. Because each file
stands alone, the same helper is sometimes repeated in several files.

**Definition (`countably_compact`, [[L 125 6-9]]).** A topological space X is *countably compact* if every
countable open cover has a finite subcover: whenever open sets U₀, U₁, U₂, … cover X, finitely many of them
already cover X. It is used by the [Munkres problem 28.5](#/node/Munkres_exercise_28_5). The same definition is
repeated in problem 308.

### The other helpers

| Helper | Meaning | Files |
|---|---|---|
| `is_topology` (and `is_topology_c`) | a family of subsets contains the whole set and is closed under unions and finite intersections | 106, 107, 108, 290, 291, 292 |
| `I` | the unit interval [0, 1] as a set of reals; see [I](#/node/I) | 115, 133, 299, 305, 310 |
| `lower_limit_topology`, `Rl`, `K_c`, `K_topology_c` | the lower-limit topology on ℝ and the K-topology, from Munkres §13 | 109, 110 |
| `limit_point_compact_strong` | a variant of limit-point compactness | 308 |
| `rational` | x is in the image of ℚ in ℝ | 295 |
| `f`, `g` | the specific sequences in Rudin 3.3 and 3.6 | 159, 160 |
| `Subgroup.relindex` | a one-line alias for Mathlib's `Subgroup.relIndex` (relative index), so the statement keeps its older spelling | 42 |

A helper is part of the problem: if it is defined wrongly, the theorem is about the wrong thing. The audit
compares helpers along with statements. For example its record for problem 42 ([[T 42]]) checks that the
alias means the relative index |K : H|.
""",
 [q("Why do some problem files define their own notions?",
    ["Mathlib lacks the notion, or names it differently, and each file must stand alone",
     "To hide the answer", "Because Mathlib cannot be imported"], 0,
    "Each file imports Mathlib (line 1) and adds only what the statement needs."),
  q("What does countably_compact X say?",
    ["Every cover of X by countably many open sets has a finite subcover",
     "X is countable and compact", "Every sequence in X converges"], 0,
    "[[L 125 6-9]]: for every sequence of open sets covering X there is a finite set of indices that already covers it."),
  q("Does a solver get to change a helper definition?",
    ["No: the helper is part of the statement, which is fixed", "Yes, helpers are hints", "Only in Munkres problems"], 0,
    "The theorem's meaning depends on the helper; changing it would change the problem."),
 ],
 caveats=["The table summarises helpers by reading their one-line definitions; only countably_compact is explained in detail here.",
          "This site's source scanner gives repeated helpers primed names (is_topology', I'' and so on) because several files define the same name. In the benchmark each file is separate, so there is no clash."])


node("I",
 "I: the unit interval [0, 1] (and a scanner mix-up)",
 "Five Munkres-style problem files define I as the closed interval [0, 1]. Separately, the I in the polarization headline is Lean's complex number i; this site's text scanner confused the two, so the dependency link between them is spurious.",
 r"""## Plain English

**Definition (`I`, [[L 115 6-6]]).** `I` is the set of real numbers x with 0 ≤ x ≤ 1, the closed unit interval
(Mathlib's `Icc 0 1`). Problem 115 uses it for functions on [0, 1], for example the sequence fₙ(x) = xⁿ. The same
one-line definition is repeated in problems 133, 299, 305 and 310 (listed here as `I'`, `I''` …).

### A false link on this site

This site finds dependencies by scanning the source text for names, without running Lean. In the
[polarization identity](#/node/Axler_exercise_6_7) the letter `I` means the **complex number i**: that file opens
the namespace `Complex`, so `I` there is Mathlib's `Complex.I`. The scanner doesn't know this and links it to
this unit interval instead. Ignore that link: the polarization problem has nothing to do with [0, 1]. The
[trust page](#/trust) lists this artefact.
""",
 [q("What is I in problem 115?",
    ["The closed interval [0, 1] of real numbers", "The complex number i", "The identity map"], 0,
    "[[L 115 6-6]]: abbrev I : Set ℝ := Icc 0 1."),
  q("What is I in the polarization identity (problem 23)?",
    ["The complex number i (Complex.I), because the file opens Complex", "The unit interval", "An index set"], 0,
    "proofnet-23 opens Complex on line 3; the link to this node is a scanner artefact."),
  q("Why does this site show a dependency from the polarization identity to the unit interval?",
    ["The text scanner matched the name I without knowing which namespace was open",
     "The polarization identity is about [0, 1]", "Lean reported it"], 0,
    "Declarations and dependencies on this site come from reading text, not from a Lean build."),
 ],
 caveats=["The dependency from Axler_exercise_6_7 to I shown on this site is a scanner artefact, not a real dependency."])
