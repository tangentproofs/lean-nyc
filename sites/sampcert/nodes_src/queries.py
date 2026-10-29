NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}
def walk(title, steps):
    return [{"type": "walkthrough", "title": title, "config": {"steps": steps}}]

NOT_BUILT = ("Not built for this site: \"proved\" means the source contains a complete-looking proof, and a text "
             "search of the project finds no `sorry`, `admit` or `axiom`. Lean's kernel was not run here.")


node("privNoisedHistogram",
 "privNoisedHistogram: counting records per bin, with noise",
 "A histogram sorts records into numBins bins with a user-supplied function, counts each bin, and adds independent "
 "noise from the chosen DP system to each count, with the budget split evenly.",
 r"""## Plain English

In DifferentialPrivacy/Queries/Histogram/Code.lean:

- `Bins T numBins` (lines 19–20) is a function `bin : T → Fin numBins` that assigns each record to a bin.
- `Histogram T numBins B` (lines 44–45) is a vector of numBins integers (counts may be negative after noise).
  `emptyHistogram` (lines 53–56) is all zeros, and `setCount` (lines 105–106) overwrites one entry.
- `exactBinCount b l` (lines 93–94) is the number of records of l in bin b.
- `privNoisedBinCount ε₁ ε₂ b` (lines 99–100) noises that count with the system's noise, sensitivity 1 and
  parameters (ε₁, ε₂·numBins).
- `privNoisedHistogramAux` (lines 108–115) fills bins 0…n one at a time, each step a composition followed by a
  post-processing.
- **`privNoisedHistogram ε₁ ε₂`** (lines 121–122) runs it for all bins.

`privMaxBinAboveThreshold` (lines 140–143) post-processes the noised histogram to report the highest bin whose
noisy count exceeds τ. Its privacy (`privMaxBinAboveThreshold_DP`, DifferentialPrivacy/Queries/Histogram/Properties.lean lines 86–92) is free by
post-processing.
""",
 [q("Where does the bin of a record come from?", ["A user-supplied function bin : T → Fin numBins", "The record's position in the list", "A hash chosen by SampCert", "Random"], 0,
    "Histogram/Code.lean lines 19–20."),
  q("What noise parameters does each bin use?", ["(ε₁, ε₂·numBins), i.e. 1/numBins of the budget", "(ε₁, ε₂)", "(ε₁·numBins, ε₂)", "None"], 0,
    "privNoisedBinCount, lines 99–100."),
 ])


node("sv1_aboveThresh",
 "sv1_aboveThresh: the executable AboveThreshold program",
 "Draw a noisy threshold once, then walk through the queries, adding fresh noise to each, and stop at the first one "
 "whose noisy value reaches the threshold. Output its index.",
 r"""## Plain English

In DifferentialPrivacy/Queries/AboveThresh/Code.lean:

- `sv_query sv_T` (line 47) is a sequence of queries: for each index k, a map from lists of records to integers.
- `privNoiseZero ε₁ ε₂` (line 32) is the DP system's noise applied to the constant query 0. In the pure DP
  instance it is a discrete Laplace sample of scale ε₂/ε₁.
- `privNoiseThresh ε₁ ε₂` (line 36) uses scale 2ε₂/ε₁, and `privNoiseGuess ε₁ ε₂` (line 34) uses scale 4ε₂/ε₁
  (`sens_cov_τ` = 1, `sens_cov_vk` = 2, lines 20–25).
- `sv1_aboveThresh qs T ε₁ ε₂ l` (lines 63–67): draw τ from privNoiseThresh, then run a
  [probWhile](#/node/probWhile) loop. The state is the list of noises so far and the current noise. The loop
  continues while qs k (l) + noise < τ + T (`sv1_aboveThreshC`, lines 55–56), drawing a new noise each time
  (`sv1_aboveThreshF`, lines 59–61). It returns the number k of queries that were below the threshold, which is the
  index of the first query above it.

The privacy proof needs a version where all noise is drawn up front. Program versions sv2 to sv9 in
AboveThresh/Properties.lean rearrange it step by step, each proved equal to the last; see
[sv9_aboveThresh_SPMF](#/node/sv9_aboveThresh_SPMF).
""",
 [q("When does the loop stop?", ["At the first k with qs k (l) + noise_k ≥ τ + T", "After T iterations", "When the noise is positive", "Never"], 0,
    "sv1_aboveThreshC (DifferentialPrivacy/Queries/AboveThresh/Code.lean lines 55–56) is the continue condition qs k l + noise < τ + T."),
  q("How do the threshold and query noise scales compare?", ["The query noise has twice the threshold's scale (4ε₂/ε₁ vs 2ε₂/ε₁)", "They are equal", "The threshold noise is larger", "There is no threshold noise"], 0,
    "DifferentialPrivacy/Queries/AboveThresh/Code.lean lines 34–36 with sens_cov_vk = 2, sens_cov_τ = 1."),
 ])


node("sv9_aboveThresh_SPMF",
 "sv9_aboveThresh_SPMF and has_lucky: AboveThreshold as a proper distribution",
 "sv9 is a rearranged form of AboveThreshold that computes the probability of each output directly, proved equal to "
 "the executable sv1 through eight program equalities. Under the 'lucky guess' hypothesis it is a genuine probability "
 "distribution.",
 r"""## Plain English

In DifferentialPrivacy/Queries/AboveThresh/Properties.lean:

- **The equality chain.** `sv1_sv2_eq` (lines 431–435), `sv2_sv3_eq`, …, `sv8_sv9_eq` (lines 1782–1796) prove that
  nine versions of the program are the same distribution. Along the way the proof turns the loop into a recursion
  (sv3), presamples all the noise (`sv4_presample`, lines 741–747), and introduces the running maximum G of the
  noisy queries from the Dwork–Roth proof (`sv8_G`, lines 1676–1679).
- **sv9** (`sv9_aboveThresh`, lines 1762–1780) gives the probability of output k directly. For k = 0 it is the
  probability that query 0's noisy value is ≥ τ + T. For k > 0 it is the probability that queries 0…k−1 stay
  below and query k reaches τ + T (`sv8_cond`, lines 1681–1682).
- **`has_lucky qs T`** (lines 1802–1803): for every τ and list l there is K such that qs A (l) + K′ ≥ τ + T for
  all A and all K′ ≥ K. So a big enough noise draw always stops the loop.
- `sv1_hasSum_one` (lines 2195–2200) uses it to prove sv1's probabilities sum to 1. The lower bound `sv1_lb`
  (lines 1897–2191) shows each iteration has a fixed positive chance of stopping. `sv1_aboveThresh_PMF` (lines
  2202–2203) and **`sv9_aboveThresh_SPMF`** (lines 2208–2219) package the two versions as SPMFs.

Both are built with the pure DP system (Laplace noise).
""",
 [q("Why is has_lucky needed?", ["Without a lower bound on the queries, the loop might run forever with positive probability", "To make queries 1-sensitive", "To choose ε", "It is not used"], 0,
    "It is the hypothesis of sv1_hasSum_one (lines 2195–2200)."),
  q("How is sv9 related to the executable sv1?", ["They are proved equal as distributions via sv1_sv2_eq … sv8_sv9_eq", "sv9 is an approximation", "sv9 is a different algorithm", "They are assumed equal"], 0,
    "The equalities are chained in sv9_aboveThresh_SPMF's proof, lines 2211–2219."),
 ],
 caveats=["has_lucky is a real restriction: for example, it fails for a query family whose values on some list are "
          "not bounded below. The exactDiffSum family used by [privUnboundedMax_DP](#/node/privUnboundedMax_DP) "
          "satisfies it (`lucky_guess`, UnboundedMax/Code.lean lines 69–103)."])


node("privUnboundedMax_DP",
 "Key result: a private maximum with no upper bound on the data",
 "SampCert's unbounded-max query estimates the maximum of a list of natural numbers without assuming any bound on "
 "them, by running AboveThreshold on differences of clipped sums. It is ε₁/ε₂ pure-DP, with no extra hypotheses.",
 r"""## Plain English

**Lemma (`privUnboundedMax_DP`, DifferentialPrivacy/Queries/UnboundedMax/Privacy.lean lines 57–58).** The mechanism
`privUnboundedMax ε₁ ε₂` (UnboundedMax/Code.lean lines 105–106) is pure DP at level ε = ε₁/ε₂.

The mechanism is [AboveThreshold](#/node/sv1_aboveThresh) with threshold T = 0 on the queries
exactDiffSum m (l) = Σ min(x, m) − Σ min(x, m+1) (DifferentialPrivacy/Queries/UnboundedMax/Code.lean line 29). That is minus the number of records
greater than m, so it reaches 0 once m passes the maximum. The README links this kind of "unbounded" query to
arXiv:1909.01917.

The proof shows each query is 1-sensitive (`exactDiffSum_sens`, DifferentialPrivacy/Queries/UnboundedMax/Privacy.lean lines 21–55), that the queries
satisfy [has_lucky](#/node/sv9_aboveThresh_SPMF) (`lucky_guess`), and then rewrites the executable program into sv9
with the equality chain (lines 70–71) and applies the headline
[sv9_aboveThresh_pmf_DP](#/node/sv9_aboveThresh_pmf_DP). It is the one place in the repository where AboveThreshold's
privacy is transferred to the executable sv1 program.
""",
 [q("Does privUnboundedMax_DP need a bound on the data values?", ["No", "Yes, a maximum U", "Yes, the list length", "Only for ε < 1"], 0,
    "The statement (lines 57–58) has only the hypothesis ε = ε₁/ε₂."),
  q("How does the proof connect the executable program to sv9?", ["By rewriting with sv8_sv9_eq, …, sv1_sv2_eq", "By testing", "By assumption", "It does not"], 0,
    "UnboundedMax/Privacy.lean lines 70–71."),
 ],
 caveats=[NOT_BUILT])


node("privSparse_DP",
 "Sparse vector: c rounds of AboveThreshold cost c·ε (CONDITIONAL)",
 "The sparse vector technique repeats AboveThreshold c times on the remaining queries. Its theorem says the result is "
 "c·ε-private, but it takes the privacy of each AboveThreshold round as a hypothesis rather than proving it.",
 r"""## Plain English

`privSparse T ε₁ ε₂ qs HL c` (DifferentialPrivacy/Queries/Sparse/Code.lean lines 47–48) runs
[AboveThreshold](#/node/sv1_aboveThresh) c times. Each round restarts on the queries after the last reported index
(`shift_qs`, line 23), and the reported indices are collected into a list (lines 37–45). The code comments cite the
proof of Theorem 3.25 in Dwork and Roth.

**Lemma (`privSparse_DP`, Sparse/Privacy.lean lines 55–58).** In any DP system, *if* every shifted AboveThreshold
round is private at level ε = ε₁/ε₂ (hypothesis `HDP`), then privSparse is c·ε-private. The proof (lines 32–53) is c
uses of adaptive composition.

**This is CONDITIONAL.** `HDP` is not discharged anywhere in the repository. For the pure DP system it should
follow from [sv9_aboveThresh_pmf_DP](#/node/sv9_aboveThresh_pmf_DP) plus the sv1 = sv9 equality chain, as in
[privUnboundedMax_DP](#/node/privUnboundedMax_DP), but that lemma is not stated. Also note that the program always
uses the Laplace-based AboveThreshold, whatever DP system `dps` the privacy is claimed for.
""",
 [q("What does privSparse_DP assume?", ["That each AboveThreshold round is ε₁/ε₂-private in the chosen system", "Nothing", "That c = 1", "That queries are bounded"], 0,
    "Hypothesis HDP, Sparse/Privacy.lean line 56."),
 ],
 caveats=["CONDITIONAL: the per-round privacy hypothesis `HDP` is never proved in the repository."])


node("privNoisedBoundedMean_DP",
 "Other verified queries: count, sums, means, parallel histogram",
 "Besides the histogram and AboveThreshold, SampCert proves privacy for a family of small queries, each generic over "
 "the DP system. Every proof is a few lines on top of the noise guarantee, composition and post-processing.",
 r"""## Plain English

All in DifferentialPrivacy/Queries/, each generic over a [DPSystem](#/node/DPSystem) with noise:

- **Count** (`privNoisedCount_DP`, Count/Properties.lean lines 46–50): the list length plus noise. It is
  1-sensitive, so it gets level ε whenever `noise_priv ε₁ ε₂ ε`.
- **Bounded sum** (`privNoisedBoundedSum_DP`, BoundedSum/Properties.lean lines 64–67): Σ min(x, U) over a list of
  naturals plus noise. It is U-sensitive.
- **Bounded mean** (`privNoisedBoundedMean_DP`, BoundedMean/Properties.lean lines 35–48): noisy sum / noisy count,
  each with half the budget (BoundedMean/Code.lean lines 24–27). Level ε if each half gets ε/2. The top-level
  SampCert.lean restates it for both systems (`combineConcentrated`, `combinePure`).
- **Histogram mean** (`privMeanHistogram_DP`, HistogramMean/Properties.lean lines 46–66): use a noised histogram
  to choose a clipping bound, then a bounded mean. Level εA + εB.
- **Parallel histogram** (`privParNoisedHistogram_DP`, ParHistogram/Properties.lean lines 70–75): for systems
  with parallel composition (`DPPar`, so pure DP), the whole histogram costs only one bin's ε, because each record
  lands in one bin.

The "noised" versions all return a single sample. The division in the bounded mean is post-processing of the two
noisy values.
""",
 [q("In the bounded mean, how is the budget split?", ["Half to the noisy sum, half to the noisy count", "All to the sum", "By the number of records", "Not at all"], 0,
    "BoundedMean/Code.lean lines 24–27 use (ε₁, 2ε₂) for both; the hypothesis gives ε/2 each (DifferentialPrivacy/Queries/BoundedMean/Properties.lean line 36)."),
  q("Why can the parallel histogram be cheaper than the ordinary one?", ["Each record affects only one bin, so parallel composition charges the max, not the sum", "It uses less noise per bin by accident", "It skips empty bins", "It is not cheaper"], 0,
    "DPPar.prop_par charges max ε₁ ε₂ (Abstract.lean lines 136–138)."),
 ],
 caveats=[NOT_BUILT])


EXTRA = {
 "privNoisedHistogram": [q("What does privMaxBinAboveThreshold cost beyond the noised histogram?", ["Nothing: it is post-processing", "Another ε", "ε/numBins", "It is not private"], 0,
    "privMaxBinAboveThreshold_DP, Histogram/Properties.lean lines 86–92.")],
 "sv1_aboveThresh": [q("What type does sv1_aboveThresh return?", ["SLang ℕ, a distribution over indices", "A list of noisy answers", "A Bool", "A histogram"], 0,
    "DifferentialPrivacy/Queries/AboveThresh/Code.lean line 63.")],
 "sv9_aboveThresh_SPMF": [q("Which DP system are sv1_aboveThresh_PMF and sv9_aboveThresh_SPMF built with?", ["PureDPSystem with Laplace noise", "zCDPSystem", "Any DPSystem", "None"], 0,
    "DifferentialPrivacy/Queries/AboveThresh/Properties.lean lines 2196 and 2209.")],
 "privUnboundedMax_DP": [q("What is exactDiffSum m l?", ["Minus the number of records greater than m", "The sum of the list", "The maximum", "m"], 0,
    "Σ min(x, m) − Σ min(x, m+1) loses 1 for each x > m (UnboundedMax/Code.lean lines 20–29).")],
 "privSparse_DP": [q("What privacy level does privSparse_DP give for c rounds?", ["c·ε", "ε", "√c·ε", "ε/c"], 0,
    "Sparse/Privacy.lean line 58."),
   q("Is the hypothesis HDP proved anywhere in the repository?", ["No", "Yes, in Sparse/Privacy.lean", "Yes, by sv9_aboveThresh_pmf_DP directly", "It is an axiom"], 0,
    "A search for privSparse_DP finds only its definition; nothing instantiates HDP.")],
 "privNoisedBoundedMean_DP": [q("Which queries here need a DPPar system rather than any DPSystem?", ["The parallel histogram", "The count", "The bounded mean", "All of them"], 0,
    "ParHistogram/Properties.lean line 24: [dps : DPPar T].")],
}
for n in NODES:
    n["quiz"] += EXTRA.get(n["id"], [])
