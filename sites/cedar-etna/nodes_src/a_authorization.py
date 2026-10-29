NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]

UPSTREAM = ("This is upstream Cedar work (cedar-policy/cedar-spec, Copyright Cedar Contributors), carried unchanged "
            "in this fork as far as we can tell; the ETNA additions don't touch it.")


node("Thm.HasSatisfiedEffect",
 "How Cedar decides: satisfied policies with an effect",
 "A Cedar request is decided by looking at which policies are satisfied (their condition evaluates to exactly `true`). `HasSatisfiedEffect e` says some policy with effect e (permit or forbid) is satisfied.",
 r"""## Plain English

Cedar is Amazon's open-source authorization-policy language. A **policy** is `permit` or `forbid`, plus a scope and
`when`/`unless` conditions; the Lean spec turns each policy into a single boolean expression `policy.toExpr`.
A **request** names a principal, an action, a resource and a context record; **entities** is the store of entity data
(attributes, tags, parents).

The authorizer is defined in Cedar/Spec/Authorizer.lean lines 29–62:

- `satisfied policy req entities` (lines 29–30) is true exactly when evaluating the policy gives `.ok true`.
  An evaluation **error** counts as *not satisfied*.
- `satisfiedPolicies effect …` (lines 37–38) is the set of ids of satisfied policies with that effect.
- `isAuthorized` (lines 56–62) answers **allow** iff there are *no* satisfied forbids **and** *at least one*
  satisfied permit. Otherwise it answers **deny**. The response also lists the determining policies and the policies
  whose evaluation errored.

**Definition (`HasSatisfiedEffect`, Cedar/Thm/Authorization.lean lines 32–36).** For an effect e:
there is a policy in the list whose effect is e and which is `satisfied` for this request and entity store.

Its two instances are [IsExplicitlyForbidden](#/node/Thm.IsExplicitlyForbidden) (e = forbid) and
[IsExplicitlyPermitted](#/node/Thm.IsExplicitlyPermitted) (e = permit). The bridge lemma
`satisfied_iff_satisfiedPolicies_non_empty` (lines 38–40) says `HasSatisfiedEffect` holds iff the computed set
`satisfiedPolicies` is non-empty. Every authorization theorem goes through it.

""" + UPSTREAM,
 [q("A policy whose condition throws an error at evaluation time is…", ["Not satisfied", "Satisfied", "Treated as forbid"], 0,
    "`satisfied` requires `evaluate … = .ok true` (Cedar/Spec/Authorizer.lean lines 29–30)."),
  q("When does `isAuthorized` answer allow?", ["No satisfied forbid and at least one satisfied permit", "At least one satisfied permit", "More permits than forbids"], 0,
    "The `if forbids.isEmpty && !permits.isEmpty` test (Cedar/Spec/Authorizer.lean line 60)."),
  q("What does `HasSatisfiedEffect .permit req es ps` assert?", ["Some permit policy in ps is satisfied", "Every permit policy in ps is satisfied", "The request is allowed"], 0,
    "An existential over policies (Cedar/Thm/Authorization.lean lines 32–36). Being explicitly permitted is not the same as being allowed: a forbid can still win."),
 ])


node("Thm.IsExplicitlyForbidden",
 "Explicitly forbidden",
 "A request is explicitly forbidden when at least one forbid policy is satisfied.",
 r"""## Plain English

**Definition (Cedar/Thm/Authorization.lean line 45).** `IsExplicitlyForbidden` is
[HasSatisfiedEffect](#/node/Thm.HasSatisfiedEffect) with effect `forbid`.

`explicitly_forbidden_iff_satisfying_forbid` (lines 47–49) restates it as "the computed set of satisfied forbid
policies is non-empty", which is the form the authorizer's `if` tests. That is what makes
[forbid trumps permit](#/node/Thm.forbid_trumps_permit) a two-line proof.
""",
 [q("Which effect does `IsExplicitlyForbidden` look at?", ["forbid", "permit", "both"], 0, "Cedar/Thm/Authorization.lean line 45."),
  q("If a forbid policy errors during evaluation, is the request explicitly forbidden by it?", ["No: erroring policies are not satisfied", "Yes"], 0,
    "Satisfied means evaluation returned `.ok true` (Cedar/Spec/Authorizer.lean lines 29–30)."),
  q("Does `IsExplicitlyForbidden` say anything about permits?", ["No", "Yes, it requires no permit to be satisfied"], 0,
    "It's only about forbid policies (Cedar/Thm/Authorization.lean line 45)."),
 ])


node("Thm.IsExplicitlyPermitted",
 "Explicitly permitted",
 "A request is explicitly permitted when at least one permit policy is satisfied. A satisfied forbid can still make the decision deny.",
 r"""## Plain English

**Definition (Cedar/Thm/Authorization.lean line 55).** `IsExplicitlyPermitted` is
[HasSatisfiedEffect](#/node/Thm.HasSatisfiedEffect) with effect `permit`. The docstring (lines 51–54) warns that being
explicitly permitted does **not** mean being allowed.

`explicitly_permitted_iff_satisfying_permit` (lines 57–59) is the set-non-empty form, used in
[allowed only if explicitly permitted](#/node/Thm.allowed_only_if_explicitly_permitted).
""",
 [q("Explicitly permitted + explicitly forbidden gives…", ["deny", "allow", "an error"], 0,
    "See [forbid trumps permit](#/node/Thm.forbid_trumps_permit)."),
  q("Which effect does `IsExplicitlyPermitted` look at?", ["permit", "forbid"], 0, "Cedar/Thm/Authorization.lean line 55."),
  q("Is 'explicitly permitted' a property of the decision or of the policies?", ["Of the policies (some permit is satisfied)", "Of the decision"], 0,
    "It's an existential over policies, not a statement about `isAuthorized` (Cedar/Thm/Authorization.lean line 55)."),
 ])


node("Thm.forbid_trumps_permit",
 "Headline: forbid trumps permit",
 "If any forbid policy is satisfied, Cedar's authorizer denies the request, no matter how many permit policies are also satisfied.",
 r"""## Plain English

**Theorem (`forbid_trumps_permit`, Cedar/Thm/Authorization.lean lines 64–72).** For every request, entity store and
list of policies: if the request is [explicitly forbidden](#/node/Thm.IsExplicitlyForbidden), then the decision of
`isAuthorized` is `deny`.

This is one of the two core safety properties of Cedar's design (the other is
[default deny](#/node/Thm.default_deny)). It means a policy author can write a `forbid` and be sure no `permit`
written elsewhere overrides it.

**What it doesn't say.** It says nothing about policies that *error*. An erroring forbid policy is not satisfied, so
it does not trigger this theorem; Cedar's design is that errors are skipped (and reported in
`erroringPolicies`). Whether that is what you want is a design question; the theorem is faithful to the definition.

**Status.** Complete proof in the source (no `sorry`). Not built for this site. Upstream Cedar result.
""",
 [q("A request has 5 satisfied permits and 1 satisfied forbid. Decision?", ["deny", "allow", "depends on order"], 0,
    "Exactly `forbid_trumps_permit` (Cedar/Thm/Authorization.lean lines 64–67)."),
  q("A forbid policy throws an evaluation error and one permit is satisfied. Does this theorem force deny?", ["No: the erroring forbid isn't satisfied, so the hypothesis fails", "Yes"], 0,
    "The hypothesis is `IsExplicitlyForbidden`, which needs `evaluate … = .ok true` (Cedar/Spec/Authorizer.lean lines 29–30). In that case the request is allowed."),
  q("Does the theorem need any hypothesis about the schema or validation?", ["No, it holds for all requests, entities and policies", "Yes, the policies must validate"], 0,
    "Its only hypothesis is `IsExplicitlyForbidden …` (Cedar/Thm/Authorization.lean line 66)."),
 ],
 caveats=["Upstream Cedar result (cedar-policy/cedar-spec), not part of the ETNA additions.",
          "Not built for this site: 'proved' means the source contains a complete-looking proof."],
 widgets=walk("How the proof goes (Cedar/Thm/Authorization.lean, lines 64-72)", [
  {"text": "Assume the request is explicitly forbidden.", "lean": "intro h", "link": "Thm.IsExplicitlyForbidden"},
  {"text": "Unfold the authorizer into its if-then-else on the forbid and permit sets.", "lean": "unfold isAuthorized"},
  {"text": "Turn the hypothesis into 'the satisfied-forbid set is non-empty' with the bridge lemma.",
   "lean": "rw [explicitly_forbidden_iff_satisfying_forbid] at h", "link": "Thm.HasSatisfiedEffect"},
  {"text": "Now the `forbids.isEmpty` test is false, so the else-branch (deny) is taken; `simp` closes it.", "lean": "simp [h]"},
 ]))


node("Thm.allowed_only_if_explicitly_permitted",
 "Allowed only if explicitly permitted",
 "If the decision is allow, some permit policy was satisfied. This is the lemma behind default deny.",
 r"""## Plain English

**Theorem (Cedar/Thm/Authorization.lean lines 75–86).** If `isAuthorized` answers `allow`, then the request is
[explicitly permitted](#/node/Thm.IsExplicitlyPermitted).

**Proof idea.** Unfold `isAuthorized`, name the forbid and permit sets, and case-split on whether each is empty
(lines 79–84). Only the case "no forbids, some permits" gives `allow`, and there the permit set is non-empty, which
the bridge lemma turns back into `IsExplicitlyPermitted` (line 86).

[Default deny](#/node/Thm.default_deny) is its contrapositive.
""",
 [q("This lemma's conclusion is…", ["Some permit policy is satisfied", "No forbid policy exists", "Every permit is satisfied"], 0,
    "Cedar/Thm/Authorization.lean lines 76–77."),
  q("How does the proof proceed?", ["Case analysis on whether the forbid and permit sets are empty", "Induction on the policy list"], 0,
    "Cedar/Thm/Authorization.lean lines 83–84."),
  q("Which headline is its contrapositive?", ["default_deny", "forbid_trumps_permit"], 0, "See Cedar/Thm/Authorization.lean lines 88–91."),
 ])


node("Thm.default_deny",
 "Headline: default deny",
 "If no permit policy is satisfied, the request is denied. Nothing is allowed unless some policy explicitly allows it.",
 r"""## Plain English

**Theorem (`default_deny`, Cedar/Thm/Authorization.lean lines 92–103).** For every request, entity store and list of
policies: if the request is **not** [explicitly permitted](#/node/Thm.IsExplicitlyPermitted), the decision is `deny`.

Together with [forbid trumps permit](#/node/Thm.forbid_trumps_permit) this pins down the decision exactly:
`allowed_iff_explicitly_permitted_and_not_denied` (lines 109–123) says allow ⇔ (some permit satisfied and no forbid
satisfied). See [the other authorization theorems](#/node/Thm.allowed_iff_explicitly_permitted_and_not_denied).

**Edge cases.** An empty policy list denies everything. A policy set where every permit errors at runtime denies.

**Status.** Complete proof in the source. Not built for this site. Upstream Cedar result.
""",
 [q("With an empty list of policies, every request is…", ["denied", "allowed", "undefined"], 0,
    "No permit can be satisfied, so `default_deny` applies (Cedar/Thm/Authorization.lean lines 92–94)."),
  q("Is default_deny a consequence of the definition of isAuthorized alone?", ["Yes, it needs no other hypothesis", "No, it needs validated policies"], 0,
    "Its only hypothesis is `¬ IsExplicitlyPermitted …` (Cedar/Thm/Authorization.lean line 93)."),
  q("default_deny is the contrapositive of…", ["allowed_only_if_explicitly_permitted", "forbid_trumps_permit", "order_and_dup_independent"], 0,
    "As its docstring says (Cedar/Thm/Authorization.lean lines 88–91)."),
 ],
 caveats=["Upstream Cedar result (cedar-policy/cedar-spec), not part of the ETNA additions.",
          "Not built for this site."],
 widgets=walk("How the proof goes (Cedar/Thm/Authorization.lean, lines 92-103)", [
  {"text": "Assume the request is not explicitly permitted.", "lean": "intro h₀"},
  {"text": "Name the decision `dec` and argue by contradiction: suppose it isn't deny.",
   "lean": "generalize h₁ : (isAuthorized request entities policies).decision = dec"},
  {"text": "Decisions are allow or deny, so case on `dec`.", "lean": "cases dec"},
  {"text": "If it's allow, the lemma gives an explicit permit, contradicting the hypothesis.",
   "lean": "have h₃ := allowed_only_if_explicitly_permitted request entities policies h₁",
   "link": "Thm.allowed_only_if_explicitly_permitted"},
  {"text": "If it's deny, it contradicts the by-contradiction assumption.", "lean": "case deny => contradiction"},
 ]))


node("Thm.allowed_iff_explicitly_permitted_and_not_denied",
 "The rest of Cedar/Thm/Authorization.lean (grouped)",
 "The decision is fully characterised (allow iff some permit and no forbid), and the authorizer is insensitive to policy order and duplicates. Adding a permit never turns allow into deny, and adding a forbid never turns deny into allow.",
 r"""## Plain English

This node groups the other theorems in Cedar/Thm/Authorization.lean (all upstream Cedar, all with complete proofs in
the source):

- **`allowed_iff_explicitly_permitted_and_not_denied`** (lines 109–123): allow ⇔ explicitly permitted and not
  explicitly forbidden. Proved from [forbid trumps permit](#/node/Thm.forbid_trumps_permit) and
  [allowed only if permitted](#/node/Thm.allowed_only_if_explicitly_permitted).
- **`denied_iff_explicitly_denied_or_not_permitted`** (lines 128–147): the dual for deny.
- **`order_and_dup_independent`** (lines 153–161): if two policy lists have the same members (`≡`, list
  equivalence up to order and duplicates), `isAuthorized` gives the *same response*, not just the same decision.
- **`unchanged_allow_when_add_permit`** (lines 166–174) and **`unchanged_deny_when_add_forbid`** (lines 179–189):
  monotonicity. Note that *adding a permit can still flip deny to allow*, and *adding a forbid can flip allow to deny*;
  these theorems only rule out the other direction.
- **`determiningPolicies_of`**, **`unchanged_determining_when_add_policy_and_decision_unchanged`**,
  **`unchanged_erroring_when_add_policy`**, **`determining_erroring_disjoint_when_unique_ids`** (lines 195–274):
  facts about the diagnostic sets in the response. The last needs policy ids to be unique (`PolicyIdsUnique`,
  lines 29–30).
""",
 [q("Can adding a permit policy change a deny into an allow?", ["Yes, the theorems only rule out allow→deny", "No, never"], 0,
    "`unchanged_allow_when_add_permit` (Cedar/Thm/Authorization.lean lines 166–169) only covers starting from allow."),
  q("Does reordering policies change the response?", ["No: same response, by order_and_dup_independent", "Only the diagnostics may change"], 0,
    "The conclusion is equality of whole responses (Cedar/Thm/Authorization.lean lines 153–156)."),
  q("Which theorem needs unique policy ids?", ["determining_erroring_disjoint_when_unique_ids", "forbid_trumps_permit", "order_and_dup_independent"], 0,
    "Cedar/Thm/Authorization.lean lines 249–251."),
 ])
