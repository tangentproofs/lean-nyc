# NOTES for the coordinator (lean-lr)

## Time spent
About 2 hours. That covers reading the six headline threads (the repo is ~41,500 lines in 106 files, so I read
the main thread only), fetching iris-lean source to check two facts (no build), writing 44 nodes and 3 pages,
and build iterations.

## Calls I made
- **Headlines (6), one per step of the course's logical-relations story:** `STLC.type_safety`,
  `SystemF.all_identity`, `SystemF.Binary.soundness_wrt_ctx_equiv`, `SystemFMuState.type_safety`,
  `ProgramLogics.ConcurrentLogRel.syn_soundness_not_stuck`, `ProgramLogics.Reloc.refines_sound`.
  `SystemF.termination` and `ProgramLogics.LogRel.syn_soundness_not_stuck` are supporting nodes, not headlines.
- **ReLoC headline kept despite the defect** (see below), because it is the course's Section 8.4.4 result and the
  defect is the most useful thing a reader can learn about this port. It is labelled CONDITIONAL, with the
  condition unsatisfiable, in its title, summary, caveats, the site lead, review.md and trust.md.
- **No licence:** no code blocks, no verbatim statements, no `lean:` walkthrough fields. The README states no
  licence either, so there was nothing to escalate. The underlying course material is MPI-SWS's. I credit the
  course by name and link only, without naming individual course authors, because I didn't verify who they are.
- **Authors:** "Alex Bai", as in site.json. Git authors are ahuoguo / Alexander Bai / Alex Bai.
- **Roots:** all of `LeanLR/` **except** TypeSystems/SystemF/ChurchEncodings.lean (see engine notes). The roots list
  therefore enumerates the SystemF files individually.
- **Fetched iris-lean** (shallow clone into my scratchpad, never built) at the manifest revision 728a171, to check
  HeapLang's pair evaluation order and fork rule, and to grep it for sorry/axiom (none active).

## The finding the author might object to (please double-check)
`ProgramLogics.Reloc.refines_sound` and `refines_sound_open` (ProgramLogics/Reloc/ContextualRefinement.lean
lines 423–449) take the hypothesis "for all K : Ctx, all σ₀, every reachable pool from [fillCtx K e] has length
1". `Ctx` is untyped, and frames carry arbitrary `Exp`. K = [.pairL (fork #())] gives `pair e (fork #())`.
iris-lean's HeapLang has the evaluation contexts `pairL v2` / `pairR e1` (right-to-left, Semantics.lean lines 30–31,
64–65), and `forkS` adds a thread (lines 436–437). The thread-pool `Step` appends forked threads
(ProgramLogic/Language.lean lines 128–130). So the first step of K[e] yields a pool of length 2 for every e and σ₀,
the hypothesis is false, and both theorems are vacuous. The proof itself only uses the hypothesis at the typed K
it is given (line 431), so restricting it to typed contexts looks like an easy fix.
**Remaining doubt:** HeapLang is an `EctxLanguage` instance (iris-lean HeapLang/Instances.lean line 24), so a
primitive step is the generic `ContextStep` (fill K around a BaseStep; cf. Instances.lean line 110). I found no extra
side condition that would block `fork` in that position, but I didn't read the generic `EctxLanguage` file in
full. I'd rate my confidence at about 95%. A 10-line Lean check would settle it.

## Other places I'm least sure of (node id + why)
- **SystemFMuState.type_safety / review.md:** I say the restriction of `ref` to first-order types "comes from
  the course". That is inferred from a comment (Types.lean lines 19–26: "rather than a `Ty` restricted to be
  first-order"). I didn't check the Rocq source.
- **SystemFMuState.semTyped caveat:** the port replaces Rocq's whole-heap invariants with per-location ones. I
  repeat the file's own claim that this suffices and flag it as unchecked.
- **ProgramLogics.LogRel.syn_soundness_not_stuck:** I say the no-fork hypothesis "plausibly holds for every
  typed Chapter 7 program". Typed terms contain no `fork`, and reduction only substitutes values built from the
  program, but I haven't proved it.
- **ProgramLogics.ConcurrentLogRel.semTyped:** the description of μ as "a guarded fixpoint with ▷" comes from
  the `fixpoint` / `later_ne` in typeInterpAux (LogRel.lean lines 170–178), not from reading `muRec`.
- **STLC.type_safety:** I call the name "misleading". The course does call this semantic type safety, and in a
  big-step setting termination implies safety, so the author may consider the name correct.
- **SystemF.termination:** "Girard's method of reducibility candidates, in a simple form" is my framing.

## Things the author might object to
- The ReLoC finding above, which is stated prominently.
- "Misleadingly named" for `STLC.type_safety`.
- Pointing out the unused typing hypotheses in `soundness_wrt_ctx_equiv`. These are faithful to the course
  statement.
- Noting that CORRESPONDENCE.md, cited from many comments and from STRUCTURE.md, is not in the repository.

## Engine notes (not fixed; I did not touch engine/)
1. **Scanner false-positive dependency causing a test failure.** `scan_decls.py` gives `SystemF.TypeWf` a
   meaning-dependency on `SystemF.unit_wf`, a theorem in ChurchEncodings.lean whose name matches the
   *constructor* `unit_wf` of `TypeWf`. That theorem depends back on `TypeWf`, so `test_statement.mjs`
   ("real data: equals the meaning-edge closure… should come before") fails. Workaround: ChurchEncodings.lean
   is excluded from `roots`. Constructor names should probably shadow/terminate resolution, or the test
   should tolerate cycles in real data as it does in the synthetic test.
2. **`mutual` blocks are not scanned.** `STLC.valRel`/`exprRel` and `SystemFMuState.valRel`/`exprRel` are missing
   from decls.json, so they are explained inside the `semTyped` nodes.
3. The remaining ~140 "no explainer yet" warnings are minor helpers (contexts, maps, `Val`, `Binder`, `subst`,
   `Ctx`, the Iris instance classes). They are described in the text of the nodes that use them.
