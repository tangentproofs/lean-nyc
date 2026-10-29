# NOTES for the coordinator: cubing (rdavison/cubing @ ad5bdd0)

Not published. Written by the Claude session that wrote this explainer.

## Time spent
About 10 minutes of wall-clock time (04:55–05:05 UTC on 2026-10-29), most of it reading the seven
library files and checking line ranges.

## What I produced
- `site.json`: filled in. Headlines: `reachable_eq_valid`, `card_reachable`, `card_valid`,
  `toStickers_injective` and `colors_move_mul`. The last two are the ones the upstream axiom audit pins
  alongside the counting theorems.
- 35 nodes in `nodes_src/` (a_model, b_invariants, c_generate, d_solvable, e_facelets, f_details). Every
  headline has a walkthrough with line references.
- `pages/about.md`, `pages/review.md`, `pages/trust.md`.
- The licence is none, so there are no Lean code blocks, no verbatim statements and no `lean:` fields. I do quote
  standard cubing move sequences such as "U D2 L2", "R U" and "R U R' U'". These are public cubing notation, not
  Lean source, but the coordinator may want to check that call.

## Judgement calls
- **Authors:** the README names no author; I kept the coordinator's `Richard Davison` (matches git author).
- **Roots:** `Cubing` only. I left out `book/` (Verso rendering, no maths), `CubingImpl` (a stub),
  `CubingAudit`/`CubingResults` (audit/empty; referenced by line in prose) and `Main.lean`. This is explained on the About page.
- `ns` = `Cubing.Cube3x3.`.
- Some minor statement-set dependencies (`CornerGroup`, `EdgeGroup`, `cornerPerm`, `edgePerm`, `edgeFlip`,
  `cornerFace`, `edgeFace`, `Vec.*`, `Move`, `Move.toCube`, `cornerSetUps`, `Facelet.pull`, `OPerm.total`,
  `OPerm.twists`) are explained inside group nodes rather than in their own, so 29 "no explainer"
  warnings remain. All are minor.

## Engine issue (worked around, not fixed)
- AUTHORING.md says files in `nodes_src/` that start with `_` are helpers and are skipped, but
  `engine/tools/write_nodes.py` loads **every** `.py` and reads `m.NODES`, so a helper without `NODES` crashes
  the build (`AttributeError: module '_extra' has no attribute 'NODES'`). Workaround: `_extra.py` defines an empty
  `NODES = []`. The fix would be `if not f.endswith(".py") or f.startswith("_"): continue`.

## Where I am least sure
- **`OPerm` node, twist convention.** The docstring says the piece in slot a goes to σ(a) and gains twist
  o(σ(a)). My paraphrase of `mul_left_apply` ("the right factor's twist carried along by the left factor's
  permutation") is loose; the exact index bookkeeping uses σ⁻¹.
- **`colors` node.** My "look back" description (inverse permutation, subtract the twist) is from reading
  Cube3x3/Facelets.lean lines 207–210. I did not evaluate it.
- **`Face.turnVec` node.** "Sends front to left for U" is my own hand computation of the formula. It agrees with
  the U edge table (UF→UL), but I didn't run anything.
- **`twoCornerTwist` node table.** The 26-move count for the corner-twist sequence is my count of the tokens.
  "Twists UBR forward and URF back" follows the docstring and `pairTwist UBR URF` (+1 at the first slot).
- **`pull_move` / `colors_move_mul` caveats.** I claim the check depends on the hand-written sticker tables as
  well as the move tables. I believe this is right (`Facelet.cubie`/`normal` go through
  `cornerStickers`/`cornerFace`), but how strong a check it is, is my judgement.
- **`OPerm.SetUp.le` walkthrough.** The line splits (176–179, 180–184, 185–187) are approximate groupings
  of the proof's `have` blocks.
- **"Face.layer has 21 facelets"** is my count, not stated upstream.

## Things the author might object to
- I call `card_valid` a headline although on its own it is only about the kernel. The node says so explicitly.
- The review notes that "positive moves only" reachability is argued in prose rather than proved as a lemma, and
  that the order checks are "divides" checks. Both are accurate, but they could read as nitpicks.
- The About page says the README's solving-methods plan is not yet in the repo at this commit. That is true at
  ad5bdd0, but it may change soon.
- I credit "Kociemba's tables" for the move tables, from the upstream CLAUDE.md. The library prose itself just
  says "the standard computer-cubing tables".
