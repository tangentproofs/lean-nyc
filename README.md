# lean-nyc: Lean NYC member projects, explained (unofficial)

**Live:** https://tangentproofs.github.io/lean-nyc/

An **independent fan index** of Lean 4 projects by members of [Lean NYC](https://lean.nyc). It is not affiliated with NYC Lean or with any project's authors. Every project belongs to its authors. Each one gets an unofficial, AI-assisted plain-English explainer pinned to a single commit.

## How members and projects were chosen

- **Members:** everyone listed on [lean.nyc/members](https://lean.nyc/members), read from the site's source, [NYC-Lean/website](https://github.com/NYC-Lean/website).
- **GitHub accounts:** used only when linked from the member's lean.nyc profile, from the home page that profile links to, or from a Lean NYC talk page. Nobody was searched for.
- **Repos:**
  - If a member gave a Lean NYC talk about a repo, that repo is used.
  - Otherwise, the most interesting or most active repo with real Lean work on the linked account.
- See [`members.tsv`](members.tsv) for every member: who is included, who was skipped, and why.

## Layout

| path | what |
|---|---|
| `projects/<owner>-<repo>` | git submodules, pinned (a pointer, not a copy) |
| `projects.json` | the hub's cards; `node tools/update.mjs` renders `index.html` |
| `engine/` | the shared informalization engine (from the tangentproofs proof-site kit) |
| `sites/<slug>/` | one explainer: `site.json`, `nodes_src/*.py` (the explainer nodes), `pages/{about,review,trust}.md` |
| `.github/workflows/pages.yml` | builds every explainer with `engine/build.sh <slug>` and deploys Pages |

## Licences

- `engine/gen.py` reads each project's licence from `site.json`.
- The site reproduces a project's Lean (highlighted source pages and verbatim statements) only under a licence that permits it. The site includes the licence text and any NOTICE file.
- Projects without a licence file are explained in prose only. Every line reference links to GitHub at the pinned commit. Statements are stripped from the published data.

## Building

There is no Lean build: declarations are scanned from the source text.

```
git submodule update --init
(cd engine && npm ci)
engine/build.sh <slug>      # -> _site/<slug>/
```

## Corrections and take-downs

[Open an issue](https://github.com/tangentproofs/lean-nyc/issues). If you are an author and want your project's page changed or removed, say so there and it will be done.
