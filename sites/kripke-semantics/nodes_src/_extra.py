# Extra quiz questions, appended to nodes by each node file (files starting with _ define no nodes).
NODES = []
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
EXTRA = {
 "Beth.BethTrees.BethTree": q("Why must every node lie on an infinite path?",
   ["So that bars are never empty, giving the 'non-empty covers' axiom", "For decidability", "It need not"], 0,
   "Pruning (Beth/BethTrees.lean line 77) feeds IsBar.nonempty (lines 179–199)."),
 "Beth.BethTrees.BethTreeCoverage": q("Does the root alone form a bar at the root?",
   ["Yes: every path starts at the root (depth 0)", "No", "Only in finite trees"], 0,
   "Take n = 0 in IsBar (Beth/BethTrees.lean lines 82–86); this is the 'maximal' case at lines 214–218."),
 "Beth.BethTrees.BethTreeFrame": q("Which two conditions must a tree valuation satisfy?",
   ["Persistence and the bar condition", "Decidability and finiteness", "Prime and closed"], 0,
   "BethVal, Beth/BethTrees.lean lines 201–204."),
 "Beth.Completeness.World": q("How does this canonical model differ from the Kripke one?",
   ["Worlds are finite consistent contexts, not infinite prime theories", "It has only one world", "It uses Boolean values"], 0,
   "Compare Beth/Completeness.lean lines 14–16 with Kripke/Completeness.lean lines 294–298."),
 "Beth.Completeness.truth_lemma": q("Which case uses the basic covering rule?",
   ["∨, from provable to forced", "∧", "true"], 0,
   "Beth/Completeness.lean lines 222–228."),
 "Beth.Completeness.truth_lemma#2": q("In the ⇒ case, what happens if φ, Γ proves false?",
   ["Γ ⊢ φ ⇒ ψ follows by false elimination and ⇒ intro", "The lemma fails", "Γ is not a world"], 0,
   "Beth/Completeness.lean lines 243–244."),
 "Beth.Examples.bethFrameOfKripke": q("Why does the sheaf condition hold in this frame?",
   ["Because w itself belongs to the only covering sieve on w", "By Zorn's lemma", "It is assumed"], 0,
   "Beth/Examples.lean lines 25–29."),
 "Beth.SemEntails": q("Which lemma makes semantic ∨ elimination valid?", ["sheaf_term", "mono_at", "covers_mono"], 0,
   "Beth/Semantics.lean lines 174–190 apply sheaf_term."),
 "Kripke.Canonical.Admissible": q("What is the 'false' case of imp_target_of_failure?",
   ["Adding φ makes the theory inconsistent, so ¬φ is in T and hence φ ⇒ A", "A is false", "T is empty"], 0,
   "Kripke/Completeness.lean lines 193–198."),
 "Kripke.Canonical.World": q("Why is persistence of variables automatic in the canonical model?",
   ["Because w ≤ v means w ⊆ v, so a member of w is a member of v", "Because of the truth lemma", "It is not"], 0,
   "Kripke/Completeness.lean lines 308–310."),
 "Kripke.Consistency.consistency": q("Does consistency need the completeness theorem?",
   ["No, soundness plus one model suffices", "Yes"], 0,
   "Kripke/Soundness.lean lines 74–78 only use soundness."),
 "Kripke.SemEntails": q("To show Γ ⊭ φ, what do you need?",
   ["One frame and one world where all of Γ holds but φ fails", "A proof of ¬φ", "Every frame to fail"], 0,
   "Negating the universal statement at Kripke/Frame.lean lines 69–70."),
 "Kripke.countermodel": q("Which lemma produces the countermodel world?",
   ["prime_extension_avoiding", "multicut", "soundness"], 0,
   "Kripke/Completeness.lean lines 470–471."),
 "Kripke.opensFrame": q("Is any theorem about opensFrame proved?", ["No, only the construction", "Yes, completeness for topological models"], 0,
   "Kripke/Examples.lean lines 30–34 is the whole development."),
}
def apply(nodes):
    for n in nodes:
        for k, v in EXTRA.items():
            if k.split("#")[0] == n["id"]: n["quiz"].append(v)
