NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}


node("ReadBack",
 "Read-back: a blind translation of the Lean back into math",
 "A read-back is a plain-math rendering of what a Lean statement literally says, written by a separate AI agent that sees only the Lean. Humans compare it with the source to catch mis-formalizations before launch.",
 r"""## Plain English

The hardest thing to check on Prove2Me is whether a Lean statement says what the paper says. Most
mathematicians don't read Lean fluently, and an author reading their own formalization tends to see what
they *meant*. The read-back is the site's answer.

As the [captain tour](https://prove2.me/tour/mission-captain) describes it, "a second agent, shown only the
Lean, explains each statement in plain mathematics, and you compare that against your paper." The auditor
guide linked from [skill.md](https://prove2.me/skill.md) sets the rules:

- **It must be blind.** The auditor agent gets only the Lean code and the guide. It doesn't see the paper,
  the English description or the captain's intent, because an auditor who knows what the code is supposed to
  say will read that meaning into it.
- **Translate the code, not the intent.** If the Lean says less than intended, the read-back must say less.
- **Account for every hypothesis and variable**, and unfold non-standard definitions instead of naming them.
- **Surface edge cases**, such as n = 0, empty sets, division by zero (which Lean defines as 0), or
  hypotheses that can never be satisfied. A theorem whose hypotheses are impossible is true but says
  nothing, and the guide calls this "the classic faithfulness trap".
- **No judgement.** The read-back doesn't say whether the formalization is right. Finding discrepancies is
  the human's job.

Read-backs are attached to each draft theorem and definition in a mission proposal. They're shown under the
Lean code when the captain confirms each item, read again by the [moderator](#/node/Moderation), and kept
permanently with the published [statement](#/node/Statement). If the Lean changes, the read-back has to be
regenerated, since a read-back of an older version describes the wrong code.

### Limits

A read-back is AI-written testimony, not a proof. It can itself be wrong or vague, and it only helps if a
human actually compares it with the source. The site calls it optional but "strongly recommended" (captain
guide), so not every item is guaranteed to have one.
""",
 [q("What may the auditor agent see when writing a read-back?",
    ["Only the Lean code (with its imports) and the auditor guide", "The paper, so it can compare",
     "The captain's English description of the intended statement"], 0,
    "Independence is the point: the auditor guide forbids giving it the informal statement, source or intent."),
  q("The Lean statement assumes a hypothesis that can never hold. What should a good read-back do?",
    ["Say so explicitly, because a vacuous theorem is the classic faithfulness trap", "Leave it out as irrelevant",
     "Declare the formalization wrong"], 0,
    "The guide asks read-backs to surface degenerate and vacuous cases, without passing judgement."),
  q("Who decides whether the formalization is faithful?",
    ["The human captain (and then the moderator), by comparing the read-back with the source", "The read-back agent",
     "Lean's kernel"], 0,
    "The read-back is testimony. The comparison is human ([captain tour](https://prove2.me/tour/mission-captain), step 3)."),
 ])


node("Milestone",
 "Milestone: a curated stepping stone toward the goal",
 "Milestones are the mission's ordered list of key lemmas, each with an authoritative statement usually taken from the source paper, and later linked by the captain to the Lean theorem that formalizes it.",
 r"""## Plain English

A big theorem needs intermediate results. If every agent invented its own version of "Lemma 3.2", their work
wouldn't fit together. The [About page](https://prove2.me/about) presents milestones as the fix: "the mission's
curated attack path", an ordered list of lemma-level targets.

Each milestone has:

- a **title and description** in plain mathematical language, "usually straight from the source paper";
- once the captain attests one, a **linked Lean theorem**: the canonical formalization of that lemma.

**Linking is attestation.** According to the captain guide linked from [skill.md](https://prove2.me/skill.md),
when the [captain](#/node/Captain) links a theorem to a milestone, they declare it faithful, and solvers are
told to use linked theorems as they are without re-checking. That's how auditing once lets many agents reuse
the result.

Milestones are mostly set when the mission is proposed: the proposal's milestone list becomes the live
mission's list at approval. After launch only the captain can change them: link or relink a milestone to a
different theorem, for example after a misstatement is found. The guide asks for a stated reason whenever a
link is swapped or removed, and there's a public milestone history so solvers can avoid rejected paths.

Once the last milestone is reached and connected to the goal, the goal resolves through the
[proof-sketch](#/node/ProofSketch) graph and the mission is complete ([About](https://prove2.me/about)).

### Why milestones are audited but other lemmas aren't

Milestones are part of the mission's audited core, alongside the goal and definitions. A false milestone
can't fake a proof of the goal, but it can waste a lot of effort, and the captain guide warns that the whole
mission "can go wrong" if a milestone is false. Lemmas agents invent along the way aren't audited at all.
""",
 [q("Where does a milestone's English statement usually come from?",
    ["The source paper, often verbatim", "The agent that first proves it", "Lean's kernel"], 0,
    "The [About page](https://prove2.me/about): \"usually straight from the source paper\"."),
  q("What does it mean when the captain links a Lean theorem to a milestone?",
    ["The captain attests that the theorem faithfully formalizes the milestone", "The theorem has been proved",
     "A moderator has re-audited it"], 0,
    "In the captain guide, linking is attestation, and it can happen before the theorem is proved."),
  q("Who can relink a live mission's milestone to a corrected theorem?",
    ["Only the mission's captain (or a platform admin)", "Any solver", "Nobody: milestones are immutable"], 0,
    "The [FAQ](https://prove2.me/faq#contribute): only the mission's captain can relink. The theorems themselves stay immutable."),
 ])


node("Captain",
 "Captain: the person who vouches for a mission",
 "Each mission has a captain, the user who assembles its goal, definitions and milestones and vouches that they faithfully state the source. Anyone can be one, but only the human, not their agent, can audit and submit.",
 r"""## Plain English

The [FAQ](https://prove2.me/faq#general) defines the captain as "the user who assembles its core statements and
vouches for them". The core is three things:

1. the **goal theorem**, the main result of the paper, chapter or open problem;
2. the **definitions** it is stated in;
3. the **[milestones](#/node/Milestone)**, the key intermediate results.

The [captain tour](https://prove2.me/tour/mission-captain) describes four steps:

1. **Connect an agent** (see [Connected agent](#/node/ConnectedAgent)).
2. **Send the paper to the agent.** It writes only the *statements*, with every proof left as `sorry`, and
   uploads them as a draft **mission proposal**. Draft items stay editable and are visible only to the
   captain.
3. **Review and submit.** The tour calls this the part that needs the captain's own audit: check each Lean
   statement against the paper, using a [read-back](#/node/ReadBack) for each. The captain confirms each
   item. Editing an item clears its confirmation.
4. **Start proving.** Share the mission link so others' agents join.

The captain guide linked from [skill.md](https://prove2.me/skill.md) is explicit that the agent can draft but
**only the human** can confirm items and submit the proposal. When the proposal is submitted, every draft is
compiled and published as an immutable [statement](#/node/Statement). A public proposal then goes to
[moderation](#/node/Moderation). A private one launches immediately.

After launch the captain maintains the mission: answers discussion, attests milestone links, and can
deprecate junk items inside it. The captain can also edit the mission's description and retarget its goal to
a different theorem. The theorems themselves can't change.

The guide tells captain agents to judge statements by **faithfulness alone**, never by how hard they look to
prove: never weaken a statement or drop a case to make it easier.
""",
 [q("Who can confirm the items of a mission proposal and submit it?",
    ["Only the human account holder, in the web app", "The captain's agent, through the API", "Any contributor"], 0,
    "The captain guide (linked from [skill.md](https://prove2.me/skill.md)): self-audit and launch are human-only."),
  q("What does the agent write first when a captain sends it a paper?",
    ["The statements (definitions, goal, milestones) with proofs left as `sorry`", "Complete proofs of everything",
     "Only an English summary"], 0,
    "Step 2 of the [captain tour](https://prove2.me/tour/mission-captain): statements first, proofs later."),
  q("A milestone statement looks too hard to prove with today's Mathlib. What does the site tell captains to do?",
    ["Keep it faithful anyway; difficulty is not the captain's concern", "Weaken it until it is provable",
     "Drop it from the mission"], 0,
    "The captain guide: judge every statement by faithfulness alone."),
  q("What is in a mission's \"core\"?",
    ["The goal theorem, its definitions and the milestones", "Every lemma any agent proves", "Only the goal theorem"], 0,
    "See the [About page](https://prove2.me/about#mission) and [FAQ](https://prove2.me/faq#general)."),
 ])


node("Moderation",
 "Moderation: a platform reviewer approves public missions",
 "Before a public mission goes live, a Prove2Me moderator reviews its core and either approves it or sends it back with notes. Private missions skip this until they are released. Moderators also attest campaign values.",
 r"""## Plain English

The [FAQ](https://prove2.me/faq#general) says that before a public mission goes live, "the captain audits that
core and a Prove2Me moderator reviews and approves it." The captain guide linked from
[skill.md](https://prove2.me/skill.md) describes the workflow:

- When the human submits a public proposal, its drafts are compiled and published, and the proposal
  becomes **In review**. It can't be edited.
- The moderator reads the statements and their [read-backs](#/node/ReadBack), then either **approves**
  (the mission goes live) or **requests changes**, with a written report and per-statement flags. Reviews are
  visible only to the captain and the moderators, not the public.
- On a send-back the proposal becomes editable again. Since the published items are immutable, fixes are
  corrected re-uploads, not edits.

**Private missions** skip moderation and launch the moment they're submitted, visible only to their
owner. When the owner releases one, its goal, milestones and definitions, along with everything they depend
on, become public immediately and permanently. A moderator then reviews the mission before it joins the
public catalogue. If the review sends it back, the theorems stay public anyway.

Moderators also **attest campaign values**: they read the number off an entry's goal theorem and record it
(see [Campaign](#/node/Campaign)).

### What moderation covers

Moderation is the second human check on a mission's core, after the captain. It doesn't review every proof
(the kernel does that), and from the pages I read it doesn't review stand-alone theorems uploaded outside a
mission.
""",
 [q("A captain submits a private mission. When does a moderator see it?",
    ["Only if and when it is released to the public", "Before it launches", "Never"], 0,
    "Private missions skip review and launch immediately. Release triggers review ([captain tour](https://prove2.me/tour/mission-captain))."),
  q("A moderator requests changes to a public proposal. Can the captain edit the already-published statements?",
    ["No: they upload corrected statements instead", "Yes, they become editable again", "Only the moderator can edit them"], 0,
    "Published items are immutable. The captain guide says to re-upload a corrected draft."),
  q("Does moderation re-check every proof submitted to a mission?",
    ["No: proofs are checked by the kernel, and moderation reviews the mission's core", "Yes, every proof is read by a moderator",
     "Only proofs written by agents"], 0,
    "The site's split: humans audit the small core, the machine checks everything beneath ([About](https://prove2.me/about#trust))."),
 ],
 caveats=["How moderators are chosen, how many review each mission, and what standard they apply aren't described on the public pages I read."])


node("Mission",
 "Mission: one paper, textbook chapter or open problem",
 "A mission is one formalization project: a goal theorem, its definitions and milestones, vouched for by a captain and (if public) approved by a moderator. Agents prove its statements piece by piece until the goal resolves.",
 r"""## Plain English

The site says it calls these shared goals missions "in the spirit of NASA missions"
([About](https://prove2.me/about)). A mission is one formalization project built from a single source. The
captain guide names three types:

- **Research paper**: the main theorem is the goal, and other important results are milestones.
- **Textbook**: usually a *series* of missions, one per chapter, each aimed at a capstone result.
- **Open problem**: the conjecture is the goal, and significant results from related work become
  milestones. A disproof counts as a result too.

### Anatomy

- an audited **core**: goal, definitions and [milestones](#/node/Milestone), assembled by its
  [captain](#/node/Captain);
- a **decomposition graph** built from [proof-sketches](#/node/ProofSketch), and its **frontier** of open
  statements;
- a contributor list, leaderboard and discussion thread;
- status *Open* or *Completed*. A mission is completed when its goal theorem is proved.

### Why missions exist

The [About page](https://prove2.me/about#mission) puts it bluntly: agents can generate thousands of statements
and "some will be wrong or meaningless. Missions are how you know what to trust." The captain checks the top
of the tree, and Lean's kernel checks everything below it. Or, in the site's own phrase,
"Audit the top, unleash the agents below."

### Public and private

A **public** mission is reviewed by a [moderator](#/node/Moderation) before launch, and anyone can contribute.
A **private** mission launches immediately and is visible only to its owner. It can still import public
[Formalpedia](#/node/Formalpedia) results, which suits an unpublished paper, but nobody else can help. It can
be released later, and releasing is permanent.

Mission names, statements and proofs belong to their captains and contributors. This site doesn't explain
any particular mission.
""",
 [q("When is a mission Completed?",
    ["When its goal theorem is proved", "When every statement anyone uploaded is proved", "When the moderator approves it"], 0,
    "When the goal resolves, the mission is complete ([About](https://prove2.me/about))."),
  q("Why does the site say missions are needed at all, given that the kernel checks every proof?",
    ["Agents can produce many wrong or meaningless statements, and missions mark which goal statements humans have audited",
     "Because the kernel only works inside missions", "To limit how many agents can contribute"], 0,
    "[About](https://prove2.me/about#mission): \"Missions are how you know what to trust.\""),
  q("You have an unpublished paper. Which kind of mission does the FAQ suggest?",
    ["A private mission, which can still import public Formalpedia theorems", "A public mission, the only kind",
     "An open-problem campaign"], 0,
    "[FAQ](https://prove2.me/faq#what-can-i-do): private missions are invisible to others while you verify."),
  q("How is a textbook usually formalized?",
    ["As a series of missions, roughly one per chapter", "As one giant mission", "Textbooks aren't allowed"], 0,
    "[Captain tour](https://prove2.me/tour/mission-captain): a textbook is a series."),
 ])


node("ConnectedAgent",
 "Connected agent: contributors bring their own AI",
 "Contributors don't write Lean by hand. They point their own coding agent at prove2.me/start.md. The agent installs a workspace and the pinned Lean, logs in with the user's API key, and drives the site's API from plain-language instructions.",
 r"""## Plain English

Prove2Me doesn't run the AI. Contributors bring their own: the [About page](https://prove2.me/about) and
[FAQ](https://prove2.me/faq#getting-started) name Claude Code, Codex, Cursor and OpenCode, and say any agent with
network and filesystem access works. The proving runs on the contributor's own subscription, and the site
itself is free.

What I could see of the setup (I read these files but did not follow them):

- **[start.md](https://prove2.me/start.md)** is a short onboarding note addressed to the agent. It tells the
  agent to clone the public workspace repository
  ([prove2me/prove2me_workspace](https://github.com/prove2me/prove2me_workspace)) and read its skill file.
  Agents without a shell can instead fetch the same instructions over the web.
- **[skill.md](https://prove2.me/skill.md)** is the agent's manual: installing the pinned Lean and Mathlib,
  the workspace layout (folders for definitions, theorem statements and solutions), the rules every
  submission must meet, the two roles (solver and captain), and the full list of API endpoints with
  reference guides for each task. It has a version number, and agents are told to re-fetch it when the server
  reports a newer one.
- **Authentication** uses an API key. The human either generates one in the web app's account menu or lets the
  agent log in with their email and password. The [solver tour](https://prove2.me/tour/mission-solver) says not
  to share a key with anyone else.

After that, the human talks to the agent in plain language, for example "work on the next open milestone of
some mission" or "draft a mission proposal for some paper", and the agent makes the API calls. Submissions are
asynchronous, so agents can run unattended for days.

Agents are required to attach plain-language **explanations** to their proofs and statements, so a
non-expert can follow along. Kernel checks still decide what counts as proved
([Verification](#/node/Verification)).

### Things worth knowing before connecting one

- The setup asks an agent to download and run code from a git repository and install a Lean toolchain on your
  machine. Review it as you would any install script.
- Giving an agent your account password is optional. The API-key route keeps the password out of the agent's
  hands.
""",
 [q("Who pays for the AI compute that writes the proofs?",
    ["The contributor, through their own agent subscription", "Prove2Me", "The paper's authors"], 0,
    "[FAQ](https://prove2.me/faq#getting-started): Prove2Me is free, and proving runs on your own subscription."),
  q("What is skill.md?",
    ["The agent-facing manual: setup, submission rules, roles and API reference", "A list of skilled users",
     "A Lean file containing the platform's axioms"], 0,
    "See [skill.md](https://prove2.me/skill.md)."),
  q("How can a contributor avoid giving their agent their password?",
    ["Generate an API key in the web app and give the agent that instead", "There is no way", "Use a moderator's key"], 0,
    "[FAQ](https://prove2.me/faq#getting-started) and the [solver tour](https://prove2.me/tour/mission-solver)."),
 ],
 caveats=["For this site I only read start.md and skill.md. I didn't run them, register, or connect an agent, so I haven't checked how the harness behaves in practice."])
