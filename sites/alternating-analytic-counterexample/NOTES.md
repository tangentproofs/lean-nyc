# NOTES for the coordinator (not published)

## Time spent

About 1.5 hours in one session. Roughly a third went on reading the source, a third on writing, and a third on
checking line references and fixing schema errors (quiz length, summary and title length).

## Decisions made without asking

- **Roots:** `["AltCounter", "Solution.lean"]`. **Challenge.lean is left out on purpose.** It declares the same two
  theorem names as Solution.lean, with `sorry`, and the scanner kept the Challenge.lean copies, so the headline pages
  pointed at the sorry'd statements. With it left out, the headlines resolve to the proved copies in Solution.lean.
  trust.md and about.md say so and still count Challenge.lean's two `sorry`s.
- **Headlines (5):** the two Solution.lean comparator theorems, plus `AltCounter.not_analyticAt_Q`,
  `AltCounter.core_false` and `AltCounter.exists_field`. I did not make `false_of_general_contDiff_omega` and
  `false_of_charTwo_banach_contDiff_omega` (Final.lean) separate nodes, because they are the same statements as the
  Solution.lean ones. They are described inside those nodes.
- **Labels:** `not_analyticAt_Q` and `core_false` are labelled CONDITIONAL (on `TailProperty`), with a note that the
  condition is discharged. The Solution.lean headlines are labelled unconditional, with no sorry.
- **Walkthrough `lean:` snippets** are only used where the snippet is verbatim inside the node's own line range. The
  engine warns, and drops the link, otherwise. For the Solution.lean headlines that leaves only step 1 with code; the
  other steps cite Final.lean lines in text.
- **Authors:** left as "Jack McCarthy" (README, CITATION.cff and formalization.yaml agree). about.md quotes the paper's
  footnote and summarises formalization.yaml's statement that the mathematics and the Lean were produced by AI
  (Claude, ChatGPT, AutoformBot) under the author's direction and not human-reviewed. That is the upstream's own
  disclosure, so it seemed right to repeat it. The coordinator may want to tone it down.
- 38 nodes, a bit above the suggested 8–25, because the statement set is large (Q, F, FSub, Wfun, W₀, mulL,
  IsBdd4, TailProperty, NSC, HasEmptyNestedBalls, IsGoodModel, plus PM, pfTerm, bal, cubePt, blockVec, Stage).

## Engine notes

- Duplicate declaration names across files (Challenge.lean and Solution.lean) are silently deduplicated in favour of
  the first file scanned. It might be worth a warning.
- Bound variables named `F` in the headline hypotheses create false meaning-dependencies on `AltCounter.F`.
  trust.md mentions this.

## Where I am least sure

- **`AltCounter.nsc_of_hasEmptyNestedBalls`:** the four-bullet proof outline is reconstructed from section comments,
  and I did not trace how the diagonal vector y is built or exactly what "φ y lies in every ball" means (it may be a
  scaled version of φ y). Flagged in a caveat.
- **`AltCounter.tailProperty_of_NSC`:** the gliding-hump and induction-on-arity summary (Claims 1 and 2) follows the
  docstrings. Roughly 1,000 lines were skimmed, not traced.
- **`AltCounter.norm_det_le_of_close_to_lowrank`:** I explain it as "terms with more than r columns from the rank-r
  part vanish". That matches the statement and is the natural proof, but I did not check that the Lean argues it this
  way.
- **`AltCounter.coeff_bal_prod_matching` / `coeff_bal_of_swap_invariant`:** the "monomials pair up under swap, only
  the balanced one is fixed" explanation is my own reconstruction. I think it is right, but I did not trace the proof.
- **`AltCounter.exists_block_point`:** I say the swap and diagonal identities follow "by polarisation" from alternation
  and the diagonal formula. `char2_key` is consistent with that, but I did not expand it by hand.
- **`AltCounter.TailProperty` / `AltCounter.NSC`:** the remarks about ℝ (Banach limits) and ℚ_p (spherically
  complete, so the tail property fails) are standard background I added. They are not in the Lean. The Defs.lean
  docstring's parenthetical "(there (ℓ^∞)' = c₀)" I did not repeat.

## Things the author might object to

- Repeating the AI-authorship and "not human-reviewed" statements from formalization.yaml in about.md. They are
  accurate quotes and summaries of upstream, but prominent.
- Calling `not_analyticAt_Q` and `core_false` "CONDITIONAL". That is accurate for those declarations, but the author
  might prefer emphasis on the unconditional headlines. Both nodes say the condition is discharged.
- The review's remark that the hypothesis quantifies over universe 0 only. Upstream lists this itself as divergence
  (1), so it should be uncontroversial.
- Leaving Challenge.lean out of the scanned roots, so its statements have no declaration pages.
