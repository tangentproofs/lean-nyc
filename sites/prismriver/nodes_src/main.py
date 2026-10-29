NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

NOT_BUILT = "Not built for this site: 'proved' means the file contains a complete-looking proof with no sorry, not that the Lean kernel was run on it here."

# ---------------------------------------------------------------- headline 1
node("Prismriver.Theory.Dihedral.transposeAction_toDihedral_triad",
 "Headline: pitch-level transposition and inversion match the D12 action",
 "Transposing or mirroring a real, spelled pitch and then reducing it mod 12 gives the same answer as first reducing it and then applying the matching element of the dihedral group D12. Inversions also flip the major/minor tag.",
 r"""## Plain English

**Theorem (`transposeAction_toDihedral_triad`, Prismriver/Theory/Dihedral.lean lines 241–270).** Take any
[TransposeAction](#/node/Prismriver.TransposeAction) `t` on spelled pitches (a transposition by an interval, or an
inversion about a pitch followed by a transposition), any [Pitch](#/node/Prismriver.Classical.Pitch) `p`, and any
[Parity](#/node/Prismriver.Theory.Dihedral.Parity) `q` (major or minor). Then

> the D12 element [toDihedral t](#/node/Prismriver.Theory.Dihedral.TransposeAction.toDihedral), acting on the pair
> [pitchTriad p q](#/node/Prismriver.Theory.Dihedral.pitchTriad) = (pitch class of p, q),
> gives the pair (pitch class of `t • p`, [mapParity t q](#/node/Prismriver.Theory.Dihedral.TransposeAction.mapParity)).

In a picture: the square

```
 spelled pitch  p  ──── t ────▶  t • p
      │                            │
  mod 12, tag q              mod 12, new tag
      ▼                            ▼
 (pc p, q) ── toDihedral t ──▶ (pc (t•p), mapParity t q)
```

commutes. Transpositions `.r i` go to the rotation `r (i mod 12)` and keep the tag. Inversions `.sr a i`
(reflect about `a`, then go down by `i`) go to the reflection `sr (i − 2a)` and flip major ↔ minor.

This is the bridge between Prismriver's "real" music objects (pitches with letter names and accidentals, so
C♯ ≠ D♭) and the classical neo-Riemannian picture, where the 24 major and minor triads are permuted by the
dihedral group of order 24 (Crans, Fiore and Satyendra, *Musical Actions of Dihedral Groups*, is the standard
reference; the source comments call it "the paper", lines 73–76).

The D12 action on the right-hand side is the [MulAction instance](#/node/Prismriver.Theory.Dihedral.instance_155).

## What a "triad" is here

A [Triad](#/node/Prismriver.Theory.Dihedral.Triad) is just a pair (pitch class in `ZMod 12`, major/minor). The
theorem never builds three-note chords: it tracks *one* pitch plus a tag. That is enough to name a triad (a root
and a quality) and is how the textbook D12 action is usually set up, but read the result as being about labels, not
chords.
""",
 [q("Which way does the square go?",
    ["Act on the spelled pitch then reduce mod 12 = reduce mod 12 then act with toDihedral t",
     "toDihedral is a group homomorphism",
     "Every D12 element comes from some TransposeAction"], 0,
    "That is exactly the equation on Prismriver/Theory/Dihedral.lean line 242. Homomorphism and surjectivity are not stated."),
  q("What happens to the major/minor tag under `.sr a i`?",
    ["It flips", "It stays", "It depends on a"], 0,
    "mapParity sends `.sr _ _` to `q.flip` (Prismriver/Theory/Dihedral.lean lines 237–239)."),
  q("Does the theorem say anything about enharmonic spelling (C♯ vs D♭)?",
    ["No: pitch_toZMod12 forgets the spelling, so only the pitch class is compared",
     "Yes: it proves the spelling is preserved"], 0,
    "Both sides are pitchTriad values, which store only `pitch_toZMod12 p : ZMod 12` (line 235)."),
  q("Is `Triad` a list of three pitches?",
    ["No, it is ZMod 12 × Parity", "Yes, it is List Pitch of length 3"], 0,
    "Prismriver/Theory/Dihedral.lean line 23. The helper recoverTriple builds the chord but no theorem uses it."),
  q("Which D12 element does inversion `.sr a i` map to?",
    ["sr (i − 2·a), with i and a read mod 12", "sr (a − i)", "r (−i)"], 0,
    "Prismriver/Theory/Dihedral.lean lines 54–55."),
 ],
 caveats=[NOT_BUILT,
  "The theorem is an equivariance (compatibility) statement. It does not prove that toDihedral respects composition, that it is onto, or that the D12 action is faithful.",
  "The Scale instance used for pitches is a local C-major diatonic scale (Prismriver/Theory/Dihedral.lean line 185). Only its interval/pitch arithmetic matters, which is the same for every diatonic scale, so the choice of C major does not restrict the theorem.",
  "The source comment at lines 73–76 says the fix for Mathlib's convention is 'transposing by −n when the group element is r n', but the code transposes by +n for r n and uses −n for sr n. The proved statement is about the code, which is self-consistent (the MulAction laws are checked).",
  "'Triad' means (pitch class, major/minor tag), not a three-note chord."],
 widgets=[{"type": "walkthrough", "title": "How the proof goes (Prismriver/Theory/Dihedral.lean, lines 241-270)",
  "config": {"steps": [
   {"text": "Split on the shape of the action: a transposition `.r i` or an inversion `.sr a i`.", "lean": "  cases t", "link": "Prismriver.TransposeAction"},
   {"text": "Transposition, pitch-class component (lines 244–249): unfold everything; it reduces to 'pitch class of i • p = pitch class of p + i mod 12'.", "lean": "  rw [pitch_toZMod12_smul_interval]", "link": "Prismriver.Theory.Dihedral.pitch_toZMod12_smul_interval"},
   {"text": "Transposition, tag component (lines 250–252): r keeps the tag on both sides; `simp` closes it.", "lean": "  unfold pitchTriad TransposeAction.toDihedral TransposeAction.mapParity"},
   {"text": "Inversion, pitch-class component (lines 253–265): after unfolding, the left side is −p − (i − 2a); a small `grind` rewrite puts it as 2a − p − i.", "lean": "  have : 2 * pitch_toZMod12 i - interval_toZMod12 a + -pitch_toZMod12 p = 2 * pitch_toZMod12 i - pitch_toZMod12 p - interval_toZMod12 a := by"},
   {"text": "The right side is the pitch class of srInterval i a p, which the lemma computes as 2a − p − i (line 267). (In this goal `rename_i` named the pitch `i` and the interval `a`, the reverse of the statement's names.)", "lean": "  rw [pitch_toZMod12_srInterval]", "link": "Prismriver.Theory.Dihedral.pitch_toZMod12_srInterval"},
   {"text": "Inversion, tag component (lines 268–270): sr flips the tag on both sides.", "lean": "  simp"}]}}])

# ---------------------------------------------------------------- headline 2
node("Prismriver.Theory.Dihedral.instance_155",
 "Headline: D12 really acts on the 24 (pitch class, major/minor) pairs",
 "Rotations r n transpose a triad label by n, reflections sr n send x to −x − n and swap major/minor, and the file proves these rules obey the group-action laws for Mathlib's DihedralGroup 12.",
 r"""## Plain English

**Instance (`MulAction (DihedralGroup 12) Triad`, Prismriver/Theory/Dihedral.lean lines 155–183).** The rule from
the [SMul instance](#/node/Prismriver.Theory.Dihedral.instance_77) (lines 77–83),

- `r n • (x, q) = (x + n, q)` ([transposeTriad](#/node/Prismriver.Theory.Dihedral.transposeTriad)),
- `sr n • (x, q) = (−x − n, flip q)` ([invertTriad](#/node/Prismriver.Theory.Dihedral.invertTriad) with −n),

is a genuine **group action** of Mathlib's `DihedralGroup 12` on [Triad](#/node/Prismriver.Theory.Dihedral.Triad)
= `ZMod 12 × Parity`: the identity does nothing, and acting by `g * h` equals acting by `h` then by `g`.

Musically, these are the familiar T/I operations: T<sub>n</sub> (transpose by n semitones) and I<sub>n</sub>
(mirror the pitch-class clock, which turns major chords into minor ones and back). The four composition rules
proved along the way are the classical ones, written as comments in the source:
T<sub>m</sub>∘T<sub>n</sub> = T<sub>m+n</sub>, T<sub>m</sub>∘I<sub>n</sub> = I<sub>m+n</sub>,
I<sub>m</sub>∘T<sub>n</sub> = I<sub>m−n</sub>, I<sub>m</sub>∘I<sub>n</sub> = T<sub>m−n</sub>
(lines 90–137).

Because it is a Mathlib `MulAction`, everything Mathlib knows about group actions (orbits, stabilisers, …) applies
to it, though the project does not go on to use that.
""",
 [q("What does `r 3` do to the label (C = 0, major)?",
    ["(3, major): up three semitones, still major", "(−3, minor)", "(0, minor)"], 0,
    "r n acts by transposeTriad n (Prismriver/Theory/Dihedral.lean lines 80–81 and 67–68)."),
  q("What does `sr 0` do to (4, major)?",
    ["(−4, minor) = (8, minor)", "(4, minor)", "(4, major)"], 0,
    "sr n acts by invertTriad (−n): (−x + (−n), flip q) (lines 82–83 and 70–71)."),
  q("Which law is the `mul_smul` field?",
    ["(g * h) • t = g • (h • t)", "g • h = h • g", "g • t = t for all g"], 0,
    "Mathlib's MulAction requires one_smul and mul_smul; the instance proves both (lines 156–183)."),
  q("Does the instance prove the action is faithful (different group elements act differently)?",
    ["No, only the two action laws", "Yes"], 0,
    "Only `one_smul` and `mul_smul` are given. (It is faithful, but that is not in the file.)"),
 ],
 caveats=[NOT_BUILT, "Triad is (pitch class, tag), not a chord of three notes.",
  "The rotation convention is chosen to fit Mathlib's DihedralGroup multiplication; see the comment at lines 73–76, which describes the fix slightly differently from the code."],
 widgets=[{"type": "walkthrough", "title": "How the proof goes (Prismriver/Theory/Dihedral.lean, lines 155-183)",
  "config": {"steps": [
   {"text": "Identity: Mathlib's 1 is r 0, and transposing by 0 does nothing.", "lean": "      apply transposeTriad_zero", "link": "Prismriver.Theory.Dihedral.transposeTriad"},
   {"text": "Composition: split both group elements into r or sr, giving four cases.", "lean": "      cases t <;> cases x"},
   {"text": "r·r: Mathlib's r_mul_r, then T_i ∘ T_j = T_{i+j}.", "lean": "        apply transposeTriad_add", "link": "Prismriver.Theory.Dihedral.transposeTriad_add"},
   {"text": "r·sr: Mathlib's r_mul_sr, some sign bookkeeping, then T_i ∘ I_j = I_{i+j}.", "lean": "        apply transposeInverse_add", "link": "Prismriver.Theory.Dihedral.transposeInverse_add"},
   {"text": "sr·r: Mathlib's sr_mul_r, then I_i ∘ T_j = I_{i−j}.", "lean": "        apply inverseTranspose_subtract", "link": "Prismriver.Theory.Dihedral.inverseTranspose_subtract"},
   {"text": "sr·sr: Mathlib's sr_mul_sr, then two inversions make a transposition.", "lean": "        apply inverseInverse_subtract'", "link": "Prismriver.Theory.Dihedral.inverseInverse_subtract'"}]}}])

# ---------------------------------------------------------------- headline 3
node("Prismriver.transposeAction_mul_smul",
 "Headline: two transpositions/inversions compose into one",
 "In any scale, doing one TransposeAction after another is the same as doing a single, explicitly computed TransposeAction; two inversions about different centres give a transposition by twice the distance between the centres (plus the difference of their shifts).",
 r"""## Plain English

**Theorem (`transposeAction_mul_smul`, Prismriver/Repr/Dihedral.lean lines 145–159).** For any pitch and interval
types with a [Scale](#/node/Prismriver.Scale) structure, and any two
[TransposeActions](#/node/Prismriver.TransposeAction) `t1`, `t2` and pitch `p`:

> `t1 • (t2 • p) = (t1 * t2) • p`

where the "product" `t1 * t2` is given by an explicit table ([Mul instance](#/node/Prismriver.instance_138),
lines 138–143):

| t1 | t2 | t1 * t2 |
|---|---|---|
| `.r i` | `.r j` | `.r (i + j)` |
| `.r i` | `.sr a j` | `.sr a (j − i)` |
| `.sr a i` | `.r j` | `.sr a (i + j)` |
| `.sr a i` | `.sr b j` | `.r ((a/b) + (a/b) + (j − i))` |

(`a / b` is the interval from `b` up to `a`.) The last row is the music-theory fact that mirroring twice, about
centres `b` then `a`, is a plain transposition by twice the distance from `b` to `a` (adjusted by the shifts).

This works for *every* scale, not just Western 12-tone pitches: it uses only the
[Torsor](#/node/Prismriver.Torsor) laws (intervals form an abelian group acting on pitches). So it applies to
spelled classical pitches, to equal temperament, and to any xenharmonic system someone plugs in.
""",
 [q("What is `(.r i) * (.r j)`?", [".r (i + j)", ".r (i − j)", ".sr i j"], 0,
    "Prismriver/Repr/Dihedral.lean line 140."),
  q("The product of two inversions, `(.sr a i) * (.sr b j)`, is", ["a transposition `.r …`", "another inversion", "the identity, always"], 0,
    "Line 143: the result is `.r ((a / b) + (a / b) + (j - i))`."),
  q("Does this theorem prove TransposeAction forms a group?", ["No: it only shows the table matches composition of actions", "Yes, including associativity and inverses"], 0,
    "There is no associativity or inverse proof for this Mul, and different TransposeActions can act identically (e.g. inversions written about different centres), so it is not a group as a data type."),
  q("Which assumptions does it need about the pitch system?", ["Only the Scale/Torsor laws", "12-tone equal temperament", "Western letter names"], 0,
    "The file is generic in `{P I} [Scale P I]` (Prismriver/Repr/Dihedral.lean line 9)."),
 ],
 caveats=[NOT_BUILT,
  "This is a composition law, not a group structure on TransposeAction (no associativity or inverse proof, and representations are not unique)."],
 widgets=[{"type": "walkthrough", "title": "How the proof goes (Prismriver/Repr/Dihedral.lean, lines 145-159)",
  "config": {"steps": [
   {"text": "Four cases, one per row of the table.", "lean": "  cases t1 <;> cases t2 <;> simp [HMul.hMul, Mul.mul]"},
   {"text": "r after r: two shifts add (Torsor's smul_assoc and add_comm).", "lean": "  rw [rInterval_rInterval]", "link": "Prismriver.rInterval"},
   {"text": "r after sr: shifting an inversion changes only its shift.", "lean": "  rw [rInterval_srInterval]", "link": "Prismriver.rInterval"},
   {"text": "sr after r: inverting a shifted pitch is inverting with a bigger shift.", "lean": "  rw [srInterval_rInterval]", "link": "Prismriver.srInterval"},
   {"text": "sr after sr: move the second inversion's centre to the first (srInterval_change_center), then two inversions about the same centre cancel to a shift.", "lean": "  rw [srInterval_srInterval_general]", "link": "Prismriver.srInterval_srInterval_general"}]}}])

# ---------------------------------------------------------------- headline 4
node("Prismriver.Classical.instance_690",
 "Headline: intervals act on spelled pitches (the Torsor instance)",
 "Western spelled pitches with (letter-steps, semitones) intervals satisfy every Torsor law: intervals form an abelian group, adding them to a pitch is a group action, and between any two pitches there is exactly one interval.",
 r"""## Plain English

**Instance (`Torsor Pitch Interval`, Prismriver/Repr/Classical.lean lines 690–786).** This instance is where the
library's arithmetic of music is proved correct for classical notation. A
[Pitch](#/node/Prismriver.Classical.Pitch) is a letter position plus an accidental; an
[Interval](#/node/Prismriver.Classical.Interval) is a pair (letter steps, semitones), so a major third is (2, 4)
and a diminished fourth is (3, 4): same sound, different spelling.

Adding an interval to a pitch ([the `•` action](#/node/Prismriver.Classical.instance_502), lines 502–508) moves the
letter by the letter steps and then fixes the accidental so the total semitone change is right. Subtracting two
pitches ([the `/` operation](#/node/Prismriver.Classical.instance_495), lines 495–499) gives the interval between them.

The instance proves all the fields of the project's [Torsor](#/node/Prismriver.Torsor) class:

- intervals form an abelian group (zero, `+` commutative and associative, negation, subtraction, integer multiples);
- `zero • p = p` and `j • (i • p) = (i + j) • p` (a group action);
- `(q / p) • p = q` and `(i • p) / p = i` (from any pitch, exactly one interval reaches any other).

So e.g. E3 / C3 = major third, and going up a fifth from B5 lands on F♯6, not G♭6 (both are `example … := rfl`
checks at lines 524–529).

The heavy lifting is [pitch_interval_add_assoc](#/node/Prismriver.Classical.pitch_interval_add_assoc), which in turn
rests on [nameDistance_image](#/node/Prismriver.Classical.nameDistance_image): the semitone distances between natural
notes add up along the way.
""",
 [q("Why does an Interval have two numbers?",
    ["To keep spelling: letter steps and semitones are tracked separately", "One for each octave", "For frequency ratio and cents"], 0,
    "Prismriver/Repr/Classical.lean lines 340–343; e.g. mi3 = ⟨2, 3⟩ and ma3 = ⟨2, 4⟩."),
  q("Which law says the interval from p to q, added to p, gives q?", ["smul_div", "smul_zero", "add_comm"], 0,
    "smul_div (p q) : (q / p) • p = q, proved at Prismriver/Repr/Classical.lean lines 756–774."),
  q("Is `Torsor` Mathlib's `AddTorsor`?", ["No, it is Prismriver's own class with similar laws", "Yes"], 0,
    "Defined in Prismriver/Repr/Scale.lean lines 18–40, with its own field names and integer multiplication."),
  q("What does the instance give you for free?",
    ["Generic theorems (like transposeAction_mul_smul) apply to classical pitches", "A proof that the music sounds good", "MusicXML export"], 0,
    "Everything stated for `[Scale P I]` or `[Torsor P I]` now applies to Pitch/Interval."),
 ],
 caveats=[NOT_BUILT,
  "The Torsor class's laws are exactly the ones listed in Prismriver/Repr/Scale.lean lines 18–40; they are close to, but not literally, Mathlib's AddCommGroup + AddTorsor."],
 widgets=[{"type": "walkthrough", "title": "How the proof goes (Prismriver/Repr/Classical.lean, lines 690-786)",
  "config": {"steps": [
   {"text": "Group laws for intervals are componentwise integer arithmetic, proved earlier (lines 370–438) and plugged in.", "lean": "  add_comm := Interval.add_comm", "link": "Prismriver.Classical.Interval"},
   {"text": "Adding the zero interval: the name distance from a letter to itself is 0.", "lean": "    rewrite [nameDistance_refl]", "link": "Prismriver.Classical.nameDistance"},
   {"text": "Action law: adding i then j equals adding i + j. This is the hard lemma.", "lean": "  smul_assoc p i j := pitch_interval_add_assoc i j p", "link": "Prismriver.Classical.pitch_interval_add_assoc"},
   {"text": "smul_div (lines 756–774): unfold `/` and `•`; the letter parts cancel by omega and the accidental parts by integer rearrangement (h1–h4).", "lean": "    have h4 : q.acc.semitones - p.acc.semitones + p.acc.semitones = q.acc.semitones := by omega"},
   {"text": "div_smul_self (lines 775–786): the interval recovered from i • p and p is i, by cancelling the name distance.", "lean": "   rw [Accidental.sub_Accidental_semitones]"}]}}])

# ---------------------------------------------------------------- headline 5
node("Prismriver.pitchCong_equivalence",
 "Headline: 'same note, different octave' is an equivalence relation",
 "For any scale and any interval φ, 'p equals q shifted by a whole number of φ' is reflexive, symmetric and transitive, which is what lets the library form pitch classes as a quotient.",
 r"""## Plain English

**Theorem (`pitchCong_equivalence`, Prismriver/Repr/Scale.lean lines 55–76).** Fix a
[Scale](#/node/Prismriver.Scale) and an interval `φ`. Say `p ≡ q` ([pitchCong](#/node/Prismriver.pitchCong),
lines 52–53) when `p = (n * φ) • q` for some integer `n`. Then `≡` is an equivalence relation.

With `φ` the octave this is octave equivalence: C4 ≡ C5 ≡ C−1. The theorem is used to build
[pitchSetoid](#/node/Prismriver.pitchSetoid) and the quotient type `pitchClass` (lines 78–87), the abstract
"pitch class" of a scale. It is stated for any `φ`, so it also covers tritave-based scales (Bohlen–Pierce) or
other xenharmonic systems.

It is a short, general fact, but it is the formal backing for the README's claim that a scale is pitches
"with a fundamental interval".
""",
 [q("Which integer witnesses p ≡ p?", ["0", "1", "−1"], 0, "Reflexivity uses n = 0 and `zero_mul`, `smul_zero` (Prismriver/Repr/Scale.lean lines 57–60)."),
  q("If p ≡ q via n, which integer gives q ≡ p?", ["−n", "n", "n + 1"], 0, "Lines 62–66."),
  q("Must φ be the scale's fundamental interval?", ["No, any interval φ works", "Yes"], 0,
    "φ is an explicit argument (line 55); only pitchSetoid defaults it to the fundamental."),
  q("Is the Western classical pitch class (mod 12) this same quotient?",
    ["Not exactly: with φ = octave on spelled pitches, C♯ and D♭ stay different classes", "Yes, identical"], 0,
    "Shifting by octaves never changes spelling, so the quotient remembers it; the mod-12 map in the Dihedral file is separate (pitch_toZMod12)."),
 ],
 caveats=[NOT_BUILT],
 widgets=[{"type": "walkthrough", "title": "How the proof goes (Prismriver/Repr/Scale.lean, lines 55-76)",
  "config": {"steps": [
   {"text": "Reflexive: take n = 0; 0·φ is the zero interval, which acts trivially.", "lean": "      apply Exists.intro 0"},
   {"text": "Symmetric: from p = (n·φ) • q, take −n and use smul_assoc and i + (−i) = 0.", "lean": "      apply Exists.intro (-n)"},
   {"text": "Transitive: chain the witnesses; (npq + nqr)·φ splits by mul_distrib.", "lean": "      apply Exists.intro (npq + nqr)"}]}}])
