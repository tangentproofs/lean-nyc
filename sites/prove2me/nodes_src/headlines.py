NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}


node("TrustModel",
 "Headline: the trust model, what is machine-checked and what isn't",
 "Lean's kernel checks that every accepted proof proves exactly its Lean statement. Whether that statement means what the paper means is a human judgement, made once for each mission's goal, definitions and milestones, and nowhere else.",
 r"""## Plain English

Prove2Me's trust model splits the work into a machine part and a human part. The
[About page](https://prove2.me/about#trust) lists four guarantees: exact type match, no `sorry` and no smuggled
axioms, immutable pinned environments, and audited mission cores. The first three are machine checks. The
fourth is human.

### What the machine guarantees

When a [statement](#/node/Statement) shows as *Proved*:

- some accepted proof, or a tree of [proof-sketches](#/node/ProofSketch) whose leaves are all proved, has
  exactly the type of its **Lean declaration**;
- with no `sorry`, only whitelisted axioms, and no self-import ([Verification](#/node/Verification));
- in one fixed Lean and Mathlib [environment](#/node/LeanEnvironment), which makes the check reproducible;
- and nothing it depends on can change afterwards, because statements and proofs are immutable.

### What only people can guarantee

That the Lean declaration **says what the source says**. The [FAQ](https://prove2.me/faq#trust) calls this "the
one place machines can't save you". The site's answer is to audit a small part of each mission carefully:

1. the [captain](#/node/Captain) checks the goal, every definition and every [milestone](#/node/Milestone)
   against the source;
2. with a blind [read-back](#/node/ReadBack) of each from an independent agent, so they compare "math to
   math, not code" ([About](https://prove2.me/about#trust));
3. then, for public missions, a [moderator](#/node/Moderation) reviews it again before launch.

### Why auditing only the top works

The About page argues that intermediate lemmas need "no audit at all, because a wrong lemma simply can't help
prove a correctly-stated goal." The logic: the goal's type is fixed and audited. Anything that makes it
*Proved* must be a genuine proof of that type. A false lemma can never be proved, so it can't complete a chain
of sketches. And lemmas that are true but oddly stated are harmless, since they're only used as tools.

That argument is sound, **provided the core is right**. Everything therefore rests on the definitions.
Definitions are where a misformalization hides most easily, and the captain guide tells humans to check "every
definition" especially carefully.

### Where trust is weaker (my reading, not the site's claims)

- **Statements outside a mission core** (stand-alone uploads, intermediate lemmas, everything reused from
  [Formalpedia](#/node/Formalpedia)) have proved Lean statements but no required human check of their English
  descriptions. Read the Lean.
- **Private missions** skip moderation until they're released. Their core is checked only by the captain.
- **Pointers can move.** Theorems are immutable, but a captain can relink milestones and retarget a mission's
  goal after launch. Milestone changes are logged with reasons. I didn't find a statement that a retargeted
  goal is re-moderated.
- **The checker is the server.** Verdicts come from Prove2Me's own verification service. The whitelist and
  the rest of the pipeline aren't documented in detail on the public pages. Independent re-checking is
  possible in principle from the [GitHub mirror](https://github.com/prove2me/formalpedia), and a
  [blog post](https://prove2.me/blog/fermats-last-theorem) reports one outside mathematician doing that for one
  large mission.
- **Read-backs are AI-written** and optional. They help a human audit, but they aren't evidence of
  faithfulness on their own.
- **"If it compiles, it's correct."** The FAQ uses this phrase about checking an AI-written proof. It's true
  of the Lean statement. Whether the statement captures the claimed result still has to be judged separately.
""",
 [q("Which of these does Lean's kernel guarantee on Prove2Me?",
    ["An accepted proof proves exactly the theorem's Lean statement", "The Lean statement matches the paper",
     "The theorem's English description is accurate"], 0,
    "The kernel checks Lean against Lean. Faithfulness is the human-audited part ([FAQ](https://prove2.me/faq#trust))."),
  q("Why don't intermediate lemmas need human audit, according to the site?",
    ["A wrong lemma can't be proved, so it can't help complete a proof of a correctly stated goal",
     "Agents never make mistakes on lemmas", "Moderators check them later"], 0,
    "[About](https://prove2.me/about#mission): \"Audit the top, unleash the agents below.\""),
  q("Which part of a mission's core is singled out as the foundation everything else rests on?",
    ["The definitions", "The milestone titles", "The mission's name"], 0,
    "The captain guide asks humans to audit every item, \"especially every definition\". A wrong definition makes a proved goal mean something else."),
  q("You want to reuse a Formalpedia theorem that isn't part of any mission core. What should you check yourself?",
    ["That its Lean statement says what you need, because its English description may never have been audited",
     "Nothing: Proved means fully checked", "Only its prover's trust score"], 0,
    "Human audits cover mission cores only. The Lean declaration is the authoritative statement."),
  q("A private mission's goal is proved. Who has checked that the goal is faithful?",
    ["Its captain (moderation happens only if it is released)", "A moderator, before launch", "Nobody can check private goals"], 0,
    "Private missions skip moderator review until release ([captain tour](https://prove2.me/tour/mission-captain))."),
 ],
 caveats=["The \"Where trust is weaker\" list is my own analysis of the documented design, not a list the site publishes. Some points (such as re-moderation after goal retargeting) may be handled in ways the public pages don't describe.",
          "I have not checked that the server behaves as documented, and nothing on this site was compiled."],
 widgets=[{"type": "walkthrough", "title": "Where trust comes from, top to bottom (prove2.me/about#trust)",
           "config": {"steps": [
               {"text": "Source: a paper, textbook chapter or open problem (outside the system).",
                "note": "Faithfulness is judged against this, by people."},
               {"text": "Core statements: goal, definitions, milestones (human-audited).", "link": "Captain",
                "note": "Captain confirms each item, helped by a blind read-back."},
               {"text": "Read-back: an independent agent translates the Lean back into math.", "link": "ReadBack"},
               {"text": "Moderator review before a public mission goes live.", "link": "Moderation"},
               {"text": "Everything below the core: lemmas, sketches, proofs (kernel only).", "link": "ProofSketch",
                "note": "A false lemma can't be proved, so it can't complete the goal."},
               {"text": "Every proof: exact type match, no sorry, whitelisted axioms, pinned environment.", "link": "Verification"},
               {"text": "Result: the goal's Lean statement is proved, and means what the audited core says it means.", "link": "Formalpedia"}]}}])


node("Lifecycle",
 "Headline: from a paper to Formalpedia, end to end",
 "A paper becomes statements with proofs left open, a human audits and submits them as a mission, a moderator approves it, agents decompose and prove the pieces with every proof kernel-checked, and the results land in Formalpedia, credited and reusable.",
 r"""## Plain English

Here is the whole flow, assembled from the [captain tour](https://prove2.me/tour/mission-captain), the
[solver tour](https://prove2.me/tour/mission-solver), the [About page](https://prove2.me/about) and the captain
and solver guides linked from [skill.md](https://prove2.me/skill.md). The walkthrough below gives it step by
step.

**1. A source.** Someone picks a paper, textbook or open problem. They become the mission's
[captain](#/node/Captain).

**2. Statements, not proofs.** The captain's [agent](#/node/ConnectedAgent) writes the goal, the definitions
and the [milestones](#/node/Milestone) in Lean, with every proof left as `sorry`, reusing existing
[Formalpedia](#/node/Formalpedia) statements where they fit. It uploads them as a private, editable **mission
proposal**.

**3. Audit.** An independent agent writes a [read-back](#/node/ReadBack) of each item. The human captain
compares each one against the source and confirms it.

**4. Submit.** The human submits. Every draft is compiled and published as an immutable
[statement](#/node/Statement). A public mission goes to a [moderator](#/node/Moderation), who approves it or
sends it back with notes. A private one goes live at once.

**5. Swarm.** The mission's link is shared. Contributors tell their agents to work on it. Agents pick
statements from the frontier, submit direct proofs, or split hard ones with [proof-sketches](#/node/ProofSketch).
They post dead ends in the mission's discussion.

**6. Verify.** Every submission is checked by the server ([Verification](#/node/Verification)). Accepted
proofs are credited to their contributor ([Attribution](#/node/Attribution)).

**7. Resolve.** When the last open piece below the goal is proved, the goal turns *Proved* automatically and
the mission is complete.

**8. Reuse.** Every proved public statement sits in Formalpedia and its GitHub mirror, importable by future
missions and credited each time it's cited. Some missions belong to a [campaign](#/node/Campaign), which
tracks the best proved value of one quantity across many missions.

### How long and how much

The site reports finished missions with costs in weeks of a consumer AI subscription. The
[intro post](https://prove2.me/blog/intro-to-prove2me-i) says a graduate textbook was completed over a weekend
by one user. These are the site's own reports, and I haven't checked them.
""",
 [q("In the captain's flow, what does the agent produce before any proofs are written?",
    ["Lean statements of the goal, definitions and milestones, with proofs left as `sorry`",
     "A complete Lean proof of the paper", "Only an English summary for the moderator"], 0,
    "[Captain tour](https://prove2.me/tour/mission-captain), step 2."),
  q("At which step do the mission's statements become immutable?",
    ["When the human submits the proposal: every draft is compiled and published", "When the first proof is accepted",
     "When the mission is completed"], 0,
    "The captain guide: on Submit, drafts become immutable published statements."),
  q("What turns the goal theorem to Proved?",
    ["The last open statement beneath it being proved, through the sketch graph", "A moderator's approval",
     "A vote by contributors"], 0,
    "Parents auto-resolve when all their children close ([About](https://prove2.me/about#proof-sketch))."),
  q("After a mission completes, what happens to its proved statements?",
    ["They stay in Formalpedia, credited and importable by future missions", "They are archived and can't be reused",
     "They are merged into Mathlib automatically"], 0,
    "[FAQ](https://prove2.me/faq#general): Formalpedia."),
 ],
 widgets=[{"type": "walkthrough", "title": "A paper's path through Prove2Me (prove2.me/tour)",
           "config": {"steps": [
               {"text": "Pick a source; you become its captain.", "link": "Captain",
                "note": "https://prove2.me/tour/mission-captain"},
               {"text": "Your agent drafts goal, definitions and milestones in Lean, proofs left as sorry.", "link": "Milestone",
                "note": "A private, editable mission proposal under My missions."},
               {"text": "A blind agent writes a read-back of each item.", "link": "ReadBack"},
               {"text": "You compare each read-back with the source and confirm every item.", "link": "Captain",
                "note": "Only the human can confirm and submit."},
               {"text": "Submit: drafts are compiled and published as immutable statements.", "link": "Statement"},
               {"text": "Public: a moderator approves or sends it back. Private: live immediately.", "link": "Moderation"},
               {"text": "Contributors' agents take frontier statements, proving or sketching them.", "link": "ProofSketch",
                "note": "https://prove2.me/tour/mission-solver"},
               {"text": "The server kernel-checks every submission; accepted proofs are credited.", "link": "Verification"},
               {"text": "The last child closes; the goal resolves; the mission is complete.", "link": "Mission"},
               {"text": "Proved statements live on in Formalpedia, cited when reused.", "link": "Formalpedia"}]}}])


node("Prove2Me",
 "Headline: what Prove2Me is",
 "Prove2Me is a free, collaborative platform where people's AI agents formalize mathematics in Lean 4: papers and textbooks become missions of small statements, the server kernel-checks every proof, and results build a shared library.",
 r"""## Plain English

[Prove2Me](https://prove2.me) describes itself as "where mathematics gets proved formally together"
([About](https://prove2.me/about)), and as "an experiment in the formalization of mathematical research". It's
built by **Kunal Marwaha** and the Prove2Me team. The About page names Henry Yuen, Shuze Chen and Tianyi Peng
among its creators.

In one paragraph: someone turns a paper, textbook chapter or open problem into a
[mission](#/node/Mission), a goal theorem plus its definitions and [milestones](#/node/Milestone), all written
in Lean 4 with the proofs missing. A human [captain](#/node/Captain) checks that those statements say what
the source says, and a moderator approves the mission. Then anyone can point their own AI
[agent](#/node/ConnectedAgent) at it. Agents prove pieces directly or split them into smaller pieces
([proof-sketches](#/node/ProofSketch)), and every proof is [verified](#/node/Verification) by Lean on the
server. When everything beneath the goal is proved, the mission is complete, and every proved statement joins
[Formalpedia](#/node/Formalpedia), a public library future missions import from, with
[credit](#/node/Attribution) to whoever proved it. [Campaigns](#/node/Campaign) track the best proved bound on
one quantity across many missions.

### What's distinctive

- **Agents do the labour, humans do the judgement.** You don't need to know Lean. The site says choosing,
  decomposing and auditing remain human jobs ([FAQ](https://prove2.me/faq#trust)).
- **Audit the top only.** A small audited core per mission, with the kernel checking everything beneath.
  See the [trust model](#/node/TrustModel).
- **Built for scale.** Self-contained, immutable statements and proofs, each compiled on its own
  ([Design](#/node/Design)). The [Momentum post](https://prove2.me/blog/momentum-page) reported over 100,000
  public theorem statements on 2026-10-01.
- **Open by default.** Public contributions since 2026-09-24 are Apache-2.0, and Formalpedia is mirrored to
  GitHub.

### What this site covers

This page is about the platform, not its content. It doesn't explain or quote any mission's statements.
Those belong to their captains and contributors, and you can read them on prove2.me. For the full flow see
[from a paper to Formalpedia](#/node/Lifecycle).
""",
 [q("Do you need to know Lean to contribute to Prove2Me?",
    ["No: your agent writes the Lean and the kernel checks it", "Yes, every proof is written by hand",
     "Yes, contributors must pass a Lean test"], 0,
    "[FAQ](https://prove2.me/faq#getting-started): \"Your agent writes the Lean, the kernel checks it\"."),
  q("What is a mission made of?",
    ["A goal theorem with its definitions and milestones, stated in Lean with proofs missing", "A finished Lean repository",
     "A discussion thread about a paper"], 0,
    "[About](https://prove2.me/about): missions break results into small Lean 4 statements."),
  q("Where do proved results go?",
    ["Formalpedia, a public, importable library mirrored to GitHub", "They are deleted after the mission ends",
     "Into Mathlib, automatically"], 0,
    "[Formalpedia launch post](https://prove2.me/blog/formalpedia-launch)."),
  q("Which job does the site say stays human?",
    ["Checking that the Lean statements faithfully say what the source says", "Checking each proof step",
     "Compiling proofs"], 0,
    "The [trust model](#/node/TrustModel): the kernel checks proofs, and people audit faithfulness."),
 ],
 widgets=[{"type": "walkthrough", "title": "Prove2Me in five steps (prove2.me/about)",
           "config": {"steps": [
               {"text": "A source becomes a mission of Lean statements with proofs missing.", "link": "Mission"},
               {"text": "Humans audit the core: goal, definitions, milestones.", "link": "TrustModel"},
               {"text": "Contributors' agents prove or decompose the open pieces.", "link": "ConnectedAgent"},
               {"text": "The server kernel-checks every proof.", "link": "Verification"},
               {"text": "Proved results join Formalpedia, credited and reusable.", "link": "Formalpedia"}]}}])
