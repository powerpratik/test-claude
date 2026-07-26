# Module 18 — Projects & Resources

Reading builds a map; building builds the territory. This module is the project
ladder (do them in order — each cashes in specific modules) and the canonical
resource list.

## 18.1 The project ladder

### Level 0 — Foundations (modules 1–2)
**Micrograd + makemore.** Follow Karpathy's videos; type every line. Backprop,
embeddings, and a neural bigram LM from scratch.
*Done when:* you can explain, on a whiteboard, how the gradient reaches an
embedding row.

### Level 1 — Build a GPT (modules 3–4)
**nanoGPT on Shakespeare**, then build the BPE tokenizer yourself. Add RoPE and
RMSNorm (module 6) as stretch goals and verify loss parity.
*Done when:* your model generates passable fake Shakespeare and you can name
every tensor shape in the forward pass from memory.

### Level 2 — Touch real training (modules 5–7, 10)
Reproduce **GPT-2 124M** pretraining (Karpathy's llm.c / nanoGPT recipe; ~$100
of cloud GPU or a long weekend on a 3090) — feel tokens/sec, loss curves, LR
schedules. Then **QLoRA fine-tune** an 8B instruct model on 500 examples of a
persona/format, and run a small **DPO** round. Compare base/instruct/yours.
*Done when:* you've watched a loss spike and know whether to panic (module 5.5),
and your fine-tune beats prompting on a 30-case golden set you built.

### Level 3 — Build the application layer (modules 8–9, 11, 15)
**RAG over your own documents**, no frameworks first (module 11 exercise 1),
then: hybrid search + reranker, structured outputs, and a promptfoo/CI eval
suite with retrieval and groundedness metrics. Serve a quantized local model
with vLLM/Ollama for the generation step and measure tokens/sec against the
module-8 napkin math.
*Done when:* a prompt change that breaks a case fails CI before it ships.

### Level 4 — Build an agent (modules 12–13)
The raw loop + 3 tools (search, code-exec sandbox, file I/O). Add: error
recovery, a context-compaction strategy, injection defenses, and an eval
harness of 20 tasks with programmatic success checks. Compare a reasoning vs
non-reasoning model as the driver at equal dollar budget (module 13 exercise 1
logic).
*Done when:* it completes a multi-step task you'd genuinely have done by hand —
and safely refuses your planted injection.

### Level 5 — Pick a specialization
- **Systems**: contribute to vLLM/SGLang; implement speculative decoding or
  paged KV cache yourself.
- **Post-training**: replicate a small R1-style RLVR run (TRL + GRPO on GSM8K
  with an 1.5–3B model — public recipes exist).
- **Interpretability**: train an SAE on a small model (Neuronpedia/SAELens
  ecosystem); find and steer one feature.
- **Product**: ship an LLM feature to real users and run the 15.5 loop for a
  month; nothing teaches faster than production traffic.

## 18.2 Canonical resources

### Video / courses
- **Karpathy, *Neural Networks: Zero to Hero*** — micrograd → makemore → GPT →
  tokenizer → GPT-2 reproduction. The single best resource in the field, and
  the spine of Levels 0–2.
- Karpathy's *Intro to LLMs* (1h) and *Deep Dive into LLMs like ChatGPT* (3.5h)
  — the big-picture talks; send them to colleagues.
- Stanford **CS224n** (NLP with deep learning) and **CS336** (Language Modeling
  from Scratch — lectures public; the academic superset of this course).
- 3Blue1Brown's neural-network and Transformer visualizations — for intuition.
- HuggingFace **LLM Course** (hf.co/learn) — practical, library-oriented.

### The ~20 papers that cover the intellectual history
Module 2–3 era: *Attention Is All You Need*; GPT-1/2/3 papers; BERT; T5.
Scaling: *Scaling Laws* (Kaplan), *Chinchilla*, *Emergent Abilities*, the
Llama reports. Post-training: *InstructGPT*, *Constitutional AI*, *DPO*,
*LIMA*, *Tülu 3*. Systems: *FlashAttention*, *vLLM/PagedAttention*, *LoRA*,
*QLoRA*, *GPTQ*. Frontier: *ReAct*, *Let's Verify Step by Step*, o1 system
card, *DeepSeek-V3* and *R1*, *Scaling Monosemanticity*. (Each module's
"further reading" gives the rest.)

### Books
- *Build a Large Language Model (From Scratch)* — Sebastian Raschka (the book
  version of Levels 1–2).
- *Hands-On Large Language Models* — Alammar & Grootendorst (visual,
  applied).
- *AI Engineering* — Chip Huyen (the application layer, Parts III–IV of this
  course in book form).
- *Deep Learning* — Goodfellow et al. (foundations reference).

### Staying current (repeat of 17.6, because it's the meta-skill)
Lab blogs & system cards > aggregators (Willison, Interconnects, Zvi, Latent
Space) > social media. Leaderboards with module-15 skepticism. Hands on the
models weekly.

## 18.3 Closing advice

1. **Build before (and while) you read.** One nanoGPT is worth fifty blog
   posts; the ladder above is the course.
2. **Keep evals under everything you ship** (module 15) — it's the one
   engineering habit that separates professionals in this field.
3. **Anchor on the invariants**: next-token prediction, attention, scaling
   dials, Goodhart, verification. Names and benchmarks churn quarterly; the
   invariants have held for years and are what this course actually taught.
4. **Recalibrate quarterly** — module 17 was obsolete the day it was written;
   your module-1-through-16 foundations are how you'll read the next model
   card in ten minutes instead of ten hours.

You're caught up. Go build something.
