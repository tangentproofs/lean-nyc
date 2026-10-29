# Workaround for a scanner false positive (see NOTES.md, "Engine issue").
# Beth/Coverage.lean lines 36-41: the structure `Coverage` has a FIELD named `covers`; the text scanner
# resolves that field name to the top-level def `Beth.covers` (line 48), which itself mentions
# `HasCoverage` -> `Coverage`. The resulting fake cycle makes test_statement.mjs fail ("Beth.HasCoverage
# should come before Beth.covers"). This file runs during write_nodes.py (after scan_decls.py) and drops
# only that one spurious edge from build/<slug>/data/decls.json. It touches nothing in engine/.
import json, os
NODES = []
_p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "decls.json")
if os.path.exists(_p):
    _d = json.load(open(_p, encoding="utf-8"))
    for _x in _d:
        if _x["id"] == "Beth.Coverage" and "Beth.covers" in _x["meaningDeps"]:
            _x["meaningDeps"].remove("Beth.covers")
        if _x["id"] == "Beth.covers" and "Beth.Coverage" in _x.get("usedBy", []):
            _x["usedBy"].remove("Beth.Coverage")
    json.dump(_d, open(_p, "w", encoding="utf-8"), ensure_ascii=False)
