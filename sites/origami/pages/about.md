# About this site

## The project

[celioboulay/origami-formalization](https://github.com/celioboulay/origami-formalization) is, in its README's words,
"a Lean formalization of Huzita–Hatori origami constructions, accompanied by a web interface for composing fold
operations and checking the resulting Lean trace". The README names no authors. The git history shows commits by
**Celio Boulay** (who started the repository), **Thomas Moulin**, **Alexander Chai**, **wurtylex** (who wrote most of
the current Huzita library), and an "OrigamiClub" account. This site credits them all; it is not affiliated with them.

### The mathematics in one paragraph

The **Huzita–Hatori axioms** list the seven ways a single straight fold can be defined by lining up given points and
lines: fold through two points, fold one point onto another, fold one line onto another, and so on. The sixth one
(place two points onto two lines at once) amounts to solving a cubic equation, which is why origami can trisect
angles and double cubes while compass and straightedge cannot. **Haga's theorem** is a practical consequence:
folding the corner of a square onto the midpoint of the opposite edge makes a crease whose folded edge marks a third.

## What the Lean covers

Everything this site explains lives in `Origami/lightweight_definitions/` (about 1,250 lines, 9 files), imported by
Origami.lean:

- **The model** (Structures.lean, Normalisation.lean): [points](#/node/Point) with real coordinates;
  [lines](#/node/Line) stored as *ax + by + c = 0* in a canonical form so that each geometric line has exactly one
  representative; [folds](#/node/Fold), which are just crease lines; and the two reflection maps
  [f_places_p](#/node/f_places_p) (points) and [f_places_l](#/node/f_places_l) (lines).
- **Basic geometry** (Relations.lean, Reflection.lean): parallel and perpendicular lines, squared distances, and
  the facts that reflections are involutions, preserve distances and fix exactly the crease.
- **The seven axioms as theorems** (Huzita_axioms.lean, with CubicRoot.lean): [1](#/node/huzita_1),
  [2](#/node/huzita_2), [3](#/node/huzita_3), [4](#/node/huzita_4), [5](#/node/huzita_5), [6](#/node/huzita_6) and
  [7](#/node/huzita_7). Axioms 1, 2, 4 and 7 come with uniqueness. Axiom 6 uses a lemma that
  [every real cubic has a root](#/node/exists_hom_cubic_root).
- **Sharpness** (Sharpness.lean): exact conditions for [axiom 5](#/node/huzita_5_iff) and
  [axiom 7](#/node/huzita_7_iff), and counterexamples showing where uniqueness fails or a hypothesis cannot be dropped.
- **Haga's theorem** (Haga.lean): [the 1/3 fold](#/node/haga_first_theorem), its
  [generalisation](#/node/haga_gen_equation) to any point on the top edge, and a
  [version tied to the web tool's output](#/node/haga_result).

Everything happens in the infinite real plane. There is no sheet of paper, no boundary and no layering, so the
theorems are about lines and reflections, not about whether a fold is physically possible on a finite square.

## The web tool

Besides the Lean, the repository contains a small toolchain, which this site describes but does not explain in
detail:

- `origami-sim/` (a git submodule, not checked out for this site) is a web UI with a Rust/WASM core. It shows a crease
  pattern (a unit square by default, or an uploaded `.fold` file) on which you pick points and creases.
- `origami_api.py` keeps a stack of Huzita axiom calls made in the UI and writes a Lean file: picked points and
  lines become opaque Lean `axiom`s, each call's side condition (for example "the two points differ") is postulated as
  another `axiom`, and the construction is a chain of uses of the proved `huzita_N` theorems.
- `origami_server.py` connects the UI to the API and compiles the generated file with `lake env lean`, reporting back
  whether it type-checks.

The top of Haga.lean is such a generated file, kept as produced ([haga_construction](#/node/haga_construction)); the
rest of that file proves something about it.

## What this site leaves out

- `Origami/paper_folding/` (about 175 lines) is an earlier experiment by Celio Boulay modelling folded paper as
  triangular faces with a stacking order, with one checked folding step. It is not imported by Origami.lean and uses
  a different, conflicting `Fold` type, so it is not scanned or explained here.
- `Origami/AngleTrisection` is a submodule pointing to a separate repository (celioboulay/origami-lib); it is not part
  of the pinned tree and is not covered. The git history also mentions earlier work on Maekawa's theorem that is no
  longer in this tree.
- Many small lemmas (symmetry of relations, coordinate formulas) are linked from the nodes but have no page of their
  own.

## Where to start

Read [Line](#/node/Line) first: the canonical form is what makes "exactly one fold" a meaningful statement. Then
[Axiom 2](#/node/huzita_2), [Axiom 6](#/node/huzita_6), and [Haga's first theorem](#/node/haga_first_theorem).
