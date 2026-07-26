# Module 5 — Pretraining & Scaling Laws

You have the architecture (module 3) and the tokens (module 4). Pretraining is the
multi-million-dollar step where they meet: next-token prediction over a large slice
of human knowledge. This module covers what goes in, what it costs, and the laws
that made labs confident enough to spend the money.

## 5.1 The objective, one more time

Nothing fancy: **cross-entropy on next-token prediction** over trillions of tokens.
The profundity is in what the objective *implies*. To predict the next token well,
across all of the internet, the model is pressured to implicitly learn grammar,
facts, style, sentiment, arithmetic-ish patterns, code semantics, and rudimentary
world modeling — because *all of those reduce prediction error somewhere in the
data*. Compression is the mother of understanding: predicting text well requires
modeling the processes that generate text.

## 5.2 The data

Order-of-magnitude picture of a frontier pretraining mix:

| Source | Notes |
|--------|-------|
| Web crawl (Common Crawl derivatives) | The bulk; heavily filtered — raw crawl is mostly junk |
| Code (GitHub etc.) | Outsized benefits: code improves *reasoning*, not just coding |
| Books, papers, reference | High quality per token; long-range structure |
| Math & scientific content | Deliberately up-weighted in recent models |
| Curated/licensed & synthetic data | The growing frontier (see 5.6) |

The pipeline that matters as much as the architecture:
1. **Extraction** — HTML → clean text.
2. **Quality filtering** — classifiers score "is this worth learning from?"; junk,
   boilerplate, and machine-generated spam are dropped.
3. **Deduplication** — near-duplicate removal at document and n-gram level.
   Duplicates waste compute and encourage memorization.
4. **Mixture weighting** — how often to sample each source. Wikipedia may be seen
   several times; random web pages less than once on average. These weights are
   among the most guarded secrets at every lab.
5. **Decontamination** — scrub benchmark test sets so evals aren't memorized
   (module 15 covers how imperfect this is).

Scale reference points (public info): GPT-3 (2020) ~300B tokens; Chinchilla (2022)
1.4T; Llama 3 (2024) ~15T; frontier models since: tens of trillions, with the
binding constraint shifting from "how much text exists" to "how much *good* text
exists" — the so-called **data wall** (5.6).

## 5.3 Scaling laws: the discovery that changed everything

**Kaplan et al. 2020 (OpenAI)**: loss falls as a smooth **power law** in each of
model parameters N, dataset tokens D, and compute C — over many orders of
magnitude, with no sign of stopping:

```
L(N) ≈ (Nc/N)^αN      L(D) ≈ (Dc/D)^αD      L(C) ≈ (Cc/C)^αC
```

Why this mattered strategically: **capability became a predictable function of
spend**. You could forecast the loss of a 100× bigger run before paying for it.
This graph is why the 2020s became a compute arms race.

**Chinchilla (Hoffmann et al. 2022, DeepMind)** corrected the recipe: for a fixed
compute budget, Kaplan-era models were far too big and undertrained. Optimal
scaling grows N and D **together** — roughly **D ≈ 20 tokens per parameter**.
Chinchilla (70B params, 1.4T tokens) beat Gopher (280B, 300B tokens) using the same
compute. Overnight, everyone's training recipe changed.

**The inference-cost amendment**: Chinchilla optimizes *training* compute only. If
you'll serve the model to millions, a **smaller model trained far beyond
Chinchilla-optimal** (Llama-style: 100+ tokens/param) is cheaper in total. This is
why "small" models kept getting better through 2024–25: labs happily overspend
training compute to save inference compute forever after.

Useful arithmetic (from module 3.8): training FLOPs ≈ **6 · N · D**. A 70B model on
15T tokens ≈ 6.3×10²⁴ FLOPs — weeks on tens of thousands of GPUs.

## 5.4 Emergence and in-context learning

- **In-context learning** (the GPT-3 surprise, 2020): a pretrained LM can perform a
  brand-new task from a few examples *in the prompt*, no weight updates. Nobody
  designed this; it fell out of scale. It's the foundation of all prompting
  (module 9).
- **"Emergent abilities"**: capabilities (3-digit arithmetic, word unscrambling)
  that look absent in small models and suddenly present in large ones. Contested:
  Schaefer et al. argue many "jumps" are artifacts of all-or-nothing metrics over
  smoothly improving log-likelihoods. The pragmatic takeaway: **downstream
  capabilities are hard to predict from loss curves**, even when loss itself is
  perfectly predictable. Both halves of that sentence matter.

## 5.5 The engineering reality

Training a frontier model is a distributed-systems problem:

- **Parallelism**: data parallel (copies of the model, different batches) × tensor
  parallel (split individual matrices across GPUs) × pipeline parallel (split
  layers across GPUs), plus ZeRO/FSDP sharding of optimizer state. Getting high
  utilization (MFU — model FLOPs utilization — of 40–50%) out of 10k+
  interconnected GPUs is elite engineering.
- **Failures are constant** at that scale (GPU dies every few hours); checkpointing
  and automatic restart are load-bearing.
- **Stability**: loss spikes, bf16 numerics, careful init and LR schedules; a
  diverged run at week 6 is millions of dollars.
- **Cost**: rough public estimates — GPT-3 ~$5M; GPT-4-class ~$50–100M+;
  2025-era frontier runs into the hundreds of millions, with clusters themselves
  costing billions.

## 5.6 The data wall and synthetic data

High-quality human text is finite; frontier runs already consume a large fraction
of what's practically harvestable. Responses (all active as of early 2026):

- **Synthetic data**: strong models generate training text — especially math, code,
  and reasoning traces where *correctness can be verified* (unit tests, proof
  checkers) before training on it. Verification is the key that prevents the
  "photocopy of a photocopy" degradation (model collapse).
- **Curriculum & quality over quantity**: better filtering beats more tokens
  (the "textbooks are all you need" line of work).
- **Multi-epoch training** on the best data; licensing private corpora.
- **Shifting compute to post-training and test-time** (modules 7 and 13) — if
  pretraining data saturates, spend the next dollar elsewhere. This is arguably
  *the* strategic story of 2024–2026.

## 5.7 What a base model is (and isn't)

The artifact after pretraining — a **base model** — is a text *continuer*, not an
assistant. Prompt it with "What is the capital of France?" and it may answer, or
continue with nine more quiz questions, because both are plausible continuations of
that text on the internet. It has enormous latent capability and no interface.
Module 7 (post-training) is what installs the interface.

## Mental models to carry forward

1. **Loss is predictable; capabilities less so.** Scaling laws de-risked the spend.
2. **Chinchilla: params and tokens scale together**; inference costs push you to
   overtrain small models.
3. **Data pipeline quality is a first-class differentiator** — likely more secret
   sauce there than in architecture.
4. **6ND** — the FLOPs formula worth memorizing.
5. A base model is **capability without an interface**.

## Exercises

1. Compute training FLOPs for: GPT-3 (175B, 300B tokens), Chinchilla (70B, 1.4T),
   Llama-3-8B (8B, 15T). Which is Chinchilla-optimal? Which is deliberately not,
   and why?
2. Using 6ND and an H100 at ~10¹⁵ FLOPs/s at 40% MFU, estimate GPU-hours for each.
3. Download a small **base** model (e.g. a Llama or Qwen base checkpoint) and a
   its instruct sibling. Give both "What is the capital of France?" and compare.
   You'll never confuse base and chat models again.
4. Read the Chinchilla abstract and reproduce the 20-tokens/param rule from its
   Table 3 numbers.

## Further reading

- Kaplan et al., *Scaling Laws for Neural Language Models* (2020).
- Hoffmann et al., *Training Compute-Optimal Large Language Models* (2022).
- Brown et al., *Language Models are Few-Shot Learners* (GPT-3 paper, 2020).
- The Llama 3 technical report (2024) — the most detailed public account of a
  modern pretraining pipeline.
- Karpathy's *"Let's reproduce GPT-2 (124M)"* video — pretraining end to end, for
  real, on a budget.
