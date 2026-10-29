# About Prismriver

**Prismriver** ([lenianiva/Prismriver](https://github.com/lenianiva/Prismriver)) is a Lean 4 library and DSL for
music by **Leni Aniva** and **Claire Wang**. It comes with the paper *Prismriver: Formalization of Music Theory and
Algorithmic Composition in Lean 4* ([arXiv:2606.19936](https://arxiv.org/abs/2606.19936)). The README lists four
aims: formalizing music theory (pitches, accidentals, scales, chords, durations, parts), algorithmic analysis and
composition (such as counterpoint), mathematical modelling of music, and LilyPond-compatible note syntax.

## What the Lean actually is

Most of the roughly 3,600 lines are an **executable music toolkit**, not theorems:

- **Representation** (`Prismriver/Repr/`): scales and tunings, classical spelled pitches and intervals, time and
  measures, notes, instruments, scores.
- **Syntax** (`Prismriver/Syntax.lean`): a LilyPond-like note DSL, e.g. `♩[e4 c'4 b4 d4 e2]`.
- **Composition** (`Prismriver/Composition/`): monadic score building, motifs, chord progressions, random
  generation and counterpoint.
- **IO** (`Prismriver/IO/`): MusicXML output (with a small XML parser) and playback through [Alda](https://alda.io/).

The **proved** part is concentrated in four files, and that is what this site explains:

1. `Prismriver/Repr/Scale.lean`: the abstract [Torsor](#/node/Prismriver.Torsor) and
   [Scale](#/node/Prismriver.Scale) classes, and [octave equivalence](#/node/Prismriver.pitchCong_equivalence).
2. `Prismriver/Repr/Classical.lean`: Western spelled pitches and intervals, with the proof that they form a
   [Torsor](#/node/Prismriver.Classical.instance_690).
3. `Prismriver/Repr/Dihedral.lean`: transpositions and inversions on any scale, and their
   [composition law](#/node/Prismriver.transposeAction_mul_smul).
4. `Prismriver/Theory/Dihedral.lean`: the 24 major/minor triad labels as a
   [D12 action](#/node/Prismriver.Theory.Dihedral.instance_155), and the
   [bridge theorem](#/node/Prismriver.Theory.Dihedral.transposeAction_toDihedral_triad) from pitch-level actions to D12.

## Where to start

Read [Interval](#/node/Prismriver.Classical.Interval) and [Pitch](#/node/Prismriver.Classical.Pitch) first,
then the headline [transposeAction_toDihedral_triad](#/node/Prismriver.Theory.Dihedral.transposeAction_toDihedral_triad).

## What this site leaves out

Everything outside those four files: time, scores, instruments, the syntax and its macros, MusicXML/XML,
Alda playback, motifs, chord progressions and random composition. The counterpoint rules get one node
([isFirstSpecies](#/node/Prismriver.Composition.Counterpoint.isFirstSpecies)) because they are stated as a `Prop`.
Small algebra lemmas (such as `Interval.add_comm`) and the key-relative `KeyInterval` (with its lemma
`plain_no_accidental`, Prismriver/Repr/Classical.lean lines 665–673) are mentioned but have no node of their own.
