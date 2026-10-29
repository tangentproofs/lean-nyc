# Shared helpers (this file is not loaded as a node file because its name starts with "_").
# The node files exec() it so the helpers are in their namespace.
import os, re

SHA = "14879cb23e078d122adecd9578dd26a7304f753b"
GH = f"https://github.com/marcusm117/ProofNet-Verified/blob/{SHA}"
_SRC = os.environ.get("LEARN_SRC_ROOT") or os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "projects", "marcusm117-proofnet-verified")

def _nlines(rel):
    with open(os.path.join(_SRC, rel), encoding="utf-8") as fh:
        return len(fh.read().rstrip("\n").split("\n"))

def _range(rel, spec):
    a, _, b = spec.partition("-")
    a, b = int(a), int(b or a)
    n = _nlines(rel)
    if not (1 <= a <= b <= n):
        raise SystemExit(f"line range {spec} outside {rel} ({n} lines)")
    return a, b

def _lines(a, b):
    return f"line {a}" if a == b else f"lines {a}–{b}"

def _anchor(a, b):
    return f"#L{a}" if a == b else f"#L{a}-L{b}"

def _sub(m):
    kind, n, spec = m.group(1), m.group(2), m.group(3)
    if kind == "L":    # the latest (corrected) statement, rendered on this site
        rel = f"proofnet-verified-latest/proofnet-{n}.lean"
        a, b = _range(rel, spec)
        return f"[proofnet-{n}.lean {_lines(a, b)}](src/{rel}.html{_anchor(a, b)})"
    if kind == "O":    # the original ProofNet statement (Lean 4.28 port), on GitHub
        rel = f"data/proofnet/proofnet-4.28/proofnet-{n}.lean"
        a, b = _range(rel, spec)
        return f"[original proofnet-{n}.lean {_lines(a, b)}]({GH}/{rel}{_anchor(a, b)})"
    if kind == "T":    # the audit record comparing ProofNet with the corrected statement
        return f"[audit record {n}]({GH}/error_taxonomy/proofnet/per_file/proofnet-{n}.json)"
    if kind == "S":    # the audit record for ProofNet#
        return f"[ProofNet# audit record {n}]({GH}/error_taxonomy/proofnet%23/per_file/proofnet-{n}.json)"
    raise SystemExit(kind)

_TOK = re.compile(r"\[\[([LOTS]) (\d+)(?: ([\d-]+))?\]\]")

def R(s):
    """Expand [[L n a-b]], [[O n a-b]], [[T n]], [[S n]] into checked links."""
    return _TOK.sub(_sub, s)

def plain(s):
    """Same, for widget text (no Markdown): just the label."""
    return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", R(s))

NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    assert len(title) <= 80 and len(summary) <= 300, (id, len(title), len(summary))
    quiz = [dict(x, explain=plain(x["explain"])) for x in quiz]
    NODES.append(dict(id=id, title=title, summary=summary, body=R(body), quiz=quiz,
                      caveats=[plain(c) for c in caveats], widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]

STATUS_SORRY = ("PARTIAL (sorry) by design: this is a benchmark problem, and its Lean proof is the single word "
                "sorry, left for a prover to fill in. The authors report ground-truth proofs for every problem, "
                "but those ship only in a zip archive (for the Lean 4.28 snapshot) that this site did not open.")
