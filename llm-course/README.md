# LLM Zero to Hero — A Complete Course

A self-contained course that takes you from "I know some programming" to understanding
how modern large language models are built, trained, deployed, and used — including
what's happening at the frontier right now (early 2026).

## Who this is for

You can write code (Python helps a lot) and remember some high-school/college math
(matrix multiplication, derivatives, probability). No prior ML experience required —
Part I builds everything from scratch.

## How to use this course

- **Linear path (recommended first pass):** read modules 1–18 in order. Each module
  builds on the previous ones.
- **Practitioner fast path:** if you only want to *use* LLMs well, read 3 → 9 → 11 → 12 → 15,
  then come back for the rest.
- **Researcher fast path:** 1–8, 13, 16, then the papers in module 18.

Every module ends with **exercises** and **further reading**. Do the exercises —
especially the coding ones. The single highest-value activity in this course is
building a tiny GPT yourself (module 3's project).

## Syllabus

### Part I — Foundations
| # | Module | What you'll learn |
|---|--------|-------------------|
| 1 | [Neural networks from scratch](01-foundations-neural-nets.md) | Tensors, gradient descent, backprop, embeddings — the substrate everything else runs on |
| 2 | [Language modeling before transformers](02-language-modeling-before-transformers.md) | N-grams, word2vec, RNNs/LSTMs, seq2seq, and the birth of attention |
| 3 | [The Transformer](03-the-transformer.md) | Self-attention, multi-head attention, the full architecture, and why it won |
| 4 | [Tokenization](04-tokenization.md) | BPE, vocabularies, and why LLMs can't spell "strawberry" |

### Part II — Building LLMs
| # | Module | What you'll learn |
|---|--------|-------------------|
| 5 | [Pretraining & scaling laws](05-pretraining-and-scaling-laws.md) | Data, objectives, compute, Chinchilla, emergent abilities |
| 6 | [Architecture evolution](06-architecture-evolution.md) | GPT-1 → today: RoPE, GQA, MoE, FlashAttention, long context |
| 7 | [Post-training: SFT, RLHF & friends](07-post-training-rlhf.md) | How a raw text predictor becomes a helpful assistant |
| 8 | [Inference & serving](08-inference-and-serving.md) | Sampling, KV cache, quantization, speculative decoding, vLLM |

### Part III — Using LLMs
| # | Module | What you'll learn |
|---|--------|-------------------|
| 9 | [Prompting & in-context learning](09-prompting.md) | Zero/few-shot, chain-of-thought, structured outputs, system prompts |
| 10 | [Fine-tuning in practice](10-fine-tuning.md) | LoRA/QLoRA, PEFT, when to fine-tune vs prompt vs RAG |
| 11 | [Retrieval-augmented generation](11-rag.md) | Embeddings, vector search, chunking, reranking, RAG evals |
| 12 | [Agents & tool use](12-agents-and-tool-use.md) | Function calling, agentic loops, MCP, coding agents, computer use |

### Part IV — The Frontier
| # | Module | What you'll learn |
|---|--------|-------------------|
| 13 | [Reasoning models & test-time compute](13-reasoning-models.md) | o1/o3, R1, extended thinking, the new scaling axis |
| 14 | [Multimodal models](14-multimodal.md) | Vision-language models, audio, image generation basics |
| 15 | [Evaluation](15-evaluation.md) | Benchmarks, their failure modes, and how to eval your own app |
| 16 | [Safety & alignment](16-safety-and-alignment.md) | Jailbreaks, interpretability, alignment techniques, open problems |
| 17 | [The current landscape (early 2026)](17-current-landscape.md) | Who's who, open vs closed weights, the trends that matter |
| 18 | [Projects & resources](18-projects-and-resources.md) | A hands-on project ladder and the canonical papers/courses/videos |

## The one-paragraph version of the whole course

A large language model is a neural network — almost always a **decoder-only
Transformer** — trained on a huge amount of text to do one thing: **predict the next
token**. That simple objective, at sufficient scale of data and compute, produces a
model with broad knowledge and surprising capabilities (Part II). Raw predictors are
then **post-trained** (supervised fine-tuning + reinforcement learning from feedback)
into assistants that follow instructions and refuse harm (module 7). At inference
time we sample from the model token by token, and an entire engineering stack exists
to make that fast and cheap (module 8). On top of the model, applications add
prompting, retrieval over private data, and tools the model can call in a loop —
which is what turns a text predictor into a coding agent or research assistant
(Part III). The current frontier (Part IV) is about **reasoning models** that spend
more compute thinking before answering, multimodality, agents that work for hours
autonomously, and the unresolved science of evaluating and aligning all of it.

## A note on freshness

Parts I–III are stable knowledge. Modules 13–17 describe a fast-moving field as of
**early 2026**; expect details (model names, benchmark numbers) to age quickly, and
treat the *concepts* as the durable content.
