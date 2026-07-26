# Module 6 — Architecture Evolution: GPT-1 to Today

The 2017 Transformer is still the blueprint, but a decade of refinements separates
it from a 2026 frontier model. This module tours the changes that stuck, and why.

## 6.1 The GPT lineage (capability history in one table)

| Model | Year | Params | Context | The lesson it taught |
|-------|------|--------|---------|----------------------|
| GPT-1 | 2018 | 117M | 512 | Generative pretraining + fine-tuning beats task-specific models |
| GPT-2 | 2019 | 1.5B | 1k | Zero-shot task behavior appears; "too dangerous" debate |
| GPT-3 | 2020 | 175B | 2k | **In-context learning**; scale is a product strategy |
| InstructGPT/ChatGPT | 2022 | — | 4k | Post-training makes it usable (module 7); fastest-adopted product ever |
| GPT-4 | 2023 | undisclosed (MoE, reportedly) | 8k–128k | Multimodal input; professional-exam-level reasoning |
| Llama 1–3 | 2023–24 | 7B–405B | up to 128k | Open weights catch up; overtraining small models works |
| o1 / R1 | 2024–25 | — | — | Test-time reasoning as a new scaling axis (module 13) |
| GPT-5 / Claude 4.x / Gemini 2–3 / DeepSeek V3.x | 2024–25 | — | 128k–1M+ | Agents, long context, efficiency; MoE everywhere |

## 6.2 The modern recipe (what changed inside the block)

A 2026 open-weights model (Llama/Qwen/DeepSeek-style) differs from GPT-2 in a
handful of now-standard swaps:

- **Pre-norm with RMSNorm** instead of post-norm LayerNorm — plain stability win.
- **SwiGLU / GeGLU MLPs** instead of ReLU/GELU MLPs — gated feed-forwards, a small
  but consistent quality gain (from the "GLU Variants Improve Transformer" line).
- **RoPE** (rotary position embeddings) instead of learned absolute positions —
  relative offsets, better extrapolation, and the lever for context extension
  (6.4).
- **No biases** in most linear layers; simpler and no worse.
- **Grouped-Query Attention (GQA)**: many query heads share a few K/V heads
  (e.g. 32 Q heads, 8 KV heads). Near-zero quality loss, 4–8× smaller KV cache —
  which is the real constraint on serving long contexts (module 8). Successor to
  the more aggressive multi-query attention (MQA). DeepSeek's **MLA**
  (multi-head latent attention) compresses the KV cache further via low-rank
  projection.

None of these is individually dramatic. Their sum, plus far better data and
training recipes, is why a 2025 8B model beats 2020's 175B GPT-3.

## 6.3 Mixture of Experts (MoE)

The biggest structural change at the frontier. Replace each dense MLP with many
"expert" MLPs plus a learned **router** that sends each token to its top-k (often
k=1–2 of 8–256) experts:

- **Decouples parameters from FLOPs**: a model can have 600B+ total parameters but
  activate only ~30B per token — big-model knowledge at small-model cost.
- Examples: Mixtral 8×7B (2023, the open proof of concept), GPT-4 (reportedly),
  DeepSeek V3 (671B total / 37B active — fine-grained experts + shared expert),
  Llama 4, Qwen3-MoE, and most frontier systems since.
- Costs: all parameters must still sit in memory; routing adds load-balancing
  headaches (auxiliary losses or bias tricks to keep experts evenly used);
  fine-tuning is touchier.
- Mental model: **conditional computation** — not every token needs every neuron.
  The "experts" are not human-legible specialists (they're not "the French
  expert"); routing patterns are mostly syntactic/statistical.

## 6.4 Long context

From 2k (GPT-3) to 128k standard, with 1M+ in production (Gemini) — a ~500×
expansion in five years. The obstacles: attention is O(T²) compute, and the KV
cache is O(T) memory *per layer per head* (at 128k tokens the cache can dwarf the
weights). What made it work:

- **FlashAttention** (2022): not an approximation — an *exact* attention algorithm
  reorganized to be IO-aware, tiling the computation so the T×T matrix never
  materializes in slow GPU memory. Made 100k-token attention affordable and is
  universal now.
- **RoPE scaling** (position interpolation, NTK-aware scaling, YaRN): train at
  moderate length, then stretch rotary frequencies and lightly fine-tune to reach
  10–100× longer contexts.
- **GQA/MLA** (above) to shrink the cache; **sliding-window / hybrid local-global
  attention** in some models (Mistral, Gemma) to bound cost.
- Long-context **quality** is its own battle: models can attend to everything and
  still ignore the middle ("lost in the middle"). Needle-in-a-haystack tests are
  necessary-but-not-sufficient (module 15).

## 6.5 Beyond the Transformer? (state of play, early 2026)

- **State-space models (Mamba et al.)**: recurrent-style models with linear-time
  inference and constant memory — attacking exactly the O(T²)/KV-cache weaknesses.
  Pure SSMs lag on recall-heavy tasks (copying, in-context lookup).
- **Hybrids** (attention layers interleaved with SSM/linear-attention layers —
  Jamba, Zamba, various lab experiments) are credible and shipping in places.
- **Diffusion LMs**: generate text by iterative denoising rather than
  left-to-right; fast parallel decoding demos exist (Gemini Diffusion research),
  not yet frontier-standard.
- Honest summary: **attention remains the frontier default**; alternatives win
  niches (edge, extreme length) and keep the pressure on.

## 6.6 How to read a model card like an engineer

When a new model drops, the spec sheet decodes with this module:

> "236B-A22B MoE, 128 experts top-8 + 1 shared, GQA 64/8, RoPE θ=1e7 with YaRN to
> 256k, RMSNorm, SwiGLU, trained on 18T tokens"

You now know: total vs active params (cost per token), the KV-cache ratio (serving
memory), the context-extension method, and — via 6ND — the training FLOPs. That's
the whole game.

## Mental models to carry forward

1. Modern architecture = **GPT-2 + a dozen compounding 1–5% wins** (RMSNorm, RoPE,
   SwiGLU, GQA) — recipes, not revolutions.
2. **MoE decouples knowledge (params) from cost (active params).**
3. Long context was won by **exact-but-IO-smart attention + positional stretching
   + cache compression**, not by approximating attention.
4. The KV cache, not the weights, is the scarce resource at inference — this
   drives GQA/MLA/MoE and sets up module 8.

## Exercises

1. For Mixtral 8×7B (46.7B total, 12.9B active): compute FLOPs/token vs a dense
   47B and vs a dense 13B. Where does it sit on quality vs cost, and why?
2. Compute KV-cache size at 128k tokens for a 70B model with full MHA (64 KV
   heads) vs GQA (8 KV heads), fp16, 80 layers, head_dim 128. Compare to the
   weight memory. (`2 × layers × kv_heads × head_dim × T × 2 bytes`)
3. Read the DeepSeek-V3 paper's architecture section and list every deviation from
   vanilla Transformer, mapping each to a subsection of this module.
4. In your nanoGPT from module 3, swap learned positions for RoPE and LayerNorm
   for RMSNorm; confirm similar or better loss.

## Further reading

- Touvron et al., the *Llama* papers; the *DeepSeek-V2/V3* reports (MLA, MoE).
- Dao et al., *FlashAttention* (2022).
- Su et al., *RoFormer* (RoPE, 2021); Peng et al., *YaRN* (2023).
- Fedus et al., *Switch Transformers* (2021) — MoE fundamentals.
- Gu & Dao, *Mamba* (2023).
