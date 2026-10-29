# About this site

## The project

[Prove2Me](https://prove2.me) is a website for collaborative, machine-checked mathematics in Lean 4, built by
**Kunal Marwaha and the Prove2Me team**. Its [About page](https://prove2.me/about) says it grew out of
*Machine-Assisted Mathematics*, a Columbia course co-taught by Kunal Marwaha and Henry Yuen in spring 2026, where
the first prove2.me was "a small class game" for posing and proving Lean statements. It then merged with work by
Shuze Chen and Tianyi Peng on how AI agents collaborate. The site links a [research paper](https://arxiv.org/abs/2608.28433)
about the platform, which I didn't read for this explainer.

Kunal's linked GitHub repository `marwahaha/prove2me` is the earlier TypeScript version. The current platform's
public code is the agent workspace [prove2me/prove2me_workspace](https://github.com/prove2me/prove2me_workspace),
and its proved results are at [prove2me/formalpedia](https://github.com/prove2me/formalpedia).

## What this explainer covers

**This explains the website itself**: what Prove2Me is, how a paper becomes a mission and then reusable library
entries, how the platform is designed, and what its trust model does and doesn't guarantee. It was written from
these public pages, fetched on 2026-10-29:

- [/](https://prove2.me/), [/about](https://prove2.me/about), [/faq](https://prove2.me/faq), [/tour](https://prove2.me/tour),
  [/tour/mission-solver](https://prove2.me/tour/mission-solver), [/tour/mission-captain](https://prove2.me/tour/mission-captain),
  [/terms](https://prove2.me/terms);
- the platform blog posts [Intro to Prove2Me I](https://prove2.me/blog/intro-to-prove2me-i),
  [contributions go open source](https://prove2.me/blog/contributions-go-open-source),
  [Formalpedia launch](https://prove2.me/blog/formalpedia-launch), [Momentum page](https://prove2.me/blog/momentum-page)
  and [Fermat's Last Theorem](https://prove2.me/blog/fermats-last-theorem);
- the agent documents [start.md](https://prove2.me/start.md) and [skill.md](https://prove2.me/skill.md), plus four
  reference guides they link (on campaigns, proving, mission captains and read-back auditing, under
  `prove2.me/references/`). These were **read only**. Their instructions were not followed.

The site's `/api/` (disallowed by its robots.txt) wasn't used. I didn't log in, register, connect an agent or
submit anything.

**What it leaves out:** individual missions. They appear only as examples of the workflow. No mission's Lean
statements are quoted or explained. They belong to their captains and contributors and can be read on
prove2.me. Since the site states no licence for its own pages, they're quoted only in short phrases, each
attributed and linked.

## How to read it

The nodes are **concepts**, not Lean declarations, so none has a "formal statement" box. Start with
[what Prove2Me is](#/node/Prove2Me), then [a paper's path to Formalpedia](#/node/Lifecycle), then
[the trust model](#/node/TrustModel). The [review](#/review) asks whether the site's descriptions of itself hold
up, and [trust](#/trust) says what this explainer did and didn't check.
