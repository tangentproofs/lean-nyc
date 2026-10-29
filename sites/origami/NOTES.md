# NOTES for the coordinator: origami

## Time spent

About 45 minutes of wall-clock time, including five builds (each a few seconds; the repo is small).

## What was produced

- 33 nodes: 6 headlines (`huzita_2`, `huzita_5_iff`, `huzita_6`, `huzita_7_iff`, `haga_first_theorem`,
  `haga_gen_equation`), the full statement set (`Point`, `Line`, `Fold`, `f_through_p`, `on_line`, `f_places_p`,
  `f_places_l`, `perpendicular`, `parallel`, `dist2`, `dist2_line`, `is_huzita_2_compliant_fold`), the other axioms
  (`huzita_1`, `_3`, `_4`, `_5`, `_7`), and key lemmas (`mk_line`, `Line.eq_of_on_line`, `f_places_p_eq_self_iff`,
  `exists_hom_cubic_root`, `huzita_6_aux`, `huzita_6_needs_not_parallel`, `huzita_2_uniqueness`, `haga_construction`,
  `haga_fold_exists`, `haga_result`).
- about / review / trust pages. No Lean code blocks, no verbatim statements, no walkthrough `lean:` fields (no licence).
- Build ends with "built _site/origami" and no warnings.

## Calls I made

1. **Authors.** Added **wurtylex** (GitHub handle; the commit email suggests a real name, which I did not use) to
   `authors`, because per `git log` that account authored the single commit that created Normalisation, Relations,
   Reflection, CubicRoot, Huzita_axioms and Sharpness, i.e. most of what the site explains. An "OrigamiClub" account
   also made commits (Haga integration, codegen fixes); I mention it on the About page but did not put it in `authors`
   because I can't tell whose account it is. The README names no authors. `members` unchanged.
2. **Headlines.** Chose the axiom-free Haga theorems (`haga_first_theorem`, `haga_gen_equation`) as headlines, not
   `haga_result`, which depends on five Lean axioms; `haga_result` has its own node labelled CONDITIONAL. Of the seven
   axioms I made the four most interesting forms headlines (2, 5-iff, 6, 7-iff); 1, 3, 4, 5, 7 are ordinary nodes.
3. **Roots.** Scanned only `Origami.lean` and `Origami/lightweight_definitions/`. `Origami/paper_folding/` is not
   imported by Origami.lean and defines a second, conflicting `Fold` structure (it would clash with the `Fold` abbrev
   id); it is described in one paragraph on the About page and otherwise left out.
4. **Licence.** No LICENSE file and the README states none; left `spdx: null`.
5. **The web tool** (origami_api.py, origami_server.py, origami-sim/) is described briefly on the About page and in
   the `haga_construction` node, from reading origami_api.py and the Haga.lean comments. The origami-sim submodule
   was not checked out; I did not inspect its Rust code.

## Least sure about

- **`huzita_6` faithfulness note.** I say "not parallel" is sufficient but not necessary, citing the trivial case of
  points already on their lines. That is clearly right; the stronger background remark that the classical Beloch
  fold can exist for genuinely parallel lines in non-trivial configurations is phrased loosely on purpose. I also call
  it "the Beloch fold" and say it can have up to three solutions; that is standard background, not from the repo.
- **`huzita_6_aux` walkthrough step 3.** I describe the non-degeneracy step (lines 254–265) as "if l₁·(a,b) = 0, the
  cubic forces l₂·(a,b) = 0 as well (using p₁ not on l₁), so the lines would be parallel". I read the
  `linear_combination` steps but did not re-derive the cubic's coefficients in `exists_fold_normal`.
- **`haga_first_theorem` "Haga's first theorem" naming.** The Lean statement is about the reflected *bottom* edge
  passing through (0, 1/3). I checked numerically that this is the familiar thirds fold (the folded bottom edge meets
  the left edge at 1/3 from the bottom) and call it Haga's first theorem; textbook presentations orient the square
  differently, so a reader may see "2/3" elsewhere.
- **`haga_gen_equation`.** I say the bounds 0 < n < 1 are only used for n ≠ 1 and n ≠ 2 (lines 126–129). The proof
  also has a `split_ifs` branch (line 170) dismissed using n ≠ 1; I believe that's the only other use.
- **"Not built" caveats on `grind`-heavy proofs** (Haga.lean lines 74, 79, 88, 155, 164): these are the proofs most
  likely to be sensitive to the exact Lean/Mathlib version. No sorry, but unverified.

## Engine notes

- The scanner ignores `axiom` declarations (no ids for `p1`, `p2`, `hyp1`, `p1_coords`, `p2_coords`). Worked around
  by linking line numbers.
- The scanner cuts a theorem's statement at the first top-level `:=`, which for the Haga theorems is inside a leading
  `let pA : Point := …`. So their meaning-dependencies are incomplete (e.g. `haga_first_theorem` doesn't list
  `on_line`/`f_places_l`). Harmless here because statements are stripped anyway; mentioned on the Trust page.

## Things the authors might object to

- Calling the Haga statement "about the line, not the paper" in every Haga caveat might read as nitpicking; it is
  accurate (the square is never modelled).
- The CONDITIONAL label on `haga_result`: the Haga.lean comments argue the coordinate axioms are "exactly as
  legitimate" as postulating the points. I agree they are consistent and say so, but still label the result
  conditional.
- Early git history mentions AI assistance ("let gemini prove the huzita existence thm", and a comment in
  paper_folding/Properties.lean). I did not mention this on the site, since that code is not what's explained.
