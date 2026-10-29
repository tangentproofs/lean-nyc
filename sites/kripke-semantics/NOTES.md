# NOTES for the coordinator: kripke-semantics (Boarders/kripke-semantics @ 95de19f)

Not published. Written by the Claude session that wrote this explainer.

## Time spent
About 15 minutes of wall-clock time (roughly 05:10–05:25 UTC on 2026-10-29). Most of it went on reading all
12 library files (~2,200 lines) and checking per-file line numbers.

## What I produced
- `site.json`: filled in. Headlines: `Kripke.soundness`, `Kripke.completeness`,
  `Kripke.ExcludedMiddle.em_not_provable`, `Beth.soundness`, `Beth.Completeness.completeness`.
  Roots: `Logic`, `Kripke`, `Beth`. `ns` left empty (three top-level namespaces: `Syntax`, `Kripke`, `Beth`).
- 48 nodes in `nodes_src/` (a_syntax, b_kripke, c_canonical, d_beth, e_trees, f_details, g_small), plus
  `_extra.py` (extra quiz questions) and `_scanfix.py` (engine workaround, below). Every headline has a
  walkthrough with line references.
- `pages/about.md`, `pages/review.md`, `pages/trust.md`.
- No licence: no Lean code blocks, no verbatim statements, no `lean:` fields. Math is described in my own
  notation (Γ ⊢ φ, ∨, ⇒ …); inline identifiers only.

## Engine issue (worked around, not fixed)
`scan_decls.py` resolves the **field** `covers` of `structure Coverage` (Beth/Coverage.lean line 37) to the
top-level def `Beth.covers` (line 48). That creates a fake cycle Coverage → covers → HasCoverage → Coverage,
and `test_statement.mjs` then fails with "Beth.HasCoverage should come before Beth.covers" (a topological-order
assertion that cannot hold on a cycle). The build stops.

Workaround: `nodes_src/_scanfix.py` runs during `write_nodes.py` (which executes every `.py` in nodes_src,
after `scan_decls.py`) and deletes that single spurious edge from `build/<slug>/data/decls.json`. It does not
touch `engine/`. It is a hack: if you'd rather not have site code patch build data, the alternatives are
(a) fix the scanner so `name :` at the start of a structure-field line is not resolved as a mention, or
(b) make `Beth.Coverage` a headline (headline deps are exempt from the order assertion), which I rejected
because it is a definition, not a result. Suggested engine fix: in `deps()`, skip tokens that are immediately
followed by ` :` inside a `structure`/`class` body.

## Judgement calls
- **Authors:** the README is just "# kripke" and there is no LICENSE/NOTICE. All 18 commits are by
  `Boarders`. I kept the coordinator's "Callan McGill" (I did not verify the real-name mapping myself).
- **Kripke/Syntax.lean** is an earlier, unimported fragment (∧, ⇒, ⊤ only). Scanned but given no node; mentioned
  on the `Syntax.Tm` node and the About page.
- **Statement set.** The scanner misses that headline statements mention `Pf`, `Ctxt`, `Tm` (opened namespace),
  but I wrote nodes for them anyway. It adds the alias `Semantics` (Kripke/Soundness.lean line 5) because of the
  same-named namespace `Kripke.Semantics`; I gave it a short node explaining this.
- 34 "no explainer" warnings remain, all for helper lemmas (snoc-list bookkeeping, `glue_sieves`, `pf_sheaf`
  as a separate id, `mk_disjunction`, etc.). These are explained inside the nodes that use them.
- The binary-tree P ∨ Q result is an anonymous `example`, so it has no id; I hung it on the
  `binaryBranchVal` node.
- I described `Beth.soundness`/`Kripke.soundness` as theorems although they are declared `def` (types are Props).

## Places I am least sure of
1. **Beth/Coverage.lean line 33 (`pullback`, `bounded` field).** From the text, it returns `hrp`, which is not
   bound anywhere (the pattern binds `hr`). I believe this does not compile, which would break the whole Beth
   half at this commit. But autoImplicit/elaboration quirks are hard to rule out without building, and the
   author's commit history ("polish and improve many things", 2026-04-14, introduced it) gives no CI signal. I
   flagged it as "possible, unconfirmed" on the Sieve, pullback, Beth.soundness and Beth completeness nodes and on
   Trust/Review pages. **If you can build it, please check; if it compiles, soften those caveats.**
2. **`Beth.Examples.bethFrameOfKripke`**: I say Beth forcing in this frame "amounts to" Kripke forcing. I argued it
   informally (the only cover is the maximal sieve, and persistence at w itself); the project does not prove it,
   and I say so. Low risk, but it is my claim, not theirs.
3. **`Beth.Completeness.completeness` / review page**: I say the result does not give completeness for Beth
   *trees*. I am fairly confident (the canonical frame is a frame of contexts with a generated coverage), but an
   author might reasonably reply that the general frames are the point.
4. **"Classical" remarks**: I state that `by_cases` on `Pf …` (a Prop with no Decidable instance in the project)
   uses classical logic. True for Mathlib's `by_cases`, but I did not check whether some instance might be found.
5. **`Kripke.SemEntails` universe remark**: I say restricting to universe 0 makes the completeness hypothesis
   weaker. I believe this is right (fewer frames to check), stated carefully.
6. **Line numbers**: my first pass read concatenated files and I converted to per-file numbers by hand; the
   build checks ranges are inside files, not that they point at the right lines. I spot-checked the main ones.

## Things the author might object to
- The "may not compile" flag on line 33, prominently on several pages.
- Calling the Kripke completeness proof "classical / not constructive" in a repo whose Lake package is named
  `constructive`. It is factual (Zorn), but could read as criticism.
- Saying world w2 in `EMFrame` is not needed for the argument.
- The lack of a licence means the site reproduces no code; the author may prefer otherwise.
