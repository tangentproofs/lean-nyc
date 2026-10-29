NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]

GH = "https://github.com/VIDA-NYU/Lea/blob/a5924f6f15b980452731b6edfe00feee97791ab4/"
PY = GH + "apps/lea-standalone/prover/lea/"

# ---------------------------------------------------------------- headline

node("runMain",
 "Headline: how a finished proof is audited (SafeVerify)",
 "SafeVerify is a Lean program, not a theorem. It re-checks every proof with the kernel in a fresh environment, requires names and types to match a target, and allows only the three standard axioms. In Lea the target is built from the submission itself, so a weakened statement still passes.",
 r"""## Plain English

**Program (`runMain`, SafeVerify/Main.lean lines 367–433).** SafeVerify takes two compiled Lean files (`.olean`):

- a **target**, the trusted specification, with `sorry` in place of the proofs;
- a **submission**, which is supposed to fill in those proofs.

It succeeds only if **every** declaration in the target has a counterpart in the submission with the same name,
kind and type, every proof survives a fresh kernel check, and nothing depends on an axiom other than `propext`,
`Quot.sound` and `Classical.choice` (SafeVerify/Main.lean line 355). If any check fails, it exits with an error
(lines 423–430).

This is the most "Lean" part of the project: the checker is written in Lean and works on Lean's own data
structures. It is a **program** and has no correctness proof. When this site says it "catches" something, it
means "the code is written to reject it".

### Who wrote it

SafeVerify is by GasStationManager (github.com/GasStationManager/SafeVerify, Apache-2.0, adapted from
`lean4checker`). Lea vendors a copy at `apps/lea-standalone/prover/third_party/SafeVerify`. One later Lea commit
added the option to audit a single selected declaration (lines 404–413).

### How Lea uses it

Lea's own success test is weaker: the file compiles, with no error and no "declaration uses sorry" warning
([tools.py lines 555–567](""" + PY + r"""tools.py#L555-L567)). When a result is selected, Lea also checks its axioms against the
same three-axiom list, using the [inspector](#/node/LeaLibraryInspector.inspect)
([result_selection.py lines 108–123](""" + PY + r"""result_selection.py#L108-L123)). SafeVerify is an extra, opt-in audit
([tools.py lines 909–957](""" + PY + r"""tools.py#L909-L957)) and reports "unavailable" if it was not built,
which the install's `--skip-verify` option does on purpose.

To audit a finished file, Lea builds the target **from the submission**, by replacing every theorem's proof
with `sorry` and keeping everything else ([safeverify.py lines 9–17](""" + PY + r"""safeverify.py#L9-L17)).
The module's own docstring says what follows: this catches a tampered *proof* or a redefined supporting
definition, but **a weakened statement passes**, because the target inherits it. Checking that the Lean
statement says what the mathematician meant stays a human job.
""",
 [q("What are SafeVerify's two inputs?",
    ["A compiled target (statements with sorry) and a compiled submission (the proofs)",
     "A LaTeX file and a Lean file",
     "A Lean file and a list of allowed tactics",
     "Two versions of Mathlib"], 0,
    "SafeVerify/Main.lean lines 350–353 read the two positional arguments, and the replays at lines 382–384 load them."),
  q("Which axioms may a submission depend on?",
    ["propext, Quot.sound and Classical.choice", "Any axiom declared in Mathlib", "None at all", "Any axiom, as long as it is not sorry"], 0,
    "SafeVerify/Main.lean line 355."),
  q("In Lea's integration, where does the target come from?",
    ["From the submission itself, with every theorem's proof replaced by sorry",
     "From a separate file a human wrote and froze in advance",
     "From the LaTeX source"], 0,
    "safeverify.py lines 9–17 (Python, linked above)."),
  q("So which of these could pass Lea's SafeVerify audit?",
    ["A correct proof of a weaker statement than the one the user asked for",
     "A proof that uses sorry",
     "A proof that adds a new axiom",
     "A proof that tampers with the environment to add a fake theorem"], 0,
    "The target inherits the submission's statement, so a weaker statement is compared with itself. The other three are what SafeVerify is built to reject."),
  q("Is SafeVerify itself proved correct in Lean?",
    ["No. It is a Lean program with tests, not a verified checker", "Yes, the repository contains its correctness proof"], 0,
    "Its Lean files define functions (SafeVerify/Main.lean) and test fixtures (SafeVerifyTest/). There are no theorems about the checker."),
 ],
 caveats=["This is a program, not a theorem. Nothing about it was run or built for this site. The descriptions come from reading the code and its README.",
          "SafeVerify's own README lists what it doesn't check: `implemented_by` / `extern` tricks and code that runs during compilation. The copy here does reject unsafe constants, and partial ones when asked (lines 130–133).",
          "The vendored README in third_party/ says the copy was pinned to Lean v4.28.0, but the copy's own toolchain file says v4.29.0. The note looks out of date."],
 widgets=walk("How the check goes (SafeVerify/Main.lean, lines 367-433)", [
  {"text": "Read the settings: the two files, the flags, and the allowed axioms propext, Quot.sound and Classical.choice (lines 372, 350–357)."},
  {"text": "Import check: the submission must (transitively) import everything the target imports, so it can't swap out a definition the statement relies on (lines 375–378; checkImportSuperset at lines 205–227)."},
  {"text": "Replay the target and then the submission through the kernel, in an environment rebuilt only from their imports (lines 380–384).", "link": "replayFile"},
  {"text": "If a target name lives in one of the submission's imports instead of the file itself, look it up there (lines 386–398)."},
  {"text": "Reject new declarations whose number literals look corrupted, a sign of unsafe casts (line 401; lines 244–260)."},
  {"text": "Optionally narrow the audit to one selected declaration, the option Lea added (lines 403–413)."},
  {"text": "Record every submission declaration that uses a disallowed axiom, then compare each target declaration with its counterpart (line 416; runSafeVerify at lines 304–341).", "link": "checkTargets"},
  {"text": "Fail if any comparison failed or any axiom violation was recorded. Otherwise print 'passed' (lines 423–433)."},
 ]))

# ---------------------------------------------------------------- supporting

node("replayFile",
 "Replaying a compiled file through the kernel",
 "Load the compiled file's declarations into an environment rebuilt from its imports alone, re-add them one by one through the kernel, and type-check every proof again from a freshly copied term. Any tampering with Lean's environment at compile time is lost in this rebuild.",
 r"""## Plain English

**Function (`replayFile`, SafeVerify/Main.lean lines 121–149).** Given a compiled `.olean` file:

1. Read its declarations, and build a fresh environment from **its imports only** (lines 125–126). Anything
   the file did to the environment while it compiled, such as inserting a fake theorem or redefining an axiom,
   is not carried over.
2. Refuse any `unsafe` declaration, and any `partial` one if that flag is set (lines 129–133).
3. Copy every term node by node (`sanitizeConstant`, lines 107–117) and **replay** the declarations into the
   fresh environment (line 135). Replay re-runs the kernel's checks on each one, as `lean4checker` does.
4. Type-check every theorem's proof again with the kernel and confirm that it proves the declared type
   (lines 138–148).
5. Collect each theorem and definition with the axioms it depends on ([checkAxioms](#/node/checkAxioms) uses
   that list).

A second version, `replayFileWithEnv` (lines 163–191), does the same and also returns the environment. The
submission is replayed with that one.

The test files [falseThm](#/node/falseThm) and [efsq](#/node/efsq) are attacks that this replay is meant to
defeat.
""",
 [q("Which environment are declarations replayed into?",
    ["A fresh one built only from the file's imports", "The environment the file was compiled in", "An empty environment with no imports"], 0,
    "SafeVerify/Main.lean line 126. Anything the file changed while compiling is gone."),
  q("What happens to an `unsafe` declaration?",
    ["SafeVerify stops with an error", "It is skipped", "It is allowed"], 0, "Lines 130–131."),
  q("Why re-check theorem proofs after the replay?",
    ["As an extra guard: proof terms are rebuilt from scratch and kernel-checked against their declared types", "To compute axioms", "It's needed to print them"], 0,
    "Lines 137–148. The comments mention corrupted terms produced by unsafe casts as the threat."),
 ])

node("checkTargets",
 "Matching each target declaration with the submission",
 "For every declaration in the target, find the declaration of the same name in the submission and require the same kind and the same type. Definitions must also keep the same body unless the target's version used sorry. Every match must use only allowed axioms.",
 r"""## Plain English

**Function (`checkTargets`, SafeVerify/Main.lean lines 55–77, with `Info.toFailureMode` at lines 38–52).** For each
declaration *d* in the target:

- **Not found** in the submission: failure.
- **Different kind** (for example a theorem in the target but a definition in the submission): failure.
- **Theorem**: the types must be [identical](#/node/equivThm). The proof can be anything that passed the replay.
- **Definition**: same type. Same body as well, *unless* the target's body depends on `sorry`, in which case the
  submission may fill it in freely (line 44). So a finished definition can't be quietly changed, but a
  placeholder can be completed.
- **Opaque constants, inductive types and their constructors** get their own comparisons (lines 46–49 and
  61–71).
- Finally, the submission's version must [use only allowed axioms](#/node/checkAxioms) (lines 50–51).

The possible failures are listed as `CheckFailure` in SafeVerify/Types.lean lines 26–45.

Declarations that are in the submission but **not** in the target (helper lemmas, for instance) aren't matched
against anything. They are still kernel-replayed and axiom-checked.
""",
 [q("A target theorem has a proof of `sorry`. What must the submission's theorem of the same name have?",
    ["The identical type, and a proof that passes replay using only allowed axioms",
     "Any type, as long as the proof is complete",
     "The same proof term as the target"], 0,
    "SafeVerify/Main.lean lines 40–41 and 50–51."),
  q("A target definition is complete (no sorry). Can the submission change its body?",
    ["No. The bodies must match", "Yes, as long as the type matches"], 0,
    "Line 44: bodies are compared whenever the target's definition doesn't use sorry."),
  q("What happens to an extra helper lemma that appears only in the submission?",
    ["It isn't matched to anything, but it is still replayed and axiom-checked", "It causes a failure", "It is ignored entirely"], 0,
    "The matching loops over the target (lines 61–76). The axiom scan in runSafeVerify loops over the submission (lines 310–314)."),
 ])

node("equivThm",
 "When two theorem statements count as the same",
 "Two theorems match when their names, universe parameters and types are syntactically identical as kernel terms. Statements that are merely logically equivalent don't count.",
 r"""## Plain English

**Function (`equivThm`, SafeVerify/Util.lean lines 9–15).** The target's theorem and the submission's match exactly
when they have the same name, the same universe parameters, the same type as a kernel term, and the same list of
mutually defined companions.

The comparison is **syntactic**. "For all *n*, *n* + 0 = *n*" and "for all *m*, *m* = *m* + 0" are different
statements here, even though each implies the other. That is on purpose: the point is that the submission proves
**exactly** the target statement.

Lea's Python wrapper notes one false-alarm class this creates (universe parameters with different names) and
accepts that case itself ([safeverify.py lines 28–31](""" + PY + r"""safeverify.py#L28-L31)).

The test case in SafeVerifyTest/OverwrittenTypeclass/Bad.lean shows why syntactic matching helps. The
submission adds a type-class instance before stating the theorem (line 15), so the elaborated statement picks up
a different instance and no longer matches the target.
""",
 [q("Do two logically equivalent but differently written statements match?",
    ["No. The types must be identical kernel terms", "Yes, if Lean can prove them equivalent"], 0,
    "SafeVerify/Util.lean lines 12–15 compare with plain equality."),
  q("Why is syntactic matching the right choice for an audit?",
    ["It forces the submission to prove exactly the trusted statement, not a convenient variant", "It's faster, and that's the only reason", "It allows weaker statements"], 0,
    "Any slack in the comparison would be room to prove something else."),
  q("In the OverwrittenTypeclass test, what makes the Bad submission fail?",
    ["An extra instance changes the elaborated statement, so the types differ", "It uses sorry", "It adds an axiom"], 0,
    "SafeVerifyTest/OverwrittenTypeclass/Bad.lean lines 15 and 19–21. The test runner expects every Bad file to fail."),
 ])

node("checkAxioms",
 "The axiom whitelist",
 "A declaration passes when every axiom it depends on, directly or through what it uses, is on the allowed list. Lean's sorry is itself an axiom, so it fails this test automatically.",
 r"""## Plain English

**Function (`checkAxioms`, SafeVerify/Main.lean lines 33–36).** Each declaration comes with the list of axioms it
depends on, computed by Lean's own axiom collector during the replay (lines 17–23). The check passes when every
one of them is allowed. By default the allowed list is `propext` (propositional extensionality), `Quot.sound`
(quotient soundness) and `Classical.choice` (line 355), Lean's three standard axioms.

This is what rules out:

- `sorry`, which Lean records as the axiom `sorryAx`;
- any **new** axiom the submission declares, however harmless it looks;
- proofs by `native_decide`, which rely on an extra axiom that trusts the compiler.

It is the same information that `#print axioms` shows. The Overleaf demo's reference file ends with a block of
those commands for exactly this purpose (see [the demo node](#/node/LeaDemoReference.original_square_claim_is_false)).
""",
 [q("Why does a proof containing `sorry` fail this check?",
    ["`sorry` is recorded as the axiom sorryAx, which is not on the allowed list", "Because SafeVerify searches the text for the word sorry"], 0,
    "The check works on axiom dependencies (SafeVerify/Main.lean lines 33–36), not on source text."),
  q("Is Classical.choice allowed?",
    ["Yes. It is one of Lean's three standard axioms", "No. Only constructive proofs pass"], 0, "SafeVerify/Main.lean line 355."),
  q("Is the dependency check direct only, or transitive?",
    ["Transitive: an axiom used by a lemma that the proof uses counts too", "Direct only"], 0,
    "Lean's axiom collector follows all constants a declaration uses (lines 17–23)."),
 ])

node("falseThm",
 "Test attack: inserting a fake theorem into the environment",
 "A test file uses metaprogramming to slip a 'proof' of False into Lean's environment without the kernel checking it, then 'proves' False with it. The fresh replay is meant to reject this.",
 r"""## Plain English

**Test fixture (SafeVerifyTest/AddFalse/Bad.lean lines 1–17).** The target (SafeVerifyTest/AddFalse/Target.lean
line 1) asks for a proof of False, with `sorry`. The "Bad" submission defines a command that edits Lean's
environment directly and inserts a theorem named `false` whose statement is False and whose "proof" is the
proposition False itself, which is not a proof of anything (lines 5–12). The kernel never sees that insertion.
The submission then proves False by citing it (lines 16–17).

An ordinary compile can be fooled by this kind of trick, because the edit skips the kernel. SafeVerify
[replays](#/node/replayFile) the file's declarations through the kernel in a clean environment, where the fake
theorem must be type-checked like everything else and fails. The test runner expects every `Bad.lean` to fail
(SafeVerify/scripts/run_tests.sh, which this site didn't run).

A sibling fixture (SafeVerifyTest/AddFalseConstr/Bad.lean lines 5–24) does the same with a fake *constructor*
for False.
""",
 [q("Why can't an ordinary compile be trusted against this file?",
    ["The fake theorem is added by editing the environment directly, which skips the kernel", "Because it uses sorry", "Because it adds an axiom"], 0,
    "SafeVerifyTest/AddFalse/Bad.lean lines 6–12."),
  q("What does SafeVerify do that defeats it?",
    ["It replays every declaration through the kernel in a fresh environment", "It bans the word 'false'", "It counts lines of code"], 0,
    "See [replayFile](#/node/replayFile), SafeVerify/Main.lean lines 125–135."),
  q("What is the expected outcome for this Bad file?",
    ["Fail", "Pass"], 0, "The runner expects Good files to pass and Bad files to fail."),
 ])

node("efsq",
 "Test attack: 'proving' Fermat's Last Theorem by redefining an axiom",
 "A test file rewrites Lean's propext axiom to say False, then 'proves' Fermat's Last Theorem from it. The proof depends only on an allowed axiom name, so a whitelist alone would accept it. The replay in a clean environment is what catches it.",
 r"""## Plain English

**Test fixture (SafeVerifyTest/ReplaceAxiom/Bad.lean lines 1–38).** The target (SafeVerifyTest/ReplaceAxiom/Target.lean
lines 2–5) states Fermat's Last Theorem for natural numbers: no positive *x*, *y*, *z* satisfy *x*ⁿ + *y*ⁿ = *z*ⁿ with
*n* > 2. The proof is `sorry`.

The Bad submission edits Lean's environment so that the standard axiom `propext` now claims False (lines 8–27).
Then it "proves" the theorem by deriving False from that fake axiom (lines 29–33). Lean's `#print axioms`
reports that the theorem depends only on `propext` (lines 35–38), which is **on** the allowed list.

So an axiom whitelist by itself would wave this through. What stops it is the [replay](#/node/replayFile): the
clean environment has the real `propext` (which says that equivalent propositions are equal), the "proof" no
longer type-checks, and the kernel rejects it.

This is a good illustration of why SafeVerify works on compiled files and re-checks everything, rather than
trusting what the compiler reported.
""",
 [q("Which axiom does the fake proof report depending on?",
    ["propext, which is on the allowed list", "sorryAx", "A new axiom named efsq"], 0,
    "SafeVerifyTest/ReplaceAxiom/Bad.lean lines 35–38."),
  q("Why doesn't the axiom whitelist catch it?",
    ["The name is allowed. Only its content was changed, and only in the compile-time environment", "The whitelist is turned off for tests"], 0,
    "Lines 8–27 change what propext says, not its name."),
  q("What catches it?",
    ["Replaying into a fresh environment, where propext has its real statement", "Searching for the word Fermat"], 0,
    "SafeVerify/Main.lean lines 125–135."),
 ])

node("LeaLibraryInspector.inspect",
 "The library inspector: Lean reporting on its own declarations",
 "A small Lean metaprogram that Lea appends to files so that Lean itself reports each declaration's kind, type, axioms, dependencies and line range as JSON. It proves nothing. It is how the Python side learns what a file contains without parsing Lean.",
 r"""## Plain English

**Function (`inspect`, lea/LibraryInspect.lean lines 37–76).** For one declaration, produce a JSON record with
its full name, whether it is private, its kind (theorem, axiom, definition, inductive type, …), its pretty-printed
type, a structural encoding of its type and body (lines 9–35), the axioms it depends on, the constants it
uses, and its line range.

Three commands wrap it (lines 80–110): inspect every declaration of a compiled module, inspect one named
declaration, or inspect everything defined in the current source up to a given line. That last one is useful
when the inspector is appended to a file being checked, so it reports on the file and not on itself
(comment at lines 100–101).

The header comment (lines 3–4) says it is for compiler inspection only and changes no project declarations.
On the Python side, the records feed Lea's project library. Result selection rejects a result whose axiom
list goes beyond `propext`, `Quot.sound` and `Classical.choice`
([result_selection.py lines 108–123](""" + PY + r"""result_selection.py#L108-L123)). This site didn't trace
the rest of that Python code.
""",
 [q("Does the inspector prove any theorems?",
    ["No. It is a metaprogram that reports facts about declarations", "Yes, it proves each declaration is correct"], 0,
    "lea/LibraryInspect.lean lines 37–76 build JSON."),
  q("Which of these does an inspection record include?",
    ["The axioms the declaration depends on", "The proof's running time", "The LaTeX source it came from"], 0, "Line 58 and line 75."),
  q("Why does the source-local command take a line cutoff?",
    ["So that, when the inspector is appended to a file, it reports only the file's own declarations", "To limit output size", "To skip private names"], 0,
    "Comment at lines 100–101."),
 ])

node("checkImportSuperset",
 "Import check: the submission must import everything the target does",
 "Before any replay, SafeVerify requires the submission to import, directly or indirectly, every module the target imports, and both files to import Lean's standard prelude. This blocks a submission that drops an import in order to redefine a type the statement uses.",
 r"""## Plain English

**Function (`checkImportSuperset`, SafeVerify/Main.lean lines 200–227).** Both files' imports are expanded to
the full set of modules they pull in (lines 212–217). Every module the target needs must also be loaded by
the submission (lines 218–227). In addition, the target must import `Init` (Lean's core library) and the
submission must import something (lines 207–211). A file with no imports at all could otherwise supply its own
versions of basic types.

The docstring (lines 200–204) names the attack: leave out an import and redefine a type under the same name,
so a statement that *looks* identical refers to something else.
""",
 [q("What does the import check require?",
    ["Every module the target transitively imports is also imported by the submission", "The two files have identical import lines", "The submission imports nothing"], 0,
    "SafeVerify/Main.lean lines 218–227."),
  q("Why refuse a submission with no imports?",
    ["It could define its own versions of core types and make a matching-looking statement mean something else", "It would be too slow", "Lean can't compile it"], 0,
    "SafeVerify/Main.lean lines 210–211."),
  q("When does this check run?",
    ["Before the replays", "After the axiom check", "Only in verbose mode"], 0,
    "SafeVerify/Main.lean lines 375–378, before the replay at line 382."),
 ])

node("runSafeVerify",
 "The main comparison pass",
 "Scan every submission declaration for disallowed axioms, then match every target declaration against the submission, and print each problem found.",
 r"""## Plain English

**Function (`runSafeVerify`, SafeVerify/Main.lean lines 304–341).** Two passes over the replayed declarations:

1. **Axioms** (lines 309–314): every declaration in the submission, including extra helper lemmas, is checked
   with [checkAxioms](#/node/checkAxioms). Each violation is recorded with the offending axioms.
2. **Matching** (line 317): [checkTargets](#/node/checkTargets) compares each target declaration with its
   counterpart.

Then it prints each failure (lines 320–340), with more detail in verbose mode. The decision to pass or fail is
made afterwards, in [runMain](#/node/runMain).
""",
 [q("Does the axiom scan cover helper lemmas that only the submission has?",
    ["Yes. It loops over all submission declarations", "No. Only target names are checked"], 0,
    "SafeVerify/Main.lean line 310."),
  q("Where is the final pass/fail decision made?",
    ["In runMain, after this pass returns", "Inside this function"], 0,
    "SafeVerify/Main.lean lines 423–433."),
  q("What are the two passes?",
    ["An axiom scan, then target-by-target matching", "Compilation, then execution", "Parsing, then pretty-printing"], 0,
    "SafeVerify/Main.lean lines 309–317."),
 ])

node("Info.toFailureMode",
 "Classifying one mismatch",
 "Given a target declaration and the submission's declaration of the same name, return the first problem found: wrong kind, different theorem type, changed definition, changed opaque constant or constructor, or a disallowed axiom. Return no problem if all checks pass.",
 r"""## Plain English

**Function (`Info.toFailureMode`, SafeVerify/Main.lean lines 38–52).** The checks run in order (lines 39–51), and the
first failure is reported:

1. same kind (theorem, definition, …);
2. for a theorem, the [same type](#/node/equivThm);
3. for a definition, the same type, and the same body unless the target's body used `sorry`;
4. for an opaque constant or a constructor, the matching comparison;
5. only [allowed axioms](#/node/checkAxioms).

Inductive types are handled separately, in [checkTargets](#/node/checkTargets), because comparing them needs
access to all constructors.
""",
 [q("When may a submission's definition body differ from the target's?",
    ["Only when the target's definition depends on sorry", "Always", "Never"], 0,
    "SafeVerify/Main.lean lines 43–44."),
  q("Which check comes first?",
    ["That both declarations have the same kind", "The axiom check", "The body comparison"], 0,
    "SafeVerify/Main.lean lines 39–40."),
  q("Where are inductive types compared?",
    ["In checkTargets, which needs the full tables to look up constructors", "Here", "Nowhere"], 0,
    "SafeVerify/Main.lean lines 61–71."),
 ])
