# Module 10 — Fine-Tuning in Practice

You rarely need to train a model from scratch (module 5: that costs millions). You
often *think* you need to fine-tune. This module covers when you actually do, and
the parameter-efficient toolbox that makes it cheap when you do.

## 10.1 Decision framework first

Fine-tuning is the *third* tool, not the first:

| Your problem | Right tool |
|---|---|
| Model lacks **your private facts** | RAG (module 11) — facts belong in context, where they're updatable and citable |
| Model misbehaves on a **describable** task | Prompting (module 9) — iterate at zero training cost |
| Model can't reliably hit a **style/format/dialect**, prompt is maxed out | **Fine-tune** |
| Latency/cost: replace GPT-class calls with a small model for one narrow task | **Fine-tune** (often distillation: train on the big model's outputs) |
| Domain language (legal, medical, your codebase's idioms) | Fine-tune, often + RAG |
| Model lacks reasoning ability | Mostly none of the above — pick a better base model |

Two spicy but load-bearing facts:
- **Fine-tuning is bad at adding knowledge.** New facts are stored brittlely and
  increase hallucination (the model learns to *state* things confidently in your
  domain, not to *know* them). Behavior/style/format is where fine-tuning shines.
- **A fine-tuned small model routinely beats a prompted frontier model** on one
  narrow, well-defined, data-rich task — at 10–100× lower cost. That's the
  economic case in one sentence.

## 10.2 Full fine-tuning vs PEFT

**Full fine-tuning** updates all weights: best quality ceiling, but needs
training-grade memory (weights + gradients + Adam states ≈ **16 bytes/param** —
~112GB for a 7B model) and produces a full-size artifact per task. Also risks
**catastrophic forgetting** of general ability if the data is narrow.

**PEFT** (parameter-efficient fine-tuning) freezes the base model and trains a
small add-on. The winner of this category:

### LoRA (Low-Rank Adaptation)

For chosen weight matrices W (attention projections, MLPs), learn a low-rank
update:

```
W' = W + (α/r) · B·A      A: r×d, B: d×r,  r « d  (r = 8–64 typical)
```

Only A and B train — commonly **<1% of parameters**. Why it works: task
adaptation empirically lives in a low-dimensional subspace of weight space; you
don't need a billion degrees of freedom to teach "respond in our house style."

Properties that made LoRA the default:
- Optimizer memory collapses (16 bytes × 1% of params).
- Adapters are tiny files (MBs); one base model + many task adapters, hot-swapped.
- At inference, merge BA into W → **zero added latency**.
- Less catastrophic forgetting (base is frozen).
- Quality: matches full fine-tuning on most task adaptation; can lag on the
  hardest "teach it something really new" cases — raise r and coverage before
  concluding you need full FT.

### QLoRA

Load the frozen base in **4-bit** (NF4 quantization, module 8.4), train LoRA
adapters in bf16 on top. A 70B model fine-tunes on a single 48GB GPU; an 8B on a
free Colab. This single paper (2023) democratized fine-tuning.

## 10.3 The practical recipe

1. **Data is 90% of the outcome.** 500–5,000 *excellent* examples beat 100k
   scraped ones (the LIMA lesson, module 7.5). Format as chat turns matching the
   base model's template exactly — template mismatch is the classic silent killer.
2. Start from the **instruct** model (not base) unless you're replacing the whole
   dialogue behavior.
3. Defaults that mostly just work: LoRA r=16–32 on all linear layers, α=2r, LR
   1e-4–2e-4 (10× lower for full FT), 1–3 epochs, cosine schedule, effective batch
   32–128. Watch eval loss; overfitting shows up fast on small sets.
4. **Hold out an eval set and score the actual task** (module 15), not just loss.
   Also spot-check general ability hasn't regressed (a few MMLU-ish questions).
5. Tooling: HuggingFace `peft` + `trl` (`SFTTrainer`), **Axolotl** or
   **LLaMA-Factory** (config-driven), **Unsloth** (fastest single-GPU). Hosted:
   OpenAI/Together/Fireworks fine-tuning endpoints when you don't want GPUs.

```python
from peft import LoraConfig, get_peft_model
model = get_peft_model(base_model, LoraConfig(
    r=16, lora_alpha=32, target_modules="all-linear",
    lora_dropout=0.05, task_type="CAUSAL_LM"))
model.print_trainable_parameters()   # ~0.5–1% of total
```

## 10.4 Beyond SFT: preference and RL fine-tuning

Everything in module 7 miniaturizes onto your task with the same PEFT tricks:
**DPO** on pairs of (good, bad) outputs when you can rank but not write perfect
answers; **GRPO/RLVR** when you have a programmatic checker (tests pass, SQL
executes, answer matches). The open-source stack (TRL) supports all of them on a
LoRA budget. For most teams the ladder is: prompt → SFT-LoRA → add DPO → (rarely)
RL.

## 10.5 Distillation as a product pattern

The highest-ROI fine-tune in industry: run the expensive frontier model in
production for a while → collect (input, output) pairs on *your* traffic → filter
for quality → SFT a small model on them → route easy traffic to it. You're buying
the big model's judgment at the small model's price for your distribution. (Check
provider ToS on training-on-outputs; open-weight teachers like DeepSeek/Qwen
avoid the issue.)

## Mental models to carry forward

1. **RAG for knowledge, prompting for instructions, fine-tuning for behavior.**
2. LoRA: adaptation lives in a **low-rank subspace** — you're steering, not
   rebuilding.
3. **Data quality > data quantity > hyperparameters**, in that order, by a lot.
4. Your eval set is your steering wheel; without it fine-tuning is astrology.

## Exercises

1. QLoRA-fine-tune an 8B model (Unsloth notebook, free Colab) on 500 examples of
   a persona/format (e.g. answers in your company's support voice, or always-valid
   JSON for one schema). Compare against the prompted base on 30 held-out inputs.
2. Deliberately overfit: 50 examples, 10 epochs. Watch what happens to general
   questions. Now you respect forgetting.
3. Distill: generate 1k (question → answer) pairs from a strong model on one
   narrow topic, fine-tune a 3B model, and measure the gap vs the teacher.
4. Take exercise 1 and add a DPO round using 100 (chosen, rejected) pairs. Did it
   move your eval?

## Further reading

- Hu et al., *LoRA* (2021); Dettmers et al., *QLoRA* (2023).
- Zhou et al., *LIMA: Less Is More for Alignment* (2023).
- HuggingFace TRL/PEFT docs; Unsloth and Axolotl repos.
- Zheng et al., *A Survey of Fine-tuning LLMs* — for the taxonomy beyond LoRA.
