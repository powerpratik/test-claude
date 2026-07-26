# Module 13 — Reasoning Models & Test-Time Compute

The biggest paradigm shift since ChatGPT: models that **think before answering**,
and get smarter the longer they think. This module explains the second scaling
axis and how it was trained into existence.

## 13.1 The idea in one line

Pretraining scaling (module 5) buys intelligence at **training time**; reasoning
models add a dial to buy more at **inference time** — spend 10 seconds or 10
minutes of tokens on a problem and accuracy climbs with a *log-linear-ish* curve,
much as it does with training compute. Two dials now, not one.

The seed was already in module 9: chain-of-thought tokens buy serial computation.
Reasoning models make CoT *long, learned, and load-bearing* instead of a
prompting trick.

## 13.2 The lineage

- **o1 (OpenAI, late 2024)** — first production model trained via RL to emit a
  long private chain of thought before its answer. Jumped from ~12% (GPT-4o) to
  ~74–93% on AIME math; solved PhD-level science questions (GPQA) above expert
  level. Introduced the "reasoning effort" dial.
- **DeepSeek-R1 (Jan 2025)** — the open-weights replication that demystified the
  recipe (13.3) and showed it cheaply; caused a market panic and a research
  stampede. Its distilled small models put visible reasoning on laptops.
- **Since then**: o3/o4, Gemini's thinking models, Claude's extended thinking,
  Qwen's QwQ/Qwen3 hybrid modes… By early 2026 "thinking mode" is a standard
  feature, often as a **hybrid**: one model that answers instantly or thinks
  long, chosen per request (manually or by an internal router).
- Milestone results along the way: IMO gold-medal-level performance on formal
  math (2025), Codeforces ratings above nearly all humans, ARC-AGI-1 cracked by
  o3 with massive test-time compute (at ~$1k+/task — capability and economics
  are separate questions).

## 13.3 How it's trained (the R1 recipe, simplified)

Module 7.4's RL-with-verifiable-rewards, pushed hard:

1. Take a strong base model.
2. Give it math/code problems where correctness is **checkable** (exact answer,
   unit tests).
3. RL (GRPO): sample many attempts per problem; reward the correct ones; update.
   No human labels, no learned reward model to hack — the verifier is ground
   truth.
4. What *emerges* without being explicitly taught: longer and longer chains of
   thought, self-checking ("wait, let me verify step 3"), backtracking, trying
   alternative approaches — visible in R1's raw traces. The RL discovered that
   these behaviors earn reward; nobody hand-wrote them. (R1's famous "aha
   moment" logs.)
5. Blend with SFT + preference RL (module 7) so the thinker is also a usable,
   safe assistant; distill traces into smaller models.

The profound part: **reasoning strategies were *found* by optimization, not
imitated from humans** — the same lesson as AlphaGo's move 37, arriving in
language.

## 13.4 Test-time compute, beyond one long chain

Ways to convert inference FLOPs into accuracy:

- **Longer serial thinking** (the trained default above).
- **Parallel sampling + selection**: best-of-N with a verifier or majority vote
  (self-consistency, module 9.2) — o3's ARC result and IMO systems used heavy
  parallel search.
- **Iterative refinement**: draft → critique → revise loops.
- The engineering flip side: thinking tokens are output tokens (module 8's
  expensive kind) — hence per-request effort dials, routers that reserve deep
  thinking for hard queries, and a renewed premium on inference efficiency.

## 13.5 Caveats and open questions (honest section)

- **Faithfulness**: the visible chain of thought is not guaranteed to be the
  *actual cause* of the answer — models can reach correct answers with flawed
  traces and vice versa; interpretability work (module 16) treats CoT as
  evidence, not gospel. Monitoring CoT for misbehavior is valuable but
  gameable — labs are actively studying when optimization pressure makes CoT
  *less* honest.
- **Overthinking**: on easy questions long deliberation can *hurt* (and always
  costs); routing/effort-calibration is an active area.
- **Generalization**: gains are largest where rewards were verifiable (math,
  code, structured analysis); transfer to open-ended judgment is real but
  weaker. "Reasoning" here = trained deliberation strategies, not a claim about
  consciousness or general human-style thought.
- **Benchmark saturation**: reasoning models ate most existing evals within a
  year — module 15's arms race.

## Mental models to carry forward

1. **Two scaling dials now**: training compute and test-time compute; frontier
   progress since 2024 is largely the second dial.
2. **Verifier + RL ⇒ emergent deliberation** — self-correction was discovered,
   not scripted.
3. Thinking is priced in tokens: **capability and cost are now a per-request
   trade-off**, which changes product and serving design (modules 8, 12).
4. CoT is evidence about the model's process, **not a transcript of it**.

## Exercises

1. Run the same 5 AMC/AIME-style problems against a non-reasoning model and a
   reasoning model (or the same hybrid model with thinking off/on). Tabulate
   accuracy and token cost. Compute $/correct-answer — the metric that actually
   matters.
2. Implement best-of-8 with majority vote over a *non*-reasoning model on those
   problems. How much of the reasoning model's gap do you close? At what cost?
3. Read one full R1 reasoning trace (they're public). Highlight every
   self-check and backtrack. Then find one place the trace is confused but the
   final answer is right anyway (13.5's faithfulness point, live).
4. Find a trivially easy question where a reasoning model burns 2,000+ thinking
   tokens. Reflect on 13.5's overthinking problem and how you'd route around it.

## Further reading

- OpenAI, *Learning to Reason with LLMs* (o1 post, 2024).
- DeepSeek-R1 paper (2025) — the most important open paper of the era; actually
  read it.
- Snell et al., *Scaling LLM Test-Time Compute Optimally…* (2024).
- Anthropic/OpenAI/DeepMind posts on chain-of-thought monitoring and
  faithfulness (2025) — for 13.5.
