# Review: do the statements say what the names suggest?

Short verdict: **yes, and they are modest.** The project makes no exaggerated claims; each headline is a
clean algebraic fact with no `sorry` and no extra hypotheses. What follows is what each statement does and does
not cover.

## transposeAction_toDihedral_triad (Prismriver/Theory/Dihedral.lean lines 241–270)

- **Says:** reducing mod 12 commutes with the action: act on a spelled pitch and then take (pitch class, tag),
  or take (pitch class, tag) and then act by `toDihedral t`. Inversions flip the major/minor tag.
- **Does not say:** that `toDihedral` respects composition (a homomorphism), that it is onto D12, or anything
  about three-note chords. A "Triad" is the pair `ZMod 12 × Parity`; the chord-building helper `recoverTriple` is
  not used in any proof.
- **Surprising detail:** the comment at lines 73–76 says the convention fix is "transposing by −n when the group
  element is r n", but the code transposes by +n for `r n` and uses −n inside `sr n`. The code is consistent
  (the `MulAction` laws are proved for it), so this is a stale comment, not a bug in the result.
- The fixed local `Scale` instance (C major, line 185) does not narrow the theorem: only the pitch/interval
  arithmetic is used.

## MulAction (DihedralGroup 12) Triad (Prismriver/Theory/Dihedral.lean lines 155–183)

- A genuine Mathlib `MulAction`, so faithful to the name. Faithfulness of the action and the PLR
  (neo-Riemannian) group are not covered.

## transposeAction_mul_smul (Prismriver/Repr/Dihedral.lean lines 145–159)

- Holds for **any** scale satisfying the Torsor laws, which is a nice generality.
- It is a composition law for an explicitly defined `*`. It does not make `TransposeAction` a group: no
  associativity or inverse laws are proved, and the representation is not unique (an inversion can be written
  about any centre, by `srInterval_change_center`).

## Torsor Pitch Interval (Prismriver/Repr/Classical.lean lines 690–786)

- Proves every field of the project's own `Torsor` class. That class is close to "abelian group acting simply
  transitively" (an affine space), but it is not Mathlib's `AddTorsor`, so Mathlib's lemmas do not apply
  directly.

## pitchCong_equivalence (Prismriver/Repr/Scale.lean lines 55–76)

- Exactly as named. Note that on spelled pitches, octave equivalence keeps spelling (C♯ and D♭ are different
  classes); the dihedral file uses a separate mod-12 map that forgets spelling.

## Non-theorem code

The counterpoint rules (`isFirstSpecies`) are definitions only; nothing proves the generator `formCounterpoint`
meets them. Many results in the library are `example … := rfl` checks of specific computations (e.g. a fifth above
B5 is F♯6), which are useful tests but not general theorems.
