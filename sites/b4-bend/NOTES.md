# NOTES for the coordinator (b4-bend)

## Time

`date` at start: Thu Oct 29 07:59:08 UTC 2026. At the end of writing: Thu Oct 29 08:14 UTC 2026 (by the box's clock).

## What was done

* 24 concept nodes (roots `[]`, like prove2me), each `url` a GitHub line range at 6bf9a57. Headlines: `VMStep`,
  `Laws`, `Fleet16384`, `Mandelbrot`, `LiveShell`. All 24 reachable from the headlines.
* Pages: about, review, trust, roadmap.
* Every line reference in bodies, quizzes, caveats and pages is an explicit markdown link built by `L()` in
  `nodes_src/_common.py` (each node file `exec`s that helper; `_common.py` itself defines `NODES = []`, so the
  engine's loader is happy with it). A scratch script checked all 304 distinct ranges against the files
  (in range, label matches URL); 0 problems.
* No code blocks, no verbatim source lines, no `lean:` fields.
* No Bend, Lean, C or JS was built or run. The only tool run on project files: Python's zlib decoding the
  committed mandelbrot.png (to confirm size, format and grey levels).
* Bend semantics (`law`, `{==}`, `%`, `+x`, `&2`, `Array` depth sizes, index wrap-around, `!`, `@unsafe`,
  `--verdict`) were taken from the Bend guide at github.com/bendlang/bend (guide/GUIDE.md), fetched once. Nothing
  from it is copied beyond short quoted phrases.

## The laws: what I concluded

* LAWS.bend: 94 `law`s; PROOF.bend: 94 matching `def L.<name>`. 78 proofs are just `{==}`; 3 split on fuel; 11 use
  `%Equal.sym(…)` rewrites with a hypothesis; `hop` uses a helper `hop_fusion`; `run_successor` splits on mode.
* Checker: Makefile `check` = `bend PROOF.bend`; `imp/test-bend` (outside imp/bend) runs `make check b4i` before
  the tanco suites; AGENTS.md says to run it before committing. Labelled **CHECKED-BY-BEND (wired in, not re-run)**.
  No run log exists in the repo. `--verdict` (the small kernel) is not used.
* No `@unsafe` in vm/LAWS/PROOF; only the input loops in b4i.bend and live.bend.

## What was hard

* There is no Lean, so the engine's banner/footer text says "The Lean project … The Lean is the ground truth"
  (engine/gen.py lines 29–32; banner at line 22). For this site that reads oddly. Engine change, not mine to make. The ownProject
  banner also uses "his request", which is the engine's wording.
* Bend 2 syntax was new to me; I had to fetch the guide to be sure what `{==}` and `%` mean.
* The Mandelbrot program is a raw byte list. I disassembled it with a throwaway script to describe it.

## Least sure (concrete)

1. **`MandelbrotProgram`**: the disassembly (register roles H I J G F C D A B E, byte ranges 256–405, the float
   constants, the "about 35 instructions per iteration, ~145,000 steps per black tile" estimate). Hand/script
   work, not stated in the repo. The committed PNG is consistent with it (black set, grey = 16·n, stretched
   aspect).
2. **`Memory`**: that `U32^16n` is 2¹⁶ slots and that out-of-array indexes wrap. From the Bend guide ("the number
   after ^ names the depth", "Indexes wrap around"), not from the repo. The review's "address 5,000 lands at 904
   in a live-shell machine" example depends on it.
3. **`Proofs`**: the counts (78/3/11/1/1) are from reading; `%` = rewrite is from the guide.
4. **`Fleet16384` / `FleetTest`**: expected outputs ("machine 100"; "0:256:0 1:258:1 2:256:0 3:256:0") are worked
   out by hand; nothing records them.
5. **`FleetZipper`**: the "affine bookkeeping" reading of `sink`/`discard` is my interpretation.
6. **`LiveShell`**: "the turn rate is not limited" — inferred from the non-blocking poll with no sleep.

## Things the author might object to

* Calling `fleet_isolation` a restatement of `fleet_tick`'s definition, and saying many laws restate the code.
  (I also say why that is the point of a contract file.)
* "No channels" / "swarm means independent copies", contrasted with the Lean swarm.
* The demo machines' smaller memories versus the 65,536-byte bounds checks (review "surprising" #2).
* `db` = `hl` and the stretched Mandelbrot aspect being called out.
* The task brief mentioned "channels" in swarm.bend; there are none in imp/bend at this commit, and the site says so.

## Licence

No LICENSE file (spdx null), unchanged. README credits nothing beyond the repo; `authors` left as Michal Wallace.
