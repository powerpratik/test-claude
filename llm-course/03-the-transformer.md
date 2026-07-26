# Module 3 — The Transformer

*"Attention Is All You Need"* (Vaswani et al., 2017) is the most consequential ML
paper of the century so far. This module dissects the architecture that every
frontier model still uses, nine years later.

## 3.1 The big idea

Module 2 ended with attention bolted onto RNNs. The Transformer's move: **delete the
RNN entirely**. Let every token attend directly to every other token. Consequences:

- **Path length 1** between any two positions — long-range dependencies are as easy
  as short-range ones (RNNs needed n sequential steps).
- **Total parallelism in training** — all positions computed simultaneously as one
  big matrix multiply. Perfect fit for GPUs. This, as much as modeling quality, is
  why Transformers won: they made it *economical* to train on internet-scale data.

## 3.2 Self-attention, precisely

For each token we compute three vectors via learned linear projections:

- **Query (Q)** — "what am I looking for?"
- **Key (K)** — "what do I contain, for matching purposes?"
- **Value (V)** — "what do I contribute if attended to?"

```
Attention(Q, K, V) = softmax(QKᵀ / √d_k) · V
```

Walk through it for one token:
1. Dot its query against every token's key → a relevance score per token.
2. Divide by √d_k (keeps scores in a range where softmax has healthy gradients).
3. Softmax → attention weights (positive, sum to 1).
4. Output = weighted average of all tokens' values.

Each token's output is a **mixture of information from the whole sequence, weighted
by learned relevance**. A token for "it" can pull in the noun it refers to; a verb
can pull in its subject. Note the direct lineage from module 2.5 — this is the same
soft lookup, applied within a single sequence ("self"-attention).

**Causal masking.** For language modeling, token *t* must not see tokens *t+1…n*
(that would be cheating — the answer leaks). We set those attention scores to −∞
before the softmax. This single mask is what makes a Transformer a *generative* LM,
and it has a huge training bonus: one forward pass over an n-token text yields **n
training examples at once** (each position predicts its next token).

## 3.3 Multi-head attention

Instead of one attention over 768-dim vectors, split into e.g. 12 **heads** of 64
dims, each with its own Q/K/V projections, attending independently; concatenate
outputs and project. Different heads learn different relations — syntax, coreference,
positional patterns, "look at the previous token," etc. It's cheap (same total FLOPs)
and much more expressive than a single head.

## 3.4 The full block

A Transformer is a stack of identical **blocks** (GPT-3: 96 of them). Each block:

```
x = x + MHA(LayerNorm(x))     # attention: tokens talk to each other
x = x + MLP(LayerNorm(x))     # feed-forward: each token thinks alone
```

Piece by piece:

- **MLP / feed-forward network**: two linear layers with a nonlinearity, applied to
  each position independently, expanding to ~4× hidden dim and back. Roughly 2/3 of
  a model's parameters live here; interpretability work suggests much of the model's
  *factual knowledge* is stored in these layers, while attention does the *routing*.
- **Residual connections** (`x + …`): the input flows around every sublayer. This is
  the gradient highway that lets 100-layer models train (recall vanishing gradients,
  module 2.4). Mental model: a **residual stream** that every layer reads from and
  writes small updates into.
- **LayerNorm**: normalizes each token's vector to stable scale. Modern models apply
  it *before* each sublayer ("pre-norm" — more stable than the original post-norm)
  and often use the simpler **RMSNorm**.

## 3.5 Position information

Attention is permutation-invariant — shuffle the tokens and the outputs shuffle
identically. Word order must be injected explicitly:

- **Original (2017)**: add sinusoidal *positional encodings* to input embeddings.
- **GPT-1/2/3**: learned absolute position embeddings.
- **Modern standard: RoPE** (Rotary Position Embeddings) — rotate Q and K vectors by
  angles proportional to position, so attention scores depend on *relative* offsets.
  Better length generalization; the basis of long-context tricks (module 6).

## 3.6 The three architectural families

| Family | Attention pattern | Objective | Examples | Status |
|--------|------------------|-----------|----------|--------|
| **Encoder-only** | bidirectional | masked-word fill-in (MLM) | BERT, RoBERTa | embeddings/classification; still used in RAG retrievers |
| **Encoder–decoder** | bidirectional + causal | span corruption / seq2seq | T5, original Transformer | translation, some research |
| **Decoder-only** | causal | next-token prediction | **GPT-x, Claude, Llama, Gemini, DeepSeek — everything frontier** | won |

Why decoder-only won: one simple objective, every token supervises, generation is
native, and it scales cleanly. When people say "LLM" today they mean a decoder-only
Transformer.

## 3.7 End-to-end shape walkthrough

For batch B, sequence length T, hidden size C, vocab V:

```
tokens  (B, T)            integers from the tokenizer (module 4)
  → embedding lookup       (B, T, C)
  → N × transformer block  (B, T, C)      # shape never changes
  → final LayerNorm        (B, T, C)
  → LM head (Linear C→V)   (B, T, V)      # logits over vocabulary
  → softmax + cross-entropy against tokens shifted by one
```

Training: loss at every position in parallel. Inference: take logits at the *last*
position, sample the next token, append, repeat (module 8 makes this fast).

## 3.8 Where the compute goes

- Parameter count ≈ `12 × n_layers × C²` (attention ~4C², MLP ~8C² per layer), plus
  the embedding table.
- Per-token FLOPs ≈ **2 × parameters** (forward); training ≈ 6 × params per token
  (forward + backward). You'll use this constantly in module 5's scaling laws.
- Attention's QKᵀ is **O(T²)** in sequence length — the cost that long-context work
  (module 6) fights against.

## Mental models to carry forward

1. **Attention = differentiable soft lookup**; multi-head = many lookups in parallel.
2. **Residual stream**: layers read and write a shared workspace; attention moves
   information *between* positions, MLPs process *within* a position.
3. **The causal mask is the language model** — everything else is capacity.
4. The Transformer won on **parallelism economics** as much as on accuracy.

## Exercises (the most important ones in the course)

1. **Build nanoGPT.** Follow Karpathy's *"Let's build GPT: from scratch, in code"*
   (2h video). Type every line yourself; train on Shakespeare; sample. Nothing else
   in this course teaches as much per hour.
2. In your implementation, print the attention-weight matrix of one head on a short
   sentence. Find a head that attends to the previous token.
3. Remove the causal mask and retrain. Observe the loss crash to ~0 and explain
   exactly why the model is cheating.
4. Compute by hand: parameters of a model with 12 layers, C=768, V=50257. Compare
   with GPT-2's published 124M.

## Further reading

- Vaswani et al., *Attention Is All You Need* (2017) — read for real.
- Jay Alammar, *The Illustrated Transformer* — the classic visual walkthrough.
- Karpathy, *nanoGPT* repo and the *Zero to Hero* GPT videos.
- Anthropic's *A Mathematical Framework for Transformer Circuits* — the residual
  stream view, once you're comfortable.
