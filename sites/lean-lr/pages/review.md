# Review: do the statements say what they claim?

Nothing below was checked by building Lean. It all comes from reading the source at the pinned commit.

## STLC.type_safety: faithful, but misnamed

- **Name:** "type safety".
- **Statement:** a closed well-typed term *terminates*: it evaluates (big-step) to a value.
- **Verdict:** this is a **normalisation** theorem, stronger than the usual "never gets stuck". The usual
  statement is proved separately, by progress and preservation, as [STLC.typed_safety](#/node/STLC.typed_safety).
  The name follows the course, which calls the semantic route "semantic type safety". A reader expecting a
  progress-style statement should know that this one says more.
- Minor: the STLC typing rules have no rule for anonymous λs (TypeSystems/Stlc/Types.lean lines 54–74), so such
  terms are untypable. That narrows the scope a little and is harmless.

## SystemF.all_identity and not_every_type_inhabited: faithful

These are the two classic free theorems. Their statements match their names. `all_identity` says the identity
behaviour holds for every **closed value** argument, typed or not, after one type application and one
application. It does not say *e* is syntactically Λα. λx. x.

## SystemF.termination: faithful

Every closed well-typed System F program evaluates to a value (call-by-value, big-step). This is Girard's
normalisation theorem in a simple form.

## SystemF.Binary.soundness_wrt_ctx_equiv: faithful, with one oddity

- **Statement:** logically related open terms are contextually equivalent, observing the integer produced by
  closed int-typed program contexts.
- **Oddity:** the two typing hypotheses are unused, since the proof only needs the relatedness hypothesis
  (TypeSystems/SystemF/BinaryLogRel.lean lines 1244–1247). Harmless: the statement just has extra assumptions.
- The theorem does not prove any particular pair equivalent. That needs a separate relatedness proof.

## SystemFMuState.type_safety: faithful for its type system

- **Statement:** a closed program typed by the *logical relation's* type system, run from the **empty heap**,
  ends only at values, whenever it stops.
- **Scope:** in this type system references hold only **first-order** types (Types.lean lines 19–26 and 48).
  The Types.lean comment implies that the restriction itself comes from the course, where `ref` is limited to
  first-order types by a predicate, and that only the encoding (a separate type of first-order types) is new. Full references are treated syntactically in `SystemFMuState.Syn` and semantically only in
  the Iris chapters.
- The port also changes the heap invariants: Rocq allows arbitrary predicates on whole heaps, the port uses one
  predicate per location (LogRel.lean lines 34–40). The file says this suffices for first-order references.
  This site has not checked that claim. It affects the expressiveness of the model, not the truth of the headline.

## ConcurrentLogRel.syn_soundness_not_stuck: faithful, unconditional

The full statement: from any state, under any interleaving, no thread of a well-typed program (System F + μ +
higher-order references + fork + CmpXchg) is ever stuck. No extra hypotheses. The final step is iris-lean's
`heap_adequacy`. Its correctness is part of the trusted base and was not checked here.

## LogRel.syn_soundness_not_stuck (Chapter 7): CONDITIONAL

The sequential chapter's safety theorem assumes that the run never forks (ProgramLogics/LogRel/Adequacy.lean
line 50). That can hold, and plausibly does hold for every typed Chapter 7 program, since the Chapter 7 type system
has no fork rule. But the repository doesn't prove it, so the theorem is **conditional** as stated. The source says
the hypothesis is an artefact of building the course's sequential weakest precondition on iris-lean
(ProgramLogics/SeqAdequacy.lean lines 18–21).

## Reloc.refines_sound and refines_sound_open: CONDITIONAL, on a condition that is never met

This is the most important finding on the site.

- **Claim:** a ReLoC refinement proof implies contextual refinement (course Section 8.4.4).
- **Statement:** as claimed, **plus** a hypothesis that, for **every** program context *K* (typed or not) and every
  initial state, every run of *K*[*e*] keeps exactly one thread (ProgramLogics/Reloc/ContextualRefinement.lean lines 436–437).
- **Problem:** program contexts can contain any HeapLang expression, including `fork`. The context that pairs the
  hole with "fork the unit value" forks on its very first step, because HeapLang evaluates pairs right to left
  (iris-lean's pair evaluation contexts and fork rule, at the pinned iris-lean revision). So the hypothesis fails for
  every *e*, and the theorem is **vacuously true**.
- **Likely fix:** quantify the no-fork hypothesis over *typed* contexts only. That is all the proof uses
  (line 431), and typed contexts cannot contain fork.
- **Not affected:** `log_related_under_typed_ctx` (the precongruence) and `logrel_adequate`, `logrel_typesafety`,
  `F_mu_ref_typesafety`, whose no-fork hypothesis concerns a single program.

We are confident in this reading, but it is still a reading, not a Lean check. A Lean proof that the hypothesis is
false would settle it, and we did not write one, because this site does not build Lean.

## Course coverage

STRUCTURE.md says every Rocq file has a Lean counterpart, with some declarations deliberately dropped and three
"open by design", as listed in a CORRESPONDENCE.md. **That file is not in the repository** at the pinned commit,
although several comments cite its sections. The text search finds no `sorry`, so "open by design" presumably
means "not ported", not "stated and left unproved".
