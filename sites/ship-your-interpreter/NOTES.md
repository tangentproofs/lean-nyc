# NOTES (for the coordinator, not published)

## Time

Started 07:23:54 UTC on 2026-10-29 (from `date`). Finished at 07:56:02 UTC. Wall-clock about 32 minutes (three full builds of about 7 minutes each make up a large share).
One full `engine/build.sh` takes about 7 minutes on this repo: the scan of about 13,100 declarations and
154,000 xref refs is slow. Most of that time is in scan_decls.py's suffix resolution and xref passes.

## What I did / decisions

- Roots are `Vsa`, `VsaIris` and the three library root files. `riscv-lean/` is excluded, as the brief asked.
  The executables (`VsaRun.lean`, `WhileC.lean`, `WhileCheck.lean`) are excluded. They are tools, not theorems.
- Headlines (4): `endToEnd_refinement` (first), `endToEnd_trichotomy`, `while_halts` (the concrete
  traced-boot result), `endToEnd_checked`. I left out type safety, AbsInt, WhileLogic and the compilers, and
  listed them on the About page as not covered.
- 50 nodes. They cover every major lemma on the path to `endToEnd_refinement`, and pages/roadmap.md links
  each one in dependency order (26 numbered steps, sections A–G, plus "what builds on it" and
  "trusted / not proved").
- No Lean code blocks, no verbatim statements, no `lean:` walkthrough fields. Output strings of test programs
  (for example 55/2500/36) are mentioned as data, not as Lean.
- The sentence "the author has said in a talk that the semantics was LLM-written" comes **from the task
  brief**, not from the repository. The repo's `abstractions/ROUND-*.md` files do document AI-agent proof
  work, but they say nothing about who wrote `Semantics.lean`. Please confirm the talk claim, or soften it.
- The licence stays `spdx: null`. The README states no licence either.

## Hardest parts

- Picking a thread through about 175k lines. The real work is in `VsaIris/Interp` and `VsaIris/Vsa` (thousands
  of per-routine proofs). I summarised them at the level of the `TermSupply` and `StuckSupply` records and did
  not explain individual routine proofs.
- Keeping exact line numbers right across about 40 files. All were checked against the source, but see below.

## Least sure (node id + why)

- `VsaIris.Interp.interpSeqT_all`: my paraphrase of `interpSeqT_body` ("machine at the statement loop with the
  C representation of st … continuation expects st' and status") comes from skimming a long, dense
  definition (SeqLoopInterp.lean lines 121–141). The details could be off.
- `VsaIris.Interp.interpRun_total_top`: "returns into main, and follows the exit path to HTIF with code 0" is
  inferred from the postcondition (machine halt with code 0) and from `ra` pointing into main. I did not read
  `interpRun_total`'s epilogue proof.
- `VsaIris.MachWP`: I describe `lagRun` loosely ("step over a stretch of code with a known footprint").
- `VsaIris.Interp.supplies_of` / `VsaIris.SymExec.symRun_swp`: how much of the routine proofs actually go
  through `symRun` and how much through other layers (StepRules, Win, HeapPermit) is my guess from the README
  table. I worded it as "with help from".
- `Vsa.stepOnce` / trust.md: the claim that the axiom-bearing `Lean_RV64D` copy is not imported comes from
  reading lakefiles and imports only. It is not confirmed by a build or `#print axioms`.
- `Vsa.While.ExecSeqCost`: "an upper estimate of bytes allocated" is my reading of the cost semantics' purpose.
  I did not check the units.
- `Vsa.Sim.EndToEnd.endToEnd_trichotomy`: the example "infinite recursion hits the call-depth check or OOM" is
  plausible but not verified against the C.

## Things the author might object to

- Stressing that "end to end" starts at `interp_run`, not at power-on or source text. The README is upfront
  about it, but the site repeats it often.
- The Review page's point that `BigStep` copies C quirks (63-character `<fn name>` truncation, two native
  display forms). This is meant as a neutral observation, but it could read as criticism.
- The LLM-written-semantics remark (see above).
- Calling `NewlibHoles` "a name left over from development". That is a guess at intent.

## Engine notes

- No engine bugs hit. The build is slow on repos this size (about 7 min). It might be worth caching the scan.
