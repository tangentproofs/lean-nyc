NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

NOTBUILT = "Not built for this site: “proved” means the file has a complete-looking proof (no sorry), not that the kernel was observed to accept it."

# ---------------- Configuration 1 ----------------

node("Config1.verdict_compatible",
 "Headline: two Preserve vendors agree",
 "Vendor A (canonicalize) and vendor B (flush model pinned to Preserve) give identical bits on all 65,536 inputs. The proof is replayed from a stored LRAT certificate, but that certificate is only 10 bytes, so the solver's share of the work is trivial here.",
 r"""## Plain English

**Theorem (`verdict_compatible`, Config1.lean lines 58–66).** `compatStmt vendorA vendorB_preserve`.

Unfolded: for every 16-bit input `x` and every admissible flag pair, vendor A's output
[canonOp](#/node/Core.Ops.canonOp) `x` equals vendor B's `vendorOp false x`. Both sides are the identity in
disguise: canonOp recombines fields that cover all 16 bits, and `vendorOp false` never takes the flush branch.

This is the first of the four Configuration-1 scenarios: **compatible**,
[divergent](#/node/Config1.verdict_divergent), [silence](#/node/Config1.verdict_silence) and
[domain-restricted](#/node/Config1.verdict_domain_restricted). They share one statement builder,
[compatStmtOn](#/node/Core.Statement.compatStmtOn), and differ only in which [fixtures](#/node/Core.Fixtures.vendorA)
go in.

**How it is checked.** The definitions are unfolded into a pure `BitVec 16` equation, and `bv_check` replays
`certs/verdict_compatible.lrat`. That file is 10 bytes (`3 0 1 2 0`), a one-step refutation. In other words,
after `bv_decide`'s preprocessing almost nothing is left for the SAT solver. The scenario does exercise the
certificate *mechanism*, but not a hard SAT problem. The hard one is [mul_true](#/node/Arith.mul_true).
""",
 [q("Which inputs does this verdict cover?", ["All 2^16 binary16 bit patterns", "Only normal numbers", "Only the witness 0x0001"], 0,
    "`compatStmt` uses `fullDomain` (Core/Statement.lean line 68)."),
  q("Why does vendor B agree with vendor A here?", ["B is pinned to Preserve, so it never flushes", "B ignores subnormals"], 0,
    "`admits (Pinned Preserve) flushB` forces flushB = false, and `vendorOp false` is the identity."),
  q("Would the verdict still hold if B were pinned to FlushToZero?", ["Yes", "No"], 1,
    "That is exactly verdict_divergent, which is refuted on 0x0001."),
  q("Does this theorem say anything about rounding or arithmetic?", ["Yes", "No"], 1,
    "The operations are rounding-free handoffs (Core/Ops.lean lines 24–27).")],
 caveats=[NOTBUILT,
          "The 10-byte certificate means the SAT step is trivial for this goal. The README's “SAT-backed” description is accurate, but the solver is barely exercised.",
          "Vendor A's own commitment plays no role, because canonOp ignores the flag."],
 widgets=[{"type": "walkthrough", "title": "How the proof goes (Config1.lean, lines 61-66)",
           "config": {"steps": [
               {"text": "Unfold the builder, the admissibility predicate, the op lookup, the mode flag, the full domain and the two fixtures, leaving a statement about flags and a 16-bit x.", "link": "Core.Statement.compatStmtOn",
                "lean": "  simp only [compatStmt, compatStmtOn, admits, opOf, modeFlag, fullDomain, vendorA, vendorB_preserve]"},
               {"text": "Introduce the flags, the input and the hypotheses. hB says flushB = false (B is pinned to Preserve).",
                "lean": "  intro flushA flushB x _ _ hB"},
               {"text": "Substitute flushB := false everywhere.", "lean": "  subst hB"},
               {"text": "Unfold the operations and masks so the goal is a pure BitVec 16 equation between canonOp x and vendorOp false x.", "link": "Core.Ops.canonOp",
                "lean": "  simp only [canonOp, vendorOp, isSubnormal, signedZero, signMask, expMask, mantMask]"},
               {"text": "Replay the stored LRAT certificate with the verified checker, with no solver.",
                "lean": "  bv_check (config := { binaryProofs := false }) \"../certs/verdict_compatible.lrat\""}]}}])


node("Config1.canon_diverges_under_flush",
 "The ground divergence fact",
 "On the input 0x0001, canonOp returns 0x0001 but the flushing vendor returns 0x0000. All the negative floating-point verdicts reduce to this one concrete inequality.",
 r"""## Plain English

**Theorem (`canon_diverges_under_flush`, Config1.lean lines 70–76).**
`canonOp w_subnormal ≠ vendorOp (modeFlag .FlushToZero) w_subnormal`.

With [w_subnormal](#/node/Core.Witnesses.w_subnormal) = `0x0001` this is `0x0001 ≠ 0x0000`. The proof unfolds
everything and calls `bv_decide`, which settles a closed (variable-free) goal by normalization. No certificate
is stored and, according to the project's measurements, no native axiom is used (TRUST.md).

It is used by [verdict_divergent](#/node/Config1.verdict_divergent), [verdict_silence](#/node/Config1.verdict_silence)
and the [DivergenceWitness](#/node/DivergenceWitness) bundle.
""",
 [q("Does this statement contain any universally quantified variable?", ["Yes", "No"], 1, "Both sides are evaluated at the fixed input 0x0001."),
  q("What are the two sides?", ["0x0001 and 0x0000", "0x0001 and 0x8000"], 0, "canonOp keeps the pattern; flush gives +0."),
  q("Does this proof need a stored certificate?", ["Yes", "No"], 1, "It is a ground goal closed by bv_decide's normalization (Config1.lean line 76); certs/ has no file for it.")],
 caveats=[NOTBUILT])


node("Config1.verdict_divergent",
 "Preserve vs flush-to-zero disagree",
 "If vendor B pins FlushToZero, the specs are incompatible: plugging the pinned flags and the witness 0x0001 into the claimed agreement contradicts the ground divergence fact.",
 r"""## Plain English

**Theorem (`verdict_divergent`, Config1.lean lines 80–85).** `¬ compatStmt vendorA vendorB_flush`.

Proof idea: suppose `h : compatStmt vendorA vendorB_flush`. Apply it with `flushA = modeFlag Preserve`,
`flushB = modeFlag FlushToZero` and `x = w_subnormal`. The three side conditions (in the full domain, flag
admitted by A, flag admitted by B) all hold by `rfl`. That gives `canonOp 0x0001 = vendorOp true 0x0001`,
which [canon_diverges_under_flush](#/node/Config1.canon_diverges_under_flush) refutes.

The source explains why it is done this way (Config1.lean lines 45–48): `bv_decide` cannot decide a negated
universal or an existential directly, so the counterexample is fed in by hand. It was found by reasoning, not by
the solver; the solver-found counterexample is [mul_false](#/node/Arith.mul_false).
""",
 [q("What does this theorem rule out?", ["That every Preserve/FlushToZero implementation pair agrees on all inputs", "That they agree on any input"], 0,
    "It is the negation of a universal: at least one input disagrees. On normal inputs they do agree."),
  q("Which input is the counterexample?", ["0x0001", "0x8000", "0x3C00"], 0, "w_subnormal (Config1.lean line 85)."),
  q("Why is the counterexample supplied explicitly?", ["bv_decide does not decide ¬∀ or ∃ goals directly", "Lean forbids negated statements"], 0, "Config1.lean lines 45–48.")],
 caveats=[NOTBUILT])


node("Config1.verdict_silence",
 "Headline: a silent spec is incompatible",
 "If vendor B's spec says nothing about subnormals, it is not compatible with vendor A, because a flush-to-zero implementation is allowed by silence and differs on 0x0001. Saying nothing counts as permission to flush.",
 r"""## Plain English

**Theorem (`verdict_silence`, Config1.lean lines 89–93).** `¬ compatStmt vendorA vendorB_unspecified`.

The proof is the same as for [verdict_divergent](#/node/Config1.verdict_divergent), with one difference: the
side condition “B admits the flush flag `true`” is now `admits Unspecified true`, which is just `True` and is
discharged by `True.intro`. So silence is exactly as bad as explicitly pinning FlushToZero, as far as
full-domain compatibility is concerned.

This is the result the project calls the **silence hazard**. Its report shell suggests two remedies: pin the
mode in B's spec, or restrict the operative input domain. The second remedy is proved in
[verdict_domain_restricted](#/node/Config1.verdict_domain_restricted).

**What it does not say.** It does not say that every implementation of the silent spec misbehaves. A
Preserve implementation of `vendorB_unspecified` agrees with A everywhere. The claim is only that the *spec*
does not guarantee agreement.
""",
 [q("Does this theorem say every implementation of B's silent spec disagrees with A?", ["Yes", "No, only that some admissible implementation does"], 1,
    "The negated statement quantifies over all admissible flags, so one bad choice (flush = true) is enough."),
  q("What discharges “B admits flush = true” in the proof?", ["rfl", "True.intro"], 1, "`admits .Unspecified _` is `True` (Config1.lean line 93)."),
  q("Which input breaks agreement?", ["0x0001", "Every subnormal input, though the proof uses 0x0001", "Both of these answers"], 2,
    "Every subnormal is changed by flushing; the proof just needs one."),
  q("Is silence treated more leniently than pinning FlushToZero?", ["Yes", "No"], 1,
    "The proof is the same as verdict_divergent, with only the admissibility witness changed.")],
 caveats=[NOTBUILT, "This reading of silence (“any behaviour is allowed”) is a modelling choice made in `admits`, and a reasonable one for audit purposes."],
 widgets=[{"type": "walkthrough", "title": "How the proof goes (Config1.lean, lines 92-93)",
           "config": {"steps": [
               {"text": "Assume h, the claimed agreement for all admissible flags and all inputs.", "link": "Core.Statement.compatStmtOn",
                "lean": "theorem verdict_silence : ¬ compatStmt vendorA vendorB_unspecified :="},
               {"text": "Instantiate h with A's flag false, B's flag true (FlushToZero) and x = 0x0001. 'In domain' and 'A admits false' hold by rfl, and 'B admits true' is True. That yields canonOp 0x0001 = vendorOp true 0x0001, which the ground divergence fact refutes.", "link": "Config1.canon_diverges_under_flush",
                "lean": "  fun h => canon_diverges_under_flush (h (modeFlag .Preserve) (modeFlag .FlushToZero) w_subnormal rfl rfl True.intro)"}]}}])


node("Config1.verdict_domain_restricted",
 "Headline: drop subnormals and silence is harmless",
 "Once the inputs exclude subnormals, vendor A agrees with vendor B for either flush flag, even though B's spec is silent. The project calls this its signature result: narrowing the input domain is as good as pinning the mode.",
 r"""## Plain English

**Theorem (`verdict_domain_restricted`, Config1.lean lines 97–105).**
`compatStmtOn normalDomain vendorA vendorB_unspecified`.

In words: for **every** flag `flushB` (B is silent, so both values are admitted) and every input that is not
[subnormal](#/node/Core.Domain.normalDomain), `canonOp x = vendorOp flushB x`. That holds because the flush branch of
[vendorOp](#/node/Core.Ops.vendorOp) only triggers on subnormals, so off them both sides are just `x`.

This is the positive counterpart of [verdict_silence](#/node/Config1.verdict_silence): the same two specs are
incompatible on the full domain but compatible on the non-subnormal domain. The flag `flushB` stays a free
variable here, so `bv_decide` has to handle both values at once.

As with [verdict_compatible](#/node/Config1.verdict_compatible), the stored certificate
(`certs/verdict_domain_restricted.lrat`) is only 10 bytes. The CHANGELOG (0.3.0) notes that it had to be
regenerated when a Lean update changed `bv_decide`'s preprocessing, and that the new one does not re-check on
the older toolchains.
""",
 [q("Which inputs are covered?", ["All inputs", "Every input that is not subnormal (including ±0, ∞, NaN)", "Only normal numbers in the strict IEEE sense"], 1,
    "`normalDomain x = !(isSubnormal x)` (Core/Domain.lean line 40)."),
  q("Does this hold for both values of B's flush flag?", ["Yes", "No, only Preserve"], 0,
    "B is Unspecified, so flushB is unconstrained and the proof handles it as a free Boolean."),
  q("Does this contradict verdict_silence?", ["Yes", "No"], 1,
    "verdict_silence is about the full domain; the only failures are on subnormals, which this domain excludes."),
  q("What practical fix does this result support?", ["Restrict the operative input range so subnormals never cross the interface", "Change vendor A's operation"], 0,
    "That is the remediation in the report shell (Report/Types.lean, silence scenario).")],
 caveats=[NOTBUILT,
          "Certificate is 10 bytes, so the solver step is trivial. It is also toolchain-sensitive (CHANGELOG 0.3.0).",
          "“Signature result” is the project's own label (Config1.lean line 41)."],
 widgets=[{"type": "walkthrough", "title": "How the proof goes (Config1.lean, lines 101-105)",
           "config": {"steps": [
               {"text": "Unfold the builder with the normal domain and the two fixtures. B's admissibility collapses to True.", "link": "Core.Statement.compatStmtOn",
                "lean": "  simp only [compatStmtOn, admits, opOf, modeFlag, normalDomain, vendorA, vendorB_unspecified]"},
               {"text": "Introduce both flags, the input and the domain hypothesis hdom (x is not subnormal). flushB stays free.",
                "lean": "  intro flushA flushB x hdom _ _"},
               {"text": "Unfold operations and masks in both hdom and the goal, giving a pure BitVec/Bool implication.", "link": "Core.Format.isSubnormal",
                "lean": "  simp only [canonOp, vendorOp, isSubnormal, signedZero, signMask, expMask, mantMask] at hdom ⊢"},
               {"text": "Replay the stored certificate. bv_check uses hdom as a hypothesis and covers both values of flushB.",
                "lean": "  bv_check (config := { binaryProofs := false }) \"../certs/verdict_domain_restricted.lrat\""}]}}])

# ---------------- Configuration 3 ----------------

node("Config3.verdict_versions_compatible",
 "Relaxing a spec is backward-compatible",
 "Going from v1 (pinned Preserve) to v2 (Unspecified) breaks nobody: everything v1 allowed, v2 still allows. The proof is a two-value tautology.",
 r"""## Plain English

**Theorem (`verdict_versions_compatible`, Config3.lean lines 53–56).** `implStmt v1_preserve v2_unspecified`.

Unfolded, this is “for every flag `f`, if `f = false` then `True`”, which is immediate. The proof unfolds and calls
`bv_decide`, which closes it by normalization with no certificate.

See [implStmt](#/node/Core.Statement.implStmt) for what “conforms” means here (only the flag counts).
""",
 [q("Why is relaxing a commitment backward-compatible?", ["Unspecified admits every flag, so it admits whatever v1 admitted", "Because both versions use FlushModel"], 0,
    "The conclusion of the implication is `True`."),
  q("Does this theorem quantify over inputs x?", ["Yes", "No"], 1, "implStmt only quantifies over the flag (Core/Statement.lean line 75)."),
  q("Would implStmt v1_preserve v2_unspecified still hold if v2 were pinned to FlushToZero?", ["Yes", "No"], 1, "v1 admits false, but a FlushToZero pin admits only true.")],
 caveats=[NOTBUILT])


node("Config3.verdict_versions_incompatible",
 "Headline: tightening a spec breaks old implementations",
 "Going from v1 (silent on subnormals) to v2 (pinned Preserve) is not backward-compatible: the flush-to-zero flag is allowed by v1 and forbidden by v2. The statement only compares flags; a separate lemma shows the two behaviours differ on 0x0001.",
 r"""## Plain English

**Theorem (`verdict_versions_incompatible`, Config3.lean lines 60–64).**
There is a flag `flush` that `v1_unspecified` admits and `v2_preserve` does not.

The witness is `flush = modeFlag .FlushToZero = true`. v1 admits it because silence admits everything, and v2 rejects it
because v2 demands `flush = false`. The statement is written as an explicit existential rather than as
`¬ implStmt v1_unspecified v2_preserve`. The two are equivalent (the existential trivially implies the negation),
but the project states the constructive form, which the Report layer lists as using **no axioms** at all.

**From flags to bits.** `versions_behavioral_bridge` (Config3.lean lines 68–74) then checks that
the two flag values really do produce different outputs on [0x0001](#/node/Core.Witnesses.w_subnormal):
`vendorOp false 0x0001 ≠ vendorOp true 0x0001`. The source calls this “the Ariane-flavored finding”
(line 40), a nod to a spec change silently invalidating an old component.
""",
 [q("Which flag witnesses the incompatibility?", ["true (FlushToZero)", "false (Preserve)"], 0, "Config3.lean line 64."),
  q("Is the theorem stated as `¬ implStmt …`?", ["Yes", "No, as an explicit ∃ that implies it"], 1, "Config3.lean lines 62–63."),
  q("Does the theorem itself mention output bits?", ["Yes", "No, only flags; output bits are in versions_behavioral_bridge"], 1,
    "The behavioural link is a separate theorem (lines 71–74)."),
  q("Which direction of spec change is safe?", ["Relaxing (pinned → unspecified)", "Tightening (unspecified → pinned)"], 0,
    "Compare verdict_versions_compatible.")],
 caveats=[NOTBUILT, "“Backward-incompatible” here means flag-level non-conformance only. The behavioural consequence is a separate, ground theorem."],
 widgets=[{"type": "walkthrough", "title": "How the proof goes (Config3.lean, lines 62-64)",
           "config": {"steps": [
               {"text": "The goal: some flag is admitted by v1 (Unspecified) but not by v2 (Pinned Preserve).", "link": "Core.Statement.admits",
                "lean": "    ∃ flush, admits v1_unspecified.subnormal flush ∧ ¬ admits v2_preserve.subnormal flush :="},
               {"text": "Supply flush = true. v1's admissibility is True. For v2, unfold to ¬ (true = false) and close it with decide.",
                "lean": "  ⟨modeFlag .FlushToZero, True.intro, by simp only [admits, modeFlag, v2_preserve]; decide⟩"},
               {"text": "Separately (lines 71–74), versions_behavioral_bridge shows vendorOp false and vendorOp true differ on 0x0001, by unfolding and bv_decide on a ground goal.", "link": "Config3.versions_behavioral_bridge"}]}}])


node("Config3.versions_behavioral_bridge",
 "The flag difference shows up in the bits",
 "The Preserve behaviour required by v2 and the flushing behaviour allowed by v1 give different bits on 0x0001. This ties the flag-level incompatibility to actual output values.",
 r"""## Plain English

**Theorem (`versions_behavioral_bridge`, Config3.lean lines 68–74).**
`vendorOp (modeFlag .Preserve) w_subnormal ≠ vendorOp (modeFlag .FlushToZero) w_subnormal`, i.e.
`0x0001 ≠ 0x0000`.

This is a ground fact closed by `bv_decide` after unfolding. Together with
[verdict_versions_incompatible](#/node/Config3.verdict_versions_incompatible), it says the flag v1 allows and
v2 forbids actually changes behaviour.
""",
 [q("Is this a statement about all inputs?", ["Yes", "No, only the witness 0x0001"], 1, "Both sides are evaluated at w_subnormal."),
  q("Which operations are compared?", ["canonOp and vendorOp", "vendorOp with the two flag values"], 1, "Config3.lean line 72."),
  q("Why is this theorem needed alongside verdict_versions_incompatible?", ["That theorem only talks about flags; this one shows the flags change output bits", "It is a duplicate"], 0, "implStmt never looks at outputs (Core/Statement.lean line 75).")],
 caveats=[NOTBUILT])

# ---------------- Arithmetic ----------------

node("Arith.shiftAddMulAux",
 "Shift-and-add multiplication (and its defect)",
 "Vendor B's multiplier adds up x shifted left by k for every set bit k of y. The defective version simply stops one bit early.",
 r"""## Plain English

**Definition (`shiftAddMulAux`, Arith/Mul.lean lines 34–38).** `shiftAddMulAux x y n` is the sum over
`k = 0 … n−1` of “`x <<< k` if bit `k` of `y` is set, else 0”, computed in `BitVec 4` (so modulo 16).

- `shiftAddMul x y = shiftAddMulAux x y 4` (line 41) is the full schoolbook multiplier: all four partial products.
- `buggyShiftAddMul x y = shiftAddMulAux x y 3` (line 46) drops the bit-3 partial product.

In 4 bits, `x <<< 3` keeps only the lowest bit of `x` (moved to bit 3). So the defect matters exactly when **`y ≥ 8`
and `x` is odd**: then the buggy result is off by 8. For example, 15 × 15 = 225 ≡ 1 (mod 16), but the buggy multiplier
computes 15 × 7 = 105 ≡ 9.
""",
 [q("How many partial products does `buggyShiftAddMul` add?", ["3", "4"], 0, "It is `shiftAddMulAux x y 3` (Arith/Mul.lean line 46)."),
  q("What is `buggyShiftAddMul 15 15`?", ["1", "9", "15"], 1, "15 × (1+2+4) = 105 ≡ 9 (mod 16)."),
  q("Does the bug show up when y < 8?", ["Yes", "No"], 1, "Bit 3 of y is 0, so the missing term would have been 0 anyway.")])


node("Arith.mulAgree",
 "The multiplier agreement statement",
 "Two multiplier specs agree when their named implementations give the same 4-bit product for every pair of 4-bit inputs. It is the arithmetic analogue of the floating-point compatibility question, without a freedom axis.",
 r"""## Plain English

**Definitions (Arith/Audit.lean lines 40–66).**

- `MulImpl` (lines 41–44): `builtin`, `shiftAdd` or `buggyShiftAdd`.
- `MulICD` (lines 47–49): a vendor label (a `String`, purely descriptive) plus an `impl`.
- `Arith.opOf` (lines 52–55): `builtin ↦ x * y`, `shiftAdd ↦ shiftAddMul`, `buggyShiftAdd ↦ buggyShiftAddMul`
  (see [shiftAddMulAux](#/node/Arith.shiftAddMulAux)).
- **`mulAgree a b`** (lines 59–60): for all `x y : BitVec 4`, `opOf a.impl x y = opOf b.impl x y`.
- Fixtures (lines 63–66): `vendorA` (builtin), `vendorB_correct` (shift-and-add), `vendorB_buggy` (defective).

Unlike [compatStmtOn](#/node/Core.Statement.compatStmtOn) there are no flags and no domain: a multiplier has nothing
left unspecified.
""",
 [q("How many input pairs does `mulAgree` quantify over?", ["16", "256", "65,536"], 1, "Two 4-bit inputs: 16 × 16."),
  q("Does the vendor label string affect the statement?", ["Yes", "No"], 1, "Only `.impl` is used in `mulAgree` (line 60)."),
  q("Is `*` on `BitVec 4` exact integer multiplication?", ["Yes", "No, it wraps modulo 16"], 1, "BitVec arithmetic is modular.")])


node("Arith.mul_true",
 "Headline: shift-and-add equals multiplication",
 "The builtin 4-bit multiply and the unrolled shift-and-add multiplier agree on every input pair. This is the one theorem whose stored certificate is substantial (about 71 KB of LRAT), and it re-checks with no solver installed.",
 r"""## Plain English

**Theorem (`mul_true`, Arith/Audit.lean lines 68–74).** `mulAgree vendorA vendorB_correct`: for all
`x y : BitVec 4`, `x * y = shiftAddMul x y`.

Mathematically this is just the schoolbook multiplication algorithm, and it is obvious once written in binary.
For a bit-blaster, though, the builtin `*` and the shift-and-add circuit are two different circuits, and proving them
equivalent is a classic SAT benchmark shape. The project uses it as its **SAT-stress** case. The stored
certificate `certs/mul_true.lrat` is about 71 KB, compared with 10 bytes for the
[floating-point verdicts](#/node/Config1.verdict_compatible), and TRUST.md (point 2 under “What this buys”)
cites it as the substantial demonstration that re-checking needs no solver.

For scale: with 4-bit inputs there are only 256 cases, so this is a small instance of a hard family, not a hard
instance. Wider multipliers grow quickly, and the source mentions “wider formats” as future work
(Arith/Mul.lean lines 27–29).

The negative twin is [mul_false](#/node/Arith.mul_false).
""",
 [q("Which two operations does `mul_true` equate?", ["BitVec 4 `*` and shiftAddMul", "Nat multiplication and shiftAddMul", "Two floating-point multipliers"], 0,
    "Arith/Audit.lean lines 52–55 and 71."),
  q("Is any IEEE 754 rounding involved?", ["Yes", "No"], 1, "It is pure integer BitVec arithmetic (Arith/Mul.lean lines 27–28)."),
  q("What makes this certificate different from the Config-1 ones?", ["It is large (~71 KB), so the solver did real work", "It was hand-written"], 0,
    "The Config-1 certificates are 10 bytes each."),
  q("Does re-checking `mul_true` require CaDiCaL?", ["Yes", "No"], 1, "It uses `bv_check` with the cached certificate (line 74).")],
 caveats=[NOTBUILT, "“SAT-hard” in the source refers to the problem family; at 4 bits the instance is small (256 input pairs).",
          "Trust base per TRUST.md: kernel, classical trio, plus one native compiler-trust axiom (the same mechanism native_decide uses)."],
 widgets=[{"type": "walkthrough", "title": "How the proof goes (Arith/Audit.lean, lines 71-74)",
           "config": {"steps": [
               {"text": "Unfold the agreement statement, the op lookup, the two fixtures and the shift-and-add definitions. The recursion on 4 unrolls into four conditional shifted adds.", "link": "Arith.shiftAddMulAux",
                "lean": "  simp only [mulAgree, opOf, vendorA, vendorB_correct, shiftAddMul, shiftAddMulAux]"},
               {"text": "Introduce the two 4-bit inputs.", "lean": "  intro x y"},
               {"text": "Bit-blast x * y = (unrolled sum) and replay the ~71 KB stored LRAT refutation of its negation with the verified checker. No solver is called.",
                "lean": "  bv_check (config := { binaryProofs := false }) \"../../certs/mul_true.lrat\""}]}}])


node("Arith.mul_false",
 "Headline: the defective multiplier is caught",
 "The builtin multiply and the defective shift-and-add give different answers on x = y = 15 (1 versus 9). The source records that this witness was found by the SAT solver, not chosen by hand.",
 r"""## Plain English

**Theorem (`mul_false`, Arith/Audit.lean lines 94–99).**
`opOf vendorA.impl w9x w9y ≠ opOf vendorB_buggy.impl w9x w9y`, where `w9x = w9y = 15` (lines 91–92).

So `15 * 15 = 1 (mod 16)` is not equal to `buggyShiftAddMul 15 15 = 9`; see
[shiftAddMulAux](#/node/Arith.shiftAddMulAux). The theorem itself is a **ground inequality**, closed by unfolding and
`bv_decide`, with no certificate.

**Where the witness came from.** The doc comment (lines 78–90) records that running `bv_decide` on the universal
claim “`x * y` equals the defective multiplier” in a scratch file made CaDiCaL report the counterexample
`x = 15#4, y = 15#4`, and that diagnostic is quoted in the source as evidence. That scratch run is **not** part of the
repository, so a reader cannot replay the discovery from the shipped files. Only the resulting inequality can be checked.

Note the statement is about one input pair. It implies `¬ mulAgree vendorA vendorB_buggy`, but the project does not
state that negation as a separate theorem.
""",
 [q("What does the theorem actually assert?", ["The two multipliers differ at x = y = 15", "They differ on every input", "¬ mulAgree vendorA vendorB_buggy, stated as such"], 0,
    "Arith/Audit.lean lines 96–97 are a ground inequality at the witness."),
  q("Can the solver's discovery of (15, 15) be replayed from the repo?", ["Yes", "No, only the resulting inequality is checked"], 1,
    "The discovery happened in a scratch file and is recorded in a comment (lines 78–90)."),
  q("Would x = 1, y = 8 also be a counterexample?", ["Yes", "No"], 0,
    "y ≥ 8 and x odd: 1 × 8 = 8, but the buggy multiplier gives 0."),
  q("What does the defective multiplier compute on (15, 15)?", ["1", "9", "105"], 1, "15 × 7 = 105 ≡ 9 (mod 16).")],
 caveats=[NOTBUILT, "“Solver-discovered” rests on the quoted diagnostic in the doc comment. This site did not reproduce it.",
          "The project does not state ¬ mulAgree vendorA vendorB_buggy; it follows immediately from this inequality."],
 widgets=[{"type": "walkthrough", "title": "How the proof goes (Arith/Audit.lean, lines 96-99)",
           "config": {"steps": [
               {"text": "The goal compares the two implementations at the recorded witness (15, 15).", "link": "Arith.mulAgree",
                "lean": "    opOf vendorA.impl w9x w9y ≠ opOf vendorB_buggy.impl w9x w9y := by"},
               {"text": "Unfold everything, including the three-step recursion of the defective multiplier and the witness values, leaving a closed BitVec 4 inequality.", "link": "Arith.shiftAddMulAux",
                "lean": "  simp only [opOf, vendorA, vendorB_buggy, buggyShiftAddMul, shiftAddMulAux, w9x, w9y]"},
               {"text": "bv_decide settles the ground goal 15*15 ≠ (buggy sum). The project reports it uses only propext, with no native axiom and no certificate.",
                "lean": "  bv_decide"}]}}])
