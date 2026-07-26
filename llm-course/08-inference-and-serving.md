# Module 8 — Inference & Serving

Training happens once; inference happens billions of times a day. This module is
how a trained model actually produces text, and the engineering stack that makes
it fast and affordable — the physics behind every API price and latency number.

## 8.1 Autoregressive generation

```
loop:
  logits = model(all tokens so far)[-1]   # last position's logits
  next   = sample(logits)
  append(next)
until stop token or length limit
```

One full forward pass **per token generated**. A 500-token answer = 500 passes.
That loop's cost structure drives everything else in this module.

## 8.2 Sampling: from logits to a token

- **Greedy** (argmax): deterministic-ish, repetitive; degenerates in loops.
- **Temperature** τ: divide logits by τ before softmax. τ→0 sharpens toward greedy
  (factual/code); τ=1 samples the model's true distribution; τ>1 flattens
  (brainstorming). It rescales, it doesn't add "creativity."
- **Top-k**: keep only the k highest-probability tokens, renormalize.
- **Top-p (nucleus)**: keep the smallest set whose cumulative probability ≥ p
  (adaptive: narrow when confident, wide when uncertain). The common default
  (τ≈0.7–1.0, p≈0.9–0.95).
- **min-p**, repetition penalties, logit bias — situational knobs.
- **Structured/constrained decoding**: mask logits so output must match a JSON
  schema or grammar — zero invalid outputs by construction. This (not prompting)
  is how "JSON mode"/structured outputs features work.

Non-determinism footnote: even at τ=0, floating-point reduction order and batching
can flip near-ties, so API outputs aren't perfectly reproducible.

## 8.3 The KV cache

Naively, generating token t re-encodes all t−1 previous tokens: O(T²) redundant
work. The fix: **cache every layer's keys and values** for past tokens; each new
token computes only its own Q/K/V and attends against the cache. This splits
inference into two phases with totally different characters:

- **Prefill** (process the prompt): all prompt tokens in parallel — compute-bound,
  big matmuls, GPUs happy. Determines **time-to-first-token**.
- **Decode** (generate): one token at a time — **memory-bandwidth-bound**. Each
  step must stream all weights (and the growing cache) from GPU memory to compute
  a tiny matmul. Determines **tokens/second**.

This is why prompt tokens are priced ~3–10× cheaper than output tokens, and why
**prompt caching** (reusing the KV cache across requests sharing a prefix — e.g. a
long system prompt) gives ~10× cost cuts on the cached portion.

Cache size is the serving constraint (recall module 6): it grows linearly with
context and batch — at long context it can exceed the weights. GQA/MLA exist to
shrink it.

## 8.4 Quantization

Weights don't need 16 bits at inference. Rounding to 8-bit (near-lossless) or
4-bit (small, usually acceptable loss) shrinks memory — and since decode is
bandwidth-bound, **smaller weights also mean faster tokens**.

- Formats/methods you'll meet: GPTQ, AWQ (activation-aware), GGUF (llama.cpp's
  format for CPU/Mac local inference), bitsandbytes NF4 (used in QLoRA,
  module 10), fp8 (native on H100+, increasingly used even in training).
- Rule of thumb: **a 4-bit-quantized bigger model usually beats a full-precision
  smaller model** at equal memory.
- This is the entire "run Llama on your laptop" ecosystem: 70B × 4 bits ≈ 35GB —
  a high-end MacBook runs it.

## 8.5 Making decode faster and cheaper

- **Continuous batching** (the vLLM-era insight): decode is bandwidth-bound, so
  processing 50 sequences' next-tokens costs barely more than 1 — the weights are
  streamed once either way. Slot new requests into the batch the moment any
  sequence finishes (no waiting for the slowest). 10–20× throughput. **PagedAttention**
  (vLLM) manages the KV cache in non-contiguous pages, virtual-memory-style,
  eliminating fragmentation and enabling cache sharing.
- **Speculative decoding**: a small *draft* model proposes k tokens; the big model
  verifies all k in **one** parallel pass, accepting the agreeing prefix. A
  rejection-sampling trick keeps the output distribution *exactly* the target
  model's — pure speedup (2–3×), no quality trade. Variants (Medusa, EAGLE) draft
  with extra heads instead of a separate model.
- **Distillation**: train a small model on a big model's outputs — how every lab's
  "mini/flash/haiku" tier is made.
- Serving stacks to know: **vLLM** and **SGLang** (open standard), TensorRT-LLM
  (NVIDIA), llama.cpp / **Ollama** / MLX (local).

## 8.6 The economics in one example

70B dense model, bf16 (140GB → 2×H100). Decode at batch 1 is limited by
bandwidth: ~3.3TB/s × 2 GPUs / 140GB ≈ ~45 tokens/s *theoretical*. Batch 50 users:
still bandwidth-limited on the same weight stream → ~45 tok/s **each**, ~2000
tok/s aggregate — same hardware, ~50× revenue. Now stack: 4-bit weights (×3-4
bandwidth win), GQA (cache fits more users), MoE (fewer active params), prompt
caching, speculative decoding. Multiply those factors and you get the 100–1000×
fall in per-token prices from 2022 → 2026. None of it is magic; all of it is this
module.

## Mental models to carry forward

1. **Prefill is compute-bound; decode is bandwidth-bound** — the one fact that
   explains pricing, batching, and quantization speedups.
2. **The KV cache is the real resource being sold** as "context length."
3. **Batching is nearly free throughput**; speculative decoding is free latency;
   quantization is free-ish memory. Modern serving stacks all three.
4. Temperature/top-p shape the *distribution*; determinism is a myth at τ=0
   anyway.

## Exercises

1. Run a 7–8B model locally with Ollama. Measure tokens/sec; compute implied
   memory bandwidth (params × bytes × tok/s) and compare to your hardware's spec.
   You'll find decode is bandwidth-bound, as promised.
2. Same model at q4 vs q8: measure speed and eyeball quality on 5 prompts.
3. Sample the same creative prompt at τ = 0, 0.7, 1.5 and the same math problem at
   each. Write down when temperature helps and when it hurts.
4. Estimate KV-cache bytes for one 128k-token conversation on an 80-layer GQA
   model (8 KV heads × 128 dims, fp16), then compute how many such users fit in
   80GB alongside 4-bit weights of a 70B model.

## Further reading

- Kwon et al., *Efficient Memory Management for LLM Serving with PagedAttention*
  (vLLM, 2023).
- Leviathan et al., *Fast Inference from Transformers via Speculative Decoding*
  (2023).
- Frantar et al., *GPTQ* (2022); Lin et al., *AWQ* (2023).
- kipply's blog, *Transformer Inference Arithmetic* — the napkin-math bible.
