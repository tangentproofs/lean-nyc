# Review: does the site's account of itself hold up?

A Lean explainer usually asks whether each headline theorem's statement is faithful. This site explains a
platform, so this page asks the equivalent question: are the site's descriptions of how it works, and especially
of why its results can be trusted, accurate and complete? Everything here comes from reading public pages. I
tested nothing.

## "Every submission runs through Lean's own kernel": consistent

The [About page](https://prove2.me/about#trust), [FAQ](https://prove2.me/faq#trust), tours and agent guide all
describe the same contract: a theorem named `solution` whose type must match the target exactly, no `sorry`,
whitelisted axioms, no self-import, compiled in the target's pinned environment. The verdict categories in the
agent guide (accepted, sketch accepted, compile error, wrong answer, sorry, failed, error) fit that contract.
**Caveat:** the axiom whitelist and the other blocked "escape hatches" aren't spelled out on the pages I read. See
[Verification](#/node/Verification).

## "A wrong lemma simply can't help prove a correctly-stated goal": sound, if the core is right

This is the key argument for auditing only a mission's core ([About](https://prove2.me/about#mission)). It holds:
a proof-sketch proves only "children imply parent", and a false child can never be proved, so it can't complete the
goal. The argument assumes the goal **and its definitions** are faithful. A subtly wrong definition makes a proved
goal mean something else, and the captain guide rightly singles definitions out for the closest audit. See
[Trust model](#/node/TrustModel).

## "Immutable": true of statements and proofs, not of every pointer

Lean statements and proofs can't be edited ([FAQ](https://prove2.me/faq#contribute)). Their English descriptions
can be edited by the submitter. A mission's milestone links can be changed by its captain (with logged reasons),
and the captain guide documents an endpoint that **retargets a live mission's goal** to another theorem. Readers
should take "immutable" to mean that the *theorems* never change, not that *a mission's goal* never changes. I
didn't find whether a retargeted public goal is re-reviewed by a moderator.

## "Audited twice": for public mission cores only

The FAQ says statement faithfulness is "audited twice": once by the captain and once by an independent agent's
read-back. Moderators add a third look for public missions. All of this applies to a mission's **core** (goal,
definitions, milestones). Private missions skip moderation until release. Stand-alone uploads and intermediate
lemmas, which make up most of Formalpedia, have no required faithfulness audit. That's by design, and it means the
Lean statement is the only reliable description of a non-core Formalpedia entry.

## "If it compiles, it's correct": true of the Lean statement

The FAQ uses this phrase when suggesting a private mission to check an AI-written proof. Compiling settles that
the *Lean statement* is proved. Whether that statement is the claimed result is the separate faithfulness question
that the same FAQ calls "the one place machines can't save you".

## Self-reported numbers

Costs, durations, line counts and totals (for example "over 100,000 public theorem statements" on 2026-10-01,
missions closed in days on one subscription) are the site's own reports. I haven't checked them. One blog post
cites an outside mathematician's independent re-check of one large mission. I didn't follow that up.

## Open questions

- What exactly is on the axiom whitelist, and is the verification pipeline's code public?
- Does the Formalpedia GitHub mirror contain everything needed to re-check results independently, with
  each item's environment?
- Is a retargeted mission goal re-moderated?
- How are moderators chosen, and what standard do they apply?
- How will statements pinned to older Mathlib environments stay useful as Mathlib moves on, given that
  cross-environment imports aren't supported?
- The site names explainability and canonicalization (the same statement proved many times) as open research
  directions ([About](https://prove2.me/about)). Nothing on the public pages yet says how they'll be measured.
