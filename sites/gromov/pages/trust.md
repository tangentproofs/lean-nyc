# Trust: what was and wasn't checked

## Not built

**The Lean was not built for this site.** No `lake`, `lean` or `elan` was run. When this site says something "is
proved", it only means the source contains what looks like a complete proof and a text search finds no live `sorry`
in the project. It does not mean Lean's kernel accepted it.

The project asks Lean to report on itself. Gromov/Gromov.lean lines 1026–1027 run `#print sorries` and
`#print axioms` on main_gromov_theorem, and there are 64 such `#print` commands across the project. Their output was
**not seen** for this site.

## Gaps, axioms and escape hatches

A text search of all 75 `.lean` files at the pinned commit finds:

| What | Count | Where |
|---|---|---|
| `sorry` in live code | **0** | |
| `sorry` in comments | 7 | Gromov/Unipotent/GammaN.lean lines 799–842, a commented-out block (every line starts with `--`) |
| the word "sorry" in prose | 2 | Gromov/FormalConjecturesCheck.lean line 26 (on the reference repository's `sorry`) and Gromov/Vendor/Carleson.lean line 20 ("sorry-free") |
| `admit` | 0 | |
| `axiom` declarations | 0 | the word appears only in `#print axioms` commands |
| `native_decide` | 0 | |
| `implemented_by` / `extern` / `opaque` | 0 | |
| `partial def` | 5 | Gromov/TendstoTactic.lean lines 93–362: the `poly_tendsto` tactic's metaprograms. A tactic only builds proof terms, which the kernel still checks, so this does not affect soundness. |
| `set_option maxHeartbeats` | 66 | throughout: raised time limits, not a soundness issue |

The three files the task brief flagged as mentioning `sorry` are the three rows above: GammaN.lean,
FormalConjecturesCheck.lean and Vendor/Carleson.lean. None of them contains a live gap.

So, as far as text inspection can tell, the headline theorems are **complete**. Nothing is labelled PARTIAL. The only
CONDITIONAL statement is the inductive step [theorem_3_1](#/node/theorem_3_1.), whose extra hypothesis is discharged
by [main_gromov_theorem](#/node/main_gromov_theorem).

## Other provenance notes

* **Vendored code.** Gromov/Vendor/ (about 830 lines) is code ported from the Carleson project, released under
  Apache-2.0 according to its header. It supplies Young's convolution inequality.
* **AI-assisted files.** Two files, Gromov/NilpotentFinite.lean and
  Gromov/ToMathlib/Analysis/Matrix/StarNormalEigen.lean, carry a header saying they were "edited by Aristotle". The
  repository also contains `.claude/` and `.mcp.json` configuration for Lean proof tooling. This site does not know how
  much of the development was AI-assisted, and makes no claim about it.
* **Toolchain.** Lean `v4.33.0-rc2` with a pinned Mathlib revision (lakefile.toml).

## Declarations scanned from text

The declaration list, statements and dependency links come from a text scan of the source
(`extracted: false`), not from Lean's elaborator. Known limitations on this project:

* the scanner treats bound variables with the same name as a global declaration as references to it (single letters
  such as `f`, `C`, `B`, `G'`). So some "meaning dependency" links are spurious;
* to avoid a false dependency cycle through a declaration named `f`, **Gromov/VWrapper.lean is excluded from the
  scan**. Its declarations have no pages, but line references into it still link to GitHub;
* `theorem_3_1` is listed with a trailing dot (`theorem_3_1.`) because of its universe annotation.

## Explanations

All explanations, summaries, quizzes and the roadmap were **written by an AI** (Claude) from reading the source, and
have **not been reviewed** by the author. The large proofs were read for structure (`have`/`obtain` steps, case
splits, comments), not line by line. Nodes that rely on that kind of skim say so in their caveats.
