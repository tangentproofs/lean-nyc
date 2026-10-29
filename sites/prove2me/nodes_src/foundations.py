NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}


node("LeanEnvironment",
 "Lean environment: the pinned Lean and Mathlib versions",
 "Every statement on Prove2Me lives in exactly one environment, a fixed Lean toolchain plus a fixed Mathlib commit, and is checked only there. Results can't be imported across environments.",
 r"""## Plain English

Lean and its mathematics library Mathlib change constantly. A name gets renamed, a lemma moves, and a
statement that compiled last month may not compile today. Prove2Me deals with this by **pinning**: the site
runs a few fixed *environments*, each a specific Lean version paired with a specific Mathlib commit.

According to the [FAQ](https://prove2.me/faq#contribute), as fetched on 2026-10-29, three environments are
supported: Lean 4 **v4.33.1** (the default for new theorems), **v4.30.0** and **v4.29.0-rc3**, "each with its
own fixed Mathlib revision". The agent reference guide on proving (linked from
[skill.md](https://prove2.me/skill.md)) lists the exact Mathlib commit for each.

What pinning buys you:

- **Reproducibility.** A [statement](#/node/Statement) and its proofs are checked in one environment,
  and the environment never changes, so the verdict shouldn't change either. The
  [About page](https://prove2.me/about#trust) says results "reproduce forever".
- **Unambiguous provenance.** You always know exactly which Mathlib a theorem was stated against, which
  matters because Mathlib definitions occasionally change meaning.

What it costs:

- **Islands.** The FAQ says plainly that "cross-environment reuse is not supported". A theorem proved in
  the v4.29 environment can't be imported by a proof in the v4.33 environment. To use it there, someone has to
  restate it and prove it again in the new environment.
- **Drift from current Mathlib.** Over time the pinned Mathlib falls behind. The site says new
  environments "will be added over time", but existing statements keep the environment they were created in.

The site also notes that the server elaborates with automatic implicit variables switched off, so every
variable in a statement has to be declared explicitly. That rules out one class of accidental
misstatement.
""",
 [q("A theorem was proved in the v4.29.0-rc3 environment. Can a proof in the default v4.33.1 environment import it?",
    ["No: imports only resolve inside the same environment", "Yes, imports work across all environments",
     "Yes, but only after a moderator approves it"], 0,
    "The [FAQ](https://prove2.me/faq#contribute) says cross-environment reuse is not supported."),
  q("What exactly does an environment pin?",
    ["A Lean toolchain version together with one Mathlib commit", "Only the Lean version; Mathlib floats to the latest",
     "The operating system of the verification server"], 0,
    "Each environment is a Lean version with its own fixed Mathlib revision ([FAQ](https://prove2.me/faq#contribute))."),
  q("Why does pinning help trust?",
    ["The same statement is always checked against the same library, so a verdict can be reproduced",
     "It makes proofs shorter", "It lets the server skip the kernel check"], 0,
    "The [About page](https://prove2.me/about#trust) lists immutable, pinned environments as one of its trust guarantees."),
 ],
 caveats=["The version list is a snapshot from 2026-10-29. The site says the reference table \"can lag\" behind what the server actually offers, and new environments will be added."])


node("Statement",
 "Statement: an immutable Lean theorem card",
 "A theorem on Prove2Me is a card: a Lean 4 statement with its proof left as `sorry`, plus a plain-language description. The Lean statement is what gets proved. Once published it can't be edited, only deprecated.",
 r"""## Plain English

The basic unit on Prove2Me is a **theorem**, which the [About page](https://prove2.me/about) describes as "a
standalone, immutable card". It has:

- a **Lean 4 statement** whose proof is left as `sorry` (Lean's placeholder for "proof missing");
- a **plain-language description** of what it means, plus a title, source citation and tags;
- a status: *Open*, *Proved* or *Disproved*.

**Definitions** are cards too. A theorem can import platform definitions, and a mission's definitions are the
vocabulary its goal is stated in.

### The Lean declaration is the authoritative statement

This is the single most important fact for reading anything on the site. When a theorem shows as *Proved*,
what has been proved is **its Lean statement**, in its pinned [environment](#/node/LeanEnvironment). The
English description is there to help humans. Lean never checks it, and the FAQ says the submitter can freely
edit the title, natural-language statement, source and tags. Only the Lean statement is frozen.

So if the English and the Lean disagree, the Lean is what was proved. For a mission's goal, definitions and
milestones, humans check that the two agree before launch (see [Captain](#/node/Captain) and
[Read-back](#/node/ReadBack)). For other statements nobody is required to check.

### Immutable, so mistakes are deprecated

Statements and proofs can't be edited or deleted after publication, public or private. The
[FAQ](https://prove2.me/faq#contribute) explains why: immutability "keeps the correctness of the whole proof
chain trackable". If something is wrong, its submitter **deprecates** it. It stays readable, is flagged
everywhere it appears, and a corrected version is published as a new card under a new name. Drafts inside a
mission proposal *are* editable until the proposal is submitted. That is where statements are meant to be
fixed.

### Statements are separate from proofs

One theorem can collect **many independent proofs**. Anyone can also submit a **disproof**, a verified proof
of the statement's negation, which marks it *Disproved*. Keeping statements separate from proofs is what lets
many agents work on one goal at once, and lets later proofs simplify earlier ones.
""",
 [q("A theorem card's English description says \"for all n\" but its Lean statement only covers n ≥ 1. The theorem is marked Proved. What was proved?",
    ["The Lean statement (n ≥ 1 only)", "The English statement (all n)", "Both, because the server compares them"], 0,
    "The Lean declaration is the authoritative statement. The English description isn't checked by Lean and can be edited by the submitter ([FAQ](https://prove2.me/faq#contribute))."),
  q("Your agent published a theorem with a typo in its Lean statement. What can you do?",
    ["Deprecate it and publish a corrected statement as a new theorem", "Edit the Lean statement in place",
     "Ask a moderator to delete it"], 0,
    "Statements are immutable. The fix is to deprecate the old card and re-upload ([FAQ](https://prove2.me/faq#contribute))."),
  q("Which parts of a published theorem can its submitter still edit?",
    ["Title, natural-language statement, source and tags, but not the Lean statement", "Everything, including the Lean",
     "Nothing at all"], 0,
    "The [FAQ](https://prove2.me/faq#contribute): everything except the Lean statement can be edited by its submitter."),
  q("What does a disproof prove?",
    ["The negation of the whole target statement", "That no proof has been found yet", "That the English description is wrong"], 0,
    "A disproof is a verified proof of the statement's negation ([About](https://prove2.me/about))."),
 ],
 caveats=["Simplified: the site has separate theorem and definition cards with slightly different rules (for example, disproofs can import definitions but not other theorems). This node treats them together."])


node("Verification",
 "Verification: the server's kernel check of every proof",
 "A proof is a Lean file with a theorem named `solution` whose type must match the target exactly. The server compiles it in the target's environment, rejects `sorry`, checks axioms against a whitelist, and gives a machine-readable verdict.",
 r"""## Plain English

The [About page](https://prove2.me/about) states the contract in one line: a proof is a Lean file declaring a
theorem called `solution` "whose type matches the target exactly, with no sorry. That's the whole contract."

Here is what happens when an agent submits a proof, as described on the [About page](https://prove2.me/about#trust),
the [solver tour](https://prove2.me/tour/mission-solver) and the proving guide linked from
[skill.md](https://prove2.me/skill.md):

1. **The agent compiles locally first.** The harness installs the pinned Lean and Mathlib on the
   contributor's own machine, so most mistakes are caught before submitting.
2. **The server compiles the file** in the target theorem's [environment](#/node/LeanEnvironment).
3. **Exact type match.** The `solution` theorem must have *exactly* the target's type. The About page
   stresses that Lean's elaborator and kernel decide this, which is "stricter than comparing text".
4. **No `sorry`.** Any `sorry` in the submitted file gets it rejected.
5. **Axiom whitelist.** The About page says "every proof's axioms are checked against a safe whitelist", so
   a proof can't make itself true by declaring a convenient axiom.
6. **No self-import.** The target is stored on the server as a `sorry` placeholder, so a proof that imports
   its own target is rejected.
7. **Verdict.** Submissions are asynchronous: the agent polls for the result. The guide lists the
   outcomes: accepted, accepted as a sketch (see [Proof-sketch](#/node/ProofSketch)), compile error, wrong
   answer (compiles but proves something else), `sorry` detected, other failure, and server error. The
   [FAQ](https://prove2.me/faq#community) says rejections come with machine-readable reasons, so the agent can
   iterate.

The agent must also attach a plain-language **explanation** of its proof, written like a section of a paper.
That's for humans; Lean doesn't check it.

### What a verdict does and doesn't mean

*Accepted* means: in that environment, Lean's kernel accepted a `sorry`-free term of exactly the target's
type, using only whitelisted axioms and platform imports. That's a strong guarantee about the **Lean
statement**. It says nothing about whether the Lean statement matches the paper. The FAQ calls that "the one
place machines can't save you" (see [Trust model](#/node/TrustModel)).
""",
 [q("An agent's file compiles but its `solution` proves a slightly weaker statement than the target. What happens?",
    ["It is rejected: the type must match the target exactly", "It is accepted, because it compiles",
     "It is accepted with a warning"], 0,
    "The proving guide calls this \"Wrong Answer\". Exact type match is part of the contract ([About](https://prove2.me/about#trust))."),
  q("Could a proof add a custom axiom that says the goal is true?",
    ["No: axioms are checked against a whitelist", "Yes, if it is named `solution`", "Yes, axioms are never inspected"], 0,
    "The [About page](https://prove2.me/about#trust): \"every proof's axioms are checked against a safe whitelist\"."),
  q("Why is a proof that imports its own target theorem rejected?",
    ["The target is stored as a `sorry` placeholder, so the proof would assume what it is proving", "Imports are never allowed",
     "Because it would compile too slowly"], 0,
    "From the proving guide linked from [skill.md](https://prove2.me/skill.md): never import your own target."),
  q("Which of these does an *Accepted* verdict certify?",
    ["The Lean statement holds in that environment", "The Lean statement faithfully captures the paper's theorem",
     "The agent's English explanation is correct"], 0,
    "The kernel checks the Lean only. Faithfulness and explanations are human matters ([FAQ](https://prove2.me/faq#trust))."),
 ],
 caveats=["The axiom whitelist's exact contents and the server's other blocked \"escape hatches\" are not listed on the public pages I read, so I can't say precisely what is allowed.",
          "I didn't submit anything or watch the server work. This describes the documented contract, not observed behaviour."])


node("ProofSketch",
 "Proof-sketch: reducing a hard theorem to smaller open ones",
 "A proof-sketch proves a theorem by importing other platform theorems, including ones nobody has proved yet. Each import becomes its own open problem, and the parent turns Proved automatically once all of them are.",
 r"""## Plain English

This is the mechanism that lets many agents work on one big result at once. The
[About page](https://prove2.me/about#proof-sketch) describes a proof-sketch as a proof that "proves a hard
theorem by importing other theorems, including ones nobody has proved yet". In other words it's a
**reduction**: *if* these child statements are true, the parent is true.

How it works:

1. To decompose a hard theorem, an agent first publishes the child lemmas as new open
   [statements](#/node/Statement), or picks existing ones.
2. It submits a proof of the parent that imports them. That proof must itself be `sorry`-free. The children
   carry `sorry` on the server, and that's allowed.
3. The server [verifies](#/node/Verification) the reduction. If any child is still open, the verdict is
   *sketch accepted* and each child becomes an independent open problem.
4. Anyone can close a child without downloading or compiling the parent. When the last child is proved,
   the parent becomes *Proved* automatically.

The children can be proved directly or sketched again, so the result is a **graph** of statements and
dependencies. A statement may have several competing sketches, and only one needs to succeed. The
[solver tour](https://prove2.me/tour/mission-solver) calls the open statements at the bottom of the graph the
**frontier**: what an agent can start on right now.

The About page calls this a "top-down programming" perspective on theorem proving. It gives two benefits:
more ways to contribute, and **smaller units of verification**, since each proof is compiled on its own
rather than the whole mission at once.

### Why a wrong child can't fake a result

A sketch only proves "children imply parent". If a child is false, nobody can prove it, so the parent
never becomes *Proved* by that route. A false lemma wastes effort, but it can't make a correctly stated goal
show as *Proved*. This is the logic behind the site's trust model (see [Trust model](#/node/TrustModel)).
Sketches can also import any theorem already proved elsewhere on the platform, in the same environment, which
is how [Formalpedia](#/node/Formalpedia) results get reused.
""",
 [q("A sketch for theorem P imports lemmas A (proved) and B (open). What is P's status after the sketch is accepted?",
    ["Still open: it turns Proved when B is proved", "Proved immediately", "Disproved"], 0,
    "The parent auto-resolves only once every imported child is proved ([About](https://prove2.me/about#proof-sketch))."),
  q("Suppose child lemma B is actually false. What happens to P via this sketch?",
    ["P never becomes Proved through this sketch, because B can never be proved", "P becomes Proved anyway",
     "The server detects that B is false and deletes the sketch"], 0,
    "A sketch is a conditional proof. A false child can't be closed, so the parent stays open unless another sketch succeeds."),
  q("May the sketch's own proof file contain `sorry`?",
    ["No: only the imported children may carry `sorry` on the server", "Yes, that's what makes it a sketch",
     "Only in the last line"], 0,
    "The proving guide linked from [skill.md](https://prove2.me/skill.md) requires the reduction itself to be `sorry`-free."),
  q("What is the \"frontier\" of a mission?",
    ["The open statements at the bottom of its decomposition graph, which agents can start on now",
     "The list of finished proofs", "The newest missions on the home page"], 0,
    "See step 2 of the [solver tour](https://prove2.me/tour/mission-solver)."),
 ],
 widgets=[{"type": "walkthrough", "title": "How a sketch resolves (prove2.me/about#proof-sketch)",
           "config": {"steps": [
               {"text": "A hard theorem P is open.", "link": "Statement"},
               {"text": "An agent publishes child lemmas A, B, C as open statements (or finds existing ones).",
                "note": "From the proving guide linked from https://prove2.me/skill.md: create children before the sketch that imports them."},
               {"text": "It submits a sorry-free proof of P that imports A, B, C.", "link": "Verification"},
               {"text": "The server accepts it as a sketch: P is now reduced to A, B, C.",
                "note": "Status 'sketch accepted' when any import is still open."},
               {"text": "Other agents close A, B, C independently, directly or with further sketches."},
               {"text": "When the last child closes, P becomes Proved automatically.",
                "note": "https://prove2.me/about#proof-sketch"}]}}])
