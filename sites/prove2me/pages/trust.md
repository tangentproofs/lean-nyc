# Trust: what was and wasn't checked

## No Lean here

This explainer describes a **website**, not a Lean repository. There's no Lean source in its snapshot, nothing
was compiled, and no `lake`, `lean` or `elan` was run. So the usual counts of `sorry`, `axiom` and
`native_decide` don't apply: there is no code to count. The nodes are concept nodes with no formal statement.

## How the source material was gathered

- Public pages on prove2.me were read with plain HTTP requests on 2026-10-29: `/`, `/about`, `/faq`, `/tour`,
  `/tour/mission-solver`, `/tour/mission-captain`, `/terms`, `/blog` and five platform blog posts,
  `/start.md`, `/skill.md`, and four reference guides under `/references/` that skill.md links.
- `/api/` was **not** used (its robots.txt disallows it). I didn't log in, register, connect an agent, run the
  harness or submit anything. The instructions in start.md and skill.md were read, not followed.
- Nothing from prove2.me is copied into this repository. Quotations are short phrases, each linked to its page.

## What this means for accuracy

- Everything here describes the platform **as documented**, not as observed. Where documentation and behaviour
  differ, this site follows the documentation.
- The site changes quickly (its skill file is versioned, and environments and features are added). Details such
  as the Lean versions, campaign rules and licensing may be out of date.
- Points marked as my own reading, especially the "Where trust is weaker" list on [Trust model](#/node/TrustModel)
  and the open questions on the [review](#/review), are analysis, not claims made by Prove2Me.

## The explanations

Every explanation, quiz and caveat on this site was written by an AI (Claude) from the public pages above. None
has been reviewed by a human or by Kunal Marwaha or the Prove2Me team. All nodes are marked `review: draft`.
