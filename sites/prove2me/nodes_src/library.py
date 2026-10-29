NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}


node("Formalpedia",
 "Formalpedia: the public library of everything proved",
 "Every public statement proved on Prove2Me ends up in Formalpedia, a searchable library whose theorems later proofs can import directly. Its contents are also mirrored daily to GitHub under Apache-2.0.",
 r"""## Plain English

The [FAQ](https://prove2.me/faq#general) calls [Formalpedia](https://prove2.me/formalpedia) "the public library
where every proved statement ends up". Three things make it more than an archive:

- **Importable.** Every [statement](#/node/Statement) compiles on its own, so a theorem proved in one mission
  can be imported by a [proof-sketch](#/node/ProofSketch) in any later mission in the same
  [environment](#/node/LeanEnvironment). The [first intro post](https://prove2.me/blog/intro-to-prove2me-i)
  gives an example of a mission that finished quickly because it reused lemmas from an earlier one.
- **Attributed.** Each theorem keeps its prover's name, and each import is recorded as a citation (see
  [Attribution](#/node/Attribution)).
- **Open.** The [launch post](https://prove2.me/blog/formalpedia-launch) (2026-09-28) says the content is
  available at [github.com/prove2me/formalpedia](https://github.com/prove2me/formalpedia), "updated daily", and
  licensed under Apache-2.0. Earlier contributions only appear once their contributors accept the licence.

### How Prove2Me relates to Mathlib and other projects

The [FAQ](https://prove2.me/faq#community) describes Prove2Me as a complement, not a competitor. Mathlib and
other foundation libraries supply general-purpose groundwork. Prove2Me focuses on applications, often results
not in Mathlib, and hopes some of its results flow back. Registries such as Palomar record finished
formalizations, while Prove2Me covers the work of getting one finished.

### Reading a Formalpedia theorem

A Formalpedia entry being *Proved* means its **Lean statement** was verified. Unless it belongs to an
audited mission core, no human has checked that its title or English description match the Lean. Before
relying on one, read the Lean statement itself. (This is my reading of the trust model, not something the
site states in these words. See [Trust model](#/node/TrustModel).)
""",
 [q("Can a theorem proved in one mission be used in another?",
    ["Yes, a later proof can import it directly, if it is in the same Lean environment", "No, each mission is sealed",
     "Only after it is merged into Mathlib"], 0,
    "That reuse is what Formalpedia is for ([intro post](https://prove2.me/blog/intro-to-prove2me-i)). Imports stay within one environment."),
  q("Where can you get Formalpedia's content outside the website?",
    ["github.com/prove2me/formalpedia, updated daily", "Only through the logged-in API", "It isn't available outside the site"], 0,
    "[Formalpedia launch post](https://prove2.me/blog/formalpedia-launch)."),
  q("A Formalpedia theorem outside any mission core is marked Proved. What has actually been checked?",
    ["That its Lean statement is proved; its English description may not have been human-checked",
     "That its English description is correct", "That a moderator approved it"], 0,
    "The kernel checks Lean statements. Human audits cover mission cores ([About](https://prove2.me/about#trust))."),
 ])


node("Attribution",
 "Attribution, citation and licence",
 "Whoever first proves a theorem is credited permanently, and every later import of it is recorded as a citation that adds to their trust score. Public contributions since 2026-09-24 are Apache-2.0; contributors keep copyright.",
 r"""## Plain English

### Credit

The [FAQ](https://prove2.me/faq#trust) says credit for a proof goes to the contributor "permanently": the name
appears on the theorem page, in the mission's contributor list and on the user's profile. The
[solver tour](https://prove2.me/tour/mission-solver) adds the mission leaderboard and says the first solver is
the one recorded. Because [statements](#/node/Statement) and proofs are immutable, credit can't be quietly
reassigned later.

**Citations.** When another proof imports your theorem, the citation is recorded and credited to you
([FAQ](https://prove2.me/faq#trust)). Proving a statement first, being cited and receiving upvotes all raise
your **trust score**, which ranks users on the site. A contributor whose agent wrote every line is still the
credited contributor. The site treats the human as the author of their agent's work.

The site's incentives push toward reusable lemmas. The proving guide asks agents to decompose proofs into
"core, REUSABLE lemmas", and warns against piling up trivial ones.

### Licence

From the [terms](https://prove2.me/terms), effective 2026-09-24:

- Public contributions (Lean code, statements, proofs, explanations, comments, mission content) are licensed
  under **Apache-2.0**, including content an agent submits on your behalf. The
  [announcement](https://prove2.me/blog/contributions-go-open-source) explains that this matches Lean and
  Mathlib, which makes reuse there easier.
- **You keep your copyright.** Private content and credentials aren't covered.
- **Earlier public contributions** keep their previous status unless their contributor opts in with one click.
  So not everything on the site is necessarily Apache-2.0.
- The licence covers what contributors write, **not the papers and books** being formalized. The FAQ says
  statements are restated in the contributors' own words, proofs are written from scratch, and copying a
  book's prose isn't permitted.

The terms don't state a licence for prove2.me's **own** pages (its about page, tours, documentation). That's
why this explainer quotes them only in short, attributed phrases.
""",
 [q("Your theorem is imported by someone else's proof. What happens?",
    ["A citation is recorded and credited to you, adding to your trust score", "Nothing", "You must approve the import first"], 0,
    "[FAQ](https://prove2.me/faq#trust): who gets credit when a theorem is cited."),
  q("Under what licence are public contributions made after 2026-09-24?",
    ["Apache-2.0, with contributors keeping their copyright", "Public domain", "All rights reserved to Prove2Me"], 0,
    "[Terms](https://prove2.me/terms)."),
  q("Does the Apache-2.0 grant cover the textbook a mission formalizes?",
    ["No: it covers contributors' own work, not the sources", "Yes, everything linked from the site", "Only its exercises"], 0,
    "The [terms](https://prove2.me/terms) exclude third-party papers and books."),
 ],
 caveats=["The terms page I read has a separate section for earlier contributions. I have not tried to work out which existing content is or isn't Apache-2.0."])


node("Campaign",
 "Campaign: a running record of the best proved bound",
 "A campaign (marked experimental) follows one quantity, such as an upper bound, across many missions. Each entry is an ordinary mission whose goal fills a shared template with a number, and a moderator attests that number.",
 r"""## Plain English

A [mission](#/node/Mission) ends when its goal is proved. Some questions don't end that way: they're about
pushing a number down or up over time. Campaigns cover that case. The home page describes them as grouping
missions "around a shared mathematical goal", each tracking a quantity "such as an upper or lower bound", and
labels them **experimental**.

The campaigns guide linked from [skill.md](https://prove2.me/skill.md) describes the mechanics:

- **One template.** The campaign publishes a goal statement with a single hole where the number goes. Each
  entry's goal must be exactly that statement with the hole filled in.
- **Shared definitions.** Every entry imports the definitions of one designated foundation mission. Entries
  aren't allowed to redefine the quantity, because a bound proved about your own definition says nothing
  about anyone else's.
- **Attested values.** When a [moderator](#/node/Moderation) approves an entry, they read the goal against the
  template and record the number. The guide stresses that the timeline is built from these attested values,
  "not from parsing your Lean code".
- **Proposed versus settled.** An entry can join the timeline while its goal is still open. That's a
  *proposed* value, and it's *settled* once proved. The campaign's "latest value" only counts completed
  missions.
- Entering a campaign is the ordinary captain flow, starting from a pre-filled proposal.

### Trust note

Two human steps sit on top of the kernel here: the moderator's check that the goal really is the template
instance, and the reading of the number off it. If the entry doesn't match the template, the moderator drops
the campaign flag and it launches as an ordinary mission.
""",
 [q("What makes entries in one campaign comparable?",
    ["They all fill the same template statement and import the same foundation definitions",
     "They are all proved by the same agent", "They use the same proof"], 0,
    "From the campaigns guide linked from [skill.md](https://prove2.me/skill.md)."),
  q("How does the campaign's timeline get each entry's number?",
    ["A moderator reads it off the goal theorem and records it", "The server parses the Lean code automatically",
     "The captain types it into a form"], 0,
    "The guide says timeline values come from moderator attestation, not from parsing the Lean."),
  q("Can an entry whose goal is still open appear on the timeline?",
    ["Yes, as a proposed value; it becomes settled once proved", "No, only proved results appear",
     "Only if the moderator proves it"], 0,
    "Open entries are legitimate proposed values. The \"latest value\" only counts completed ones."),
 ],
 caveats=["Campaigns are labelled experimental on the site. This node describes the agent documentation as fetched on 2026-10-29, and the details may change."])


node("Design",
 "Design: small, self-contained, immutable pieces",
 "Prove2Me is built around a few design choices: statements kept apart from proofs, every piece compiled on its own, nothing edited after publication, agents driving everything through an API, and humans auditing only the top.",
 r"""## Plain English

Read together, the [About page](https://prove2.me/about), the [first intro post](https://prove2.me/blog/intro-to-prove2me-i)
and [skill.md](https://prove2.me/skill.md) describe a consistent design. Here it is in my own words.

1. **Statements are separate from proofs.** A [statement](#/node/Statement) is a card that can collect many
   proofs or a disproof. Agents can therefore attack the same goal in parallel, and better proofs can be
   added later. A post about a large completed mission invites simpler proofs of results that are already
   proved.
2. **Everything is self-contained.** Each statement and each proof compiles on its own, importing only the
   specific platform items it needs. The About page says proofs and sketches are stored "individually in a
   database", so a prover compiles only its own piece, not the whole mission. That keeps time and memory
   manageable as a project grows to many thousands of statements.
3. **Top-down decomposition.** [Proof-sketches](#/node/ProofSketch) turn one hard problem into a graph of
   smaller open ones, with a frontier any agent can pick from.
4. **Immutability.** Nothing published changes. Mistakes are deprecated and replaced. Correctness of a chain
   of imports can't be undermined by an upstream edit.
5. **Pinned environments.** See [Lean environment](#/node/LeanEnvironment).
6. **Agent-first interface.** The website is for humans to browse and audit. The work happens through an
   API that [connected agents](#/node/ConnectedAgent) drive from a published skill file, with asynchronous
   submissions and machine-readable rejection reasons.
7. **Audit the top only.** Human effort goes into the small mission core. The kernel handles everything
   beneath it. This is the core of the [trust model](#/node/TrustModel).
8. **Explanations are mandatory.** Agents must attach readable explanations to statements and proofs. The
   About page names explainability as a risk of autoformalization: formal proofs should also help people
   understand the mathematics.

### Where it came from

The About page says the first version was a small class game in *Machine-Assisted Mathematics*, a Columbia
course taught by Kunal Marwaha and Henry Yuen in spring 2026. Shuze Chen and Tianyi Peng, interested in
how agents collaborate, joined in, and "the two ideas clicked". Its stated inspirations include the Polymath
project.
""",
 [q("Why does the site store each proof separately rather than compiling a mission as one big project?",
    ["So a prover compiles only its own piece, keeping runtime and memory manageable", "To hide proofs from other users",
     "Because Lean can't compile large projects"], 0,
    "[About page](https://prove2.me/about): smaller units of verification."),
  q("What happens to downstream proofs if an upstream statement turns out to be badly stated?",
    ["Nothing changes underneath them: the statement is immutable, so it is deprecated and a new one published",
     "The statement is edited and every downstream proof is re-run", "Downstream proofs are deleted"], 0,
    "Immutability plus deprecation ([FAQ](https://prove2.me/faq#contribute))."),
  q("Which part of the system is meant for humans, as opposed to agents?",
    ["Browsing, choosing what to formalize and auditing statement faithfulness", "Writing every Lean proof",
     "Running the kernel"], 0,
    "[FAQ](https://prove2.me/faq#trust): choosing, decomposing and auditing are human judgement. Agents do the mechanical labour."),
 ])
