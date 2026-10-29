# About this site

## The project

[Zetetic-Dhruv/formal-learning-theory-kernel](https://github.com/Zetetic-Dhruv/formal-learning-theory-kernel),
"Formal(ized) Learning Theory", is a Lean 4 + Mathlib library of statistical and computational learning theory. Its
maintainer is **Dhruv Gupta**, Principal Investigator at **Zetesis Labs** (at ARTPARK, IISc), and the source files
carry "Copyright (c) 2026 Dhruv Gupta" and the Apache 2.0 licence. Dhruv presented the work at Lean NYC in the
lecture [*Formal Learning Theory in Lean 4*](https://lean.nyc/blog/formal-learning-theory) (October 18, 2026).

The README describes how the library was made: a "42-node typed premise", a type architecture written before any
proofs, scoped "human-guided, AI-driven proof search" across three learning paradigms (PAC, online and Gold-style).
It reports the effect of that premise on the search ("87.5% vs 0% first-attempt success on articulated unknowns").
This site does not evaluate those methodological claims. It explains what the Lean states and proves.

The project has live docs and a blueprint PDF, linked from its README, and a CHANGELOG.

### Citing the work

The project's LICENSE file adds a prior-art notice and a **citation request**: if you use, adapt or build on the
work in a publication, software or a derivative work, please cite

> Gupta, D. (2026). *Formal Learning Theory Kernel: Lean4 Formalization of the Fundamental Theorem of Statistical
> Learning.* https://github.com/Zetetic-Dhruv/formal-learning-theory-kernel

```bibtex
@software{gupta2026flt_kernel,
  author = {Gupta, Dhruv},
  title  = {Formal Learning Theory Kernel: {Lean4} Formalization
            of the Fundamental Theorem of Statistical Learning},
  year   = {2026},
  url    = {https://github.com/Zetetic-Dhruv/formal-learning-theory-kernel}
}
```

This explainer quotes short pieces of the source under Apache 2.0 and, honouring that request, cites the work
above. If you build on what you learn here, please cite the original project, not this site.

## What the Lean covers

The compiled library is FLT_Proofs/ (102 files, about 29,900 lines at the pinned commit). Its spine:

1. **Vocabulary.** Concepts, concept classes, three deliberately separate learner types
   ([BatchLearner](#/node/BatchLearner), [OnlineLearner](#/node/OnlineLearner), [GoldLearner](#/node/GoldLearner)),
   and the learning criteria [PACLearnable](#/node/PACLearnable), [OnlineLearnable](#/node/OnlineLearnable) and
   [EXLearnable](#/node/EXLearnable).
2. **Complexity measures.** [VCDim](#/node/VCDim), [GrowthFunction](#/node/GrowthFunction),
   [LittlestoneDim](#/node/LittlestoneDim), [RademacherComplexity](#/node/RademacherComplexity), compression schemes
   and many more (Natarajan, DS, pseudo-, fat-shattering, teaching, eluder and SQ dimensions are *defined* in
   Complexity/Structures.lean, mostly without theorems).
3. **The PAC headline.** The [fundamental theorem](#/node/fundamental_theorem): finite VC dimension ⟺ PAC ⟺
   compression ⟺ vanishing Rademacher complexity ⟺ Sauer–Shelah growth, plus a sample-complexity sandwich.
   The hard direction is [uniform convergence by symmetrization](#/node/vcdim_finite_imp_uc'), about 3,000 lines.
4. **Compression.** [Moran–Yehudayoff](#/node/fundamental_vc_compression_with_info), with an approximate-minimax
   (multiplicative weights) route the README credits as new.
5. **Other paradigms.** The [Littlestone characterization](#/node/littlestone_characterization) of online learning,
   [Gold's theorem](#/node/gold_theorem), and [separations](#/node/online_pac_gold_separation) between the three.
6. **Further results** summarised in grouped nodes: [measurability theory](#/node/exists_measTarget_separation)
   (Choquet capacitability, analytic ⟹ null-measurable, a Borel–analytic separation), [PAC-Bayes](#/node/pac_bayes_finite),
   [advice elimination and meta-learning](#/node/advice_elimination), [mind changes](#/node/mind_change_characterization),
   [no-free-lunch and Occam](#/node/nfl_theorem_infinite), and the newer [IndependentVC development](#/node/vcDim_fundamental_theorem).

## Where to start

Read the [fundamental theorem](#/node/fundamental_theorem), then [PACLearnable](#/node/PACLearnable) and
[MeasurableConceptClass](#/node/MeasurableConceptClass). The [Roadmap](#/roadmap) gives the PAC proof in dependency
order, with links to exact lines. The [Review](#/review) page says, for each headline, how close the Lean statement is
to the textbook one.

## What this site leaves out

- Most of Complexity/IndependentVC/ (about 8,000 lines): scanned and browsable in the source view, summarised in one
  [group node](#/node/vcDim_fundamental_theorem), not explained theorem by theorem.
- The internals of the long proofs: the Moran–Yehudayoff construction (Complexity/Compression.lean lines 805–1105),
  the approximate minimax (PureMath/ApproxMinimax.lean), the symmetrization chain (Complexity/Symmetrization.lean),
  the Choquet capacitability theorem (PureMath/ChoquetCapacity.lean) and the advice-elimination proof.
- `Verification/` (the Comparator challenge statements, which are `sorry` by design) and `world_model/` (an
  experimental tactic and proof-operad layer, not part of the library build), plus the README's premise/ and
  blueprint/ material.
