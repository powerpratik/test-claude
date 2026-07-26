# Module 15 — Evaluation

"How good is this model?" is the hardest question in the field — harder than
training, by common admission. This module covers public benchmarks and their
failure modes, then the part that pays your salary: evaluating **your own**
application.

## 15.1 Why eval is hard

Outputs are open-ended (many right answers), capabilities are jagged (superhuman
at X, silly at Y — a single number misleads), test sets leak into training data,
and models improve faster than benchmarks are built. Every number you read comes
with these asterisks.

## 15.2 The public benchmark landscape

| Benchmark | Measures | Status (early 2026) |
|---|---|---|
| MMLU / MMLU-Pro | broad multiple-choice knowledge | saturated / near-saturated at frontier |
| GSM8K, MATH | school/competition math | saturated — replaced by AIME, HMMT, FrontierMath |
| GPQA (Diamond) | PhD-level science, "Google-proof" | reasoning models exceed expert baseline |
| HumanEval → LiveCodeBench, Codeforces | coding | HumanEval saturated; live/contest evals current |
| **SWE-bench (Verified)** | real GitHub issues fixed end-to-end by an *agent* | the flagship applied benchmark; ~frontier race territory |
| ARC-AGI-1/2 | abstract fluid reasoning | 1 cracked with heavy test-time compute; 2 open |
| Humanity's Last Exam, FrontierMath | expert-frontier knowledge/math | current headroom benchmarks |
| **LMArena (Chatbot Arena)** | blind human preference, Elo | the vibes-check; huge sample, own biases (15.3) |
| τ-bench, GAIA, OSWorld, BrowseComp | tool-use/agentic tasks | the active frontier of eval-building |

Trajectory to internalize: knowledge quizzes → reasoning problems → **agentic
task completion**. Evals moved from "what do you know" to "what can you do,"
tracking modules 12–13. (For long-horizon agentic work, METR's
time-horizon studies — how long a task a model can complete at 50% reliability —
became a widely quoted capability curve, doubling every ~4–7 months.)

## 15.3 How benchmark numbers lie

- **Contamination**: test questions leak into pretraining crawls despite
  decontamination (module 5.2); suspiciously exact memorization is repeatedly
  documented. Private/live/rotating sets (LiveBench, contest problems by date)
  are the countermeasure.
- **Benchmarkmaxxing**: labs optimize for headline evals (it's marketing);
  gains don't fully transfer off-benchmark. Goodhart, again (module 7.1).
- **Harness sensitivity**: few-shot count, prompt format, sampling settings,
  and answer-extraction regexes move scores by whole points; cross-paper tables
  are rarely apples-to-apples. Agentic scores depend on scaffold as much as
  model.
- **Preference ≠ quality**: arena Elo rewards confident, long, well-formatted,
  sycophantic answers (modules 7.5, 9.4) — style leaks into "capability"
  ratings; style-controlled Elo exists precisely because of this.
- **Saturation compresses signal**: between 88% and 91% on a saturated eval
  lies mostly noise and contamination, not capability.

Reading rule: trust *relative* movement across many evals + held-out/live sets +
your own testing; discount any single headline number.

## 15.4 LLM-as-judge

Human review doesn't scale, so models grade models — powering arena analyses,
RLAIF (module 7.3), RAG faithfulness scores (module 11.6), and most production
eval pipelines. Known biases, all measurable and partially correctable:
position bias (judges prefer answer A — randomize order), length bias (longer
looks better — control it), self-preference (models favor their own family),
sycophancy toward confident tone, and insensitivity to subtle factual errors
(pair with ground truth where possible). Used carefully — rubrics, pairwise
comparisons, order randomization, spot-audits against human labels — judges are
reliable *enough* to be the workhorse. Used naively they launder noise into
dashboards.

## 15.5 Evaluating your application (the part that matters)

The public boards tell you which base model to start from; they say nothing
about *your* task. The craft:

1. **Build a golden set from real traffic**: 50–200 real inputs, labeled with
   expected outcomes. Start day one; grow it with every production failure
   (each bug becomes a permanent regression test). This set is worth more than
   any framework.
2. **Grade with the cheapest sufficient method**, in order: exact/programmatic
   checks (schema valid? number correct? test passes? — free and perfect when
   applicable) → LLM judge with a written rubric (for fuzzy quality) → human
   review (calibrate the judge; audit samples).
3. **Wire it like CI**: every prompt change, model swap, or retrieval tweak
   runs the suite; diffs reviewed before deploy (prompts are code — module 9.3).
   Track per-case results, not just the average, so you see *which* cases
   regressed.
4. **Close the loop in production**: log traces (module 12.3), sample and
   grade continuously, feed failures back into the golden set (and later into
   fine-tuning data, module 10.5). Tools exist (promptfoo, Braintrust,
   LangSmith, OpenAI Evals) but the discipline, not the tool, is the value.

Teams that do this ship LLM features like software; teams that don't ship vibes
and roll back a lot.

## Mental models to carry forward

1. **All benchmarks decay** — contamination + optimization + saturation is the
   life cycle; live and agentic evals are the current refuge.
2. Capabilities are **jagged**; demand eval *profiles*, not single scores.
3. **LLM judges are biased instruments** — usable once you've measured the bias.
4. Your golden set from real traffic is the only benchmark that can't lie to
   you about your app.

## Exercises

1. Pick a saturated benchmark (GSM8K) and a current one (recent AIME). Run a
   small open model on 20 problems of each with two different prompt formats.
   Observe harness sensitivity (15.3) firsthand.
2. Build a 30-case golden set for any earlier exercise's pipeline (the module
   11 RAG one is ideal). Add programmatic checks where possible and an LLM
   judge with a 4-line rubric for the rest.
3. Measure your judge: grade 20 outputs yourself, compare to the judge's
   grades, compute agreement. Then swap the order of pairwise candidates and
   measure position bias.
4. Take one production-style failure, add it to the golden set, "fix" it via
   prompt change, and confirm no other case regressed. You've just done real
   LLM engineering.

## Further reading

- Zheng et al., *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena* (2023).
- SWE-bench and τ-bench papers — how agentic evals are constructed.
- LiveBench / LiveCodeBench — the contamination-resistant design pattern.
- METR, *Measuring AI Ability to Complete Long Tasks* (2025).
- Hamel Husain, *Your AI Product Needs Evals* — the practitioner's essay.
