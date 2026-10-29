# NOTES for the coordinator (gromov)

## Time

By the system clock (`date -u`): started 07:24:28 UTC, finished about 07:39 UTC on 2026-10-29, so **about 15
minutes** of wall-clock time. That seems short for the amount of reading involved, but it is what the clock shows.

## What the repo is, and status

* A complete-looking formalization of the **forward (hard) direction** of Gromov's theorem, by Aaron Hill.
  `FormalConjecturesCheck.gromov_forward` restates it with definitions copied from google-deepmind/formal-conjectures.
* **No live `sorry`.** The three files that mention it are GammaN.lean (a commented-out block, lines 799–842),
  FormalConjecturesCheck.lean line 26 (prose about the reference's `sorry`) and Vendor/Carleson.lean line 20
  ("sorry-free"). No `axiom`, `admit`, `native_decide`, `extern` or `implemented_by`. There are 5 `partial def`s,
  all in the `poly_tendsto` tactic metaprogram.
* Nothing is labelled PARTIAL. `theorem_3_1` is labelled CONDITIONAL by design: the inductive hypothesis is an
  explicit argument, which `main_gromov_theorem` discharges.
* The converse (Bass–Guivarc'h) is not proved. The repo says so, and the site says so prominently.
* Route: Kleiner via Tao's 2010 blog post (per the lean.nyc talk page), with numbering from a thesis the comments call
  "Vikman". I did not find its full title or author first name, so the site just says "a thesis the comments call
  Vikman". No asymptotic cones, Hilbert 5th or Tits.

## Decisions (made without asking)

* **Headlines (6):** gromov_forward, main_gromov_theorem, exists_nontrivial_harmonic, Lipschitz_finite_dimensional,
  compact_lie_virtually_abelian, theorem_3_1. These are Tao's four ingredients plus the two top-level statements.
* **Excluded Gromov/VWrapper.lean from `roots`.** That file defines a global `GeneratesNS.f` (line 91). The scanner
  then reads the bound variable `f` in `Harmonic`'s statement as that global, creating a cycle
  Harmonic → f → Q_R_matrix → LipschitzH → Harmonic. That made `test_statement.mjs` fail ("f should come before
  Harmonic"). Excluding the file only loses its declarations' pages; line links into it still work.
  **Engine bug:** the scanner doesn't respect binders. The same bug produces spurious meaning-deps `C`, `B`, `G'` and
  `G_FG` (warnings only).
* `vikman_errata.txt` (a non-Lean file in Gromov/) is left out of roots. Since its name is lower-case it isn't
  auto-linked; it is mentioned in prose.
* **Engine quirk:** the scanned id for `theorem_3_1.{u}` is `theorem_3_1.` (trailing dot). I used that id as is. Node
  links `#/node/theorem_3_1.` resolve. The fix belongs in the engine (strip `.{u}` universe annotations).
* Licence is null, so there are no Lean blocks, no `lean:` fields, and only paraphrase plus inline identifiers. I also
  rewrote quiz explanations that had quoted Lean fragments.

## Hardest parts

* Getting the proof spine right from a 28k-line repo without building. I relied on `have`/`obtain` skeletons, file
  docstrings and comments.
* The `theorem_3_1` proof (~950 lines). The step boundaries in its walkthrough are approximate.

## Where I am least sure

* **`exists_nontrivial_harmonic`**: the description of Case 1 vs Case 2 (which uses spectral theory and which uses
  sign-pattern test functions) is inferred from the case hypotheses and the first `let`s, not traced fully.
* **`compact_lie_virtually_abelian`**: the claim that the "non-scalar central element" case splits into eigenspaces
  and inducts is inferred from the `nontrivial_centrer_implies_virtual` hypothesis name and the Prod.Lex well-founded
  goals. I did not trace the induction measure.
* **`exists_theorem_3_1_input` / `rho_g_case_finite`**: I describe the image of λ as a f.g. torsion-free abelian group
  mapping onto ℤ, which is the classical argument. The Lean specifics after line 131 were skimmed.
* **`three_two_kernel_poly_growth`**: the "intuition" paragraph is the classical argument, not the Lean proof's.
* **`theorem_3_1.` walkthrough line ranges** (especially 677–989) are coarse.
* **`int_matrix_poly_growth_eigenvalue`**: I paraphrased its long counting hypothesis loosely. Also, the claim that
  eigenvalues inside the unit circle are handled via A⁻¹ is my assumption about how the proof goes.
* **`theorem_3_23`**: I summarized it as "for every finite-dimensional, non-trivial, even-dimensional V". Those are the
  V_Wrapper fields, but I didn't check why evenness is needed.

## Things the author might object to

* Calling the compact step "Jordan–Zassenhaus-style" (Tao's wording is loose too). Also, the site describes
  `compact_lie_virtually_abelian` as narrower than "compact Lie groups", while the name says compact Lie.
* Mentioning the "edited by Aristotle" headers and the `.claude/` and `.mcp.json` tooling in Trust. It is factual and
  hedged, but the author might prefer it unmentioned.
* "Vikman" is never given a full citation. The author would know the right reference.
* The sizeNote counts the vendored Carleson code and the tactic files in the 28.4k lines.
* The README is a bare title, so `authors`/`members` stay "Aaron Hill" (from git history and the talk). The repo has no
  licence file, and nothing in the README states one.
