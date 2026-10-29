NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}


node("Core.Format.isSubnormal",
 "Subnormal binary16 bit patterns",
 "A 16-bit pattern counts as subnormal exactly when its five exponent bits are all zero and its ten mantissa bits are not. This is the only floating-point fact the whole project needs.",
 r"""## Plain English

IEEE 754 *binary16* (“half precision”) packs a number into 16 bits: **bit 15** is the sign, **bits 14–10** are
the exponent and **bits 9–0** are the mantissa. The project gives each field a named mask
(Core/Format.lean lines 31–38):

| name | value | bits |
|---|---|---|
| `signMask` | `0x8000` | 15 |
| `expMask` | `0x7C00` | 14–10 |
| `mantMask` | `0x03FF` | 9–0 |

**Definition (`isSubnormal`, Core/Format.lean lines 40–43).** A pattern `x : BitVec 16` is subnormal when
`x AND expMask` is zero (the exponent field is all zeros) **and** `x AND mantMask` is nonzero (the mantissa is not
all zeros).

That matches IEEE 754: a zero exponent with a nonzero fraction is a *subnormal* (denormal) number, i.e. a value
smaller in magnitude than the smallest normal number. A zero exponent with a zero fraction is ±0, and that is
**not** subnormal. The smallest positive subnormal is `0x0001`; see [the witness](#/node/Core.Witnesses.w_subnormal).

The companion `signedZero x` (Core/Format.lean lines 45–48) keeps only the sign bit: it is `+0` (`0x0000`) or `−0`
(`0x8000`) depending on the sign of `x`. Flush-to-zero replaces a subnormal with this value; see
[vendorOp](#/node/Core.Ops.vendorOp).

Everything is a pure bit-level `Bool` test with no real numbers involved, which is why `bv_decide` can reason about it.
""",
 [q("Which of these binary16 patterns is subnormal?", ["0x0000", "0x0001", "0x0400", "0x7C00"], 1,
    "0x0001 has exponent field 0 and mantissa 1 (Core/Format.lean lines 42–43). 0x0000 has mantissa 0 (it is +0); 0x0400 and 0x7C00 have a nonzero exponent field."),
  q("Is negative zero (0x8000) subnormal under this definition?", ["Yes", "No"], 1,
    "Its exponent and mantissa fields are both zero, so the mantissa test `(x &&& mantMask) != 0` fails."),
  q("What does `signedZero 0x8001` return?", ["0x0000", "0x8000", "0x8001"], 1,
    "It keeps only the sign bit: 0x8001 AND 0x8000 = 0x8000, i.e. −0 (Core/Format.lean lines 47–48).")],
 caveats=["The model only looks at bit fields. It never interprets a pattern as a real number, and NaN and infinity are not singled out (they are simply not subnormal)."])


node("Core.Ops.vendorOp",
 "The flush-parameterized handoff",
 "One operation with one switch: with the flush flag off it passes the 16 bits through unchanged, and with it on it also replaces every subnormal by a zero of the same sign. That switch is the only freedom the specs in this project leave open.",
 r"""## Plain English

**Definition (`vendorOp`, Core/Ops.lean lines 37–41).** Given a flag `flush : Bool` and an input `x : BitVec 16`:

- if `flush` is true **and** `x` is [subnormal](#/node/Core.Format.isSubnormal), return `signedZero x`
  (that is, +0 or −0);
- otherwise return `x` unchanged.

So `vendorOp false` is the identity (“Preserve”) and `vendorOp true` is flush-to-zero (“FlushToZero”).
The mapping from the named modes to the flag is `modeFlag` (Core/ICD.lean lines 52–55): Preserve ↦ `false`,
FlushToZero ↦ `true`.

These are *rounding-free handoffs*: no arithmetic, only “pass the number along, maybe flushing tiny values”.
Real hardware often has a flush-to-zero (FTZ/DAZ) mode, and two components that disagree about it can hand
each other different bits. That disagreement is the hazard every Configuration-1 verdict is about.

The same file also defines `idOp` (the bare identity, line 44), which no theorem uses, and
[canonOp](#/node/Core.Ops.canonOp), vendor A's operation.
""",
 [q("What is `vendorOp false x`?", ["Always x", "x, unless x is subnormal", "signedZero x"], 0,
    "`false && isSubnormal x` is false, so the `else` branch returns x (Core/Ops.lean line 41)."),
  q("What is `vendorOp true 0x8001`?", ["0x8001", "0x8000", "0x0000"], 1,
    "0x8001 is subnormal (exponent 0, mantissa 1), so it is replaced by the signed zero with its sign bit: −0 = 0x8000."),
  q("Does `vendorOp true` change normal numbers such as 0x3C00 (1.0)?", ["Yes", "No"], 1,
    "Only subnormal inputs take the flush branch.")])


node("Core.Ops.canonOp",
 "Vendor A's canonicalize handoff",
 "Vendor A splits the word into sign, exponent and mantissa and ORs them back together. That is secretly the identity, but only bit-level reasoning shows it, which is why vendor A's agreement proofs go through the SAT path.",
 r"""## Plain English

**Definition (`canonOp`, Core/Ops.lean lines 46–50).**
`canonOp x = (x AND signMask) OR (x AND expMask) OR (x AND mantMask)`.

The three masks `0x8000`, `0x7C00` and `0x03FF` are disjoint and together cover all 16 bits (`0xFFFF`),
so recombining the three fields gives back `x` exactly. The source comment (line 47) says as much: it is
“equal to the identity for every input, but only provably so by bit-level reasoning.”

The name is a little misleading if you know IEEE 754: the standard's own `canonicalize` operation can change
non-canonical encodings (for example, NaN payloads). This `canonOp` changes nothing. In the project it is a
deliberate **stand-in** whose sameness with the identity has to be checked bit by bit, so that the
compatible verdicts exercise the certificate path instead of closing by simplification.

`canonOp` ignores the flush flag completely: [opOf](#/node/Core.Statement.opOf) maps the `Canonicalize` tag to
`fun _ x => canonOp x`. So vendor A behaves the same whatever its subnormal commitment says.
""",
 [q("For which inputs does `canonOp x = x` hold?", ["All 65,536 inputs", "Only normal numbers", "Only non-NaN inputs"], 0,
    "The three masks are disjoint and cover every bit, so the recombination is exactly x."),
  q("Does `canonOp` flush subnormals?", ["Yes", "No"], 1,
    "It has no flush branch at all; on 0x0001 it returns 0x0001. This is why vendor A diverges from a flushing vendor."),
  q("Is `canonOp` the IEEE 754 `canonicalize` operation?", ["Yes, exactly", "No, it is a bit-recombination stand-in that equals the identity"], 1,
    "Core/Ops.lean lines 46–50 define it purely as an OR of the three masked fields.")],
 caveats=["“Canonicalize” here is the project's name for a toy operation, not IEEE 754's canonicalize."])


node("Core.ICD.MockICD",
 "A mock interface spec (ICD)",
 "A spec here records only two things: which operation the vendor runs, and what it promises about subnormals: pinned to Preserve, pinned to FlushToZero, or Unspecified. Unspecified is the faithful model of a spec that says nothing.",
 r"""## Plain English

An **ICD** (interface control document) is the engineering spec that says what crosses an interface between two
components. The project models only a tiny slice of one (Core/ICD.lean lines 31–50):

- `SubnormalMode` (lines 32–34): `Preserve` or `FlushToZero`.
- `Commitment` (lines 38–40): `Pinned m` (the spec commits to mode `m`) or `Unspecified` (the spec is silent).
- `OpTag` (lines 43–45): `Canonicalize` (vendor A's [canonOp](#/node/Core.Ops.canonOp)) or `FlushModel`
  (the flag-driven [vendorOp](#/node/Core.Ops.vendorOp)).
- **`MockICD`** (lines 48–50): a record with an `op : OpTag` and a `subnormal : Commitment`.

The key modelling decision is what `Unspecified` means. The statement builder turns it into “**any** flag is
admissible” ([admits](#/node/Core.Statement.admits)). So a compatibility claim must hold for every behaviour a
silent spec allows, and silence counts as a hazard, not as a free pass.

The concrete specs used by the theorems are listed under [the fixtures](#/node/Core.Fixtures.vendorA).
""",
 [q("Which of these can a `MockICD` express?", ["A rounding mode", "A subnormal-handling commitment", "An input range"], 1,
    "Its only fields are `op` and `subnormal` (Core/ICD.lean lines 48–50). Input domains are supplied separately to `compatStmtOn`."),
  q("How does the project read an `Unspecified` commitment?", ["As Preserve by default", "As 'every flag value is allowed'", "As an error"], 1,
    "`admits .Unspecified _ = True` (Core/Statement.lean line 51)."),
  q("What is `modeFlag .FlushToZero`?", ["true", "false"], 0, "Core/ICD.lean line 55.")],
 caveats=["Format is fixed to binary16 and the only freedom is subnormal handling; the source says this is deliberately “the narrow ICD slices the bit-exact audit needs” (Core/ICD.lean lines 22–23)."])


node("Core.Statement.admits",
 "Which flags a commitment allows",
 "A pinned commitment allows exactly one flush-flag value, and silence allows both. This one small definition is how “the spec doesn't say” becomes a universally quantified Boolean in every compatibility statement.",
 r"""## Plain English

**Definition (`admits`, Core/Statement.lean lines 46–51).** `admits c f` is a proposition saying that flag `f` is
allowed under commitment `c`:

- `admits (Pinned m) f` is `f = modeFlag m` (exactly one value);
- `admits Unspecified f` is `True` (every value).

The statements below say “for every `flushA`, `flushB` with `admits … flushA` and `admits … flushB`, …”.
With a pinned spec this hypothesis forces the flag to one value. With a silent spec it is vacuous, so the claim
has to hold for **both** flag values. The source calls this “the decidable realization of ICD silence”
(lines 30–32).

`admits` is also reused for version conformance in [implStmt](#/node/Core.Statement.implStmt).
""",
 [q("How many flag values does `admits (Pinned .Preserve)` allow?", ["0", "1", "2"], 1, "Only `false` (= modeFlag Preserve)."),
  q("How many does `admits Unspecified` allow?", ["0", "1", "2"], 2, "Both: the predicate is `True` (Core/Statement.lean line 51)."),
  q("Is `admits` a `Bool` function or a `Prop`?", ["Bool", "Prop"], 1, "Its type is `Commitment → Bool → Prop` (line 49).")])


node("Core.Statement.opOf",
 "From operation tag to function",
 "The tag in a spec picks the function. Canonicalize ignores the flag and runs canonOp, and FlushModel runs vendorOp with the flag.",
 r"""## Plain English

**Definition (`opOf`, Core/Statement.lean lines 53–58).** `opOf : OpTag → (Bool → BitVec 16 → BitVec 16)`.

- `opOf Canonicalize = fun _ x => canonOp x`: the flag argument is thrown away;
- `opOf FlushModel = vendorOp`.

So every vendor is treated as a function of (flag, input), even vendor A, whose output never depends on the flag.
In particular vendor A's own commitment (`Pinned Preserve`) has **no effect** on any verdict: it constrains a flag
that `canonOp` never reads.

(The arithmetic scenario has its own, separate `Arith.opOf` for multipliers; see [mulAgree](#/node/Arith.mulAgree).)
""",
 [q("What does `opOf .Canonicalize true 0x0001` return?", ["0x0001", "0x0000"], 0,
    "The flag is ignored and canonOp 0x0001 = 0x0001."),
  q("If vendor A's spec said `Unspecified` instead of `Pinned Preserve`, would the Configuration-1 verdicts change?", ["Yes", "No"], 1,
    "Vendor A's operation ignores its flag, so admitting more flag values for A changes nothing about its outputs."),
  q("What does `opOf .FlushModel` return?", ["canonOp", "vendorOp", "idOp"], 1, "Core/Statement.lean line 58.")])


node("Core.Statement.compatStmtOn",
 "The compatibility question",
 "Two specs are compatible on a domain when every pair of implementations they allow gives identical bits on every input in that domain. Every Configuration-1 verdict is this one proposition, or its negation.",
 r"""## Plain English

**Definition (`compatStmtOn`, Core/Statement.lean lines 60–65).** For a domain `dom : BitVec 16 → Bool` and specs
`a`, `b`:

> for all flags `flushA`, `flushB` and every input `x`, if `x` is in `dom`, `flushA` is
> [admitted](#/node/Core.Statement.admits) by `a`'s commitment and `flushB` by `b`'s, then
> `opOf a.op flushA x = opOf b.op flushB x`.

**`compatStmt a b`** (lines 67–68) is the same with the full domain (`fullDomain`, every one of the 2¹⁶ patterns).

This is the audit question the project's docs phrase as “for any pair of compliant implementations of these two
specs, will their outputs agree?” (Config1.lean lines 27–28). Note what it compares: **the 16 output bits must be
identical**, so `+0` and `−0` count as different, and so does any change to a subnormal.

The builder is written so that, for concrete fixtures, unfolding it with `simp only` leaves a pure
`BitVec`/`Bool` goal that `bv_decide` can bit-blast (lines 35–39).
""",
 [q("Does `compatStmt` treat +0 (0x0000) and −0 (0x8000) as the same output?", ["Yes", "No"], 1,
    "It asks for equality of `BitVec 16` values, i.e. identical bits."),
  q("If spec b is `Unspecified`, how many values of flushB must the agreement hold for?", ["One", "Both true and false"], 1,
    "`admits Unspecified flushB` is `True`, so nothing restricts flushB."),
  q("What does the `dom` argument restrict?", ["Which flags are allowed", "Which inputs x must agree", "Which operation is used"], 1,
    "It appears only as the hypothesis `dom x` (line 64)."),
  q("To refute `compatStmt a b`, what is enough?", ["One admissible flag pair and one input where outputs differ", "Showing the specs have different op tags"], 0,
    "A universal claim fails on a single counterexample; this is exactly how verdict_divergent is proved.")])


node("Core.Statement.implStmt",
 "Backward compatibility of versions",
 "Version 2 is backward-compatible with version 1 when every flush flag that v1 allows is also allowed by v2. This checks conformance only at the level of the flag, not output bits.",
 r"""## Plain English

**Definition (`implStmt`, Core/Statement.lean lines 70–75).** `implStmt v1 v2` says: for every `flush : Bool`, if
`admits v1.subnormal flush` then `admits v2.subnormal flush`.

The docstring reads this as “every v1-conforming implementation also conforms to v2”, where an
implementation is identified with its flush flag. Relaxing a spec (Preserve → Unspecified) is
backward-compatible ([verdict_versions_compatible](#/node/Config3.verdict_versions_compatible)), and tightening
it (Unspecified → Preserve) is not ([verdict_versions_incompatible](#/node/Config3.verdict_versions_incompatible)).

Unlike [compatStmtOn](#/node/Core.Statement.compatStmtOn) there is **no input quantifier** and no operation:
`v1.op` and `v2.op` are never consulted. The link to actual output bits is made separately by
[versions_behavioral_bridge](#/node/Config3.versions_behavioral_bridge).
""",
 [q("Does `implStmt` look at the operation tags of v1 and v2?", ["Yes", "No"], 1, "Only `.subnormal` appears in its body (line 75)."),
  q("Is `implStmt (Pinned Preserve) Unspecified`-style relaxation backward-compatible?", ["Yes", "No"], 0,
    "Anything is admitted by Unspecified, so the implication always holds."),
  q("Is `implStmt` symmetric?", ["Yes", "No"], 1, "Relaxing is fine, tightening is not: the two Config3 verdicts go opposite ways.")],
 caveats=["Conformance is modelled purely as flag admissibility (Core/Statement.lean lines 71–73). This is a deliberately coarse notion of “implementation”."])


node("Core.Domain.normalDomain",
 "The input domains",
 "There are two domains: every bit pattern, or every pattern that is not subnormal. Excluding subnormals is exactly what makes the flush flag stop mattering.",
 r"""## Plain English

**Definitions (Core/Domain.lean lines 36–40).**

- `fullDomain x = true`: every 16-bit pattern is admissible.
- `normalDomain x = not (isSubnormal x)`: every pattern **except** the [subnormals](#/node/Core.Format.isSubnormal).

“Normal” here is loose: `normalDomain` includes ±0, infinities and NaNs as well as the normal numbers. It is
simply “not subnormal”. Since [vendorOp](#/node/Core.Ops.vendorOp) only flushes subnormals, on this domain
the flag is inert and every vendor behaves like the identity. That is the content of
[verdict_domain_restricted](#/node/Config1.verdict_domain_restricted).
""",
 [q("Is 0x0000 (+0) in `normalDomain`?", ["Yes", "No"], 0, "+0 is not subnormal (its mantissa is zero), so it is admitted."),
  q("Is 0x7E00 (a NaN) in `normalDomain`?", ["Yes", "No"], 0, "Its exponent field is nonzero, so it is not subnormal."),
  q("How many 16-bit patterns does `normalDomain` exclude?", ["2 × 1023 = 2046", "1024", "None"], 0,
    "Two signs times the 1023 nonzero mantissas with a zero exponent.")],
 caveats=["The name suggests “normal numbers” but the predicate is just “not subnormal”."])


node("Core.Fixtures.vendorA",
 "The invented vendors and versions",
 "Every theorem is about a handful of invented specs. Vendor A is the canonicalize reference, three vendor-B variants differ only in their subnormal promise, and two pairs of “versions” differ the same way.",
 r"""## Plain English

All fixtures are in Core/Fixtures.lean, and the project says plainly that they are synthetic and formalize no
real interface (README).

| fixture | op | subnormal commitment | lines |
|---|---|---|---|
| `vendorA` | Canonicalize | Pinned Preserve | 35–36 |
| `vendorB_preserve` | FlushModel | Pinned Preserve | 38–39 |
| `vendorB_flush` | FlushModel | Pinned FlushToZero | 41–42 |
| `vendorB_unspecified` | FlushModel | Unspecified | 44–45 |
| `v1_unspecified` / `v2_preserve` | FlushModel | Unspecified / Pinned Preserve | 53–58 |
| `v1_preserve` / `v2_unspecified` | FlushModel | Pinned Preserve / Unspecified | 60–65 |

`selectedA` / `selectedB` (lines 47–49) are editable “which pair does the driver run” settings. No theorem
uses them.

Note that `v2_preserve` and `vendorB_preserve` are the same record, as are `v1_unspecified` and
`vendorB_unspecified`. They are named differently because they play different roles.
""",
 [q("How do the three vendor-B fixtures differ?", ["In their op tag", "Only in their subnormal commitment", "In their input domain"], 1,
    "All three use FlushModel (Core/Fixtures.lean lines 38–45)."),
  q("Do these fixtures describe a real aerospace or automotive interface?", ["Yes", "No"], 1,
    "The README says the shipped fixtures are invented and no real interface is formalized."),
  q("Which fixture is silent on subnormals?", ["vendorB_flush", "vendorB_unspecified", "vendorA"], 1, "Its commitment is `.Unspecified` (line 45).")])


node("Core.Witnesses.w_subnormal",
 "The witness 0x0001",
 "The smallest positive subnormal, 0x0001, is the single input that breaks every negative verdict on the floating-point side. Preserve keeps it as is, and flush-to-zero turns it into 0x0000.",
 r"""## Plain English

**Definition (`w_subnormal`, Core/Witnesses.lean lines 30–34).** `w_subnormal : BitVec 16 := 0x0001`.

Its exponent field is 0 and its mantissa is 1, so it is [subnormal](#/node/Core.Format.isSubnormal). It is the
binary16 number 2⁻²⁴ ≈ 5.96 × 10⁻⁸.

- `vendorOp false 0x0001 = 0x0001` (Preserve).
- `vendorOp true 0x0001 = signedZero 0x0001 = 0x0000` (FlushToZero).
- `canonOp 0x0001 = 0x0001`.

The project keeps counterexamples as **named definitions** in a model layer instead of literals inside theorems
(lines 22–25), so each one doubles as an executable test vector.
""",
 [q("What does flush-to-zero turn 0x0001 into?", ["0x0000", "0x8000", "0x0001"], 0, "Its sign bit is 0, so the signed zero is +0."),
  q("Why does 0x0001 separate Preserve from FlushToZero?", ["It is subnormal", "It is a NaN", "It is negative"], 0,
    "Only subnormals are affected by the flush flag."),
  q("Would any other subnormal also work as a witness?", ["Yes", "No"], 0,
    "Every subnormal is non-zero in its mantissa, so flushing always changes it. 0x0001 is just the canonical choice.")])


node("DivergenceWitness",
 "A divergence, packaged",
 "A DivergenceWitness bundles an input, two outputs and a proof that the outputs differ, so a consumer can read the counterexample without recomputing anything. The one shipped instance is 0x0001 ↦ 0x0001 versus 0x0000.",
 r"""## Plain English

**Structure (`DivergenceWitness`, DivergenceWitness.lean lines 40–52).** Fields: `input`, `outputA`,
`outputB : BitVec 16`, and `differ : outputA ≠ outputB`. Because the proof is a field, you cannot build a
`DivergenceWitness` whose outputs are actually equal.

**Instance (`subnormalFlushWitness`, lines 54–62).** Input `w_subnormal`, `outputA = canonOp w_subnormal`,
`outputB = vendorOp (modeFlag .FlushToZero) w_subnormal`, with `differ` supplied by
[canon_diverges_under_flush](#/node/Config1.canon_diverges_under_flush).

`subnormalFlushWitness_diverges` (lines 64–68) just re-exports that `differ` field under a name.

Note that the structure does not record *which* two operations were compared. It is the caller's job to remember
that `outputA` came from `canonOp` and so on.
""",
 [q("Can you construct a `DivergenceWitness` with `outputA = outputB`?", ["Yes", "No"], 1,
    "You would have to supply a proof of `outputA ≠ outputB`, which is impossible when they are equal."),
  q("Does the structure record which operations produced the outputs?", ["Yes", "No"], 1, "Only the input, two outputs and the proof (lines 44–52)."),
  q("What are the two outputs in `subnormalFlushWitness`?", ["0x0001 and 0x0000", "0x0001 and 0x8000", "0x0000 and 0x0000"], 0,
    "canonOp keeps 0x0001; flush-to-zero gives +0.")])


node("Smoke.cached_xor_identity",
 "The cached-certificate canary",
 "This is a small bitvector identity that is re-checked from a stored LRAT certificate with no SAT solver installed. It is the reproducibility primitive the rest of the demo relies on.",
 r"""## Plain English

**Theorem (`cached_xor_identity`, Smoke.lean lines 45–47).** For all 8-bit `x`, `y`:
`(x OR y) − (x AND y) = x XOR y`.

Why it's true (lines 34–37): `x XOR y` and `x AND y` occupy disjoint bit positions, so `x OR y` is their sum, and
subtracting `x AND y` leaves `x XOR y`.

The proof is one line, `bv_check "../certs/smoke.lrat"`. `bv_check` rebuilds the bit-blasted SAT problem
from the goal, reads a stored **LRAT** proof (a step-by-step refutation certificate) from `certs/`, and has Lean's
verified checker confirm it, with no SAT solver involved. The twin `live_xor_identity` in LiveSolveCanary.lean
proves the same goal with live `bv_decide` (it calls CaDiCaL) and is kept out of the default build on purpose.
""",
 [q("Does re-checking this theorem need a SAT solver?", ["Yes", "No"], 1, "`bv_check` replays the stored certificate (Smoke.lean line 47)."),
  q("Why does it carry a certificate instead of closing by simplification?", ["It mixes subtraction with bitwise operations, so normalization alone does not settle it", "Certificates are mandatory for every theorem"], 0,
    "Smoke.lean lines 36–37."),
  q("What would break the stored certificate?", ["A toolchain whose bv_decide preprocessing produces a different SAT problem", "Running on a different computer"], 0,
    "TRUST.md, re-verification protocol step 3; CHANGELOG 0.3.0 records exactly this happening to one certificate.")],
 caveats=["Not built for this site. The project reports the axioms as the classical trio plus one native compiler-trust axiom (TRUST.md); see the Trust page."],
 widgets=[{"type": "walkthrough", "title": "How the proof goes (Smoke.lean, lines 45-47)",
           "config": {"steps": [
               {"text": "The goal is a quantifier-free statement about two 8-bit words, already in bv_decide's fragment.", "lean": "    (x ||| y) - (x &&& y) = x ^^^ y := by"},
               {"text": "bv_check bit-blasts the goal to CNF, then checks the stored LRAT refutation of its negation with the verified checker (run as compiled code). No solver is called.", "lean": "  bv_check \"../certs/smoke.lrat\""}]}}])
