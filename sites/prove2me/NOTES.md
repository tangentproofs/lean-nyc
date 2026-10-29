# prove2me: notes for the coordinator (not published)

## Time spent

About 1.5 hours: roughly 30 minutes reading the site, 15 on the engine change and checking it, and 45 on
writing and building.

## What was done

- An explainer of the **prove2.me website** (Kunal Marwaha and the Prove2Me team), with 17 concept nodes. The
  headlines are `Prove2Me`, `Lifecycle` and `TrustModel`. There are pages for about, review and trust.
- Sources, fetched with curl on 2026-10-29 using a descriptive User-Agent and a pause of about 1 s between
  requests: `/`, `/about`, `/faq`, `/tour`, `/tour/mission-solver`, `/tour/mission-captain`, `/terms`,
  `/blog`, five platform blog posts (intro-to-prove2me-i, contributions-go-open-source, formalpedia-launch,
  momentum-page, fermats-last-theorem), `/start.md`, `/skill.md`, and robots.txt.
- **Judgement call:** I also read four reference guides that skill.md links: `/references/campaigns.md`,
  `prove.md`, `mission_captain.md` and `mission_auditor.md`. They're public pages, not under `/api/`, and
  skill.md is only an index to them. Without them, campaigns, moderation, read-backs and verdicts can't be
  described accurately. Everything was only read. No instructions were followed, there was no login, and
  `/api/` was never touched.
- No mission content is quoted or explained. Mission names appear only where the site itself uses them as
  examples, and I avoided even those in the node texts. The About and tour pages include a toy Lean example,
  which I described in words and did not quote.
- `site.json`: snapshot, licence, repo and sha were kept as given. `authors` was kept as "Kunal Marwaha and the
  Prove2Me team". The about page and the Prove2Me node name Henry Yuen, Shuze Chen and Tianyi Peng as
  co-creators, as the site's About page does.

## Engine change (minimal, guarded)

The engine required every node id to be a declaration in `decls.json`, and with no Lean there are none. The
change adds **concept nodes**, driven by a new optional `site.json` key, `concepts`
(`{id: {deps: [...], url: "..."}}`):

- `engine/gen.py`: passes `concepts` into `scan.config.json`, but only when present.
- `engine/tools/scan_decls.py`: appends one synthetic declaration per concept (`kind: "concept"`,
  `file: null`, `statement: null`, `meaningDeps` taken from `deps`, plus `url`) before usedBy and depth are
  computed. `module` is set to "concepts" when `file` is null.
- `engine/assets/app.js`: for `kind === "concept"`, the source link points to the page URL, the
  statement box says "A concept, not a Lean declaration…", the node list's file column links the page, the
  agent prompt shows the URL, and the file list skips the "Read X.lean" link when there is no file.
- `engine/assets/style.css`: adds one `.pill.kind-concept` colour rule.
- `engine/tools/test_leanlines.mjs`: skips concept declarations in the "statements survive wrapping" test.
  It crashed on `statement: null`. Side note: `build.sh` chains the tests with `&&`, so under `set -e` a failing
  test doesn't stop the build. The FAIL line was printed and the build still said "built". That's worth
  fixing separately. I didn't change it.

**Checked:** I built `lean-tic-tac-toe` and `expander-graphs` with the original engine (`git checkout engine`)
and again with the change, and compared `_site/<slug>` with `diff -r`. Every data file and page is identical, and
so are the build logs. Only the shared `assets/app.js` and `assets/style.css` differ, by the inert concept
branches and the one CSS rule.

**Not changed:** the engine's generic wording ("Start here: what the theorem says", "the proof graph", "The Lean
is the ground truth" in the footer, the "From Mathlib" heading on the start page, which is empty here) still
talks as if there were a theorem. I set `startNote` to explain that the nodes are concepts. A snapshot-aware
wording pass would be a larger engine change, so I left it for you to decide.
`projects.json` still has `"explainer": false` for prove2me, and I didn't touch it, per AUTHORING.

## Hardest parts

- Explaining a trust model without quoting mission statements. Everything had to be described in words, and the
  quizzes had to test the model rather than examples.
- Keeping apart what the site **claims** and what I **infer**. The "Where trust is weaker" section of
  `TrustModel` and the review's open questions are my analysis, and they're labelled that way.

## Where I'm least sure

- **TrustModel / review, "retargeted goal not re-moderated":** the captain guide documents a `main_statement`
  field for editing a live mission's goal, and I found no statement that this triggers re-review. Moderators
  may still review it in practice, or the UI may restrict it. This is a gap in what's documented, not a finding.
- **Verification, axiom whitelist:** the site says axioms are checked against a whitelist but doesn't list
  it on the pages I read. I didn't guess its contents.
- **Moderation, scope:** I say moderation covers mission cores, not stand-alone uploads. That's inferred from
  the docs describing moderation only for proposals and releases.
- **Milestone, "goal resolves when the last milestone is connected":** the About page phrases it that way.
  Mechanically, resolution goes through the sketch graph, so a milestone has to be linked into the goal's
  decomposition to count. My wording may be slightly off on how milestones connect.
- **Formalpedia, "Proved but English unaudited":** this is my inference from the documented rules (the
  submitter can edit descriptions freely, and audits cover cores). Agents are required to write explanations,
  and the community may vote or flag. So "no human check" means none is *required*, not that none ever happens.
- **LeanEnvironment:** version numbers are a snapshot, and the docs say their own table can lag.
- **Attribution, "first solver" credit:** the tour and skill.md mention the first solver. How credit works for
  later alternative proofs isn't clear to me.

## Things Kunal / the team might object to

- The "Where trust is weaker" list and the review's caveats on "immutable", "audited twice" and "if it compiles,
  it's correct". I tried to be fair: each says the site's claim is true in its intended sense, and states the
  boundary. They might still read as nitpicking.
- Calling the cost and scale numbers "self-reported" and unverified.
- The ConnectedAgent node's advice to review the install script before letting an agent run it, and its note
  that sharing a password is optional. That's standard caution, but it is advice about their onboarding flow.
- Credit: the title credits "Kunal Marwaha and the Prove2Me team". The team might prefer the four named
  creators to be listed equally.
- The site states no licence for its own pages. I kept quotations to short phrases with links. If even that is
  unwelcome, they're easy to remove.
