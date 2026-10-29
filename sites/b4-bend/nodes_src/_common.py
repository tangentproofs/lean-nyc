# Helpers shared by the node files (loaded with exec; files starting with _ define no nodes).
NODES = []
SHA = "6bf9a57996a8d7ddd9b07adff2e40375e12f0294"
BASE = "https://github.com/tangentstorm/b4/blob/" + SHA + "/imp/bend/"


def U(f, a, b=None):
    """GitHub URL for imp/bend/<f> lines a..b at the pinned commit."""
    return BASE + f + ("#L%d" % a if b is None or b == a else "#L%d-L%d" % (a, b))


def L(f, a, b=None):
    """Markdown link 'f lines a–b' to those lines at the pinned commit."""
    if b is None or b == a:
        return "[%s line %d](%s)" % (f, a, U(f, a))
    return "[%s lines %d–%d](%s)" % (f, a, b, U(f, a, b))


def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))


def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}


def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]
