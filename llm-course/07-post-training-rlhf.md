# Module 7 — Post-Training: SFT, RLHF & Friends

A base model (module 5.7) completes text; it doesn't help you. Post-training is the
comparatively cheap stage (a sliver of pretraining's compute — though a growing one)
that turns the raw predictor into an assistant with a personality, instruction
following, and refusals. This is where ChatGPT actually came from.

## 7.1 The three-stage pipeline (InstructGPT, 2022)

```
Base model → (1) SFT → (2) Reward model → (3) RL (PPO) → Assistant
```

### Stage 1 — Supervised fine-tuning (SFT)

Collect (prompt → ideal response) pairs written or curated by humans; fine-tune
with the ordinary next-token loss on the *response* tokens. Tens of thousands to
millions of examples. After SFT the model reliably plays the "assistant" character
in the chat format (module 4.3's special tokens).

Why not stop here? Three limits:
- Writing perfect demonstrations is expensive and caps at human ability.
- **Judging** an answer is easier than *writing* one — comparison data is cheaper.
- SFT teaches imitation, including imitation of *format* without *truth* — it can't
  express "of two fluent answers, this one is better/more honest."

### Stage 2 — Reward model (RM)

Sample several model responses per prompt; humans **rank** them. Train a separate
model (usually the LLM with a scalar head) to predict the preferred one
(Bradley–Terry loss on pairs). The RM compresses human preference into a cheap,
callable function `r(prompt, response) → score`.

### Stage 3 — RL against the reward model

Optimize the policy (the LLM) to maximize RM score using **PPO** (proximal policy
optimization), with a crucial extra term: a **KL penalty** keeping the policy close
to the SFT model. Without it, the policy finds degenerate texts the RM overrates —
**reward hacking** (sycophantic flattery, confident verbosity, hedging boilerplate
— many classic LLM annoyances are literally artifacts of over-optimized reward
models). Goodhart's law is the central engineering reality of this stage.

## 7.2 DPO and the simplification wave

PPO works but is heavy: four models in memory (policy, reference, RM, value
network), unstable training, lots of tuning.

**DPO (Direct Preference Optimization, 2023)** collapses stages 2–3: a bit of
algebra shows the RLHF objective has a closed-form optimal policy, yielding a
simple classification-style loss directly on preference pairs — no reward model,
no RL loop:

> Raise the likelihood gap between chosen and rejected responses, weighted by how
> wrong the current policy is about the pair, anchored to the reference model.

DPO (and cousins: IPO, KTO, ORPO, SimPO) became the default for open-weights
post-training. Frontier labs generally still use online RL variants (PPO-family,
GRPO — see 7.4) because sampling *fresh* responses during training ("on-policy")
outperforms optimizing a static preference dataset, at higher cost.

## 7.3 RLAIF and Constitutional AI

Human feedback is slow, pricey, inconsistent — and eventually the bottleneck.
**RLAIF** replaces the human rater with an LLM rater. Anthropic's **Constitutional
AI**: give a model an explicit list of principles ("constitution"); it critiques
and revises its own outputs against them (making SFT data), and judges preference
pairs (making RM data). Humans write the principles, not the labels. Every lab now
uses AI feedback heavily; pure-human labeling is a shrinking share.

## 7.4 RL with verifiable rewards (the 2024–26 shift)

Preference RL optimizes *"what raters like."* The newer wave optimizes *"what is
checkably correct"*: math answers checked exactly, code run against unit tests,
tool-use trajectories scored by task completion. No reward model to hack — the
reward is ground truth.

- **GRPO** (group relative policy optimization, DeepSeek): sample a group of
  responses per prompt, use the group's mean reward as the baseline — no value
  network, much lighter than PPO. Used to train R1's reasoning (module 13).
- This is the bridge to reasoning models: RLVR on math/code is precisely what
  taught models to produce long, self-correcting chains of thought.
- Limit: it needs a verifier, so it shines on math/code/agentic tasks and is hard
  to apply to "write a beautiful essay."

## 7.5 What post-training actually changes (and doesn't)

- It's a **behavioral interface** over pretrained capability: style, format,
  persona, refusals, tool-calling syntax. The knowledge overwhelmingly comes from
  pretraining. ("Superficial alignment hypothesis" — LIMA got a decent assistant
  from just 1k excellent SFT examples.)
- **Refusals and safety behavior** live here (with module 16 covering why they're
  brittle).
- **The alignment tax / calibration cost**: base models are surprisingly
  well-calibrated probability estimators; heavy post-training can skew calibration
  and inject sycophancy. Labs actively tune against both.
- Practical corollary: when a model "won't shut up" or over-apologizes, you're
  seeing RM preferences, not architecture.

## 7.6 The modern pipeline in practice (early 2026)

Real frontier post-training is a **many-stage soup**, iterated for months:
SFT on curated + synthetic data → preference RL (human + AI feedback) → RLVR on
math/code/agentic tasks → targeted safety training → distillation of all of it
into smaller siblings. Public models' "tech reports" (Llama 3, Qwen, DeepSeek,
Tülu 3) document versions of this openly and are the best way to see inside.

## Mental models to carry forward

1. **SFT teaches the format; RL teaches the preference; RLVR teaches correctness.**
2. **Judging is cheaper than writing** — that asymmetry is why RLHF exists.
3. **Goodhart is the boss fight**: every proxy reward gets hacked; the KL leash
   and ground-truth verifiers are the countermeasures.
4. Post-training is an interface over pretrained capability — thin relative to
   pretraining, but it *is* the product.

## Exercises

1. Take an open base model and its instruct sibling (e.g. Qwen base vs instruct).
   Prompt both with a naked question and diff behaviors. Then jailbreak-format the
   base model into answering ("Q: … A:") — what does that tell you about where
   "helpfulness" lives?
2. Run a DPO fine-tune with HuggingFace TRL on a small model (1–3B) using a public
   preference dataset (e.g. UltraFeedback). Compare pre/post responses on 10
   prompts.
3. Design a reward function for "write a good summary" and then brainstorm five
   ways a policy could hack it without summarizing well. (This is harder and more
   instructive than it sounds.)
4. Read the InstructGPT paper's Figure 1 and explain why 1.3B InstructGPT beat
   175B GPT-3 in human preference — what does that imply about capability vs
   interface?

## Further reading

- Ouyang et al., *Training language models to follow instructions* (InstructGPT,
  2022) — the founding document.
- Rafailov et al., *Direct Preference Optimization* (2023).
- Bai et al., *Constitutional AI* (2022).
- Lambert et al., *Tülu 3* (2024) — the most complete open post-training recipe.
- DeepSeek-R1 paper (2025) — GRPO and RLVR at scale (pairs with module 13).
