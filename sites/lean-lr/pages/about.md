# About this site

## The project

[ahuoguo/lean-lr](https://github.com/ahuoguo/lean-lr) is **Alex Bai**'s port to Lean 4 of the logical-relations
development of the MPI-SWS [Semantics course](https://plv.mpi-sws.org/semantics-course/). In the README's words,
it is "Porting the logical relations in MPI-SWS's Semantics course to Lean". The original development is in Rocq
and belongs to the course. This port follows it chapter by chapter. The repository's STRUCTURE.md maps each section
of the lecture notes to a Lean file. The commits run from December 2025 to September 2026. The port targets
Lean 4.32 and builds the program-logic chapters on [iris-lean](https://github.com/leanprover-community/iris-lean).

All the mathematics (the languages, the relations, the theorems) comes from the course. What the port adds is the
Lean formalisation, a tactic layer for the sequential weakest precondition, and the changes needed to run on
iris-lean instead of the course's fork of Rocq Iris. Comments in the files record those changes.

## What the Lean covers

About 41,500 lines in 106 files, in two halves:

1. **Type systems** (TypeSystems/, course Chapters 1–4). Each language has its syntax, operational semantics,
   typing rules, a syntactic safety proof, and one or more logical relations:
   - the simply typed λ-calculus, and an extended version with products and sums;
   - System F, with a unary relation (termination, free theorems) and a binary relation (contextual equivalence);
   - System F with recursive types (step-indexed relation, Z combinator);
   - System F with recursive types and first-order references (step- and world-indexed relation, MutBit).
2. **Program logics** (ProgramLogics/, course Chapters 5–10), built on iris-lean: Hoare logic, the Iris Proof
   Mode, persistency and later, a semantic type system in Iris (Chapter 7), ghost state and resource algebras
   (Chapter 8), the **ReLoC** binary relation for refinement (Chapter 8.4), and concurrency with a concurrent
   logical relation (Chapter 10). Exercise files from the course are included, with solutions.

## The thread this site follows

The site explains six headline results, one for each step up in power of the logical-relations method:

| Headline | What it shows | Status |
|---|---|---|
| [STLC.type_safety](#/node/STLC.type_safety) | closed well-typed STLC terms **terminate** (despite the name) | complete-looking proof |
| [SystemF.all_identity](#/node/SystemF.all_identity) | a free theorem: ∀α. α → α is the identity | complete-looking proof |
| [SystemF.Binary.soundness_wrt_ctx_equiv](#/node/SystemF.Binary.soundness_wrt_ctx_equiv) | related programs are contextually equivalent | complete-looking proof |
| [SystemFMuState.type_safety](#/node/SystemFMuState.type_safety) | safety with recursive types and first-order state | complete-looking proof |
| [ConcurrentLogRel.syn_soundness_not_stuck](#/node/ProgramLogics.ConcurrentLogRel.syn_soundness_not_stuck) | no stuck thread in a well-typed concurrent program | complete-looking proof (relies on iris-lean) |
| [Reloc.refines_sound](#/node/ProgramLogics.Reloc.refines_sound) | ReLoC refinement ⇒ contextual refinement | **CONDITIONAL**, on a hypothesis that cannot hold |

## Where to start

Read the STLC nodes first: [semTyped](#/node/STLC.semTyped), [fundamental](#/node/STLC.fundamental) and
[type_safety](#/node/STLC.type_safety). Every later chapter has the same three-part shape. Then go up the table.

## What this site leaves out

Most of the repository: the extended STLC, call-by-name, System F's Church encodings and existential-invariant
examples, the whole of `SystemFMu` (whose safety theorem `SystemFMu.type_safety` is the stepping stone between
System F and the state chapter), the substitution and evaluation-context infrastructure (the `ParallelSubst`,
`Pure` and `Execution` files, several thousand lines), Chapters 5–6 and 8 of the program logics (Hoare logic, the
Iris Proof Mode, ghost theories, resource algebras), the ADT proofs of Chapter 10 (counter, channel, symbol
generator) and `Arc.lean`, and the two OPLSS lecture files.

The file TypeSystems/SystemF/ChurchEncodings.lean is also **not scanned** by this site. That is a workaround for
a name clash in the site's text scanner, not a judgement on the file.

The repository has **no licence file**, so this site quotes none of its code. Everything here is a paraphrase,
with links to the exact lines on GitHub.
