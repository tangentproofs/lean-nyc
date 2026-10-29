NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

node("Prismriver.Theory.Dihedral.interval_toZMod12",
 "interval_toZMod12: semitones mod 12",
 "An interval's semitone count reduced mod 12; spelling and octaves are forgotten, so aug4 and dim5 both become 6.",
 r"""## Plain English

**Definition (Prismriver/Theory/Dihedral.lean lines 28–29).** `interval_toZMod12 i = i.semitones` in `ZMod 12`.
It is the interval half of the bridge to D12, used by
[toDihedral](#/node/Prismriver.Theory.Dihedral.TransposeAction.toDihedral).
""",
 [q("interval_toZMod12 of the octave is", ["0", "12", "7"], 0, "12 ≡ 0 mod 12 (octave is (7, 12), Prismriver/Repr/Classical.lean line 440)."),
  q("Do aug4 and dim5 map to the same value?", ["Yes, 6", "No"], 0, "Both have 6 semitones (Prismriver/Repr/Classical.lean lines 447–448)."),
  q("Does it use the letter part of the interval?", ["No", "Yes"], 0, "Only `i.semitones` appears (Prismriver/Theory/Dihedral.lean line 29).")])

LAWS = [
 ("Prismriver.Theory.Dihedral.transposeTriad_add", "T_m after T_n is T_(m+n)",
  "Transposing a triad label by j and then by i is transposing by i + j.", "91–97",
  "transposeTriad i (transposeTriad j t) = transposeTriad (i + j) t", "r·r"),
 ("Prismriver.Theory.Dihedral.transposeInverse_add", "T_m after I_n is I_(m+n)",
  "Inverting with index j and then transposing by i is inverting with index i + j.", "104–111",
  "transposeTriad i (invertTriad j t) = invertTriad (i + j) t", "r·sr"),
 ("Prismriver.Theory.Dihedral.inverseTranspose_subtract", "I_m after T_n is I_(m−n)",
  "Transposing by j and then inverting with index i is inverting with index i − j.", "114–122",
  "invertTriad i (transposeTriad j t) = invertTriad (i - j) t", "sr·r"),
 ("Prismriver.Theory.Dihedral.inverseInverse_subtract'", "Two inversions give a transposition",
  "Inverting with index −j and then with −i is transposing by j − i (the signed form the D12 action needs).", "139–153",
  "invertTriad (-i) (invertTriad (-j) t) = transposeTriad (j - i) t", "sr·sr"),
]
for id, title, summary, lines, stmt, case in LAWS:
    node(id, title, summary,
     f"""## Plain English

**Lemma (Prismriver/Theory/Dihedral.lean lines {lines}).** `{stmt}`. One of the four classical T/I composition
rules (the source comments quote them in the T<sub>n</sub>/I<sub>n</sub> notation). It is the {case} case of the
[MulAction instance](#/node/Prismriver.Theory.Dihedral.instance_155). The proof is a few `ZMod 12` rewrites
(`add_assoc`, `add_comm`) on the pair, plus a case split on the tag where flips occur.
""",
     [q("Which case of the D12 action law does it serve?", [case, "none"], 0, "See the mul_smul proof, Prismriver/Theory/Dihedral.lean lines 160–183."),
      q("Does it hold for every triad label t?", ["Yes, t is arbitrary", "Only for major triads"], 0, f"No hypotheses on t (Prismriver/Theory/Dihedral.lean lines {lines})."),
      q("Is the arithmetic done in ordinary integers?", ["No, in ZMod 12", "Yes"], 0, "Triad's first component is ZMod 12 (Prismriver/Theory/Dihedral.lean line 23).")])
