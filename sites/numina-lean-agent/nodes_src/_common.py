# Shared helpers for the numina-lean-agent nodes.
# The engine only auto-links .lean files whose names start with a capital letter, and every problem file here is
# lower-case (putnam_2025_a1.lean), so bodies use explicit GitHub links at the pinned commit. `ln` checks the range
# against the submodule source so a typo fails the build the way the engine's own check would.
import os

SHA = "1c9af8a52e715f22fede766425ba3d3b95526132"
BLOB = f"https://github.com/project-numina/numina-lean-agent/blob/{SHA}/"
SRC = os.environ.get("LEARN_SRC_ROOT") or os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "projects", "project-numina-numina-lean-agent")

NODES = []  # stays empty: write_nodes.py also loads this file, and each node file keeps its own list


def node_maker(nodes):
    """Each node file calls `node = node_maker(NODES)` with its own NODES list."""
    def node(id, title, summary, body, quiz, caveats=(), widgets=None):
        nodes.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
    return node


def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}


def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]


def _check(path, a, b):
    n = len(open(os.path.join(SRC, path), encoding="utf-8").read().splitlines())
    if not (1 <= a <= b <= n):
        raise ValueError(f"{path} lines {a}-{b} outside file ({n} lines)")


def ln(path, a, b=None):
    """Markdown link 'name.lean lines a–b' to GitHub at the pinned commit. `path` is relative to the repo root."""
    b = b or a
    _check(path, a, b)
    name = path.split("/")[-1]
    rng = f"line {a}" if a == b else f"lines {a}–{b}"
    anchor = f"#L{a}" if a == b else f"#L{a}-L{b}"
    return f"[{name} {rng}]({BLOB}{path}{anchor})"


def txt(path, a, b=None):
    """Plain-text reference for places that don't render Markdown links (quiz explanations, walkthrough steps)."""
    b = b or a
    _check(path, a, b)
    name = path.split("/")[-1]
    return f"{name} line {a}" if a == b else f"{name} lines {a}–{b}"


def P(x):
    return f"leanproblems/Putnam2025/putnam_2025_{x}.lean"


def M(x):
    return f"leanproblems/Minif2f/{x}.lean"


NOT_BUILT = ("Not built for this site: the statement was read from source text, and no Lean was compiled.")
SORRY = ("PARTIAL (sorry): this is a benchmark problem statement. Its proof in this repository is a single "
         "`sorry`, on purpose: it is the hole the agent is asked to fill. The agent's finished Putnam proofs are in "
         "the separate project-numina/Numina-Putnam2025 repository, which this site did not examine.")
