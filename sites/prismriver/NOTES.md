# NOTES for the coordinator: prismriver

## Time spent

About 10–15 minutes of wall-clock time (system clock 04:55 → ~05:05 UTC, 2026-10-29), in one session: reading the four
proof files in full, skimming the rest, writing 41 nodes and 3 pages, then building until it passed.

## What I built

- 5 headlines: `transposeAction_toDihedral_triad`, the anonymous `MulAction (DihedralGroup 12) Triad` instance
  (`Prismriver.Theory.Dihedral.instance_155`), `transposeAction_mul_smul`, the anonymous `Torsor Pitch Interval`
  instance (`Prismriver.Classical.instance_690`), and `pitchCong_equivalence`.
- 36 supporting nodes (statement set plus a few proof lemmas), and one node for the counterpoint `Prop`
  `isFirstSpecies`, so the site shows that most of the library is executable code.
- Builds cleanly. The remaining "no explainer yet" warnings are small algebra lemmas (`Interval.add_comm`,
  `nameDistance_refl`, `transposeTriad_zero`, `Parity.flip`, `PseudoScale`, counterpoint sub-predicates).

## Calls I made (no questions asked)

- `ns` left empty, so ids are the full `Prismriver.…` names.
- Two headlines are anonymous instances. I used the scanner ids `instance_155` / `instance_690` because the
  instances are where the results are. If the engine or hub shows ids, these look ugly; the titles explain them.
- Authors kept as "Leni Aniva and Claire Wang" (README "Contributors" section and the arXiv paper). Git history:
  most commits are Leni Aniva's; the dihedral work started in Claire Wang's commits (as `clairew`).
- Paper title taken from the arXiv abstract page (2606.19936). I did not read the paper itself.
- I attributed the "paper" in the source comments (Prismriver/Theory/Dihedral.lean lines 73–76) to Crans–Fiore–
  Satyendra, *Musical Actions of Dihedral Groups*. **That is my inference**: the comment doesn't name it.

## Hardest parts

- The line numbers in Theory/Dihedral.lean: I first read it concatenated with another file and had to re-derive the
  per-file numbers. I checked every `lean:` walkthrough snippet against the source with a script (all verbatim)
  and checked the ranges against the scanner's `line`/`endLine`.
- Working out sign conventions: `srInterval`, `toDihedral (.sr a i) = sr (i − 2a)`, and the D12 action
  `sr n • (x,q) = (−x − n, flip q)`. I checked these by hand on several examples (used in the quizzes).

## Where I am least sure

- **`Prismriver.Theory.Dihedral.Triad`**: I say that a minor label (x, minor) has x = the chord's **fifth**,
  because `recoverTriple` uses `x + 5` as the root (lines 58–65). This is a reading of a display helper that no
  theorem uses; it is flagged as a caveat.
- **`Prismriver.Theory.Dihedral.transposeAction_toDihedral_triad`** and **review.md**: I call the comment at lines
  73–76 stale ("fix is transposing by −n when the group element is r n" vs. code using +n for `r n`). I think the
  comment may describe an earlier version, or mean something I'm missing. The walkthrough also notes that
  `rename_i` swaps the names `a`/`i` in the inversion case. My reading of that comes from the `have` on line 261
  (`2 * pitch_toZMod12 i`), not from running Lean.
- **`Prismriver.srInterval`** quiz: "srInterval 0 C4 E4 = A♭3". I computed this by hand from the definitions
  (name 26 = A3, accidental −1). I believe it's right but it isn't checked by an `example` in the repo.
- **`Prismriver.Composition.Counterpoint.isFirstSpecies`**: my paraphrase of `noTritoneTurningPoints` (lines
  67–74) as "no tritone outlined between turning points" is a simplification of a fiddly quantifier.
- **Torsor ≈ affine space.** I describe the project's `Torsor` as an abelian group acting simply transitively. That
  follows from `smul_div` + `div_smul_self`, but the class isn't literally Mathlib's `AddTorsor` (noted on the page).

## Things the authors might object to

- Calling most of the library "not theorems" / "an executable toolkit". That's true of the code, but it may
  undersell the design (the DSL and composition monads are a main contribution of the paper).
- Calling the D12 comment "stale".
- Saying the theorems are "modest" in review.md. I meant it as accurate, not dismissive.
- The two `native_decide` uses are flagged in trust.md even though they sit in an isolated `example`.

## Engine notes

- No engine bugs found. The schema needs ≥3 quiz questions and explanations of ≥10 characters. Tiny definition
  nodes therefore get somewhat padded quizzes (added through an `EXTRA` dict at the end of `nodes_src/defs.py`).
- Walkthrough `link`s to ids without a node are silently allowed. I pointed them at existing nodes instead.
