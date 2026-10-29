NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

# ------------------------------------------------------------ abstract layer
node("Prismriver.Torsor",
 "Torsor: intervals acting on pitches",
 "The project's own axioms for 'a group of intervals acting on a space of pitches': every result that is stated for a general scale uses only these laws.",
 r"""## Plain English

**Class (`Torsor P I`, Prismriver/Repr/Scale.lean lines 18–40).** `P` is a type of pitches, `I` a type of
intervals. The class asks for `+`, `−`, negation and integer multiples on intervals, an action `i • p` (move `p` by
`i`) and a difference `q / p` (the interval from `p` to `q`), with laws:

- intervals form an abelian group with `zero` (lines 19–31), and integer multiplication distributes (lines 32–35);
- `zero • p = p` and `j • (i • p) = (i + j) • p` (lines 37–38);
- `(q / p) • p = q` and `(i • p) / p = i` (lines 39–40).

Mathematically that is an *affine space* / *torsor* over an abelian group, as the README says: pitches have no
zero, but differences of pitches are intervals. Note the notation: `/` means "difference" here, not division.

Two instances in the project: 12-tone (or n-tone) equal temperament where both are integers
([EqualTemp instance](#/node/Prismriver.EqualTemp.instance_97)), and classical spelled pitches
([Classical instance](#/node/Prismriver.Classical.instance_690)).
""",
 [q("What does `q / p` mean for a Torsor?", ["The interval from p up to q", "A frequency ratio", "Integer division"], 0,
    "smul_div says (q / p) • p = q (Prismriver/Repr/Scale.lean line 39)."),
  q("Is there a 'zero pitch' in the axioms?", ["No, only a zero interval", "Yes, `zero : P`"], 0, "`zero : I` (line 19)."),
  q("In `j • (i • p) = (i + j) • p`, which interval is applied first?", ["i", "j"], 0, "i acts on p first (line 38).")])

node("Prismriver.Scale",
 "Scale: a torsor with a fundamental interval and a list of pitches",
 "A Scale adds a name, a repeating 'fundamental' interval (usually the octave) and one period's worth of pitches to the Torsor laws; the README stresses that tunings and scales are deliberately the same kind of object.",
 r"""## Plain English

**Class (`Scale P I`, Prismriver/Repr/Scale.lean lines 44–48).** It extends [Torsor](#/node/Prismriver.Torsor)
and `PseudoScale` (just a name, lines 8–9) with:

- `fundamental : I`, the period, e.g. the octave;
- `pitches : List P`, the notes in one period, e.g. C D E F G A B for C major.

The theorems that use a `Scale` (such as [transposeAction_mul_smul](#/node/Prismriver.transposeAction_mul_smul)
and [pitchCong_equivalence](#/node/Prismriver.pitchCong_equivalence)) only use its Torsor part, and the
`fundamental` when given. No theorem says that `pitches` is sorted, has no repeats, or is closed under anything.

Examples: `EqualTemp.scale n` (n-tone equal temperament, with the small theorem `n_et_notes` that it has n notes,
lines 125–135), and `diatonic root modus`, `chromatic`, `japanese_in` in Prismriver/Repr/Classical.lean lines 788–891.
""",
 [q("What is `fundamental` usually?", ["The octave", "The tonic pitch", "A semitone"], 0, "Prismriver/Repr/Scale.lean line 46."),
  q("Do any theorems constrain the `pitches` list?", ["No (apart from n_et_notes counting the ET list)", "Yes, it must be sorted"], 0,
    "`pitches : List P` has no attached laws (line 48)."),
  q("Does Prismriver distinguish scales from tuning systems?", ["No, deliberately not", "Yes, strictly"], 0,
    "README and the doc comment on Tuning, Prismriver/Repr/Scale.lean lines 11–14.")])

node("Prismriver.pitchCong",
 "pitchCong: equal up to whole multiples of an interval",
 "p ≡ q (mod φ) means p is q moved by n·φ for some integer n; with φ the octave this is octave equivalence.",
 r"""## Plain English

**Definition (`pitchCong`, Prismriver/Repr/Scale.lean lines 52–53).** For a scale and an interval `φ`,
`pitchCong φ p q` holds when there is an integer `n` with `p = (n * φ) • q`.

[pitchCong_equivalence](#/node/Prismriver.pitchCong_equivalence) proves this is an equivalence relation, and
[pitchSetoid](#/node/Prismriver.pitchSetoid) packages it for the quotient `pitchClass`.
""",
 [q("Is C4 pitchCong to C2 with φ = octave?", ["Yes, n = 2", "No"], 0, "C4 = (2·octave) • C2."),
  q("Can n be negative?", ["Yes, n : Int", "No"], 0, "Line 53 quantifies over `n : Int`.")])

node("Prismriver.pitchSetoid",
 "pitchSetoid: the octave-equivalence setoid",
 "Packages pitchCong and its equivalence proof as a Lean Setoid, defaulting φ to the scale's fundamental, so pitch classes can be a quotient type.",
 r"""## Plain English

**Definition (`pitchSetoid`, Prismriver/Repr/Scale.lean lines 78–83)** bundles [pitchCong](#/node/Prismriver.pitchCong)
with [pitchCong_equivalence](#/node/Prismriver.pitchCong_equivalence). The next definition, `pitchClass`
(lines 85–87), is the quotient of pitches by it. Nothing else in the project currently uses `pitchClass`; the
dihedral file uses its own mod-12 map instead.
""",
 [q("What is φ by default?", ["scale.fundamental", "zero", "a semitone"], 0, "Prismriver/Repr/Scale.lean line 80."),
  q("What does the quotient `pitchClass` identify?", ["Pitches differing by whole multiples of φ", "Enharmonic spellings"], 0, "Lines 85–87.")])

node("Prismriver.TransposeAction",
 "TransposeAction: transposition or inversion, as data",
 "A TransposeAction is either 'shift every pitch by i' or 'mirror every pitch about a, then shift down by i'; these are the pitch-level versions of T_n and I_n.",
 r"""## Plain English

**Inductive (`TransposeAction`, Prismriver/Repr/Dihedral.lean lines 11–15).** Two constructors:

- `.r i`: p ↦ p + i ([rInterval](#/node/Prismriver.rInterval));
- `.sr a i`: p ↦ a − (p − a) − i ([srInterval](#/node/Prismriver.srInterval)): reflect p about the pitch a,
  then go down by i.

They act on pitches through the [SMul instance](#/node/Prismriver.instance_21) (lines 21–24), and compose
by [transposeAction_mul_smul](#/node/Prismriver.transposeAction_mul_smul). The names `r` and `sr` copy Mathlib's
names for rotations and reflections of a polygon.
""",
 [q("What does `.sr a 0` do to the pitch a itself?", ["Leaves it fixed", "Moves it up an octave"], 0,
    "a − (a − a) − 0 = a; the centre of a reflection is fixed."),
  q("Is TransposeAction specific to Western pitches?", ["No, it works over any Scale", "Yes"], 0, "The file is generic, `variable { P I } [Scale P I]` (line 9).")])

node("Prismriver.rInterval",
 "rInterval: shift a pitch by an interval",
 "rInterval i p is just i • p, transposition by i.",
 r"""## Plain English

**Definition (`rInterval`, Prismriver/Repr/Dihedral.lean line 17).** `rInterval i p = i • p`. Two shifts add
(`rInterval_rInterval`, lines 26–29).
""",
 [q("rInterval j (rInterval i p) equals", ["rInterval (i + j) p (up to commuting the sum)", "rInterval (i − j) p"], 0,
    "Lines 26–29 state rInterval i (rInterval j p) = rInterval (i + j) p.")])

node("Prismriver.srInterval",
 "srInterval: mirror a pitch about a centre",
 "srInterval i a p = (−(p / a) − i) • a: take the interval from a to p, flip its sign, subtract i, and apply it to a.",
 r"""## Plain English

**Definition (`srInterval`, Prismriver/Repr/Dihedral.lean line 19).** If p is a major third above a, then
`srInterval 0 a p` is a major third *below* a. A nonzero `i` then lowers the result by i.

Key facts: two inversions about the same centre cancel to a shift (`srInterval_srInterval`, lines 71–86), and an
inversion about b can be rewritten as an inversion about a with a corrected shift
([srInterval_change_center](#/node/Prismriver.srInterval_change_center), lines 93–125).
""",
 [q("With spelled pitches, srInterval 0 C4 E4 is", ["A♭3 (a major third below C4)", "G♯3", "E3"], 0,
    "−(major third) applied to C4 gives the spelled pitch a major third down, A♭3; the Torsor keeps spelling."),
  q("Is `p / a` the interval from a to p, or from p to a?", ["From a to p", "From p to a"], 0, "Torsor's smul_div: (p / a) • a = p.")])

node("Prismriver.instance_21",
 "How a TransposeAction acts on a pitch",
 "The SMul instance that turns the data .r i / .sr a i into the functions rInterval i / srInterval i a.",
 r"""## Plain English

**Instance (Prismriver/Repr/Dihedral.lean lines 21–24).** `t • p` is `rInterval i p` when `t = .r i` and
`srInterval i a p` when `t = .sr a i`. See [TransposeAction](#/node/Prismriver.TransposeAction).
""",
 [q("(.r i) • p equals", ["i • p", "−i • p"], 0, "Line 23 and rInterval (line 17).")])

node("Prismriver.instance_138",
 "The composition table for TransposeActions",
 "Multiplying TransposeActions is defined case by case so that it matches composing them as functions; that match is the theorem transposeAction_mul_smul.",
 r"""## Plain English

**Instance (`Mul TransposeAction`, Prismriver/Repr/Dihedral.lean lines 138–143).** See the table in
[transposeAction_mul_smul](#/node/Prismriver.transposeAction_mul_smul). This multiplication is only a definition;
no associativity or identity laws are proved for it.
""",
 [q("Is `.r zero` proved to be an identity for this multiplication?", ["No", "Yes"], 0, "Only the action compatibility is proved (lines 145–159).")])

node("Prismriver.srInterval_change_center",
 "Moving the centre of an inversion",
 "Inverting about b is the same as inverting about a with the shift increased by twice the interval from b to a; this is what makes two inversions about different centres compose to a transposition.",
 r"""## Plain English

**Theorem (`srInterval_change_center`, Prismriver/Repr/Dihedral.lean lines 93–125).** For any interval j and
pitches a, b, p: `srInterval j b p = srInterval ((a/b) + (a/b) + j) a p`. Geometrically, a mirror at b equals a
mirror at a followed by a shift of 2·(a − b). The proof is a long chain of Torsor rewrites.

It feeds `srInterval_srInterval_general` (lines 127–136), the sr·sr case of
[transposeAction_mul_smul](#/node/Prismriver.transposeAction_mul_smul).
""",
 [q("Mirror at b vs mirror at a differ by", ["a shift of twice the interval from b to a", "nothing", "an octave"], 0, "Prismriver/Repr/Dihedral.lean line 95.")])

node("Prismriver.srInterval_srInterval_general",
 "Two inversions make a transposition",
 "Inverting about b (shift j) and then about a (shift i) is a single shift by 2·(a/b) + (j − i).",
 r"""## Plain English

**Theorem (`srInterval_srInterval_general`, Prismriver/Repr/Dihedral.lean lines 127–136).** Proved by moving the
first centre with [srInterval_change_center](#/node/Prismriver.srInterval_change_center), then cancelling two
mirrors about the same point (`srInterval_srInterval`, lines 71–86).
""",
 [q("If a = b, two inversions with shifts j then i give", ["the shift j − i", "the shift 2j", "an inversion"], 0,
    "a / a is the zero interval, so only j − i is left.")])

# ------------------------------------------------------------ classical layer
node("Prismriver.Classical.Accidental",
 "Accidental: sharps and flats as an integer",
 "An accidental is just a whole number of semitones away from natural: ♯ is 1, ♭ is −1, double sharp is 2.",
 r"""## Plain English

**Structure (`Accidental`, Prismriver/Repr/Classical.lean lines 8–10)** holds one integer `semitones`
(default 0). `natural`, `sharp`, `flat` are 0, 1, −1 (lines 33–35); `+`, `−` and integer multiples act on the
integer (lines 41–48).
""",
 [q("What is a double flat?", ["semitones = −2", "semitones = 2", "Not representable"], 0, "Any integer is allowed (line 9).")])

node("Prismriver.Classical.Pitch",
 "Pitch: a spelled note (letter position + accidental)",
 "A pitch stores which letter it is on an infinite staff (C0 = 0, D0 = 1, …, C1 = 7) and its accidental, so C♯4 and D♭4 are different pitches.",
 r"""## Plain English

**Structure (`Pitch`, Prismriver/Repr/Classical.lean lines 143–146).** `name : Int` counts letter steps from C0,
seven per octave, and `acc` is an [Accidental](#/node/Prismriver.Classical.Accidental). `Pitch.new .g 4` is
G4 = 4 + 4·7 = 32 (lines 151–152); the letter and octave are recovered by mod/div 7 (lines 153–159).

The sound (semitones above C0) is not stored; it is computed by
[nameDistance](#/node/Prismriver.Classical.nameDistance) plus the accidental, e.g. by
[pitch_toZMod12](#/node/Prismriver.Theory.Dihedral.pitch_toZMod12).
""",
 [q("Are C♯4 and D♭4 equal as Pitch values?", ["No: different name, different acc", "Yes"], 0, "Equality is structural on (name, acc)."),
  q("What is `name` for E0?", ["2", "4", "3"], 0, "C=0, D=1, E=2 (letters, not semitones).")])

node("Prismriver.Classical.Interval",
 "Interval: letter steps and semitones",
 "An interval records both how many letters it spans and how many semitones, so a major third (2, 4) and a diminished fourth (3, 4) are different intervals even though they sound the same.",
 r"""## Plain English

**Structure (`Interval`, Prismriver/Repr/Classical.lean lines 340–343)** has `name : Int` (letter steps, 0 =
unison, 4 = fifth) and `semitones : Int`. Arithmetic is componentwise (lines 350–368). The named intervals are
at lines 440–454: `p5 = (4, 7)`, `ma3 = (2, 4)`, `octave = (7, 12)`, `aug4 = (3, 6)`, `dim5 = (4, 6)`, …

These are the classical "interval names". The abelian group laws are proved at lines 370–438 and gathered in the
[Torsor instance](#/node/Prismriver.Classical.instance_690).
""",
 [q("What is the octave?", ["(7, 12)", "(8, 12)", "(12, 12)"], 0, "Prismriver/Repr/Classical.lean line 440."),
  q("Are aug4 and dim5 equal?", ["No: (3, 6) vs (4, 6)", "Yes"], 0, "Lines 447–448.")])

node("Prismriver.Classical.nameDistance",
 "nameDistance: semitones between two natural notes",
 "nameDistance n2 n1 counts the semitones from the natural note at letter n1 up to the one at n2, using the pattern 2 2 1 2 2 2 1 (negative if n2 is lower).",
 r"""## Plain English

**Definition (`nameDistance`, Prismriver/Repr/Classical.lean lines 246–253).** Walk from letter `n1` to letter
`n2`, adding the step sizes in `spaces = [2, 2, 1, 2, 2, 2, 1]` (line 130, C→D→E→F→G→A→B→C); if `n2 < n1`, walk the
other way and negate. So nameDistance(E, C) = 4 and nameDistance(C, E) = −4.

Its three laws: `nameDistance_refl` (distance to itself is 0, lines 255–261), `nameDistance_swap` (swapping
negates, lines 263–276) and [nameDistance_image](#/node/Prismriver.Classical.nameDistance_image) (distances add).
""",
 [q("nameDistance of B0 above C0 (n2 = 6, n1 = 0)?", ["11", "12", "6"], 0, "2+2+1+2+2+2 = 11."),
  q("Which argument is the upper note?", ["The first, n2", "The second, n1"], 0, "The docstring says it computes n2 − n1 (line 245).")])

node("Prismriver.Classical.nameDistance_image",
 "nameDistance_image: letter distances add up",
 "Going from k to j and then from j to i covers the same number of semitones as going straight from k to i, in every order of i, j, k; this cocycle law is what makes interval addition well behaved.",
 r"""## Plain English

**Theorem (`nameDistance_image`, Prismriver/Repr/Classical.lean lines 281–336).**
`nameDistance i j + nameDistance j k = nameDistance i k` for all integers i, j, k.

The proof splits into the six possible orderings of i, j, k (each `split` on an `if` in
[nameDistance](#/node/Prismriver.Classical.nameDistance)) and uses `nameDistanceAux_image` (lines 214–234), which
says a walk of n + m letters is a walk of n followed by a walk of m starting where the first ended.
""",
 [q("Does it need i ≥ j ≥ k?", ["No, it holds for all orderings", "Yes"], 0, "The statement has no hypotheses (line 281)."),
  q("Why is the proof long?", ["nameDistance has a sign split, so there are six order cases", "It uses native_decide"], 0, "Lines 284–336.")])

node("Prismriver.Classical.pitch_interval_add_assoc",
 "pitch_interval_add_assoc: adding intervals one at a time",
 "Moving a pitch up by i and then by j gives exactly the same spelled pitch as moving it up by i + j, including the accidental.",
 r"""## Plain English

**Theorem (`pitch_interval_add_assoc`, Prismriver/Repr/Classical.lean lines 577–604).**
`j • (i • p) = (i + j) • p`. The letter part is integer associativity (line 582); the accidental part is a
rearrangement that ends with [nameDistance_image](#/node/Prismriver.Classical.nameDistance_image) (line 604).

It is the `smul_assoc` field of the [Torsor instance](#/node/Prismriver.Classical.instance_690). A companion,
`pitch_interval_add_comm` (lines 544–575), proves the order of i and j does not matter.
""",
 [q("Is spelling preserved: does C4 up a major third up a minor third give G4 (not F𝄪4)?",
    ["Yes: letters add (2 + 2 = 4 steps → G) and semitones add (4 + 3 = 7)", "No"], 0,
    "Both components of the interval add; the letter is fixed by name steps.")])

node("Prismriver.Classical.instance_502",
 "Adding an interval to a pitch",
 "i • p moves the letter by i's letter steps, then sets the accidental so the semitone change is exactly i's semitones.",
 r"""## Plain English

**Instance (`HSMul Interval Pitch Pitch`, Prismriver/Repr/Classical.lean lines 502–508).** New name =
`p.name + i.name`; new accidental = old accidental + `i.semitones` − (semitones between the two natural letters,
[nameDistance](#/node/Prismriver.Classical.nameDistance)). Example (line 526): a perfect fifth (4, 7) above B5 is
F♯6, since B→F naturally spans only 6 semitones.
""",
 [q("A perfect fifth above B is", ["F♯", "G♭", "F"], 0, "Prismriver/Repr/Classical.lean line 526.")])

node("Prismriver.Classical.instance_495",
 "The interval between two pitches",
 "q / p is (letter difference, semitone difference), where the semitone difference is the natural-letter distance plus the difference of accidentals.",
 r"""## Plain English

**Instance (`HDiv Pitch Pitch Interval`, Prismriver/Repr/Classical.lean lines 495–499).** Example (line 527):
E3 / C3 = major third (2, 4). See the [Torsor instance](#/node/Prismriver.Classical.instance_690) for the laws.
""",
 [q("E3 / C3 is", ["ma3 = (2, 4)", "mi3 = (2, 3)", "(4, 2)"], 0, "Prismriver/Repr/Classical.lean line 527.")])

# ------------------------------------------------------------ dihedral layer
node("Prismriver.Theory.Dihedral.Triad",
 "Triad: a pitch class with a major/minor tag",
 "A 'triad' here is only the pair (x in ZMod 12, major or minor), the usual way to label the 24 major and minor chords.",
 r"""## Plain English

**Abbreviation (`Triad := ZMod 12 × Parity`, Prismriver/Theory/Dihedral.lean line 23).** The first part is a
pitch class (C = 0, …, B = 11), the second a [Parity](#/node/Prismriver.Theory.Dihedral.Parity).

The helper `recoverTriple` (lines 58–65) turns a label into actual notes: major (x, major) gives x, x + M3, x + P5;
for minor it uses x + 5 as the root, so the minor label's number is the chord's fifth, not its root. That
convention matters only for display; no theorem uses `recoverTriple`.
""",
 [q("How many Triad values are there?", ["24", "12", "36"], 0, "12 pitch classes × 2 parities."),
  q("Does any theorem mention the actual chord notes?", ["No", "Yes"], 0, "recoverTriple is unused by the proofs.")],
 caveats=["The minor-label convention (number = fifth of the chord) is read off recoverTriple and is my interpretation; it does not affect any theorem."])

node("Prismriver.Theory.Dihedral.Parity",
 "Parity: major or minor",
 "A two-valued tag; flip swaps major and minor.",
 r"""## Plain English

**Inductive (`Parity`, Prismriver/Theory/Dihedral.lean lines 13–14)** with `flip` (lines 19–21). Inversions flip
it, because mirroring a major chord gives a minor chord.
""",
 [q("flip (flip q) is", ["q", "major"], 0, "Two swaps cancel.")])

node("Prismriver.Theory.Dihedral.pitch_toZMod12",
 "pitch_toZMod12: forget spelling and octave",
 "Semitones above C (natural-letter distance plus accidental), reduced mod 12; C♯ and D♭ both go to 1.",
 r"""## Plain English

**Definition (Prismriver/Theory/Dihedral.lean lines 25–26).** `accidental + nameDistance p.name 0`, cast to
`ZMod 12`. Its companion `interval_toZMod12` (lines 28–29) sends an interval to its semitones mod 12.

The key lemma `pitch_toZMod12_smul_interval` (lines 187–192) says the pitch class of i • p is the pitch class of
p plus i mod 12.
""",
 [q("pitch_toZMod12 of B♯3?", ["0", "11", "12"], 0, "11 + 1 = 12 ≡ 0."),
  q("Is it injective on spelled pitches?", ["No", "Yes"], 0, "It forgets spelling and octave.")])

node("Prismriver.Theory.Dihedral.pitch_toZMod12_smul_interval",
 "Pitch class of a transposed pitch",
 "pc(i • p) = pc(p) + i mod 12.",
 r"""## Plain English

**Lemma (Prismriver/Theory/Dihedral.lean lines 187–192).** Proved from the formulas for the action and
[nameDistance_image](#/node/Prismriver.Classical.nameDistance_image), then `grind`.
""",
 [q("It shows that pitch_toZMod12 turns `•` into", ["addition mod 12", "multiplication"], 0, "Prismriver/Theory/Dihedral.lean line 188.")])

node("Prismriver.Theory.Dihedral.pitch_toZMod12_srInterval",
 "Pitch class of an inverted pitch",
 "pc(srInterval i a p) = 2·pc(a) − pc(p) − i mod 12: the mod-12 mirror image of p about a, shifted down.",
 r"""## Plain English

**Lemma (Prismriver/Theory/Dihedral.lean lines 210–233).** Uses the pitch-class formulas for `•` with a negative
interval (lines 194–200) and for pitch differences (lines 202–208). It is the inversion case of the
[headline](#/node/Prismriver.Theory.Dihedral.transposeAction_toDihedral_triad).
""",
 [q("Mirror E (4) about C (0), shift 0:", ["8 (A♭)", "4", "0"], 0, "2·0 − 4 = −4 ≡ 8.")])

node("Prismriver.Theory.Dihedral.TransposeAction.toDihedral",
 "toDihedral: the D12 element of a pitch-level action",
 "A shift by i becomes the rotation r(i mod 12); an inversion about a with shift i becomes the reflection sr(i − 2a).",
 r"""## Plain English

**Definition (Prismriver/Theory/Dihedral.lean lines 50–55).** From a
[TransposeAction](#/node/Prismriver.TransposeAction) on classical pitches to Mathlib's `DihedralGroup 12`. The
`− 2a` is what moves the mirror's centre from a to C. The
[headline](#/node/Prismriver.Theory.Dihedral.transposeAction_toDihedral_triad) shows this choice is correct.
""",
 [q("toDihedral (.r ma3) is", ["r 4", "r 2", "sr 4"], 0, "ma3 has 4 semitones (line 53).")])

node("Prismriver.Theory.Dihedral.pitchTriad",
 "pitchTriad: label from a pitch and a tag",
 "pitchTriad p q = (pitch class of p, q).",
 r"""## Plain English

**Definition (Prismriver/Theory/Dihedral.lean line 235).** Uses
[pitch_toZMod12](#/node/Prismriver.Theory.Dihedral.pitch_toZMod12).
""",
 [q("pitchTriad (D♭4) major is", ["(1, major)", "(2, major)"], 0, "D♭ has pitch class 1.")])

node("Prismriver.Theory.Dihedral.TransposeAction.mapParity",
 "mapParity: does the action flip major/minor?",
 "Shifts keep the tag; inversions flip it.",
 r"""## Plain English

**Definition (Prismriver/Theory/Dihedral.lean lines 237–239).** See [Parity](#/node/Prismriver.Theory.Dihedral.Parity).
""",
 [q("mapParity (.r i) minor is", ["minor", "major"], 0, "Prismriver/Theory/Dihedral.lean line 238.")])

node("Prismriver.Theory.Dihedral.instance_77",
 "How D12 acts on a triad label",
 "r n adds n to the pitch class; sr n sends x to −x − n and flips the tag.",
 r"""## Plain English

**Instance (Prismriver/Theory/Dihedral.lean lines 77–83)**, using
[transposeTriad](#/node/Prismriver.Theory.Dihedral.transposeTriad) and
[invertTriad](#/node/Prismriver.Theory.Dihedral.invertTriad). The
[MulAction instance](#/node/Prismriver.Theory.Dihedral.instance_155) proves the action laws for it.
""",
 [q("sr 2 • (0, major) is", ["(10, minor)", "(2, minor)", "(2, major)"], 0, "−0 − 2 = −2 ≡ 10.")])

node("Prismriver.Theory.Dihedral.transposeTriad",
 "transposeTriad: T_n",
 "Adds n to the pitch class, keeps the tag.",
 r"""## Plain English

**Definition (Prismriver/Theory/Dihedral.lean lines 67–68).**
""",
 [q("transposeTriad 12 t is", ["t (12 ≡ 0 in ZMod 12)", "a different triad"], 0, "ZMod 12 arithmetic.")])

node("Prismriver.Theory.Dihedral.invertTriad",
 "invertTriad: I_n",
 "Sends (x, q) to (n − x, flip q).",
 r"""## Plain English

**Definition (Prismriver/Theory/Dihedral.lean lines 70–71).** The D12 action uses it with −n.
""",
 [q("invertTriad 0 (4, major) is", ["(8, minor)", "(4, minor)"], 0, "−4 ≡ 8, tag flips.")])

# ------------------------------------------------------------ not theorems
node("Prismriver.Composition.Counterpoint.isFirstSpecies",
 "isFirstSpecies: first-species counterpoint rules, as a Prop",
 "The counterpoint file writes the textbook first-species rules as a checkable proposition, and generates a mirror-image counterpoint, but proves nothing about the generator satisfying the rules.",
 r"""## Plain English

**Definition (Prismriver/Composition/Counterpoint.lean lines 76–113).** Two melodies of equal nonzero length are
first-species counterpoint when: every vertical interval is consonant (a parameter), every melodic move is allowed
(a parameter), the last two notes move in contrary motion, neither line outlines a tritone between turning points,
and (by default) the first and last intervals are unison or an octave (lines 22–74 define these pieces). The file header credits
the approach to Dr. Youyou Cong (line 1).

`formCounterpoint` (lines 10–20) builds a counterpoint by mirroring the cantus firmus. The only proofs here are two
small `example`s (lines 120–133), one closed by `native_decide`. There is no theorem that `formCounterpoint`
produces first-species counterpoint.

This is typical of most of Prismriver: the composition, score, syntax and IO modules are executable code, not
theorems.
""",
 [q("Is there a proof that formCounterpoint satisfies isFirstSpecies?", ["No", "Yes"], 0, "Only examples at lines 120–133."),
  q("Which choices are parameters rather than fixed?", ["What counts as consonant and as an allowed melodic move", "The length of the melodies"], 0,
    "`(consonant movement : Interval → Prop)`, line 80; the README explains consonance varies across cultures.")],
 caveats=["The native_decide example (lines 126–127) trusts the compiler, but it is an isolated example and nothing depends on it."])


# ------------------------------------------------------------ extra quiz questions (schema wants >= 3)
EXTRA = {
 "Prismriver.Classical.Accidental": [
  q("What is Accidental.sharp + Accidental.flat?", ["natural (0)", "a double sharp", "undefined"], 0, "Addition adds the integers: 1 + (−1) = 0 (Prismriver/Repr/Classical.lean lines 41–42)."),
  q("Does an Accidental know which letter it belongs to?", ["No, it is only an integer offset", "Yes"], 0, "The structure has the single field `semitones` (line 9).")],
 "Prismriver.Classical.Interval": [
  q("What is mi3 + ma3?", ["(4, 7) = p5", "(4, 8)", "(5, 7)"], 0, "Componentwise: (2+2, 3+4) = (4, 7), which is p5 (line 449).")],
 "Prismriver.Classical.Pitch": [
  q("What is Pitch.new .c 4?", ["name 28, natural", "name 48, natural", "name 4, natural"], 0, "0 + 4·7 = 28 (Prismriver/Repr/Classical.lean lines 151–152 and 174).")],
 "Prismriver.Classical.instance_495": [
  q("What is the letter part of (q / p)?", ["q.name − p.name", "p.name − q.name", "always 0"], 0, "`div_Pitch_Pitch_name`, Prismriver/Repr/Classical.lean lines 541–542."),
  q("Does C4 / B3 give a minor second (1, 1)?", ["Yes: one letter step, one semitone", "No, it gives (0, 1)"], 0, "B→C is one letter and nameDistance gives 1 semitone.")],
 "Prismriver.Classical.instance_502": [
  q("What is the letter part of i • p?", ["p.name + i.name", "p.name · i.name", "i.name"], 0, "`smul_Pitch_Interval_name`, Prismriver/Repr/Classical.lean lines 538–539."),
  q("Going up an octave from C4 gives", ["C5", "B4♯", "C4"], 0, "Prismriver/Repr/Classical.lean line 524 checks this by rfl.")],
 "Prismriver.Classical.nameDistance": [
  q("nameDistance 3 2 (F above E) is", ["1", "2", "0"], 0, "The step E→F is the third entry of spaces, 1 (Prismriver/Repr/Classical.lean line 130).")],
 "Prismriver.Classical.nameDistance_image": [
  q("Taking k = i, what does it give?", ["nameDistance i j = −nameDistance j i (with refl)", "nameDistance i j = 0"], 0, "nd(i,j) + nd(j,i) = nd(i,i) = 0, matching nameDistance_swap.")],
 "Prismriver.Classical.pitch_interval_add_assoc": [
  q("Which lemma closes the accidental part?", ["nameDistance_image", "native_decide", "pitchCong_equivalence"], 0, "Prismriver/Repr/Classical.lean line 604."),
  q("Which Torsor field does this theorem fill?", ["smul_assoc", "smul_div", "add_comm"], 0, "Prismriver/Repr/Classical.lean line 755.")],
 "Prismriver.Composition.Counterpoint.isFirstSpecies": [
  q("What does isFirstSpecies require of the two melodies' lengths?", ["Equal and nonzero", "Any lengths", "Exactly 4 notes"], 0, "The implicit arguments heq and h, Prismriver/Composition/Counterpoint.lean lines 78–79.")],
 "Prismriver.Theory.Dihedral.Parity": [
  q("Does a reflection sr n change the parity?", ["Yes, it flips it", "No"], 0, "invertTriad flips the tag (Prismriver/Theory/Dihedral.lean lines 70–71)."),
  q("Does a rotation r n change it?", ["No", "Yes"], 0, "transposeTriad keeps the tag (Prismriver/Theory/Dihedral.lean lines 67–68).")],
 "Prismriver.Theory.Dihedral.TransposeAction.mapParity": [
  q("mapParity (.sr a i) major is", ["minor", "major"], 0, "Prismriver/Theory/Dihedral.lean line 239 uses q.flip."),
  q("Does mapParity depend on a or i?", ["No, only on the constructor", "Yes"], 0, "Both arguments are ignored (`_`) in lines 238–239.")],
 "Prismriver.Theory.Dihedral.TransposeAction.toDihedral": [
  q("Which kind of D12 element does an inversion become?", ["A reflection sr", "A rotation r"], 0, "Prismriver/Theory/Dihedral.lean lines 54–55."),
  q("toDihedral (.sr C0 0) is", ["sr 0", "sr 12", "r 0"], 0, "C has pitch class 0, so 0 − 2·0 = 0.")],
 "Prismriver.Theory.Dihedral.Triad": [
  q("Which part of a Triad does a rotation change?", ["Only the pitch class", "Only the tag", "Both"], 0, "transposeTriad (Prismriver/Theory/Dihedral.lean lines 67–68).")],
 "Prismriver.Theory.Dihedral.instance_77": [
  q("r 5 • (7, minor) is", ["(0, minor)", "(2, minor)", "(0, major)"], 0, "7 + 5 = 12 ≡ 0, tag kept."),
  q("Is this instance alone a proof of the group-action laws?", ["No, those are in the MulAction instance at lines 155–183", "Yes"], 0, "SMul only gives the operation; MulAction adds the laws.")],
 "Prismriver.Theory.Dihedral.invertTriad": [
  q("Applying invertTriad n twice gives", ["the original triad", "a transposition by 2n"], 0, "n − (n − x) = x and flip∘flip = id; this is inverseInverse_subtract with i = j."),
  q("What does it do to the tag?", ["Flips it", "Keeps it"], 0, "Prismriver/Theory/Dihedral.lean line 71 uses t.2.flip.")],
 "Prismriver.Theory.Dihedral.pitchTriad": [
  q("Do C♯4 and D♭4 give the same pitchTriad (with the same tag)?", ["Yes, both have pitch class 1", "No"], 0, "pitch_toZMod12 forgets spelling."),
  q("Does pitchTriad change the tag?", ["No, it stores q as given", "Yes, it flips it"], 0, "Prismriver/Theory/Dihedral.lean line 235.")],
 "Prismriver.Theory.Dihedral.pitch_toZMod12": [
  q("pitch_toZMod12 of C5 is", ["0", "5", "60"], 0, "60 semitones above C0 is 0 mod 12.")],
 "Prismriver.Theory.Dihedral.pitch_toZMod12_smul_interval": [
  q("For p = B3 and i = mi2, the pitch class of i • p is", ["0 (C)", "11", "1"], 0, "11 + 1 = 12 ≡ 0."),
  q("Which earlier lemma does the proof use?", ["nameDistance_image", "transposeTriad_add"], 0, "Prismriver/Theory/Dihedral.lean line 191.")],
 "Prismriver.Theory.Dihedral.pitch_toZMod12_srInterval": [
  q("What does the shift i do?", ["Subtracts i mod 12 from the mirror image", "Adds 2i"], 0, "Prismriver/Theory/Dihedral.lean line 211."),
  q("Mirror G (7) about D (2), shift 0:", ["9 (A)", "5", "7"], 0, "2·2 − 7 = −3 ≡ 9.")],
 "Prismriver.Theory.Dihedral.transposeTriad": [
  q("transposeTriad 4 (0, major) is", ["(4, major)", "(4, minor)", "(8, major)"], 0, "Prismriver/Theory/Dihedral.lean lines 67–68."),
  q("Composing transposeTriad i and transposeTriad j gives", ["transposeTriad (i + j)", "invertTriad (i + j)"], 0, "transposeTriad_add, lines 91–97.")],
 "Prismriver.TransposeAction": [
  q("What does `.r i` do?", ["Shifts every pitch by i", "Mirrors about i"], 0, "rInterval i p = i • p (Prismriver/Repr/Dihedral.lean line 17).")],
 "Prismriver.instance_138": [
  q("(.sr a i) * (.r j) is", [".sr a (i + j)", ".r (i + j)", ".sr a (i − j)"], 0, "Prismriver/Repr/Dihedral.lean line 142."),
  q("Where is it shown that this table is right?", ["transposeAction_mul_smul", "pitchCong_equivalence"], 0, "Prismriver/Repr/Dihedral.lean lines 145–159.")],
 "Prismriver.instance_21": [
  q("(.sr a i) • p equals", ["srInterval i a p", "rInterval i p", "a"], 0, "Prismriver/Repr/Dihedral.lean line 24."),
  q("Is this instance specific to classical pitches?", ["No, generic over any Scale", "Yes"], 0, "It uses the file's variable [Scale P I] (line 9).")],
 "Prismriver.pitchCong": [
  q("Is pitchCong specific to octaves?", ["No, φ is any interval", "Yes"], 0, "φ : I is an argument (Prismriver/Repr/Scale.lean line 52).")],
 "Prismriver.pitchSetoid": [
  q("What proof does the setoid carry?", ["pitchCong_equivalence", "transposeAction_mul_smul"], 0, "Prismriver/Repr/Scale.lean line 82."),
  q("Is pitchClass used by the dihedral theorems?", ["No, they use pitch_toZMod12", "Yes"], 0, "Prismriver/Theory/Dihedral.lean never mentions pitchClass.")],
 "Prismriver.rInterval": [
  q("rInterval zero p is", ["p", "zero"], 0, "Torsor's smul_zero (Prismriver/Repr/Scale.lean line 37)."),
  q("rInterval i (srInterval j a p) is", ["srInterval (j − i) a p", "rInterval (i + j) p"], 0, "rInterval_srInterval, Prismriver/Repr/Dihedral.lean lines 31–44.")],
 "Prismriver.srInterval": [
  q("srInterval i a (srInterval j a p) is", ["rInterval (j − i) p", "p, always", "srInterval (i + j) a p"], 0, "srInterval_srInterval, Prismriver/Repr/Dihedral.lean line 71.")],
 "Prismriver.srInterval_change_center": [
  q("If a = b, the extra shift is", ["zero", "an octave"], 0, "a / a is the zero interval, so nothing changes."),
  q("Which composite theorem uses it?", ["srInterval_srInterval_general", "pitchCong_equivalence"], 0, "Prismriver/Repr/Dihedral.lean line 129.")],
 "Prismriver.srInterval_srInterval_general": [
  q("Which case of transposeAction_mul_smul does it handle?", ["sr after sr", "r after r"], 0, "Prismriver/Repr/Dihedral.lean line 159."),
  q("Does it need a and b to be equal?", ["No", "Yes"], 0, "a and b are arbitrary pitches (Prismriver/Repr/Dihedral.lean line 127).")],
}
for n in NODES:
    n["quiz"] += EXTRA.get(n["id"], [])
