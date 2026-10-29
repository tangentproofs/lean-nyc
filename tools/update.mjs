#!/usr/bin/env node
// Render index.html (the Lean NYC member-project hub) from projects.json. Same layout as tangentproofs.github.io.
//   node tools/update.mjs
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const { projects } = JSON.parse(readFileSync(join(ROOT, "projects.json"), "utf8"));
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const GH = `<svg viewBox="0 0 16 16" width="15" height="15" aria-hidden="true"><path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>`;
// Per-site summary written by the explainer build (title, lead, node count), if the explainer exists.
const info = (p) => { const f = join(ROOT, "sites", p.slug || "-", "site.json"); return p.slug && existsSync(f) ? JSON.parse(readFileSync(f, "utf8")) : null; };
// Secondary projects (secondaryOf: <slug>) are listed on their primary's card instead of getting their own.
const also = (p) => projects.filter((q) => q.secondaryOf === p.slug).map((q) => {
  const live = q.explainer && info(q);
  return `<p class="meta also">Also explained: ${live ? `<a href="${q.slug}/">${esc(q.repo.split("/")[1])}</a> (${q.nodeCount ?? ""} nodes, unofficial)` : esc(q.repo.split("/")[1])} · upstream <a href="https://github.com/${esc(q.repo)}">github.com/${esc(q.repo)}</a> by ${esc(q.authors)}${q.sha ? ` · pinned at <code>${q.sha.slice(0, 7)}</code>` : ""} · ${q.license ? `licence ${esc(q.license)}` : "no licence file"}</p>`;
}).join("");
function card(p) {
  const s = info(p), live = p.explainer && s;
  const name = p.url ? new URL(p.url).host : p.repo.split("/")[1];
  const hue = [...name].reduce((h, c) => (h * 31 + c.charCodeAt(0)) >>> 0, 7) % 6;
  const href = live ? `${p.slug}/` : p.demo ? p.demo.url : p.url || `https://github.com/${p.repo}`; // stubs link upstream until their explainer is live
  const who = p.members.map((m) => `<a href="${esc(m.profile)}">${esc(m.name)}</a>`).join(" &amp; ");
  const talk = p.talk ? ` · talk at Lean NYC: <a href="${esc(p.talkUrl || "https://lean.nyc/calendar")}">${esc(p.talk)}</a>` : "";
  const lic = p.license ? `licence ${esc(p.license)}` : p.slug ? "no licence file (source not reproduced)" : "";
  const desc = (s && s.desc) || p.description;
  const btns = [
    p.demo ? `<a class="btn site" href="${esc(p.demo.url)}"><b>Plain-English informalization</b> <span class="host">demo: ${esc(p.demo.label)}</span> →</a>`
      : live ? `<a class="btn site" href="${p.slug}/"><b>Plain-English informalization</b> <span class="host">unofficial explainer</span> →</a>`
      : p.slug ? `<span class="btn site soon"><b>Explainer in progress</b></span>`
      : p.url ? `<a class="btn site" href="${esc(p.url)}"><b>Project site</b> <span class="host">${esc(new URL(p.url).host)}</span> →</a>`
      : `<span class="btn site soon">Explainer in progress</span>`,
    p.url ? `<a class="btn gh" href="${esc(p.url)}">${esc(new URL(p.url).host)} ↗</a>`
      : `<a class="btn gh" href="https://github.com/${esc(p.repo)}">${GH} ${esc(p.repo)}</a>`].join("");
  return `<article class="card inf">
  <a class="thumb ph c${hue}" href="${esc(href)}" aria-label="${esc(name)}"><span class="ph-name">${esc(name)}</span><span class="ph-note">${live ? `${p.nodeCount ?? ""} explained nodes` : p.demo ? "demo explainer" : p.slug ? "explainer in progress" : p.url ? "project site" : "explainer coming"}</span></a>
  <div class="body">
    <h3><a href="${esc(href)}">${esc(name)}</a> <span class="pill">${p.url ? "site" : "Lean"}</span>${p.slug && !live ? ` <span class="pill soon">explainer in progress</span>` : ""}</h3>
    <p class="who">${who}</p>
    <p>${esc(desc)}</p>
    <p class="meta">Upstream: ${p.url ? `<a href="${esc(p.url)}">${esc(new URL(p.url).host)}</a>` : `<a href="https://github.com/${esc(p.repo)}">github.com/${esc(p.repo)}</a>`} by ${esc(p.authors)}${p.sha ? ` · pinned at <code>${p.sha.slice(0, 7)}</code>` : ""}${lic ? ` · ${lic}` : ""}${talk}</p>
    ${also(p)}<div class="links multi">${btns}</div>
  </div>
</article>`;
}
const url = "https://tangentproofs.github.io/lean-nyc/";
const title = "Lean NYC member projects, explained (unofficial)";
const desc = "An independent fan index of Lean projects by members of Lean NYC, each with an unofficial, AI-assisted plain-English explainer.";
const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${title}</title>
<meta name="description" content="${esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:title" content="${title}">
<meta property="og:description" content="${esc(desc)}">
<meta property="og:url" content="${url}">
<meta name="twitter:card" content="summary">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="top"><a class="brand" href="./">lean<span>nyc</span> explained</a>
<nav><a href="#projects">Projects</a><a href="https://lean.nyc/members">Lean NYC community</a><a href="https://github.com/tangentproofs/lean-nyc">GitHub</a></nav></header>
<main>
<section class="hero">
  <h1>lean<span>nyc</span> explained</h1>
  <p class="tag">Lean&nbsp;4 projects by members of <a href="https://lean.nyc">Lean NYC</a>, each read back into <em>plain English</em>: statements, proof outlines, quizzes.</p>
</section>
<p class="optout"><b>An experiment in AI-assisted informalization.</b> These are plain-English explainers for Lean NYC members' projects, using only repos linked from members' lean.nyc profiles, their home pages or their Lean NYC talks. Each explainer is unofficial, written with Claude, and may contain mistakes. Where a repo has no licence, no code is copied and the explainer links to GitHub instead. If you'd like your project removed, want a different repo featured, or want to be added, please say so in the Lean NYC group or contact Michal Wallace (<a href="https://github.com/tangentstorm">tangentstorm</a>).</p>
<p class="fan"><b>An independent fan index.</b> Not affiliated with or endorsed by NYC Lean or by the projects' authors. Every project belongs to its authors, linked on its card. The explainers are unofficial and AI-assisted (written by Claude, scaffolded by Grok Bot), pinned to one commit each, and may contain errors. Projects without a licence file are explained in prose only, with links to their exact lines on GitHub, never copied. Members are listed only where a GitHub (or other public git host) account is linked from their <a href="https://lean.nyc/members">lean.nyc profile</a>, their home page or a Lean NYC talk page. Corrections or take-down requests: <a href="https://github.com/tangentproofs/lean-nyc/issues">open an issue</a>.</p>
<section id="projects">
<h2>Member projects <span class="muted small">${projects.length}</span></h2>
<div class="grid feature">${projects.filter((p) => !p.secondaryOf).map(card).join("\n")}</div>
</section>
</main>
<footer>Generated by <a href="https://github.com/tangentproofs/lean-nyc/blob/main/tools/update.mjs"><code>tools/update.mjs</code></a> from <a href="https://github.com/tangentproofs/lean-nyc/blob/main/projects.json"><code>projects.json</code></a>. Member list read from <a href="https://lean.nyc/members">lean.nyc/members</a>.</footer>
</body>
</html>
`;
writeFileSync(join(ROOT, "index.html"), html);
console.error(`wrote index.html (${projects.length} projects)`);
